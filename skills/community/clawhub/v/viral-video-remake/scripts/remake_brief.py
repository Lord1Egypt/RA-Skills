#!/usr/bin/env python3
"""Turn a LinkDigest read with `breakdown` into a brief for making your own video.

    python3 scripts/linkdigest.py "<link>" --breakdown --depth transcript --format json > post.json
    python3 scripts/remake_brief.py post.json --topic "我的主题" [--lang en]

The brief keeps the post's structure (hook mechanism, timed beats, title
formula, cover text, call to action) and says not to reuse its lines, footage
or images. Standard library only. Mirrors web/src/lib/remake.ts on linkdigest.dev.
"""
import argparse
import json
import sys


def mmss(sec):
    s = max(0, round(float(sec)))
    return f"{s // 60}:{s % 60:02d}"


def target_seconds(duration):
    d = duration if isinstance(duration, (int, float)) and duration > 0 else 60
    return max(15, round(d / 5) * 5)


def brief(post, topic, lang="zh"):
    b = post.get("breakdown")
    if not b:
        sys.exit("这条结果里没有 breakdown：读取时要加 --breakdown")
    hook = b.get("hook") or {}
    beats = [x for x in (b.get("beats") or []) if x.get("label") or x.get("summary")]
    # Older cached reads carry no duration: the transcript's last line, else the last beat, plus 15 s.
    ts = [x.get("t") for x in (post.get("transcript") or []) if isinstance(x.get("t"), (int, float))] or \
         [x.get("t") for x in (b.get("beats") or []) if isinstance(x.get("t"), (int, float))]
    n = target_seconds(post.get("duration_seconds") or ((max(ts) + 15) if ts else None))
    title, platform = post.get("title") or "", post.get("platform") or ""
    template, ideas = b.get("template") or [], b.get("remix_ideas") or []
    at = lambda x: f"[{mmss(x['t'])}] " if x.get("t") is not None else ""
    if lang == "en":
        lines = [
            f'Make a ~{n}-second video of my own, using the structure of a post that worked: "{title}" ({platform}).',
            "Borrow the structure, pacing and the way the hook works. Do NOT reuse the original's lines, footage or images.",
            "", f"My topic: {topic}", "",
            "Hook (first 3 seconds) — how the original's worked:",
            f"- said: {hook.get('spoken') or '—'}", f"- on screen: {hook.get('on_screen') or '—'}",
            f"- visual: {hook.get('visual') or '—'}", f"- why it works: {hook.get('why') or '—'}", "",
            "Beats (keep the order and the rough timing, scaled to my length):",
            *[f"{i}. {at(x)}{x.get('label', '')}{(' — ' + x['summary']) if x.get('summary') else ''}" for i, x in enumerate(beats, 1)],
            "", f"Title formula: {b.get('title_formula') or '—'}", f"Cover text pattern: {b.get('cover_text') or '—'}",
            f"Call to action: {b.get('cta') or '—'}", f"Audience: {b.get('audience') or '—'}",
        ]
        if template:
            lines += ["", "Reusable template:", *[f"- {x}" for x in template]]
        if ideas:
            lines += ["", "Angles to consider:", *[f"- {x}" for x in ideas]]
        lines += ["", "Write the script first and show it to me, then the storyboard, then render."]
        return "\n".join(lines)
    lines = [
        f"帮我做一条约 {n} 秒的视频，参考一条已经验证过的爆款的结构：「{title}」（{platform}）。",
        "只借它的结构、节奏和钩子的写法；不要用原视频的台词、画面和图片——主题、例子和画面都用我自己的。",
        "", f"我的主题：{topic}", "",
        "开头钩子（前 3 秒）——原视频是这样起作用的：",
        f"- 说的：{hook.get('spoken') or '—'}", f"- 屏幕字：{hook.get('on_screen') or '—'}",
        f"- 画面：{hook.get('visual') or '—'}", f"- 为什么有效：{hook.get('why') or '—'}", "",
        "结构节拍（顺序和大致时间照着来，按我的时长缩放）：",
        *[f"{i}. {at(x)}{x.get('label', '')}{('——' + x['summary']) if x.get('summary') else ''}" for i, x in enumerate(beats, 1)],
        "", f"标题公式：{b.get('title_formula') or '—'}", f"封面文字的写法：{b.get('cover_text') or '—'}",
        f"结尾行动号召：{b.get('cta') or '—'}", f"目标人群：{b.get('audience') or '—'}",
    ]
    if template:
        lines += ["", "可复用模板：", *[f"- {x}" for x in template]]
    if ideas:
        lines += ["", "可以考虑的角度：", *[f"- {x}" for x in ideas]]
    lines += ["", "先写口播稿给我看，再出分镜，最后再渲染。"]
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description="LinkDigest 读取结果 → 同款视频脚本说明")
    p.add_argument("json", help="linkdigest.py --breakdown --format json 的输出文件；- 从标准输入读")
    p.add_argument("--topic", default="<在这里写你的主题>", help="你自己的主题")
    p.add_argument("--lang", choices=["zh", "en"], default="zh")
    a = p.parse_args()
    raw = sys.stdin.read() if a.json == "-" else open(a.json, encoding="utf-8").read()
    print(brief(json.loads(raw), a.topic, a.lang))


if __name__ == "__main__":
    main()
