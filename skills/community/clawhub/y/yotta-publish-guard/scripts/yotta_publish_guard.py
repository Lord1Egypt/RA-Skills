#!/usr/bin/env python3
"""yotta-publish-guard: 发布前守门 —— 聚合校验 / 版本五件对齐 / npm pack 检查 /
名称三通道查重 / 三源发布命令封装（元阁「工坊」发布守门）。

零依赖（Python 3.8+ 标准库）。用法:
  python3 scripts/yotta_publish_guard.py check <skill-dir> [--with-audit --with-vetter --with-verify]
  python3 scripts/yotta_publish_guard.py pack <skill-dir>          # npm pack --dry-run 检查
  python3 scripts/yotta_publish_guard.py versions <skill-dir>      # 版本五件对齐
  python3 scripts/yotta_publish_guard.py names <skill-dir>         # 名称三通道查重（npm/GitHub/ClawHub）
  python3 scripts/yotta_publish_guard.py publish <skill-dir> [--dry-run] [--exec] [--force]

行为锚点:
  - 推送闸门：publish 前先跑内置校验，未通过默认阻断（--force 仅显式授权后可用）。
  - 网络命令（npm view / gh repo view / clawhub search）失败时优雅降级为「需手动查重」。
  - 只读：除 npm pack 临时产物外不修改任何文件（git init/commit 仅在 --exec 时执行）。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

VERSION = "0.4.5"
TOOL_NAME = "yotta-publish-guard"
CN_NAME = "元守"

SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}[a-z0-9]$")

# ---- 对外口吻黑名单（README 命中即 ERROR）----
COLLOQUIAL_PHRASES = (
    "别默认", "咱们", "你自己", "严格记住", "别忘", "别忘了", "别以为",
    "别搞", "别乱", "别乱动", "给我记住", "你必须", "听明白", "懂了吗",
    "记住了吗", "先别管", "别去管", "千万不要", "切记", "务必记住",
    "随便", "哈哈", "呗", "咯",
)
AI_INSTALL_GUIDANCE = ("AI 帮你装", "让 AI 帮", "自动帮你装")

class GuardConfig:
    """发布归属配置（可自定义，默认 YottaMeta）。

    自定义归属的取值由 CLI 参数或环境变量注入，支持将本守门复用于
    任意发布组织；默认值即 YottaMeta 家族配置，开箱即用。
    本技能不持有、不读取任何平台凭据——发布鉴权由各平台 CLI
    （npm / gh / clawhub）按使用者本机配置完成。
    """

    def __init__(self, npm_scope="@yottameta", github_org="YottaMeta",
                 clawhub_owner="yottameta", topic="yottaskills"):
        self.npm_scope = _norm_scope(npm_scope)
        self.github_org = str(github_org or "YottaMeta")
        self.clawhub_owner = str(clawhub_owner or "yottameta")
        self.topic = str(topic or "yottaskills")

    @property
    def npm_scope_full(self):
        return self.npm_scope


def _norm_scope(v):
    """规范化 npm scope：确保以 @ 开头且无尾部斜杠。"""
    v = str(v or "@yottameta").strip()
    if not v.startswith("@"):
        v = "@" + v
    return v.rstrip("/")


def resolve_config(args=None) -> GuardConfig:
    """解析发布归属配置：CLI 参数优先，其次环境变量，最后默认。"""
    def pick(cli_val, env_key, default):
        if cli_val:
            return cli_val
        env = os.environ.get(env_key)
        if env:
            return env
        return default
    return GuardConfig(
        npm_scope=pick(getattr(args, "npm_scope", None), "YOTTA_GUARD_NPM_SCOPE", "@yottameta"),
        github_org=pick(getattr(args, "github_org", None), "YOTTA_GUARD_GITHUB_ORG", "YottaMeta"),
        clawhub_owner=pick(getattr(args, "clawhub_owner", None), "YOTTA_GUARD_CLAWHUB_OWNER", "yottameta"),
        topic=pick(getattr(args, "topic", None), "YOTTA_GUARD_TOPIC", "yottaskills"),
    )


def _install_patterns(cfg: GuardConfig):
    """按配置生成 README 四方式安装校验正则（不再写死 YottaMeta）。"""
    scope = cfg.npm_scope_full
    org = cfg.github_org
    return {
        "方式一 npx 一行装": re.compile(r"npx\s+-y\s+" + re.escape(scope) + r"/[^\s`\"]+"),
        "方式二 git clone": re.compile(r"git\s+clone\s+https?://github\.com/" + re.escape(org) + r"/"),
        "方式三 Download ZIP": re.compile(r"Download\s+ZIP|下载压缩包|下载 ZIP"),
        "方式四 install.sh": re.compile(r"install\.sh\s+--agent"),
    }, {
        "npx skills（走 GitHub 克隆，无代理不可用）": re.compile(r"npx\s+skills\b", re.I),
        "-g 安装（为未安装智能体建目录，污染）": re.compile(
            r"npx\s+-y\s+" + re.escape(scope) + r"/[^\s`\"]+\s+-g|install\.sh\s+-g"),
    }


FOUR_WAYS, FORBIDDEN_INSTALL = _install_patterns(GuardConfig())

# 可选校验器 CLI 脚本名（与技能目录名不一致的特例）
EXTERNAL_CLI_SCRIPTS = {
    "yotta-security-audit": "yotta_audit.py",
    "yotta-vetter": "yotta_vetter.py",
    "yotta-verify": "yotta_verify.py",
}
EXTERNAL_FLAGS = {
    "yotta-security-audit": "--with-audit",
    "yotta-vetter": "--with-vetter",
    "yotta-verify": "--with-verify",
}

SECURITY_FAMILY_NAMES = {
    "yotta-security-audit", "yotta-vetter", "yotta-recon", "yotta-guardian",
    "yotta-secret", "yotta-chain", "yotta-triage", "yotta-logwatch",
    "yotta-intel", "yotta-verify", "yotta-agent-hardening",
    "yotta-security-testing",
}
SECURITY_KEYWORDS = ("security", "安全", "审计", "威胁", "侦察", "密钥", "供应链",
                     "样本", "日志", "审查", "护栏", "恶意", "扫描", "检测", "安全分析")

# 明确非安全家族的工具类技能（防止描述关键词如「审查」被误分类，
# 导致 Defense Triple 误报、ClawHub categories 错选 security）
NON_SECURITY_NAMES = {
    "yotta-anti-shallow",
    "yotta-code-quality",
    "yotta-humanize",
    "yotta-learn",
    "yotta-logs",
    "yotta-memory",
    "yotta-partner",
    "yotta-present",
    "yotta-prompt",
    "yotta-publish-guard",
    "yotta-skill-creator",
    "yotta-skills",
    "yotta-workflow",
}


def is_security(slug: str, desc: str) -> bool:
    if slug in NON_SECURITY_NAMES:
        return False
    if slug in SECURITY_FAMILY_NAMES:
        return True
    low = desc.lower()
    return any(k.lower() in low for k in SECURITY_KEYWORDS)


def parse_frontmatter(text: str) -> dict:
    """极简 frontmatter 解析：顶层 key: value + metadata 缩进块（zh_name 等）。"""
    fm = {}
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.S)
    if not m:
        return fm
    meta = None
    for line in m.group(1).splitlines():
        if line.startswith((" ", "\t")):
            if meta is not None:
                kv = re.match(r"^\s*([A-Za-z_][\w-]*):\s*(.*?)\s*$", line)
                if kv:
                    meta[kv.group(1)] = kv.group(2).strip().strip("\"'")
            continue
        kv = re.match(r"^([A-Za-z_][\w-]*):\s*(.*?)\s*$", line)
        if kv:
            key, val = kv.group(1), kv.group(2).strip().strip("\"'")
            fm[key] = val
            meta = {} if key == "metadata" else None
            if key == "metadata":
                fm["metadata"] = meta
    return fm


# --------------------------------------------------------------------------
# 内置校验（自包含副本，不依赖仓库 tools/）
# --------------------------------------------------------------------------
def validate_dir(skill_dir: Path, mode="full", config=None):
    cfg = config or resolve_config()
    """返回 (errors, warns)。skill_dir 为技能目录绝对路径。

    mode:
      - full   ：完整发布件要求（README 中英四方式 / package.json / CHANGELOG /
                 LICENSE / NOTICE 等），npm + ClawHub 双渠道发布前用。
      - github ：只推 GitHub 时用：要求 SKILL.md / LICENSE / README.md（英文），
                 不强制 README.zh-CN / package.json / CHANGELOG / NOTICE /
                 publish.yml 等 npm 发布件；已存在的文件仍做对应检查。
      - self   ：自用模式：只查技能本体完整性（SKILL.md / frontmatter / 占位符 /
                 围栏 / Defense Triple），不要求任何发布件。
    """
    errors, warns = [], []
    if not skill_dir.is_dir():
        return ["技能目录不存在: %s" % skill_dir], []

    slug = skill_dir.name
    if not SLUG_RE.fullmatch(slug):
        errors.append("目录名不符合小写连字符规范: %s" % slug)

    require_full = mode == "full"
    require_readme = mode in ("full", "github")

    skill = skill_dir / "SKILL.md"
    fm, text = {}, ""
    if not skill.is_file():
        errors.append("缺少 SKILL.md（技能入口）")
    else:
        text = skill.read_text(encoding="utf-8", errors="ignore")
        fm = parse_frontmatter(text)
        if fm.get("name") != slug:
            errors.append("SKILL.md frontmatter name=%r 与目录名不一致" % fm.get("name"))
        for k in ("description", "version", "license"):
            if not fm.get(k):
                errors.append("SKILL.md frontmatter 缺少 %s" % k)
        desc = fm.get("description", "")

        # Defense Triple（安全家族：范围 / 授权 / 法律红线）
        if is_security(slug, desc):
            need = (("范围", "Scope"), ("授权", "authorized"), ("法律", "legal"))
            for zh, en in need:
                if zh not in text and en.lower() not in text.lower():
                    errors.append("SKILL.md 缺少安全家族 Defense Triple 声明：%s/%s" % (zh, en))

    if require_full and not (skill_dir / "LICENSE").is_file():
        errors.append("缺少 LICENSE（必需，默认 MIT）")
    if mode == "github" and not (skill_dir / "LICENSE").is_file():
        warns.append("GitHub 仓库建议带 LICENSE（默认 MIT）")

    # ---- README（发布件要求；github 模式只要求 README.md，自用模式不强制）----
    rdt = skill_dir / "README.md"
    if not rdt.is_file():
        if require_readme:
            errors.append("缺少 README.md（对外门面）")
    else:
        rtext = rdt.read_text(encoding="utf-8", errors="ignore")
        errors += check_voice(rtext, "README.md")
        if require_full:
            if not re.search(r"Language[^<\n]{0,20}English|English.*中文", rtext):
                errors.append("README.md 缺少语言切换标识（<b>Language</b>: English · 中文）")
            check_readme_install(rtext, "README.md", errors, warns, config=cfg)
    rzt = skill_dir / "README.zh-CN.md"
    if not rzt.is_file():
        if require_full:
            errors.append("缺少 README.zh-CN.md（中文版，对外文档必须中英双语）")
    else:
        ztext = rzt.read_text(encoding="utf-8", errors="ignore")
        errors += check_voice(ztext, "README.zh-CN.md")
        if re.search(r"Language[^<\n]{0,20}English", ztext):
            warns.append("README.zh-CN.md 出现 Language=English 标识，疑似语言版本放反")

    # ---- 版本（package / SKILL / CHANGELOG / CLI）----
    pkg_v = None
    pkg = skill_dir / "package.json"
    if not pkg.is_file():
        if require_full:
            errors.append("缺少 package.json（npm 双源发布必需）")
    else:
        try:
            data = json.loads(pkg.read_text(encoding="utf-8"))
            pkg_v = str(data.get("version") or "")
            expect = cfg.npm_scope_full + "/" + slug
            if data.get("name") != expect:
                errors.append("package.json name=%r 与 %s 不一致" % (data.get("name"), expect))
        except Exception as e:
            errors.append("package.json 解析失败: %s" % e)
    skill_v = fm.get("version")
    if pkg_v and skill_v and pkg_v != str(skill_v):
        errors.append("版本不一致：package.json=%s vs SKILL.md=%s" % (pkg_v, skill_v))

    chg = skill_dir / "CHANGELOG.md"
    if chg.is_file():
        cm = re.search(r"^##\s*v?([0-9]+\.[0-9]+\.[0-9]+)",
                       chg.read_text(encoding="utf-8", errors="ignore"), re.M)
        if cm:
            if pkg_v and cm.group(1) != pkg_v:
                errors.append("版本不一致：package.json=%s vs CHANGELOG 顶部=%s"
                              % (pkg_v, cm.group(1)))
        else:
            warns.append("CHANGELOG.md 未找到版本标题（应为 ## vX.Y.Z）")
    elif pkg_v and require_full:
        warns.append("缺少 CHANGELOG.md（发布规范建议提供）")

    # ---- 占位符残留（技能自带 template/ 语料豁免，如 yotta-skill-creator）----
    for f in skill_dir.rglob("*"):
        if f.is_file() and f.suffix in (".md", ".json", ".sh", ".yml", ".yaml"):
            rel = f.relative_to(skill_dir)
            if "template" in rel.parts:
                continue
            if "{{" in f.read_text(encoding="utf-8", errors="ignore"):
                errors.append("存在未替换占位符: %s" % rel)

    # ---- Markdown 围栏 ----
    for f in skill_dir.rglob("*.md"):
        if f.is_file():
            t = f.read_text(encoding="utf-8", errors="ignore")
            if t.count("```") % 2 != 0:
                errors.append("Markdown 代码围栏不配对: %s" % f.relative_to(skill_dir))
    return errors, warns


def check_voice(text: str, label: str):
    errs = []
    for p in COLLOQUIAL_PHRASES:
        if p in text:
            errs.append("%s 命中对外口吻黑名单: %s" % (label, p))
    for p in AI_INSTALL_GUIDANCE:
        if p in text:
            errs.append("%s 命中 AI 安装引导禁用词: %s" % (label, p))
    return errs


def check_readme_install(text: str, label: str, errors, warns, config=None):
    cfg = config or resolve_config()
    ways, forbidden = _install_patterns(cfg)
    for name, pat in ways.items():
        if not pat.search(text):
            errors.append("%s 缺少%s（发布规范四方式安装）" % (label, name))
    for name, pat in forbidden.items():
        if pat.search(text):
            errors.append("%s 命中禁用安装方式：%s" % (label, name))


# --------------------------------------------------------------------------
# 可选校验器（元安 / 元审 / 元信，若已装）
# --------------------------------------------------------------------------
def find_external_cli(name: str) -> Path:
    """在常见位置查找可选的校验技能 CLI。name 为技能目录名（如 yotta-security-audit）。"""
    script = EXTERNAL_CLI_SCRIPTS.get(name) or ("%s.py" % name.replace("-", "_"))
    candidates = []
    here = Path(__file__).resolve()
    # 发布包内 / 相邻（开发仓库 yottaskills/ 下）
    for depth in (1, 2, 3, 4):
        cand = here.parents[depth] / name / "scripts" / script
        candidates.append(cand)
    # 常见用户级技能目录
    home = Path.home()
    user_dirs = [
        home / ".codex" / "skills", home / ".claude" / "skills",
        home / ".config" / "opencode" / "skills", home / ".gemini" / "skills",
        home / ".cursor" / "skills", home / ".agents" / "skills",
    ]
    for ud in user_dirs:
        candidates.append(ud / name / "scripts" / script)
    for c in candidates:
        if c.is_file():
            return c
    return None


def _win_cmd(cmd):
    """Windows 下 .cmd/.bat 需经 cmd.exe 执行（CreateProcess 不直接支持）。"""
    if os.name != "nt":
        return cmd
    first = cmd[0]
    exe = shutil.which(first) or first
    if exe.lower().endswith((".cmd", ".bat")):
        comspec = os.environ.get("COMSPEC", "cmd.exe")
        return [comspec, "/d", "/s", "/c", subprocess.list2cmdline(cmd)]
    return cmd


def run_cmd(cmd, cwd=None, env=None, timeout=120):
    """返回 (returncode, stdout, stderr)。"""
    label = cmd[0]
    cmd = _win_cmd(cmd)
    try:
        r = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True,
                           timeout=timeout)
        out = r.stdout.decode("utf-8", errors="replace")
        err = r.stderr.decode("utf-8", errors="replace")
        return r.returncode, out, err
    except FileNotFoundError:
        return 127, "", "命令不存在: %s" % label
    except subprocess.TimeoutExpired:
        return 124, "", "命令超时: %s" % cmd[0]


def _json_summary(out: str) -> str:
    """从 JSON 报告提取一句话摘要；非 JSON 返回空串。"""
    try:
        data = json.loads(out)
    except Exception:
        return ""
    if isinstance(data, list):
        return "findings=%d" % len(data)
    if not isinstance(data, dict):
        return ""
    bits = []
    tool = data.get("tool")
    if isinstance(tool, dict):
        name = tool.get("cn") or tool.get("name") or ""
        ver = tool.get("version") or data.get("version") or ""
        if name:
            bits.append("%s v%s" % (name, ver))
    for k in ("verdict", "result", "summary"):
        v = data.get(k)
        if isinstance(v, str) and v:
            bits.append("%s=%s" % (k, v))
            break
    counts = data.get("counts")
    if isinstance(counts, dict) and counts:
        bits.append(" ".join("%s=%s" % (k, v) for k, v in sorted(counts.items())))
    elif "findings" in data and isinstance(data["findings"], list):
        bits.append("findings=%d" % len(data["findings"]))
    return "；".join(b for b in bits if b)


def external_verdict(name, run_args, label):
    """运行可选的校验器；返回 (ok, summary)。找不到/失败不阻断。"""
    cli = find_external_cli(name)
    if cli is None:
        return None, "%s 未安装，跳过（可选：安装后加 %s 复查）" % (
            label, EXTERNAL_FLAGS.get(name, "--with-%s" % name))
    code, out, err = run_cmd([sys.executable, str(cli)] + run_args)
    if code == 127:
        return None, "%s 不可用（%s）" % (label, err.strip() or "命令不存在")
    summary = _json_summary(out)
    if not summary:
        lines = [ln for ln in out.strip().splitlines() if ln.strip()]
        summary = (lines[0] if lines else err.strip()) or "(无输出)"
    return code, "%s → exit %s：%s" % (label, code, summary)


# --------------------------------------------------------------------------
# 子命令实现
# --------------------------------------------------------------------------
def cmd_check(args) -> int:
    d = Path(args.dir).expanduser().resolve()
    cfg = resolve_config(args)
    errors, warns = validate_dir(d, mode="self" if args.self_use else "full", config=cfg)
    mode = "自用模式（只查技能本体）" if args.self_use else "发布就绪检查"
    print("== %s %s v%s —— %s（归属 %s / %s）==" % (CN_NAME, TOOL_NAME, VERSION, mode, cfg.npm_scope_full, cfg.github_org))
    print("技能目录: %s" % d)

    optional = []
    if args.with_audit:
        optional.append(external_verdict(
            "yotta-security-audit",
            ["--target", "skill", "--path", str(d), "--no-color", "--json"],
            "元安 yotta-security-audit"))
    if args.with_vetter:
        optional.append(external_verdict(
            "yotta-vetter", ["check", str(d), "--no-color", "--json"],
            "元审 yotta-vetter"))
    if args.with_verify:
        optional.append(external_verdict(
            "yotta-verify", ["scan", str(d), "--json"],
            "元信 yotta-verify"))

    print("\n[validate] %d ERROR / %d WARN" % (len(errors), len(warns)))
    for e in errors:
        print("  [ERROR] %s" % e)
    for w in warns:
        print("  [WARN ] %s" % w)
    for verdict in optional:
        if verdict is not None:
            ok, summary = verdict
            print("  [%s] %s" % ("PASS" if ok == 0 else "CHECK", summary))

    if errors:
        print("\n结果: BLOCKED —— 修复后重跑，或 publish 显式 --force")
        return 2
    print("\n结果: READY%s" % ("（含 %d 条 WARN 建议）" % len(warns) if warns else ""))
    return 1 if warns else 0


def _npm_pack_files(d: Path):
    """返回 (files, used_npm)。npm 不可用时本地回退列举（近似 npmignore）。"""
    npm = shutil.which("npm")
    if npm:
        cache = tempfile.mkdtemp(prefix="pg-npmcache-")
        code, out, err = run_cmd(
            [npm, "pack", "--dry-run", "--json", "--cache", cache], cwd=str(d))
        if code == 0 and out.strip():
            try:
                entries = json.loads(out)
                files = []
                if isinstance(entries, dict):
                    entries = list(entries.values())
                for entry in entries:
                    if isinstance(entry, dict):
                        files += [f.get("path", "") for f in entry.get("files", [])]
                if files:
                    return files, True
            except Exception:
                pass
        # 失败时回退
    files = []
    skip_dirs = {".git", "node_modules", "__pycache__", ".tmp"}
    for p in d.rglob("*"):
        rel = p.relative_to(d)
        parts = rel.parts
        if any(seg in skip_dirs for seg in parts):
            continue
        if p.is_file():
            name = p.name
            if name.endswith((".pyc", ".pyo", ".tgz")) or name == ".npmignore":
                continue
            files.append(str(rel).replace("\\", "/"))
    return sorted(files), False


def cmd_pack(args) -> int:
    d = Path(args.dir).expanduser().resolve()
    files, used_npm = _npm_pack_files(d)
    print("== npm pack 检查（%s）==" % ("npm --dry-run" if used_npm else "本地回退列举"))
    bad = [f for f in files if f.endswith(".pyc") or "__pycache__" in f]
    required = ["SKILL.md", "LICENSE", "README.md", "README.zh-CN.md"]
    missing = [r for r in required if r not in files]
    print("打包文件数: %d" % len(files))
    for f in sorted(files):
        print("  - %s" % f)
    if bad:
        print("  [ERROR] 包内混入 pyc/__pycache__: %s" % ", ".join(bad))
    if missing:
        print("  [ERROR] 包内缺少关键文件: %s" % ", ".join(missing))
    for extra in ("NOTICE", "CHANGELOG.md"):
        if (d / extra).is_file() and extra not in files:
            print("  [WARN ] %s 存在于目录但未进包（检查 package.json files 字段）" % extra)
    if bad or missing:
        return 2
    print("结果: PASS")
    return 0


def _cli_versions(d: Path, slug: str):
    """提取 CLI 版本。返回 (found, version 列表)。"""
    found = []
    pat = re.compile(r'VERSION\s*=\s*["\']([^"\']+)["\']')
    scripts = []
    primary = d / "scripts" / ("%s.py" % slug.replace("-", "_"))
    if primary.is_file():
        scripts.append(primary)
    for p in sorted((d / "scripts").glob("*.py")) if (d / "scripts").is_dir() else []:
        if p not in scripts and p.name.startswith("yotta_") and "test" not in p.name:
            scripts.append(p)
    for p in scripts:
        m = pat.search(p.read_text(encoding="utf-8", errors="ignore"))
        if m:
            found.append((p.name, m.group(1)))
    return found


def cmd_versions(args) -> int:
    d = Path(args.dir).expanduser().resolve()
    slug = d.name
    pkg_v, skill_v, chg_v, body_v = None, None, None, None
    pkg = d / "package.json"
    if pkg.is_file():
        try:
            pkg_v = str(json.loads(pkg.read_text(encoding="utf-8")).get("version") or "")
        except Exception:
            pkg_v = ""
    skill = d / "SKILL.md"
    if skill.is_file():
        skill_text = skill.read_text(encoding="utf-8")
        skill_v = parse_frontmatter(skill_text).get("version")
        body_match = re.search(r"版本[：:]\s*v?([0-9]+\.[0-9]+\.[0-9]+)", skill_text)
        if body_match:
            body_v = body_match.group(1)
    chg = d / "CHANGELOG.md"
    if chg.is_file():
        cm = re.search(r"^##\s*v?([0-9]+\.[0-9]+\.[0-9]+)",
                       chg.read_text(encoding="utf-8", errors="ignore"), re.M)
        if cm:
            chg_v = cm.group(1)
    cli_vers = _cli_versions(d, slug)

    rows = [("package.json", pkg_v), ("SKILL.md", skill_v), ("CHANGELOG", chg_v)]
    if body_v:
        rows.append(("SKILL.md 正文版本行", body_v))
    for name, v in cli_vers:
        rows.append(("CLI %s" % name, v))
    print("== 版本五件对齐 ==")
    seen = set()
    for name, v in rows:
        print("  %-22s %s" % (name, v or "(缺失)"))
        seen.add(v)
    if None in (pkg_v, skill_v):
        print("结果: FAIL —— 缺少 package.json 或 SKILL.md 版本")
        return 2
    if len(seen) > 1:
        print("结果: FAIL —— 版本不一致（%s）" % " / ".join(sorted(x or "缺失" for x in seen)))
        return 2
    print("结果: PASS —— 全部对齐 %s" % pkg_v)
    return 0


def _npm_taken(slug: str, cfg: GuardConfig):
    cache = tempfile.mkdtemp(prefix="pg-npmcache-")
    code, out, err = run_cmd(
        ["npm", "view", cfg.npm_scope_full + "/" + slug, "version", "--cache", cache])
    if code == 0:
        return "taken", out.strip().splitlines()[-1] if out.strip() else "?"
    if "404" in err or "ENOTFOUND" in err or "E404" in err:
        return "free", ""
    return "unknown", err.strip()[:120]


def _gh_taken(slug: str, cfg: GuardConfig):
    code, out, err = run_cmd(["gh", "repo", "view", cfg.github_org + "/" + slug])
    if code == 0:
        return "taken", ""
    if "not found" in err.lower() or "could not resolve" in err.lower() or "404" in err:
        return "free", ""
    return "unknown", err.strip()[:120]


def _clawhub_taken(slug: str):
    code, out, err = run_cmd(["clawhub", "search", "--exact", slug, "--limit", "5"])
    if code == 0:
        if slug in out:
            return "taken", out.strip()[:120]
        return "free", ""
    return "unknown", err.strip()[:120]


def cmd_names(args) -> int:
    slug = Path(args.dir).expanduser().resolve().name
    cfg = resolve_config(args)
    print("== 名称三通道查重：%s（归属 %s / %s）==\n" % (slug, cfg.npm_scope_full, cfg.github_org))
    checks = [("npm %s/%s" % (cfg.npm_scope_full, slug), _npm_taken(slug, cfg)),
              ("GitHub %s/%s" % (cfg.github_org, slug), _gh_taken(slug, cfg)),
              ("ClawHub %s" % slug, _clawhub_taken(slug))]
    unknown = taken = 0
    for label, (status, detail) in checks:
        if status == "taken":
            taken += 1
            print("  [TAKEN ] %s —— 已被占用%s" % (label, "（%s）" % detail if detail else ""))
        elif status == "free":
            print("  [FREE  ] %s —— 可占用" % label)
        else:
            unknown += 1
            print("  [UNKNOWN] %s —— 无法确认（%s）" % (label, detail or "网络/CLI 不可用"))
    if unknown:
        print("提示：以下渠道无法确认，发布前请手动查重：")
        print("  - npm:  https://www.npmjs.com/package/%s/%s" % (cfg.npm_scope_full, slug))
        print("  - GitHub: https://github.com/%s/%s" % (cfg.github_org, slug))
        print("  - ClawHub: https://clawhub.com (search %s)" % slug)
        return 1
    if taken:
        return 2
    print("结果: 三通道全部空闲，可发布。")
    return 0


def _channels_from_args(args):
    """解析发布渠道列表（github / npm / clawhub）。"""
    if getattr(args, "github_only", False):
        return ["github"]
    raw = getattr(args, "channels", "") or "github,npm,clawhub"
    channels = []
    for c in raw.split(","):
        c = c.strip().lower()
        if c in ("github", "npm", "clawhub") and c not in channels:
            channels.append(c)
    if not channels:
        raise ValueError("--channels 至少选择一个：github / npm / clawhub")
    return channels


def _shell_quote(v):
    """计划展示用：值含空白/引号时加引号（PowerShell 与 bash 均可复制执行）。"""
    v = str(v)
    if not v:
        return "''"
    if not any(ch.isspace() for ch in v) and "'" not in v and '"' not in v:
        return v
    if "'" not in v:
        return "'%s'" % v
    if '"' not in v:
        return '"%s"' % v
    return v


GH_DESC_MAX = 350  # GitHub repo description 上限（createRepository 拒绝 >350 字符）


def _publish_plan(d: Path, args, config=None):
    """构建发布命令计划。返回 (渠道列表, 计划行列表, 阻断 errors)。"""
    cfg = config or resolve_config(args)
    channels = _channels_from_args(args)
    mode = "github" if channels == ["github"] else "full"
    errors, warns = validate_dir(d, mode=mode, config=cfg)
    plan = []
    slug = d.name
    pkg_v = "0.1.0"
    desc = ""
    zh = slug
    pkg = d / "package.json"
    if pkg.is_file():
        try:
            data = json.loads(pkg.read_text(encoding="utf-8"))
            pkg_v = str(data.get("version") or pkg_v)
            desc = str(data.get("description") or "")
        except Exception:
            pass
    skill = d / "SKILL.md"
    if skill.is_file():
        fm = parse_frontmatter(skill.read_text(encoding="utf-8"))
        zh = (fm.get("metadata") or {}).get("zh_name") or fm.get("zh_name") or slug
    if args.description:
        desc = args.description
    if len(desc) > GH_DESC_MAX:
        desc = desc[:GH_DESC_MAX - 3] + "..."
    if is_security(slug, desc):
        cats = args.categories or "security"
    else:
        cats = args.categories or "productivity"
    topics = args.topics or cats

    if "github" in channels:
        plan.append(("git init", ["git", "init"]))
        plan.append(("git add .", ["git", "add", "."]))
        plan.append(("git commit", ["git", "commit", "-m",
                                    "feat: initial release v%s" % pkg_v]))
        plan.append(("gh repo create",
                     ["gh", "repo", "create", cfg.github_org + "/" + slug, "--public",
                      "--source=.", "--push", "--description", desc]))
        plan.append(("gh add topic",
                     ["gh", "repo", "edit", cfg.github_org + "/" + slug, "--add-topic",
                      cfg.topic]))
    if "npm" in channels:
        npm_cmd = ["npm", "publish", "--registry=https://registry.npmjs.org/"]
        if os.name == "nt":
            cache = tempfile.mkdtemp(prefix="pg-npmcache-")
            npm_cmd += ["--cache", cache]
        plan.append(("npm publish", npm_cmd))
    if "clawhub" in channels:
        owner = cfg.clawhub_owner
        plan.append(("clawhub publish",
                     ["clawhub", "publish", str(d),
                      "--name", "%s %s" % (zh, slug),
                      "--owner", owner,
                      "--version", pkg_v,
                      "--categories", cats,
                      "--topics", topics]))
    if os.name == "nt":
        plan.append(("note",
                     "git 走代理需加 -c http.sslBackend=openssl（schannel 报 SEC_E_NO_CREDENTIALS）"))
    if "clawhub" in channels:
        plan.append(("note",
                     "clawhub 发布归属 org=%s（勿发布到个人账号）；GitHub 建仓必须带 --description（否则 About 显示 No description）" % cfg.clawhub_owner))
    return channels, plan, errors


def cmd_publish(args) -> int:
    d = Path(args.dir).expanduser().resolve()
    try:
        channels, plan, errors = _publish_plan(d, args)
    except ValueError as e:
        print("[ERROR] %s" % e, file=sys.stderr)
        return 2
    print("== 发布计划（渠道：%s）：%s ==" % (" + ".join(channels), d.name))
    if errors:
        print("推送闸门：以下校验未通过，默认阻断（--force 仅显式授权后可用）：")
        for e in errors:
            print("  [ERROR] %s" % e)
        if not args.force:
            return 2
        print("  --force 已显式授权，继续生成命令。")

    for title, cmd in plan:
        if title == "note":
            print("  # %s" % cmd)
        else:
            print("  $ %s" % " ".join(_shell_quote(a) for a in cmd))

    if not args.exec:
        print("\n[DRY-RUN] 未执行。复制以上命令执行，或加 --exec 直接执行。")
        return 0

    print("\n[EXEC] 按序执行……")
    for title, cmd in plan:
        if title == "note":
            continue
        print("$ %s" % " ".join(_shell_quote(a) for a in cmd))
        code, out, err = run_cmd(cmd, cwd=str(d))
        if out.strip():
            print(out.strip())
        if err.strip():
            print(err.strip(), file=sys.stderr)
        if code != 0:
            print("[ERROR] %s 失败（exit %s），已中止。" % (title, code), file=sys.stderr)
            return code
    print("\n[EXEC] 发布命令全部执行完成。")
    return 0

def build_parser():
    ap = argparse.ArgumentParser(
        prog=TOOL_NAME,
        description="%s —— 发布前守门（零依赖 Python 3.8+）" % CN_NAME,
    )
    ap.add_argument("--version", action="version", version="%(prog)s " + VERSION)
    g = ap.add_argument_group("归属配置（可选，缺省 YottaMeta 开箱即用）")
    g.add_argument("--npm-scope", default=None, metavar="SCOPE",
                   help="npm scope（如 @acme；缺省 @yottameta）")
    g.add_argument("--github-org", default=None, metavar="ORG",
                   help="GitHub org（如 AcmeOrg；缺省 YottaMeta）")
    g.add_argument("--clawhub-owner", default=None, metavar="OWNER",
                   help="ClawHub 发布归属 org（缺省 yottameta）")
    g.add_argument("--topic", default=None, metavar="TOPIC",
                   help="GitHub 仓库 topic（缺省 yottaskills）")
    sub = ap.add_subparsers(dest="command", required=True)

    pc = sub.add_parser("check", help="聚合校验，输出发布就绪报告")
    pc.add_argument("dir", help="技能目录")
    pc.add_argument("--self-use", action="store_true",
                    help="自用模式：只查技能本体完整性，不要求发布件（README 中英 / "
                         "package.json / CHANGELOG / LICENSE）")
    pc.add_argument("--with-audit", action="store_true", help="聚合元安 yotta-security-audit")
    pc.add_argument("--with-vetter", action="store_true", help="聚合元审 yotta-vetter")
    pc.add_argument("--with-verify", action="store_true", help="聚合元信 yotta-verify")
    pc.set_defaults(func=cmd_check)

    pp = sub.add_parser("pack", help="npm pack --dry-run 检查（无 pyc / 关键文件在包内）")
    pp.add_argument("dir")
    pp.set_defaults(func=cmd_pack)

    pv = sub.add_parser("versions", help="版本五件对齐（package / SKILL frontmatter / SKILL 正文版本行 / CHANGELOG / CLI）")
    pv.add_argument("dir")
    pv.set_defaults(func=cmd_versions)

    pn = sub.add_parser("names", help="名称三通道查重（npm / GitHub / ClawHub）")
    pn.add_argument("dir")
    pn.set_defaults(func=cmd_names)

    ppu = sub.add_parser("publish", help="发布命令封装（默认 dry-run，--exec 执行）")
    ppu.add_argument("dir")
    ppu.add_argument("--dry-run", action="store_true", help="只打印计划（默认）")
    ppu.add_argument("--exec", action="store_true", help="直接按序执行发布命令")
    ppu.add_argument("--force", action="store_true", help="显式授权跳过推送闸门")
    ppu.add_argument("--channels", default="",
                    help="发布渠道（逗号分隔，可选 github/npm/clawhub；缺省全渠道）")
    ppu.add_argument("--github-only", action="store_true",
                    help="只推 GitHub（等价 --channels github；npm / ClawHub 非必选）")
    ppu.add_argument("--categories", default="", help="ClawHub 分类 slug（逗号分隔）")
    ppu.add_argument("--topics", default="", help="ClawHub topics（逗号分隔）")
    ppu.add_argument("--clawhub-owner", default=None, help="ClawHub 发布归属 org handle（默认见全局归属配置）")
    ppu.add_argument("--description", default="", help="GitHub 仓库简介（覆盖 package.json description）")
    ppu.set_defaults(func=cmd_publish)
    return ap


def main(argv=None) -> int:
    ap = build_parser()
    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception as e:
        print("[FATAL] %s: %s" % (TOOL_NAME, e), file=sys.stderr)
        sys.exit(4)
