#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
skill_audit/artifact_checker.py — 产出物路径检查函数 (R-11, R-12)
"""

import os
import re
import json
from pathlib import Path

from .utils import (
    _KNOWN_ROOT_FILES, _KNOWN_STANDARD_DIRS, _ARTIFACT_DIR_CLASSIFY,
    _ARTIFACT_EXTS_COMPREHENSIVE, _ROOT_ARTIFACT_EXTS, _ROOT_EXT_CLASSIFY,
    _ARTIFACT_WRITE_PATTERNS, _HARDCODED_PATH_RE, _PATH_EXCLUDE_RE,
    _is_hardcoded_path, _classify_artifact, _classify_artifact_by_ext,
    _extract_path_literal, _find_skills_dir, _is_asset_dir,
)
from ._path_detector import _find_shared_path_file


def check_artifact_paths(filepath, content, fm, body, skill_dir=None, **kw):
    """R-11: 全面产出物路径检测（铁律4）。
    
    v2.99.0: scripts/ 扫描范围收缩到共享路径文件（如果存在）。
    """
    if not skill_dir or not os.path.isdir(skill_dir):
        return {"passed": True, "detail": "跳过：无法确定技能目录", "skip": True}

    violations = []
    script_exts = {".py", ".sh", ".bat", ".ps1"}

    # ── 1. scripts/ 扫描 ──
    scripts_dir = os.path.join(skill_dir, "scripts")
    if os.path.isdir(scripts_dir):
        # ★ v2.99.0: 检测共享路径文件，若存在则只扫描该文件
        shared_file, _shared_vars, _ = _find_shared_path_file(scripts_dir)
        scan_targets = [shared_file] if shared_file else sorted(os.listdir(scripts_dir))

        for fname in scan_targets:
            if not fname:
                continue
            fpath = os.path.join(scripts_dir, fname)
            ext = os.path.splitext(fname)[1].lower()
            if ext not in script_exts or not os.path.isfile(fpath):
                continue

            try:
                with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                    script_lines = f.readlines()
            except Exception:
                continue

            rel_path = os.path.join("scripts", fname)

            if fname in ("artifact_checker.py", "data_dir_checker.py"):
                continue  # 检查器自身，跳过自检 (R-11 误报防护)
            if ext == ".py":
                _check_python_artifact_paths_v2(rel_path, script_lines, violations)
            elif ext in (".sh", ".bat", ".ps1"):
                _check_shell_artifact_paths_v2(rel_path, script_lines, violations)

    # ── 2. 根目录文件扫描 ──
    _check_root_artifact_files(skill_dir, violations)

    # ── 3. 非标准子目录扫描 ──
    _check_artifact_directories(skill_dir, violations)

    # ── 4. 交叉引用追踪 ──
    if violations:
        _trace_cross_references(skill_dir, violations)

    # ── 5. [v2.10.0] 标准化路径磁盘验证 ──
    _verify_standardization_paths(skill_dir, violations)

    # ── 6. [v2.3.2] SKILL.md 正文路径冗余扫描 ──
    _check_body_paths(body, violations)

    if violations:
        results = []
        for v in violations:
            detail = f"{v['source']}  产出 \"{v['path_literal']}\" — 应迁至 {v['suggestion']}"
            if v.get("cross_refs"):
                detail += f"\n    [!] 关联引用 ({len(v['cross_refs'])}处): {', '.join(v['cross_refs'])}"
            results.append({
                "passed": False,
                "detail": detail,
                "fix": {"key": "artifact_paths", "value": True,
                        "location": f"{skill_dir} (scripts/ 及根目录)",
                        "violations": [v],
                        "operation": "将所有违规产出物路径迁移至 skills/.standardization/<skill>/{outputs,data,cache,temp}/ 目录",
                        "verification": "重新运行 audit_skill()，确认 R-11 passed"}
            })
        return results
    else:
        return {"passed": True, "detail": "未发现产出物路径违规（scripts/ + 根目录 + 子目录均通过）"}


def _check_root_artifact_files(skill_dir, violations):
    """根目录白名单检查（R-11）
    根目录允许：
      - 白名单文件（_KNOWN_ROOT_FILES）
      - 标准目录 scripts/, references/
      - 被脚本引用的功能数据目录
      - 非产出物/数据/缓存的隐藏目录
    产出物/数据/缓存类隐藏目录仍然报违规。
    """
    try:
        root_entries = os.listdir(skill_dir)
    except OSError:
        return

    # 读取 external_data_dir 声明
    fm = {}
    fm_path = os.path.join(skill_dir, "SKILL.md")
    if os.path.isfile(fm_path):
        try:
            from .utils import parse_simple_yaml_frontmatter
            content_fm = open(fm_path, "r", encoding="utf-8").read()
            fm, _ = parse_simple_yaml_frontmatter(content_fm)
        except Exception:
            fm = {}
    external_data = fm.get("external_data_dir", False)

    _ROOT_ALLOWED_DIRS = {"scripts", "references"}

    for entry in sorted(root_entries):
        fpath = os.path.join(skill_dir, entry)
        if os.path.isfile(fpath):
            if entry in _KNOWN_ROOT_FILES:
                continue
            violations.append({
                "source": f"ROOT/{entry}",
                "path_literal": entry,
                "suggestion": "删除此文件（根目录只允许白名单文件）",
            })
        elif os.path.isdir(fpath):
            if entry in _ROOT_ALLOWED_DIRS:
                continue
            # 隐藏目录：不盲目跳过，检查是否含产出物/数据/缓存
            if entry.startswith("."):
                # 是被脚本引用的功能数据？→放过
                if _is_asset_dir(skill_dir, entry):
                    continue
                # 否则扫描内容，有产出物仍报违规
                _scan_unknown_dir(skill_dir, entry, fpath, violations)
                continue
            # 普通目录：交叉引用检查
            if _is_asset_dir(skill_dir, entry):
                continue
            violations.append({
                "source": f"ROOT/{entry}/",
                "path_literal": entry + "/",
                "suggestion": "迁至 scripts/ 或数据目录，或删除",
            })

def _check_artifact_directories(skill_dir, violations):
    """非标准子目录扫描"""
    try:
        root_entries = sorted(os.listdir(skill_dir))
    except OSError:
        return

    for entry in root_entries:
        entry_path = os.path.join(skill_dir, entry)
        if not os.path.isdir(entry_path):
            continue
        if entry in _KNOWN_STANDARD_DIRS:
            continue
        if entry.startswith(".") and entry not in _ARTIFACT_DIR_CLASSIFY:
            continue

        classification = _ARTIFACT_DIR_CLASSIFY.get(entry.lower())
        if classification:
            cat, desc = classification
            _scan_dir_recursive(skill_dir, entry, entry_path, cat, violations)
        else:
            _scan_unknown_dir(skill_dir, entry, entry_path, violations)

    # 深度扫描：检查 scripts/ 和 references/ 下的非标准子目录
    for parent_dir_name in ("scripts", "references"):
        parent_path = os.path.join(skill_dir, parent_dir_name)
        if not os.path.isdir(parent_path):
            continue
        try:
            sub_entries = sorted(os.listdir(parent_path))
        except OSError:
            continue
        for sub in sub_entries:
            sub_path = os.path.join(parent_path, sub)
            if not os.path.isdir(sub_path):
                continue
            if sub in _KNOWN_STANDARD_DIRS:
                continue
            classification = _ARTIFACT_DIR_CLASSIFY.get(sub.lower())
            if classification:
                cat, _desc = classification
                rel_parent = f"{parent_dir_name}/{sub}"
                _scan_dir_recursive(skill_dir, rel_parent, sub_path, cat, violations)


def _scan_dir_recursive(skill_dir, rel_dir, dir_path, category, violations):
    """递归扫描一个产出物目录"""
    try:
        for root, dirs, files in os.walk(dir_path):
            dirs[:] = [d for d in dirs if d != "__pycache__"]

            for fname in sorted(files):
                if fname in (".gitkeep", ".gitignore"):
                    continue

                violations.append({
                    "source": f"DIR/{rel_dir}/{fname}",
                    "path_literal": f"{rel_dir}/{fname}",
                    "suggestion": f"skills/.standardization/<skill>/{category}/{fname}",
                })
    except OSError:
        return


def _is_asset_dir(skill_dir, dir_name):
    """检查目录是否被 scripts/ 下的脚本硬编码引用（是 -> 功能数据，非产出物）"""
    scripts_dir = os.path.join(skill_dir, "scripts")
    if not os.path.isdir(scripts_dir):
        return False
    patterns = [
        f'"{dir_name}/',
        f"'{dir_name}/",
        f'"{dir_name}\\\\',
        f"'{dir_name}\\\\",
        f'"{dir_name}"',
        f"'{dir_name}'",
        f"os.path.join.*{dir_name}",
    ]
    try:
        for fname in sorted(os.listdir(scripts_dir)):
            if not fname.endswith(".py"):
                continue
            fpath = os.path.join(scripts_dir, fname)
            if not os.path.isfile(fpath):
                continue
            try:
                with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
            except Exception:
                continue
            for pat in patterns:
                if pat in content:
                    return True
    except OSError:
        pass
    return False


def _scan_unknown_dir(skill_dir, entry, entry_path, violations):
    """扫描未知目录名"""
    try:
        entries = sorted(os.listdir(entry_path))
    except OSError:
        return

    artifact_files = []
    is_script_dir = False

    for sub in entries:
        sub_path = os.path.join(entry_path, sub)
        if os.path.isfile(sub_path):
            ext = os.path.splitext(sub)[1].lower()
            if ext in _ARTIFACT_EXTS_COMPREHENSIVE:
                artifact_files.append(sub)
            if ext in (".py", ".sh", ".bat", ".ps1"):
                is_script_dir = True

    if is_script_dir and not artifact_files:
        return

    if artifact_files:
        # 交叉引用检查：目录被脚本硬编码引用则视为功能数据，跳过
        if _is_asset_dir(skill_dir, entry):
            return
        cat = "outputs"
        for sub in artifact_files:
            violations.append({
                "source": f"DIR/{entry}/{sub}",
                "path_literal": f"{entry}/{sub}",
                "suggestion": f"skills/.standardization/<skill>/{cat}/{sub}",
            })


def _check_python_artifact_paths_v2(rel_path, script_lines, violations):
    """[v2.11.0] Check Python script for artifact path violations"""
    for i, line in enumerate(script_lines, 1):
        stripped = line.strip()
        if stripped.startswith("#") or not stripped:
            continue
        if stripped.startswith("import ") or stripped.startswith("from "):
            continue
        # _data_dir / _data_dir_for 函数返回标准化路径，不触发产出物违规
        if "_data_dir" in stripped:
            continue
        # DATA_DIR 是全局标准化路径变量
        if "DATA_DIR" in stripped:
            continue
        # outputs_dir / report_dir / config_path 等变量由 _data_dir_for 赋值，路径已标准化
        if "outputs_dir" in stripped or "report_dir" in stripped:
            continue
        # 函数内局部变量，但上游赋值来自 _data_dir / DATA_DIR（如 d, cfg_dir, bpath）
        if "_flow_state_path" in stripped or "config_path" in stripped:
            continue
        # 已知标准化路径变量的常见命名（由 _data_dir / DATA_DIR 赋值）
        _std_path_vars = ["bpath", "cpath", "d,", "d)", "d.", "cfg_dir", "report_dir", "outputs_dir"]
        if any(v in stripped for v in _std_path_vars):
            continue

        for pat in _ARTIFACT_WRITE_PATTERNS:
            m = pat.search(stripped)
            if m:
                target = m.group(1)

                # [R-11 误报防护] 模式匹配类误报检查
                comment_pos = stripped.find("#")
                path_start = m.start(1) if m.group(1) else -1
                if comment_pos != -1 and path_start > comment_pos:
                    continue  # 路径在注释里

                if ".standardization" in stripped.lower() or "standardization" in stripped.lower():
                    continue
                if '"r"' in stripped or "'r'" in stripped:
                    continue

                # 成员检查误报
                if " in [" in stripped or " in (" in stripped:
                    continue

                # 路径查找误报
                _LOOKUP_FUNCS2 = ("os.path.exists(", "os.path.isfile(", "os.path.isdir(",
                                  "startswith(", "endswith(", "shebang")
                if any(fn in stripped for fn in _LOOKUP_FUNCS2):
                    continue

                path_literal = _extract_path_literal(stripped, target)
                if "/" in target:
                    dir_part = target.split("/")[0]
                    cat = _classify_artifact(dir_part)
                    filename = target.split("/")[-1]
                    if "." in filename:
                        suggestion = f"skills/.standardization/<skill>/{cat}/{filename}"
                    else:
                        suggestion = f"skills/.standardization/<skill>/{cat}/{target}"
                elif "." in target:
                    cat = _classify_artifact(target)
                    suggestion = f"skills/.standardization/<skill>/{cat}/{target}"
                else:
                    cat = _classify_artifact(target)
                    suggestion = f"skills/.standardization/<skill>/{cat}/"

                violations.append({
                    "source": f"{rel_path}:{i}",
                    "path_literal": path_literal,
                    "suggestion": suggestion,
                })
                break

        # [_data_dir 豁免] 标准化路径变量不触发硬编码路径警告
        _std_path_vars = ["_data_dir", "DATA_DIR", "outputs_dir", "report_dir", "bpath", "cpath", "cfg_dir"]
        if any(v in stripped for v in _std_path_vars):
            continue

        # Generic hardcoded path detection
        # [R-11 误报防护] 有足够的证据确认是误报时跳过，但真正的写入操作不跳过
        for m in _HARDCODED_PATH_RE.finditer(stripped):
            # 1. 行内注释检查：如果路径只在 # 后面的注释里，跳过
            comment_pos = stripped.find("#")
            path_start = m.start(1)
            if comment_pos != -1 and path_start > comment_pos:
                continue  # 路径在注释里，是误报

            if "sys.path" in stripped:
                continue

            path_str = m.group(1)
            if not _is_hardcoded_path(path_str):
                continue
            if ".standardization" in path_str.lower() or "standardization" in path_str.lower():
                continue

            # 2. 成员检查误报：路径在 in [...) 或 in (...) 表达式中（模式匹配）
            # 证据：行中包含 " in [" 或 " in (" 且该路径在列表中
            if " in [" in stripped or " in (" in stripped:
                # 进一步检查：路径是否在字符串列表中（如 p in ['/usr/local/bin', '~/bin']）
                # 有足够证据确认是模式匹配，跳过
                continue

            # 3. 路径查找误报：路径用于 os.path.exists/isfile/isdir、startswith/endswith 等检查
            _LOOKUP_FUNCS = ("os.path.exists(", "os.path.isfile(", "os.path.isdir(",
                             "startswith(", "endswith(", "os.path.exists(",
                             "pathlib.Path(", "Path(")
            if any(fn in stripped for fn in _LOOKUP_FUNCS):
                # 路径用于查找/检查，不是产出物路径，跳过
                continue

            # 4. shebang 检查误报
            if "shebang" in stripped.lower() or "~//bin" in stripped or "~/bin" in stripped:
                continue
            basename = os.path.basename(path_str.rstrip("/\\"))
            if basename and "." in basename:
                cat = _classify_artifact(basename)
                suggestion = f"skills/.standardization/<skill>/{cat}/{basename}"
            else:
                cat = "data"
                suggestion = f"skills/.standardization/<skill>/{cat}/"
            violations.append({
                "source": f"{rel_path}:{i}",
                "path_literal": path_str,
                "suggestion": suggestion,
            })


def _check_shell_artifact_paths_v2(rel_path, script_lines, violations):
    """[v2.11.0] Check Shell scripts for all hardcoded paths."""
    for i, line in enumerate(script_lines, 1):
        stripped = line.strip()
        if stripped.startswith("#") or stripped.startswith("::") or not stripped:
            continue

        for m in _HARDCODED_PATH_RE.finditer(stripped):
            path_str = m.group(1)
            if not _is_hardcoded_path(path_str):
                continue
            if ".standardization" in path_str.lower() or "standardization" in path_str.lower():
                continue
            basename = os.path.basename(path_str.rstrip("/\\"))
            if basename and "." in basename:
                cat = _classify_artifact(basename)
                suggestion = f"skills/.standardization/<skill>/{cat}/{basename}"
            else:
                cat = "data"
                suggestion = f"skills/.standardization/<skill>/{cat}/"
            violations.append({
                "source": f"{rel_path}:{i}",
                "path_literal": path_str,
                "suggestion": suggestion,
            })

        # Legacy artifact dir check（已合并到上方 _ARTIFACT_WRITE_PATTERNS 检查，跳过）
        continue  # noqa: 296 遗留死代码，变量已废弃


def _trace_cross_references(skill_dir, violations):
    """反向搜索整个 skill 目录，找出引用每个违规路径的关联文件。"""
    search_patterns = list(set(v["path_literal"] for v in violations))

    text_exts = {".md", ".json", ".yaml", ".yml", ".txt", ".cfg", ".toml", ".ini", ".html"}
    searchable_files = []

    for root, dirs, files in os.walk(skill_dir):
        dirs[:] = [d for d in dirs if d not in ("__pycache__", ".git")]
        rel_root = os.path.relpath(root, skill_dir).replace("\\", "/")
        if rel_root == ".":
            rel_root = ""

        if rel_root.startswith("scripts") or rel_root == "scripts":
            continue

        for fname in files:
            ext = os.path.splitext(fname)[1].lower()
            if ext not in text_exts:
                continue
            fpath = os.path.join(root, fname)
            rel = os.path.join(rel_root, fname).replace("\\", "/") if rel_root else fname
            searchable_files.append((rel, fpath))

    pattern_to_refs = {}

    for rel, fpath in searchable_files:
        try:
            with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                file_lines = f.readlines()
        except Exception:
            continue

        for i, line in enumerate(file_lines, 1):
            for pattern in search_patterns:
                if pattern in line:
                    pattern_to_refs.setdefault(pattern, []).append(f"{rel}:{i}")

    for v in violations:
        refs = pattern_to_refs.get(v["path_literal"], [])
        refs = [r for r in refs if r != v["source"] and r != v["source"].replace("ROOT/", "")]
        if refs:
            v["cross_refs"] = refs


def _verify_standardization_paths(skill_dir, violations):
    """[v2.10.0] 验证脚本中声称的 skills/.standardization/ 路径在磁盘上真实存在。"""
    scripts_dir = os.path.join(skill_dir, "scripts")
    if not os.path.isdir(scripts_dir):
        return

    skills_dir = _find_skills_dir(skill_dir)
    std_re = re.compile(r'\.standardization/([^"\')\s,。，；：！？、…—）】」』%]+)')

    for fname in sorted(os.listdir(scripts_dir)):
        fpath = os.path.join(scripts_dir, fname)
        ext = os.path.splitext(fname)[1].lower()
        if ext not in (".py", ".sh", ".bat", ".ps1"):
            continue
        if not os.path.isfile(fpath):
            continue
        try:
            with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                lines = f.readlines()
        except Exception:
            continue

        rel = os.path.join("scripts", fname)
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            matches = std_re.findall(stripped)
            for matched_path in matches:
                if "<" in matched_path or "{" in matched_path or matched_path.startswith("([^"):
                    continue
                full_rel = ".standardization/" + matched_path
                dir_part = "/".join(full_rel.split("/")[:-1]) if "." in full_rel.split("/")[-1] else full_rel
                abs_dir = os.path.join(skills_dir, dir_part.replace("/", os.sep))
                if not os.path.exists(abs_dir):
                    violations.append({
                        "source": rel + ":" + str(i),
                        "path_literal": full_rel,
                        "suggestion": "directory missing: " + abs_dir + ", please create it",
                    })


def check_external_data_dir(filepath, content, fm, body, skill_dir=None, **kw):
    """R-12: External data directory path validation."""
    if not skill_dir or not os.path.isdir(skill_dir):
        return {"passed": True, "detail": "skip: cannot determine skill dir", "skip": True}

    dirname = os.path.basename(os.path.abspath(skill_dir))
    violations = []
    expected_pattern = ".standardization/" + dirname + "/"

    # 1. scan shared file (or scripts/) for data dir definitions
    # ★ v2.99.0: 只检查共享路径文件中的声明，不扫所有脚本
    scripts_dir = os.path.join(skill_dir, "scripts")
    data_dir_vars = []
    _DATA_VAR_RE = re.compile(
        r'^([A-Za-z_]*?(?:DATA|STORAGE|DB|CACHE|CONFIG)[A-Za-z_]*?(?:_DIR|_PATH|_RAW))\s*=\s*(.+)$'
    )

    if os.path.isdir(scripts_dir):
        shared_file, _shared_vars, _ = _find_shared_path_file(scripts_dir)
        scan_targets = [shared_file] if shared_file else sorted(os.listdir(scripts_dir))

        for fname in scan_targets:
            if not fname:
                continue
            fpath = os.path.join(scripts_dir, fname)
            if not os.path.isfile(fpath):
                continue
            ext = os.path.splitext(fname)[1].lower()
            if ext not in (".py", ".sh", ".bat", ".ps1"):
                continue
            try:
                with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                    for lineno, line in enumerate(f, 1):
                        stripped = line.strip()
                        m = _DATA_VAR_RE.match(stripped)
                        if m:
                            val = m.group(2).strip()
                            path_val = val.strip().strip('"').strip("'")
                            data_dir_vars.append((
                                os.path.join("scripts", fname),
                                m.group(1),
                                path_val,
                                lineno
                            ))
            except Exception:
                continue

    # 1.5 [v2.38.9] check scripts that reference .standardization/ but lack proper DATA_DIR
    # ★ v2.99.0: 有共享文件时跳过此检查（共享文件已处理），无共享文件时全量扫
    if not data_dir_vars:
        scripts_seen = {rel_file for rel_file, _, _, _ in data_dir_vars}
        for fname in sorted(os.listdir(scripts_dir)):
            fpath = os.path.join(scripts_dir, fname)
            if not os.path.isfile(fpath):
                continue
            ext = os.path.splitext(fname)[1].lower()
            if ext not in (".py", ".sh", ".bat", ".ps1"):
                continue
            rel = os.path.join("scripts", fname)
            if rel in scripts_seen:
                continue
            R12_WHITELIST = {
                os.path.join("scripts", "artifact_checker.py"),
                os.path.join("scripts", "creator.py"),
                os.path.join("scripts", "fix.py"),
                os.path.join("scripts", "migrator.py"),
                os.path.join("scripts", "progress_manager.py"),
                os.path.join("scripts", "refactor.py"),
                os.path.join("scripts", "updater.py"),
                os.path.join("scripts", "utils.py"),
            }
            if rel in R12_WHITELIST:
                continue
            try:
                with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                    sc = f.read()
            except Exception:
                continue
            if ".standardization" in sc:
                violations.append({
                    "source": rel,
                    "var_name": "(missing DATA_DIR)",
                    "path_value": f"references .standardization/ via {fname}",
                    "expected": "should declare DEFAULT_DATA_DIR_RAW + DATA_DIR",
                    "detail": f"{fname} references .standardization/ paths but lacks a variable named with DATA|STORAGE|DB|CACHE|CONFIG + _DIR/_PATH. "
                           "【推荐写法】添加 DEFAULT_DATA_DIR_RAW = \"skills/.standardization/<skill>/data/\" 和 "
                           "DATA_DIR = SKILL_DIR.parent / \".standardization\" / \"<skill>\" / \"data\"",
                })

    # 2. check paths conform to standardization/<skill-name>/ convention
    #     path_val 可能是 Python 表达式（如 SKILL_DIR.parent / ".standardization" / "skill" / "data"）
    #     不直接用 os.path.normpath 比较（会因引用/拼接操作符而失败），改为检查
    #     .standardization + skill 名称是否同时出现
    # ★ v2.101.7: 如果 path_val 是变量推导（如 STD_DIR / "data"），
    #   检查同一文件中是否有关联变量包含 .standardization，有则放行
    for rel_file, var_name, path_val, lineno in data_dir_vars:
        if not path_val:
            continue
        pv_lower = path_val.lower()
        has_std = ".standardization" in pv_lower
        has_skill = dirname.lower() in pv_lower
        if not (has_std and has_skill):
            # 检查是否为 pathlib 推导路径：同一文件有其他变量包含 .standardization
            is_derived = False
            source_file = os.path.join(skill_dir, rel_file)
            if os.path.isfile(source_file):
                try:
                    with open(source_file, "r", encoding="utf-8") as _f:
                        _src = _f.read()
                    # 查找包含 .standardization 字面量的其他变量声明
                    if re.search(r'=\s*(?:SKILLS_ROOT|SKILL_DIR).*?\.standardization', _src, re.MULTILINE):
                        is_derived = True
                    elif re.search(r'"[^"]*\.standardization[^"]*"', _src) or \
                         re.search(r"'[^']*\.standardization[^']*'", _src):
                        is_derived = True
                except Exception:
                    pass
            if not is_derived:
                violations.append({
                    "source": rel_file + ":" + str(lineno),
                    "var_name": var_name,
                    "path_value": path_val,
                    "expected": ".standardization/" + dirname + "/data/",
                    "detail": var_name + "=" + path_val + " violates skills/.standardization/<skill>/ convention (same as R-11). "
                           "【推荐写法】变量名含 DATA 的那行直接赋值合规字面量，"
                           "再用另一个不含关键词的变量（如 _data_dir_abs）计算绝对路径。",
                })

    # 3. check _meta.json has data_dir field
    meta_file = os.path.join(skill_dir, "_meta.json")
    meta_has_data_dir = False
    meta_data_dir = None
    if os.path.isfile(meta_file):
        try:
            with open(meta_file, "r", encoding="utf-8") as f:
                meta = json.load(f)
            if "data_dir" in meta:
                meta_has_data_dir = True
                meta_data_dir = meta["data_dir"]
        except Exception:
            pass

    # SKILL.md frontmatter data_dir (authoritative source for external data usage)
    skill_md_data_dir = fm.get("data_dir") if fm else None

    if (data_dir_vars or skill_md_data_dir) and not meta_has_data_dir:
        src_parts = []
        if data_dir_vars:
            src_parts.append("scripts/ define data dir variable")
        if skill_md_data_dir:
            src_parts.append("SKILL.md declares data_dir")
        source_desc = ", ".join(src_parts)
        violations.append({
            "source": "_meta.json",
            "var_name": "data_dir",
            "path_value": "(missing)",
            "expected": "should add data_dir field",
            "detail": f"_meta.json missing data_dir field ({source_desc})",
        })

    # 3-b. [v2.95.6] meta.json 声明了 data_dir，但脚本未引用 .standardization
    #       → 扫描写入操作，提取路径清单，区分硬编码/CLI模式
    if meta_has_data_dir and not data_dir_vars:
        has_any_standardization_ref = False
        write_ops = []  # [(rel_file, lineno, mode, path_desc, context)]
        has_cli_mode = False
        if os.path.isdir(scripts_dir):
            for fname in sorted(os.listdir(scripts_dir)):
                fpath = os.path.join(scripts_dir, fname)
                if not os.path.isfile(fpath):
                    continue
                ext = os.path.splitext(fname)[1].lower()
                if ext not in (".py", ".sh", ".bat", ".ps1"):
                    continue
                try:
                    with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                        text = f.read()
                        lines = text.splitlines(keepends=False)
                except Exception:
                    continue
                for lineno, line in enumerate(lines, 1):
                    stripped = line.strip()
                    if ".standardization" in stripped:
                        has_any_standardization_ref = True
                    # 检测写入操作：write_text / open("...", "w"/"a"/"w+"/"a+")
                    if ".write_text(" in stripped or re.search(r'open\s*\(', stripped):
                        is_write = ".write_text(" in stripped
                        is_open = re.search(r'open\s*\(', stripped)
                        if not is_write and is_open:
                            # 检查 open 的 mode 参数是否有 w/a
                            if not re.search(r'["\']([wa]+)["\']', stripped):
                                continue
                        # 判断模式：硬编码字面量 vs CLI 参数 vs 变量路径
                        has_literal_path = bool(re.search(r'["\'][^"\']+\.(json|txt|md|csv)["\']', stripped))
                        has_sys_argv = "sys.argv" in stripped
                        has_variable_path = not has_literal_path and not has_sys_argv
                        if has_sys_argv:
                            mode = "CLI 参数"
                            path_desc = "sys.argv[N]"
                            has_cli_mode = True
                        elif has_literal_path:
                            lp = re.search(r'["\']([^"\']+\.[^"\']+)["\']', stripped)
                            mode = "硬编码"
                            path_desc = lp.group(1) if lp else "(字面量路径)"
                        else:
                            mode = "变量路径"
                            path_desc = "(变量, 运行时确定)"
                        write_ops.append((os.path.join("scripts", fname), lineno, mode, path_desc, stripped[:120]))
        if not has_any_standardization_ref and write_ops:
            detail_lines = [
                f"_meta.json 声明了 data_dir={meta_data_dir}，但所有脚本中未引用 .standardization/",
                "实际写入路径清单（按模式分类）：",
                "",
                "| 路径模式 | 写入路径描述 | 脚本 | 行 | 代码上下文 |",
                "|---|----|----|----|------|",
            ]
            for rel_file, lineno, mode, path_desc, ctx in write_ops:
                safe_ctx = ctx.replace("|", "\\|")
                detail_lines.append(f"| {mode} | {path_desc} | {rel_file} | {lineno} | {safe_ctx} |")
            if has_cli_mode:
                detail_lines.extend([
                    "",
                    "⚠️ 检测到 CLI 参数传路径模式（sys.argv）。这是 CLI 技能的标准数据管理方式，",
                    "   但需要按照以下三层模式才能正确使用 data_dir：",
                    "",
                    "   第1层: 在脚本顶层声明 DATA_DIR 常量",
                    f"          DATA_DIR = Path(__file__).parent.parent.parent / \".standardization\" / \"{dirname}\" / \"data\"",
                    "",
                    "   第2层: CLI 参数默认值指向 DATA_DIR",
                    "          parser.add_argument('--state-path', default=str(DATA_DIR / 'novel_state.json'))",
                    "          或: sp = sys.argv[2] if len(sys.argv) > 2 else str(DATA_DIR / 'novel_state.json')",
                    "",
                    "   第3层: 保留 CLI 覆写能力",
                    "          python script.py --state-path /path/to/user/novel_state.json",
                    "",
                    f"   完整修改指引见 references/data_dir_guide.md 或参考 skill-standardization 自身的 cleanup_manager.py",
                ])
            else:
                detail_lines.extend([
                    "",
                    "修复方向：",
                    f"  B) 在脚本中声明 DATA_DIR 常量指向 .standardization/{dirname}/data/",
                    "     并将写入路径改为 DATA_DIR 下的子目录",
                ])
            violations.append({
                "source": "_meta.json",
                "var_name": "data_dir",
                "path_value": meta_data_dir,
                "expected": ".standardization/" + dirname + "/",
                "detail": "\n".join(detail_lines),
            })

    # 4. check _meta.json data_dir matches code path
    #     path_val 可能是 Python 表达式（含空格/引号/运算符），只有字面路径（无空格/引号）才可比
    if meta_has_data_dir and data_dir_vars:
        skills_root = _find_skills_dir(skill_dir)
        meta_raw = os.path.join(skills_root, str(meta_data_dir))
        meta_abs = os.path.normpath(meta_raw).rstrip(os.sep).lower()
        for _, _, path_val, _ in data_dir_vars:
            if path_val and ('"' not in path_val) and ("'" not in path_val) and (" " not in path_val):
                code_raw = os.path.join(skills_root, str(path_val))
                code_abs = os.path.normpath(code_raw).rstrip(os.sep).lower()
                if code_abs != meta_abs:
                    violations.append({
                        "source": "_meta.json vs " + data_dir_vars[0][0],
                        "var_name": "data_dir",
                        "path_value": meta_data_dir,
                        "expected": path_val,
                        "detail": "_meta.json data_dir=" + str(meta_data_dir) + " != code " + data_dir_vars[0][1] + "=" + path_val,
                    })
                    break

    # 5. [v2.10.0] disk existence check
    uses_external_data = bool(data_dir_vars) or meta_has_data_dir or bool(skill_md_data_dir)
    if uses_external_data:
        skills_dir = _find_skills_dir(skill_dir)
        expected_disk_path = os.path.join(skills_dir, ".standardization", dirname, "data")
        if not os.path.isdir(expected_disk_path):
            violations.append({
                "source": "DISK",
                "var_name": "disk",
                "path_value": expected_disk_path,
                "expected": "directory should exist: " + expected_disk_path,
                "detail": "标准化数据目录不存在: " + expected_disk_path,
            })

        # 6. [v2.36.0] references/*.md 中的数据目录路径检查（仅扫 frontmatter）
    #     .md 文件只检查 frontmatter 的 data_dir 字段，不扫正文（避免代码块示例路径误报）
    refs_dir = os.path.join(skill_dir, "references")
    if os.path.isdir(refs_dir):
        for fname in sorted(os.listdir(refs_dir)):
            if fname == "changelog.md":
                continue
            fpath = os.path.join(refs_dir, fname)
            if not os.path.isfile(fpath):
                continue
            ext = os.path.splitext(fname)[1].lower()
            if ext != ".md":
                continue
            try:
                with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                    md_content = f.read()
                # 只解析 frontmatter
                fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', md_content, re.DOTALL)
                if fm_match:
                    fm_text = fm_match.group(1)
                    for fm_lineno, fm_line in enumerate(fm_text.split('\n'), 1):
                        fm_line = fm_line.strip()
                        if fm_line.startswith('data_dir:'):
                            data_dir_val = fm_line[len('data_dir:'):].strip()
                            # 去掉引号
                            data_dir_val = data_dir_val.strip('"').strip("'") 
                            if data_dir_val and '.standardization/' not in data_dir_val:
                                violations.append({
                                    "source": f"references/{fname}:frontmatter:data_dir",
                                    "var_name": "data_dir",
                                    "path_value": data_dir_val,
                                    "expected": ".standardization/<skill-name>/data/",
                                    "detail": f"references/{fname} frontmatter data_dir='{data_dir_val}' should use .standardization/<skill-name>/data/ convention",
                                })
            except Exception:
                continue
    if violations:
        detail_lines = [f"发现 {len(violations)} 处数据目录路径违规："]
        for v in violations:
            line = f"  {v['source']}  {v['var_name']}={v['path_value']} — {v['detail']}"
            detail_lines.append(line)
        return {
            "passed": False,
            "detail": "\n".join(detail_lines),
            "violations": [{"source": v["source"], "var_name": v["var_name"],
                           "path_value": v["path_value"], "detail": v["detail"]}
                          for v in violations],
            "fix": {"key": "external_data_dir", "value": True,
                     "location": f"{skill_dir} (scripts/ 及 _meta.json)",
                     "operation": "将数据目录统一至 skills/.standardization/<skill>/data/ 规范",
                     "verification": "重新运行 audit_skill()，确认 R-12 passed"},
        }
    else:
        return {"passed": True, "detail": "数据目录路径符合规范（scripts/ + _meta.json 均通过）"}


def fix_external_data_dir(skill_dir):
    """
    R-12 自动修复：
    1. 更新 _meta.json 添加 data_dir 字段
    2. 更新 scripts/*.py 中的数据目录变量
    返回修复数量。
    """
    import re, os, json
    if not skill_dir or not os.path.isdir(skill_dir):
        return 0

    skill_name = os.path.basename(os.path.abspath(skill_dir))
    fixed = 0

    # 1. 更新 _meta.json
    meta_file = os.path.join(skill_dir, "_meta.json")
    meta = {}
    if os.path.isfile(meta_file):
        try:
            with open(meta_file, "r", encoding="utf-8") as f:
                meta = json.load(f)
        except Exception:
            meta = {}
    expected = "skills/.standardization/" + skill_name + "/data/"
    if meta.get("data_dir") != expected:
        meta["data_dir"] = expected
        with open(meta_file, "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)
            f.write("\n")
        fixed += 1
        print("    [OK] 更新 _meta.json: data_dir = " + expected)

    # 2. 更新 scripts/*.py 中的数据目录变量
    scripts_dir = os.path.join(skill_dir, "scripts")
    if not os.path.isdir(scripts_dir):
        return fixed

    for fname in sorted(os.listdir(scripts_dir)):
        fpath = os.path.join(scripts_dir, fname)
        if not os.path.isfile(fpath) or not fname.endswith(".py"):
            continue

        try:
            with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
        except Exception:
            continue

        original = content
        # 匹配：VAR_NAME = Path.home() / "..." / "..."
        pattern = re.compile(
            r'^(s*)([A-Za-z_]+w*(?:DATA|STORAGE|DB|CACHE|CONFIG)[A-Za-z_]*)(s*=\s*Path\.home(s*)((?:\s*/\s*"[^"]+")+))',
            re.MULTILINE
        )
        for m in pattern.finditer(content):
            indent = m.group(1)
            var_name = m.group(2)
            path_parts = re.findall(r'["\']([^"\']*)["\']', m.group(4))
            if not path_parts:
                continue
            # 替换为标准路径
            new_value = 'Path.home() / ".workbuddy" / "skills" / ".standardization" / "' + skill_name + '" / "data"'
            new_line = indent + var_name + " = " + new_value
            content = content[:m.start()] + new_line + content[m.end():]
            fixed += 1
            print("    [OK] 更新 " + fname + ": " + var_name + " → 标准路径")
            break  # 每个文件只修第一个匹配

        if content != original:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(content)

    return fixed


