#!/usr/bin/env python3
"""
i18n — report output language catalog for skill-release-audit.

Resolution order for the active language:
  1. explicit set_lang() / --lang CLI flag
  2. SKILL_AUDIT_LANG environment variable
  3. default "zh"

Only the SECOND language supported today is "en"; unknown codes fall back to zh.
All USER-FACING strings (report scaffolding + per-issue messages + module names)
go through t(key, **kw). Developer code comments are intentionally NOT translated.

Usage:
    from i18n import t, set_lang, current_lang
    t("module.logic")                       # -> "模块1 语法与逻辑" / "Module 1 Syntax & Logic"
    t("deps.py_missing", pkg="requests")    # -> formatted, interpolated
"""

import os

_SUPPORTED = ("zh", "en")
_DEFAULT = "zh"
_lang = None  # lazily resolved


def set_lang(code: str | None) -> str:
    """Set the active language explicitly (e.g. from --lang). Returns the
    effective code (falls back to zh for unknown)."""
    global _lang
    if code and code.lower() in _SUPPORTED:
        _lang = code.lower()
    else:
        _lang = _DEFAULT
    return _lang


def current_lang() -> str:
    global _lang
    if _lang is None:
        env = (os.environ.get("SKILL_AUDIT_LANG") or "").lower()
        _lang = env if env in _SUPPORTED else _DEFAULT
    return _lang


def t(key: str, **kw) -> str:
    """Translate `key` into the active language and format with kw."""
    lang = current_lang()
    table = _CATALOG.get(key)
    if table is None:
        # Unknown key: surface it rather than crash, so missing entries are caught.
        return key
    template = table.get(lang) or table.get(_DEFAULT) or key
    if kw:
        try:
            return template.format(**kw)
        except (KeyError, IndexError):
            return template
    return template


