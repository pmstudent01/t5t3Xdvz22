# Vehicle Service App

A small Python application that implements the **Vehicle Service** API by consuming the
auto-generated `vehicle_service_collection_sdk` (located in
`postman/sdks/Collections SDKs/vehicle/python`).

It exposes all five operations from the **Vehicle Service Collection** as a command-line tool:

| Command    | HTTP            | SDK method            |
| ---------- | --------------- | --------------------- |
| `list`     | `GET /vehicles`       | `get_all_vehicles`     |
| `create`   | `POST /vehicles`      | `create_a_vehicle`     |
| `get`      | `GET /vehicles/:id`   | `retrieve_a_vehicle`   |
| `update`   | `PATCH /vehicles/:id` | `update_a_collection`  |
| `delete`   | `DELETE /vehicles/:id`| `delete_a_vehicle`     |

## Setup

```bash
# From the repo root
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate

# Install the generated SDK (editable) + this app's deps
pip install -e "postman/sdks/Collections SDKs/vehicle/python"
pip install -r app/requirements.txt
```

## Configuration

The generated SDK ships with a placeholder base URL (`https://baseUrl`), so you must
supply the real service URL. Configuration is read from environment variables:

| Variable              | Required | Description                                        |
| --------------------- | -------- | -------------------------------------------------- |
| `VEHICLE_BASE_URL`    | yes      | Base URL of the running Vehicle Service, e.g. `http://localhost:3000` |
| `VEHICLE_API_KEY`     | no       | API key, if the service requires one               |
| `VEHICLE_TIMEOUT`     | no       | Request timeout in seconds (default `10`)          |

You can also pass `--base-url` / `--api-key` on the command line to override them.

## Usage

```bash
# List all vehicles
python -m app.main list

# Create a vehicle
python -m app.main create \
  --nick-name "The Lisa Marie" --vin 4M2DV11W4RDJ53329 \
  --make Mercury --model Villager --year 1994 --miles 159864

# Retrieve one
python -m app.main get 1

# Update one (only pass the fields you want to change)
python -m app.main update 1 --miles 159999

# Delete one
python -m app.main delete 1
```

All commands print the JSON response (or a status message) to stdout.
