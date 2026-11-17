#!/usr/bin/env python3
"""
release_gate.py — 发布前放行门禁：公开面敏感信息判定引擎

与常规密钥扫描器的根本区别：**判定对象是「公开面」，不是工作目录**。

对 git 仓库而言，别人能看到的是：
  1. 被 git 追踪的文件（未追踪 / 已gitignore 的本地文件不算）
  2. 全部提交历史（当前删掉了，旧 commit 里依然公开）
这两者与`ls` 看到的内容差别极大。只扫工作树会同时犯两种错：
把本地噪音误报成泄露，又漏掉历史里真实存在的密钥。

四类威胁分离（后果与修法都不同）：
  CREDENTIAL   凭证密钥        → 必须吊销，删除不等于修复
  ORG_INTERNAL 雇主内部信息    → 泛化或移除
  PII          个人身份/机器指纹 → 同时也是可移植性缺陷
  LOCAL_ONLY   本地专属产物    → 确认已 gitignore 且未被追踪

用法：
    python3 release_gate.py <目标路径> [选项]

    --mode {public,worktree,history,all}
                public   仅判定公开面（git 已追踪 + 历史）【默认】
                     worktree 仅扫工作目录（含未追踪文件）
                     history  仅扫提交历史
                     all      三者都跑
    --org-config <path>   内部词表配置文件（YAML 风格的简单键值，见 assets/）
    --format {text,json}  输出格式
    --severity {P0,P1,P2} 最低报告级别，默认 P1
    --baseline <path>     基线文件，用于整改前后对比

退出码：0 = 可放行；1 = 存在 P0 阻断项；2 = 用法错误；3 = 环境不满足

设计约束：内部词表**绝不硬编码在本文件中**，一律外部注入。否则这个脚本
本身就带着雇主信息，无法作为开源产物发布——审查工具必须自己先过审。
"""

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path


# ─── 严重级别────────────────────────────────────────────────────
# P0 = 阻断发布；P1 = 必须人工判定；P2 = 提示
SEVERITIES = ("P0", "P1", "P2")

# 哪些 surface 构成「公开面」——只有落在公开面的 P0 才阻断发布。
#   tracked  被 git 追踪的文件（别人 clone 即可见）
#   history  提交历史（当前删了也照样公开）
#   worktree 非公开面判定模式下的工作目录内容
#   file     目标不是 git 仓库时的退化模式，无法区分公开性，保守视为公开
# untracked 不在此列：未被追踪的本地文件尚未公开，仅作提示。
BLOCKING_SURFACES = ("tracked", "history", "worktree", "file")

SURFACE_LABEL = {
    "tracked": "已追踪", "history": "历史",
    "untracked": "未追踪", "worktree": "工作树", "file": "文件",
}


@dataclass
class Pattern:
    category: str
    severity: str
    regex: str
    desc: str


@dataclass
class Finding:
    category: str
    severity: str
    desc: str
    location: str      # 文件路径，或 "commit:<sha>"
    line: int
    snippet: str
    surface: str       # tracked / untracked / history

    def key(self):
        return (self.category, self.location, self.line, self.desc)


