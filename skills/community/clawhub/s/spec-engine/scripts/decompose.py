#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
decompose.py - 智能任务拆解脚本

输入一个项目 spec 或简短目标描述，自动拆解为可执行的任务清单。

用法:
    python decompose.py -i input_spec.md [-o tasks.md] [--json] [--format table|list]

示例:
    python decompose.py -i project_spec.md
    python decompose.py -i spec.md -o output.md --json
    python decompose.py -i spec.md --format list
"""

import argparse
import io
import json
import os
import re
import sys
from typing import Optional

# 修复 Windows 控制台编码问题
if sys.platform == "win32":
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
    except (AttributeError, io.UnsupportedOperation):
        pass  # 已经被包装过或不可用


# ============================================================
# 配置常量
# ============================================================

# 复杂度关键词 → 工时映射
COMPLEXITY_KEYWORDS = {
    # 复杂任务关键词（1d = 8h）
    "complex": [
        "认证", "授权", "安全", "加密", "实时", "并发", "分布式",
        "微服务", "机器学习", "深度学习", "AI", "算法优化",
        "性能优化", "高可用", "负载均衡", "集群", "同步",
        "事务", "锁", "缓存策略", "消息队列", "WebSocket",
        "OAuth", "SSO", "权限", "审计", "日志系统",
        "监控", "告警", "CI/CD", "部署", "容器化",
    ],
    # 中等任务关键词（4h）
    "medium": [
        "接口", "API", "数据库", "表", "查询", "搜索",
        "导出", "导入", "文件上传", "文件下载", "报表",
        "图表", "统计", "分页", "排序", "过滤",
        "校验", "验证", "解析", "转换", "格式化",
        "通知", "邮件", "短信", "推送", "集成",
        "第三方", "Webhook", "回调", "定时任务",
    ],
}

# 负责人建议关键词 → 角色映射
ROLE_KEYWORDS = {
    "CMO": [
        "前端", "UI", "UX", "界面", "页面", "样式", "CSS",
        "组件", "交互", "响应式", "移动端", "小程序",
        "可视化", "图表", "动画", "设计", "用户体验",
    ],
    "CTO": [
        "后端", "API", "数据库", "服务器", "接口", "架构",
        "部署", "运维", "DevOps", "CI/CD", "性能", "安全",
        "加密", "认证", "缓存", "消息队列", "微服务",
        "SDK", "框架", "中间件", "网关", "负载",
        "数据", "算法", "计算", "处理", "同步",
    ],
    "CPO": [
        "文档", "说明", "教程", "帮助", "用户手册",
        "需求", "原型", "流程图", "UML", "设计文档",
        "产品", "功能", "规划", "路线图", "PRD",
    ],
    "CFO": [
        "财务", "支付", "账单", "发票", "结算",
        "成本", "预算", "对账", "退款", "充值",
        "订单", "交易", "金额", "价格", "费用",
    ],
}

# 依赖关系关键词
DEPENDENCY_KEYWORDS = ["基于", "需要先", "在.*之后", "依赖", "前提", "前置", "完成.*后"]

# 功能需求提取模式
FEATURE_PATTERNS = [
    # "- 功能X" / "- **功能X**"
    re.compile(r"^[\s]*[-*]\s*\*?\*?(.+?)[\s:：]*(.*)$", re.MULTILINE),
    # "功能：XXX" / "功能: XXX"
    re.compile(r"^[\s]*(功能|特性|模块|支持|实现|提供|包含|需要|要求)[\s:：]+(.+)$", re.MULTILINE),
    # "## 功能X" / "### 功能X" (标题形式)
    re.compile(r"^#{2,4}\s+(.+)$", re.MULTILINE),
]


# ============================================================
# 核心函数
# ============================================================

def read_input(file_path: str) -> str:
    """
    读取输入文件，支持 UTF-8 编码。

    Args:
        file_path: 输入文件路径

    Returns:
        文件内容字符串

    Raises:
        FileNotFoundError: 文件不存在
        IOError: 读取失败
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"输入文件不存在: {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        # 尝试其他编码
        try:
            with open(file_path, "r", encoding="gbk") as f:
                return f.read()
        except Exception as e:
            raise IOError(f"无法读取文件 {file_path}: {e}")
    except Exception as e:
        raise IOError(f"读取文件失败 {file_path}: {e}")


