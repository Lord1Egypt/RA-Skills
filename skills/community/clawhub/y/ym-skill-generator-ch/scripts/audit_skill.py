#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_skill.py — 技能打包前体检器

对目标技能目录做检查，输出分级结论（同类问题自动聚合，不再逐行刷屏）：

    P0  阻断项 —— 禁止打包（真实凭据、破坏性操作）
    P1  警告项 —— 建议修复后再打包（硬编码绝对路径、外部依赖、引用缺失、配置无模板）
    P2  提示项 —— 可选优化与知情项（命名规范、外部副作用、体积、运行时数据）

用法:
    python scripts/audit_skill.py <技能目录> [--json] [--hide-p2] [--no-color] [--samples N]
    python scripts/audit_skill.py <技能目录> --ignore-rule 引用缺失 [--ignore-rule ...]
    python scripts/audit_skill.py --explain 引用缺失        # 这条规则判什么、怎么改、怎么放行
    python scripts/audit_skill.py --selftest                # 自检：用带病样例验证体检器本身没坏
    python scripts/audit_skill.py <技能目录> --fix [--write] # 半自动修复（默认只打印建议）

退出码:
    0 通过 | 1 有 P1 | 2 有 P0 | 3 参数/目录错误 | 4 写入/打包失败
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True          # 体检不该在技能目录里留 __pycache__
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _friendly import backup_root, die, explain_exit, use_utf8_stdout  # noqa: E402

# ------------------------------------------------------------------ 常量

TEXT_EXT = {
    ".md", ".markdown", ".txt",
    ".py", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".vue",
    ".json", ".jsonc", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf", ".properties",
    ".sh", ".bash", ".zsh", ".ps1", ".bat", ".cmd",
    ".html", ".htm", ".css", ".scss", ".sql", ".xml",
    ".env", ".example", ".template", ".sample", ".dist",
    ".java", ".go", ".rs", ".rb", ".php",
}
CODE_EXT = {".py", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".sh", ".bash", ".zsh",
            ".ps1", ".bat", ".cmd", ".vue", ".go", ".rs", ".rb", ".php", ".java"}
DOC_EXT = {".md", ".markdown", ".txt"}
TEMPLATE_HINT = (".example", ".template", ".sample", ".dist")

JUNK_DIRS = {
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".tox",
    "node_modules", ".venv", "venv", "env", ".idea", ".vscode", ".git", ".svn", ".hg",
    "dist", "build", ".cache", ".tmp", "tmp", ".egg-info",
}
JUNK_SUFFIX = {".pyc", ".pyo", ".pyd", ".class", ".o", ".obj", ".log", ".tmp",
               ".bak", ".swp", ".orig", ".rej", ".ds_store"}
JUNK_FILES = {"Thumbs.db", "desktop.ini", "nul", "con"}
RUNTIME_DIR_HINTS = {"profile", "profiles", "user_data", "user-data", "output", "outputs",
                     "logs", "cache", "caches", "runtime", "temp", "storage"}
BIG_FILE_BYTES = 5 * 1024 * 1024

STDIO = getattr(sys, "stdlib_module_names", set())

# ------------------------------------------------------------------ 正则

_ASCII_PATH_CHAR = r"[A-Za-z0-9_().\-\\/+~$@#%&=:,]"
# 路径主体：普通字符照收；括号/方括号/花括号只有后面还接路径字符时才收（避免吃掉句子收尾的括号）；
# 空格只在后面接 ASCII 路径字符时才收（避免把后面的中文正文一并吞掉）。
_PATH_BODY = (r"(?:[^\s\"'`<>|,;)\]}{，。；、）】]"
              r"|[)\]}](?=[A-Za-z0-9_().\\/])"
              r"|\s(?=[A-Za-z0-9_().\\/-]))*")
ABS_PATH_RULES = [
    # 负向后视排除 `%`：格式化串 `r"^%s:\s*..."` 里的 `s:\` 会被当成盘符路径误判。
    # 同理排除 `//` 前缀外的 URL 场景（https:// 的 `s:` 前一个是词字符，已被 (?<!\w) 挡掉）。
    ("windows 盘符路径", re.compile(r"(?<![\w%])([A-Za-z]:[\\/]" + _PATH_BODY + r")")),
    ("UNC 网络路径", re.compile(r"(?<![\w\\:)\]}])(\\\\[A-Za-z0-9_.\-]+(?:\\[A-Za-z0-9_$.\- ()]+)*)")),
    ("POSIX 家目录路径", re.compile(
        r"(?<![\w:!#])(/(?:home|Users|root|media|Volumes|mnt/[a-zA-Z])/[^\s\"'`<>|,;)\]}{，。；、）】]*)")),
]

SECRET_KEYWORD = re.compile(
    r"(?i)\b(password|passwd|pwd|secret|token|api[_-]?key|apikey|access[_-]?key|"
    r"app[_-]?key|app[_-]?secret|client[_-]?secret|private[_-]?key|access[_-]?token|"
    r"auth[_-]?token|credential|passphrase|cookie|session[_-]?id|"
    r"密码|密钥|口令|令牌|凭据)\b"
)
# 赋值形式：key = value  /  "key": "value"
ASSIGN_RE = re.compile(r"(?P<key>[\w\u4e00-\u9fa5_\-]+)\s*[:=]\s*(?P<val>.+?)\s*[,;]?\s*$")
QUOTED_LITERAL = re.compile(r"^[\"'](?P<v>[^\"']{4,})[\"']$")
BARE_LITERAL = re.compile(r"^[A-Za-z0-9_\-\.@$#%&*+=/]{6,}$")
# 纯属性链（resp.result.sessionId、obj?.a.b），不可能是写死的密钥字面量
PROPERTY_CHAIN = re.compile(r"^[\w$]+(?:\??\.[\w$]+)+$")

