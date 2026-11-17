#!/usr/bin/env python3
"""扫描主题组件库中的 HTML 代码块，检测已知会导致微信公众号排版问题的写法。

在交付排版产物之前，先在组件库源头拦截问题——如果组件库本身的 HTML
包含公众号不支持的写法，用它们生成的文章必然出错。

用法:
    component_lint.py [skill-root-dir]

退出码: 0 = 全部通过, 1 = 发现严重问题
"""

import re
import sys
from pathlib import Path

# 严重问题：会导致粘贴后样式失效
CRITICAL_PATTERNS = [
    (r"white-space\s*:\s*pre",
     "white-space:pre 会把源码缩进渲染成多余空白，代码块应逐行用 <p>"),
    (r"</?div[\s>]",
     "<div> 在公众号会被改写，应替换为 <section>"),
    (r"\sclass\s*=",
     "class 属性会被编辑器移除"),
    (r"\sid\s*=",
     "id 属性会被编辑器移除"),
    (r"<style[\s>]",
     "<style> 标签会被编辑器移除"),
    (r"<script[\s>]",
     "<script> 标签会被编辑器移除"),
    (r"<link[\s>]",
     "<link> 标签会被编辑器移除"),
    (r"position\s*:\s*(?:fixed|absolute|sticky)",
     "position 定位在公众号不可用"),
    (r"display\s*:\s*grid",
     "display:grid 不可用，应改用 flex 布局"),
    (r"float\s*:",
     "float 在公众号不可用"),
    (r"var\s*\(\s*--",
     "CSS 变量语法在公众号不可用，需写死具体值"),
    (r"@(?:media|keyframes|import)",
     "@media / @keyframes / @import 在公众号不可用"),
]

# 建议检查：非致命但影响排版质量
DASHED_BORDER_ALL_SIDES = re.compile(r"border\s*:\s*[^;{}]*dashed", re.I)
IS_CENTERED = re.compile(r"text-align\s*:\s*center", re.I)

HTML_BLOCK_FINDER = re.compile(r"```html\s*\n(.*?)```", re.S)


def scan_markdown(path: Path) -> list[tuple[str, str]]:
    """从 Markdown 文件提取 HTML 代码块，返回 (级别, 描述) 列表。"""
    content = path.read_text(encoding="utf-8", errors="replace")
    findings: list[tuple[str, str]] = []
    reported = set()

    for match in HTML_BLOCK_FINDER.finditer(content):
        block = match.group(1)

        for pattern, description in CRITICAL_PATTERNS:
            if re.search(pattern, block, re.I) and description not in reported:
                findings.append(("critical", description))
                reported.add(description)

        # 四周虚线框：居中素材占位块允许使用，其余情况提醒
        if DASHED_BORDER_ALL_SIDES.search(block) and not IS_CENTERED.search(block):
            msg = "四周 dashed 虚线框用于正文强调过于笨重，建议改用左竖条；仅居中素材占位块可用"
            if msg not in reported:
                findings.append(("advisory", msg))
                reported.add(msg)

    return findings


def discover_component_files(root: Path) -> list[Path]:
    """找到所有主题组件库和通用组件文件。"""
    results = []
    refs_dir = root / "references"
    if not refs_dir.is_dir():
        return results
    results.extend(refs_dir.glob("theme-*.md"))
    common = refs_dir / "common-components.md"
    if common.exists():
        results.append(common)
    return sorted(results)


def main():
    root_arg = sys.argv[1] if len(sys.argv) > 1 else "."
    root = Path(root_arg)

    files = discover_component_files(root)
    if not files:
        print(f"未找到组件库文件（{root}/references/theme-*.md）")
        sys.exit(1)

    total_critical = 0
    total_advisory = 0
    clean_count = 0

    print(f"组件库源头检查: {len(files)} 个文件\n")

    for path in files:
        findings = scan_markdown(path)
        if not findings:
            clean_count += 1
            continue

        critical = [d for lv, d in findings if lv == "critical"]
        advisory = [d for lv, d in findings if lv == "advisory"]
        total_critical += len(critical)
        total_advisory += len(advisory)

        print(f"[{path.name}]")
        for desc in critical:
            print(f"  严重 - {desc}")
        for desc in advisory:
            print(f"  建议 - {desc}")
        print()

    print(f"结果: {clean_count}/{len(files)} 文件通过, "
          f"严重 {total_critical}, 建议 {total_advisory}")

    if total_critical == 0 and total_advisory == 0:
        print("全部组件库检查通过")

    sys.exit(1 if total_critical else 0)


if __name__ == "__main__":
    main()