def extract_project_name(content: str) -> str:
    """
    从内容中提取项目名称。

    优先从第一个一级标题提取，否则使用默认名称。

    Args:
        content: 输入内容

    Returns:
        项目名称
    """
    # 尝试从 # 标题提取
    match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    if match:
        name = match.group(1).strip()
        # 去除可能的前缀
        name = re.sub(r"^(项目|产品|系统|平台)[\s:：]+", "", name)
        return name

    # 尝试从 "项目名称" 或 "项目名" 提取
    match = re.search(r"(?:项目名称?|产品名称?|系统名称?)[\s:：]+(.+)$", content, re.MULTILINE)
    if match:
        return match.group(1).strip()

    return "未命名项目"


def extract_features(content: str) -> list[dict]:
    """
    从内容中提取功能需求。

    使用多种模式匹配功能描述，去重并整理。

    Args:
        content: 输入内容

    Returns:
        功能列表，每项包含 name 和 description
    """
    features = []
    seen = set()

    # 按行处理
    lines = content.split("\n")
    for line in lines:
        line = line.strip()
        if not line or line.startswith("```") or line.startswith("---"):
            continue

        # 跳过纯标题行（一级标题通常是项目名）
        if re.match(r"^#\s+", line):
            continue

        # 匹配列表项 "- 功能X" / "* 功能X"
        match = re.match(r"^[-*]\s+(.+)$", line)
        if match:
            text = match.group(1).strip()
            # 去除 markdown 加粗
            text = re.sub(r"\*{1,2}([^*]+)\*{1,2}", r"\1", text)
            # 去除 checkbox
            text = re.sub(r"^\[[ xX]\]\s*", "", text)

            if len(text) < 2 or text in seen:
                continue

            # 分离名称和描述
            name, desc = _split_name_desc(text)
            if name and name not in seen:
                seen.add(name)
                features.append({"name": name, "description": desc})
            continue

        # 匹配 "功能：XXX" 等模式
        match = re.match(r"^(?:功能|特性|模块|支持|实现|提供|包含|需要|要求)[\s:：]+(.+)$", line)
        if match:
            text = match.group(1).strip()
            name, desc = _split_name_desc(text)
            if name and name not in seen:
                seen.add(name)
                features.append({"name": name, "description": desc})
            continue

        # 匹配子标题 "## 功能X"
        match = re.match(r"^#{2,4}\s+(.+)$", line)
        if match:
            text = match.group(1).strip()
            if text not in seen and len(text) >= 2:
                seen.add(text)
                features.append({"name": text, "description": ""})

    return features


def _split_name_desc(text: str) -> tuple[str, str]:
    """
    将文本分离为名称和描述。

    支持冒号、破折号等分隔符。

    Args:
        text: 原始文本

    Returns:
        (名称, 描述) 元组
    """
    # 尝试用冒号分隔
    for sep in [":", "：", " - ", " — ", " – "]:
        if sep in text:
            parts = text.split(sep, 1)
            name = parts[0].strip()
            desc = parts[1].strip() if len(parts) > 1 else ""
            # 如果名称太长，截取前30字
            if len(name) > 30:
                name = name[:30]
            return name, desc

    # 没有分隔符，整行作为名称
    name = text[:30] if len(text) > 30 else text
    return name, ""


def estimate_complexity(name: str, description: str) -> str:
    """
    根据关键词判断任务复杂度。

    Args:
        name: 任务名称
        description: 任务描述

    Returns:
        复杂度等级: "复杂"/"中等"/"简单"
    """
    text = (name + " " + description).lower()

    # 检查复杂关键词
    for keyword in COMPLEXITY_KEYWORDS["complex"]:
        if keyword.lower() in text:
            return "复杂"

    # 检查中等关键词
    for keyword in COMPLEXITY_KEYWORDS["medium"]:
        if keyword.lower() in text:
            return "中等"

    return "简单"


def complexity_to_hours(complexity: str) -> str:
    """
    将复杂度转换为工时字符串。

    Args:
        complexity: 复杂度等级

    Returns:
        工时字符串，如 "2h" 或 "1d"
    """
    mapping = {
        "简单": "2h",
        "中等": "4h",
        "复杂": "1d",
    }
    return mapping.get(complexity, "4h")


