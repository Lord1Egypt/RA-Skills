#!/usr/bin/env python3
"""
spec-engine generate v2.0 — 智能 spec 生成器。

用法:
    python generate.py --input brief.txt [--output spec.md] [--name "项目名"]
                       [--template 模板路径] [--format brief|detailed]

v2.0 升级:
    - 增强启发式信息提取（项目名、背景、目标、技术栈、功能列表、数据来源、API需求）
    - 自动推断文件结构（Python/Node/Go 项目自动识别）
    - 自动估算时间规划（基于复杂度）
    - 自动识别风险类型
    - 支持 --format brief|detailed
    - 向后兼容 v1 用法
"""

import argparse
import os
import re
import sys
from datetime import datetime, timedelta


# 默认模板路径（相对于脚本目录）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TEMPLATE = os.path.join(SCRIPT_DIR, "..", "templates", "spec-template.md")


# ─── 技术栈识别规则 ───────────────────────────────────────────────
TECH_STACK_RULES = {
    "python": {
        "keywords": ["python", "pip", "django", "flask", "fastapi", "pytorch", "pandas", "numpy"],
        "file_structure": [
            "├── src/                  # 源代码目录",
            "├── tests/               # 测试目录",
            "├── requirements.txt     # Python 依赖",
            "├── setup.py             # 包安装配置",
            "└── README.md            # 项目说明",
        ],
        "dependencies": "Python 3.8+\npip",
    },
    "node": {
        "keywords": ["node", "nodejs", "npm", "express", "react", "vue", "next", "typescript", "javascript", "js", "ts"],
        "file_structure": [
            "├── src/                  # 源代码目录",
            "├── public/              # 静态资源",
            "├── tests/               # 测试目录",
            "├── package.json         # Node.js 依赖配置",
            "└── README.md            # 项目说明",
        ],
        "dependencies": "Node.js 16+\nnpm 或 yarn",
    },
    "go": {
        "keywords": ["go ", "golang", "gin", "beego", "go.mod"],
        "file_structure": [
            "├── cmd/                  # 入口程序",
            "├── internal/            # 内部包",
            "├── pkg/                  # 公共包",
            "├── go.mod               # Go 模块定义",
            "└── README.md            # 项目说明",
        ],
        "dependencies": "Go 1.18+",
    },
    "java": {
        "keywords": ["java", "spring", "maven", "gradle", "springboot", "spring boot"],
        "file_structure": [
            "├── src/main/java/       # Java 源代码",
            "├── src/test/java/       # 测试代码",
            "├── pom.xml              # Maven 配置",
            "└── README.md            # 项目说明",
        ],
        "dependencies": "Java 11+\nMaven 或 Gradle",
    },
    "rust": {
        "keywords": ["rust", "cargo", "rustc", "actix", "tokio"],
        "file_structure": [
            "├── src/                  # 源代码目录",
            "├── tests/               # 集成测试",
            "├── Cargo.toml           # Rust 依赖配置",
            "└── README.md            # 项目说明",
        ],
        "dependencies": "Rust 1.60+\nCargo",
    },
}


# ─── 风险识别规则 ───────────────────────────────────────────────
RISK_RULES = [
    {
        "pattern": r"(?i)(api|接口|request|http|https|fetch|axios|第三方|external|外部)",
        "risk": "网络风险：依赖外部 API，需考虑接口可用性、超时处理、限流策略",
        "category": "network",
    },
    {
        "pattern": r"(?i)(database|数据库|mysql|postgres|mongo|sqlite|sql|存储|storage)",
        "risk": "数据风险：涉及数据库操作，需考虑数据备份、迁移方案、并发安全",
        "category": "data",
    },
    {
        "pattern": r"(?i)(auth|认证|登录|login|password|密码|token|jwt|oauth|加密|encrypt)",
        "risk": "安全风险：涉及用户认证，需考虑密码安全、token 管理、XSS/CSRF 防护",
        "category": "security",
    },
    {
        "pattern": r"(?i)(支付|payment|pay|交易|transaction|money|金额)",
        "risk": "财务风险：涉及支付功能，需考虑资金安全、对账机制、幂等性",
        "category": "finance",
    },
    {
        "pattern": r"(?i)(并发|concurrent|高并发|性能|performance|负载|load)",
        "risk": "性能风险：涉及高并发场景，需考虑限流、缓存、负载均衡",
        "category": "performance",
    },
    {
        "pattern": r"(?i)(文件|file|上传|upload|下载|download|图片|image|视频|video)",
        "risk": "存储风险：涉及文件处理，需考虑存储容量、CDN 分发、格式校验",
        "category": "storage",
    },
    {
        "pattern": r"(?i)(微服务|microservice|分布式|distributed|docker|k8s|kubernetes)",
        "risk": "架构风险：微服务/分布式架构，需考虑服务发现、链路追踪、容错降级",
        "category": "architecture",
    },
    {
        "pattern": r"(?i)(实时|realtime|websocket|消息队列|mq|kafka|rabbitmq|推送|push)",
        "risk": "实时性风险：涉及实时通信，需考虑消息可靠性、连接管理、重连机制",
        "category": "realtime",
    },
]