# ─── 内置模式（仅通用、公开可查的凭证格式，不含任何雇主特定内容）───
BUILTIN_PATTERNS = [
    # 凭证：一旦泄露即需吊销
    Pattern("CREDENTIAL", "P0", r"github_pat_[A-Za-z0-9_]{20,}", "GitHub 细粒度 PAT"),
    Pattern("CREDENTIAL", "P0", r"\bghp_[A-Za-z0-9]{30,}", "GitHub classic token"),
    Pattern("CREDENTIAL", "P0", r"\bghu_[A-Za-z0-9]{30,}", "GitHub user-to-server token"),
    Pattern("CREDENTIAL", "P0", r"\bgho_[A-Za-z0-9]{30,}", "GitHub OAuth token"),
    Pattern("CREDENTIAL", "P0", r"\bghr_[A-Za-z0-9]{30,}", "GitHub refresh token"),
    Pattern("CREDENTIAL", "P0", r"\bsk-[A-Za-z0-9]{20,}", "OpenAI 风格密钥"),
    Pattern("CREDENTIAL", "P0", r"\bsk-ant-[A-Za-z0-9\-_]{20,}", "Anthropic API key"),
    Pattern("CREDENTIAL", "P0", r"AKIA[0-9A-Z]{16}", "AWS Access Key ID"),
    Pattern("CREDENTIAL", "P0", r"AKID[A-Za-z0-9]{13,}", "Tencent Cloud SecretId"),
    Pattern("CREDENTIAL", "P0", r"LTAI[A-Za-z0-9]{12,}", "Alibaba Cloud AccessKey"),
    Pattern("CREDENTIAL", "P0", r"AIza[A-Za-z0-9_\-]{30,}", "Google API Key"),
    Pattern("CREDENTIAL", "P0", r"xox[baprs]-[A-Za-z0-9\-]{10,}", "Slack token"),
    Pattern("CREDENTIAL", "P0", r"sk_live_[0-9a-zA-Z]{20,}", "Stripe 生产密钥"),
    Pattern("CREDENTIAL", "P0", r"SG\.[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]{20,}", "SendGrid API Key"),
    Pattern("CREDENTIAL", "P0", r"npm_[A-Za-z0-9]{30,}", "npm token"),
    Pattern("CREDENTIAL", "P0", r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "私钥块"),
    Pattern("CREDENTIAL", "P0", r"eyJ[A-Za-z0-9_\-]{10,}\.eyJ[A-Za-z0-9_\-]{10,}\.", "含payload 的 JWT"),
    Pattern("CREDENTIAL", "P0",
            r"(?i)\b(?:api[_-]?key|secret|token|password|passwd)\s*[=:]\s*['\"][^'\"\s${}<>]{12,}['\"]",
            "硬编码密钥赋值"),
    Pattern("CREDENTIAL", "P0",
            r"(?i)(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis)://[^:\s]+:[^@\s]{6,}@",
            "含内联密码的数据库连接串"),

    # 内网线索（通用形态，不含具体公司域名）
    Pattern("ORG_INTERNAL", "P1",
            r"\b(?:10\.\d{1,3}|192\.168|172\.(?:1[6-9]|2\d|3[01]))\.\d{1,3}\.\d{1,3}\b",
            "内网 IP 地址"),
    Pattern("ORG_INTERNAL", "P1",
            r"(?i)\b[a-z0-9\-]+\.(?:internal|intra|corp|lan)\b",
            "疑似内网主机名"),

    # 个人身份 / 机器指纹
    Pattern("PII", "P1", r"/Users/[a-z0-9_\-\.]+/", "macOS 绝对家目录（泄露用户名）"),
    Pattern("PII", "P1", r"/home/[a-z0-9_\-\.]+/", "Linux 绝对家目录（泄露用户名）"),
    Pattern("PII", "P1", r"C:\\Users\\[A-Za-z0-9_\-\. ]+", "Windows 绝对家目录"),
    Pattern("PII", "P1", r"\b1[3-9]\d{9}\b", "疑似手机号"),
    Pattern("PII", "P2",
            r"[A-Za-z0-9._%+\-]+@(?!example\.(?:com|org|net)|test\.com|localhost)[A-Za-z0-9.\-]+\.[A-Za-z]{2,}",
            "邮箱地址"),
]

# 本地专属产物：只有出现在「已追踪」里才是问题。
# 这类目录躺在本地完全正常，被 git 追踪才进入公开面。
# 需要补充自己环境的目录时，可在 --org-config 里追加，或直接扩展本列表。
LOCAL_ONLY_HINTS = [
    # AI/agent 工具的本地状态目录（各家命名不同，按需增删）
    ".agent/", ".ai/", ".assistant/",
    # 编辑器/IDE 个人配置
    ".vscode/", ".idea/", ".fleet/",
    # 系统与本地缓存
    ".DS_Store", "Thumbs.db", "*.local.json", "*.local.yml",
    # 本地笔记/草稿
    "scratch/", "notes-local/",
]

