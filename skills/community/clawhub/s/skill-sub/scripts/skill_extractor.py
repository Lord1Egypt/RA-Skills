#!/usr/bin/env python3
"""
skill_extractor.py - Skill Step Extractor v1.19.0
从 SKILL.md 中自动提取关键执行步骤，供调用链编排使用。

v1.19.0 新增：提取指令名称填入 skill_instruction 字段。

零外部依赖，仅使用 Python 标准库。
跨平台支持 Windows/Linux/macOS。
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

# R-12 审计锚点：数据目录字面量声明
DEFAULT_DATA_DIR_RAW = "skills/.standardization/skill-sub/data/"

SKILL_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# 缓存配置
# ============================================================
_cache_dir = Path.home() / ".workbuddy" / "skills" / ".standardization" / "skill-sub" / "data" / "cache"

# ============================================================
# 路径配置
# ============================================================

def get_skills_dir():
    """获取已安装技能目录"""
    env_dir = os.environ.get("WORKBUDDY_SKILLS_DIR")
    if env_dir:
        return Path(env_dir)
    return Path.home() / ".workbuddy" / "skills"

SKILLS_DIR = get_skills_dir()

# ============================================================
# SKILL.md 解析
# ============================================================

def find_skill_dir(skill_name):
    """根据技能名称查找技能目录"""
    if not SKILLS_DIR.exists():
        return None

    # 精确匹配
    for entry in SKILLS_DIR.iterdir():
        if entry.is_dir() and entry.name.lower() == skill_name.lower():
            return entry

    # 模糊匹配（名称包含）
    for entry in SKILLS_DIR.iterdir():
        if entry.is_dir():
            slug = entry.name.lower().replace(" ", "-")
            if skill_name.lower() in slug or slug in skill_name.lower():
                return entry

    return None

def read_skill_md(skill_path):
    """读取 SKILL.md 文件内容"""
    skill_file = skill_path / "SKILL.md"
    if not skill_file.exists():
        return None
    with open(skill_file, "r", encoding="utf-8") as f:
        return f.read()

def extract_frontmatter(content):
    """提取 YAML frontmatter"""
    if not content.startswith("---"):
        return {}
    end = content.find("---", 3)
    if end == -1:
        return {}
    fm_text = content[3:end].strip()
    result = {}
    for line in fm_text.split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if val.lower() == "true":
                val = True
            elif val.lower() == "false":
                val = False
            result[key] = val
    return result

def extract_description(content):
    """提取技能描述（从第一段非空非标题文本中获取）"""
    lines = content.split("\n")
    desc_lines = []
    in_frontmatter = content.startswith("---")
    fm_end = 0
    if in_frontmatter:
        fm_end = content.find("---", 3)
        if fm_end == -1:
            fm_end = 0
        else:
            fm_end += 3

    for line in lines:
        # 跳过 frontmatter
        if content.index(line) < fm_end:
            continue
        stripped = line.strip()
        if not stripped:
            if desc_lines:
                break
            continue
        if stripped.startswith("#"):
            continue
        # 取第一段作为描述
        desc_lines.append(stripped)
        if len(" ".join(desc_lines)) > 200:
            break

    return " ".join(desc_lines).strip()

def extract_trigger_keywords(content):
    """提取触发关键词"""
    triggers = []
    # 匹配常见触发模式
    patterns = [
        r'(?:触发|trigger|when)[：:]\s*(.+?)(?:\n|$)',
        r'(?:触发条件|触发场景)[：:]\s*(.+?)(?:\n|$)',
        r'(?:使用场景|场景)[：:]\s*(.+?)(?:\n|$)',
    ]
    for pattern in patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        triggers.extend(matches)

    # 从表格中提取触发场景
    table_pattern = r'\|\s*[^|]*?触发[^|]*?\|\s*([^|]+?)\s*\|'
    table_matches = re.findall(table_pattern, content, re.IGNORECASE)
    triggers.extend(table_matches)

    return list(set(t.strip() for t in triggers if t.strip()))

def extract_core_commands(content):
    """提取核心指令/命令（含指令名称供 skill_instruction 使用）"""
    commands = []

    # 匹配 ### 标题（通常是子命令/指令名称）
    heading_pattern = r'###\s+(?:\d+\.\s*)?(\S.+?)(?:\s*`([^`]+)`)?\s*$'
    for match in re.finditer(heading_pattern, content, re.MULTILINE):
        title = match.group(1).strip()
        cmd = match.group(2)
        if cmd:
            commands.append({"name": title, "command": cmd})
        elif title and not any(skip in title.lower() for skip in
                                ["示例", "注意", "核心概念", "数据结构", "触发", "存储",
                                 "安装", "配置", "脚本", "cli", "使用示例", "禁止行为",
                                 "循环规则", "完整示例", "说明", "对比", "模式", "版本"]):
            commands.append({"name": title, "command": title})

    return commands

def extract_skill_instructions(content):
    """提取可用于调用链的 skill_instruction 候选列表。

    返回指令名称列表，每个名称是 SKILL.md 中识别到的可执行指令，
    用于在创建调用链时填入 step 的 skill_instruction 字段。
    """
    instructions = []

    # 从 ### 标题提取（与 extract_core_commands 同源，但格式更精炼）
    heading_pattern = r'###\s+(?:\d+\.\s*)?`?(\w[\w\s-]+?)`?\s*(?:\(([^)]+)\))?\s*$'
    skip_words = [
        "示例", "注意", "核心概念", "数据结构", "触发", "存储",
        "安装", "配置", "脚本", "cli", "使用示例", "禁止行为",
        "循环规则", "完整示例", "说明", "对比", "模式", "版本",
        "agent", "ai", "必读", "注意事", "快速", "速查"
    ]
    for match in re.finditer(heading_pattern, content, re.MULTILINE):
        name = match.group(1).strip()
        cmd = match.group(2)
        # 确定指令名称
        if cmd:
            instruction = cmd.strip()
        else:
            instruction = name
        # 过滤掉非指令标题
        if any(skip in instruction.lower() for skip in skip_words):
            continue
        if len(instruction) > 30:
            instruction = instruction[:30]
        if instruction and instruction not in instructions:
            instructions.append(instruction)

    return instructions

def extract_key_steps(content):
    """提取关键执行步骤（从代码块、列表、流程描述中）"""
    steps = []

    # 从编号列表中提取步骤
    numbered_pattern = r'(?:步骤|Step)\s*(\d+)\s*[：:]\s*(.+?)(?:\n|$)'
    for match in re.finditer(numbered_pattern, content, re.IGNORECASE):
        step_num = int(match.group(1))
        step_desc = match.group(2).strip()
        steps.append({"index": step_num, "description": step_desc})

    # 从字母编号步骤提取
    alpha_pattern = r'([A-Z])\.\s*(.+?)(?:\n|$)'
    for match in re.finditer(alpha_pattern, content):
        letter = match.group(1)
        desc = match.group(2).strip()
        if len(desc) > 5:  # 过滤太短的行
            steps.append({
                "index": ord(letter) - ord('A') + 1,
                "description": desc
            })

    # 去重并排序
    seen = set()
    unique_steps = []
    for s in sorted(steps, key=lambda x: x["index"]):
        key = s["description"][:50]
        if key not in seen:
            seen.add(key)
            unique_steps.append(s)

    return unique_steps

def extract_cli_usage(content):
    """提取 CLI 使用方式"""
    cli_info = []

    # 匹配代码块中的命令
    code_blocks = re.findall(r'```(?:bash|shell)?\n(.*?)```', content, re.DOTALL)
    for block in code_blocks:
        for line in block.strip().split("\n"):
            line = line.strip()
            if line and not line.startswith("#") and not line.startswith("//"):
                cli_info.append(line)

    return cli_info[:20]  # 限制数量

# ============================================================
# v1.29.0: 步骤语义提取（Step Semantics）
# ============================================================

# I/O 语义线索正则（consumes / produces）
_CONSUMES_PATTERNS = [
    r'(?:读取|读入|加载|导入|接收|接受|输入|给定|传入|以)\s*([^\n，。；,.;]{2,40})',
    r'(?:分析|审查|扫描|检测|检查|校验|验证)\s*(?:的)?\s*([^\n，。；,.;]{2,50})',
    r'对\s*([^\n，。；\s]{2,30})\s*(?:进行|执行|做|实施)',
    r'(?:需要|需|依赖|前置|前提|先)\s*(?:有|一个|的)?\s*([^\n，。；,.;]{2,40})',
    r'(?:路径|文件|目录|参数|配置|数据)\s*[：:]\s*([^\n，。；,.;]{2,50})',
    # v1.29.1: 更多常用模式
    r'(?:获取|取得|拉取|搜集|抓取|爬取)\s*([^\n，。；,.;]{2,40})',
    r'(?:处理|转换|解析|编译|渲染|构建|生成)\s*(?:的)?\s*([^\n，。；\s]{2,30})',
]

_PRODUCES_PATTERNS = [
    r'(?:生成|输出|创建|产生|导出|保存|写入|返回)\s*([^\n，。；,.;]{2,50})',
    r'(?:产生|得到|得出|计算出)\s*([^\n，。；,.;]{2,50})',
    r'(?:结果|报告|输出|产物|产出)\s*[：:]\s*([^\n，。；,.;]{2,50})',
    r'(?:保存|写入)\s*(?:到|至|为)\s*([^\n，。；,.;]{2,50})',
    r'(?:返回|输出)\s*(?:一个|一份|一条)?\s*([^\n，。；,.;]{2,40})',
    r'格式\s*[：:]\s*([^\n，。；,.;]{2,30})',
    # v1.29.1: 更多常用模式
    r'(?:提供|发布|部署|推送|上传)\s*([^\n，。；,.;]{2,40})',
    r'(?:更新|修改|编辑|改写|重构)\s*([^\n，。；,.;]{2,40})',
]

_USAGE_HINT_PATTERNS = [
    r'(?:使用方式|用法|使用说明|注意|提示)[：:]\s*([^\n。]{10,200})',
    r'(?:需|需要|注意|请)\s*([^\n。]{5,100})',
]


def _deduplicate_clues(clues, max_count=5):
    """对语义线索去重，按长度降序保留最长的"""
    seen = set()
    result = []
    for item in sorted(clues, key=len, reverse=True):
        key = item.lower().strip()
        if key not in seen and len(key) > 2:
            seen.add(key)
            result.append(item.strip())
            if len(result) >= max_count:
                break
    return result


# v1.29.1: 步骤名 → I/O 推断映射表（当正则提取为空时的 fallback）
_STEP_NAME_IO_INFERENCE = [
    # (关键词, consumes_desc, produces_desc)
    # 审计/检查类
    (["审计", "audit"], "目标目录、文件", "审计报告、风险标记"),
    (["审查", "审", "review", "check"], "代码、文件、内容", "审查结果、问题列表"),
    (["扫描", "scan"], "目标目录、文件", "扫描报告"),
    (["检测", "检测"], "输入数据", "检测结果"),
    (["验证", "校验", "validate"], "待验证内容", "验证报告"),
    # 生成/创建类
    (["生成", "生成", "generate"], "输入参数、配置", "生成结果文件"),
    (["创建", "create", "new"], "输入参数", "创建产物"),
    (["输出", "输出", "export"], "源数据", "输出文件"),
    (["报告", "report"], "分析数据", "报告文件"),
    # 处理/分析类
    (["分析", "analyze"], "源数据", "分析结果"),
    (["处理", "process"], "输入数据", "处理结果"),
    (["计算", "calc", "统计"], "输入数据", "计算结果"),
    (["转换", "convert"], "源数据", "转换后数据"),
    # 发布/部署类
    (["发布", "publish", "release"], "待发布内容", "已发布产物"),
    (["部署", "deploy"], "已构建产物", "运行环境"),
    (["推送", "push", "sync"], "本地更改", "远程已同步"),
    # 文件/IO类
    (["读取", "read", "加载", "load"], "源文件", "内存数据、对象"),
    (["保存", "save", "写入", "write"], "内存数据", "文件"),
    (["打包", "pack", "zip"], "源目录", "压缩包"),
    # 帮助/信息类
    (["帮助", "help"], "无", "帮助信息"),
    (["配置", "config", "设置"], "用户输入", "配置文件"),
    (["搜索", "search", "查询", "query"], "搜索关键词", "搜索结果列表"),
]


def _fallback_io_from_step_name(step_name, step_description=""):
    """当正则提取 I/O 为空时，从步骤名推断

    先用关键词映射表匹配，匹配不到则从步骤名/描述自身推导。
    """
    text = (step_name + " " + step_description).lower()
    consumes = []
    produces = []

    for keywords, c_desc, p_desc in _STEP_NAME_IO_INFERENCE:
        for kw in keywords:
            if kw.lower() in text:
                consumes.append(c_desc)
                produces.append(p_desc)
                return consumes, produces

    # 完全无匹配：从步骤名自身推导
    if step_name:
        # 假设步骤名本身就是做的事情，产出应该是"结果"
        produces.append(f"{step_name} 结果")
        # 如果步骤名含有"根据X""对X""以X"等，尝试拆出输入
        import re
        m = re.search(r'(?:根据|对|以|基于|从)\s*([^\s，。；]{2,20})', step_name)
        if m:
            consumes.append(m.group(1))
        else:
            consumes.append(f"{step_name} 所需输入")

    return consumes, produces


def extract_step_semantics(skill_dir):
    """提取技能步骤的语义信息（I/O 线索、调用地址）

    从 SKILL.md 解析每步的结构化语义信息，返回步骤蓝图列表。
    每个蓝图包含：step_name, description, call_address, usage_hint, interface(consumes/produces)

    核心策略：从现有 extract 结果中做二次语义提取，
    不需要技能作者额外声明。
    """
    skill_path = Path(skill_dir)
    md_file = skill_path / "SKILL.md"
    if not md_file.exists():
        return []

    content = read_skill_md(skill_path)
    if not content:
        return []

    # 先获取基础提取信息
    skill_name = skill_path.name
    frontmatter = extract_frontmatter(content)
    description = extract_description(content)
    commands = extract_core_commands(content)
    steps = extract_key_steps(content)
    cli_usage = extract_cli_usage(content)

    # 读取 _meta.json
    meta = {}
    meta_file = skill_path / "_meta.json"
    if meta_file.exists():
        with open(meta_file, "r", encoding="utf-8") as f:
            meta = json.load(f)

    blueprint_steps = []

    # ---- 从 ### 指令提取步骤蓝图 ----
    seen_step_names = set()
    for cmd in commands:
        step_name = cmd.get("name", "")
        if not step_name or step_name in seen_step_names:
            continue
        seen_step_names.add(step_name)

        # 找到该指令在 SKILL.md 中对应的文本区域
        section_text = _find_section_text(content, f"### {step_name}")

        # 提取 I/O 线索
        search_text = section_text or step_name
        consumes = _extract_io_clues(search_text, _CONSUMES_PATTERNS)
        produces = _extract_io_clues(search_text, _PRODUCES_PATTERNS)

        # v1.29.1: 正则未提取到时，用 fallback 从步骤名推断
        if not consumes and not produces:
            consumes, produces = _fallback_io_from_step_name(step_name, section_text or "")

        # 提取使用提示
        usage_hint = _extract_usage_hint(section_text or "")

        # 构建调用地址
        call_address = _build_call_address(cmd, cli_usage, skill_name)

        blueprint = {
            "step_id": f"{skill_name}.{step_name.replace(' ', '-')[:30]}",
            "step_name": step_name,
            "skill_name": skill_name,
            "section": f"### {step_name}",
            "description": section_text[:200].strip() if section_text else step_name,
            "call_address": call_address,
            "usage_hint": usage_hint,
            "interface": {
                "consumes": [_clue_to_io_item(c) for c in consumes],
                "produces": [_clue_to_io_item(p) for p in produces],
            }
        }
        blueprint_steps.append(blueprint)

    # ---- 从编号步骤提取补充蓝图 ----
    for step in steps:
        step_desc = step.get("description", "")
        step_index = step.get("index", 0)
        step_name = f"步骤{step_index}"
        full_name = f"{step_name}: {step_desc[:40]}"
        if full_name in seen_step_names:
            continue
        seen_step_names.add(full_name)

        consumes = _extract_io_clues(step_desc, _CONSUMES_PATTERNS)
        produces = _extract_io_clues(step_desc, _PRODUCES_PATTERNS)

        # v1.29.1: fallback
        if not consumes and not produces:
            consumes, produces = _fallback_io_from_step_name(step_desc, "")

        # 编号步骤没有 call_address，标记为手动
        blueprint = {
            "step_id": f"{skill_name}.step-{step_index}",
            "step_name": full_name,
            "skill_name": skill_name,
            "section": f"步骤{step_index}",
            "description": step_desc[:200],
            "call_address": {"instructions": [], "cli": ""},
            "usage_hint": "",
            "interface": {
                "consumes": [_clue_to_io_item(c) for c in consumes],
                "produces": [_clue_to_io_item(p) for p in produces],
            },
            "_fallback": True,
        }
        blueprint_steps.append(blueprint)

    return blueprint_steps


def _find_section_text(content, heading):
    """找到 ### 标题后的文本区域（直到下一个 ### 或文件结束）"""
    if not heading:
        return ""
    pattern = re.escape(heading) + r'\s*\n(.*?)(?=\n###|\Z)'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        text = match.group(1).strip()
        # 去掉代码块
        text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
        return text.strip()
    return ""


