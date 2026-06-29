from __future__ import annotations

import system_config as sc


def can_scan_source(open_id: str, source: dict) -> tuple[bool, str]:
    if open_id in {"", "system"}:
        return True, ""
    user = sc.users().get(open_id)
    if not user:
        return False, "user_not_registered"
    if source.get("target_scope") == "personal":
        if source.get("target_kb_owner") == user.get("personal_kb_owner") and source.get("target_kb_repo") == user.get("personal_kb_repo"):
            return True, ""
        if source.get("created_by") == open_id:
            return True, ""
        return False, "not_personal_source_owner"
    if source.get("target_scope") == "team":
        team_id = source.get("target_team_id", "")
        team = sc.teams().get(team_id)
        if not team:
            return False, "team_not_found"
        if user.get("team_id") != team_id or open_id not in team.get("members", []):
            return False, "not_team_member"
        return True, ""
    return False, "bad_target_scope"


def can_config_source(open_id: str, source: dict) -> tuple[bool, str]:
    if open_id in {"", "system"}:
        return True, ""
    user = sc.users().get(open_id)
    if not user:
        return False, "user_not_registered"
    if source.get("target_scope") == "personal":
        return can_scan_source(open_id, source)
    if source.get("target_scope") == "team":
        team = sc.teams().get(source.get("target_team_id", ""))
        if not team:
            return False, "team_not_found"
        if open_id not in team.get("admins", []):
            return False, "team_source_requires_admin"
        return True, ""
    return False, "bad_target_scope"
