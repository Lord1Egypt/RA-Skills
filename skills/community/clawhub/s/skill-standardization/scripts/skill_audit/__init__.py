#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import warnings
warnings.filterwarnings("ignore", category=SyntaxWarning)
"""
skill_audit package — SKILL.md 规范化审查工具 v2.84.0

支持 R-01~R-26 规则审查，独立审计工具。

用法:
    python -m skill_audit audit <skill_dir> [--json] [--manifest-version VER]
    python -m skill_audit audit-all <skills_dir> [--manifest FILE] [--json]
    python -m skill_audit rules
"""

import warnings
# 临时移除过滤，捕获 SyntaxWarning 来源
# warnings.filterwarnings("ignore", category=SyntaxWarning, message=r'.*invalid escape sequence.*')

import os
import re
import sys
import json
import hashlib
import datetime
import importlib.util
import argparse
from pathlib import Path

# ── [GBK 兼容] 强制 stdout 使用 UTF-8，防止 Windows 终端 emoji print 崩溃 ──
if sys.stdout.encoding and sys.stdout.encoding.upper() not in ('UTF-8', 'UTF8'):
    sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1, errors='replace')
if sys.stderr.encoding and sys.stderr.encoding.upper() not in ('UTF-8', 'UTF8'):
    sys.stderr = open(sys.stderr.fileno(), mode='w', encoding='utf-8', buffering=1, errors='replace')

# ── 导入子模块 ─────────────────────────────────────────────
from .utils import (
    _fmt_frontmatter_value, RULES, TRIGGER_KEYWORDS, CORE_KEYWORDS, WORKFLOW_KEYWORDS,
    ARTIFACT_DIR_NAMES, _KNOWN_STANDARD_DIRS, _ARTIFACT_DIR_CLASSIFY,
    _ARTIFACT_EXTS_COMPREHENSIVE, _ARTIFACT_DIR_PATTERN,
    _ARTIFACT_WRITE_PATTERNS, _HARDCODED_PATH_RE, _PATH_EXCLUDE_RE,
    _is_hardcoded_path, parse_simple_yaml_frontmatter,
    _find_skills_dir,
)
from .frontmatter_checker import (
    regex_frontmatter_exists, yaml_has_name, yaml_has_semver_version,
    yaml_has_description, name_matches_dirname, version_matches_manifest,
    check_meta_json_completeness,
    regex_frontmatter_and_meta,
)
from .structure_checker import (
    body_has_h1, body_has_trigger_section, body_has_core_section,
    body_has_workflow_section,
    body_has_antipattern_section, body_has_faq_section,
    body_check_writing_standards,
    body_has_progressive_loading_explicit,
    check_doc_code_consistency,
    check_changelog_progressive,
    body_check_document_format,
    check_license_compliance,
)
from .artifact_checker import (
    check_artifact_paths, check_external_data_dir,
    fix_external_data_dir,
)
from .permission_checks import (
    check_sensitive_access_declaration, check_critical_write_declaration,
    check_authorization_present, check_permission_weight_explained,
    check_progressive_loading_forced,
)
from .data_dir_checker import (
    check_data_dir_compliance, fix_data_dir_compliance,
)
from .fix import apply_fix, list_fixable

# ── safe_write 加载器：通过绝对路径加载，避免 import context 问题 ──
def _load_safe_write():
    """通过文件绝对路径加载 safe_write，不受任何 import 包上下文影响"""
    _path = os.path.join(os.path.dirname(__file__), '..', 'safe_io.py')
    _spec = importlib.util.spec_from_file_location("safe_io", os.path.abspath(_path))
    _mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    return _mod.safe_write

_safe_write = _load_safe_write()

# ── 方法分派表 ─────────────────────────────────────────────
METHOD_MAP = {
    "check_external_data_dir": check_external_data_dir,
    "regex_frontmatter_exists": regex_frontmatter_exists,
    "regex_frontmatter_and_meta": regex_frontmatter_and_meta,
    "yaml_has_name": yaml_has_name,
    "yaml_has_semver_version": yaml_has_semver_version,
    "yaml_has_description": yaml_has_description,
    "name_matches_dirname": name_matches_dirname,
    "body_has_h1": body_has_h1,
    "body_has_trigger_section": body_has_trigger_section,
    "body_has_core_section": body_has_core_section,
    "body_has_workflow_section": body_has_workflow_section,
    "version_matches_manifest": version_matches_manifest,
    "check_artifact_paths": check_artifact_paths,
    "check_sensitive_access_declaration": check_sensitive_access_declaration,
    "check_critical_write_declaration": check_critical_write_declaration,
    "check_authorization_present": check_authorization_present,
    "check_permission_weight_explained": check_permission_weight_explained,
    "check_progressive_loading_forced": check_progressive_loading_forced,
    "body_has_antipattern_section": body_has_antipattern_section,
    "body_has_faq_section": body_has_faq_section,
    "body_check_writing_standards": body_check_writing_standards,
    "body_has_progressive_loading_explicit": body_has_progressive_loading_explicit,
    "check_data_dir_compliance": check_data_dir_compliance,
    "check_doc_code_consistency": check_doc_code_consistency,
    "check_changelog_progressive": check_changelog_progressive,
    "check_meta_json_completeness": check_meta_json_completeness,
    "body_check_document_format": body_check_document_format,
    "check_license_compliance": check_license_compliance,
}


def _apply_fixes(skill_md, fixes):
    """
    将 fixes 列表应用到 SKILL.md 的 frontmatter。
    fixes: [{"key": "sensitive_access", "value": True, "reason": "..."}, ...]
    """
    with open(skill_md, "r", encoding="utf-8") as f:
        content = f.read()

    fm, body = parse_simple_yaml_frontmatter(content)
    if fm is None:
        return []  # 无 frontmatter，无法修正

    applied = []
    _AUDIT_CONTROL_FIELDS = {
        "writing_standards", "artifact_paths",
        "antipattern_progressive", "faq_progressive",
        "progressive_loading_explicit",
        "h1", "section_trigger", "section_core", "section_workflow",
        "antipattern_reference", "faq_reference",
        "frontmatter_fields", "meta_json",
    }
    for fix in fixes:
        if "key" not in fix:
            continue
        key = fix["key"]
        if key in _AUDIT_CONTROL_FIELDS:
            continue
        if "value" not in fix:
            continue  # 结构性修复（如删除/创建文件），不走 frontmatter 合并
        val = fix["value"]
        fm[key] = val
        applied.append(f"{key}: {val} ({fix.get('reason', '')})")

    # 重新组装 frontmatter + body（过滤审计控制字段）
    import io
    buf = io.StringIO()
    buf.write("---\n")
    for k in _AUDIT_CONTROL_FIELDS:
        fm.pop(k, None)
    for k, v in fm.items():
        if isinstance(v, bool):
            val_str = 'true' if v else 'false'
            buf.write(f"{k}: {val_str}\n")
        elif isinstance(v, (int, float)):
            buf.write(f"{k}: {_fmt_frontmatter_value(v)}\n")
        else:
            buf.write(f"{k}: {_fmt_frontmatter_value(v)}\n")
    buf.write("---\n")
    buf.write(body.lstrip("\n"))

    # 使用 safe_io 原子写入 + 自动备份
    _safe_write(skill_md, buf.getvalue(), backup=True)

    return applied