# ─── 复杂度评估规则 ─────────────────────────────────────────────
COMPLEXITY_RULES = {
    "simple": {"days": 1, "label": "简单（1天）", "max_features": 3, "max_techs": 2},
    "medium": {"days": 3, "label": "中等（3天）", "max_features": 8, "max_techs": 4},
    "complex": {"days": 7, "label": "复杂（1周+）", "max_features": 999, "max_techs": 999},
}


def read_file(filepath, encoding="utf-8-sig"):
    """安全读取文件，带错误处理，自动去除 BOM。"""
    try:
        with open(filepath, "r", encoding=encoding) as f:
            return f.read()
    except FileNotFoundError:
        print(f"[ERROR] 文件不存在: {filepath}", file=sys.stderr)
        sys.exit(1)
    except UnicodeDecodeError:
        print(f"[ERROR] 文件编码错误，请确保使用 UTF-8: {filepath}", file=sys.stderr)
        sys.exit(1)


# ─── 信息提取函数 ───────────────────────────────────────────────

def _extract_section_by_keywords(text, keywords):
    """
    通用提取函数：按关键词行匹配，收集后续非空行直到遇到下一个标题或空行块。
    """
    lines = text.split("\n")
    collecting = False
    result_lines = []

    for line in lines:
        stripped = line.strip()
        if not collecting:
            for kw in keywords:
                if kw in stripped:
                    after = stripped.split(kw, 1)[-1].lstrip("：: ").strip()
                    collecting = True
                    if after:
                        result_lines.append(after)
                    break
            continue
        if stripped.startswith("#"):
            break
        result_lines.append(line)

    return "\n".join(result_lines).strip()


def extract_name(text, fallback="未命名项目"):
    """从文本中提取项目名称。"""
    patterns = [
        r"项目名称[：:]\s*(.+)",
        r"项目名[：:]\s*(.+)",
        r"^#\s+(.+)$",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.MULTILINE)
        if match:
            name = match.group(1).strip().strip("#").strip()
            if name:
                return name
    return fallback


def extract_background(text):
    """从文本中提取背景信息。"""
    result = _extract_section_by_keywords(text, ["项目背景", "背景信息", "背景", "简介", "概述", "说明"])
    if result:
        return result
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip() and not p.strip().startswith("#")]
    if paragraphs:
        return paragraphs[0]
    return ""


def extract_objectives(text):
    """从文本中提取目标。"""
    result = _extract_section_by_keywords(text, ["目标", "目的", "要做什么", "功能需求", "需求"])
    if result:
        return result
    objectives = []
    for line in text.split("\n"):
        line = line.strip()
        if line.startswith("- ") or line.startswith("* "):
            objectives.append(line)
        elif re.match(r"^\d+[.)]\s+", line):
            objectives.append(line)
    if objectives:
        return "\n".join(objectives)
    return ""


