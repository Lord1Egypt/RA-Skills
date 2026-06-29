from __future__ import annotations

import argparse
import json

import chat_context
import system_config as sc
from utils import json_fail


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


PERSONAL_WORDS = ["我的", "我之前", "我存", "个人", "我自己的", "我的资料", "我的笔记"]
GROUP_PERSONAL_WORDS = ["我的", "我之前", "我存", "个人", "我自己的", "我的资料", "我的笔记"]
TEAM_WORDS = ["我们", "团队", "组会", "项目", "同学", "成员"]


def find_project_id(question: str, team: dict) -> str:
    for pid, project in team.get("projects", {}).items():
        if pid in question or project.get("name", "") in question:
            return pid
    return ""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--open_id", default="", help="Backward-compatible alias for SenderId.")
    parser.add_argument("--sender_id", default="", help="OpenClaw SenderId: the message sender open_id.")
    parser.add_argument("--chat_type", default="", help="OpenClaw ChatType: direct/group.")
    parser.add_argument("--chat_id", default="", help="OpenClaw GroupSubject in group chats.")
    parser.add_argument("--question", required=True)
    parser.add_argument("--scope", default="", choices=["", "personal", "team", "both"])
    args = parser.parse_args()

    sender_id = chat_context.actor_id(args.open_id, args.sender_id)
    if not sender_id:
        out(json_fail("missing_sender_id", "缺少 SenderId，不能识别用户。"))
        return

    chat_type = chat_context.normalize_chat_type(args.chat_type)
    q = args.question

    if chat_type == "group":
        group, error = chat_context.resolve_group_context(sender_id, args.chat_id)
        if error:
            out(error)
            return
        if args.scope in {"personal", "both"} or any(word in q for word in GROUP_PERSONAL_WORDS):
            out(json_fail("personal_scope_not_allowed_in_group", "群聊中不能查询个人知识库。请私聊我查询个人资料。"))
            return
        team = group["team"]
        out({
            "success": True,
            "chat_type": "group",
            "chat_id": args.chat_id,
            "scope": "team",
            "user": group["user"],
            "team": team,
            "binding": group["binding"],
            "project_id": find_project_id(q, team),
            "personal_kb": None,
            "team_kb": {
                "owner": team.get("team_kb_owner"),
                "repo": team.get("team_kb_repo"),
            },
        })
        return

    users = sc.users()
    user = users.get(sender_id)
    if not user:
        out(json_fail("user_not_registered", "请先完成个人知识库初始化。"))
        return

    teams = sc.teams()
    team = teams.get(user.get("team_id", ""))
    has_team = bool(team)

    scope = args.scope
    if not scope:
        if any(w in q for w in PERSONAL_WORDS) and any(w in q for w in TEAM_WORDS):
            scope = "both" if has_team else "personal"
        elif any(w in q for w in TEAM_WORDS):
            scope = "team" if has_team else "personal"
        elif any(w in q for w in PERSONAL_WORDS):
            scope = "personal"
        else:
            scope = "both" if has_team else "personal"

    if scope in {"team", "both"} and not has_team:
        scope = "personal"

    out({
        "success": True,
        "chat_type": chat_type or "direct",
        "chat_id": args.chat_id,
        "scope": scope,
        "user": user,
        "team": team,
        "project_id": find_project_id(q, team) if has_team else "",
        "personal_kb": {
            "owner": user.get("personal_kb_owner") or user.get("gitea_username"),
            "repo": user.get("personal_kb_repo"),
        },
        "team_kb": ({
            "owner": team.get("team_kb_owner"),
            "repo": team.get("team_kb_repo"),
        } if team else None),
    })


if __name__ == "__main__":
    main()