SECRET_VALUE_RULES = [
    ("JWT", re.compile(r"\beyJ[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{4,}")),
    ("OpenAI Key", re.compile(r"\bsk-[A-Za-z0-9]{20,}")),
    ("AWS AK", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("GitHub Token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}")),
    ("Slack Token", re.compile(r"\bxox[baprs]-[A-Za-z0-9\-]{10,}")),
    ("私钥块", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
]
LONG_HEX = re.compile(r"\b[0-9a-fA-F]{32,}\b")

# 高危操作（P0）
DANGER_P0 = [
    ("递归删除根/家目录", re.compile(r"rm\s+-[a-zA-Z]*[rR][a-zA-Z]*f?\s+(/|~|\$HOME|\*)")),
    ("强制格式化/批量删除", re.compile(r"(?i)\bformat\s+[a-zA-Z]:|\bdel\s+/[sS]\s+/[qQ]|\brd\s+/[sS]")),
    ("远程脚本直灌 shell", re.compile(r"curl[^\n|]*\|\s*(sudo\s+)?(ba)?sh")),
    ("动态执行外部输入", re.compile(r"(?<![\w.])(eval|exec)\s*\(\s*(input|sys\.argv|request|body)")),
    ("写入系统关键文件", re.compile(r"(?i)\b(WINDIR|System32)\b.*\b(write|open|copy)|/etc/(passwd|shadow)")),
]
# 需人工确认范围的操作（P1）
DANGER_P1 = [
    ("递归删除目录", re.compile(r"shutil\.rmtree\s*\(|os\.removedirs?\s*\(|fs\.rmSync\s*\(")),
    # 前缀 (?<!#!) 必须罩住两个分支：否则内嵌在字符串里的 shebang
    # （`SETUP_PY = '''#!/usr/bin/env python3`）会被当成引用系统目录。
    ("引用系统目录", re.compile(r"(?i)(?<!#!)(?:[A-Za-z]:\\Windows\b|/usr/(?:bin|lib)\b)")),
    ("终止进程", re.compile(r"(?i)\btaskkill\b|\bkillall\b|\bpkill\b")),
]

SIDE_EFFECT_RULES = [
    ("发送消息 / 调用 webhook", re.compile(r"(?i)(send_single_message|send_group_message|sendMessage|webhook|机器人发消息|发群消息)")),
    ("发送邮件", re.compile(r"(?i)(smtplib|sendmail|send_mail|SMTP\()")),
    ("上传文件到外部", re.compile(r"(?i)((?:post|put)\s*\([^)\n]{0,200}?\bfiles\s*=|upload_media|put_object|上传到)")),
    ("驱动浏览器", re.compile(r"(?i)(selenium|playwright|--headless|CDP|chrome\.exe|msedge\.exe|debugging-port)")),
    ("模拟键鼠 / 剪贴板", re.compile(r"(?i)(pyautogui|keyboard\.press|pyperclip|mouse\.click|SendKeys)")),
    ("写入外部系统", re.compile(r"(?i)(UPDATE\s+[A-Z_]+\s+SET|INSERT\s+INTO|commit\(\)|push\(\))")),
]

PY_IMPORT = re.compile(r"^\s*(?:import\s+([A-Za-z_][\w.]*)|from\s+([A-Za-z_][\w.]*)\s+import\b)", re.M)
JS_IMPORT = re.compile(r"""(?:require\s*\(\s*['"]([^'"]+)['"]\s*\)|from\s*['"]([^'"]+)['"])""")
PYPI_ALIAS = {
    "PIL": "Pillow", "bs4": "beautifulsoup4", "yaml": "PyYAML", "cv2": "opencv-python",
    "fitz": "PyMuPDF", "docx": "python-docx", "dotenv": "python-dotenv", "serial": "pyserial",
    "sklearn": "scikit-learn", "skimage": "scikit-image", "dateutil": "python-dateutil",
    "OpenSSL": "pyOpenSSL", "jwt": "PyJWT", "win32com": "pywin32", "win32api": "pywin32",
    "pptx": "python-pptx", "edge_tts": "edge-tts", "moviepy": "moviepy",
    "websocket": "websocket-client", "Crypto": "pycryptodome", "qrcode": "qrcode",
    "moviepy.editor": "moviepy", "imageio_ffmpeg": "imageio-ffmpeg",
}
# 仅收录不会误伤普通英文词的外部可执行文件
EXTERNAL_TOOLS = {
    "ffmpeg": "音视频合成", "ffprobe": "音视频探测", "edge-tts": "微软 TTS 配音",
    "tesseract": "OCR 引擎", "pandoc": "文档转换", "soffice": "LibreOffice",
    "libreoffice": "LibreOffice", "wkhtmltopdf": "HTML 转 PDF", "magick": "ImageMagick",
    "xelatex": "LaTeX", "unoconv": "unoconv", "pdftotext": "poppler",
    "msedge.exe": "Edge 浏览器", "chrome.exe": "Chrome 浏览器",
    "gswin64c": "Ghostscript", "gswin32c": "Ghostscript",
}
FONT_HINT = re.compile(r"(?i)(ImageFont\.truetype|[A-Za-z_]*font[A-Za-z_]*\s*[:=]\s*[^\s]+\.(ttf|otf|ttc)|msyh|simhei|simsun|PingFang)")

# 引用提取
REF_PATTERNS = [
    re.compile(r"\[[^\]]*\]\(([^)\s]+)\)"),                      # Markdown 链接
    re.compile(r"`([A-Za-z0-9_./\-]+\.(?:py|js|mjs|cjs|ts|json|md|txt|ya?ml|toml|sh|ps1|bat|png|jpe?g|svg|csv|xlsx|docx|html|css))`"),
    re.compile(r"(?:python3?|node|bash|sh|pwsh)\s+(?:-[A-Za-z\-]+\s+)*([A-Za-z0-9_./\-]+\.(?:py|js|mjs|cjs|ts|sh|ps1|bat))"),
    re.compile(r"`((?:scripts|references|assets|config|templates|src|bin)/[^`\s]+)`"),
]

# 正文里显式标注了「运行时产物」的行，其中的路径是运行后才生成的文件
# （如 avatars/expert.png、output/report.pdf），不是技能自带依赖，不该判引用缺失。
OUTPUT_HINT_RE = re.compile(r"运行时产物|输出文件|产物文件|运行后生成|由脚本生成|生成的")

PLACEHOLDER_HINTS = (
    "your_", "your-", "your", "xxx", "example", "sample", "placeholder", "changeme",
    "change_me", "todo", "fixme", "none", "null", "true", "false", "os.environ",
    "getenv", "process.env", "input(", "getpass", "***", "****", "{{", "${", "<", ">",
    "n/a", "dummy", "占位", "请填", "示例",
)

# 「规则定义行不是规则命中」—— 扫描器/校验类技能自身会包含它要搜索的字面量，
# 这些行必须跳过，否则体检器会把自己的规则表当成违规代码。
PATTERN_DEF_MARKERS = ("re.compile(", "RegExp(", "new RegExp", "Pattern.compile(", "regex::Regex")

# 规则表还有一种写法是**字典字面量**（`"msedge.exe": "Edge 浏览器",`）。
# 上面那组标记只认 re.compile(，字典项一律漏网 —— 本技能自己就因此被判「驱动浏览器」。
# 判据：命中词在该行里是被引号包住的字典键（`"词":` ）。真实代码不会这么写。
DICT_KEY_LITERAL_RE = re.compile(r"""["']([^"'\n]{1,60})["']\s*:\s*["']""")

# 低价值噪音：默认不逐条打印（仍计数，加 --show-noise 才展开）。
# 「示例路径里没有这个文件」是正常的，逐条刷屏只会让人以为体检器在乱报。
NOISE_RULES = {"约定/示例路径", "疑似产物路径"}


def is_rule_table_hit(line: str, hit: str) -> bool:
    """命中词是否只是规则表里被列出来的字面量，而不是真的在用。"""
    if not hit:
        return False
    for m in DICT_KEY_LITERAL_RE.finditer(line):
        if m.group(1).strip() == hit.strip():
            return True
    return False

# ------------------------------------------------------------------ 工具


def read_text(path: Path, limit: int = 2_000_000):
    try:
        if path.stat().st_size > limit:
            return None
        raw = path.read_bytes()
        if b"\x00" in raw[:4096]:
            return None
        return raw.decode("utf-8", errors="replace")
    except Exception:
        return None


def is_cjk(s: str) -> bool:
    return bool(re.search(r"[\u4e00-\u9fa5]", s))


def looks_like_placeholder(value: str, soft: bool = True) -> bool:
    s = value.strip().strip("\"'`,;:)").strip()
    low = s.lower()
    if not s:
        return True
    if low in {"", "none", "null", "true", "false", "n/a", "na", "0", "1"}:
        return True
    if any(h in low for h in PLACEHOLDER_HINTS):
        return True
    # 纯中文短值在文档/模板里一律视为字段说明，如 "OA密码"
    if soft and is_cjk(s) and len(s) <= 10 and not re.search(r"\d", s):
        return True
    return False


def mask(s: str) -> str:
    """脱敏：报告里永不回显完整凭据，只留首尾便于定位。"""
    s = s.strip()
    if len(s) <= 6:
        return s[:1] + "***"
    return s[:4] + "***" + s[-2:]


def is_literal_secret_value(val: str) -> bool:
    """只把「写死的字面量」当凭据，排除变量、函数调用、表达式。"""
    v = val.strip().rstrip(",;")
    m = QUOTED_LITERAL.match(v)
    if m:
        return len(m.group("v").strip()) >= 4 and not looks_like_placeholder(m.group("v"), soft=False)
    if BARE_LITERAL.match(v):
        return True
    return False


def is_identifier_reference(key: str, val: str) -> bool:
    """右侧是属性访问、或与左侧同名的标识符 → 是引用/透传，不是写死的密钥。

    典型误报：`const sid = resp.result.sessionId;`（属性链）
              `sessionId = sessionId`（自赋值）
    两者都不可能携带字面量密钥，误判成 P0 会让报告失去可信度。
    """
    v = val.strip().rstrip(",;").strip()
    if not v or "'" in v or '"' in v:
        return False          # 带引号的才是字面量，不能放过
    if PROPERTY_CHAIN.match(v):
        return True
    norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())   # noqa: E731
    k, vv = norm(key), norm(v)
    return bool(k) and bool(vv) and (k == vv or k in vv)


class Report:
    def __init__(self, ignored_rules=None):
        self._map = {}
        self.ignored_rules = set(ignored_rules or ())
        self.ignored_hits = 0          # 被 --ignore-rule / .skillignore 放过的条数

    def add(self, sev, cat, file, rule, line, sample, hint):
        if rule in self.ignored_rules:
            self.ignored_hits += 1
            return
        key = (sev, cat, str(file), rule)
        f = self._map.get(key)
        if f is None:
            f = {"severity": sev, "category": cat, "file": str(file), "rule": rule,
                 "hint": hint, "hits": []}
            self._map[key] = f
        f["hits"].append({"line": line, "sample": sample})

    def count(self, sev):
        return sum(1 for f in self._map.values() if f["severity"] == sev)

    def findings(self):
        order = {"P0": 0, "P1": 1, "P2": 2}
        return sorted(self._map.values(),
                      key=lambda f: (order[f["severity"]], f["category"], f["file"]))

    @property
    def worst(self):
        if self.count("P0"):
            return "P0"
        if self.count("P1"):
            return "P1"
        return "P2"


# ------------------------------------------------------------------ 遍历