def _extract_io_clues(text, patterns):
    """从文本中提取 I/O 语义线索"""
    clues = []
    for pattern in patterns:
        matches = re.findall(pattern, text)
        clues.extend(m.strip() for m in matches if m.strip())
    return _deduplicate_clues(clues)


def _extract_usage_hint(section_text):
    """从段落文本中提取使用提示"""
    if not section_text:
        return ""
    for pattern in _USAGE_HINT_PATTERNS:
        match = re.search(pattern, section_text)
        if match:
            hint = match.group(1).strip()
            if len(hint) > 5:
                return hint[:150]
    return ""


def _build_call_address(cmd, cli_usage, skill_name):
    """构建步骤的调用地址"""
    cmd_name = cmd.get("command", cmd.get("name", ""))

    # 从 CLI 用法中匹配与此指令相关的命令
    related_clis = []
    for cli in cli_usage:
        if cmd_name.lower() in cli.lower() or cmd_name.replace("-", "").lower() in cli.lower():
            related_clis.append(cli)

    # 构建 call_address
    call_address = {
        "instructions": [cmd_name] if cmd_name else [],
        "cli": related_clis[0] if related_clis else "",
        "cli_alternatives": related_clis[1:3] if len(related_clis) > 1 else [],
    }
    return call_address


