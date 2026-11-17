#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ym-skillhub · 把本地技能一键创建/更新到 SkillHub（skillhub.cn）

子命令
------
  doctor                  环境自检：CLI 位置 / python 解释器 / 登录凭据 / 网络
  check  <技能目录>        发布预检：平台字段 + 版本号 + 扩展名白名单 + 市场规范 + CLI dry-run
  fix    <技能目录>        自动补齐平台字段（slug / displayName / summary / tags），
                          并把块标量、多行列表、行尾注释规整成平台能读的形态（幂等）
  bump   <技能目录>        递增版本号（--patch 默认 / --minor / --major / --set X.Y.Z）
  publish <技能目录>       调用 skillhub CLI 发布（--changelog / --dry-run / --version）
  status <slug>           查线上真实状态（latestVersion / category / 版本列表 / 下载包）
  release <技能目录>       一条龙：check → fix → bump → publish → status

只用标准库。退出码：0 通过 / 1 有告警 / 2 有阻断 / 3 环境不可用。
"""

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

sys.dont_write_bytecode = True

API = "https://api.skillhub.cn/api/v1"
HOME = Path(os.path.expanduser("~"))

# ── 平台 13 个分类枚举（实测） ──────────────────────────────────────────────
CATEGORIES = [
    "office-efficiency", "content-creation", "dev-programming", "data-analysis",
    "design-media", "ai-agent", "knowledge-management", "business-ops",
    "education", "professional", "it-ops-security", "life-service", "pay-skill",
]

# ── 平台只收纯文本：扩展名白名单 ───────────────────────────────────────────
TEXT_EXT = {
    "md", "markdown", "txt", "py", "js", "mjs", "cjs", "ts", "tsx", "jsx",
    "json", "yaml", "yml", "toml", "ini", "cfg", "conf", "sh", "bash", "ps1",
    "html", "htm", "css", "scss", "csv", "tsv", "sql", "xml", "svg", "env",
    "gitkeep", "editorconfig",
}

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.\-]+)?$")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
KEY_RE = re.compile(r"^([A-Za-z_][\w\-]*)\s*:\s*(.*)$")

# 平台真正会读的字段。**只有这些**才需要按平台解析器口味规整 ——
# `trigger` / `display_name` / `agent_created` 是 WorkBuddy 本机字段，平台不看，
# 擅自把它们的多行列表压成单行会把本机技能弄坏。
PLATFORM_KEYS = {
    "name", "slug", "version", "displayName", "summary", "description",
    "description_zh", "description_en", "tags", "category", "author", "license", "homepage",
}


# ══════════════════════════════════════════════════════════════════════════
# 输出小工具
# ══════════════════════════════════════════════════════════════════════════
class R:
    """计数器（模块级状态，供各子命令累加）。"""
    warnings = 0
    errors = 0


def say(msg=""):
    print(msg)


def ok(msg):
    print("  ✔ " + msg)


def warn(msg):
    print("  ! " + msg)
    R.warnings += 1


def bad(msg):
    print("  ✘ " + msg)
    R.errors += 1


def info(msg):
    print("  · " + msg)


def reset_counter():
    R.warnings = 0
    R.errors = 0


# ══════════════════════════════════════════════════════════════════════════
# 环境：定位 CLI 与 python 解释器
# ══════════════════════════════════════════════════════════════════════════
def find_cli():
    """返回 skills_store_cli.py 的路径。"""
    cands = [
        HOME / ".skillhub" / "skills_store_cli.py",
        HOME / ".skillhub" / "skills_store_cli.pyc",
    ]
    for c in cands:
        if c.exists():
            return c
    return None


def find_python():
    """优先系统 python —— managed 3.13 在本机跑带网络请求的脚本会 segfault。"""
    cands = []
    if os.environ.get("SKILLHUB_PYTHON"):
        cands.append(os.environ["SKILLHUB_PYTHON"])
    local = os.environ.get("LOCALAPPDATA")
    if local:
        cands.append(str(Path(local) / "Microsoft" / "WindowsApps" / "python.exe"))
    cands.append(sys.executable)
    for c in cands:
        if c and Path(c).exists():
            return c
    return sys.executable


def cli_env():
    """skillhub CLI 在 Git Bash 下会 RuntimeError: Could not determine home directory，
    显式给 HOME / USERPROFILE 即可。"""
    env = dict(os.environ)
    env["HOME"] = str(HOME)
    env["USERPROFILE"] = str(HOME)
    env["PYTHONIOENCODING"] = "utf-8"
    return env


def run_cli(args, timeout=180):
    cli = find_cli()
    if not cli:
        return 3, "找不到 skillhub CLI（期望 ~/.skillhub/skills_store_cli.py）"
    cmd = [find_python(), str(cli)] + list(args)
    try:
        p = subprocess.run(cmd, capture_output=True, timeout=timeout,
                           env=cli_env(), cwd=str(cli.parent))
        out = (p.stdout or b"").decode("utf-8", "replace")
        err = (p.stderr or b"").decode("utf-8", "replace")
        return p.returncode, (out + ("\n" + err if err.strip() else "")).strip()
    except subprocess.TimeoutExpired:
        return 3, "skillhub CLI 超时（网络或平台无响应）"
    except Exception as e:  # noqa: BLE001
        return 3, "调用 skillhub CLI 失败：%r" % (e,)


def has_credential():
    if os.environ.get("SKILLHUB_TOKEN"):
        return True
    return (HOME / ".skillhub" / "credentials.json").exists()


# ══════════════════════════════════════════════════════════════════════════
# frontmatter 读写（保持其余内容一字不动）
# ══════════════════════════════════════════════════════════════════════════
class FM:
    """行级 frontmatter。只认平台那套 `key: 值` / `key: [a, b]`，但读得比平台宽容，
    以便发现平台会读错的地方并修掉。"""

    def __init__(self, path: Path):
        self.path = path
        self.text = path.read_text(encoding="utf-8")
        self.nl = "\r\n" if "\r\n" in self.text else "\n"
        self.lines = self.text.split(self.nl)
        self.entries = []          # [{key, inline, cont, start, end}]
        self.body_start = None
        self._parse()

    def _parse(self):
        lines = self.lines
        if not lines or lines[0].strip() != "---":
            self.body_start = 0
            return
        close = None
        for i in range(1, len(lines)):
            if lines[i].strip() in ("---", "..."):
                close = i
                break
        if close is None:
            self.body_start = 0
            return
        i = 1
        while i < close:
            m = KEY_RE.match(lines[i])
            if not m:
                i += 1
                continue
            ent = {"key": m.group(1), "inline": m.group(2).strip(),
                   "cont": [], "start": i, "end": i + 1}
            j = i + 1
            while j < close and lines[j].strip() and lines[j][:1] in (" ", "\t"):
                ent["cont"].append(lines[j].strip())
                j += 1
            ent["end"] = j
            self.entries.append(ent)
            i = j
        self.body_start = close

    # ── 读 ──
    def entry(self, key):
        for e in self.entries:
            if e["key"] == key:
                return e
        return None

    def raw(self, key):
        e = self.entry(key)
        return e["inline"] if e else None

    def value(self, key):
        """剥引号、剥行尾注释、展开块标量/多行列表后的真实值。"""
        e = self.entry(key)
        if not e:
            return ""
        inline = e["inline"]
        if inline in (">-", ">", "|", "|-", "|+", ">+") or (not inline and e["cont"]):
            if e["cont"] and e["cont"][0].startswith("- "):
                return ", ".join(x[2:].strip() for x in e["cont"])
            return " ".join(e["cont"])
        quoted = len(inline) >= 2 and inline[0] == inline[-1] and inline[0] in ("'", '"')
        if quoted:
            return inline[1:-1]
        return re.sub(r"\s+#\s.*$", "", inline).strip()

    def list_value(self, key):
        v = self.value(key)
        if v.startswith("[") and v.endswith("]"):
            v = v[1:-1]
        return [x.strip().strip("'\"") for x in v.split(",") if x.strip()]

    # ── 写（只改动被碰到的行） ──
    def _set_lines(self, ent, new_line):
        self.lines[ent["start"]:ent["end"]] = [new_line]

    def set(self, key, value):
        e = self.entry(key)
        line = "%s: %s" % (key, value)
        if e:
            self._set_lines(e, line)
        else:
            self._insert(key, line)
        self._parse()

    def _insert(self, key, line):
        anchor = {
            "slug": "name", "displayName": "display_name", "summary": "description_zh",
            "tags": "trigger", "category": "description_en",
        }.get(key)
        pos = None
        if anchor:
            e = self.entry(anchor)
            if e:
                pos = e["end"]
        if pos is None:
            pos = self.body_start if self.body_start is not None else len(self.lines)
        self.lines[pos:pos] = [line]

    def drop(self, key):
        e = self.entry(key)
        if e:
            del self.lines[e["start"]:e["end"]]
            self._parse()

    def render(self):
        return self.nl.join(self.lines)

    def save(self, text=None):
        self.path.write_text(text if text is not None else self.render(), encoding="utf-8")


def load_skill(skill_dir):
    d = Path(skill_dir).expanduser().resolve()
    md = d / "SKILL.md"
    if not md.exists():
        return None, d, None
    return FM(md), d, md


# ══════════════════════════════════════════════════════════════════════════
# doctor
# ══════════════════════════════════════════════════════════════════════════
def cmd_doctor(args):
    say("环境自检")
    cli = find_cli()
    if cli:
        ok("CLI 主程序：%s" % cli)
    else:
        bad("找不到 ~/.skillhub/skills_store_cli.py —— 需先安装 SkillHub CLI")
    py = find_python()
    info("python 解释器：%s" % py)
    if has_credential():
        ok("登录凭据：已就绪（~/.skillhub/credentials.json 或 SKILLHUB_TOKEN）")
    else:
        bad("未登录。先在 PowerShell 执行 `skillhub login --key skh_xxx`，token 在 skillhub.cn 设置页生成")
    rc, out = run_cli(["--version"])
    if rc == 0:
        ok("CLI 可用：%s" % out.strip().splitlines()[0])
    else:
        warn("CLI 自检返回 %s：%s" % (rc, out[:200]))
    try:
        req = urllib.request.Request(API + "/categories", headers={"User-Agent": "ym-skillhub"})
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.load(r)
        # 接口实际结构：{"count": 13, "items": [...]}；兼容另两种字段名
        items = data.get("items") or data.get("categories") or data.get("data") or []
        n = len(items) if isinstance(items, list) else int(data.get("count") or 0)
        ok("平台接口连通（categories 返回 %d 项）" % n)
    except Exception as e:  # noqa: BLE001
        warn("平台接口不可达：%r（发布前需联网）" % (e,))
    return 0 if R.errors == 0 else 2


# ══════════════════════════════════════════════════════════════════════════
# 检查：平台字段
# ══════════════════════════════════════════════════════════════════════════
def check_fields(fm, skill_dir):
    """返回 (blocking_count, warn_count)。"""
    b = w = 0
    say()
    say("① 平台字段（CLI 只硬校验 slug / version / displayName，其余是静默失败）")
    before = R.errors + R.warnings

    slug = fm.value("slug") or fm.value("name")
    if not fm.value("slug"):
        warn("缺 `slug` —— 平台 CLI 会硬报错「SKILL.md 缺少 slug」"); w += 1
    if slug and not SLUG_RE.match(slug):
        bad("`slug` 不是 kebab-case：%s" % slug); b += 1
    name = fm.value("name")
    if slug and name and slug != name:
        warn("`slug`(%s) 与 `name`(%s) 不一致，建议统一" % (slug, name)); w += 1
    if name and name != skill_dir.name:
        warn("`name`(%s) 与目录名(%s) 不一致 —— 绑 GitHub 发布时 slug 取自 `name`" % (name, skill_dir.name)); w += 1

    ver = fm.value("version")
    if not ver:
        bad("缺 `version`（语义化版本号），CLI 硬报错"); b += 1
    elif not SEMVER_RE.match(ver):
        bad("`version` 不是合法 SemVer：%s" % ver); b += 1

    dn = fm.value("displayName")
    if not dn:
        bad("缺 `displayName`（驼峰）。缺了不报错，商店列表里直接显示英文 slug"); b += 1
    elif " · " in dn:
        warn("`displayName` 含「 · 」功能后缀，展示名建议保持干净"); w += 1

    if not fm.value("summary"):
        warn("缺 `summary` —— 商店列表摘要为空"); w += 1

    if not fm.value("description_zh") or not fm.value("description_en"):
        warn("缺 `description_zh` / `description_en` —— 上架会被打回"); w += 1

    cat = fm.value("category")
    if not cat:
        warn("缺 `category` —— 上架后显示「未分类」（且 CLI 传不上去，只能网页 dashboard 改）"); w += 1
    elif cat not in CATEGORIES:
        bad("`category` 不在平台 13 枚举内：%s（`development` 应写 `dev-programming`）" % cat); b += 1

    tags = fm.list_value("tags")
    if not tags:
        warn("缺 `tags` —— 商店标签为空，搜不到"); w += 1
    if R.errors + R.warnings == before:
        ok("齐备：slug / version / displayName / summary / tags / category / description 三件套")
    return b, w


def check_parser_quirks(fm):
    """平台解析器只认 `key: 值` 与 `key: [a, b]`，这三种写法会静默丢内容。
    只检查 PLATFORM_KEYS，本机字段不动。"""
    b = w = 0
    say()
    say("② 平台解析器怪癖（这几种写法平台读出来是空的/错的）")
    hits = 0
    for e in fm.entries:
        k, inline = e["key"], e["inline"]
        if k not in PLATFORM_KEYS:
            continue
        if inline in (">-", ">", "|", "|-", "|+", ">+"):
            warn("`%s` 用了块标量（%s）—— 平台会读成字面量两个字符「%s」" % (k, inline, inline)); w += 1; hits += 1
        elif not inline and e["cont"]:
            warn("`%s` 用了多行列表 —— 平台会读空" % k); w += 1; hits += 1
        elif inline.startswith("[") and not re.match(r"^\[\s*([^\[\]]*)\]\s*$", inline):
            warn("`%s` 内联列表没在一行内闭合" % k); w += 1; hits += 1
        elif not inline:
            continue
        if not (len(inline) >= 2 and inline[0] == inline[-1] and inline[0] in ("'", '"')):
            if re.search(r"\s+#\s", inline):
                warn("`%s` 行尾有 `#` 注释 —— 平台不剥注释，会拼进字段值" % k); w += 1; hits += 1
    if not hits:
        ok("没有块标量 / 多行列表 / 行尾注释")
    else:
        info("跑 `fix` 可自动把这 %d 处规整成平台能读的形态" % hits)
    return b, w


def check_files(skill_dir):
    """扩展名白名单。平台扫描仓库时逐个文件校验，命中一个就整单拒收。"""
    b = 0
    say()
    say("③ 文件类型白名单（命中非纯文本即整单拒收）")
    bad_files, dot_files, others = [], [], []
    for p in sorted(skill_dir.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(skill_dir)
        if rel.parts and rel.parts[0] == ".git":
            continue
        ext = p.suffix.lstrip(".").lower()
        if ext in TEXT_EXT:
            if p.name.startswith(".") and p.parent == skill_dir:
                dot_files.append(rel)
            continue
        (dot_files if p.name.startswith(".") else others).append(rel)

    if dot_files:
        for rel in dot_files:
            bad("非白名单（点开头，平台不收）：%s" % rel)
            b += 1
        info("对策：git 元数据迁到 `.git/info/exclude` 与 `.git/info/attributes`（行为一致，但不在仓库里）")
    if others:
        for rel in others:
            bad("非白名单扩展名：%s" % rel)
            b += 1
        info("对策：图标输出到技能目录之外；模板改 `.md` 后缀；附件/zip 放目录外")
    if not dot_files and not others:
        ok("目录内全部是纯文本文件")
    return b


def check_market(skill_dir, run_dry=True, run_audit=True):
    """复用 ym-skill-generator 的两把尺子：本地体检 + CLI dry-run。"""
    b = 0
    say()
    say("④ 平台侧预检")

    audit = HOME / ".workbuddy" / "skills" / "ym-skill-generator" / "scripts" / "audit_skill.py"
    if run_audit and audit.exists():
        rc, out = _run_py([str(audit), str(skill_dir), "--market", "--hide-p2"])
        tail = [l for l in out.splitlines() if l.strip()]
        summary = next((l for l in tail if "P0" in l and "P1" in l), tail[-1] if tail else "")
        if rc == 0:
            ok("本地市场体检通过：%s" % summary.strip())
        elif rc == 1:
            warn("本地市场体检有 P1：%s" % summary.strip())
            for l in tail[-12:]:
                info(l.strip())
            b = 0
        else:
            bad("本地市场体检有 P0：%s" % summary.strip())
            for l in tail[-12:]:
                info(l.strip())
            b += 1
    elif run_audit:
        info("未装 ym-skill-generator，跳过本地体检（可选）")

    if run_dry:
        rc, out = run_cli(["publish", str(skill_dir), "--dry-run"])
        line = next((l.strip() for l in out.splitlines() if "Dry-run" in l or "dry" in l.lower()), "")
        if rc == 0:
            ok("CLI 发布预检通过：%s" % (line or "ok"))
        else:
            bad("CLI 发布预检失败：")
            for l in out.splitlines()[-10:]:
                info(l.strip())
            b += 1
    return b


def _run_py(args, timeout=180):
    try:
        p = subprocess.run([find_python()] + args, capture_output=True, timeout=timeout,
                           env=cli_env())
        return p.returncode, ((p.stdout or b"") + (p.stderr or b"")).decode("utf-8", "replace")
    except Exception as e:  # noqa: BLE001
        return 3, repr(e)


# ══════════════════════════════════════════════════════════════════════════
# fix
# ══════════════════════════════════════════════════════════════════════════
def cmd_fix(args):
    fm, skill_dir, md = load_skill(args.skill_dir)
    if fm is None:
        bad("找不到 %s/SKILL.md" % skill_dir); return 2
    say("自动补齐平台字段：%s" % skill_dir)
    changes = []

    # 1) 把会被平台读错的写法先规整掉（必须在取值之前做）
    #    只动 PLATFORM_KEYS —— `trigger` 等多行列表是 WorkBuddy 本机字段，压成单行会弄坏本机技能
    for e in list(fm.entries):
        k, inline = e["key"], e["inline"]
        if k not in PLATFORM_KEYS:
            continue
        need = False
        if inline in (">-", ">", "|", "|-", "|+", ">+") or (not inline and e["cont"]):
            need = True
        if need:
            if e["cont"] and e["cont"][0].startswith("- "):
                items = [x[2:].strip() for x in e["cont"]]
                fm.set(k, "[%s]" % ", ".join(items))
                changes.append("%s：多行列表 → 内联列表 [%d 项]" % (k, len(items)))
            else:
                joined = fm.value(k).replace('"', "'").strip()
                fm.set(k, _quote(joined))
                changes.append("%s：块标量 → 单行" % k)
        elif inline and not (len(inline) >= 2 and inline[0] == inline[-1] and inline[0] in ("'", '"')):
            if re.search(r"\s+#\s", inline):
                clean = re.sub(r"\s+#\s.*$", "", inline).strip()
                fm.set(k, _quote(clean))
                changes.append("%s：去掉行尾注释" % k)

    # 2) 补齐平台字段
    name = fm.value("name") or fm.value("slug")
    if not fm.value("slug") and name:
        fm.set("slug", name); changes.append("slug ← name（%s）" % name)

    if not fm.value("displayName"):
        dn = fm.value("display_name") or fm.value("display_name_en") or name
        dn = re.split(r"\s*[·|]\s*", dn)[0].strip()      # 去掉「 · 功能列举」
        fm.set("displayName", _quote(dn)); changes.append("displayName ← display_name（%s）" % dn)

    if not fm.value("summary"):
        s = fm.value("description_zh") or fm.value("description")
        s = " ".join(s.split())
        if len(s) > 120:
            s = s[:117].rstrip() + "..."
        fm.set("summary", _quote(s)); changes.append("summary ← description_zh")

    if not fm.list_value("tags"):
        tags = fm.list_value("trigger") or fm.list_value("keywords")
        if not tags:
            tags = [x for x in re.split(r"[-_]", name or "") if len(x) > 1][:3]
        tags = tags[:8]
        if tags:
            fm.set("tags", "[%s]" % ", ".join(tags))
            changes.append("tags ← trigger（%d 项）" % len(tags))

    # 3) category：只能提示，不能猜
    cat = fm.value("category")
    if args.category:
        if args.category not in CATEGORIES:
            bad("--category %s 不在平台 13 枚举内：%s" % (args.category, ", ".join(CATEGORIES))); return 2
        if cat != args.category:
            fm.set("category", args.category); changes.append("category：%s → %s" % (cat or "空", args.category))

    if changes:
        fm.save()
        for c in changes:
            ok(c)
        say("  已写回：%s" % md)
    else:
        ok("无需改动，字段已齐备")

    if not args.category and cat and cat not in CATEGORIES:
        bad("category = %s 不在平台 13 枚举内，用 --category 指定（如 dev-programming）" % cat)
        info("分类走 CLI 传不上去，改这里只是让仓库里的声明正确；线上分类仍需网页 dashboard 改")
    return 0 if R.errors == 0 else 2


def _quote(v):
    v = (v or "").replace('"', "'").replace("\n", " ").strip()
    if any(ch in v for ch in ":[]{}#,") or v != v.strip():
        return '"%s"' % v
    return v


# ══════════════════════════════════════════════════════════════════════════
# bump
# ══════════════════════════════════════════════════════════════════════════
def cmd_bump(args):
    fm, skill_dir, md = load_skill(args.skill_dir)
    if fm is None:
        bad("找不到 %s/SKILL.md" % skill_dir); return 2
    cur = fm.value("version") or "0.0.0"
    if args.set_version:
        new = args.set_version
    else:
        m = re.match(r"^(\d+)\.(\d+)\.(\d+)", cur)
        if not m:
            bad("当前 version 不是 SemVer：%s（用 --set X.Y.Z 指定）" % cur); return 2
        a, b, c = (int(x) for x in m.groups())
        if args.major:
            a, b, c = a + 1, 0, 0
        elif args.minor:
            a, b, c = a, b + 1, 0
        else:
            c += 1
        new = "%d.%d.%d" % (a, b, c)
    if not SEMVER_RE.match(new):
        bad("目标版本号不是合法 SemVer：%s" % new); return 2
    if new == cur:
        ok("版本未变：%s" % cur); return 0
    fm.set("version", new)
    fm.save()
    ok("版本：%s → %s" % (cur, new))
    return 0


# ══════════════════════════════════════════════════════════════════════════
# publish / status
# ══════════════════════════════════════════════════════════════════════════
def cmd_publish(args):
    fm, skill_dir, md = load_skill(args.skill_dir)
    if fm is None:
        bad("找不到 %s/SKILL.md" % skill_dir); return 2
    slug = fm.value("slug") or fm.value("name")
    if not has_credential():
        bad("未登录。先在 PowerShell 跑 `skillhub login --key skh_xxx`（token 在 skillhub.cn 设置页生成）")
        return 3
    argv = ["publish", str(skill_dir)]
    if args.changelog:
        argv += ["--changelog", args.changelog]
    if args.version:
        argv += ["--version", args.version]
    if args.dry_run:
        argv.append("--dry-run")
    say("发布：%s@%s%s" % (slug, fm.value("version"), "（dry-run，不发 HTTP）" if args.dry_run else ""))
    rc, out = run_cli(argv)
    for l in out.splitlines():
        if l.strip():
            say("  " + l.strip())
    if rc != 0 or "✓" not in out:
        bad("发布失败（退出码 %s）" % rc)
        return 2
    ok("平台已受理。注意：`✓ Published` ≠ 已上线 —— 线上字段分三档更新，跑 `status` 复核")
    return 0


def _get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "ym-skillhub", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)


def cmd_status(args):
    slug = args.slug
    say("线上状态：%s" % slug)
    try:
        d = _get_json("%s/skills/%s" % (API, slug))
    except urllib.error.HTTPError as e:
        bad("查询失败 HTTP %s（slug 可能还没发布过）" % e.code); return 2
    except Exception as e:  # noqa: BLE001
        bad("查询失败：%r（需要联网）" % (e,)); return 3

    latest = (d.get("latestVersion") or {})
    sk = (d.get("skill") or {})
    tags = list((sk.get("tags") or {}).keys())
    say("  最新已上线版本 : %s" % (latest.get("version") or "—"))
    say("  分类（category）: %s   ← CLI 改不动，只能网页 dashboard 改" % (sk.get("category") or "—"))
    say("  摘要            : %s" % ((sk.get("summary_zh") or sk.get("summary") or "—")[:80]))
    say("  标签            : %s" % (", ".join(tags) if tags else "（空）"))
    say("  版本计数        : %s" % ((sk.get("stats") or {}).get("versions") or "—"))

    versions = []
    try:
        v = _get_json("%s/skills/%s/versions?page=1&pageSize=50" % (API, slug))
        versions = v.get("versions") or []
    except Exception as e:  # noqa: BLE001
        warn("版本列表查询失败：%r" % (e,))
    if versions:
        say("  已过审版本      : %s" % ", ".join(str(x.get("version")) for x in versions))

    dl = ""
    try:
        req = urllib.request.Request("%s/download?slug=%s" % (API, slug), headers={"User-Agent": "ym-skillhub"})
        with urllib.request.urlopen(req, timeout=25) as r:
            cd = r.headers.get("Content-Disposition", "")
        m = re.search(r'filename\*?=(?:UTF-8\'\')?"?([^";]+)', cd)
        dl = m.group(1) if m else ""
        if dl:
            say("  下载包          : %s" % dl)
    except Exception:  # noqa: BLE001
        pass

    # ── 判定 ──
    say()
    expect = args.expect
    online = [str(x.get("version")) for x in versions]
    if expect:
        if expect in online or (latest.get("version") == expect and not versions):
            ok("%s 已过审上线" % expect)
        elif (sk.get("stats") or {}).get("versions"):
            warn("%s 尚未出现在已过审版本列表 —— 还在审核中（内容合规 + 科恩漏洞扫描 + 云鼎 AI 安全评估）"
                 % expect)
        else:
            warn("%s 没查到，发布可能未成功" % expect)
    if sk.get("category") and sk["category"] not in ("dev-programming",):
        info("提醒：若该技能应属「开发编程」，请去 https://skillhub.cn/dashboard 手动改分类")
    return 0


# ══════════════════════════════════════════════════════════════════════════
# release
# ══════════════════════════════════════════════════════════════════════════
def cmd_release(args):
    global R
    fm, skill_dir, md = load_skill(args.skill_dir)
    if fm is None:
        bad("找不到 %s/SKILL.md" % skill_dir); return 2

    say("═══ 1/5 自动补齐平台字段 ═══")
    cmd_fix(argparse.Namespace(skill_dir=str(skill_dir), category=args.category))

    if args.fix_only:
        return 0 if R.errors == 0 else 2

    say()
    say("═══ 2/5 版本递增 ═══")
    cmd_bump(argparse.Namespace(skill_dir=str(skill_dir), set_version=args.set_version,
                                major=args.major, minor=args.minor))

    fm = FM(md)                      # 重新读，拿新版本号
    reset_counter()

    say()
    say("═══ 3/5 发布预检 ═══")
    check_fields(fm, skill_dir)
    check_parser_quirks(fm)
    check_files(skill_dir)
    pre_b = check_market(skill_dir, run_dry=not args.skip_dry, run_audit=not args.skip_audit)

    if pre_b and not args.force:
        say()
        bad("预检有 %d 项阻断，已中止发布（确认无碍可加 --force）" % pre_b)
        return 2

    say()
    say("═══ 4/5 发布 ═══")
    rc = cmd_publish(argparse.Namespace(skill_dir=str(skill_dir), changelog=args.changelog,
                                        version=args.version or None, dry_run=args.dry_run))
    if args.dry_run:
        return rc

    say()
    say("═══ 5/5 复核线上状态 ═══")
    slug = fm.value("slug") or fm.value("name")
    try:
        cmd_status(argparse.Namespace(slug=slug, expect=fm.value("version")))
    except SystemExit:
        pass
    say()
    info("线上字段分三档：tags 秒级生效；version/summary/描述 随审核（实测约 3 分钟）；"
         "category 走 CLI 永远不变，只能网页 dashboard 改")
    return rc


# ══════════════════════════════════════════════════════════════════════════
def cmd_check(args):
    fm, skill_dir, md = load_skill(args.skill_dir)
    if fm is None:
        bad("找不到 %s/SKILL.md" % skill_dir); return 2
    say("发布预检：%s" % skill_dir)
    b1, _ = check_fields(fm, skill_dir)
    b2, _ = check_parser_quirks(fm)
    b3 = check_files(skill_dir)
    b4 = check_market(skill_dir, run_dry=not args.skip_dry, run_audit=not args.skip_audit)
    say()
    total_b = b1 + b2 + b3 + b4
    if total_b:
        bad("共 %d 项阻断、%d 项告警 —— 先跑 `fix`，再重跑 `check`" % (total_b, R.warnings))
        return 2
    if R.warnings:
        warn("无阻断，%d 项告警（不拦发布）" % R.warnings)
        return 1
    ok("全部通过，可以发布")
    return 0


def main():
    ap = argparse.ArgumentParser(description="SkillHub 技能创建 / 更新一条龙", formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("doctor", help="环境自检")
    p.set_defaults(func=cmd_doctor)

    p = sub.add_parser("check", help="发布预检")
    p.add_argument("skill_dir")
    p.add_argument("--skip-dry", action="store_true", help="跳过 CLI dry-run")
    p.add_argument("--skip-audit", action="store_true", help="跳过本地市场体检")
    p.set_defaults(func=cmd_check)

    p = sub.add_parser("fix", help="自动补齐平台字段")
    p.add_argument("skill_dir")
    p.add_argument("--category", help="显式指定分类（13 枚举之一）")
    p.set_defaults(func=cmd_fix)

    p = sub.add_parser("bump", help="递增版本号")
    p.add_argument("skill_dir")
    p.add_argument("--patch", action="store_true", help="第三位 +1（默认）")
    p.add_argument("--minor", action="store_true", help="第二位 +1")
    p.add_argument("--major", action="store_true", help="第一位 +1")
    p.add_argument("--set", dest="set_version", help="直接指定版本号")
    p.set_defaults(func=cmd_bump)

    p = sub.add_parser("publish", help="发布到 SkillHub")
    p.add_argument("skill_dir")
    p.add_argument("--changelog", default="", help="本次变更说明")
    p.add_argument("--version", help="覆盖 SKILL.md 里的 version")
    p.add_argument("--dry-run", action="store_true", help="只做本地预检，不发 HTTP")
    p.set_defaults(func=cmd_publish)

    p = sub.add_parser("status", help="查线上状态")
    p.add_argument("slug")
    p.add_argument("--expect", help="期望上线的版本号，用它判定是否已过审")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("release", help="一条龙：fix → bump → check → publish → status")
    p.add_argument("skill_dir")
    p.add_argument("--changelog", default="", help="本次变更说明")
    p.add_argument("--category", help="显式指定分类")
    p.add_argument("--version", help="覆盖版本号（传给 CLI）")
    p.add_argument("--set", dest="set_version", help="直接设定版本号，不做递增")
    p.add_argument("--major", action="store_true")
    p.add_argument("--minor", action="store_true")
    p.add_argument("--dry-run", action="store_true", help="只预检不发布")
    p.add_argument("--fix-only", action="store_true", help="只做 fix，不 bump 不发布")
    p.add_argument("--skip-dry", action="store_true")
    p.add_argument("--skip-audit", action="store_true")
    p.add_argument("--force", action="store_true", help="预检有阻断也继续发布")
    p.set_defaults(func=cmd_release)

    args = ap.parse_args()
    if args.cmd == "doctor":
        return cmd_doctor(args)
    rc = args.func(args)
    return rc or 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
