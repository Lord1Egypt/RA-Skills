#!/usr/bin/env python3
"""
情绪追踪器 - 记录会话中连续的情绪变化
当连续3条消息 score 持续下降时触发告警
"""

import sys
import json
import os
from datetime import datetime

TRACK_DIR = "/tmp/sentiment_tracking"


def ensure_track_dir():
    if not os.path.exists(TRACK_DIR):
        os.makedirs(TRACK_DIR)


def load_session(session_id: str) -> list:
    """加载会话历史"""
    ensure_track_dir()
    path = os.path.join(TRACK_DIR, f"{session_id}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_session(session_id: str, history: list):
    """保存会话历史"""
    ensure_track_dir()
    path = os.path.join(TRACK_DIR, f"{session_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def track(text: str, session_id: str) -> dict:
    """追踪单条消息情绪，返回完整分析"""
    from analyze import analyze

    result = analyze(text)
    history = load_session(session_id)

    # 添加元数据
    result["timestamp"] = datetime.now().isoformat()
    result["message_index"] = len(history) + 1

    history.append({
        "text": text[:100],  # 仅保存前100字
        "sentiment": result["sentiment"],
        "score": result["score"],
        "timestamp": result["timestamp"],
    })

    # 检查连续下降
    if len(history) >= 3:
        recent = history[-3:]
        if all(h["score"] < 0 for h in recent):
            if recent[0]["score"] > recent[1]["score"] > recent[2]["score"]:
                result["escalation_alert"] = True
                result["escalation_reason"] = "情绪连续3条持续恶化，建议人工介入"

    save_session(session_id, history)
    return result


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "请传入消息文本"}, ensure_ascii=False))
        sys.exit(1)

    session_id = "default"
    text = sys.argv[1]
    if len(sys.argv) >= 3 and sys.argv[1] == "--session-id":
        session_id = sys.argv[2]
        text = sys.argv[3]

    result = track(text, session_id)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()