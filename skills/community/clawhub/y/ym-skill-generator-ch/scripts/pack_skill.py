#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pack_skill.py — 技能校验 + 打包 + 安装

配套脚本：
    new_skill.py   从需求生成合规骨架（生成即体检）
    audit_skill.py 单跑体检（人读 / --json 机器读）
    make_icon.py   技能图标：生成提示词 → 居中裁切 + 清生成标 → 512×512 / ≤500KB

用法:
    python scripts/pack_skill.py <技能目录> [选项]

产出形态:
    默认（★ 上传用这个）
        技能目录包 —— zip 顶层 = <技能名>/，内含 SKILL.md + references/ + scripts/ + templates/。
        它既是**本机技能包**（解压即得技能目录，装到 ~/.workbuddy/skills），
        也是**开放平台「技能」类目的上传包** —— 官方要求就是技能目录本身，
        **不需要** .codebuddy-plugin/plugin.json。

    --as-plugin
        插件形态包 —— <插件名>/.codebuddy-plugin/plugin.json + <插件名>/skills/<技能名>/...
        用于**插件市场**分发（团队 marketplace、把技能挂到一个插件下）。
        ⚠️ **上传 open.workbuddy.cn「技能」类目不要用这个包**：
        平台是在技能目录下找 SKILL.md，这种包里 SKILL.md 被埋在 skills/<技能名>/ 下，
        会直接报「压缩包缺少 SKILL.md 文件」。

交付定义:
    打包的终点是「本机有一份可用的技能」，zip 是给别人的分发副本。
    因此**默认就会安装到 ~/.workbuddy/skills**，不是可选项。

不进包的东西（技能包只装技能本身）:
    · 构建缓存：__pycache__ / node_modules / *.pyc / *.log …
    · 仓库元数据：.git/ / .gitignore / .gitattributes / README.md / LICENSE …
    · 发布图标：icons/ 下的图标 —— 平台在创建技能时**单独**收这个文件，
      不随 zip 走（用 scripts/make_icon.py 生成，512×512 / PNG·JPG / ≤500KB）

选项:
    --out <目录>           zip 输出目录（默认：当前工作目录）
    --platform             产出开放平台插件包（含 .codebuddy-plugin/plugin.json）
    --flat-root            平台包不带顶层目录（zip 根即插件根）；仅当平台拒绝顶层目录时用
    --install-dir <目录>   安装目标（默认 ~/.workbuddy/skills）
    --no-install           只打 zip，不安装（仅当只是帮别人打包时才用）
    --allow-p1             接受 P1 警告继续打包（P0 永远阻断）
    --market               按技能市场分发规范加严检查（frontmatter 必填字段、kebab-case name）
    --no-market            跳过市场分发规范检查（仅本机自用时才用）
    --force                安装时覆盖已存在的同名技能
    --dry-run              只体检 + 打印将打包的文件清单，不写 zip
    --quiet                简版输出

退出码:
    0 成功 | 2 体检 P0 | 1 体检 P1 且未加 --allow-p1 | 3 参数错误 | 4 打包失败
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True          # 体检/打包不该在技能目录里留 __pycache__
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _friendly import die, explain_exit, make_backup, use_utf8_stdout  # noqa: E402
from _paths import (PathResolutionError, SKILLS_HOME_ENV,  # noqa: E402
                    skills_dir, skills_dir_of)
from audit_skill import JUNK_DIRS, JUNK_FILES, JUNK_SUFFIX, audit  # noqa: E402

# 技能市场分发规范字段：(字段名, 是否硬性)
# 与 audit_skill.py 的 MARKET_REQUIRED / MARKET_RECOMMENDED 保持同一套口径 ——
# 分头维护两套清单，正是「本地看着齐备、平台读不到」那类问题的病根。
MARKET_FIELD_SPEC = [
    ("name", True), ("slug", False),
    ("displayName", True),                                   # 平台（SkillHub）的展示名，驼峰
    ("display_name", False), ("display_name_en", False),      # WorkBuddy 本机展示名
    ("description", True), ("description_zh", True), ("description_en", True),
    ("summary", False), ("tags", False),
    ("category", False), ("version", True), ("author", False),
]