def hours_to_numeric(hours_str: str) -> float:
    """
    将工时字符串转换为数值（小时）。

    Args:
        hours_str: 工时字符串，如 "2h" 或 "1d"

    Returns:
        小时数
    """
    if hours_str.endswith("d"):
        return float(hours_str[:-1]) * 8
    elif hours_str.endswith("h"):
        return float(hours_str[:-1])
    return 4.0


def numeric_to_hours_str(total_hours: float) -> str:
    """
    将总工时数值转换为可读字符串。

    Args:
        total_hours: 总小时数

    Returns:
        可读的工时字符串，如 "2d 4h"
    """
    days = int(total_hours // 8)
    hours = int(total_hours % 8)
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if not parts:
        parts.append("0h")
    return " ".join(parts)


def suggest_role(name: str, description: str) -> str:
    """
    根据任务类型建议负责人。

    Args:
        name: 任务名称
        description: 任务描述

    Returns:
        建议负责人角色
    """
    text = (name + " " + description).lower()

    # 统计各角色匹配分数
    scores = {}
    for role, keywords in ROLE_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw.lower() in text)
        if score > 0:
            scores[role] = score

    if scores:
        # 返回得分最高的角色
        return max(scores, key=scores.get)

    # 默认 CTO
    return "CTO"


def detect_dependencies(features: list[dict]) -> dict[int, list[str]]:
    """
    检测任务之间的依赖关系。

    基于关键词匹配：如果任务描述中提到另一个任务的名称，
    则认为存在依赖关系。

    Args:
        features: 功能列表

    Returns:
        依赖映射 {任务索引: [依赖的任务名称列表]}
    """
    dependencies = {}

    for i, feature in enumerate(features):
        text = (feature["name"] + " " + feature["description"]).lower()
        deps = []

        # 检查显式依赖关键词
        for keyword_pattern in DEPENDENCY_KEYWORDS:
            if re.search(keyword_pattern, text):
                # 查找可能依赖的其他任务
                for j, other in enumerate(features):
                    if j != i:
                        other_name = other["name"].lower()
                        if other_name in text:
                            deps.append(other["name"])

        # 检查隐式依赖（基于任务类型）
        # 数据库/模型 → API → 前端 的自然依赖
        feature_lower = feature["name"].lower()
        if any(kw in feature_lower for kw in ["前端", "页面", "ui", "界面", "展示"]):
            for j, other in enumerate(features):
                other_lower = other["name"].lower()
                if any(kw in other_lower for kw in ["api", "接口", "后端", "服务"]):
                    if other["name"] not in deps:
                        deps.append(other["name"])

        if any(kw in feature_lower for kw in ["api", "接口", "服务", "后端"]):
            for j, other in enumerate(features):
                other_lower = other["name"].lower()
                if any(kw in other_lower for kw in ["数据库", "模型", "表", "存储"]):
                    if other["name"] not in deps:
                        deps.append(other["name"])

        if deps:
            dependencies[i] = deps

    return dependencies


def find_parallel_tasks(
    features: list[dict], dependencies: dict[int, list[str]]
) -> list[tuple[int, int]]:
    """
    查找可以并行执行的任务对。

    两个任务如果没有直接或间接依赖关系，则可以并行。

    Args:
        features: 功能列表
        dependencies: 依赖映射

    Returns:
        可并行的任务对列表 [(任务A索引, 任务B索引)]
    """
    parallel = []
    n = len(features)

    # 构建任务名称到索引的映射
    name_to_idx = {f["name"]: i for i, f in enumerate(features)}

    for i in range(n):
        for j in range(i + 1, n):
            # 检查是否有直接依赖
            i_deps = dependencies.get(i, [])
            j_deps = dependencies.get(j, [])

            i_dep_indices = {name_to_idx[d] for d in i_deps if d in name_to_idx}
            j_dep_indices = {name_to_idx[d] for d in j_deps if d in name_to_idx}

            if j not in i_dep_indices and i not in j_dep_indices:
                parallel.append((i, j))

    return parallel


