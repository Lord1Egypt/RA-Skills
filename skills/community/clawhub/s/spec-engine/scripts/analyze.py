#!/usr/bin/env python3
"""
spec-engine analyze v2.0 — 历史 spec 分析工具。

用法:
    python analyze.py [--dir <目录>] [--output <报告文件>] [--json]

功能:
    - 扫描指定目录下的所有 .md 文件
    - 识别 spec 文件（通过检测 "# 项目名称" 等特征）
    - 分析统计：总数量、技术栈分布、时间规划、常见风险类型
    - 输出分析报告（markdown 格式）

v2.0 新增脚本。
"""

import argparse
import json
import os
import re
import sys
from collections import Counter


# spec 文件识别特征
SPEC_INDICATORS = [
    r"^#\s+项目名称",
    r"^#\s+.+",
    r"##\s*\d*[.、]?\s*目标",
    r"##\s*\d*[.、]?\s*技术方案",
    r"##\s*\d*[.、]?\s*验收标准",
]

# 至少匹配这些特征才算 spec 文件
MIN_SPEC_MATCHES = 2

# 技术栈关键词
TECH_KEYWORDS = {
    "Python": ["python", "django", "flask", "fastapi", "pytorch", "pandas"],
    "JavaScript/TypeScript": ["javascript", "typescript", "js", "ts", "node", "react", "vue", "next"],
    "Go": ["golang", "go ", "gin"],
    "Java": ["java", "spring", "springboot", "maven"],
    "Rust": ["rust", "cargo", "actix", "tokio"],
    "C/C++": ["c++", "cpp", "cmake"],
    "Ruby": ["ruby", "rails"],
    "PHP": ["php", "laravel"],
    "数据库": ["mysql", "postgres", "mongodb", "sqlite", "redis"],
    "容器/云": ["docker", "kubernetes", "k8s", "aws", "gcp"],
    "前端": ["react", "vue", "angular", "svelte", "html", "css"],
}

# 风险关键词分类
RISK_CATEGORIES = {
    "网络/接口风险": ["api", "http", "第三方", "外部接口", "网络"],
    "数据风险": ["数据库", "存储", "备份", "迁移"],
    "安全风险": ["认证", "登录", "密码", "token", "加密", "安全"],
    "性能风险": ["并发", "性能", "负载", "缓存", "限流"],
    "架构风险": ["微服务", "分布式", "docker", "k8s"],
    "财务风险": ["支付", "交易", "金额"],
}

# ANSI 颜色
GREEN = "\033[32m"
CYAN = "\033[36m"
RESET = "\033[0m"


def read_file(filepath):
    """安全读取文件。"""
    try:
        with open(filepath, "r", encoding="utf-8-sig") as f:
            return f.read()
    except Exception:
        return ""


def is_spec_file(text):
    """检测文件是否是 spec 文件。"""
    match_count = 0
    for pattern in SPEC_INDICATORS:
        if re.search(pattern, text, re.MULTILINE | re.IGNORECASE):
            match_count += 1
    return match_count >= MIN_SPEC_MATCHES