SKIP_DIRS = {".git", "node_modules", "dist", "build", ".pnpm", "__pycache__",
             ".venv", "venv", ".next", "coverage", ".turbo", ".gradle", "target"}
SKIP_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", ".zip",
            ".woff", ".woff2", ".ttf", ".otf", ".mp4", ".webm", ".mp3",
            ".so", ".dylib", ".dll", ".wasm", ".pyc", ".class", ".jar"}

# 本工具自己产出的中间报告：里面必然复述着命中的原文片段，
# 再扫一遍只会产生自我污染的噪音（同一条泄露被报两次：一次在源文件，
# 一次在报告里）。按文件名兜底跳过，不依赖用户是否配了 .gitignore。
SELF_OUTPUT_NAMES = {"before.json", "after.json"}
SELF_OUTPUT_SUFFIXES = (".report.json", "-report.json", ".gate.json")

# 常见误报特征：命中后降级提示，但绝不自动丢弃
FALSE_POSITIVE_HINTS = [
    "example", "EXAMPLE", "sample", "dummy", "placeholder", "your_", "YOUR_",
    "changeme", "change-me", "xxx", "XXX", "<", "${", "test-", "fake",
    "localhost", "127.0.0.1", "TODO", "REDACTED", "***",
]

# 路径维度的误报信号：比字面特征更可靠。
# 单测里的 apiKey:"secret-token" 字面上看不出是假的，但它在 test/ 下、
# 配 mock 使用，就是典型的固定装置（fixture）。示例/模板同理。
FALSE_POSITIVE_PATH_HINTS = [
    "/test/", "/tests/", "/__tests__/", "/spec/", "/fixtures/", "/mocks/",
    "/examples/", "/example/", "/samples/", "/demo/", "/docs/",
    ".test.", ".spec.", "_test.", "test_", ".example", ".sample", ".template",
]


def load_org_patterns(config_path):
    """从外部配置加载组织自定义词条。绝不内置。

    配置文件格式（每行一条，# 为注释）：

        internal.example.com                # 默认归为 ORG_INTERNAL
        SomeInternalPlatform
        cred:MYCO-                # 显式指定类别为凭证
        credential:svc_tok_                 # 同上，全称也可
        regex:MYCO-[A-Za-z0-9]{16}          # 按正则匹配而非字面
        cred+regex:INT-[0-9a-f]{32}         # 两个修饰可组合

    可选前缀（不写就是 ORG_INTERNAL + 字面匹配，向后兼容）：
      cred / credential  → 归类为 CREDENTIAL，处置动作变成「吊销并轮换」
      regex→ 该条按正则处理，用于自研凭证的格式匹配

    也支持 ORG_PATTERNS 环境变量（逗号分隔），与配置文件合并。
    """
    terms = []
    if config_path:
        p = Path(config_path)
        if not p.exists():
            print(f"[!] 内部词表配置不存在: {config_path}", file=sys.stderr)
        else:
            for raw in p.read_text(encoding="utf-8").splitlines():
                line = raw.strip()
                if line and not line.startswith("#"):
                    terms.append(line)
    env = os.environ.get("ORG_PATTERNS", "").strip()
    terms += [t.strip() for t in env.split(",") if t.strip()]

    out = []
    for raw in dict.fromkeys(terms):        # 去重且保序
        category, as_regex, body = "ORG_INTERNAL", False, raw
        if ":" in raw:
            head, rest = raw.split(":", 1)
            mods = {m.strip().lower() for m in head.split("+")}
            known = {"cred", "credential", "regex"}
            # 只有修饰词全部可识别时才当作前缀，避免把
            # "https://x" 或 "host:port" 这类字面内容误解析
            if mods and mods <= known and rest.strip():
                body = rest.strip()
                if mods & {"cred", "credential"}:
                    category = "CREDENTIAL"
                as_regex = "regex" in mods

        if as_regex:
            try:
                re.compile(body)
            except re.error as e:
                print(f"[!] 跳过无效正则词条 {raw!r}: {e}", file=sys.stderr)
                continue
            rx = body
        else:
            rx = "(?i)" + re.escape(body)

        label = "组织自定义凭证" if category == "CREDENTIAL" else "雇主内部标识"
        out.append(Pattern(category, "P0", rx, f"{label}: {body}"))
    return out


