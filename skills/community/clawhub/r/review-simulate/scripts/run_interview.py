#!/usr/bin/env python3
"""Run a Chinese voice interview simulation with LLM, ASR, and TTS."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

import requests
from openai import OpenAI

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    load_dotenv = None

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
OUTPUT_DIR = SKILL_DIR / "outputs"

LLM_BASE_URL = ""
LLM_MODEL = ""
LLM_API_KEY = ""
LLM_TIMEOUT = 60.0
LLM_TEMPERATURE = 0.3

ASR_URL = ""
ASR_MODEL = ""
ASR_API_KEY = ""
ASR_TIMEOUT = 300.0
ASR_RESPONSE_FORMAT = "verbose_json"

TTS_URL = ""
TTS_MODEL = ""
TTS_API_KEY = ""
TTS_VOICE_ID = "male_0004_a"
TTS_TIMEOUT = 60.0

OPENING_SYSTEM_PROMPT = (
    "你是一名中文求职面试官。"
    "你需要为候选人生成真实、自然的模拟面试开场和第一问。"
    "只输出 JSON，不要输出 Markdown。"
)
EVALUATION_SYSTEM_PROMPT = (
    "你负责评估中文求职模拟面试中的单轮回答质量。"
    "评分是练习用途，不是正式招聘结论。"
    "只输出 JSON，不要输出 Markdown。"
)
DECISION_SYSTEM_PROMPT = (
    "你负责决定中文模拟面试下一步是追问、换题还是结束。"
    "必须严格遵守最小轮数和最大轮数限制。"
    "只输出 JSON，不要输出 Markdown。"
)
NEXT_QUESTION_SYSTEM_PROMPT = (
    "你是一名中文求职面试官，需要根据历史上下文生成下一问。"
    "每次只问一个问题。"
    "只输出 JSON，不要输出 Markdown。"
)
FINAL_REPORT_SYSTEM_PROMPT = (
    "你负责为中文求职模拟面试生成结构化最终报告。"
    "反馈要具体、可执行。"
    "只输出 JSON，不要输出 Markdown。"
)


def load_env() -> None:
    if load_dotenv is None:
        return
    for path in (SKILL_DIR / ".env", Path.cwd() / ".env"):
        if path.exists():
            load_dotenv(path)


def refresh_runtime_settings() -> None:
    global LLM_BASE_URL, LLM_MODEL, LLM_API_KEY, LLM_TIMEOUT, LLM_TEMPERATURE
    global ASR_URL, ASR_MODEL, ASR_API_KEY, ASR_TIMEOUT, ASR_RESPONSE_FORMAT
    global TTS_URL, TTS_MODEL, TTS_API_KEY, TTS_VOICE_ID, TTS_TIMEOUT

    LLM_BASE_URL = os.environ.get("INTERVIEW_LLM_BASE_URL", "https://models.audiozen.cn/v1")
    LLM_MODEL = os.environ.get("INTERVIEW_LLM_MODEL", "doubao-seed-2-0-lite-260215")
    LLM_API_KEY = os.environ.get("INTERVIEW_LLM_API_KEY", os.environ.get("IME_MODEL_API_KEY", ""))
    LLM_TIMEOUT = float(os.environ.get("INTERVIEW_LLM_TIMEOUT", "60"))
    LLM_TEMPERATURE = float(os.environ.get("INTERVIEW_LLM_TEMPERATURE", "0.3"))

    ASR_URL = os.environ.get("INTERVIEW_ASR_URL", "https://api.senseaudio.cn/v1/audio/transcriptions")
    ASR_MODEL = os.environ.get("INTERVIEW_ASR_MODEL", "sense-asr-pro")
    ASR_API_KEY = os.environ.get("INTERVIEW_ASR_API_KEY", os.environ.get("SENSEAUDIO_API_KEY", ""))
    ASR_TIMEOUT = float(os.environ.get("INTERVIEW_ASR_TIMEOUT", "300"))
    ASR_RESPONSE_FORMAT = os.environ.get("INTERVIEW_ASR_RESPONSE_FORMAT", "verbose_json")

    TTS_URL = os.environ.get("INTERVIEW_TTS_URL", "https://api.senseaudio.cn/v1/t2a_v2")
    TTS_MODEL = os.environ.get("INTERVIEW_TTS_MODEL", "SenseAudio-TTS-1.0")
    TTS_API_KEY = os.environ.get("INTERVIEW_TTS_API_KEY", os.environ.get("SENSEAUDIO_API_KEY", ""))
    TTS_VOICE_ID = os.environ.get("INTERVIEW_TTS_VOICE_ID", "male_0004_a")
    TTS_TIMEOUT = float(os.environ.get("INTERVIEW_TTS_TIMEOUT", "60"))


def require_env(name: str, value: str) -> str:
    if value:
        return value
    raise SystemExit(f"缺少必要配置: {name}")


def build_client() -> OpenAI:
    api_key = require_env("INTERVIEW_LLM_API_KEY / IME_MODEL_API_KEY", LLM_API_KEY)
    return OpenAI(api_key=api_key, base_url=LLM_BASE_URL, timeout=LLM_TIMEOUT)


def extract_message_content(response: Any) -> str:
    content = response.choices[0].message.content
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        text_parts = []
        for item in content:
            text = getattr(item, "text", None)
            if isinstance(text, str):
                text_parts.append(text)
            elif isinstance(item, dict) and isinstance(item.get("text"), str):
                text_parts.append(item["text"])
        return "".join(text_parts).strip()
    raise ValueError("模型响应缺少文本内容")


def extract_json(text: str) -> dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if len(lines) >= 3:
            text = "\n".join(lines[1:-1]).strip()
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError(f"模型未返回 JSON: {text}")
    return json.loads(text[start : end + 1])


def llm_json(system_prompt: str, user_prompt: str) -> dict[str, Any]:
    client = build_client()
    response = client.chat.completions.create(
        model=LLM_MODEL,
        temperature=LLM_TEMPERATURE,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return extract_json(extract_message_content(response))


def generate_opening(config: dict[str, Any]) -> dict[str, Any]:
    user_prompt = f"""输入信息：