def load_skillignore(root: Path):
    """读技能根的 .skillignore，返回 (glob 列表, 规则名集合)。

    写法：每行一个 glob（如 `icons/*`）；要按规则名放行写 `rule:引用缺失`。

    ⚠️ v2.3.0 之前文档里写了这个文件，代码却没读它 —— 建了也不生效，这是实现与文档不一致的 bug。
    """
    p = root / ".skillignore"
    globs, rules = [], set()
    if not p.exists():
        return globs, rules
    for line in (read_text(p) or "").splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if s.lower().startswith("rule:"):
            rules.add(s[len("rule:"):].strip())
        else:
            globs.append(s.rstrip("/"))
    return globs, rules


def _ignored_by_glob(rel: str, globs) -> bool:
    import fnmatch
    name = Path(rel).name
    for g in globs:
        if fnmatch.fnmatch(name, g) or fnmatch.fnmatch(rel, g) or fnmatch.fnmatch(rel, g + "/*"):
            return True
    return False


def walk_tree(root: Path, ignore_globs=()):
    files, junk_dirs = [], []
    for dirpath, dirnames, filenames in os.walk(root):
        d = Path(dirpath)
        keep = []
        for dn in dirnames:
            if dn in JUNK_DIRS:
                junk_dirs.append(d / dn)
                continue
            if ignore_globs and _ignored_by_glob(str((d / dn).relative_to(root)).replace("\\", "/"), ignore_globs):
                continue
            keep.append(dn)
        dirnames[:] = keep
        for fn in filenames:
            rel = str((d / fn).relative_to(root)).replace("\\", "/")
            if ignore_globs and _ignored_by_glob(rel, ignore_globs):
                continue
            files.append(d / fn)
    return files, junk_dirs


def scan_lines(path: Path):
    """逐行产出 (行号, 行文本)。

    跳过：显式放行行、以及正则规则定义行（规则表里写着要搜的字面量，不是真的在用）。
    """
    text = read_text(path)
    if text is None:
        return
    for i, line in enumerate(text.splitlines(), 1):
        if "skill-audit: ignore" in line:
            continue
        if any(m in line for m in PATTERN_DEF_MARKERS):
            continue
        yield i, line


# ------------------------------------------------------------------ 检查项


def check_structure(root: Path, rep: Report, market: bool = False):
    """返回 SKILL.md 正文内容（供后续检查复用）。"""
    skill_md = root / "SKILL.md"
    if not skill_md.exists():
        rep.add("P0", "结构", root / "SKILL.md", "缺 SKILL.md", 0,
                "目录下没有 SKILL.md", "运行 skill-creator 的 init_skill.py，或手动创建")
        return None

    content = read_text(skill_md) or ""
    if not content.startswith("---"):
        rep.add("P0", "结构", skill_md, "缺 frontmatter", 1,
                "文件未以 --- 开头", "首行必须是 ---，在第二个 --- 之前写 name / description")
        return content

    m = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not m:
        rep.add("P0", "结构", skill_md, "frontmatter 未闭合", 1,
                "找不到闭合的 ---", "补齐 frontmatter 结束标记")
        return content
    fm = m.group(1)

    name_m = re.search(r"^name:\s*(.+)$", fm, re.M)

    if not name_m:
        rep.add("P0", "结构", skill_md, "缺 name", 1, "frontmatter 无 name 字段", "补 name")
    else:
        name = name_m.group(1).strip().strip("\"'")
        if not re.match(r"^[a-z0-9-]+$", name):
            rep.add("P2", "结构", skill_md, "name 命名", 1,
                    "name = %r 非 kebab-case" % name,
                    "本机自用没问题；若要发布到技能市场，name 需改成小写字母+数字+连字符，中文触发词放 description")
        if name != root.name:
            rep.add("P2", "结构", skill_md, "name 与目录不一致", 1,
                    "name(%s) ≠ 目录名(%s)" % (name, root.name),
                    "安装/升级按目录名定位，建议对齐")

    # description 常写成 YAML 折叠块（`description: >-`），必须拼起来再判，否则误报「过短」
    desc = fm_text(fm, "description")
    if not desc:
        rep.add("P0", "结构", skill_md, "缺 description", 1, "frontmatter 无 description", "补 description")
    else:
        if "<" in desc or ">" in desc:
            rep.add("P1", "结构", skill_md, "description 含尖括号", 1,
                    "description 含 < 或 >，打包校验会失败", "换成方括号或中文书名号")
        if len(desc) < 30:
            rep.add("P2", "结构", skill_md, "description 过短", 1,
                    "description 仅 %d 字符" % len(desc),
                    "写清三件事：做什么 / 何时触发 / 触发词")

    if "agent_created" not in fm:
        rep.add("P2", "结构", skill_md, "缺 agent_created", 1,
                "缺少 agent_created: true",
                "加上后 Agent 才能用 skill_manage 后续修改/删除该技能")

    chars = len(content)
    if chars > 30_000:
        rep.add("P1", "结构", skill_md, "SKILL.md 过长", 1,
                "SKILL.md %d 字符，会挤占上下文" % chars,
                "把踩坑细节/字段表/示例搬到 references/，正文只留流程骨架")
    elif chars > 15_000:
        rep.add("P2", "结构", skill_md, "SKILL.md 偏长", 1,
                "SKILL.md %d 字符" % chars, "考虑把细节拆进 references/")

    # 必需目录（存在就必须在正文里说明，否则模型不知道它可用）
    for d in ("scripts", "references", "assets", "templates"):
        if (root / d).is_dir() and d + "/" not in content:
            rep.add("P2", "引用", Path("SKILL.md"), "目录未在正文说明", 0,
                    "存在 %s/ 但 SKILL.md 未提及" % d,
                    "写明每个文件的用途与调用方式，否则模型不知道它可用")

    return content


# ------------------------------------------------- 市场分发合规（--market）

# SkillHub 平台只认这 13 个分类 key（实测 GET https://api.skillhub.cn/api/v1/categories）。
# 传枚举外的值不会报错，但上架后会显示成「未分类」——静默失败，最容易被忽略。
SKILLHUB_CATEGORIES = {
    "pay-skill", "office-efficiency", "content-creation", "dev-programming",
    "data-analysis", "design-media", "ai-agent", "knowledge-management",
    "business-ops", "education", "professional", "it-ops-security", "life-service",
}

# 平台会读、且必须写成单行标量的字段：平台的解析器只支持 `key: value` 与 `key: [a, b]`，
# 写成 `>-` 折叠块或多行列表时会被读成字面量 ">-" 或空串（静默丢失）。
PLATFORM_SCALAR_KEYS = ("description", "description_zh", "description_en", "summary", "tags")

# 市场规范中明确标注「必填」的字段：缺一个就会上架失败
MARKET_REQUIRED = [
    ("description_zh", "缺 description_zh", "补一句话中文介绍，30 字以内；不要照抄 description"),
    ("description_en", "缺 description_en", "补一句话英文介绍，首字母大写、结尾不加句号"),
    ("version",        "缺 version",        "补语义化版本号，如 1.0.0；每次改动后递增"),
    # 平台用驼峰 displayName 当展示名（下划线 display_name 它不认）。
    # 缺了不报错，但商店里会直接显示英文 slug —— 静默失败，必须当必填拦。
    ("displayName",    "缺 displayName",    "补中文展示名（驼峰 displayName；下划线 display_name 平台不认）"),
]
# 规范示例里出现、但未标为必填的字段：缺了不阻断上架，只影响展示效果
# author 归在这一档有实证依据：本机 4 个真实市场技能里只有 1 个带 author（且写在 metadata 下），
# 说明平台并未把它当硬性门槛，因此定级 P2 报警而非 P1 阻断。
MARKET_RECOMMENDED = [
    ("display_name",    "缺 display_name",    "补中文展示名，市场列表里显示这个"),
    ("display_name_en", "缺 display_name_en", "补英文展示名"),
    ("category",        "缺 category",        "补分类；取值须落在平台分类枚举内（见 SKILLHUB_CATEGORIES）"),
    ("author",          "缺 author",          "补署名（个人或团队/公司名）；也可写在 metadata: 之下"),
    ("slug",            "缺 slug",            "补 slug（与 name 一致）；平台 CLI 发布时报错「SKILL.md 缺少 slug」"),
]


def fm_value(fm: str, key: str):
    """取 frontmatter 里的标量值；支持引号与 metadata 下的缩进嵌套，忽略 YAML 块标记（>/|）。

    嵌套是必要的：真实市场技能会把 author / category 写在 metadata: 之下。
    """
    m = re.search(r"^[ \t]*%s:[ \t]*(.*)$" % re.escape(key), fm, re.M)
    if not m:
        return None
    v = m.group(1).strip().strip("\"'").strip()
    return None if v in ("", ">", "|", ">-", "|-") else v