# ─── git 交互 ────────────────────────────────────────────────────
def run_git(args, cwd):
    try:
        r = subprocess.run(["git"] + args, cwd=cwd, capture_output=True,
                           text=True, timeout=120)
        return r.returncode, r.stdout, r.stderr
    except FileNotFoundError:
        return 127, "", "git 未安装"
    except subprocess.TimeoutExpired:
        return 124, "", "git 命令超时"


def is_git_repo(path):
    code, out, _ = run_git(["rev-parse", "--is-inside-work-tree"], path)
    return code == 0 and out.strip() == "true"


def tracked_files(path):
    code, out, _ = run_git(["ls-files"], path)
    if code != 0:
        return []
    return [l for l in out.splitlines() if l.strip()]


def untracked_files(path):
    code, out, _ = run_git(["ls-files", "--others", "--exclude-standard"], path)
    if code != 0:
        return []
    return [l for l in out.splitlines() if l.strip()]


# ─── 扫描 ────────────────────────────────────────────────────────
def looks_like_false_positive(snippet, location=""):
    """两个维度判定疑似误报：内容字面特征 + 所在路径性质。

    只用于「标注提示」，绝不自动丢弃——判定权始终在人手上。
    """
    low = snippet.lower()
    if any(h.lower() in low for h in FALSE_POSITIVE_HINTS):
        return True
    loc = location.lower().replace("\\", "/")
    if loc and not loc.startswith("commit:"):
        if any(h in loc for h in FALSE_POSITIVE_PATH_HINTS):
            return True
    return False


def scan_text(text, patterns, location, surface, min_sev):
    findings = []
    order = {s: i for i, s in enumerate(SEVERITIES)}
    limit = order[min_sev]
    for i, line in enumerate(text.splitlines(), 1):
        if len(line) > 4000:            # 压缩产物/长base64，跳过避免误报风暴
            continue
        for p in patterns:
            if order[p.severity] > limit:
                continue
            for m in re.finditer(p.regex, line):
                snip = line.strip()
                if len(snip) > 160:
                    s = max(0, m.start() - 50)
                    snip = "..." + snip[s:m.end() + 60] + "..."
                findings.append(Finding(p.category, p.severity, p.desc,
                                        location, i, snip, surface))
    return findings


def should_skip(rel_path, extra_skip=()):
    """extra_skip 用于排除审查产物自身。

    基线文件天然含有它所豁免的那些片段（记录了什么就含有什么），
    报告文件同理。不排除的话每次扫描都会命中自己的产物，
    形成永远清不掉的循环噪音。
    """
    norm = str(rel_path).replace("\\", "/")
    for pat in extra_skip:
        if pat and (norm == pat or norm.endswith("/" + pat) or pat in norm):
            return True
    parts = Path(rel_path).parts
    if any(d in SKIP_DIRS for d in parts):
        return True
    name = parts[-1] if parts else norm
    if name in SELF_OUTPUT_NAMES or name.endswith(SELF_OUTPUT_SUFFIXES):
        return True
    return Path(rel_path).suffix.lower() in SKIP_EXT


