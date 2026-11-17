#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
short-drama-storyboard-pipeline :: export_prompts.py

把标准化分镜表（CSV）批量导出为逐镜提示词包：
  out/<name>/
    S01.image.txt / S01.video.i2v.txt(或 .fl2v / .t2v) ...
    manifest.csv / manifest.json

用法：
  python3 export_prompts.py --input 分镜表.csv --outdir out/EP01 \
      --mode both --model hailuo [--anchors characters.csv] [--check]

模式：
  scaffold  生成本镜提示词骨架文件（占位符按 references/model-dialects.md 填写）
  manifest  输出 manifest.csv / manifest.json 批量清单
  both      两者都要
  --check   只校验分镜表，不生成文件

仅依赖 Python 3.8+ 标准库。
"""

import argparse
import csv
import json
import re
import sys
from pathlib import Path

REQUIRED_COLS = ["shot_id", "scene", "shot_size", "camera_move", "duration_s",
                 "action_visual", "frame_mode"]
ALL_COLS = REQUIRED_COLS + ["dialogue_vo", "sfx_music", "negative_extra"]
FRAME_MODES = {"i2v", "fl2v", "t2v"}

# 安全：shot_id 仅允许字母/数字/下划线/连字符，避免用 \,/, .. 等片段拼文件路径造成目录逃逸
# （ClawHub 扫描 T09 · Insecure Skill Coding Practices 自动审计项）
SHOT_ID_RE = re.compile(r"^[A-Za-z0-9_-]+$")


def safe_name(name):
    """硬校验：非安全字符一律替换为下划线，防止路径注入（如 ../、绝对路径）。"""
    return re.sub(r"[^A-Za-z0-9_-]", "_", str(name or ""))

# 各模型时长档位近似值（随官方版本变化，仅用于提醒式校验，生成前请核对官方文档）
MODEL_DURATION = {
    "hailuo": (4, 15),
    "jimeng": (3, 12),
    "kling": (5, 10),
    "seedance": (4, 12),
    "vidu": (4, 8),
    "runway": (5, 10),
    "generic": (4, 15),
}

IMAGE_TEMPLATE = """# 首帧图提示词 — {shot_id}（{scene}）| 景别 {shot_size}
# 填写规范：references/model-dialects.md（目标模型方言）+ references/consistency-anchor.md
[风格前缀：全表统一，如「电影感真人短剧写实风格 / 2D日漫画风漫剧 / 3D卡通渲染」]
{anchors}
{shot_size}，9:16 竖幅，主体居中偏上，底部 1/4 留字幕安全区
{visual}
[光线氛围：从场景与情绪推断，如 冷雨夜霓虹 / 逆光轮廓 / 暖黄室内光]
[画质词：胶片颗粒感，高清细节，浅景深]
[negative]{negative}"""

I2V_TEMPLATE = """# 图生视频提示词（首帧驱动 I2V）— {shot_id} | 时长 {duration}s | 模型 {model}
# 首帧图：{shot_id}.image.txt 生成后上传；方言规则见 references/model-dialects.md
[镜头：{camera_move}]
[从首帧出发的运动描述：主体动作 + 表情变化 + 镜头运动，运动量与 {duration}s 匹配，不写跨镜时间]{dialogue_line}"""

FL2V_TEMPLATE = """# 图生视频提示词（首尾帧 FL2V）— {shot_id} | 时长 {duration}s | 模型 {model}
# 首帧 = {shot_id}.image.txt；尾帧 = {tail_hint}
# 描述首帧到尾帧的连续运动路径，中间状态平滑，勿跳变
[运动路径描述]{dialogue_line}"""

T2V_TEMPLATE = """# 文生视频提示词（空镜/氛围镜）— {shot_id} | 时长 {duration}s | 模型 {model}
# 无首帧，纯文字生成；锚点不适用，环境描述要具体
[环境 + 动态元素（雨/风/光斑） + {camera_move} + 氛围]"""


def read_csv(path):
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        rows = [dict(r) for r in csv.DictReader(f)]
    for r in rows:
        for k in list(r.keys()):
            if r[k] is not None:
                r[k] = r[k].strip()
    return rows


def read_anchors(path):
    anchors = {}
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            name = (r.get("name") or r.get("角色") or "").strip()
            anchor = (r.get("anchor") or r.get("锚点") or "").strip()
            if name:
                anchors[name] = anchor
    return anchors


def validate(rows, model, anchors):
    errors, warns = [], []
    lo, hi = MODEL_DURATION.get(model, MODEL_DURATION["generic"])
    seen = set()
    for i, r in enumerate(rows, 1):
        sid = r.get("shot_id", "") or f"#row{i}"
        if not SHOT_ID_RE.match(sid):
            errors.append(
                f"{sid}: shot_id 仅允许字母/数字/下划线/连字符（[A-Za-z0-9_-]+），"
                "避免路径逃逸；请改成简单序号如 S01"
            )
        for col in REQUIRED_COLS:
            if not r.get(col):
                errors.append(f"{sid}: 必填列 {col} 为空")
        fm = (r.get("frame_mode") or "").lower()
        if fm and fm != "t2v" and not r.get("characters"):
            errors.append(f"{sid}: i2v/fl2v 镜头必填 characters（t2v 空镜可空）")
        if fm and fm not in FRAME_MODES:
            errors.append(f"{sid}: frame_mode 非法值 {fm}（应为 i2v/fl2v/t2v）")
        try:
            dur = float(r.get("duration_s") or 0)
            if dur and not (lo <= dur <= hi):
                warns.append(f"{sid}: 时长 {dur:g}s 超出 {model} 近似档位 {lo}-{hi}s（以官方文档为准）")
        except ValueError:
            errors.append(f"{sid}: duration_s 不是数字")
        for name in [c for c in (r.get("characters") or "").replace("＋", "+").split("+") if c]:
            name = name.split("@")[0].strip()
            seen.add(name)
            if anchors and name not in anchors:
                warns.append(f"{sid}: 角色「{name}」不在锚点表（Step 2 先补锚点）")
    ids = [r.get("shot_id") for r in rows]
    if len(ids) != len(set(ids)):
        errors.append("shot_id 存在重复")
    return errors, warns


def anchor_block(characters, anchors):
    if not anchors:
        return "[锚点串：先按 references/consistency-anchor.md 生成并确认锚点表]"
    parts = []
    for name in [c for c in characters.replace("＋", "+").split("+") if c]:
        base = name.split("@")[0].strip()
        a = anchors.get(base, f"[{base} 锚点缺失]")
        parts.append(f"<ANCHOR {name}> {a} </ANCHOR>")
    return "\n".join(parts)


def scaffold(rows, model, anchors, outdir):
    made = []
    for i, r in enumerate(rows):
        # 安全：以清洗后的 shot_id 作为文件名片段，杜绝拼路径逃逸（validate 已前置拦截，此处兜底）
        sid = safe_name(r["shot_id"])
        fm = (r.get("frame_mode") or "i2v").lower()
        common = {
            "shot_id": sid, "scene": r.get("scene", ""), "shot_size": r.get("shot_size", ""),
            "duration": r.get("duration_s", ""), "model": model,
            "camera_move": r.get("camera_move", ""),
            "anchors": anchor_block(r.get("characters", ""), anchors),
            "visual": r.get("action_visual", ""),
            "negative": ("负面：" + r["negative_extra"]) if r.get("negative_extra") else "负面：见全局负面库",
            "dialogue_line": ("\n[台词/口型]：" + r["dialogue_vo"]) if r.get("dialogue_vo") else "",
        }
        (outdir / f"{sid}.image.txt").write_text(IMAGE_TEMPLATE.format(**common), encoding="utf-8")
        if fm == "i2v":
            vf, text = f"{sid}.video.i2v.txt", I2V_TEMPLATE.format(**common)
        elif fm == "fl2v":
            nxt = safe_name(rows[i + 1]["shot_id"]) if i + 1 < len(rows) else "悬念定格（集末钩子画面）"
            hint = f"下一镜 {nxt} 的首帧（跨镜衔接）" if i + 1 < len(rows) else nxt
            vf = f"{sid}.video.fl2v.txt"
            text = FL2V_TEMPLATE.format(tail_hint=hint, **common)
        else:
            vf, text = f"{sid}.video.t2v.txt", T2V_TEMPLATE.format(**common)
        (outdir / vf).write_text(text, encoding="utf-8")
        made.append({"shot_id": sid, "scene": common["scene"], "shot_size": common["shot_size"],
                     "camera_move": r.get("camera_move", ""), "duration_s": common["duration"],
                     "characters": r.get("characters", ""), "frame_mode": fm, "model": model,
                     "image_file": f"{sid}.image.txt", "video_file": vf, "status": "todo"})
    return made


def write_manifest(manifest, outdir):
    cols = list(manifest[0].keys()) if manifest else ["shot_id"]
    with open(outdir / "manifest.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(manifest)
    (outdir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description="短剧分镜提示词批量导出")
    ap.add_argument("--input", required=True, help="标准化分镜表 CSV")
    ap.add_argument("--outdir", default="out/EP01", help="输出目录（默认 out/EP01）")
    ap.add_argument("--mode", choices=["scaffold", "manifest", "both"], default="both")
    ap.add_argument("--model", choices=list(MODEL_DURATION), default="generic")
    ap.add_argument("--anchors", help="角色锚点表 CSV（列：name,anchor），可选")
    ap.add_argument("--check", action="store_true", help="只校验，不生成文件")
    args = ap.parse_args()

    rows = read_csv(args.input)
    if not rows:
        sys.exit("✗ 分镜表为空")
    missing_cols = [c for c in REQUIRED_COLS if c not in rows[0]]
    if missing_cols:
        sys.exit(f"✗ 分镜表缺少列：{', '.join(missing_cols)}（规范见 references/storyboard-spec.md）")

    anchors = read_anchors(args.anchors) if args.anchors else {}
    errors, warns = validate(rows, args.model, anchors)

    print(f"分镜表：{len(rows)} 镜 | 模型：{args.model}")
    for w in warns:
        print(f"⚠ {w}")
    if errors:
        for e in errors:
            print(f"✗ {e}")
        sys.exit(f"✗ 校验未通过：{len(errors)} 个错误，请先修复分镜表")
    if not anchors:
        print("⚠ 未提供 --anchors 锚点表：脚手架中锚点为占位符，务必先完成 Step 2 再批量出图")
    print("✓ 校验通过" if not warns else f"✓ 校验通过（{len(warns)} 条提醒）")

    if args.check:
        return

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    manifest = []
    if args.mode in ("scaffold", "both"):
        manifest = scaffold(rows, args.model, anchors, outdir)
        print(f"✓ 生成 {len(manifest)} 镜提示词骨架 → {outdir}/")
    if args.mode in ("manifest", "both"):
        if not manifest:
            manifest = [{"shot_id": r["shot_id"], "frame_mode": r.get("frame_mode", ""),
                         "model": args.model, "status": "todo"} for r in rows]
        write_manifest(manifest, outdir)
        print(f"✓ manifest.csv / manifest.json → {outdir}/")
    print(f"下一步：按 references/model-dialects.md 的 {args.model} 方言填写占位符，"
          f"再按 manifest 逐镜粘贴到目标工具。")


if __name__ == "__main__":
    main()
