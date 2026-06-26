#!/usr/bin/env python3
"""
模型分级路由 — 适配 OpenClaw-Manager 的 zai/kimi Provider

根据 prompt 复杂度分类，推荐使用不同模型：
  - cheap:    glm-4.7-flashx (简单对话、心跳、后台任务)
  - standard: glm-4.7        (写代码、调试、常规工作)
  - premium:  glm-4.7 / k2p5 (复杂推理、架构设计)

纯本地运行，无网络请求，无副作用。
"""

import json
import re
import sys

# ============================================================================
# Provider 模型配置 — 适配本项目
# ============================================================================

PROVIDER_MODELS = {
    "zai-proxy": {
        "cheap": "zai-proxy/glm-4.7-flashx",
        "standard": "zai-proxy/glm-4.7",
        "premium": "zai-proxy/glm-4.7",
    },
    "zai-coding-proxy": {
        "cheap": "zai-coding-proxy/glm-4.7-flashx",
        "standard": "zai-coding-proxy/glm-4.7",
        "premium": "zai-coding-proxy/glm-4.7",
    },
    "kimi-coding-proxy": {
        "cheap": "kimi-coding-proxy/k2p5",
        "standard": "kimi-coding-proxy/k2p5",
        "premium": "kimi-coding-proxy/k2p5",
    },
}

DEFAULT_PROVIDER = "zai-proxy"

# ============================================================================
# 分类模式
# ============================================================================

# 简单通信 — 必须走 cheap (永远不用 standard/premium)
COMMUNICATION_PATTERNS = [
    r"^(hi|hey|hello|yo|你好|嗨)[\s!！.。]*$",
    r"^(thanks|thank you|thx|谢谢|感谢)[\s!！.。]*$",
    r"^(ok|okay|sure|got it|understood|好的|好|行|知道了|明白|收到)[\s!！.。]*$",
    r"^(yes|yeah|yep|no|nope|是|否|对|不)[\s!！.。]*$",
    r"^(good|great|nice|cool|awesome|不错|很好)[\s!！.。]*$",
    r"^.{1,5}$",  # 任何 5 字符以内的短消息 (中文字符信息密度高，不能用 10)
]

# 后台/例行任务 — 走 cheap
BACKGROUND_PATTERNS = [
    r"heartbeat",
    r"心跳",
    r"check\s+(email|calendar|status|health)",
    r"检查\s*(邮件|日历|状态|健康)",
    r"cron",
    r"定时任务",
    r"parse\s+(csv|json|xml|log|yaml)",
    r"解析\s*(文件|日志)",
    r"read\s+(file|log)",
    r"读取?\s*(文件|日志)",
]

# 复杂任务 — 走 premium
COMPLEX_PATTERNS = [
    r"(design|architect|设计|架构)",
    r"(comprehensive|全面|深入)\s*(analy|分析|review|审查)",
    r"(refactor|重构)\s*(entire|整个|all|全部)",
    r"(strategy|策略|plan|方案|规划)",
    r"(migrate|迁移|migration)",
]


def classify_prompt(prompt: str) -> tuple[str, float, str]:
    """分类 prompt 复杂度。

    Returns:
        (tier, confidence, reasoning)
        tier: "cheap" | "standard" | "premium"
    """
    p = prompt.strip().lower()

    # 1. 简单通信 → cheap
    for pattern in COMMUNICATION_PATTERNS:
        if re.search(pattern, p, re.IGNORECASE):
            return ("cheap", 1.0, "简单通信/短消息")

    # 2. 后台任务 → cheap
    for pattern in BACKGROUND_PATTERNS:
        if re.search(pattern, p, re.IGNORECASE):
            return ("cheap", 0.9, "后台/例行任务")

    # 3. 复杂任务 → premium
    for pattern in COMPLEX_PATTERNS:
        if re.search(pattern, p, re.IGNORECASE):
            return ("premium", 0.8, "复杂推理/架构设计")

    # 4. 默认 → standard
    return ("standard", 0.6, "标准工作请求")


def route(prompt: str, provider: str = DEFAULT_PROVIDER,
          current_model: str | None = None) -> dict:
    """路由决策。

    Args:
        prompt: 用户输入
        provider: 使用的 provider 名
        current_model: 当前模型 (可选)

    Returns:
        dict with routing decision
    """
    tier, confidence, reasoning = classify_prompt(prompt)

    provider_cfg = PROVIDER_MODELS.get(provider, PROVIDER_MODELS[DEFAULT_PROVIDER])
    recommended = provider_cfg[tier]

    if current_model is None:
        current_model = provider_cfg["standard"]

    return {
        "prompt": prompt[:80] + ("..." if len(prompt) > 80 else ""),
        "tier": tier,
        "confidence": confidence,
        "reasoning": reasoning,
        "recommended_model": recommended,
        "current_model": current_model,
        "should_switch": recommended != current_model,
        "provider": provider,
    }


def main():
    if len(sys.argv) < 2:
        print("用法: model_router.py <prompt> [provider]")
        print()
        print("示例:")
        print('  model_router.py "thanks!"')
        print('  model_router.py "设计一个微服务架构" zai-coding-proxy')
        print('  model_router.py compare')
        sys.exit(1)

    if sys.argv[1] == "compare":
        print(json.dumps(PROVIDER_MODELS, indent=2, ensure_ascii=False))
        return

    prompt = sys.argv[1]
    provider = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_PROVIDER
    result = route(prompt, provider)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