def _clue_to_io_item(clue):
    """将语义线索转为 interface 条目"""
    clue = clue.strip()
    # 尝试识别类型（路径/文件/报告/配置等）
    io_type = "other"
    type_keywords = {
        "路径": "path", "目录": "dir", "文件": "file",
        "报告": "report", "结果": "result", "配置": "config",
        "数据": "data", "列表": "list", "JSON": "json",
        "Markdown": "markdown", "YAML": "yaml", "文本": "text",
        "URL": "url", "名称": "name", "参数": "param",
    }
    for kw, t in type_keywords.items():
        if kw in clue:
            io_type = t
            break

    return {"type": io_type, "desc": clue}

def extract_parameters(content):
    """提取技能可调用的参数列表（从 SKILL.md 的 trigger/参数表中）"""
    params = []
    # 从表格中提取参数（| 参数 | 类型 | 说明 |）
    table_header = None
    in_table = False
    for ln in content.split(chr(10)):
        stripped = ln.strip()
        if stripped.startswith('|'):
            if not in_table:
                in_table = True
                if '参数' in stripped or 'param' in stripped.lower():
                    table_header = [h.strip() for h in stripped.split('|')[1:-1]]
                    continue
            if table_header and stripped != stripped.replace('-', ' ').replace('|', '-'):
                cells = [c.strip() for c in stripped.split('|')[1:-1]]
                if len(cells) >= 1:
                    params.append({
                        'name': cells[0],
                        'type': cells[1] if len(cells) > 1 else 'string',
                        'description': cells[2] if len(cells) > 2 else ''
                    })
        else:
            if in_table and table_header:
                break
            in_table = False

    # 从 argparse / CLI 定义中提取参数
    import re
    arg_pattern = r'--(\w[-\w]*)'
    for m in re.finditer(arg_pattern, content):
        param_name = m.group(1)
        if not any(p['name'] == param_name for p in params):
            params.append({'name': param_name, 'type': 'string', 'description': ''})

    return params[:20]

