#!/usr/bin/env python3
"""Shared validation and query helpers for verified motherboard capabilities.

The bundled catalog records only exact-model facts confirmed from a vendor
specification or manual.  Missing fields mean "not yet verified"; they must
never be treated as a verified negative.
"""

from __future__ import annotations

from typing import Any


PCIE_WIDTHS = ("x1", "x4", "x8", "x16")
PCIE_SOURCES = {"cpu", "chipset"}
USB4_STATUSES = {"native", "via_thunderbolt", "none_verified"}
THUNDERBOLT_STATUSES = {"native", "header_only", "none_verified"}
USB4_SPEEDS_GBPS = {20, 40, 80, 120}
THUNDERBOLT_VERSIONS = {3, 4, 5}

PCIE_SLOT_REQUIRED_KEYS = {
    "slot_id", "mechanical", "electrical", "generation", "source",
}
PCIE_SLOT_OPTIONAL_KEYS = {"conditions", "shares_with"}
M2_INTERFACES = {"pcie", "sata"}
M2_PCIE_LANES = {1, 2, 4}
M2_SLOT_REQUIRED_KEYS = {
    "slot_id", "interfaces", "pcie_generation", "lanes", "source",
}
M2_SLOT_OPTIONAL_KEYS = {"conditions", "shares_with"}


def _positive_int(value: Any, *, allow_zero: bool = False) -> bool:
    minimum = 0 if allow_zero else 1
    return (
        not isinstance(value, bool)
        and isinstance(value, int)
        and value >= minimum
    )


def _non_blank_string_list(value: Any) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(isinstance(item, str) and item.strip() for item in value)
    )


def validate_pcie_slot_layout(value: Any) -> list[str]:
    """Return validation errors for an exact physical/electrical slot layout."""
    errors: list[str] = []
    if not isinstance(value, list) or not value:
        return ["pcie_slot_layout must be a non-empty list"]

    seen_ids: set[str] = set()
    for index, slot in enumerate(value):
        prefix = f"pcie_slot_layout[{index}]"
        if not isinstance(slot, dict):
            errors.append(f"{prefix} must be an object")
            continue
        missing = sorted(PCIE_SLOT_REQUIRED_KEYS - set(slot))
        extra = sorted(set(slot) - PCIE_SLOT_REQUIRED_KEYS - PCIE_SLOT_OPTIONAL_KEYS)
        if missing:
            errors.append(f"{prefix} missing fields: {', '.join(missing)}")
        if extra:
            errors.append(f"{prefix} has unsupported fields: {', '.join(extra)}")

        slot_id = slot.get("slot_id")
        if not isinstance(slot_id, str) or not slot_id.strip():
            errors.append(f"{prefix}.slot_id must be a non-blank string")
        elif slot_id in seen_ids:
            errors.append(f"{prefix}.slot_id duplicates {slot_id}")
        else:
            seen_ids.add(slot_id)

        mechanical = slot.get("mechanical")
        electrical = slot.get("electrical")
        if mechanical not in PCIE_WIDTHS:
            errors.append(f"{prefix}.mechanical must be one of {PCIE_WIDTHS}")
        if electrical not in PCIE_WIDTHS:
            errors.append(f"{prefix}.electrical must be one of {PCIE_WIDTHS}")
        if mechanical in PCIE_WIDTHS and electrical in PCIE_WIDTHS:
            if PCIE_WIDTHS.index(electrical) > PCIE_WIDTHS.index(mechanical):
                errors.append(f"{prefix}.electrical cannot exceed its physical slot width")

        generation = slot.get("generation")
        if not _positive_int(generation) or generation > 5:
            errors.append(f"{prefix}.generation must be an integer from 1 to 5")
        if slot.get("source") not in PCIE_SOURCES:
            errors.append(f"{prefix}.source must be cpu or chipset")
        for key in ("conditions", "shares_with"):
            if key in slot and not _non_blank_string_list(slot[key]):
                errors.append(f"{prefix}.{key} must be a non-empty string list")
    return errors


