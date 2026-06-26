from __future__ import annotations

import httpx

VALID_UNITS = {"W", "kW", "Wh", "kWh"}


def _headers(token: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


def fetch_states(ha_url: str, token: str) -> list[dict]:
    """Fetch all entity states from Home Assistant."""
    url = f"{ha_url.rstrip('/')}/api/states"
    try:
        resp = httpx.get(url, headers=_headers(token), timeout=10.0)
        resp.raise_for_status()
    except httpx.ConnectError as exc:
        raise ConnectionError(
            f"Cannot reach Home Assistant at {ha_url}: {exc}"
        ) from exc
    return resp.json()


def fetch_area_registry(ha_url: str, token: str) -> list[dict]:
    """Fetch the area registry from Home Assistant."""
    url = f"{ha_url.rstrip('/')}/api/config/area_registry"
    try:
        resp = httpx.get(url, headers=_headers(token), timeout=10.0)
        resp.raise_for_status()
    except httpx.ConnectError as exc:
        raise ConnectionError(
            f"Cannot reach Home Assistant at {ha_url}: {exc}"
        ) from exc
    return resp.json()


def filter_energy_entities(entities: list[dict]) -> list[dict]:
    """Keep only entities with numeric state and energy/power units."""
    result = []
    for entity in entities:
        attrs = entity.get("attributes", {})
        unit = attrs.get("unit_of_measurement")
        if unit not in VALID_UNITS:
            continue
        try:
            float(entity["state"])
        except (ValueError, TypeError):
            continue
        result.append(entity)
    return result


def fetch_entity_area_map(ha_url: str, token: str) -> dict[str, str]:
    """Build a mapping of entity_id to area name from HA device/area registries."""
    url = f"{ha_url.rstrip('/')}/api/config/device_registry"
    try:
        resp = httpx.get(url, headers=_headers(token), timeout=10.0)
        resp.raise_for_status()
    except httpx.ConnectError as exc:
        raise ConnectionError(
            f"Cannot reach Home Assistant at {ha_url}: {exc}"
        ) from exc
    except httpx.HTTPStatusError:
        return {}

    devices = resp.json()
    areas = fetch_area_registry(ha_url, token)
    area_id_to_name = {a["area_id"]: a["name"] for a in areas}

    entity_area = {}
    for device in devices:
        area_id = device.get("area_id")
        if not area_id:
            continue
        area_name = area_id_to_name.get(area_id)
        if not area_name:
            continue
        for entity_id in device.get("entities", []):
            entity_area[entity_id] = area_name

    return entity_area
