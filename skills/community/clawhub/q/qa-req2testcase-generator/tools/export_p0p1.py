#!/usr/bin/env python3
"""
P0/P1 导出脚本 — 将 P0 需求理解和 P1 功能点拆解导出为 Markdown 文件。
用于段落3完成后发送给产品经理审阅。

依赖: 无（仅使用标准库）
用法: python3 export_p0p1.py --data-dir /path/to/data --output /path/to/output.md

退出码:
  0 = 成功
  1 = 输入文件不存在
  2 = JSON 解析失败
"""

import argparse
import json
import sys
from pathlib import Path


def load_json(path: Path) -> dict:
    """加载JSON文件，失败时返回空字典"""
    if not path.exists():
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"⚠️ 警告: JSON 解析失败 → {path}: {e}", file=sys.stderr)
        return {}




def _blocks_to_markdown(blocks: dict) -> str:
    """将P0的blocks结构数据转换为Markdown格式。
    
    Bugfix V4.6.9: 当blocks_markdown为空时，从blocks结构数据生成markdown。
    blocks是dict，key为block_type，value为array。
    """
    if not blocks:
        return ""
    
    lines = []
    
    # pages
    if blocks.get("pages"):
        lines.append("### 页面/功能")
        for p in blocks["pages"]:
            name = p.get("name", "未命名")
            path = p.get("page_path", "")
            desc = p.get("description", "")
            lines.append(f"- **{name}** {f'→ {path}' if path else ''}")
            if desc:
                lines.append(f"  - {desc}")
        lines.append("")
    
    # operations
    if blocks.get("operations"):
        lines.append("### 操作链路")
        for op in blocks["operations"]:
            name = op.get("name", "未命名")
            trigger = op.get("trigger", "")
            actor = op.get("actor", "")
            pre = op.get("precondition", "")
            lines.append(f"- **{name}**")
            if trigger: lines.append(f"  - 触发: {trigger}")
            if actor: lines.append(f"  - 参与者: {actor}")
            if pre: lines.append(f"  - 前置: {pre}")
        lines.append("")
    
    # business_rules
    if blocks.get("business_rules"):
        lines.append("### 业务规则")
        for br in blocks["business_rules"]:
            bid = br.get("id", "")
            desc = br.get("description", "")
            src = br.get("source", "")
            lines.append(f"- **{bid}** {desc}" if bid else f"- {desc}")
            if src: lines.append(f"  - 来源: {src}")
        lines.append("")
    
    # data_entities
    if blocks.get("data_entities"):
        lines.append("### 数据实体")
        for de in blocks["data_entities"]:
            name = de.get("name", "未命名")
            fields = de.get("fields", [])
            if isinstance(fields, list) and fields:
                field_names = [f.get("name", "") or f.get("field_name", "") for f in fields if isinstance(f, dict)]
                field_str = ", ".join(filter(None, field_names)) or "（无字段）"
                lines.append(f"- **{name}**: {field_str}")
                lines.append(f"- **{name}**")
        lines.append("")
    
    # ui_elements
    if blocks.get("ui_elements"):
        lines.append("### UI元素")
        for el in blocks["ui_elements"]:
            name = el.get("name", el.get("element_name", ""))
            etype = el.get("element_type", "")
            loc = el.get("locator", "")
            lines.append(f"- **{name}** ({etype})" + (f" → {loc}" if loc else ""))
        lines.append("")
    
    # use_cases
    if blocks.get("use_cases"):
        lines.append("### 用例")
        for uc in blocks["use_cases"]:
            name = uc.get("name", "未命名")
            actor = uc.get("actor", "")
            pre = uc.get("precondition", "")
            post = uc.get("postcondition", "")
            lines.append(f"- **{name}**")
            if actor: lines.append(f"  - 参与者: {actor}")
            if pre: lines.append(f"  - 前置: {pre}")
            if post: lines.append(f"  - 后置: {post}")
        lines.append("")
    
    # test_point_candidates
    if blocks.get("test_point_candidates"):
        lines.append("### 候选测试点")
        for tp in blocks["test_point_candidates"]:
            desc = tp.get("description", tp.get("name", ""))
            priority = tp.get("priority", "")
            if desc:
                lines.append(f"- {desc}" + (f" [{priority}]" if priority else ""))
        lines.append("")
    
    # state_transitions
    if blocks.get("state_transitions"):
        lines.append("### 状态流转")
        for st in blocks["state_transitions"]:
            obj = st.get("object", "")
            from_state = st.get("from", "")
            to = st.get("to", "")
            lines.append(f"- **{obj}**: {from_state} → {to}")
        lines.append("")
    
    # unknowns (待确认项)
    if blocks.get("unknowns"):
        lines.append("### 待确认项")
        for unk in blocks["unknowns"]:
            desc = unk.get("description", "")
            impact = unk.get("impact", "")
            blocking = unk.get("blocking", False)
            lines.append(f"- {'🚨' if blocking else '⚠️'} **{desc}**" + (f" (影响: {impact})" if impact else ""))
        lines.append("")
    
    # missing_items
    if blocks.get("missing_items"):
        lines.append("### 缺失项")
        for mi in blocks["missing_items"]:
            desc = mi.get("description", mi.get("item", ""))
            lines.append(f"- ❌ {desc}")
        lines.append("")
    
    # 兜底：未知block类型
    known = {"pages", "operations", "business_rules", "data_entities", "ui_elements",
             "use_cases", "test_point_candidates", "field_specs", "missing_items",
             "blocked_pci_list", "unknowns", "state_transitions"}
    for key, val in blocks.items():
        if key not in known and isinstance(val, list) and val:
            lines.append(f"### {key}")
            for item in val:
                if isinstance(item, dict):
                    parts = [f"{k}: {v}" for k, v in item.items() if v and k not in ('id', 'source')]
                    lines.append(f"- {parts[0] if parts else str(item)}")
                elif isinstance(item, str) and item:
                    lines.append(f"- {item}")
            lines.append("")
    
    return "\n".join(lines)


