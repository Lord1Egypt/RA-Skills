#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

DEFAULT_PROFILE = {
    "project_name": "x-growth-project",
    "primary_language": "en",
    "secondary_languages": [],
    "niche_summary": "AI, agents, automation",
    "daily_min": 2,
    "daily_max": 5,
    "monthly_cap": 300,
    "community_enabled": False,
    "community_platform": "",
    "community_link": "",
    "reply_cta_enabled": False,
    "reply_cta_style": "soft_contextual_end_of_reply",
    "source_branching_enabled": False,
    "source_branching_label": "",
    "bird_enabled": True,
    "x_api_enabled": True,
    "live_publish": False
}

README = """# x-growth-project

Reusable X growth automation scaffold.

## Default mode
- live publish disabled unless config says otherwise
- Bird for discovery
- X API for publishing
- no platform-specific community/source assumptions

## Customize first
- config/topics.json
- config/publish-policy.json
- config/budget-policy.json
- config/project-profile.json
- .env.example
- docs/operator-notes.md
"""

ENV_EXAMPLE = """X_API_KEY=
X_API_SECRET=
X_ACCESS_TOKEN=
X_ACCESS_TOKEN_SECRET=
AUTH_TOKEN=
CT0=
XGROWTH_DRY_RUN=true
XGROWTH_PUBLISH_ENABLED=false
"""

PROMPT = """# LLM Drafting Prompt

Write natural, X-native posts in the user's configured language.
If the project is multilingual, follow the primary language unless a workflow explicitly chooses another language.
Avoid hype, hashtags, and robotic phrasing.
Keep outputs mobile-readable and concise.
"""

STYLE = """# Style Rules

- natural
- concise
- X-native
- one main idea per post
- avoid hype and hashtags
- keep CTA separate unless policy explicitly allows it
- avoid platform-specific assumptions unless configured
"""

DOCTOR = """import json, pathlib
root = pathlib.Path.cwd()
print(json.dumps({\"ok\": True, \"project\": root.name}))
"""


def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", required=True)
    ap.add_argument("--profile-json", default="{}")
    args = ap.parse_args()

    profile = DEFAULT_PROFILE.copy()
    profile.update(json.loads(args.profile_json))

    root = Path(args.path)
    root.mkdir(parents=True, exist_ok=True)

    write(root / "README.md", README)
    write(root / ".env.example", ENV_EXAMPLE.replace("XGROWTH_DRY_RUN=true", f"XGROWTH_DRY_RUN={str(not profile.get('live_publish', False)).lower()}").replace("XGROWTH_PUBLISH_ENABLED=false", f"XGROWTH_PUBLISH_ENABLED={str(profile.get('live_publish', False)).lower()}"))
    write(root / "prompts" / "llm-drafting.md", PROMPT)
    write(root / "config" / "style-rules.md", STYLE)
    write(root / "docs" / "operator-notes.md", "Fill in operator decisions, niche choices, language rules, community integration, rollout notes, and reply-lane safety rules here.\n\nSuggested live-mode notes:\n- preferred reply sources (mentions only vs broader)\n- what counts as a permanent reply failure\n- whether failed replies should skip or fallback\n- where publish results are logged\n- anti-repetition window (for example last 48h similarity threshold)\n- idempotent slot-key design (stable fields only; never draft text)\n")
    write(root / "scripts" / "doctor.py", DOCTOR)

    write_json(root / "config" / "project-profile.json", {
        "primary_language": profile["primary_language"],
        "secondary_languages": profile["secondary_languages"],
        "niche_summary": profile["niche_summary"],
        "community": {
            "enabled": bool(profile["community_enabled"]),
            "platform": profile["community_platform"],
            "link": profile["community_link"]
        },
        "source_branching": {
            "enabled": bool(profile["source_branching_enabled"]),
            "label": profile["source_branching_label"]
        }
    })
    write_json(root / "config" / "topics.json", {
        "primary_language": profile["primary_language"],
        "secondary_languages": profile["secondary_languages"],
        "niche_summary": profile["niche_summary"],
        "searchQueries": [],
        "watchAccounts": []
    })
    write_json(root / "config" / "budget-policy.json", {
        "publishEnabled": bool(profile["live_publish"]),
        "dryRun": not bool(profile["live_publish"]),
        "hardMonthlyPublishCap": profile["monthly_cap"],
        "softMonthlyPublishCap": min(profile["monthly_cap"], max(profile["daily_max"] * 30, 60))
    })
    write_json(root / "config" / "publish-policy.json", {
        "cadence": {
            "dailyIdealMin": profile["daily_min"],
            "dailyIdealMax": profile["daily_max"],
            "monthlyHardCap": profile["monthly_cap"]
        },
        "community": {
            "enabled": bool(profile["community_enabled"]),
            "platform": profile["community_platform"],
            "link": profile["community_link"]
        },
        "replyCTA": {
            "enabled": bool(profile["reply_cta_enabled"]),
            "style": profile["reply_cta_style"]
        },
        "sourceBranching": {
            "enabled": bool(profile["source_branching_enabled"]),
            "label": profile["source_branching_label"]
        },
        "providers": {
            "bird": bool(profile["bird_enabled"]),
            "x_api": bool(profile["x_api_enabled"])
        }
    })

    for rel in [
        "data/raw/.gitkeep",
        "data/normalized/.gitkeep",
        "data/scored/.gitkeep",
        "data/queue/.gitkeep",
        "data/llm-drafts/.gitkeep",
        "reports/approval/.gitkeep",
        "reports/final/.gitkeep"
    ]:
        write(root / rel, "")

    print(json.dumps({
        "ok": True,
        "path": str(root),
        "live_publish": bool(profile["live_publish"]),
        "primary_language": profile["primary_language"],
        "secondary_languages": profile["secondary_languages"],
        "daily_range": [profile["daily_min"], profile["daily_max"]],
        "monthly_cap": profile["monthly_cap"]
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
