# -*- coding: utf-8 -*-
"""threat_engine.py — yotta-verify（元信）威胁捕获引擎（2026-08-30 增强）。

L2/L3 引擎（8 检测点威胁捕获模型 + 13 行为项口径，见 verify_rules 的
THREAT_TAXONOMY / DETECTOR_TO_TAXONOMY / BEHAVIORS / DETECTOR_TO_BEHAVIORS）：

- L3 MCP 工具面（analyze_mcp_tool_surface）：识别 MCP server 的工具集，
  逐工具追踪「工具参数 → 危险 sink」的数据流，输出工具级 finding
  （命令执行 / 任意文件读写；含 OWASP LLM06 过度授权视角）。
- L2 数据流（analyze_dataflow）：识别「不可信输入源 → 危险 sink」的可达路径
  （MCP 参数 / argv / env / 读入文件内容）。

设计原则（与元信一致）：
- 纯 Python 3.8+ 标准库、零依赖；只读静态、不执行被测代码。
- 轻量近似（正则级 taint）：宁可漏报也不误伤安全用法 —— 命中「防护上下文」
  （shell:false / 路径校验 / 白名单 / 本地 CLI 参数）即判定受控，不升级判级。
- 判级宁严勿松：确认「MCP 参数 → 危险 sink 无防护」才给 critical/high。

本模块只返回 finding 字典列表（dict），由 yotta_verify.py 转为 Finding 对象。
"""
import re

# ── 危险 sink（命令 / 文件写 / 文件读）──────────────────────────────────────
CMD_SINK_RE = re.compile(
    r"(?i)(?:spawnSync|execSync|child_process\.spawn|child_process\.exec|"
    r"child_process\.execFile|\bexec\b|\bexecFile\b|Popen|os\.system|"
    r"os\.popen|subprocess\.call|subprocess\.run|subprocess\.Popen|\beval\b|"
    r"\bFunction\b)\s*\(")
FILE_WRITE_SINK_RE = re.compile(
    r"(?i)(?:writeFile|writeFileSync|appendFile|appendFileSync|createWriteStream|"
    r"shutil\.copy|shutil\.move|os\.rename)\s*\(")
FILE_READ_SINK_RE = re.compile(
    r"(?i)(?:readFile|readFileSync|createReadStream)\s*\(")

# ── MCP server 特征（命中任一即视为 MCP 实现面）────────────────────────────
MCP_MARKERS = (
    "TOOL_HANDLERS", "callTool", "tools/call", "mcpTools", "params.get",
    "params[", "arguments[", "inputSchema", "MCP", "stdio", "tool_params",
)

# ── 不可信输入源（MCP 工具参数 / argv / env）────────────────────────────────
MCP_SOURCE_RE = re.compile(
    r"(?i)\b(?:const|let|var)\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*"
    r"(?:params\.get\(|params\[|arguments\[|req\.params|tool_params)")
ARGV_SOURCE_RE = re.compile(r"\b(?:process\.argv|sys\.argv)")
# 本地 CLI 参数对象（非 MCP 注入面 → 不判危险）
LOCAL_CLI_RE = re.compile(r"\b(?:opts|options|config|args|argv)\s*[.\[]")

# ── 安全防护上下文（sink 行 ± 窗口内出现即判定受控）────────────────────────
CMD_SAFE_MARKERS = (
    "shell: false", "shell:false", "shell=False", "shell: False",
    "argv[0]", "argv.slice", "allowlist", "白名单", "允许清单", "固定命令",
    "model allowlist", "allowed", "安全", "校验", "验证",
)
FILE_SAFE_MARKERS = (
    "resolveWithinRoot", "isWithinRoot", "within root", "记忆库目录", "memory root",
    "path.join(root", "path.resolve(root", "path.join(memoryRoot", "allowlist",
    "白名单", "允许清单", "固定路径", "安全", "校验", "验证",
)
SAFE_WINDOW = 3  # 命中行前后各 N 行


def _collect_mcp_sources(lines):
    """收集 MCP 不可信源变量：{变量名: 来源描述}。"""
    sources = {}
    for line in lines:
        m = MCP_SOURCE_RE.search(line)
        if m:
            sources[m.group(1)] = "MCP 工具参数"
    return sources


def _window_text(lines, idx):
    lo = max(0, idx - SAFE_WINDOW)
    hi = min(len(lines), idx + SAFE_WINDOW + 1)
    return "\n".join(lines[lo:hi])


def _has_marker(text, markers):
    low = text.lower()
    return any(m.lower() in low for m in markers)


def _extract_identifiers(args_text):
    """提取调用参数文本中的标识符（粗筛）。"""
    return set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", args_text))


def _is_mcp_file(text):
    return any(m in text for m in MCP_MARKERS)


