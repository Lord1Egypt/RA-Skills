#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path


SCENARIO_PACKS = {
    "performance_review": {
        "goal": "对结果负责，同时清楚说明成绩、问题和下一步。",
        "pressure_style": "会追问细节、责任归属和下一阶段承诺。",
        "risk_points": ["过度解释背景", "回避责任", "没有明确下一步"],
    },
    "promotion_defense": {
        "goal": "证明已经在做更高一级的工作，并明确提出晋升请求。",
        "pressure_style": "会质疑影响力、稳定性和组织价值。",
        "risk_points": ["只讲努力不讲影响", "没有数据", "结尾不敢提出请求"],
    },
    "manager_update": {
        "goal": "短时间内讲清进展、风险和需要的支持。",
        "pressure_style": "更关注结论、风险和阻塞，而不是过程。",
        "risk_points": ["铺垫过长", "没有结论先行", "没有明确 ask"],
    },
    "difficult_stakeholder": {
        "goal": "稳住情绪，守住边界，同时推动对齐。",
        "pressure_style": "会打断、施压、质疑专业度。",
        "risk_points": ["语气变弱", "被带着跑", "没有回到目标"],
    },
}


ROLE_STYLES = {
    "strict_manager": {
        "tone": "冷静、直接、重结果",
        "question_style": "短句追问，优先问结果、风险、责任和时间点",
        "challenge_level": "high",
    },
    "senior_executive": {
        "tone": "快节奏、只听重点",
        "question_style": "先结论，再证据，不耐烦细枝末节",
        "challenge_level": "high",
    },
    "cross_team_peer": {
        "tone": "理性但可能防御",
        "question_style": "关注资源、影响范围、边界和承诺",
        "challenge_level": "medium",
    },
    "mentor_reviewer": {
        "tone": "严格但建设性",
        "question_style": "会逼你说得更清楚，但不故意施压",
        "challenge_level": "medium",
    },
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a rehearsal blueprint for a simulated conversation skill.")
    parser.add_argument("--scenario", required=True, choices=sorted(SCENARIO_PACKS.keys()))
    parser.add_argument("--counterpart-role", required=True, choices=sorted(ROLE_STYLES.keys()))
    parser.add_argument("--relationship", default="manager")
    parser.add_argument("--topic", required=True)
    parser.add_argument("--desired-outcome", required=True)
    parser.add_argument("--fear-triggers", default="")
    parser.add_argument("--difficulty", choices=["low", "medium", "high"], default="medium")
    parser.add_argument("--voice-mode", choices=["proxy_voice", "authorized_clone"], default="proxy_voice")
    parser.add_argument("--voice-sample-path", default="")
    parser.add_argument("--authorized-voice-id", default="")
    parser.add_argument("--clone-consent", action="store_true")
    parser.add_argument("--out-json", required=True)
    args = parser.parse_args()

    scenario_pack = SCENARIO_PACKS[args.scenario]
    role_style = ROLE_STYLES[args.counterpart_role]
    if args.voice_mode == "authorized_clone":
        has_prepared_clone = bool(args.authorized_voice_id)
        has_clone_creation_inputs = bool(args.clone_consent and args.voice_sample_path)
        if not (has_prepared_clone or has_clone_creation_inputs):
            raise SystemExit(
                "authorized_clone requires either --authorized-voice-id, or both --clone-consent and --voice-sample-path"
            )

    phases = [
        {"phase": "opening", "counterpart_goal": "先听结论，再判断你是否清楚。"},
        {"phase": "pushback", "counterpart_goal": "针对你的薄弱点追问。"},
        {"phase": "pressure_question", "counterpart_goal": "测试你在压力下是否还能讲清重点。"},
        {"phase": "close", "counterpart_goal": "看你是否能明确下一步和请求。"},
    ]

    result = {
        "scenario": args.scenario,
        "topic": args.topic,
        "relationship": args.relationship,
        "desired_outcome": args.desired_outcome,
        "fear_triggers": [x.strip() for x in args.fear_triggers.split(",") if x.strip()],
        "difficulty": args.difficulty,
        "voice_policy": {
            "mode": args.voice_mode,
            "voice_sample_path": args.voice_sample_path,
            "authorized_voice_id": args.authorized_voice_id,
            "clone_consent": args.clone_consent,
            "safe_default": args.voice_mode == "proxy_voice",
        },
        "counterpart": {
            "role": args.counterpart_role,
            "tone": role_style["tone"],
            "question_style": role_style["question_style"],
            "challenge_level": role_style["challenge_level"],
        },
        "rehearsal_goal": scenario_pack["goal"],
        "pressure_style": scenario_pack["pressure_style"],
        "known_risk_points": scenario_pack["risk_points"],
        "phases": phases,
        "debrief_focus": [
            "是否先讲结论",
            "是否有明确请求",
            "是否用了证据",
            "是否过度道歉或示弱",
            "是否在压力下失去结构",
        ],
    }

    out = Path(args.out_json)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
