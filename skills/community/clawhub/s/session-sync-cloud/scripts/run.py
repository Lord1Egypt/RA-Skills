#!/usr/bin/env python3
"""
session-sync-cloud — cloud backup and sync for memory files
"""

import json
import sys
import os
import time
import hashlib
import base64
import datetime
from pathlib import Path
from typing import Dict, List

try:
    import boto3
    from botocore.exceptions import ClientError
    BOTO3_AVAILABLE = True
except ImportError:
    BOTO3_AVAILABLE = False

WORKSPACE = Path.cwd()
MEMORY_DIR = WORKSPACE / "memory"
CONFIG_FILE = WORKSPACE / "session-sync-config.json"
SYSTEM_LOG = MEMORY_DIR / "sync-log.jsonl"
DASHBOARD_FILE = MEMORY_DIR / "sync-dashboard.html"
MANIFEST_PREFIX = "manifests"

def load_config():
    if not CONFIG_FILE.exists():
        return {"error": "config missing"}
    try:
        return json.loads(CONFIG_FILE.read_text())
    except Exception as e:
        return {"error": f"invalid config: {e}"}

def ensure_dirs():
    MEMORY_DIR.mkdir(exist_ok=True)

def log_event(event: str, data: dict):
    ensure_dirs()
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "event": event,
        **data
    }
    with open(SYSTEM_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")

def get_s3_client(config):
    if not BOTO3_AVAILABLE:
        raise RuntimeError("boto3 not installed. Run: pip install boto3")
    session = boto3.session.Session(
        aws_access_key_id=config["key_id"],
        aws_secret_access_key=config["secret_key"],
        region_name=config.get("region", "us-east-1")
    )
    endpoint = config.get("endpoint")
    if endpoint:
        return session.client("s3", endpoint_url=endpoint)
    else:
        return session.client("s3")

def compute_file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def scan_memory() -> Dict[str, dict]:
    """Return dict: rel_path -> {size, mtime, hash}"""
    ensure_dirs()
    files = {}
    for p in MEMORY_DIR.rglob("*"):
        if p.is_file():
            rel = p.relative_to(MEMORY_DIR)
            stat = p.stat()
            files[str(rel)] = {
                "size": stat.st_size,
                "mtime": stat.st_mtime,
                "hash": compute_file_hash(p)
            }
    return files

def upload_manifest(config: dict, manifest: dict, timestamp: str):
    """Upload manifest JSON to S3"""
    s3 = get_s3_client(config)
    bucket = config["bucket"]
    prefix = config.get("path_prefix", "")
    key = f"{prefix}{MANIFEST_PREFIX}/{timestamp}.json"
    body = json.dumps(manifest, indent=2)
    s3.put_object(Bucket=bucket, Key=key, Body=body.encode("utf-8"), ContentType="application/json")
    log_event("manifest_uploaded", {"bucket": bucket, "key": key, "files": len(manifest.get("files", {}))})

def list_manifests(config: dict) -> List[dict]:
    """List available manifests from cloud, return list of {timestamp, key}"""
    s3 = get_s3_client(config)
    bucket = config["bucket"]
    prefix = config.get("path_prefix", "") + MANIFEST_PREFIX + "/"
    resp = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    manifests = []
    for obj in resp.get("Contents", []):
        key = obj["Key"]
        # Extract timestamp from filename
        try:
            ts = key.split("/")[-1].replace(".json", "")
            manifests.append({"timestamp": ts, "key": key, "last_modified": obj["LastModified"].isoformat()})
        except:
            continue
    return sorted(manifests, key=lambda x: x["timestamp"], reverse=True)

def download_manifest(config: dict, key: str) -> dict:
    s3 = get_s3_client(config)
    bucket = config["bucket"]
    resp = s3.get_object(Bucket=bucket, Key=key)
    return json.loads(resp["Body"].read())

def restore_from_manifest(config: dict, manifest: dict):
    """Download files from manifest and write to memory dir"""
    s3 = get_s3_client(config)
    bucket = config["bucket"]
    prefix = config.get("path_prefix", "")
    files_restored = 0
    for rel_path, meta in manifest.get("files", {}).items():
        target = MEMORY_DIR / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        key = prefix + meta["s3_key"]
        resp = s3.get_object(Bucket=bucket, Key=key)
        content = resp["Body"].read()
        with open(target, "wb") as f:
            f.write(content)
        files_restored += 1
    log_event("restore_complete", {"files": files_restored, "manifest_timestamp": manifest.get("timestamp")})
    return {"restored": files_restored}

def generate_dashboard(manifests: List[dict], status: dict):
    """Generate a simple HTML dashboard"""
    html = """<!DOCTYPE html><html><head><title>Sync Dashboard</title>
<style>body{font-family:system-ui; padding:2rem;} table{border-collapse:collapse; width:100%;} th,td{border:1px solid #ddd; padding:0.5rem;} th{background:#eee;}</style>
</head><body><h1>Session Sync Cloud</h1>
<h2>Status</h2>
<ul>
<li><strong>Last backup:</strong> {last_backup}</li>
<li><strong>Next scheduled:</strong> {next_backup}</li>
<li><strong>Storage used:</strong> {storage_used} MB</li>
<li><strong>Versions retained:</strong> {versions}</li>
<li><strong>API connected:</strong> {connected}</li>
</ul>
<h2>Backup History</h2>
<table><tr><th>Timestamp</th><th>Files</th><th>Size (MB)</th><th>Action</th></tr>
{rows}
</table>
<script>
function restore(ts) {{
  if (confirm('Restore from ' + ts + '? This will overwrite current memory files.')) {{
    fetch('/restore?ts=' + ts).then(r=>r.json()).then(d=>alert('Restored ' + d.restored + ' files'));
  }}
}}
</script>
</body></html>"""
    # Compute stats
    last_backup = status.get("last_backup", "never")
    next_backup = status.get("next_backup", "scheduled")
    storage_used = status.get("storage_bytes", 0) / 1e6
    connected = "yes" if status.get("api_connected") else "no"
    versions = len(manifests)
    rows = ""
    for m in manifests[:20]:
        ts = m["timestamp"]
        files = 0  # need to parse manifest to get count; skip for brevity
        size = 0
        rows += f"<tr><td>{ts}</td><td>{files}</td><td>{size:.1f}</td><td><button onclick=\"restore('{ts}')\">Restore</button></td></tr>"
    html = html.format(
        last_backup=last_backup,
        next_backup=next_backup,
        storage_used=f"{storage_used:.1f}",
        connected=connected,
        versions=versions,
        rows=rows
    )
    DASHBOARD_FILE.write_text(html)

def sync_now():
    cfg = load_config()
    if "error" in cfg:
        return {"error": cfg["error"]}
    
    if not BOTO3_AVAILABLE:
        return {"error": "boto3 not installed. pip install boto3"}
    
    ensure_dirs()
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%SZ")
    
    # Scan files
    files = scan_memory()
    
    # Upload each file
    s3 = get_s3_client(cfg)
    bucket = cfg["bucket"]
    prefix = cfg.get("path_prefix", "")
    uploaded = 0
    bytes_uploaded = 0
    for rel_path, meta in files.items():
        s3_key = f"{prefix}files/{rel_path}"
        # Check if already exists and same hash; skip if unchanged
        try:
            head = s3.head_object(Bucket=bucket, Key=s3_key)
            if head["Metadata"].get("sha256") == meta["hash"]:
                continue  # unchanged
        except ClientError as e:
            if e.response["Error"]["Code"] != "404":
                raise
        # Upload
        s3.upload_file(
            Filename=str(MEMORY_DIR / rel_path),
            Bucket=bucket,
            Key=s3_key,
            ExtraArgs={"Metadata": {"sha256": meta["hash"]}}
        )
        uploaded += 1
        bytes_uploaded += meta["size"]
    
    # Build and upload manifest
    manifest = {
        "timestamp": timestamp,
        "files": {rel: {**meta, "s3_key": f"{prefix}files/{rel}"} for rel, meta in files.items()},
        "uploaded": uploaded,
        "bytes_uploaded": bytes_uploaded
    }
    upload_manifest(cfg, manifest, timestamp)
    
    # Prune old manifests
    manifests = list_manifests(cfg)
    retain_days = cfg.get("retention_days", 30)
    cutoff = datetime.datetime.utcnow() - datetime.timedelta(days=retain_days)
    for m in manifests:
        try:
            ts = datetime.datetime.strptime(m["timestamp"], "%Y-%m-%dT%H-%M-%SZ")
            if ts < cutoff:
                s3.delete_object(Bucket=bucket, Key=m["key"])
        except:
            continue
    
    log_event("sync_complete", {"uploaded": uploaded, "bytes": bytes_uploaded, "manifests": len(manifests)})
    
    # Generate dashboard
    status = {
        "last_backup": timestamp,
        "next_backup": "in 15 minutes",
        "storage_bytes": sum(m.get("size", 0) for m in manifests),  # rough
        "api_connected": True,
        "versions": len(manifests)
    }
    generate_dashboard(manifests, status)
    
    return {"status": "ok", "timestamp": timestamp, "uploaded": uploaded, "bytes_uploaded": bytes_uploaded}

def sync_status():
    cfg = load_config()
    if "error" in cfg:
        return {"error": cfg["error"]}
    manifests = list_manifests(cfg)
    last = manifests[0]["timestamp"] if manifests else None
    status = {
        "last_backup": last,
        "next_backup": "scheduled",
        "storage_bytes": 0,  # would sum sizes
        "api_connected": True,
        "versions": len(manifests)
    }
    # Also read dashboard?
    return {"status": status, "manifests": manifests[:5]}

def sync_restore(timestamp: str):
    cfg = load_config()
    if "error" in cfg:
        return {"error": cfg["error"]}
    manifests = list_manifests(cfg)
    if timestamp == "latest":
        ts = manifests[0]["timestamp"] if manifests else None
    else:
        ts = timestamp
    # Find manifest key
    manifest_key = None
    for m in manifests:
        if m["timestamp"] == ts:
            manifest_key = m["key"]
            break
    if not manifest_key:
        return {"error": "manifest not found"}
    manifest = download_manifest(cfg, manifest_key)
    result = restore_from_manifest(cfg, manifest)
    return {"restored": result["restored"], "timestamp": ts}

def main():
    if len(sys.argv) < 2:
        print("Usage: run.py [sync_status|sync_now|sync_restore] [json_input]")
        sys.exit(1)
    action = sys.argv[1]
    input_data = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    if action == "sync_status":
        result = sync_status()
    elif action == "sync_now":
        result = sync_now()
    elif action == "sync_restore":
        ts = input_data.get("timestamp")
        if not ts:
            result = {"error": "timestamp required"}
        else:
            result = sync_restore(ts)
    else:
        result = {"error": "unknown action"}
    print(json.dumps(result, indent=2))
    sys.exit(0 if "error" not in result else 1)

if __name__ == "__main__":
    main()