# description 尾部触发词串的分界词（市场展示位不该带这串）
TRIGGER_TAIL_RE = re.compile(r"当用户(?:说|提到)|也适用于|亦适用于|触发词[:：]?|使用场景[:：]?")

# 不打进技能包的目录 / 文件。技能包只装「技能本身」，不装仓库与发布产物：
#   · 仓库元数据：`.git/` 与 `.gitignore` / `.gitattributes` 这类是版本控制的东西，
#     跟技能能不能跑毫无关系，打进去只会污染 zip（`.git/` 已被 JUNK_DIRS 覆盖）。
#   · `icons/`：技能的发布图标。平台是在创建技能时的「图标」处**单独**收这个文件，
#     不进 zip；留在技能目录里只是方便再次发布时取用。
REPO_META_DIRS = {".github", ".gitlab", ".circleci", ".azure"}
REPO_META_FILES = {
    ".gitignore", ".gitattributes", ".gitmodules", ".gitkeep", ".editorconfig",
    ".travis.yml", ".gitlab-ci.yml", ".npmrc", ".prettierrc", ".prettierrc.json",
    "README.md", "README_zh.md", "README_EN.md", "CHANGELOG.md", "CONTRIBUTING.md",
    "LICENSE", "LICENSE.md", "LICENSE.txt",
}
ICON_DIRS = {"icons", "icon"}


def _excluded_dir(name: str) -> bool:
    return name in REPO_META_DIRS or name in ICON_DIRS



def market_field_report(root: Path):
    """逐项核对市场规范字段的齐备情况，让「按规范打包」有可见证据。

    返回 (齐备的必填数, 必填总数, [展示用条目...])。
    """
    text = (root / "SKILL.md").read_text(encoding="utf-8", errors="replace")
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    fm = m.group(1) if m else ""      # 支持 metadata: 下的缩进嵌套字段
    items, ok_req, total_req = [], 0, 0
    for key, required in MARKET_FIELD_SPEC:
        has = bool(re.search(r"^[ \t]*%s:" % re.escape(key), fm, re.M))
        if required:
            total_req += 1
            ok_req += 1 if has else 0
            state = "已填" if has else "缺失"
        else:
            state = "已填" if has else "未填（建议补）"
        items.append((key, has, required, state))
    return ok_req, total_req, items


def collect_packable(root: Path):
    """返回 (要打包的文件列表, 被排除的垃圾列表, 被排除的图标文件列表)。

    排除四类：构建缓存（JUNK_*）、仓库元数据（`.gitignore` / `README.md`…）、
    发布图标（`icons/`）、以及 `.skillignore` 里指定的文件。
    前三类不是「垃圾」，是**不该进技能包**——图标由平台在「图标」处单独收，
    仓库元数据只对 git 有意义。
    """
    from audit_skill import _ignored_by_glob, load_skillignore
    si_globs, _ = load_skillignore(root)

    keep, dropped, icons = [], [], []
    for dirpath, dirnames, filenames in os.walk(root):
        d = Path(dirpath)
        keepdirs = []
        for dn in dirnames:
            if si_globs and _ignored_by_glob(
                    str((d / dn).relative_to(root)).replace("\\", "/"), si_globs):
                dropped.append(d / dn)
            elif dn in JUNK_DIRS or dn in REPO_META_DIRS:
                dropped.append(d / dn)
            elif dn in ICON_DIRS:
                for sub in sorted((d / dn).rglob("*")):
                    if sub.is_file():
                        icons.append(sub)
            else:
                keepdirs.append(dn)
        dirnames[:] = keepdirs
        for fn in filenames:
            p = d / fn
            if si_globs and _ignored_by_glob(
                    str(p.relative_to(root)).replace("\\", "/"), si_globs):
                dropped.append(p)
            elif fn in JUNK_FILES or p.suffix.lower() in JUNK_SUFFIX:
                dropped.append(p)
            elif fn in REPO_META_FILES:
                dropped.append(p)
            elif any(part in ICON_DIRS for part in p.relative_to(root).parts[:-1]):
                icons.append(p)
            else:
                keep.append(p)
    return sorted(keep), sorted(dropped), sorted(icons)


# 正文里讲「这类文件不进包」的表格行 / 踩坑条目，会顺带提到 README.md 的名字。
# 那是在陈述排除规则，不是引用它，不该算悬空。
EXPLAIN_HINT_RE = re.compile(r"不进包|打进包|排除|仓库元数据|只对 git|既没用|漏出仓库")