def fm_text(fm: str, key: str):
    """取字段文本值；写成 YAML 块标量时把缩进的后续行拼成一行。

    真实技能里 description 常写成 `description: >-` 折叠块，
    只认单行标量会把它们误判成「缺字段」或「过短」。
    """
    lines = fm.splitlines()
    for i, line in enumerate(lines):
        m = re.match(r"^[ \t]*%s:[ \t]*(.*)$" % re.escape(key), line)
        if not m:
            continue
        val = m.group(1).strip()
        if val and val not in (">", "|", ">-", "|-", ">+", "|+"):
            return val.strip("\"'").strip() or None
        buf = []
        for nxt in lines[i + 1:]:
            if not nxt.strip():
                buf.append("")
                continue
            if not nxt.startswith((" ", "\t")):
                break
            buf.append(nxt.strip())
        return " ".join(x for x in buf if x).strip() or None
    return None


def fm_is_block(fm: str, key: str) -> bool:
    """该字段是否写成 YAML 块标量（`>-` / `|`）或多行列表。

    平台侧解析器只看「key: value」这一行，块写法的内容它读不到。
    """
    lines = fm.splitlines()
    for i, line in enumerate(lines):
        m = re.match(r"^[ \t]*%s:[ \t]*(.*)$" % re.escape(key), line)
        if not m:
            continue
        val = m.group(1).strip()
        if val in (">", "|", ">-", "|-", ">+", "|+"):
            return True
        if val == "":
            for nxt in lines[i + 1:]:
                if not nxt.strip():
                    continue
                return bool(re.match(r"^[ \t]+", nxt))
            return False
        return False
    return False


def parse_frontmatter(content: str):
    m = re.match(r"^---\s*\n(.*?)\n---", content or "", re.DOTALL)
    return m.group(1) if m else None


def check_market(root: Path, rep: Report, content: str):
    """按技能市场分发规范检查 frontmatter（用 --market 启用，默认不跑）。"""
    fm = parse_frontmatter(content)
    if fm is None:
        return  # frontmatter 缺失/未闭合，结构检查已报 P0

    skill_md = root / "SKILL.md"
    for key, rule, hint in MARKET_REQUIRED:
        if not fm_text(fm, key):
            rep.add("P1", "市场分发", skill_md, rule, 1,
                    "frontmatter 缺 %s，市场规范标为必填" % key, hint)
    for key, rule, hint in MARKET_RECOMMENDED:
        if not fm_text(fm, key):
            rep.add("P2", "市场分发", skill_md, rule, 1,
                    "frontmatter 缺 %s" % key, hint)

    v = fm_value(fm, "version")
    if v and not re.match(r"^\d+\.\d+\.\d+", v):
        rep.add("P2", "市场分发", skill_md, "version 非语义化", 1,
                "version = %r" % v, "改成 主版本.次版本.修订号，如 1.0.0")

    zh, en = fm_text(fm, "description_zh"), fm_text(fm, "description_en")
    if zh and not re.search(r"[\u4e00-\u9fff]", zh):
        rep.add("P2", "市场分发", skill_md, "description_zh 无中文", 1,
                "description_zh = %r" % zh[:60], "这是中文介绍，应含中文")
    if en and re.search(r"[\u4e00-\u9fff]", en):
        rep.add("P2", "市场分发", skill_md, "description_en 含中文", 1,
                "description_en = %r" % en[:60], "这是英文介绍，不应含中文字符")

    # 尖括号会和 description 同源地让市场校验失败，四类展示字段都要查
    for key in ("description_zh", "description_en", "display_name", "display_name_en"):
        val = fm_text(fm, key)
        if val and ("<" in val or ">" in val):
            rep.add("P1", "市场分发", skill_md, "%s 含尖括号" % key, 1,
                    "%s 含 < 或 >，市场校验会失败" % key, "换成方括号或中文书名号")

    a = fm_text(fm, "author")
    if a and re.search(r"(?i)workbuddy|assistant|ai\b|unknown|todo|your|xxx|示例", a):
        rep.add("P2", "市场分发", skill_md, "author 为占位署名", 1,
                "author = %r" % a, "改成真实署名（个人或团队/公司名）")

    # 平台的解析器只认单行标量：`>-` 折叠块 / 多行列表会被读成 ">-" 或空串。
    # 这是静默失败 —— 上传成功，但描述、标签在商店里是空的。
    for key in PLATFORM_SCALAR_KEYS:
        if fm_is_block(fm, key):
            rep.add("P2", "市场分发", skill_md, "%s 用了块标量/多行列表" % key, 1,
                    "%s 写成 >- / | 块或多行列表" % key,
                    "平台解析器只认单行 `%s: 值`（列表用 `[a, b]`），块写法它读成 \">-\" 或空；"
                    "长文本折成一行即可" % key)

    cat = fm_value(fm, "category")
    if cat and cat not in SKILLHUB_CATEGORIES:
        rep.add("P2", "市场分发", skill_md, "category 不在平台枚举内", 1,
                "category = %r" % cat,
                "平台只认 13 个 key，非枚举值会上架为「未分类」：%s"
                % "、".join(sorted(SKILLHUB_CATEGORIES)))


def check_junk(root: Path, files, junk_dirs, rep: Report):
    # 垃圾文件打包时由 pack_skill.py 自动排除，不构成阻断，只做知情提示。
    for d in junk_dirs:
        if d.name == ".git":
            # 技能目录常常同时是 git 仓库；打包本就排除，报出来只是噪音
            continue
        rep.add("P2", "垃圾文件", d.relative_to(root), "垃圾目录", 0,
                "不应分发的目录：%s" % d.relative_to(root),
                "打包时自动排除，无需手动清理；若该目录其实是技能的一部分，请改名")
    junk_files = [f for f in files if f.name.lower() in {j.lower() for j in JUNK_FILES} or f.suffix.lower() in JUNK_SUFFIX]
    for f in junk_files:
        rel = f.relative_to(root)
        rep.add("P2", "垃圾文件", rel.parent, "临时文件", 0,
                "临时/缓存文件：%s" % rel.name, "打包时自动排除")

    seen = set()
    for f in files:
        parts = f.relative_to(root).parts
        for i, part in enumerate(parts[:-1]):
            if part.lower() in RUNTIME_DIR_HINTS and part not in seen:
                seen.add(part)
                rep.add("P2", "运行时数据", Path(*parts[:i + 1]), "运行时目录", 0,
                        "疑似运行时数据目录：%s" % part,
                        "确认它是使用者本机生成的；是则不要随技能分发")

    for f in files:
        try:
            size = f.stat().st_size
        except OSError:
            continue
        if size > BIG_FILE_BYTES:
            rep.add("P1", "体积", f.relative_to(root), "大文件", 0,
                    "%.1f MB" % (size / 1024 / 1024),
                    "确认必须随包分发；否则改为运行时下载，或放进 assets 并注明来源")


# 命中片段附近出现这些标记，说明是写作占位符而不是真实机器路径
PATH_PLACEHOLDER_MARKERS = ("...", "<", ">", "xxx", "XXX", "用户名", "占位", "示例", "某")


def has_path_placeholder(line: str, start: int, end: int) -> bool:
    seg = line[max(0, start - 2): end + 4]
    return any(k in seg for k in PATH_PLACEHOLDER_MARKERS)


def check_abs_paths(root: Path, files, rep: Report):
    for f in files:
        if f.suffix.lower() not in TEXT_EXT:
            continue
        rel = f.relative_to(root)
        is_code = f.suffix.lower() in CODE_EXT
        sev = "P1" if is_code else "P2"
        for lineno, line in scan_lines(f):
            for rule_name, rx in ABS_PATH_RULES:
                for m in rx.finditer(line):
                    hit = m.group(1).rstrip("\\/,;:'\"")
                    if len(hit) < 4 or hit.endswith(":\\"):
                        continue
                    if has_path_placeholder(line, m.start(1), m.end(1)):
                        continue
                    rep.add(sev, "绝对路径", rel, rule_name, lineno, hit,
                            "代码里改成：Path(__file__).resolve() 定位技能自身 / os.path.expanduser('~') 定位用户目录 / "
                            "从配置文件或环境变量取；文档里改成 <技能目录> 这类占位符。详见 references/sanitize-rules.md")


