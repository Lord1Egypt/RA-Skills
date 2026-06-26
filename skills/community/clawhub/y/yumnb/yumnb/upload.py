"""
yumnb upload dispatcher — push generated artifacts (mp3 / pptx / md) to
a cloud destination after `publish`, then return shareable URLs.

Providers:
  - none           : do nothing (keep local file:// URIs)
  - local          : explicit no-op (kept for clarity)
  - onedrive_graph : reuse tommy-talkshow's onedrive_upload.py (Edge SSO
                     via SharePoint REST API). No external binary, no
                     rclone setup — uploads to OneDrive for Business and
                     returns an org sharing link. Default for this user.
  - rclone         : shell out to `rclone` — supports OneDrive, Google
                     Drive, S3, Dropbox, Box, pCloud, Yandex, WebDAV and
                     ~50 more backends via the user's pre-configured
                     remote (https://rclone.org/docs/#configure).
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


DEFAULT_FILES = ["talkshow.mp3", "deck.pptx", "summary.md"]


def _onedrive_graph_upload(folder: Path, cfg: Dict, files: List[str],
                           label_map: Dict[str, str]) -> Dict[str, str]:
    """Upload via tommy-talkshow's onedrive_upload.upload_and_share().

    Imports the script as a module so we share the Edge SSO session across
    files in one publish run (faster than spawning a subprocess per file
    and re-attaching to Edge each time).
    """
    sub = cfg.get("onedrive_graph") or {}
    uploader_setting = sub.get("uploader_path")
    if not uploader_setting:
        print("upload [onedrive_graph] SKIP — set upload.onedrive_graph.uploader_path "
              "in config.yaml (path to tommy-talkshow/scripts/onedrive_upload.py)")
        return {}
    uploader_path = Path(os.path.expandvars(os.path.expanduser(str(uploader_setting))))
    base_url = sub.get("base_url") or None
    base_folder = (sub.get("folder") or "yumnb").strip("/")
    per_note = bool(sub.get("per_note_subfolder", True))
    remote_folder = f"{base_folder}/{folder.name}" if per_note else base_folder

    if not uploader_path.exists():
        print(f"upload [onedrive_graph] SKIP — uploader not found: {uploader_path}")
        return {}

    # Import the uploader script as a one-off module.
    import importlib.util
    spec = importlib.util.spec_from_file_location("_yumnb_onedrive", uploader_path)
    if spec is None or spec.loader is None:
        print(f"upload [onedrive_graph] SKIP — cannot load {uploader_path}")
        return {}
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)  # type: ignore[union-attr]
    except Exception as e:  # noqa: BLE001
        print(f"upload [onedrive_graph] SKIP — import failed: {e}")
        return {}

    upload_and_share = getattr(mod, "upload_and_share", None)
    if upload_and_share is None:
        print("upload [onedrive_graph] SKIP — upload_and_share() missing")
        return {}

    out: Dict[str, str] = {}
    for fname in files:
        fp = folder / fname
        if not fp.exists():
            continue
        try:
            link = upload_and_share(str(fp), filename=fname,
                                    base_url=base_url, folder=remote_folder)
        except TypeError:
            # Older onedrive_upload.py without `folder` kw — fall back to default.
            try:
                link = upload_and_share(str(fp), filename=fname, base_url=base_url)
            except Exception as e:  # noqa: BLE001
                print(f"upload [onedrive_graph {fname}] FAILED: {e}")
                continue
        except Exception as e:  # noqa: BLE001
            print(f"upload [onedrive_graph {fname}] FAILED: {e}")
            continue
        if link:
            out[label_map.get(fname, fname)] = link
            print(f"upload [onedrive_graph {fname}] OK -> {link}")
    return out


def _run(cmd: List[str], timeout: int = 300) -> Tuple[int, str, str]:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout)
        return r.returncode, (r.stdout or "").strip(), (r.stderr or "").strip()
    except FileNotFoundError as e:
        return 127, "", f"binary not found: {e}"
    except subprocess.TimeoutExpired:
        return 124, "", f"timeout after {timeout}s: {' '.join(cmd)}"
    except Exception as e:  # noqa: BLE001
        return 1, "", f"{type(e).__name__}: {e}"


def _rclone_upload_one(rclone_bin: str, local_path: Path,
                       remote_spec: str, share: bool,
                       extra_args: Optional[List[str]] = None) -> Optional[str]:
    """Upload one file via rclone copyto, optionally fetch a public link.

    remote_spec is `<rclone-remote>:<remote-folder>` (no filename).
    Returns the share URL on success, "" on upload-ok + share-skipped/failed,
    or None on upload failure.
    """
    remote_path = remote_spec.rstrip("/") + "/" + local_path.name
    args = [rclone_bin, "copyto", str(local_path), remote_path]
    if extra_args:
        args.extend(extra_args)

    rc, _out, err = _run(args, timeout=600)
    if rc != 0:
        print(f"upload [rclone copyto {local_path.name}] FAILED rc={rc}: {err}")
        return None
    print(f"upload [rclone copyto {local_path.name}] OK -> {remote_path}")

    if not share:
        return ""

    rc, out, err = _run([rclone_bin, "link", remote_path], timeout=120)
    if rc != 0 or not out:
        print(f"upload [rclone link {local_path.name}] WARN rc={rc}: {err}")
        return ""
    return out.strip().splitlines()[-1].strip()


def upload_folder(folder: Path, cfg: Dict) -> Dict[str, str]:
    """Upload artifacts from `folder` per `cfg` (the `upload` config block).

    Returns a label -> URL mapping. Labels mirror the local-link labels used
    in cmd_publish so the notify payload can swap them in transparently.
    Files that fail to upload are simply omitted.
    """
    provider = (cfg or {}).get("provider", "none") or "none"
    provider = provider.strip().lower()
    if provider in ("none", "local", ""):
        return {}

    files: List[str] = (cfg.get("files") or DEFAULT_FILES)
    label_map = {
        "talkshow.mp3": "🎧 Listen",
        "deck.pptx":   "📊 Slides",
        "summary.md":  "📝 Summary",
    }
    out: Dict[str, str] = {}

    if provider in ("onedrive_graph", "onedrive", "sharepoint"):
        return _onedrive_graph_upload(folder, cfg, files, label_map)

    if provider == "rclone":
        rconf = cfg.get("rclone") or {}
        remote = rconf.get("remote") or ""
        if not remote or ":" not in remote:
            print("upload [rclone] SKIP — upload.rclone.remote must be 'remote:path'")
            return {}
        rclone_bin = rconf.get("rclone_bin") or "rclone"
        if not shutil.which(rclone_bin) and not os.path.isfile(rclone_bin):
            print(f"upload [rclone] SKIP — '{rclone_bin}' not on PATH")
            return {}
        share = bool(rconf.get("share", True))
        extra_args = rconf.get("extra_args") or []

        # Per-note subfolder keeps uploads organized.
        per_note = bool(rconf.get("per_note_subfolder", True))
        remote_spec = remote.rstrip("/")
        if per_note:
            remote_spec = remote_spec + "/" + folder.name

        for fname in files:
            fp = folder / fname
            if not fp.exists():
                continue
            url = _rclone_upload_one(rclone_bin, fp, remote_spec, share, extra_args)
            if url:
                out[label_map.get(fname, fname)] = url
        return out

    print(f"upload [{provider}] SKIP — unknown provider")
    return {}
