#!/usr/bin/env python3
"""
Raon OS — Gamification Engine
XP, 레벨, 뱃지 관리 시스템
"""

import json
import os
from datetime import date, datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
PROFILE_PATH = os.path.join(BASE_DIR, "user_profile.json")

# XP 테이블
XP_TABLE = {
    "evaluate": 20,
    "improve": 20,
    "re_evaluate_bonus": 30,
    "score_improve_10": 50,
    "match": 15,
    "draft": 25,
    "checklist_complete": 40,
    "valuation": 10,
    "idea": 10,
    "streak_7day": 100,
    "first_80_score": 200,
}

# 레벨 테이블
LEVELS = [
    (0, "🌱 예비창업자"),
    (100, "🌿 초기창업자"),
    (300, "🌳 성장기업"),
    (600, "🚀 스케일업"),
    (1000, "⭐ 유니콘"),
]

# 뱃지
BADGES = {
    "first_eval": {"name": "🏆 첫 평가", "desc": "첫 사업계획서 평가 완료"},
    "growth_king": {"name": "📈 성장왕", "desc": "재평가로 20점 이상 향상"},
    "match_master": {"name": "🎯 매칭 마스터", "desc": "3개 프로그램 매칭"},
    "draft_artisan": {"name": "📝 지원서 장인", "desc": "지원서 3개 생성"},
    "streak_7": {"name": "🔥 7일 연속", "desc": "일주일 연속 사용"},
    "club_90": {"name": "💎 90점 클럽", "desc": "평가 90점 이상 달성"},
}


def _default_profile():
    return {
        "xp": 0,
        "level": 1,
        "title": "🌱 예비창업자",
        "badges": [],
        "stats": {"evaluate": 0, "improve": 0, "match": 0, "draft": 0, "checklist": 0, "valuation": 0, "idea": 0},
        "scores": [],
        "streak_days": [],
        "created": date.today().isoformat(),
    }


def load_profile(path=None):
    p = path or PROFILE_PATH
    try:
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        # ensure all keys exist
        default = _default_profile()
        for k, v in default.items():
            if k not in data:
                data[k] = v
        if isinstance(data.get("stats"), dict):
            for sk, sv in default["stats"].items():
                if sk not in data["stats"]:
                    data["stats"][sk] = sv
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        return _default_profile()


def save_profile(profile, path=None):
    p = path or PROFILE_PATH
    with open(p, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)


def get_level(xp):
    """Return (level_number, title) for given XP."""
    level_num = 1
    title = LEVELS[0][1]
    for i, (threshold, t) in enumerate(LEVELS):
        if xp >= threshold:
            level_num = i + 1
            title = t
    return level_num, title


def get_next_level_xp(xp):
    """Return XP needed for next level, or None if max."""
    for threshold, _ in LEVELS:
        if xp < threshold:
            return threshold
    return None


def check_badges(profile, action, context=None):
    """Check and award badges. Returns list of newly earned badge ids."""
    context = context or {}
    new_badges = []
    earned = profile.get("badges", [])

    # first_eval
    if action == "evaluate" and "first_eval" not in earned:
        new_badges.append("first_eval")

    # club_90
    score = context.get("score")
    if score is not None and score >= 90 and "club_90" not in earned:
        new_badges.append("club_90")

    # growth_king: 재평가로 20점 이상 향상
    score_improvement = context.get("score_improvement")
    if score_improvement is not None and score_improvement >= 20 and "growth_king" not in earned:
        new_badges.append("growth_king")

    # match_master: 3개 프로그램 매칭
    if action == "match" and profile.get("stats", {}).get("match", 0) >= 3 and "match_master" not in earned:
        new_badges.append("match_master")

    # draft_artisan: 지원서 3개 생성
    if action == "draft" and profile.get("stats", {}).get("draft", 0) >= 3 and "draft_artisan" not in earned:
        new_badges.append("draft_artisan")

    # streak_7
    if len(profile.get("streak_days", [])) >= 7 and "streak_7" not in earned:
        new_badges.append("streak_7")

    return new_badges


def check_streak(profile):
    """Update streak_days with today and return current streak length."""
    today = date.today().isoformat()
    days = profile.get("streak_days", [])

    if today not in days:
        days.append(today)

    # Sort and compute consecutive days ending today
    days_sorted = sorted(set(days))
    profile["streak_days"] = days_sorted

    if not days_sorted or days_sorted[-1] != today:
        return 0

    streak = 1
    for i in range(len(days_sorted) - 1, 0, -1):
        curr = date.fromisoformat(days_sorted[i])
        prev = date.fromisoformat(days_sorted[i - 1])
        if (curr - prev).days == 1:
            streak += 1
        else:
            break

    return streak


