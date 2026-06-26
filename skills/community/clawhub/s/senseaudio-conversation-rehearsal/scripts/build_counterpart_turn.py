#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path


PHASE_QUESTIONS = {
    "opening": {
        "strict_manager": "先别铺垫，直接说结论。你凭什么觉得自己已经到了更高一级？",
        "senior_executive": "我只听重点。你先用一句话告诉我，这次你想争取什么。",
        "cross_team_peer": "你先把目标讲清楚，不然后面很难对齐。",
        "mentor_reviewer": "先讲结论，再讲你最有说服力的一条证据。",
    },
    "pushback": {
        "strict_manager": "这些更像过程，不像结果。你的影响到底体现在哪？",
        "senior_executive": "如果拿掉你自己主观判断，客观结果还剩什么？",
        "cross_team_peer": "这会不会只是你团队内部视角，别的团队为什么要买账？",
        "mentor_reviewer": "你说得还不够硬。换成可以被质询也站得住的说法。",
    },
    "pressure_question": {
        "strict_manager": "如果我现在就问你一个薄弱点，你最担心我问什么？你怎么回答？",
        "senior_executive": "假设我只给你三十秒，你要怎么让我相信这不是提前要头衔？",
        "cross_team_peer": "如果资源不增加，你凭什么还能保证结果？",
        "mentor_reviewer": "你现在的表达还是偏软，收紧一点，再来一次。",
    },
    "close": {
        "strict_manager": "最后一次机会，直接告诉我你要什么，以及我为什么现在该给你。",
        "senior_executive": "结尾别散。你的请求是什么，时间点是什么？",
        "cross_team_peer": "你希望我现在具体做什么支持？",
        "mentor_reviewer": "用一句最有力的话收尾，不要再解释。",
    },
}


def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def assess_reply(text: str) -> list[str]:
    notes = []
    if len(text) > 120:
        notes.append("回复偏长")
    if "我觉得" in text or "可能" in text or "其实" in text:
        notes.append("有缓冲词")
    if not re.search(r"\d", text) and all(marker not in text for marker in ["结果", "提升", "数据", "指标"]):
        notes.append("缺少证据")
    if all(marker not in text for marker in ["我希望", "我需要", "我的请求", "希望这次", "我想争取"]):
        notes.append("请求不明确")
    return notes


def pick_phase(turn_index: int) -> str:
    order = ["opening", "pushback", "pressure_question", "close"]
    return order[min(turn_index, len(order) - 1)]


def build_turn(blueprint: dict, history: dict, user_reply: str = "") -> dict:
    counterpart_count = sum(1 for item in history.get("turns", []) if item.get("kind") == "counterpart")
    phase = pick_phase(counterpart_count)
    role = blueprint["counterpart"]["role"]
    base_prompt = PHASE_QUESTIONS.get(phase, {}).get(role, "你再讲清楚一点。")
    notes = assess_reply(user_reply) if user_reply else []
    challenge_prefix = ""
    if notes:
        challenge_prefix = "我先指出几个问题：{}。".format("、".join(notes))
    return {
        "turn_index": counterpart_count + 1,
        "phase": phase,
        "counterpart_text": clean(f"{challenge_prefix}{base_prompt}"),
        "assessment_notes": notes,
        "user_reply": user_reply,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the next counterpart turn for a rehearsal session.")
    parser.add_argument("--blueprint-json", required=True)
    parser.add_argument("--history-json", required=True)
    parser.add_argument("--user-reply-file", default="")
    parser.add_argument("--opening-only", action="store_true")
    parser.add_argument("--out-json", required=True)
    args = parser.parse_args()

    blueprint = load_json(args.blueprint_json)
    history = load_json(args.history_json)
    user_reply = ""
    if not args.opening_only:
        if not args.user_reply_file:
            raise SystemExit("Pass --user-reply-file or use --opening-only.")
        user_reply = Path(args.user_reply_file).read_text(encoding="utf-8").strip()
        if not user_reply:
            raise SystemExit("User reply is empty.")

    result = build_turn(blueprint, history, user_reply=user_reply)

    out = Path(args.out_json)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
