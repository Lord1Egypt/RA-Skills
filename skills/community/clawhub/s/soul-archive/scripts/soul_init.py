#!/usr/bin/env python3
"""
🧬 Soul Archive Initializer (Cross-platform)
Create the Soul Archive data directory and default configuration files.

The soul data is stored under the current user's home directory (~/.agent-commons/skills_data/soul-archive/)
so it can be accessed across different IDEs, AI tools, and workspaces on the same machine.

       7-axis schema (industry-aligned): Identity / Personality / Language /
       Knowledge / Memory / Workflow / Aspirations.
       Privacy is enforced by keeping data local and out of any VCS via .gitignore.

Usage:
  python soul_init.py [--soul-dir /custom/path]
  python3 soul_init.py

Works on: macOS, Linux, Windows
"""


# ── Windows console safety: force UTF-8 on stdout/stderr so Chinese / emoji
#    don't blow up under the default cp936 codec on Windows PowerShell / cmd.
#    No-op on POSIX terminals that are already UTF-8.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
    _sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


from soul_paths import resolve_soul_dir
DEFAULT_SOUL_DIR = resolve_soul_dir()


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")


def write_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description="🧬 灵魂存档初始化")
    parser.add_argument("--soul-dir", type=Path, default=DEFAULT_SOUL_DIR,
                        help=f"灵魂数据目录路径（默认: {DEFAULT_SOUL_DIR}）")
    args = parser.parse_args()

    soul_dir = args.soul_dir

    if (soul_dir / "profile.json").exists():
        print(f"⚠️  灵魂存档已存在于 {soul_dir}")
        print(f"   如需重新初始化，请先删除 {soul_dir} 目录")
        return

    print("🧬 正在初始化灵魂存档...")
    print(f"   路径: {soul_dir}")

    now = now_iso()

    # 7-axis schema: identity / personality / language / knowledge /
    #                memory (episodic+semantic+emotional) / workflow / aspirations
    dirs = [
        soul_dir / "identity",
        soul_dir / "memory" / "episodic",
        soul_dir / "memory" / "semantic",
        soul_dir / "memory" / "emotional",
        soul_dir / "style",
        soul_dir / "workflow",
        soul_dir / "reports",
        soul_dir / "agent" / "episodes",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    write_json(soul_dir / "profile.json", {
        "soul_version": "3.0",
        "created_at": now,
        "last_updated": now,
        "total_conversations": 0,
        "total_extractions": 0,
        "completeness_score": 0.0,
        "dimensions": {
            "identity": 0.0,
            "personality": 0.0,
            "language_style": 0.0,
            "knowledge": 0.0,
            "memory": 0.0,
            "workflow": 0.0,
            "aspirations": 0.0
        }
    })

    # config.json — minimal, no encryption fields
    config_data = {
        "privacy_level": "standard",
        "auto_extract": True,
        "auto_reflect": True,
        "auto_context_inject": True,
        "extract_dimensions": {
            "identity": True,
            "personality": True,
            "language_style": True,
            "knowledge": True,
            "episodic_memory": True,
            "emotional_patterns": True,
            "workflow": True,
            "aspirations": True
        },
        "agent_self_improvement": {
            "enabled": True,
            "auto_reflect_on_completion": True,
            "auto_critique_on_correction": True,
            "pattern_extraction": True,
            "recall_on_task_start": True,
            "warn_on_failure_pattern_match": True,
            "auto_distill_threshold": 5
        },
        "deduplication": {
            "enabled": True,
            "similarity_threshold": 0.85
        },
        "sensitive_topics_filter": True,
        "require_confirmation_for": ["health", "finance", "intimate_relationships"],
        "data_retention_days": None
    }
    write_json(soul_dir / "config.json", config_data)

    # identity/basic_info.json
    write_json(soul_dir / "identity" / "basic_info.json", {
        "name": None, "nickname": None, "age": None, "birth_year": None,
        "gender": None, "location": None, "hometown": None,
        "occupation": None, "company": None, "education": None,
        "languages": [], "hobbies": [], "self_description": None, "life_motto": None,
        "daily_routine": None, "sleep_schedule": None,
        "food_preferences": [], "food_dislikes": [],
        "music_taste": [], "movie_taste": [], "book_taste": [],
        "travel_preferences": None, "pet_preference": None,
        "aesthetic_style": None, "spending_style": None,
        "online_personas": [], "favorite_apps": [], "social_platforms": [],
        "digital_habits": None, "tech_proficiency": None,
        "_meta": {}
    })

    # identity/personality.json
    write_json(soul_dir / "identity" / "personality.json", {
        "mbti": None,
        "big_five": {
            "openness": None, "conscientiousness": None,
            "extraversion": None, "agreeableness": None, "neuroticism": None
        },
        "traits": [], "values": [],
        "decision_style": None, "communication_preference": None,
        "strengths": [], "weaknesses": [],
        "risk_tolerance": None, "procrastination_level": None,
        "perfectionism_level": None, "planning_style": None,
        "learning_style": None, "work_style": None,
        "social_energy": None, "group_role": None,
        "trust_building": None, "conflict_approach": None,
        "stress_response": None, "motivation_drivers": [], "growth_areas": [],
        "_meta": {}
    })

    # style/language.json
    write_json(soul_dir / "style" / "language.json", {
        "catchphrases": [], "sentence_patterns": [],
        "preferred_words": [], "avoided_words": [],
        "emoji_usage": {"frequency": "unknown", "favorites": []},
        "punctuation_habits": {},
        "formality_level": None, "verbosity": None,
        "humor_style": None, "response_length_preference": None,
        "thinking_expression": None, "examples": [],
        "dialect_features": [], "filler_words": [],
        "persuasion_style": None, "storytelling_style": None,
        "question_style": None, "agreement_expressions": [],
        "disagreement_expressions": [],
        "greeting_style": None, "farewell_style": None,
        "typing_habits": None,
        "_meta": {}
    })

    # style/communication.json
    write_json(soul_dir / "style" / "communication.json", {
        "directness": None, "logic_vs_emotion": None,
        "detail_level": None, "listening_style": None,
        "conflict_style": None, "encouragement_style": None,
        "criticism_style": None, "_meta": {}
    })

    # memory/semantic/topics.json
    write_json(soul_dir / "memory" / "semantic" / "topics.json", {
        "topics": [], "_meta": {}
    })

    # memory/semantic/knowledge.json
    write_json(soul_dir / "memory" / "semantic" / "knowledge.json", {
        "domains": [], "skills": [], "expertise_level": {},
        "belief_frameworks": [],   # 信奉的方法论/思考框架
        "_meta": {}
    })

    # memory/emotional/patterns.json
    write_json(soul_dir / "memory" / "emotional" / "patterns.json", {
        "triggers": {
            "joy": [], "anger": [], "sadness": [], "anxiety": [],
            "excitement": [], "nostalgia": [], "pride": [], "gratitude": [],
            "frustration": [], "curiosity": [], "peace": [], "guilt": []
        },
        "expression_style": None, "emotional_range": None,
        "emotional_awareness": None, "empathy_level": None,
        "coping_mechanisms": [], "comfort_activities": [],
        "celebration_style": None, "_meta": {}
    })

    # workflow/preferences.json
    write_json(soul_dir / "workflow" / "preferences.json", {
        "tools": {
            "ide": [], "terminal": [], "ai_tools": [],
            "vcs": [], "doc_systems": [], "communication": []
        },
        "tech_stack": {
            "languages": [], "frameworks": [], "platforms": []
        },
        "hard_rules": [],            # 用户明示的"必须/禁止"（如"禁止 git rebase"）
        "collab_conventions": [],    # 审核流程、commit 风格、分享平台等
        "cli_habits": [],            # 偏好的命令/别名/脚本风格
        "output_preferences": {      # 输出格式偏好（合并自 ChatGPT custom instructions）
            "preferred_format": None,    # 表格/列表/段落
            "preferred_length": None,    # 简短/中等/详尽
            "preferred_tone": None,      # 直接/温和/活泼
            "structure_first": None      # 是否要求"结论先行"
        },
        "pet_peeves": [],            # 反感的事：被铺垫、冗长解释、AI 自我介绍等
        "_meta": {}
    })

    # aspirations.json
    write_json(soul_dir / "aspirations.json", {
        "long_term_goals": [],          # 长期目标：职业、生活、技能
        "active_projects": [],          # 正在做的项目（含状态/期望）
        "identity_aspirations": [],     # 想成为什么样的人
        "skills_to_learn": [],          # 想学但还没学的
        "knowledge_gaps": [],           # 频繁提问/承认不懂的领域（"认知盲区"）
        "_meta": {}
    })

    # agent/patterns.json — AI 自我学习
    write_json(soul_dir / "agent" / "patterns.json", {
        "patterns": {},
        "_meta": {"description": "AI behavioral patterns learned from experience"}
    })

    for fname in ("corrections.jsonl", "reflections.jsonl"):
        f = soul_dir / "agent" / fname
        if not f.exists():
            f.touch()

    changelog = soul_dir / "soul_changelog.jsonl"
    if not changelog.exists():
        changelog.touch()

    gitignore = soul_dir / ".gitignore"
    gitignore.write_text(
        "# Soul archive data -- highly private, never commit to VCS\n*\n!.gitignore\n",
        encoding="utf-8"
    )

    print()
    print("✅ 灵魂存档初始化完成！")
    print()
    print(f"   📂 数据目录: {soul_dir}")
    print(f"   📋 配置文件: {soul_dir / 'config.json'}")
    print(f"   🔒 隐私: 全部本地明文 JSON，不上传任何云端")
    print(f"   🧬 7 维 schema: identity / personality / language / knowledge / memory / workflow / aspirations")
    print()
    print("   下一步:")
    print('   1. 开始与 AI 对话，灵魂存档会按 auto_extract 配置静默采集')
    print('   2. 随时说 "灵魂报告" 查看人格画像')
    print('   3. 说 "灵魂对话" 让克隆体跟别人聊天')
    print('   4. agent 可调用 soul_context.py 在对话开始时加载人格摘要')


if __name__ == "__main__":
    main()