def validate_m2_slot_layout(value: Any) -> list[str]:
    """Return validation errors for an exact M.2 storage-slot layout.

    The layout deliberately models M.2 sockets separately from conventional
    PCIe expansion slots. Every supported entry is a PCIe/NVMe-capable Key-M
    storage socket; ``interfaces`` may additionally contain ``sata`` when the
    exact socket supports M.2 SATA devices.
    """
    errors: list[str] = []
    if not isinstance(value, list) or not value:
        return ["m2_slot_layout must be a non-empty list"]

    seen_ids: set[str] = set()
    for index, slot in enumerate(value):
        prefix = f"m2_slot_layout[{index}]"
        if not isinstance(slot, dict):
            errors.append(f"{prefix} must be an object")
            continue
        missing = sorted(M2_SLOT_REQUIRED_KEYS - set(slot))
        extra = sorted(set(slot) - M2_SLOT_REQUIRED_KEYS - M2_SLOT_OPTIONAL_KEYS)
        if missing:
            errors.append(f"{prefix} missing fields: {', '.join(missing)}")
        if extra:
            errors.append(f"{prefix} has unsupported fields: {', '.join(extra)}")

        slot_id = slot.get("slot_id")
        if not isinstance(slot_id, str) or not slot_id.strip():
            errors.append(f"{prefix}.slot_id must be a non-blank string")
        elif slot_id in seen_ids:
            errors.append(f"{prefix}.slot_id duplicates {slot_id}")
        else:
            seen_ids.add(slot_id)

        interfaces = slot.get("interfaces")
        if (
            not isinstance(interfaces, list)
            or not interfaces
            or len(set(interfaces)) != len(interfaces)
            or any(interface not in M2_INTERFACES for interface in interfaces)
            or "pcie" not in interfaces
        ):
            errors.append(
                f"{prefix}.interfaces must be a unique list containing pcie and optional sata"
            )

        generation = slot.get("pcie_generation")
        if not _positive_int(generation) or generation > 5:
            errors.append(f"{prefix}.pcie_generation must be an integer from 1 to 5")
        if slot.get("lanes") not in M2_PCIE_LANES:
            errors.append(f"{prefix}.lanes must be one of {sorted(M2_PCIE_LANES)}")
        if slot.get("source") not in PCIE_SOURCES:
            errors.append(f"{prefix}.source must be cpu or chipset")
        for key in ("conditions", "shares_with"):
            if key in slot and not _non_blank_string_list(slot[key]):
                errors.append(f"{prefix}.{key} must be a non-empty string list")
    return errors