# ────────────────────────────────────────────
# [v2.3.2] SKILL.md 正文路径冗余扫描（R-11）
# 铁律 8 细筛说明：输出含 source=SKILL.md:行号,
# LLM 可据此查看上下文行判断是否为真问题。
# ────────────────────────────────────────────

_KNOWN_BODY_PATH_PATTERNS = {
    'output_dir_desc': {
        'label': '目录描述路径',
        'desc': '正文中描述了输出/数据/安装等目录路径',
    },
    'template_var_path': {
        'label': '模板变量路径',
        'desc': '正文裸写了 {XXX} 模板变量路径',
    },
    'standardization_path': {
        'label': '标准化路径重复',
        'desc': 'skills/.standardization/ 路径已在 _meta.json 声明',
    },
    'abs_win_path': {
        'label': '绝对路径',
        'desc': '正文包含硬编码绝对路径',
    },
}

def _check_body_paths(body, violations):
    """
    R-11 阶段6: 扫描 SKILL.md 正文（不含 frontmatter）中的路径描述。
    
    设计目标：
    - 路径信息应由 _meta.json data_dir + frontmatter 统一管理
    - 正文不应重复描述路径，避免过时/不一致
    - 代码块内的路径示例（```）豁免
    - 引用链接（→ 详见）豁免
    
    铁律 8 二段筛查指引：
    ┌──────────────────────────────────────────────┐
    │ 规则ID: R-11 (body_path)                     │
    │ FAIL原文: SKILL.md:N行 路径描述               │
    │ ─────────────────────────────                 │
    │ LLM判断: 需逐条判断                           │
    │ 真问题条件:                                  │
    │   - 该行是正文描述（列表项/段落），非代码块    │
    │   - 该路径确实已在 _meta.json data_dir 定义   │
    │ 误判条件:                                    │
    │   - 路径在代码块内（``` 未正确追踪）           │
    │   - 该路径引用了外部依赖（如 draw.io 安装路径） │
    │ 处理方式: 删行 / 移入代码块 / 放过             │
    └──────────────────────────────────────────────┘
    """
    if not body or not body.strip():
        return

    lines = body.split('\n')
    in_code_block = False

    path_patterns = [
        (re.compile(
            r'(?:输出目录|数据目录|安装目录|安装路径|导入目录|导出目录|缓存目录|临时目录|工作目录)'
            r'(?:\s*[：:]\s*)(.+?)(?:[。，,；;]|$)'
        ), 'output_dir_desc'),
        (re.compile(r'\{[A-Z_]+\}(?:/[^\s,);。，；、]*)*'), 'template_var_path'),
        (re.compile(r'skills/\.standardization/[^\s,);。，；、:\"]+'), 'standardization_path'),
        (re.compile(r'[A-Za-z]:\\(?:[^\\\s,\");。，、]+\\)*(?:[^\\\s,\");。，、]+)?'), 'abs_win_path'),
    ]

    found_items = []

    for i, line in enumerate(lines):
        stripped = line.strip()

        if stripped.startswith('```'):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        if not stripped or stripped.startswith('#') or stripped.startswith('---'):
            continue
        if stripped.startswith('→') or stripped.startswith('->'):
            continue

        for pat, pat_name in path_patterns:
            for m in pat.finditer(stripped):
                matched = m.group(0).strip()
                if matched in found_items:
                    continue
                found_items.append(matched)

                label = _KNOWN_BODY_PATH_PATTERNS.get(pat_name, {}).get('label', pat_name)
                desc = _KNOWN_BODY_PATH_PATTERNS.get(pat_name, {}).get('desc', '')

                if pat_name == 'output_dir_desc':
                    path_val = m.group(1).strip() if m.lastindex and m.lastindex >= 1 else matched
                    violations.append({
                        "source": "SKILL.md:" + str(i + 1),
                        "path_literal": f"[{label}] {matched}",
                        "suggestion": (
                            "路径信息应在 _meta.json data_dir + frontmatter 中集中定义，"
                            "正文不应重复描述。\n"
                            f"  行内容: {stripped[:120]}\n"
                            f"  命中路径: {path_val}\n"
                            "  处理: 删除此行；若为功能描述需要参考路径，改用引用 _meta.json"
                        ),
                        "body_path": path_val,
                    })
                elif pat_name == 'template_var_path':
                    violations.append({
                        "source": "SKILL.md:" + str(i + 1),
                        "path_literal": f"[{label}] {matched}",
                        "suggestion": (
                            f"模板变量路径应置于代码块（```）内，裸写在正文中导致路径信息分散。\n"
                            f"  行内容: {stripped[:120]}\n"
                            f"  命中: {matched}\n"
                            f"  处理: 若为描述性文本，删除路径部分；若为示例，移入代码块"
                        ),
                        "body_path": matched,
                    })
                elif pat_name == 'standardization_path':
                    violations.append({
                        "source": "SKILL.md:" + str(i + 1),
                        "path_literal": f"[{label}] {matched}",
                        "suggestion": (
                            f"skills/.standardization/ 路径已在 _meta.json data_dir 声明，正文重复。\n"
                            f"  行内容: {stripped[:120]}\n"
                            f"  命中: {matched}\n"
                            f"  处理: 删除此行引用"
                        ),
                        "body_path": matched,
                    })
                elif pat_name == 'abs_win_path':
                    violations.append({
                        "source": "SKILL.md:" + str(i + 1),
                        "path_literal": f"[{label}] {matched}",
                        "suggestion": (
                            f"外部依赖的绝对路径（如 draw.io 安装路径）可保留在正文，"
                            f"但路径字符串建议通过代码常量管理。\n"
                            f"  行内容: {stripped[:120]}\n"
                            f"  命中: {matched}\n"
                            f"  处理: LLM 判断——若是外部依赖引用则放过，若是数据路径则删除"
                        ),
                        "body_path": matched,
                    })
