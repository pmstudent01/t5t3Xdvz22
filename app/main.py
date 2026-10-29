"""Command-line entrypoint for the Vehicle Service app.

Run with:  python -m app.main <command> [options]
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from .client import Settings, VehicleService


def _print_result(result: Any) -> None:
    """Pretty-print whatever the SDK returned (dict/list/str/None)."""
    if result is None or result == "":
        print("OK (no content returned)")
        return
    try:
        print(json.dumps(result, indent=2, default=str))
    except (TypeError, ValueError):
        print(result)


def _build_service(args: argparse.Namespace) -> VehicleService:
    settings = Settings.resolve(
        base_url=getattr(args, "base_url", None),
        api_key=getattr(args, "api_key", None),
        timeout=getattr(args, "timeout", None),
    )
    return VehicleService(settings)


# --- command handlers -------------------------------------------------------


def cmd_list(args: argparse.Namespace) -> None:
    _print_result(_build_service(args).list_vehicles())


def cmd_get(args: argparse.Namespace) -> None:
    _print_result(_build_service(args).get_vehicle(args.id))


def cmd_create(args: argparse.Namespace) -> None:
    _print_result(
        _build_service(args).create_vehicle(
            nick_name=args.nick_name,
            vin=args.vin,
            make=args.make,
            model=args.model,
            year=args.year,
            miles=args.miles,
        )
    )


def cmd_update(args: argparse.Namespace) -> None:
    _print_result(
        _build_service(args).update_vehicle(
            args.id,
            nick_name=args.nick_name,
            vin=args.vin,
            make=args.make,
            model=args.model,
            year=args.year,
            miles=args.miles,
        )
    )


def cmd_delete(args: argparse.Namespace) -> None:
    _build_service(args).delete_vehicle(args.id)
    print(f"Deleted vehicle {args.id}")


# --- argument parsing -------------------------------------------------------


def _add_global_opts(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--base-url",
        dest="base_url",
        help="Base URL of the Vehicle Service (overrides VEHICLE_BASE_URL).",
    )
    parser.add_argument(
        "--api-key",
        dest="api_key",
        help="API key, if required (overrides VEHICLE_API_KEY).",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=None,
        help="Request timeout in seconds (overrides VEHICLE_TIMEOUT, default 10).",
    )


def _add_vehicle_fields(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--nick-name", dest="nick_name", help="Vehicle nickname.")
    parser.add_argument("--vin", help="Vehicle identification number.")
    parser.add_argument("--make", help="Vehicle make.")
    parser.add_argument("--model", help="Vehicle model.")
    parser.add_argument("--year", help="Vehicle year.")
    parser.add_argument("--miles", type=int, help="Odometer reading.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="vehicle-app",
        description="CLI for the Vehicle Service API (built on the generated SDK).",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="List all vehicles.")
    _add_global_opts(p_list)
    p_list.set_defaults(func=cmd_list)

    p_get = sub.add_parser("get", help="Retrieve a single vehicle by id.")
    p_get.add_argument("id", help="Vehicle id.")
    _add_global_opts(p_get)
    p_get.set_defaults(func=cmd_get)

    p_create = sub.add_parser("create", help="Create a new vehicle.")
    _add_vehicle_fields(p_create)
    _add_global_opts(p_create)
    p_create.set_defaults(func=cmd_create)

    p_update = sub.add_parser("update", help="Update an existing vehicle.")
    p_update.add_argument("id", help="Vehicle id.")
    _add_vehicle_fields(p_update)
    _add_global_opts(p_update)
    p_update.set_defaults(func=cmd_update)

    p_delete = sub.add_parser("delete", help="Delete a vehicle by id.")
    p_delete.add_argument("id", help="Vehicle id.")
    _add_global_opts(p_delete)
    p_delete.set_defaults(func=cmd_delete)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        args.func(args)
    except ValueError as exc:
        # Configuration problems (e.g. missing base URL).
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # noqa: BLE001 - surface SDK/request errors cleanly
        print(f"Request failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