def _is_example_ref(t: str) -> bool:
    """只判「写作示例」占位符；约定可选文件（CHANGELOG 等）**不算**占位符。

    `audit_skill` 把 changelog.md 列进 CONVENTIONAL_OPTIONAL 是对的——技能没有
    CHANGELOG 完全正常，不该因此判「引用缺失」。但**一旦正文显式引用了它**，
    性质就变了：它从「可有可无」变成「被依赖」。此时若还被打包排除掉，
    用户装上就是悬空引用。所以这一步刻意不查 CONVENTIONAL_OPTIONAL。
    """
    from audit_skill import PLACEHOLDER_SEGMENT
    if re.search(r"(?i)\.(example|template|sample|dist)(\.|$)", Path(t).name):
        return True
    for seg in re.split(r"[\\/]", t):
        if not seg:
            continue
        if PLACEHOLDER_SEGMENT.match(seg) or PLACEHOLDER_SEGMENT.match(Path(seg).stem):
            return True
    return False


def check_pack_refs(root: Path, files, dropped):
    """包内引用完整性：找出「源码树里有、但被打包排除」的引用。

    `audit_skill.check_refs` 以**源码树**为基准解析引用——被打包排除的文件
    在源码树里依然存在，所以它判通过。但用户装上技能包后那个文件根本不存在，
    SKILL.md 里的引用就成了悬空指针。这一步补的正是这个 gap：
    只报「被 dropped 掉的、同时又被正文引用了」的文件，误报极少。
    """
    from audit_skill import (DOC_EXT, OUTPUT_HINT_RE, REF_PATTERNS,
                             is_placeholder_path, scan_lines)

    inpack = {str(f.relative_to(root)).replace("\\", "/"): f for f in files}
    dropped_set = {str(d.relative_to(root)).replace("\\", "/") for d in dropped}

    hits = []
    for f in files:
        if f.suffix.lower() not in DOC_EXT:
            continue
        rel = str(f.relative_to(root)).replace("\\", "/")
        for lineno, line in scan_lines(f):
            if OUTPUT_HINT_RE.search(line) or EXPLAIN_HINT_RE.search(line):
                continue          # 运行时产物 / 排除规则说明，本来就不在包里
            seen = set()
            for rx in REF_PATTERNS:
                for m in rx.finditer(line):
                    t = m.group(1)
                    if t in seen:
                        continue
                    seen.add(t)
                    if _is_example_ref(t):
                        continue  # references/xxx.md 这类写作示例不算引用
                    norm = t.replace("\\", "/")
                    if norm in inpack:
                        continue  # 包里有，正常
                    if norm in dropped_set:
                        hits.append((rel, lineno, t))
    return hits


def collect_empty_dirs(root: Path, files):
    """找出递归下去一个文件都没有的目录。

    必须写进 zip：刚用 new_skill.py 生成的骨架，`scripts/`、`references/` 是空的，
    不写目录条目的话解压后结构就丢了，「解压即得规范结构」不成立。
    """
    with_files = set()
    for f in files:
        for p in f.parents:
            if p == root.parent:
                break
            with_files.add(p)
    out = []
    for dirpath, dirnames, _ in os.walk(root):
        dirnames[:] = [d for d in dirnames
                       if d not in JUNK_DIRS and d not in REPO_META_DIRS and d not in ICON_DIRS]
        d = Path(dirpath)
        if d != root and d not in with_files:
            out.append(d)
    return sorted(out)


def build_zip(root: Path, out_dir: Path, files, name: str, empty_dirs=()) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    zip_path = out_dir / ("%s.zip" % name)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            zf.write(f, f.relative_to(root.parent))
        for d in empty_dirs:
            zf.writestr(str(d.relative_to(root.parent)).replace("\\", "/") + "/", b"")
    return zip_path


def is_inside(child: Path, parent: Path) -> bool:
    """child 是否位于 parent 之内。

    用于判断「源技能目录是否已经是本机已装技能」——是的话必须跳过安装，
    否则安装会把源目录当成待覆盖目标删掉，等于打包时自我删除。
    """
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except (ValueError, OSError):
        return False