def scan_paths(base, rel_paths, patterns, surface, min_sev, extra_skip=()):
    findings = []
    for rel in rel_paths:
        if should_skip(rel, extra_skip):
            continue
        fp = Path(base) / rel
        if not fp.is_file():
            continue
        try:
            text = fp.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        findings += scan_text(text, patterns, rel, surface, min_sev)
    return findings


def scan_history(base, patterns, min_sev, max_commits=0):
    """扫全部提交的diff 内容。当前文件已清理，旧 commit 仍是公开的。"""
    args = ["log", "--all", "-p", "--no-color", "--no-merges"]
    if max_commits:
        args.insert(2, f"-{max_commits}")
    code, out, err = run_git(args, base)
    if code != 0:
        print(f"[!] 读取 git 历史失败: {err.strip()}", file=sys.stderr)
        return []

    findings = []
    order = {s: i for i, s in enumerate(SEVERITIES)}
    limit = order[min_sev]
    commit = "unknown"
    skip_file = False
    # 历史里只关心凭证与雇主内部信息——PII 路径在历史里价值低、噪音高
    hist_pats = [p for p in patterns if p.category in ("CREDENTIAL", "ORG_INTERNAL")]

    for line in out.splitlines():
        if line.startswith("commit "):
            commit = line.split()[1][:12]
            continue
        # 跟踪 diff 当前所属文件，用于跳过本工具自己产出的中间报告
        # （报告里复述了命中原文，会把同一条泄露重复报一遍）
        if line.startswith("+++ "):
            path = line[4:].strip()
            if path.startswith("b/"):
                path = path[2:]
            name = path.rsplit("/", 1)[-1]
            skip_file = (name in SELF_OUTPUT_NAMES
                         or name.endswith(SELF_OUTPUT_SUFFIXES))
            continue
        if skip_file:
            continue
        if not line.startswith("+") or line.startswith("+++"):
            continue
        content = line[1:]
        for p in hist_pats:
            if order[p.severity] > limit:
                continue
            for m in re.finditer(p.regex, content):
                snip = content.strip()
                if len(snip) > 160:
                    s = max(0, m.start() - 50)
                    snip = "..." + snip[s:m.end() + 60] + "..."
                findings.append(Finding(p.category, p.severity, p.desc,
                                        f"commit:{commit}", 0, snip, "history"))
    return findings


def check_local_only(base, tracked):
    """本地专属产物若被 git 追踪 → 真问题。"""
    out = []
    for rel in tracked:
        for hint in LOCAL_ONLY_HINTS:
            h = hint.rstrip("/").lstrip("*")
            if h and h in rel:
                out.append(Finding("LOCAL_ONLY", "P1",
                                   f"本地专属产物被 git 追踪（应gitignore）: {hint}",
                                   rel, 0, rel, "tracked"))
                break
    return out


# ─── 输出 ────────────────────────────────────────────────────────
CATEGORY_ACTION = {
    "CREDENTIAL":   "吊销并轮换凭证（删除不等于修复），再清理 git 历史",
    "ORG_INTERNAL": "泛化为通用示例或直接移除（保留结论，去掉标识）",
    "PII":          "改为相对路径 / 环境变量 /裸包名（同时修掉可移植性问题）",
    "LOCAL_ONLY":   "加入 .gitignore 并 git rm --cached 停止追踪",
}


