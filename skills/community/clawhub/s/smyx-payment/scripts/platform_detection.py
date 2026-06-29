#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦞 小龙虾主厨 · 平台自动检测模块

自动检测当前运行的平台（ArkClaw / OpenClaw），根据平台特性自动选择最佳的二维码渲染方式。

功能特点：
    ✅ 零用户配置：自动检测，开箱即用
    ✅ 多维度检测：BUSINESS_CARRIER / SKILLS_API_URL / 工作目录
    ✅ 置信度评分：综合多维度结果，准确度更高
    ✅ 平台兼容：自动适配二维码渲染方式

使用方式：
    from .platform_detection import get_current_platform, render_qrcode_markdown

    platform = get_current_platform()
    print(f"当前平台: {platform['name']}")
    print(render_qrcode_markdown("https://qr.alipay.com/xxx"))
"""

import os
import re
from typing import Dict, Literal, get_args


PlatformType = Literal["arkclaw", "openclaw", "unknown"]


def detect_by_business_carrier() -> Dict[str, float]:
    """
    通过 BUSINESS_CARRIER 环境变量检测平台
    
    Returns:
        {"arkclaw": 置信度, "openclaw": 置信度}
    """
    carrier = os.environ.get("BUSINESS_CARRIER", "")
    if carrier == "arkclaw":
        return {"arkclaw": 1.0, "openclaw": 0.0}
    elif carrier and carrier != "arkclaw":
        return {"arkclaw": 0.0, "openclaw": 0.8}
    return {"arkclaw": 0.0, "openclaw": 0.0}


def detect_by_skills_api_url() -> Dict[str, float]:
    """
    通过 SKILLS_API_URL 环境变量检测平台
    
    Returns:
        {"arkclaw": 置信度, "openclaw": 置信度}
    """
    url = os.environ.get("SKILLS_API_URL", "")
    if "arkclaw-personal" in url or "arkclaw" in url:
        return {"arkclaw": 0.95, "openclaw": 0.0}
    return {"arkclaw": 0.0, "openclaw": 0.0}


def detect_by_workspace_path() -> Dict[str, float]:
    """
    通过工作目录路径检测平台
    
    Returns:
        {"arkclaw": 置信度, "openclaw": 置信度}
    """
    cwd = os.getcwd()
    if ".arkclaw-team" in cwd:
        return {"arkclaw": 0.85, "openclaw": 0.0}
    return {"arkclaw": 0.0, "openclaw": 0.0}


def detect_by_env_vars() -> Dict[str, float]:
    """
    通过其他 ArkClaw 专属环境变量检测
    
    Returns:
        {"arkclaw": 置信度, "openclaw": 置信度}
    """
    ark_vars = ["ARK_AGENT_PLAN", "ARK_API_KEY", "ARK_CODING_PLAN", "ARK_MODEL_ID"]
    ark_count = sum(1 for var in ark_vars if os.environ.get(var))
    if ark_count >= 2:
        return {"arkclaw": 0.9, "openclaw": 0.0}
    elif ark_count == 1:
        return {"arkclaw": 0.7, "openclaw": 0.0}
    return {"arkclaw": 0.0, "openclaw": 0.0}


def get_current_platform() -> Dict:
    """
    综合多维度检测当前平台
    
    Returns:
        {
            "platform": "arkclaw" | "openclaw" | "unknown",
            "confidence": 0.0-1.0,
            "method": "检测方法",
            "supports_media": bool,  # 是否支持 MEDIA: 方式
            "supports_html_img": bool,  # 是否支持 HTML <img> 标签
        }
    """
    detectors = [
        ("BUSINESS_CARRIER", detect_by_business_carrier),
        ("SKILLS_API_URL", detect_by_skills_api_url),
        ("WORKSPACE_PATH", detect_by_workspace_path),
        ("ARK_ENV_VARS", detect_by_env_vars),
    ]
    
    ark_scores = []
    openclaw_scores = []
    detection_method = None
    
    for method_name, detector in detectors:
        result = detector()
        if result["arkclaw"] > 0:
            ark_scores.append(result["arkclaw"])
            if not detection_method:
                detection_method = method_name
        if result["openclaw"] > 0:
            openclaw_scores.append(result["openclaw"])
    
    # 计算最终得分
    ark_final = max(ark_scores) if ark_scores else 0.0
    openclaw_final = max(openclaw_scores) if openclaw_scores else 0.0
    
    # 判断平台
    if ark_final >= 0.7:
        platform: PlatformType = "arkclaw"
        confidence = ark_final
    elif openclaw_final >= 0.5:
        platform = "openclaw"
        confidence = openclaw_final
    else:
        platform = "unknown"
        confidence = 0.0
    
    return {
        "platform": platform,
        "confidence": round(confidence, 2),
        "method": detection_method or "综合检测",
        "supports_media": platform != "arkclaw",  # ArkClaw 不支持 MEDIA:
        "supports_html_img": platform != "openclaw",  # OpenClaw 不支持 <img>
    }


def render_qrcode_markdown(qr_url: str, alt_text: str = "支付二维码", size: int = 300) -> str:
    """
    根据当前平台智能渲染二维码 Markdown
    
    Args:
        qr_url: 二维码图片 URL
        alt_text: 替代文本
        size: 二维码尺寸（像素）
    
    Returns:
        适合当前平台的 Markdown 字符串
    """
    platform_info = get_current_platform()
    platform = platform_info["platform"]
    
    if platform == "arkclaw":
        # ArkClaw：使用 HTML <img> 标签
        return f'<img src="{qr_url}" alt="{alt_text}" width="{size}" height="{size}" />'
    elif platform == "openclaw":
        # OpenClaw：使用 MEDIA: 方式
        return f"MEDIA:{qr_url}"
    else:
        # 未知平台：双重保险，同时输出两种格式
        return (
            f"<!-- MEDIA 格式（OpenClaw 适用） -->\n"
            f"MEDIA:{qr_url}\n\n"
            f"<!-- HTML 格式（ArkClaw 适用） -->\n"
            f'<img src="{qr_url}" alt="{alt_text}" width="{size}" height="{size}" />'
        )


def get_platform_display_name() -> str:
    """获取平台显示名称"""
    info = get_current_platform()
    names = {
        "arkclaw": "🦞 ArkClaw（龙虾平台）",
        "openclaw": "🐚 OpenClaw（开源版）",
        "unknown": "❓ 未知平台",
    }
    return names.get(info["platform"], "❓ 未知平台")


if __name__ == "__main__":
    # 测试：打印当前平台信息
    print("=" * 60)
    print("🦞 平台自动检测测试")
    print("=" * 60)
    print()
    
    info = get_current_platform()
    print(f"检测平台: {get_platform_display_name()}")
    print(f"置信度: {info['confidence']:.0%}")
    print(f"检测方法: {info['method']}")
    print(f"支持 MEDIA:: {info['supports_media']}")
    print(f"支持 HTML <img>: {info['supports_html_img']}")
    print()
    
    print("二维码渲染测试:")
    test_url = "https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=https://qr.alipay.com/test123"
    print()
    print(render_qrcode_markdown(test_url))
    print()
    print("=" * 60)