def format_issues(issues: list) -> str:
    """格式化问题清单"""
    if not issues:
        return "✅ 无阻塞问题"
    
    lines = []
    severity_map = {"high": "🔴 高", "medium": "🟡 中", "low": "🟢 低"}
    
    for idx, issue in enumerate(issues, 1):
        severity = severity_map.get(issue.get("severity", "medium"), "🟡 中")
        location = issue.get("location", "未知位置")
        problem = issue.get("problem", "")
        suggestion = issue.get("suggestion", "")
        
        lines.append(f"### 问题 {idx}: {location}")
        lines.append(f"**严重程度**: {severity}")
        lines.append(f"**问题描述**: {problem}")
        if suggestion:
            lines.append(f"**建议**: {suggestion}")
        lines.append("")
    
    return "\n".join(lines)


def format_feature_tree(feature_tree) -> str:
    """格式化功能点拆解树
    Bugfix V4.6.9: feature_tree可能是list(P1 schema定义)也可能是dict,统一处理
    """
    if not feature_tree:
        return "⚠️ 功能点拆解数据为空"

    # V4.6.9: 兼容list(dict)和dict.modules两种结构
    if isinstance(feature_tree, list):
        modules = feature_tree
    elif isinstance(feature_tree, dict):
        modules = feature_tree.get("modules", [])
    else:
        return "⚠️ 功能点拆解数据格式异常"

    if not modules:
        return "⚠️ 功能点拆解数据为空"

    lines = []
    
    # 统计
    total_modules = len(modules)
    total_features = sum(len(m.get("children", [])) for m in modules)
    total_scenarios = sum(
        len(f.get("children", []))
        for m in modules
        for f in m.get("children", [])
    )
    
    lines.append(f"**统计**: {total_modules}个模块 / {total_features}个功能点 / {total_scenarios}个场景")
    lines.append("")
    
    # 遍历模块
    for module in modules:
        module_name = module.get("name", "未命名模块")
        module_id = module.get("id", "")
        lines.append(f"## {module_name}")
        lines.append(f"*模块ID*: `{module_id}`")
        lines.append("")
        
        # 遍历功能点
        for feature in module.get("children", []):
            feature_name = feature.get("name", "未命名功能点")
            feature_id = feature.get("id", "")
            source_op = feature.get("source_operation", "")
            
            lines.append(f"### {feature_name}")
            lines.append(f"*功能ID*: `{feature_id}`")
            if source_op:
                lines.append(f"*来源操作*: {source_op}")
            lines.append("")
            
            # 遍历场景
            scenarios = feature.get("children", [])
            if scenarios:
                lines.append("**测试场景**:")
                for scenario in scenarios:
                    scenario_name = scenario.get("name", "未命名场景")
                    scenario_type = scenario.get("scenario_type", "")
                    scenario_id = scenario.get("id", "")
                    
                    type_icon = {
                        "positive": "✅",
                        "negative": "❌",
                        "boundary": "⚠️",
                        "exception": "🚨"
                    }.get(scenario_type, "📋")
                    
                    lines.append(f"- {type_icon} {scenario_name} (`{scenario_id}`)")
                lines.append("")
    
    return "\n".join(lines)


