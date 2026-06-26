"""
image_generator.py - 生图模块 (通用版 v2.3)
所有配置从参数传入，不 hardcode 任何凭证
环境变量兜底优先级：BANANA2_API_KEY → ACEDATA_API_KEY → PAPER_DIAGRAM_API_KEY
"""

import os
import sys
import time
import requests

_skill_dir = os.path.dirname(os.path.abspath(__file__))
if _skill_dir not in sys.path:
    sys.path.insert(0, _skill_dir)

from style_presets import get_preset, build_style_prompt, build_negative_prompt


def build_academic_prompt(
    topology: str,
    figure_type: str,
    user_requirement: str = "",
    style_name: str = None
) -> dict:
    preset = get_preset(style_name)
    style_base = build_style_prompt(preset)
    negative   = build_negative_prompt(preset)

    type_suffix_map = {
        "teaser": (
            "Teaser/motivation figure: concept diagram with side-by-side comparison, "
            "old method (gray/red tones) vs new method (blue/green tones), "
            "arrows showing improvement flow, concise boxed labels."
        ),
        "architecture": (
            "System architecture diagram: modular rounded rectangles with labels, "
            "data flow arrows left-to-right, color-coded modules by function, "
            "hierarchical subgraph grouping, consistent line weights."
        ),
        "flowchart": (
            "Algorithm flowchart: rounded process boxes, diamond decision nodes, "
            "oval start/end nodes, directional arrows with step numbers, "
            "clean grid layout, top-to-bottom or left-to-right flow."
        ),
        "environment": (
            "Environment interaction diagram: agent-environment feedback loop, "
            "simplified environment block, agent block, "
            "state/action/reward labeled arrows, clean abstract representation."
        ),
    }
    type_suffix = type_suffix_map.get(figure_type, type_suffix_map["architecture"])
    user_extra  = f" Additional requirements: {user_requirement}" if user_requirement else ""

    positive = (
        f"Academic paper figure, publication quality. {style_base} "
        f"Diagram type: {type_suffix} "
        f"Diagram content: {topology}"
        f"{user_extra}"
    ).strip()

    return {"positive": positive, "negative": negative}


def _get_output_dir(skill_dir: str = None) -> str:
    """
    输出目录优先级：
    1. 环境变量 PAPER_DIAGRAM_OUTPUT_DIR
    2. skill_dir/../outputs/
    3. ./outputs/
    """
    if skill_dir is None:
        skill_dir = _skill_dir

    env_dir = os.environ.get("PAPER_DIAGRAM_OUTPUT_DIR", "").strip()
    if env_dir:
        return env_dir

    rel = os.path.normpath(os.path.join(skill_dir, "..", "outputs"))
    parent = os.path.dirname(rel)
    if os.path.exists(parent) and os.access(parent, os.W_OK):
        return rel

    return os.path.join(os.getcwd(), "outputs")


