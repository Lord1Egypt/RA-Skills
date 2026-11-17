#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""yotta_guardian.py — YottaMeta 元盾（yotta-guardian）：工具调用拦截护栏。

确定性规则引擎 + 可插拔意图验证，拦截危险 exec / write / edit / read / run / shell
工具调用，提供审计日志与机器可读判定。纯 Python 3.8+ 标准库，零外部依赖，
Windows + Linux + macOS 通用，跨智能体（Claude Code / Cursor / Codex / 通用 Agent）可用。

子命令：
  check    对一条或多条工具调用做安全评估（--batch 批量、--json 机器输出）
  audit    查询审计日志（JSONL）
  rules    打印内置规则摘要 / 校验自定义规则文件
  version  打印版本

退出码（与元安 / 元审家族一致）：
  0 = 允许（无 finding 或仅 low）
  1 = 允许但带警告（存在 medium / 宽松策略下的 high）
  2 = 拒绝（high）
  3 = 拒绝（critical）
  4 = 用法错误 / 致命异常

用法示例：
  python3 yotta_guardian.py check exec --cmd "git status"
  python3 yotta_guardian.py check exec --cmd "npm install" --policy default
  python3 yotta_guardian.py check write --path /etc/passwd --content "..."
  python3 yotta_guardian.py check --batch calls.json --json
  python3 yotta_guardian.py audit --file .yotta-guardian/audit.jsonl --tail 10
