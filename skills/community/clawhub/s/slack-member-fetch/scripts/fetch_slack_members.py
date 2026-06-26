#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request

SLACK_API_BASE = "https://slack.com/api"


def slack_get(method: str, token: str, params: dict | None = None) -> dict:
    params = params or {}
    url = f"{SLACK_API_BASE}/{method}"
    if params:
        url += "?" + urllib.parse.urlencode(params)

    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        method="GET",
    )

    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body)
    except Exception as e:
        return {"ok": False, "error": f"http_error: {e}"}


def paginate(method: str, token: str, data_key: str, base_params: dict | None = None, limit: int = 200):
    base_params = base_params or {}
    cursor = None

    while True:
        params = dict(base_params)
        params["limit"] = limit
        if cursor:
            params["cursor"] = cursor

        data = slack_get(method, token, params)
        if not data.get("ok"):
            raise RuntimeError(data.get("error", "unknown_error"))

        for item in data.get(data_key, []):
            yield item

        cursor = (data.get("response_metadata") or {}).get("next_cursor")
        if not cursor:
            break


def build_user_record(user: dict) -> dict:
    profile = user.get("profile", {}) or {}
    return {
        "user_id": user.get("id"),
        "username": user.get("name"),
        "real_name": user.get("real_name"),
        "display_name": profile.get("display_name"),
        "email": profile.get("email"),
        "title": profile.get("title"),
        "timezone": user.get("tz"),
        "is_admin": bool(user.get("is_admin")),
        "is_owner": bool(user.get("is_owner")),
        "is_bot": bool(user.get("is_bot")),
        "deleted": bool(user.get("deleted")),
    }


def fetch_workspace_users(token: str) -> list[dict]:
    return list(paginate("users.list", token, "members"))


def fetch_workspace_members(token: str) -> list[dict]:
    return [build_user_record(u) for u in fetch_workspace_users(token)]


def fetch_channel_member_ids(token: str, channel_id: str) -> list[str]:
    return list(
        paginate(
            "conversations.members",
            token,
            "members",
            base_params={"channel": channel_id},
        )
    )


def find_channel_id_by_name(token: str, channel_name: str) -> str:
    normalized = channel_name.lstrip("#").strip().lower()
    channels = paginate(
        "conversations.list",
        token,
        "channels",
        base_params={
            "exclude_archived": "true",
            "types": "public_channel,private_channel",
        },
    )

    for channel in channels:
        if str(channel.get("name", "")).lower() == normalized:
            return channel.get("id")

    raise RuntimeError(f"channel_not_found: {channel_name}")


def fetch_channel_members(token: str, channel_id: str) -> list[dict]:
    member_ids = set(fetch_channel_member_ids(token, channel_id))
    workspace_users = fetch_workspace_users(token)

    return [
        build_user_record(user)
        for user in workspace_users
        if user.get("id") in member_ids
    ]


def main():
    parser = argparse.ArgumentParser(description="Fetch Slack workspace or channel member info.")
    parser.add_argument("--workspace", action="store_true", help="Fetch all workspace members")
    parser.add_argument("--channel", help="Slack channel/conversation ID, e.g. C0123456789")
    parser.add_argument("--channel-name", help="Slack channel name, e.g. general")
    parser.add_argument("--out", help="Write JSON output to a file")
    parser.add_argument("--include-deleted", action="store_true", help="Include deactivated users")
    parser.add_argument("--include-bots", action="store_true", help="Include bot users")
    args = parser.parse_args()

    token = os.environ.get("SLACK_BOT_TOKEN")
    if not token:
        print(json.dumps({
            "ok": False,
            "error": "missing_env",
            "message": "SLACK_BOT_TOKEN is not set"
        }, indent=2))
        sys.exit(1)

    selected = [bool(args.workspace), bool(args.channel), bool(args.channel_name)]
    if sum(selected) != 1:
        print(json.dumps({
            "ok": False,
            "error": "invalid_args",
            "message": "Use exactly one of --workspace, --channel, or --channel-name"
        }, indent=2))
        sys.exit(1)

    try:
        channel_id = None
        channel_name = None

        if args.workspace:
            members = fetch_workspace_members(token)
            source = "workspace"
        else:
            if args.channel_name:
                channel_name = args.channel_name.lstrip("#").strip()
                channel_id = find_channel_id_by_name(token, channel_name)
            else:
                channel_id = args.channel
            members = fetch_channel_members(token, channel_id)
            source = "channel"

        if not args.include_deleted:
            members = [m for m in members if not m.get("deleted")]

        if not args.include_bots:
            members = [m for m in members if not m.get("is_bot")]

        result = {
            "ok": True,
            "source": source,
            "channel_id": channel_id,
            "channel_name": channel_name,
            "count": len(members),
            "members": members,
        }

        output = json.dumps(result, indent=2, ensure_ascii=False)

        if args.out:
            with open(args.out, "w", encoding="utf-8") as f:
                f.write(output)

        print(output)

    except Exception as e:
        print(json.dumps({
            "ok": False,
            "error": "runtime_error",
            "message": str(e)
        }, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