- 目标岗位：{config['target_role']}
- 面试风格：{config['interviewer_style']}
- 语言：{config['language']}

请输出 JSON，字段包括：
- opening_text
- first_question
- question_type

要求：
- 开场自然，不要过度客套
- 第一个问题优先从 self_intro 或 motivation 中选择
- 每次只问一个问题
- 问题不超过两句话
"""
    return llm_json(OPENING_SYSTEM_PROMPT, user_prompt)


def evaluate_turn(question: str, question_type: str, answer: str, history_summary: str) -> dict[str, Any]:
    user_prompt = f"""输入：
- 当前问题：{question}
- 问题类型：{question_type}
- 用户回答：{answer}
- 历史摘要：{history_summary}

请输出 JSON，字段包括：
- relevance
- clarity
- specificity
- persuasiveness
- brief_comment
- gap_summary

要求：
- 四维评分使用 1-5 分整数
- brief_comment 控制在 1-2 句
- 评语具体，不要空泛夸奖
- gap_summary 只总结最需要追问或改进的点
"""
    return llm_json(EVALUATION_SYSTEM_PROMPT, user_prompt)


def decide_next(
    current_round: int,
    config: dict[str, Any],
    covered_question_types: list[str],
    evaluation: dict[str, Any],
    history_summary: str,
    user_wants_to_end: bool,
) -> dict[str, Any]:
    user_prompt = f"""输入：
- 当前轮次：{current_round}
- 最小轮次：{config['min_rounds']}
- 最大轮次：{config['max_round_limit']}
- 已覆盖问题类型：{covered_question_types}
- 本轮评估：{json.dumps(evaluation, ensure_ascii=False)}
- 用户是否主动结束：{str(user_wants_to_end).lower()}
- 历史摘要：{history_summary}

请输出 JSON，字段包括：
- action
- reason
- next_question_type

约束：
- action 只能是 follow_up、new_question、end
- 未达到最小轮次前，若用户未主动结束，不得输出 end
- 达到最大轮次时必须输出 end
- 若继续追问，reason 必须指向本轮回答中的具体缺口
"""
    decision = llm_json(DECISION_SYSTEM_PROMPT, user_prompt)
    if current_round >= config["max_round_limit"]:
        decision["action"] = "end"
        decision["reason"] = "已达到最大轮数上限。"
    elif current_round < config["min_rounds"] and not user_wants_to_end and decision.get("action") == "end":
        decision["action"] = "new_question"
        decision["reason"] = "尚未达到最小轮数，继续面试。"
    return decision


def generate_next_question(
    decision: dict[str, Any],
    current_answer: str,
    history_summary: str,
    config: dict[str, Any],
) -> dict[str, Any]:
    user_prompt = f"""输入：
- 决策结果：{json.dumps(decision, ensure_ascii=False)}
- 当前用户回答：{current_answer}
- 历史摘要：{history_summary}
- 目标岗位：{config['target_role']}
- 面试官风格：{config['interviewer_style']}