def check_secrets(root: Path, files, rep: Report):
    for f in files:
        if f.suffix.lower() not in TEXT_EXT:
            continue
        rel = f.relative_to(root)
        is_doc = f.suffix.lower() in DOC_EXT or f.name.lower().endswith(TEMPLATE_HINT)
        for lineno, line in scan_lines(f):
            # 1) 高置信度密钥字面量
            for rule_name, rx in SECRET_VALUE_RULES:
                for m in rx.finditer(line):
                    rep.add("P0", "凭据", rel, rule_name, lineno, mask(m.group(0)),
                            "立刻删除并把值改从配置/环境变量读取；若已外泄需轮换")
            if SECRET_KEYWORD.search(line):
                for m in LONG_HEX.finditer(line):
                    rep.add("P0", "凭据", rel, "疑似哈希密钥", lineno, mask(m.group(0)),
                            "确认是否为密钥；是则外置")
            # 2) 关键字 + 字面量赋值
            if SECRET_KEYWORD.search(line):
                am = ASSIGN_RE.search(line.strip())
                if (am and is_literal_secret_value(am.group("val"))
                        and not is_identifier_reference(am.group("key"), am.group("val"))):
                    key, val = am.group("key"), am.group("val").strip()
                    if is_doc and looks_like_placeholder(val):
                        rep.add("P2", "凭据", rel, "文档中的字段示例", lineno,
                                "%s = %s" % (key, val[:40]),
                                "文档示例建议留空或写 <你的密码>")
                    else:
                        sev = "P1" if is_doc else "P0"
                        rep.add(sev, "凭据", rel, "明文凭据赋值", lineno,
                                "%s = %s" % (key, mask(val)),
                                "外置为 config/xxx.example.json 空模板，真实值放 ~/.workbuddy/<name>_config.json，"
                                "并加入 .gitignore")


def check_danger(root: Path, files, rep: Report):
    for f in files:
        if f.suffix.lower() not in TEXT_EXT:
            continue
        rel = f.relative_to(root)
        for lineno, line in scan_lines(f):
            if line.lstrip().startswith("#!"):
                continue
            for rule_name, rx in DANGER_P0:
                m = rx.search(line)
                if m and not is_rule_table_hit(line, m.group(0)):
                    rep.add("P0", "危险操作", rel, rule_name, lineno, line.strip()[:100],
                            "限制作用范围（只动自身进程/自身目录）、加二次确认，并在 SKILL.md 写明风险与回滚方案")
            for rule_name, rx in DANGER_P1:
                m = rx.search(line)
                if m and not is_rule_table_hit(line, m.group(0)):
                    rep.add("P1", "危险操作", rel, rule_name, lineno, line.strip()[:100],
                            "确认作用范围可控；在 SKILL.md 说明会清理什么、不会碰什么。"
                            "作用范围已收窄（如上方已校验目标确属自身目录）时，"
                            "在该行行尾加 # skill-audit: ignore 放行")
            for rule_name, rx in SIDE_EFFECT_RULES:
                m = rx.search(line)
                if m and not is_rule_table_hit(line, m.group(0)):
                    rep.add("P2", "外部副作用", rel, rule_name, lineno, line.strip()[:90],
                            "在 SKILL.md 显式声明该能力及其影响范围，并说明凭据来源；这条是知情项，不是错误")


# 文档里的 HTML 注释放行标记。注释渲染后不可见，第三方安全审计会把它读成
# 「隐蔽地指示审计放行」= 提示注入（实测已使技能在 SkillHub 被判 suspicious）。
DOC_SUPPRESS = re.compile(r"<!--\s*skill-audit\s*:\s*ignore\s*-->")


def check_doc_suppression(root: Path, files, rep: Report):
    """文档里禁止用 HTML 注释放行（脚本文件的行尾注释不查）。

    注释渲染后不可见，第三方安全审计读到「让审计跳过」的隐藏指令会判定为提示注入
    —— 实测已使技能在 SkillHub 被判 suspicious。放行应当可见、可审阅。
    """
    for f in files:
        if f.suffix.lower() not in DOC_EXT:
            continue
        text = read_text(f)
        if not text:
            continue
        rel = f.relative_to(root)
        for lineno, line in enumerate(text.splitlines(), 1):
            if DOC_SUPPRESS.search(line):
                rep.add("P1", "文档放行标记", rel, "隐藏注释放行", lineno, line.strip()[:100],
                        "文档注释渲染后不可见，第三方安全审计会判为「隐蔽地指示审计放行」。"
                        "改法：① 改写正文让它不再命中该规则；② 确需例外，就改用技能根目录 .skillignore "
                        "写 `rule:规则名`，并在正文显式说明理由。该标记今后只用于脚本文件的行尾注释")


def check_deps(root: Path, files, rep: Report):
    py_files = [f for f in files if f.suffix == ".py"]
    js_files = [f for f in files if f.suffix.lower() in {".js", ".mjs", ".cjs", ".ts"}]
    local_py = {f.stem for f in py_files}

    py_deps, js_deps, tools = set(), set(), {}
    font_hit = None

    for f in py_files:
        text = read_text(f) or ""
        for m in PY_IMPORT.finditer(text):
            mod = (m.group(1) or m.group(2) or "").split(".")[0]
            if not mod or mod.startswith("_") or mod in STDIO or mod in local_py:
                continue
            py_deps.add(mod)
        if font_hit is None:
            for _, line in scan_lines(f):
                if FONT_HINT.search(line):
                    font_hit = f.relative_to(root)
                    break

    for f in files:
        name = f.name
        if name in EXTERNAL_TOOLS:
            tools[name] = EXTERNAL_TOOLS[name]

    for f in js_files:
        text = read_text(f) or ""
        for m in JS_IMPORT.finditer(text):
            pkg = m.group(1) or m.group(2) or ""
            if not pkg or pkg.startswith((".", "node:", "/")):
                continue
            js_deps.add("/".join(pkg.split("/")[:2]) if pkg.startswith("@") else pkg.split("/")[0])

    if py_deps:
        pypi = sorted({PYPI_ALIAS.get(d, d) for d in py_deps})
        rep.add("P2", "依赖", Path("scripts"), "Python 第三方包", 0,
                "、" .join(pypi),
                "在 SKILL.md 写明安装命令；建议提供 scripts/setup.py 一键安装")
    if js_deps:
        rep.add("P2", "依赖", Path("scripts"), "Node 第三方包", 0,
                "、".join(sorted(js_deps)),
                "在 SKILL.md 写明安装命令与 package.json 位置")
    if tools:
        rep.add("P1", "外部依赖", Path("scripts"), "外部可执行文件", 0,
                "、".join("%s(%s)" % (k, v) for k, v in sorted(tools.items())),
                "SKILL.md 必须写「运行前提」：安装方式 + 检测方法 + 缺失时的行为")
    if font_hit:
        rep.add("P1", "外部依赖", font_hit, "中文字体", 0,
                "使用中文字体渲染",
                "不同机器字体缺失会渲染成方块；SKILL.md 说明字体回退顺序与缺失表现")

    if (py_deps or js_deps) and not (root / "scripts" / "setup.py").exists() and not (root / "package.json").exists():
        rep.add("P1", "依赖", root, "缺一键安装入口", 0,
                "有第三方依赖但没有 setup.py / package.json",
                "让使用者手动 pip install 必漏装，补一个安装脚本")


# 约定俗成、可选的辅助文件：缺失时只提示不告警
CONVENTIONAL_OPTIONAL = {
    "setup.py", "install.py", "install.sh", "install.ps1", "package.json",
    "package-lock.json", "requirements.txt", "makefile", "readme.md",
    "license", "license.txt", "changelog.md", "todo.md",
}
# 路径里出现这些片段，说明是写作示例而非真实引用
PLACEHOLDER_SEGMENT = re.compile(
    r"(?i)^(xxx+|yyy+|zzz+|your[_-].*|my[_-].*|foo|bar|baz|placeholder|demo|sample|template|"
    r"<.+>|\.\.\.|路径|文件名)$"
)


def is_placeholder_path(t: str) -> bool:
    name = Path(t).name
    if name.lower() in CONVENTIONAL_OPTIONAL:
        return True
    # 平台/宿主的清单目录：位于插件包根或用户目录，本来就不在技能目录里。
    # 文档里写它们是必要的（上架说明），不能因此判「引用缺失」。
    norm = t.replace("\\", "/")
    if any(d in norm for d in (".codebuddy-plugin/", ".workbuddy-plugin/", ".claude-plugin/")):
        return True
    if re.search(r"(?i)\.(example|template|sample|dist)(\.|$)", name):
        return True
    for seg in re.split(r"[\\/]", t):
        if not seg:
            continue
        if PLACEHOLDER_SEGMENT.match(seg) or PLACEHOLDER_SEGMENT.match(Path(seg).stem):
            return True
    return False


def _resolve_ref(root: Path, doc: Path, target: str):
    t = target.strip()
    if not t or t.startswith(("http://", "https://", "mailto:", "#", "data:", "file:")):
        return True
    if t.startswith(".") and "/" not in t and "\\" not in t:
        return True          # `config/*.example.json` 会被截出 `.example.json`，属噪声
    if any(ch in t for ch in "*?{}$%<>") or t.endswith("/"):
        return True
    if "://" in t:
        return True
    # 既无目录分隔符也无扩展名 → 是行文里的占位词（如 [文字](路径)），不是文件引用
    if "/" not in t and "\\" not in t and "." not in t:
        return True
    for base in (doc.parent, root):
        try:
            if (base / t).resolve().exists():
                return True
        except OSError:
            pass
    if "/" not in t and "\\" not in t:
        # 裸文件名：在技能内递归找同名文件
        name = Path(t).name
        for p in root.rglob(name):
            if p.is_file():
                return True
    return False


