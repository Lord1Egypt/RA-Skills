#!/usr/bin/env python3
"""
narration_writer.py
Uses Claude API (via Anthropic) to write cinematic, emotionally gripping
narration scripts for movie clips.

Narration style rules:
- Opening hook: "眼前这个[角色]只是[做了什么]，才[意外结果]..."
- Use suspense, rhythm, contrast to pull viewers in
- Each segment ≤ 40 Chinese characters
- Transition words: 随后、然而、就在此时、与此同时、没想到、令人意外的是、最终
- Voice: dramatic, storytelling, third-person omniscient
"""

import os
import json
import re

# ── Global API config ──────────────────────────────────────────────────────────
ANTHROPIC_API_KEY = None   # fallback: os.environ.get("ANTHROPIC_API_KEY")
NARRATION_MODEL   = "claude-sonnet-4-20250514"

# Narration style templates for different story stages
STAGE_HOOKS = {
    "opening": [
        "眼前这个{character}，只是{action}，没想到竟然{twist}……",
        "谁也没料到，{character}的一个{action}，彻底改变了……",
        "故事开始得很平静——{character}只是{action}，然而……",
    ],
    "development": [
        "随后，事情开始失控——",
        "然而，就在这时，",
        "没想到，{character}却{action}，",
    ],
    "climax": [
        "就在此时，一切走向了无法挽回的边缘——",
        "令人窒息的是，",
        "与此同时，{character}做出了一个改变命运的决定——",
    ],
    "resolution": [
        "最终，真相浮出水面——",
        "一切尘埃落定，",
        "谁也没想到，结局会是这样——",
    ]
}