def compute_critical_path(
    features: list[dict], dependencies: dict[int, list[str]]
) -> list[int]:
    """
    计算关键路径（最长依赖链）。

    Args:
        features: 功能列表
        dependencies: 依赖映射

    Returns:
        关键路径上的任务索引列表
    """
    name_to_idx = {f["name"]: i for i, f in enumerate(features)}
    n = len(features)

    # 构建邻接表
    graph = {i: [] for i in range(n)}
    for i, deps in dependencies.items():
        for dep_name in deps:
            if dep_name in name_to_idx:
                dep_idx = name_to_idx[dep_name]
                graph[dep_idx].append(i)

    # DFS 找最长路径
    longest_path = []
    memo = {}

    def dfs(node, path):
        if node in memo:
            return memo[node]

        current_path = [node]
        max_sub_path = []

        for next_node in graph[node]:
            sub_path = dfs(next_node, path + [node])
            if len(sub_path) > len(max_sub_path):
                max_sub_path = sub_path

        result = current_path + max_sub_path
        memo[node] = result
        return result

    # 从每个没有依赖的任务开始搜索
    for i in range(n):
        if not any(
            i in {name_to_idx.get(d, -1) for d in deps}
            for deps in dependencies.values()
        ):
            path = dfs(i, [])
            if len(path) > len(longest_path):
                longest_path = path

    return longest_path


def generate_tasks(
    features: list[dict],
) -> list[dict]:
    """
    为每个功能生成完整任务信息。

    Args:
        features: 功能列表

    Returns:
        任务列表，包含完整信息
    """
    tasks = []

    # 检测依赖
    dependencies = detect_dependencies(features)
    name_to_idx = {f["name"]: i for i, f in enumerate(features)}

    for i, feature in enumerate(features):
        complexity = estimate_complexity(feature["name"], feature["description"])
        hours = complexity_to_hours(complexity)
        role = suggest_role(feature["name"], feature["description"])

        # 获取依赖
        deps = dependencies.get(i, [])
        dep_nums = []
        for dep_name in deps:
            if dep_name in name_to_idx:
                dep_nums.append(f"#{name_to_idx[dep_name] + 1}")
        dep_str = ", ".join(dep_nums) if dep_nums else "无"

        # 生成描述
        desc = feature["description"]
        if not desc:
            desc = f"实现{feature['name']}相关功能"

        tasks.append({
            "index": i + 1,
            "name": feature["name"],
            "description": desc,
            "complexity": complexity,
            "hours": hours,
            "hours_numeric": hours_to_numeric(hours),
            "dependencies": dep_str,
            "dependency_names": deps,
            "role": role,
        })

    return tasks


# ============================================================
# 输出格式化
# ============================================================

def format_markdown_table(tasks: list[dict], project_name: str) -> str:
    """
    格式化为 Markdown 表格。

    Args:
        tasks: 任务列表
        project_name: 项目名称

    Returns:
        Markdown 格式字符串
    """
    lines = []
    lines.append(f"# 任务拆解：{project_name}")
    lines.append("")
    lines.append("| # | 任务 | 描述 | 预估工时 | 依赖 | 建议负责人 |")
    lines.append("|---|------|------|---------|------|-----------|")

    total_hours = 0
    for task in tasks:
        lines.append(
            f"| {task['index']} | {task['name']} | {task['description']} "
            f"| {task['hours']} | {task['dependencies']} | {task['role']} |"
        )
        total_hours += task["hours_numeric"]

    # 工时汇总
    lines.append("")
    lines.append("## 工时汇总")
    lines.append(f"- 总工时：{numeric_to_hours_str(total_hours)}")

    # 关键路径
    critical_path = compute_critical_path(tasks, {i: t["dependency_names"] for i, t in enumerate(tasks)})
    if critical_path and len(critical_path) > 1:
        path_str = " → ".join(f"#{i + 1}" for i in critical_path)
        lines.append(f"- 关键路径：{path_str}")

    # 可并行任务
    dependencies = {i: t["dependency_names"] for i, t in enumerate(tasks)}
    parallel_pairs = find_parallel_tasks(tasks, dependencies)
    if parallel_pairs:
        # 只显示前3对
        shown = parallel_pairs[:3]
        parallel_strs = [f"#{a + 1} 与 #{b + 1} 可并行" for a, b in shown]
        lines.append(f"- 可并行：{'; '.join(parallel_strs)}")

    return "\n".join(lines)


