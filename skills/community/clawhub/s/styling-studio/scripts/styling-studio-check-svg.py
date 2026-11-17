#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
styling-studio SVG 素材规范校验
校验 references/ 目录下 SVG 素材是否符合素材模板规范（XML 合法性 + 模板注释要求，见
references/styling-studio-requirements.md 的 SS2 域知识「素材体系规范」）。

支持两种形态：
  1. 独立 .svg 文件（单个种子）；
  2. 品类打包文件 .md（references/svg-bundle-*.md 平铺于 references/ 根层，多个种子合并）——
     自动按 <!-- seed: ... --> 注释切块，逐种子校验。

用法:
    python scripts/styling-studio-check-svg.py <文件或目录>

输出: 逐种子 [PASS]/[FAIL]/[WARN] + 汇总；存在 FAIL 时退出码为 1，否则 0。
依赖: 仅 Python 3.8+ 标准库。
"""
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def check_text(text: str):
    """对单个 SVG 文本块执行规范校验，返回 (级别, 消息) 列表。"""
    issues = []
    if "<svg" not in text:
        return [("FAIL", "缺少 <svg> 根元素")]
    try:
        ET.fromstring(text)
    except ET.ParseError as e:
        issues.append(("FAIL", f"XML 非法（查看器打开将报错）: {e}"))
    if not re.search(r'viewBox\s*=\s*"[^"]+"', text):
        issues.append(("FAIL", "缺少 viewBox（模板要求固定画布）"))
    if not re.search(r"<!--\s*meta:", text):
        issues.append(("FAIL", "缺少 meta 注释（编号/名称/分类/难度/标签）"))
    if not re.search(r"<!--\s*palette:", text):
        issues.append(("FAIL", "缺少 palette 注释（配色槽位，支持诊断联动替换）"))
    if not re.search(r"<!--\s*layer:", text):
        issues.append(("WARN", "未发现 layer 注释（建议按 底/主体/点缀 分层）"))
    if not re.search(r'xmlns\s*=\s*"http://www\.w3\.org/2000/svg"', text):
        issues.append(("WARN", "缺少 xmlns 命名空间声明（建议补全）"))
    if not issues:
        issues.append(("PASS", "符合素材模板规范"))
    return issues


def iter_seeds(path: Path):
    """从目标文件产出 (种子标签, SVG 文本) 序列。.md 包按 seed 注释切块。"""
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md" and path.name.startswith("svg-bundle-"):
        # seed 注释行之后最近的 <svg>...</svg> 块即为该种子
        found = re.findall(
            r'<!--\s*seed:\s*(\S+?)\s*[｜|][^\n]*?-->\s*(<svg[\s\S]*?</svg>)',
            text,
        )
        if not found:
            yield (path.name, "NO_SEED")
            return
        for seed_id, block in found:
            yield (seed_id, block)
    else:
        yield (path.name, text)


def main():
    if len(sys.argv) < 2:
        print("用法: python scripts/styling-studio-check-svg.py <文件或目录>")
        sys.exit(2)
    target = Path(sys.argv[1])
    if not target.exists():
        print(f"[FAIL] 目标不存在: {target}")
        sys.exit(2)
    if target.is_dir():
        files = sorted(target.rglob("*.svg")) + sorted(target.rglob("svg-bundle-*.md"))
    else:
        files = [target]
    if not files:
        print(f"[WARN] 未找到 SVG / SVGX 文件: {target}")
        sys.exit(0)
    n_fail = 0
    n_seeds = 0
    for f in files:
        for seed_id, block in iter_seeds(f):
            n_seeds += 1
            if block == "NO_SEED":
                print(f"❌ [FAIL] {f.name} — 未找到任何 seed 块（包格式损坏？）")
                n_fail += 1
                continue
            for lv, msg in check_text(block):
                mark = {"PASS": "✅", "FAIL": "❌", "WARN": "⚠️ "}[lv]
                print(f"{mark} [{lv}] {f.name} · {seed_id} — {msg}")
                if lv == "FAIL":
                    n_fail += 1
    print(f"----- 汇总: 文件 {len(files)} 个 / 种子 {n_seeds} 个，FAIL {n_fail} 项 -----")
    if n_fail:
        print("结论: 未通过（修复 FAIL 项后复检）")
        sys.exit(1)
    print("结论: 通过（WARN 项请人工确认）")


if __name__ == "__main__":
    main()