def report_text(findings, meta):
    RESET, BOLD, RED, YEL, CYA, GRN = "\033[0m", "\033[1m", "\033[31m", "\033[33m", "\033[36m", "\033[32m"
    if not sys.stdout.isatty():
        RESET = BOLD = RED = YEL = CYA = GRN = ""

    print(f"{BOLD}发布前放行门禁 — 公开面审查{RESET}")
    print("=" * 68)
    print(f"目标        : {meta['target']}")
    print(f"git 仓库    : {'是' if meta['is_git'] else '否（退化为目录扫描）'}")
    print(f"判定范围    : {meta['mode']}")
    print(f"已追踪文件  : {meta['tracked_count']}")
    if meta["is_git"] and meta["mode"] in ("public", "all"):
        print(f"未追踪文件  : {meta['untracked_count']}（不属于公开面，仅提示）")
    print(f"生效模式数: {meta['pattern_count']}（含外部注入内部词 {meta['org_count']} 条）")
    print("=" * 68)

    if not findings:
        print(f"\n{GRN}未发现任何命中。{RESET}")
    else:
        buckets = {}
        for f in findings:
            buckets.setdefault((f.severity, f.category), []).append(f)
        for sev in SEVERITIES:
            for cat in ("CREDENTIAL", "ORG_INTERNAL", "PII", "LOCAL_ONLY"):
                fs = buckets.get((sev, cat))
                if not fs:
                    continue
                color = RED if sev == "P0" else (YEL if sev == "P1" else CYA)
                print(f"\n{color}{BOLD}[{sev}] {cat}{RESET} — {len(fs)} 项")
                print(f"  处置：{CATEGORY_ACTION.get(cat, '人工判定')}")
                for f in fs[:40]:
                    tag = SURFACE_LABEL.get(f.surface, f.surface)
                    loc = f"{f.location}:{f.line}" if f.line else f.location
                    warn = "  <- 疑似误报，需读上下文" if looks_like_false_positive(f.snippet, f.location) else ""
                    print(f"    · [{tag}] {loc}  {f.desc}{warn}")
                    print(f"      > {f.snippet}")
                if len(fs) > 40:
                    print(f"    ... 另有 {len(fs) - 40} 项，用 --format json 查看全部")

    counts = meta["counts"]
    print("\n" + "=" * 68)
    print(f"合计  P0={counts['P0']}  P1={counts['P1']}  P2={counts['P2']}")
    blocking = [f for f in findings if f.severity == "P0" and f.surface in BLOCKING_SURFACES]
    if blocking:
        suspect = [f for f in blocking if looks_like_false_positive(f.snippet, f.location)]
        print(f"\n{RED}{BOLD}裁决：待人工确认{RESET} — 公开面存在 {len(blocking)} 项 P0")
        if suspect:
            print(f"  其中 {len(suspect)} 项已标注为疑似误报"
                  f"（测试/示例路径或占位符特征），{len(blocking) - len(suspect)} 项无此特征。")
        print("  正则只能高召回，工具不代替你下结论。请逐条读上下文：厂商文档示例串")
        print("  （如 REDACTED-SECRET）、localhost 测试凭证、${VAR} 插值都是常见误报。")
        print("  确认为误报的写入基线文件（--baseline），不要放宽规则。")
        print("  确认为真实泄露的：先吊销，再删代码，再清历史——顺序不能颠倒。")
    elif counts["P0"]:
        print(f"\n{YEL}{BOLD}裁决：可发布（有条件）{RESET} — P0 命中均不在公开面（未追踪文件）")
        print("  请确认这些文件确实已被 .gitignore 排除。")
    else:
        print(f"\n{GRN}{BOLD}裁决：可发布{RESET} — 公开面无 P0 命中")
        if counts["P1"]:
            print(f"  仍有 {counts['P1']} 项 P1 建议人工过一遍。")


def report_json(findings, meta):
    print(json.dumps({
        "meta": meta,
        "findings": [
            {"category": f.category, "severity": f.severity, "desc": f.desc,
             "location": f.location, "line": f.line, "snippet": f.snippet,
             "surface": f.surface,
             "possible_false_positive": looks_like_false_positive(f.snippet, f.location)}
            for f in findings
        ],
    }, ensure_ascii=False, indent=2))


def load_baseline(path):
    if not path or not Path(path).exists():
        return set()
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return {tuple(x) for x in data.get("accepted", [])}
    except Exception as e:
        print(f"[!] 基线文件解析失败: {e}", file=sys.stderr)
        return set()


