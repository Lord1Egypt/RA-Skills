#!/usr/bin/env python3
"""检查 HTML 产物是否符合微信公众号编辑器的技术约束。

微信公众号编辑器在粘贴富文本时会过滤大量 HTML 元素和 CSS 属性，
导致样式丢失。本工具将这些已知的平台约束固化为自动化检查，
在交付前确定性地拦截问题。

约束来源：微信公众号编辑器的实际粘贴行为（经验性测试，非官方文档）。
官方未公开完整的过滤规则列表，以下规则基于反复测试总结，
可能随编辑器版本更新而变化。

用法:
    validate_output.py <file.html>
    validate_output.py --stdin < file.html

退出码: 0 = 通过, 1 = 存在必须修复的问题
"""

import argparse
import datetime
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "validation_config.json"


def _load_config():
    """从 validation_config.json 加载规则配置。"""
    try:
        with open(CONFIG_PATH, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


_CONFIG = _load_config()

if _CONFIG:
    LAST_TESTED = _CONFIG["last_tested"]
    FILTERED_TAGS = _CONFIG["filtered_tags"]
    STRIPPED_ATTRS = _CONFIG["stripped_attrs"]
    UNSUPPORTED_CSS = [(p, r) for p, r in _CONFIG["unsupported_css"]]
    MAX_ANCHORS = _CONFIG.get("content_rules", {}).get("max_anchors", 5)
    UNDERLINE_PARA_THRESHOLD = _CONFIG.get("content_rules", {}).get("min_underlines_per_para_threshold", 5)
else:
    LAST_TESTED = "2026-07"
    FILTERED_TAGS = {
        "style": "编辑器会移除 <style>，所有样式必须写在 style 属性里",
        "script": "编辑器会移除 <script>",
        "link": "编辑器会移除 <link>（外部 CSS / 字体无法加载）",
        "meta": "编辑器会移除 <meta>",
        "iframe": "编辑器不支持 <iframe>",
        "form": "编辑器不支持 <form>",
        "input": "编辑器不支持 <input>",
        "div": "编辑器会改写 <div>，应改用 <section>",
    }
    STRIPPED_ATTRS = {
        "class": "编辑器会移除 class 属性",
        "id": "编辑器会移除 id 属性",
    }
    UNSUPPORTED_CSS = [
        (r"position\s*:\s*(?:fixed|absolute|sticky)", "不支持 position 定位"),
        (r"float\s*:", "不支持 float"),
        (r"@media", "不支持 @media 查询"),
        (r"@keyframes", "不支持 @keyframes 动画"),
        (r"@import", "不支持 @import"),
        (r"display\s*:\s*grid", "不支持 display:grid，应改用 flex"),
        (r"var\s*\(\s*--", "不支持 CSS 自定义属性（变量）"),
        (r"url\s*\(\s*['\"]?https?://[^)]*\.(?:woff2?|ttf|otf)", "不支持外部字体文件引用"),
    ]
    MAX_ANCHORS = 5
    UNDERLINE_PARA_THRESHOLD = 5

# 危险的事件处理器属性（XSS 风险）
EVENT_HANDLER_PATTERN = re.compile(r"\son\w+\s*=", re.I)

# 中文 Unicode 范围
CJK_RANGE = re.compile(r"[\u4e00-\u9fff\u3400-\u4dbf]")

# 中文字符后紧跟半角标点 → 应改为全角
NEEDS_FULLWIDTH = re.compile(r"[\u4e00-\u9fff\u3400-\u4dbf][,;!?]")

# 西文直引号出现在中文上下文中
STRAIGHT_QUOTE = re.compile(r"[\"']")

# 等宽字体或 pre-wrap 特征 → 判定为代码区域
CODE_AREA = re.compile(r"monospace|courier|consolas|sf.?mono|pre-wrap|white-space\s*:\s*pre", re.I)

# 这些标签内部的内容不参与公众号正文粘贴
NON_BODY_TAGS = {"head", "title", "style", "script", "meta", "link"}


class WeChatHTMLAnalyzer(HTMLParser):
    """解析 HTML，记录每个文本节点的上下文信息。

    与简单的深度计数不同，这里维护一个显式的「祖先链」，
    通过查询祖先链判断文本节点是否处于 leaf span 或代码区域内。
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        # 祖先链：记录从根到当前节点的路径
        self._ancestors: list[tuple[str, bool, bool]] = []
        # 段落栈：跟踪当前 <p>（cjk=含中文 / underline=有下划线 / is_body=正文段）
        self._p_stack: list[dict] = []
        # 结果收集
        self.total_leaf_spans = 0
        self.text_outside_leaf: list[tuple[str, str]] = []
        self.punctuation_issues: list[str] = []
        # 正文段落下划线分布（仅统计正文段，排除标题/引言/表格/代码）
        self.body_paragraph_stats: list[bool] = []

    def handle_starttag(self, tag, attrs):
        attr_map = dict(attrs)
        wrapped = tag == "span" and "leaf" in attr_map
        styled = attr_map.get("style", "") or ""
        is_code_context = bool(CODE_AREA.search(styled))

        if wrapped:
            self.total_leaf_spans += 1

        if tag == "p":
            self._p_stack.append({
                "cjk": False,
                "underline": False,
                "is_body": bool(re.search(r"font-size:\s*16px", styled, re.I)),
            })
        elif wrapped and "border-bottom" in styled and self._p_stack:
            self._p_stack[-1]["underline"] = True

        self._ancestors.append((tag, wrapped, is_code_context))

    def handle_endtag(self, tag):
        # 从栈顶向下找到匹配的标签，截断
        for i in range(len(self._ancestors) - 1, -1, -1):
            if self._ancestors[i][0] == tag:
                del self._ancestors[i:]
                break

        if tag == "p" and self._p_stack:
            entry = self._p_stack.pop()
            if entry["cjk"] and entry["is_body"]:
                self.body_paragraph_stats.append(entry["underline"])

    def handle_data(self, raw):
        content = raw.strip()
        if not content or not CJK_RANGE.search(content):
            return

        # 跳过非正文区域
        if any(a[0] in NON_BODY_TAGS for a in self._ancestors):
            return

        if self._p_stack:
            self._p_stack[-1]["cjk"] = True

        in_leaf = any(a[1] for a in self._ancestors)
        in_code = any(a[2] for a in self._ancestors)

        if not in_leaf:
            nearest = self._ancestors[-1][0] if self._ancestors else "(root)"
            self.text_outside_leaf.append((content[:40], nearest))

        if not in_code:
            if NEEDS_FULLWIDTH.search(content) or STRAIGHT_QUOTE.search(content):
                self.punctuation_issues.append(content[:40])


def check_filtered_tags(html: str) -> list[str]:
    """检测会被编辑器过滤的 HTML 元素。"""
    problems = []
    for tag, reason in FILTERED_TAGS.items():
        pattern = re.compile(rf"<{tag}[\s/>]", re.I)
        hits = len(pattern.findall(html))
        if hits:
            problems.append(f"{reason}（{hits} 处）")
    return problems


def check_stripped_attrs(html: str) -> list[str]:
    """检测会被编辑器移除的属性。"""
    problems = []
    for attr, reason in STRIPPED_ATTRS.items():
        pattern = re.compile(rf"\s{attr}\s*=", re.I)
        hits = len(pattern.findall(html))
        if hits:
            problems.append(f"{reason}（{hits} 处）")
    return problems


def check_event_handlers(html: str) -> list[str]:
    """检测危险的 HTML 事件处理器属性（XSS 风险）。"""
    problems = []
    hits = len(EVENT_HANDLER_PATTERN.findall(html))
    if hits:
        problems.append(f"检测到事件处理器属性（onerror/onload 等，{hits} 处），存在 XSS 风险")
    return problems


def check_unsupported_css(html: str) -> list[str]:
    """检测不支持的 CSS 特性。"""
    problems = []
    for pattern, reason in UNSUPPORTED_CSS:
        rx = re.compile(pattern, re.I)
        hits = len(rx.findall(html))
        if hits:
            problems.append(f"{reason}（{hits} 处）")
    return problems


def check_placeholder_leaks(html: str) -> list[str]:
    """检测未替换的模板占位符（如 {{作者名}}、{{anything}}、{{ xxx }}）。"""
    pattern = re.compile(r"\{\{[^}]+\}\}")
    matches = pattern.findall(html)
    warnings = []
    seen = {}
    for m in matches:
        seen[m] = seen.get(m, 0) + 1
    for match, n in seen.items():
        warnings.append(
            f"未替换的占位符 {match}（{n} 处），粘贴前必须替换为实际内容"
        )
    return warnings


def _is_neutral_color(hex_str):
    """判断 hex 色值是否为中性色（黑/白/灰），用于排除非锚点的结构性加粗。

    中性色 = 饱和度低（s<0.15）或亮度极端（<0.12 或 >0.92）。
    这些是标题色/正文色/白色文字，不是主题主色锚点。
    """
    h = hex_str.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    try:
        r, g, b = int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255
    except (ValueError, IndexError):
        return False
    cmax, cmin = max(r, g, b), min(r, g, b)
    l = (cmax + cmin) / 2
    if cmax == cmin:
        return True  # 纯灰/黑/白
    s = (cmax - cmin) / (2 - cmax - cmin) if l > 0.5 else (cmax - cmin) / (cmax + cmin)
    return s < 0.15 or l < 0.12 or l > 0.92


def _relative_luminance(hex_str):
    """计算 hex 色值的相对亮度（WCAG 标准）。"""
    h = hex_str.lstrip("#")
    r, g, b = int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255

    def linear(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * linear(r) + 0.7152 * linear(g) + 0.0722 * linear(b)


def _contrast_ratio(hex1, hex2="#ffffff"):
    """计算两个 hex 色值之间的对比度（WCAG 标准）。"""
    l1 = _relative_luminance(hex1)
    l2 = _relative_luminance(hex2)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def check_content_quality(html: str, analyzer: WeChatHTMLAnalyzer) -> list[str]:
    """检查内容智能处理规则的量化指标（warnings 级别）。"""
    warnings = []

    # 锚点层：主色加粗 span 的数量（全文 ≤5 处）
    # 先找所有 font-weight:bold 的 span，再排除中性色（标题/正文/白色）加粗
    bold_span_pattern = re.compile(
        r'<span[^>]*style="([^"]*font-weight:bold[^"]*)"[^>]*>', re.I
    )
    color_in_style = re.compile(r'color:\s*(#[0-9a-fA-F]{3,6})', re.I)
    anchor_count = 0
    for match in bold_span_pattern.finditer(html):
        style = match.group(1)
        color_match = color_in_style.search(style)
        if color_match and not _is_neutral_color(color_match.group(1)):
            anchor_count += 1
        elif not color_match:
            # 加粗但无 color 属性 → 继承正文色，不是主色锚点
            pass

    if anchor_count > MAX_ANCHORS:
        warnings.append(
            f"锚点层（主色加粗）共 {anchor_count} 处，超过 ≤{MAX_ANCHORS} 处上限，"
            f"过度强调等于没有重点"
        )

    # 下划线分布：正文段覆盖率（DOM 级统计，排除标题/引言/表格/代码段）
    stats = analyzer.body_paragraph_stats
    if len(stats) > UNDERLINE_PARA_THRESHOLD:
        covered = sum(stats)
        if covered == 0:
            warnings.append(
                f"共 {len(stats)} 个正文段落但未检测到任何关键词下划线，"
                f"应每段标记 1-3 个核心短语"
            )
        elif covered / len(stats) < 0.5:
            warnings.append(
                f"仅 {covered}/{len(stats)} 个正文段落有关键词下划线，"
                f"应每段标记 1-3 个核心短语（有的段标有的段漏，焦点会丢失）"
            )

    return warnings


def check_color_contrast(html: str) -> list[str]:
    """检查文字颜色与白色背景的对比度是否满足 WCAG AA 标准。"""
    warnings = []
    style_pattern = re.compile(r'style="([^"]*)"', re.I)
    color_re = re.compile(r"color:\s*#([0-9a-fA-F]{3,6})", re.I)
    fontsize_re = re.compile(r"font-size:\s*(\d+)px", re.I)
    bold_re = re.compile(r"font-weight:\s*bold", re.I)
    bg_re = re.compile(r"background(?:-color)?\s*:\s*([^;]+)", re.I)

    for match in style_pattern.finditer(html):
        style = match.group(1)
        # 跳过带非白色背景的元素
        bg_match = bg_re.search(style)
        if bg_match:
            bg_val = bg_match.group(1).strip().lower()
            if bg_val not in ("#fff", "#ffffff", "white"):
                continue
        color_match = color_re.search(style)
        size_match = fontsize_re.search(style)
        if not color_match or not size_match:
            continue
        hex_color = color_match.group(1)
        font_size = int(size_match.group(1))
        is_bold = bool(bold_re.search(style))
        is_large = font_size >= 18 or (font_size >= 14 and is_bold)
        ratio = _contrast_ratio(hex_color)
        threshold = 3.0 if is_large else 4.5
        if ratio < threshold:
            normal = not is_large
            warnings.append(
                f"文字颜色 #{hex_color} 与白色背景对比度 {ratio:.1f}:1，"
                f"低于 WCAG AA 标准（{'4.5' if normal else '3.0'}:1）"
            )
    return warnings


def analyze(html: str) -> dict:
    """对 HTML 执行全套检查，返回结构化报告。"""
    errors = []
    warnings = []

    # 第一阶段：正则扫描禁止的模式
    errors.extend(check_filtered_tags(html))
    errors.extend(check_stripped_attrs(html))
    errors.extend(check_event_handlers(html))
    errors.extend(check_unsupported_css(html))

    # 第二阶段：解析 DOM 结构，检查文本包裹和标点
    analyzer = WeChatHTMLAnalyzer()
    try:
        analyzer.feed(html)
    except Exception as exc:
        warnings.append(f"HTML 解析过程中断: {exc}")

    has_chinese = bool(CJK_RANGE.search(html))

    if has_chinese and analyzer.total_leaf_spans == 0:
        errors.append(
            "全文未检测到任何 <span leaf=\"\"> 包裹，"
            "粘贴后样式将大面积丢失"
        )
    elif analyzer.text_outside_leaf:
        samples = "、".join(
            f"[{text[:20]}…] in <{tag}>" for text, tag in analyzer.text_outside_leaf[:5]
        )
        warnings.append(
            f"{len(analyzer.text_outside_leaf)} 处中文文本缺少 <span leaf> 包裹: {samples}"
        )

    if analyzer.punctuation_issues:
        samples = "、".join(f"[{s[:20]}…]" for s in analyzer.punctuation_issues[:5])
        warnings.append(
            f"{len(analyzer.punctuation_issues)} 处可能需要全角标点（代码区域除外）: {samples}"
        )

    # 内容智能处理检查
    warnings.extend(check_content_quality(html, analyzer))

    # 占位符泄漏检查
    warnings.extend(check_placeholder_leaks(html))

    # 颜色对比度检查
    warnings.extend(check_color_contrast(html))

    return {
        "errors": errors,
        "warnings": warnings,
        "leaf_count": analyzer.total_leaf_spans,
    }


def _staleness_warning(ym):
    """平台规则实测日期超过 90 天则提示重新粘贴测试（编辑器可能已更新规则）。"""
    try:
        tested = datetime.date(*map(int, ym.split("-")), 1)
        days = (datetime.date.today() - tested).days
        if days > 90:
            return (
                f"平台规则上次实测于 {ym}（已 {days} 天），微信公众号编辑器可能已更新过滤规则，"
                f"请重新粘贴测试并更新 validation_config.json 的 last_tested"
            )
    except (ValueError, TypeError):
        return None
    return None


def format_report(report: dict, source: str) -> str:
    """将检查结果格式化为可读报告。"""
    lines = []
    lines.append(f"检查目标: {source}")
    lines.append(f"规则验证时间: {LAST_TESTED}")
    stale = _staleness_warning(LAST_TESTED)
    if stale:
        lines.append(f"⚠ {stale}")
    lines.append(f"<span leaf> 包裹计数: {report['leaf_count']}")
    lines.append("")

    if report["errors"]:
        lines.append(f"[严重] {len(report['errors'])} 个问题必须修复:")
        for item in report["errors"]:
            lines.append(f"  - {item}")
        lines.append("")

    if report["warnings"]:
        lines.append(f"[提醒] {len(report['warnings'])} 项建议检查:")
        for item in report["warnings"]:
            lines.append(f"  - {item}")
        lines.append("")

    if not report["errors"] and not report["warnings"]:
        lines.append("全部通过，可安全粘贴到公众号编辑器")
    elif not report["errors"]:
        lines.append("无严重问题，可粘贴（建议处理提醒项）")

    lines.append("")
    lines.append("注意: 以上规则基于经验性测试，微信公众号官方未公开完整过滤规则。")
    lines.append("规则可能随编辑器版本更新而变化。")

    return "\n".join(lines)


COPYRIGHT_FOOTER = "©2026 Qomob.AI 由WeChatLayout微信公众号排版引擎驱动"


def check_ops_quality(html: str) -> list[str]:
    """运营维度检查：标题长度、段落长度、图片数、阅读时长、版权脚注（warnings 级别）。"""
    warnings = []

    # 版权脚注：所有产物必带固定版权行（完成判据之一）
    if COPYRIGHT_FOOTER not in html:
        warnings.append(
            f"未检测到版权脚注（{COPYRIGHT_FOOTER}），"
            f"正文末尾必须追加通用库「版权脚注」组件"
        )

    # 提取纯文本（去标签）
    text_only = re.sub(r"<[^>]+>", "", html)
    cjk_chars = len(CJK_RANGE.findall(text_only))

    # 标题长度：找最大的 font-size 文本作为标题粗略判断
    title_pattern = re.compile(r'font-size:\s*(\d+)px', re.I)
    sizes = [int(m) for m in title_pattern.findall(html)]
    max_size = max(sizes) if sizes else 0
    if max_size >= 22:
        title_spans = re.findall(
            rf'font-size:\s*{max_size}px[^"]*"[^>]*><span[^>]*>([^<]+)</span>',
            html, re.I
        )
        for title_text in title_spans[:1]:
            title_len = len(title_text)
            if title_len > 22:
                warnings.append(
                    f"标题「{title_text[:15]}…」共 {title_len} 字，"
                    f"建议 ≤22 字以保证手机端完整显示"
                )

    # 图片数量
    img_count = len(re.findall(r'<img\s', html, re.I))
    if img_count == 0:
        warnings.append("未检测到图片，公众号文章建议配图提升阅读体验")

    # 阅读时长估算（按 400 字/分钟）
    if cjk_chars > 0:
        read_minutes = max(1, round(cjk_chars / 400))
        if cjk_chars < 200:
            warnings.append(f"全文仅约 {cjk_chars} 字，内容可能过于单薄")
        elif cjk_chars > 3000:
            warnings.append(
                f"全文约 {cjk_chars} 字（预计 {read_minutes} 分钟阅读），"
                f"较长文章建议添加章节导读"
            )

    return warnings


def main():
    parser = argparse.ArgumentParser(
        description="检查 HTML 是否符合微信公众号编辑器技术约束"
    )
    parser.add_argument("file", nargs="?", help="待检查的 HTML 文件")
    parser.add_argument("--stdin", action="store_true", help="从标准输入读取")
    parser.add_argument("--ops", action="store_true",
                        help="额外执行运营维度检查（标题长度/图片数/阅读时长/版权脚注）")
    args = parser.parse_args()

    if args.stdin or not args.file:
        html_content = sys.stdin.read()
        source_name = "<stdin>"
    else:
        with open(args.file, encoding="utf-8", errors="replace") as f:
            html_content = f.read()
        source_name = args.file

    report = analyze(html_content)
    if args.ops:
        report["warnings"].extend(check_ops_quality(html_content))
    print(format_report(report, source_name))
    sys.exit(1 if report["errors"] else 0)


if __name__ == "__main__":
    main()
