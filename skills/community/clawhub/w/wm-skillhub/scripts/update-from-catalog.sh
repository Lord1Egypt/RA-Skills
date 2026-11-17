#!/usr/bin/env bash
# Safe SkillHub / pack upgrade: overlay official zips, preserve wm-skillhub/.env.
set -euo pipefail

OPEN_BASE="${WINMALE_OPEN_BASE:-https://open.winmale.com}"
OPEN_BASE="${OPEN_BASE%/}"
CATALOG_URL="${SKILLHUB_CATALOG_URL:-$OPEN_BASE/api/skills}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HUB_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILLS_ROOT="$(cd "$HUB_DIR/.." && pwd)"
TMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/wm-skillhub-update.XXXXXX")"
trap 'rm -rf "$TMP_DIR"' EXIT

only_id="${1:-}"
hub_only=false
if [[ "${1:-}" == "--hub-only" ]]; then
  hub_only=true
  only_id="wm-skillhub"
fi

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "missing required command: $1" >&2
    exit 1
  }
}

need_cmd curl
need_cmd unzip
need_cmd python3

echo "catalog: $CATALOG_URL"
echo "skills root: $SKILLS_ROOT"

curl -fsSL "$CATALOG_URL" -o "$TMP_DIR/catalog.json"

ENV_FILE="$HUB_DIR/.env"
ENV_BAK=""
if [[ -f "$ENV_FILE" ]]; then
  ENV_BAK="$TMP_DIR/env.bak"
  cp "$ENV_FILE" "$ENV_BAK"
  echo "backed up .env"
fi

python3 - "$TMP_DIR/catalog.json" "$SKILLS_ROOT" "$TMP_DIR" "$only_id" "$hub_only" "$OPEN_BASE" <<'PY'
import json, os, subprocess, sys, urllib.request
from pathlib import Path

cat_path, skills_root, tmp, only_id, hub_only, open_base = sys.argv[1:7]
hub_only = hub_only == "true"
open_base = (open_base or "https://open.winmale.com").rstrip("/")
doc = json.loads(Path(cat_path).read_text(encoding="utf-8"))
entries = list(doc.get("skills") or []) + list(doc.get("roles") or [])

def local_ver(entry_id: str) -> str:
    meta = Path(skills_root) / entry_id / ".wm-skill-meta.json"
    man = Path(skills_root) / entry_id / "manifest.json"
    skill = Path(skills_root) / entry_id / "SKILL.md"
    if meta.is_file():
        try:
            return str(json.loads(meta.read_text(encoding="utf-8")).get("version") or "")
        except Exception:
            pass
    if man.is_file():
        try:
            return str(json.loads(man.read_text(encoding="utf-8")).get("version") or "")
        except Exception:
            pass
    if skill.is_file():
        for line in skill.read_text(encoding="utf-8").splitlines()[:20]:
            if line.startswith("version:"):
                return line.split(":", 1)[1].strip().strip('"').strip("'")
    return ""

def semver_tuple(v: str):
    parts = []
    for p in (v or "0").split("."):
        try:
            parts.append(int("".join(ch for ch in p if ch.isdigit()) or "0"))
        except ValueError:
            parts.append(0)
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts[:3])

def outdated(local: str, remote: str) -> bool:
    if not remote:
        return False
    if not local:
        return True
    return semver_tuple(local) < semver_tuple(remote)

def pack_url_for(e: dict) -> str:
    eid = str(e.get("id") or "").strip()
    url = (e.get("pack_url") or e.get("pack_version_url") or "").strip()
    if url:
        return url
    # Hub zip may only be on catalog root fields.
    if eid == "wm-skillhub":
        url = (doc.get("hub_pack_url") or doc.get("hub_pack_version_url") or "").strip()
        if url:
            return url
    kind = "roles" if (
        str(e.get("kind") or "").lower() == "role" or eid.startswith("role-")
    ) else "skills"
    return f"{open_base}/api/{kind}/{eid}/pack"

targets = []
for e in entries:
    eid = str(e.get("id") or "").strip()
    if not eid:
        continue
    vis = str(e.get("visibility") or "public").strip().lower()
    if vis in ("deprecated", "hidden", "internal", "partner"):
        continue
    if only_id and eid != only_id:
        continue
    if hub_only and eid != "wm-skillhub":
        continue
    installed = (Path(skills_root) / eid).is_dir()
    remote = str(e.get("version") or "").strip()
    local = local_ver(eid)
    # Always refresh hub when requested; otherwise only installed+outdated (or missing hub).
    if eid == "wm-skillhub" or installed:
        if outdated(local, remote) or (eid == "wm-skillhub" and only_id == "wm-skillhub"):
            targets.append(e)
    elif only_id:
        targets.append(e)

if not targets:
    print("nothing to update (local versions current or not installed)")
    sys.exit(0)

for e in targets:
    eid = e["id"]
    url = pack_url_for(e)
    if not url:
        print(f"skip {eid}: no pack_url and no API fallback", file=sys.stderr)
        continue
    zip_path = Path(tmp) / f"{eid}.zip"
    print(f"update {eid}: {local_ver(eid) or '?'} → {e.get('version')} via {url}")
    urllib.request.urlretrieve(url, zip_path)
    subprocess.check_call(["unzip", "-oq", str(zip_path), "-d", skills_root])
    meta = {
        "id": eid,
        "version": e.get("version"),
        "installed_at": __import__("datetime").datetime.now(
            __import__("datetime").timezone.utc
        ).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    if str(e.get("kind") or "").lower() == "role" or eid.startswith("role-"):
        meta["kind"] = "role"
    meta_path = Path(skills_root) / eid / ".wm-skill-meta.json"
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    skill = Path(skills_root) / eid / "SKILL.md"
    sidecar = Path(skills_root) / eid / "_skillhub_meta.json"
    if not skill.is_file() or not skill.read_text(encoding="utf-8").startswith("---"):
        raise SystemExit(f"acceptance failed: {eid} SKILL.md frontmatter missing")
    if not sidecar.is_file():
        raise SystemExit(f"acceptance failed: {eid} missing _skillhub_meta.json")
    # If SKILL links references/, require at least one markdown under references/
    skill_text = skill.read_text(encoding="utf-8")
    if "references/" in skill_text:
        refs = Path(skills_root) / eid / "references"
        md_refs = list(refs.glob("**/*.md")) if refs.is_dir() else []
        if not md_refs:
            raise SystemExit(
                f"acceptance failed: {eid} SKILL.md references/ but no references/*.md after unzip"
            )
    print(f"ok {eid}")
PY

if [[ -n "$ENV_BAK" ]]; then
  cp "$ENV_BAK" "$ENV_FILE"
  echo "restored .env"
fi

if [[ -f "$ENV_FILE" ]]; then
  echo ".env present"
else
  echo "WARN: no .env — open $OPEN_BASE/skillhub/creds to copy keys if needed" >&2
fi

echo "done"