def main():
    ap = argparse.ArgumentParser(
        description="发布前放行门禁：以git 公开面为判定对象的敏感信息审查")
    ap.add_argument("target", help="目标目录")
    ap.add_argument("--mode", choices=["public", "worktree", "history", "all"],
                    default="public")
    ap.add_argument("--org-config", help="雇主内部词表配置文件路径")
    ap.add_argument("--format", choices=["text", "json"], default="text")
    ap.add_argument("--severity", choices=list(SEVERITIES), default="P1")
    ap.add_argument("--baseline", help="已确认误报的基线文件（JSON）")
    ap.add_argument("--max-commits", type=int, default=0,
                    help="限制历史扫描的提交数（0=全部）")
    args = ap.parse_args()

    base = os.path.abspath(args.target)
    if not os.path.isdir(base):
        print(f"错误：目标目录不存在: {base}", file=sys.stderr)
        return 2

    org_patterns = load_org_patterns(args.org_config)
    patterns = BUILTIN_PATTERNS + org_patterns
    org_count = len(org_patterns)
    git_ok = is_git_repo(base)

    # 排除审查工作自身的产物：基线文件与内部词表文件天然含有敏感片段
    extra_skip = []
    for p in (args.baseline, args.org_config):
        if p:
            try:
                rel = os.path.relpath(os.path.abspath(p), base)
                if not rel.startswith(".."):
                    extra_skip.append(rel.replace("\\", "/"))
            except ValueError:
                pass

    tracked, untracked = [], []
    findings = []
    # 非 git 目录时，"公开面"概念不成立，所有文件同等对待。
    # 用独立标记避免把普通文件伪装成"已追踪"从而误导裁决。
    plain_files = []

    if git_ok:
        tracked = tracked_files(base)
        untracked = untracked_files(base)
    else:
        if args.mode in ("public", "history", "all"):
            print("[!] 目标不是 git 仓库，公开面/历史判定不可用，退化为目录扫描。",
                  file=sys.stderr)
        for root, dirs, names in os.walk(base):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for n in names:
                plain_files.append(os.path.relpath(os.path.join(root, n), base))

    if not git_ok:
        # 退化模式：无论用户选哪个 mode，都扫全部文件。
        # 否则 worktree 模式会因为列表为空而扫不到任何东西，
        # 报出"未发现命中"的假绿灯——这比漏报更危险。
        findings += scan_paths(base, plain_files, patterns, "file", args.severity, extra_skip)
    else:
        if args.mode in ("public", "all"):
            findings += scan_paths(base, tracked, patterns, "tracked", args.severity, extra_skip)
            findings += check_local_only(base, tracked)
        if args.mode in ("worktree", "all"):
            # worktree 模式应覆盖工作目录的全部内容（已追踪 + 未追踪）
            targets = untracked if args.mode == "all" else tracked + untracked
            surface = "untracked" if args.mode == "all" else "worktree"
            findings += scan_paths(base, targets, patterns, surface, args.severity, extra_skip)
        if args.mode in ("public", "history", "all"):
            findings += scan_history(base, patterns, args.severity, args.max_commits)

    # 基线过滤：只排除明确确认过的误报
    baseline = load_baseline(args.baseline)
    if baseline:
        findings = [f for f in findings if f.key() not in baseline]

    counts = {s: sum(1 for f in findings if f.severity == s) for s in SEVERITIES}
    meta = {
        "target": base,
        "is_git": git_ok,
        "mode": args.mode,
        "tracked_count": len(tracked) if git_ok else len(plain_files),
        "untracked_count": len(untracked),
        "pattern_count": len(patterns),
        "org_count": org_count,
        "counts": counts,
    }

    if args.format == "json":
        report_json(findings, meta)
    else:
        report_text(findings, meta)

    blocking = [f for f in findings
                if f.severity == "P0" and f.surface in BLOCKING_SURFACES]
    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