请输出 JSON，字段包括：
- next_question
- question_type

要求：
- 如果 action=follow_up，围绕上一轮缺口深挖
- 如果 action=new_question，自然切换到未充分覆盖的维度
- 每次只生成一个问题
- 语言自然，像真实中文面试官
"""
    return llm_json(NEXT_QUESTION_SYSTEM_PROMPT, user_prompt)


def generate_final_report(turns: list[dict[str, Any]], config: dict[str, Any]) -> dict[str, Any]:
    user_prompt = f"""输入：
- 全部轮次记录：{json.dumps(turns, ensure_ascii=False)}
- 会话配置：{json.dumps(config, ensure_ascii=False)}

请输出 JSON，字段包括：
- overall_score
- dimension_scores
- strengths
- weaknesses
- round_summaries
- improvement_suggestions
- sample_better_answer
- final_summary_text

要求：
- 反馈要具体、可执行
- strengths 和 weaknesses 各给 2-4 条
- improvement_suggestions 给 2-4 条
- sample_better_answer 用中文给出一段更优表达示例
- final_summary_text 适合直接展示给用户，也可交给 TTS 朗读
"""
    return llm_json(FINAL_REPORT_SYSTEM_PROMPT, user_prompt)


def transcribe_audio(audio_path: Path, language: str) -> dict[str, Any]:
    api_key = require_env("INTERVIEW_ASR_API_KEY / SENSEAUDIO_API_KEY", ASR_API_KEY)
    headers = {"Authorization": f"Bearer {api_key}"}
    data: dict[str, Any] = {
        "model": ASR_MODEL,
        "response_format": ASR_RESPONSE_FORMAT,
    }
    if language and language != "auto":
        data["language"] = language.replace("-CN", "").lower()
    with audio_path.open("rb") as handle:
        files = {"file": (audio_path.name, handle)}
        response = requests.post(
            ASR_URL,
            headers=headers,
            data=data,
            files=files,
            timeout=ASR_TIMEOUT,
        )
    response.raise_for_status()
    payload = response.json()
    text = payload.get("text", "").strip()
    if not text and payload.get("segments"):
        text = " ".join(seg.get("text", "").strip() for seg in payload["segments"]).strip()
    if not text:
        raise ValueError("ASR 未返回可用文本")
    return {"text": text, "raw": payload}


def synthesize_tts(text: str, round_id: int, prefix: str) -> str | None:
    if not text:
        return None
    api_key = require_env("INTERVIEW_TTS_API_KEY / SENSEAUDIO_API_KEY", TTS_API_KEY)
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": TTS_MODEL,
        "text": text,
        "stream": False,
        "voice_setting": {"voice_id": TTS_VOICE_ID},
        "audio_setting": {"format": "mp3", "sample_rate": 32000},
    }
    response = requests.post(TTS_URL, headers=headers, json=payload, timeout=TTS_TIMEOUT)
    response.raise_for_status()
    result = response.json()
    if result.get("base_resp", {}).get("status_code") != 0:
        raise RuntimeError(result.get("base_resp", {}).get("status_msg", "TTS 调用失败"))
    audio_hex = result.get("data", {}).get("audio", "")
    if not audio_hex:
        raise RuntimeError("TTS 响应缺少音频数据")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / f"{prefix}_{round_id}.mp3"
    out_path.write_bytes(bytes.fromhex(audio_hex))
    return str(out_path)


def build_history_summary(turns: list[dict[str, Any]]) -> str:
    if not turns:
        return "暂无历史。"
    parts = []
    for turn in turns[-4:]:
        parts.append(
            f"第{turn['round_id']}轮[{turn['question_type']}] "
            f"问:{turn['interviewer_question']} "
            f"答:{turn['asr_text']} "
            f"评:{turn['evaluation'].get('brief_comment', '')}"
        )
    return "\n".join(parts)


def prompt_for_answer() -> tuple[str, str | None, bool]:
    print("请输入回答方式：1) 音频文件路径 2) 直接输入文本 3) 结束面试")
    choice = input("选择 [1/2/3]: ").strip() or "1"
    if choice == "3":
        return "", None, True
    if choice == "2":
        text = input("输入你的回答文本：").strip()
        return text, None, False
    path = input("输入音频文件路径：").strip()
    return "", path, False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="运行中文语音面试模拟器")
    parser.add_argument("--target-role", default="通用求职者", help="目标岗位")
    parser.add_argument(
        "--style",
        default="professional",
        choices=["friendly", "professional", "stress"],
        help="面试官风格",
    )
    parser.add_argument("--min-rounds", type=int, default=4, help="最小轮数")
    parser.add_argument("--max-round-limit", type=int, default=8, help="最大轮数")
    parser.add_argument("--language", default="zh-CN", help="语言，默认 zh-CN")
    parser.add_argument("--no-tts", action="store_true", help="不调用 TTS，只输出文本问题")
    parser.add_argument("--save-report", default="", help="最终报告保存路径")
    return parser.parse_args()


def main() -> None:
    load_env()
    refresh_runtime_settings()
    args = parse_args()
    if args.max_round_limit < args.min_rounds:
        raise SystemExit("max-round-limit 必须大于等于 min-rounds")

    config = {
        "target_role": args.target_role,
        "interviewer_style": args.style,
        "min_rounds": args.min_rounds,
        "max_round_limit": args.max_round_limit,
        "language": args.language,
    }

    opening = generate_opening(config)
    print(f"\n面试官：{opening['opening_text']}")
    current_question = opening["first_question"]
    current_question_type = opening["question_type"]
    turns: list[dict[str, Any]] = []
    covered_question_types: list[str] = []

    round_id = 1
    while round_id <= config["max_round_limit"]:
        print(f"\n第 {round_id} 轮")
        print(f"问题类型：{current_question_type}")
        print(f"面试官：{current_question}")

        tts_path = None
        if not args.no_tts:
            try:
                tts_path = synthesize_tts(current_question, round_id, "question")
                print(f"TTS 音频已保存：{tts_path}")
            except Exception as exc:
                print(f"TTS 调用失败，继续文本模式：{exc}", file=sys.stderr)

        answer_text, answer_audio_path, user_wants_to_end = prompt_for_answer()
        if user_wants_to_end:
            break

        asr_raw = None
        if answer_audio_path:
            audio_path = Path(answer_audio_path).expanduser()
            if not audio_path.exists():
                print("音频文件不存在，请重新回答。", file=sys.stderr)
                continue
            try:
                asr_result = transcribe_audio(audio_path, config["language"])
            except Exception as exc:
                print(f"ASR 调用失败：{exc}", file=sys.stderr)
                continue
            answer_text = asr_result["text"]
            asr_raw = asr_result["raw"]
            print(f"ASR 文本：{answer_text}")

        if not answer_text.strip():
            print("回答为空，请重新输入。", file=sys.stderr)
            continue

        history_summary = build_history_summary(turns)
        evaluation = evaluate_turn(current_question, current_question_type, answer_text, history_summary)
        covered_question_types.append(current_question_type)
        decision = decide_next(
            round_id,
            config,
            covered_question_types,
            evaluation,
            history_summary,
            False,
        )

        turn = {
            "round_id": round_id,
            "question_type": current_question_type,
            "interviewer_question": current_question,
            "interviewer_audio": tts_path,
            "asr_text": answer_text,
            "asr_raw": asr_raw,
            "evaluation": evaluation,
            "decision": decision,
        }
        turns.append(turn)

        print(f"评估：{evaluation.get('brief_comment', '')}")
        print(f"决策：{decision.get('action')} | 原因：{decision.get('reason', '')}")

        if decision.get("action") == "end":
            break

        next_question = generate_next_question(decision, answer_text, build_history_summary(turns), config)
        current_question = next_question["next_question"]
        current_question_type = next_question["question_type"]
        round_id += 1

    final_report = generate_final_report(turns, config)
    closing_text = "好的，本次模拟面试先到这里。接下来我会为你总结本次表现。"
    print(f"\n面试官：{closing_text}\n")
    print(json.dumps(final_report, ensure_ascii=False, indent=2))

    report_tts = None
    if not args.no_tts:
        try:
            report_tts = synthesize_tts(final_report.get("final_summary_text", ""), round_id + 1, "summary")
            if report_tts:
                print(f"总结 TTS 音频已保存：{report_tts}")
        except Exception as exc:
            print(f"总结 TTS 调用失败：{exc}", file=sys.stderr)

    payload = {
        "config": config,
        "closing_text": closing_text,
        "turns": turns,
        "final_report": final_report,
        "report_summary_tts_audio": report_tts,
    }

    if args.save_report:
        report_path = Path(args.save_report)
    else:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        report_path = OUTPUT_DIR / "final_report.json"
    report_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"完整结果已保存：{report_path}")


if __name__ == "__main__":
    main()