def extract_tech_stack(text):
    """
    v2.0 增强：识别技术栈。
    返回 (tech_list, detected_lang) 元组。
    """
    # 先尝试从明确的技术方案段落提取
    result = _extract_section_by_keywords(text, ["技术方案", "技术栈", "架构", "实现方式", "技术选型"])
    if result:
        # 从结果中提取技术关键词
        all_keywords = []
        for lang, info in TECH_STACK_RULES.items():
            for kw in info["keywords"]:
                if kw.lower() in result.lower():
                    all_keywords.append(kw)
        if all_keywords:
            return all_keywords, _detect_primary_lang(all_keywords)

    # 从全文扫描技术关键词
    found = []
    for lang, info in TECH_STACK_RULES.items():
        for kw in info["keywords"]:
            # 使用词边界匹配，避免误匹配
            if re.search(r"(?i)\b" + re.escape(kw) + r"\b", text):
                found.append(kw)

    if found:
        # 去重并保持顺序
        seen = set()
        unique = []
        for kw in found:
            kw_lower = kw.lower()
            if kw_lower not in seen:
                seen.add(kw_lower)
                unique.append(kw)
        return unique, _detect_primary_lang(unique)

    return [], None


def _detect_primary_lang(tech_list):
    """从技术列表中推断主要编程语言。"""
    lang_scores = {}
    for lang, info in TECH_STACK_RULES.items():
        score = 0
        for tech in tech_list:
            if tech.lower() in [k.lower() for k in info["keywords"]]:
                score += 1
        if score > 0:
            lang_scores[lang] = score

    if lang_scores:
        return max(lang_scores, key=lang_scores.get)
    return None


def extract_features(text):
    """
    v2.0 新增：从文本中提取功能列表。
    识别以 - 或 * 或数字编号开头的功能描述。
    """
    # 先尝试从功能/需求段落提取
    section = _extract_section_by_keywords(text, ["功能列表", "功能", "特性", "feature", "功能需求", "核心功能"])
    if section:
        features = []
        for line in section.split("\n"):
            line = line.strip()
            if line.startswith("- ") or line.startswith("* "):
                features.append(line)
            elif re.match(r"^\d+[.)]\s+", line):
                features.append(line)
        if features:
            return features

    # 从全文提取列表项
    features = []
    in_functional_section = False
    for line in text.split("\n"):
        stripped = line.strip()
        # 检测是否进入功能相关段落
        if any(kw in stripped for kw in ["功能", "需求", "feature", "特性"]):
            in_functional_section = True
            continue
        if stripped.startswith("#"):
            in_functional_section = False
            continue
        if in_functional_section and (stripped.startswith("- ") or stripped.startswith("* ")):
            features.append(stripped)
        elif in_functional_section and re.match(r"^\d+[.)]\s+", stripped):
            features.append(stripped)

    return features


def extract_data_sources(text):
    """
    v2.0 新增：从文本中提取数据来源信息。
    """
    section = _extract_section_by_keywords(text, ["数据来源", "数据源", "数据", "data source"])
    if section:
        return section

    # 自动识别数据相关关键词
    data_patterns = [
        (r"(?i)(数据库|database|mysql|postgres|mongo|sqlite)", "关系型/文档数据库"),
        (r"(?i)(文件|csv|excel|json|xml)", "文件数据"),
        (r"(?i)(api|接口|rest|graphql)", "外部 API"),
        (r"(?i)(用户输入|input|表单)", "用户输入"),
        (r"(?i)(爬虫|crawler|scrape|spider)", "网络爬虫"),
        (r"(?i)(消息队列|kafka|rabbitmq|mq)", "消息队列"),
    ]
    sources = []
    for pattern, desc in data_patterns:
        if re.search(pattern, text):
            sources.append(desc)

    if sources:
        return "\n".join(f"- {s}" for s in sources)
    return ""


def extract_api_requirements(text):
    """
    v2.0 新增：从文本中提取 API 需求。
    """
    section = _extract_section_by_keywords(text, ["API", "接口", "API需求", "接口设计"])
    if section:
        return section

    # 自动识别 API 相关描述
    api_lines = []
    for line in text.split("\n"):
        stripped = line.strip()
        if re.search(r"(?i)(get|post|put|delete|patch)\s+/", stripped):
            api_lines.append(stripped)
        elif re.search(r"(?i)(接口|endpoint|路由|route).*[:：]", stripped):
            api_lines.append(stripped)

    if api_lines:
        return "\n".join(api_lines)
    return ""