def extract_all(skill_name, skill_path=None, use_cache=True):
    """提取技能的所有关键信息"""
    # 检查缓存
    if use_cache:
        cached = get_cached_extraction(skill_name)
        if cached:
            return cached

    if skill_path is None:
        skill_dir = find_skill_dir(skill_name)
        if not skill_dir:
            return {"error": f"技能 '{skill_name}' 未找到", "skill_name": skill_name}
    else:
        skill_dir = Path(skill_path)

    content = read_skill_md(skill_dir)
    if content is None:
        return {"error": f"SKILL.md 不存在于 {skill_dir}", "skill_name": skill_name}

    frontmatter = extract_frontmatter(content)
    description = extract_description(content)
    triggers = extract_trigger_keywords(content)
    commands = extract_core_commands(content)
    skill_instructions = extract_skill_instructions(content)
    key_steps = extract_key_steps(content)
    cli_usage = extract_cli_usage(content)

    # 读取 _meta.json
    meta = {}
    meta_file = skill_dir / "_meta.json"
    if meta_file.exists():
        with open(meta_file, "r", encoding="utf-8") as f:
            meta = json.load(f)

    result = {
        "skill_name": skill_name,
        "dir_name": skill_dir.name,
        "slug": frontmatter.get("slug", meta.get("slug", "")),
        "version": frontmatter.get("version", meta.get("version", "")),
        "agent_created": frontmatter.get("agent_created", False),
        "description": description[:500],
        "trigger_keywords": triggers[:10],
        "core_commands": commands[:10],
        "skill_instructions": skill_instructions[:20],
        "key_steps": key_steps[:10],
        "cli_examples": cli_usage[:10],
        "has_scripts": (skill_dir / "scripts").is_dir(),
        "script_files": [f.name for f in (skill_dir / "scripts").glob("*.py")] if (skill_dir / "scripts").is_dir() else []
    }
    # 缓存结果
    if use_cache:
        cache_extraction(skill_name, result)

    return result

