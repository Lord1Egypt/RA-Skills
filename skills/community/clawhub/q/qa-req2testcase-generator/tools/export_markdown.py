#!/usr/bin/env python3
"""
轻量 Markdown 生成脚本 — 将 P6 输出 JSON 转换为 Markdown 表格格式的测试用例文件。
用于 Excel 生成失败时的降级方案。

依赖: 无（仅使用标准库）
用法: python3 export_markdown.py --input p6_output.json --output testcases.md

退出码:
  0 = 成功
  1 = 输入文件不存在
  2 = JSON 解析失败
"""

import argparse
import json
import sys
from pathlib import Path

# 表格列定义（与 Excel 对齐，取核心可读列）
DISPLAY_COLUMNS = [
    ("case_id",          "用例编号"),
    ("title",            "用例标题"),
    ("priority",         "优先级"),
    ("menu_path",        "菜单路径"),
    ("precondition",     "预置条件"),
    ("steps",            "操作步骤"),
    ("expected_results", "期望结果"),
    ("is_smoke",         "是否冒烟"),
    ("case_type",        "用例类型"),
    ("test_category",    "测试类别"),
    ("remarks",          "备注"),
]

PRIORITY_MAP = {
    "P0": "核心", "core": "核心",
    "P1": "高", "high": "高",
    "P2": "中", "medium": "中",
    "P3": "低", "low": "低",
}


def normalize_value(key: str, raw) -> str:
    """将 JSON 值转换为 Markdown 友好字符串。"""
    try:
        if raw is None:
            return ""
        if key == "priority":
            return PRIORITY_MAP.get(str(raw), str(raw))
        if key == "is_smoke":
            return "是" if raw in (True, "true", "是") else "否"
        if key == "steps" and isinstance(raw, list):
            return "\n".join(f"{i+1}. {s}" for i, s in enumerate(raw))
        if key == "expected_results" and isinstance(raw, list):
            return "\n".join(f"{i+1}. {r}" for i, r in enumerate(raw))
        if isinstance(raw, (list, dict)):
            return json.dumps(raw, ensure_ascii=False, indent=None)
        return str(raw)
    except Exception:
        return str(raw)[:500]


def escape_md(text: str) -> str:
    """转义 Markdown 表格中的特殊字符。"""
    return text.replace("|", "\\|").replace("\n", "<br>")


def build_markdown(cases: list, task_id: str = "", domain: str = "", p7_status: str = "") -> str:
    lines = []
    lines.append(f"# 测试用例")
    lines.append("")
    if task_id:
        lines.append(f"- **任务ID**: {task_id}")
    if domain:
        lines.append(f"- **业务域**: {domain}")
    lines.append(f"- **用例总数**: {len(cases)}")
    if p7_status:
        lines.append(f"- **质量自检**: {p7_status}")
    lines.append("")

    # 统计
    smoke_count = sum(1 for c in cases if c.get("is_smoke") in (True, "true", "是"))
    priority_count = {}
    for c in cases:
        p = c.get("priority", "未知")
        p = PRIORITY_MAP.get(str(p), str(p))
        priority_count[p] = priority_count.get(p, 0) + 1
    lines.append(f"- **冒烟用例**: {smoke_count} 条")
    lines.append(f"- **优先级分布**: " + " / ".join(f"{k}{v}条" for k, v in sorted(priority_count.items())))
    lines.append("")
    lines.append("---")
    lines.append("")

    # 每条用例独立卡片
    for idx, case in enumerate(cases, 1):
        case_id = case.get("case_id", f"TC-{idx:03d}")
        title = case.get("title", "未命名用例")
        lines.append(f"## {case_id} | {title}")
        lines.append("")

        for field_key, field_name in DISPLAY_COLUMNS:
            if field_key in ("case_id", "title"):
                continue  # 已在标题中
            val = normalize_value(field_key, case.get(field_key, ""))
            if val:
                # 多行内容用引用块
                if "\n" in val:
                    lines.append(f"**{field_name}**:")
                    lines.append(f"> {val.replace(chr(10), chr(10) + '> ')}")
                else:
                    lines.append(f"**{field_name}**: {val}")
                lines.append("")

        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="P6 JSON → Markdown 测试用例")
    parser.add_argument("--input", required=True, help="P6 输出 JSON 文件路径")
    parser.add_argument("--output", required=True, help="输出 Markdown 文件路径")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"错误: 输入文件不存在 → {input_path}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"错误: JSON 解析失败 → {e}", file=sys.stderr)
        sys.exit(2)

    # 兼容两种格式
    if isinstance(data, dict):
        cases = data.get("testcases", data.get("test_cases", []))
        task_id = data.get("requirement_id", "")
        domain = data.get("domain", "")
        p7_status = ""
    elif isinstance(data, list):
        cases = data
        task_id = ""
        domain = ""
        p7_status = ""
    else:
        print("错误: JSON 顶层结构不是数组或对象", file=sys.stderr)
        sys.exit(2)

    if not cases:
        print("⚠️ 警告: 用例列表为空，将生成空 Markdown", file=sys.stderr)

    md_content = build_markdown(cases, task_id, domain, p7_status)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(str(output_path), "w", encoding="utf-8") as f:
            f.write(md_content)
    except Exception as e:
        print(f"错误: Markdown 写入失败 → {e}", file=sys.stderr)
        sys.exit(4)

    print(f"✅ 已生成 {len(cases)} 条用例 → {output_path}")


if __name__ == "__main__":
    main()