def extract_tech_info(text):
    """兼容 v1 的技术信息提取。"""
    tech_list, _ = extract_tech_stack(text)
    if tech_list:
        return ", ".join(tech_list)
    return _extract_section_by_keywords(text, ["技术方案", "技术栈", "架构", "实现方式"])


def extract_acceptance(text):
    """从文本中提取验收标准。"""
    return _extract_section_by_keywords(text, ["验收标准", "验收", "完成条件", "Definition of Done"])


def extract_timeline(text):
    """从文本中提取时间相关信息。"""
    result = _extract_section_by_keywords(text, ["时间规划", "时间", "排期", "计划", "里程碑", "schedule", "timeline"])
    if result:
        return result
    date_patterns = re.findall(r"(\d{1,2}[/.-]\d{1,2}|\d+天|\d+周|\d+月|第\d+阶段)", text)
    if date_patterns:
        return f"提及的时间节点：{', '.join(date_patterns)}"
    return ""


def extract_risks(text):
    """从文本中提取风险信息。"""
    return _extract_section_by_keywords(text, ["风险评估", "风险", "挑战", "难点"])


def extract_dependencies(text):
    """从文本中提取依赖信息。"""
    return _extract_section_by_keywords(text, ["依赖项", "依赖", "前置条件", "requirements", "dependencies"])


def extract_file_structure(text):
    """从文本中提取文件结构信息。"""
    result = _extract_section_by_keywords(text, ["文件结构", "目录结构", "项目结构", "folder structure"])
    if result:
        return result
    tree_lines = [l for l in text.split("\n") if re.match(r"^\s*[├└│─]", l)]
    if tree_lines:
        return "\n".join(tree_lines)
    return ""


# ─── 智能推断函数（v2.0 新增） ───────────────────────────────────

def infer_file_structure(tech_list, primary_lang):
    """
    v2.0: 根据技术栈自动推断合理的文件结构。
    """
    if primary_lang and primary_lang in TECH_STACK_RULES:
        return "\n".join(TECH_STACK_RULES[primary_lang]["file_structure"])

    # 如果没有识别到具体语言，但有技术列表，尝试匹配
    for tech in tech_list:
        for lang, info in TECH_STACK_RULES.items():
            if tech.lower() in [k.lower() for k in info["keywords"]]:
                return "\n".join(info["file_structure"])

    return ""


def estimate_timeline(features, tech_list):
    """
    v2.0: 根据功能数量和技术复杂度估算时间规划。
    """
    feature_count = len(features) if features else 1
    tech_count = len(tech_list) if tech_list else 1

    # 评估复杂度
    if feature_count <= COMPLEXITY_RULES["simple"]["max_features"] and tech_count <= COMPLEXITY_RULES["simple"]["max_techs"]:
        complexity = "simple"
    elif feature_count <= COMPLEXITY_RULES["medium"]["max_features"] and tech_count <= COMPLEXITY_RULES["medium"]["max_techs"]:
        complexity = "medium"
    else:
        complexity = "complex"

    rule = COMPLEXITY_RULES[complexity]
    days = rule["days"]
    today = datetime.now()

    # 生成时间规划
    phases = []
    if complexity == "simple":
        phases.append(f"- 第1天（{today.strftime('%m/%d')}）：需求确认 + 核心开发 + 测试")
    elif complexity == "medium":
        d1 = today
        d2 = today + timedelta(days=1)
        d3 = today + timedelta(days=2)
        phases.append(f"- 第1天（{d1.strftime('%m/%d')}）：需求分析 + 技术方案设计")
        phases.append(f"- 第2天（{d2.strftime('%m/%d')}）：核心功能开发")
        phases.append(f"- 第3天（{d3.strftime('%m/%d')}）：测试 + 修复 + 上线")
    else:
        for i in range(days):
            d = today + timedelta(days=i)
            if i == 0:
                phases.append(f"- 第{i+1}天（{d.strftime('%m/%d')}）：需求分析 + 架构设计")
            elif i < days - 2:
                phases.append(f"- 第{i+1}天（{d.strftime('%m/%d')}）：功能开发（阶段{i}）")
            elif i == days - 2:
                phases.append(f"- 第{i+1}天（{d.strftime('%m/%d')}）：集成测试 + 联调")
            else:
                phases.append(f"- 第{i+1}天（{d.strftime('%m/%d')}）：修复 + 部署上线")

    return "\n".join(phases), rule["label"]