def format_markdown_list(tasks: list[dict], project_name: str) -> str:
    """
    格式化为 Markdown 列表。

    Args:
        tasks: 任务列表
        project_name: 项目名称

    Returns:
        Markdown 格式字符串
    """
    lines = []
    lines.append(f"# 任务拆解：{project_name}")
    lines.append("")

    total_hours = 0
    for task in tasks:
        lines.append(f"## {task['index']}. {task['name']}")
        lines.append(f"- **描述**: {task['description']}")
        lines.append(f"- **预估工时**: {task['hours']} ({task['complexity']})")
        lines.append(f"- **依赖**: {task['dependencies']}")
        lines.append(f"- **建议负责人**: {task['role']}")
        lines.append("")
        total_hours += task["hours_numeric"]

    # 工时汇总
    lines.append("## 工时汇总")
    lines.append(f"- 总工时：{numeric_to_hours_str(total_hours)}")

    critical_path = compute_critical_path(tasks, {i: t["dependency_names"] for i, t in enumerate(tasks)})
    if critical_path and len(critical_path) > 1:
        path_str = " → ".join(f"#{i + 1}" for i in critical_path)
        lines.append(f"- 关键路径：{path_str}")

    return "\n".join(lines)


def format_json(tasks: list[dict], project_name: str) -> str:
    """
    格式化为 JSON。

    Args:
        tasks: 任务列表
        project_name: 项目名称

    Returns:
        JSON 格式字符串
    """
    total_hours = sum(t["hours_numeric"] for t in tasks)
    dependencies = {i: t["dependency_names"] for i, t in enumerate(tasks)}
    critical_path = compute_critical_path(tasks, dependencies)

    output = {
        "project": project_name,
        "tasks": [
            {
                "index": t["index"],
                "name": t["name"],
                "description": t["description"],
                "complexity": t["complexity"],
                "hours": t["hours"],
                "hours_numeric": t["hours_numeric"],
                "dependencies": t["dependencies"],
                "role": t["role"],
            }
            for t in tasks
        ],
        "summary": {
            "total_hours": total_hours,
            "total_hours_display": numeric_to_hours_str(total_hours),
            "critical_path": [f"#{i + 1}" for i in critical_path] if critical_path else [],
            "task_count": len(tasks),
        },
    }

    return json.dumps(output, ensure_ascii=False, indent=2)


# ============================================================
# 主函数
# ============================================================

def main():
    """
    主入口函数。

    解析命令行参数，读取输入，生成任务清单，输出结果。
    """
    parser = argparse.ArgumentParser(
        description="智能任务拆解工具 - 将项目 spec 拆解为可执行任务清单",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python decompose.py -i project_spec.md
  python decompose.py -i spec.md -o tasks.md --json
  python decompose.py -i spec.md --format list
        """,
    )

    parser.add_argument(
        "-i", "--input",
        required=True,
        help="输入文件路径（项目 spec 或简短描述）",
    )

    parser.add_argument(
        "-o", "--output",
        default="tasks.md",
        help="输出文件路径（默认：tasks.md）",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="输出 JSON 格式",
    )

    parser.add_argument(
        "--format",
        choices=["table", "list"],
        default="table",
        help="输出格式（默认：table）",
    )

    args = parser.parse_args()

    try:
        # 读取输入
        content = read_input(args.input)
        print(f"✓ 已读取输入文件: {args.input}")

        # 提取项目名称
        project_name = extract_project_name(content)
        print(f"✓ 项目名称: {project_name}")

        # 提取功能需求
        features = extract_features(content)
        if not features:
            print("⚠ 未检测到功能需求，请检查输入文件格式")
            print("  支持格式: '- 功能X'、'功能：XXX'、'## 功能X'")
            sys.exit(1)
        print(f"✓ 检测到 {len(features)} 个功能需求")

        # 生成任务
        tasks = generate_tasks(features)
        print(f"✓ 已生成 {len(tasks)} 个任务")

        # 格式化输出
        if args.json:
            output = format_json(tasks, project_name)
        elif args.format == "list":
            output = format_markdown_list(tasks, project_name)
        else:
            output = format_markdown_table(tasks, project_name)

        # 写入文件
        output_dir = os.path.dirname(args.output)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)

        print(f"✓ 任务清单已保存到: {args.output}")

        # 同时输出到控制台
        print("\n" + "=" * 50)
        print(output)

    except FileNotFoundError as e:
        print(f"✗ 错误: {e}", file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        print(f"✗ IO 错误: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"✗ 未知错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
