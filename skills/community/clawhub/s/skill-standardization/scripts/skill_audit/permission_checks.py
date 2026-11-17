#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
skill_audit/permission_checks.py — 权限相关检查函数 (R-13~R-17)
v2.16.0: 直接内嵌 PermissionChecker，不再 shell out
"""

import os
import re
import sys
import json

# ── 直接导入 PermissionChecker，不再 subprocess.run() ─────────────────────
_scripts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, _scripts_dir)
from permission_checker import PermissionChecker


def _get_report(skill_dir):
    """
    直接调用 PermissionChecker（不再 shell out）。
    返回 report dict，失败返回 None。
    """
    try:
        checker = PermissionChecker(skill_dir, verbose=False)
        return checker.scan()
    except Exception:
        return None


# ── R-13 ~ R-17 检查函数 ─────────────────────────────────────────────────────

def check_sensitive_access_declaration(filepath, content, fm, body, skill_dir=None, **kw):
    """R-13: 敏感信息访问声明检查。不一致时返回 fix 建议。"""
    # 修复：先检查 frontmatter 是否缺少字段
    if fm is None:
        return {"passed": False, "detail": f"{filepath}:1 - SKILL.md 缺少 frontmatter（--- 包裹的元数据区）"}
    
    if "sensitive_access" not in fm:
        # 获取实际扫描结果，返回 fix 建议
        if not skill_dir or not os.path.isdir(skill_dir):
            return {"passed": False, "detail": f"{filepath}:1 - frontmatter 缺少 sensitive_access 字段（必须声明，值为 true 或 false）"}
        report = _get_report(skill_dir)
        if report is None:
            return {"passed": False, "detail": f"{filepath}:1 - frontmatter 缺少 sensitive_access 字段（必须声明，值为 true 或 false）"}
        stats = report.get("stats", {})
        has_sensitive = stats.get("sensitive_access", 0) > 0
        return {
            "passed": False,
            "detail": f"{filepath}:1 - frontmatter 缺少 sensitive_access 字段（必须声明，值为 true 或 false）",
            "fix": {"key": "sensitive_access", "value": has_sensitive,
                     "location": "<skill-dir>/SKILL.md frontmatter",
                     "operation": f"设置 sensitive_access: {has_sensitive}",
                     "verification": "重新运行 audit_skill()，确认 R-13 passed",
                     "reason": f"缺少 sensitive_access 字段，根据实际扫描结果（{has_sensitive} 处敏感信息访问）自动添加"}
        }
    
    if not skill_dir or not os.path.isdir(skill_dir):
        return {"passed": True, "detail": f"{filepath}:1 - 跳过：无法确定技能目录", "skip": True}

    report = _get_report(skill_dir)
    if report is None:
        return {
            "passed": True,
            "detail": f"{filepath}:1 - PermissionChecker 不可用，跳过详细检查",
            "skip": True
        }

    stats = report.get("stats", {})
    has_sensitive_access = stats.get("sensitive_access", 0) > 0
    fm_sensitive = fm.get("sensitive_access", False)

    if has_sensitive_access and not fm_sensitive:
        return {
            "passed": False,
            "detail": f"{filepath}:1 - 脚本含敏感信息访问（memory/credentials/token），但 frontmatter 声明 sensitive_access: false",
            "fix": {"key": "sensitive_access", "value": True,
                     "reason": f"实际扫描发现 {stats.get('sensitive_access', 0)} 处敏感信息访问，与声明不一致"}
        }

    if not has_sensitive_access and fm_sensitive:
        return {
            "passed": False,
            "detail": f"{filepath}:1 - frontmatter 声明 sensitive_access: true，但脚本未检测到敏感信息访问",
            "fix": {"key": "sensitive_access", "value": False,
                     "reason": "实际扫描未发现敏感信息访问，与声明不一致"}
        }

    return {
        "passed": True,
        "detail": f"{filepath}:1 - 敏感信息访问声明检查通过" + (f"（检测到 {stats.get('sensitive_access', 0)} 处访问）" if has_sensitive_access else "")
    }


def check_critical_write_declaration(filepath, content, fm, body, skill_dir=None, **kw):
    """R-14: 关键位置写入声明检查。不一致时返回 fix 建议。"""
    # 修复：先检查 frontmatter 是否缺少字段
    if fm is None:
        return {"passed": False, "detail": f"{filepath}:1 - SKILL.md 缺少 frontmatter（--- 包裹的元数据区）"}
    
    if "critical_write" not in fm:
        # 获取实际扫描结果，返回 fix 建议
        if not skill_dir or not os.path.isdir(skill_dir):
            return {"passed": False, "detail": f"{filepath}:1 - frontmatter 缺少 critical_write 字段（必须声明，值为 true 或 false）"}
        report = _get_report(skill_dir)
        if report is None:
            return {"passed": False, "detail": f"{filepath}:1 - frontmatter 缺少 critical_write 字段（必须声明，值为 true 或 false）"}
        stats = report.get("stats", {})
        has_critical = stats.get("critical_write", 0) > 0
        return {
            "passed": False,
            "detail": f"{filepath}:1 - frontmatter 缺少 critical_write 字段（必须声明，值为 true 或 false）",
            "fix": {"key": "critical_write", "value": has_critical,
                     "location": "<skill-dir>/SKILL.md frontmatter",
                     "operation": f"设置 critical_write: {has_critical}",
                     "verification": "重新运行 audit_skill()，确认 R-14 passed",
                     "reason": f"缺少 critical_write 字段，根据实际扫描结果（{has_critical} 处关键位置写入）自动添加"}
        }
    
    if not skill_dir or not os.path.isdir(skill_dir):
        return {"passed": True, "detail": f"{filepath}:1 - 跳过：无法确定技能目录", "skip": True}

    report = _get_report(skill_dir)
    if report is None:
        return {
            "passed": True,
            "detail": f"{filepath}:1 - PermissionChecker 不可用，跳过详细检查",
            "skip": True
        }

    stats = report.get("stats", {})
    has_critical_write = stats.get("critical_write", 0) > 0
    fm_critical = fm.get("critical_write", False)

    if has_critical_write and not fm_critical:
        return {
            "passed": False,
            "detail": f"{filepath}:1 - 脚本含关键位置写入（skills/.workbuddy/系统目录），但 frontmatter 声明 critical_write: false",
            "fix": {"key": "critical_write", "value": True,
                     "reason": f"实际扫描发现 {stats.get('critical_write', 0)} 处关键位置写入，与声明不一致"}
        }

    if not has_critical_write and fm_critical:
        return {
            "passed": False,
            "detail": f"{filepath}:1 - frontmatter 声明 critical_write: true，但脚本未检测到关键位置写入",
            "fix": {"key": "critical_write", "value": False,
                     "reason": "实际扫描未发现关键位置写入，与声明不一致"}
        }

    return {
        "passed": True,
        "detail": f"{filepath}:1 - 关键位置写入声明检查通过" + (f"（检测到 {stats.get('critical_write', 0)} 处写入）" if has_critical_write else "")
    }


def check_authorization_present(filepath, content, fm, body, skill_dir=None, **kw):
    """R-15: 高权限操作风险说明检查。检查 references/permissions.md 是否包含高权限操作风险说明。"""
    if not skill_dir or not os.path.isdir(skill_dir):
        return {"passed": True, "detail": f"{filepath}:1 - 跳过：无法确定技能目录", "skip": True}

    # 用 PermissionChecker 获取风险等级
    report = _get_report(skill_dir)
    risk_level = report.get("risk_level", "low").upper() if report else "LOW"

    # 低风险/中风险：无需说明高权限操作风险，但仍需校验权限文档头部
    if risk_level in ("LOW", "MEDIUM"):
        refs_dir = os.path.join(skill_dir, "references")
        permissions_md = os.path.join(refs_dir, "permissions.md")
        if not os.path.isfile(permissions_md):
            return {
                "passed": False,
                "detail": f"{filepath}:1 - 风险等级 {risk_level}，references/permissions.md 不存在",
                "fix": {"key": "create_permissions_md", "value": True,
                         "location": permissions_md,
                         "operation": "创建 permissions.md 并补充 skill-standardization 权限说明头部",
                         "verification": "重新运行 audit_skill()，确认 R-15 passed"}
            }
        try:
            with open(permissions_md, "r", encoding="utf-8", errors="replace") as f:
                pm_content = f.read()
        except Exception:
            return {
                "passed": False,
                "detail": f"{filepath}:1 - 风险等级 {risk_level}，但无法读取 references/permissions.md",
                "fix": {"key": "fix_permissions_md_readable", "value": True,
                         "location": permissions_md,
                         "operation": "确保 permissions.md 可读，并补充 skill-standardization 权限说明头部",
                         "verification": "重新运行 audit_skill()"}
            }
        # 检查是否含未填写的占位符（仅检查明确的未填写标记，不含正常文档结构词）
        placeholders = ["（请填写）", "（如含敏感信息访问"]
        if any(p in pm_content for p in placeholders):
            return {
                "passed": False,
                "detail": f"{filepath}:1 - permissions.md 含未填写的占位符",
                "fix": {"key": "create_permissions_md", "value": True,
                         "location": permissions_md,
                         "operation": "填充 permissions.md 的风险等级和高权限操作说明",
                         "verification": "重新运行 audit_skill()，确认 R-15 passed"}
            }
        if "基于 skill-standardization 渐进式披露规范的权限说明" not in pm_content:
            return {
                "passed": False,
                "detail": f"{filepath}:1 - 风险等级 {risk_level}，references/permissions.md 缺少 skill-standardization 权限说明头部",
                "fix": {"key": "create_permissions_md", "value": True,
                         "location": permissions_md,
                         "operation": "在 permissions.md 最前面插入 skill-standardization 权限说明头部",
                         "verification": "重新运行 audit_skill()，确认 R-15 passed"}
            }
        return {"passed": True, "detail": f"{filepath}:1 - 风险等级 {risk_level}，references/permissions.md 包含权限说明头部 ✓"}

    # 高风险/严重风险：必须在 references/permissions.md 中说明
    if risk_level in ("HIGH", "CRITICAL"):
        refs_dir = os.path.join(skill_dir, "references")
        if not os.path.isdir(refs_dir):
            return {
                "passed": False,
                "detail": f"{filepath}:1 - 风险等级 {risk_level}，但 references/ 目录不存在，无法检查风险说明",
                "fix": {"key": "create_references_permissions_md", "value": True,
                         "location": f"{skill_dir}/references/permissions.md",
                         "operation": "创建 references/ 目录和 permissions.md，并在其中说明高权限操作风险",
                         "verification": "重新运行 audit_skill()，确认 R-15 passed"}
            }

        permissions_md = os.path.join(refs_dir, "permissions.md")
        if not os.path.isfile(permissions_md):
            return {
                "passed": False,
                "detail": f"{filepath}:1 - 风险等级 {risk_level}，但 references/permissions.md 不存在",
                "fix": {"key": "create_permissions_md", "value": True,
                         "location": permissions_md,
                         "operation": "创建 permissions.md 并在其中说明高权限操作风险（风险等级、具体操作、为什么需要）",
                         "verification": "重新运行 audit_skill()，确认 R-15 passed"}
            }

        # 读取 permissions.md 内容
        try:
            with open(permissions_md, "r", encoding="utf-8", errors="replace") as f:
                pm_content = f.read()
        except Exception as e:
            return {
                "passed": False,
                "detail": f"{filepath}:1 - 风险等级 {risk_level}，但无法读取 references/permissions.md: {e}",
                "fix": {"key": "fix_permissions_md_readable", "value": True,
                         "location": permissions_md,
                         "operation": "确保 permissions.md 可读，并包含高权限操作风险说明",
                         "verification": "重新运行 audit_skill()，确认 R-15 passed"}
            }

        # 检查是否包含风险说明关键词
        risk_keywords = ["风险", "risk", "高权限", "high risk", "critical", "授权", "authorization", "权限"]
        found_risk = False
        for kw in risk_keywords:
            if kw.lower() in pm_content.lower():
                found_risk = True
                break

        if not found_risk:
            return {
                "passed": False,
                "detail": f"{filepath}:1 - 风险等级 {risk_level}，但 references/permissions.md 未包含高风险操作风险说明",
                "fix": {"key": "add_risk_description", "value": True,
                         "location": permissions_md,
                         "operation": "在 permissions.md 中添加高风险操作风险说明（风险等级、具体操作、为什么需要、如何降低风险）",
                         "verification": "重新运行 audit_skill()，确认 R-15 passed"}
            }

        return {
            "passed": True,
            "detail": f"{filepath}:1 - 高权限操作风险说明检查通过（风险等级 {risk_level}，references/permissions.md 包含风险说明）"
        }

    # 未知风险等级
    return {"passed": True, "detail": f"{filepath}:1 - 风险等级 {risk_level}（未知），跳过检查", "skip": True}


def check_permission_weight_explained(filepath, content, fm, body, skill_dir=None, **kw):
    """R-16: 权限权重说明检查。不一致时返回 fix 建议。"""
    if not skill_dir or not os.path.isdir(skill_dir):
        return {"passed": True, "detail": f"{filepath}:1 - 跳过：无法确定技能目录", "skip": True}

    # 1. 检查 frontmatter 中是否有 permission_weight 字段
    fm_weight = fm.get("permission_weight", None)
    if fm_weight is None:
        # 获取实际扫描的风险等级，用于 fix 建议
        if not skill_dir or not os.path.isdir(skill_dir):
            return {"passed": False, "detail": f"{filepath}:1 - frontmatter 缺少 permission_weight 字段（必须声明风险等级：LOW/MEDIUM/HIGH/CRITICAL）"}
        report = _get_report(skill_dir)
        actual_weight = report.get("risk_level", "low").upper() if report else "LOW"
        return {
            "passed": False,
            "detail": f"{filepath}:1 - frontmatter 缺少 permission_weight 字段（必须声明风险等级：LOW/MEDIUM/HIGH/CRITICAL）",
            "fix": {"key": "permission_weight", "value": actual_weight,
                     "location": "<skill-dir>/SKILL.md frontmatter",
                     "operation": f"设置 permission_weight: {actual_weight}",
                     "verification": "重新运行 audit_skill()，确认 R-16 passed",
                     "reason": f"缺少 permission_weight 字段，根据实际扫描风险等级 {actual_weight} 自动添加"}
        }

    # 2. 获取实际扫描的风险等级
    report = _get_report(skill_dir)
    actual_weight = report.get("risk_level", "low").upper() if report else "LOW"
    fm_weight_upper = fm_weight.upper() if isinstance(fm_weight, str) else "LOW"

    # 3. 对比声明和实际是否一致
    if fm_weight_upper != actual_weight:
        return {
            "passed": False,
            "detail": f"{filepath}:1 - frontmatter permission_weight: {fm_weight}，但实际扫描风险等级: {actual_weight}",
            "fix": {"key": "permission_weight", "value": actual_weight,
                     "reason": f"实际扫描风险等级为 {actual_weight}，与声明 {fm_weight} 不一致"}
        }

    # 4. 检查 references/ 里有没有权重说明文档（保留原有检查）
    refs_dir = os.path.join(skill_dir, "references")
    if not os.path.isdir(refs_dir):
        return {"passed": False, "detail": f"{filepath}:1 - 建议增加权限权重说明（references/ 目录不存在）"}

    weight_keywords = ["权限权重", "permission weight", "权重", "weight", "风险等级", "risk level"]
    found_explanation = False
    for fname in sorted(os.listdir(refs_dir)):
        fpath = os.path.join(refs_dir, fname)
        if not os.path.isfile(fpath):
            continue
        ext = os.path.splitext(fname)[1].lower()
        if ext not in (".md", ".txt", ".rst"):
            continue
        try:
            with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                file_content = f.read()
        except Exception:
            continue
        for keyword in weight_keywords:
            if keyword.lower() in file_content.lower():
                found_explanation = True
                break
        if found_explanation:
            break

    if not found_explanation:
        return {
            "passed": False,
            "detail": f"{filepath}:1 - 建议在 references/ 中说明各操作的权限权重，便于审查时评估风险",
        }

    return {"passed": True, "detail": f"{filepath}:1 - 权限权重说明检查通过（声明: {fm_weight}，实际风险: {actual_weight}）"}


def _load_allowed_sections():
    """加载 body.json 的 allowed_sections 白名单。"""
    # 本文件在 scripts/skill_audit/，body.json 在 scripts/spec/
    spec_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'spec', 'body.json'
    )
    if not os.path.isfile(spec_path):
        return None
    try:
        import json
        with open(spec_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return {
            "allowed": data.get("allowed_sections", []),
            "synonyms": data.get("section_synonyms", {})
        }
    except Exception:
        return None


def _find_nonstandard_sections(body_text, skill_dir=None):
    """
    扫描正文中的 ## H2 章节，与 body.json allowed_sections 白名单对比。
    Phase 1: 正则粗筛。
    返回非标章节列表，每项含 (line_no, title, content_preview)。
    content_preview 供 LLM 全报告LLM精筛判断。
    """
    spec = _load_allowed_sections()
    if spec is None:
        return []

    allowed = spec["allowed"]
    synonyms = spec["synonyms"]

    allowed_keywords_lower = set(k.lower() for k in allowed)

    # 提取 H2 及其后续内容直到下一个 ##
    section_pattern = re.compile(r'^##\s+(.+?)$\n(.*?)(?=^##\s|\Z)', re.MULTILINE | re.DOTALL)
    h2_matches = list(section_pattern.finditer(body_text))
    if not h2_matches:
        # 回退：只匹配标题
        h2_matches = [m for m in re.finditer(r'^##\s+(.+)$', body_text, re.MULTILINE)]

    nonstandard = []
    for m in h2_matches:
        title = m.group(1).strip()
        title_lower = title.lower()
        if title_lower in allowed_keywords_lower:
            continue
        found = False
        for canon, syns in synonyms.items():
            if title_lower in [s.lower() for s in syns]:
                found = True
                break
        if not found:
            line_no = body_text[:m.start()].count('\n') + 1
            content = m.group(2).strip() if m.lastindex and m.lastindex >= 2 else ""
            # 取前 80 字作为内容预览（供 LLM 判断用）
            preview = content[:80].replace('\n', ' ') if content else "(无内容)"
            nonstandard.append((line_no, title, preview))

    return nonstandard


def check_progressive_loading_forced(filepath, content, fm, body, **kw):
    """
    R-17: 渐进加载强制检查 + 非标准章节检测。
    
    检查 1: SKILL.md > 230 行时必须拆分到 references/（v2.50.1 修复：移除松散引用检测，超限即 ERROR）。
    检查 2: 正文中超出 body.json allowed_sections 白名单的非标准 H2 章节，输出 🟡 WARN 供 LLM 精筛。
    """
    if not content:
        return {"passed": True, "detail": f"{filepath}:1 - 无内容，跳过检查"}

    _skill_dir_r17 = kw.get("skill_dir", "")
    lines = content.splitlines()
    line_count = len(lines)
    detail_parts = []
    passed = True

    # ── 检查 1: 行数超过 230 → ERROR（不移除引用检测，超限即强制拆分）──
    if line_count > 230:
        passed = False
        detail_parts.append(
            f"SKILL.md 共 {line_count} 行，超过 230 行限制，必须将非核心章节拆分到 references/ 并替换为「→ 详见 references/xxx.md」引用"
        )

    # ── 检查 2: 非标准章节检测（Phase 1 正则粗筛 → LLM 精筛）──
    nonstandard = _find_nonstandard_sections(body, _skill_dir_r17)
    if nonstandard:
        phase1_lines = []
        for ln, title, preview in nonstandard:
            phase1_lines.append(f"  {filepath}:{ln} - 「{title}」（内容预览：{preview}...）")
        detail_parts.append(
            f"🟡 粗筛 {len(nonstandard)} 个疑似非标章节，由全报告 LLM 精筛判断应拆分到 references/ 还是合并到标准章节："
            f"\n【两阶段】正则粗筛：以下 H2 章节不在 allowed_sections 白名单中，"
            f"需 LLM 精筛判断为真实非标（应拆分到 references/）"
            f"还是应合并到已有标准章节（如「注意事项」→「铁律/规范」）："
            f"\n" + '\n'.join(phase1_lines)
        )

    if not detail_parts:
        return {"passed": True, "detail": f"{filepath}:1 - SKILL.md 共 {line_count} 行，符合渐进加载要求（≤230 行），无非标章节"}

    return {
        "passed": passed,
        "detail": f"{filepath}:1 - {'; '.join(detail_parts)}",
        "suggestion": "全报告 LLM 精筛：对上述非标章节逐条判断。如果内容属于某标准章节（如「注意事项」→「铁律/规范」），合并之；如果确实是非标内容，拆分到 references/ 并替换为 → 详见引用。"
    }