def check_refs(root: Path, files, rep: Report):
    for f in files:
        if f.suffix.lower() not in DOC_EXT:
            continue
        rel = f.relative_to(root)
        for lineno, line in scan_lines(f):
            seen = set()
            output_ctx = bool(OUTPUT_HINT_RE.search(line))
            for rx in REF_PATTERNS:
                for m in rx.finditer(line):
                    t = m.group(1)
                    if t in seen:
                        continue
                    seen.add(t)
                    if _resolve_ref(root, f, t):
                        continue
                    if is_placeholder_path(t) or output_ctx:
                        rep.add("P2", "引用", rel, "约定/示例路径", lineno, t,
                                "写作示例、可选约定文件或运行时产物，目录下没有属正常；若确为真实依赖则需补上")
                    elif "/" in t or "\\" in t:
                        rep.add("P1", "引用", rel, "引用缺失", lineno, t,
                                "文件不存在；补齐它，或修正 SKILL.md 中的路径")
                    else:
                        rep.add("P2", "引用", rel, "疑似产物路径", lineno, t,
                                "技能内找不到该文件。若是运行时产物，在正文标注「输出文件」以免误判为缺失")

    cfg_dir = root / "config"
    if cfg_dir.is_dir():
        cfgs = [c for c in cfg_dir.rglob("*") if c.is_file()]
        has_example = any(c.name.lower().endswith((".example", ".template", ".sample")) or "example" in c.name.lower() for c in cfgs)
        if cfgs and not has_example:
            rep.add("P1", "配置模板", cfg_dir, "缺 example 模板", 0,
                    "config/ 有 %d 个配置文件但没有 .example 模板" % len(cfgs),
                    "补 config/xxx.example.json 空模板，别人照抄即可上手")
        for c in cfgs:
            text = read_text(c) or ""
            if any(rx.search(text) for _, rx in SECRET_VALUE_RULES):
                rep.add("P0", "配置模板", c.relative_to(root), "模板含真实凭据", 0,
                        "配置模板里出现高置信度密钥", "模板中所有敏感字段留空字符串")


# ------------------------------------------------------------------ 主流程


def audit(root: Path, market: bool = False, ignored_rules=None, ignore_globs=None) -> Report:
    # .skillignore 里既能写 glob 排除文件，也能写 `rule:规则名` 按规则放行
    # load_skillignore 返回 (glob 列表, 规则名集合)，顺序不能颠倒
    si_globs, si_rules = load_skillignore(root)
    rep = Report(ignored_rules=set(ignored_rules or ()) | si_rules)
    if not root.exists() or not root.is_dir():
        rep.add("P0", "参数", root, "目录无效", 0, "目录不存在或不是目录", "")
        return rep
    content = check_structure(root, rep, market)
    if market and content is not None:
        check_market(root, rep, content)
    files, junk_dirs = walk_tree(root, list(ignore_globs or ()) + si_globs)
    check_junk(root, files, junk_dirs, rep)
    check_abs_paths(root, files, rep)
    check_secrets(root, files, rep)
    check_danger(root, files, rep)
    check_doc_suppression(root, files, rep)
    check_deps(root, files, rep)
    check_refs(root, files, rep)
    if content is not None and not re.search(r"\.workbuddy|~/|配置|config", content):
        rep.add("P2", "配置模板", Path("SKILL.md"), "未说明配置位置", 0,
                "SKILL.md 未说明运行时配置/数据的存放位置",
                "建议统一写成 ~/.workbuddy/<name>_config.json 这类可展开路径")
    return rep


SEV_ORDER = {"P0": 0, "P1": 1, "P2": 2}
SEV_LABEL = {"P0": "P0 阻断", "P1": "P1 警告", "P2": "P2 提示"}
SEV_COLOR = {"P0": "\033[91m", "P1": "\033[93m", "P2": "\033[90m"}
RESET = "\033[0m"


def render(rep: Report, root: Path, show_p2=True, use_color=True, samples=3, show_noise=False):
    def paint(sev, s):
        return (SEV_COLOR[sev] + s + RESET) if use_color else s

    findings, noise = [], 0
    for f in rep.findings():
        if not show_p2 and f["severity"] == "P2":
            continue
        # 示例路径/产物路径是知情项，默认折叠成一行计数，不再逐条刷屏
        if not show_noise and f["rule"] in NOISE_RULES:
            noise += len(f["hits"])
            continue
        findings.append(f)
    print("=" * 74)
    print("技能体检报告: %s" % root)
    print("=" * 74)
    if not findings:
        print("未发现问题。")

    cur = None
    for f in findings:
        head = (f["severity"], f["category"])
        if head != cur:
            cur = head
            print("\n[%s] %s" % (SEV_LABEL[f["severity"]], f["category"]))
        n = len(f["hits"])
        suffix = "  (共 %d 处)" % n if n > 1 else ""
        print("  - %s%s" % (f["file"], suffix))
        shown_lines, shown = set(), 0
        for h in f["hits"]:
            if shown >= samples:
                break
            if h["sample"]:
                print("      %s :: %s" % (f["rule"], h["sample"]))
                shown_lines.add(h["line"])
                shown += 1
        if not shown:
            print("      %s" % f["rule"])
        rest = sorted({h["line"] for h in f["hits"]} - shown_lines)
        if rest:
            print("      其余 %d 处，行号：%s" % (len(rest), ", ".join(map(str, rest[:20]))))
        if f["hint"]:
            print("      → %s" % f["hint"])

    p0, p1, p2 = rep.count("P0"), rep.count("P1"), rep.count("P2")
    print("\n" + "-" * 74)
    print("汇总: P0=%d  P1=%d  P2=%d" % (p0, p1, p2))
    if noise:
        print("另有 %d 处「示例/产物路径」提示已折叠（目录下没有属正常，加 --show-noise 展开）" % noise)
    if rep.ignored_hits:
        print("按 .skillignore / --ignore-rule 放行了 %d 处" % rep.ignored_hits)
    if p0:
        print("结论: %s 禁止打包，先修 P0。" % paint("P0", "不通过"))
    elif p1:
        print("结论: %s 建议修完 P1 再打包（确认安全后可加 --allow-p1）。" % paint("P1", "有警告"))
    else:
        print("结论: 通过，可以打包。")
    print("-" * 74)


# ------------------------------------------------------------------ 规则说明