def generate_image(
    prompt_dict: dict,
    api_url: str,
    api_key: str,
    model: str = "nano-banana-2",
    output_filename: str = "paper_diagram.png",
    output_dir: str = None,
    skill_dir: str = None,
    timeout: int = 120
) -> tuple:
    """
    调用任意兼容生图 API（Banana2 / SD / 自建服务）

    Args:
        prompt_dict:    {"positive": ..., "negative": ...}
        api_url:        API 地址（必填）
        api_key:        密钥（必填）
        model:          模型名，默认 nano-banana-2
        output_filename: 输出文件名
        output_dir:     输出目录（None → 自动推断）
        skill_dir:      skill 目录（None → 自动推断）
        timeout:        请求超时秒数

    Returns: (success: bool, output_path: str, error_msg: str)
    """
    if not api_url or not api_key:
        return False, "", "api_url and api_key are required"

    if output_dir is None:
        output_dir = _get_output_dir(skill_dir)
    os.makedirs(output_dir, exist_ok=True)

    try:
        print(f"[ImageGen] POST {model} @ {api_url}", flush=True)
        t0 = time.time()

        # 关键：禁用系统代理（避免 exec 代理干扰 Kong）+ acedata 正确参数格式
        session = requests.Session()
        session.trust_env = False

        headers = {
            "Authorization": f"Bearer {api_key}",
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        payload = {
            "action": "generate",
            "model": model,
            "prompt": prompt_dict.get("positive", ""),
            "negative_prompt": prompt_dict.get("negative", ""),
            "aspect_ratio": "16:9",
            "resolution": "2K"
        }

        response = session.post(api_url, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        elapsed = time.time() - t0

        print(f"[ImageGen] Response in {elapsed:.1f}s: {str(data)[:300]}", flush=True)

        if not data.get("success"):
            return False, "", f"API error: {data}"

        # 解析 acedata 响应格式
        image_url = None
        for key in ("image_url", "url"):
            image_url = data.get(key)
            if image_url:
                break
        if not image_url:
            body = data.get("body", {})
            inner = body.get("data") if isinstance(body, dict) else None
            if inner and isinstance(inner, list):
                image_url = inner[0].get("image_url") if isinstance(inner[0], dict) else None
        if not image_url:
            for k in ("data", "images", "outputs"):
                arr = data.get(k)
                if isinstance(arr, list) and arr:
                    item = arr[0]
                    image_url = item.get("image_url") if isinstance(item, dict) else None
                    if image_url:
                        break
        if not image_url:
            return False, "", f"No image URL in response: {str(data)[:500]}"

        print(f"[ImageGen] Image URL found, downloading...", flush=True)

        img_resp = session.get(image_url, timeout=60)
        img_resp.raise_for_status()

        output_path = os.path.join(output_dir, output_filename)
        with open(output_path, "wb") as f:
            f.write(img_resp.content)

        total = time.time() - t0
        size  = os.path.getsize(output_path)
        print(f"[ImageGen] Done: {output_path} ({size/1024:.1f} KB, {total:.1f}s)", flush=True)
        return True, output_path, ""

    except requests.exceptions.Timeout:
        return False, "", f"Request timed out after {timeout}s"
    except requests.exceptions.ConnectionError as e:
        return False, "", f"Connection failed: {e}"
    except Exception as e:
        return False, "", str(e)


def _resolve_api_credentials(api_url: str = None, api_key: str = None) -> tuple:
    """
    统一凭证解析 — 参数优先，环境变量兜底。

    api_key 优先级：参数 → BANANA2_API_KEY → ACEDATA_API_KEY → PAPER_DIAGRAM_API_KEY
    api_url 优先级：参数 → BANANA2_API_URL → PAPER_DIAGRAM_API_URL → 默认值

    Returns: (resolved_api_url, resolved_api_key)
    """
    # ── api_key 兜底链 ──
    if not api_key:
        for env_name in ("BANANA2_API_KEY", "ACEDATA_API_KEY", "PAPER_DIAGRAM_API_KEY"):
            val = os.environ.get(env_name, "").strip()
            if val:
                api_key = val
                print(f"[ImageGen] API key from env {env_name}", flush=True)
                break

    # ── api_url 兜底链 ──
    if not api_url:
        for env_name in ("BANANA2_API_URL", "PAPER_DIAGRAM_API_URL"):
            val = os.environ.get(env_name, "").strip()
            if val:
                api_url = val
                break
        if not api_url:
            api_url = "https://api.acedata.cloud/nano-banana/images"

    return api_url, api_key


def generate(
    topology: str,
    figure_type: str,
    user_requirement: str = "",
    api_url: str = None,
    api_key: str = None,
    model: str = "nano-banana-2",
    style_name: str = None,
    output_dir: str = None
) -> tuple:
    """
    主入口 — 兼容旧签名，所有凭证从参数传入或环境变量自动兜底
    环境变量优先级：BANANA2_API_KEY → ACEDATA_API_KEY → PAPER_DIAGRAM_API_KEY
    """
    api_url, api_key = _resolve_api_credentials(api_url, api_key)

    prompt_dict = build_academic_prompt(topology, figure_type, user_requirement, style_name)
    filename = f"{figure_type}_diagram.png"

    if not api_key:
        return False, "", (
            "API Key not configured.\n"
            "请设置以下任一环境变量：\n"
            "  BANANA2_API_KEY（推荐）\n"
            "  ACEDATA_API_KEY\n"
            "  PAPER_DIAGRAM_API_KEY\n"
            "或在对话中直接传入 api_key 参数。"
        )

    return generate_image(
        prompt_dict,
        api_url=api_url,
        api_key=api_key,
        model=model,
        output_filename=filename,
        output_dir=output_dir
    )
