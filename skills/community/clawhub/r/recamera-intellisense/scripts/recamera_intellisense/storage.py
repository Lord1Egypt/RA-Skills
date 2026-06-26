"""Storage slots, quota, and async tasks (``/record/storage/{status,config,control}``)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from . import _config, _http

__all__ = [
    "get_storage_status",
    "set_storage_slot",
    "configure_storage_quota",
    "storage_task_submit",
    "storage_task_status",
    "storage_task_cancel",
    "ensure_storage",
    "normalize_action",
    "DEFAULT_INTERNAL_DEV_PATH",
]

PATH_STATUS = "/cgi-bin/entry.cgi/record/storage/status"
PATH_CONFIG = "/cgi-bin/entry.cgi/record/storage/config"
PATH_CONTROL = "/cgi-bin/entry.cgi/record/storage/control"

DEFAULT_INTERNAL_DEV_PATH = "/dev/mmcblk0p8"

_STORAGE_ACTIONS = {
    "FORMAT",
    "FREE_UP",
    "EJECT",
    "REMOVE_FILES_OR_DIRECTORIES",
}
_STORAGE_ACTION_ALIASES = {
    "REMOVE": "REMOVE_FILES_OR_DIRECTORIES",
    "REMOVE_FILES": "REMOVE_FILES_OR_DIRECTORIES",
}


def normalize_action(action: str) -> str:
    """Canonicalise a storage-task action name (accepts aliases)."""
    up = str(action).upper()
    if up in _STORAGE_ACTIONS:
        return up
    if up in _STORAGE_ACTION_ALIASES:
        return _STORAGE_ACTION_ALIASES[up]
    raise ValueError(
        f"Unknown storage action {action!r}. Allowed: {sorted(_STORAGE_ACTIONS)}."
    )


def _parse_slot(s: Dict[str, Any], data_dir: str) -> Dict[str, Any]:
    def _s(k: str) -> str:
        return str(s.get(k, ""))

    def _b(k: str) -> bool:
        return bool(s.get(k, False))

    def _i(k: str) -> int:
        return int(s.get(k, 0) or 0)

    return {
        "dev_path": _s("sDevPath"),
        "mount_path": _s("sMountPath"),
        "removable": _b("bRemovable"),
        "internal": _b("bInternal"),
        "label": s.get("sLabel"),
        "uuid": s.get("sUUID"),
        "fs_type": s.get("sType"),
        "selected": _b("bSelected"),
        "enabled": _b("bEnabled"),
        "syncing": _b("bSyncing"),
        "writing": _b("bWriting"),
        "rotating": _b("bRotating"),
        "state_code": _i("eState"),
        "state": _s("sState"),
        "size_bytes": _i("iStatsSizeBytes"),
        "free_bytes": _i("iStatsFreeBytes"),
        "quota_min_recommend_bytes": _i("iQuotaMinimumRecommendBytes"),
        "quota_preserved_bytes": _i("iQuotaPreservedBytes"),
        "quota_used_bytes": s.get("iQuotaUsedBytes"),
        "quota_limit_bytes": _i("iQuotaLimitBytes"),
        "quota_rotate": _b("bQuotaRotate"),
        "data_dir": data_dir,
    }


def get_storage_status(device_name: str) -> List[Dict[str, Any]]:
    """List the storage slots (each as a dict)."""
    dev = _config.resolve(device_name)
    data = _http.get_json(dev, PATH_STATUS) or {}
    data_dir = data.get("sDataDirName", "") or ""
    slots = data.get("lSlots") or []
    return [_parse_slot(s, data_dir) for s in slots if isinstance(s, dict)]


def set_storage_slot(
    device_name: str,
    *,
    by_dev_path: str = "",
    by_uuid: str = "",
) -> None:
    """Select the slot to enable; pass both empty to disable all slots."""
    dev = _config.resolve(device_name)
    if by_dev_path or by_uuid:
        select: Any = {"sByDevPath": by_dev_path, "sByUUID": by_uuid}
    else:
        select = None
    resp = _http.post_json(dev, PATH_CONFIG, payload={"dSelectSlotToEnable": select})
    _http.expect_ok(resp, "set storage selection")


def configure_storage_quota(
    device_name: str,
    *,
    dev_path: str,
    quota_limit_bytes: int,
    quota_rotate: bool = True,
) -> None:
    """Set per-slot quota. ``quota_limit_bytes = -1`` means no limit."""
    dev = _config.resolve(device_name)
    payload = {
        "sTask": "SYNC",
        "sAction": "CONFIG",
        "sSlotDevPath": dev_path,
        "dSlotConfig": {
            "iQuotaLimitBytes": int(quota_limit_bytes),
            "bQuotaRotate": bool(quota_rotate),
        },
    }
    resp = _http.post_json(dev, PATH_CONTROL, payload=payload)
    _http.expect_ok(resp, "configure storage quota")


def _task_payload(
    task_type: str,
    action: str,
    dev_path: str,
    files: Optional[List[str]] = None,
    task_uid: Optional[str] = None,
) -> Dict[str, Any]:
    action = normalize_action(action)
    payload: Dict[str, Any] = {
        "sTask": task_type,
        "sAction": action,
        "sSlotDevPath": dev_path,
    }
    if action == "REMOVE_FILES_OR_DIRECTORIES":
        if not files:
            raise ValueError("REMOVE_FILES_OR_DIRECTORIES requires non-empty 'files'.")
        payload["lFilesOrDirectoriesToRemove"] = list(files)
    if task_uid:
        payload["sTaskUID"] = task_uid
    return payload


def storage_task_submit(
    device_name: str,
    *,
    action: str,
    dev_path: str,
    sync: bool = False,
    files: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Submit a storage action. ``sync=True`` blocks until completion.

    ``FORMAT`` and ``FREE_UP`` can take a long time and are rejected with
    ``sync=True`` (submit async and poll :func:`storage_task_status` instead).
    """
    action_canonical = normalize_action(action)
    if sync and action_canonical in ("FORMAT", "FREE_UP"):
        raise ValueError(
            f"Action '{action_canonical}' may take a long time and cannot be run "
            f"with sync=true. Submit async (sync=false) and poll with "
            f"storage_task_status."
        )
    dev = _config.resolve(device_name)
    payload = _task_payload("SYNC" if sync else "ASYNC_SUBMIT", action, dev_path, files)
    resp = _http.post_json(dev, PATH_CONTROL, payload=payload)
    _http.expect_ok(resp, f"storage task submit {payload['sAction']}")
    return resp if isinstance(resp, dict) else {}