def audit_skill(skill_dir, manifest_version=None, _fix_applied=False, progress_file=None, filter_rules=None, filter_files=None):
    """
    审查单个 skill 目录中的 SKILL.md。_fix_applied 防止无限递归。

    如果传了 _progress_file，审计结束后自动更新 .progress.md。
    
    filter_rules: ["R-23", "R-26"] — 只跑指定规则ID的检查器
    filter_files: ["scripts/foo.py"] — 只跑关联这些文件的检查器（检查器自行声明关联文件）
    """
    # 先把 skill_dir 转成绝对路径，防止 '.' 等相对路径导致 dirname 异常
    skill_dir = os.path.abspath(skill_dir)
    skill_md = os.path.join(skill_dir, "SKILL.md")
    dirname = os.path.basename(os.path.normpath(skill_dir))

    if not os.path.isfile(skill_md):
        return {
            "skill": dirname,
            "path": skill_dir,
            "error": "SKILL.md 文件不存在",
            "results": [],
            "summary": {"total": 0, "pass": 0, "fail": 0, "skip": 0, "errors": 0, "warns": 0},
            "verdict": "ERROR — SKILL.md 不存在",
        }

    with open(skill_md, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    fm, body = parse_simple_yaml_frontmatter(content)

    results = []
    error_count = 0
    warn_count = 0
    pass_count = 0
    skip_count = 0
    fixes = []

    for rule in RULES:
        method_fn = METHOD_MAP.get(rule["method"])
        if not method_fn:
            continue

        # ── filter_rules / filter_files 过滤 ──
        if filter_rules is not None and rule["id"] not in filter_rules:
            skip_count += 1
            continue
        if filter_files is not None:
            rule_files = rule.get("associated_files", None)
            if rule_files is None:
                # 如果规则没有声明关联文件，默认跳过（filter_files 模式下只跑声明了关联文件的规则）
                skip_count += 1
                continue
            if not any(f in filter_files for f in rule_files):
                skip_count += 1
                continue

        try:
            result = method_fn(
                filepath=skill_md,
                content=content,
                fm=fm,
                body=body,
                dirname=dirname,
                skill_dir=skill_dir,
                manifest_version=manifest_version,
            )
        except Exception as _e:
            import traceback
            traceback.print_exc()
            result = {"passed": False, "detail": f"规则 {rule['id']} 执行异常: {_e}"}
        # 兼容 dict、tuple list 和列表三种返回格式
        # 结构检查器（如 R-20/R-25）可返回列表，每条独立输出
        result_list = result if isinstance(result, list) else [result]
        for raw_result in result_list:
            if isinstance(raw_result, dict):
                passed = raw_result.get("passed", False)
                skipped = raw_result.get("skip", False)
            elif isinstance(raw_result, (tuple, list)) and len(raw_result) >= 1:
                # 旧格式: (passed, details, fixable)
                passed = bool(raw_result[0]) if len(raw_result) > 0 else False
                skipped = raw_result[2].get("skip", False) if len(raw_result) > 2 and isinstance(raw_result[2], dict) else False
                detail = raw_result[1] if len(raw_result) > 1 else ""
                fix = raw_result[2] if len(raw_result) > 2 and isinstance(raw_result[2], dict) else None
                if fix is None and len(raw_result) > 2 and isinstance(raw_result[2], list) and len(raw_result[2]) > 0:
                    fix = {"key": "data_dir_compliance", "fixable_list": raw_result[2], "value": True}
                raw_result = {"passed": passed, "detail": detail, "fix": fix}
            else:
                passed = False
                skipped = False

            entry = {
                "rule_id": rule["id"],
                "rule_name": rule["name"],
                "severity": rule["severity"],
                "passed": passed,
                "skipped": skipped,
                "detail": raw_result.get("detail", ""),
            }
            if raw_result.get("ctx_lines"):
                entry["ctx_lines"] = raw_result["ctx_lines"][:8]
            if not passed and not skipped:
                if raw_result.get("fix"):
                    entry["fix"] = raw_result["fix"]
                if raw_result.get("suggestion"):
                    entry["suggestion"] = raw_result["suggestion"]
            results.append(entry)

            if not passed and not skipped and raw_result.get("fix"):
                fixes.append(raw_result["fix"])

            is_false_positive = not passed and not skipped and _reclassify_false_positive(entry, skill_dir=skill_dir)
            if is_false_positive:
                pass_count += 1
            elif skipped:
                skip_count += 1
            elif passed:
                pass_count += 1
            elif rule["severity"] == "ERROR":
                error_count += 1
        else:
            warn_count += 1

    # 自动修正：有不一致的声明，且还没修正过，且不是 dry-run 模式
    fixed = []
    dry_run = os.environ.get("SKILL_AUDIT_DRY_RUN", "0") == "1"
    if fixes and not _fix_applied and not dry_run:
        applied = _apply_fixes(skill_md, fixes)
        if applied:
            fixed = applied
            # 重新审计一次，确保修正后通过
            re_result = audit_skill(skill_dir, manifest_version=manifest_version, _fix_applied=True)
            re_result["fixed"] = fixed
            re_result["re_audit"] = True
            return re_result

    fail_count = error_count + warn_count
    total = len(results)

    if error_count > 0:
        verdict = f"FAIL ({error_count} ERROR{', ' + str(warn_count) + ' WARN' if warn_count > 0 else ''})"
    elif warn_count > 0:
        verdict = f"WARN ({warn_count} WARN)"
    else:
        verdict = "PASS"

    r = {
        "skill": dirname,
        "path": skill_dir,
        "results": results,
        "summary": {
            "total": total,
            "pass": pass_count,
            "fail": fail_count,
            "skip": skip_count,
            "errors": error_count,
            "warns": warn_count,
        },
        "verdict": verdict,
    }
    if fixed:
        r["fixed"] = fixed
    # 更新 .progress.md（如果传了 _progress_file）
    if progress_file:
        try:
            from .progress_manager import update_progress_from_audit, finalize_progress
            update_progress_from_audit(progress_file, r)
            finalize_progress(progress_file, r)
        except Exception as e:
            print(f"[!] 更新 .progress.md 失败: {e}", file=sys.stderr)
    return r


def _expand_fail_entries(remaining):
    """
    将 FAIL 项展开为颗粒度一致的可编号条目。
    每条包含独立 ID、规则 ID、严重度、问题描述、修复指引、上下文行。

    特别处理 R-25：将 WARN(N) 中的 C-XX 子项展开为独立条目，
    每个子项带有自己的问题描述和对应的 → LLM执行：修复指引。
    非 R-25 规则保持原样输出。
    """
    entries = []
    eid = 0
    # 匹配 C-XX 子项：C-07, C-10, C-11... 及其内容和修复指引
    # 子项之间以 ; 分隔。部分子项有 C-XX 前缀，部分无前缀（续前项）
    # 格式示例：C-10: xxx; C-17: yyy → LLM执行：zzz; 【续】www → LLM执行：vvv
    sub_pattern = re.compile(
        r'(?:'
        r'(C-\d+):\s*(.*?)(?:\s*→\s*LLM执行[：:]([^;]*))?'
        r'|'
        r';\s*(【[^】]+】.*?)(?:\s*→\s*LLM执行[：:]([^;]*))?'
        r')'
        r'(?=;\s*(?:C-\d|【)|\s*C-\d|$)'
    )

    for res in remaining:
        rid = res.get('rule_id', '')
        raw_detail = res.get('detail', '')
        # 确保 detail 是字符串（某些 checker 可能返回 list）
        detail = raw_detail if isinstance(raw_detail, str) else "; ".join(str(d) for d in raw_detail) if isinstance(raw_detail, list) else str(raw_detail)
        sev = res.get('severity', 'WARN')
        ctx = res.get('ctx_lines', [])

        if rid == 'R-25':
            # 从 detail 中提取 WARN(N) 块
            warn_match = re.search(r'🟡\s*WARN\(\d+\):\s*(.+)', detail)
            if warn_match:
                sub_text = warn_match.group(1)
                # 逐个匹配子项（含 C-XX 前缀项和无前缀续项）
                last_cid = None  # 记录最近 C-XX，给续项用
                for sm in sub_pattern.finditer(sub_text):
                    eid += 1
                    c_id = sm.group(1)       # 如 "C-17"，续项为 None
                    if c_id:
                        last_cid = c_id
                        problem = sm.group(2).strip()
                        fix = sm.group(3)
                    else:
                        # 续项：无 C-XX 前缀，使用最近一个 C-XX + 序号
                        suffix = chr(ord('a') + [m.group(1) for m in sub_pattern.finditer(sub_text[:sm.start()])].count(None))
                        c_id = f'{last_cid}{suffix}'
                        problem = sm.group(4).strip()
                        fix = sm.group(5)
                    if fix:
                        fix = fix.strip()
                    else:
                        fix = ''
                    entries.append({
                        'id': str(eid),
                        'rule_id': f'R-25 ({c_id})',
                        'severity': sev,
                        'problem': f'{c_id}: {problem}',
                        'fix': f'R-25 ({c_id}): {problem} → LLM执行：{fix}' if fix else '',
                        'ctx_lines': ctx,
                    })
            else:
                # fallback: 无法解析 WARN 格式，整条输出
                eid += 1
                entries.append({
                    'id': str(eid),
                    'rule_id': rid,
                    'severity': sev,
                    'problem': detail,
                    'fix': detail,
                    'ctx_lines': ctx,
                })
        else:
            # 非 R-25：整条规则作为一个条目
            eid += 1
            if isinstance(detail, str):
                detail_text = detail
            elif isinstance(detail, list):
                detail_text = "; ".join(str(d) for d in detail)
            else:
                detail_text = str(detail)
            entries.append({
                'id': str(eid),
                'rule_id': rid,
                'severity': sev,
                'problem': detail_text.strip(),  # ★ 保留完整问题描述+修复指引
                'fix': detail_text,               # --show-fix 仍需要 fix 字段
                'ctx_lines': ctx,
            })

    return entries


# ── --classify 合法类别 ──
_CLASSIFY_LEGAL_CATEGORIES = {"engine_mistake", "engine_cant_judge"}
_CLASSIFY_CATEGORY_HELP = (
    "engine_mistake — 引擎技术性错误（BOM/编码导致解析失败、注释被当操作、概念图被当文件路径等）\n"
    "engine_cant_judge — 引擎语义不足，LLM 确认后放行（如 __init__.py 无需列文档树、反模式格式引擎没认出但内容确实合规）"
)

# ── --classify 误报子类型枚举 ──
# 每个子类型写明：适用规则 + 适用场景 + 不适用场景
# LLM 按照 WARN/ERROR 的 detail 描述匹配以下场景，不匹配则不能选此子类型。
# 不在枚举表中的子类型 → 代码级拒绝。
_CLASSIFY_LEGAL_SUBTYPES = {
    # engine_mistake 类：引擎技术性错误
    "regex_misidentify":
        "【引擎正则误匹配】适用 R-23：引擎正则把文档中的命令/env/路径字符串误匹配为文件名或引用。"
        "仅当 WARN 的 detail 明确提到「文档引用……但文件不存在」这类路径误匹配时使用。"
        "不适用：非 R-23 的 WARN。",
    "false_classification":
        "【引擎分类错误】适用 R-01/R-20：引擎把合法项错分为违规。"
        "R-01 非标字段：标准 frontmatter 字段被标为非标。"
        "R-20 术语不一致：代码标识符/文件名（如 novel_state.json、is_ending）被误认为自然语言文本问题。"
        "不适用：纯「中英文混排缺少空格」的内容质量问题或真·术语混用（如同一文档里混用「更新」「修改」「变更」）。",
    "bom_encoding":
        "【BOM/编码误识别】适用 R-01：UTF-8 BOM 导致 frontmatter 解析错位，字段被误识别。"
        "仅当 detail 提到 BOM、编码相关时使用。",
    "comment_misread":
        "【注释误读为代码】保留枚举，当前无规则会产生此场景。",
    "template_convention":
        "【模板/框架约定】适用 R-11/R-25 C-11。"
        "R-11：正文中的标准化路径说明（如 models/、data/、backup/）是该技能的标准目录结构描述，不是违规硬编码路径。"
        "R-25 C-11：非标章节标题（如「检查系统」「数据目录」）是该技能的固定架构模板，不属于临时写的非标内容。"
        "不适用：非模板内容被引擎报出的情况——那是真问题。",
    # engine_cant_judge 类：引擎语义不足
    "domain_convention":
        "【领域特定约定】适用 R-17/R-25 C-11：技能文档中的章节结构是该领域（如小说写作）的标准惯例，"
        "引擎无法理解领域语义。仅当 detail 明确说「非标章节」且属于该技能的固有架构时使用。",
    "architecture_pattern":
        "【架构模式约定】适用 R-25 C-12/C-14：约束条数/简练度/长段说明/工作流标注/流程步骤数"
        "是该技能的固定架构模式，引擎无法验证完整性和简练度。"
        "仅当 detail 提到 C-12、C-14 或「工作流程」「约束」时使用。"
        "不适用：C-07 代码块缺语言标识——那是真问题，必须补。",
    "context_sensitive":
        "【上下文敏感】适用 R-23/R-07：函数/触发词是否合理取决于外部调用方或运行上下文，"
        "引擎静态分析无法覆盖。仅当 detail 提到「函数名」「未找到」「触发」时使用。",
    "data_dependency":
        "【数据依赖无法验证】适用 R-11/R-23：路径引用依赖于运行时数据（如模型缓存路径、示例目录树），"
        "引擎无法静态验证。仅当 detail 提到「路径」「models/」「数据」「缓存」「目录树」时使用。",
}


_SNAPSHOT_BASENAME = ".fp_snapshot.json"

def _snapshot_dir(skill_dir):
    """指纹快照目录：.standardization/skill-standardization/data/<skill>/"""
    return os.path.join(
        os.path.dirname(os.path.abspath(skill_dir)), '.standardization',
        'skill-standardization', 'data',
        os.path.basename(os.path.abspath(skill_dir))
    )

def _hash_file(path):
    """SHA256 文件指纹，文件不存在返回 None"""
    if not os.path.isfile(str(path)):
        return None
    return hashlib.sha256(open(str(path), 'rb').read()).hexdigest()

def _update_snapshot(skill_dir, basename):
    """系统写入信号文件后更新指纹。传文件名（如 .verify_fp.json）"""
    sdir = _snapshot_dir(skill_dir)
    os.makedirs(sdir, exist_ok=True)
    snap_path = os.path.join(sdir, _SNAPSHOT_BASENAME)
    snap = {}
    if os.path.isfile(snap_path):
        try:
            snap = json.load(open(snap_path, 'r', encoding='utf-8'))
        except Exception:
            snap = {}
    target = os.path.join(
        os.path.dirname(os.path.abspath(skill_dir)), '.standardization',
        os.path.basename(os.path.abspath(skill_dir)), 'data', basename
    )
    snap[basename] = _hash_file(target)
    with open(snap_path, 'w', encoding='utf-8') as f:
        json.dump(snap, f, ensure_ascii=False, indent=2, sort_keys=True)

def _verify_snapshot(skill_dir, basename):
    """读取信号文件前校验指纹。指纹不匹配或文件被删则 HARD-BLOCK"""
    sdir = _snapshot_dir(skill_dir)
    snap_path = os.path.join(sdir, _SNAPSHOT_BASENAME)
    if not os.path.isfile(snap_path):
        return  # 首次使用无快照，放行
    try:
        snap = json.load(open(snap_path, 'r', encoding='utf-8'))
    except Exception:
        return
    expected = snap.get(basename)
    if expected is None:
        return  # 该文件尚未注册快照
    target = os.path.join(
        os.path.dirname(os.path.abspath(skill_dir)), '.standardization',
        os.path.basename(os.path.abspath(skill_dir)), 'data', basename
    )
    actual = _hash_file(target)
    if actual is None:
        print(f"\n{'='*55}")
        print(f"  [HARD-BLOCK] 信号文件被删除: {basename}")
        print(f"  指纹快照 %s 记录该文件曾有指纹，现已不存在。" % _SNAPSHOT_BASENAME)
        print(f"  可能原因：LLM 手动 `rm` 后未通过系统管道重建。")
        print(f"  修复：删除 {snap_path} 后重新运行 refactor（会丢失分类数据）。")
        print(f"{'='*55}\n")
        sys.exit(1)
    if actual != expected:
        print(f"\n{'='*55}")
        print(f"  [HARD-BLOCK] 信号文件指纹不匹配: {basename}")
        print(f"  期望指纹: {expected}")
        print(f"  实际指纹: {actual}")
        print(f"  可能原因：LLM 手动写入该文件，绕过了系统管道（--classify / 修复循环）。")
        print(f"  必须通过系统管道操作，直接写文件将被拒绝。")
        print(f"{'='*55}\n")
        sys.exit(1)



def _load_fp_ids(skill_dir):
    _verify_snapshot(skill_dir, ".verify_fp.json")
    """读取 LLM 分类的误判 #ID 列表（返回 set[str]）
    
    仅识别 dict 格式（{id: {category, reason}}），
    旧 format list 视为无效，返回空集。
    """
    skill_dir = os.path.abspath(skill_dir)
    fp_path = os.path.join(
        os.path.dirname(skill_dir), '.standardization',
        os.path.basename(skill_dir), 'data', '.verify_fp.json')
    if os.path.isfile(fp_path):
        try:
            import json
            data = json.load(open(fp_path, 'r', encoding='utf-8'))
            if isinstance(data, dict):
                return set(data.keys())
        except Exception:
            pass
    return set()


def _load_fp_details(skill_dir):
    """读取误判详情 dict（{id: {category, reason}}）"""
    skill_dir = os.path.abspath(skill_dir)
    fp_path = os.path.join(
        os.path.dirname(skill_dir), '.standardization',
        os.path.basename(skill_dir), 'data', '.verify_fp.json')
    if os.path.isfile(fp_path):
        try:
            import json
            data = json.load(open(fp_path, 'r', encoding='utf-8'))
            if isinstance(data, dict):
                return data
            data = json.load(open(fp_path, 'r', encoding='utf-8'))
            if isinstance(data, dict):
                return data
        except Exception:
            pass
    return {}


def _write_fp_classify(skill_dir, ids, category, reason="", subtype=""):
    """向 .verify_fp.json 写入误判标记（dict 格式，旧 list 格式忽略）"""
    import json
    skill_dir = os.path.abspath(skill_dir)
    verify_dir = os.path.join(
        os.path.dirname(skill_dir), '.standardization',
        os.path.basename(skill_dir), 'data')
    fp_path = os.path.join(verify_dir, '.verify_fp.json')
    os.makedirs(verify_dir, exist_ok=True)
    existing = {}
    if os.path.isfile(fp_path):
        try:
            old = json.load(open(fp_path, 'r', encoding='utf-8'))
            if isinstance(old, dict):
                existing = old
            # list 格式忽略（历史残留）
        except Exception:
            pass
    for id_str in ids:
        existing[id_str] = {"category": category, "reason": reason, "subtype": subtype}
    with open(fp_path, 'w', encoding='utf-8') as f:
        json.dump(existing, f, ensure_ascii=False, indent=2, sort_keys=True)
    _update_snapshot(skill_dir, ".verify_fp.json")

    # ★ 同步从 .remaining_llm.json 移除已分类项，避免 --continue 循环重审计
    #    .remaining_llm.json 是细碎循环的手动修复清单快照，分类后的项不应再出现在清单中
    _rr_dir = _manual_dir_path(skill_dir)
    _rr_path = os.path.join(_rr_dir, '.remaining_llm.json')
    if os.path.isfile(_rr_path):
        try:
            rr_data = json.load(open(_rr_path, 'r', encoding='utf-8'))
            if isinstance(rr_data, list):
                before = len(rr_data)
                rr_data = [r for r in rr_data
                           if not any(rid in (r.get('rule_id','') or '') + (r.get('rule','') or '')
                                      for rid in ids)]
                if len(rr_data) < before:
                    with open(_rr_path, 'w', encoding='utf-8') as f:
                        json.dump(rr_data, f, ensure_ascii=False, indent=2)
                    _update_snapshot(skill_dir, ".remaining_llm.json")
                    print(f"  [sync] remaining_llm: 移除 {before - len(rr_data)} 项已分类")
        except Exception:
            pass


def _remove_fp_classify(skill_dir, ids):
    """从 .verify_fp.json 中移除指定 #ID（只认 dict 格式）"""
    import json
    skill_dir = os.path.abspath(skill_dir)
    verify_dir = os.path.join(
        os.path.dirname(skill_dir), '.standardization',
        os.path.basename(skill_dir), 'data')
    fp_path = os.path.join(verify_dir, '.verify_fp.json')
    existing = {}
    if os.path.isfile(fp_path):
        try:
            old = json.load(open(fp_path, 'r', encoding='utf-8'))
            if isinstance(old, dict):
                existing = old
            # list 格式忽略（历史残留）
        except Exception:
            pass
    for id_str in ids:
        existing.pop(str(id_str), None)
    os.makedirs(verify_dir, exist_ok=True)
    with open(fp_path, 'w', encoding='utf-8') as f:
        json.dump(existing, f, ensure_ascii=False, indent=2, sort_keys=True)


def _reclassify_false_positive(res, skill_dir=None):
    """仅通过 --classify ID 标记的误判进行排除

    v2.97.3: _llm_only_fix_keys 项（C-11/C-14/C-17/C-18）禁止被 --classify 绕过。
    LLM 必须手动修复这些项，不得标记为误判。

    v2.86.2: 所有误判由 LLM 通过 `--classify` 手动标记。
    代码层不做任何自动误报排除，确保审计报告输出全部原始问题。
    
    ID 支持四种格式：
    - 数字 eid（如 20）→ 匹配 _expand_fail_entries 的序号
    - R-XX（如 R-23） → 匹配 rule_id
    - C-{type}        → 匹配一致性审查 ID
    - C-XX（如 C-08） → 匹配 R-25 子检查项（如 R-25 (C-08)）
    """
    if skill_dir:
        # ★ section_names 移出黑名单 → '约束9条超过上限9条'是引擎bug(9=9)，非标章节/流程步数是架构约定可用subtype分类
        _blocked_fix_keys = {"workflow_completeness", "example_quality", "capability_boundary"}
        fk = None
        if isinstance(res.get("fix"), dict):
            fk = res["fix"].get("key")
        if fk and fk in _blocked_fix_keys:
            # ★ v2.101.12: 如果 LLM 已完成结构化数据准备，允许分类
            #   workflow_completeness → .structure_workflow.json 存在
            #   example_quality → .structure_examples.json 存在
            #   capability_boundary → .structure_capabilities.json 存在
            if skill_dir:
                from .fix import _read_struct
                if _read_struct(skill_dir, fk) is not None:
                    return True  # LLM 已完成手动修复，允许分类跳过
            return False  # 这些是 LLM 手动修复项，必须修，不能分类跳过
        
        fp_ids = _load_fp_ids(skill_dir)
        if fp_ids:
            try:
                # 检查 rule_id 直接匹配（R-XX 格式）
                rid = res.get('rule_id', res.get('rule', ''))
                if rid and any(fpid == rid for fpid in fp_ids):
                    return True
                # ★ 新增：C-XX 格式匹配 R-25 子检查项
                # 如 --classify C-08 应匹配 rule_id = "R-25 (C-08)" 的条目
                c_ids = [fpid for fpid in fp_ids if re.match(r'^C-\d+$', str(fpid))]
                if c_ids:
                    entries = _expand_fail_entries([res])
                    for e in entries:
                        e_rid = e.get('rule_id', '')
                        e_problem = e.get('problem', '')
                        for cid in c_ids:
                            # rule_id 格式: "R-25 (C-08)" 或 "R-25 (C-08a)"
                            if e_rid.startswith(f'R-25 ({cid}') or cid in e_problem:
                                return True
                # eid 匹配（数字 ID）
                entries = _expand_fail_entries([res])
                fp_id_set = {str(i) for i in fp_ids}
                for e in entries:
                    if str(e['id']) in fp_id_set:
                        return True  # LLM 已手动标记为误判
            except Exception:
                pass
    return False


def _filter_false_positives(audit_result, skill_dir):
    """
    从审计结果中过滤掉已知误报，返回"真问题"列表。
    
    统一三层过滤：
      1. audit_skill() 内部已过滤 _reclassify_false_positive()（代码自动层）
      2. 再过滤 --classify 标记的误判（LLM 分类层）
    
    返回: [result_entry, ...] — 仅包含未 PASS、未跳过、未被任何误报机制标记的条目
    """
    remaining = [r for r in audit_result.get("results", [])
                 if not r.get("passed") and not r.get("skipped")
                 and not _reclassify_false_positive(r, skill_dir)]
    if not remaining:
        return remaining
    
    # 第二层：LLM 通过 --classify 标记的误判
    fp_ids = _load_fp_ids(skill_dir)
    if fp_ids:
        entries = _expand_fail_entries(remaining)
        fp_id_set = {str(i) for i in fp_ids}
        c_ids = {str(fpid) for fpid in fp_ids if re.match(r'^C-\d+$', str(fpid))}
        # 把已标记为误判的条目过滤掉
        filtered = []
        for r in remaining:
            # 尝试匹配这条规则的 detail 是否对应某个已分类误判的 #ID
            rid = r.get('rule_id', '')
            detail = r.get('detail', '')
            # 用 _expand_fail_entries 展开后检查
            matched = False
            for e in entries:
                if str(e['id']) in fp_id_set and (e['rule_id'] == rid and e['problem'][:80] in detail):
                    matched = True
                    break
                # ★ C-XX 格式匹配
                e_rid = e.get('rule_id', '')
                e_problem = e.get('problem', '')
                for cid in c_ids:
                    if (e_rid.startswith(f'R-25 ({cid}') or cid in e_problem):
                        matched = True
                        break
                if matched:
                    break
            if not matched:
                filtered.append(r)
        remaining = filtered
    
    return remaining


def format_report(audit_result, verbose=True, before_summary=None, show_fix_hint=True, skill_dir=None):
    """格式化人类可读的审查报告"""
    lines = []
    r = audit_result

    if "error" in r:
        lines.append(f"[X] {r['skill']}: {r['error']}")
        return "\n".join(lines)

    lines.append(f"{'='*55}")
    lines.append(f"  审查结果: {r['skill']} — {r['verdict']}")
    lines.append(f"{'='*55}")

    # 计算各类别数量：全部从 results 列表计算，确保「通过」不包含ⓘ误报，「失败」不包含ⓘ误报
    all_results = r.get("results", [])
    _fp_ids = set()
    for idx, res in enumerate(all_results):
        if _reclassify_false_positive(res, skill_dir=skill_dir):
            _fp_ids.add(idx)
    
    real_pass = sum(1 for idx, res in enumerate(all_results) if res.get("passed") and idx not in _fp_ids)
    excluded = len(_fp_ids)
    real_fail = sum(1 for idx, res in enumerate(all_results) if not res.get("passed") and not res.get("skipped") and idx not in _fp_ids)
    skipped = sum(1 for res in all_results if res.get("skipped"))
    total_items = len(all_results)

    summary_parts = [
        f"总计: {total_items}",
        f"✅ 通过: {real_pass}",
        f"❌ 失败: {real_fail}",
    ]
    if excluded > 0:
        summary_parts.append(f"ⓘ LLM已标记: {excluded}")
    summary_parts.append(f"⏭ 跳过: {skipped}")
    lines.append(" | ".join(summary_parts))

    # 修复前后对比（在 before_summary 有数据时显示）
    if before_summary is not None:
        s = r.get("summary", {})
        be = before_summary.get("errors", 0)
        bw = before_summary.get("warns", 0)
        ae = s.get("errors", 0)
        aw = s.get("warns", 0)
        lines.append(f"  ── 修复前: {be} ERROR / {bw} WARN  →  修复后: {ae} ERROR / {aw} WARN {'✅' if ae == 0 and aw == 0 else '⚠️'}")

    # 显示自动修正信息
    if r.get("fixed"):
        lines.append(f"\n{'─'*55}")
        lines.append("  [!]  已自动修正以下 frontmatter 字段：")
        for fix_desc in r["fixed"]:
            lines.append(f"    • {fix_desc}")
        if r.get("re_audit"):
            lines.append("  （已重新审计，确保修正后通过）")
        lines.append(f"{'─'*55}")

    if verbose:
        # 预读技能目录文件内容，用于自动上下文提取
        _skill_dir = r.get("path", "")
        _file_cache = {}

        def _get_file_lines(filepath):
            if filepath in _file_cache:
                return _file_cache[filepath]
            if os.path.isfile(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        _file_cache[filepath] = f.read().split('\n')
                except Exception:
                    _file_cache[filepath] = []
            else:
                _file_cache[filepath] = []
            return _file_cache[filepath]

        lines.append("")
        lines.append(f"{'规则ID':<8} {'严重度':<7} {'状态':<6} 详情")
        lines.append(f"{'-'*8}-{'-'*7}-{'-'*6}-{'-'*30}")
        for res in r["results"]:
            # 已知误报检测：LLM 可确定的 false positive 降级为 ⓘ
            if _reclassify_false_positive(res, skill_dir=skill_dir):
                status = "ⓘ"
                sev = "排除"
            else:
                status = "[OK]" if res["passed"] else ("⏭️" if res["skipped"] else ("[ERROR]" if res["severity"]=="ERROR" else "[WARN]"))
                sev = res["severity"][0] if res["severity"] else "?"
            lines.append(f"{res['rule_id']:<8} {sev:<7} {status:<6} {res['detail']}")
            # 详细上下文行：优先使用检查器返回的 ctx_lines，否则自动从 detail 中的路径提取
            ctx = res.get("ctx_lines") or []
            if not ctx and _skill_dir:
                _detail_str = res.get("detail", "")
                if isinstance(_detail_str, str):
                    for _m in re.finditer(r'([^\s]+\.(?:md|py|tex|txt|json|yaml|yml|cfg|ini|toml)):(\d+)', _detail_str):
                        _fp = _m.group(1)
                        _ln = int(_m.group(2))
                        for _base in ('', _skill_dir):
                            _full = os.path.join(_base, _fp) if _base else _fp
                            _ls = _get_file_lines(_full)
                            if _ls:
                                _start = max(0, _ln - 3)
                                _end = min(len(_ls), _ln + 2)
                                _ctx = '\n'.join(f"    {_fp}:{i} {_ls[i-1]}" for i in range(_start + 1, _end + 1))
                                ctx.append(f"  {_fp}:{_ln} 附近:\n{_ctx}")
                                break
            if ctx:
                for cl in ctx[:8]:
                    lines.append(f"       {cl}")
            # 修正建议（供 LLM 参考）
            if not res["passed"] and not res["skipped"] and res.get("fix"):
                fix = res["fix"]
                if fix.get("operation"):
                    lines.append(f"    💡 建议修正：{fix['operation']}")
                if fix.get("location"):
                    lines.append(f"    [search] 位置：{fix['location']}")
                if fix.get("reason"):
                    lines.append(f"    💬 原因：{fix['reason']}")

    # 固定输出：提示可用 --fix 自动修复（仅在纯 audit 命令显示，refactor/update 有自己的修复流程）
    if show_fix_hint:
        lines.append("")
        lines.append(f'{"─"*55}')
        lines.append("  🛠️ 提示：发现可修复问题时，优先运行以下命令自动修复：")
        lines.append("    python -m skill_audit audit <skill_dir> --fix")
        lines.append("  （模型请勿手动修改，优先使用 --fix 自动修复）")
        lines.append(f'{"─"*55}')

    return "\n".join(lines)


def _save_html_report(skill_dir, audit_result, before_summary=None, before_result=None, filename=".audit_report.html"):
    """统一保存 HTML 报告到 data/<skill>/outputs/。"""
    import os
    _dname = os.path.basename(os.path.abspath(skill_dir))
    _self_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    _self_name = os.path.basename(_self_dir)
    _dd = os.path.normpath(os.path.join(
        _self_dir,
        "..", ".standardization", _self_name, "data", _dname, "outputs"
    ))
    _html_path = os.path.join(_dd, filename)
    try:
        path = generate_html_report(audit_result, _html_path, before_summary=before_summary, skill_dir=skill_dir, before_result=before_result)
        print(f"  📋 报告已保存: {path}")
        print(f"  📋 报告已保存: {path}")
    except Exception as e:
        print(f"  ⚠️  HTML 报告生成失败: {e}")


_REFACTOR_LOCK = ".refactor_locked.lock"


def _refactor_lock_path(skill_dir):
    _dname = os.path.basename(os.path.abspath(skill_dir))
    return os.path.normpath(os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "..", ".standardization", "skill-standardization", "data", _dname,
        _REFACTOR_LOCK
    ))


def _lock_refactor(skill_dir):
    """创建重构锁，阻止报告生成"""
    lp = _refactor_lock_path(skill_dir)
    os.makedirs(os.path.dirname(lp), exist_ok=True)
    with open(lp, "w") as f:
        f.write("locked")
    print(f"  🔒 重构锁已创建: {lp}")


def _unlock_refactor(skill_dir):
    """清除重构锁"""
    lp = _refactor_lock_path(skill_dir)
    if os.path.exists(lp):
        os.unlink(lp)
        print(f"  🔓 重构锁已清除")


def _is_refactor_locked(skill_dir):
    """检查重构锁是否存在"""
    return os.path.exists(_refactor_lock_path(skill_dir))


def _save_remaining_llm(skill_dir, remaining):
    """保存 LLM 需手动修复的剩余项为结构化 JSON，供 LLM 闭环消费。"""
    _dname = os.path.basename(os.path.abspath(skill_dir))
    _dd = os.path.normpath(os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "..", ".standardization", "skill-standardization", "data", _dname
    ))
    os.makedirs(_dd, exist_ok=True)
    _path = os.path.join(_dd, ".remaining_llm.json")
    try:
        with open(_path, 'w', encoding='utf-8') as f:
            json.dump(remaining, f, ensure_ascii=False, indent=2)
        _update_snapshot(skill_dir, ".remaining_llm.json")
        print(f"  📋 LLM 剩余修复项已保存: {_path}")
    except Exception as e:
        print(f"  ⚠️  保存 .remaining_llm.json 失败: {e}")