# ============================================================
# 命令实现
# ============================================================

def load_cache():
    """加载缓存数据"""
    cf = _cache_dir / "extraction_cache.json"
    if cf.exists():
        try:
            with open(cf, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_cache(cache_data):
    """保存缓存数据"""
    cf = _cache_dir / "extraction_cache.json"
    cf.parent.mkdir(parents=True, exist_ok=True)
    with open(cf, "w", encoding="utf-8") as f:
        json.dump(cache_data, f, ensure_ascii=False, indent=2)

def get_cached_extraction(skill_name):
    """获取缓存的提取结果（检查时效性：缓存有效期 1 小时）"""
    cache = load_cache()
    if skill_name not in cache:
        return None
    entry = cache[skill_name]
    import time
    if time.time() - entry.get("cached_at", 0) > 3600:
        return None
    return entry.get("data")

def cache_extraction(skill_name, data):
    """缓存提取结果"""
    cache = load_cache()
    import time

    cache[skill_name] = {
        "data": data,
        "cached_at": time.time()
    }
    save_cache(cache)

def cmd_extract(args):
    """提取单个技能的关键信息"""
    result = extract_all(args.skill, args.path)
    if "error" in result:
        print(f"❌ {result['error']}")
        return 1

    print(f"📌 技能: {result['skill_name']}")
    print(f"{'='*60}")
    print(f"  目录: {result['dir_name']}")
    if result.get("slug"):
        print(f"  Slug: {result['slug']}")
    if result.get("version"):
        print(f"  版本: {result['version']}")
    print(f"  描述: {result['description'][:200]}")

    if result.get("trigger_keywords"):
        print(f"\n  🔑 触发关键词:")
        for t in result["trigger_keywords"]:
            print(f"     - {t}")

    if result.get("core_commands"):
        print(f"\n  📋 核心指令:")
        for c in result["core_commands"]:
            cmd_str = f" ({c['command']})" if c.get("command") and c["command"] != c["name"] else ""
            print(f"     - {c['name']}{cmd_str}")

    # v1.19.0: 显示可用的 skill_instruction 候选
    if result.get("skill_instructions"):
        print(f"\n  🏷️ 可用指令（skill_instruction 候选）:")
        for si in result["skill_instructions"]:
            print(f"     - {si}")

    if result.get("key_steps"):
        print(f"\n  🔧 关键步骤:")
        for s in result["key_steps"]:
            print(f"     {s['index']}. {s['description']}")

    if result.get("has_scripts"):
        print(f"\n  📁 脚本文件:")
        for sf in result["script_files"]:
            print(f"     - {sf}")

    # JSON 输出（可选）
    if args.json:
        print(f"\n{'─'*60}")
        print(json.dumps(result, ensure_ascii=False, indent=2))

    return 0

def cmd_extract_params(args):

    """提取指定技能的参数列表"""
    result = extract_all(args.skill, args.path)

    if "error" in result:

        print(f"❌ {result['error']}")

        return 1

    params = []

    skill_dir = find_skill_dir(args.skill)

    if skill_dir:

        md = read_skill_md(skill_dir)

        if md:

            params = extract_parameters(md)

    if not params:

        print(f"未找到参数：{args.skill}")

        return 0

    print(f"📋 技能参数：{args.skill}")

    print(f"{'='*60}")

    for p in params:

        name = p.get('name', '')

        typ = p.get('type', 'string')

        desc = p.get('description', '')

        print(f"  - {name} ({typ})：{desc}")

    if args.json:

        print(json.dumps(params, ensure_ascii=False, indent=2))

    return 0

def cmd_scan(args):
    """扫描所有已安装技能"""
    if not SKILLS_DIR.exists():
        print(f"❌ 技能目录不存在: {SKILLS_DIR}")
        return 1

    skills = []
    for entry in sorted(SKILLS_DIR.iterdir()):
        if entry.is_dir() and not entry.name.startswith("."):
            skill_md = entry / "SKILL.md"
            if skill_md.exists():
                skills.append(entry)

    if not skills:
        print("📋 未找到任何已安装技能")
        return 0

    print(f"📋 扫描已安装技能（共 {len(skills)} 个）")
    print(f"{'='*60}")

    results = []
    for skill_dir in skills:
        result = extract_all(skill_dir.name, skill_dir)
        if "error" not in result:
            # 标签过滤
            if args.tag:
                desc_lower = result.get("description", "").lower()
                triggers_str = " ".join(result.get("trigger_keywords", [])).lower()
                tags_str = desc_lower + " " + triggers_str
                if args.tag.lower() not in tags_str:
                    continue
            results.append(result)

    if not results:
        print(f"  未找到匹配 '{args.tag}' 的技能" if args.tag else "  无结果")
        return 0

    for r in results:
        print(f"\n  📌 {r['dir_name']}")
        print(f"     描述: {r['description'][:100]}")
        if r.get("trigger_keywords"):
            print(f"     触发: {'; '.join(r['trigger_keywords'][:3])}")
        if r.get("core_commands"):
            cmd_names = [c["name"] for c in r["core_commands"][:5]]
            print(f"     指令: {', '.join(cmd_names)}")
        if r.get("skill_instructions"):
            si_names = r["skill_instructions"][:5]
            print(f"     可用指令: {', '.join(si_names)}")
        scripts = r.get("script_files", [])
        if scripts:
            print(f"     脚本: {', '.join(scripts)}")

    # JSON 输出（可选）
    if args.json:
        print(f"\n{'─'*60}")
        print(json.dumps(results, ensure_ascii=False, indent=2))

    return 0

# ============================================================
# CLI 入口
# ============================================================

def cmd_clear_cache(args):

    """清空提取缓存"""
    cf = _cache_dir / "extraction_cache.json"

    if cf.exists():

        cf.unlink()

        print("✅ 缓存已清空")

    else:

        print("ℹ️ 无缓存可清空")

    return 0

def cmd_suggest(args):
    """根据用户意图推荐技能并检测缺口（v1.29.1: 同义词展开 + n-gram 匹配）"""
    # 同义词映射（精简版）
    _SYNONYM_MAP_SHORT = {
        "审查": "review 审 audit 审计",
        "审计": "audit 审 review 审查",
        "分析": "analyze analysis",
        "代码": "code",
        "测试": "test",
        "部署": "deploy release 发布 上线",
        "发布": "publish release deploy 部署",
        "生成": "generate create 创建",
        "报告": "report",
        "验证": "verify validate 校验",
        "扫描": "scan 检测",
        "构建": "build compile 编译",
        "打包": "pack zip",
        "推送": "push sync 同步",
        "搜索": "search query 查询",
        "处理": "process handle",
        "配置": "config 参数 param",
        "数据": "data",
        "文件": "file",
        "文档": "doc document",
    }
    
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass
    
    intent = args.intent.lower().strip()
    if not intent:
        print("❌ 请提供意图关键词")
        return 1

    if not SKILLS_DIR.exists():
        print(f"❌ 技能目录不存在: {SKILLS_DIR}")
        return 1

    # 1. 扫描所有技能
    candidates = []
    for entry in sorted(SKILLS_DIR.iterdir()):
        if not entry.is_dir() or entry.name.startswith("."):
            continue
        skill_md = entry / "SKILL.md"
        if not skill_md.exists():
            continue

        result = extract_all(entry.name, entry)
        if "error" in result:
            continue

        # 2. 关键词匹配打分
        desc = result.get("description", "").lower()
        triggers = " ".join(result.get("trigger_keywords", [])).lower()
        tags = " ".join(result.get("tags", [])).lower()
        skill_name = result.get("dir_name", "").lower()

        search_text = f"{skill_name} {desc} {triggers} {tags}"
        intent_words = intent.split()

        if not intent_words:
            continue

        # v1.29.1: 同义词展开 + n-gram 匹配
        # 同义词展开
        syn_intent = intent
        syn_search = search_text
        for word, syns in _SYNONYM_MAP_SHORT.items():
            if word in syn_intent:
                syn_intent += " " + syns
            if word in syn_search:
                syn_search += " " + syns

        syn_intent_words = syn_intent.split()
        syn_search_words = syn_search.split()

        # 词匹配 + 同义词匹配
        word_matches = sum(1 for w in intent_words if w in search_text)
        syn_matches = sum(1 for w in syn_intent_words if w in syn_search)

        # 中文 bi-gram
        intent_chars = set("".join(intent_words))
        search_chars = set(search_text.replace(" ", ""))
        ngram = len(intent_chars & search_chars) / max(len(intent_chars | search_chars), 1)

        score = (
            (word_matches / max(len(intent_words), 1)) * 0.4 +
            (syn_matches / max(len(syn_intent_words), 1)) * 0.4 +
            ngram * 0.2
        )
        score = min(score, 1.0)

        if score >= args.min_score:
            candidates.append({
                "name": result["dir_name"],
                "description": result.get("description", ""),
                "trigger": result.get("trigger_keywords", []),
                "tags": result.get("tags", []),
                "score": round(score, 2),
            })

    # 3. 按分数排序
    candidates.sort(key=lambda c: c["score"], reverse=True)

    # 4. 缺口检测：意图中有但没有任何 skill 匹配的词（v1.29.1: 支持同义词展开）
    matched_words = set()
    for c in candidates:
        text = f"{c['name']} {c['description']} {' '.join(c['trigger'])} {' '.join(c['tags'])}".lower()
        syn_text = text
        for word, syns in _SYNONYM_MAP_SHORT.items():
            if word in syn_text:
                syn_text += " " + syns
        for w in intent_words:
            if w in text:
                matched_words.add(w)
            # 同义词展开匹配
            for word, syns in _SYNONYM_MAP_SHORT.items():
                if w == word and any(s.lower() in syn_text for s in syns.split()):
                    matched_words.add(w)
                    break

    unmatched = [w for w in intent_words if w not in matched_words and len(w) > 1]

    # 5. 输出
    result = {
        "intent": intent,
        "total_skills": len([e for e in SKILLS_DIR.iterdir() if e.is_dir() and not e.name.startswith(".")]),
        "candidates": candidates,
        "gaps": [{"word": w, "hint": f"意图中的「{w}」无 skill 直接匹配，可能需要粘连点或新 skill"} for w in unmatched],
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"推荐报告: {intent}")
        print(f"扫描技能: {result['total_skills']} 个")
        print(f"匹配候选: {len(candidates)} 个")
        if candidates:
            print(f"{'':-<50}")
            print(f"{'排名':<6} {'技能名称':<20} {'匹配分':<8} {'描述'}")
            print(f"{'':-<50}")
            for i, c in enumerate(candidates, 1):
                desc_short = c["description"][:40] + "..." if len(c["description"]) > 40 else c["description"]
                print(f"{i:<6} {c['name']:<20} {c['score']:<8} {desc_short}")
        if result["gaps"]:
            print(f"\n检测到缺口（{len(result['gaps'])} 个）：")
            for g in result["gaps"]:
                print(f"  - {g['hint']}")
        else:
            print("\n未检测到明显缺口")

    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Skill Extractor v1.19.0 - 技能关键步骤提取工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python skill_extractor.py extract --skill "triphasic-execution"
  python skill_extractor.py extract --skill "git-sync" --json
  python skill_extractor.py scan
  python skill_extractor.py scan --tag "搜索"
  python skill_extractor.py scan --json
        """
    )
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # extract
    p_extract = subparsers.add_parser("extract", help="提取单个技能的关键信息")
    p_extract.add_argument("--skill", required=True, help="技能名称")
    p_extract.add_argument("--path", default=None, help="技能目录路径（可选）")
    p_extract.add_argument("--json", action="store_true", help="JSON 格式输出")

    # scan
    p_scan = subparsers.add_parser("scan", help="扫描所有已安装技能")
    p_scan.add_argument("--tag", default=None, help="按关键词过滤")
    p_scan.add_argument("--json", action="store_true", help="JSON 格式输出")
    # extract-params
    p_params = subparsers.add_parser("extract-params", help="提取技能参数列表")
    p_params.add_argument("--skill", required=True, help="技能名称")
    p_params.add_argument("--path", default=None, help="技能目录路径（可选）")
    p_params.add_argument("--json", action="store_true", help="JSON 格式输出")
    p_params.add_argument("--no-cache", action="store_true", help="跳过缓存")

    # clear-cache
    p_clear = subparsers.add_parser("clear-cache", help="清空提取缓存")

    # suggest (v1.25.0)
    p_suggest = subparsers.add_parser("suggest", help="根据用户意图推荐技能并检测缺口")
    p_suggest.add_argument("--intent", required=True, help="用户意图关键词（自然语言描述）")
    p_suggest.add_argument("--json", action="store_true", help="JSON 格式输出")
    p_suggest.add_argument("--min-score", type=float, default=0.1, help="最低匹配分数（默认0.1）")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    commands = {
        "extract": cmd_extract,
        "scan": cmd_scan,
        "extract-params": cmd_extract_params,
        "clear-cache": cmd_clear_cache,
        "suggest": cmd_suggest,
    }

    cmd_func = commands.get(args.command)
    if cmd_func:
        return cmd_func(args)
    else:
        parser.print_help()
        return 1

if __name__ == "__main__":
    sys.exit(main())
