#!/usr/bin/env python3
"""
心跳优化配置

生成心跳相关的 openclaw.json 配置补丁:
  1. 心跳模型强制使用 glm-4.7-flashx (而非默认 glm-4.7)
  2. 心跳间隔调整为 55min (保持缓存热度)

纯本地运行，无网络请求，无副作用。
"""

import json
import sys


def generate_heartbeat_config(
    interval_minutes: int = 55,
    model: str = "zai-proxy/glm-4.7-flashx",
) -> dict:
    """生成心跳优化配置补丁。

    Args:
        interval_minutes: 心跳间隔 (分钟)，默认 55
        model: 心跳使用的模型

    Returns:
        openclaw.json 配置补丁
    """
    return {
        "agents": {
            "defaults": {
                "heartbeat": {
                    "every": f"{interval_minutes}m",
                    "model": model,
                }
            }
        }
    }


def show_recommendation(cache_ttl_minutes: int = 60) -> dict:
    """推荐心跳间隔。

    按缓存 TTL 计算最优间隔 (TTL - 5min buffer)。
    """
    buffer = 5
    recommended = cache_ttl_minutes - buffer

    return {
        "cache_ttl_minutes": cache_ttl_minutes,
        "recommended_interval_minutes": recommended,
        "heartbeat_model": "zai-proxy/glm-4.7-flashx",
        "explanation": (
            f"缓存 TTL 是 {cache_ttl_minutes} 分钟。"
            f"设置心跳为 {recommended} 分钟 (留 {buffer} 分钟缓冲)，"
            f"保持缓存热度，避免缓存重建费用。"
        ),
        "config_patch": generate_heartbeat_config(recommended),
        "savings": {
            "model": f"心跳用 flashx 替代 glm-4.7 → 成本大幅降低",
            "interval": (
                f"从默认 30min 调为 {recommended}min → "
                f"减少约 {round((1 - 30/recommended) * 100)}% 心跳调用"
            ),
        },
    }


def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  heartbeat_config.py recommend [cache_ttl_minutes]")
        print("  heartbeat_config.py patch")
        print()
        print("示例:")
        print("  heartbeat_config.py recommend      # 默认 60min 缓存 TTL")
        print("  heartbeat_config.py recommend 120   # 自定义 120min 缓存 TTL")
        print("  heartbeat_config.py patch           # 输出 openclaw.json 补丁")
        sys.exit(1)

    command = sys.argv[1]

    if command == "recommend":
        ttl = int(sys.argv[2]) if len(sys.argv) > 2 else 60
        result = show_recommendation(ttl)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif command == "patch":
        patch = generate_heartbeat_config()
        print(json.dumps(patch, indent=2, ensure_ascii=False))

    else:
        print(f"未知命令: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