# ---------------------------------------------------------------------------
# Catalog: key -> {lang: template}
# ---------------------------------------------------------------------------
_CATALOG: dict[str, dict[str, str]] = {
    # ---- module names ----
    "module.logic":     {"zh": "模块1 语法与逻辑",       "en": "Module 1 Syntax & Logic"},
    "module.features":  {"zh": "模块2 功能完整性",       "en": "Module 2 Feature Completeness"},
    "module.edges":     {"zh": "模块3 边界与异常处理",   "en": "Module 3 Edge Cases & Errors"},
    "module.data":      {"zh": "模块4 数据与配置安全",   "en": "Module 4 Data & Config Safety"},
    "module.deps":      {"zh": "模块5 依赖检查",         "en": "Module 5 Dependencies"},
    "module.docs":      {"zh": "模块6 文档规范",         "en": "Module 6 Documentation"},
    "module.crashed":   {"zh": "模块运行出错",           "en": "Module crashed"},

    # ---- report scaffolding (healthcheck.py) ----
    "report.auto_installed":   {"zh": "↳ 已自动安装: {pkgs}", "en": "↳ auto-installed: {pkgs}"},
    "report.no_issues":        {"zh": "无问题",              "en": "no issues"},
    "report.summary":          {"zh": "📊 汇总: {name}",      "en": "📊 Summary: {name}"},
    "report.pass":             {"zh": "✅ PASS: {n} 个模块",  "en": "✅ PASS: {n} module(s)"},
    "report.warn":             {"zh": "⚠️  WARN: {n} 个模块 — {mods}", "en": "⚠️  WARN: {n} module(s) — {mods}"},
    "report.fail":             {"zh": "❌ FAIL: {n} 个模块 — {mods}", "en": "❌ FAIL: {n} module(s) — {mods}"},
    "report.all_pass":         {"zh": "🎉 全部通过，skill 可安全使用！", "en": "🎉 All checks passed — the skill is safe to use!"},
    "report.warns_only":       {"zh": "共 {w} 个警告，建议修复后再发布", "en": "{w} warning(s) — recommended to fix before publishing"},
    "report.errors":           {"zh": "共 {e} 个错误 + {w} 个警告，需修复", "en": "{e} error(s) + {w} warning(s) — must fix"},
    "report.target_profile":   {"zh": "target profile: {name}", "en": "target profile: {name}"},
    "report.module_crashed":   {"zh": "检查模块崩溃: {err}", "en": "Check module crashed: {err}"},

    # ---- CLI errors (healthcheck.py main) ----
    "cli.unknown_target":      {"zh": "未知的 --target '{t}'。可用: {avail}", "en": "unknown --target '{t}'. Available: {avail}"},
    "cli.dir_not_found":       {"zh": "目录不存在: {path}", "en": "directory not found: {path}"},
    "cli.not_a_skill":         {"zh": "不是有效的 skill 目录（缺少 SKILL.md）: {path}", "en": "not a valid skill directory (missing SKILL.md): {path}"},
    "cli.bad_modules":         {"zh": "--modules 格式错误，示例: --modules 1,3,5", "en": "invalid --modules format, example: --modules 1,3,5"},
    "cli.profile_corrupt":     {"zh": "[WARN] 目标 profile '{name}' 文件损坏或无法解析，已降级为内置 generic 规则集。请人工核实 profiles/{name}.json。", "en": "[WARN] target profile '{name}' is corrupt or unparseable; degraded to the built-in generic ruleset. Please check profiles/{name}.json manually."},

    # ---- module 1: logic ----
    "logic.py_syntax":         {"zh": "Python 语法错误: {msg}", "en": "Python syntax error: {msg}"},
    "logic.py_unparseable":    {"zh": "无法解析文件: {err}", "en": "Cannot parse file: {err}"},
    "logic.bash_check_fail":   {"zh": "无法运行 bash 语法检查: {err}", "en": "Cannot run bash syntax check: {err}"},
    "logic.bash_syntax":       {"zh": "Bash 语法错误: {line}", "en": "Bash syntax error: {line}"},
    "logic.missing_ref":       {"zh": "引用了不存在的文件: {ref}", "en": "References a non-existent file: {ref}"},
    "logic.import_not_found":  {"zh": "相对导入模块未找到: {module}", "en": "Relative import module not found: {module}"},
    "logic.leftover_marker":   {"zh": "遗留标记: {line}", "en": "Leftover marker: {line}"},

    # ---- module 2: features ----
    "features.script_unmentioned": {"zh": "脚本 {name} 存在但 SKILL.md 中未提及", "en": "Script {name} exists but is not mentioned in SKILL.md"},
    "features.ref_unmentioned":    {"zh": "参考文件 {name} 存在但 SKILL.md 中未提及", "en": "Reference file {name} exists but is not mentioned in SKILL.md"},
    "features.stub_script":        {"zh": "脚本内容过少（{n} 行有效代码），可能是存根文件", "en": "Script has too little content ({n} effective lines); may be a stub"},
    "features.thin_body":          {"zh": "SKILL.md 正文内容过少，缺少使用说明", "en": "SKILL.md body is too thin; lacks usage instructions"},

    # ---- module 3: edges ----
    "edges.no_try":            {"zh": "[{cat}] {name}() 调用未被 try/except 保护", "en": "[{cat}] {name}() call is not protected by try/except"},
    "edges.no_timeout":        {"zh": "网络调用 {name}() 缺少 timeout 参数，可能导致永久挂起", "en": "Network call {name}() lacks a timeout; may hang forever"},
    "edges.no_status_check":   {"zh": "发现 HTTP 调用但未检查响应状态码（缺少 raise_for_status 或 .status_code 判断）", "en": "HTTP call found but response status is not checked (missing raise_for_status or .status_code)"},
    "edges.no_set_e":          {"zh": "Bash 脚本缺少 'set -e'（建议使用 set -euo pipefail）", "en": "Bash script lacks 'set -e' (recommend set -euo pipefail)"},

    # ---- module 4: data safety ----
    "data.file_write_in_dir":  {"zh": "检测到基于 __file__ 的路径构造 + 写操作，数据可能写入 skill 目录（更新后丢失）。建议改为 skill 目录外的持久化目录，例如 {hint}", "en": "Detected __file__-based path construction + write; data may be written inside the skill dir (lost on update). Use a persistent dir outside the skill, e.g. {hint}"},
    "data.relative_write":     {"zh": "相对路径数据存储: {snippet} — 若写入 skill 目录，更新后数据将丢失", "en": "Relative-path data storage: {snippet} — if written inside the skill dir, data is lost on update"},
    "data.hardcoded_dir":      {"zh": "硬编码的 skill 目录路径用于数据存储: {snippet}", "en": "Hardcoded skill-dir path used for data storage: {snippet}"},
    "data.datafile_in_dir":    {"zh": "skill 目录内存在数据文件 {rel}，重新安装 skill 后该文件将被覆盖或删除", "en": "Data file {rel} exists inside the skill dir; it will be overwritten or removed on reinstall"},
    "data.hint":               {"zh": "数据/缓存/配置推荐路径（skill 目录外）: {hint}", "en": "Recommended data/cache/config path (outside the skill dir): {hint}"},

    # ---- module 5: deps ----
    "deps.undeclared_env":     {"zh": "代码读取了以下环境变量但未在 frontmatter 声明: {vars}\n  ClawHub 安全审查会判为「声明与代码不一致」。请在 metadata.openclaw.requires.env / primaryEnv / envVars 中声明。", "en": "Code reads these env vars but they are not declared in frontmatter: {vars}\n  ClawHub security analysis flags this as a declaration-vs-code mismatch. Declare them under metadata.openclaw.requires.env / primaryEnv / envVars."},
    "deps.install_timeout":    {"zh": "安装超时（{timeout}s）", "en": "install timed out ({timeout}s)"},
    "deps.installed":          {"zh": "已自动安装 {pip}", "en": "auto-installed {pip}"},
    "deps.unknown_error":      {"zh": "未知错误", "en": "unknown error"},
    "deps.py_install_failed":  {"zh": "Python 包 '{pkg}' 未安装，自动安装失败: {msg}\n  手动安装: pip install {pip}", "en": "Python package '{pkg}' not installed, auto-install failed: {msg}\n  Install manually: pip install {pip}"},
    "deps.py_missing":         {"zh": "Python 包 '{pkg}' 未安装", "en": "Python package '{pkg}' not installed"},
    "deps.py_optional_missing":{"zh": "可选 Python 包 '{pkg}' 未安装（已在 frontmatter python_optional 声明）；如需使用相关功能请：pip install {pip}", "en": "Optional Python package '{pkg}' not installed (declared in frontmatter python_optional); install it if you need that feature: pip install {pip}"},
    "deps.node_missing":       {"zh": "Node 包 '{pkg}' 未找到", "en": "Node package '{pkg}' not found"},
    "deps.bin_missing":        {"zh": "系统命令 '{b}' 未找到（PATH 中不存在）", "en": "System command '{b}' not found (not on PATH)"},
    "deps.py_undeclared":      {"zh": "以下 Python 依赖未在 SKILL.md frontmatter 中声明: {pkgs}", "en": "The following Python deps are not declared in SKILL.md frontmatter: {pkgs}"},
    "deps.bin_undeclared":     {"zh": "以下系统命令依赖未在 SKILL.md frontmatter 中声明: {bins}", "en": "The following system-command deps are not declared in SKILL.md frontmatter: {bins}"},
    "deps.install_hint_generic": {"zh": "请手动安装 {bin}", "en": "Please install {bin} manually"},

    # ---- module 6: docs ----
    "docs.no_description":     {"zh": "frontmatter 缺少 description 字段", "en": "frontmatter is missing the description field"},
    "docs.desc_too_short":     {"zh": "description 过短（{n} 字符），建议描述使用场景和触发词", "en": "description is too short ({n} chars); add usage scenarios and trigger words"},
    "docs.desc_no_scenario":   {"zh": "description 建议包含使用场景（'当用户说...' 或 'Use when...'）", "en": "description should include usage scenarios ('when the user...' or 'Use when...')"},
    "docs.no_deps_section":    {"zh": "有 Python 脚本但 SKILL.md 中缺少依赖说明章节（建议添加 ## 依赖 章节，列出 pip install 命令）", "en": "Python scripts present but SKILL.md lacks a dependencies section (add a ## Dependencies section listing pip install commands)"},
    "docs.name_mismatch":      {"zh": "frontmatter name='{name}' 与目录名 '{dir}' 不一致", "en": "frontmatter name='{name}' does not match directory name '{dir}'"},
    "docs.no_version":         {"zh": "frontmatter 缺少 version 字段。多数 Hub 视为可选，但部分私有 SkillHub 发布时必填，缺失会报「版本不允许为空」。建议添加：version: 1.0.0", "en": "frontmatter is missing the version field. Optional on most hubs, but required by some private SkillHub deployments (else 'version may not be empty'). Suggest adding: version: 1.0.0"},
    "docs.bad_version":        {"zh": "frontmatter version='{version}' 格式建议使用语义化版本号（如 1.0.0）", "en": "frontmatter version='{version}' should use semantic versioning (e.g. 1.0.0)"},
    "docs.unexpected_keys":    {"zh": "frontmatter 包含非标准字段: {keys}。允许字段: {allowed}", "en": "frontmatter contains non-standard fields: {keys}. Allowed fields: {allowed}"},
    "docs.required_field":     {"zh": "目标 Hub 要求 frontmatter 字段 '{key}'，当前缺失或为空", "en": "Target hub requires frontmatter field '{key}', currently missing or empty"},
    "docs.slug_pattern":       {"zh": "slug '{slug}' 不符合目标 Hub 的命名规则 {pattern}（通常要求小写字母/数字/连字符）", "en": "slug '{slug}' does not match the target hub naming rule {pattern} (usually lowercase letters/digits/hyphens)"},
    "docs.slug_too_long":      {"zh": "slug '{slug}' 长度 {n} 超过目标 Hub 上限 {max}", "en": "slug '{slug}' length {n} exceeds the target hub limit {max}"},
    "docs.name_too_long":      {"zh": "name 长度 {n} 超过目标规范上限 {max}", "en": "name length {n} exceeds the target spec limit {max}"},
    "docs.desc_too_long":      {"zh": "description 长度 {n} 超过目标规范上限 {max}", "en": "description length {n} exceeds the target spec limit {max}"},
    "docs.no_readme":          {"zh": "目标 Hub（如 GitHub）要求 README，但未找到 README.md", "en": "Target hub (e.g. GitHub) requires a README, but README.md was not found"},
    "docs.no_license":         {"zh": "目标 Hub（如 GitHub）要求 LICENSE 文件，但未找到", "en": "Target hub (e.g. GitHub) requires a LICENSE file, but none was found"},
    "docs.no_skill_md":        {"zh": "SKILL.md 不存在", "en": "SKILL.md does not exist"},
}
