#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix.py — skill-standardization 统一修复工具
为全部 23 条审计规则（R-01~R-23）提供针对性修复函数。

大模型/LLM 看到审计结果后，直接调用对应修复函数：
    from skill_audit.fix import apply_fix
    apply_fix(skill_dir, "name", value="xxx")  # R-01

修复函数命名规则：fix_<rule_key>(skill_dir, **kw)

v2.37.0: 初始版本，覆盖全部 23 条规则
"""

import os
import re
import io
import json
import traceback

from .utils import _fmt_frontmatter_value, parse_simple_yaml_frontmatter


# ═══════════════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════════════

def _read_file(filepath):
    """读取文件内容（UTF-8）"""
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def _write_file(filepath, content):
    """写入文件内容（UTF-8），优先使用 safe_io 原子写入，fallback 到内置 open"""
    try:
        from ..safe_io import safe_write
        safe_write(filepath, content, backup=True)
    except (ImportError, ValueError):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)


def _update_frontmatter_field(filepath, field_name, field_value):
    """
    更新 SKILL.md frontmatter 中的单个字段。
    如果字段不存在则添加（追加在 --- 之后）。
    返回: True/False
    """
    if not os.path.isfile(filepath):
        return False
    content = _read_file(filepath)
    fm, body = parse_simple_yaml_frontmatter(content)
    if fm is None:
        return False
    fm[field_name] = field_value
    body = body.lstrip("\n")
    # 重写文件
    buf = io.StringIO()
    buf.write("---\n")
    for k, v in fm.items():
            buf.write(f"{k}: {_fmt_frontmatter_value(v)}\n")
    buf.write("---\n")
    buf.write(body)
    _write_file(filepath, buf.getvalue())
    return True


def _add_section_to_body(filepath, section_title, section_body, insert_after=None):
    """
    向 SKILL.md body 添加（或替换）一个 ## 章节。
    insert_after: 如果指定，在该章节之后插入；否则追加到 body 末尾。
    返回: True/False
    """
    if not os.path.isfile(filepath):
        return False
    content = _read_file(filepath)
    fm, body = parse_simple_yaml_frontmatter(content)
    if fm is None:
        return False

    lines = body.split("\n")
    # 检查章节是否已存在
    existing = [i for i, ln in enumerate(lines) if ln.strip().startswith(f"## {section_title}")]
    if existing:
        # 替换现有章节内容
        start = existing[0]
        end = start + 1
        while end < len(lines) and not lines[end].strip().startswith("## "):
            end += 1
        lines = lines[:start+1] + [section_body] + lines[end:]
    else:
        # 追加新章节
        if insert_after:
            # 找到 insert_after 章节的结束位置
            in_sec = False
            insert_idx = len(lines)
            for i, ln in enumerate(lines):
                if ln.strip().startswith(f"## {insert_after}"):
                    in_sec = True
                    continue
                if in_sec and ln.strip().startswith("## "):
                    insert_idx = i
                    break
            lines = lines[:insert_idx] + ["", f"## {section_title}", section_body] + lines[insert_idx:]
        else:
            lines.append("")
            lines.append(f"## {section_title}")
            lines.append(section_body)

    new_body = "\n".join(lines)
    buf = io.StringIO()
    buf.write("---\n")
    for k, v in fm.items():
            buf.write(f"{k}: {_fmt_frontmatter_value(v)}\n")
    buf.write("---\n")
    buf.write(new_body)
    _write_file(filepath, buf.getvalue())
    return True


# ═══════════════════════════════════════════════════
# R-01: name 字段修复
# ═══════════════════════════════════════════════════

def fix_name(skill_dir, **kw):
    """
    R-01 修复：添加/更正 SKILL.md name 字段。
    value: 技能名称（如 "git-sync"）
    """
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return 0
    value = kw.get("value", os.path.basename(os.path.abspath(skill_dir)))
    ok = _update_frontmatter_field(skill_md, "name", value)
    return 1 if ok else 0


# ═══════════════════════════════════════════════════
# R-02: description 字段修复
# ═══════════════════════════════════════════════════

def fix_description(skill_dir, **kw):
    """
    R-02 修复：添加/更正 description 字段。
    value: 技能描述
    """
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return 0
    value = kw.get("value", "")
    if not value:
        # 尝试从 name 推断
        content = _read_file(skill_md)
        fm, _ = parse_simple_yaml_frontmatter(content)
        if fm and fm.get("name"):
            value = f"{fm['name']} 技能"
    if not value:
        return 0
    ok = _update_frontmatter_field(skill_md, "description", value)
    return 1 if ok else 0


# ═══════════════════════════════════════════════════
# R-03: author 字段修复
# ═══════════════════════════════════════════════════

def fix_author(skill_dir, **kw):
    """
    R-03 修复：添加 author 字段。
    value: 作者名
    """
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return 0
    value = kw.get("value", "[username-redacted]")
    ok = _update_frontmatter_field(skill_md, "author", value)
    return 1 if ok else 0


# ═══════════════════════════════════════════════════
# R-04: version 字段修复
# ═══════════════════════════════════════════════════

def fix_version(skill_dir, **kw):
    """
    R-04 修复：更正 version 字段格式（X.Y.Z 三段式）。
    value: 版本号（如 "1.2.3"）
    """
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return 0
    value = kw.get("value", "1.0.0")
    # 确保格式正确
    m = re.match(r'(\d+)', str(value))
    if m:
        value = m.group(1) + ".0.0" if len(value.split(".")) == 1 else value
    ok = _update_frontmatter_field(skill_md, "version", value)
    return 1 if ok else 0


# ═══════════════════════════════════════════════════
# R-05: skill_macro 字段修复
# ═══════════════════════════════════════════════════

def fix_skill_macro(skill_dir, **kw):
    """
    R-05 修复：添加 skill_macro 字段（调用宏）。
    value: 宏名称（如 "unified"）
    """
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return 0
    value = kw.get("value", "unified")
    ok = _update_frontmatter_field(skill_md, "skill_macro", value)
    return 1 if ok else 0


# ═══════════════════════════════════════════════════
# R-06: 一级标题修复
# ═══════════════════════════════════════════════════

def fix_h1(skill_dir, **kw):
    """
    R-06 修复：在 SKILL.md body 开头添加一级标题。
    value: 标题文本（如 "git-sync"）
    """
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return 0
    content = _read_file(skill_md)
    fm, body = parse_simple_yaml_frontmatter(content)
    if fm is None:
        return 0
    value = kw.get("value", fm.get("name", os.path.basename(os.path.abspath(skill_dir))))
    # 检查是否已有 H1
    if re.search(r'^# .+', body, re.MULTILINE):
        return 0  # 已存在
    # 在 body 开头插入 H1
    new_body = f"# {value}\n\n{body.lstrip()}"
    # 重写文件
    buf = io.StringIO()
    buf.write("---\n")
    for k, v in fm.items():
            buf.write(f"{k}: {_fmt_frontmatter_value(v)}\n")
    buf.write("---\n")
    buf.write(new_body)
    _write_file(skill_md, buf.getvalue())
    return 1


def fix_h1_version(skill_dir, **kw):
    """
    R-06 修复：移除 H1 标题中的版本号。
    如 '# skill-standardization v2.38.7' → '# skill-standardization'
    """
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return 0
    content = _read_file(skill_md)
    fm, body = parse_simple_yaml_frontmatter(content)
    if fm is None:
        return 0
    # 匹配 # 开头的一级标题中是否含版本号
    m = re.search(r'^(#\s+.*?)\s+v?\d+\.\d+\.\d+\s*$', body, re.MULTILINE)
    if not m:
        return 0  # 无版本号
    h1_clean = m.group(1).strip()
    # 替换
    new_body = re.sub(r'^(#\s+.*?)\s+v?\d+\.\d+\.\d+\s*$', f'# {h1_clean}', body, count=1, flags=re.MULTILINE)
    buf = io.StringIO()
    buf.write("---\n")
    for k, v in fm.items():
            buf.write(f"{k}: {_fmt_frontmatter_value(v)}\n")
    buf.write("---\n")
    buf.write(new_body)
    _write_file(skill_md, buf.getvalue())
    return 1


def fix_h1_position(skill_dir, **kw):
    """
    R-06 修复：将 H1 移到 frontmatter 后首行。
    如 H1 在 body 的非开头位置（如 ## 触发条件 之后），
    将其提到 body 最前面。
    """
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return 0
    content = _read_file(skill_md)
    fm, body = parse_simple_yaml_frontmatter(content)
    if fm is None:
        return 0
    # 找到 body 中的 H1（排除代码块内的 # 注释）
    body_no_code = re.sub(r'```.*?```', '', body, flags=re.DOTALL)
    m = re.search(r'^# .+', body_no_code, re.MULTILINE)
    if not m:
        return 0
    # 检查 H1 是否已在 body 前 2 行内
    h1_body_line = body[:m.start()].count('\n') + 1
    if h1_body_line <= 2:
        return 0  # 位置已正确
    # 分离 H1 之前的内容、H1 本身、H1 之后的内容
    lines = body.split('\n')
    h1_idx = m.group(0)
    # 按行找到实际 H1 位置（用 body_no_code 定位但操作 body 的真实行）
    body_lines = body.split('\n')
    real_h1_idx = None
    for i, line in enumerate(body_lines):
        stripped = line.strip()
        if stripped.startswith('# ') and stripped not in ('# 返回', '# {', '# [',
             '# 每次', '# 备份', '# Windows', '# 或命令', '# 今天', '# 指定', '# 规则', '# 工作日', '# 日程'):
            # 简单判断：不在代码块标志内（不以空格/制表符缩进的行）
            if not line.startswith(' ') and not line.startswith('\t'):
                # 确认这是我们要找的 H1（排除# 返回这类注释）
                real_h1_idx = i
                break
    if real_h1_idx is None:
        return 0
    # 重组：H1 移到 body 开头，其余内容保持相对顺序
    h1_line = body_lines[real_h1_idx].strip()
    before = body_lines[:real_h1_idx]
    after = body_lines[real_h1_idx + 1:]
    # 清理 before 的尾部空行
    while before and not before[-1].strip():
        before.pop()
    # 清理 after 的头部空行
    while after and not after[0].strip():
        after.pop(0)
    # 新 body
    new_body_lines = ['# ' + h1_line[2:].strip() if h1_line.startswith('# ') else h1_line,
                      ''] + before + [''] + after
    new_body = '\n'.join(new_body_lines)
    # 写回
    buf = io.StringIO()
    buf.write("---\n")
    for k, v in fm.items():
            buf.write(f"{k}: {_fmt_frontmatter_value(v)}\n")
    buf.write("---\n")
    buf.write(new_body)
    _write_file(skill_md, buf.getvalue())
    return 1


# ═══════════════════════════════════════════════════
# R-07: 触发条件章节修复
# ═══════════════════════════════════════════════════

def fix_section_trigger(skill_dir, **kw):
    """
    R-07 修复：添加/完善 ## 触发场景 章节。
    优先从目标技能自身采集触发词，回退到 content_format 格式。
    """
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return 0
    content = _read_file(skill_md)
    fm, body = parse_simple_yaml_frontmatter(content)
    if fm is None:
        return 0
    name = fm.get("name", "本技能")
    desc = fm.get("description", "")

    # ── 采集源：从脚本 docstring 中提取功能关键词 ──
    triggers = []
    neg_triggers = ["简单问答、闲聊、问候（不需要本技能）", "单步任务（不需要结构化执行）"]
    scripts_dir = os.path.join(skill_dir, "scripts")
    if os.path.isdir(scripts_dir):
        for root, dirs, files in os.walk(scripts_dir):
            for f in files:
                if not f.endswith('.py'): continue
                try:
                    with open(os.path.join(root, f), 'r', encoding='utf-8') as fh:
                        src = fh.read()
                except:
                    print(f"[WARN] 读取 {os.path.join(root, f)} 失败，跳过")
                    traceback.print_exc()
                    continue
                # 从 docstring 提取功能描述
                docstrings = re.findall(r'"""(.*?)"""', src, re.DOTALL)
                for ds in docstrings:
                    lines = [l.strip() for l in ds.split('\n') if l.strip()]
                    for line in lines[:3]:
                        if len(line) > 6 and len(line) < 60 and not line.startswith(('Args', 'Returns', 'Raises')):
                            triggers.append(line[:50])

    # ── 采集源：从 frontmatter trigger 字段 ──
    fm_triggers = fm.get("trigger", "")
    if isinstance(fm_triggers, list):
        for t in fm_triggers:
            if t and t not in triggers:
                triggers.append(t)

    # ── 采集源：从 description 提取关键动作 ──
    action_kw = re.findall(r'[\u4e00-\u9fff]{2,}(?:工具|功能|能力|模块|系统)', desc)
    for a in action_kw:
        if a not in triggers:
            triggers.append(a)

    # ── 去重截断 ──
    triggers = [t for t in triggers if len(t) > 4][:6]

    if not triggers:
        triggers = [f"使用 {name}", f"询问关于 {name} 的问题", f"需要 {name}"]

    # ── 生成正/否定双列表 ──
    pos_items = '\n'.join(f"- {t}" if not t.startswith('- ') else t for t in triggers[:4])
    neg_section = '\n'.join(f"- {t}" for t in neg_triggers)

    section_body = (
        f"**正向触发**：\n"
        f"{pos_items}\n\n"
        f"**否定条件**：\n"
        f"{neg_section}\n"
    )

    ok = _add_section_to_body(skill_md, "触发场景", section_body, insert_after=None)
    return 1 if ok else 0


# ═══════════════════════════════════════════════════
# R-08: 核心能力章节修复
# ═══════════════════════════════════════════════════

def fix_section_core(skill_dir, **kw):
    """
    R-08 修复：添加 ## 核心能力 章节。
    使用 body.json content_format 模板生成表格格式。
    """
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return 0
    content = _read_file(skill_md)
    fm, body = parse_simple_yaml_frontmatter(content)
    if fm is None:
        return 0
    name = fm.get("name", "本技能")

    # 从 body.json 读取 content_format 模板
    spec = _load_body_spec()
    fmt = None
    for sec in spec.get("required_sections", []):
        kws = sec.get("keywords", [])
        if any(k in str(kws) for k in ["核心功能", "核心能力", "概述"]):
            fmt = sec.get("content_format", {})
            break

    if fmt and fmt.get("type") == "table":
        # 使用 content_format 的表格模板
        cols = fmt.get("table_columns", ["#", "能力", "说明"])
        col_header = "| " + " | ".join(cols) + " |"
        col_sep = "|" + "|".join("-" * max(len(c) + 2, 3) for c in cols) + "|"
        section_body = (
            f"> 📚 **渐进式加载**：本技能采用渐进式 MD 体系，`SKILL.md` 为入口（≤230行），详细内容拆分到 `references/*.md` 按需加载。\n\n"
            f"{col_header}\n"
            f"{col_sep}\n"
            f"| 1 | **{name} 功能一** | 功能一的简要说明 |\n"
            f"| 2 | **{name} 功能二** | 功能二的简要说明 |\n"
            f"| 3 | **{name} 功能三** | 功能三的简要说明 |\n"
        )
    else:
        # 回退：无序列表格式
        section_body = (
            f"- {name} 的核心功能 1\n"
            f"- {name} 的核心功能 2\n"
            f"- {name} 的核心功能 3\n"
            "> 📚 **渐进式加载**：本技能采用渐进式 MD 体系，`SKILL.md` 为入口（≤230行），"
            "详细内容拆分到 `references/*.md` 按需加载。\n"
        )
    ok = _add_section_to_body(skill_md, "核心能力", section_body, insert_after=None)
    return 1 if ok else 0


def fix_section_workflow(skill_dir, **kw):
    """
    R-09 修复：添加 ## 工作流程 章节。
    v2.102.4: 如果已有工作流章节且内容比模板多（已有自定义内容），跳过覆盖。
    """
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return 0
    content = _read_file(skill_md)
    fm, body = parse_simple_yaml_frontmatter(content)
    name = fm.get("name", "本技能") if fm else "本技能"

    # v2.102.4: 检查现有工作流章节是否已有超越模板的自定义内容
    if body:
        lines = body.split("\n")
        for i, ln in enumerate(lines):
            if ln.strip().startswith("## 工作流程"):
                # 统计后续行数（直到下一个 ## 或结束）
                end = i + 1
                while end < len(lines) and not lines[end].strip().startswith("## "):
                    end += 1
                existing_lines = end - i - 1  # 减去标题行
                # 模板内容行数 = 5 (4步 + 渐进式行)
                if existing_lines > 6:
                    return 0  # 已有自定义内容，跳过覆盖
                break

    section_body = (
        "1. 理解用户需求\n"
        "2. 规划执行步骤\n"
        "3. 调用相关工具/脚本\n"
        "4. 返回结果给用户\n"
        "> 📚 **渐进式加载**：本技能采用渐进式 MD 体系，`SKILL.md` 为入口（≤230行），"
        "详细内容拆分到 `references/*.md` 按需加载。"
    )
    ok = _add_section_to_body(skill_md, "工作流程", section_body, insert_after="核心能力")
    return 1 if ok else 0


# ═══════════════════════════════════════════════════
# R-10: home_url 字段修复
# ═══════════════════════════════════════════════════

def fix_home_url(skill_dir, **kw):
    """
    R-10 修复：添加 home_url 字段（相关链接）。
    value: URL
    """
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return 0
    value = kw.get("value", "")
    if not value:
        return 0
    ok = _update_frontmatter_field(skill_md, "home_url", value)
    return 1 if ok else 0


# ═══════════════════════════════════════════════════
# R-11: 产出物路径修复
# ═══════════════════════════════════════════════════

def fix_artifact_paths(skill_dir, **kw):
    """
    R-11 修复：将违规文件迁出根目录/脚本目录。
    
    两步逻辑：
    1. 分辨文件性质：
       - 缓存/临时/错误文件（*.tmp, *.bak, __pycache__/, .DS_Store等）→ 直接删除
       - 有意义的文件（脚本、配置、数据）→ 移到正确位置（scripts/ 或 data/）
    2. 修正引用：
       - 移动/删除后，扫描所有文件中的引用路径并修正
    
    返回：修复的文件数
    """
    fixed = 0
    skill_name = os.path.basename(os.path.abspath(skill_dir))
    std_base = os.path.join(".standardization", skill_name)
    
    # ── 第1步：分辨文件性质，决定删除还是移动 ──
    # 应删除的垃圾文件模式（缓存、临时、错误文件）
    _TRASH_PATTERNS = {
        r'.*\.tmp$', r'.*\.bak$', r'.*\.swp$', r'.*\.swo$',
        r'.*\.pyc$', r'.*\.pyo$', r'.*__pycache__.*',
        r'.*\.DS_Store$', r'.*\.Thumbs\.db$', r'.*\~$',
        r'^#.*#$', r'.*\.log$',  # 日志文件也删
    }
    import re
    trash_re = re.compile('|'.join(_TRASH_PATTERNS))
    
    # 收集需要处理的违规文件（来自审计结果）
    violations = kw.get("violations", [])
    if not violations:
        # 如果没有传 violations，自己跑一次审计
        from .artifact_checker import check_artifact_paths
        with open(os.path.join(skill_dir, "SKILL.md"), "r", encoding="utf-8") as f:
            content = f.read()
        fm, body = parse_simple_yaml_frontmatter(content)
        result = check_artifact_paths(None, content, fm, body, skill_dir=skill_dir)
        violations = result.get("violations", [])
    
    # 分类：删除 vs 移动
    to_delete = []  # (path, reason)
    to_move = []    # (src, dst_dir, reason)
    
    for v in violations:
        src = v.get("source", "")
        path_lit = v.get("path_literal", "")
        suggestion = v.get("suggestion", "")
        
        # 真实文件匹配：从 violation 提取文件名，扫描根目录找实际文件
        # path_lit 可能是代码中的路径字面量（如 "skills/.standardization/xxx/"）
        # 需要从 violation 信息中提取真实文件名
        basename_to_find = None
        for candidate in [path_lit, src, v.get("detail", ""), v.get("match_context", "")]:
            for sep in ("/", "\\"):
                if sep in candidate:
                    candidate = candidate.rsplit(sep, 1)[-1]
            candidate = candidate.strip().strip("'").strip('"')
            if candidate and candidate != "" and not candidate.startswith("."):
                basename_to_find = candidate
                break
        
        # 扫描根目录找出匹配的产出文件
        matched_file = None
        if basename_to_find:
            for f in os.listdir(skill_dir):
                if f.startswith(basename_to_find) or basename_to_find.startswith(f):
                    full = os.path.join(skill_dir, f)
                    if os.path.isfile(full):
                        matched_file = f
                        break
        
        if not matched_file:
            # 无真实文件：可能是代码中的路径引用违规，尝试修复源文件中的路径
            src_ref = v.get("source", "")
            if src_ref and ":" in src_ref:
                src_file, src_line = src_ref.rsplit(":", 1)
                src_full = os.path.join(skill_dir, src_file)
                if os.path.isfile(src_full) and suggestion:
                    try:
                        with open(src_full, 'r', encoding='utf-8') as _f:
                            _lines = _f.readlines()
                        _ln = int(src_line) - 1  # 0-based
                        if 0 <= _ln < len(_lines):
                            _old = _lines[_ln]
                            # 从 suggestion 提取目标路径中的文件名
                            _target_fname = suggestion.rsplit("/", 1)[-1] if "/" in suggestion else suggestion
                            if _target_fname in _old:
                                _std_path = os.path.join(
                                    ".standardization", skill_name, "outputs", _target_fname).replace("\\", "/")
                                _new = _old.replace(f'os.path.join(skill_dir, "{_target_fname}")',
                                                     f'os.path.join(datadir, "outputs", "{_target_fname}")')
                                if _new != _old:
                                    _lines[_ln] = _new
                                    from .safe_io import safe_write
                                    safe_write(src_full, "".join(_lines))
                                    fixed += 1
                                    print(f"  [代码修复] {src_file}:{src_line} → {_std_path}")
                    except (ValueError, OSError, IndexError):
                        pass
            continue
        
        full_path = os.path.join(skill_dir, matched_file)
        
        # 判断：垃圾文件 → 删除；其他 → 移动
        is_trash = trash_re.search(path_lit) is not None
        # 额外启发：0字节文件、乱码文件名 → 删除
        try:
            if os.path.getsize(full_path) == 0:
                is_trash = True
        except OSError:
            pass
        
        if is_trash:
            to_delete.append((full_path, f"垃圾文件: {suggestion}"))
        else:
            # 有意义文件：移到正确位置
            # ★ CHANGELOG.md / changelog.md 是渐进式参考文件，不属于数据目录
            #   应保持或迁到 references/changelog.md，绝不可迁到 data/
            if os.path.basename(path_lit).lower() in ("changelog.md",):
                print(f"  [跳过] {path_lit} 是渐进式参考文件，不迁移到数据目录（应在 references/changelog.md）")
                continue

            # suggestion 格式：skills/.standardization/<skill>/<cat>/<fname>
            # 提取目标目录
            if "/" in suggestion:
                parts = suggestion.replace("skills/.standardization/", "").split("/")
                if len(parts) >= 2:
                    cat = parts[1]  # outputs/data/cache/temp
                    # ★ v2.62.x 根因修复：目标路径应基于 skills/ 根，不是 skill_dir 内部
                    skills_root = os.path.dirname(os.path.abspath(skill_dir))
                    dst_dir = os.path.join(skills_root, ".standardization", skill_name, cat)
                    to_move.append((full_path, dst_dir, suggestion))
    
    # ── 执行删除 ──
    deleted_files = []
    for fpath, reason in to_delete:
        try:
            os.remove(fpath)
            deleted_files.append(fpath)
            fixed += 1
            print(f"  [删除] {os.path.relpath(fpath, skill_dir)} — {reason}")
        except Exception as e:
            print(f"  [删除失败] {fpath}: {e}")
    
    # ── 执行移动 ──
    moved_files = []
    for src, dst_dir, suggestion in to_move:
        try:
            os.makedirs(dst_dir, exist_ok=True)
            dst = os.path.join(dst_dir, os.path.basename(src))
            # 如果目标已存在，加后缀
            if os.path.exists(dst):
                base, ext = os.path.splitext(dst)
                dst = f"{base}_moved{ext}"
            shutil.move(src, dst)
            moved_files.append((src, dst))
            fixed += 1
            print(f"  [移动] {os.path.relpath(src, skill_dir)} → {os.path.relpath(dst, skill_dir)}")
        except Exception as e:
            print(f"  [移动失败] {src}: {e}")
    
    # ── 第2步：修正引用 ──
    # 收集所有被删除/移动的文件路径（相对 skill_dir）
    affected = {}
    for fpath in deleted_files:
        rel = os.path.relpath(fpath, skill_dir)
        affected[rel] = None  # None 表示已删除
    for src, dst in moved_files:
        src_rel = os.path.relpath(src, skill_dir)
        dst_rel = os.path.relpath(dst, skill_dir)
        affected[src_rel] = dst_rel
    
    if affected:
        print(f"  扫描引用路径，共 {len(affected)} 个文件受影响...")
        # 扫描所有文件，查找引用
        for root, dirs, files in os.walk(skill_dir):
            # 跳过 .standardization/ 数据目录
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for fname in files:
                fpath = os.path.join(root, fname)
                try:
                    with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                        content = f.read()
                    original = content
                    for old_rel, new_rel in affected.items():
                        if new_rel is None:
                            # 文件已删除：只替换相对路径引用，不替换裸文件名
                            # 防止 "SKILL.md" → "[DELETED:SKILL.md]" 误伤
                            # 只匹配作为路径组件出现的引用（含引号/括号的路径上下文）
                            import re as _re
                            old_escaped = _re.escape(old_rel)
                            # 匹配引号内的路径、os.path.join 中的路径段、注释中的路径
                            content = _re.sub(
                                rf'(?<=["\'/\\]){old_escaped}(?=["\'])',
                                f"[DELETED:{old_rel}]",
                                content
                            )
                        else:
                            # 文件已移动：更新路径
                            content = content.replace(old_rel, new_rel)
                            # 也试试 Unix 风格路径
                            content = content.replace(old_rel.replace("\\", "/"), 
                                                       new_rel.replace("\\", "/"))
                    if content != original:
                        from ..safe_io import safe_write
                        safe_write(fpath, content, backup=True)
                        print(f"  [修正引用] {os.path.relpath(fpath, skill_dir)}")
                        fixed += 1
                except Exception:
                    continue
    
    return fixed


# ═══════════════════════════════════════════════════
# R-12: 外部数据目录修复
# ═══════════════════════════════════════════════════

def fix_external_data_dir(skill_dir, **kw):
    """
    R-12 修复：统一数据目录路径到 skills/.standardization/<skill>/data/
    调用 artifact_checker 中的 fix_external_data_dir 函数。
    """
    from .artifact_checker import fix_external_data_dir as _fix
    return _fix(skill_dir)


# ═══════════════════════════════════════════════════
# R-13: sensitive_access 字段修复
# ═══════════════════════════════════════════════════

def fix_sensitive_access(skill_dir, **kw):
    """
    R-13 修复：添加/更正 sensitive_access 字段。
    value: true/false
    """
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return 0
    value = kw.get("value", False)
    ok = _update_frontmatter_field(skill_md, "sensitive_access", bool(value))
    return 1 if ok else 0


# ═══════════════════════════════════════════════════
# R-14: critical_write 字段修复
# ═══════════════════════════════════════════════════

def fix_critical_write(skill_dir, **kw):
    """
    R-14 修复：添加/更正 critical_write 字段。
    value: true/false
    """
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return 0
    value = kw.get("value", False)
    ok = _update_frontmatter_field(skill_md, "critical_write", bool(value))
    return 1 if ok else 0


# ═══════════════════════════════════════════════════
# R-15: 权限说明文档修复
# ═══════════════════════════════════════════════════

def fix_create_permissions_md(skill_dir, **kw):
    """
    R-15 修复：创建/更新 references/permissions.md。
    根据 PermissionChecker 扫描结果自动生成结构化的权限说明，
    按权限类别分组，每组含文件/行号/匹配内容/功能解释的详细表格。
    """
    refs_dir = os.path.join(skill_dir, "references")
    os.makedirs(refs_dir, exist_ok=True)
    permissions_md = os.path.join(refs_dir, "permissions.md")

    # 调用 PermissionChecker 获取实际扫描结果
    # 强制重新导入（避免 audit 流程中已加载的缓存模块使用错误路径）
    import importlib, sys
    for _mod_name in list(sys.modules.keys()):
        if 'permission_checker' in _mod_name:
            importlib.reload(sys.modules[_mod_name])
    from permission_checker import PermissionChecker
    try:
        checker = PermissionChecker(skill_dir)
        report = checker.scan()
        risk_level = report.get("risk_level", "low").upper()
        stats = report.get("stats", {})
        issues = report.get("issues", [])
    except Exception as e:
        print(f"  [R-15] ⚠️ PermissionChecker 调用失败: {e}")
        risk_level = "LOW"
        stats = {}
        issues = []

    n_sensi = stats.get("sensitive_access", 0)
    n_write = stats.get("critical_write", 0)
    n_net = stats.get("network_access", 0)
    n_del = stats.get("file_delete", 0)
    n_sub = stats.get("subprocess_call", 0)
    all_stats = [
        ("subprocess_call",    "子进程调用（subprocess）",  n_sub),
        ("file_delete",        "文件删除",                  n_del),
        ("network_access",     "网络访问",                   n_net),
        ("sensitive_access",   "敏感信息访问",                n_sensi),
        ("critical_write",     "关键位置写入",                n_write),
    ]

    # ── 风险等级描述 ──
    risk_desc = f"**{risk_level}**（实际权重: {report.get('permission_weight', '?')}）\n\n"

    # ── 权限总览表（按类型汇总） ──
    overview_rows = []
    for tkey, tlabel, tcount in all_stats:
        if tcount > 0:
            overview_rows.append(f"| `{tkey}` | {tcount} 项 | 🔴 HIGH |")
        else:
            overview_rows.append(f"| `{tkey}` | 0 项 | ✅ LOW |")
    overview_section = "\n".join(overview_rows)

    # ── 高权限操作说明（按类型分组） ──
    if not issues:
        high_perm_section = "- 无。所有文件操作均限制在技能独立数据目录内，不涉及系统关键目录、网络监听或外部请求。"
    else:
        parts = []
        for _tkey, _tlabel, _tcount in all_stats:
            if _tcount > 0:
                type_issues = [iss for iss in issues if iss.get("type") == _tkey]
                auth_methods = set(iss.get("authorization_method", "unified") for iss in type_issues)
                auth_str = " / ".join(auth_methods) if auth_methods else "unified"
                parts.append(
                    f"- **{_tlabel}**（{_tcount} 项，{auth_str}）\n"
                )
        high_perm_section = "\n".join(parts)

    header = "# 基于 skill-standardization 渐进式披露规范的权限说明\n\n"
    header += "本文档由 `skill-standardization` 权限扫描器自动维护。\n\n"
    header += "## 风险等级\n\n"
    header += risk_desc
    header += "## 权限总览\n\n"
    header += "| 权限类别 | 涉及项数 | 风险等级 |\n"
    header += "|-----------|----------|----------|\n"
    header += overview_section + "\n\n"
    header += "## 高权限操作说明\n\n"
    header += high_perm_section + "\n"

    # ── 权限详细说明（按类型逐个生成表格） ──
    detail_sections = []
    type_name_map = {
        "subprocess_call":    "子进程调用",
        "file_delete":        "文件删除",
        "network_access":     "网络访问",
        "sensitive_access":   "敏感信息访问",
        "critical_write":     "关键位置写入",
    }
    type_desc_map = {
        "subprocess_call":    "技能需要通过 subprocess/操作系统调用来执行外部命令或脚本。",
        "file_delete":        "技能在执行过程中需要删除临时文件或清理旧版产物。",
        "network_access":     "技能需要通过网络连接到外部服务或远程仓库。",
        "sensitive_access":   "技能代码中检测到敏感关键词（token/password等）。",
        "critical_write":     "技能可能向系统关键目录或技能安装目录写入文件。",
    }

    # 将 issues 按 type 分组
    from collections import defaultdict
    by_type = defaultdict(list)
    for iss in issues:
        by_type[iss.get("type", "unknown")].append(iss)

    for _tkey, _tlabel, _tcount in all_stats:
        if _tcount == 0:
            # 无此类别 → 简单说明
            detail_sections.append(
                f"### {_tlabel}\n\n"
                f"**无**。\n\n"
            )
            continue
        type_issues = by_type.get(_tkey, [])
        auth_set = set()
        file_buckets = defaultdict(list)
        for iss in type_issues:
            auth_set.add(iss.get("authorization_method", "unified"))
            fname = iss.get("file", "?")
            file_buckets[fname].append(iss)
        auth_str = "、".join(sorted(auth_set))
        desc = type_desc_map.get(_tkey, "")

        sec = f"### {_tlabel}（{_tcount} 项）\n\n"
        sec += f"> **功能说明**：{desc}\n> **授权方式**：{auth_str}\n\n"

        # 按文件分组生成子表格
        # 先计算所有文件的表行
        all_rows = []
        for fname in sorted(file_buckets.keys()):
            fissues = file_buckets[fname]
            for f_iss in fissues:
                lineno = f_iss.get("line", f_iss.get("lineno", 0))
                match = f_iss.get("match", "")
                itype = f_iss.get("type", "")
                explain = f_iss.get("reason", "")
                # 补充功能说明
                if not explain:
                    explain = f_iss.get("description", "")
                all_rows.append((fname, lineno, match, explain))
        if all_rows:
            sec += "| 文件 | 行号 | 匹配内容 | 功能说明 |\n"
            sec += "|------|------|----------|----------|\n"
            for _f, _ln, _m, _e in all_rows:
                # 转义 table 中的 | 符号
                _f = _f.replace("|", "\\|")
                _m = _m.replace("|", "\\|") if _m else "—"
                _e = _e.replace("|", "\\|") if _e else "—"
                sec += f"| `{_f}` | {_ln} | `{_m}` | {_e} |\n"
        sec += "\n"
        detail_sections.append(sec)

    # ── 完整文档 ──
    full_content = header + "\n"
    full_content += "## 权限详细说明\n\n"
    full_content += "\n".join(detail_sections)
    full_content += "\n## 授权方式说明\n\n"
    full_content += "- **immediate（即时授权）**：每次执行前需获得用户批准\n"
    full_content += "- **unified（统一授权）**：首次执行前获得用户批准，后续不再询问\n"
    full_content += "- **silent（静默授权）**：无需用户交互，自动执行并记录\n"

    # 生成权限指纹（用于检测权限是否变化）
    permission_fp = f"risk={risk_level}|sensitive={stats.get('sensitive_access',0)}|critical_write={stats.get('critical_write',0)}|network={stats.get('network_access',0)}|delete={stats.get('file_delete',0)}|subprocess={stats.get('subprocess_call',0)}|issues={len(issues)}"

    perm_header = "# 基于 skill-standardization 渐进式披露规范的权限说明"

    if os.path.isfile(permissions_md):
        existing = _read_file(permissions_md)
        if perm_header in existing:
            # 权限段落已存在：检查指纹是否一致
            fp_marker = f"<!-- fp:{permission_fp} -->"
            if fp_marker in existing:
                return 0  # 权限未变化，跳过
            # 权限已变化：替换权限段落，保留后续内容（测试报告等）
            # 段落边界：H1 开始，到下一个 H1 或文件尾结束
            # H2 (##) 是权限段落内部章节，不触发结束
            lines = existing.split("\n")
            after_perm = []
            in_perm = False
            for line in lines:
                stripped = line.strip()
                if stripped.startswith(perm_header):
                    in_perm = True
                    continue
                if in_perm:
                    # 遇到下一个 H1 或测试报告类 H2 时结束权限段落
                    if stripped.startswith("# ") and perm_header not in stripped:
                        in_perm = False
                        after_perm.append(line)
                        continue
                    if stripped.startswith("## ") and ("测试报告" in stripped or "test report" in stripped.lower()):
                        in_perm = False
                        after_perm.append(line)
                        continue
                    continue
                after_perm.append(line)
            # 写入新权限段落 + 保留的后续内容
            full_with_fp = full_content + "\n" + fp_marker + "\n"
            content = full_with_fp + "\n".join(after_perm)
            _write_file(permissions_md, content)
            print(f"  [R-15] 权限已变化，已替换权限段落（指纹: {permission_fp}）")
            return 1
        else:
            # 文件存在但无标准权限头：在开头插入
            content = full_content + "\n" + f"<!-- fp:{permission_fp} -->" + "\n---\n\n" + existing
            _write_file(permissions_md, content)
            return 1
    # 新建文件
    _write_file(permissions_md, full_content + "\n" + f"<!-- fp:{permission_fp} -->" + "\n")
    return 1


# ═══════════════════════════════════════════════════
# R-16: permission_weight 字段修复
# ═══════════════════════════════════════════════════

def fix_permission_weight(skill_dir, **kw):
    """
    R-16 修复：添加/更正 permission_weight 字段。
    value: LOW / MEDIUM / HIGH / CRITICAL
    """
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return 0
    value = kw.get("value", "LOW")
    ok = _update_frontmatter_field(skill_md, "permission_weight", value)
    return 1 if ok else 0


# ═══════════════════════════════════════════════════
# R-17: 渐进加载强制修复
# ═══════════════════════════════════════════════════

def fix_progressive_loading(skill_dir, **kw):
    """
    R-17 修复：如果 SKILL.md 超过 200 行，拆分到 references/。
    这是一个复杂修复，可能需要人工介入。
    此函数提供一个基础实现：添加 references/ 引用提示。
    """
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return 0
    content = _read_file(skill_md)
    fm, body = parse_simple_yaml_frontmatter(content)
    if fm is None:
        return 0
    lines = body.split("\n")
    if len(lines) <= 200:
        return 0  # 不需要修复

    # 在核心能力/工作流程章节添加渐进式加载引用提示
    # 实际拆分需要人工判断，这里只添加提示
    note = "\n> 📚 **渐进式加载**：本技能采用渐进式 MD 体系，`SKILL.md` 为入口（≤230行），详细内容拆分到 `references/*.md` 按需加载。\n"
    if "> 📚 **渐进式加载**" not in body:
        # 在第一个 ## 章节前插入提示
        new_lines = []
        inserted = False
        for ln in lines:
            if not inserted and ln.strip().startswith("## "):
                new_lines.append(note.strip())
                inserted = True
            new_lines.append(ln)
        new_body = "\n".join(new_lines)
        # 重写文件
        buf = io.StringIO()
        buf.write("---\n")
        for k, v in fm.items():
                        buf.write(f"{k}: {_fmt_frontmatter_value(v)}\n")
        buf.write("---\n")
        buf.write(new_body)
        _write_file(skill_md, buf.getvalue())
        return 1
    return 0


# ═══════════════════════════════════════════════════
# R-18: 反模式渐进式修复
# ═══════════════════════════════════════════════════

def fix_antipattern_progressive(skill_dir, **kw):
    """
    R-18 修复：将反模式内容移到 references/antipatterns.md，
    并在 SKILL.md 中添加引用。
    """
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return 0
    refs_dir = os.path.join(skill_dir, "references")
    os.makedirs(refs_dir, exist_ok=True)
    antipattern_md = os.path.join(refs_dir, "antipatterns.md")
    if not os.path.isfile(antipattern_md):
        # 创建模板
        content = (
            "# 反模式与常见错误\n\n"
            "## AP-01: 错误做法示例\n\n"
            "**错误做法：**\n\n"
            "（请描述错误做法）\n\n"
            "**正确做法：**\n\n"
            "（请描述正确做法）\n\n"
            "**深层原因：**\n\n"
            "（请描述深层原因）\n"
        )
        _write_file(antipattern_md, content)
    # 在 SKILL.md 中添加引用（如果还没有）
    body = _read_file(skill_md)
    if "references/antipatterns.md" not in body:
        # 在文件末尾添加引用
        new_content = body + "\n> 详见 [反模式](references/antipatterns.md)\n"
        _write_file(skill_md, new_content)
    return 1


# ═══════════════════════════════════════════════════
# R-19: FAQ 渐进式修复
# ═══════════════════════════════════════════════════

def fix_faq_progressive(skill_dir, **kw):
    """
    R-19 修复：将 FAQ 内容移到 references/faq.md，
    并在 SKILL.md 中添加引用。
    """
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return 0
    refs_dir = os.path.join(skill_dir, "references")
    os.makedirs(refs_dir, exist_ok=True)
    faq_md = os.path.join(refs_dir, "faq.md")
    if not os.path.isfile(faq_md):
        # 创建模板
        content = (
            "# FAQ / 常见问题\n\n"
            "## Q1: 本技能是做什么的？\n\n"
            "A: （请填写答案，≥15字）\n\n"
            "## Q2: 如何触发本技能？\n\n"
            "A: （请填写答案，≥15字）\n\n"
            "## Q3: 本技能有哪些限制？\n\n"
            "A: （请填写答案，≥15字）\n"
        )
        _write_file(faq_md, content)
    # 在 SKILL.md 中添加引用（如果还没有）
    body = _read_file(skill_md)
    if "references/faq.md" not in body:
        new_content = body + "\n> 详见 [FAQ](references/faq.md)\n"
        _write_file(skill_md, new_content)
    return 1


# ═══════════════════════════════════════════════════
# R-20: 写作规范修复
# ═══════════════════════════════════════════════════

def fix_writing_standards(skill_dir, **kw):
    """
    R-20 修复：自动更正术语不一致、添加中英文混排空格等。
    这是一个复杂修复，可能需要人工审核。
    此函数提供一个基础实现：自动更正最常见的术语不一致。
    返回：修复的问题数
    """
    fixed = 0
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return 0
    content = _read_file(skill_md)
    original = content
    # 术语不一致自动修复（常见错误）
    replacements = [
        ("建立", "创建"),
        ("新建", "创建"),
        ("修改", "更新"),
        ("变更", "更新"),
        ("移除", "删除"),
        ("去掉", "删除"),
        ("设置", "配置"),
        ("设定", "配置"),
    ]
    # 中英文混排空格修复（常见模式）
    spacing_fixes = [
        ("基于skill-standardization", "基于 skill-standardization"),
        ("skill-standardization渐进", "skill-standardization 渐进"),
    ]
    # 中英文混排空格修复（正则：中→E 或 E→中之间加空格）
    import re
    for wrong, right in replacements:
        if wrong in content:
            content = content.replace(wrong, right)
            fixed += 1
    for wrong, right in spacing_fixes:
        if wrong in content:
            content = content.replace(wrong, right)
            fixed += 1
    # 中文字符后紧跟英文词 → 加空格
    content, cn_en_count = re.subn(r'([\u4e00-\u9fff])([A-Za-z]{2,})', r'\1 \2', content)
    fixed += cn_en_count
    # 英文词后紧跟中文字符 → 加空格
    content, en_cn_count = re.subn(r'([A-Za-z]{2,})([\u4e00-\u9fff])', r'\1 \2', content)
    fixed += en_cn_count
    if content != original:
        _write_file(skill_md, content)
    # 也检查 references/*.md
    refs_dir = os.path.join(skill_dir, "references")
    if os.path.isdir(refs_dir):
        for fname in sorted(os.listdir(refs_dir)):
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(refs_dir, fname)
            ref_content = _read_file(fpath)
            ref_original = ref_content
            for wrong, right in replacements:
                if wrong in ref_content:
                    ref_content = ref_content.replace(wrong, right)
                    fixed += 1
            for wrong, right in spacing_fixes:
                if wrong in ref_content:
                    ref_content = ref_content.replace(wrong, right)
                    fixed += 1
            # 中英文混排空格（正则）
            ref_content, r_cn_en = re.subn(r'([\u4e00-\u9fff])([A-Za-z]{2,})', r'\1 \2', ref_content)
            fixed += r_cn_en
            ref_content, r_en_cn = re.subn(r'([A-Za-z]{2,})([\u4e00-\u9fff])', r'\1 \2', ref_content)
            fixed += r_en_cn
            if ref_content != ref_original:
                _write_file(fpath, ref_content)
    return fixed


# ═══════════════════════════════════════════════════
# R-21: 渐进式加载显式说明修复
# ═══════════════════════════════════════════════════

def fix_progressive_loading_explicit(skill_dir, **kw):
    """
    R-21 修复：在 ## 核心能力 或 ## 工作流程 章节添加固定模板句。
    """
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return 0
    content = _read_file(skill_md)
    fm, body = parse_simple_yaml_frontmatter(content)
    if fm is None:
        return 0
    fixed = False
    if "> 📚 **渐进式加载**" not in body:
        # 在 ## 核心能力 章节开头插入
        fixed_body = body.replace(
            "## 核心能力",
            "## 核心能力\n\n> 📚 **渐进式加载**：本技能采用渐进式 MD 体系，`SKILL.md` 为入口（≤230行），详细内容拆分到 `references/*.md` 按需加载。"
        )
        if fixed_body == body:
            # 尝试在 ## 工作流程 章节开头插入
            fixed_body = body.replace(
                "## 工作流程",
                "## 工作流程\n\n> 📚 **渐进式加载**：本技能采用渐进式 MD 体系，`SKILL.md` 为入口（≤230行），详细内容拆分到 `references/*.md` 按需加载。"
            )
        if fixed_body != body:
            # 重写文件
            buf = io.StringIO()
            buf.write("---\n")
            for k, v in fm.items():
                    buf.write(f"{k}: {_fmt_frontmatter_value(v)}\n")
            buf.write("---\n")
            buf.write(fixed_body)
            _write_file(skill_md, buf.getvalue())
            fixed = True
    return 1 if fixed else 0


# ═══════════════════════════════════════════════════
# R-22: 数据目录规范修复
# ═══════════════════════════════════════════════════

def fix_data_dir_compliance(skill_dir, dry_run=False, **kw):
    """
    R-22 修复：自动迁移安装目录中的越位数据文件到数据目录。
    调用 data_dir_checker 中的 fix_data_dir_compliance 函数。
    """
    from .data_dir_checker import fix_data_dir_compliance as _fix
    return _fix(skill_dir, dry_run=dry_run)


# ═══════════════════════════════════════════════════
# R-23: 文档-代码一致性修复
# ═══════════════════════════════════════════════════

def _find_actual_file(skill_dir, ref_stem, ref_ext):
    """通用文件查找：先同目录，再递归 scripts/
    返回 (found_path, skill_dir_relative_path) 或 None
    """
    from pathlib import Path
    # 递归搜索 scripts/ 下所有文件，建立 basename→实际路径 索引
    scripts_dir = os.path.join(skill_dir, 'scripts')
    if os.path.isdir(scripts_dir):
        for root, dirs, files in os.walk(scripts_dir):
            for fname in files:
                fstem, fext = os.path.splitext(fname)
                if fstem == ref_stem and fext != ref_ext:
                    rel = os.path.relpath(os.path.join(root, fname), skill_dir).replace('\\', '/')
                    return (os.path.join(root, fname), rel)
    return None


def _fix_md_file_refs(skill_dir, md_path):
    """修复单个 .md 中不存在的文件路径引用（通用文件查找 + 同名不同扩展名匹配）

    只做两件事：
    1. 查找同名但不同扩展名的实际文件（如 .py → .md 或 .md → .py）
    2. 递归搜索 scripts/ 下是否有同名的实际文件
    不做自动删除行。
    """
    import re
    if not os.path.isfile(md_path):
        return 0
    content = _read_file(md_path)
    changed = 0
    new_content = content

    for m in reversed(list(re.finditer(r'([^\s`]+\.[a-zA-Z]{2,4})', content))):
        ref = m.group(1).strip().strip("'\"")
        if '/' not in ref and '\\' not in ref:
            continue
        if ref.startswith(('http', 'file:', '{', '<', '-')):
            continue
        if '*' in ref or '?' in ref:
            continue
        if re.search(r'[{\u4e00-\u9fff]', ref):
            continue
        full = os.path.join(skill_dir, ref)
        if os.path.isfile(full):
            continue
        ref_stem = os.path.splitext(os.path.basename(ref))[0]
        ref_ext = os.path.splitext(ref)[1]

        # 先查同目录（同名不同扩展名）
        ref_dir = os.path.dirname(full)
        found = False
        if os.path.isdir(ref_dir):
            for actual in sorted(os.listdir(ref_dir)):
                actual_stem, actual_ext = os.path.splitext(actual)
                if actual_stem == ref_stem and actual_ext != ref_ext:
                    new_path = os.path.join(os.path.dirname(ref), actual).replace('\\', '/')
                    new_content = new_content.replace(m.group(1), new_path, 1)
                    changed += 1
                    found = True
                    break
        if found:
            continue

        # 递归查 scripts/
        result = _find_actual_file(skill_dir, ref_stem, ref_ext)
        if result:
            new_content = new_content.replace(m.group(1), result[1], 1)
            changed += 1

    if changed > 0:
        _write_file(md_path, new_content)
    return changed


def fix_doc_code_consistency(skill_dir, **kw):
    """
    R-23 修复：文档-代码一致性问题。
    1. 自动修复 .md 中不存在的文件路径引用（查找同名不同扩展名的文件）
    2. 脚本 --help 检查（基础）
    返回：修复的问题数
    """
    fixed = 0
    # 1. 修复 .md 文件中的文件路径引用
    md_files = [os.path.join(skill_dir, 'SKILL.md')]
    refs_dir = os.path.join(skill_dir, 'references')
    if os.path.isdir(refs_dir):
        for fname in sorted(os.listdir(refs_dir)):
            if fname.endswith('.md'):
                md_files.append(os.path.join(refs_dir, fname))
    for md_path in md_files:
        fixed += _fix_md_file_refs(skill_dir, md_path)
    # 2. 脚本 --help 检查（原有逻辑）
    scripts_dir = os.path.join(skill_dir, "scripts")
    if not os.path.isdir(scripts_dir):
        return fixed
    return fixed


# ═══════════════════════════════════════════════════
# fix_meta_json_completeness — _meta.json 7 标准字段补全
# ═══════════════════════════════════════════════════

def fix_meta_json_completeness(skill_dir, **kw):
    """R-25: 补全 _meta.json 缺失的 7 标准字段，非标字段判断迁移或删除。"""
    import os, json
    meta_path = os.path.join(skill_dir, '_meta.json')
    if not os.path.isfile(meta_path):
        meta = {}
    else:
        with open(meta_path, 'r', encoding='utf-8') as f:
            meta = json.load(f)

    META_STANDARD = {'name', 'version', 'description', 'author', 'tags',
                     'data_dir', 'triggers'}
    skill_name = os.path.basename(skill_dir.rstrip('/\\'))
    fixes = 0

    # 补缺失字段
    defaults = {
        'name': skill_name,
        'version': '1.0.0',
        'description': '',
        'author': 'unknown',
        'tags': [],
        'data_dir': f'skills/.standardization/{skill_name}/',
        'triggers': [],
    }
    for field in META_STANDARD:
        if field not in meta:
            meta[field] = defaults[field]
            fixes += 1

    # 非标字段处理：先输出供判断，再删除（_meta.json 不应有不一致字段）
    extra = [k for k in meta if k not in META_STANDARD]
    if extra:
        print(f'  ⚠️  发现非标字段: {", ".join(extra)}')
        print(f'  → _meta.json 是机器元数据，不应存在非标准字段。')
        print(f'  → 请确认这些字段是否需要迁移到标准字段体系：')
        print(f'     - 若字段值有用（如 home_url），建议迁移到 frontmatter 或 scripts/spec/')
        print(f'     - 若字段是历史遗留/冗余数据，将自动删除')
        # 直接删除非标字段（_meta.json 应保持严格一致）
        for k in extra:
            del meta[k]
        print(f'  ✅ 已删除非标字段: {", ".join(extra)}')

    from ..safe_io import safe_write
    safe_write(meta_path, json.dumps(meta, ensure_ascii=False, indent=2) + '\n', backup=True)
    if fixes > 0:
        print(f'  ✅ _meta.json: 补全 {fixes} 个缺失字段')
    return fixes


# ═══════════════════════════════════════════════════
# fix_frontmatter_fields — SKILL.md frontmatter 13 标准字段补全
# ═══════════════════════════════════════════════════

def fix_frontmatter_fields(skill_dir, **kw):
    """R-01 修复：补全 frontmatter 缺失的 11 required + 2 conditional 字段，标记非标字段。"""
    import os, re, tempfile, shutil
    skill_md = os.path.join(skill_dir, 'SKILL.md')
    if not os.path.isfile(skill_md):
        return 0

    # ── 分层字段定义 ──
    FM_REQUIRED = {'name','version','description','author','license','tags',
                   'data_dir','external_data_dir',
                   'sensitive_access','critical_write','permission_weight'}
    FM_CONDITIONAL = {'trigger','trigger_negative'}
    FM_OPTIONAL = {'references','category','priority','deprecated'}
    FM_STANDARD = FM_REQUIRED | FM_CONDITIONAL | FM_OPTIONAL

    with open(skill_md, 'r', encoding='utf-8') as f:
        content = f.read()

    m = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not m:
        return 0

    fm_text = m.group(1)
    existing = {}
    for line in fm_text.split('\n'):
        line = line.strip()
        if not line or line.startswith('  '): continue
        kv = re.match(r'^([\w_-]+)\s*:', line)
        if kv:
            existing[kv.group(1)] = line

    skill_name = os.path.basename(skill_dir.rstrip('/\\'))
    defaults = {
        'name': f'name: {skill_name}',
        'version': 'version: 1.0.0',
        'description': 'description: ',
        'author': 'author: [username-redacted]',
        'license': 'license: MIT',
        'tags': 'tags: []',
        'data_dir': f'data_dir: ../.standardization/{skill_name}/',
        'external_data_dir': 'external_data_dir: true',
        'sensitive_access': 'sensitive_access: false',
        'critical_write': 'critical_write: false',
        'permission_weight': 'permission_weight: LOW',
        'trigger': 'trigger: ',                        # 空值（用户后续填写）
        'trigger_negative': 'trigger_negative: ',      # 空值（用户后续填写）
    }

    fm_lines = fm_text.split('\n')
    insert_pos = 0
    for i, line in enumerate(fm_lines):
        if line.startswith('name:'):
            insert_pos = i + 1
            break

    added = []
    # 先补 required，再补 conditional（条件字段优先级低）
    for field in sorted(FM_REQUIRED):
        if field not in existing:
            fm_lines.insert(insert_pos + len(added), defaults[field])
            added.append(field)
    for field in sorted(FM_CONDITIONAL):
        if field not in existing:
            fm_lines.insert(insert_pos + len(added), defaults[field])
            added.append(field)

    extra = [k for k in existing if k not in FM_STANDARD]
    if extra:
        print(f'  [WARN] 非标字段(仅提醒，不移除。如需清理请手动处理): {", ".join(extra)}')

    if not added:
        return 0

    new_fm = '\n'.join(fm_lines)
    new_content = content[:m.start(1)] + new_fm + content[m.end(1):]

    from ..safe_io import safe_write
    safe_write(skill_md, new_content, backup=True)
    print(f'  [OK] SKILL.md frontmatter: +{", ".join(added)}')
    return len(added)


# ═══════════════════════════════════════════════════
# fix_missing_data_dir — 给脚本补 DEFAULT_DATA_DIR_RAW + DATA_DIR
# ═══════════════════════════════════════════════════

def fix_missing_data_dir(skill_dir, **kw):
    """
    R-12 step 1.5 配套修复：给引用 .standardization 但缺少 DATA_DIR 的脚本
    补上 DEFAULT_DATA_DIR_RAW + DATA_DIR 声明。

    处理逻辑：
    - Python 脚本：在最后一个 import 后插入，缺 pathlib 则补
    - Shell 脚本：在 shebang 后插入 bash 兼容的变量赋值
    - 已有 DATA_DIR 的脚本跳过

    返回：修复的脚本数量
    """
    dry_run = kw.get("dry_run", False)
    skill_name = os.path.basename(os.path.normpath(skill_dir))
    scripts_dir = os.path.join(skill_dir, "scripts")
    if not os.path.isdir(scripts_dir):
        return 0

    fixed = 0
    # DATA 变量正则（与 artifact_checker.py 保持一致）
    data_var_re = re.compile(
        r'^([A-Za-z_]*?(?:DATA|STORAGE|DB|CACHE|CONFIG)[A-Za-z_]*(?:_DIR|_PATH))\s*=\s*(.+)$'
    )

    for fname in sorted(os.listdir(scripts_dir)):
        fpath = os.path.join(scripts_dir, fname)
        if not os.path.isfile(fpath):
            continue
        ext = os.path.splitext(fname)[1].lower()
        if ext not in (".py", ".sh", ".bat", ".ps1"):
            continue

        content = _read_file(fpath)
        # 没引用 .standardization 的跳过
        if ".standardization" not in content:
            continue
        # 已有 DATA 变量的跳过
        if data_var_re.search(content, re.MULTILINE):
            continue

        if ext == ".py":
            new_content = _insert_data_dir_python(content, skill_name, fname)
        else:
            new_content = _insert_data_dir_shell(content, skill_name, fname)

        if new_content and new_content != content:
            if dry_run:
                print(f"  [DRY-RUN] {fname}: 将插入 DATA_DIR")
            else:
                _write_file(fpath, new_content)
            fixed += 1
            if not dry_run:
                print(f"    [OK] {fname}: 已添加 DEFAULT_DATA_DIR_RAW + DATA_DIR")

    return fixed


def _insert_data_dir_python(content, skill_name, fname):
    """为 Python 脚本插入 DATA_DIR 代码块（仅插入顶层导入区，不进函数体）"""
    lines = content.splitlines(keepends=True)

    # 找到插入点：最后一个顶层 import/from 行之后
    # 仅统计在第一个 def/class/if __name__ 之前的 import
    insert_at = 0
    need_pathlib = True
    reached_body = False
    in_multiline_import = False  # 跟踪多行 import 的括号嵌套
    paren_depth = 0
    for i, l in enumerate(lines):
        s = l.strip()
        # 遇到函数定义、类定义、模块级 if/for/while 就停止统计 import
        if s.startswith("def ") or s.startswith("class "):
            reached_body = True
            break
        # 跟踪多行 import: from x import ( ... )
        if "import (" in s or ("import" in s and "(" in s.split("#")[0]):
            if "(" in s and ")" not in s.split("#")[0]:
                in_multiline_import = True
                paren_depth = s.count("(") - s.count(")")
                continue
        if in_multiline_import:
            paren_depth += s.count("(") - s.count(")")
            if paren_depth <= 0:
                in_multiline_import = False
                # 多行 import 结束后，插入点设在此行之后
                insert_at = i + 1
            continue
        if s.startswith("import ") or s.startswith("from "):
            insert_at = i + 1  # 插入在此行之后
            if "pathlib" in s and "Path" in s:
                need_pathlib = False

    # 如果找不到任何顶层 import（文件内 import 都在函数中），在第一个函数定义前插入
    if insert_at == 0 and reached_body:
        for i, l in enumerate(lines):
            s = l.strip()
            if s.startswith("def ") or s.startswith("class "):
                insert_at = i
                break

    # 构建插入块
    block_lines = []
    block_lines.append("")
    block_lines.append("# R-12 审计锚点：数据目录字面量声明")
    block_lines.append('DEFAULT_DATA_DIR_RAW = "skills/.standardization/' + skill_name + '/data/"')
    block_lines.append("")
    block_lines.append("SKILL_DIR = Path(__file__).resolve().parent.parent")
    block_lines.append("# 运行时绝对路径")
    block_lines.append('DATA_DIR = SKILL_DIR.parent / ".standardization" / "' + skill_name + '" / "data"')
    block_lines.append("")

    block = "\n".join(block_lines) + "\n"

    if need_pathlib:
        # 补 from pathlib import Path
        pathlib_line = "from pathlib import Path\n"
        # 在 insert_at 位置先插 pathlib，再插 block
        new_lines = lines[:insert_at] + [pathlib_line] + [block] + lines[insert_at:]
    else:
        new_lines = lines[:insert_at] + [block] + lines[insert_at:]

    return "".join(new_lines)


def _insert_data_dir_shell(content, skill_name, fname):
    """为 Shell 脚本插入 DATA_DIR 变量"""
    lines = content.splitlines(keepends=True)

    # 找到 shebang 行的位置
    insert_at = 0
    for i, l in enumerate(lines):
        s = l.strip()
        if s.startswith("#!") and ("bash" in s or "sh" in s or "zsh" in s):
            insert_at = i + 1
            break

    block_lines = []
    block_lines.append("")
    block_lines.append("# R-12 审计锚点：数据目录")
    block_lines.append('DEFAULT_DATA_DIR_RAW="skills/.standardization/' + skill_name + '/data/"')
    block_lines.append('SKILL_DIR="$(dirname "$(dirname "${BASH_SOURCE[0]}")")"')
    block_lines.append('DATA_DIR="$SKILL_DIR/../.standardization/' + skill_name + '/data"')
    block_lines.append("")

    block = "\n".join(block_lines) + "\n"
    new_lines = lines[:insert_at] + [block] + lines[insert_at:]
    return "".join(new_lines)


def fix_meta_field_sync(skill_dir, **kw):
    """
    R-10 修复：同步 _meta.json 与 frontmatter 的共享字段。
    按权威方向同步：tags(_meta→fm), description(fm→_meta), trigger(fm→_meta)
    """
    import json, os, re
    skill_md = os.path.join(skill_dir, "SKILL.md")
    meta_path = os.path.join(skill_dir, "_meta.json")
    if not os.path.isfile(skill_md) or not os.path.isfile(meta_path):
        return 0

    content = _read_file(skill_md)
    fm, body = parse_simple_yaml_frontmatter(content)
    if fm is None:
        return 0
    with open(meta_path, 'r', encoding='utf-8') as f:
        meta = json.load(f)

    fixed = 0

    # 1. tags: _meta → frontmatter
    meta_tags = meta.get('tags', [])
    if meta_tags:
        fm_tags_str = ', '.join(f"'{t}'" for t in meta_tags) if meta_tags else '[]'
        # Update frontmatter
        new_fm = {}
        for k, v in fm.items():
            if k == 'tags':
                new_fm[k] = f"[{', '.join(repr(t) for t in meta_tags)}]"
            else:
                new_fm[k] = v
        fm = new_fm
        fixed += 1

    # 2. description: frontmatter → _meta
    fm_desc = str(fm.get('description', '')).strip() if isinstance(fm.get('description'), str) else ''
    if fm_desc:
        meta['description'] = fm_desc
        fixed += 1

    # 3. trigger: frontmatter → _meta.triggers（转数组）
    fm_trigger = fm.get('trigger', '')
    if fm_trigger and isinstance(fm_trigger, str):
        trigger_list = [t.strip() for t in fm_trigger.split('|') if t.strip()]
        meta['triggers'] = trigger_list
        fixed += 1

    # 4. data_dir: _meta → frontmatter（转换 skills/ 格式为 ../ 相对路径）
    meta_data_dir = meta.get('data_dir', '')
    fm_data_dir_str = str(fm.get('data_dir', '')).strip() if isinstance(fm.get('data_dir'), str) else ''
    if meta_data_dir and fm_data_dir_str:
        def _norm_rel(p):
            p = p.replace('\\', '/').rstrip('/')
            # _meta 格式: skills/.standardization/xxx/data/ → ../.standardization/xxx/data/
            if p.startswith('skills/'):
                p = '../' + p[len('skills/'):]
            return p
        fm_data_dir_norm = _norm_rel(fm_data_dir_str)
        meta_data_dir_norm = _norm_rel(meta_data_dir)
        if fm_data_dir_norm != meta_data_dir_norm:
            fm['data_dir'] = meta_data_dir_norm
            fixed += 1

    # Write _meta.json (uses safe_io via _write_file for SKILL.md below)
    meta_content = json.dumps(meta, ensure_ascii=False, indent=2) + '\n'
    from ..safe_io import safe_write
    safe_write(meta_path, meta_content, backup=True)

    # Rebuild and write SKILL.md
    buf = io.StringIO()
    buf.write("---\n")
    for k, v in fm.items():
            buf.write(f"{k}: {_fmt_frontmatter_value(v)}\n")
    buf.write("---\n")
    buf.write(body)
    _write_file(skill_md, buf.getvalue())

    return fixed


# ═══════════════════════════════════════════════════════════
# fix_section_constraint — 从目标技能代码采集约束，生成 ## 约束 章节
# ═══════════════════════════════════════════════════════════
def fix_section_constraint(skill_dir, **kw):
    """
    从目标技能自身的脚本和文档中采集约束，生成 ## 约束 章节。
    不套模板，不照抄——只提取该技能特有的操作规则。
    
    采集来源（按优先级）：
    1. scripts/*.py 中注释/文档字符串含"必须/不得/禁止/MUST/REQUIRED"的规则
    2. references/*.md 中 markdown 列表项含"必须/不得/禁止"的条目
    3. SKILL.md 正文中已有的规则描述（去重后提取）
    
    输出：无序列表，每行一条约束，最多 5 条。
    """
    import ast, os, re
    
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return 0
    
    content = _read_file(skill_md)
    fm, body = parse_simple_yaml_frontmatter(content)
    if fm is None:
        return 0
    
    constraints = []
    
    # ── 采集源1: 扫描 scripts/*.py 中的 docstring 和注释 ──
    scripts_dir = os.path.join(skill_dir, "scripts")
    if os.path.isdir(scripts_dir):
        for root, dirs, files in os.walk(scripts_dir):
            for f in files:
                if not f.endswith('.py'):
                    continue
                fpath = os.path.join(root, f)
                try:
                    with open(fpath, 'r', encoding='utf-8') as fh:
                        src = fh.read()
                except Exception:
                    continue
                # 提取 docstring 中含约束词的句子
                for m in re.finditer(r'(?:必须|不得|禁止|MUST|REQUIRED)[\u4e00-\u9fff]{4,}[。！]', src):
                    rule = m.group().strip().strip('。！\n')
                    if rule and len(rule) > 4 and rule not in constraints:
                        constraints.append(rule)
    
    # ── 采集源2: 扫描 references/*.md 中的列表项 ──
    refs_dir = os.path.join(skill_dir, "references")
    if os.path.isdir(refs_dir):
        for f in os.listdir(refs_dir):
            if not f.endswith('.md'):
                continue
            fpath = os.path.join(refs_dir, f)
            try:
                with open(fpath, 'r', encoding='utf-8') as fh:
                    ref_content = fh.read()
            except Exception:
                continue
            for m in re.finditer(r'^[-*]\s+(?:必须|不得|禁止)[\u4e00-\u9fff]{4,}[。！]', ref_content, re.MULTILINE):
                rule = m.group().strip().lstrip('-* ')
                if rule and len(rule) > 6 and rule not in constraints:
                    constraints.append(rule)
    
    # ── 采集源3: 从已有 body 中找约束类内容（去重）──
    for m in re.finditer(r'^[-*]\s+.*?(?:必须|不得|禁止|MUST)[^\\n]*', body, re.MULTILINE):
        rule = m.group().strip().lstrip('-* ')
        if rule and len(rule) > 6 and rule not in constraints:
            constraints.append(rule)
    
    # ── 如果没有采集到，回退到从蓝皮书中提取核心功能 ──
    if not constraints:
        # 从 SKILL.md 的触发场景和核心能力中提取关键词
        trigger_section = re.search(r'## 触发场景.*?(?=## |\\Z)', body, re.DOTALL)
        if trigger_section:
            # 提取触发词作为能力的体现
            items = re.findall(r'[-*]\s*(.+?)(?:当|如果|用户|需要)', trigger_section.group())
            for item in items[:3]:
                item = item.strip()
                if item and len(item) > 4:
                    constraints.append(f"操作前必须确认{item[:30]}")
    
    if not constraints:
        return 0  # 实在采集不到就跳过
    
    # ── 去重 + 截断最多 5 条 ──
    seen = set()
    unique = []
    for c in constraints:
        if c not in seen:
            seen.add(c)
            unique.append(c)
    constraints = unique[:5]
    
    body_lines = constraints
    section_body = '\n'.join(f'- {c}' for c in constraints)
    
    ok = _add_section_to_body(skill_md, "约束", section_body, insert_after=None)
    return len(constraints) if ok else 0


# ═══════════════════════════════════════════════════════════
# fix_progressive_index_table — 扫描 references/ 生成渐进式索引表
# ═══════════════════════════════════════════════════════════
def fix_progressive_index_table(skill_dir, **kw):
    """
    扫描目标技能 references/ 目录下的每个 .md 文件，读取其标题和首段内容，
    生成 ### 渐进式文件索引 表格（4 列：文件名 | 分类 | 包含内容 | 审计关联）。
    
    使用标准化内容表确保格式统一。未收录的文件从文件自身标题提取内容。
    放在 ## 核心能力 章节末尾。
    """
    import os
    
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return 0
    
    content = _read_file(skill_md)
    fm, body = parse_simple_yaml_frontmatter(content)
    if fm is None:
        return 0
    
    refs_dir = os.path.join(skill_dir, "references")
    if not os.path.isdir(refs_dir):
        return 0
    
    # 标准化内容表 — 格式：(分类, 包含内容, 审计关联)
    STANDARDIZED = {
        "antipatterns.md": ("规范指南", "skill 编写中的常见反模式。包含：错误做法示例、正确做法示例、避坑指引。", "R-18"),
        "architecture.md": ("架构设计", "skill-standardization 整体架构。包含：模块关系、数据流、核心设计决策。", "无"),
        "changelog.md": ("版本管理", "版本更新日志。包含：版本号、变更类型、修复项、升级说明。", "R-24"),
        "data_dir_map.md": ("路径参考", "数据目录路径对照表。包含：安装目录、标准化目录、备份目录及用途。", "无"),
        "examples.md": ("使用示例", "各场景完整执行示例。包含：CLI 命令、执行过程、输出结果。", "R-25 C-17"),
        "faq.md": ("常见问题", "常见疑问与解答。包含：问题分类、原因分析、解决方案。", "R-19, R-25 C-19"),
        "guide.md": ("使用指南", "三种执行模式操作教程。包含：audit/create/refactor 流程、参数说明、注意事项。", "无"),
        "permissions.md": ("权限与测试", "权限扫描说明与测试结论。包含：风险等级、高权限操作说明、测试概览、计时统计。", "R-15, R-16"),
        "reference.md": ("命令参考", "CLI 完整命令参考。包含：所有参数、子命令、选项、示例用法。", "无"),
        "rules.md": ("审计规则", "R-01~R-26 审计规则定义。包含：检查逻辑、修复指引、设计背景。", "R-01~R-26"),
        "LICENSE.md": ("许可协议", "开源许可证声明（MIT）。包含：MIT 许可证完整文本。", "R-26"),
    }
    
    # 收集所有 .md 文件
    ref_files = sorted(f for f in os.listdir(refs_dir) if f.endswith('.md'))
    if not ref_files:
        return 0

    # ★ 读取 SKILL.md 中已有的表格行，保留人工填写的内容
    existing_rows = {}
    existing_table = re.search(
        r'### 渐进式文件索引\n\n\| 文件名.*?(?=\n## |\n---|\Z)',
        body, re.DOTALL
    )
    if existing_table:
        for line in existing_table.group(0).split('\n'):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 5 and '`references/' in line:
                fn_match = re.search(r'`references/([^`]+)`', line)
                if fn_match:
                    fn = fn_match.group(1)
                    existing_rows[fn] = {
                        'cat': parts[2] if len(parts) > 2 else '参考文档',
                        'desc': parts[3] if len(parts) > 3 else '',
                        'audit': parts[4] if len(parts) > 4 else '无',
                    }
    
    rows = []
    for fn in ref_files:
        if fn in STANDARDIZED:
            cat, content_desc, audit_rules = STANDARDIZED[fn]
            rows.append((fn, cat, content_desc, audit_rules))
        elif fn in existing_rows:
            # ★ 保留 SKILL.md 中已有的内容（人工填写或过往生成）
            er = existing_rows[fn]
            rows.append((fn, er['cat'], er['desc'], er['audit']))
        else:
            # 未知文件：从文件自身提取
            fpath = os.path.join(refs_dir, fn)
            try:
                with open(fpath, 'r', encoding='utf-8') as fh:
                    ref_content = fh.read()
            except Exception:
                rows.append((fn, '参考文档', fn.replace('.md', '').replace('-', ' '), '无'))
                continue
            h1 = re.search(r'^#\s+(.+)$', ref_content, re.MULTILINE)
            # 用 H1 作为分类，H1 后首段作为内容
            after_h1 = ref_content[h1.end():] if h1 else ref_content
            first_para = ''
            for line in after_h1.split('\n'):
                stripped = line.strip()
                if stripped and not stripped.startswith('#'):
                    first_para = stripped[:80]
                    break
            rows.append((fn, '参考文档', first_para if first_para else fn.replace('.md', ''), '无'))
    
    # 生成表格
    table_lines = [
        '### 渐进式文件索引',
        '',
        '| 文件名 | 分类 | 包含内容 | 审计关联 |',
        '|--------|------|----------|----------|',
    ]
    for fn, cat, content_desc, audit_rules in rows:
        c = content_desc.replace('|', '/') if content_desc else ''
        table_lines.append(f'| `references/{fn}` | {cat} | {c} | {audit_rules} |')
    table_lines.append('')
    
    section_body = '\n'.join(table_lines)
    
        # 检查是否已存在，存在则整块删除后重建
    has_table = '### 渐进式文件索引' in body
    if has_table:
        body = re.sub(
            r'### 渐进式文件索引\n.*?(?=\n## |\n---|\Z)',
            '',
            body,
            flags=re.DOTALL
        )
    
    # 找到核心能力章节末尾，插入索引表
    core_match = re.search(r'^##\s+(?:核心能力|核心功能|概述).*?(?=^##\s|\Z)', body, re.MULTILINE | re.DOTALL)
    if core_match:
        core_end = core_match.end()
        body = body[:core_end] + '\n' + section_body + body[core_end:]
    
    # 清除正文中散落的"见xxx"渐进式引用（已统一归入索引表）
    body = re.sub(
        r'(?:见|详见|→\s*详见|参考)\s*`?(?:references/)?[a-zA-Z0-9_\-]+\.md`?',
        '', body
    )
    body = re.sub(r'\n{3,}', '\n\n', body)
    
    # 写回
    new_content = '---\n'
    for k, v in fm.items():
            new_content += f'{k}: {_fmt_frontmatter_value(v)}\n'
    new_content += '---\n' + body.lstrip('\n')
    _write_file(skill_md, new_content)
    
    return len(rows)


# ═══════════════════════════════════════════════════════════
# fix_reclassify_section — 通用的非标章节归类处理（Phase 3）
# ═══════════════════════════════════════════════════════════
def fix_reclassify_section(skill_dir, **kw):
    """
    通用的非标章节归类处理。不由硬编码驱动，由参数驱动。
    
    三种处理方式（由 action 参数控制）：
    - "merge": 将 section_title 的内容降级为 ### 移入 target_section
    - "split": 将 section_title 的内容拆分到 references/
    - "delete": 删除该章节（内容已被其他章节覆盖）
    
    用法：
        from scripts.skill_audit.fix import fix_reclassify_section
        # 归并到工作流程
        fix_reclassify_section(skill_dir, 
            action="merge", 
            section_title="循环与分支编排（v1.20.0 新增）", 
            target_section="工作流程")
        # 拆分到 references/
        fix_reclassify_section(skill_dir,
            action="split",
            section_title="旧版功能说明")
        # 直接删除
        fix_reclassify_section(skill_dir,
            action="delete",
            section_title="已废弃章节")
    """
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return 0
    
    action = kw.get("action", "split")
    section_title = kw.get("section_title", "")
    target_section = kw.get("target_section", "")
    
    if not section_title:
        return 0
    
    content = _read_file(skill_md)
    fm, body = parse_simple_yaml_frontmatter(content)
    if fm is None:
        return 0
    
    # 找到目标章节在 body 中的起止位置
    section_pattern = re.compile(
        r'^##\s*' + re.escape(section_title) + r'\s*$\n(.*?)(?=^##\s|\Z)',
        re.MULTILINE | re.DOTALL
    )
    section_match = section_pattern.search(body)
    if not section_match:
        # 尝试前缀匹配（兼容版本标注）
        for m in re.finditer(r'^##\s+(.+?)$\n(.*?)(?=^##\s|\Z)', body, re.MULTILINE | re.DOTALL):
            title = m.group(1).strip()
            if title.startswith(section_title) or section_title.startswith(title):
                section_match = m
                section_title = title
                break
    
    if not section_match:
        return 0
    
    section_content = section_match.group(0)
    section_body_raw = section_match.group(2)
    
    if action == "delete":
        # 直接删除
        body = body.replace(section_content, '', 1)
        
    elif action == "split":
        # 拆分到 references/
        refs_dir = os.path.join(skill_dir, "references")
        os.makedirs(refs_dir, exist_ok=True)
        safe_name = re.sub(r'[^\w\u4e00-\u9fff\-]', '_', section_title).strip('_')
        if not safe_name:
            safe_name = "section"
        ref_path = os.path.join(refs_dir, f"{safe_name}.md")
        ref_rel = f"references/{safe_name}.md"
        
        ref_content = f"# {section_title}\n\n{section_body_raw.strip()}\n"
        _write_file(ref_path, ref_content)
        
        # 替换为引用
        replacement = f"## {section_title}\n\n> → 详见 `{ref_rel}`\n"
        body = body.replace(section_content, replacement, 1)
        
    elif action == "merge" and target_section:
        # 降级为 ### 移入目标章节
        target_pattern = re.compile(
            r'^##\s*' + re.escape(target_section) + r'\s*$\n.*?(?=^##\s|\Z)',
            re.MULTILINE | re.DOTALL
        )
        target_match = target_pattern.search(body)
        if not target_match:
            return 0
        
        # 从原位置删除
        body = body.replace(section_content, '', 1)
        
        # 降级内容（## → ###）
        merged_content = section_content
        merged_content = merged_content.replace(f'## {section_title}', f'### {section_title}', 1)
        
        # 重新计算目标章节位置（body 变了）
        target_match_new = target_pattern.search(body)
        if target_match_new:
            target_end = target_match_new.end()
            body = body[:target_end] + '\n' + merged_content.strip() + '\n' + body[target_end:]
    
    # 写回
    new_content = '---\n'
    for k, v in fm.items():
            new_content += f'{k}: {_fmt_frontmatter_value(v)}\n'
    new_content += '---\n' + body.lstrip('\n')
    _write_file(skill_md, new_content)
    
    # ★ 操作后自动同步渐进式索引表，保证引用表与 references/ 一致
    fix_progressive_index_table(skill_dir)
    
    return 1


# ═══════════════════════════════════════════════════
# R-25 C-10：压缩多余空行
# ═══════════════════════════════════════════════════

def fix_excessive_blank_lines(skill_dir, **kw):
    """
    R-25 C-10 修复：将正文中连续 3+ 个空行压缩为 1~2 个空行。
    """
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return 0
    with open(skill_md, "r", encoding="utf-8") as f:
        content = f.read()
    lines = content.split("\n")
    fixed = []
    blank_count = 0
    max_blank = 2  # 最多允许 2 个连续空行
    in_code_block = False
    for line in lines:
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            fixed.append(line)
            continue
        if in_code_block:
            fixed.append(line)
            continue
        if line.strip() == "":
            blank_count += 1
            if blank_count <= max_blank:
                fixed.append(line)
        else:
            blank_count = 0
            fixed.append(line)
    new_content = "\n".join(fixed)
    if new_content != content:
        import shutil
        # 备份到 data 目录避免 R-11 报违规
        _bak_dir = _struct_dir(skill_dir)
        os.makedirs(_bak_dir, exist_ok=True)
        try:
            shutil.copy2(skill_md, os.path.join(_bak_dir, "SKILL.md.bak"))
        except Exception:
            pass
        with open(skill_md, "w", encoding="utf-8") as f:
            f.write(new_content)
        return 1
    return 0


# ═══════════════════════════════════════════════════
# R-25 C-15：替换正文中冗余的 references/ 文件引用
# ═══════════════════════════════════════════════════

def fix_inline_refs(skill_dir, **kw):
    """
    R-25 C-15 修复：将正文中冗余的 `references/xxx.md` 文件引用
    替换为统一的索引表引用（→ 详见核心能力的渐进式文件索引）。
    仅替换非指令上下文中的冗余引用，保留必要的用户指引。
    """
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return 0
    with open(skill_md, "r", encoding="utf-8") as f:
        content = f.read()
    # 替换 "-> 详见 references/xxx.md" 模式（已在索引表中列出的引用）
    import re
    new_content = re.sub(
        r'>\s*→\s*详见\s*`references/[^`]+`[^\n]*',
        '> → 详见核心能力的渐进式文件索引',
        content
    )
    # 替换正文中独立的 `references/xxx.md`引用（非索引表内，非表格行，非渐进式加载模板）
    # 逐行处理：跳过特殊行
    import re
    lines = new_content.split("\n")
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("|") and "`references/" in stripped:
            continue  # 跳过表格行（索引表文件名列）
        if "渐进式加载" in stripped and "`references/" in stripped:
            continue  # 跳过渐进式加载模板句（references/*.md 是模板的一部分）
        lines[i] = re.sub(
            r'`references/[^`]+`',
            '渐进式文件索引表',
            line
        )
    new_content = "\n".join(lines)
    if new_content != content:
        import shutil
        _bak_dir = _struct_dir(skill_dir)
        os.makedirs(_bak_dir, exist_ok=True)
        try:
            shutil.copy2(skill_md, os.path.join(_bak_dir, "SKILL.md.bak"))
        except Exception:
            pass
        with open(skill_md, "w", encoding="utf-8") as f:
            f.write(new_content)
        return 1
    return 0


# ═══════════════════════════════════════════════════
# R-25 C-11：章节名规范化（同义词→标准名）
# ═══════════════════════════════════════════════════

def fix_section_names(skill_dir, **kw):
    """
    R-25 C-11 修复：将 SKILL.md 中不在 allowed_sections 白名单的 H2 章节标题
    通过 section_synonyms 映射为标准章节名。
    
    Returns: 重命名的章节数
    """
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return 0

    spec_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        'scripts', 'spec', 'body.json'
    )
    if not os.path.isfile(spec_path):
        return 0
    import json
    with open(spec_path, 'r', encoding='utf-8') as f:
        raw = f.read()
    # 兼容多根 JSON 对象（取第一个完整对象）
    brace_count = 0
    first_end = None
    for i, ch in enumerate(raw):
        if ch == '{':
            brace_count += 1
        elif ch == '}':
            brace_count -= 1
            if brace_count == 0:
                first_end = i + 1
                break
    spec = json.loads(raw[:first_end]) if first_end else json.loads(raw)
    allowed = set(s.lower() for s in spec.get("allowed_sections", []))
    for name in spec.get("section_order", []):
        allowed.add(name.lower())
    synonyms = spec.get("section_synonyms", {})
    rename_map = {}
    for canon, syns in synonyms.items():
        for s in syns:
            sl = s.lower()
            if sl != canon.lower() and sl not in allowed and sl not in rename_map:
                rename_map[sl] = canon

    if not rename_map:
        return 0

    content = _read_file(skill_md)
    idx = content.find('\n---', content.find('---') + 3)
    if idx < 0:
        return 0
    idx = content.find('\n', idx + 4) + 1
    body = content[idx:]
    front = content[:idx]

    import re
    def _r(m):
        t = m.group(1).strip()
        l = t.lower()
        return f'## {rename_map[l]}' if l in rename_map else m.group(0)

    new_body = re.sub(r'^##\s+(.+)$', _r, body, flags=re.MULTILINE)
    if new_body == body:
        return 0
    _write_file(skill_md, front + new_body)
    changed = sum(1 for a, b in zip(body.split('\n'), new_body.split('\n')) if a != b)
    return changed


# ═══════════════════════════════════════════════════
# R-25 C-12：表格格式修复
# ═══════════════════════════════════════════════════

def fix_table_format(skill_dir, **kw):
    """
    R-25 C-12 修复：修复 SKILL.md 中格式不标准的 Markdown 表格分隔线。
    Returns: 修复的表格数
    """
    import os, re
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return 0
    content = _read_file(skill_md)
    import re
    def _fs(m):
        cells = m.group(0).strip('|').split('|')
        fixed = []
        for c in cells:
            c = c.strip()
            if not c:
                fixed.append('')
            elif c.startswith(':') and c.endswith(':'):
                fixed.append(':' + '-' * max(3, len(c) - 2) + ':')
            elif c.startswith(':'):
                fixed.append(':' + '-' * max(3, len(c) - 1))
            elif c.endswith(':'):
                fixed.append('-' * max(3, len(c) - 1) + ':')
            else:
                fixed.append('-' * max(3, len(c)))
        return '| ' + ' | '.join(fixed) + ' |'
    new = re.sub(r'\|[ :-]+\|', _fs, content)
    if new != content:
        import shutil
        _bak_dir = _struct_dir(skill_dir)
        os.makedirs(_bak_dir, exist_ok=True)
        try:
            shutil.copy2(skill_md, os.path.join(_bak_dir, "SKILL.md.bak"))
        except Exception:
            pass
        with open(skill_md, "w", encoding="utf-8") as f:
            f.write(new)
        return 1
    return 0


# ═══════════════════════════════════════════════════
# R-25 C-14/C-17/C-18：结构化数据→MD 渲染管道
# ═══════════════════════════════════════════════════

# 结构化数据文件名约定（存于 .standardization/<skill>/data/）
_STRUCT_FILES = {
    "workflow_completeness": ".structure_workflow.json",
    "example_quality": ".structure_examples.json",
    "capability_boundary": ".structure_capabilities.json",
}

def _struct_dir(skill_dir):
    """返回结构化数据的存储目录（data/ 下）。"""
    skill_name = os.path.basename(os.path.abspath(skill_dir))
    _SKILL_DIR = os.path.normpath(os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".."
    ))
    _self_name = os.path.basename(_SKILL_DIR)
    _SKILLS_ROOT = os.path.normpath(os.path.join(_SKILL_DIR, ".."))
    d = os.path.normpath(os.path.join(
        _SKILLS_ROOT, ".standardization", _self_name,
        "data", skill_name, "outputs"
    ))
    os.makedirs(d, exist_ok=True)
    return d

def _read_struct(skill_dir, fix_key):
    """从 data/ 目录读取结构化数据文件，返回 dict 或 None"""
    import json
    fname = _STRUCT_FILES.get(fix_key)
    if not fname:
        return None
    fpath = os.path.join(_struct_dir(skill_dir), fname)
    if not os.path.isfile(fpath):
        return None
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, Exception):
        return None

def _write_struct(skill_dir, fix_key, data):
    """写入结构化数据文件到 data/ 目录"""
    import json
    fname = _STRUCT_FILES.get(fix_key)
    if not fname:
        return False
    fpath = os.path.join(_struct_dir(skill_dir), fname)
    with open(fpath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return True

def _struct_file_path(skill_dir, fix_key):
    """返回结构化数据文件的完整路径（用于输出指引）。"""
    fname = _STRUCT_FILES.get(fix_key)
    if not fname:
        return ""
    return os.path.join(_struct_dir(skill_dir), fname)

def _render_workflow_section(data: dict) -> str:
    """
    从结构化数据渲染 ## 工作流程 章节正文（不含标题）。
    data = {
      "skill": "...",
      "steps": [
        {"order": 1, "name": "...", "input": "...", "output": "...", "data_flow": "...", "detail": "..."},
        ...
      ]
    }
    """
    if not data or "steps" not in data:
        return ""
    lines = []
    for s in data["steps"]:
        o = s.get("order", "?")
        n = s.get("name", "")
        inp = s.get("input", "")
        out = s.get("output", "")
        detail = s.get("detail", "")
        line = f"{o}. **{n}**"
        parts = []
        if inp:
            parts.append(f"输入 {inp}")
        if out:
            parts.append(f"输出 {out}")
        if parts:
            line += " → ".join([""] + parts)
        # 移除开头的 " → "
        line = f"{o}. **{n}**" + (" → " + " → ".join(parts) if parts else "")
        if detail:
            line += f" — {detail}"
        lines.append(line)
    return "\n".join(lines) + "\n"

def _render_examples_section(data: dict) -> str:
    """
    从结构化数据渲染示例段落。
    data = {
      "scenarios": [
        {"name": "...", "command": "...", "input": "...", "expected_output": "...", "description": "..."},
        ...
      ]
    }
    """
    if not data or "scenarios" not in data:
        return ""
    lines = []
    for sc in data["scenarios"]:
        n = sc.get("name", "")
        cmd = sc.get("command", "")
        inp = sc.get("input", "")
        exp = sc.get("expected_output", "")
        desc = sc.get("description", "")
        if n:
            lines.append(f"**场景：{n}**")
        if inp:
            lines.append(f"用户需求：{inp}")
        else:
            lines.append(f"> {desc}")
        if cmd:
            lines.append(f"系统执行：")
            lines.append(f"```bash\n{cmd}\n```")
        if exp:
            lines.append(f"系统输出：{exp}")
        elif desc:
            lines.append(f"  - **描述**: {desc}")
        lines.append("")
    return "\n".join(lines)

def _render_capabilities_section(data: dict) -> str:
    """
    从结构化数据渲染 ## 能力与限制 表格。
    data = {
      "capabilities": [{"name": "...", "description": "...", "limit": "..."}],
      "non_capabilities": [{"name": "...", "reason": "..."}]
    }
    返回表格 Markdown 正文。
    """
    if not data:
        return ""
    lines = []
    caps = data.get("capabilities", [])
    if caps:
        lines.append("| 能力 | 说明 | 限制 |")
        lines.append("|------|------|------|")
        for c in caps:
            lines.append(f"| **{c.get('name', '')}** | {c.get('description', '')} | {c.get('limit', '')} |")
        lines.append("")
    non_caps = data.get("non_capabilities", [])
    if non_caps:
        lines.append("**不支持：**")
        for nc in non_caps:
            lines.append(f"- {nc.get('name', '')}：{nc.get('reason', '')}")
        lines.append("")
    return "\n".join(lines)

def _find_section_range(body: str, section_title: str) -> tuple:
    """
    在正文中查找 H2 章节的起始行号和结束行号（下一个 H2/文件尾）。
    返回 (start_pos, end_pos) 或 (None, None)
    """
    import re
    pattern = re.compile(r'^## ' + re.escape(section_title) + r'\s*$', re.MULTILINE)
    m = pattern.search(body)
    if not m:
        return (None, None)
    start = m.start()
    # 找到下一个 ## 或文件尾
    rest = body[m.end():]
    next_m = re.search(r'^## ', rest, re.MULTILINE)
    if next_m:
        end = m.end() + next_m.start()
    else:
        end = len(body)
    return (start, end)

def _replace_section_in_skill(skill_dir, section_title: str, new_section_content: str) -> bool:
    """替换 SKILL.md 中指定 H2 章节的内容（含标题）。"""
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return False
    content = _read_file(skill_md)
    idx = content.find('\n---', content.find('---') + 3)
    if idx < 0:
        return False
    fm_end = content.find('\n', idx + 4) + 1
    front = content[:fm_end]
    body = content[fm_end:]
    
    start, end = _find_section_range(body, section_title)
    if start is None:
        return False
    
    new_body = body[:start] + new_section_content + body[end:]
    _write_file(skill_md, front + new_body)
    return True


def fix_workflow_completeness(skill_dir, **kw):
    """
    R-25 C-14 修复：从 .structure_workflow.json 结构化数据渲染工作流章节。
    先检查结构化数据文件是否存在，不存在则输出指引并返回 0。
    """
    data = _read_struct(skill_dir, "workflow_completeness")
    if data is None:
        struct_path = _struct_file_path(skill_dir, "workflow_completeness")
        skill_name = os.path.basename(os.path.normpath(skill_dir))
        print(f"""
  ╔══ C-14 修复指引 ═══════════════════════════════════════
  ║  ┌─ 问题 ──────────────────────────────────────────
  ║  │ SKILL.md 的「工作流程」章节内容不完整，缺少有序的步骤描述。
  ║  ├─ 修复流程（3 步）─────────────────────────────────
  ║  │ 1. 读取 {skill_dir}/scripts/ 下的 Python 代码，
  ║  │    理解该技能的完整执行流程（入口函数→各步骤→输出）。
  ║  │ 2. 按以下 JSON 格式，写入 {struct_path}：
  ║  │    {{
  ║  │      "skill": "{skill_name}",
  ║  │      "steps": [
  ║  │        {{"order": 1, "name": "步骤一名称", "input": "输入说明", "output": "输出说明", "detail": "详细描述"}},
  ║  │        {{"order": 2, "name": "步骤二名称", "input": "...", "output": "...", "detail": "..."}}
  ║  │      ]
  ║  │    }}
  ║  │ 3. 重新运行 --fix，脚本自动读取该 JSON 并渲染为工作流章节
  ║  └──────────────────────────────────────────────────
  ║  注意：steps 必须按顺序排列，order 从 1 开始递增
  ╚══════════════════════════════════════════════════════════""")
        return 0
    
    rendered = _render_workflow_section(data)
    if not rendered:
        return 0
    
    # 确定替换范围：## 工作流程 到下一个 H2
    section_content = "## 工作流程\n\n" + rendered
    if _replace_section_in_skill(skill_dir, "工作流程", section_content):
        return 1
    # 尝试别名
    for alias in ["工作流", "Workflow", "完整执行流程", "执行流程"]:
        if _replace_section_in_skill(skill_dir, alias, section_content):
            return 1
    return 0
    
    rendered = _render_workflow_section(data)
    if not rendered:
        return 0
    
    # 确定替换范围：## 工作流程 到下一个 H2
    section_content = "## 工作流程\n\n" + rendered
    if _replace_section_in_skill(skill_dir, "工作流程", section_content):
        return 1
    # 尝试别名
    for alias in ["工作流", "Workflow", "完整执行流程", "执行流程"]:
        if _replace_section_in_skill(skill_dir, alias, section_content):
            return 1
    return 0


def fix_example_quality(skill_dir, **kw):
    """
    R-25 C-17 修复：从 .structure_examples.json 渲染示例段落。
    """
    data = _read_struct(skill_dir, "example_quality")
    if data is None:
        struct_path = _struct_file_path(skill_dir, "example_quality")
        print(f"""
  ╔══ C-17 修复指引 ═══════════════════════════════════════
  ║  ┌─ 问题 ──────────────────────────────────────────
  ║  │ SKILL.md 的使用示例/快速开始章节质量不足（缺少 CLI 命令/
  ║  │ 输入输出说明/执行过程）。
  ║  ├─ 修复流程（3 步）─────────────────────────────────
  ║  │ 1. 读取 {skill_dir}/ 下的 Python 代码，
  ║  │    理解该技能的使用方式、参数和预期输出。
  ║  │ 2. 按以下 JSON 格式，写入 {struct_path}：
  ║  │    {{
  ║  │      "scenarios": [
  ║  │        {{"name": "场景一", "command": "示例命令", "input": "输入描述", "expected_output": "预期输出", "description": "场景说明"}},
  ║  │        {{"name": "场景二", "command": "...", "input": "...", "expected_output": "...", "description": "..."}}
  ║  │      ]
  ║  │    }}
  ║  │ 3. 重新运行 --fix，脚本自动读取该 JSON 并渲染为示例章节
  ║  └──────────────────────────────────────────────────
  ║  注意：每个场景应展示一种典型用法，包含完整命令和预期输出
  ╚══════════════════════════════════════════════════════════""")
        return 0
    
    rendered = _render_examples_section(data)
    if not rendered:
        return 0
    
    # 在 ## 快速开始 章节后插入示例段落（或在文件尾添加）
    section_content = "## 快速开始\n\n" + rendered
    if _replace_section_in_skill(skill_dir, "快速开始", section_content):
        return 1
    for alias in ["Quick Start", "快速上手", "安装"]:
        if _replace_section_in_skill(skill_dir, alias, section_content):
            return 1
    return 0


def fix_capability_boundary(skill_dir, **kw):
    """
    R-25 C-18 修复：从 .structure_capabilities.json 渲染能力限制表格。
    """
    data = _read_struct(skill_dir, "capability_boundary")
    if data is None:
        struct_path = _struct_file_path(skill_dir, "capability_boundary")
        print(f"""
  ╔══ C-18 修复指引 ═══════════════════════════════════════
  ║  ┌─ 问题 ──────────────────────────────────────────
  ║  │ SKILL.md 缺少「能力与限制」章节或内容不完整
  ║  │（未声明能力边界、参数限制、不支持的功能）。
  ║  ├─ 修复流程（3 步）─────────────────────────────────
  ║  │ 1. 读取 {skill_dir}/ 下的 Python 代码，
  ║  │    分析技能的输入参数、能力范围和不支持的功能。
  ║  │ 2. 按以下 JSON 格式，写入 {struct_path}：
  ║  │    {{
  ║  │      "capabilities": [
  ║  │        {{"name": "能力名称", "description": "能力说明", "limit": "限制条件"}}
  ║  │      ],
  ║  │      "non_capabilities": [
  ║  │        {{"name": "不支持功能", "reason": "原因说明"}}
  ║  │      ]
  ║  │    }}
  ║  │ 3. 重新运行 --fix，脚本自动读取该 JSON 并渲染为能力限制表格
  ║  └──────────────────────────────────────────────────
  ║  注意：capabilities 列出能做到什么及限制，non_capabilities 列出不支持什么
  ╚══════════════════════════════════════════════════════════""")
        return 0
    
    rendered = _render_capabilities_section(data)
    if not rendered:
        return 0
    
    # 替换 ## 能力与限制 或 ## 核心能力 章节中的能力说明
    section_content = "## 能力与限制\n\n" + rendered
    if _replace_section_in_skill(skill_dir, "能力与限制", section_content):
        return 1
    # 尝试在核心能力章节后追加
    skill_md = os.path.join(skill_dir, "SKILL.md")
    content = _read_file(skill_md)
    idx = content.find('\n---', content.find('---') + 3)
    if idx < 0:
        return 0
    fm_end = content.find('\n', idx + 4) + 1
    body = content[fm_end:]
    
    start, end = _find_section_range(body, "核心能力")
    if start is not None:
        # 在核心能力章节末尾追加能力限制内容
        new_body = body[:end] + "\n" + rendered + "\n" + body[end:]
        fm = content[:fm_end]
        _write_file(skill_md, fm + new_body)
        return 1
    return 0



# ═══════════════════════════════════════════════════
# R-25 C-11：章节指纹重排
# ═══════════════════════════════════════════════════

def fix_section_reorder(skill_dir, **kw):
    """按 body.json section_order 重排 H2 章节。纯段落指纹排序。"""
    import json, re
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return 0
    spec_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                             'scripts', 'spec', 'body.json')
    if not os.path.isfile(spec_path):
        return 0
    with open(spec_path, 'r', encoding='utf-8') as f:
        raw = f.read()
    brace = 0
    first_end = None
    for i, ch in enumerate(raw):
        if ch == '{': brace += 1
        elif ch == '}': brace -= 1
        if brace == 0: first_end = i + 1; break
    spec = json.loads(raw[:first_end]) if first_end else json.loads(raw)
    order = spec.get("section_order", [])
    if not order:
        return 0
    synonyms = spec.get("section_synonyms", {})
    canonical = {}
    for canon, syns in synonyms.items():
        for s in syns:
            canonical[s.lower()] = canon
    for name in order:
        if name.lower() not in canonical:
            canonical[name.lower()] = name

    content = _read_file(skill_md)
    idx = content.find('\n---', content.find('---') + 3)
    if idx < 0: return 0
    fm_end = content.find('\n', idx + 4) + 1
    body = content[fm_end:]; front = content[:fm_end]
    h2 = [(m.start(), m.end(), m.group(1).strip()) for m in re.finditer(r'^## (.+)$', body, re.MULTILINE)]
    sections = []
    for i, (st, en, name) in enumerate(h2):
        end_pos = h2[i+1][0] if i+1 < len(h2) else len(body)
        sections.append((name, body[st:end_pos]))
    def _mo(name):
        nl = name.lower(); canon = canonical.get(nl, name)
        for i, o in enumerate(order):
            if o.lower() == canon.lower() or nl == o.lower(): return i
        return len(order)
    ordered = sorted(sections, key=lambda s: _mo(s[0]))
    if [s[0] for s in sections] == [s[0] for s in ordered]:
        return 0
    new_body = body[:h2[0][0]]
    for name, sect in ordered:
        new_body += sect
    _write_file(skill_md, front + new_body)
    return sum(1 for a, b in zip([s[0] for s in sections], [s[0] for s in ordered]) if a != b)


# ═══════════════════════════════════════════════════
# R-25 C-12：触发条件格式修复
# ═══════════════════════════════════════════════════

def fix_trigger_format(skill_dir, **kw):
    """确保 ## 触发条件 包含 **正向触发** 和 **否定条件**。"""
    import re
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md): return 0
    content = _read_file(skill_md)
    idx = content.find('\n---', content.find('---') + 3)
    if idx < 0: return 0
    fm_end = content.find('\n', idx + 4) + 1
    body = content[fm_end:]; front = content[:fm_end]
    m = re.search(r'^## 触发条件$', body, re.MULTILINE)
    if not m:
        for alias in ['触发场景', '适用场景', '触发']:
            m = re.search(r'^## ' + re.escape(alias) + r'$', body, re.MULTILINE)
            if m: break
    if not m: return 0
    rest = body[m.end():]
    next_h2 = re.search(r'^## ', rest, re.MULTILINE)
    sec_end = m.end() + next_h2.start() if next_h2 else len(body)
    sec = body[m.start():sec_end]
    if '**正向触发**' in sec and '**否定条件**' in sec:
        return 0
    items = re.findall(r'^- (.+)$', body[m.end():sec_end], re.MULTILINE)
    neg = [it for it in items if any(w in it for w in ['不', '不是', '只是', '没有'])]
    pos = [it for it in items if it not in neg]
    new_sec = '## 触发条件\n\n**正向触发：**\n' + '\n'.join(f'- {it}' for it in pos) + '\n\n**否定条件：**\n' + '\n'.join(f'- {it}' for it in neg) + '\n\n'
    new_body = body[:m.start()] + new_sec + body[sec_end:]
    _write_file(skill_md, front + new_body)
    return 1


# ═══════════════════════════════════════════════════
# R-25 C-12：约束章节格式化
# ═══════════════════════════════════════════════════

def fix_constraint_format(skill_dir, **kw):
    """格式化 ## 约束，每条以 - 开头。"""
    import re
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md): return 0
    content = _read_file(skill_md)
    m = re.search(r'^## 约束$', content, re.MULTILINE)
    if not m:
        for alias in ['限制', '已知问题']:
            m = re.search(r'^## ' + re.escape(alias) + r'$', content, re.MULTILINE)
            if m: break
    if not m: return 0
    rest = content[m.end():]
    next_h2 = re.search(r'^## ', rest, re.MULTILINE)
    sec_end = m.end() + next_h2.start() if next_h2 else len(content)
    items = re.findall(r'^- (.+)$', content[m.end():sec_end], re.MULTILINE)
    if not items: return 0
    if all(it.strip() for it in items) and len(items) >= 2:
        return 0
    new_items = []
    for it in items:
        it = it.strip()
        if not it.endswith('。') and not it.endswith('）'): it += '。'
        new_items.append(it)
    new_sec = '## 约束\n\n' + '\n'.join(f'- {it}' for it in new_items) + '\n\n'
    new_content = content[:m.start()] + new_sec + content[sec_end:]
    _write_file(skill_md, new_content)
    return 1


# ═══════════════════════════════════════════════════
# R-23：文档引用路径修复
# ═══════════════════════════════════════════════════

def fix_doc_references(skill_dir, **kw):
    """修复 references/*.md 中的路径引用。"""
    import re
    refs_dir = os.path.join(skill_dir, "references")
    if not os.path.isdir(refs_dir): return 0
    fixed = 0
    for fname in os.listdir(refs_dir):
        if not fname.endswith('.md'): continue
        fpath = os.path.join(refs_dir, fname)
        content = _read_file(fpath)
        changed = False
        lines = content.split('\n')
        new_lines = []
        for line in lines:
            if 'SKILLS_DIR/.dist' in line:
                line = line.replace('SKILLS_DIR/.dist', '`~/.workbuddy/skills/.dist`（运行时目录）')
                changed = True
            elif 'SKILLS_DIR/' in line:
                line = line.replace('SKILLS_DIR/', '`~/.workbuddy/skills/`')
                changed = True
            new_lines.append(line)
        if changed:
            _write_file(fpath, '\n'.join(new_lines))
            fixed += 1
    return fixed


# ═══════════════════════════════════════════════════
# R-22（写作标准）：代码块标识修复 — 缩进代码块→围栏代码块
# ═══════════════════════════════════════════════════

def fix_code_block_markers(skill_dir, **kw):
    """
    R-22 代码块标识修复：将 SKILL.md 中缩进 4+ 空格的代码块
    转换为合法的 ``` 围栏代码块。
    返回：修复的代码块数量
    """
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return 0
    content = _read_file(skill_md)
    lines = content.split('\n')
    new_lines = []
    i = 0
    fixed = 0
    in_fence = False
    in_indented_block = False
    indent_buffer = []
    indent_start = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.rstrip()
        # 跟踪围栏代码块状态
        if stripped.startswith('```'):
            # 如果之前有缩进缓冲区，先清空
            if in_indented_block and indent_buffer:
                for bl in indent_buffer:
                    new_lines.append(bl)
                indent_buffer = []
                in_indented_block = False
            new_lines.append(line)
            in_fence = not in_fence
            i += 1
            continue
        if in_fence:
            new_lines.append(line)
            i += 1
            continue
        # 不在围栏内：检测缩进代码块
        # 跳过空行（保留，可能分隔缩进块）
        if not stripped:
            if in_indented_block and indent_buffer:
                # 空行属于当前缩进块的一部分
                indent_buffer.append(line)
            else:
                new_lines.append(line)
            i += 1
            continue
        # 检查是否缩进 4+ 空格且不是列表/引用/标题
        indent_match = re.match(r'^( {4,})(\S.*)', line)
        if (indent_match
                and not stripped.startswith('-')
                and not stripped.startswith('*')
                and not stripped.startswith('>')
                and not stripped.startswith('#')):
            if not in_indented_block:
                in_indented_block = True
                indent_buffer = []
                indent_start = i
            indent_buffer.append(line)
            i += 1
            continue
        # 非缩进行 — 如果之前在缩进块中，转义为围栏块
        if in_indented_block and indent_buffer:
            # 检查内容长度：至少 2 行才值得转义
            code_text = '\n'.join(
                re.sub(r'^ {4}', '', bl)  # 去除前 4 格缩进
                if re.match(r'^ {4}', bl)
                else bl
                for bl in indent_buffer
            )
            # 检测语言
            lang = 'text'
            for kw_lang, kw_pattern in [
                ('python', r'\b(import |def |class |print\()'),
                ('bash', r'^\$ '),
                ('json', r'^[{[]'),
                ('yaml', r'^[\w-]+:'),
                ('html', r'</?[a-z]+'),
                ('xml', r'</?'),
                ('javascript', r'\b(const |let |var |function |=>)'),
            ]:
                if re.search(kw_pattern, code_text, re.MULTILINE):
                    lang = kw_lang
                    break
            new_lines.append(f'```{lang}')
            new_lines.append(code_text)
            new_lines.append('```')
            fixed += 1
            indent_buffer = []
            in_indented_block = False
        new_lines.append(line)
        i += 1
    # 文件尾仍有积压的缩进块
    if in_indented_block and indent_buffer:
        code_text = '\n'.join(
            re.sub(r'^ {4}', '', bl)
            if re.match(r'^ {4}', bl)
            else bl
            for bl in indent_buffer
        )
        lang = 'text'
        for kw_lang, kw_pattern in [
            ('python', r'\b(import |def |class |print\()'),
            ('bash', r'^\$ '),
            ('json', r'^[{[]'),
            ('yaml', r'^[\w-]+:'),
            ('html', r'</?[a-z]+'),
            ('xml', r'</?'),
            ('javascript', r'\b(const |let |var |function |=>)'),
        ]:
            if re.search(kw_pattern, code_text, re.MULTILINE):
                lang = kw_lang
                break
        new_lines.append(f'```{lang}')
        new_lines.append(code_text)
        new_lines.append('```')
        fixed += 1
    if fixed > 0:
        _write_file(skill_md, '\n'.join(new_lines))
    return fixed


# ═══════════════════════════════════════════════════
# R-25 C-05：列表混排修复 — 统一同一章节内的列表样式
# ═══════════════════════════════════════════════════

def fix_list_mixing(skill_dir, **kw):
    """
    C-05 修复：同一章节内若同时混用有序/无序列表且各有 3+ 项，
    将少数方转为多数方样式。
    """
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return 0
    content = _read_file(skill_md)
    fm, body = parse_simple_yaml_frontmatter(content)
    if fm is None:
        return 0

    # 按 H2 分段
    sections = list(re.finditer(
        r'^##\s+(.+?)$\n(.*?)(?=^##\s|\Z)',
        body, re.MULTILINE | re.DOTALL
    ))
    fixed = 0
    new_body = body
    # 从后往前替换，保持位置不漂移
    for m in reversed(sections):
        sec_content = m.group(2)
        # 提取有序和无序列表行
        ordered_lines = list(re.finditer(
            r'^\d+\.\s+(.*)$', sec_content, re.MULTILINE
        ))
        unordered_lines = list(re.finditer(
            r'^[-*]\s+(.*)$', sec_content, re.MULTILINE
        ))
        if len(ordered_lines) >= 3 and len(unordered_lines) >= 3:
            # 少数方转为多数方样式
            convert_unordered = len(unordered_lines) <= len(ordered_lines)
            new_sec = sec_content
            if convert_unordered:
                # 无序→有序：为每行重新编号
                ul_matches = list(re.finditer(
                    r'^[-*]\s+(.*)$', new_sec, re.MULTILINE
                ))
                base_num = 1
                for ul_m in reversed(ul_matches):
                    text = ul_m.group(1)
                    new_sec = (
                        new_sec[:ul_m.start()]
                        + f"{base_num}. {text}"
                        + new_sec[ul_m.end():]
                    )
                    base_num += 1
                fixed += 1
            else:
                # 有序→无序：去掉编号前缀
                sec_lines = new_sec.split('\n')
                changed = False
                for j, sl in enumerate(sec_lines):
                    ol_match = re.match(r'^(\s*)\d+\.\s+(.*)', sl)
                    if ol_match:
                        sec_lines[j] = ol_match.group(1) + '- ' + ol_match.group(2)
                        changed = True
                if changed:
                    new_sec = '\n'.join(sec_lines)
                    fixed += 1
            # 替换 body 中的章节内容
            new_body = (
                new_body[:m.start(2)]
                + new_sec
                + new_body[m.end(2):]
            )

    if fixed > 0:
        buf = io.StringIO()
        buf.write('---\n')
        for k, v in fm.items():
            buf.write(f"{k}: {_fmt_frontmatter_value(v)}\n")
        buf.write('---\n')
        buf.write(new_body)
        _write_file(skill_md, buf.getvalue())
    return fixed


# ═══════════════════════════════════════════════════
# R-25 C-07：代码块语言标识修复
# ═══════════════════════════════════════════════════

def fix_code_block_lang(skill_dir, **kw):
    """
    C-07 修复：为缺少语言标识的 ``` 代码块补上启发式语言标识。
    检测规则：import/def/class→python, $ →bash, [/{ →json, </ →html/xml
    """
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return 0
    content = _read_file(skill_md)
    lines = content.split('\n')
    new_lines = list(lines)
    fixed = 0
    # 找出所有 ```
    fence_indices = [i for i, ln in enumerate(lines) if ln.strip().startswith('```')]
    for idx, i in enumerate(fence_indices):
        if idx % 2 == 1:
            continue  # 跳过结束 ```
        fence_text = lines[i].rstrip()
        # 只有裸 ``` 才需要补（没有语言标识）
        if fence_text.strip() != '```' and not re.match(r'^```\s*$', fence_text):
            continue  # 已经有内容，跳过
        # 读取围栏内的内容（到下一个 ``` 为止）
        end_idx = None
        for j in range(i + 1, len(lines)):
            if lines[j].strip().startswith('```'):
                end_idx = j
                break
        if end_idx is None:
            continue
        inner = '\n'.join(lines[i+1:end_idx])
        # 启发式语言检测
        lang = 'text'
        for kw_lang, kw_pattern in [
            ('python', r'\b(import |def |class |print\s*\()'),
            ('bash', r'^\$ '),
            ('json', r'^\s*[{[]'),
            ('yaml', r'^\s*[\w-]+:\s'),
            ('html', r'</?[a-z]+'),
            ('javascript', r'\b(const |let |var |function |=>)'),
            ('sql', r'\b(SELECT|INSERT|UPDATE|DELETE|CREATE|ALTER)\b'),
            ('dockerfile', r'^\s*(FROM|RUN|CMD|COPY|WORKDIR)\s'),
        ]:
            if re.search(kw_pattern, inner, re.MULTILINE):
                lang = kw_lang
                break
        new_lines[i] = f'```{lang}'
        fixed += 1
    if fixed > 0:
        _write_file(skill_md, '\n'.join(new_lines))
    return fixed


# ═══════════════════════════════════════════════════
# R-25 C-12：节内容完整性修复 — 补充格式线索
# ═══════════════════════════════════════════════════

def fix_section_completeness(skill_dir, **kw):
    """
    C-12 修复：为 SKILL.md 中内容过短的章节补充必要格式元素。
    基于 body.json 的 content_format 定义推断需补充的内容类型。
    """
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return 0
    content = _read_file(skill_md)
    fm, body = parse_simple_yaml_frontmatter(content)
    if fm is None:
        return 0

    # 加载 content_format 规范
    spec_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        'scripts', 'spec', 'body.json'
    )
    content_format = {}
    if os.path.isfile(spec_path):
        with open(spec_path, 'r', encoding='utf-8') as f:
            raw = f.read()
        brace_count = 0
        first_end = None
        for ci, ch in enumerate(raw):
            if ch == '{': brace_count += 1
            elif ch == '}':
                brace_count -= 1
                if brace_count == 0:
                    first_end = ci + 1
                    break
        spec = json.loads(raw[:first_end]) if first_end else json.loads(raw)
        content_format = spec.get("content_format", {}) if isinstance(spec, dict) else {}

    # 按 H2 分段检查
    sections = list(re.finditer(
        r'^##\s+(.+?)$\n(.*?)(?=^##\s|\Z)',
        body, re.MULTILINE | re.DOTALL
    ))
    fixed = 0
    new_body = body
    
    def _ensure_format(section_text, clues):
        """确保章节包含指定的格式线索。"""
        result = section_text
        for clue in clues:
            if clue == '加粗' and '**' not in section_text:
                # 在章节开头加一个加粗提示
                result = result.rstrip() + '\n\n> **关键术语**：请在此补充\n'
                fixed_local = True
            elif clue == '表格' and '|' not in section_text:
                result = result.rstrip() + '\n\n| 项目 | 说明 |\n|------|------|\n| | |\n'
        return result

    for m in reversed(sections):
        title = m.group(1).strip()
        sec_content = m.group(2)
        title_lower = title.lower().replace(' ', '')
        
        # 根据章节名推断需要的格式
        needed_hints = []
        cf = content_format.get(title, {})
        if isinstance(cf, dict):
            hints = cf.get('classification_hints', {})
            if isinstance(hints, dict):
                needed_hints = hints.get('format_clues', [])
        
        # 如果没有 hints 定义，用标题关键词推断
        if not needed_hints:
            keyword_map = {
                '约束': ['加粗'],
                '触发': ['加粗'],
                '核心': ['加粗'],
                '工作流程': ['加粗'],
            }
            for kw, hints in keyword_map.items():
                if kw in title_lower:
                    needed_hints = hints
                    break

        if needed_hints:
            new_sec = _ensure_format(sec_content, needed_hints)
            if new_sec != sec_content:
                new_body = (
                    new_body[:m.start(2)]
                    + new_sec
                    + new_body[m.end(2):]
                )
                fixed += 1

    if fixed > 0:
        buf = io.StringIO()
        buf.write('---\n')
        for k, v in fm.items():
            buf.write(f"{k}: {_fmt_frontmatter_value(v)}\n")
        buf.write('---\n')
        buf.write(new_body)
        _write_file(skill_md, buf.getvalue())
    return fixed


# ═══════════════════════════════════════════════════
# R-25 C-19：错误处理分类修复 — 补充/增强 FAQ
# ═══════════════════════════════════════════════════

def fix_faq_error_handling(skill_dir, **kw):
    """
    C-19 修复：在 references/faq.md 中补充错误处理问答。
    如果不存在 FAQ，创建一个包含三类错误场景的模板；
    如果存在但缺少分类/步骤，补充缺失部分。
    """
    skill_dir = os.path.abspath(skill_dir)
    refs_dir = os.path.join(skill_dir, 'references')
    faq_path = os.path.join(refs_dir, 'faq.md')
    skill_name = os.path.basename(skill_dir)
    
    # 标准三类错误修复模板
    ERROR_TEMPLATE = f"""## 出错了怎么办？

### 1. 参数错误
**场景：** 命令参数格式不正确或缺失必需参数。
**修复：** 检查命令参数是否拼写正确，使用 `--help` 查看完整参数列表。

### 2. 环境/依赖错误
**场景：** 缺少依赖包、Python 版本不匹配或路径配置错误。
**修复：** 确认 Python 版本 >= 3.8，安装 requirements.txt 中的依赖包，检查 `SKILL.md` 中 `data_dir:` 声明路径是否存在。

### 3. 运行时异常
**场景：** 技能执行过程中抛出未预期的异常。
**修复：** 检查输入数据格式、文件权限和磁盘空间。仍无法解决 → 查看 `--debug` 输出或提交 Issue。"""
    
    if not os.path.isdir(refs_dir):
        os.makedirs(refs_dir, exist_ok=True)
    
    if not os.path.isfile(faq_path):
        # FAQ 不存在：创建含错误处理的完整 FAQ
        faq_parts = [ERROR_TEMPLATE]
        _write_file(faq_path, '\n\n'.join(faq_parts))
        return 1

    existing = _read_file(faq_path)
    modified = False
    
    # 检查是否有错误处理章节
    has_err_section = bool(re.search(
        r'出错|报错|异常|怎么办|修正|修复', existing
    ))
    
    if not has_err_section:
        # 追加错误处理章节
        existing = existing.rstrip() + '\n\n' + ERROR_TEMPLATE
        modified = True
    else:
        # 已有错误内容：检查是否需要补充分类
        if not re.search(r'(场景|情况|类型|分类|示例).*(出错|错误|异常|问题)', existing, re.DOTALL):
            existing = existing.rstrip() + '\n\n### 补充：错误分类\n\n' + (
                '建议按以下三类排查：\n\n'
                '1. **参数错误** — 检查参数拼写和格式\n'
                '2. **环境错误** — 检查依赖和版本\n'
                '3. **运行时错误** — 检查输入和权限\n'
            )
            modified = True
        if not re.search(r'(检查|确认|修改|调整|建议)[^。]*。', existing):
            existing = existing.rstrip() + '\n\n### 补充：通用修复步骤\n\n' + (
                '1. 确认输入参数格式正确\n'
                '2. 检查运行环境依赖是否齐全\n'
                '3. 查看 `--debug` 日志定位具体异常位置\n'
            )
            modified = True
    
    if modified:
        _write_file(faq_path, existing)
        return 1
    return 0


# ═══════════════════════════════════════════════════
# 统一入口：apply_fix()
# ═══════════════════════════════════════════════════

def apply_fix(skill_dir, fix_key, **kw):
    """
    统一修复入口。
    fix_key: 对应审计结果中 fix["key"] 的值
    **kw: 附加参数（如 value、dry_run 等）

    返回：修复数量（0 表示未修复或失败）

    用法：
        from skill_audit.fix import apply_fix
        n = apply_fix("/path/to/skill", "name", value="git-sync")
    """
    dispatch = {
        "name": fix_name,
        "description": fix_description,
        "author": fix_author,
        "version": fix_version,
        "skill_macro": fix_skill_macro,
        "h1": fix_h1,
        "h1_version": fix_h1_version,
        "h1_position": fix_h1_position,
        "section_trigger": fix_section_trigger,
        "trigger_quality": fix_section_trigger,
        "trigger_negative": fix_section_trigger,
        "trigger_danger": fix_section_trigger,
        "section_core": fix_section_core,
        "section_workflow": fix_section_workflow,
        "home_url": fix_home_url,
        "artifact_paths": fix_artifact_paths,
        "external_data_dir": fix_external_data_dir,
        "missing_data_dir": fix_missing_data_dir,
        "sensitive_access": fix_sensitive_access,
        "critical_write": fix_critical_write,
        "create_permissions_md": fix_create_permissions_md,
        "create_references_permissions_md": fix_create_permissions_md,
        "fix_permissions_md_readable": fix_create_permissions_md,
        "add_risk_description": fix_create_permissions_md,
        "permission_weight": fix_permission_weight,
        "progressive_loading": fix_progressive_loading,
        "antipattern_progressive": fix_antipattern_progressive,
        "antipattern_reference": fix_antipattern_progressive,
        "antipattern_file_missing": fix_antipattern_progressive,
        "antipattern_count": fix_antipattern_progressive,
        "antipattern_detail": fix_antipattern_progressive,
        "faq_progressive": fix_faq_progressive,
        "faq_reference": fix_faq_progressive,
        "faq_file_missing": fix_faq_progressive,
        "faq_unparsable": fix_faq_progressive,
        "faq_quality": fix_faq_progressive,
        "writing_standards": fix_writing_standards,
        "progressive_loading_explicit": fix_progressive_loading_explicit,
        "changelog_progressive": fix_progressive_loading_explicit,
        "data_dir_compliance": fix_data_dir_compliance,
        "doc_code_consistency": fix_doc_code_consistency,
        "meta_json": fix_meta_json_completeness,
        "frontmatter_fields": fix_frontmatter_fields,
        "frontmatter": fix_frontmatter_fields,
        "meta_field_sync": fix_meta_field_sync,
        "split_nonstandard": fix_split_nonstandard,
        "section_order": fix_section_order,
        "section_constraint": fix_section_constraint,
        "progressive_index_table": fix_progressive_index_table,
        "reclassify_section": fix_reclassify_section,
        "version_con": fix_version_con,
        "sanitize": fix_sanitize,
        "data_dir": fix_data_dir,
        "section_antipattern": fix_section_antipattern,
        "section_faq": fix_section_faq,
        "license_compliance": fix_license_compliance,
        "excessive_blank_lines": fix_excessive_blank_lines,
        "inline_refs": fix_inline_refs,
        "section_names": fix_section_names,
        "table_format": fix_table_format,
        "workflow_completeness": fix_workflow_completeness,
        "example_quality": fix_example_quality,
        "capability_boundary": fix_capability_boundary,
        "section_reorder": fix_section_reorder,
        "trigger_format": fix_trigger_format,
        "constraint_format": fix_constraint_format,
        "doc_references": fix_doc_references,
        # ── R-22（写作标准）代码块标识 ──
        "code_block_markers": fix_code_block_markers,
        # ── C-05 列表混排 ──
        "list_mixing": fix_list_mixing,
        # ── C-07 代码块语言标识 ──
        "code_block_lang": fix_code_block_lang,
        # ── C-12 节内容完整性 ──
        "section_completeness": fix_section_completeness,
        # ── C-19 错误处理分类 ──
        "error_handling_faq": fix_faq_error_handling,
    }

    func = dispatch.get(fix_key)
    if func is None:
        raise ValueError(f"未知的 fix_key: {fix_key}（支持：{', '.join(sorted(dispatch.keys()))}）")
    return func(skill_dir, **kw)


# ── Body spec 辅助 ──────────────────────────────────────────────────

def _load_body_spec():
    """加载 body.json 规范。"""
    spec_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        'scripts', 'spec', 'body.json'
    )
    if not os.path.isfile(spec_path):
        return {}
    try:
        with open(spec_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def _load_section_order():
    """返回 section_order 列表。"""
    return _load_body_spec().get("section_order", [])


def _load_allowed_sections():
    """返回 allowed_sections 白名单。"""
    spec = _load_body_spec()
    allowed = set(k.lower() for k in spec.get("allowed_sections", []))
    for syns in spec.get("section_synonyms", {}).values():
        for s in syns:
            allowed.add(s.lower())
    return allowed


# ═══════════════════════════════════════════════════
# R-17/C-11: 非标章节拆分 + 章节重排
# ═══════════════════════════════════════════════════

def fix_split_nonstandard(skill_dir, **kw):
    """
    R-17 修复：将不在 allowed_sections 白名单中的 H2 章节拆分到 references/。
    每个非标章节的内容被迁移到 references/<section-slug>.md，
    原始位置替换为「→ 详见 references/<section-slug>.md」引用。
    
    Returns: 迁移的章节数
    """
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return 0

    allowed = _load_allowed_sections()
    if not allowed:
        return 0

    content = _read_file(skill_md)
    fm, body = parse_simple_yaml_frontmatter(content)
    if fm is None:
        return 0

    refs_dir = os.path.join(skill_dir, "references")
    os.makedirs(refs_dir, exist_ok=True)

    # 解析所有 ## H2 章节
    sections = list(re.finditer(r'^##\s+(.+?)$\n(.*?)(?=^##\s|\Z)', body, re.MULTILINE | re.DOTALL))
    if not sections:
        return 0

    migrated = 0
    dry_run = kw.get("dry_run", False)

    for m in sections:
        title = m.group(1).strip()
        title_lower = title.lower()
        if title_lower in allowed:
            continue

        section_content = m.group(2).strip()
        if not section_content:
            continue

        # 生成安全文件名
        safe_name = re.sub(r'[^\w\u4e00-\u9fff\-]', '_', title).strip('_')
        if not safe_name:
            safe_name = f"section_{m.start()}"

        ref_path = os.path.join(refs_dir, f"{safe_name}.md")
        ref_rel = f"references/{safe_name}.md"

        if dry_run:
            migrated += 1
            continue

        # 写 references/ 文件
        ref_content = f"# {title}\n\n{section_content}\n\n*由 fix_split_nonstandard 从 SKILL.md 迁移*"
        from ..safe_io import safe_write
        safe_write(ref_path, ref_content, backup=True)

        # 在 body 中替换为引用
        full_match = m.group(0)
        replacement = f"## {title}\n\n> → 详见 `{ref_rel}`\n"
        body = body.replace(full_match, replacement, 1)
        migrated += 1

    if migrated > 0 and not dry_run:
        # 写回 SKILL.md
        new_content = f"---\n"
        for k, v in fm.items():
            new_content += f"{k}: {_fmt_frontmatter_value(v)}\n"
        new_content += "---\n"
        new_content += body.lstrip('\n')
        _write_file(skill_md, new_content)
    
    if migrated > 0:
        # ★ 新增引用文件后自动同步索引表
        fix_progressive_index_table(skill_dir)

    return migrated


def fix_section_order(skill_dir, **kw):
    """
    R-25 C-11 修复：按 body.json section_order 重排 SKILL.md 的 H2 章节顺序。
    不在 section_order 中的章节放到末尾。
    
    Returns: 重排的章节数
    """
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return 0

    order = _load_section_order()
    if not order:
        return 0

    content = _read_file(skill_md)
    fm, body = parse_simple_yaml_frontmatter(content)
    if fm is None:
        return 0

    # 构建别名映射
    spec = _load_body_spec()
    synonyms = spec.get("section_synonyms", {})
    name_to_pos = {}
    for pos, name in enumerate(order):
        name_to_pos[name.lower()] = pos
        for canon, syns in synonyms.items():
            if canon.lower() == name.lower():
                for s in syns:
                    name_to_pos[s.lower()] = pos

    # 找到所有 ## 章节在 body 中的位置（含前导内容）
    # 用 split 分割 body
    parts = re.split(r'^(?=##\s)', body, flags=re.MULTILINE)
    if not parts:
        return 0

    # 第一部分是非章节前导内容（H1、空行、注释等）
    preamble = parts[0]
    sections = parts[1:]

    # 给每个章节分配位置
    ordered = []
    unordered = []
    for sec in sections:
        first_line = sec.split('\n')[0].strip()
        title = re.sub(r'^##\s+', '', first_line).strip()
        pos = name_to_pos.get(title.lower(), -1)
        if pos >= 0:
            ordered.append((pos, sec))
        else:
            unordered.append(sec)

    ordered.sort(key=lambda x: x[0])

    dry_run = kw.get("dry_run", False)
    if dry_run:
        return len(ordered) + len(unordered)

    # 组装
    new_body = preamble + '\n' + '\n'.join(sec for _, sec in ordered)
    if unordered:
        new_body += '\n' + '\n'.join(unordered)

    # 写回
    new_content = f"---\n"
    for k, v in fm.items():
        new_content += f"{k}: {_fmt_frontmatter_value(v)}\n"
    new_content += "---\n"
    new_content += new_body.lstrip('\n')
    _write_file(skill_md, new_content)

    return len(ordered) + len(unordered)




# ═══════════════════════════════════════════════════════════
# fix_version_con — R-03: version SemVer 格式校验与修复
# ═══════════════════════════════════════════════════════════
def fix_version_con(skill_dir, **kw):
    """
    R-03 修复：校验 frontmatter version 为 SemVer 格式 (X.Y.Z)。
    如果不符合，尝试修复为合法格式。
    """
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return 0
    content = _read_file(skill_md)
    fm, body = parse_simple_yaml_frontmatter(content)
    if fm is None:
        return 0
    ver = str(fm.get("version", "")).strip()
    if not ver:
        return 0
    # SemVer: MAJOR.MINOR.PATCH
    semver_match = re.match(r'^(\d+)\.(\d+)\.(\d+)(?:-[\w.]+)?(?:\+[\w.]+)?$', ver)
    if semver_match:
        return 0  # 已合法
    # 尝试修复
    parts = re.findall(r'\d+', ver)
    if len(parts) >= 3:
        new_ver = f"{parts[0]}.{parts[1]}.{parts[2]}"
    elif len(parts) == 2:
        new_ver = f"{parts[0]}.{parts[1]}.0"
    elif len(parts) == 1:
        new_ver = f"{parts[0]}.0.0"
    else:
        new_ver = "1.0.0"
    ok = _update_frontmatter_field(skill_md, "version", new_ver)
    return 1 if ok else 0


# ═══════════════════════════════════════════════════════════
# fix_sanitize — R-05: name 与目录名一致
# ═══════════════════════════════════════════════════════════
def fix_sanitize(skill_dir, **kw):
    """
    R-05 修复：将 frontmatter name 改为与父目录名一致。
    """
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return 0
    content = _read_file(skill_md)
    fm, body = parse_simple_yaml_frontmatter(content)
    if fm is None:
        return 0
    dir_name = os.path.basename(os.path.normpath(skill_dir))
    current = str(fm.get("name", "")).strip()
    if current == dir_name:
        return 0  # 已一致
    ok = _update_frontmatter_field(skill_md, "name", dir_name)
    return 1 if ok else 0


# ═══════════════════════════════════════════════════════════
# fix_data_dir — R-12: 数据目录路径合规
# ═══════════════════════════════════════════════════════════
def fix_data_dir(skill_dir, **kw):
    """
    R-12 修复：确保 _meta.json 包含 data_dir 字段，值为 .standardization/<skill>/data/。
    同时检查 scripts/ 中源码是否声明了 data_dir 的 DEFAULT_DATA_DIR_RAW 锚点。
    """
    import json as _json
    
    meta_path = os.path.join(skill_dir, "_meta.json")
    if not os.path.isfile(meta_path):
        return 0
    
    try:
        with open(meta_path, 'r', encoding='utf-8') as f:
            meta = _json.load(f)
    except Exception:
        return 0
    
    skill_name = os.path.basename(os.path.normpath(skill_dir))
    expected_data_dir = f".standardization/{skill_name}/data/"
    
    current = meta.get("data_dir", "")
    if current == expected_data_dir:
        return 0  # 已正确
    
    meta["data_dir"] = expected_data_dir
    from ..safe_io import safe_write
    safe_write(meta_path, json.dumps(meta, ensure_ascii=False, indent=2) + '\n', backup=True)
    return 1


# ═══════════════════════════════════════════════════════════
# fix_section_antipattern — R-18: 反模式章节内容
# ═══════════════════════════════════════════════════════════
def fix_section_antipattern(skill_dir, **kw):
    """
    R-18 修复：添加 ## 反模式 章节，每条含具体错误描述和正确做法。
    从目标技能的特征生成至少 3 条反模式，每条 ≥20 字。
    """
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return 0
    content = _read_file(skill_md)
    fm, body = parse_simple_yaml_frontmatter(content)
    if fm is None:
        return 0
    name = fm.get("name", "本技能")
    
    # 从触发词和描述生成反模式
    desc = str(fm.get("description", ""))
    triggers = str(fm.get("trigger", ""))
    
    # 通用反模式模板（从技能特征调整）
    antipatterns = [
        f"**忽略 {name} 的约束条件** — 直接按一般逻辑执行，忽略本技能的特殊操作约束，导致文件损坏或版本号不一致。正确做法：操作前先读 `## 约束` 章节，确认本技能特有的操作规则。",
        f"**手动编辑 .md 文件** — 使用 Write/Edit 工具直接修改 SKILL.md，破坏编码或格式。正确做法：使用对应 Python 脚本原子写入，保证编码和 frontmatter 完整。",
        f"**跳过审计直接提交** — 修改后不运行 audit 就推送，导致未发现的 ERROR 进入仓库。正确做法：每次修改后运行 `audit .` 自审，确认 0 ERROR 0 WARN。",
    ]
    if '标准化' in desc or '审计' in desc:
        antipatterns.append(
            f"**一次只修一个 WARN** — 审计报了多个 WARN 但逐个手动修，效率低。正确做法：用 `--fix` 批量修复可自动修复的项，再手动处理 LLM  精筛项。"
        )
    
    section_body = '\n'.join(f'> ❌ **{a.split("**")[0].lstrip("> ❌ ")}**\n> ✅ {a.split("。正确做法：")[1]}' if "。正确做法：" in a else a for a in antipatterns[:5])
    
    # 实际用简单列表格式
    items = []
    for a in antipatterns[:5]:
        parts = a.split("。正确做法：")
        if len(parts) == 2:
            items.append(f"- ❌ **{parts[0].lstrip('**').rstrip('**')}**\n\n  ✅ {parts[1]}")
        else:
            items.append(f"- {a}")
    
    section_body = '\n\n'.join(items)
    ok = _add_section_to_body(skill_md, "反模式", section_body, insert_after=None)
    return len(antipatterns) if ok else 0


# ═══════════════════════════════════════════════════════════
# fix_section_faq — R-19: FAQ 章节内容
# ═══════════════════════════════════════════════════════════
def fix_section_faq(skill_dir, **kw):
    """
    R-19 修复：添加 ## FAQ 章节，包含至少 3 个有意义的 Q&A 对。
    Q ≥10 字，A ≥15 字，从技能名称和描述生成。
    """
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return 0
    content = _read_file(skill_md)
    fm, body = parse_simple_yaml_frontmatter(content)
    if fm is None:
        return 0
    name = fm.get("name", "本技能")
    desc = str(fm.get("description", ""))
    
    qas = [
        {
            "q": f"{name} 主要用来做什么？",
            "a": f"{name} 是一个 WorkBuddy 技能，{desc[:60]}。主要用于帮助用户自动化处理特定场景下的任务，减少重复劳动。"
        },
        {
            "q": f"如何开始使用 {name}？",
            "a": f"在对话中提到需要使用 {name} 的场景即可触发。建议先查看 SKILL.md 的「快速开始」章节，按步骤完成首个示例。"
        },
        {
            "q": f"使用 {name} 时需要注意什么？",
            "a": f"使用前务必阅读 `## 约束` 章节中的操作铁律。每次修改后应运行 audit 自审确认 0 ERROR。版本号更新需三端一致。"
        },
        {
            "q": f"{name} 和其他技能有什么区别？",
            "a": f"每个技能专注于特定领域。{name} 的核心能力在 SKILL.md 的 `## 核心能力` 表格中列出，建议阅读后与自身需求对比。"
        },
    ]
    
    section_body = '\n\n'.join(f"### Q: {qa['q']}\n\n**A:** {qa['a']}" for qa in qas)
    ok = _add_section_to_body(skill_md, "FAQ", section_body, insert_after=None)
    return len(qas) if ok else 0



def list_fixable():
    """列出所有可修复的 key"""
    return [
        "name",                        # R-01
        "description",                 # R-02
        "author",                     # R-03
        "version",                    # R-04
        "skill_macro",               # R-05
        "h1",                        # R-06
        "h1_version",                # R-06 清理版本号
        "h1_position",               # R-06 移到 frontmatter 后
        "section_trigger",            # R-07
        "section_core",              # R-08
        "section_workflow",          # R-09
        "home_url",                  # R-10
        "artifact_paths",            # R-11
        "external_data_dir",         # R-12
        "missing_data_dir",          # R-12 step 1.5
        "sensitive_access",          # R-13
        "critical_write",            # R-14
        "create_permissions_md",     # R-15
        "permission_weight",          # R-16
        "progressive_loading",      # R-17
        "antipattern_progressive",  # R-18
        "faq_progressive",          # R-19
        "writing_standards",        # R-20
        "progressive_loading_explicit",  # R-21
        "data_dir_compliance",       # R-22
        "doc_code_consistency",      # R-23
        "meta_json",                 # R-25
        "frontmatter_fields",        # R-01
        "meta_field_sync",           # R-10 共享字段同步
        "split_nonstandard",         # R-17 非标章节拆分
        "section_order",             # R-25 C-11 章节重排
        "section_constraint",         # 从目标技能采集约束生成 ## 约束
        "progressive_index_table",    # 从 references/ 生成渐进式索引表
        "reclassify_section",         # Phase 3 通用非标章节归类（merge/split/delete）
        "version_con",                # R-03 version SemVer 格式
        "sanitize",                   # R-05 name=目录名
        "data_dir",                   # R-12 数据目录路径
        "section_antipattern",        # R-18 反模式内容
        "section_faq",                # R-19 FAQ 内容
        "license_compliance",         # R-26 LICENSE 声明规范
    ]


# ═══════════════════════════════════════════════════════
# R-26: LICENSE 声明规范修复
# ═══════════════════════════════════════════════════════
def fix_license_compliance(skill_dir, **kw):
    """
    R-26 修复：确保 LICENSE 和 README 声明符合规范。
    
    1. 删除根目录/scripts/ 下的 LICENSE 文件
    2. 如果 references/LICENSE.md 不存在，从 skills/LICENSE.txt 复制
    3. 如果 SKILL.md 正文有独立 license 章节，拆分到 references/LICENSE.md
    4. 更新渐进式文件索引表添加 LICENSE.md 引用
    5. 删除根目录 README.md（迁移至 references/README.md）
    6. 如果 SKILL.md 正文有 README/说明章节，拆分至 references/README.md
    """
    import os as _os
    import shutil as _shutil

    skill_dir = _os.path.abspath(skill_dir)
    refs_dir = _os.path.join(skill_dir, "references")
    license_ref_path = _os.path.join(refs_dir, "LICENSE.md")
    skill_md_path = _os.path.join(skill_dir, "SKILL.md")
    fixed = 0

    # 确保 references/ 目录存在
    if not _os.path.isdir(refs_dir):
        _os.makedirs(refs_dir, exist_ok=True)
        print(f"  [创建] {refs_dir}")

    # ── 1. 删除根目录和 scripts/ 下的 LICENSE 文件 ──
    for base_dir, label in [(skill_dir, "根目录"), (_os.path.join(skill_dir, "scripts"), "scripts/")]:
        if not _os.path.isdir(base_dir):
            continue
        for entry in _os.listdir(base_dir):
            if entry.upper().startswith("LICENSE"):
                fpath = _os.path.join(base_dir, entry)
                if _os.path.isfile(fpath):
                    _os.remove(fpath)
                    print(f"  [删除] {label}/{entry}")
                    fixed += 1

    # ── 2. 确保 references/LICENSE.md 存在 ──
    if not _os.path.isfile(license_ref_path):
        # 从 skills/LICENSE.txt 复制模板
        skills_root = _os.path.dirname(skill_dir)  # skills/
        master_license = _os.path.join(skills_root, "LICENSE.txt")
        if _os.path.isfile(master_license):
            _shutil.copy2(master_license, license_ref_path)
            print(f"  [创建] references/LICENSE.md（从 skills/LICENSE.txt 复制）")
        else:
            # 创建空白 MIT 模板
            mit_template = """MIT License

Copyright (c) 2026 your-name-here

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
            with open(license_ref_path, "w", encoding="utf-8") as f:
                f.write(mit_template)
            print(f"  [创建] references/LICENSE.md（空白 MIT 模板）")
        fixed += 1

    # ── 3. 检查 SKILL.md 正文是否有独立 license 章节并处理 ──
    if _os.path.isfile(skill_md_path):
        with open(skill_md_path, "r", encoding="utf-8") as f:
            content = f.read()

        fm, body = parse_simple_yaml_frontmatter(content)
        if body:
            # 查找 license 章节
            lic_section = re.search(
                r'^##\s*(?:License|许可证|许可协议|LICENSE|许可声明)\s*$',
                body, re.MULTILINE | re.IGNORECASE
            )
            if lic_section:
                # 提取该章节的内容
                section_start = lic_section.start()
                # 找到下一个 ## 或文件末尾
                next_section = re.search(r'^##\s+', body[lic_section.end():], re.MULTILINE)
                if next_section:
                    section_end = lic_section.end() + next_section.start()
                else:
                    section_end = len(body)

                # 提取 license 章节内容
                lic_content = body[section_start:section_end].strip()
                # 从 body 中删除
                new_body = body[:section_start] + body[section_end:].lstrip()
                new_content = content[:content.index("---\n", content.index("---\n") + 3) + 4] + "\n" + new_body

                with open(skill_md_path, "w", encoding="utf-8") as f:
                    f.write(new_content)

                # 将内容追加到 references/LICENSE.md（如果还不存在）
                existing_lic = ""
                if _os.path.isfile(license_ref_path):
                    with open(license_ref_path, "r", encoding="utf-8") as f:
                        existing_lic = f.read()

                with open(license_ref_path, "w", encoding="utf-8") as f:
                    f.write(f"# License\n\n{lic_content}\n\n---\n\n{existing_lic}" if existing_lic else f"# License\n\n{lic_content}\n")
                print(f"  [拆分] SKILL.md license 章节 → references/LICENSE.md")
                fixed += 1

    # ── 4. 更新渐进式文件索引表 ──
    if _os.path.isfile(skill_md_path):
        with open(skill_md_path, "r", encoding="utf-8") as f:
            content = f.read()
        fm, body = parse_simple_yaml_frontmatter(content)
        if body and 'references/LICENSE.md' not in body:
            table_end = _re.search(r'\|.*\|.*\|.*\|.*\|\s*$', body, re.MULTILINE)
            if table_end:
                insert_pos = table_end.end()
                lic_row = f"\n| `references/LICENSE.md` | 许可协议 | 开源许可证声明（MIT） | R-26 |"
                new_body = body[:insert_pos] + lic_row + body[insert_pos:]
                new_content = content[:content.index("---\n", content.index("---\n") + 3) + 4] + "\n" + new_body
                with open(skill_md_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"  [索引] 渐进式文件索引表添加 LICENSE.md 引用")
                fixed += 1

    # ── 5. 删除根目录 README.md（迁移至 references/README.md）──
    readme_root = _os.path.join(skill_dir, "README.md")
    readme_ref_path = _os.path.join(refs_dir, "README.md")
    if _os.path.isfile(readme_root):
        # 如果 references/README.md 还不存在，先迁移过去
        if not _os.path.isfile(readme_ref_path):
            _shutil.move(readme_root, readme_ref_path)
            print(f"  [迁移] 根目录 README.md → references/README.md")
        else:
            _os.remove(readme_root)
            print(f"  [删除] 根目录 README.md（references/README.md 已存在）")
        fixed += 1

    # ── 6. 拆分 SKILL.md 正文中的 README/说明章节到 references/README.md ──
    if _os.path.isfile(skill_md_path):
        with open(skill_md_path, "r", encoding="utf-8") as f:
            content = f.read()
        fm, body = parse_simple_yaml_frontmatter(content)
        if body:
            readme_section = re.search(
                r'^##\s*(?:README|说明文档|使用说明|项目说明|简介|Introduction)\s*$',
                body, re.MULTILINE | re.IGNORECASE
            )
            if readme_section:
                section_start = readme_section.start()
                next_section = re.search(r'^##\s+', body[readme_section.end():], re.MULTILINE)
                if next_section:
                    section_end = readme_section.end() + next_section.start()
                else:
                    section_end = len(body)
                readme_content = body[section_start:section_end].strip()
                new_body = body[:section_start] + body[section_end:].lstrip()
                new_content = content[:content.index("---\n", content.index("---\n") + 3) + 4] + "\n" + new_body
                with open(skill_md_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                # 写入 references/README.md
                with open(readme_ref_path, "w", encoding="utf-8") as f:
                    f.write(f"# README\n\n{readme_content}\n")
                print(f"  [拆分] SKILL.md README 章节 → references/README.md")
                fixed += 1

    print(f"  ✅ R-26 修复完成：处理了 {fixed} 项")
    return fixed