def storage_task_status(
    device_name: str,
    *,
    action: str,
    dev_path: str,
    task_uid: Optional[str] = None,
) -> Dict[str, Any]:
    """Query the status of the last async task for (*action*, *dev_path*)."""
    dev = _config.resolve(device_name)
    payload = _task_payload("ASYNC_STATUS", action, dev_path, task_uid=task_uid)
    resp = _http.post_json(dev, PATH_CONTROL, payload=payload)
    _http.expect_ok(resp, f"storage task status {payload['sAction']}")
    return resp if isinstance(resp, dict) else {}


def storage_task_cancel(
    device_name: str,
    *,
    action: str,
    dev_path: str,
    task_uid: Optional[str] = None,
) -> Dict[str, Any]:
    """Cancel an in-flight async task."""
    dev = _config.resolve(device_name)
    payload = _task_payload("ASYNC_CANCEL", action, dev_path, task_uid=task_uid)
    resp = _http.post_json(dev, PATH_CONTROL, payload=payload)
    _http.expect_ok(resp, f"storage task cancel {payload['sAction']}")
    return resp if isinstance(resp, dict) else {}


def ensure_storage(device_name: str, *, timeout_s: float = 3.0) -> None:
    """Ensure one slot is enabled with rotate-quota on (mirrors Rust ``storage::ensure_storage``)."""
    import time

    slots = get_storage_status(device_name)
    if not any(s["enabled"] for s in slots):
        default = next(
            (s for s in slots if s["dev_path"] == DEFAULT_INTERNAL_DEV_PATH), None
        )
        if default is None:
            raise ValueError(
                f"Default storage '{DEFAULT_INTERNAL_DEV_PATH}' not found; "
                "call set_storage_slot to pick one."
            )
        set_storage_slot(device_name, by_dev_path=default["dev_path"])
        deadline = time.time() + timeout_s
        while time.time() < deadline:
            current = get_storage_status(device_name)
            match = next(
                (s for s in current if s["dev_path"] == default["dev_path"]), None
            )
            if (
                match
                and match["enabled"]
                and match.get("state") in ("IDLE", "WRITING", "READY")
            ):
                break
            time.sleep(0.25)
        configure_storage_quota(
            device_name,
            dev_path=default["dev_path"],
            quota_limit_bytes=-1,
            quota_rotate=True,
        )
        return
    for s in slots:
        if s["enabled"] and not s["quota_rotate"]:
            configure_storage_quota(
                device_name,
                dev_path=s["dev_path"],
                quota_limit_bytes=s["quota_limit_bytes"],
                quota_rotate=True,
            )


COMMANDS = {
    "get_storage_status": get_storage_status,
    "set_storage_slot": set_storage_slot,
    "configure_storage_quota": configure_storage_quota,
    "storage_task_submit": storage_task_submit,
    "storage_task_status": storage_task_status,
    "storage_task_cancel": storage_task_cancel,
}
COMMAND_SCHEMAS = {
    "get_storage_status": {"required": {"device_name"}, "optional": set()},
    "set_storage_slot": {
        "required": {"device_name"},
        "optional": {"by_dev_path", "by_uuid"},
    },
    "configure_storage_quota": {
        "required": {"device_name", "dev_path", "quota_limit_bytes"},
        "optional": {"quota_rotate"},
    },
    "storage_task_submit": {
        "required": {"device_name", "action", "dev_path"},
        "optional": {"sync", "files"},
    },
    "storage_task_status": {
        "required": {"device_name", "action", "dev_path"},
        "optional": {"task_uid"},
    },
    "storage_task_cancel": {
        "required": {"device_name", "action", "dev_path"},
        "optional": {"task_uid"},
    },
}
