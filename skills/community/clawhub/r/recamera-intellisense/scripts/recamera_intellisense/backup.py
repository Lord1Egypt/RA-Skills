"""Whole-device configuration backup (``/config/export``): the device stages a
tarball and returns a relay URL; we download it to a LOCAL file. Read-only
with respect to the device."""

from __future__ import annotations

if __name__ == "__main__" and __package__ is None:
    import os
    import sys

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from recamera_intellisense._cli import main

    raise SystemExit(main())

import os
from typing import Any, Dict, Optional

from . import _config, _http
from ._errors import RecameraError

__all__ = ["export_device_config"]

PATH_EXPORT = "/cgi-bin/entry.cgi/config/export"

_DOWNLOAD_TIMEOUT = 120.0  # tarball can be tens of MiB


def export_device_config(
    device_name: Optional[str] = None,
    *,
    output: str,
) -> Dict[str, Any]:
    """Download the full device configuration tarball to the LOCAL `output` path.

    Returns ``{output, size_bytes}``. Snapshot the device before an agent makes
    configuration changes, so a known-good state can be restored by a human
    from the Web Console. Refuses to overwrite an existing local file — pick a
    fresh name per snapshot.
    """
    if not output or not isinstance(output, str):
        raise ValueError("output (local file path) is required")
    out_path = os.path.abspath(os.path.expanduser(output))
    if os.path.exists(out_path):
        raise ValueError(f"output already exists (refusing to overwrite): {out_path}")
    dev = _config.resolve(device_name)
    meta = _http.get_json(dev, PATH_EXPORT)
    if not isinstance(meta, dict) or not meta.get("url"):
        raise RecameraError(f"config export failed: unexpected payload {meta!r}")
    url = str(meta["url"])
    body, _ = _http.get_bytes(dev, url, timeout=_DOWNLOAD_TIMEOUT)
    with open(out_path, "wb") as fh:
        fh.write(body)
    return {"output": out_path, "size_bytes": len(body)}


COMMANDS = {"export_device_config": export_device_config}