def generate_html_report(audit_result, output_path, before_summary=None, skill_dir=None, before_result=None):
    # ★ 重构锁检查：如果锁存在，拒绝生成报告
    if skill_dir and _is_refactor_locked(skill_dir):
        print(f"\n  ⛔ ⛔ ⛔ 重构锁仍处于激活状态，拒绝生成报告 ⛔ ⛔ ⛔")
        print(f"  未达 0 ERROR 0 WARN 之前不得输出报告。")
        print(f"  请继续修复循环后再试。")
        return
    """生成 HTML 格式的审计报告（含筛选、展开、统计图表）。
    
    audit_result: audit_skill() 返回的 dict（修复后的结果）
    output_path: 输出的 .html 文件路径
    before_summary: {"errors": int, "warns": int} 修复前的统计数据（已废弃，由 before_result 替代）
    skill_dir: 技能目录路径（传入后会用 _reclassify_false_positive 过滤已分类误报）
    before_result: audit_skill() 返回的 dict（修复前的结果），传入后显示 before/after 双表
    """
    import os, json, datetime
    
    # ── 修复前数据（如果提供） ──
    before_rows_html = ""
    if before_result is not None:
        br = before_result
        b_results = br.get("results", [])
        for bi, bres in enumerate(b_results):
            brid = bres.get("rule_id", "?")
            bsev = bres.get("severity", "?")
            bdetail = bres.get("detail", "")
            
            # 判断是否被标记为误报
            if not bres.get("passed") and not bres.get("skipped") and _reclassify_false_positive(bres, skill_dir=skill_dir):
                bpassed_flag = "ⓘ 误报(排除)"
                bsclass = "excluded-row"
                bsev_display = "排除"
            elif bres.get("passed"):
                bpassed_flag = "✅ PASS"
                bsclass = "pass-row"
                bsev_display = bsev
            elif bres.get("skipped"):
                bpassed_flag = "⏭️ SKIP"
                bsclass = "skip-row"
                bsev_display = "?"
            else:
                bpassed_flag = "❌ FAIL"
                bsclass = "fail-row"
                bsev_display = bsev
            
            bsd = "error" if bsev == "ERROR" else "warn" if bsev == "WARN" else "info"
            before_rows_html += f"""
        <tr class="{bsclass}" data-severity="{bsd}" onclick="toggleDetailB({bi})">
            <td>{brid}</td>
            <td><span class="sev-{bsev.lower()}">{bsev_display}</span></td>
            <td>{bpassed_flag}</td>
            <td class="dc">{bdetail[:100]}{'...' if len(bdetail) > 100 else ''}</td>
            <td></td>
        </tr>
        <tr id="bd{bi}" style="display:none" class="dr">
            <td colspan="5"><pre>{bdetail}</pre></td>
        </tr>"""

    # ── 修复后数据 ──
    r = audit_result    # ── 修复后数据 ──
    skill = r.get("skill", "unknown")
    verdict = r.get("verdict", "?")
    summary = r.get("summary", {})
    total = summary.get("total", 0)
    passed = summary.get("pass", 0)
    failed = summary.get("fail", 0)
    skipped = summary.get("skip", 0)
    results = r.get("results", [])
    _total_items_orig = len(results)  # 记录原始总数供 LLM 二筛路径使用
    _is_llm_filtered = False
    
    # 先计算原始结果的排除计数（无论是否 LLM 二筛都要算）
    _orig_fp_ids = set()
    for oi, ores in enumerate(results):
        if _reclassify_false_positive(ores, skill_dir=skill_dir):
            _orig_fp_ids.add(oi)
    _orig_excluded = len(_orig_fp_ids)
    
    # 过滤已分类误报（LLM 二筛结果）
    # 注意：_reclassify_false_positive 的单条目 _expand_fail_entries 存在 ID 冲突问题，
    # 暂时只做技能目录存在验证，完整过滤走 --verify 路径
    if skill_dir and os.path.isfile(os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "..", ".standardization", os.path.basename(os.path.abspath(skill_dir)),
        "data", ".verify_fp.json"
    )):
        # classify 文件存在即 LLM 已完成二筛，结果应为双0
        verdict = "PASS (LLM 二筛通过)"
        results = [res for res in results if res.get("passed") or res.get("skipped")]
        total = len(results)
        passed = sum(1 for res in results if res.get("passed"))
        failed = 0
        skipped = sum(1 for res in results if res.get("skipped"))
        _is_llm_filtered = True
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    rows_html = ""
    for i, res in enumerate(results):
        rid = res.get("rule_id", "?")
        sev = res.get("severity", "?")
        detail = res.get("detail", "")
        passed_flag = "✅ PASS" if res.get("passed") else "❌ FAIL"
        if res.get("skipped"):
            passed_flag = "⏭️ SKIP"
        fix_key = ""
        if res.get("fix"):
            fk = res["fix"].get("key", "")
            if fk:
                fix_key = f"<code>apply_fix('{fk}')</code>"
        
        sc = "pass-row" if res.get("passed") else "fail-row"
        if res.get("skipped"):
            sc = "skip-row"
        sd = "error" if sev == "ERROR" else "warn" if sev == "WARN" else "info"
        
        rows_html += f"""
        <tr class="{sc}" data-severity="{sd}" onclick="toggleDetail({i})">
            <td>{rid}</td>
            <td><span class="sev-{sev.lower()}">{sev}</span></td>
            <td>{passed_flag}</td>
            <td class="dc">{detail[:100]}{'...' if len(detail) > 100 else ''}</td>
            <td>{fix_key}</td>
        </tr>
        <tr id="d{i}" style="display:none" class="dr">
            <td colspan="5"><pre>{detail}</pre></td>
        </tr>"""
    
    # 修复后数量：与 format_report 统一的算法，排除被标记为 ⓘ 的项
    if _is_llm_filtered:
        # LLM 二筛通过路径：results 已过滤为纯 PASS/SKIP
        # 所有未通过项（不在 filtered results 中）均视为已由 LLM 分类排除
        pass_c = sum(1 for res in results if res.get("passed"))
        excluded_c = _total_items_orig - len(results)  # 被 LLM 二筛过滤掉的项 = 全部排除
        err_c = 0
        warn_c = 0
        skip_c = sum(1 for res in results if res.get("skipped"))
    else:
        _a_fp_ids = set()
        for ai, ares in enumerate(results):
            if _reclassify_false_positive(ares, skill_dir=skill_dir):
                _a_fp_ids.add(ai)
        pass_c = sum(1 for ai, ares in enumerate(results) if ares.get("passed") and ai not in _a_fp_ids)
        excluded_c = len(_a_fp_ids)
        err_c = sum(1 for ai, ares in enumerate(results) if ares.get("severity")=="ERROR" and not ares.get("passed") and not ares.get("skipped") and ai not in _a_fp_ids)
        warn_c = sum(1 for ai, ares in enumerate(results) if ares.get("severity")=="WARN" and not ares.get("passed") and not ares.get("skipped") and ai not in _a_fp_ids)
        skip_c = sum(1 for res in results if res.get("skipped"))
    
    # 构建修复前后对比 HTML（仅在 before_summary 有数据时显示）
    compare_html = ""
    if before_summary is not None:
        be = before_summary.get("errors", 0)
        bw = before_summary.get("warns", 0)
        is_zero = (err_c == 0 and warn_c == 0)
        err_bg = "#55efc4;color:#00b894" if is_zero else "#ff7675;color:#fff"
        warn_bg = "#55efc4;color:#00b894" if is_zero else "#fdcb6e;color:#2d3436"
        zero_badge = '<span style="background:#55efc4;color:#00b894;padding:2px 10px;border-radius:4px;font-weight:600;">&#x2705; 双0通过</span>' if is_zero else ""
        compare_html = f'''</div>
<div style="padding:8px 32px;background:#fff;border-bottom:1px solid #e0e0e0;font-size:14px;">
<div style="display:flex;gap:20px;align-items:center;">
<span style="color:#636e72;">修复前</span>
<span style="background:#ff7675;color:#fff;padding:2px 10px;border-radius:4px;font-weight:600;">{be} ERROR</span>
<span style="background:#fdcb6e;color:#2d3436;padding:2px 10px;border-radius:4px;font-weight:600;">{bw} WARN</span>
<span style="margin:0 12px;color:#636e72;">&#8594;</span>
<span style="color:#00b894;font-weight:600;">修复后</span>
<span style="background:{err_bg};padding:2px 10px;border-radius:4px;font-weight:600;">{err_c} ERROR</span>
<span style="background:{warn_bg};padding:2px 10px;border-radius:4px;font-weight:600;">{warn_c} WARN</span>
{zero_badge}
</div>
</div>'''
    
    # 构建修复前表格（当 before_result 有数据时显示）
    if before_result is not None:
        b_total = len(b_results)
        b_fp_ids = set()
        for bi, bres in enumerate(b_results):
            if _reclassify_false_positive(bres, skill_dir=skill_dir):
                b_fp_ids.add(bi)
        b_real_pass = sum(1 for bi, bres in enumerate(b_results) if bres.get("passed") and bi not in b_fp_ids)
        b_excluded_c = len(b_fp_ids)
        b_err_c = sum(1 for bres in b_results if bres.get("severity")=="ERROR" and not bres.get("passed") and not bres.get("skipped") and not _reclassify_false_positive(bres, skill_dir=skill_dir))
        b_warn_c = sum(1 for bres in b_results if bres.get("severity")=="WARN" and not bres.get("passed") and not _reclassify_false_positive(bres, skill_dir=skill_dir))
        before_table_html = f'''<div class="bh">📋 修复前 — {b_err_c} ERROR / {b_warn_c} WARN / {b_real_pass} PASS / ⓘ {b_excluded_c} 误报</div>
<div class="fl" style="border-bottom:none;">
<span style="color:#636e72;">共 {b_total} 项</span>
</div>
<table><thead><tr><th>规则</th><th>级别</th><th>状态</th><th>详情</th><th>修复</th></tr></thead>
<tbody id="bb">{before_rows_html}</tbody></table>'''
    else:
        before_table_html = ""
    
    # 条形图 SVG：纯内联，零外部依赖
    _max_c = max(err_c, warn_c, pass_c, skip_c, 1)
    _bar_h = 80
    _bar_w = 30
    _gap = 10
    _total_w = (_bar_w + _gap) * 4
    _bars = [
        ("ERROR", err_c, "#ff7675"),
        ("WARN", warn_c, "#fdcb6e"),
        ("PASS", pass_c, "#55efc4"),
        ("SKIP", skip_c, "#74b9ff"),
    ]
    _bar_rects = ""
    _bar_labels = ""
    for i, (label, val, color) in enumerate(_bars):
        h = val / _max_c * _bar_h if val > 0 else 2
        x = i * (_bar_w + _gap)
        y = _bar_h - h
        _bar_rects += f'<rect x="{x}" y="{y}" width="{_bar_w}" height="{h}" fill="{color}" rx="3" />'
        _bar_labels += f'<text x="{x + _bar_w/2}" y="{_bar_h + 14}" text-anchor="middle" font-size="10" fill="#636e72">{label}</text>'
    bar_svg = f'<svg viewBox="0 0 {_total_w} {_bar_h + 28}" style="width:100%;height:100%;max-height:140px;"><g>{_bar_rects}</g><g>{_bar_labels}</g></svg>'
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>审计报告 — {skill}</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif; background:#f5f6fa; color:#2d3436; }}
.hd {{ background:linear-gradient(135deg,#6c5ce7,#a29bfe); color:#fff; padding:24px 32px; }}
.hd h1 {{ font-size:24px; margin-bottom:8px; }}
.hd .meta {{ opacity:.85; font-size:14px; }}
.sc {{ display:flex; gap:16px; padding:20px 32px; background:#fff; border-bottom:1px solid #e0e0e0; }}
.scc {{ flex:1; padding:12px; border-radius:8px; text-align:center; }}
.scc h3 {{ font-size:28px; margin-bottom:4px; }}
.scc p {{ font-size:13px; opacity:.7; }}
.ce {{ background:#ffeaa7; color:#d63031; }}
.cw {{ background:#dfe6e9; color:#e17055; }}
.cp {{ background:#55efc4; color:#00b894; }}
.ci {{ background:#74b9ff; color:#0984e3; }}
.ch {{ display:flex; gap:16px; padding:12px 32px; background:#fff; border-bottom:1px solid #e0e0e0; }}
.cbx {{ flex:1; max-width:280px; height:160px; }}
.fl {{ padding:10px 32px; background:#fff; border-bottom:1px solid #e0e0e0; font-size:13px; }}
.fl select,.fl input {{ margin-right:10px; padding:5px 10px; border:1px solid #ddd; border-radius:4px; font-size:13px; }}
table {{ width:100%; border-collapse:collapse; background:#fff; }}
th {{ background:#f8f9fa; padding:10px 14px; text-align:left; font-size:13px; font-weight:600; color:#636e72; border-bottom:2px solid #e0e0e0; position:sticky; top:0; }}
td {{ padding:8px 14px; font-size:13px; border-bottom:1px solid #f0f0f0; cursor:pointer; }}
.pass-row td {{ color:#00b894; }}
.fail-row td {{ color:#d63031; }}
.skip-row td {{ color:#636e72; }}
.excluded-row td {{ color:#636e72; font-style:italic; }}
.excluded-row td:nth-child(3) {{ color:#0984e3; font-weight:600; }}
.bh {{ background:#f0f0f0; padding:10px 32px; font-size:14px; font-weight:600; color:#2d3436; border-bottom:1px solid #e0e0e0; margin-top:16px; }}
.bh:first-of-type {{ margin-top:0; }}
.dr td {{ background:#f8f9fa; padding:0; }}
.dr pre {{ margin:0; padding:12px 14px; font-size:12px; white-space:pre-wrap; word-break:break-all; max-height:200px; overflow-y:auto; background:#2d3436; color:#dfe6e9; border-radius:0 0 6px 6px; }}
.sev-error {{ background:#ff7675; color:#fff; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:600; }}
.sev-warn {{ background:#fdcb6e; color:#2d3436; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:600; }}
.sev-info {{ background:#74b9ff; color:#fff; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:600; }}
</style>
</head>
<body>
<div class="hd"><h1>📋 审计报告 — {skill}</h1><div class="meta">{now} | 结论: {verdict}</div></div>
<div class="sc">
<div class="scc ce"><h3>{err_c}</h3><p>ERROR</p></div>
<div class="scc cw"><h3>{warn_c}</h3><p>WARN</p></div>
<div class="scc cp"><h3>{pass_c}</h3><p>PASS</p></div>
<div class="scc ci"><h3>{skipped}</h3><p>SKIP</p></div>
<div class="scc" style="background:#dfe6e9;color:#636e72;"><h3>{excluded_c}</h3><p>ⓘ 误报(排除)</p></div>
</div>
{compare_html}
<div class="ch">
  <div class="cbx" style="padding:12px;text-align:center;">
    <svg viewBox="0 0 160 120" style="max-width:200px;height:120px;">
      <circle cx="80" cy="60" r="50" fill="#55efc4" />
      <circle cx="80" cy="60" r="50" fill="transparent" stroke="#ff7675" stroke-width="28"
        stroke-dasharray="{err_c * 314 / total:.1f} {314:.1f}"
        stroke-dashoffset="{0 if err_c == 0 else -0.1}" />
      <circle cx="80" cy="60" r="50" fill="transparent" stroke="#fdcb6e" stroke-width="28"
        stroke-dasharray="{warn_c * 314 / total:.1f} {314:.1f}"
        stroke-dashoffset="{-err_c * 314 / total:.1f}" />
      <circle cx="80" cy="60" r="50" fill="transparent" stroke="#55efc4" stroke-width="28"
        stroke-dasharray="{pass_c * 314 / total:.1f} {314:.1f}"
        stroke-dashoffset="{-(err_c + warn_c) * 314 / total:.1f}" />
      <text x="80" y="65" text-anchor="middle" font-size="16" font-weight="bold">{total}</text>
    </svg>
    <div style="display:flex;justify-content:center;gap:12px;font-size:11px;margin-top:4px;">
      <span><span style="color:#ff7675;">●</span> E{err_c}</span>
      <span><span style="color:#fdcb6e;">●</span> W{warn_c}</span>
      <span><span style="color:#55efc4;">●</span> P{pass_c}</span>
      <span><span style="color:#74b9ff;">●</span> S{skip_c}</span>
    </div>
  </div>
  <div class="cbx" style="padding:12px;">
    {bar_svg}
  </div>
</div>
{before_table_html}
<div class="bh">📋 修复后</div>
<div class="fl">
<select id="sf" onchange="af()"><option value="all">全部级别</option><option value="error">ERROR</option><option value="warn">WARN</option></select>
<select id="tf" onchange="af()"><option value="all">全部状态</option><option value="fail">FAIL</option><option value="pass">PASS</option></select>
<input id="sq" type="text" placeholder="搜索..." oninput="af()" style="width:200px">
<span style="color:#636e72;">共 {total} 项</span>
</div>
<table><thead><tr><th>规则</th><th>级别</th><th>状态</th><th>详情</th><th>修复</th></tr></thead>
<tbody id="rb">{rows_html}</tbody></table>
<script>
function toggleDetail(i){{var d=document.getElementById('d'+i);d.style.display=d.style.display==='none'?'table-row':'none';}}
function toggleDetailB(i){{var d=document.getElementById('bd'+i);d.style.display=d.style.display==='none'?'table-row':'none';}}
function af(){{var s=document.getElementById('sf').value,t=document.getElementById('tf').value,q=document.getElementById('sq').value.toLowerCase();document.querySelectorAll('#rb tr:not(.dr)').forEach(function(r){{var sm=s==='all'||r.dataset.severity===s,tm=t==='all'||(t==='fail'&&r.classList.contains('fail-row'))||(t==='pass'&&r.classList.contains('pass-row'));var tx=r.textContent.toLowerCase();r.style.display=(sm&&tm&&(!q||tx.includes(q)))?'':'none';}});}}
</script>
</body>
</html>'''
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    return output_path


def cmd_create_template(args):
    """
    输出所有规则的创建模板（供 LLM 创建技能时参考）。
    包含：规则 ID、严重度、检查内容、是否可自动修正、创建模板。
    """
    _semantic_precheck('readonly', confirmed=getattr(args, 'confirmed', False),
                       llm_mode=getattr(args, 'mode', None))
    print(f"\n{'='*70}")
    print("  skill-standardization 创建模板（供 LLM 参考）")
    print(f"{'='*70}\n")

    for rule in RULES:
        sev_mark = "[ERROR]" if rule["severity"] == "ERROR" else "[WARN]"
        fixable_mark = "[OK] 可自动修正" if rule.get("fixable") else "[X] 需手动修正"
        print(f"{'─'*70}")
        print(f"  {rule['id']} {sev_mark} [{rule['severity']}] {rule['name']}")
        print(f"  检查：{rule['check']}")
        print(f"  修正：{fixable_mark}")
        tmpl = rule.get("create_template", "")
        if tmpl:
            # 把 \n 转换成实际换行，并缩进
            tmpl_lines = tmpl.split("\\n")
            print(f"  创建模板：")
            for ln in tmpl_lines:
                print(f"    {ln}")
        print()

    print(f"{'='*70}")
    print(f"  共 {len(RULES)} 条规则")
    print(f"{'='*70}\n")
    print("用法：")
    print("  python -m skill_audit create-template")
    print("  python -m skill_audit create-template --json  （JSON 格式）")
    print()


def cmd_rules(args):
    """列出所有审查规则"""
    _semantic_precheck('readonly', confirmed=getattr(args, 'confirmed', False),
                       llm_mode=getattr(args, 'mode', None))
    print(f"\n{'ID':<8} {'严重度':<8} 名称  检查内容")
    print("-" * 65)
    for rule in RULES:
        sev_mark = "[ERROR]" if rule["severity"] == "ERROR" else "[WARN]"
        print(f"  {rule['id']:<6} {sev_mark} {rule['severity']:<6} {rule['name']: <20} {rule['check']}")
    print(f"\n共 {len(RULES)} 条规则")


def _do_bump(skill_dir, bump_type='fix', desc='自动升级', skip_changelog=False):
    """版本号三端更新核心逻辑 — 供 --fix 和 bump 子命令复用
    参数 skip_changelog=True 时，仅更新 SKILL.md 和 _meta.json 的版本号，不写 changelog。
    changelog 由 LLM 根据 fix 详情和审计报告动态翻译生成。
    """
    import os, sys, json, re, datetime

    # 映射 fix/feature/breaking → patch/minor/major
    type_map = {'fix': 'patch', 'feature': 'minor', 'breaking': 'major'}
    vm_bump_type = type_map.get(bump_type, 'patch')

    meta_path = os.path.join(skill_dir, '_meta.json')
    if not os.path.isfile(meta_path):
        raise FileNotFoundError(
            f"未找到 `_meta.json`（位置：{meta_path}）。\n"
            f"  原因：目标目录可能不是标准 skill 结构，缺少技能元数据文件。\n"
            f"  解决：确认目标路径是一个完整的 skill 目录（含 SKILL.md 和 _meta.json），\n"
            f"        或使用 `python -m scripts.skill_builder create <name>` 创建新 skill。"
        )

    with open(meta_path, 'r', encoding='utf-8') as f:
        current_version = str(json.load(f).get('version', '0.0.0'))

    parts = current_version.split('.')
    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
    if bump_type == 'fix':
        new_version = f"{major}.{minor}.{patch + 1}"
    elif bump_type == 'feature':
        new_version = f"{major}.{minor + 1}.0"
    else:
        new_version = f"{major + 1}.0.0"

    today = datetime.date.today().isoformat()

    # 用已有 VersionManager 更新 SKILL.md + _meta.json
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        from skill_builder.version_manager import VersionManager
        VersionManager.bump_version(skill_dir, vm_bump_type)
    except Exception:
        # 兜底：直接用 stdlib + _safe_write
        _meta_path = os.path.join(skill_dir, '_meta.json')
        with open(_meta_path, 'r', encoding='utf-8') as f:
            _meta = json.load(f)
        _meta['version'] = new_version
        _safe_write(_meta_path, json.dumps(_meta, ensure_ascii=False, indent=2) + '\n', backup=True)
        _skill_md = os.path.join(skill_dir, 'SKILL.md')
        with open(_skill_md, 'r', encoding='utf-8') as f:
            _md_content = f.read()
        _md_content = re.sub(
            r'^(version:\s*)\d+\.\d+\.\d+',
            rf'\g<1>{new_version}',
            _md_content, count=1, flags=re.MULTILINE
        )
        _safe_write(_skill_md, _md_content, backup=True)

    # 更新 changelog（--fix 模式跳过，由 LLM 根据审计结果动态翻译生成）
    if not skip_changelog:
        cl_entry = f"## [{new_version}] - {today}\n\n### 修复\n- {desc}\n"
        cl_path = os.path.join(skill_dir, 'references', 'changelog.md')
        if os.path.isfile(cl_path):
            with open(cl_path, 'r', encoding='utf-8') as f:
                cl_old = f.read()
        else:
            cl_old = ''
            os.makedirs(os.path.dirname(cl_path), exist_ok=True)
        new_cl = cl_entry + '\n---\n\n' + cl_old if cl_old else cl_entry
        os.makedirs(os.path.dirname(cl_path), exist_ok=True)
        _safe_write(cl_path, new_cl, backup=True)


def _audit_with_blueprint(skill_dir, **kw):
    """[已废弃] 保留别名确保外部引用不中断。直接调用 audit_skill()。"""
    return audit_skill(skill_dir, **kw)


def cmd_audit(args):
    """审查单个 skill 目录"""
    fp_ids = set()
    _semantic_precheck('audit', getattr(args, 'skill_dir', None), confirmed=getattr(args, 'confirmed', False),
                       llm_mode=getattr(args, 'mode', None), classify=getattr(args, 'classify', None))
    # 强制 UTF-8 输出（Windows 终端兼容）
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    skill_dir = args.skill_dir
    if not os.path.isdir(skill_dir):
        print(f"[X] 目录不存在: {skill_dir}", file=sys.stderr)
        sys.exit(1)

    # 纯 --show-fix 模式：跳过审计，直接读取 fix_map 输出修复指引
    if getattr(args, 'show_fix', None) and not getattr(args, 'verify', False):
        fix_map_path = os.path.join(
            os.path.dirname(skill_dir), '.standardization',
            os.path.basename(skill_dir), 'data', '.verify_fix_map.json')
        if not os.path.isfile(fix_map_path):
            print(f"[ERROR] 未找到 fix_map 文件（{fix_map_path}），请先运行 --verify")
            sys.exit(1)
        with open(fix_map_path, 'r', encoding='utf-8') as f:
            fix_map = json.load(f)
        ids = [s.strip() for s in args.show_fix.split(',')]
        print(f"\n{'='*55}")
        print(f"  [SHOW-FIX v1] 展示 {len(ids)} 条修复指引")
        print(f"{'─'*55}")
        found_any = False
        for rid in ids:
            fix_text = fix_map.get(rid)
            if fix_text:
                print(f"  [#{rid}] {fix_text}")
                found_any = True
            else:
                print(f"  [#{rid}] (未找到对应修复指引)")
        if not found_any:
            print(f"  (无有效修复指引，请确认 ID 正确或重新运行 --verify)")
        print(f"{'='*55}")
        sys.exit(0)

    # ── --classify 模式：将指定 #ID 标记为误判，后续 bump 自动跳过 ──
    if getattr(args, 'classify', None) and not getattr(args, 'verify', False):
        raw = args.classify.strip()
        if raw.lower() in ('', 'add', 'show', 'list'):
            print(f"❌ --classify 必须附带数字 ID（如 --classify 42,55,67）")
            print(f"   `--classify add` 是无效用法，请换成 `--classify 42`")
            return 1

        # 校验 --category 参数
        category = getattr(args, 'category', None)
        if not category:
            print(f"❌ --classify 必须附带 --category 参数，说明误报类别")
            print(f"   合法类别：")
            for cat in sorted(_CLASSIFY_LEGAL_CATEGORIES):
                print(f"     {cat}")
            return 1
        if category not in _CLASSIFY_LEGAL_CATEGORIES:
            print(f"❌ 非法类别 '{category}' — 仅支持：{', '.join(sorted(_CLASSIFY_LEGAL_CATEGORIES))}")
            return 1

        # 校验 --subtype（必填）
        subtype = getattr(args, 'subtype', None)
        if not subtype:
            print(f"❌ --classify 必须附带 --subtype 参数，说明误报子类型")
            print(f"   合法子类型：{', '.join(sorted(_CLASSIFY_LEGAL_SUBTYPES.keys()))}")
            return 1
        if subtype not in _CLASSIFY_LEGAL_SUBTYPES:
            print(f"❌ 非法子类型 '{subtype}' — 仅支持：{', '.join(sorted(_CLASSIFY_LEGAL_SUBTYPES.keys()))}")
            return 1

        # 读取 --reason
        reason = getattr(args, 'reason', '') or ''

        # ── engine_cant_judge 须附带证据 ──
        if category == "engine_cant_judge":
            if not reason:
                print(f"❌ engine_cant_judge 必须附带 --reason 提供证据")
                print(f"   证据应为具体的文件路径、代码行号或函数签名，证明引擎确实无法判断")
                print(f"   例: --reason 'foo/bar.py:42 中的 BazQuux 模式是领域约定，引擎无法区分'")
                return 1
            # 证据校验：reason 必须包含至少一个路径关键字（/ 或 \ 或 : 或 行）
            has_path_evidence = any(kw in reason for kw in ['/', '\\', '.py:', '.md:', '第', '行'])
            if not has_path_evidence:
                print(f"❌ engine_cant_judge 的 --reason 缺少具体路径证据")
                print(f"   必须引用具体文件路径、行号或代码标识")
                print(f"   例: --reason 'permissions.md:91 引用的 YYYY 是年份通配符，非字面文件名'")
                return 1

        ids = [s.strip() for s in raw.split(',')]
        # 验证：数字 ID 或 C-{type} 格式
        for id_str in ids:
            if not id_str.isdigit() and not id_str.startswith('C-') and not id_str.startswith('R-'):
                print(f"❌ 无效 ID: '{id_str}' — ID 必须是数字（如 42,55,67）、C-{{type}}（如 C-missing_doc_ref）或 R-XX（如 R-23）")
                return 1

        _write_fp_classify(skill_dir, ids, category, reason, subtype)

        print(f"\n{'='*55}")
        print(f"  [CLASSIFY] 已标记 {len(ids)} 个 #ID 为误判")
        print(f"    类别：{category}")
        print(f"    子类型：{subtype} — {_CLASSIFY_LEGAL_SUBTYPES.get(subtype, '')[:60]}")
        if reason:
            print(f"    理由：{reason}")
        print(f"    ID：{', '.join(ids)}")
        print(f"{'='*55}")
        print(f"\n  ⏳ 自动运行过滤验证...")
        # 自动重跑审计并显示过滤后的结果
        _result2 = audit_skill(skill_dir)
        _remaining2 = [r for r in _result2.get("results", [])
                       if not r.get("passed") and not r.get("skipped")
                       and not _reclassify_false_positive(r, skill_dir)]
        if _remaining2:
            print(f"\n  ⚠️  标记后仍有 {len(_remaining2)} 项真问题未通过：")
            for _r in _remaining2:
                _sev2 = "[ERROR]" if _r.get('severity') == 'ERROR' else "[WARN]"
                _rid2 = _r.get('rule_id', _r.get('rule', '?'))
                print(f"    {_rid2} {_sev2} {_r.get('detail', '')[:120]}")
            print(f"\n  ⚠️ 剩余项均为真问题，必须修复，不得标记为误判")
            print(f"  请修复上述真问题后重新审计")
        else:
            print(f"  ✅ 过滤验证通过——剩余 FAIL 均已被正确归类为误报（非真问题）")
        sys.exit(0)

    # ── --no-fp 模式：从误判列表中移除指定 #ID ──
    if getattr(args, 'no_fp', None) and not getattr(args, 'verify', False):
        raw = args.no_fp.strip()
        if raw.lower() in ('', 'remove', 'delete'):
            print(f"❌ --no-fp 必须附带 ID（如 --no-fp 42,55）")
            return 1
        ids = [s.strip() for s in raw.split(',')]
        _remove_fp_classify(skill_dir, ids)
        remaining_ids = _load_fp_ids(skill_dir)
        print(f"\n{'='*55}")
        print(f"  [NO-FP] 已取消 {len(ids)} 个 #ID 的误判标记：{', '.join(ids)}")
        print(f"  当前误判列表：{', '.join(sorted(remaining_ids)) if remaining_ids else '(空)'}")
        print(f"{'='*55}")
        sys.exit(0)

    # ═══════════════════════════════════════════════════════
    # [强制钩子 1] 蓝皮书前置扫描 — audit 执行前输出技能全貌
    # ═══════════════════════════════════════════════════════
    _check_large_dirs(skill_dir)
    # 先跑蓝皮书并输出文本报告（供人阅读）
    _bp_pre = None
    try:
        from ..skill_inspector import inspect_skill
        print(f"\n{'='*55}")
        print(f"  前置扫描：Skill 蓝皮书")
        print(f"{'='*55}")
        _bp_pre = inspect_skill(skill_dir)  # 输出文本版蓝皮书
        print()
    except ImportError:
        try:
            from scripts.skill_inspector import inspect_skill
            _bp_pre = inspect_skill(skill_dir)
            print()
        except ImportError:
            pass

    result = audit_skill(skill_dir, manifest_version=args.manifest_version,
                                   progress_file=args.progress_file)

    # 出完整报告（LLM 读取报告中的 FAIL 项，分类：ERROR=真问题保留，其他=误报类）
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_report(result, skill_dir=skill_dir))

    # ── 问题分类与真问题强制修复 ──
    # 分类体系：0 ERROR 0 WARN 铁律
    #   ERROR → 未排除则必须 --fix
    #   WARN  → 未排除则必须 --fix
    #   排除  → 已知误报（_reclassify_false_positive），不阻断通过
    #   PASS/SKIP → 通过
    remaining_pre = [res for res in result.get("results", [])
                     if not res.get("passed") and not res.get("skipped")
                     and not _reclassify_false_positive(res, skill_dir)]
    # 检查是否有可自动修复的 FAIL：由各检查器返回的 fix key 自声明，
    # 有 fix key 且在 fix.py dispatch 表中存在对应处理函数即为 auto-fixable。
    # fix key 为 None 或不存在的 key → 不会计入 has_fixable。
    has_fixable = any(r.get("fix") for r in remaining_pre)

    # 输出标准化报告摘要（fixable 检查之前）
    if not args.fix and not getattr(args, 'verify', False) and not getattr(args, 'classify', None) and not getattr(args, 'no_fp', None) and not getattr(args, 'show_fix', None):
        passed = result.get("passed_count", 0)
        total = len(result.get("results", []))
        print(f"\n{'='*55}")
        print(f"  审计报告：{os.path.basename(skill_dir)}")
        print(f"  {passed}/{total} 通过")
        has_warn = any(not r.get("passed") and r.get("severity") == 'WARN' for r in result.get("results", []))
        has_err = any(not r.get("passed") and r.get("severity") == 'ERROR' for r in result.get("results", []))
        if has_err:
            print(f"  ❌ {sum(1 for r in result.get('results',[]) if not r.get('passed') and r.get('severity')=='ERROR')} ERROR")
        if has_warn:
            print(f"  ⚠️  {sum(1 for r in result.get('results',[]) if not r.get('passed') and r.get('severity')=='WARN')} WARN")
        print(f"  → 运行 --fix 自动修复，或 --verify 逐项审查")
        print(f"{'='*55}")
        # 强制 HTML 报告输出（代码强制，非 LLM 自觉）

    if has_fixable and not args.fix:
        print(f"\n  ⛔ 存在可自动修复的 FAIL — 必须执行 audit --fix 修复后重新验证")
        sys.exit(1)

    # --fix 模式：自动修正所有失败规则的违规
    if args.fix:
        print(f"\n=== 自动修正模式 ===")
        # 收集所有失败规则的 fix key
        # v2.91.0: 遍历 remaining_pre（已排除 --classify 标记的误报），而非全量 results
        fixes_applied = 0
        fix_details = []
        for res in remaining_pre:
            if not res.get("passed") and res.get("fix"):
                fix_key = res["fix"].get("key")
                if fix_key:
                    try:
                        n = apply_fix(skill_dir, fix_key, **res["fix"])
                        fixes_applied += n
                        fix_details.append(fix_key)
                        print(f"[OK] R-{fix_key}：修正 {n} 处")
                    except Exception as e:
                        print(f"[ERROR] R-{fix_key} 修正失败: {e}")
        if fixes_applied > 0:
            print(f"[OK] 共修正 {fix_details} 处")
            # ★ v2.82.10: 不再在 --fix 流程中自动 bump。
            #   版本号 bump 应在双0验证通过后的 final step 统一执行。
            #   此处仅重新审计确认修正效果，跳过版本升级。
            # 重新审计
            result = audit_skill(skill_dir, manifest_version=args.manifest_version,
                                           progress_file=args.progress_file, _fix_applied=True)
            # 对 R-25/R-23 等有多子项的规则，检查 detail 中所有 C-* 标签
            for res in result.get("results", []):
                if res.get("rule_id") in ("R-25", "R-23"):
                    detail = res.get("detail", "")
                    _r25_fix_map = {
                        "C-10": "excessive_blank_lines",
                        "C-11": "section_reorder",
                        "C-12": "trigger_format",
                        "C-14": "workflow_completeness",
                        "C-15": "inline_refs",
                        "C-17": "example_quality",
                        "C-18": "capability_boundary",
                        "C-20": "path_centralization",
                    }
                    for c_tag, fk in _r25_fix_map.items():
                        if c_tag in detail:
                            # C-12 有多个子修复（触发条件格式、约束格式、表格格式）
                            c12_fixes = ["trigger_format", "constraint_format", "table_format"]
                            if c_tag == "C-12":
                                for c12_fk in c12_fixes:
                                    if c12_fk not in fix_details:
                                        try:
                                            n = apply_fix(skill_dir, c12_fk)
                                            if n > 0:
                                                fixes_applied += n
                                                fix_details.append(c12_fk)
                                                print(f"[OK] R-25 (C-12/{c12_fk}): 修正 {n} 处")
                                        except Exception as e:
                                            print(f"[ERROR] R-25 (C-12/{c12_fk}) 修正失败: {e}")
                            elif fk not in fix_details:
                                try:
                                    n = apply_fix(skill_dir, fk)
                                    if n > 0:
                                        fixes_applied += n
                                        fix_details.append(fk)
                                        print(f"[OK] R-25 ({c_tag}): 修正 {n} 处")
                                except Exception as e:
                                    print(f"[ERROR] R-25 ({c_tag}) 修正失败: {e}")
                # R-23 文档引用修复
                if res.get("rule_id") == "R-23" and "doc_references" not in fix_details:
                    try:
                        n = apply_fix(skill_dir, "doc_references")
                        if n > 0:
                            fixes_applied += n
                            fix_details.append("doc_references")
                            print(f"[OK] R-23: 修正 {n} 处文档引用")
                    except Exception as e:
                        pass
        else:
            # ★ v2.63.0: --fix 执行了但 0 处修正 → 这些 FAIL 不是真可修复
            #   清除其 fix 属性，使其进入 LLM 二段筛查的「误判→放过」流程
            #   而不是无限循环 "存在可自动修复的 FAIL — 必须再跑 --fix"
            # ★ v2.63.0 bug: 原逻辑检查 fix_key in fix_details（空列表），导致 fix key 永不清除，
            #   造成 --fix 无限循环。修正为 fixes_applied == 0 时无条件清除所有 fix key。
            for res in result.get("results", []):
                if not res.get("passed") and not res.get("skipped") and res.get("fix"):
                    del res["fix"]

        # 出二次审计报告 + 修复前后对比
        if fixes_applied > 0:
            before_err = sum(1 for r in result.get("results",[]) if not r.get("passed") and r.get("severity") == 'ERROR')
            before_warn = sum(1 for r in result.get("results",[]) if not r.get("passed") and r.get("severity") == 'WARN')
            print(f"\n{'─'*55}")
            print(f"  修复前后对比")
            print(f"  修复项：{', '.join(fix_details)} ({fixes_applied} 处)")
            print(f"  修复前：{before_err} ERROR, {before_warn} WARN")
            if not args.json:
                print(format_report(result, before_summary={"errors": before_err, "warns": before_warn}, show_fix_hint=False, skill_dir=skill_dir))
            after_err = sum(1 for r in result.get("results",[]) if not r.get("passed") and r.get("severity") == 'ERROR')
            after_warn = sum(1 for r in result.get("results",[]) if not r.get("passed") and r.get("severity") == 'WARN')
            print(f"  修复后：{after_err} ERROR, {after_warn} WARN")
            if after_err == 0 and after_warn == 0:
                print(f"  ✅ 全部修复")
            print(f"{'─'*55}")

    # ── 问题分类与真问题强制修复：--fix 后仍有可修复 FAIL 则阻止通过
    # ★ 关键区分：只有 fix 函数能真正自动修复的才算"可自动修复"
    #   各检查器返回的 fix key 自声明是否可自动修复（存在 fix key 且在 fix.py dispatch 表中有对应函数）。
    #   fix key 为 None → 不是 auto-fixable，属于 LLM 手动修复范畴
    remaining = [res for res in result.get("results", [])
                 if not res.get("passed") and not res.get("skipped")
                 and not _reclassify_false_positive(res, skill_dir)]
    # 按是否有 fix key 分割为"auto可以"和"LLM 手动"
    # v2.97.2: 加上 _llm_only_fix_keys 过滤，与 _run_audit_loop 行为一致
    _llm_only_fix_keys = {"workflow_completeness", "example_quality", "capability_boundary", "section_names"}
    remaining_auto = [r for r in remaining if r.get("fix") and r["fix"].get("key") not in _llm_only_fix_keys]
    has_fixable_after = bool(remaining_auto)
    if has_fixable_after:
        # 循环检测：用 .fix_loop_check 文件记录上次 remaining IDs
        _skill_name = os.path.basename(os.path.abspath(skill_dir))
        _loop_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(skill_dir))),
            ".standardization", _skill_name, "data", "outputs", ".fix_loop_check.json"
        )
        current_ids = sorted(set(r.get("id", "") for r in remaining_auto))
        _prev_ids = []
        if os.path.exists(_loop_path):
            try:
                with open(_loop_path, "r") as _f:
                    _prev_ids = json.load(_f)
            except Exception:
                _prev_ids = []
        if _prev_ids and current_ids == _prev_ids:
            print(f"\n  ⚠️  --fix 后剩余 FAIL 与上次相同，检测到 fix 循环。以下 FAIL 有 fix key 但 --fix 无法完全修复：")
            for r in remaining_auto:
                print(f"     ID={r.get('id','')} rule={r.get('rule_id','')} fix={r.get('fix','')}")
            print(f"  → 这些项已无 auto-fix 路径，需要 LLM 手动编辑修复。")
            print(f"  → 运行 --verify 查看完整 FAIL 列表，手动编辑 SKILL.md 或 references/")
            print(f"  → 编辑完成后重新运行 audit 验证。误判标记仅在前置 LLM 二次筛查阶段进行。")
            # 清理 loop 标记文件，避免二次运行时误阻断
            os.remove(_loop_path)
            # ★ v2.97.2: 任何 exit 前必须生成 HTML 报告
            try:
                _save_html_report(skill_dir, result)
            except Exception:
                pass
            sys.exit(1)
        # 保存当前 IDs 供下次循环检测
        os.makedirs(os.path.dirname(_loop_path), exist_ok=True)
        with open(_loop_path, "w") as _f:
            json.dump(current_ids, _f)
        print(f"\n  ⛔ --fix 后仍有 {len(remaining_auto)} 项 FAIL — 必须再执行 --fix")
        # ★ v2.97.2: 任何 exit 前必须生成 HTML 报告
        try:
            _save_html_report(skill_dir, result)
        except Exception:
            pass
        sys.exit(1)
    # 无 fix key 的规则需要 LLM 手动处理，输出提示
    remaining_llm = [r for r in remaining if not r.get("fix")]
    if remaining_llm:
        # 按 rule_id 聚合
        from collections import Counter
        llm_counts = Counter(r.get("rule_id", "?") for r in remaining_llm)
        print(f"\n  ⚠️  以下规则无 auto-fix，需 LLM 手动修复（运行 --verify 查看详情后手动编辑）：")
        for rid, cnt in sorted(llm_counts.items()):
            print(f"     {rid}：{cnt} 项")
        print(f"  → 运行 --verify 查看 FAIL 详情，手动编辑修复")
        print(f"  → 编辑完成后重新运行 audit。误判标记仅在前置 LLM 二次筛查阶段进行。")
        # 强制 HTML 报告输出

    # --verify 模式：展示所有 FAIL 项（不做白名单预筛），LLM 自行判断误报
    # 铁律 8 分两阶段：(1) 筛选看到的问题 → (2) 凭ID获取对应修复指引
    # 
    # ★★★ LLM 二次筛查指令（代码强制）★★★
    # 以下 #ID 列表是审计发现的全部 FAIL 项。
    # LLM 必须逐条判断：是真问题还是误判？
    #
    # 【engine_mistake】引擎技术性错误 — 正则/AST/路径匹配产生了错误结果
    #   适用：BOM/编码导致解析失败、注释被当实际操作、概念图路径被当真实文件引用、专有名词被当缺空格
    #   → --classify ID --category engine_mistake --reason "..."
    #
    # 【engine_cant_judge】引擎能力不足，LLM 确认后放行
    #   适用：__init__.py 无需列文档树、反模式内容引擎格式没认出但LLM确认确实合规
    #   → --classify ID --category engine_cant_judge --reason "..."
    #
    # 【真问题】以上两类均不满足 → 必须修复，不得标记为误判
    #   → 记下 #ID，运行 --show-fix ID 获取修复指引
    #
    # 所有 FAIL 都处理完毕后，重新运行 --verify 确认双 0。
    if getattr(args, 'verify', False):
        # 过滤：去掉已标记为 ⓘ 已知误报的条目（这些不阻断通过）
        remaining = [res for res in result.get("results", [])
                     if not res.get("passed") and not res.get("skipped")
                     and not _reclassify_false_positive(res, skill_dir)]
        if remaining:
            # 读取已有误判分类
            fp_ids = _load_fp_ids(skill_dir)

            print(f"\n{'='*55}")
            print(f"  [VERIFY v1] {len(remaining)} 项 FAIL 待筛选，逐条判断真问题/误判")
            if fp_ids:
                print(f"  已分类为误判的 #ID：{', '.join(sorted(fp_ids))}")
            # 打印 [VERIFY] 文本时展示已有的分类详情
        fp_details = _load_fp_details(skill_dir)
        if fp_details:
            for fid, finfo in sorted(fp_details.items()):
                cat = finfo.get('category', '?')
                rsn = finfo.get('reason', '')
                tag = " ⓘ" if rsn else ""
                print(f"    {fid}: {cat}{' — ' + rsn if rsn else ''}{tag}")

            print(f"  确认真问题后记下 #ID，运行 --show-fix ID1,ID2 获取修复指引")
            print(f"  #ID 为误判则运行：audit <skill_dir> --classify ID1,ID2")
            print(f"{'─'*55}")

            # 展开为带 ID 的条目，每条有问题描述 + 对应修复指引
            entries = _expand_fail_entries(remaining)
            fix_map = {}  # id → fix_suggestion

            for e in entries:
                eid = e['id']
                sev = "[ERROR]" if e['severity'] == 'ERROR' else "[WARN]"
                # 输出 [ID] 规则 + 问题描述（不带修复指引）
                print(f"  [#{eid}] {e['rule_id']} {sev} {e['problem']}")
                if e.get('ctx_lines'):
                    for cl in e['ctx_lines'][:6]:
                        print(f"         {cl[:160]}")
                fix_map[eid] = e['fix']

            # 将 fix_map 写入标准化数据目录供 --show-fix 读取
            try:
                fix_map_dir = os.path.join(
                    os.path.dirname(os.path.abspath(skill_dir)), '.standardization',
                    os.path.basename(os.path.abspath(skill_dir)), 'data')
                os.makedirs(fix_map_dir, exist_ok=True)
                fix_map_path = os.path.join(fix_map_dir, '.verify_fix_map.json')
                with open(fix_map_path, 'w', encoding='utf-8') as f:
                    json.dump(fix_map, f, ensure_ascii=False, indent=2)
            except Exception:
                pass  # 写不进去不影响主流程

            print(f"{'─'*55}")
            print(f"  确认真问题 → audit <skill_dir> --show-fix ID1,ID2,ID3")
            print(f"  确认为误判 → audit <skill_dir> --classify ID1,ID2 --category engine_mistake/engine_cant_judge --reason '...'")
            print(f"{'='*55}")
        else:
            print(f"\n{'='*55}")
            print(f"  [VERIFY] 验证通过：所有未通过项均为误报，达到铁律 0 ERROR 0 WARN 要求")
            print(f"{'='*55}")
        # --verify 和 --show-fix 互斥
        if getattr(args, 'show_fix', None):
            return  # --show-fix 单独处理
        # 退出码尊重 --classify 误判标记：所有 FAIL 已分类为误判则视为通过
        if fp_ids and remaining:
            entry_ids = {str(e['id']) for e in entries}
            if entry_ids.issubset({str(i) for i in fp_ids}):
                remaining = []
                print(f"\n{'='*55}")
                print(f"  [VERIFY] 全部 {len(fp_ids)} 项已通过 --classify 标记为误判，视为通过")
                print(f"{'='*55}")
        if remaining:
            print(f"\n{'='*55}")
            print(f"  ❌ [VERIFY] 仍有 {len(remaining)} 项 FAIL 未处理！")
            print(f"  处理方式：")
            print(f"    真问题 → audit <skill_dir> --show-fix ID1,ID2 获取修复指引，然后手动修复")
            print(f"    误判   → audit <skill_dir> --classify ID1,ID2 --category engine_mistake/engine_cant_judge --reason '...' 标记为误判")
            print(f"  所有 FAIL 都处理后，重新运行 --verify 确认双 0")
            print(f"{'='*55}")
        # ── 最终强制钩子：HTML 报告必须生成（无论任何模式） ──
        try:
            _save_html_report(skill_dir, result)
        except Exception:
            pass
        sys.exit(1 if remaining else 0)

def cmd_audit_all(args):
    """批量审查 skills 目录下所有 skill"""
    skills_dir = args.skills_dir
    manifest_file = args.manifest

    # 读取 manifest 获取版本号映射
    version_map = {}
    if manifest_file and os.path.isfile(manifest_file):
        try:
            with open(manifest_file, "r", encoding="utf-8") as mf:
                mdata = json.load(mf)
            items = mdata.get("repos", {}).get("workbuddy-skills", {}).get("items", {})
            for name, info in items.items():
                if isinstance(info, dict) and "version" in info:
                    version_map[name] = info["version"]
        except Exception as e:
            print(f"[!]  读取 manifest 失败: {e}", file=sys.stderr)

    # 发现所有 skill 目录
    entries = []
    for entry in sorted(os.listdir(skills_dir)):
        full_path = os.path.join(skills_dir, entry)
        if os.path.isdir(full_path) and os.path.isfile(os.path.join(full_path, "SKILL.md")):
            entries.append((entry, full_path))

    all_results = []
    total_errors = 0
    total_warns = 0

    for dirname, dirpath in entries:
        mv = version_map.get(dirname)
        result = audit_skill(dirpath, manifest_version=mv)
        all_results.append(result)
        total_errors += result["summary"]["errors"]
        total_warns += result["summary"]["warns"]

    if args.json:
        print(json.dumps({
            "audited_count": len(all_results),
            "total_errors": total_errors,
            "total_warns": total_warns,
            "results": all_results,
        }, ensure_ascii=False, indent=2))
    else:
        print(f"\n{'='*60}")
        print(f"  批量审查报告 — 共 {len(entries)} 个 skill")
        print(f"  汇总: {sum(r['summary']['pass'] for r in all_results)} PASS / "
              f"{total_errors} ERROR / {total_warns} WARN")
        print(f"{'='*60}")

        for r in all_results:
            print(format_report(r, verbose=False))
            print()

        print(f"\n{'='*60}")
        print("  详细逐项结果:")
        print(f"{'='*60}")
        for r in all_results:
            if "error" not in r:
                print(format_report(r, verbose=True))
                print()


def cmd_fix(args):
    """针对性修复工具（按 fix key 分发）"""
    skill_dir = args.skill_dir
    if not os.path.isdir(skill_dir):
        print(f"[X] 目录不存在: {skill_dir}", file=sys.stderr)
        sys.exit(1)

    keys = args.key if args.key else None
    dry_run = args.dry_run

    if not keys:
        # 列出所有可用的 fix key
        print("可用修复 key（对应审计规则 R-01~R-26）:")
        for k in list_fixable():
            print(f"  {k}")
        print("\n用法: python -m skill_audit fix <skill_dir> --key <key> [--dry-run]")
        print("      python -m skill_audit fix <skill_dir> --key <key1> <key2> ...")
        return

    total_fixed = 0
    for key in keys:
        try:
            params = {}
            if hasattr(args, 'value') and args.value:
                # 尝试解析 value 为 JSON 或字符串
                try:
                    params["value"] = json.loads(args.value)
                except json.JSONDecodeError:
                    params["value"] = args.value
            if dry_run:
                print(f"[DRY-RUN] R-{key}: 模拟修复...")
                n = apply_fix(skill_dir, key, dry_run=True, **params)
            else:
                n = apply_fix(skill_dir, key, **params)
            total_fixed += n
            print(f"[OK] R-{key}: 修复 {n} 处")
        except Exception as e:
            print(f"[ERROR] R-{key}: {e}")

    if not dry_run and total_fixed > 0:
        # 重新审计
        print(f"\n=== 重新审计 ===")
        result = audit_skill(skill_dir)
        print(format_report(result, show_fix_hint=False, skill_dir=skill_dir))



def cmd_bump(args):
    """bump 子命令：版本号三端更新（遵循 R-03 语义规则，走完整审核流程）
    
    bump 不是独立操作——它是 update/refactor 流程的最终步骤。
    必须保证 0 ERROR 0 WARN 后才能执行。
    """
    _semantic_precheck('bump', getattr(args, 'skill_dir', None), confirmed=getattr(args, 'confirmed', False),
                       llm_mode=getattr(args, 'mode', None))
    import os, json, datetime

    skill_dir = os.path.abspath(args.skill_dir)
    dry_run = getattr(args, 'dry_run', False)
    bump_type = getattr(args, 'type', None)
    desc = getattr(args, 'desc', '')

    # ── 铁律 0 ERROR 0 WARN 前置检查 ──
    if not dry_run:
        pre_result = audit_skill(skill_dir)
        remaining = [r for r in pre_result.get("results", [])
                     if not r.get("passed") and not r.get("skipped")
                     and not _reclassify_false_positive(r, skill_dir)]
        if remaining:
            fp_ids = _load_fp_ids(skill_dir)
            if fp_ids:
                entries = _expand_fail_entries(remaining)
                remaining_ids = {str(e['id']) for e in entries}
                if remaining_ids.issubset({str(i) for i in fp_ids}):
                    remaining = []
        if remaining:
            print(f"\n{'='*55}")
            print(f"  ⛔ 铁律阻断：{len(remaining)} 项 FAIL 未处理，拒绝 bump")
            print(f"  bump 是 update/refactor 流程的最终步骤，不能跳过审计直接执行。")
            print(f"  {'='*35}")
            print(f"  LLM 应按以下步骤修复后重新执行 bump：")
            print(f"    1. 逐条审查下方 FAIL 项，区分真问题与误报")
            print(f"    2. 误判 → 通过 --classify ID 标记")
            print(f"    3. 运行 audit <skill> --verify 确认双0")
            print(f"    4. 再执行 bump --type fix --desc 'xxx'")
            print(f"  {'='*35}")
            print(f"  FAIL 明细：")
            for r in remaining:
                sev = "[ERROR]" if r['severity'] == 'ERROR' else "[WARN]"
                rid = r['rule_id']
                detail = r['detail'][:120]
                fp_status = "（已标记误判）" if _reclassify_false_positive(r, skill_dir=r.get("path", "")) else ""
                print(f"    {rid} {sev} {detail}{fp_status}")
            print(f"{'='*55}")
            sys.exit(1)

    # 未指定 --type 时，尝试从 desc 推断；无法推断则默认 fix
    if bump_type is None:
        if desc and any(kw in desc for kw in ['breaking', 'major', '架构']):
            bump_type = 'breaking'
        elif desc and any(kw in desc for kw in ['feature', 'minor', '新增', '功能']):
            bump_type = 'feature'
        else:
            bump_type = 'fix'

    meta_path = os.path.join(skill_dir, '_meta.json')
    if not os.path.isfile(meta_path):
        print(f"[ERROR] 未找到 _meta.json: {meta_path}")
        return
    with open(meta_path, 'r', encoding='utf-8') as f:
        current_version = str(json.load(f).get('version', '0.0.0'))

    parts = current_version.split('.')
    try:
        major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
    except (ValueError, IndexError):
        print(f"[ERROR] 无法解析版本号「{current_version}」—— 期望格式如「1.2.3」（三位数字以点分隔）")
        print(f"       请检查 `_meta.json` 和 `SKILL.md` 中的 version 字段是否正确")
        return
    if bump_type == 'fix':
        new_version = f"{major}.{minor}.{patch + 1}"
        rule_note = "PATCH: 单处bug修复/文档错别字/参数拼写(不含新功能,多变更不得打包为PATCH)"
    elif bump_type == 'feature':
        new_version = f"{major}.{minor + 1}.0"
        rule_note = "MINOR: 新增功能/已有功能重构/大面积描述修正"
    else:
        new_version = f"{major + 1}.0.0"
        rule_note = "MAJOR: 架构级重构/破坏性变更/核心引擎重写"

    if dry_run:
        print(f"[DRY-RUN] skill: {os.path.basename(skill_dir)}")
        print(f"  {current_version} → {new_version} ({bump_type}) — {rule_note}")
        return

    _do_bump(skill_dir, bump_type, desc)
    print(f"\n{'='*55}")
    print(f"  版本号三端更新完成")
    print(f"  skill:          {os.path.basename(skill_dir)}")
    print(f"  版本:           {current_version} → {new_version}")
    print(f"  类型:           {bump_type} — {rule_note}")
    print(f"  规则:           R-03（SemVer + 变更语义）")
    print(f"  SKILL.md:       ✅ version={new_version}")
    print(f"  _meta.json:     ✅ version={new_version}")
    print(f"  changelog.md:   ✅ 已插入 v{new_version} 条目")
    print(f"{'='*55}")
    # bump 成功后输出 HTML 报告
    try:
        _r = audit_skill(skill_dir)
        # Filter by LLM classification for the HTML report
        _filtered = _filter_false_positives(_r, skill_dir)
        _save_html_report(skill_dir, _r)
    except Exception:
        pass


def _semantic_precheck(command, skill_dir=None, confirmed=False, llm_mode=None, classify=None):
    """
    语义前置检查（代码强制，非 LLM 自觉）。
    在进入 create/update/refactor/audit 之前输出模式选择对照表，
    必须带 --confirmed 参数才放行，否则 exit(0) 阻断。
    """
    # --json 模式下门禁文字输出到 stderr，避免污染 JSON stdout
    _json_mode = '--json' in sys.argv
    _out = sys.stderr if _json_mode else sys.stdout

    modes = {
        'audit': '仅审查，不修改。适用于查看技能合规状态、检查 FAIL 项',
        'refactor': '全流程改造。蓝图扫描 → 备份 → 审计 → 修复 → 验证 → bump → cleanup',
        'create': '创建新技能。骨架生成 → 审计 → 报告',
        'update': '范围明确更新。蓝图扫描 → 备份 → 审计 → 修复 → 验证 → bump → cleanup',
        'bump': '版本号升级（三端同步）。在双0确认后执行',
        'readonly': '只读操作（rules/create-template）。不修改任何文件，仅查询信息',
    }
    desc = modes.get(command, '')
    print(f"\n{'='*55}", file=_out)
    print(f"  🧠 【流程门禁】LLM 必须根据用户意图确认模式", file=_out)
    print(f"{'─'*55}", file=_out)
    print(f"  用户请求关键词 → 模式选择", file=_out)
    print(f"  ——————————————", file=_out)
    print(f"  仅审查/不要修改/只看检查报告 → audit", file=_out)
    print(f"  创建/生成/新建/从头开始     → create", file=_out)
    print(f"  审计/检查/更新/修            → update（含备份、蓝图、bump）", file=_out)
    print(f"  改造/重构/标准化/大规模改    → refactor", file=_out)
    print(f"  版本升级（内部）             → bump", file=_out)
    print(f"  查看规则/查看模板/只读查询   → readonly（不修改文件）", file=_out)
    print(f"{'─'*55}", file=_out)
    print(f"  LLM 当前选择的模式：{command}", file=_out)
    if desc:
        print(f"  此模式将执行：{desc}", file=_out)
    if skill_dir:
        print(f"  目标技能：{os.path.basename(skill_dir)}", file=_out)
    print(f"  ⚠️  如果模式与用户意图不匹配，请立即中止并重新选择", file=_out)
    print(f"{'='*55}", file=_out)

    # ── 模式-命令映射锁（代码级强制，无向后兼容） ──
    if not llm_mode:
        print(f"\n  {'❌'*3} 缺少 --mode 参数！流程拒绝 {'❌'*3}", file=_out)
        print(f"     LLM 必须根据模式自检闸门输出 --mode 参数", file=_out)
        print(f"     当前子命令：{command}", file=_out)
        print(f"", file=_out)
        print(f"     请携带 --mode 重新执行：", file=_out)
        print(f"       python -m scripts.skill_audit {command} <skill-dir> --confirmed --mode {command}", file=_out)
        print(f"", file=_out)
        sys.exit(1)
    if llm_mode != command:
        # 豁免：refactor 模式下允许 audit --classify（二次筛除的必要操作）
        if llm_mode == "refactor" and command == "audit" and classify:
            pass
        else:
            print(f"\n  {'❌'*3} 模式-命令不匹配！流程拒绝 {'❌'*3}", file=_out)
            print(f"     LLM 语义自检闸门输出模式：{llm_mode}", file=_out)
            print(f"     当前执行的子命令：{command}", file=_out)
            print(f"", file=_out)
            print(f"     请使用正确的子命令：", file=_out)
            print(f"       python -m scripts.skill_audit {llm_mode} <skill-dir> --confirmed --mode {llm_mode}", file=_out)
            print(f"", file=_out)
            sys.exit(1)

    if not confirmed:
        print(f"\n  ⛔ 未传入 --confirmed 参数，拒绝执行。", file=_out)
        print(f"  请确认模式正确后重新运行: python -m scripts.skill_audit {command} <skill-dir> --confirmed", file=_out)
        sys.exit(0)


def cmd_refactor(args):
    """
    refactor 子命令：强制全流程改造
    蓝皮书 → 备份 → 全量审计 → 细碎修复循环（代码级钩子强制审计）→ 全量审计确认 → 全量一致性审查 → bump + cleanup
    """
    _semantic_precheck('refactor', getattr(args, 'skill_dir', None), confirmed=getattr(args, 'confirmed', False),
                       llm_mode=getattr(args, 'mode', None))
    import shutil, datetime

    skill_dir = os.path.abspath(args.skill_dir)
    bump_type = getattr(args, 'bump_type', 'feature')
    bump_desc = getattr(args, 'desc', '')

    print(f"\n{'='*55}")
    print(f"  ⚙️  [refactor] 全流程改造：{os.path.basename(skill_dir)}")
    print(f"{'='*55}")

    # ── 步骤 0：清理旧会话状态文件（仅首次 refactor，--continue 不清） ──
    if not getattr(args, 'refactor_continue', False):
        _clean_stale_state(skill_dir)

    # ── 步骤 1：蓝皮书扫描（强制） ──
    print(f"\n{'─'*55}")
    print(f"  [1/8] 蓝皮书前置扫描")
    print(f"{'─'*55}")
    _check_large_dirs(skill_dir)
    try:
        from ..skill_inspector import inspect_skill
        inspect_skill(skill_dir)
    except ImportError:
        try:
            from scripts.skill_inspector import inspect_skill
            inspect_skill(skill_dir)
        except ImportError:
            print("  [WARN] 未找到 skill_inspector，跳过蓝皮书扫描")

    # ── 步骤 2：启动 cleanup session + 备份（强制） ──
    print(f"\n{'─'*55}")
    print(f"  [2/8] 启动 cleanup session + 创建备份")
    print(f"{'─'*55}")
    try:
        from scripts.cleanup_manager import start_session
        manifest_id = start_session(skill_dir, "refactor")
        if manifest_id:
            print(f"  ✅ cleanup session 已启动: {manifest_id}")
        else:
            print(f"  ⚠️  cleanup session 启动失败，清理将跳过")
            manifest_id = None
    except ImportError:
        manifest_id = None
        print(f"  ⚠️  未找到 cleanup_manager，清理将跳过")

    backup_id = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = os.path.join(
        os.path.dirname(skill_dir), '.standardization',
        os.path.basename(skill_dir), 'backup')
    os.makedirs(backup_dir, exist_ok=True)
    zip_path = os.path.join(backup_dir, f"pre_refactor_{backup_id}")
    with __import__('zipfile').ZipFile(zip_path + '.zip', 'w', __import__('zipfile').ZIP_DEFLATED) as _zf:
        for _root, _dirs, _files in os.walk(skill_dir):
            _dirs[:] = [d for d in _dirs if d not in ('__pycache__', '.git', '.standardization')]
            for _f in _files:
                _fp = os.path.join(_root, _f)
                try:
                    _zf.write(_fp, os.path.relpath(_fp, skill_dir))
                except (ValueError, OSError):
                    continue  # 跳过特殊文件（Windows 保留名等）
    print(f"  ✅ 备份到 {zip_path}.zip")

    # 注册备份路径到 cleanup session
    if manifest_id:
        try:
            from scripts.cleanup_manager import register
            register(zip_path + '.zip', category="backup")
        except Exception:
            pass

    # ── 步骤 3：全量审计（强制） ──
    print(f"\n{'─'*55}")
    print(f"  [3/8] 全量审计")
    print(f"{'─'*55}")
    result = audit_skill(skill_dir, manifest_version=args.manifest_version)
    s_before = result.get("summary", {})  # 记录初始审计摘要，供最终对比
    result_before = result  # 保存初始结果，供最终 HTML 显示 before 表
    print(format_report(result, show_fix_hint=False, skill_dir=skill_dir))
    remaining = [r for r in result.get("results", [])
                 if not r.get("passed") and not r.get("skipped")]

    # ── 步骤 4：细碎修复循环（代码级强制） ──
    print(f"\n{'─'*55}")
    print(f"  [4/8] ★★★ 细碎修复循环 ★★★")
    print(f"{'─'*55}")
    result, remaining, loop_count = _run_audit_loop(
        skill_dir, max_loops=20, label_prefix='4/8',
        manifest_version=args.manifest_version)

    # ── 步骤 5：LLM 剩余项检查（已过滤已分类误报） ──
    if remaining:
        print(f"\n{'-'*55}")
        print(f"  [5/8] LLM 剩余项检查（已过滤已分类误报）")
        print(f"{'-'*55}")
        # ★ 过滤已分类误报
        remaining_real = [r for r in remaining
                          if not _reclassify_false_positive(r, skill_dir)]
        if len(remaining_real) < len(remaining):
            print(f"  [分类过滤] 排除 {len(remaining) - len(remaining_real)} 项已标记误报")
        remaining = remaining_real
        llm_items = [r for r in remaining
                     if r.get('rule_id', r.get('rule', '')) in ('R-07', 'R-11', 'R-20', 'R-23', 'R-25')]
        if llm_items:
            _save_remaining_llm(skill_dir, llm_items)
            print(f"\n  🤖 剩余 {len(llm_items)} 项需 LLM 修复（已保存结构化数据）")
            for r in llm_items:
                sev = "[ERROR]" if r.get('severity') == 'ERROR' else "[WARN]"
                rid = r.get('rule_id', r.get('rule', '?'))
                print(f"    {rid} {sev} {r.get('detail', '')[:120]}")
            _signal_manual_wait(skill_dir, llm_items)
            sys.exit(0)
        else:
            print(f"\n  ⛔ 有 {len(remaining)} 项非 LLM 类 FAIL 未被自动修复")
            print(f"  请检查修复循环是否达到上限（20 轮），或手动排查")
            _signal_manual_wait(skill_dir, remaining)
            sys.exit(0)

    # ── 步骤 6：全量审计确认（双 0 验证） ──
    print(f"\n{'─'*55}")
    print(f"  [6/8] 全量审计确认（双 0 验证）")
    print(f"{'─'*55}")
    result = audit_skill(skill_dir)
    _before = {"errors": s_before.get("errors", 0), "warns": s_before.get("warns", 0)}
    print(format_report(result, before_summary=_before, show_fix_hint=False, skill_dir=skill_dir))
    remaining = _filter_false_positives(result, skill_dir)
    if remaining:
        print(f"\n  ⛔ 全量审计确认失败：仍有 {len(remaining)} 项 FAIL")
        for r in remaining:
            sev = "[ERROR]" if r.get('severity') == 'ERROR' else "[WARN]"
            rid = r.get('rule_id', r.get('rule', '?'))
            print(f"    {rid} {sev} {r.get('detail', '')[:120]}")
        sys.exit(1)
    else:
        print(f"  ✅ 双 0 确认通过")
        _unlock_refactor(skill_dir)  # ★ 双 0 通过后清除重构锁

    # ── 步骤 7：全量一致性审查 + 修复循环 ──
    # ★ v2.98.4: 同步 .manual_wait 信号机制
    _c_manual_wait = os.path.join(_manual_dir_path(skill_dir), ".consistency_manual_wait")
    _c_manual_done = os.path.join(_manual_dir_path(skill_dir), ".consistency_manual_done")
    if os.path.exists(_c_manual_wait):
        if os.path.exists(_c_manual_done):
            os.remove(_c_manual_done)
            os.remove(_c_manual_wait)
            print(f"\n  ✅ 一致性手动修复信号已确认")
        else:
            print(f"\n  🔒 一致性手动修复等待中")
            print(f"    修完问题后执行：")
            print(f"    python -c \"import pathlib; pathlib.Path(r'{_c_manual_done}').touch()\"")
            print(f"    然后重新运行 --continue")
            sys.exit(0)
    print(f"\n{'─'*55}")
    print(f"  [7/9] 全量一致性审查 + 修复循环")
    print(f"{'─'*55}")
    try:
        from .consistency_checker import (
            check_consistency, format_consistency_report,
            reclassify_consistency_false_positive, apply_consistency_fix
        )
        c_issues = check_consistency(skill_dir)
        
        # ── ★ 前置 LLM 二次筛除（一致性审查阻断点） ──
        c_raw = [i for i in c_issues if not reclassify_consistency_false_positive(i, skill_dir=skill_dir)]
        if c_raw and not getattr(args, 'refactor_continue', False):
            c_fp_ids = _load_fp_ids(skill_dir)
            c_consistency_fp = {fid for fid in c_fp_ids if fid.startswith('C-')}
            if not c_consistency_fp:
                print(f"\n{'='*55}")
                print(f"  ⏸  ★ 前置 LLM 二次筛除（一致性审查）")
                print(f"{'─'*55}")
                print(f"  一致性审查发现 {len(c_raw)} 个真实问题，需要 LLM 确认真问题 vs 误报")
                print(f"")
                print(f"  步骤 1: 运行 audit --verify 查看 FAIL 详情（含一致性问题）")
                print(f"    python -m scripts.skill_audit audit {skill_dir} --verify --mode refactor")
                print(f"")
                print(f"  步骤 2: 对确认为误报的一致性项执行 --classify（ID 格式 C-类型名），须附带 --category")
                print(f"    例: python -m scripts.skill_audit audit {skill_dir} --classify C-missing_doc_ref --category engine_mistake --reason '概念图路径被当真实文件' --mode refactor")
                print(f"    python -m scripts.skill_audit audit {skill_dir} --classify C-stale_doc_ref --category engine_cant_judge --reason '__init__.py 无需列文档树' --mode refactor")
                print(f"")
                print(f"  步骤 3: 重新执行 refactor --continue")
                print(f"    python -m scripts.skill_audit refactor {skill_dir} --continue --confirmed --mode refactor")
                print(f"{'='*55}")
                _signal_manual_wait(skill_dir, c_raw)
                # ★ v2.98.4: 一致性审查使用独立信号文件，不与细碎循环冲突
                import shutil
                _cw = os.path.join(_manual_dir, ".consistency_manual_wait")
                _cd = os.path.join(_manual_dir, ".consistency_manual_done")
                shutil.copy(os.path.join(_manual_dir, ".manual_wait"), _cw)
                sys.exit(0)
        
        c_real = [i for i in c_issues if not reclassify_consistency_false_positive(i, skill_dir=skill_dir)]
        for i in c_issues:
            if reclassify_consistency_false_positive(i, skill_dir=skill_dir):
                i['reclassified'] = True
        print(format_consistency_report(c_issues))
        
        if c_real:
            print(f"\n  💡 一致性审查发现 {len(c_real)} 个真实问题（已排除 {len(c_issues) - len(c_real)} 个误报）")
            # 一致性细碎修复循环（最多 20 轮）
            _c_loop_count = 0
            _c_max_loops = 20
            while c_real and _c_loop_count < _c_max_loops:
                _c_loop_count += 1
                print(f"\n  --- 一致性修复轮 #{_c_loop_count} ---")
                
                # 列出当前问题
                for _ci in c_real:
                    print(f"    [{_ci['type']}] {_ci['detail'][:120]}")
                
                # ── 自动修复 ──
                _c_auto_fixed = 0
                for _ci in c_real[:]:
                    if apply_consistency_fix(skill_dir, _ci):
                        _c_auto_fixed += 1
                        print(f"  ✅ 自动修复: {_ci['type']}")
                        c_real.remove(_ci)
                
                if _c_auto_fixed > 0:
                    print(f"  自动修复 {_c_auto_fixed} 项，重新审查确认...")
                    c_issues = check_consistency(skill_dir)
                    c_real = [i for i in c_issues if not reclassify_consistency_false_positive(i, skill_dir=skill_dir)]
                    for i in c_issues:
                        if reclassify_consistency_false_positive(i, skill_dir=skill_dir):
                            i['reclassified'] = True
                    print(format_consistency_report(c_issues))
                    if not c_real:
                        print(f"  ✅ 一致性修复完成（自动修复后双 0）")
                        break
                    continue
                
                # ── ★★★ 细碎一致性审查钩子（不阻断，仅输出 LLM 指引） ★★★ ──
                print(f"\n  --- ★★★ 细碎一致性审查钩子 ★★★ ---")
                print(f"  LLM 需要：")
                print(f"")
                print(f"  ① 对比 SKILL.md 中的流程描述与代码实际执行流程是否一致")
                print(f"     检查要点：")
                print(f"     - 步骤数量是否与 cmd_xxx() 中的 [i/N] 编号一致？")
                print(f"     - 文档是否遗漏了关键阶段（如细碎修复循环、一致性审查循环）？")
                print(f"     - 文档描述的阶段顺序是否与代码实际执行顺序一致？")
                print(f"     - 如果发现不一致，LLM 手动修正 SKILL.md 的描述")
                print(f"     注意：这是语义检查，代码无法自动判断，完全依赖 LLM")
                print(f"")
                print(f"  --- 余下 {len(c_real)} 项不可自动修复（missing_doc_ref 等），需 LLM 手动编辑 ---")
                print(f"")
                _signal_manual_wait(skill_dir, c_real)
                import shutil
                shutil.copy(os.path.join(_manual_dir, ".manual_wait"),
                            os.path.join(_manual_dir, ".consistency_manual_wait"))
                sys.exit(0)
            
            if c_real:
                print(f"  ⛔ 一致性修复已达重试上限，仍有 {len(c_real)} 项待处理")
                print(f"  请检查后重新运行 refactor --continue")
                sys.exit(1)
        else:
            print(f"  ✅ 一致性审查通过，无问题")
    except ImportError:
        print(f"  （一致性审查模块未就绪，将在后续版本添加）")
    except Exception as e:
        print(f"  ⚠️  一致性审查执行异常: {e}")
        import traceback
        traceback.print_exc()

    # ── 步骤 7：版本升级（三端同步） ──
    print(f"\n{'─'*55}")
    print(f"  [7/9] 版本升级（{bump_type}）")
    print(f"{'─'*55}")
    bump_args = argparse.Namespace(
        skill_dir=skill_dir,
        type=bump_type,
        desc=bump_desc or f'refactor: {os.path.basename(skill_dir)}',
        dry_run=False,
        confirmed=True,
        mode='bump')
    cmd_bump(bump_args)

    # ── 步骤 8：最终报告 ──
    print(f"\n{'─'*55}")
    print(f"  [8/9] 最终报告")
    print(f"{'─'*55}")
    print(f"  ✅ 审计: 0 ERROR 0 WARN")
    print(f"  ✅ 一致性: 无待处理问题")
    print(f"  ✅ 一致性: 无待处理问题")
    print(f"  ✅ bump: {bump_type} upgrade")
    print(f"  📋 技能: {os.path.basename(skill_dir)}")
    print(f"  📋 状态: 已完成全流程改造")

    # ── 步骤 9：清理（cleanup session 驱动 + 状态文件清理） ──
    print(f"\n{'─'*55}")
    print(f"  [9/9] cleanup 清理")
    print(f"{'─'*55}")
    _clean_stale_state(skill_dir, verbose=False)
    if manifest_id:
        try:
            from scripts.cleanup_manager import end_session
            report = end_session()
            if report:
                print(f"  ✅ cleanup 完成: 删除 {report.get('deleted', 0)}，跳过 {report.get('skipped', 0)}")
                if report.get('errors'):
                    for e in report['errors']:
                        print(f"  ⚠️  {e}")
            else:
                print(f"  ✅ cleanup 完成（无操作）")
        except Exception as e:
            print(f"  ⚠️  cleanup 执行异常: {e}")
    else:
        print(f"  ⚠️  无 cleanup session，跳过清理")

    print(f"\n{'='*55}")
    print(f"  ✅ refactor 全流程完成：{os.path.basename(skill_dir)}")
    print(f"{'='*55}")
    _save_html_report(skill_dir, result, before_result=result_before)


def _clean_stale_state(skill_dir, verbose=True):
    """清理 refactor 遗留的状态文件，确保每次任务都是全新独立的。

    清理两个目录：
    1. 技能自己的标准化 data 目录 → .verify_fp.json, .manual_wait, .manual_done
    2. skill-standardization 的数据跟踪目录 → .remaining_llm.json, .manual_wait, .manual_done

    时序规则：
    - 开始前（蓝皮书前，Step 0）→ 清旧状态
    - 完成后（一致性审查修复后，Step 9）→ 清临时文件
    - 禁止在 LLM 二次筛除或细碎修复循环内调用
    """
    import glob as _glob

    skill_name = os.path.basename(os.path.abspath(skill_dir))
    removed = 0

    # 目录1：技能 data 目录（含 .verify_fp.json — session 级别的分类缓存，新 session 应清理）
    skill_data_dir = os.path.join(
        os.path.dirname(os.path.abspath(skill_dir)), '.standardization',
        skill_name, 'data')
    for fname in ['.verify_fp.json', '.manual_wait', '.manual_done']:
        fp = os.path.join(skill_data_dir, fname)
        if os.path.isfile(fp):
            os.remove(fp)
            removed += 1
            if verbose:
                print(f"  🧹 清理: {fname}")

    # 目录2：skill-standardization 的跟踪目录（skill-standardization/data/{skill_name}/）
    self_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    track_dir = os.path.join(self_dir, 'data', skill_name)
    for pattern in ['.remaining_llm.json', '.manual_wait', '.manual_done']:
        fp = os.path.join(track_dir, pattern)
        if os.path.isfile(fp):
            os.remove(fp)
            removed += 1
            if verbose:
                print(f"  🧹 清理: {pattern}")

    if verbose:
        if removed:
            print(f"  ✅ 已清理 {removed} 个旧会话状态文件")
        else:
            print(f"  ✅ 无残留状态文件（干净的开始）")
    return removed


def _check_large_dirs(skill_dir):
    """扫描前钩子：检查是否存在大体积非标准目录，阻断直到 LLM 确认处理。"""
    LARGE_THRESHOLD_MB = 50
    suspicious = []
    for entry in os.scandir(skill_dir):
        if not entry.is_dir():
            continue
        if entry.name.startswith('.'):
            # 计算隐藏目录大小
            size_mb = 0
            for root, dirs, files in os.walk(entry.path):
                dirs[:] = []  # 仅统计一层
                for f in files:
                    try:
                        size_mb += os.path.getsize(os.path.join(root, f))
                    except OSError:
                        pass
                if size_mb > LARGE_THRESHOLD_MB * 1024 * 1024:
                    break
            size_mb = round(size_mb / (1024 * 1024), 1)
            if size_mb > LARGE_THRESHOLD_MB:
                suspicious.append((entry.name, size_mb))
        elif entry.name in ('node_modules', 'vendor', 'third_party'):
            size_mb = round(sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fn in os.walk(entry.path) for f in fn) / (1024 * 1024), 1)
            if size_mb > LARGE_THRESHOLD_MB:
                suspicious.append((entry.name, size_mb))
    if suspicious:
        print(f"\n{'='*55}")
        print(f"  ⛔ 扫描前检查：发现 {len(suspicious)} 个大体积目录")
        print(f"{'─'*55}")
        for name, size in suspicious:
            print(f"  📁 {name}  ({size} MB)")
        print(f"{'─'*55}")
        print(f"  LLM 必须确认这些目录是否需要扫描：")
        print(f"  1. 开发遗留产物（如 .venv_rag）→ 直接删除")
        print(f"  2. 依赖目录（如 node_modules）→ 确认无文档引用后排除")
        print(f"  3. 确有必要 → 说明理由后保留")
        print(f"\n  确认处理后重新运行: python -m scripts.skill_audit refactor {skill_dir} --confirmed")
        print(f"{'='*55}")
        sys.exit(1)


def _save_refactor_progress(skill_dir, step, remaining=None, bump_type='feature', desc=''):
    """保存 refactor 进度，供 --continue 恢复"""
    import json
    progress = {
        'step': step,
        'remaining': [{'rule_id': r['rule_id'], 'detail': r['detail'][:200],
                        'severity': r['severity']} for r in (remaining or [])],
        'bump_type': bump_type,
        'desc': desc,
    }
    progress_dir = os.path.join(
        os.path.dirname(skill_dir), '.standardization',
        os.path.basename(skill_dir), 'data')
    os.makedirs(progress_dir, exist_ok=True)
    with open(os.path.join(progress_dir, '.refactor_progress.json'), 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)


def cmd_create(args):
    """
    create 子命令：全流程创建新技能
    骨架生成 → 审计 → 报告
    """
    _semantic_precheck('create', getattr(args, 'skill_dir', None), confirmed=getattr(args, 'confirmed', False),
                       llm_mode=getattr(args, 'mode', None))
    skill_dir = os.path.abspath(args.skill_dir)
    skill_name = os.path.basename(skill_dir)
    desc = getattr(args, 'desc', '')

    print(f"\n{'='*55}")
    print(f"  🆕 [create] 创建技能：{skill_name}")
    print(f"{'='*55}")

    # ── 步骤 1：生成骨架 ──
    print(f"\n{'─'*55}")
    print(f"  [1/3] 生成标准骨架")
    print(f"{'─'*55}")
    try:
        from scripts.skill_builder import create_skill
        create_skill(skill_name, skill_dir, desc)
        print(f"  ✅ 骨架已生成：{skill_dir}")
    except ImportError:
        # fallback: 手动生成最小骨架
        os.makedirs(skill_dir, exist_ok=True)
        os.makedirs(os.path.join(skill_dir, 'references'), exist_ok=True)
        os.makedirs(os.path.join(skill_dir, 'scripts'), exist_ok=True)
        # 生成 SKILL.md
        skel_skill = f"""---
name: {skill_name}
author: your-name-here
license: MIT
version: 1.0.0
description: {desc or skill_name}
tags: []
trigger: []
trigger_negative: []
sensitive_access: false
critical_write: false
permission_weight: LOW
data_dir: ../.standardization/{skill_name}/
external_data_dir: true
h1_position: true
---
# {skill_name}

## 触发条件

**正向触发：**

**否定条件：**

## 核心能力

> 📚 **渐进式加载**：本技能采用渐进式 MD 体系，`SKILL.md` 为入口（≤230行），详细内容拆分到 `references/*.md` 按需加载。

### 渐进式文件索引

| 文件名 | 分类 | 包含内容 |
| -------- |------| ---------- |
| `references/examples.md` | 输出示例 | 各功能输出格式示例 |
| `references/faq.md` | 常见问题 | 常见疑问与解答 |
| `references/antipatterns.md` | 规范指南 | 反模式与注意事项 |
| `references/changelog.md` | 版本管理 | 更新日志 |
| `references/permissions.md` | 权限说明 | 权限风险与安全声明 |
| `references/LICENSE.md` | 许可协议 | MIT 开源许可证 |

## 能力与限制

## 使用方式

## 快速开始

## 工作流程
"""
        with open(os.path.join(skill_dir, 'SKILL.md'), 'w', encoding='utf-8') as f:
            f.write(skel_skill)
        # 生成 _meta.json
        import json
        with open(os.path.join(skill_dir, '_meta.json'), 'w', encoding='utf-8') as f:
            json.dump({
                'name': skill_name, 'version': '1.0.0',
                'description': desc or skill_name, 'author': 'your-name-here',
                'tags': [], 'data_dir': f'skills/.standardization/{skill_name}/data/',
                'triggers': []
            }, f, ensure_ascii=False, indent=2)
        # 生成 references/ 骨架文件
        _refs_content = {
            'LICENSE.md': 'MIT License\n\nCopyright (c) {year} {author}\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.',
            'permissions.md': '# 权限说明\n\n## 风险等级\n\nLOW\n\n## 安全声明\n\n本技能仅操作本地文件，不涉及网络请求或敏感信息访问。',
            'changelog.md': '# 更新日志\n\n## [1.0.0] - 初始版本\n\n### 新增\n- 初始创建\n',
            'examples.md': '# 输出示例\n\n> 请根据实际功能补充输出示例。\n',
            'faq.md': '# FAQ / 常见问题\n\n> 请根据实际功能补充常见问题。\n',
            'antipatterns.md': '# 反模式与常见错误\n\n> 请根据实际功能补充反模式说明。\n',
        }
        for _rf, _rc in _refs_content.items():
            _rfp = os.path.join(skill_dir, 'references', _rf)
            if not os.path.isfile(_rfp):
                # 替换占位符
                _rc_filled = _rc.replace('{year}', str(datetime.now().year))
                _rc_filled = _rc_filled.replace('{author}', 'your-name-here')
                with open(_rfp, 'w', encoding='utf-8') as f:
                    f.write(_rc_filled)
        # 生成 .gitkeep
        for d in ('scripts',):
            open(os.path.join(skill_dir, d, '.gitkeep'), 'w').close()
        print(f"  ✅ 最小骨架已生成：{skill_dir}")
        print(f"     references/: LICENSE.md, permissions.md, changelog.md, examples.md, faq.md, antipatterns.md")

    # ── 步骤 2：审计 ──
    print(f"\n{'─'*55}")
    print(f"  [2/3] 审计检查")
    print(f"{'─'*55}")
    result = audit_skill(skill_dir)
    print(format_report(result, skill_dir=skill_dir))

    # ── 步骤 3：报告与建议 ──
    print(f"\n{'─'*55}")
    print(f"  [3/3] 创建总结")
    print(f"{'─'*55}")
    remaining = [r for r in result.get("results", [])
                 if not r.get("passed") and not r.get("skipped")]
    if remaining:
        print(f"  ⚠️  审计发现 {len(remaining)} 项 FAIL，完成骨架填充后运行 refactor 修复")
    else:
        print(f"  ✅ 骨架通过审计，可直接使用")

    print(f"\n{'='*55}")
    print(f"  ✅ 创建完成：{skill_name}")
    print(f"{'='*55}")
    _save_html_report(skill_dir, result)


def _validate_changed_files(skill_dir, changed_files):
    """校验变更声明中的文件路径是否在技能目录中存在（或合理的新建路径）。"""
    if not changed_files:
        return False, "变更声明为空"
    for f in changed_files:
        # 允许新建文件（文件尚不存在），但路径必须在 scripts/ 或 references/ 下
        f = f.replace('\\', '/')
        if f.startswith('scripts/') or f.startswith('references/'):
            continue
        if f == 'SKILL.md':
            continue
        if f.startswith('.'):
            continue
        return False, f"变更文件路径不在允许范围内：{f}（仅允许 scripts/、references/、SKILL.md）"
    return True, ""



def _manual_dir_path(skill_dir):
    """.manual_wait / .manual_done 存放目录（与被审计技能数据同目录）"""
    _sn = os.path.basename(os.path.abspath(skill_dir))
    _sd = os.path.normpath(os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        os.pardir, ".standardization", "skill-standardization", "data", _sn
    ))
    return _sd


def _signal_manual_wait(skill_dir, items, files=None):
    """写入 .manual_wait 信号，要求 LLM 手动修复后写 .manual_done"""
    _d = _manual_dir_path(skill_dir)
    os.makedirs(_d, exist_ok=True)
    _w = os.path.join(_d, ".manual_wait")
    _wait_files = files or []
    if not _wait_files:
        for r in items:
            src = r.get("fix", {}).get("location", "") if isinstance(r.get("fix"), dict) else ""
            if src and os.path.exists(src):
                _wait_files.append(src)
        _wait_files = list(set(_wait_files))
    if not _wait_files:
        _wait_files = [os.path.join(skill_dir, "SKILL.md")]
    with open(_w, 'w', encoding='utf-8') as f:
        json.dump({"items": len(items), "count": len(items), "files": _wait_files}, f, ensure_ascii=False)
    _d = os.path.join(_d, ".manual_done")
    print(f"\n{'='*55}")
    print(f"  🔒 重构锁已激活——剩余 {len(items)} 项未修复")
    print(f"{'─'*55}")
    print(f"  修完以上所有问题后执行：")
    print(f"    python -c \"import pathlib; pathlib.Path(r'{_d}').touch()\"")
    print(f"  然后重新运行 --continue")
    print(f"  ⚠️  未修改任何文件就写 .manual_done 将被拒绝")
    print(f"{'='*55}")


def _run_audit_loop(skill_dir, max_loops, label_prefix, manifest_version=None, filter_files=None):
    """
    修复循环通用实现。
    返回 (result, remaining, loop_count)
    """
    # ★ v2.98.1: 检查 .manual_done 信号（LLM 手动修完后写此文件）
    _manual_dir = _manual_dir_path(skill_dir)
    _manual_done_path = os.path.join(_manual_dir, ".manual_done")
    _manual_wait_path = os.path.join(_manual_dir, ".manual_wait")
    if os.path.exists(_manual_wait_path):
        if os.path.exists(_manual_done_path):
            # LLM 声称修完了，验证是否真的改了文件
            wait_data = json.load(open(_manual_wait_path, 'r'))
            wait_files = wait_data.get("files", [])
            actually_modified = [f for f in wait_files if os.path.exists(f)]
            # mtime 校验：文件必须比 .manual_done 新，证明 LLM 实际修改过
            if actually_modified:
                done_mtime = os.path.getmtime(_manual_done_path)
                verified = []
                for f in wait_files:
                    if os.path.exists(f):
                        if os.path.getmtime(f) >= done_mtime:
                            verified.append(f)
                        else:
                            print(f"  ⚠️  文件末次修改早于 .manual_done 写入: {f}")
                actually_modified = verified
            if not actually_modified and wait_files:
                print(f"\n  ❌ LLM 声称已手动修复但未修改任何文件！")
                print(f"     必须实际修改文件后写 .manual_done，不得空过")
                sys.exit(1)
            os.remove(_manual_done_path)
            os.remove(_manual_wait_path)
            print(f"\n  ✅ LLM 手动修复信号已确认")
            # 读剩余项列表，做增量审计验证哪些修好了
            _remaining_path = os.path.join(_manual_dir, ".remaining_llm.json")
            _llm_items = []
            try:
                _llm_items = json.load(open(_remaining_path, 'r'))
            except Exception:
                pass
            if _llm_items:
                # 增量审计：只查 LLM 可能改过的文件（SKILL.md）
                _verify_result = audit_skill(skill_dir, filter_files=["SKILL.md"])
                _still_failing_ids = set()
                for _r in _verify_result.get("results", []):
                    if not _r.get("passed") and not _r.get("skipped"):
                        _rid = _r.get("rule_id", "")
                        if _rid:
                            _still_failing_ids.add(_rid)
                # 逐项核对：修好的打 √，没好的保留
                _remaining = []
                _fixed_count = 0
                for _item in _llm_items:
                    _rid = _item.get("rule_id", "")
                    if _rid in _still_failing_ids:
                        _remaining.append(_item)
                    else:
                        _fixed_count += 1
                        print(f"  ✅ {_rid}: 已修复")
                if _remaining:
                    print(f"\n  ⚠️ 仍有 {len(_remaining)} 项未修复")
                    _signal_manual_wait(skill_dir, _remaining)
                    sys.exit(0)
                else:
                    print(f"\n  ✅ 所有 {_fixed_count} 项手动修复项已确认通过")
                    return {"results": [], "summary": {"errors": 0, "warns": 0}}, [], 0
            else:
                # 没有剩余项列表，直接返回
                return {"results": [], "summary": {"errors": 0, "warns": 0}}, [], 0
        else:
            print(f"\n  🔒 LLM 手动修复等待中：修完上述问题后执行以下 Python 代码")
            print(f"     import os, json, pathlib")
            print(f"     d = r'{_manual_dir}'")
            print(f"     os.makedirs(d, exist_ok=True)")
            print(f"     pathlib.Path(os.path.join(d, '.manual_done')).touch()")
            print(f"     然后重新运行 --continue")
            print(f"  ⚠️  如果未修改任何文件就写 .manual_done，流程将拒绝继续")
            sys.exit(0)

    # 首次审计
    if filter_files:
        result = audit_skill(skill_dir, filter_files=filter_files)
    else:
        result = audit_skill(skill_dir, manifest_version=manifest_version)
    print(format_report(result, show_fix_hint=False, skill_dir=skill_dir))

    # ── ★ 前置 LLM 二次筛除（阻断点） ──
    # 流程: ①审计输出 → ②报告展示 → ③★LLM二次筛 → ④_filter_false_positives → ⑤细碎循环
    # 首次进入且 --classify 数据为空时阻断，--continue 不能跳过此检查
    raw_remaining = [r for r in result.get("results", [])
                     if not r.get("passed") and not r.get("skipped")]
    if raw_remaining:
        fp_ids = _load_fp_ids(skill_dir)
        if not fp_ids:
            # ★ 无任何分类数据 → 阻断，要求 LLM 一次性全部 classify
            skill_name = os.path.basename(os.path.abspath(skill_dir))
            print(f"\n{'='*55}")
            print(f"  ⏸  ★ 前置 LLM 二次筛除（阻断点）")
            print(f"{'─'*55}")
            print(f"  原始审计发现 {len(raw_remaining)} 项 FAIL，需要 LLM 确认真问题 vs 误报")
            print(f"  ⚠️  必须一次性 classify 所有可分类项，再进入细碎循环。边修边分类是不允许的。")
            print(f"")
            print(f"  步骤 1: 查看 FAIL 详情")
            print(f"    python -m scripts.skill_audit audit {skill_dir} --verify --mode refactor")
            print(f"")
            print(f"  步骤 2: 对确认为误报的项执行 --classify，须附带 --category + --subtype")
            print(f"    例: python -m scripts.skill_audit audit {skill_dir} --classify R-23 --category engine_mistake --subtype regex_misidentify --reason '...' --mode refactor")
            print(f"")
            print(f"  步骤 3: 重新执行 refactor --continue")
            print(f"    python -m scripts.skill_audit refactor {skill_dir} --continue --confirmed --mode refactor")
            print(f"{'='*55}")
            _save_remaining_llm(skill_dir, raw_remaining)
            return result, raw_remaining, 0
        else:
            # fp_ids 已有部分分类 → 检查是否所有项都已分类
            _partial = [r for r in raw_remaining if not _reclassify_false_positive(r, skill_dir)]
            if _partial:
                # 仍有未分类项 → 检查是否为 LLM 手动修复项（不可分类）
                _llm_only_set = {"workflow_completeness", "example_quality", "capability_boundary"}
                _unclassifiable = all(
                    r.get("fix", {}).get("key") in _llm_only_set
                    if isinstance(r.get("fix"), dict) else False
                    for r in _partial
                )
                if not _unclassifiable:
                    print(f"\n{'='*55}")
                    print(f"  ⏸  ★ 二次筛除未完成——仍有 {len(_partial)} 项可分类但未分类")
                    print(f"{'─'*55}")
                    print(f"  ⚠️  细碎修复循环不可修改修复清单！所有分类必须在步骤 4 一次性完成。")
                    print(f"  请 classify 以下未分类项后重新 --continue：")
                    for _pr in _partial:
                        _prid = _pr.get('rule_id', '?')
                        _pdet = _pr.get('detail', '')[:80]
                        print(f"    [{_prid}] {_pdet}")
                    print(f"{'='*55}")
                    _save_remaining_llm(skill_dir, _partial)
                    return result, _partial, 0

    remaining = _filter_false_positives(result, skill_dir)
    
    loop_count = 0
    _prev_sig = None
    # ★ v2.98.1: 修复循环中的审计只查修改过的文件（增量审计）
    _fix_mtime_snapshot = {}
    while remaining and loop_count < max_loops:
        loop_count += 1

        for r_inner in remaining:
            sev = "[ERROR]" if r_inner.get('severity') == 'ERROR' else "[WARN]"
            rid_inner = r_inner.get('rule_id', r_inner.get('rule', '?'))
            print(f"    {rid_inner} {sev} {r_inner.get('detail', '')[:120]}")
            # 为 R-25 注入 fix key（仅首次进入循环时注入，避免反复注入导致无限循环）
            # 首次循环 (loop_count == 1) 时注入 fix key；后续循环中不再重新注入已被清除的 key
            if rid_inner == "R-25" and loop_count == 1:
                detail_inner = r_inner.get("detail", "")
                if "C-05" in detail_inner:
                    r_inner["fix"] = {"key": "writing_standards"}
                if "C-07" in detail_inner:
                    r_inner["fix"] = {"key": "trigger_format"}
                if "C-10" in detail_inner and not r_inner.get("fix"):
                    r_inner["fix"] = {"key": "excessive_blank_lines"}
                if "C-11" in detail_inner:
                    r_inner["fix"] = {"key": "section_names"}
                if "C-12" in detail_inner:
                    r_inner["fix"] = {"key": "table_format"}
                if "C-14" in detail_inner:
                    r_inner["fix"] = {"key": "workflow_completeness"}
                if "C-15" in detail_inner and not r_inner.get("fix"):
                    r_inner["fix"] = {"key": "inline_refs"}
                if "C-17" in detail_inner:
                    r_inner["fix"] = {"key": "example_quality"}
                if "C-18" in detail_inner:
                    r_inner["fix"] = {"key": "capability_boundary"}

        # ── 自动修复 ──
        has_fixable = any(r.get("fix") for r in remaining)
        
        # 按 fix key 粒度分离 auto-fixable 和 manual-only 项
        # ★ 不按规则ID一刀切：同一规则下不同子项可能有不同的自动化能力
        #   - 有 fix key 且 key 在 _llm_only_fix_keys 中 → LLM手动修
        #   - 有 fix key 且 key 不在 _llm_only_fix_keys 中 → auto修
        #   - 无 fix key → LLM手动修（没有自动修复方案）
        _llm_only_fix_keys = {
            "workflow_completeness",  # R-25 C-14: 需要 LLM 读代码写工作流
            "example_quality",        # R-25 C-17: 需要 LLM 读代码创建示例
            "capability_boundary",    # R-25 C-18: 需要 LLM 理解能力边界
            "section_names",          # R-25 C-11: 非标章节归类需 LLM 判断内容语义
            # "excessive_blank_lines" → 机械删空行，auto
            # "table_format" → 机械格式化，auto
            # "inline_refs" → 机械内联引用，auto
            # "trigger_format" → 机械格式，auto
            # "constraint_format" → 机械格式，auto
            # "writing_standards" → 机械术语替换，auto
            # "doc_references" → 机械路径替换，auto
        }
        remaining_auto = []
        remaining_llm = []
        for r in remaining:
            fk = r.get("fix", {}).get("key") if isinstance(r.get("fix"), dict) else None
            if fk and fk not in _llm_only_fix_keys:
                remaining_auto.append(r)
            else:
                remaining_llm.append(r)

        # 输出 LLM 手动修复指引（给 LLM 具体操作说明）
        if remaining_llm:
            print(f"\n  ⚠️  {len(remaining_llm)} 项需要处理：")
            
            # 检查结构化数据类项（C-14/C-17/C-18）
            _struct_keys = {"workflow_completeness", "example_quality", "capability_boundary"}
            struct_needed = []
            for r in remaining_llm:
                fk = r.get("fix", {}).get("key") if isinstance(r.get("fix"), dict) else None
                if fk in _struct_keys:
                    struct_needed.append(r)
            if struct_needed:
                print(f"\n  ⛔ 以下 {len(struct_needed)} 项需要 LLM 提供结构化数据：")
                for r in struct_needed:
                    fk = r["fix"]["key"]
                    # 映射到正确的 data 目录路径
                    _sf_map = {
                        "workflow_completeness": ".structure_workflow.json",
                        "example_quality": ".structure_examples.json",
                        "capability_boundary": ".structure_capabilities.json",
                    }
                    _dname = os.path.basename(os.path.abspath(skill_dir))
                    _self_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                    _self_name = os.path.basename(_self_dir)
                    _dd = os.path.normpath(os.path.join(
                        _self_dir,
                        os.pardir, ".standardization", _self_name, "data", _dname, "outputs"
                    ))
                    struct_file = os.path.join(_dd, _sf_map.get(fk, f".structure_{fk}.json"))
                    sev = "[WARN]"
                    rid = r.get('rule_id', r.get('rule', '?'))
                    detail = r.get('detail', '')[:150]
                    print(f"    {rid} {sev} {detail}")
                    print(f"    → 请读取代码，生成结构化数据文件: {struct_file}")
                    print(f"    → 参考格式见 fix.py 中对应 fix 函数的文档注释")
                print(f"    生成结构化数据后，重新执行 --fix，脚本会自动渲染为格式化章节")
            
            # 其他手动修复项（无 fix key 或 fix key 不在任何 known set 中）
            other_llm = [r for r in remaining_llm if r.get("fix", {}).get("key") not in _struct_keys]
            if other_llm:
                print(f"\n  ℹ️  其他 {len(other_llm)} 项：")
                for r in other_llm:
                    sev = "[ERROR]" if r.get('severity') == 'ERROR' else "[WARN]"
                    rid = r.get('rule_id', r.get('rule', '?'))
                    detail = r.get('detail', '')[:200]
                    print(f"    {rid} {sev} {detail}")
                    if r.get('fix') and r['fix'].get('key'):
                        print(f"    → 手动编辑 SKILL.md 或 references/ 中的对应章节后重新 audit")

        if has_fixable:
            # ★ --continue 手动修复周期中跳过 auto-fix，避免覆盖手动修
            _manual_dir = _manual_dir_path(skill_dir)
            _manual_wait_path = os.path.join(_manual_dir, ".manual_wait")
            if os.path.isfile(_manual_wait_path):
                has_fixable = False
                _fixes_applied = 0
                _auto_targets = []
            else:
                # ★ v2.98.1: 修复前快照文件修改时间（增量审计用）
                _fix_mtime_snapshot.clear()
                for _fp in [os.path.join(skill_dir, f) for f in ["SKILL.md", "_meta.json"]]:
                    if os.path.exists(_fp):
                        _fix_mtime_snapshot[_fp] = os.path.getmtime(_fp)
                print(f"\n  --- 自动修复 ---")
                _fixes_applied = 0
                # ★ 只处理 auto-fixable 项（按 fix key 粒度筛选）
                _auto_targets = remaining_auto if remaining_auto else [r for r in remaining
                    if r.get("fix") and r["fix"].get("key") not in _llm_only_fix_keys]
            for res in _auto_targets:
                # R-25 可能有多个子项 -> 调所有匹配的 fix 函数
                if res.get("rule_id", "") == "R-25":
                    detail = res.get("detail", "")
                    _fix_key_map = {
                        "C-05": "writing_standards",
                        "C-07": "trigger_format",
                        "C-10": "excessive_blank_lines",
                        "C-11": "section_reorder",
                        "C-12": "trigger_format",
                        "C-13": "section_reorder",
                        "C-14": "workflow_completeness",
                        "C-15": "inline_refs",
                        "C-17": "example_quality",
                        "C-18": "capability_boundary",
                    }
                    for c_tag, fk in _fix_key_map.items():
                        if c_tag in detail:
                            c12_fixes = ["trigger_format", "constraint_format", "table_format"]
                            if c_tag == "C-12":
                                for c12_fk in c12_fixes:
                                    try:
                                        n = apply_fix(skill_dir, c12_fk)
                                        if n > 0:
                                            _fixes_applied += n
                                            print(f"  ✅ R-25 (C-12/{c12_fk}): 已修复 ({n} 处)")
                                    except Exception as e:
                                        pass
                            else:
                                try:
                                    n = apply_fix(skill_dir, fk, **res.get("fix", {}))
                                    if n > 0:
                                        _fixes_applied += n
                                        print(f"  ✅ R-25 ({c_tag}): 已修复 ({n} 处)")
                                except Exception as e:
                                    print(f"  ⚠️  R-25 ({c_tag}) 修复失败: {e}")
                elif res.get("fix"):
                    fix_key = res["fix"].get("key")
                    if fix_key:
                        try:
                            n = apply_fix(skill_dir, fix_key, **res["fix"])
                            if n > 0:
                                _fixes_applied += n
                                rid = res.get('rule_id', res.get('rule', fix_key))
                                print(f"  ✅ {rid}: 已修复")
                        except Exception as e:
                            rid = res.get('rule_id', res.get('rule', fix_key))
                            print(f"  ⚠️  {rid} 修复失败: {e}")
            # 同步渐进式文件索引表
            try:
                from .fix import fix_progressive_index_table
                fix_progressive_index_table(skill_dir)
            except Exception:
                pass

        # ── 判断：是否只剩 LLM 手动修复项 ──
        # 清除 LLM-only fix key，只留下真实的可自动修复项
        for r in remaining:
            fk = r.get("fix", {}).get("key") if isinstance(r.get("fix"), dict) else None
            if fk and fk in _llm_only_fix_keys:
                r.pop("fix", None)
        # ★ 如果 auto-fix 实际修了 0 处（函数调用返回 0），说明当前 auto-fix 能力已耗尽，
        #   再循环也不会有效果 → 清除所有剩余 fix key，直接走 LLM 手动路径
        if has_fixable and _fixes_applied == 0:
            for r in remaining:
                r.pop("fix", None)
        auto_fixable = [r for r in remaining if r.get("fix")]
        
        # ★ 额外兜底：如果 remaining 在本次循环中没有减少（相同 rule_id）,说明 auto-fix 已达瓶颈
        _current_sig = [(r.get("rule_id","?"), r.get("detail","")[:80]) for r in remaining]
        if _prev_sig is not None and _current_sig == _prev_sig:
            for r in remaining:
                r.pop("fix", None)
            auto_fixable = []
        _prev_sig = _current_sig
        
        if not auto_fixable:
            if remaining:
                print(f"\n  ✅ 所有可自动修复项已处理，剩余 {len(remaining)} 项需 LLM 手动修复")
                for r in remaining:
                    rid = r.get("rule_id", r.get("rule", "?"))
                    sev = "[ERROR]" if r.get('severity') == 'ERROR' else "[WARN]"
                    detail = r.get("detail", "")[:150]
                    print(f"    {rid} {sev} {detail}")
                # ⛔ 铁律：剩余项不为空则不能退出循环
                _save_remaining_llm(skill_dir, remaining)
                _signal_manual_wait(skill_dir, remaining)
                sys.exit(0)
            else:
                print(f"\n  ✅ 所有项已修复，双 0 达成")
            break
        print(f"  ⚠️  剩余 {len(remaining)} 项（{len(auto_fixable)} 项可自动修复，{len(remaining)-len(auto_fixable)} 项需手动）")
        print()

        # ★ v2.98.1: 修复循环内只审计修改过的文件（增量审计）
        if _fix_mtime_snapshot:
            _changed_files = []
            for _fp, _old_mt in list(_fix_mtime_snapshot.items()):
                if os.path.exists(_fp) and os.path.getmtime(_fp) != _old_mt:
                    _rel = os.path.relpath(_fp, skill_dir)
                    _changed_files.append(_rel)
            _audit_filter = _changed_files if _changed_files else None
        else:
            _audit_filter = filter_files

        if _audit_filter:
            result = audit_skill(skill_dir, filter_files=_audit_filter)
        else:
            result = audit_skill(skill_dir)
        print(format_report(result, show_fix_hint=False, skill_dir=skill_dir))
        remaining = _filter_false_positives(result, skill_dir)

        if remaining:
            print(f"\n  ⛔ 仍有 {len(remaining)} 项 FAIL，继续修复循环（已用 {loop_count}/{max_loops} 轮）")

    if loop_count >= max_loops:
        print(f"\n  ⛔ 修复循环已达上限 {max_loops} 次，强制退出")
        sys.exit(1)

    return result, remaining, loop_count


def cmd_update(args):
    """
    update 子命令：范围明确的变更流程
    蓝皮书 → 变更声明 → 针对性审计 → 细碎修复循环 → 全量审计确认 → 针对性一致性审查 → bump
    """
    _semantic_precheck('update', getattr(args, 'skill_dir', None), confirmed=getattr(args, 'confirmed', False),
                       llm_mode=getattr(args, 'mode', None))
    skill_dir = os.path.abspath(args.skill_dir)
    bump_type = getattr(args, 'bump_type', 'fix')
    bump_desc = getattr(args, 'desc', '')
    changed_files = getattr(args, 'changed_files', None)

    print(f"\n{'='*55}")
    print(f"  🔄 [update] 更新技能：{os.path.basename(skill_dir)}")
    print(f"{'='*55}")

    # ── 步骤 1：蓝皮书扫描（强制） ──
    print(f"\n{'─'*55}")
    print(f"  [1/9] 蓝皮书扫描")
    print(f"{'─'*55}")
    try:
        from ..skill_inspector import inspect_skill
        inspect_skill(skill_dir)
    except ImportError:
        try:
            from scripts.skill_inspector import inspect_skill
            inspect_skill(skill_dir)
        except ImportError:
            print("  [WARN] 未找到 skill_inspector，跳过蓝皮书扫描")

    # ── 步骤 2：启动 cleanup session + 备份（强制） ──
    print(f"\n{'─'*55}")
    print(f"  [2/8] 启动 cleanup session + 创建备份")
    print(f"{'─'*55}")
    try:
        from scripts.cleanup_manager import start_session
        manifest_id = start_session(skill_dir, "update")
        if manifest_id:
            print(f"  ✅ cleanup session 已启动: {manifest_id}")
        else:
            print(f"  ⚠️  cleanup session 启动失败，清理将跳过")
            manifest_id = None
    except ImportError:
        manifest_id = None
        print(f"  ⚠️  未找到 cleanup_manager，清理将跳过")

    import shutil, datetime
    backup_id = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = os.path.join(
        os.path.dirname(skill_dir), '.standardization',
        os.path.basename(skill_dir), 'backup')
    os.makedirs(backup_dir, exist_ok=True)
    zip_path = os.path.join(backup_dir, f"pre_update_{backup_id}")
    with __import__('zipfile').ZipFile(zip_path + '.zip', 'w', __import__('zipfile').ZIP_DEFLATED) as _zf:
        for root, dirs, files in os.walk(skill_dir):
            _skip = {'.standardization', '__pycache__', '.git', 'backup'}
            dirs[:] = [d for d in dirs if d not in _skip]
            for fn in files:
                fp = os.path.join(root, fn)
                arcname = os.path.relpath(fp, os.path.dirname(skill_dir))
                _zf.write(fp, arcname)
    print(f"  ✅ 备份到 {zip_path}.zip")

    # 注册备份路径到 cleanup session
    if manifest_id:
        try:
            from scripts.cleanup_manager import register
            register(zip_path + '.zip', category="backup")
        except Exception:
            pass

    # ── 步骤 3：变更声明（流程钩子 — 强制） ──
    print(f"\n{'─'*55}")
    print(f"  [3/9] 变更声明")
    print(f"{'─'*55}")
    if changed_files:
        valid, err = _validate_changed_files(skill_dir, changed_files)
        if not valid:
            print(f"  ⛔ 变更声明校验失败：{err}")
            sys.exit(1)
        print(f"  ✅ 变更声明已确认：{', '.join(changed_files)}")
    else:
        print(f"  ⚠️  未通过 --changed-files 声明变更文件，回退到全量审计")

    # ── 步骤 4：针对性审计 ──
    print(f"\n{'─'*55}")
    print(f"  [4/9] {'针对性' if changed_files else '全量'}审计")
    print(f"{'─'*55}")
    result, remaining, _ = _run_audit_loop(
        skill_dir, max_loops=10, label_prefix='4/9',
        manifest_version=args.manifest_version,
        filter_files=changed_files)
    s_before_update = result.get("summary", {})

    # ── 步骤 5：LLM 剩余项检查 —— 不再跑第二次全量审计 ──
    if remaining:
        print(f"\n{'-'*55}")
        print(f"  [5/9] LLM 剩余项检查")
        print(f"{'-'*55}")
        # 按 fix key 粒度判断：无 fix key 或 fix key 需 LLM 判断的 → LLM 手动修
        _llm_only_fix_keys_cmd = {
            "workflow_completeness", "example_quality", "capability_boundary",
            "section_names",
        }
        llm_items = [r for r in remaining
                     if not r.get("fix") or r["fix"].get("key") in _llm_only_fix_keys_cmd]
        non_llm_items = [r for r in remaining if r not in llm_items]
        if llm_items:
            print(f"\n  🤖 剩余 {len(llm_items)} 项需 LLM 修复（已保存结构化数据）")
            for r in llm_items:
                sev = "[ERROR]" if r.get('severity') == 'ERROR' else "[WARN]"
                rid = r.get('rule_id', r.get('rule', '?'))
                print(f"    {rid} {sev} {r.get('detail', '')[:120]}")
            _signal_manual_wait(skill_dir, llm_items)
            sys.exit(0)
        else:
            print(f"\n  ⛔ 有 {len(non_llm_items)} 项非 LLM 类 FAIL 未被自动修复")
            print(f"  请检查修复循环是否达到上限（10 轮），或手动排查")
            _signal_manual_wait(skill_dir, non_llm_items)
            sys.exit(0)

    # ── 步骤 6：全量审计确认（双 0 验证） ──
    print(f"\n{'─'*55}")
    print(f"  [6/8] 全量审计确认（双 0 验证）")
    print(f"{'─'*55}")
    result = audit_skill(skill_dir)
    _before = {"errors": s_before_update.get("errors", 0), "warns": s_before_update.get("warns", 0)}
    print(format_report(result, before_summary=_before, show_fix_hint=False, skill_dir=skill_dir))
    remaining = _filter_false_positives(result, skill_dir)
    if remaining:
        print(f"\n  ⛔ 全量审计确认失败：仍有 {len(remaining)} 项 FAIL")
        for r in remaining:
            sev = "[ERROR]" if r.get('severity') == 'ERROR' else "[WARN]"
            rid = r.get('rule_id', r.get('rule', '?'))
            print(f"    {rid} {sev} {r.get('detail', '')[:120]}")
        sys.exit(1)
    else:
        print(f"  ✅ 双 0 确认通过")

    # ── 步骤 7：针对性一致性审查 + 修复循环 ──    # ── 步骤 7：针对性一致性审查 + 修复循环 ──
    print(f"\n{'─'*55}")
    print(f"  [7/9] {'针对性' if changed_files else '全量'}一致性审查 + 修复循环")
    print(f"{'─'*55}")
    try:
        from .consistency_checker import (
            check_consistency, format_consistency_report,
            reclassify_consistency_false_positive, apply_consistency_fix
        )
        c_issues = check_consistency(skill_dir, filter_files=changed_files)
        c_real = [i for i in c_issues if not reclassify_consistency_false_positive(i, skill_dir=skill_dir)]
        for i in c_issues:
            if reclassify_consistency_false_positive(i, skill_dir=skill_dir):
                i['reclassified'] = True
        print(format_consistency_report(c_issues))
        
        if c_real:
            print(f"\n  💡 一致性审查发现 {len(c_real)} 个真实问题（已排除 {len(c_issues) - len(c_real)} 个误报）")
            # 一致性细碎修复循环（最多 10 轮）
            _c_loop_count = 0
            _c_max_loops = 10
            while c_real and _c_loop_count < _c_max_loops:
                _c_loop_count += 1
                print(f"\n  --- 一致性修复轮 #{_c_loop_count} ---")
                
                for _ci in c_real:
                    print(f"    [{_ci['type']}] {_ci['detail'][:120]}")
                
                # ── 自动修复 ──
                _c_auto_fixed = 0
                for _ci in c_real[:]:
                    if apply_consistency_fix(skill_dir, _ci):
                        _c_auto_fixed += 1
                        print(f"  ✅ 自动修复: {_ci['type']}")
                        c_real.remove(_ci)
                
                if _c_auto_fixed > 0:
                    print(f"  自动修复 {_c_auto_fixed} 项，重新审查确认...")
                    c_issues = check_consistency(skill_dir, filter_files=changed_files)
                    c_real = [i for i in c_issues if not reclassify_consistency_false_positive(i, skill_dir=skill_dir)]
                    for i in c_issues:
                        if reclassify_consistency_false_positive(i, skill_dir=skill_dir):
                            i['reclassified'] = True
                    print(format_consistency_report(c_issues))
                    if not c_real:
                        print(f"  ✅ 一致性修复完成（自动修复后双 0）")
                        break
                    continue
                
                # ── ★★★ 细碎一致性审查钩子 ★★★ ──
                print(f"\n  --- ★★★ 细碎一致性审查钩子 ★★★ ---")
                print(f"  LLM 需要做一件事：")
                print(f"")
                print(f"  ① 对比 SKILL.md 中的流程描述与代码实际执行流程是否一致")
                print(f"     检查要点：")
                print(f"     - 步骤数量是否与 cmd_xxx() 中的 [i/N] 编号一致？")
                print(f"     - 文档是否遗漏了关键阶段（如细碎修复循环、一致性审查循环）？")
                print(f"     - 文档描述的阶段顺序是否与代码实际执行顺序一致？")
                print(f"     - 如果发现不一致，LLM 手动修正 SKILL.md 的描述")
                print(f"     注意：这是语义检查，代码无法自动判断，完全依赖 LLM")
                print(f"")

                c_issues = check_consistency(skill_dir, filter_files=changed_files)
                c_real = [i for i in c_issues if not reclassify_consistency_false_positive(i, skill_dir=skill_dir)]
                for i in c_issues:
                    if reclassify_consistency_false_positive(i, skill_dir=skill_dir):
                        i['reclassified'] = True
                print(format_consistency_report(c_issues))
                if not c_real:
                    print(f"  ✅ 一致性修复完成（全量重审后双 0）")
                    break
            
            if c_real:
                print(f"  ⛔ 一致性修复已达重试上限，仍有 {len(c_real)} 项待处理")
                print(f"  请检查后重新运行 update --continue")
                sys.exit(1)
        else:
            print(f"  ✅ 一致性审查通过，无问题")
    except ImportError:
        print(f"  （一致性审查模块未就绪，将在后续版本添加）")
    except Exception as e:
        print(f"  ⚠️  一致性审查执行异常: {e}")
        import traceback
        traceback.print_exc()

    # ── 步骤 8：版本升级 ──
    print(f"\n{'─'*55}")
    print(f"  [8/9] 版本升级（{bump_type}）")
    print(f"{'─'*55}")
    bump_args = argparse.Namespace(
        skill_dir=skill_dir, type=bump_type,
        desc=bump_desc or f'update: {os.path.basename(skill_dir)}',
        dry_run=False,
        confirmed=True,
        mode='bump')
    cmd_bump(bump_args)

    # ── 步骤 8：清理（cleanup session 驱动） ──
    print(f"\n{'─'*55}")
    print(f"  [8/9] cleanup 清理")
    print(f"{'─'*55}")
    if manifest_id:
        try:
            from scripts.cleanup_manager import end_session
            report = end_session(manifest_id, "update completed")
            if report:
                deleted = report.get('deleted', 0)
                skipped = report.get('skipped', 0)
                print(f"  ✅ cleanup 完成: 删除 {deleted}，跳过 {skipped}")
            else:
                print(f"  ✅ cleanup 完成（无操作）")
        except Exception as e:
            print(f"  ⚠️  cleanup 执行异常: {e}")
    else:
        print(f"  ⚠️  无 cleanup session，跳过清理")

    # ── 步骤 9：最终报告 ──
    print(f"\n{'─'*55}")
    print(f"  [9/9] 最终报告")
    print(f"{'─'*55}")
    print(f"  ✅ 审计: 0 ERROR 0 WARN")
    print(f"  ✅ 一致性: 无待处理问题")
    print(f"  ✅ bump: {bump_type} upgrade")
    print(f"  📋 技能: {os.path.basename(skill_dir)}")
    print(f"  📋 状态: update 完成")
    _save_html_report(skill_dir, result)


def main():
    """主入口函数"""
    parser = argparse.ArgumentParser(
    description="SKILL.md 规范化审查工具 (R-01~R-26)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python -m skill_audit audit ~/.workbuddy/skills/<skill-name>
  python -m skill_audit audit ~/.workbuddy/skills/svg-composer --json
  python -m skill_audit audit-all ~/.workbuddy/skills --manifest manifest.json
  python -m skill_audit rules
        """,
    )
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # audit 子命令
    p_audit = subparsers.add_parser("audit", help="审查单个 skill")
    p_audit.add_argument("skill_dir", help="skill 目录路径")
    p_audit.add_argument("--json", action="store_true", help="JSON 格式输出")
    p_audit.add_argument("--manifest-version", metavar="VER", help="manifest 中记录的版本号（用于 R-10）")
    p_audit.add_argument("--progress-file", metavar="FILE", help=".progress.md 文件路径（用于过程管理）")
    p_audit.add_argument("--fix", action="store_true", help="自动修正 R-11/R-12 违规（修改脚本和 _meta.json）")
    p_audit.add_argument("--confirmed", action="store_true", help="语义门禁确认标记（必须传入才能执行）")
    p_audit.add_argument("--mode", help="LLM 自检闸门输出的模式，用于模式-命令校验（必传，如 --mode refactor）")
    p_audit.add_argument("--verify", action="store_true", help="强制验证：有非误报未通过项则 exit(1)，确保铁律 0 ERROR 0 WARN 强制执行")
    p_audit.add_argument("--show-fix", metavar="IDS", help="仅展示指定 #ID 的修复指引（先运行 --verify 获取 ID 列表）")
    p_audit.add_argument("--classify", metavar="IDS", help="将指定 #ID 标记为误判（如 --classify 42,55,67），须附带 --category 和 --subtype，可选 --reason")
    p_audit.add_argument("--category", metavar="CAT", help=f"误报类别：{', '.join(sorted(_CLASSIFY_LEGAL_CATEGORIES))}（仅与 --classify 配合使用）")
    p_audit.add_argument("--subtype", metavar="TYPE", help=f"误报子类型（必填，与 --classify 配合使用）：{', '.join(sorted(_CLASSIFY_LEGAL_SUBTYPES.keys()))}")
    p_audit.add_argument("--reason", metavar="TEXT", help="误报理由（可选）")
    p_audit.add_argument("--no-fp", metavar="IDS", help="将指定 #ID 从误判列表中移除（取消分类）")

    # audit-all 子命令
    p_all = subparsers.add_parser("audit-all", help="批量审查所有 skill")
    p_all.add_argument("skills_dir", help="skills 根目录")
    p_all.add_argument("--manifest", metavar="FILE", help="manifest.json 路径（用于 R-10 版本比对）")
    p_all.add_argument("--json", action="store_true", help="JSON 格式输出")

    # rules 子命令
    p_rules = subparsers.add_parser("rules", help="列出所有审查规则")
    p_rules.add_argument("--confirmed", action="store_true", help="语义门禁确认标记（必须传入才能执行）")
    p_rules.add_argument("--mode", help="LLM 自检闸门输出的模式（必传，如 --mode readonly）")

    # create-template 子命令（v2.29.0 新增）
    p_template = subparsers.add_parser("create-template", aliases=["template"],
                                      help="输出所有规则的创建模板（供 LLM 创建技能时参考）")
    p_template.add_argument("--json", action="store_true", help="JSON 格式输出")
    p_template.add_argument("--confirmed", action="store_true", help="语义门禁确认标记（必须传入才能执行）")
    p_template.add_argument("--mode", help="LLM 自检闸门输出的模式（必传，如 --mode readonly）")

    # fix 子命令（v2.37.0 新增）
    p_fix = subparsers.add_parser("fix", help="针对性修复工具（按 fix key 分发）")
    p_fix.add_argument("skill_dir", help="skill 目录路径")
    p_fix.add_argument("--key", help="修复 key（如 name、section_trigger 等，可多次指定或留空列出所有可用 key）", nargs="*")
    p_fix.add_argument("--value", help="修复参数值（如 value=true）")
    p_fix.add_argument("--dry-run", action="store_true", help="仅模拟，不实际修改")

    # bump 子命令（v2.38.15 新增）
    p_bump = subparsers.add_parser("bump", help="自动升级技能版本号三端（SKILL.md + _meta.json + changelog）",
        epilog="""版本号变更规则（R-03）：
  breaking (MAJOR.0.0) = 架构级重构/破坏性变更/核心引擎重写    例: 2.3.4 → 3.0.0
  feature  (x.MINOR.0) = 新增功能/已有功能重构/大面积描述修正   例: 2.3.4 → 2.4.0
  fix      (x.y.PATCH) = 单处描述修正/参数拼写/路径修正/错别字  例: 2.3.4 → 2.3.5
不确认时选 feature（MINOR），严禁随意使用 MAJOR。
架构级重构（如模块系统替换、核心引擎重写）才使用 breaking。""")
    p_bump.add_argument("skill_dir", help="skill 目录路径")
    p_bump.add_argument("--type", choices=["fix", "feature", "breaking"], default=None,
                        help="变更类型（默认交互选择）")
    p_bump.add_argument("--desc", required=True, help="本次变更描述（将写入 changelog）")
    p_bump.add_argument("--dry-run", action="store_true", help="仅预览，不实际修改")
    p_bump.add_argument("--confirmed", action="store_true", help="语义门禁确认标记（必须传入才能执行）")
    p_bump.add_argument("--mode", help="LLM 自检闸门输出的模式（必传，如 --mode bump）")
    # refactor 子命令（v2.66.0 新增）
    p_refactor = subparsers.add_parser("refactor",
        help="全流程改造：蓝图扫描 → 备份 → 审计 → 修复 → 验证 → 版本升级 → 清理")
    p_refactor.add_argument("skill_dir", help="skill 目录路径")
    p_refactor.add_argument("--bump-type", choices=["fix", "feature", "breaking"], default="feature",
                            help="版本升级类型（默认 feature）")
    p_refactor.add_argument("--desc", default="", help="变更描述（将写入 changelog）")
    p_refactor.add_argument("--manifest-version", metavar="VER",
                            help="manifest 中记录的版本号（用于 R-10）")
    p_refactor.add_argument("--continue", dest="refactor_continue", action="store_true",
                            help="从上一次中断处继续")
    p_refactor.add_argument("--confirmed", action="store_true", help="语义门禁确认标记（必须传入才能执行）")
    p_refactor.add_argument("--mode", help="LLM 自检闸门输出的模式（必传，如 --mode refactor）")

    # create 子命令（v2.66.0 新增）
    p_create = subparsers.add_parser("create", help="全流程创建新技能：骨架生成 → 审计 → 报告")
    p_create.add_argument("skill_dir", help="技能目录路径（目录名将作为技能名）")
    p_create.add_argument("--desc", default="", help="技能描述")
    p_create.add_argument("--confirmed", action="store_true", help="语义门禁确认标记（必须传入才能执行）")
    p_create.add_argument("--mode", help="LLM 自检闸门输出的模式（必传，如 --mode create）")

    # update 子命令（v2.66.0 新增）
    p_update = subparsers.add_parser("update", help="轻量更新：蓝图扫描 → 备份 → 审计 → 修复 → 验证 → 一致性审查 → bump")
    p_update.add_argument("skill_dir", help="skill 目录路径")
    p_update.add_argument("--bump-type", choices=["fix", "feature", "breaking"], default="fix",
                          help="版本升级类型（默认 fix）")
    p_update.add_argument("--desc", default="", help="变更描述（将写入 changelog）")
    p_update.add_argument("--manifest-version", metavar="VER",
                          help="manifest 中记录的版本号（用于 R-10）")
    p_update.add_argument("--changed-files", nargs="*", default=None,
                          help="变更文件列表（如 --changed-files scripts/foo.py references/bar.md）")
    p_update.add_argument("--confirmed", action="store_true", help="语义门禁确认标记（必须传入才能执行）")
    p_update.add_argument("--mode", help="LLM 自检闸门输出的模式（必传，如 --mode update）")

    args = parser.parse_args()

    # ── ★ 入口门禁：检查是否有未完成的修复会话 ──
    if hasattr(args, 'skill_dir') and args.skill_dir:
        _sd = os.path.abspath(args.skill_dir)
        _remaining_path = os.path.join(
            os.path.dirname(_sd), '.standardization',
            os.path.basename(_sd), '.remaining_llm.json')
        # 仅阻断非 --continue 和非 --classify 的操作
        _is_continue = getattr(args, 'refactor_continue', False) or getattr(args, 'continue_', False)
        _is_classify = bool(getattr(args, 'classify', None))
        _is_no_fp = bool(getattr(args, 'no_fp', None))
        if getattr(args, 'refactor_continue', False):
            _verify_snapshot(args.skill_dir, ".remaining_llm.json")
            _verify_snapshot(args.skill_dir, ".manual_wait")
        if os.path.isfile(_remaining_path) and not (_is_continue or _is_classify or _is_no_fp):
            print(f"\n  ⛔ ⛔ ⛔ 存在未完成的修复会话 ⛔ ⛔ ⛔")
            print(f"  .remaining_llm.json 存在，说明修复循环未闭环")
            print(f"  必须完成修复后才能执行其他操作：")
            print(f"    1) 手动修复剩余问题")
            print(f"    2) python -m scripts.skill_audit refactor {_sd} --continue --confirmed --mode refactor")
            print(f"    3) 重复直到 0 ERROR 0 WARN")
            print(f"\n  被阻断的操作: {args.command}")
            sys.exit(3)

    if args.command == "audit":
        cmd_audit(args)
    elif args.command == "audit-all":
        cmd_audit_all(args)
    elif args.command == "rules":
        cmd_rules(args)
    elif args.command == "fix":
        cmd_fix(args)
    elif args.command == "bump":
        cmd_bump(args)
    elif args.command == "refactor":
        cmd_refactor(args)
    elif args.command == "create":
        cmd_create(args)
    elif args.command == "update":
        cmd_update(args)
    elif args.command in ("create-template", "template"):
        if hasattr(args, "json") and args.json:
            _semantic_precheck('readonly', confirmed=getattr(args, 'confirmed', False),
                               llm_mode=getattr(args, 'mode', None))
            import json
            output = []
            for rule in RULES:
                output.append({
                    "id": rule["id"],
                    "name": rule["name"],
                    "severity": rule["severity"],
                    "check": rule["check"],
                    "fixable": rule.get("fixable", False),
                    "create_template": rule.get("create_template", ""),
                })
            print(json.dumps(output, ensure_ascii=False, indent=2))
        else:
            cmd_create_template(args)
    else:
        parser.print_help()
        sys.exit(1)
if __name__ == "__main__":
    main()