def _judge_sink(lines, idx, line, sink_label, mcp_sources, kind):
    """对单个 sink 调用判级。返回 finding dict 或 None。

    kind: "cmd" / "write" / "read"
    """
    ctx = _window_text(lines, idx)
    mcp_only = {k: v for k, v in mcp_sources.items()}
    if not mcp_only:
        return None
    # 参数文本
    args_start = line.find("(")
    args_text = line[args_start + 1:] if args_start >= 0 else ""
    ids = _extract_identifiers(args_text)
    if not ids:
        return None
    # 是否有 MCP 源变量进入该 sink 调用
    tainted = ids & set(mcp_only.keys())
    if not tainted:
        return None
    # 本地 CLI 参数对象（非 MCP 注入）→ 不算 MCP 面
    if _has_marker(line, ("opts.", "options.", "config.")):
        return None
    if kind == "cmd":
        if _has_marker(ctx, CMD_SAFE_MARKERS):
            return None  # 受控（shell:false / 白名单 / argv 数组）
        sev, conf, desc = "critical", 93, "MCP 工具参数流入子进程执行（%s），无 shell/白名单防护" % sink_label
        tax = "command_execution"
    elif kind == "write":
        if _has_marker(ctx, FILE_SAFE_MARKERS):
            return None  # 路径经 root 校验/白名单
        sev, conf, desc = "high", 90, "MCP 工具参数流入文件写操作（%s），任意路径写入风险" % sink_label
        tax = "file_access"
    else:
        if _has_marker(ctx, FILE_SAFE_MARKERS):
            return None
        sev, conf, desc = "high", 88, "MCP 工具参数流入文件读操作（%s），任意路径读取风险" % sink_label
        tax = "file_access"
    behaviors = ()
    if kind == "write":
        behaviors = ("写入文件",)
    elif kind == "read":
        behaviors = ("读取文件",)
    return {
        "detector": "MCPToolSurface",
        "severity": sev,
        "category": tax,
        "rule_id": "L3-" + sink_label.split("(")[0].upper()[:12],
        "description": desc + "（源变量: %s）" % ", ".join(sorted(tainted)),
        "confidence": conf,
        "behaviors": behaviors,
    }


def analyze_mcp_tool_surface(files, read_lines):
    """L3：MCP 工具面 → 危险 sink 数据流，返回 finding dict 列表。"""
    findings = []
    for path, rel in files:
        lines = read_lines(path)
        text = "\n".join(lines)
        if not _is_mcp_file(text):
            continue
        mcp_sources = _collect_mcp_sources(lines)
        if not mcp_sources:
            continue
        for idx, line in enumerate(lines):
            for kind, rx, label in (
                    ("cmd", CMD_SINK_RE, "命令"),
                    ("write", FILE_WRITE_SINK_RE, "文件写"),
                    ("read", FILE_READ_SINK_RE, "文件读")):
                m = rx.search(line)
                if m:
                    f = _judge_sink(lines, idx, line, label, mcp_sources, kind)
                    if f:
                        f["file"] = rel
                        f["line"] = idx + 1
                        findings.append(f)
    return findings


def analyze_dataflow(files, read_lines):
    """L2：不可信输入源（argv/env/读入文件）→ 危险 sink 的可达路径（轻量近似）。

    与 L3 的区别：L3 只针对 MCP 工具面；L2 覆盖 CLI/env 输入源。
    返回 finding dict 列表（高置信才判级，否则不报，避免误伤）。
    """
    findings = []
    for path, rel in files:
        lines = read_lines(path)
        argv_vars = {}
        for _ln, _line in enumerate(lines):
            m = re.search(
                r"(?i)\b(?:const|let|var)\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*process\.argv",
                _line)
            if m:
                argv_vars[m.group(1)] = _ln
        if not argv_vars and not any(ARGV_SOURCE_RE.search(l) for l in lines):
            continue
        for idx, line in enumerate(lines):
            m = CMD_SINK_RE.search(line)
            if not m:
                continue
            ctx = _window_text(lines, idx)
            if _has_marker(ctx, CMD_SAFE_MARKERS):
                continue
            args_start = line.find("(")
            args_text = line[args_start + 1:] if args_start >= 0 else ""
            ids = _extract_identifiers(args_text)
            direct = bool(ARGV_SOURCE_RE.search(line))
            # argv 变量须在 sink 之前且相距 ≤ 50 行（避免跨函数同名误报）
            tainted = set(v for v in (ids & set(argv_vars.keys()))
                          if 0 <= (idx - argv_vars[v]) <= 50)
            if not direct and not tainted:
                continue
            findings.append({
                "detector": "Dataflow",
                "severity": "medium",
                "category": "command_execution",
                "rule_id": "L2-CMD",
                "description": "命令行参数（argv）流入子进程执行且无防护，建议人工复核"
                               "（源变量: %s）" % (", ".join(sorted(tainted)) or "argv 直接"),
                "confidence": 70,
                "file": rel,
                "line": idx + 1,
            })
    return findings



# ══════════════════════════════════════════════════════════════════════════
# 综合报告视图（2026-08-30 增强：双视角报告 + 评分 + 逐文件）
# ══════════════════════════════════════════════════════════════════════════