# 规则名 → (判什么, 为什么算问题, 怎么改, 怎么放行)
RULES_DOC = {
    "缺 SKILL.md": ("技能目录下必须有 SKILL.md", "没有它就不是技能，平台与本机都识别不了",
                    "新建 SKILL.md：首行 `---`，frontmatter 里至少写 name 与 description", "不能放行"),
    "缺 frontmatter": ("SKILL.md 必须以 `---` 开头并带 YAML frontmatter", "没有 frontmatter 就没有 name / description，技能不会被触发",
                       "首行写 `---`，第二个 `---` 之前写 name / description 等字段", "不能放行"),
    "缺 name": ("frontmatter 里要有 name", "name 与目录名一起决定技能被怎么定位",
                "加一行 `name: <与目录名一致的小写连字符名>`", "不能放行"),
    "缺 description": ("frontmatter 里要有 description", "模型靠 description 判断要不要触发这个技能",
                       "写清三件事：做什么 / 何时触发 / 用户会怎么说", "不能放行"),
    "description 含尖括号": ("description 里出现了 < 或 >", "市场校验会直接失败",
                             "把 `<技能目录>` 这类占位换成方括号或中文书名号", "不能放行，必须替换"),
    "SKILL.md 过长": ("SKILL.md 超过 30000 字符", "每次触发都要读进上下文，会把对话挤爆",
                      "把字段表、踩坑细节、版本历史搬进 references/，正文只留流程骨架", "把细节外迁后自然消除"),
    "SKILL.md 偏长": ("SKILL.md 超过 15000 字符", "同上，程度较轻",
                      "考虑把细节拆进 references/，正文写明「什么时候需要读它」", "确认必要可留着"),
    "引用缺失": ("正文里提到（反引号 / 链接 / 命令里）的文件在技能目录里找不到",
                 "模型按正文去调文件会落空，技能跑不起来",
                 "补齐这个文件，或修正正文里的路径", "确实是运行时产物就在同一行标注「输出文件」；确实要忽略写 .skillignore 的 `rule:引用缺失`"),
    "约定/示例路径": ("正文提到的路径像是写作示例（含 xxx / your_ / 尖括号）或运行时产物",
                     "只是知情项，目录下没有属正常", "不需要改；若确为真实依赖则补上", "默认已折叠，加 --show-noise 才展开"),
    "疑似产物路径": ("技能内找不到这个裸文件名", "可能是运行后才生成的文件",
                     "若是产物，在正文标注「输出文件」；若是依赖则补齐", "同上"),
    "windows 盘符路径": ("代码或文档里写死了 C:\\ 这类盘符路径", "换台机器就跑不起来，还可能漏出内网结构",
                         "代码改成 Path(__file__).resolve() / os.path.expanduser('~')；文档改成 `<技能目录>` 占位符",
                         "占位示例加行尾 `# skill-audit: ignore`"),
    "POSIX 家目录路径": ("写死了 /home/xxx、/Users/xxx", "同上", "同上", "同上"),
    "明文凭据赋值": ("password / token / api_key 等关键字被赋了字面量", "别人拿到技能就等于拿到你的凭据",
                     "外置成 config/xxx.example.json 空模板，真值放 ~/.workbuddy/<name>_config.json 或环境变量；已外泄的必须轮换",
                     "不能放行（P0）"),
    "递归删除目录": ("代码里出现 shutil.rmtree / os.remove / fs.rmSync", "删错目录就是不可逆事故",
                     "把作用范围收窄（先校验目标确属自身目录），并在 SKILL.md 说明会清理什么",
                     "范围已收窄时在该行行尾加 `# skill-audit: ignore`"),
    "驱动浏览器": ("脚本会驱动浏览器 / 走 Chrome DevTools 协议", "属于外部副作用，要让用户知情",
                   "在 SKILL.md 显式声明并说明凭据来源", "本就是知情项（P2）"),
    "外部可执行文件": ("依赖 ffmpeg / edge-tts / 浏览器等外部程序", "使用者机器上没有就跑不起来",
                       "在 SKILL.md 写「运行前提」：安装方式 + 检测方法 + 缺失时的行为", "补说明后仍在，属知情"),
    "中文字体": ("渲染时用了中文字体", "别的机器缺字体会渲染成方块",
                 "说明字体回退顺序与缺失表现", "补说明后仍在，属知情"),
    "缺 example 模板": ("config/ 有真实配置但没有 .example 空模板", "使用者不知道要填哪些字段，容易把自己的配置传出去",
                        "补 config/xxx.example.json：字段名留全、值留空", "补模板后消除"),
    "模板含真实凭据": ("config 模板里出现了高置信度密钥", "等于把密钥写进了分发包",
                       "模板里所有敏感字段留空字符串，并轮换已外泄的凭据", "不能放行（P0）"),
    "缺 description_zh": ("frontmatter 缺中文一句话介绍", "平台上架必填，缺了会被打回",
                          "补 `description_zh: 30 字以内的中文介绍`", "补字段后消除"),
    "缺 description_en": ("frontmatter 缺英文一句话介绍", "同上", "补 `description_en: One-line English intro`", "补字段后消除"),
    "缺 version": ("frontmatter 缺版本号", "上架必填，也让人分不清新旧",
                   "补 `version: 1.0.0`；之后用 `python scripts/bump.py <技能目录>` 递增", "补字段后消除"),
    "缺 displayName": ("缺驼峰 displayName（平台字段）", "平台只认驼峰；缺了不报错但商店里显示英文 slug（静默失败）",
                       "补 `displayName: 中文展示名`（下划线 display_name 是本机字段，两者都写）", "补字段后消除"),
    "category 不在平台枚举内": ("category 取值不在平台 13 个 key 里", "上架后显示「未分类」，等于少一个曝光入口",
                                "改成枚举内的值，如 dev-programming", "改值后消除"),
    "垃圾目录": ("目录里出现 .venv / node_modules / dist 等", "打进包会又大又带隐私",
                 "打包时自动排除；若它其实是技能的一部分就改名", "打包已自动排除"),
    "隐藏注释放行": ("文档（.md / .markdown / .txt）里出现 HTML 注释形式的放行标记",
                     "注释渲染后不可见，第三方安全审计会读成「隐蔽地指示审计放行」= 提示注入"
                     "（实测已使技能在 SkillHub 被判 suspicious）",
                     "① 改写正文让它不再命中那条规则；② 或改用技能根目录 .skillignore 写 "
                     "`rule:规则名`，并在正文显式说明理由",
                     "不放行 —— 放行应当可见、可审阅。该标记只用于脚本文件的行尾注释"),
}


def explain_rule(name: str) -> int:
    d = RULES_DOC.get(name)
    if not d:
        print("没有收录「%s」这条规则的详细说明。" % name)
        print()
        print("拿准确规则名：python scripts/audit_skill.py <技能目录>")
        print("看所有规则：  python scripts/audit_skill.py --explain 引用缺失   （换任意已收录名查看格式）")
        print("规则名就是体检报告里 `- 文件` 下面那一行 `规则名 :: 样例` 的前半段。")
        return 3
    what, why, how, allow = d
    print("=" * 74)
    print("规则：%s" % name)
    print("=" * 74)
    print("  判什么：%s" % what)
    print("  为什么：%s" % why)
    print("  怎么改：%s" % how)
    print("  怎么放行：%s" % allow)
    print()
    print("  临时不去管它：python scripts/audit_skill.py <技能目录> --ignore-rule %s" % name)
    print("  永久放行：在技能根目录的 .skillignore 里写一行 `rule:%s`" % name)
    return 0


# ------------------------------------------------------------------ 自检

# ⚠️ 这些"坏味道"必须在源码里**拆开写**。样例若原样写在源码里，
# 体检器扫本技能自己时会把自己的样例当成真凭据（实测 P0=2），自检就永远失败。
_SELFTEST_KEY = "sk-" + "abcdefghijklmnopqrstuvwxyz012345"
_SELFTEST_KEY_NAME = "api" + "_key"
_SELFTEST_RM = "rm" + "tree"
_SELFTEST_PATH = "C:/" + "work/someone/secret/data"
# 同理拆开写：否则这行本身就是一条「文档放行标记」样例，会污染本技能自身的体检
_SELFTEST_SUPPRESS = "<!--" + " skill-audit: ignore " + "-->"

_BAD_SKILL_MD = '''---
name: bad-skill-selftest
description: "自检用的带病样例，故意包含各类应当被判定的问题。"
---

# 带病样例

{keyname} = "{key}"
work_dir = "{path}"
import shutil; shutil.{rm}(target)
'''.format(keyname=_SELFTEST_KEY_NAME, key=_SELFTEST_KEY,
           path=_SELFTEST_PATH, rm=_SELFTEST_RM)

_GOOD_SKILL_MD = '''---
name: good-skill-selftest
slug: good-skill-selftest
description: "自检用的干净样例，不应被判定出任何阻断或警告项。"
description_zh: "自检用的干净样例"
description_en: "Clean sample used by selftest"
version: 1.0.0
displayName: 自检干净样例
display_name: 自检干净样例
display_name_en: Selftest Clean Sample
summary: 自检用的干净样例
category: dev-programming
author: selftest
tags: [selftest]
agent_created: true
---

# 干净样例

运行 `scripts/demo.py` 完成自检。
'''

# 文档里带隐藏的审计放行注释：应判出 P1「隐藏注释放行」
_SUPPRESS_SKILL_MD = '''---
name: suppress-selftest
description: "自检用的样例：正文里藏了不可见的审计放行注释，应被判出 P1。"
---

# 隐藏注释样例

正文本身很正常。{sup}
'''.format(sup=_SELFTEST_SUPPRESS)


def _build_tmp_skill(md_text: str, extra_files=()):
    import shutil
    import tempfile
    d = Path(tempfile.mkdtemp(prefix="skill-audit-selftest-"))
    (d / "SKILL.md").write_text(md_text, encoding="utf-8")
    for rel in extra_files:
        p = d / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("# 自检用\n", encoding="utf-8")
    return d