def validate_motherboard_capabilities(item: dict[str, Any]) -> list[str]:
    """Validate cross-field motherboard facts while preserving unknown state."""
    errors: list[str] = []
    if "pcie_slot_layout" in item:
        errors.extend(validate_pcie_slot_layout(item.get("pcie_slot_layout")))
    if "m2_slot_layout" in item:
        layout = item.get("m2_slot_layout")
        errors.extend(validate_m2_slot_layout(layout))
        if (
            isinstance(layout, list)
            and isinstance(item.get("m2_slots"), int)
            and not isinstance(item.get("m2_slots"), bool)
            and item["m2_slots"] != len(layout)
        ):
            errors.append("m2_slots must equal the number of m2_slot_layout entries")

    for key in ("usb4_shares_with", "usb4_disable_conditions", "sata_port_conditions"):
        if key in item and not _non_blank_string_list(item.get(key)):
            errors.append(f"{key} must be a non-empty string list")

    usb4_status = item.get("usb4_status")
    usb4_ports = item.get("usb4_rear_ports")
    usb4_speed = item.get("usb4_speed_gbps")
    if usb4_status is not None:
        if usb4_status not in USB4_STATUSES:
            errors.append(f"usb4_status must be one of {sorted(USB4_STATUSES)}")
        if not _positive_int(usb4_ports, allow_zero=True) or usb4_ports > 8:
            errors.append("usb4_rear_ports must be an integer from 0 to 8")
        elif usb4_status in {"native", "via_thunderbolt"} and usb4_ports == 0:
            errors.append(f"usb4_status={usb4_status} requires a rear port")
        elif usb4_status == "none_verified" and usb4_ports != 0:
            errors.append("usb4_status=none_verified requires zero rear ports")
        if usb4_status in {"native", "via_thunderbolt"} and usb4_speed not in USB4_SPEEDS_GBPS:
            errors.append(f"verified USB4 support requires speed in {sorted(USB4_SPEEDS_GBPS)} Gbps")
        if usb4_status == "none_verified" and usb4_speed is not None:
            errors.append("usb4_status=none_verified cannot declare usb4_speed_gbps")
    elif any(key in item for key in ("usb4_rear_ports", "usb4_speed_gbps", "usb4_shares_with", "usb4_disable_conditions")):
        errors.append("USB4 detail fields require usb4_status")

    thunderbolt_status = item.get("thunderbolt_status")
    thunderbolt_ports = item.get("thunderbolt_rear_ports")
    thunderbolt_version = item.get("thunderbolt_version")
    thunderbolt_header = item.get("thunderbolt_header")
    if thunderbolt_status is not None:
        if thunderbolt_status not in THUNDERBOLT_STATUSES:
            errors.append(
                f"thunderbolt_status must be one of {sorted(THUNDERBOLT_STATUSES)}"
            )
        if not _positive_int(thunderbolt_ports, allow_zero=True) or thunderbolt_ports > 8:
            errors.append("thunderbolt_rear_ports must be an integer from 0 to 8")
        elif thunderbolt_status == "native" and thunderbolt_ports == 0:
            errors.append("thunderbolt_status=native requires a rear port")
        elif thunderbolt_status != "native" and thunderbolt_ports != 0:
            errors.append(f"thunderbolt_status={thunderbolt_status} requires zero rear ports")
        if thunderbolt_status == "native" and thunderbolt_version not in THUNDERBOLT_VERSIONS:
            errors.append(
                f"native Thunderbolt requires version in {sorted(THUNDERBOLT_VERSIONS)}"
            )
        if thunderbolt_status != "native" and thunderbolt_version is not None:
            errors.append(f"thunderbolt_status={thunderbolt_status} cannot declare a version")
        if thunderbolt_header is not None and not isinstance(thunderbolt_header, bool):
            errors.append("thunderbolt_header must be boolean")
        if thunderbolt_status == "header_only" and thunderbolt_header is not True:
            errors.append("thunderbolt_status=header_only requires thunderbolt_header=true")
    elif any(key in item for key in ("thunderbolt_rear_ports", "thunderbolt_version", "thunderbolt_header")):
        errors.append("Thunderbolt detail fields require thunderbolt_status")

    display_outputs = item.get("display_outputs") or []
    if any(str(output).strip().lower() == "thunderbolt" for output in display_outputs):
        if thunderbolt_status != "native" or not _positive_int(thunderbolt_ports):
            errors.append("Thunderbolt display output requires a verified native rear port")

    return errors


def pcie_physical_slot_count(item: dict[str, Any] | None) -> int | None:
    """Count verified physical slots; unknown layout remains None."""
    layout = (item or {}).get("pcie_slot_layout")
    if validate_pcie_slot_layout(layout):
        return None
    return len({slot["slot_id"] for slot in layout})


def verified_m2_slot_layout(item: dict[str, Any] | None) -> list[dict[str, Any]] | None:
    """Return a verified M.2 layout; malformed or absent evidence stays unknown."""
    layout = (item or {}).get("m2_slot_layout")
    if validate_m2_slot_layout(layout):
        return None
    return layout


def verified_m2_slot_count(item: dict[str, Any] | None) -> int | None:
    """Return the exact M.2 slot count when a valid per-slot layout exists."""
    layout = verified_m2_slot_layout(item)
    return len(layout) if layout is not None else None


def verified_usb4_ports(item: dict[str, Any] | None) -> int:
    """Return verified rear USB4-capable ports, including explicit TB compatibility."""
    item = item or {}
    if item.get("usb4_status") not in {"native", "via_thunderbolt"}:
        return 0
    ports = item.get("usb4_rear_ports")
    return ports if _positive_int(ports) else 0


def verified_thunderbolt_ports(item: dict[str, Any] | None) -> int:
    """Return native rear Thunderbolt ports; an expansion header is not a port."""
    item = item or {}
    if item.get("thunderbolt_status") != "native":
        return 0
    ports = item.get("thunderbolt_rear_ports")
    return ports if _positive_int(ports) else 0
