"""
assemble_result.py — Assemble the final JSON output for the update-advisor skill.

Usage:
  python3 assemble_result.py <current> <latest> <has_update>
                             <changelog_result.json> <update_status.txt> <doctor_output.txt>
                             [update_status.json] [doctor_exit.txt]
"""
import sys
import json
import re

current     = sys.argv[1]
latest      = sys.argv[2]
has_update  = sys.argv[3] == "true"
changelog_f = sys.argv[4]
status_f    = sys.argv[5]
doctor_f    = sys.argv[6]
status_json_f = sys.argv[7] if len(sys.argv) > 7 else None
doctor_exit_f = sys.argv[8] if len(sys.argv) > 8 else None

# ── Changelog parse result ────────────────────────────────────────────────────
with open(changelog_f, 'r', encoding='utf-8') as f:
    cl = json.load(f)

changelog_delta      = cl.get('delta', '')
flagged_items        = cl.get('flagged', [])
latest_not_local     = cl.get('latest_not_local', False)
changelog_not_found  = cl.get('changelog_not_found', False)
changelog_empty      = cl.get('changelog_empty', False)
# Pass through semantic flags from parse step
same_version         = cl.get('same_version', False)
already_latest       = cl.get('already_latest', False)

# ── Update status output ──────────────────────────────────────────────────────
with open(status_f, 'r', encoding='utf-8') as f:
    update_status = f.read().strip()

update_meta = {}
if status_json_f:
    try:
        with open(status_json_f, 'r', encoding='utf-8') as f:
            raw_meta = json.load(f)
        update_meta = {
            "root": raw_meta.get("update", {}).get("root"),
            "install_kind": raw_meta.get("update", {}).get("installKind"),
            "package_manager": raw_meta.get("update", {}).get("packageManager")
                or raw_meta.get("update", {}).get("deps", {}).get("manager"),
            "channel": raw_meta.get("channel", {}).get("value"),
            "channel_label": raw_meta.get("channel", {}).get("label"),
            "available": raw_meta.get("availability", {}).get("available"),
        }
        update_meta = {k: v for k, v in update_meta.items() if v is not None}
    except Exception:
        update_meta = {}

# ── Doctor output analysis ────────────────────────────────────────────────────
with open(doctor_f, 'r', encoding='utf-8') as f:
    doctor_raw = f.read()

doctor_ok = True
doctor_issues = []
doctor_exit_code = None

if doctor_exit_f:
    try:
        with open(doctor_exit_f, 'r', encoding='utf-8') as f:
            doctor_exit_code = int(f.read().strip())
    except Exception:
        doctor_exit_code = None

if doctor_exit_code not in (None, 0):
    doctor_ok = False
    doctor_issues.append(f"openclaw doctor exited with code {doctor_exit_code}")

for line in doctor_raw.splitlines():
    stripped = line.strip()
    if not stripped:
        continue

    # Summary count lines (e.g. "Errors: 0", "Warnings: 2") are useful when
    # non-zero, but should not create false positives when zero.
    summary = re.search(r'(Errors|Warnings|Issues):\s*(\d+)', line, re.IGNORECASE)
    if summary:
        if int(summary.group(2)) > 0:
            doctor_ok = False
            doctor_issues.append(stripped)
        continue

    # Detect failure indicators
    has_fail = re.search(r'✗|\bfailed\b|\binvalid\b|\bunrecognized\b', line, re.IGNORECASE)
    has_error = re.search(r'\berror\b', line, re.IGNORECASE) and not re.search(r'Errors:\s*\d+', line)

    # `openclaw doctor` can exit successfully while still suggesting fixes.
    # Treat explicit fix guidance and common integrity/auth warnings as issues.
    has_fix_hint = re.search(r'Run "openclaw doctor --fix"|\bFix:\b', line)
    has_warning = re.search(
        r'\bmissing\b|Multiple state directories|orphan transcript|stale=yes',
        line,
        re.IGNORECASE,
    )

    if has_fail or has_error or has_fix_hint or has_warning:
        doctor_ok = False
        doctor_issues.append(stripped)

doctor_issues = doctor_issues[:10]  # cap at 10 entries

# ── Rollback command candidates ───────────────────────────────────────────────
# Rollbacks can be downgrades and may restart the Gateway again. Expose only a
# preview command and a manually-confirmed execute path (no implicit --yes).
rollback_dry_run_cmd = f"openclaw update --dry-run --tag {current}"
rollback_execute_cmd = f"openclaw update --tag {current}"

# ── Final output ─────────────────────────────────────────────────────────────
result = {
    "current_version":      current,
    "latest_version":       latest,
    "has_update":           has_update,
    "same_version":         same_version,
    "already_latest":       already_latest,
    "rollback_cmd":         rollback_dry_run_cmd,
    "rollback_dry_run_cmd": rollback_dry_run_cmd,
    "rollback_execute_cmd": rollback_execute_cmd,
    "latest_not_local":     latest_not_local,
    "changelog_not_found":  changelog_not_found,
    "changelog_empty":      changelog_empty,
    "update_status":        update_status,
    "update_meta":          update_meta,
    "doctor_ok":            doctor_ok,
    "doctor_exit_code":     doctor_exit_code,
    "doctor_issues":        doctor_issues,
    "flagged_count":        len(flagged_items),
    "flagged_items":        flagged_items,
    "changelog_delta":      changelog_delta,
}

print(json.dumps(result, ensure_ascii=False, indent=2))