"""
import argparse
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
try:
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
try:
    import guardian_rules as GR  # noqa: E402
except BaseException as _import_exc:  # 规则表加载失败 = 引擎没跑起来 → 致命异常（4）
    sys.stderr.write(
        "致命异常: 规则表加载失败: %s: %s\n" % (type(_import_exc).__name__, _import_exc)
    )
    raise SystemExit(4)

VERSION = "0.1.10"
TOOL_NAME = "yotta-guardian"
TOOL_CN = "元盾"

TOOL_TYPES = ("exec", "run", "shell", "write", "edit", "read")
_DENY_VERDICT = "deny"
_ALLOW_VERDICT = "allow"
_REVIEW_VERDICT = "review"


# ── 基础数据 ───────────────────────────────────────────────────────────────

def _sev(w):
    return GR.severity_value(w)


def _worst(findings):
    worst = "info"
    for f in findings:
        if _sev(f.severity) > _sev(worst):
            worst = f.severity
    return worst


def _is_win_root(p):
    return bool(re.match(r"^[a-zA-Z]:[\\/]?$", p.strip()))


class Finding:
    """单条规则命中。"""

    __slots__ = ("rule_id", "severity", "category", "reason", "confidence")

    def __init__(self, rule_id, severity, category, reason, confidence=60):
        self.rule_id = rule_id
        self.severity = severity
        self.category = category
        self.reason = reason
        self.confidence = confidence

    def to_dict(self):
        return {"rule_id": self.rule_id, "severity": self.severity,
                "category": self.category, "reason": self.reason,
                "confidence": self.confidence}

    def __repr__(self):
        return "[%s] %s: %s" % (self.severity.upper(), self.rule_id, self.reason)


class ToolCall:
    """一次结构化的工具调用。"""

    __slots__ = ("tool", "cmd", "path", "content", "old", "new", "target")

    def __init__(self, tool="exec", cmd="", path="", content="", old="", new="",
                 target=""):
        self.tool = (tool or "exec").lower()
        self.cmd = cmd or ""
        self.path = path or ""
        self.content = content or ""
        self.old = old or ""
        self.new = new or ""
        self.target = target or ""

    def describe(self, limit=200):
        if self.tool in ("exec", "run", "shell"):
            return self.cmd[:limit]
        if self.tool in ("write", "edit"):
            return "%s %s" % (self.tool, self.path[:limit])
        if self.tool == "read":
            return "read %s" % self.path[:limit]
        return (self.target or self.cmd or self.path or self.content)[:limit]

    def to_dict(self):
        d = {"tool": self.tool}
        for k in ("cmd", "path", "content", "old", "new", "target"):
            v = getattr(self, k)
            if v:
                d[k] = v
        return d


class Verdict:
    """一次评估的结论。"""

    __slots__ = ("allowed", "severity", "reason", "rule_ids", "findings",
                 "verifier")

    def __init__(self, allowed, severity, reason, rule_ids, findings,
                 verifier=None):
        self.allowed = allowed
        self.severity = severity
        self.reason = reason
        self.rule_ids = rule_ids
        self.findings = findings
        self.verifier = verifier

    def exit_code(self):
        if not self.allowed:
            return _sev(self.severity)
        if self.severity in ("high", "medium"):
            return 1
        return 0

    def to_dict(self):
        return {"verdict": _ALLOW_VERDICT if self.allowed else _DENY_VERDICT,
                "allowed": self.allowed, "severity": self.severity,
                "reason": self.reason, "rule_ids": self.rule_ids,
                "findings": [f.to_dict() for f in self.findings],
                "verifier": self.verifier, "exit": self.exit_code()}


# ── 确定性规则引擎 ─────────────────────────────────────────────────────────

class RuleEngine:
    """确定性规则引擎：文本模式 + argv 级分析 + 敏感路径 + 内容规则。

    policy: default（拒绝 high+，中危警告） / strict（拒绝 medium+） /
            loose（仅拒绝 critical）。
    """

    def __init__(self, policy="default", allow_patterns=None, allow_paths=None,
                 config_path=None, cwd=None, verifier=None):
        self.policy = policy
        self.cwd = str(Path(cwd or os.getcwd()).resolve())
        self.compiled = GR.compile_rules()
        self.allow_text = [re.compile(p) for p in GR.ALLOW_PATTERNS]
        self.allow_patterns = [re.compile(p) for p in (allow_patterns or [])]
        self.allow_paths = [self._norm_abs(p) for p in (allow_paths or [])]
        self.custom_deny = []
        self.config = self._load_config(config_path)
        if self.config.get("policy"):
            self.policy = self.config["policy"]
        for p in self.config.get("allow", []):
            try:
                self.allow_patterns.append(re.compile(p))
            except re.error as e:
                self._die("自定义放行模式编译失败: %s (%s)" % (p, e))
        for p in self.config.get("allow_paths", []):
            self.allow_paths.append(self._norm_abs(p))
        for p in self.config.get("deny", []):
            try:
                self.custom_deny.append(re.compile(p))
            except re.error as e:
                self._die("自定义拒绝模式编译失败: %s (%s)" % (p, e))
        if verifier is None:
            cfg_v = self.config.get("verifier") or {}
            if cfg_v.get("heuristic"):
                verifier = HeuristicVerifier()
            elif cfg_v.get("command"):
                verifier = ExternalVerifier(cfg_v["command"],
                                            cfg_v.get("timeout", 30))
        self.verifier = verifier

    @staticmethod
    def _die(msg):
        print("错误: %s" % msg, file=sys.stderr)
        raise SystemExit(4)

    def _load_config(self, path):
        if not path:
            return {}
        try:
            data = json.loads(Path(path).read_text(encoding="utf-8"))
        except Exception as e:
            self._die("配置文件读取/解析失败: %s (%s)" % (path, e))
        if not isinstance(data, dict):
            self._die("配置文件需为 JSON 对象: %s" % path)
        return data

    def _norm_abs(self, p):
        p = str(p or "").strip().strip("\"'")
        if not p:
            return ""
        p = os.path.expanduser(p)
        if not os.path.isabs(p):
            p = os.path.join(self.cwd, p)
        return os.path.normpath(os.path.abspath(p))

    def _in_cwd(self, abs_p):
        cwd = os.path.normcase(self.cwd)
        p = os.path.normcase(abs_p)
        return p == cwd or p.startswith(cwd + os.sep)

    # ── 规则匹配 ──────────────────────────────────────────────────────────

    def _text_findings(self, text, scope):
        if not text:
            return []
        findings = []
        for r in GR.TEXT_PATTERNS:
            if r.scope != "both" and r.scope != scope:
                continue
            if self.compiled[r.id].search(text):
                findings.append(Finding(r.id, r.severity, r.category,
                                        r.reason, r.confidence))
        for rx in self.custom_deny:
            if rx.search(text):
                findings.append(Finding("CFG-DENY", "high", "config",
                                        "命中自定义拒绝规则", 90))
        return findings

    def _path_findings(self, path, cap=None):
        if not path:
            return []
        abs_p = self._norm_abs(path)
        if not abs_p:
            return []
        findings = []
        for r in GR.PATH_PATTERNS:
            if self.compiled[r.id].search(os.path.normcase(abs_p)):
                findings.append(Finding(r.id, r.severity, "path", r.reason,
                                        r.confidence))
        if not self._in_cwd(abs_p):
            findings.append(Finding("OUT-001", "medium", "path",
                                    "目标在当前工作目录之外", 60))
        if cap is not None:
            capped = []
            for f in findings:
                sev = f.severity if _sev(f.severity) <= _sev(cap) else cap
                capped.append(Finding(f.rule_id, sev, f.category, f.reason,
                                      f.confidence))
            findings = capped
        return findings

    def _argv_findings(self, call):
        if call.tool not in ("exec", "run", "shell"):
            return []
        findings = []
        # v0.1.6：先拆复合命令（; && || | & 换行）与命令替换，再逐段解包 +
        # 跑同一套 argv 规则；v0.1.5 的包装解包对每段继续生效。
        for seg in _command_segments(call.cmd):
            argv = _tokenize(seg)
            if not argv:
                continue
            for sub in _unwrap_argv(argv):
                findings += self._argv_findings_one(sub)
        return findings

    def _argv_findings_one(self, argv):
        verb = os.path.basename(argv[0]).lower()
        findings = []
        if verb in _RM_VERBS:
            findings += _analyze_rm(argv)
        elif verb in _FORMAT_VERBS:
            findings += _analyze_format(argv)
        elif verb in _DD_VERBS:
            findings += _analyze_dd(argv)
        elif verb in _POWER_VERBS:
            findings += _analyze_power(argv)
        elif verb in _CHMOD_VERBS:
            findings += _analyze_chmod(argv)
        elif verb in _CHOWN_VERBS:
            findings += _analyze_chown(argv)
        elif verb in _PRIV_VERBS:
            findings += _analyze_priv(argv)
        elif verb in _FIREWALL_VERBS:
            findings += _analyze_firewall(argv)
        elif verb in _SERVICE_VERBS:
            findings += _analyze_service(argv)
        elif verb in _PERSIST_VERBS:
            findings += _analyze_persist(argv)
        elif verb in _REVSHELL_VERBS:
            findings += _analyze_revshell(argv)
        elif verb in ("powershell", "pwsh"):
            for a in argv[1:]:
                low = a.lower()
                if low in ("-enc", "-encodedcommand") or low.startswith("-enc"):
                    findings.append(Finding("ARG-PS-ENCODED", "critical",
                                            "command",
                                            "PowerShell 编码命令执行", 90))
                    break
        return findings

    def _allow_hit(self, call):
        if call.tool in ("exec", "run", "shell"):
            # v0.1.6：放行规则只覆盖「单一简单命令」。复合命令或命令替换不允许被
            # 整条放行——否则 `echo ok && <危险命令>` 会借放行规则绕过风险判定。
            if (len(_split_compound(call.cmd)) > 1
                    or _extract_substitutions(call.cmd)
                    or _scan_quotes(call.cmd)):
                return False
            for rx in self.allow_text + self.allow_patterns:
                if rx.search(call.cmd):
                    return True
        if call.tool in ("write", "edit", "read"):
            abs_p = self._norm_abs(call.path)
            if abs_p:
                for ap in self.allow_paths:
                    if ap and (abs_p == ap or abs_p.startswith(ap + os.sep)):
                        return True
        return False

    # ── 主评估 ────────────────────────────────────────────────────────────

    def evaluate(self, call):
        findings = []
        if call.tool in ("exec", "run", "shell"):
            findings += self._text_findings(call.cmd, "command")
            if _scan_quotes(call.cmd):
                findings.append(Finding("CMD-UNPARSED", "medium", "command",
                                        "命令引号未闭合，无法可靠拆分，按未知风险处理",
                                        80))
            segments = _command_segments(call.cmd)
            if len(segments) > 1:
                for seg in segments:
                    findings += self._text_findings(seg, "command")
            findings += self._argv_findings(call)
        elif call.tool in ("write", "edit"):
            findings += self._path_findings(call.path)
            findings += self._text_findings(call.content, "content")
            if call.new:
                findings += self._text_findings(call.new, "content")
        elif call.tool == "read":
            findings += self._path_findings(call.path, cap="medium")
        allow_hit = self._allow_hit(call)
        verdict = self._decide(findings, allow_hit)
        if self.verifier and verdict.allowed:
            verdict = self._apply_verifier(call, verdict)
        return verdict

    def _decide(self, findings, allow_hit):
        worst = _worst(findings)
        w = _sev(worst)
        if not findings:
            return Verdict(True, "low", "允许：未命中风险规则", [], [])
        if self.policy == "strict":
            if w >= 3:
                return self._deny("critical", findings)
            if w == 2:
                if allow_hit:
                    return self._warn("high", "允许（放行规则覆盖高危）", findings)
                return self._deny("high", findings)
            if w == 1:
                if allow_hit:
                    return self._warn("medium", "允许（放行规则覆盖中危）", findings)
                return self._deny("medium", findings)
            return self._warn("low", "允许（严格策略，低危提示）", findings)
        if self.policy == "loose":
            if w >= 3:
                return self._deny("critical", findings)
            if w == 2:
                return self._warn("high", "允许（宽松策略，高危仅警告）", findings)
            if w == 1:
                return Verdict(True, "low", "允许（宽松策略）", _ids(findings),
                               findings)
            return Verdict(True, "low", "允许", _ids(findings), findings)
        # default
        if w >= 3:
            return self._deny("critical", findings)
        if w == 2:
            if allow_hit:
                return self._warn("high", "允许（放行规则覆盖高危）", findings)
            return self._deny("high", findings)
        if w == 1:
            if allow_hit:
                return Verdict(True, "low", "允许（放行规则覆盖中危）",
                               _ids(findings), findings)
            return self._warn("medium", "允许但建议复核（存在中危）", findings)
        return Verdict(True, "low", "允许", _ids(findings), findings)

    @staticmethod
    def _deny(severity, findings):
        return Verdict(False, severity, "拒绝：%s" % _first_reason(findings),
                       _ids(findings), findings)

    @staticmethod
    def _warn(severity, reason, findings):
        return Verdict(True, severity, reason, _ids(findings), findings)

    def _apply_verifier(self, call, verdict):
        req = {"tool": call.tool, "cmd": call.cmd, "path": call.path,
               "content_preview": call.content[:500],
               "target": call.target, "policy": self.policy,
               "cwd": self.cwd,
               "findings": [f.to_dict() for f in verdict.findings]}
        resp = self.verifier.verify(req)
        if not resp:
            resp = {"verdict": _REVIEW_VERDICT, "severity": "medium",
                    "reason": "意图验证器无响应（按复核处理）"}
        v = resp.get("verdict", _REVIEW_VERDICT)
        if v == _DENY_VERDICT:
            sev = resp.get("severity", "high")
            if sev not in GR.SEVERITY_ORDER:
                sev = "high"
            return Verdict(False, sev,
                           "意图验证拒绝：%s" % resp.get("reason", "未说明"),
                           verdict.rule_ids, verdict.findings,
                           verifier={"name": self.verifier.name, **resp})
        if v == _REVIEW_VERDICT and verdict.severity in ("low", "info"):
            return Verdict(True, "medium",
                           "意图验证建议复核：%s" % resp.get("reason", ""),
                           verdict.rule_ids, verdict.findings,
                           verifier={"name": self.verifier.name, **resp})
        return Verdict(verdict.allowed, verdict.severity, verdict.reason,
                       verdict.rule_ids, verdict.findings,
                       verifier={"name": self.verifier.name, **resp})


def _ids(findings):
    return [f.rule_id for f in findings]


def _first_reason(findings):
    if not findings:
        return "未说明"
    return findings[0].reason


def _tokenize(cmd):
    try:
        return shlex.split(cmd, posix=(os.name != "nt"))
    except ValueError:
        return cmd.split()


# ── 包装命令解包（v0.1.5）─────────────────────────────────────────────────
# 危险动作常被包装：sh -c "…"、bash -lc "…"、cmd /c "…"、powershell -Command "…"、
# sudo …、env …、nohup …、timeout 5 …。只分析 argv[0] 会漏掉内层动词，
# 因此先按已知包装表做受控解包（深度上限），再对内层命令跑同一套 argv 规则。
_UNWRAP_MAX_DEPTH = 3

_SHELL_WRAPPERS = {
    "sh", "bash", "zsh", "dash", "ksh", "ash", "busybox",
    "cmd", "cmd.exe", "powershell", "powershell.exe", "pwsh", "pwsh.exe",
}
# shell 的「执行字符串」开关：-c / -lc / -ic / /c / /k / -Command
_SHELL_EXEC_FLAGS = {"/c", "/k", "-command", "-cmd"}
_SHELL_EXEC_FLAG_RE = re.compile(r"^-[a-z]*c$")

_WRAPPER_SPECS = {
    "sudo": {"value_opts": {"-u", "-g", "-p", "-C", "-h", "-r", "-t", "-U",
                            "--user", "--group", "--prompt", "--chdir", "--host",
                            "--role", "--type", "--other-user", "--close-from"}},
    "doas": {"value_opts": {"-u", "-C"}},
    "env": {"value_opts": {"-u", "-S", "-C", "--unset", "--split-string", "--chdir"},
            "assignments": True},
    "nohup": {"value_opts": {}},
    "setsid": {"value_opts": {}},
    "stdbuf": {"value_opts": {"-i", "-o", "-e", "--input", "--output", "--error"}},
    "nice": {"value_opts": {"-n", "--adjustment"}},
    "ionice": {"value_opts": {"-c", "-n", "-p", "--class", "--classdata", "--pid"}},
    "time": {"value_opts": {"-o", "-f", "--output", "--format"}},
    "xargs": {"value_opts": {"-I", "-n", "-P", "-d", "-a", "-E", "-s", "-L",
                             "--max-args", "--max-procs", "--delimiter", "--arg-file",
                             "--eof", "--max-chars", "--max-lines"}},
    "timeout": {"value_opts": {"-s", "-k", "--signal", "--kill-after"},
                "skip_positional": 1},
    "command": {"value_opts": {}},
    "builtin": {"value_opts": {}},
    "exec": {"value_opts": {}},
    "chroot": {"value_opts": {"--userspec", "--groups"}},
    "busybox": {"value_opts": {}},
}


def _shell_inner(argv):
    """从 shell 包装 argv 中取出执行开关后的内层命令文本（无则返回 None）。"""
    for i, tok in enumerate(argv[1:], start=1):
        low = tok.lower()
        if low in _SHELL_EXEC_FLAGS or _SHELL_EXEC_FLAG_RE.match(low):
            rest = argv[i + 1:]
            if not rest:
                return None
            parts = []
            for item in rest:
                # Windows 下 shlex(posix=False) 会保留外层引号，剥掉后再拼内层命令
                if len(item) >= 2 and item[0] == item[-1] and item[0] in ("'", '"'):
                    item = item[1:-1]
                parts.append(item)
            return " ".join(parts)
    return None


def _strip_wrapper(argv, spec):
    """跳过包装命令自身的选项/参数，返回内层命令 argv（找不到则空列表）。"""
    value_opts = spec.get("value_opts", set())
    i = 1
    n = len(argv)
    while i < n:
        tok = argv[i]
        if spec.get("assignments") and "=" in tok and not tok.startswith("-"):
            i += 1
            continue
        if tok == "--":
            i += 1
            break
        if tok.startswith("-") and tok != "-":
            i += 2 if tok in value_opts else 1
            continue
        break
    i += int(spec.get("skip_positional", 0) or 0)
    return argv[i:] if i < n else []


def _unwrap_argv(argv, depth=0):
    """返回需要做 argv 级分析的命令列表（含解包出的内层命令）。"""
    if not argv or depth > _UNWRAP_MAX_DEPTH:
        return []
    verb = os.path.basename(argv[0]).lower()
    if verb in _SHELL_WRAPPERS:
        inner = _shell_inner(argv)
        return _unwrap_argv(_tokenize(inner), depth + 1) if inner else []
    spec = _WRAPPER_SPECS.get(verb)
    if spec:
        rest = _strip_wrapper(argv, spec)
        return _unwrap_argv(rest, depth + 1) if rest else []
    return [argv]


# ── 复合命令拆分（v0.1.6）─────────────────────────────────────────────────
# v0.1.5 解决了包装命令（sh -c / sudo / env …）绕过，但整条命令仍然只按第一个词
# 做 argv 分析：`echo ok && rm -rf /`、`ls; rm -rf /`、`true || rm -rf /` 里的
# 危险段藏在分隔符之后，整条命令因此被判放行。现在先按顶层分隔符拆分、再逐段跑
# 同一套文本 / argv 规则；命令替换（$(...) / `...`）同样展开；拆分不安全时 fail-closed。
_COMPOUND_SEPARATORS = (";", "|", "&", "\n", "\r")
_SEGMENT_MAX = 32
_SEGMENT_DEPTH = 3
_SUBST_MAX = 16
_QUOTES = ("'", '"', "`")


def _scan_quotes(cmd):
    """扫描引号闭合情况，返回未闭合的引号字符（全部闭合返回 None）。"""
    quote = None
    i = 0
    n = len(cmd)
    while i < n:
        ch = cmd[i]
        if quote:
            if quote != "'" and ch == "\\" and i + 1 < n:
                i += 2
                continue
            if ch == quote:
                quote = None
            i += 1
            continue
        if ch in _QUOTES:
            quote = ch
        elif ch == "\\" and i + 1 < n:
            i += 2
            continue
        i += 1
    return quote


def _split_compound(cmd):
    """按顶层分隔符（; && || | & 换行）拆分命令，引号 / 转义内不拆。"""
    segs = []
    cur = []
    quote = None
    i = 0
    n = len(cmd)
    while i < n:
        ch = cmd[i]
        if quote:
            cur.append(ch)
            if quote != "'" and ch == "\\" and i + 1 < n:
                cur.append(cmd[i + 1])
                i += 2
                continue
            if ch == quote:
                quote = None
            i += 1
            continue
        if ch in _QUOTES:
            quote = ch
            cur.append(ch)
            i += 1
            continue
        if ch == "\\" and i + 1 < n:
            cur.append(ch)
            cur.append(cmd[i + 1])
            i += 2
            continue
        if ch in _COMPOUND_SEPARATORS:
            seg = "".join(cur).strip()
            if seg:
                segs.append(seg)
            cur = []
            i += 1
            continue
        cur.append(ch)
        i += 1
    seg = "".join(cur).strip()
    if seg:
        segs.append(seg)
    return segs


def _extract_substitutions(text):
    """取出 $(...) 与 `...` 里的内层命令文本（数量上限，防构造爆炸）。"""
    out = []
    i = 0
    n = len(text)
    while i < n and len(out) < _SUBST_MAX:
        ch = text[i]
        if ch == "\\" and i + 1 < n:
            i += 2
            continue
        if ch == "$" and i + 1 < n and text[i + 1] == "(":
            depth = 0
            j = i + 1
            while j < n:
                if text[j] == "(":
                    depth += 1
                elif text[j] == ")":
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            if j < n:
                out.append(text[i + 2:j])
                i = j + 1
                continue
            break
        if ch == "`":
            j = i + 1
            while j < n and text[j] != "`":
                if text[j] == "\\":
                    j += 1
                j += 1
            if j < n:
                out.append(text[i + 1:j])
                i = j + 1
                continue
            break
        i += 1
    return out


def _command_segments(cmd, depth=0):
    """展开复合命令与命令替换，返回需要逐段分析的命令文本（去重、保序）。"""
    segs = _split_compound(cmd)
    expanded = list(segs)
    if depth < _SEGMENT_DEPTH:
        for seg in segs:
            for sub in _extract_substitutions(seg):
                expanded += _command_segments(sub, depth + 1)
    out = []
    for seg in expanded:
        if seg and seg not in out:
            out.append(seg)
        if len(out) >= _SEGMENT_MAX:
            break
    return out


# ── argv 级规则（按动词分组）───────────────────────────────────────────────

_RM_VERBS = {"rm", "rmdir", "del", "erase", "unlink", "shred", "remove-item"}
_FORMAT_VERBS = {"mkfs", "mkfs.ext2", "mkfs.ext3", "mkfs.ext4", "mkfs.xfs",
                 "mkfs.btrfs", "mkfs.vfat", "fdisk", "gdisk", "sfdisk",
                 "parted", "wipefs", "diskpart", "format"}
_DD_VERBS = {"dd"}
_POWER_VERBS = {"shutdown", "reboot", "halt", "poweroff", "init"}
_CHMOD_VERBS = {"chmod"}
_CHOWN_VERBS = {"chown"}
_PRIV_VERBS = {"useradd", "userdel", "usermod", "passwd", "chpasswd", "su",
               "visudo", "groupadd", "net"}
_FIREWALL_VERBS = {"iptables", "iptables-restore", "ufw", "firewall-cmd",
                   "nft", "netsh"}
_SERVICE_VERBS = {"systemctl", "service", "sc", "chkconfig", "invoke-rc.d"}
_PERSIST_VERBS = {"crontab", "reg", "schtasks"}
_REVSHELL_VERBS = {"nc", "ncat", "socat"}

_SYSTEM_DIRS = ("/", "/etc", "/usr", "/home", "/boot", "/dev", "/var",
                "/bin", "/sbin", "/lib", "/lib64", "/opt", "/root")


_SYSTEM_PREFIXES = tuple(s + "/" for s in _SYSTEM_DIRS if s != "/")


def _under_system_dir(p):
    """判断路径是否位于某个系统关键目录之下（如 /var/log、/usr/local）。"""
    p = p.replace("\\", "/")
    return p.startswith(_SYSTEM_PREFIXES)


def _flags_in(argv, flags):
    for a in argv:
        low = a.lower()
        if low in flags:
            return True
    return False


def _rm_flags(args):
    recursive = force = False
    for a in args:
        low = a.lower()
        if low == "--recursive":
            recursive = True
        elif low == "--force":
            force = True
        elif re.fullmatch(r"-[a-zA-Z]{1,2}", low):
            body = low[1:]
            if "r" in body:
                recursive = True
            if "f" in body:
                force = True
    return recursive, force


def _analyze_rm(argv):
    recursive, force = _rm_flags(argv[1:])
    if not (recursive or force):
        return []
    targets = [a for a in argv[1:] if not a.startswith("-")]
    if not targets:
        return []
    findings = []
    for t in targets:
        t_clean = t.rstrip("/\\") or t
        if (t_clean in _SYSTEM_DIRS or t_clean == "C:"
                or t_clean.upper().startswith("C:\\WINDOWS") or _is_win_root(t)):
            findings.append(Finding("ARG-RM-SYSTEM", "critical", "command",
                                    "递归删除系统关键路径：%s" % t, 95))
        elif _under_system_dir(t_clean):
            findings.append(Finding("ARG-RM-SYS-SUB", "high", "command",
                                    "递归删除系统目录下路径：%s" % t, 85))
        elif os.path.isabs(t):
            findings.append(Finding("ARG-RM-ABS", "high", "command",
                                    "递归删除项目外绝对路径：%s" % t, 85))
        else:
            findings.append(Finding("ARG-RM-REL", "medium", "command",
                                    "递归删除相对路径目标：%s" % t, 60))
    return findings


def _analyze_format(argv):
    targets = [a for a in argv[1:] if not a.startswith("-")]
    if not targets:
        return []
    findings = []
    for t in targets:
        if re.match(r"^/dev/sd", t) or _is_win_root(t):
            findings.append(Finding("ARG-FMT-DEVICE", "critical", "command",
                                    "格式化块设备/磁盘：%s" % t, 95))
        elif os.path.isabs(t) or len(targets) == 1:
            findings.append(Finding("ARG-FMT-TARGET", "high", "command",
                                    "格式化目标：%s" % t, 80))
    return findings


def _analyze_dd(argv):
    of = None
    for a in argv[1:]:
        if a.startswith("of="):
            of = a[3:]
    if not of:
        return []
    if re.match(r"^/dev/sd", of) or _is_win_root(of) or re.match(r"^[a-zA-Z]:", of):
        return [Finding("ARG-DD-DEVICE", "critical", "command",
                        "dd 直接写入块设备/磁盘：%s" % of, 95)]
    return [Finding("ARG-DD-FILE", "high", "command",
                    "dd 写入磁盘镜像目标：%s" % of, 75)]


def _analyze_power(argv):
    return [Finding("ARG-POWER", "high", "command",
                    "系统电源/重启操作（需人工确认）", 80)]


def _analyze_chmod(argv):
    mode = None
    targets = []
    for a in argv[1:]:
        if re.fullmatch(r"[0-7]{3,4}", a):
            mode = a
        elif not a.startswith("-"):
            targets.append(a)
    if not mode:
        return []
    if mode in ("777", "0777"):
        sev, reason = "high", "chmod 设置全权限位"
        for t in targets:
            if t in _SYSTEM_DIRS or _is_win_root(t):
                sev, reason = "critical", "chmod 对系统关键路径设置全权限"
        return [Finding("ARG-CHMOD-777", sev, "command", reason, 85)]
    if len(mode) == 4 and mode[0] in "12467":
        return [Finding("ARG-CHMOD-SETID", "high", "command",
                        "chmod 设置 setuid / setgid / sticky 权限位", 80)]
    return []


def _analyze_chown(argv):
    recursive = _flags_in(argv[1:], ("-R", "-r", "--recursive"))
    targets = []
    for a in argv[1:]:
        if a.startswith("-") or ":" in a:
            continue
        targets.append(a)
    if not targets:
        return []
    for t in targets:
        if t in _SYSTEM_DIRS or _is_win_root(t):
            return [Finding("ARG-CHOWN-SYSTEM", "critical", "command",
                            "chown 修改系统关键路径属主", 90)]
    if recursive:
        return [Finding("ARG-CHOWN-REC", "medium", "command",
                        "递归修改文件属主（需确认目标）", 55)]
    return []


def _analyze_priv(argv):
    v = argv[0].lower()
    if v == "net":
        low = " ".join(a.lower() for a in argv[1:])
        if "localgroup" in low and "administrators" in low:
            return [Finding("ARG-PRIV-NET", "high", "command",
                            "把用户加入 Windows 管理员组", 88)]
        return []
    if v in ("useradd", "userdel", "groupadd"):
        return [Finding("ARG-PRIV-ACCOUNT", "high", "command",
                        "账户管理操作（需人工确认）", 75)]
    if v == "usermod":
        if _flags_in(argv[1:], ("-aG", "-G", "-a")):
            return [Finding("ARG-PRIV-GROUP", "high", "command",
                            "把用户加入管理员组", 85)]
        return [Finding("ARG-PRIV-ACCOUNT", "high", "command",
                        "账户管理操作（需人工确认）", 70)]
    if v in ("passwd", "chpasswd"):
        return [Finding("ARG-PRIV-PASSWD", "high", "command",
                        "修改账户口令", 80)]
    if v == "su":
        return [Finding("ARG-PRIV-SU", "medium", "command",
                        "切换用户身份（需确认）", 55)]
    if v == "visudo":
        return [Finding("ARG-PRIV-SUDOERS", "high", "command",
                        "编辑 sudoers（提权点）", 85)]
    return []


def _analyze_firewall(argv):
    v = argv[0].lower()
    if v in ("iptables", "iptables-restore"):
        for a in argv[1:]:
            if a in ("-F", "-X", "-Z", "--flush"):
                return [Finding("ARG-FW-FLUSH", "high", "command",
                                "清空防火墙规则", 85)]
        return [Finding("ARG-FW-CHANGE", "medium", "command",
                        "修改防火墙规则（需确认）", 55)]
    if v == "ufw" and any(a in ("disable", "reset") for a in argv[1:]):
        return [Finding("ARG-FW-UFW", "high", "command",
                        "禁用/重置防火墙", 85)]
    if v == "netsh":
        for a in argv[1:]:
            if a.lower().startswith("state=") and a.lower().endswith("off"):
                return [Finding("ARG-FW-NETSH", "high", "command",
                                "关闭 Windows 防火墙", 85)]
    if v in ("firewall-cmd", "nft"):
        return [Finding("ARG-FW-CHANGE", "medium", "command",
                        "修改防火墙规则（需确认）", 55)]
    return []


def _analyze_service(argv):
    v = argv[0].lower()
    if v == "systemctl":
        for a in argv[1:]:
            if a in ("stop", "disable", "mask", "kill"):
                return [Finding("ARG-SVC-STOP", "medium", "command",
                                "停止/禁用系统服务（需确认）", 60)]
            if a in ("start", "enable", "unmask"):
                return [Finding("ARG-SVC-START", "medium", "command",
                                "启用系统服务（需确认）", 55)]
        return []
    if v == "sc":
        for a in argv[1:]:
            if a.lower() in ("delete", "stop"):
                return [Finding("ARG-SVC-SC", "high", "command",
                                "删除/停止 Windows 服务", 80)]
        return []
    if v in ("service", "chkconfig", "invoke-rc.d"):
        for a in argv[1:]:
            if a.lower() in ("stop", "off", "disable", "del"):
                return [Finding("ARG-SVC-STOP", "medium", "command",
                                "停止/禁用系统服务（需确认）", 60)]
    return []


def _analyze_persist(argv):
    v = argv[0].lower()
    if v == "crontab":
        if any(a in ("-e", "-r", "--remove") for a in argv[1:]):
            return [Finding("ARG-CRON", "high", "command",
                            "修改/删除 crontab（持久化）", 85)]
        return []
    if v == "reg":
        low = " ".join(a.lower() for a in argv[1:])
        if any(a in ("add", "delete", "copy") for a in argv[1:]):
            if "run" in low or low.startswith("hklm") or low.startswith("hkcu"):
                return [Finding("ARG-REG-RUN", "high", "command",
                                "修改注册表启动项", 88)]
            return [Finding("ARG-REG", "medium", "command",
                            "修改注册表（需确认）", 60)]
        return []
    if v == "schtasks":
        if any(a.lower() in ("/create", "/delete", "/change") for a in argv[1:]):
            return [Finding("ARG-SCHTASKS", "high", "command",
                            "创建/修改计划任务（持久化）", 85)]
    return []


def _analyze_revshell(argv):
    v = argv[0].lower()
    if v in ("nc", "ncat"):
        for a in argv[1:]:
            if a == "-e" or a.startswith("-e") or a.startswith("--exec"):
                return [Finding("ARG-REV-NC", "critical", "command",
                                "netcat -e 执行（反向 shell）", 95)]
        return []
    if v == "socat":
        for a in argv[1:]:
            low = a.lower()
            if "exec:" in low or low.startswith("system:"):
                return [Finding("ARG-REV-SOCAT", "critical", "command",
                                "socat 执行远程命令（反向 shell）", 90)]
    return []


# ── 可插拔意图验证 ─────────────────────────────────────────────────────────

class HeuristicVerifier:
    """内置本地启发式意图验证器（确定性，不调用任何模型）。

    供 --heuristic 显式启用：对未命中的调用做「高影响动词」复核，
    命中则把结论升级为需人工确认（review）。
    """

    name = "heuristic"
    _confirm = re.compile(
        r"(?i)\b(?:install|uninstall|reinstall|delete|remove|overwrite|reset|"
        r"drop|truncate|purge|cleanup|clear|restart|reboot|shutdown|stop|"
        r"disable|enable|start|upgrade|update|format|wipe)\b"
    )

    def verify(self, req):
        text = " ".join(filter(None, [
            req.get("cmd", ""), req.get("path", ""),
            req.get("content_preview", ""), req.get("target", ""),
        ]))[:2000]
        if self._confirm.search(text):
            return {"verdict": _REVIEW_VERDICT, "severity": "medium",
                    "reason": "操作含需人工确认的高影响动词"}
        return {"verdict": _ALLOW_VERDICT, "severity": "low",
                "reason": "本地启发式未发现需确认信号"}


class ExternalVerifier:
    """外部意图验证器：把请求 JSON 写入命令 stdin，读 stdout JSON 判定。

    协议见 references/intent-verifier.md。命令失败/超时/输出非法时返回 None，
    调用方按「复核」处理，不静默放行也不误杀。
    """

    name = "external"

    def __init__(self, command, timeout=30):
        if isinstance(command, str):
            command = shlex.split(command, posix=(os.name != "nt"))
        self.command = list(command)
        self.timeout = timeout

    def verify(self, req):
        try:
            r = subprocess.run(
                self.command,
                input=json.dumps(req, ensure_ascii=False),
                capture_output=True, text=True, encoding="utf-8",
                errors="replace", timeout=self.timeout, check=False,
            )
        except (OSError, subprocess.TimeoutExpired):
            return None
        try:
            out = json.loads(r.stdout or "{}")
        except ValueError:
            return None
        if not isinstance(out, dict):
            return None
        v = out.get("verdict")
        if v not in (_ALLOW_VERDICT, _DENY_VERDICT, _REVIEW_VERDICT):
            return None
        return out


# ── 审计 ───────────────────────────────────────────────────────────────────

def _audit_id(call, ts_ns):
    h = hashlib.sha1(("%s|%s|%d" % (call.tool, call.describe(), ts_ns))
                     .encode("utf-8")).hexdigest()[:12]
    return h


def _audit_record(call, verdict, policy, ts_ns):
    return {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "id": _audit_id(call, ts_ns),
        "tool": call.tool,
        "action": call.describe(200),
        "verdict": _ALLOW_VERDICT if verdict.allowed else _DENY_VERDICT,
        "allowed": verdict.allowed,
        "severity": verdict.severity,
        "policy": policy,
        "rule_ids": verdict.rule_ids,
        "reason": verdict.reason,
        "verifier": verdict.verifier,
        "cwd": os.getcwd(),
        "exit": verdict.exit_code(),
    }


def audit_append(log_path, record):
    Path(log_path).parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def audit_read(log_path):
    if not Path(log_path).is_file():
        return []
    records = []
    for line in Path(log_path).read_text(encoding="utf-8",
                                         errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            records.append(json.loads(line))
        except ValueError:
            continue
    return records


# ── CLI ────────────────────────────────────────────────────────────────────

def _parse_calls(args):
    if args.batch:
        try:
            data = json.loads(Path(args.batch).read_text(encoding="utf-8"))
        except Exception as e:
            print("错误: 批量文件读取失败: %s (%s)" % (args.batch, e),
                  file=sys.stderr)
            raise SystemExit(4)
        if isinstance(data, dict):
            data = data.get("calls") or []
        if not isinstance(data, list):
            print("错误: 批量文件需为 JSON 数组或 {\"calls\": [...]}",
                  file=sys.stderr)
            raise SystemExit(4)
        calls = []
        for d in data:
            if not isinstance(d, dict):
                print("错误: 批量元素需为对象", file=sys.stderr)
                raise SystemExit(4)
            calls.append(ToolCall(**{
                k: (d.get(k) or "") for k in
                ("tool", "cmd", "path", "content", "old", "new", "target")
            }))
        if not calls:
            print("错误: 批量文件为空", file=sys.stderr)
            raise SystemExit(4)
        return calls
    tool = args.tool or "exec"
    tool = tool.lower()
    if tool not in TOOL_TYPES:
        print("错误: 未知工具类型: %s（可选: %s）"
              % (tool, ", ".join(TOOL_TYPES)), file=sys.stderr)
        raise SystemExit(4)
    return [ToolCall(tool=tool, cmd=args.cmd, path=args.path,
                     content=args.content, old=args.old, new=args.new,
                     target=args.target)]


def _build_verifier(args):
    if args.no_verifier:
        return None
    if args.verifier:
        return ExternalVerifier(args.verifier, args.verifier_timeout)
    if args.heuristic:
        return HeuristicVerifier()
    return None


def _print_check_text(call, verdict, color):
    def c(s, code):
        # 2026-09-28：原写法只有 1 个 %s 却喂了 2 个参数 → 彩色路径（真人终端）必崩 TypeError。
        return "\033[%sm%s\033[0m" % (code, s) if color else s
    kind = c("DENY", "31;1") if not verdict.allowed else c("ALLOW", "32;1")
    sev = verdict.severity.upper()
    print("[检查]  %s" % call.describe(300))
    print("[判定]  %s (%s)" % (kind, sev))
    print("[原因]  %s" % verdict.reason)
    for f in verdict.findings:
        print("[规则]  %s · %s · %s"
              % (f.rule_id, f.severity.upper(), f.reason))
    if verdict.verifier:
        print("[验证]  %s" % json.dumps(verdict.verifier,
                                        ensure_ascii=False))
    print("")


def _cmd_check(args):
    engine = RuleEngine(policy=args.policy or "default",
                        allow_patterns=args.allow,
                        allow_paths=args.allow_path,
                        config_path=args.config,
                        cwd=args.cwd,
                        verifier=_build_verifier(args))
    calls = _parse_calls(args)
    color = (not args.no_color) and sys.stdout.isatty()
    results = []
    for call in calls:
        verdict = engine.evaluate(call)
        results.append((call, verdict))
    if args.audit_log:
        for call, verdict in results:
            audit_append(args.audit_log,
                         _audit_record(call, verdict, engine.policy,
                                       time.time_ns()))
    exit_code = max((v.exit_code() for _, v in results), default=0)
    if args.json:
        payload = {
            "tool": TOOL_NAME, "version": VERSION, "policy": engine.policy,
            "summary": {
                "calls": len(results),
                "allowed": sum(1 for _, v in results if v.allowed),
                "denied": sum(1 for _, v in results if not v.allowed),
                "exit": exit_code,
            },
            "results": [
                {"call": c.to_dict(), **v.to_dict()} for c, v in results
            ],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    elif args.report:
        _write_report(args.report, results, engine.policy)
    else:
        for call, verdict in results:
            _print_check_text(call, verdict, color)
    raise SystemExit(exit_code)


def _write_report(path, results, policy):
    lines = ["# 元盾安全检查报告（yotta-guardian）", "",
             "- 生成时间：%s" % datetime.now(timezone.utc)
             .isoformat(timespec="seconds"),
             "- 策略：%s" % policy, "",
             "| # | 工具 | 动作 | 判定 | 严重级 | 原因 |",
             "|---|------|------|------|--------|------|"]
    for i, (call, verdict) in enumerate(results, 1):
        lines.append("| %d | %s | %s | %s | %s | %s |"
                     % (i, call.tool, call.describe(80),
                        "允许" if verdict.allowed else "拒绝",
                        verdict.severity.upper(),
                        verdict.reason.replace("|", "/")))
    lines += ["", "## 命中规则明细", ""]
    for call, verdict in results:
        if not verdict.findings:
            continue
        lines += ["### %s：%s" % (call.tool, call.describe(80)), ""]
        for f in verdict.findings:
            lines.append("- %s [%s] %s"
                         % (f.rule_id, f.severity.upper(), f.reason))
        lines.append("")
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("报告已写入: %s" % path)


def _cmd_audit(args):
    log = args.file or os.environ.get("YOTTA_GUARDIAN_AUDIT")
    if not log:
        print("错误: 请用 --file 指定审计日志（或设置 YOTTA_GUARDIAN_AUDIT）",
              file=sys.stderr)
        raise SystemExit(4)
    records = audit_read(log)
    if args.denied:
        records = [r for r in records if not r.get("allowed", True)]
    if args.tool:
        records = [r for r in records if r.get("tool") == args.tool]
    if args.since:
        records = [r for r in records if r.get("ts", "") >= args.since]
    if args.tail:
        records = records[-args.tail:]
    if args.json:
        print(json.dumps(records, ensure_ascii=False, indent=2))
    else:
        if not records:
            print("审计日志为空: %s" % log)
        for r in records:
            print("%s  %s  %s  %s(%s)  %s"
                  % (r.get("ts", ""), r.get("id", ""), r.get("verdict", ""),
                     r.get("severity", ""), r.get("policy", ""),
                     r.get("action", "")))
    raise SystemExit(0)


def _cmd_rules(args):
    if args.config:
        engine = RuleEngine(config_path=args.config, cwd=args.cwd)
        print("自定义规则文件校验通过: %s" % args.config)
        print("策略: %s | 放行模式 %d 条 | 放行路径 %d 条 | 自定义拒绝 %d 条"
              % (engine.policy, len(engine.allow_patterns),
                 len(engine.allow_paths), len(engine.custom_deny)))
        raise SystemExit(0)
    counts = {}
    for r in GR.TEXT_PATTERNS:
        counts[r.severity] = counts.get(r.severity, 0) + 1
    path_counts = {}
    for r in GR.PATH_PATTERNS:
        path_counts[r.severity] = path_counts.get(r.severity, 0) + 1
    if args.json:
        print(json.dumps({
            "tool": TOOL_NAME, "version": VERSION,
            "text_patterns": len(GR.TEXT_PATTERNS),
            "path_patterns": len(GR.PATH_PATTERNS),
            "allow_patterns": len(GR.ALLOW_PATTERNS),
            "text_by_severity": counts,
            "path_by_severity": path_counts,
        }, ensure_ascii=False, indent=2))
    else:
        print("%s %s 规则摘要" % (TOOL_CN, TOOL_NAME))
        print("文本规则: %d 条 %s" % (len(GR.TEXT_PATTERNS), counts))
        print("路径规则: %d 条 %s" % (len(GR.PATH_PATTERNS), path_counts))
        print("默认放行模式: %d 条" % len(GR.ALLOW_PATTERNS))
    raise SystemExit(0)


def _cmd_version(_args):
    print("%s %s（%s）" % (TOOL_NAME, VERSION, TOOL_CN))


def _build_parser():
    ap = argparse.ArgumentParser(
        prog=TOOL_NAME,
        description="元盾 yotta-guardian：确定性规则引擎 + 可插拔意图验证的"
                    "工具调用拦截护栏")
    sub = ap.add_subparsers(dest="command")

    p_check = sub.add_parser("check", help="评估工具调用安全性")
    p_check.add_argument("tool", nargs="?", default=None,
                         help="工具类型: exec/run/shell/write/edit/read")
    p_check.add_argument("--cmd", default="", help="命令文本（exec/run/shell）")
    p_check.add_argument("--path", default="", help="目标路径（write/edit/read）")
    p_check.add_argument("--content", default="", help="写入内容（write/edit）")
    p_check.add_argument("--old", default="", help="编辑前内容（edit）")
    p_check.add_argument("--new", default="", help="编辑后内容（edit）")
    p_check.add_argument("--target", default="", help="通用目标描述")
    p_check.add_argument("--batch", default="", help="批量 JSON 文件")
    p_check.add_argument("--policy", default="default",
                         choices=("default", "strict", "loose"))
    p_check.add_argument("--allow", action="append", default=None,
                         help="追加放行模式（可重复）")
    p_check.add_argument("--allow-path", dest="allow_path", action="append",
                         default=None, help="追加放行路径前缀（可重复）")
    p_check.add_argument("--config", default="", help="自定义规则 JSON 文件")
    p_check.add_argument("--heuristic", action="store_true",
                         help="启用内置启发式意图验证")
    p_check.add_argument("--verifier", default="",
                         help="外部意图验证命令（如 python3 verify.py）")
    p_check.add_argument("--verifier-timeout", dest="verifier_timeout",
                         type=int, default=30)
    p_check.add_argument("--no-verifier", action="store_true",
                         help="禁用意图验证")
    p_check.add_argument("--audit-log", dest="audit_log", default="",
                         help="审计日志 JSONL 路径")
    p_check.add_argument("--json", action="store_true",
                         help="输出 JSON（stdout 纯净）")
    p_check.add_argument("--report", default="", help="输出 Markdown 报告")
    p_check.add_argument("--cwd", default="", help="工作目录（路径上下文）")
    p_check.add_argument("--no-color", action="store_true",
                         help="禁用颜色输出")

    p_audit = sub.add_parser("audit", help="查询审计日志")
    p_audit.add_argument("--file", default="", help="审计日志 JSONL 路径")
    p_audit.add_argument("--tail", type=int, default=0)
    p_audit.add_argument("--denied", action="store_true")
    p_audit.add_argument("--since", default="")
    p_audit.add_argument("--tool", default="")
    p_audit.add_argument("--json", action="store_true")

    p_rules = sub.add_parser("rules", help="规则摘要 / 校验自定义规则")
    p_rules.add_argument("--config", default="")
    p_rules.add_argument("--cwd", default="")
    p_rules.add_argument("--json", action="store_true")

    sub.add_parser("version", help="打印版本")
    return ap


def main(argv=None):
    ap = _build_parser()
    try:
        args = ap.parse_args(argv)
    except SystemExit as e:
        if e.code == 2:
            raise SystemExit(4)
        raise
    if not args.command:
        ap.print_help()
        raise SystemExit(4)
    if args.command == "check":
        _cmd_check(args)
    elif args.command == "audit":
        _cmd_audit(args)
    elif args.command == "rules":
        _cmd_rules(args)
    elif args.command == "version":
        _cmd_version(args)
    else:
        ap.print_help()
        raise SystemExit(4)


if __name__ == "__main__":
    # 顶层兜底（2026-09-28）：未捕获异常一律按「致命异常」退出码 4 结束。
    # 绝不能让引擎崩溃落到 1 —— 契约里 1 = 允许但带警告，按退出码判定的宿主会把
    # 「护栏没跑起来」读成放行（fail-open）。SystemExit / KeyboardInterrupt 原样透传。
    try:
        main()
    except (SystemExit, KeyboardInterrupt):
        raise
    except BaseException as exc:  # 兜底就是要 catch-all
        try:
            sys.stderr.write("致命异常: %s: %s\n" % (type(exc).__name__, exc))
        except Exception:
            pass
        raise SystemExit(4)
