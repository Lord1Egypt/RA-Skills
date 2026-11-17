#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
skill_inspector.py -- Skill 结构快速扫描（蓝皮书生成器）
输出结构化报告：元信息、目录树、章节内容摘要、函数/类签名、引用链路、安全数据

只读操作，不修改任何文件。

用法：
    python -m scripts.skill_inspector <skill-dir>
    python -m scripts.skill_inspector <skill-dir> --json

v2.44.0: 初始版本
v2.45.0: AST 函数扫描 + H2 内容摘要 + 引用链路图
"""

import os
import re
import sys
import json
import ast
from pathlib import Path


def inspect_skill(skill_dir, output_format="text"):
    """
    扫描 skill 目录，生成结构化蓝皮书。
    output_format: "text" (markdown树, 默认) | "json"
    只读操作，不修改任何文件。
    """
    skill_path = Path(skill_dir).resolve()
    skill_name = skill_path.name

    # ---- 1. 读取 SKILL.md ----
    skill_md_path = skill_path / "SKILL.md"
    fm = {}
    body_lines = []
    h2_sections = []
    body_text = ""

    if skill_md_path.exists():
        with open(skill_md_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        m_fm = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if m_fm:
            for line in m_fm.group(1).split('\n'):
                if ':' in line:
                    k, _, v = line.partition(':')
                    fm[k.strip()] = v.strip()
            body_text = content[m_fm.end():]
        else:
            body_text = content
        body_lines = body_text.split('\n')
        # 提取 H2 章节及其内容摘要
        for m in re.finditer(r'^##\s+(.+?)$\n(.*?)(?=^##\s|\Z)', body_text, re.MULTILINE | re.DOTALL):
            title = m.group(1).strip()
            sec_content = m.group(2).strip()[:100].replace('\n', ' ')
            h2_sections.append({"title": title, "preview": sec_content + ("..." if len(m.group(2).strip()) > 100 else "")})

    # ---- 2. 读取 _meta.json ----
    meta = {}
    meta_path = skill_path / "_meta.json"
    if meta_path.exists():
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
        except Exception:
            meta = {"error": "parse_failed"}

    # ---- 3. 扫描所有文件 ----
    all_files = []
    for entry in sorted(skill_path.rglob('*')):
        if entry.name.startswith('.'):
            continue
        rel = entry.relative_to(skill_path)
        rel_str = str(rel)
        if rel_str.startswith('__pycache__') or rel_str.startswith('.git'):
            continue
        all_files.append((rel_str, entry.is_dir()))

    py_files = sorted([f for f, is_d in all_files if f.endswith('.py')])
    md_files = sorted([f for f, is_d in all_files
                       if f.endswith('.md') and f != 'SKILL.md' and not f.startswith('_meta')])
    script_files = sorted([f for f, is_d in all_files
                           if f.endswith(('.sh', '.bat', '.ps1', '.js', '.ts'))])
    config_files = sorted([f for f, is_d in all_files
                           if f.endswith(('.json', '.yaml', '.yml', '.toml', '.ini', '.cfg'))])
    other_files = sorted([f for f, is_d in all_files
                          if f not in py_files + md_files + script_files + config_files])
    root_py = [f for f in py_files if os.sep not in f]
    root_md = [f for f in md_files if os.sep not in f]

    has_scripts_dir = (skill_path / 'scripts').is_dir()
    has_refs_dir = (skill_path / 'references').is_dir()
    standard_score = sum([has_scripts_dir, has_refs_dir])
    if standard_score == 2:
        struct_label = "标准（scripts/ + references/）"
    elif standard_score == 1:
        struct_label = "半标准"
    else:
        struct_label = "非标准（文件散落根目录）"

    # ---- 4. AST 扫描 Python 函数/类/CLI ----
    py_ast_info = {}
    for pf in py_files:
        pf_path = skill_path / pf
        info = {"functions": [], "classes": [], "cli_subcommands": [], "key_constants": []}
        try:
            with open(pf_path, "r", encoding="utf-8", errors="replace") as f:
                src = f.read()
            tree = ast.parse(src, filename=pf)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    doc = ast.get_docstring(node)
                    info["functions"].append({
                        "name": node.name,
                        "lineno": node.lineno,
                        "doc": (doc[:60] + "..." if doc and len(doc) > 60 else doc) if doc else None,
                        "args": [a.arg for a in node.args.args[:5]],
                    })
                elif isinstance(node, ast.ClassDef):
                    doc = ast.get_docstring(node)
                    methods = [n.name for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
                    info["classes"].append({
                        "name": node.name,
                        "lineno": node.lineno,
                        "doc": (doc[:60] + "..." if doc and len(doc) > 60 else doc) if doc else None,
                        "methods": methods[:8],
                    })
                elif isinstance(node, ast.Assign):
                    # 提取大写下划线常量
                    for target in node.targets:
                        if isinstance(target, ast.Name) and re.match(r'^[A-Z][A-Z_]+$', target.id):
                            try:
                                val = ast.literal_eval(node.value)
                                info["key_constants"].append(f"{target.id} = {repr(val)[:40]}")
                            except Exception:
                                pass
            # CLI 子命令扫描
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and hasattr(node.func, 'attr') and node.func.attr == 'add_parser':
                    for k in node.keywords:
                        if k.arg == 'name' and isinstance(k.value, ast.Constant):
                            info["cli_subcommands"].append(k.value.value)
                        elif k.arg == 'aliases' and isinstance(k.value, (ast.List, ast.Tuple)):
                            for elt in k.value.elts:
                                if isinstance(elt, ast.Constant):
                                    info["cli_subcommands"].append(elt.value)
            py_ast_info[pf] = info
        except (SyntaxError, Exception) as e:
            py_ast_info[pf] = {"error": str(e)[:60]}

    # ---- 5. 引用链路图：SKILL.md → references/ 文件 ----
    ref_links = {}
    if body_text and md_files:
        for mf in md_files:
            mf_path = skill_path / mf
            try:
                with open(mf_path, "r", encoding="utf-8", errors="replace") as f:
                    m_content = f.read()
                ref_links[mf] = {
                    "referenced_in_skillmd": mf.replace('\\', '/') in body_text or mf.split('/')[-1] in body_text,
                    "lines": m_content.count('\n') + 1,
                    "h1_title": "",
                }
                m1 = re.search(r'^#\s+(.+)$', m_content, re.MULTILINE)
                if m1:
                    ref_links[mf]["h1_title"] = m1.group(1).strip()
            except Exception:
                pass

    # ---- 6. 文档-代码潜在脱节标记 ----
    doc_code_gaps = []
    # 检查 SKILL.md 描述的规则数 vs 实际
    all_r_numbers = re.findall(r'R-(\d+)', body_text) if body_text else []
    if all_r_numbers:
        claimed = max(int(x) for x in all_r_numbers)
        rules_json_path = skill_path / "scripts" / "spec" / "rules.json"
        if rules_json_path.exists():
            try:
                with open(rules_json_path) as f:
                    rules_data = json.load(f)
                actual = rules_data.get('_total_rules', 0)
                if claimed != actual:
                    doc_code_gaps.append(f"SKILL.md 声称 R-01~R-{claimed}，实际 rules.json 有 {actual} 条")
            except Exception:
                pass

    # ---- 7. 安全 & 数据信息 ----
    sec_info = {
        "sensitive_access": fm.get("sensitive_access", "?"),
        "critical_write": fm.get("critical_write", "?"),
        "permission_weight": fm.get("permission_weight", "?"),
        "data_dir": fm.get("data_dir", meta.get("data_dir", "?"))
    }

    # ---- 组装报告 ----
    # 新增：结构化目录元信息（供审计规则直接使用，避免重复 os.listdir）
    root_files = sorted([f for f, is_d in all_files if os.sep not in f and not is_d])
    root_dirs = sorted([f for f, is_d in all_files if os.sep not in f and is_d])
    ref_files = sorted([f.split(os.sep)[-1] for f in md_files if f.startswith('references' + os.sep)])
    scripts_dir_files = sorted([f.split(os.sep, 1)[-1] for f, is_d in all_files
                                 if f.startswith('scripts' + os.sep) and not is_d])
    has_data_dir = (skill_path / 'data').is_dir()
    has_output_dir = (skill_path / 'data' / 'output').is_dir()
    has_logs_dir = (skill_path / 'data' / 'logs').is_dir()
    has_temp_dir = (skill_path / 'data' / 'temp').is_dir()

    report = {
        "name": skill_name,
        "version": fm.get("version", meta.get("version", "?")),
        "description": fm.get("description", meta.get("description", "")),
        "structure": struct_label,
        "skill_md": {
            "exists": skill_md_path.exists(),
            "lines": len(body_lines),
            "h2_sections_count": len(h2_sections),
            "h2_sections": h2_sections,
            "frontmatter_fields": list(fm.keys()) if fm else [],
        },
        "meta_json": meta,
        "directory": {
            "py_files": len(py_files),
            "md_files": len(md_files),
            "script_files": len(script_files),
            "config_files": len(config_files),
            "other_files": len(other_files),
            "root_py": root_py,
            "root_md": root_md,
        },
        "python_ast": py_ast_info,
        "reference_links": ref_links,
        "doc_code_gaps": doc_code_gaps,
        "security": sec_info,
        # ── 蓝皮书 v2 新增：结构化目录元信息 ────────────
        "structure_tree": _format_structure_tree(skill_path, all_files),
        "root_files": root_files,
        "root_dirs": root_dirs,
        "ref_files": ref_files,
        "scripts_files": scripts_dir_files,
        "has_data_dir": has_data_dir,
        "has_output_dir": has_output_dir,
        "has_logs_dir": has_logs_dir,
        "has_temp_dir": has_temp_dir,
        "has_scripts_dir": has_scripts_dir,
        "has_refs_dir": has_refs_dir,
    }

    if output_format == "json":
        return json.dumps(report, ensure_ascii=False, indent=2)
    elif output_format == "dict":
        return report

    return _format_text_report(report, skill_path)


def _format_text_report(report, skill_path):
    """格式化为可读的 Markdown 蓝皮书"""
    lines = []
    name = report["name"]
    ver = report["version"]

    lines.append(f"=== {name} v{ver} ===")
    lines.append("")

    # ---- 元信息 ----
    lines.append("|-- 元信息")
    smd = report["skill_md"]
    lines.append(f"|   |-- SKILL.md: {'[OK]' if smd['exists'] else '[MISS]'}"
                 f" ({smd['lines']}行, {smd['h2_sections_count']}个 ## 章节)")
    lines.append(f"|   |-- 结构: {report['structure']}")
    desc = report.get("description", "")
    if desc:
        lines.append(f"|   |-- 描述: {desc[:80]}{'...' if len(desc) > 80 else ''}")
    meta = report.get("meta_json", {})
    if meta and "error" not in meta:
        meta_fields = list(meta.keys())
        lines.append(f"|   +-- _meta.json: {len(meta_fields)} 字段")
    else:
        lines.append("|   +-- _meta.json: [MISS] 缺失或解析失败")
    lines.append("")

    # ---- 正文章节（含内容预览） ----
    sections = smd["h2_sections"]
    if sections:
        lines.append("|-- 正文章节 (##)")
        for sec in sections:
            title = sec["title"]
            preview = sec.get("preview", "")
            if preview:
                lines.append(f"|   |-- {title}")
                lines.append(f"|   |   `-- {preview}")
            else:
                lines.append(f"|   +-- {title}")
        lines.append("")

    # ---- AST 功能清单 ----
    py_info = report.get("python_ast", {})
    if py_info:
        lines.append("|-- Python 代码结构 (AST)")
        items = list(py_info.items())
        for i, (fpath, info) in enumerate(items):
            marker = "+--" if i == len(items) - 1 else "|--"
            lines.append(f"|   {marker} {fpath}")
            if info.get("error"):
                lines.append(f"|       [解析失败] {info['error']}")
                continue
            for func in info.get("functions", [])[:5]:
                args = ", ".join(func.get("args", [])[:4])
                doc = f" — {func['doc']}" if func.get("doc") else ""
                lines.append(f"|       |-- def {func['name']}({args}){doc}")
            for cls in info.get("classes", [])[:3]:
                doc = f" — {cls['doc']}" if cls.get("doc") else ""
                lines.append(f"|       |-- class {cls['name']}{doc}")
                for m in cls.get("methods", [])[:4]:
                    lines.append(f"|       |   +-- method: {m}")
            for const in info.get("key_constants", [])[:3]:
                lines.append(f"|       |-- {const}")
            subs = info.get("cli_subcommands", [])
            if subs:
                lines.append(f"|       +-- CLI: {', '.join(subs[:6])}")
        lines.append("")

    # ---- 引用链路 ----
    refs = report.get("reference_links", {})
    if refs:
        lines.append("|-- 引用文件链路")
        items = list(refs.items())
        for i, (fname, info) in enumerate(items):
            marker = "+--" if i == len(items) - 1 else "|--"
            status = "引用" if info.get("referenced_in_skillmd") else "未引用"
            h1 = f" ({info['h1_title']})" if info.get("h1_title") else ""
            lines.append(f"|   {marker} {fname} [{status}]{h1} ({info['lines']}行)")
        lines.append("")

    # ---- 文档-代码潜在脱节 ----
    gaps = report.get("doc_code_gaps", [])
    if gaps:
        lines.append("+-- ⚠️ 文档-代码潜在脱节")
        for g in gaps:
            lines.append(f"    +-- {g}")
        lines.append("")

    # ---- 文件清单（按类型分组） ----
    lines.append("+-- 文件清单")
    d = report["directory"]
    lines.append(f"    |-- Python: {d['py_files']} 个")
    if d['root_py']:
        for rp in d['root_py']:
            lines.append(f"    |   [note] {rp} 在根目录，建议迁至 scripts/")
    lines.append(f"    |-- Markdown: {d['md_files']} 个")
    if d['root_md']:
        for rm in d['root_md']:
            lines.append(f"    |   [note] {rm} 在根目录，建议迁至 references/")
    lines.append(f"    |-- 脚本(sh/bat/js): {d['script_files']} 个")
    lines.append(f"    |-- 配置(json/yaml): {d['config_files']} 个")
    lines.append(f"    +-- 其他: {d['other_files']} 个")
    lines.append("")

    # ---- 目录结构树 ----
    tree = report.get("structure_tree", "")
    if tree:
        lines.append("+-- 目录结构")
        for line in tree.split('\n'):
            lines.append(f"    {line}")
        lines.append("")

    lines.append("-" * 40)
    lines.append("蓝皮书：结构扫描 + AST 功能清单 + 引用链路")
    lines.append(f"  python -m scripts.skill_inspector {skill_path} --json")

    return "\n".join(lines)


def main():
    """CLI 入口 — 只读，不修改任何文件"""
    if sys.stdout.encoding and sys.stdout.encoding.upper() not in ('UTF-8', 'UTF8'):
        sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1, errors='replace')

    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("Usage: python -m scripts.skill_inspector <skill-dir> [--json]")
        print("只读操作，输出 skill 蓝皮书：结构、AST函数签名、引用链路")
        print("用于 update/refactor 前的全貌扫描")
        sys.exit(1)

    skill_dir = sys.argv[1]
    fmt = "json" if "--json" in sys.argv else "text"

    if not os.path.isdir(skill_dir):
        print(f"[ERROR] Directory not found: {skill_dir}", file=sys.stderr)
        sys.exit(1)

    result = inspect_skill(skill_dir, fmt)
    print(result)


def _format_structure_tree(skill_path, all_files):
    """
    生成类 tree 命令的目录结构树。
    all_files: [(rel_path, is_dir), ...]
    排除隐藏目录（. 开头）和 __pycache__/.git。
    """
    tree_lines = [skill_path.name + "/"]
    # 构建路径树
    children = {}  # {parent_dir: [(name, is_dir, full_rel_path), ...]}
    for rel, is_dir in all_files:
        parts = rel.split(os.sep)
        if len(parts) == 1:
            children.setdefault("", []).append((parts[0], is_dir, rel))
        else:
            parent = os.sep.join(parts[:-1])
            children.setdefault(parent, []).append((parts[-1], is_dir, rel))

    def _render(parent, prefix=""):
        items = sorted(children.get(parent, []), key=lambda x: (not x[1], x[0]))
        for i, (name, is_dir, rel) in enumerate(items):
            is_last = (i == len(items) - 1)
            connector = "+-- " if is_last else "|-- "
            sub_prefix = "    " if is_last else "|   "
            tree_lines.append(prefix + connector + name)
            if is_dir:
                _render(rel, prefix + sub_prefix)

    _render("")
    return "\n".join(tree_lines)


if __name__ == "__main__":
    main()