def extract_project_name(text):
    """提取项目名称。"""
    match = re.match(r"^#\s+项目名称[：:]\s*(.+)", text, re.MULTILINE)
    if match:
        return match.group(1).strip()
    match = re.match(r"^#\s+(.+)", text, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return "未知项目"


def detect_tech_stack(text):
    """检测技术栈。"""
    found = set()
    text_lower = text.lower()
    for category, keywords in TECH_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in text_lower:
                found.add(category)
                break
    return found


def extract_timeline_days(text):
    """提取时间规划天数（估算）。"""
    # 匹配 "N天" 或 "N 周" 格式
    day_matches = re.findall(r"(\d+)\s*天", text)
    week_matches = re.findall(r"(\d+)\s*周", text)

    total_days = 0
    if day_matches:
        total_days += max(int(d) for d in day_matches)
    if week_matches:
        total_days += max(int(w) for w in week_matches) * 7

    # 从阶段数估算
    phase_count = len(re.findall(r"第\d+[天阶段步]", text))
    if phase_count > 0 and total_days == 0:
        total_days = phase_count

    return total_days


def detect_risks(text):
    """检测风险类型。"""
    found = set()
    text_lower = text.lower()
    for category, keywords in RISK_CATEGORIES.items():
        for kw in keywords:
            if kw.lower() in text_lower:
                found.add(category)
                break
    return found


def scan_directory(dir_path):
    """扫描目录，返回 spec 文件列表和分析数据。"""
    if not os.path.isdir(dir_path):
        print(f"[ERROR] 目录不存在: {dir_path}", file=sys.stderr)
        sys.exit(1)

    specs = []
    all_files = []

    for root, dirs, files in os.walk(dir_path):
        for fname in files:
            if fname.endswith(".md"):
                fpath = os.path.join(root, fname)
                all_files.append(fpath)
                text = read_file(fpath)
                if is_spec_file(text):
                    specs.append({
                        "path": fpath,
                        "name": extract_project_name(text),
                        "tech_stack": detect_tech_stack(text),
                        "timeline_days": extract_timeline_days(text),
                        "risks": detect_risks(text),
                        "size_kb": os.path.getsize(fpath) / 1024,
                    })

    return specs, len(all_files)


def generate_report(specs, total_files, dir_path):
    """生成分析报告（markdown 格式）。"""
    lines = []
    lines.append(f"# Spec 分析报告")
    lines.append(f"")
    lines.append(f"**扫描目录**: `{dir_path}`")
    lines.append(f"**扫描时间**: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"")

    # 总览
    lines.append(f"## 总览")
    lines.append(f"")
    lines.append(f"- 扫描 .md 文件总数: **{total_files}**")
    lines.append(f"- 识别为 spec 文件: **{len(specs)}**")
    lines.append(f"")

    if not specs:
        lines.append(f"> 未发现 spec 文件。spec 文件需包含 \"# 项目名称\" + \"## 目标/技术方案/验收标准\" 等特征。")
        return "\n".join(lines)

    # 项目列表
    lines.append(f"## 项目列表")
    lines.append(f"")
    lines.append(f"| # | 项目名称 | 技术栈 | 预估天数 | 文件大小 |")
    lines.append(f"|---|---------|--------|---------|---------|")
    for i, spec in enumerate(specs, 1):
        techs = ", ".join(sorted(spec["tech_stack"])) if spec["tech_stack"] else "未识别"
        days = f"{spec['timeline_days']}天" if spec["timeline_days"] > 0 else "未指定"
        size = f"{spec['size_kb']:.1f}KB"
        lines.append(f"| {i} | {spec['name']} | {techs} | {days} | {size} |")
    lines.append(f"")

    # 技术栈分布
    tech_counter = Counter()
    for spec in specs:
        for tech in spec["tech_stack"]:
            tech_counter[tech] += 1

    if tech_counter:
        lines.append(f"## 技术栈分布")
        lines.append(f"")
        for tech, count in tech_counter.most_common():
            bar = "█" * count + "░" * (len(specs) - count)
            pct = count / len(specs) * 100
            lines.append(f"- **{tech}**: {count}/{len(specs)} ({pct:.0f}%) {bar}")
        lines.append(f"")

    # 时间规划统计
    timelines = [s["timeline_days"] for s in specs if s["timeline_days"] > 0]
    if timelines:
        avg_days = sum(timelines) / len(timelines)
        lines.append(f"## 时间规划统计")
        lines.append(f"")
        lines.append(f"- 有时间规划的项目: {len(timelines)}/{len(specs)}")
        lines.append(f"- 平均规划天数: **{avg_days:.1f}天**")
        lines.append(f"- 最短: {min(timelines)}天 / 最长: {max(timelines)}天")
        lines.append(f"")

    # 风险类型分布
    risk_counter = Counter()
    for spec in specs:
        for risk in spec["risks"]:
            risk_counter[risk] += 1

    if risk_counter:
        lines.append(f"## 常见风险类型")
        lines.append(f"")
        for risk, count in risk_counter.most_common():
            bar = "█" * count + "░" * (len(specs) - count)
            pct = count / len(specs) * 100
            lines.append(f"- **{risk}**: {count}/{len(specs)} ({pct:.0f}%) {bar}")
        lines.append(f"")

    # 建议
    lines.append(f"## 分析建议")
    lines.append(f"")

    if len(specs) < 3:
        lines.append(f"- 样本量较少（{len(specs)}个），建议积累更多 spec 后再做趋势分析")

    no_timeline = [s for s in specs if s["timeline_days"] == 0]
    if no_timeline:
        names = ", ".join(s["name"] for s in no_timeline)
        lines.append(f"- 以下项目缺少时间规划: {names}")

    no_tech = [s for s in specs if not s["tech_stack"]]
    if no_tech:
        names = ", ".join(s["name"] for s in no_tech)
        lines.append(f"- 以下项目未识别技术栈: {names}")

    no_risk = [s for s in specs if not s["risks"]]
    if no_risk:
        names = ", ".join(s["name"] for s in no_risk)
        lines.append(f"- 以下项目缺少风险评估: {names}")

    lines.append(f"")
    return "\n".join(lines)


def generate_json_report(specs, total_files, dir_path):
    """生成 JSON 格式分析报告。"""
    tech_counter = Counter()
    risk_counter = Counter()
    timelines = []

    for spec in specs:
        for tech in spec["tech_stack"]:
            tech_counter[tech] += 1
        for risk in spec["risks"]:
            risk_counter[risk] += 1
        if spec["timeline_days"] > 0:
            timelines.append(spec["timeline_days"])

    report = {
        "directory": dir_path,
        "total_md_files": total_files,
        "spec_count": len(specs),
        "specs": [
            {
                "name": s["name"],
                "path": s["path"],
                "tech_stack": sorted(s["tech_stack"]),
                "timeline_days": s["timeline_days"],
                "risks": sorted(s["risks"]),
                "size_kb": round(s["size_kb"], 1),
            }
            for s in specs
        ],
        "tech_distribution": dict(tech_counter.most_common()),
        "risk_distribution": dict(risk_counter.most_common()),
        "timeline_stats": {
            "count": len(timelines),
            "average_days": round(sum(timelines) / len(timelines), 1) if timelines else 0,
            "min_days": min(timelines) if timelines else 0,
            "max_days": max(timelines) if timelines else 0,
        },
    }
    return json.dumps(report, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="spec-engine analyze v2.0 — 历史 spec 分析工具"
    )
    parser.add_argument("--dir", "-d",
                        default=os.path.join(SCRIPT_DIR, "..", "..", "..", "teams", "shared", "specs"),
                        help="扫描目录（默认 teams/shared/specs/）")
    parser.add_argument("--output", "-o", default=None,
                        help="输出报告文件路径（默认打印到终端）")
    parser.add_argument("--json", "-j", action="store_true",
                        help="JSON 格式输出")
    args = parser.parse_args()

    # 解析目录路径
    dir_path = os.path.abspath(args.dir)

    # 扫描
    specs, total_files = scan_directory(dir_path)

    # 生成报告
    if args.json:
        report = generate_json_report(specs, total_files, dir_path)
    else:
        report = generate_report(specs, total_files, dir_path)

    # 输出
    if args.output:
        output_dir = os.path.dirname(args.output)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"[OK] 分析报告已生成: {args.output}")
    else:
        print(report)


# 脚本目录（用于默认路径计算）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    main()