def read_frontmatter(root: Path) -> dict:
    """解析 SKILL.md 的 YAML frontmatter（够用即可，不引第三方库）。

    特意处理 YAML 折叠块（`>-` / `|`）：description 这类长文本常这么写，
    只认单行标量会把它读成空串，生成的 plugin.json 描述就丢了。
    """
    text = (root / "SKILL.md").read_text(encoding="utf-8", errors="replace")
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}
    data, key = {}, None
    for line in m.group(1).splitlines():
        if re.match(r"^[A-Za-z0-9_.-]+\s*:", line):          # 新的顶层键
            k, _, v = line.partition(":")
            key, v = k.strip(), v.strip().strip("\"'")
            if v in (">", "|", ">-", "|-"):
                data[key] = ""                               # 折叠块，内容在后续缩进行
            elif v.startswith("[") and v.endswith("]"):
                data[key] = [x.strip().strip("\"'") for x in v[1:-1].split(",") if x.strip()]
            else:
                data[key] = v
        elif key and line.strip().startswith("- "):          # YAML 列表项
            data.setdefault("__list_" + key, []).append(line.strip()[2:].strip().strip("\"'"))
        elif key and line[:1] in (" ", "\t") and line.strip():   # 折叠块续行
            data[key] = (str(data.get(key, "")) + " " + line.strip()).strip()
    return data


def build_plugin_json(root: Path, name: str) -> dict:
    """从 SKILL.md 生成开放平台插件清单。

    平台校验的是这个文件，不是 SKILL.md —— 缺它直接报
    「压缩包缺少 .codebuddy-plugin/plugin.json」，技能写得多好都传不上去。
    `name` 是唯一必需字段，其余字段尽量从 frontmatter 映射。
    """
    fm = read_frontmatter(root)
    author = fm.get("author") or ""
    if isinstance(author, list):
        author = author[0] if author else ""
    pj = {"name": name, "version": fm.get("version") or "1.0.0"}

    # 描述：去掉尾部那串触发词后再截断。
    # 触发词是给模型判断触发用的，一股脑搬进市场展示位会又长又难读；
    # 但功能描述本身要留全——平台中文搜索匹配的就是它。
    #
    # 分界词要覆盖全：「当用户说…」「也适用于…」「触发词：…」「使用场景：…」都常见，
    # 之前只认「当用户说」，导致「也适用于『生成专家包』这类说法」整句残留进市场文案。
    full = TRIGGER_TAIL_RE.split(fm.get("description") or "")[0]
    desc = re.sub(r"\s+", " ", full).strip() or (fm.get("description_zh") or "")
    if len(desc) > 200:
        desc = desc[:197].rstrip() + "..."
    # 折叠块拼出来的中文之间会夹空格（YAML 把换行折成空格），清掉更像人话
    desc = re.sub(r"(?<=[\u4e00-\u9fff，。、；：（）「」])[ \t]+"
                  r"(?=[\u4e00-\u9fff，。、；：（）「」])", "", desc)
    if desc:
        pj["description"] = desc
    if fm.get("description_en"):
        pj["description_en"] = re.sub(r"\s+", " ", fm["description_en"]).strip()

    if author:
        pj["author"] = {"name": author}

    # category：技能上架规范的**展示分类**，是独立字段（线上技能插件都有）。
    # ⚠️ 别和专家的 `categoryId`（数字枚举）混 —— 那是另一套规范。
    if fm.get("category"):
        pj["category"] = fm["category"]

    # keywords：名字拆词 + 触发词，去重后给平台检索用（category 已单独成字段，不重复塞）
    kws = []
    for src in name.split("-") + fm.get("__list_trigger", [])[:6]:
        if src and src not in kws:
            kws.append(src)
    if kws:
        pj["keywords"] = kws

    # 不写 `skills` 字段：技能放在 skills/ 就是平台默认位置，靠默认发现即可。
    # 线上插件 finance-data（4 个技能同布局）同样没写这个字段，是验证过的做法；
    # 反而显式写 `["./skills"]` 有语义风险——若平台把它当"技能目录列表"，
    # 会去找该目录下层的 SKILL.md（不存在）而漏掉下面的技能。
    return pj