def write_narration_script(
    events: list,
    movie_name: str,
    characters: list = None,
    language: str = "zh",
    style: str = "dramatic"
) -> list:
    """
    Call Claude to write a full cinematic narration script for the movie.

    Args:
        events     : list of plot events from plot_researcher.parse_plot_to_events()
        movie_name : movie title
        characters : list of {"name": "...", "role": "..."} dicts
        language   : "zh" (Chinese) or "en" (English)
        style      : "dramatic" | "suspense" | "emotional"

    Returns:
        list of narration dicts with 'narration_text' field added
    """
    api_key = ANTHROPIC_API_KEY or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("No ANTHROPIC_API_KEY found. Using rule-based narration fallback.")
        return _fallback_narration(events, movie_name)

    try:
        import anthropic
    except ImportError:
        import subprocess, sys
        subprocess.run([sys.executable, "-m", "pip", "install", "anthropic",
                        "--break-system-packages", "-q"], check=True)
        import anthropic

    client = anthropic.Anthropic(api_key=api_key)

    char_desc = ""
    if characters:
        char_desc = "主要角色：\n" + "\n".join(
            f"- {c['name']}（{c.get('role', '未知')}）" for c in characters
        )

    events_text = "\n".join(
        f"[{e['event_id']}] {e['stage']} @ {e['video_timestamp']}\n  情节：{e['description']}"
        for e in events
    )

    style_guide = {
        "dramatic": "极具感染力、戏剧张力强、节奏紧凑",
        "suspense": "悬念感强、欲言又止、引发好奇",
        "emotional": "情感深沉、共鸣强烈、直击人心"
    }.get(style, "极具感染力")

    prompt = f"""你是一位专业的电影解说文案写手，风格{style_guide}。

电影名称：《{movie_name}》
{char_desc}

以下是电影的关键情节节点，请为每个节点写一段旁白文案：

{events_text}

要求：
1. 第一段必须用悬念开头，格式如：
   "眼前这个[角色名]，只是[做了一件普通的事]，才[出乎意料的结果]……"
   或"谁也没料到，[角色]的一个[动作]，竟然……"

2. 每段文案不超过40个汉字，语言简洁有力

3. 段与段之间用过渡词衔接：随后、然而、就在此时、与此同时、没想到、令人意外的是、最终

4. 禁止剧透结局（结局段除外），用省略号制造悬念

5. 语气：第三人称全知视角，像讲故事一样娓娓道来但充满紧迫感

请严格按以下JSON格式返回，不要输出任何其他内容：
{{
  "narrations": [
    {{
      "event_id": "evt_001",
      "narration_text": "旁白文案内容"
    }}
  ]
}}"""

    response = client.messages.create(
        model=NARRATION_MODEL,
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text.strip()

    # Parse JSON response
    try:
        # Strip markdown fences if present
        clean = re.sub(r"```json|```", "", raw).strip()
        result = json.loads(clean)
        narration_map = {n["event_id"]: n["narration_text"] for n in result["narrations"]}
    except Exception as e:
        print(f"JSON parse failed ({e}), using fallback.")
        return _fallback_narration(events, movie_name)

    # Merge narration text back into events
    output = []
    for event in events:
        narration_text = narration_map.get(event["event_id"], "")
        if not narration_text:
            # Fallback for any missing event
            narration_text = _single_fallback(event)
        output.append({**event, "narration_text": narration_text})

    return output


def refine_narration(
    narrations: list,
    feedback: str,
    movie_name: str
) -> list:
    """
    Re-call Claude to refine narrations based on user feedback.
    e.g. "第二段太平淡了，加强悬念感" or "开头改成更震撼的风格"
    """
    api_key = ANTHROPIC_API_KEY or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("No API key. Cannot refine.")
        return narrations

    try:
        import anthropic
    except ImportError:
        import subprocess, sys
        subprocess.run([sys.executable, "-m", "pip", "install", "anthropic",
                        "--break-system-packages", "-q"], check=True)
        import anthropic

    client = anthropic.Anthropic(api_key=api_key)

    current = "\n".join(
        f"[{n['event_id']}] {n['narration_text']}" for n in narrations
    )

    prompt = f"""以下是《{movie_name}》的旁白文案：

{current}

用户反馈：{feedback}

请根据反馈修改文案，保持其他段落不变，只修改需要改动的部分。
每段仍不超过40个汉字。

严格按JSON返回：
{{
  "narrations": [
    {{"event_id": "evt_001", "narration_text": "修改后的文案"}}
  ]
}}"""

    response = client.messages.create(
        model=NARRATION_MODEL,
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text.strip()
    try:
        clean = re.sub(r"```json|```", "", raw).strip()
        result = json.loads(clean)
        narration_map = {n["event_id"]: n["narration_text"] for n in result["narrations"]}
        return [{**n, "narration_text": narration_map.get(n["event_id"], n["narration_text"])}
                for n in narrations]
    except Exception as e:
        print(f"Refinement parse failed ({e}). Returning original.")
        return narrations


# ── Rule-based fallback ────────────────────────────────────────────────────────
def _fallback_narration(events: list, movie_name: str) -> list:
    """Simple rule-based narration when no API key is available."""
    result = []
    for i, event in enumerate(events):
        result.append({**event, "narration_text": _single_fallback(event, i)})
    return result


def _single_fallback(event: dict, index: int = 0) -> str:
    stage = event.get("stage", "development")
    desc  = event.get("description", "")

    if index == 0 or stage == "opening":
        return f"故事就这样开始了——{desc[:30]}……"
    elif stage == "climax":
        return f"就在此时，{desc[:30]}……"
    elif stage == "resolution":
        return f"最终，{desc[:30]}。"
    else:
        return f"随后，{desc[:30]}……"


# ── CLI test ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    test_events = [
        {"event_id": "evt_001", "stage": "opening",
         "video_timestamp": "00:05:00", "video_seconds": 300,
         "description": "陆永瑜意外发现父亲陆建业贪污受贿的证据"},
        {"event_id": "evt_002", "stage": "development",
         "video_timestamp": "00:25:00", "video_seconds": 1500,
         "description": "陆金强带人找到废车场监听室，拿视频要挟陆永瑜"},
        {"event_id": "evt_003", "stage": "climax",
         "video_timestamp": "01:10:00", "video_seconds": 4200,
         "description": "陆永瑜被迫签下认罪书，律师张远发现监控录像有剪辑痕迹"},
        {"event_id": "evt_004", "stage": "resolution",
         "video_timestamp": "01:45:00", "video_seconds": 6300,
         "description": "法庭上伪证被当庭揭穿，陆永瑜无罪释放"},
    ]
    characters = [
        {"name": "陆永瑜", "role": "主角"},
        {"name": "陆金强", "role": "反派"},
        {"name": "张远",   "role": "律师"},
    ]

    results = write_narration_script(test_events, "误判", characters)
    print("\n=== Generated Narrations ===")
    for n in results:
        print(f"\n[{n['event_id']}] {n['stage']} @ {n['video_timestamp']}")
        print(f"  {n['narration_text']}")
