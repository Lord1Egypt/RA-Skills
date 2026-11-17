#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""social-collaboration-mind: 心智理论(ToM)+自适应协作策略选择。

用法:
  python social_mind.py --selftest
  echo '{"expertise":0.9,"confidence":0.8,"busy":0.1}' | python social_mind.py

输入伙伴信号:
  expertise ∈ [0,1], confidence ∈ [0,1], busy ∈ [0,1],
  trust ∈ [0,1] (默认0.7), mood ∈ {neutral,positive,negative}
输出: {"strategy","reason","tone","watch"}
策略: delegate / consult / monitor / pair / avoid
"""
import sys, json


def decide(sig):
    expertise = float(sig.get("expertise", 0.5))
    confidence = float(sig.get("confidence", 0.5))
    busy = float(sig.get("busy", 0.3))
    trust = float(sig.get("trust", 0.7))
    mood = sig.get("mood", "neutral")

    tone = "soft" if mood == "negative" else "neutral"
    watch = []

    # 低信任：回避关键委派，自己兜底
    if trust < 0.4:
        return {"strategy": "avoid", "reason": "历史守信度过低，关键任务不委，改自行兜底",
                "tone": tone, "watch": ["自行复核"]}

    if expertise >= 0.7 and confidence >= 0.6 and busy < 0.5:
        return {"strategy": "delegate", "reason": "专业度高且自信、有余力，委派并收结果",
                "tone": tone, "watch": ["验收结果"]}
    if expertise >= 0.7 and (confidence < 0.6 or busy >= 0.5):
        return {"strategy": "consult", "reason": "专业度高但置信不足或偏忙，征询意见不松手",
                "tone": tone, "watch": ["意见质量", "时间窗"]}
    if expertise < 0.7 and confidence >= 0.6:
        return {"strategy": "monitor", "reason": "专业度低但过度自信，令其试做并加校验门",
                "tone": tone, "watch": ["过程校验", "产出自检"]}
    if expertise < 0.7 and confidence < 0.6:
        return {"strategy": "pair", "reason": "专业度与自信均低，结对并给脚手架",
                "tone": tone, "watch": ["分步引导"]}
    return {"strategy": "consult", "reason": "默认征询", "tone": tone, "watch": []}


def selftest():
    cases = [
        ({"expertise": 0.9, "confidence": 0.8, "busy": 0.1}, "delegate"),
        ({"expertise": 0.9, "confidence": 0.3, "busy": 0.1}, "consult"),
        ({"expertise": 0.9, "confidence": 0.8, "busy": 0.8}, "consult"),
        ({"expertise": 0.3, "confidence": 0.9, "busy": 0.1}, "monitor"),
        ({"expertise": 0.2, "confidence": 0.2, "busy": 0.1}, "pair"),
        ({"expertise": 0.9, "confidence": 0.9, "busy": 0.1, "trust": 0.2}, "avoid"),
        ({"expertise": 0.9, "confidence": 0.9, "busy": 0.1, "mood": "negative"}, "delegate"),
    ]
    try:
        for sig, exp in cases:
            out = decide(sig)
            assert out["strategy"] == exp, f"信号{sig} 期望 {exp}，实际 {out['strategy']}"
        # 负向情绪应触发柔和语气
        neg = decide({"expertise": 0.9, "confidence": 0.9, "busy": 0.1, "mood": "negative"})
        assert neg["tone"] == "soft", f"负向情绪应转柔和: {neg}"
        # 低信任应回避
        low = decide({"expertise": 0.9, "confidence": 0.9, "busy": 0.1, "trust": 0.1})
        assert low["strategy"] == "avoid", f"低信任应回避: {low}"
        print("🧪 selftest PASS：7 策略判定 + 负向柔和 + 低信任回避 全过")
        return 0
    except AssertionError as e:
        print("❌ selftest FAIL:", e); return 1


def main():
    if "--selftest" in sys.argv:
        return selftest()
    raw = sys.stdin.read().strip()
    if not raw:
        print("⚠️ 未提供 JSON 伙伴信号，回退 --selftest 演示。")
        return selftest()
    sig = json.loads(raw)
    print(json.dumps(decide(sig), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