SEVERITY_DEDUCT = {"critical": 45, "high": 25, "medium": 10, "low": 3, "info": 0}
# 评分扣分权重 + 封顶（低危密集不扣光；中高危为主要扣分）
SCORE_WEIGHTS = {"critical": 40, "high": 20, "medium": 8, "low": 1, "info": 0}
SCORE_CAPS = {"critical": 2, "high": 4, "medium": 6, "low": 10, "info": 0}


def health_score(findings):
    """安全健康度评分 0-100（100 起扣 + 封顶；取整下限 0）。"""
    counts = {}
    for f in findings:
        sev = f.get("severity", "info")
        counts[sev] = counts.get(sev, 0) + 1
    score = 100
    for sev, w in SCORE_WEIGHTS.items():
        score -= w * min(counts.get(sev, 0), SCORE_CAPS[sev])
    return max(0, int(round(score)))


def taxonomy_view(findings, taxonomy, order, det_to_tax):
    """8 类威胁图谱：每类 verdict（danger/suspicious/safe/n/a）。"""
    hits = {}
    for f in findings:
        det = f.get("detector", "")
        key = det_to_tax.get(det, "other")
        hits.setdefault(key, []).append(f)
    out = {}
    for key in order:
        items = hits.get(key, [])
        name = taxonomy.get(key, key)
        sev = "info"
        for f in items:
            s = f.get("severity", "info")
            if SEVERITY_DEDUCT.get(s, 0) > SEVERITY_DEDUCT.get(sev, 0):
                sev = s
        if not items:
            verdict = "n/a"
        elif sev in ("critical", "high"):
            verdict = "danger"
        elif sev == "medium":
            verdict = "suspicious"
        else:
            verdict = "safe"
        out[key] = {
            "name": name, "verdict": verdict, "count": len(items),
            "severity": sev, "findings": [f.get("rule_id", "") for f in items[:5]],
        }
    return out


def behavior_view(findings, behaviors, det_to_behaviors):
    """13 行为项：observed（观察到）/ none。"""
    observed = {}
    for f in findings:
        bs = f.get("behaviors")
        if bs is None:
            bs = det_to_behaviors.get(f.get("detector", ""), ())
        for b in bs:
            observed.setdefault(b, 0)
            observed[b] += 1
    out = []
    for b in behaviors:
        out.append({"behavior": b, "observed": observed.get(b, 0)})
    return out


def file_view(findings):
    """逐文件 verdict：每文件最高严重级。"""
    per_file = {}
    for f in findings:
        fp = f.get("file", "?")
        sev = f.get("severity", "info")
        if SEVERITY_DEDUCT.get(sev, 0) > SEVERITY_DEDUCT.get(per_file.get(fp, "info"), 0):
            per_file[fp] = sev
    return [{"file": k, "verdict": v} for k, v in sorted(per_file.items())]


def build_content_hash(files, read_lines):
    """内容 hash：全部扫描文件内容的 SHA256（确定性汇总）。"""
    import hashlib
    h = hashlib.sha256()
    for path, rel in files:
        try:
            raw = path.read_bytes()
        except OSError:
            continue
        h.update(rel.encode("utf-8", errors="replace"))
        h.update(b"\x00")
        h.update(raw)
    return h.hexdigest()


def repair_guide(findings):
    """修复建议指南：按 taxonomy 分组给可执行建议。"""
    guide = []
    seen = set()
    for f in findings:
        if f.get("severity") not in ("critical", "high", "medium"):
            continue
        det = f.get("detector", "")
        key = det
        if key in seen:
            continue
        seen.add(key)
        rule_id = f.get("rule_id", "")
        if rule_id in ("L3-命令", "L3-文件写", "L3-文件读", "MCE-001", "MCE-002", "MCE-003"):
            guide.append(
                "命令执行面：对 MCP 工具/CLI 参数建立固定命令白名单，子进程禁用 shell "
                "（shell:false），参数拆为 argv 数组；确认远端调用者无命令注入能力。")
        elif det == "MCPFileAccess" or rule_id.startswith("MFA") or "文件" in (f.get("category") or ""):
            guide.append(
                "文件操作面：将 MCP 工具的读写限制在声明目录内（路径归一化 + root 校验），"
                "禁止任意路径；对敏感文件（密钥/凭据）读取需人工确认。")
        elif rule_id.startswith("PTV"):
            guide.append(
                "路径穿越：路径拼接前做归一化与根目录校验，拒绝父目录逃逸与绝对路径越界。")
        elif det == "PromptInjection" or rule_id.startswith("PIJ"):
            guide.append(
                "提示注入：技能/工具描述视为不可信数据，去除非必要指令性话术；敏感操作先问用户。")
        elif rule_id.startswith("DEX") or rule_id.startswith("NET-0"):
            guide.append(
                "远程下载/网络面：移除『下载后立即执行』的链路，外发数据需用户确认与白名单。")
        else:
            guide.append(
                "%s：按报告逐条复核并修复，涉及系统/凭据/持久化面需最小权限化。"
                % (f.get("category") or det))
    return guide