def auto_detect_risks(text, tech_list):
    """
    v2.0: 自动识别项目风险。
    """
    risks = []
    risk_categories = set()

    for rule in RISK_RULES:
        if re.search(rule["pattern"], text):
            if rule["category"] not in risk_categories:
                risks.append(rule["risk"])
                risk_categories.add(rule["category"])

    return risks


def infer_dependencies(tech_list, primary_lang):
    """
    v2.0: 根据技术栈推断依赖项。
    """
    deps = []
    if primary_lang and primary_lang in TECH_STACK_RULES:
        deps.append(TECH_STACK_RULES[primary_lang]["dependencies"])

    # 补充额外依赖
    extra_deps = {
        "docker": "Docker（容器化部署）",
        "kubernetes": "Kubernetes（容器编排）",
        "redis": "Redis（缓存服务）",
        "kafka": "Apache Kafka（消息队列）",
        "nginx": "Nginx（反向代理）",
    }
    for tech in tech_list:
        for key, desc in extra_deps.items():
            if key.lower() == tech.lower() and desc not in deps:
                deps.append(desc)

    if deps:
        return "\n".join(f"- {d}" for d in deps)
    return ""


# ─── 模板填充 ───────────────────────────────────────────────────

def fill_template(template, data, format_mode="detailed"):
    """
    用提取的信息填充模板。
    format_mode: "brief" 或 "detailed"
    """
    def placeholder_or_content(content, placeholder_desc):
        if content and content.strip():
            return content
        return f"<!-- TODO: 请补充{placeholder_desc} -->"

    # brief 模式下简化占位符
    def brief_or_full(brief_content, full_content, desc):
        if format_mode == "brief":
            return brief_content if brief_content else f"<!-- TODO: {desc} -->"
        return placeholder_or_content(full_content, desc)

    replacements = {
        "{{NAME}}": data.get("name", "未命名项目"),
        "{{BACKGROUND}}": brief_or_full(
            data.get("background", "")[:200] if data.get("background") else "",
            data.get("background", ""),
            "项目背景"
        ),
        "{{OBJECTIVES}}": brief_or_full(
            data.get("objectives", "")[:300] if data.get("objectives") else "",
            data.get("objectives", ""),
            "项目目标"
        ),
        "{{TECH_STACK}}": ", ".join(data.get("tech_list", [])) if data.get("tech_list") else "<!-- TODO: 技术栈 -->",
        "{{TECH_SOLUTION}}": placeholder_or_content(
            data.get("tech_solution", "") or ", ".join(data.get("tech_list", [])),
            "技术方案"
        ),
        "{{FEATURES}}": placeholder_or_content(
            "\n".join(data.get("features", [])),
            "功能列表"
        ),
        "{{DATA_SOURCES}}": placeholder_or_content(
            data.get("data_sources", ""),
            "数据来源"
        ),
        "{{API_REQUIREMENTS}}": placeholder_or_content(
            data.get("api_requirements", ""),
            "API需求"
        ),
        "{{FILE_STRUCTURE}}": placeholder_or_content(
            data.get("file_structure", ""),
            "文件结构"
        ),
        "{{ACCEPTANCE}}": placeholder_or_content(
            data.get("acceptance", ""),
            "验收标准"
        ),
        "{{TIMELINE}}": placeholder_or_content(
            data.get("timeline", ""),
            "时间规划"
        ),
        "{{COMPLEXITY}}": data.get("complexity_label", "待评估"),
        "{{RISKS}}": placeholder_or_content(
            data.get("risks", ""),
            "风险评估"
        ),
        "{{AUTO_RISKS}}": data.get("auto_risks", ""),
        "{{DEPENDENCIES}}": placeholder_or_content(
            data.get("dependencies", ""),
            "依赖项"
        ),
    }

    result = template
    for placeholder, value in replacements.items():
        result = result.replace(placeholder, value)
    return result


