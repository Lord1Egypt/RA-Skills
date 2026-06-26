#!/usr/bin/env python3
"""
推文发布前预检脚本（Pre-flight Check）

用法：python3 scripts/preflight_check.py <html_file>

执行所有检查项，全部通过才允许调用 API。
退出码：0 = 全部通过，1 = 有未通过项
"""

import sys
import re


def check(filepath: str) -> bool:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    lines = content.split("\n")

    all_ok = True
    results = []

    def ok(name: str, detail: str = ""):
        results.append(f"  ✅ {name}" + (f" — {detail}" if detail else ""))

    def fail(name: str, detail: str = ""):
        nonlocal all_ok
        all_ok = False
        results.append(f"  ❌ {name}" + (f" — {detail}" if detail else ""))

    # ── 1. 占位符检查 ──
    placeholders = ["{BANNER_URL}", "{DIVIDER_URL}", "{COVER_URL}"]
    found_placeholders = [p for p in placeholders if p in content]
    if found_placeholders:
        fail("占位符残留", "发现未替换：{}".format(", ".join(found_placeholders)))
    else:
        ok("占位符检查", "无残留")

    # ── 2. Section 嵌套检查 ──
    depth = 0
    max_depth = 0
    nesting_bad_lines = []
    for i, line in enumerate(lines, 1):
        opens = line.count("<section") - line.count("</section") - line.count("<!--")
        closes = line.count("</section")
        depth += opens - closes
        if depth > max_depth:
            max_depth = depth
        if depth > 1:
            nesting_bad_lines.append("第{}行 (depth={})".format(i, depth))

    if max_depth > 1:
        fail("Section 嵌套", "最大嵌套深度 {}，违规行：{}".format(max_depth, nesting_bad_lines[:5]))
    else:
        ok("Section 嵌套", "最大深度 1，无嵌套")

    # ── 3. 标签闭合检查 ──
    opens = content.count("<section")
    closes = content.count("</section>")
    if opens != closes:
        fail("Section 闭合", "打开 {} 次，闭合 {} 次（应相等）".format(opens, closes))
    else:
        ok("Section 闭合", "打开/闭合各 {} 次".format(opens))

    # ── 4. Word-break 检查 ──
    section_pattern = re.compile(r'<section\s+style="([^"]*)"')
    total_sections = len(section_pattern.findall(content))
    wb_pattern = re.compile(r'<section\s+style="[^"]*word-break[^"]*white-space[^"]*"')
    wb_sections = len(wb_pattern.findall(content))
    missing_wb = total_sections - wb_sections

    if missing_wb > 0:
        fail("Word-break 属性", "{} 个 section 中 {} 个缺少 word-break + white-space".format(
            total_sections, missing_wb))
    else:
        ok("Word-break 属性", "全部 {} 个 section 均已设置".format(total_sections))

    # ── 5. Padding 一致性检查（跳过表格元素） ──
    no_table_lines = []
    for line in lines:
        if "<td" in line or "<tr" in line or "<th" in line:
            continue
        no_table_lines.append(line)
    no_table = "\n".join(no_table_lines)

    side_paddings = re.findall(r"padding:\d+px\s+(\d+)px", no_table)
    non_20 = [p for p in side_paddings if p != "20"]
    if non_20:
        seen = {}
        for p in non_20:
            seen[p] = seen.get(p, 0) + 1
        exceptions_ok = True
        allowed_exceptions = {"10", "6", "12", "44", "36", "32", "24", "0"}
        for val, count in sorted(seen.items()):
            if val in allowed_exceptions and count <= 5:
                ok("侧边距 {}px".format(val), "出现 {} 次（特殊位置，允许）".format(count))
            else:
                fail("Padding 一致性", "非 20px 侧边距：{}px 出现 {} 次".format(val, count))
                exceptions_ok = False
        if exceptions_ok:
            pass  # All exceptions were acceptable
    else:
        ok("Padding 一致性", "全部 {} 处侧边距均为 20px".format(len(side_paddings)))

    # ── 6. pre-wrap 残留检查 ──
    if "pre-wrap" in content:
        fail("pre-wrap 残留", "发现 white-space:pre-wrap，中文会逐字断行")
    else:
        ok("pre-wrap 检查", "无残留")

    # ── 7. 内容大小检查 ──
    byte_size = len(content.encode("utf-8"))
    if byte_size > 64000:
        fail("内容大小", "{} bytes（超过微信 64KB 限制）".format(byte_size))
    elif byte_size > 20000:
        ok("内容大小", "{} bytes（超过 20KB 建议值，但仍可发布）".format(byte_size))
    else:
        ok("内容大小", "{} bytes".format(byte_size))

    # ── 8. 必含内容检查 ──
    must_have = [
        ("Banner 图片", "mmbiz.qpic"),
        ("Footer 品牌签名", "巡梦人"),
        ("金色强调色", "#d4a574"),
    ]
    for name, keyword in must_have:
        if keyword in content:
            ok("必含：{}".format(name), "含关键词「{}」".format(keyword))
        else:
            fail("必含：{}".format(name), "未找到「{}」".format(keyword))

    # ── 9. 禁用词检查 ──
    excluded = ["做梦", "发呆", "REM", "DMN"]
    found_excluded = [w for w in excluded if w in content]
    if found_excluded:
        fail("禁用词检查", "发现禁用词：{}".format(", ".join(found_excluded)))
    else:
        ok("禁用词检查", "无禁用词")

    # ── 输出结果 ──
    print("\n📋 预检报告 — {}".format(filepath))
    print("   文件大小：{} bytes / {} 字符".format(byte_size, len(content)))
    print("   Section 数：{}".format(total_sections))
    print()
    for r in results:
        print(r)
    print()
    if all_ok:
        print("🎉 全部检查通过，可以发布！")
    else:
        print("⚠️  有未通过项，请修复后重试。")
    print()

    return all_ok


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python3 scripts/preflight_check.py <html_file>")
        sys.exit(1)

    success = check(sys.argv[1])
    sys.exit(0 if success else 1)
