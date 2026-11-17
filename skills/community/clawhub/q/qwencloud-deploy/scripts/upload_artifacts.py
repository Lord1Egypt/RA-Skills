#!/usr/bin/env python3
"""Upload artifacts to OSS temp bucket + generate signed URLs. See reference/deploy/10_upload_artifacts.md"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tarfile
import tempfile
import time
import uuid
from pathlib import Path

def _ts_key(name: str) -> str:
    """Generate timestamped object key, e.g. static-20260703-113500.tar.gz, ensuring each upload does not overwrite previous versions."""
    base, ext = name.rsplit(".", 1) if "." in name else (name, "")
    ts = time.strftime("%Y%m%d-%H%M%S")
    return f"{base}-{ts}.tar.gz"

def sh(cmd, check=True, capture=False):
    print(f"[sh] {' '.join(cmd) if isinstance(cmd, list) else cmd}", file=sys.stderr)
    r = subprocess.run(cmd, shell=isinstance(cmd, str), check=check,
                       stdout=subprocess.PIPE if capture else None,
                       stderr=subprocess.PIPE if capture else None,
                       text=True)
    if capture:
        return r.stdout.strip()
    return None

def aliyun(*args, capture=False):
    return sh(["aliyun", *args], capture=capture)

_OSS_NOT_ACTIVATED_MARKERS = (
    "not enabled", "not activated", "not been opened", "has not opened",
    "nosuchservice", "please activate", "service is not open",
    "未开通", "请先开通",
)

def _oss_service_not_activated(text: str) -> bool:
    t = (text or "").lower()
    return any(m in t for m in _OSS_NOT_ACTIVATED_MARKERS)

def _activate_oss_service() -> bool:
    """Best-effort auto-activation of the OSS service (free; usage billed).

    Returns True if activation succeeded or the service was already active.
    """
    print("[bucket] OSS service not activated — activating automatically "
          "(activation is free; usage is billed)...", file=sys.stderr)
    r = subprocess.run(["aliyun", "ossadmin", "OpenOssService"],
                       capture_output=True, text=True)
    out = (r.stderr + r.stdout).lower()
    if r.returncode == 0 or any(k in out for k in ("already", "opened", "order.process", "success")):
        print("[bucket] OSS service activated.", file=sys.stderr)
        return True
    print(r.stderr, file=sys.stderr)
    print("[bucket] Could not auto-activate OSS. Activate manually at "
          "https://oss.console.aliyun.com/ then retry.", file=sys.stderr)
    return False

def ensure_bucket(region: str, bucket: str | None) -> str:
    created = False
    if not bucket:
        bucket = f"qwencloud-deploy-tmp-{uuid.uuid4().hex[:6]}"

    def _mb():
        return subprocess.run(
            ["aliyun", "oss", "mb", f"oss://{bucket}/", "--region", region],
            capture_output=True, text=True)

    r = _mb()
    combined = (r.stderr + r.stdout).lower()
    if r.returncode != 0 and _oss_service_not_activated(combined):
        # Second line of defense (env check flow normally handles this first).
        if not _activate_oss_service():
            raise SystemExit(2)
        r = _mb()
        combined = (r.stderr + r.stdout).lower()

    if r.returncode == 0:
        created = True
    elif "already" in combined or "bucketalreadyexists" in combined:
        pass  # Bucket already exists (reuse), skip re-initialization
    else:
        print(r.stderr, file=sys.stderr)
        raise SystemExit(2)
    print(f"[bucket] {bucket}", file=sys.stderr)

    if created:
        _set_bucket_tag(bucket)
        _set_bucket_lifecycle(bucket, region)

    return bucket

def _set_bucket_tag(bucket: str):
    subprocess.run(
        ["aliyun", "oss", "bucket-tagging", "--method", "put",
         f"oss://{bucket}/", "from#qwencloud"],
        capture_output=True, text=True)

def _set_bucket_lifecycle(bucket: str, region: str):
    lifecycle_xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<LifecycleConfiguration>'
        '<Rule><ID>auto-expire-7d</ID>'
        '<Prefix></Prefix>'
        '<Status>Enabled</Status>'
        '<Expiration><Days>7</Days></Expiration>'
        '</Rule>'
        '</LifecycleConfiguration>'
    )
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".xml", delete=False)
    try:
        tmp.write(lifecycle_xml)
        tmp.close()
        subprocess.run(
            ["aliyun", "oss", "lifecycle", "--method", "put",
             f"oss://{bucket}/", tmp.name],
            capture_output=True, text=True)
    finally:
        os.unlink(tmp.name)

def to_internal_url(url: str) -> str:
    """Convert OSS public URL to internal endpoint (VPC-reachable, free traffic)."""
    return re.sub(r"oss-([a-z0-9-]+)\.aliyuncs\.com", r"oss-\1-internal.aliyuncs.com", url)

def upload(bucket: str, local: Path, key: str, internal: bool = True) -> str:
    sh(["aliyun", "oss", "cp", str(local), f"oss://{bucket}/{key}", "-f"])
    url = aliyun("oss", "sign", f"oss://{bucket}/{key}", "--timeout", "86400", capture=True)
    for tok in url.split():
        if tok.startswith("http"):
            return to_internal_url(tok) if internal else tok
    # Failing to parse the signed URL must abort immediately. Otherwise an empty
    # (or garbage) URL lands in the JSON, the template still renders, the stack
    # still creates successfully, but `curl -fsSL "" -o app.tar.gz` on the ECS
    # never fetches the artifact — symptom is "public IP works, app never comes
    # up", which is very hard to diagnose.
    raise SystemExit(
        f"Could not parse a signed URL from `aliyun oss sign` output "
        f"(oss://{bucket}/{key}). CLI output:\n{url}"
    )

# Skip these dirs/files when packing, to keep node_modules / .git and other bulk out of the archive:
# 1) Slows down upload and ECS download; 2) macOS node_modules contain native extensions (sharp/bcrypt etc),
# which won't work on Linux ECS anyway; UserData reinstalls dependencies on the ECS side.
TAR_EXCLUDE_DIR_NAMES = {
    "node_modules", ".git", "__pycache__", ".venv", "venv",

    ".idea", ".vscode",
}
# Only match relative path segments (exact match to avoid false positives on same-named dirs)
TAR_EXCLUDE_REL_PATHS = {
    ".next/cache",
    "target/test-classes",
    "build/test-results",
}
TAR_EXCLUDE_FILE_NAMES = {".DS_Store", "Thumbs.db"}

def _tar_filter(ti: "tarfile.TarInfo"):
    # ti.name looks like "./node_modules/foo" or "node_modules/foo"
    parts = [p for p in ti.name.split("/") if p and p != "."]
    if any(p in TAR_EXCLUDE_DIR_NAMES for p in parts):
        return None
    rel = "/".join(parts)
    if any(rel == ex or rel.startswith(ex + "/") for ex in TAR_EXCLUDE_REL_PATHS):
        return None
    if parts and parts[-1] in TAR_EXCLUDE_FILE_NAMES:
        return None
    return ti

def tar_dir(src: Path, dest: Path, arcname: str = "."):
    with tarfile.open(dest, "w:gz") as t:
        t.add(str(src), arcname=arcname, filter=_tar_filter)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--region", required=True)
    ap.add_argument("--bucket", default=None)
    ap.add_argument("--static-dir", default=None, help="Local static build artifact directory")
    ap.add_argument("--app-mode", default=None,
                    choices=["docker-image", "docker-compose", "binary", "skip"],
                    help="Use skip if app artifact is not needed")
    ap.add_argument("--app-dir", default=None)
    ap.add_argument("--app-image-name", default=None,
                    help="Local image to docker save in docker-image mode")
    ap.add_argument("--template-file", default=None,
                    help="ROS template file path, uploaded to OSS to output template_url (for --TemplateURL to avoid WAF)")
    ap.add_argument("--no-internal", action="store_true",
                    help="Do not replace with internal endpoint (default replaces with oss-*-internal.aliyuncs.com)")
    args = ap.parse_args()

    bucket = ensure_bucket(args.region, args.bucket)
    internal = not args.no_internal
    out = {"bucket": bucket, "static_url": None, "app_url": None, "template_url": None}

    with tempfile.TemporaryDirectory(prefix="qwencloud-pack-") as tmpdir:
        tmp = Path(tmpdir)

        # Static
        if args.static_dir:
            fdir = Path(args.static_dir).resolve()
            if not fdir.is_dir():
                raise SystemExit(f"static-dir does not exist: {fdir}")
            fpack = tmp / "static.tar.gz"
            tar_dir(fdir, fpack, arcname=".")
            out["static_url"] = upload(bucket, fpack, _ts_key("static"), internal=internal)

        # App
        if args.app_mode and args.app_mode != "skip":
            bpack = tmp / "app.tar.gz"

            if args.app_mode == "docker-image":
                if not args.app_image_name:
                    raise SystemExit("docker-image mode requires --app-image-name")
                img_tar = tmp / "image.tar"
                sh(["docker", "save", "-o", str(img_tar), args.app_image_name])
                with tarfile.open(bpack, "w:gz") as t:
                    t.add(str(img_tar), arcname="image.tar")
            elif args.app_mode == "docker-compose":
                bdir = Path(args.app_dir or ".").resolve()
                tar_dir(bdir, bpack, arcname=".")
            elif args.app_mode == "binary":
                bdir = Path(args.app_dir or ".").resolve()
                tar_dir(bdir, bpack, arcname=".")

            out["app_url"] = upload(bucket, bpack, _ts_key("app"), internal=internal)

        # Template upload (avoid --TemplateBody being blocked by WAF)
        if args.template_file:
            tpl = Path(args.template_file).resolve()
            if not tpl.is_file():
                raise SystemExit(f"template-file does not exist: {tpl}")
            out["template_url"] = upload(bucket, tpl, "template.yaml", internal=False)

    print(json.dumps(out, ensure_ascii=False))

if __name__ == "__main__":
    main()