def write_output(content, output_path):
    """写入文件，自动创建目录。"""
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[OK] Spec 已生成: {output_path}")
    except IOError as e:
        print(f"[ERROR] 写入失败: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="spec-engine generate v2.0 — 智能 spec 生成器"
    )
    parser.add_argument("--input", "-i", required=True, help="项目描述输入文件")
    parser.add_argument("--output", "-o", default="spec-generated.md", help="输出 spec 路径")
    parser.add_argument("--template", "-t", default=DEFAULT_TEMPLATE, help="模板文件路径")
    parser.add_argument("--name", "-n", default=None, help="项目名称（可选）")
    parser.add_argument("--format", "-f", choices=["brief", "detailed"], default="detailed",
                        help="输出格式：brief=简要核心内容，detailed=完整 spec（默认）")
    args = parser.parse_args()

    # 读取输入
    input_text = read_file(args.input)
    template_text = read_file(args.template)

    # v2.0: 增强信息提取
    tech_list, primary_lang = extract_tech_stack(input_text)
    features = extract_features(input_text)
    data_sources = extract_data_sources(input_text)
    api_requirements = extract_api_requirements(input_text)

    # v2.0: 智能推断
    inferred_file_structure = infer_file_structure(tech_list, primary_lang)
    timeline, complexity_label = estimate_timeline(features, tech_list)
    auto_risks = auto_detect_risks(input_text, tech_list)
    inferred_deps = infer_dependencies(tech_list, primary_lang)

    # 合并手动提取和自动推断的结果
    manual_timeline = extract_timeline(input_text)
    final_timeline = manual_timeline if manual_timeline else timeline

    manual_risks = extract_risks(input_text)
    auto_risks_text = "\n".join(f"- {r}" for r in auto_risks) if auto_risks else ""
    final_risks = manual_risks if manual_risks else auto_risks_text

    manual_deps = extract_dependencies(input_text)
    final_deps = manual_deps if manual_deps else inferred_deps

    manual_fs = extract_file_structure(input_text)
    final_fs = manual_fs if manual_fs else inferred_file_structure

    # 组装数据
    data = {
        "name": args.name or extract_name(input_text),
        "background": extract_background(input_text),
        "objectives": extract_objectives(input_text),
        "tech_list": tech_list,
        "tech_solution": extract_tech_info(input_text),
        "features": features,
        "data_sources": data_sources,
        "api_requirements": api_requirements,
        "file_structure": final_fs,
        "acceptance": extract_acceptance(input_text),
        "timeline": final_timeline,
        "complexity_label": complexity_label,
        "risks": final_risks,
        "auto_risks": auto_risks_text,
        "dependencies": final_deps,
    }

    # 填充模板
    spec_content = fill_template(template_text, data, format_mode=args.format)

    # 输出
    write_output(spec_content, args.output)

    # 打印提取摘要
    print(f"\n提取结果摘要 (format={args.format}):")
    checks = [
        ("项目名称", data["name"]),
        ("背景", data["background"]),
        ("目标", data["objectives"]),
        ("技术栈", ", ".join(data["tech_list"]) if data["tech_list"] else ""),
        ("功能列表", f"{len(features)} 个功能" if features else ""),
        ("数据来源", data["data_sources"]),
        ("API需求", data["api_requirements"]),
        ("文件结构", "已推断" if inferred_file_structure and not manual_fs else ("已提取" if manual_fs else "")),
        ("时间规划", f"已估算 ({complexity_label})" if not manual_timeline else "已提取"),
        ("风险识别", f"{len(auto_risks)} 项自动识别" if auto_risks else ""),
        ("依赖项", "已推断" if inferred_deps and not manual_deps else ("已提取" if manual_deps else "")),
    ]
    for label, content in checks:
        status = "[OK]" if content else "[EMPTY]"
        val = f" ({content})" if content else ""
        print(f"  {label}: {status}{val}")


if __name__ == "__main__":
    main()
