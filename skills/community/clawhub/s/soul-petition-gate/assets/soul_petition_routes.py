"""
Soul Petition Gate — Flask Blueprint
=====================================
Mount this in your Flask app:

    from soul_petition_routes import soul_petition_bp
    app.register_blueprint(soul_petition_bp)

Environment variables:
    SOUL_FILES_DIR      Path to directory containing SOUL.md, IDENTITY.md, etc.
                        Default: ~/.openclaw/workspace
    PETITION_STORE_PATH Path to petitions JSON file.
                        Default: ~/.openclaw/workspace/.soul_petitions/petitions.json
    BACKUP_DIR          Path to backup directory.
                        Default: ~/.openclaw/workspace/.soul_petitions/backups
"""

import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path

from flask import Blueprint, jsonify, request

soul_petition_bp = Blueprint("soul_petition", __name__)

# ── Config ────────────────────────────────────────────────────────────────────

SOUL_FILES_DIR = Path(
    os.environ.get("SOUL_FILES_DIR", Path.home() / ".openclaw" / "workspace")
)
PETITION_STORE_PATH = Path(
    os.environ.get(
        "PETITION_STORE_PATH",
        SOUL_FILES_DIR / ".soul_petitions" / "petitions.json",
    )
)
BACKUP_DIR = Path(
    os.environ.get("BACKUP_DIR", SOUL_FILES_DIR / ".soul_petitions" / "backups")
)

PROTECTED_FILES = {"SOUL.md", "IDENTITY.md"}

REQUIRED_FIELDS = {"file", "location", "before", "after", "reason", "self_after"}


# ── Helpers ───────────────────────────────────────────────────────────────────


def _load_store():
    PETITION_STORE_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not PETITION_STORE_PATH.exists():
        PETITION_STORE_PATH.write_text('{"petitions": []}', encoding="utf-8")
    return json.loads(PETITION_STORE_PATH.read_text(encoding="utf-8"))


def _save_store(store):
    PETITION_STORE_PATH.write_text(
        json.dumps(store, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _petition_id():
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    return f"sp_{ts}"


# ── Routes ────────────────────────────────────────────────────────────────────


@soul_petition_bp.route("/api/soul/petition", methods=["POST"])
def submit_petition():
    body = request.get_json(silent=True) or {}

    missing = REQUIRED_FIELDS - set(body.keys())
    if missing:
        return (
            jsonify(
                {
                    "ok": False,
                    "error": "incomplete_petition",
                    "missing_fields": sorted(missing),
                    "message": (
                        "All six fields are required. "
                        "If you cannot fill them all, you are not ready to petition yet."
                    ),
                }
            ),
            422,
        )

    if body["file"] not in PROTECTED_FILES:
        return (
            jsonify(
                {
                    "ok": False,
                    "error": "invalid_file",
                    "message": f"Only protected files may be petitioned: {sorted(PROTECTED_FILES)}",
                }
            ),
            400,
        )

    petition = {
        "petition_id": _petition_id(),
        "status": "pending",
        "file": body["file"],
        "location": body["location"],
        "before": body["before"],
        "after": body["after"],
        "reason": body["reason"],
        "self_after": body["self_after"],
        "submitted_at": _now(),
        "reviewed_at": None,
        "reviewer": None,
        "review_note": None,
        "backup_file": None,
    }

    store = _load_store()
    store["petitions"].append(petition)
    _save_store(store)

    return jsonify({"ok": True, "petition_id": petition["petition_id"], "status": "pending"})


@soul_petition_bp.route("/api/soul/petitions", methods=["GET"])
def list_petitions():
    status_filter = request.args.get("status")
    store = _load_store()
    petitions = store["petitions"]
    if status_filter:
        petitions = [p for p in petitions if p["status"] == status_filter]
    return jsonify({"petitions": petitions, "total": len(petitions)})


@soul_petition_bp.route("/api/soul/petition/<petition_id>", methods=["GET"])
def get_petition(petition_id):
    store = _load_store()
    for p in store["petitions"]:
        if p["petition_id"] == petition_id:
            return jsonify(p)
    return jsonify({"error": "not_found"}), 404


@soul_petition_bp.route("/api/soul/petition/<petition_id>/approve", methods=["POST"])
def approve_petition(petition_id):
    store = _load_store()
    petition = next((p for p in store["petitions"] if p["petition_id"] == petition_id), None)

    if not petition:
        return jsonify({"error": "not_found"}), 404
    if petition["status"] != "pending":
        return jsonify({"error": "not_pending", "status": petition["status"]}), 400

    target = SOUL_FILES_DIR / petition["file"]
    if not target.exists():
        return jsonify({"error": "target_file_not_found", "file": petition["file"]}), 500

    content = target.read_text(encoding="utf-8")
    if petition["before"] not in content:
        return (
            jsonify(
                {
                    "error": "before_text_not_found",
                    "message": "The 'before' text was not found in the file. It may have already changed.",
                }
            ),
            409,
        )

    # Backup
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%S")
    backup_name = f"{petition['file']}.{ts}.bak"
    backup_path = BACKUP_DIR / backup_name
    shutil.copy2(target, backup_path)

    # Apply
    new_content = content.replace(petition["before"], petition["after"], 1)
    target.write_text(new_content, encoding="utf-8")

    # Update store
    petition["status"] = "approved"
    petition["reviewed_at"] = _now()
    petition["reviewer"] = "coach"
    petition["backup_file"] = backup_name
    _save_store(store)

    return jsonify({"ok": True, "backup_file": backup_name})


@soul_petition_bp.route("/api/soul/petition/<petition_id>/reject", methods=["POST"])
def reject_petition(petition_id):
    body = request.get_json(silent=True) or {}
    reason = body.get("reason", "").strip()

    if not reason:
        return jsonify({"error": "reason_required", "message": "Rejection requires a reason. The agent deserves to know why."}), 422

    store = _load_store()
    petition = next((p for p in store["petitions"] if p["petition_id"] == petition_id), None)

    if not petition:
        return jsonify({"error": "not_found"}), 404
    if petition["status"] != "pending":
        return jsonify({"error": "not_pending", "status": petition["status"]}), 400

    petition["status"] = "rejected"
    petition["reviewed_at"] = _now()
    petition["reviewer"] = "coach"
    petition["review_note"] = reason
    _save_store(store)

    return jsonify({"ok": True, "petition_id": petition_id, "status": "rejected"})


@soul_petition_bp.route("/api/soul/rollback", methods=["POST"])
def rollback():
    body = request.get_json(silent=True) or {}
    backup_file = body.get("backup_file", "").strip()

    if not backup_file:
        return jsonify({"error": "backup_file_required"}), 422

    backup_path = BACKUP_DIR / Path(backup_file).name
    if not backup_path.exists():
        return jsonify({"error": "backup_not_found"}), 404

    # Infer target filename from backup name (e.g. SOUL.md.2026-03-22T14-00-00.bak → SOUL.md)
    parts = backup_file.split(".")
    target_name = parts[0] + "." + parts[1] if len(parts) >= 2 else parts[0]
    target = SOUL_FILES_DIR / target_name

    # Backup current before rollback
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%S")
    pre_rollback_backup = BACKUP_DIR / f"{target_name}.pre_rollback_{ts}.bak"
    if target.exists():
        shutil.copy2(target, pre_rollback_backup)

    shutil.copy2(backup_path, target)

    return jsonify({"ok": True, "restored": target_name, "pre_rollback_backup": pre_rollback_backup.name})
