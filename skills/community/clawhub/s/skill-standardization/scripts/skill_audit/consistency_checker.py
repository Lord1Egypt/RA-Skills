#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
consistency_checker.py — 文档-代码一致性审查（双 0 后执行）

功能：
  - 文档-代码双向一致性检查（文档有代码没有 / 代码有文档没有）
  - 目录树 vs 磁盘文件双向对比
  - 规则编号范围过时检测（SKILL.md + references/*.md）
  - argparse flag 一致性（文档示例 vs 代码实际参数）
  - data_dir 路径一致性
  - 函数签名一致性（骨架）

触发条件：仅在双 0 确认后执行
"""

import os
import re
import json
from ._path_detector import has_path_feature, _find_shared_path_file


def check_consistency(skill_dir, filter_files=None):
    """
    执行一致性审查。
    
    返回: [{"type": "missing_file|stale_doc_ref|missing_doc_ref|outdated_rule_ref|argparse_mismatch|path_mismatch|...",
            "detail": "...", "severity": "WARN"}, ...]
    """
    issues = []
    
    if not os.path.isdir(skill_dir):
        return issues
    
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return issues
    
    with open(skill_md, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
    
    # ── 1. 目录树 vs 磁盘文件双向对比 ──
    # 解析目录树：跟踪缩进层级重建完整路径
    tree_pattern = re.compile(r'^(?P<indent>[ │]+)?(?P<branch>[├└])──\s+(?P<name>.+)$', re.MULTILINE)
    doc_files = set()
    # 维护一个按缩进深度堆叠的路径前缀栈
    path_stack = [""]  # stack[0] = 根目录
    prev_indent_len = -1
    for m in tree_pattern.finditer(content):
        raw_indent = m.group('indent') or ""
        indent_len = len(raw_indent)
        name = m.group('name').strip().rstrip()
        # 跳过中文名称（概念描述，非真实文件）
        if re.search(r'[\u4e00-\u9fff]', name):
            # 但如果是目录（以/结尾），仍要更新路径栈
            if name.endswith('/') or name.endswith('\\'):
                # 根据缩进深度调整栈
                if indent_len > prev_indent_len:
                    path_stack.append(name.rstrip('/\\'))
                elif indent_len < prev_indent_len:
                    depth_diff = (prev_indent_len - indent_len) // 2
                    for _ in range(min(depth_diff + 1, len(path_stack) - 1)):
                        path_stack.pop()
                    path_stack.append(name.rstrip('/\\'))
                else:
                    if len(path_stack) > 1:
                        path_stack.pop()
                    path_stack.append(name.rstrip('/\\'))
                prev_indent_len = indent_len
            continue
        
        # 判断是目录还是文件
        if name.endswith('/') or name.endswith('\\'):
            # 目录：更新路径栈
            if indent_len > prev_indent_len:
                # 子目录：推入栈
                path_stack.append(name.rstrip('/\\'))
            elif indent_len < prev_indent_len:
                # 上级目录：弹出然后推入
                depth_diff = (prev_indent_len - indent_len) // 2
                for _ in range(min(depth_diff + 1, len(path_stack) - 1)):
                    path_stack.pop()
                path_stack.append(name.rstrip('/\\'))
            else:
                # 同级目录：替换
                if len(path_stack) > 1:
                    path_stack.pop()
                path_stack.append(name.rstrip('/\\'))
            prev_indent_len = indent_len
            continue
        
        # 是文件：用当前路径栈重建完整路径
        if not name.endswith(('.md', '.py', '.json', '.txt', '.toml', '.yaml', '.yml', '.cfg', '.ini', '.csv')):
            continue
        # 从栈重建相对路径（跳过根 ""）
        dir_prefix = "/".join(p for p in path_stack[1:] if p) if len(path_stack) > 1 else ""
        full_name = f"{dir_prefix}/{name}" if dir_prefix else name
        doc_files.add(full_name)
        prev_indent_len = indent_len
    
    if filter_files:
        for f in filter_files:
            fpath = os.path.join(skill_dir, f)
            if not os.path.isfile(fpath):
                issues.append({
                    "type": "missing_file",
                    "detail": f"变更声明中的文件 {f} 在磁盘上不存在",
                    "severity": "ERROR"
                })
    else:
        scripts_dir = os.path.join(skill_dir, "scripts")
        refs_dir = os.path.join(skill_dir, "references")
        
        disk_scripts = set()
        if os.path.isdir(scripts_dir):
            for f in os.listdir(scripts_dir):
                if f.endswith('.py') and f != '__init__.py':
                    disk_scripts.add(f"scripts/{f}")
        
        disk_refs = set()
        if os.path.isdir(refs_dir):
            for f in os.listdir(refs_dir):
                if f.endswith('.md'):
                    disk_refs.add(f"references/{f}")
        
        for f in doc_files:
            fpath = os.path.join(skill_dir, f)
            if not os.path.isfile(fpath):
                issues.append({
                    "type": "stale_doc_ref",
                    "detail": f"文档目录树引用了 {f} 但磁盘上不存在",
                    "severity": "WARN"
                })
        
        for f in sorted(disk_scripts | disk_refs):
            if f not in doc_files:
                issues.append({
                    "type": "missing_doc_ref",
                    "detail": f"磁盘存在 {f} 但文档目录树未列出",
                    "severity": "WARN"
                })
    
    # ── 2. 规则编号范围过时检测 ──
    # 扫描 SKILL.md + references/*.md 中 R-XX~R-YY 的范围引用
    _check_rule_range_consistency(skill_dir, content, issues, filter_files)
    
    # ── 3. argparse flag 一致性 ──
    # 扫描文档中的 --xxx 参数 vs 脚本实际 add_argument('--xxx')
    if not filter_files or any(f.endswith('.py') for f in filter_files):
        _check_argparse_consistency(skill_dir, content, issues)
    
    # ── 4. data_dir 路径一致性 ──
    _check_data_dir_consistency(skill_dir, content, issues)
    
    # ── 5. 路径集中管理（R-25 C-20） ──
    try:
        issues += _check_path_centralization(skill_dir)
    except Exception:
        pass  # 非阻断
    
    return issues


def _check_rule_range_consistency(skill_dir, content, issues, filter_files):
    """检查 SKILL.md + references/*.md 中引用的规则编号范围是否与 rules.json 一致。"""
    # 读取 rules.json 获取实际最大规则编号
    _rules_spec_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'spec', 'rules.json'
    )
    if not os.path.isfile(_rules_spec_path):
        return
    try:
        with open(_rules_spec_path, 'r', encoding='utf-8') as f:
            _rules_data = json.load(f)
        _actual_max = _rules_data.get('_total_rules', 0)
    except Exception:
        return
    if not _actual_max:
        return
    
    # 需要扫描的文件
    _docs_to_scan = []
    _refs_dir = os.path.join(skill_dir, 'references')
    
    if filter_files:
        # 更新模式：只扫描变更文件
        for f in filter_files:
            if f == 'SKILL.md':
                _docs_to_scan.append(('SKILL.md', content))
            elif f.startswith('references/') and f.endswith('.md'):
                fp = os.path.join(skill_dir, f)
                if os.path.isfile(fp):
                    try:
                        with open(fp, 'r', encoding='utf-8') as _rf:
                            _docs_to_scan.append((f, _rf.read()))
                    except Exception:
                        pass
    else:
        # 全量：SKILL.md + 所有 references/*.md
        _docs_to_scan.append(('SKILL.md', content))
        if os.path.isdir(_refs_dir):
            for _rf in sorted(os.listdir(_refs_dir)):
                if _rf.endswith('.md'):
                    _rp = os.path.join(_refs_dir, _rf)
                    try:
                        with open(_rp, 'r', encoding='utf-8') as _rfh:
                            _docs_to_scan.append((f'references/{_rf}', _rfh.read()))
                    except Exception:
                        pass
    
    for _doc_name, _doc_content in _docs_to_scan:
        for m in re.finditer(r'R-(\d+)~R-(\d+)', _doc_content):
            _claimed_max = int(m.group(2))
            if _claimed_max != _actual_max:
                _line_no = _doc_content[:m.start()].count('\n') + 1
                issues.append({
                    "type": "outdated_rule_ref",
                    "detail": f"{_doc_name}:{_line_no} - 声称最大规则编号为 R-{_claimed_max}，"
                              f"但 rules.json 实际为 R-{_actual_max}，描述可能过时",
                    "severity": "WARN"
                })


def _check_argparse_consistency(skill_dir, content, issues):
    """
    检查文档中的 --xxx 参数是否在对应脚本中实际定义。
    从文档提取 scripts/xxx.py 引用及其 --flags，与代码 add_argument 对比。
    """
    # 提取文档中所有代码块和行内代码的命令行引用
    code_blocks = re.findall(r'```(?:bash|sh)?\s*\n(.*?)```', content, re.DOTALL)
    # ⚠️ 限制单行：`[^`\n]+` 防止误吞 ```bash``` 代码块内容（之前用 `[^`]+?` 惰性匹配会吞整块）
    inline_codes = re.findall(r'`([^`\n]+?)`', content)
    
    all_cmds = []
    for block in code_blocks:
        for line in block.splitlines():
            line = line.strip()
            if line.startswith('#') or not line:
                continue
            all_cmds.append(line)
    for ic in inline_codes:
        all_cmds.append(ic)
    
    # 匹配 scripts/xxx.py 的引用
    for cmd in all_cmds:
        for m in re.finditer(r'(scripts/[a-zA-Z_][a-zA-Z0-9_/]*\.py)', cmd):
            script_path = m.group(1)
            full_path = os.path.join(skill_dir, script_path)
            if not os.path.isfile(full_path):
                continue
            
            # 提取文档中此命令的 --flags
            doc_flags = set(re.findall(r'--([a-z][-a-z]*)', cmd))
            if not doc_flags:
                continue
            
            # 从脚本源码提取实际 argparse flags
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    src = f.read()
                actual_flags = set(re.findall(r"add_argument\(\s*['\"]--([a-z][-a-z]*)['\"]", src))
                # 也检测手动 sys.argv 解析（if "--xxx" in sys.argv 等）
                manual_flags = set(re.findall(r"""['\"]--([a-z][-a-z]*)['\"]\s*(?:in\s+sys\.argv|not in\s+sys\.argv)""", src))
                actual_flags.update(manual_flags)
                
                for flag in doc_flags:
                    if flag not in actual_flags and flag not in ('help', 'version', 'html', 'markdown'):
                        issues.append({
                            "type": "argparse_mismatch",
                            "detail": f"文档示例中 `{script_path}` 含 `--{flag}` 但代码未定义此参数"
                                      f"（实际定义：{', '.join(sorted(actual_flags)[:5]) or '无'}）",
                            "severity": "WARN"
                        })
            except Exception:
                pass


def _check_data_dir_consistency(skill_dir, content, issues):
    """
    检查 SKILL.md 正文中的 data_dir 路径描述是否与 frontmatter 一致。
    从 frontmatter 解析 data_dir，检查正文中是否包含缺少 .standardization/ 层级的路径。
    """
    fm, body = _parse_frontmatter(content)
    if not fm or not fm.get('data_dir'):
        return
    
    data_dir_val = str(fm['data_dir']).replace('\\', '/')
    if '.standardization' not in data_dir_val:
        return
    
    # 从 data_dir 提取技能目录名
    _dd_parts = data_dir_val.rstrip('/').split('/')
    skill_name_in_dir = _dd_parts[-2] if len(_dd_parts) >= 2 else ''
    if not skill_name_in_dir:
        return
    
    # 搜索正文中 skills/<skill>/data/ 模式（缺少 .standardization 前缀）
    _old_path_re = re.compile(
        r'skills/(?:(?!\.standardization/)[^/]+/)*' + re.escape(skill_name_in_dir) + r'/data/'
    )
    for _m in _old_path_re.finditer(body):
        _line = body[:_m.start()].count('\n') + 1
        issues.append({
            "type": "path_mismatch",
            "detail": f"SKILL.md:{_line} - 正文路径 `{_m.group()}` 缺少 `.standardization/` 层级"
                      f"（frontmatter data_dir 为 `{data_dir_val}`，路径应包含 `.standardization/` 前缀）",
            "severity": "WARN"
        })


def _parse_frontmatter(text):
    """简易 frontmatter 解析。返回 (dict, body_text)。"""
    if not text.startswith("---"):
        return None, text
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    lines = text.split("\n", 1)
    rest = lines[1] if len(lines) > 1 else ""
    end_idx = rest.find("\n---")
    if end_idx == -1:
        return None, text
    fm_text = rest[:end_idx]
    body = rest[end_idx + 4:]
    
    result = {}
    for line in fm_text.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith(">"):
            continue
        colon_idx = stripped.find(":")
        if colon_idx > 0:
            key = stripped[:colon_idx].strip()
            val = stripped[colon_idx + 1:].strip()
            if (val.startswith('"') and val.endswith('"')) or \
               (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
            if val.lower() == "true":
                result[key] = True
            elif val.lower() == "false":
                result[key] = False
            else:
                result[key] = val
    return result, body


def format_consistency_report(issues):
    """格式化为可读报告"""
    if not issues:
        return "  ✅ 一致性审查通过，无问题"
    
    lines = []
    for issue in issues:
        if issue.get('reclassified'):
            sev = "[ⓘ]"
            label = "排除"
        else:
            sev = "[ERROR]" if issue['severity'] == 'ERROR' else "[WARN]"
            label = issue['severity']
        lines.append(f"  {sev} {issue['type']}: {issue['detail']}")
    
    return '\n'.join(lines)


def reclassify_consistency_false_positive(issue, skill_dir=None):
    """
    一致性审查误判过滤。
    标记已知不是真正问题的项。
    返回 True 表示该问题是误报，应排除。
    
    v2.91.0: 读取共享 .verify_fp.json 误判标记（ID 格式 C-{type}）。
    所有误判统一由 LLM 通过 --classify 标记，代码层不做自动排除。
    与审计 _reclassify_false_positive 一致。
    """
    detail = str(issue.get('detail', ''))
    issue_type = issue.get('type', '')
    severity = issue.get('severity', 'WARN')
    
    # ── 层1：共享 --classify 误判标记（读取 .verify_fp.json） ──
    if skill_dir:
        skill_dir = os.path.abspath(skill_dir)
        fp_path = os.path.join(
            os.path.dirname(skill_dir), '.standardization',
            os.path.basename(skill_dir), 'data', '.verify_fp.json')
        if os.path.isfile(fp_path):
            try:
                with open(fp_path, 'r', encoding='utf-8') as _fpf:
                    fp_ids = set(json.load(_fpf))
                # 一致性问题的 ID 格式: "C-{type}"
                issue_id = f"C-{issue_type}"
                if issue_id in fp_ids:
                    return True
            except Exception:
                pass
    
    # 所有误判统一由 LLM 通过 --classify 标记（写入 .verify_fp.json），
    # 代码层不做任何自动误报排除。与审计 _reclassify_false_positive 一致。
    return False


def apply_consistency_fix(skill_dir, issue):
    """
    尝试自动修复一致性审查问题。
    返回 True 表示已修复，False 表示无法自动修复（需 LLM 处理）。
    """
    import re
    issue_type = issue.get('type', '')
    detail = str(issue.get('detail', ''))
    
    if issue_type == 'outdated_rule_ref':
        # 格式: "SKILL.md:86 - 声称最大规则编号为 R-26，但 rules.json 实际为 R-25"
        # 或 "references/xxx.md:99 - 声称最大规则编号为 R-17，但 rules.json 实际为 R-25"
        _m = re.match(r'([^:]+):(\d+) - 声称最大规则编号为 R-(\d+).*实际为 R-(\d+)', detail)
        if not _m:
            return False
        _file = _m.group(1)
        _line = int(_m.group(2))
        _old_max = int(_m.group(3))
        _actual_max = int(_m.group(4))
        
        _fp = os.path.join(skill_dir, _file)
        if not os.path.isfile(_fp):
            return False
        
        try:
            with open(_fp, 'r', encoding='utf-8') as f:
                _content = f.read()
            
            # 替换文件中所有旧规则编号引用：
            # 1. R-XX 精确匹配（如 R-4 → R-25, R-04 → R-25）
            # 2. R-XX~R-YY 范围中的旧最大值（如 R-01~R-04 → R-01~R-25）
            # ⚠️ 注意：旧值 < 新值时才是过时需要替换（如 R-4 → R-25）
            #       旧值 > 新值时（如 R-26 → R-25）说明文件本身正确但 rules.json 落后
            #       此时不应自动修复，应由 LLM 判断
            if _old_max < _actual_max:
                _content_new = _content
                # 替换带前导零的格式: R-04 → R-25, R-06 → R-25
                _content_new = _content_new.replace(f'R-{_old_max:02d}', f'R-{_actual_max}')
                # 替换不带前导零的格式: R-4 → R-25, R-9 → R-25
                _content_new = _content_new.replace(f'R-{_old_max}', f'R-{_actual_max}')
                
                if _content_new != _content:
                    with open(_fp, 'w', encoding='utf-8') as f:
                        f.write(_content_new)
                    return True
        except Exception:
            return False
    
    # missing_doc_ref: 检查是否需要在 SKILL.md 的目录树中添加引用
    # 这种需要 LLM 判断具体放在哪，不自动修复
    
    # stale_doc_ref: 文档目录树引用了已删除的文件
    # 需要 LLM 确认是否确实删除了
    
    # ── 路径集中管理：检测 _paths.py 缺失/路径定义分散 ──
    if issue_type == 'path_centralization':
        return _fix_path_centralization(skill_dir, issue)
    
    return False





def _check_path_centralization(skill_dir):
    """
    检测 scripts/*.py 中的路径定义是否集中管理（R-25 C-20）。
    
    v2.99.0: 
      - 自动识别共享文件（不限于 _paths.py）
      - 检测所有非从共享文件导入的路径构造，全部输出（不再只输出重复定义）
    
    P1 — 模块级路径常量定义（_DIR/_PATH/_ROOT）
    P2 — sys.argv[N] 用于文件 I/O
    P3 — 局域路径推导（Path拼接/os.path.join含.standardization）
    P4 — 硬编码路径字面量
    
    返回 [{"type": "path_centralization", "detail": "...", "severity": "WARN",
            "fix": {"key": "path_centralization", ...}}, ...]
    """
    import ast, os, re
    issues = []
    scripts_dir = os.path.join(skill_dir, "scripts")
    if not os.path.isdir(scripts_dir):
        return issues

    # ── 自动检测共享文件 ──
    shared_file, shared_vars, _shared_cnt = _find_shared_path_file(scripts_dir)
    shared_basename = shared_file[:-3] if shared_file else "_paths"  # 含默认 fallback
    has_shared_module = shared_file is not None

    # 收集所有脚本中的路径定义（按解析值分组，同时标记是否已在共享文件中）
    from collections import defaultdict
    path_defs = defaultdict(list)  # key: 解析后的路径值, value: [(file, line, var_name, code_line)]

    for fname in sorted(os.listdir(scripts_dir)):
        if not fname.endswith(".py") or fname == shared_file or fname.startswith("__"):
            continue
        fpath = os.path.join(scripts_dir, fname)
        try:
            with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                lines = f.readlines()
            text = "".join(lines)
        except Exception:
            continue

        rel = os.path.join("scripts", fname).replace("\\", "/")

        # 检查脚本是否已从共享文件导入
        uses_shared = (
            f"from {shared_basename} import" in text or 
            f"from scripts.{shared_basename} import" in text
        )

        # ── P1: 模块级路径常量定义 ──
        p1_pat = re.compile(
            r'^([A-Za-z_]+(?:_DIR|_PATH|_ROOT))\s*=\s*(.+?)$',
            re.MULTILINE
        )
        for m in p1_pat.finditer(text):
            var_name = m.group(1)
            val = m.group(2).strip()
            line_num = text[:m.start()].count('\n') + 1
            stripped = lines[line_num - 1].strip() if line_num <= len(lines) else ""
            if stripped.startswith("#"):
                continue
            if not has_path_feature(val):
                continue

            # ★ v2.99.0: 检查是否已从共享文件导入，不在则输出
            if has_shared_module and uses_shared and var_name in shared_vars:
                continue  # 已在共享文件中声明且已导入 → OK

            path_defs[val.strip()].append((
                rel, line_num, var_name, stripped
            ))

        # ── P3/P4: 所有含路径特征的构造（非模块级常量） ──
        # 检测所有硬编码路径字面量和路径推导，如果不在共享文件中则输出
        if uses_shared:
            continue  # 已使用共享模块，假设该文件路径都从共享文件来
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith("import") or stripped.startswith("from"):
                continue
            # 检测路径特征（字面量、Path、os.path.join、parent 链等）
            if has_path_feature(stripped):
                # 排除注释和非常量赋值中的路径引用
                if re.match(r'^\s*#', stripped):
                    continue
                # 检查是否是变量赋值或路径构造函数调用
                is_path_construct = (
                    re.search(r'["\'](?:skills/|\.standardization/|\.workbuddy)["\']', stripped) or
                    re.search(r'Path\s*\(', stripped) or
                    re.search(r'os\.path\.join', stripped) or
                    re.search(r'\.parent', stripped) or
                    re.search(r'[A-Za-z]:[\\/]', stripped)
                )
                if not is_path_construct:
                    continue

                # P2: sys.argv[N] + 文件 I/O
                if re.search(r'sys\.argv\[\d+\]', stripped):
                    has_file_op = any(fn in stripped for fn in [
                        '.read_text(', '.write_text(', 'open(', '.read(', '.write(',
                        'Path(', 'json.load', 'json.dump',
                    ])
                    if has_file_op:
                        issues.append({
                            "type": "path_centralization",
                            "severity": "WARN",
                            "detail": (
                                f"{rel}:{i}  sys.argv 裸用于文件 I/O\n"
                                f"  行内容: {stripped[:120]}\n"
                                f"  修复: 改为 from {shared_basename} import resolve_state_path，包裹 sys.argv 读取"
                            ),
                            "fix": {
                                "key": "path_centralization",
                                "location": f"{rel}:{i}",
                                "operation": (
                                    f"1) 添加 from {shared_basename} import resolve_state_path\n"
                                    "2) 将 sys.argv[N] 读取路径改为 resolve_state_path(sys.argv[N])"
                                ),
                            }
                        })
                    continue  # 已作为 P2 输出

                # P3/P4: 硬编码/推导路径 → 输出
                issues.append({
                    "type": "path_centralization",
                    "severity": "WARN",
                    "detail": (
                        f"{rel}:{i}  路径构造未从共享文件导入\n"
                        f"  行内容: {stripped[:120]}\n"
                        f"  修复: 将路径定义移入 scripts/{shared_file or '_paths.py'}，"
                        f"原处改为 from {shared_basename} import <变量>"
                    ),
                    "fix": {
                        "key": "path_centralization",
                        "location": f"{rel}:{i}",
                        "operation": (
                            f"1) 将路径定义移入 scripts/{shared_file or '_paths.py'}\n"
                            f"2) 原处改为 from {shared_basename} import <变量>"
                        ),
                    }
                })

    # ── P1 分组输出：每条路径定义都输出（不论是否重复） ──
    for val, defs in path_defs.items():
        # ★ v2.99.0: 每条不在共享文件中的路径定义都输出，不再只输出重复定义
        sources = [f"{d[0]}:{d[1]}" for d in defs]
        vars_list = [d[2] for d in defs]
        example_code = defs[0][3]

        # 检查此值是否已在共享文件中声明
        if has_shared_module and any(v in shared_vars for v in vars_list):
            continue  # 已在共享文件中声明 → OK

        if len(defs) == 1:
            # 单文件定义，但不在共享文件中 → 输出
            issues.append({
                "type": "path_centralization",
                "severity": "WARN",
                "detail": (
                    f"{sources[0]}  {defs[0][2]} 路径定义未集中\n"
                    f"  表达式: {example_code[:120]}\n"
                    f"  修复: 移入 scripts/{shared_file or '_paths.py'}，"
                    f"原处改为 from {shared_basename} import {vars_list[0]}"
                ),
                "fix": {
                    "key": "path_centralization",
                    "location": sources[0],
                    "operation": (
                        f"1) 在 scripts/{shared_file or '_paths.py'} 中添加 {vars_list[0]} = {example_code}\n"
                        f"2) 删除 {sources[0]} 的该行定义\n"
                        f"3) 在 {defs[0][0]} 顶部添加 from {shared_basename} import {vars_list[0]}"
                    ),
                }
            })
        else:
            # 多文件重复定义
            all_shared = all(v in shared_vars for v in vars_list) if has_shared_module else False
            if all_shared:
                continue
            issues.append({
                "type": "path_centralization",
                "severity": "WARN",
                "detail": (
                    f"{sources[0]}  {defs[0][2]} 路径重复定义\n"
                    f"  表达式: {example_code[:120]}\n"
                    f"  同值文件: {', '.join(sources[1:])}\n"
                    f"  修复: 移入 scripts/{shared_file or '_paths.py'}，"
                    f"原处改为 from {shared_basename} import {vars_list[0]}"
                ),
                "fix": {
                    "key": "path_centralization",
                    "location": sources[0],
                    "operation": (
                        f"1) 在 scripts/{shared_file or '_paths.py'} 中添加 {vars_list[0]} = {example_code}\n"
                        f"2) 删除 {sources[0]} 的该行定义\n"
                        f"3) 在 {defs[0][0]} 顶部添加 from {shared_basename} import {vars_list[0]}\n"
                        f"4) 对 {', '.join(sources[1:])} 同样替换为 import"
                    ),
                }
            })

    return issues


def _fix_path_centralization(skill_dir, issue):
    """
    自动修复路径集中管理问题。
    创建/更新共享文件（自动识别文件名），将分散的路径定义替换为 import。
    返回 True 表示修复成功，False 表示失败。
    """
    import re, os, tempfile
    detail = str(issue.get("detail", ""))
    
    # 从 detail 提取共享文件名（路径构造 / 路径未集中 / 重复定义）
    # 新格式: ...移入 scripts/<filename>，...
    _m_shared = re.search(r'scripts/(\S+?)(?:\'|"|\s|，|,|$)', detail)
    if _m_shared:
        shared_fname = _m_shared.group(1)
    else:
        shared_fname = "_paths.py"
    
    # 从 detail 提取首个源文件路径和变量名
    m = re.match(r'(scripts/[^:]+):(\d+)\s+(\w+)\s+(?:路径重复定义|路径定义未集中)', detail)
    if not m:
        # 尝试匹配 sys.argv / 路径构造格式
        m2 = re.match(r'(scripts/[^:]+):(\d+)\s+(?:sys\.argv|路径构造)', detail)
        if not m2:
            return False
        return False  # sys.argv/路径构造需要 LLM 手动修复

    src_file = m.group(1)
    src_line = int(m.group(2))
    var_name = m.group(3)
    src_abs = os.path.join(skill_dir, src_file)
    paths_abs = os.path.join(skill_dir, "scripts", shared_fname)

    if not os.path.isfile(src_abs):
        return False

    # 1. 从源文件提取定义行
    try:
        with open(src_abs, "r", encoding="utf-8") as f:
            src_lines = f.readlines()
    except Exception:
        return False

    if src_line > len(src_lines):
        return False

    def_line = src_lines[src_line - 1]

    # 2. 创建/更新共享文件
    paths_dir = os.path.dirname(paths_abs)
    os.makedirs(paths_dir, exist_ok=True)

    shared_basename = shared_fname[:-3]  # 去掉 .py

    if os.path.isfile(paths_abs):
        with open(paths_abs, "r", encoding="utf-8") as f:
            paths_content = f.read()
    else:
        # 创建标准骨架
        skill_name = os.path.basename(os.path.abspath(skill_dir))
        paths_content = (
            '"""\n'
            f'{shared_fname} — 路径集中管理\n'
            '只包含路径常量和路径推导函数，不包含任何业务逻辑。\n'
            '"""\n'
            'import os\n'
            'from pathlib import Path\n\n'
            '_SCRIPT_DIR = Path(__file__).resolve().parent\n'
            'SKILL_DIR    = _SCRIPT_DIR.parent\n'
            'SKILLS_ROOT  = SKILL_DIR.parent\n'
            'SKILL_NAME   = SKILL_DIR.name\n\n'
            'STD_ROOT     = SKILLS_ROOT / ".standardization"\n'
            'STD_DIR      = STD_ROOT / SKILL_NAME\n'
            'DATA_DIR     = STD_DIR / "data"\n'
            'OUTPUTS_DIR  = STD_DIR / "outputs"\n'
            'BACKUP_DIR   = STD_DIR / "backup"\n'
            'CACHE_DIR    = STD_DIR / "cache"\n'
            'TEMP_DIR     = STD_DIR / "temp"\n\n'
        )

    # 检查变量是否已存在于共享文件
    if f"{var_name} " in paths_content or f"{var_name}=" in paths_content:
        pass  # 已存在，跳过
    else:
        # 追加定义行
        paths_content += f"{def_line.strip()}\n"

    # 原子写入共享文件
    tmp = paths_abs + ".tmp." + os.urandom(4).hex()
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(paths_content)
        os.replace(tmp, paths_abs)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        return False

    # 3. 替换源文件：删除定义行 + 添加 import
    new_src_lines = []
    for i, line in enumerate(src_lines):
        if i == src_line - 1:
            continue  # 跳过定义行
        new_src_lines.append(line)

    # 在文件顶部添加 import（在第一行非注释/非空行前）
    insert_pos = 0
    for i, line in enumerate(new_src_lines):
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and not stripped.startswith('"""'):
            insert_pos = i
            break
        if stripped.startswith('"""') or stripped.startswith("'''"):
            continue

    # 检查是否已有 from X import，有则追加变量名
    import_line_idx = -1
    for i, line in enumerate(new_src_lines):
        if re.match(rf'from\s+(?:scripts\.)?{re.escape(shared_basename)}\s+import', line.strip()):
            import_line_idx = i
            break

    if import_line_idx >= 0:
        existing = new_src_lines[import_line_idx].strip()
        if var_name not in existing:
            new_src_lines[import_line_idx] = existing + ", " + var_name + "\n"
    else:
        new_src_lines.insert(insert_pos, f"from {shared_basename} import {var_name}\n")

    # 原子写入源文件
    tmp2 = src_abs + ".tmp." + os.urandom(4).hex()
    try:
        with open(tmp2, "w", encoding="utf-8") as f:
            f.writelines(new_src_lines)
        os.replace(tmp2, src_abs)
    except Exception:
        if os.path.exists(tmp2):
            os.unlink(tmp2)
        return False

    # 4. 验证：编译共享文件和源文件
    try:
        import py_compile
        py_compile.compile(paths_abs, doraise=True)
        py_compile.compile(src_abs, doraise=True)
    except py_compile.PyCompileError:
        # 验证失败 → 回滚
        if os.path.exists(tmp):
            os.replace(tmp, paths_abs)
        if os.path.exists(tmp2):
            os.replace(tmp2, src_abs)
        return False

    return True
