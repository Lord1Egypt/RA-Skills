#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
release_audit.py — 发布前侵权/法律风险审核（Release Infringement Audit）

用法:
    python3 release_audit.py <project_dir> [--format md|json] [--out FILE]

审核范围（五大类）:
    A  开源许可证兼容性   依赖 license 与本项目 license 的冲突（GPL 传染 / CC-NC 等）
    B  复制的第三方代码   SPDX 头、版权行、copied-from 标记
    C  文档/图片/字体素材 字体再分发、CC-NC 素材、无来源图片
    D  品牌与商标         项目名/标题与知名商标冲突
    E  密钥与隐私         内置规则（绝不执行被审项目的脚本）

退出码: 0 = 干净    1 = 仅警告(WARN/INFO)    2 = 存在阻断项(BLOCK)

判定依据锚定 SPDX license-list（https://spdx.org/licenses/）与
FSF/choosealicense 的分类，见 references/verdict-basis.md。
本工具输出不构成法律意见。
"""
import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

# ---------------------------------------------------------------- 常量表

PERMISSIVE = {
    "MIT", "MIT-0", "ISC", "0BSD", "BSD-1-Clause", "BSD-2-Clause",
    "BSD-3-Clause", "BSD-4-Clause", "ZLIB", "BSL-1.0", "APACHE-1.1",
    "APACHE-2.0", "PYTHON-2.0", "UNLICENSE", "CC0-1.0", "WTFPL",
    "BLUEOAK-1.0.0", "ARTISTIC-2.0", "POSTGRESQL", "MULANPSL-2.0",
}
STRONG_COPYLEFT_PREFIX = ("GPL-1.", "GPL-2.", "GPL-3.", "AGPL-", "SSPL-")
WEAK_COPYLEFT_PREFIX = ("LGPL-", "MPL-", "EPL-", "CDDL-", "NPL-")
# CC 许可证单独处理：CC0 ok；CC-BY / CC-BY-SA 对软件 warn；含 NC/ND 对软件 block

EXCLUDE_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv",
                "dist", "build", ".dsh", "paperclip-data", ".pycache"}
TEXT_EXTS = {".js", ".ts", ".jsx", ".tsx", ".mjs", ".cjs", ".py", ".sh",
             ".md", ".txt", ".json", ".yml", ".yaml", ".html", ".css",
             ".svg", ".rb", ".go", ".java", ".toml", ".ini", ".cfg", ".env"}
# B 类（代码溯源）只认源码文件：文档/测试夹具里「提到」的许可证示例不是许可证头
SOURCE_EXTS = {".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".py", ".sh",
               ".rb", ".go", ".java", ".c", ".h", ".cpp", ".hpp", ".rs",
               ".php", ".swift", ".kt", ".cs"}
# 真许可证头/版权行都在注释里：行首是注释标记才算，
# 否则字符串字面量与散文里的引用会被误判成真声明
COMMENT_START_RE = re.compile(r"^\s*(?://|#|/\*|\*|<!--|--|;)")
# 许可证头按 SPDX 约定出现在文件开头
SPDX_HEADER_WINDOW = 40
# 「声明许可/署名」类文件：这里的 NC/ND 才是真约束，不是说明文字
LICENSEISH_RE = re.compile(
    r"LICENSE|LICENCE|COPYING|CREDITS|ATTRIBUTION|NOTICE|THIRD[-_]?PARTY|package\.json",
    re.I)
FONT_EXTS = {".ttf", ".otf", ".woff", ".woff2", ".eot"}
IMG_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".svg"}

SECRET_PATTERNS = [
    (r"sk-[A-Za-z0-9_-]{20,}", "疑似 OpenAI/通用 sk- 密钥"),
    (r"sk-ant-[A-Za-z0-9_-]{20,}", "疑似 Anthropic 密钥"),
    (r"ghp_[A-Za-z0-9]{36}|gho_[A-Za-z0-9]{36}", "疑似 GitHub token"),
    (r"AKIA[0-9A-Z]{16}", "疑似 AWS Access Key"),
    (r"xox[baprs]-[A-Za-z0-9-]{10,}", "疑似 Slack token"),
    (r"npm_[A-Za-z0-9]{30,}", "疑似 npm granular token"),
    (r"AIza[0-9A-Za-z_-]{35}", "疑似 Google API key"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "疑似私钥文件内容"),
]

SPDX_RE = re.compile(r"SPDX-License-Identifier:\s*([A-Za-z0-9._+-]+)")
COPYRIGHT_RE = re.compile(
    r"Copyright\s+(?:\(c\)|©)?\s*(?:\d{4}[\d,\s-]*)\s*"
    r"([A-Za-z\u4e00-\u9fa5][\w\u4e00-\u9fa5 .&'-]{1,48})", re.I)
LICENSED_UNDER_RE = re.compile(
    r"[Ll]icensed\s+under\s+(?:the\s+)?([A-Za-z0-9 .,'()-]{3,60})")
COPIED_RE = re.compile(
    r"\b(copied from|forked from|based on|adapted from|ported from)\b"
    r"[^\n]{0,120}", re.I)

SEV_ORDER = {"INFO": 0, "WARN": 1, "BLOCK": 2}
CAT_NAMES = {"A": "开源许可证兼容性", "B": "复制的第三方代码",
             "C": "文档/图片/字体素材", "D": "品牌与商标", "E": "密钥与隐私"}

DISCLAIMER = ("⚠️ 本报告为自动化初筛，不构成法律意见。BLOCK/WARN 项请在发布前逐条处置，"
              "拿不准的咨询专业律师。")


# ---------------------------------------------------------------- 工具函数

def iter_files(root, extra_skip=None):
    skip = set(EXCLUDE_DIRS)
    if extra_skip:
        skip |= set(extra_skip)
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in skip and not d.startswith(".git")]
        for fn in filenames:
            p = Path(dirpath) / fn
            # 不跟随符号链接：被审仓库可能是恶意的，可借 symlink 指向项目外的
            # 敏感文件（~/.ssh 等），让审核报告把它读出来。
            if p.is_symlink():
                continue
            yield p


def license_sniff(text):
    """从 LICENSE 文本嗅探 SPDX id（锚定 choosealicense 的关键词特征）。"""
    head = text[:600].upper()
    if "AFFERO" in head:
        return "AGPL-3.0" if "VERSION 3" in head or "V3" in head else "AGPL"
    if "LESSER GENERAL PUBLIC LICENSE" in head:
        return "LGPL-3.0" if "VERSION 3" in head else "LGPL-2.1"
    if "GENERAL PUBLIC LICENSE" in head:
        if "VERSION 3" in head:
            return "GPL-3.0"
        if "VERSION 2" in head:
            return "GPL-2.0"
        return "GPL"
    if "APACHE LICENSE" in head and "2" in head[:300]:
        return "Apache-2.0"
    if "MOZILLA PUBLIC LICENSE" in head:
        return "MPL-2.0"
    if "ECLIPSE PUBLIC LICENSE" in head:
        return "EPL-2.0"
    if "COMMON DEVELOPMENT AND DISTRIBUTION" in head:
        return "CDDL-1.0"
    if "CREATIVE COMMONS ATTRIBUTION NON COMMERCIAL" in head:
        return "CC-BY-NC-4.0"
    if "MIT LICENSE" in head:
        return "MIT"
    if "ISC LICENSE" in head or "PERMISSION TO USE, COPY, MODIFY, AND/OR DISTRIBUTE" in head:
        return "ISC"
    if "BOOST SOFTWARE LICENSE" in head:
        return "BSL-1.0"
    if "THE UNLICENSE" in head:
        return "Unlicense"
    if "REDISTRIBUTION AND USE IN SOURCE AND BINARY FORMS" in head and "NEITHER THE NAME" in head:
        return "BSD-3-Clause"
    return None


def classify(spdx_id):
    """返回 'ok' | 'warn' | 'block' | 'unknown'。

    判定依据：
    - GPL/AGPL/SSPL 强传染 → block（FSF: 与专有代码聚合即整体受 GPL 约束）
    - LGPL/MPL/EPL/CDDL 弱传染 → warn（限定条件下可用，不得复制进自己的源文件）
    - CC 含 NC/ND → block（非自由软件许可，不可用于可再分发的软件包）
    - CC-BY / CC-BY-SA → warn（CC 官方不建议用于软件）
    - 宽松许可 → ok
    """
    if not spdx_id:
        return "unknown"
    s = spdx_id.upper().strip()
    if s.startswith("CC"):
        if s.startswith("CC0"):
            return "ok"
        if "NC" in s or "ND" in s:
            return "block"
        return "warn"  # CC-BY / CC-BY-SA 用于软件：官方不建议
    if s in PERMISSIVE:
        return "ok"
    if any(s.startswith(p) for p in STRONG_COPYLEFT_PREFIX):
        return "block"
    if any(s.startswith(p) for p in WEAK_COPYLEFT_PREFIX):
        return "warn"
    return "unknown"


def load_trademarks():
    # trademarks.txt 在技能根目录（scripts/ 的上一级）
    path = Path(__file__).resolve().parent.parent / "trademarks.txt"
    items = []
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                items.append(line)
    return items


def fetch_registry_license(name, version, cache):
    """node_modules 解析不到时，从 npm registry 兜底查询（可失败，不致命）。"""
    key = f"{name}@{version or 'latest'}"
    if key in cache:
        return cache[key]
    enc = urllib.parse.quote(name, safe="")
    url = f"https://registry.npmjs.org/{enc}/{version or 'latest'}"
    lic = None
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "release-infringement-audit/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        lic = data.get("license") or None
        if isinstance(lic, dict):
            lic = lic.get("type")
    except Exception:
        lic = None
    cache[key] = lic
    return lic


# ---------------------------------------------------------------- 审核器

class Audit:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.findings = []
        self._reg_cache = {}
        # 离线模式：不访问 npm registry（依赖名/版本属于私有信息，可能不愿外发）
        self.offline = False

    def _within_root(self, path):
        """路径解析后必须仍在被审项目内（防止 node_modules 里的 symlink 越界读取）。"""
        try:
            real = Path(path).resolve()
            root = self.root.resolve()
            return real == root or str(real).startswith(str(root) + os.sep)
        except OSError:
            return False

    def add(self, sev, cat, title, evidence, basis, fix):
        self.findings.append({
            "id": f"{cat}{len([f for f in self.findings if f['category'] == cat]) + 1}",
            "severity": sev, "category": cat, "title": title,
            "evidence": evidence, "basis": basis, "fix": fix,
        })

    # ---- 项目自身 license ----
    def detect_project_license(self):
        pkg = self.root / "package.json"
        field_lic = None
        if pkg.exists():
            try:
                data = json.loads(pkg.read_text(encoding="utf-8"))
                v = data.get("license")
                if isinstance(v, dict):
                    v = v.get("type")
                if v:
                    field_lic = str(v).strip()
            except Exception:
                self.add("WARN", "A", "package.json 无法解析",
                         str(pkg), "SPDX 要求 license 字段可机器读", "修复 JSON 语法")
        lic_file = None
        lic_path = None
        # 覆盖 LICENSE / LICENSE.md / LICENSE-APACHE-2.0.txt / COPYING 等变体
        for pat in ("LICENSE*", "LICENCE*", "COPYING*", "license*", "copying*"):
            for p in sorted(self.root.glob(pat)):
                if p.is_file() and p.stat().st_size < 1024 * 1024:
                    lic_path = p
                    break
            if lic_path:
                break
        if lic_path:
            lic_file = license_sniff(lic_path.read_text(encoding="utf-8", errors="replace"))
        # 多个 LICENSE 文件：可能是双许可、第三方声明文本或误放 → 提示人工确认
        multi = sorted(p for pat in ("LICENSE*", "LICENCE*", "COPYING*")
                       for p in self.root.glob(pat) if p.is_file())
        if len(multi) > 1:
            names = ", ".join(p.name for p in multi[:4])
            self.add("INFO", "A", f"存在多个许可文件（{names}）",
                     "可能是双许可（MIT OR Apache-2.0）、随附的第三方许可文本或误放",
                     "SPDX: 双许可须用表达式明确写出；第三方许可文本应在 NOTICES 引用",
                     "确认关系：双许可写 \"license\": \"MIT OR Apache-2.0\"；"
                     "第三方文本移入 THIRD-PARTY-NOTICES 并在 package.json 引用")
        if not lic_file and field_lic:
            self.add("WARN", "A", "未找到 LICENSE 文件，仅有 package.json 声明",
                     f"license 字段 = {field_lic}",
                     "choosealicense: 没有许可证 = 默认保留所有权利，他人无法合法使用",
                     "添加 LICENSE 文件并写明 SPDX id")
        if lic_file and not field_lic:
            self.add("WARN", "A", "有 LICENSE 文件但 package.json 无 license 字段",
                     f"{lic_path.name} 嗅探 = {lic_file or '未识别'}；npm 元数据缺 license",
                     "npm 官方要求 license 字段用 SPDX 表达式，缺字段时下游机器无法校验",
                     f"package.json 加 \"license\": \"{lic_file or 'SPDX 标识符'}\"")
        if not field_lic and not lic_file:
            self.add("BLOCK", "A", "项目完全未声明许可证",
                     "package.json 无 license 字段，且无 LICENSE 文件",
                     "choosealicense.com: 无许可证 = 默认版权保护，发布即侵权风险",
                     "选择一个 SPDX 许可证并写入 LICENSE 文件")
        if field_lic and lic_file:
            norm_f = field_lic.upper().split()[0].strip("()")
            norm_s = (lic_file or "").upper()
            if norm_f not in norm_s and norm_s not in norm_f:
                self.add("WARN", "A", "package.json 与 LICENSE 文件声明不一致",
                         f"package.json = {field_lic}，LICENSE 嗅探 = {lic_file}",
                         "SPDX: 两处声明冲突时下游无法确定有效许可",
                         "统一两处声明")
        return field_lic

    # ---- A: 依赖兼容性 ----
    def scan_dependencies(self):
        pkg = self.root / "package.json"
        if not pkg.exists():
            return
        try:
            data = json.loads(pkg.read_text(encoding="utf-8"))
        except Exception:
            return
        deps = {}
        for key in ("dependencies", "devDependencies", "optionalDependencies"):
            deps.update(data.get(key) or {})
        for name, want_ver in sorted(deps.items()):
            verdict_lic, src = None, None
            nm = self.root / "node_modules" / name / "package.json"
            if nm.is_file() and self._within_root(nm):
                try:
                    d = json.loads(nm.read_text(encoding="utf-8"))
                    verdict_lic, src = d.get("license"), "node_modules"
                except Exception:
                    pass
            if verdict_lic is None and not self.offline:
                verdict_lic = fetch_registry_license(name, want_ver, self._reg_cache)
                src = "registry"
            if verdict_lic is None and self.offline:
                self.add("INFO", "A", f"离线模式下依赖 license 无法解析: {name}",
                         "node_modules 中未找到该依赖，且默认不联网（--online 可开启 registry 查询）",
                         "默认不发送任何依赖信息到外部（隐私优先）",
                         "先 npm install 再审核，或加 --online")
                continue
            if verdict_lic is None:
                self.add("INFO", "A", f"依赖 license 无法解析: {name}",
                         f"node_modules 与 registry 均未取得 license 字段",
                         "SPDX: 未知许可证无法判定兼容性",
                         "npm install 后重扫，或人工到仓库确认其 LICENSE")
                continue
            for one in self._split_license_expr(verdict_lic, self.root / "node_modules" / name):
                v = classify(one)
                if v == "ok":
                    continue
                if v == "unknown":
                    self.add("WARN", "A", f"依赖许可证未知: {name} ({one})",
                             f"license 字段 = {verdict_lic!r}（来源 {src}）",
                             "SPDX: 无法识别的标识符",
                             "人工查看该包 LICENSE 原文")
                elif v == "block":
                    self.add("BLOCK", "A", f"依赖许可证与发布冲突: {name} ({one})",
                             f"license 字段 = {verdict_lic!r}（来源 {src}）",
                             self._basis_for(one),
                             self._fix_for(one))
                else:
                    self.add("WARN", "A", f"依赖为弱传染/受限许可: {name} ({one})",
                             f"license 字段 = {verdict_lic!r}（来源 {src}）",
                             self._basis_for(one),
                             self._fix_for(one))

    @staticmethod
    def _split_license_expr(val, pkg_root):
        """拆 'MIT OR Apache-2.0' / '(MIT OR X)' / 'SEE LICENSE IN xxx'。"""
        if isinstance(val, dict):
            val = val.get("type", "")
        val = str(val).strip()
        if not val:
            return [None]
        m = re.match(r"SEE LICENSE IN\s+(.+)", val, re.I)
        if m:
            f = pkg_root / m.group(1).strip()
            if f.is_file():
                sniff = license_sniff(f.read_text(encoding="utf-8", errors="replace"))
                return [sniff] if sniff else [None]
            return [None]
        val = val.replace("(", " ").replace(")", " ")
        out = []
        for chunk in val.split(" AND "):
            alts = [c.strip() for c in chunk.split(" OR ") if c.strip()]
            if not alts:
                continue
            if " OR " in chunk or len(alts) > 1:
                # OR 取最宽松的判定
                best, best_v = alts[0], classify(alts[0])
                rank = {"ok": 0, "warn": 1, "unknown": 2, "block": 3}
                for a in alts[1:]:
                    if rank[classify(a)] < rank[best_v]:
                        best, best_v = a, classify(a)
                out.append(best)
            else:
                out.append(alts[0])
        return out or [None]

    @staticmethod
    def _basis_for(lic):
        u = lic.upper()
        if u.startswith(("GPL", "AGPL", "SSPL")):
            return ("FSF GPL FAQ（gnu.org/licenses/gpl-faq）：GPL 代码与你的代码聚合后"
                    "整体须以 GPL 发布，npm 分发即触发")
        if "NC" in u or "ND" in u:
            return ("Creative Commons FAQ：NC/ND 不是自由软件许可，"
                    "CC 官方明确不建议用于软件")
        if u.startswith(("LGPL", "MPL", "EPL", "CDDL")):
            return ("FSF/choosealicense：弱传染许可限定条件下可用；"
                    "复制其源码进你的文件则该文件须同样开源")
        if u.startswith("CC"):
            return "Creative Commons 官方：CC 许可证设计用于内容而非软件"
        return "SPDX license list（spdx.org/licenses）"

    @staticmethod
    def _fix_for(lic):
        u = lic.upper()
        if u.startswith(("GPL", "AGPL", "SSPL")):
            return "移除该依赖，或换等效宽松许可实现；确需保留则整包改 GPL 并接受传染"
        if "NC" in u or "ND" in u:
            return "换掉该素材/依赖，或取得权利人商业授权"
        if u.startswith(("LGPL", "MPL", "EPL", "CDDL")):
            return "保持独立文件引用（不复制进你的源码），在 THIRD-PARTY-NOTICES 中声明"
        return "与本项目许可证核对兼容性"

    # ---- B: 复制的第三方代码 ----
    def scan_snippets(self, owner_names):
        # 声明类文件本身就是「他人版权行」的合法载体，跳过
        DECLARATION_RE = re.compile(
            r"NOTICE|CREDITS|ATTRIBUTION|THIRD[-_]?PARTY|AUTHORS|CONTRIBUTORS", re.I)
        for p in iter_files(self.root):
            # 只看源码文件：文档和测试夹具里出现的许可证/版权示例不是真声明
            if p.suffix.lower() not in SOURCE_EXTS:
                continue
            if p.name.upper().startswith("LICENSE") or DECLARATION_RE.search(p.name):
                continue
            try:
                text = p.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            rel = p.relative_to(self.root)
            lines = text.splitlines()
            # SPDX 头：注释行 + 文件开头窗口（SPDX 约定头部声明）
            for idx, raw in enumerate(lines[:SPDX_HEADER_WINDOW]):
                if not COMMENT_START_RE.match(raw):
                    continue
                m = SPDX_RE.search(raw)
                if not m:
                    continue
                lic = m.group(1)
                v = classify(lic)
                line = idx + 1
                if v == "block":
                    self.add("BLOCK", "B", f"文件标注强传染许可证: {rel}",
                             f"L{line}: SPDX-License-Identifier: {lic}",
                             self._basis_for(lic),
                             "删除该文件或联系原作者取得宽松授权；保留则整包须遵守该许可证")
                elif v == "warn":
                    self.add("WARN", "B", f"文件声明了受限许可证: {rel}",
                             f"L{line}: SPDX-License-Identifier: {lic}",
                             self._basis_for(lic),
                             "确认来源并按要求保留声明 + 记入 THIRD-PARTY-NOTICES")
                elif v == "unknown":
                    self.add("WARN", "B", f"文件标注了无法识别的许可证: {rel}",
                             f"L{line}: SPDX-License-Identifier: {lic}",
                             "SPDX: 标识符不在 license list 中",
                             "核对 SPDX 官网写法，确认原文许可")
                elif lic:  # ok 类：源文件自带宽松许可头 → 疑似第三方代码
                    self.add("INFO", "B", f"文件自带宽松许可头（疑似第三方代码）: {rel}",
                             f"L{line}: SPDX-License-Identifier: {lic}",
                             "自有源文件通常无需 SPDX 头；出现即需核实来源",
                             "确认来源；第三方代码记入 THIRD-PARTY-NOTICES")
            # 版权行与来源标注：同样只认注释行（真声明都在注释里）
            for idx, raw in enumerate(lines):
                if not COMMENT_START_RE.match(raw):
                    continue
                line = idx + 1
                for m in COPYRIGHT_RE.finditer(raw):
                    name = m.group(1).strip()
                    low = name.lower()
                    if any(o.lower() in low or low in o.lower() for o in owner_names):
                        continue
                    if re.fullmatch(r"(the\s+)?(project|authors?|contributors|this\s+\w+)\s*.*", low):
                        continue
                    self.add("WARN", "B", f"疑似他人版权行: {rel}",
                             f"L{line}: {m.group(0).strip()[:90]}",
                             "《著作权法》: 他人代码的著作权不因复制而转移",
                             "确认该文件来源；若为第三方代码，保留声明并记入 NOTICES")
                for m in COPIED_RE.finditer(raw):
                    self.add("INFO", "B", f"疑似复制自外部项目: {rel}",
                             f"L{line}: {m.group(0).strip()[:90]}",
                             "来源标注存在 → 需核实其许可证",
                             "核实来源项目许可证后保留署名或移除")

    # ---- C: 素材 ----
    def scan_content(self):
        has_credits = any(p.name.upper().startswith(("CREDITS", "ATTRIBUTION", "THIRD-PARTY"))
                          for p in self.root.iterdir() if p.is_file())
        fonts, imgs = [], []
        for p in iter_files(self.root):
            ext = p.suffix.lower()
            if ext in FONT_EXTS:
                fonts.append(p)
            elif ext in IMG_EXTS:
                imgs.append(p)
        for f in fonts:
            sibs = [q.name for q in f.parent.iterdir()]
            if not any("license" in s.lower() or "ofl" in s.lower() for s in sibs):
                rel = f.relative_to(self.root)
                self.add("WARN", "C", f"字体文件缺少许可说明: {rel}",
                         "同目录无 LICENSE/OFL 说明文件",
                         "绝大多数商用字体禁止再分发；OFL 字体须随附 OFL.txt",
                         "换开源字体（如思源/Noto，OFL）并附许可文件")
        for img in imgs:
            if img.suffix.lower() == ".svg":
                try:
                    t = img.read_text(encoding="utf-8", errors="replace")
                    if "base64," in t:
                        rel = img.relative_to(self.root)
                        self.add("WARN", "C", f"SVG 内嵌 base64 位图: {rel}",
                                 "含 data:image/...;base64 —— 来源无法自动确认",
                                 "嵌入图可能是下载来的版权图",
                                 "确认来源，或改为矢量绘制")
                except Exception:
                    pass
        if imgs and not has_credits:
            self.add("INFO", "C", f"存在 {len(imgs)} 个图片文件但无 CREDITS/署名文件",
                     "; ".join(p.relative_to(self.root).name for p in imgs[:5]),
                     "无法自动确认图片来源",
                     "自行创作可忽略；否则注明来源与许可")
        for p in iter_files(self.root):
            if p.suffix.lower() not in (".md", ".txt", ".html"):
                continue
            if p.name.upper().startswith("LICENSE"):
                continue
            try:
                text = p.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            for m in re.finditer(r"CC[- ]BY[- ](NC|ND)[-\w.]*|禁止商用|不得用于商业用途|非商业", text):
                line = text[:m.start()].count("\n") + 1
                rel = p.relative_to(self.root)
                # 只有在「声明许可/署名」的文件里才是真约束；
                # 说明文档里解释 NC/ND 规则属于正常写作 → 降为 INFO
                if LICENSEISH_RE.search(p.name):
                    self.add("WARN", "C", f"许可/署名文件声明了 NC/ND 授权: {rel}",
                             f"L{line}: {m.group(0)}",
                             "NC/ND 素材不可用于可再分发的软件项目",
                             "更换素材或取得授权")
                else:
                    self.add("INFO", "C", f"文档提到 NC/ND 授权（需确认是否为项目自身素材）: {rel}",
                             f"L{line}: {m.group(0)}",
                             "可能是解释许可证规则，也可能是项目素材确实受限",
                             "确认该处指的是自家素材还是引用说明")
                break

    # ---- D: 商标 ----
    def scan_trademark(self):
        marks = load_trademarks()
        if not marks:
            return
        names = []
        pkg = self.root / "package.json"
        if pkg.exists():
            try:
                names.append(("package.json name", json.loads(pkg.read_text(encoding="utf-8")).get("name") or ""))
            except Exception:
                pass
        readme = None
        for cand in ("README.md", "README_EN.md", "readme.md", "README.en.md"):
            if (self.root / cand).is_file():
                readme = self.root / cand
                break
        h1 = ""
        if readme:
            for line in readme.read_text(encoding="utf-8", errors="replace").splitlines():
                if line.strip().startswith("# "):
                    h1 = line.lstrip("# ").strip()
                    break
            names.append(("README 标题", h1))
        for src, nm in names:
            if not nm:
                continue
            for mk in marks:
                hit = None
                if re.fullmatch(r"[\x00-\x7f]+", mk):
                    if re.search(r"(?i)(?<![a-z0-9])" + re.escape(mk) + r"(?![a-z0-9])", nm):
                        hit = mk
                else:
                    if mk in nm:
                        hit = mk
                if hit:
                    self.add("WARN", "D", f"项目命名命中知名商标「{hit}」: {src}",
                             f"{src} = {nm}",
                             "《商标法》: 未经许可在同类商品/服务上使用他人商标可能侵权；"
                             "描述性使用（「X for Y」）通常可主张指示性使用",
                             "若为描述性用途注明「不隶属于 Y」；作为品牌名使用建议改名")
                    break

    # ---- E: 密钥（只读扫描，绝不执行被审项目代码）----
    def scan_secrets(self):
        # 安全边界：绝不执行被审项目里的任何脚本。
        # 被审仓库可能是恶意的（这正是审核存在的理由），执行它的 check-secrets.sh
        # 等于把任意代码执行权交给被审对象 —— ClawHub 的 aig/skillspector 曾按
        # High 风险判定此行为，修复方式是彻底移除执行路径，而不是加开关。
        # 内置规则已覆盖 check-secrets.sh 的模式并做了扩展，无需委托。
        hook = self.root / "check-secrets.sh"
        if hook.is_file():
            self.add("INFO", "E", "项目自带 check-secrets.sh（已跳过执行）",
                     f"发现 {hook.name}；为安全起见不执行被审项目的脚本",
                     "审核工具会打开不可信仓库；执行其中脚本即任意代码执行",
                     "需要时请自行在可信环境运行该脚本；内置规则已覆盖其模式")
        for p in iter_files(self.root):
            # 密钥文件常以 .pem/.key 等扩展名存在，必须纳入扫描
            if (p.suffix.lower() not in TEXT_EXTS
                    and p.suffix.lower() not in {".pem", ".key", ".crt", ".cer", ".p12", ".pfx"}
                    and p.suffix != ""):
                continue
            if p.stat().st_size > 1024 * 1024:
                continue
            try:
                text = p.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            for pat, desc in SECRET_PATTERNS:
                for m in re.finditer(pat, text):
                    line = text[:m.start()].count("\n") + 1
                    rel = p.relative_to(self.root)
                    self.add("BLOCK", "E", f"{desc}: {rel}",
                             f"L{line}: 模式命中（值已隐藏，不在报告中回显）",
                             "密钥一旦公开必须先吊销再清理（AGENTS.md 密钥安全章节）",
                             "改为占位符、移入 .env（.gitignore 已拦）并吊销已泄露 key")

    # ---- 汇总 ----
    def worst(self):
        if any(f["severity"] == "BLOCK" for f in self.findings):
            return 2
        if any(f["severity"] == "WARN" for f in self.findings):
            return 1
        return 0

    def render_md(self):
        lines = ["# 发布前侵权风险审核报告", "",
                 f"- 审核目录: `{self.root}`",
                 f"- 结论: " + self._verdict_text(),
                 f"- 发现: BLOCK ×{sum(1 for f in self.findings if f['severity']=='BLOCK')} · "
                 f"WARN ×{sum(1 for f in self.findings if f['severity']=='WARN')} · "
                 f"INFO ×{sum(1 for f in self.findings if f['severity']=='INFO')}", ""]
        if not self.findings:
            lines += ["✅ 未发现自动化可识别的侵权风险点。", "",
                      "> 仍建议人工复核：README 引用的外部图片、README 大段引文、图标是否原创。", ""]
        for cat in "ABCDE":
            items = [f for f in self.findings if f["category"] == cat]
            if not items:
                continue
            lines.append(f"## {cat} {CAT_NAMES[cat]}")
            for f in items:
                lines.append(f"- **[{f['severity']}] {f['title']}**")
                lines.append(f"  - 证据: {f['evidence']}")
                lines.append(f"  - 依据: {f['basis']}")
                lines.append(f"  - 处置: {f['fix']}")
            lines.append("")
        lines.append("---")
        lines.append(DISCLAIMER)
        return "\n".join(lines) + "\n"

    def _verdict_text(self):
        w = self.worst()
        if w == 2:
            return "🚫 不建议发布（存在阻断项）"
        if w == 1:
            return "🟡 修复警告后可发布"
        return "✅ 可发布"


def main():
    ap = argparse.ArgumentParser(description="发布前侵权风险审核")
    ap.add_argument("project", help="项目目录")
    ap.add_argument("--format", choices=("md", "json"), default="md")
    ap.add_argument("--out", help="写入文件而非 stdout")
    ap.add_argument("--online", action="store_true",
                    help="允许访问 npm registry 解析未安装依赖的许可证（默认不联网）")
    args = ap.parse_args()

    root = Path(args.project)
    if not root.is_dir():
        print(f"错误: {root} 不是目录", file=sys.stderr)
        return 2

    audit = Audit(root)
    audit.offline = not bool(args.online)
    owner_names = set()
    pkg = root / "package.json"
    if pkg.exists():
        try:
            d = json.loads(pkg.read_text(encoding="utf-8"))
            a = d.get("author")
            if isinstance(a, dict):
                a = a.get("name")
            if a:
                owner_names.add(str(a))
            repo = (d.get("repository") or "")
            if isinstance(repo, dict):
                repo = repo.get("url", "")
            m = re.search(r"github\.com[/:]([\w-]+)", str(repo))
            if m:
                owner_names.add(m.group(1))
            if d.get("name"):
                owner_names.add(str(d["name"]))
        except Exception:
            pass

    audit.detect_project_license()
    audit.scan_dependencies()
    audit.scan_snippets(owner_names or {"placeholder-owner"})
    audit.scan_content()
    audit.scan_trademark()
    audit.scan_secrets()

    if args.format == "json":
        out = json.dumps({"project": str(audit.root), "verdict": audit._verdict_text(),
                          "exit_hint": audit.worst(), "findings": audit.findings,
                          "disclaimer": DISCLAIMER},
                         ensure_ascii=False, indent=2)
    else:
        out = audit.render_md()
    if args.out:
        Path(args.out).write_text(out, encoding="utf-8")
        print(f"报告已写入 {args.out}")
    else:
        print(out)
    return audit.worst()


if __name__ == "__main__":
    sys.exit(main())