def build_plugin_zip(root: Path, out_dir: Path, name: str, files, empty_dirs, plugin_json,
                     flat_root: bool = False) -> Path:
    """打成开放平台能认的插件包。

    结构（与平台真实插件一致）：
        flat_root=False → <name>/.codebuddy-plugin/plugin.json
                          <name>/skills/<name>/SKILL.md + scripts/ + references/ ...
        flat_root=True  → .codebuddy-plugin/plugin.json
                          skills/<name>/SKILL.md + ...        （zip 根即插件根）

    技能统一放进 `skills/` —— 平台文档的默认技能位置，不必依赖额外声明。
    顶层目录要不要带，平台报错信息区分不出来，所以两种都留一手。
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    # 文件名加 -plugin 后缀，与本机技能包区分（两者结构不同，混在一起会拿错）
    zip_path = out_dir / ("%s-plugin%s.zip" % (name, "-flat" if flat_root else ""))
    base = "" if flat_root else "%s/" % name
    prefix = "%sskills/%s" % (base, name)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("%s.codebuddy-plugin/plugin.json" % base,
                    json.dumps(plugin_json, ensure_ascii=False, indent=2) + "\n")
        for f in files:
            rel = f.relative_to(root).as_posix()
            zf.write(f, "%s/%s" % (prefix, rel))
        for d in empty_dirs:
            zf.writestr("%s/%s/" % (prefix, d.relative_to(root).as_posix()), b"")
    return zip_path


def install_skill(root: Path, target_dir: Path, name: str, force: bool, files, empty_dirs=()):
    target = target_dir / name
    if target.exists():
        if not force:
            print("!! 目标已存在：%s（要覆盖请加 --force）" % target)
            return None
        # 双重保险：绝不把自己删掉
        if is_inside(root, target):
            print("!! 源目录即目标目录，拒绝覆盖：%s" % target)
            return None
        print("!! 覆盖已有技能目录：%s" % target)
        # 先备份再覆盖：旧版直接 rmtree，复制中途失败本机技能就没了
        bak = make_backup(target)
        print("   旧版已备份到：%s" % bak)
    target.mkdir(parents=True, exist_ok=True)
    for f in files:
        rel = f.relative_to(root)
        dst = target / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, dst)
    for d in empty_dirs:            # 保留空目录，结构与本机副本一致
        (target / d.relative_to(root)).mkdir(parents=True, exist_ok=True)
    return target


def main():
    use_utf8_stdout()

    ap = argparse.ArgumentParser(description="技能校验 + 打包 + 安装")
    ap.add_argument("skill_dir")
    ap.add_argument("--out", default=None, help="zip 输出目录")
    ap.add_argument("--as-plugin", "--platform", action="store_true", dest="platform",
                    help="产出「插件形态」包（.codebuddy-plugin/plugin.json + skills/<技能名>/），"
                         "用于插件市场分发；上传开放平台技能类目不要用它，直接传默认包")
    ap.add_argument("--flat-root", action="store_true",
                    help="平台包不带顶层目录（zip 根即插件根）；平台若不接受顶层目录时用")
    ig = ap.add_mutually_exclusive_group()
    ig.add_argument("--install", action="store_true", dest="install", default=True,
                    help="安装到技能目录（默认开启）")
    ig.add_argument("--no-install", action="store_false", dest="install",
                    help="只打 zip，不安装")
    ap.add_argument("--install-dir", default=None, help="默认 ~/.workbuddy/skills")
    ap.add_argument("--allow-p1", action="store_true")
    mg = ap.add_mutually_exclusive_group()
    mg.add_argument("--market", action="store_true", dest="market", default=True,
                    help="按技能市场分发规范检查（默认开启）")
    mg.add_argument("--no-market", action="store_false", dest="market",
                    help="跳过市场分发规范检查（仅本机自用时才用）")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    root = Path(args.skill_dir).expanduser().resolve()
    if not root.is_dir():
        die(3, "技能目录不存在或不是目录：%s" % root,
            "确认路径拼写；含空格要加引号；也可以先跑 audit_skill.py --selftest 确认环境正常")
    if not (root / "SKILL.md").exists():
        die(3, "目标目录里没有 SKILL.md，不是技能目录：%s" % root,
            "要么进错目录了，要么技能还没建；先用 new_skill.py 生成骨架")

    # ---------- 1. 体检 ----------
    print("[1/4] 体检 ...%s" % ("  模式：技能市场分发规范" if args.market else ""))
    rep = audit(root, market=args.market)
    p0, p1, p2 = rep.count("P0"), rep.count("P1"), rep.count("P2")
    print("      P0=%d  P1=%d  P2=%d" % (p0, p1, p2))

    if args.market:
        ok_req, total_req, items = market_field_report(root)
        print("      市场分发字段：必填 %d/%d 齐备" % (ok_req, total_req))
        for key, has, required, state in items:
            flag = "!" if (required and not has) else " "
            print("        %s %-16s %s" % (flag, key, state))

    if p0:
        print("\n体检未通过，禁止打包。请先修复以下 P0 项：\n")
        for f in rep.findings():
            if f["severity"] != "P0":
                continue
            hits = f["hits"]
            where = ", ".join(str(h["line"]) for h in hits[:6] if h["line"]) or "-"
            print("  [%s] %s" % (f["category"], f["rule"]))
            print("      位置: %s:%s" % (f["file"], where))
            if hits and hits[0]["sample"]:
                print("      样例: %s" % hits[0]["sample"])
            if f["hint"]:
                print("      改法: %s" % f["hint"])
            print()
        print("    %s" % explain_exit(2))
        raise SystemExit(2)

    if p1 and not args.allow_p1:
        print("\n存在 %d 类 P1 警告，默认不打包。修复后重跑，或确认安全后加 --allow-p1：\n" % p1)
        for f in rep.findings():
            if f["severity"] != "P1":
                continue
            hits = f["hits"]
            where = ", ".join(str(h["line"]) for h in hits[:6] if h["line"]) or "-"
            print("  [%s] %s  (%d 处)" % (f["category"], f["rule"], len(hits)))
            print("      %s:%s" % (f["file"], where))
            if hits and hits[0]["sample"]:
                print("      样例: %s" % hits[0]["sample"])
            if f["hint"]:
                print("      改法: %s" % f["hint"])
        print("    %s" % explain_exit(1))
        raise SystemExit(1)

    if p1:
        print("      已用 --allow-p1 放过 %d 类 P1 警告。" % p1)
        for f in rep.findings():
            if f["severity"] == "P1":
                print("        · [%s] %s @ %s" % (f["category"], f["rule"], f["file"]))

    # ---------- 2. 清理清单 ----------
    print("[2/4] 生成打包清单 ...")
    files, dropped, icons = collect_packable(root)
    empties = collect_empty_dirs(root, files)
    total = sum(f.stat().st_size for f in files)
    print("      纳入 %d 个文件，共 %.1f KB" % (len(files), total / 1024))
    if empties:
        print("      保留 %d 个空目录（结构完整）：%s"
              % (len(empties), "、".join(str(d.relative_to(root)) + "/" for d in empties)))
    if icons:
        print("      排除 %d 个图标文件（**不进技能包**）：" % len(icons))
        for d in icons[:6]:
            print("        - %s" % d.relative_to(root))
        print("        发布时在平台「图标」处单独上传 icons/ 下的那张"
              "（512×512、PNG/JPG、≤500KB）")
    if dropped:
        print("      排除 %d 项缓存/仓库元数据：" % len(dropped))
        for d in dropped[:12]:
            print("        - %s" % d.relative_to(root))
        if len(dropped) > 12:
            print("        ... 其余 %d 项" % (len(dropped) - 12))

    # 引用完整性：被排除的文件若仍被正文引用，装到用户机器上就是悬空指针。
    # audit_skill 看的是源码树（文件还在），抓不到这类；只有打包这一步知道谁被丢了。
    ref_hits = check_pack_refs(root, files, dropped)
    if ref_hits:
        print("      [!] %d 处引用指向被排除的文件，装上后会悬空：" % len(ref_hits))
        for rel, lineno, t in ref_hits[:10]:
            print("        - %s:%d -> %s" % (rel, lineno, t))
        if len(ref_hits) > 10:
            print("        ... 其余 %d 处" % (len(ref_hits) - 10))
        print("        改法：让它进包，或把引用措辞改成指向仓库 / 外部说明。")

    if not args.quiet:
        for f in files:
            print("        %s" % f.relative_to(root))

    # ---------- 3. 打包 ----------
    name = root.name
    out_dir = Path(args.out).expanduser().resolve() if args.out else Path.cwd()
    plugin_json = build_plugin_json(root, name) if args.platform else None
    print("[3/4] 打包 ...%s"
          % ("  形态：插件包（插件市场分发用）" if args.platform else "  形态：技能目录包（上传用）"))
    if args.platform:
        print("      插件清单 .codebuddy-plugin/plugin.json：")
        for k, v in plugin_json.items():
            sv = json.dumps(v, ensure_ascii=False)
            print("        %-16s %s" % (k, sv if len(sv) <= 70 else sv[:67] + "..."))
    if args.dry_run:
        print("[dry-run] 不写 zip，结束。")
        return
    try:
        if args.platform:
            zip_path = build_plugin_zip(root, out_dir, name, files, empties, plugin_json,
                                        flat_root=args.flat_root)
        else:
            zip_path = build_zip(root, out_dir, files, name, empties)
    except Exception as e:
        die(4, "打包失败：%s" % root.name,
            "确认输出目录可写、磁盘有空间；zip 同名文件没被占用", exc=e)
    print("      -> %s" % zip_path)
    if args.platform:
        print("      结构：%s.codebuddy-plugin/plugin.json + %sskills/%s/..."
              % ("" if args.flat_root else "%s/" % name,
                 "" if args.flat_root else "%s/" % name, name))

    # ---------- 4. 安装 ----------
    # 安装目标：显式指定 > 被打包的技能原所在的技能目录 > 本脚本所在的技能目录
    if args.install_dir:
        target_dir = Path(args.install_dir).expanduser().resolve()
    else:
        try:
            target_dir = skills_dir_of(root)     # 装回它本来在的那个技能目录
        except PathResolutionError:
            try:
                target_dir = skills_dir()        # 退回本脚本自己所在的技能目录
            except PathResolutionError as e:
                if args.install:
                    die(3, "定位不到安装目标：%s" % e,
                        "显式传入 --install-dir <目录>，或设置环境变量 %s" % SKILLS_HOME_ENV)
                target_dir = root.parent         # --no-install 时只用于展示
    installed = None
    if not args.install:
        print("[4/4] 跳过安装（--no-install）")
        print("      提醒：本机还没有这个技能，拿到的只有 zip。")
    elif is_inside(root, target_dir):
        print("[4/4] 跳过安装：源目录已在本机技能目录内，无需复制")
    else:
        print("[4/4] 安装 ...")
        installed = install_skill(root, target_dir, name, args.force, files, empties)
        if installed:
            print("      -> %s" % installed)
            print("      若技能未立刻出现在可用列表，重启会话即可被识别。")

    print("\n完成。")
    print("  技能目录 : %s" % (installed or root))
    print("  分发 zip : %s" % zip_path)
    icon_dir = root / "icons"
    if icon_dir.is_dir() and (icons or any(icon_dir.iterdir())):
        print("  发布图标 : %s（未进包 —— 上传技能时在平台「图标」处单独提交）" % icon_dir)
        for ic in sorted(icon_dir.iterdir()):
            if ic.is_file():
                print("             %s" % ic.name)
    if args.platform:
        print("  用途     : 插件形态包 —— 插件市场分发（团队 marketplace / 把技能挂到插件下）")
        print("  !! 上传 open.workbuddy.cn「技能」类目**不要**用这个包：")
        print("     它会报「压缩包缺少 SKILL.md 文件」——SKILL.md 被埋在 skills/<技能名>/ 下了。")
        print("     上传请去掉 --as-plugin 重打一次，用默认产出的那个 zip。")
    else:
        print("  用途     : 技能目录包 —— 既是本机包，也是**开放平台技能类目的上传包**")
        print("     官方要求形态：<技能名>/SKILL.md + references/ + scripts/ + templates/（本包即是）")
        print("     直接把这个 zip 传到 open.workbuddy.cn 的技能类目即可，无需额外清单文件")
    if not installed and not is_inside(root, target_dir):
        print("\n  !! 技能未装到本机，现在还不可用。")
        print("     去掉 --no-install，或把技能目录放到 %s 下。" % target_dir)


if __name__ == "__main__":
    main()