def build_markdown(p0_data: dict, p1_data: dict, task_id: str = "") -> str:
    """构建完整的Markdown文档"""
    lines = []
    
    # 标题
    lines.append("# 需求理解与功能点拆解报告")
    lines.append("")
    if task_id:
        lines.append(f"**任务ID**: {task_id}")
    lines.append(f"**生成时间**: {p0_data.get('created_at', 'N/A')}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # P0: 需求理解
    lines.append("# 第一部分：需求结构化 (P0)")
    lines.append("")
    
    objective = p0_data.get("objective", "")
    if objective:
        lines.append("## 需求目标")
        lines.append(objective)
        lines.append("")
    
    quality_score = p0_data.get("quality_score", 0)
    quality_check = p0_data.get("quality_check", {})
    status = quality_check.get("status", "UNKNOWN")
    
    lines.append("## 质量评分")
    lines.append(f"**评分**: {quality_score:.2f}")
    lines.append(f"**状态**: {status}")
    lines.append("")
    
    # 需求结构化内容
    # Bugfix V4.6.9: blocks_markdown可能为空，fallback到从blocks结构数据生成
    blocks_markdown = p0_data.get("blocks_markdown", "")
    blocks = p0_data.get("blocks", {})
    if not blocks_markdown and blocks:
        blocks_markdown = _blocks_to_markdown(blocks)
    if blocks_markdown:
        lines.append("## 需求结构化")
        lines.append(blocks_markdown)
        lines.append("")
    
    # 问题清单
    issues = p0_data.get("issues", [])
    lines.append("## 问题清单")
    lines.append(format_issues(issues))
    lines.append("")
    
    lines.append("---")
    lines.append("")
    
    # P1: 功能点拆解
    lines.append("# 第二部分：功能点拆解 (P1)")
    lines.append("")
    
    feature_tree = p1_data.get("feature_tree", {})
    lines.append(format_feature_tree(feature_tree))
    lines.append("")
    
    lines.append("---")
    lines.append("")
    lines.append("*本报告由 qa-req2testcase-generator 自动生成*")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="P0/P1 导出为 Markdown")
    parser.add_argument("--data-dir", required=True, help="数据目录路径")
    parser.add_argument("--output", required=True, help="输出 Markdown 文件路径")
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    if not data_dir.exists():
        print(f"错误: 数据目录不存在 → {data_dir}", file=sys.stderr)
        sys.exit(1)

    # 加载P0和P1的JSON
    p0_path = data_dir / "p0_output.json"
    p1_path = data_dir / "p1_output.json"
    
    p0_data = load_json(p0_path)
    p1_data = load_json(p1_path)
    
    if not p0_data and not p1_data:
        print("错误: P0 和 P1 数据均不存在或解析失败", file=sys.stderr)
        sys.exit(1)
    
    # 获取task_id
    task_id = ""
    task_meta_path = data_dir / "task_meta.json"
    if task_meta_path.exists():
        task_meta = load_json(task_meta_path)
        task_id = task_meta.get("task_id", "")
    
    # 生成Markdown
    md_content = build_markdown(p0_data, p1_data, task_id)
    
    # 写入文件
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(str(output_path), "w", encoding="utf-8") as f:
            f.write(md_content)
    except Exception as e:
        print(f"错误: Markdown 写入失败 → {e}", file=sys.stderr)
        sys.exit(4)

    print(f"✅ 已生成需求理解与功能点拆解报告 → {output_path}")


if __name__ == "__main__":
    main()