def selftest() -> int:
    """验证体检器本身没坏：造一个带病样例、一个干净样例，再对自身跑一遍。

    样例一律落在系统临时目录，**不写进技能目录** —— 否则假密钥会让本技能自己的体检报 P0。
    """
    import shutil

    print("=" * 74)
    print("体检器自检（样例建在系统临时目录，不写进技能目录）")
    print("=" * 74)

    results = []

    def run_case(title, root, expect_p0, expect_p1, cleanup=True):
        rep = audit(root, market=False)
        p0, p1, p2 = rep.count("P0"), rep.count("P1"), rep.count("P2")
        ok = (p0 >= expect_p0) and (p1 >= expect_p1)
        results.append(ok)
        print("\n[%s] %s  P0=%d P1=%d P2=%d  (期望 P0>=%d 且 P1>=%d)"
              % ("OK" if ok else "X ", title, p0, p1, p2, expect_p0, expect_p1))
        for f in rep.findings():
            if f["severity"] in ("P0", "P1"):
                print("      [%s] %s :: %s" % (f["severity"], f["rule"], (f["hits"][0]["sample"] or "")[:50]))
        if cleanup:
            shutil.rmtree(root, ignore_errors=True)  # skill-audit: ignore 只删自己刚建的临时目录
        return ok

    run_case("带病样例（应判出 P0 凭据 + P1 路径 + P1 危险操作）",
             _build_tmp_skill(_BAD_SKILL_MD), 1, 2)

    run_case("文档隐藏注释放行（应判出 P1 文档放行标记）",
             _build_tmp_skill(_SUPPRESS_SKILL_MD), 0, 1)

    ok_clean = True
    root = _build_tmp_skill(_GOOD_SKILL_MD, ("scripts/demo.py",))
    rep = audit(root, market=True)
    p0, p1, p2 = rep.count("P0"), rep.count("P1"), rep.count("P2")
    ok_clean = (p0 == 0 and p1 == 0)
    results.append(ok_clean)
    print("\n[%s] 干净样例（应零 P0 零 P1）  P0=%d P1=%d P2=%d"
          % ("OK" if ok_clean else "X ", p0, p1, p2))
    for f in rep.findings():
        if f["severity"] in ("P0", "P1"):
            print("      [%s] %s :: %s" % (f["severity"], f["rule"], (f["hits"][0]["sample"] or "")[:50]))
    shutil.rmtree(root, ignore_errors=True)  # skill-audit: ignore 只删自己刚建的临时目录

    me = Path(__file__).resolve().parent.parent
    rep = audit(me, market=True)
    p0, p1, p2 = rep.count("P0"), rep.count("P1"), rep.count("P2")
    ok_self = (p0 == 0 and p1 == 0)
    results.append(ok_self)
    print("\n[%s] 本技能自身（应零 P0 零 P1）  P0=%d P1=%d P2=%d" % ("OK" if ok_self else "X ", p0, p1, p2))

    all_ok = all(results)
    print("\n" + "-" * 74)
    print("自检%s：%d/%d 项通过。" % ("通过" if all_ok else "失败", sum(1 for r in results if r), len(results)))
    if not all_ok:
        print("把上面的输出发给技能作者；体检器本身的判定逻辑可能被动过。")
    print("-" * 74)
    return 0 if all_ok else 1


# ------------------------------------------------------------------ 半自动修复

# 占位值一律**不用尖括号**：check_market 会把含 <> 的展示字段判成 P1。
FIX_FIELDS = [
    ("description_zh", "待填写：30 字以内的中文一句话介绍"),
    ("description_en", "TODO: One-line English introduction"),
    ("version", "1.0.0"),
    ("displayName", "待填写：中文展示名"),
    ("display_name", "待填写：中文展示名"),
    ("display_name_en", "TODO: English Display Name"),
    ("summary", None),                 # 复用 description_zh
    ("category", "dev-programming"),
    ("author", "待填写：署名"),
    ("tags", "[技能]"),
    ("slug", None),                    # 取 name（下面的分支处理）
    ("agent_created", "true"),         # 缺了 skill_manage 后续改不动这个技能
]


def fix_skill(root: Path, write: bool = False) -> int:
    """保守修复：只补 frontmatter 里缺失的字段（写之前先备份），绝不改正文。"""
    import shutil
    from _friendly import backup_root

    skill_md = root / "SKILL.md"
    if not skill_md.exists():
        die(3, "目录里没有 SKILL.md：%s" % root, "确认这是技能目录")

    content = read_text(skill_md) or ""
    fm = parse_frontmatter(content)
    if fm is None:
        die(1, "frontmatter 缺失或未闭合，无法自动补字段",
            "先手动补齐 `--- ... ---`，再跑 --fix")

    name = fm_value(fm, "name") or root.name
    zh = fm_text(fm, "description_zh") or ""
    additions = []
    for key, tpl in FIX_FIELDS:
        if fm_text(fm, key) or fm_value(fm, key):
            continue
        val = zh if (key == "summary" and zh) else tpl
        if key == "slug":
            val = name
        if val:
            additions.append("%s: %s" % (key, val))

    noise = [f for f in audit(root, market=True).findings() if f["rule"] in NOISE_RULES]

    print("=" * 74)
    print("半自动修复：%s" % root)
    print("=" * 74)
    if additions:
        print("将补齐 %d 个 frontmatter 字段（占位值，写完记得替换）：" % len(additions))
        for a in additions:
            print("  + %s" % a)
    else:
        print("frontmatter 字段齐全，无需补。")

    if noise:
        total = sum(len(f["hits"]) for f in noise)
        print("\n另有 %d 处「示例/产物路径」提示 —— 这是知情项不是错误，" % total)
        print("若确认无需处理，可在技能根目录建 .skillignore 写一行：")
        print("  rule:约定/示例路径")
        print("  rule:疑似产物路径")

    if not additions:
        return 0

    if not write:
        print("\n[dry-run] 未落盘。确认无误后加 --write 写入（写之前会自动备份原文件）。")
        return 0

    from datetime import datetime
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    bak_dir = backup_root() / root.name
    bak_dir.mkdir(parents=True, exist_ok=True)
    bak = bak_dir / ("SKILL.md.%s" % stamp)
    shutil.copy2(skill_md, bak)

    m = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    new_fm = m.group(1).rstrip() + "\n" + "\n".join(additions) + "\n"
    new_content = content[:m.start(1)] + new_fm + content[m.end(1):]
    skill_md.write_text(new_content, encoding="utf-8")
    print("\n[OK] 已写入 %s" % skill_md)
    print("     原文件备份在：%s" % bak)
    print("     下一步：把占位值替换成真实内容，再跑一次体检。")
    return 0


def main():
    use_utf8_stdout()

    ap = argparse.ArgumentParser(description="技能打包前体检器")
    ap.add_argument("skill_dir", nargs="?",
                    help="技能目录；用 --explain / --selftest 时可省略")
    ap.add_argument("--ignore-rule", action="append", default=[], metavar="规则名",
                    help="按规则名放行（可重复）；规则名见体检报告，含义用 --explain 查")
    ap.add_argument("--show-noise", action="store_true",
                    help="展开「示例/产物路径」这类低价值提示（默认折叠）")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--hide-p2", action="store_true")
    ap.add_argument("--no-color", action="store_true")
    ap.add_argument("--market", action="store_true",
                    help="附加技能市场分发规范检查（frontmatter 必填字段、kebab-case name 等）")
    ap.add_argument("--samples", type=int, default=3, help="每类问题最多展示几条样例")
    ap.add_argument("--explain", metavar="规则名", help="只打印某条规则的判据、改法与放行方式")
    ap.add_argument("--selftest", action="store_true", help="自检体检器本身")
    ap.add_argument("--fix", action="store_true", help="半自动修复：补齐缺失的 frontmatter 字段")
    ap.add_argument("--write", action="store_true", help="配合 --fix 真正落盘（默认只打印建议）")
    args = ap.parse_args()

    if args.selftest:
        raise SystemExit(selftest())
    if args.explain:
        raise SystemExit(explain_rule(args.explain))

    if not args.skill_dir:
        print("[X] 缺少技能目录参数。")
        print("    用法：python scripts/audit_skill.py <技能目录>")
        print("    %s" % explain_exit(3))
        raise SystemExit(3)

    root = Path(args.skill_dir).expanduser().resolve()
    if not root.is_dir():
        die(3, "目录不存在或不是目录：%s" % root,
            "确认路径拼写；路径含空格时要加引号；也可以先跑 --selftest 确认体检器正常")

    if args.fix:
        raise SystemExit(fix_skill(root, write=args.write))

    rep = audit(root, market=args.market, ignored_rules=args.ignore_rule)
    if args.json:
        print(json.dumps({
            "skill": str(root), "name": root.name, "market": args.market,
            "verdict": rep.worst,
            "summary": {"P0": rep.count("P0"), "P1": rep.count("P1"), "P2": rep.count("P2")},
            "ignored_hits": rep.ignored_hits,
            "findings": rep.findings(),
        }, ensure_ascii=False, indent=2))
    else:
        render(rep, root, show_p2=not args.hide_p2,
               use_color=not args.no_color, samples=args.samples,
               show_noise=args.show_noise)

    if rep.count("P0"):
        print(explain_exit(2))
        raise SystemExit(2)
    if rep.count("P1"):
        print(explain_exit(1))
        raise SystemExit(1)
    print(explain_exit(0))
    raise SystemExit(0)


if __name__ == "__main__":
    main()