def add_xp(action, context=None, profile_path=None):
    """
    Add XP for an action. Returns dict with xp_gained, new_badges, leveled_up, profile.
    """
    context = context or {}
    profile = load_profile(profile_path)

    xp_gained = 0
    old_level = profile["level"]

    # Base XP
    base_xp = XP_TABLE.get(action, 0)
    xp_gained += base_xp

    # Update stats
    stat_key = action if action in profile.get("stats", {}) else None
    if stat_key:
        profile["stats"][stat_key] = profile["stats"].get(stat_key, 0) + 1

    # Score tracking for evaluate
    score = context.get("score")
    if action == "evaluate" and score is not None:
        prev_scores = profile.get("scores", [])

        # Check score improvement
        if prev_scores:
            last_score = prev_scores[-1]
            improvement = score - last_score
            context["score_improvement"] = improvement

            if improvement > 0:
                xp_gained += XP_TABLE["re_evaluate_bonus"]
            if improvement >= 10:
                xp_gained += XP_TABLE["score_improve_10"]

        # First 80+ score
        if score >= 80 and not any(s >= 80 for s in prev_scores):
            xp_gained += XP_TABLE["first_80_score"]

        profile["scores"].append(score)

    # Streak
    streak = check_streak(profile)
    if streak >= 7 and streak % 7 == 0:
        xp_gained += XP_TABLE["streak_7day"]

    # Apply XP
    profile["xp"] = profile.get("xp", 0) + xp_gained
    new_level, new_title = get_level(profile["xp"])
    profile["level"] = new_level
    profile["title"] = new_title

    leveled_up = new_level > old_level

    # Badges
    new_badges = check_badges(profile, action, context)
    for b in new_badges:
        if b not in profile["badges"]:
            profile["badges"].append(b)

    save_profile(profile, profile_path)

    return {
        "xp_gained": xp_gained,
        "total_xp": profile["xp"],
        "level": new_level,
        "title": new_title,
        "leveled_up": leveled_up,
        "new_badges": [BADGES[b]["name"] for b in new_badges],
        "new_badge_ids": new_badges,
        "profile": profile,
    }


def format_profile(profile):
    """CLI-friendly profile display."""
    xp = profile.get("xp", 0)
    level, title = get_level(xp)
    next_xp = get_next_level_xp(xp)

    lines = []
    lines.append("🌅 라온 프로필")
    lines.append("=" * 40)
    lines.append(f"  칭호: {title}")
    lines.append(f"  레벨: {level}")
    lines.append(f"  XP: {xp}")
    if next_xp:
        lines.append(f"  다음 레벨까지: {next_xp - xp} XP")
    else:
        lines.append("  🎉 최고 레벨 달성!")

    badges = profile.get("badges", [])
    if badges:
        badge_names = [BADGES[b]["name"] for b in badges if b in BADGES]
        lines.append(f"\n  🏅 뱃지: {', '.join(badge_names)}")
    else:
        lines.append("\n  🏅 뱃지: (아직 없음)")

    stats = profile.get("stats", {})
    lines.append("\n  📊 통계:")
    lines.append(f"    평가: {stats.get('evaluate', 0)}회")
    lines.append(f"    매칭: {stats.get('match', 0)}회")
    lines.append(f"    지원서: {stats.get('draft', 0)}회")
    lines.append(f"    체크리스트: {stats.get('checklist', 0)}회")
    lines.append(f"    밸류에이션: {stats.get('valuation', 0)}회")

    streak = 0
    days = profile.get("streak_days", [])
    if days:
        today = date.today().isoformat()
        if days[-1] == today or (len(days) >= 1):
            # recalculate
            days_sorted = sorted(set(days))
            if days_sorted:
                streak = 1
                for i in range(len(days_sorted) - 1, 0, -1):
                    curr = date.fromisoformat(days_sorted[i])
                    prev = date.fromisoformat(days_sorted[i - 1])
                    if (curr - prev).days == 1:
                        streak += 1
                    else:
                        break
    lines.append(f"\n  🔥 연속 접속: {streak}일")

    scores = profile.get("scores", [])
    if scores:
        lines.append(f"  📈 최근 점수: {scores[-1]}점 (최고: {max(scores)}점)")

    return "\n".join(lines)


def format_xp_gain(xp_gained, new_badges=None, leveled_up=False, title=None):
    """Format XP gain result for CLI output."""
    lines = []
    if xp_gained > 0:
        lines.append(f"\n  ✨ +{xp_gained} XP 획득!")
    if leveled_up and title:
        lines.append(f"  🎉 레벨 업! → {title}")
    if new_badges:
        for b in new_badges:
            lines.append(f"  🏅 새 뱃지: {b}")
    return "\n".join(lines)


if __name__ == "__main__":
    import sys
    args = sys.argv[1:]

    if not args or args[0] in ("--help", "-h", "help"):
        print("Usage: gamification.py [profile|profile --json|reset]")
        sys.exit(0)

    if args[0] == "profile":
        profile = load_profile()
        if "--json" in args:
            print(json.dumps(profile, ensure_ascii=False, indent=2))
        else:
            print(format_profile(profile))
    elif args[0] == "reset":
        save_profile(_default_profile())
        print("✅ 프로필 초기화 완료")
    else:
        print(f"Unknown command: {args[0]}")
        sys.exit(1)
