"""Factory + service layer around the generated Vehicle Service SDK.

This module isolates the rest of the app from the SDK's exact construction
details. If the generated SDK changes, this is the only file that needs to adapt.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Optional

from vehicle_service_collection_sdk import VehicleServiceCollectionSdk
from vehicle_service_collection_sdk.models import (
    CreateAVehicleRequest,
    UpdateACollectionRequest,
)


@dataclass
class Settings:
    """Runtime configuration, resolved from CLI args then environment variables."""

    base_url: str
    api_key: Optional[str] = None
    timeout: float = 10.0

    @classmethod
    def resolve(
        cls,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> "Settings":
        resolved_base_url = base_url or os.getenv("VEHICLE_BASE_URL")
        if not resolved_base_url:
            raise ValueError(
                "No base URL configured. Set VEHICLE_BASE_URL or pass --base-url. "
                "The generated SDK ships with a placeholder URL that is not a real host."
            )
        resolved_timeout = (
            timeout
            if timeout is not None
            else float(os.getenv("VEHICLE_TIMEOUT", "10"))
        )
        return cls(
            base_url=resolved_base_url,
            api_key=api_key or os.getenv("VEHICLE_API_KEY"),
            timeout=resolved_timeout,
        )


class VehicleService:
    """High-level, intention-revealing operations for the Vehicle Service API."""

    def __init__(self, settings: Settings):
        self._settings = settings
        # The SDK accepts api_key=None gracefully when the service needs no auth.
        self._sdk = VehicleServiceCollectionSdk(
            api_key=settings.api_key,
            base_url=settings.base_url,
            timeout=settings.timeout,
        )

    @property
    def _api(self):
        return self._sdk.vehicle_service_collection_sdk

    def list_vehicles(self) -> Any:
        return self._api.get_all_vehicles()

    def get_vehicle(self, vehicle_id: str) -> Any:
        return self._api.retrieve_a_vehicle(id_=str(vehicle_id))

    def create_vehicle(
        self,
        *,
        nick_name: Optional[str] = None,
        vin: Optional[str] = None,
        make: Optional[str] = None,
        model: Optional[str] = None,
        year: Optional[str] = None,
        miles: Optional[int] = None,
    ) -> Any:
        request_body = CreateAVehicleRequest(
            nick_name=nick_name,
            vin=vin,
            make=make,
            model=model,
            year=year,
            miles=miles,
        )
        return self._api.create_a_vehicle(request_body=request_body)

    def update_vehicle(
        self,
        vehicle_id: str,
        *,
        nick_name: Optional[str] = None,
        vin: Optional[str] = None,
        make: Optional[str] = None,
        model: Optional[str] = None,
        year: Optional[str] = None,
        miles: Optional[int] = None,
    ) -> Any:
        request_body = UpdateACollectionRequest(
            nick_name=nick_name,
            vin=vin,
            make=make,
            model=model,
            year=year,
            miles=miles,
        )
        return self._api.update_a_collection(
            request_body=request_body, id_=str(vehicle_id)
        )

    def delete_vehicle(self, vehicle_id: str) -> Any:
        return self._api.delete_a_vehicle(id_=str(vehicle_id))
