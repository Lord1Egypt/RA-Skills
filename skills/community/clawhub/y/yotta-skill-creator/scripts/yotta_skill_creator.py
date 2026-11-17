#!/usr/bin/env python3
"""yotta-skill-creator: 从内嵌模板生成合规技能目录并做结构自检（元阁「工坊」造技能端）。

零依赖（Python 3.8+ 标准库）。用法:
  python3 scripts/yotta_skill_creator.py create <skill-name> --zh 元X --desc "..."
      [--summary "一句话简介"] [--out <目录>] [--with-cli] [--no-banner]
      [--skip-installer] [--self-use]
  python3 scripts/yotta_skill_creator.py --version

自用模式（--self-use）：只生成技能本体（SKILL.md / references / 可选 CLI），不生成
README 中英 / package.json / CHANGELOG / LICENSE / NOTICE / install.sh / publish.yml
等发布件 —— 自用技能不一定要推 GitHub。

行为:
  - 命名校验：yotta- 前缀 / 小写连字符 / 长度 <= 64 / 中文名 元X 规范 / 目标不重复。
  - 脚手架：从包内 template/ 生成 SKILL.md / README 中英四方式 / package.json /
    CHANGELOG / LICENSE / NOTICE / install.sh + bin/install.js / .gitignore / .npmignore /
    .github/workflows/publish.yml / references / assets，占位符统一替换。
  - 结构自检：生成后立即校验（frontmatter / 版本四件 / README 四方式 / 无残留占位符），
    通过才输出「脚手架合格」。
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

VERSION = "0.1.7"
TOOL_NAME = "yotta-skill-creator"
CN_NAME = "元造"

SLUG_RE = re.compile(r"^yotta-[a-z0-9]+(?:-[a-z0-9]+)*$")
PLACEHOLDER_RE = re.compile(r"\{\{[^{}]+\}\}")

FOUR_WAYS = {
    "方式一 npx 一行装": re.compile(r"npx\s+-y\s+@yottameta/[^\s`\"]+"),
    "方式二 git clone": re.compile(r"git\s+clone\s+https?://github\.com/YottaMeta/"),
    "方式三 Download ZIP": re.compile(r"Download\s+ZIP|下载压缩包|下载 ZIP"),
    "方式四 install.sh": re.compile(r"install\.sh\s+--agent"),
}
FORBIDDEN_INSTALL = {
    "npx skills（走 GitHub 克隆，无代理不可用）": re.compile(r"npx\s+skills\b", re.I),
    "-g 安装（为未安装智能体建目录，污染）": re.compile(
        r"npx\s+-y\s+@yottameta/[^\s`\"]+\s+-g|install\.sh\s+-g"),
}

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "template"
TEMPLATE_FILE_MAP = {
    "SKILL.md.tmpl.txt": "SKILL.md",
    "gitignore.tmpl.txt": ".gitignore",
    "npmignore.tmpl.txt": ".npmignore",
    "LICENSE.tmpl.txt": "LICENSE",
    "NOTICE.tmpl.txt": "NOTICE",
}
TEMPLATE_REL_MAP = {
    "github/workflows/publish.yml.tmpl.txt": ".github/workflows/publish.yml",
}

# 自用模式（--self-use）不生成的发布件（顶层名）
PUBLISH_TOP_LEVEL = {
    "README.md", "README.zh-CN.md", "package.json", "CHANGELOG.md",
    "NOTICE", "LICENSE", ".npmignore", "install.sh", "bin", "assets", ".github",
}


def normalize_slug(name: str) -> str:
    name = (name or "").strip()
    if not name:
        raise ValueError("技能名不能为空")
    if len(name) > 64:
        raise ValueError("技能名超过 64 字符")
    if not SLUG_RE.fullmatch(name):
        raise ValueError(
            "技能名必须为小写连字符且以 yotta- 开头（如 yotta-skill-creator）")
    return name


def validate_zh(zh: str) -> str:
    zh = (zh or "").strip()
    if not zh:
        raise ValueError("中文名（--zh）不能为空")
    if not zh.startswith("元"):
        raise ValueError("中文名应以「元」开头（家族规范，如 元造 / 元安全）")
    if not 2 <= len(zh) <= 8:
        raise ValueError("中文名长度应为 2-8 个字符（元 + 1-7 字）")
    return zh


# v0.1.3：外部元数据（描述 / 摘要 / 中文名）会被写进 SKILL.md frontmatter、package.json、
# 文档与生成的 CLI 源码。旧行为直接字符串替换，含引号 / 换行 / `---` 的输入可以注入
# 额外 frontmatter 字段或指令。现在统一走白名单校验 + YAML 引号化 + 生成后回读校验。
_META_MAX_LEN = {"desc": 400, "summary": 200, "zh": 8}


def validate_meta_text(label: str, value: str, limit: int) -> str:
    v = (value or "").strip()
    if not v:
        raise ValueError("%s 不能为空" % label)
    if len(v) > limit:
        raise ValueError("%s 过长（> %d 字符）" % (label, limit))
    if any(ord(ch) < 0x20 for ch in v):
        raise ValueError("%s 含控制字符（换行 / 制表符等），会破坏生成文件的语法" % label)
    if "---" in v:
        raise ValueError("%s 含 frontmatter 分隔符 '---'，已拒绝" % label)
    for ch in ('"', "\\", "`"):
        if ch in v:
            raise ValueError("%s 含保留字符 %s，请改用其他写法" % (label, ch))
    return v


def yaml_quote(value: str) -> str:
    """把元数据安全地写进 YAML frontmatter（双引号 + 转义反斜杠与双引号）。"""
    return '"%s"' % value.replace("\\", "\\\\").replace('"', '\\"')


FRONTMATTER_KEYS = {"name", "description", "version", "license", "metadata"}


def verify_generated_frontmatter(skill_dir: Path, slug: str, desc: str) -> None:
    """生成后回读校验：frontmatter 必须可解析、字段与入参一致、不出现额外顶层键。"""
    skill_md = skill_dir / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    if fm.get("name") != slug:
        raise ValueError("生成后回读失败：frontmatter name=%r != %r"
                         % (fm.get("name"), slug))
    if fm.get("description") != desc:
        raise ValueError("生成后回读失败：description 与入参不一致（疑似转义问题）")
    extra = sorted(set(fm) - FRONTMATTER_KEYS)
    if extra:
        raise ValueError("生成后回读失败：frontmatter 出现额外字段 %s" % ", ".join(extra))


def cli_module(slug: str) -> str:
    return slug.replace("-", "_")


def render(template: Path, out: Path, subs, skip_installer, with_cli, no_banner,
           self_use=False):
    """复制模板并替换占位符；返回生成的文件相对路径列表。"""
    created = []
    for src in sorted(template.rglob("*")):
        rel = src.relative_to(template)
        parts = list(rel.parts)
        if "__pycache__" in parts or src.suffix == ".pyc":
            continue
        first = parts[0] if parts else ""
        logical_first = TEMPLATE_FILE_MAP.get(first, first)
        if self_use and logical_first in PUBLISH_TOP_LEVEL:
            continue
        if first == "assets" and no_banner:
            continue
        if first == "bin" and skip_installer:
            continue
        if first == "scripts" and not with_cli:
            continue
        if src.is_file():
            if first == "install.sh" and skip_installer:
                continue
            def _repl(m):
                return subs.get(m.group(1), m.group(0))
            new_parts = [re.sub(r"\{\{(\w+)\}\}", _repl, p) for p in parts]
            mapped_rel = TEMPLATE_REL_MAP.get("/".join(new_parts))
            if mapped_rel:
                dst = out.joinpath(*Path(mapped_rel).parts)
            else:
                mapped_name = TEMPLATE_FILE_MAP.get(new_parts[-1])
                if mapped_name:
                    new_parts[-1] = mapped_name
                dst = out.joinpath(*new_parts)
            dst.parent.mkdir(parents=True, exist_ok=True)
            text = src.read_text(encoding="utf-8")
            for k, v in subs.items():
                text = text.replace("{{" + k + "}}", v)
            dst.write_text(text, encoding="utf-8")
            created.append(str(dst.relative_to(out)))
    return created


def adjust_package_json(out: Path, skip_installer: bool, no_banner: bool = False) -> None:
    if not (skip_installer or no_banner):
        return
    pkg = out / "package.json"
    data = json.loads(pkg.read_text(encoding="utf-8"))
    if skip_installer:
        data.pop("bin", None)
    if "files" in data and isinstance(data["files"], list):
        drop = set()
        if skip_installer:
            drop.update(("bin", "install.sh"))
        if no_banner:
            drop.add("assets")
        data["files"] = [f for f in data["files"] if f not in drop]
    pkg.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def parse_frontmatter(text: str):
    """极简 frontmatter 解析：--- 围栏 + 顶层 key: value（缩进块忽略）。"""
    fm = {}
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.S)
    if not m:
        return fm
    for line in m.group(1).splitlines():
        if line.startswith((" ", "\t")):
            continue
        kv = re.match(r"^([A-Za-z_][\w-]*):\s*(.*?)\s*$", line)
        if kv:
            fm[kv.group(1)] = kv.group(2).strip().strip("\"'")
    return fm


def check_readme_install(text: str, label: str, errors, warns):
    for name, pat in FOUR_WAYS.items():
        if not pat.search(text):
            errors.append("%s 缺少%s（发布规范 §3.3.1 四方式安装）" % (label, name))
    for name, pat in FORBIDDEN_INSTALL.items():
        if pat.search(text):
            errors.append("%s 命中禁用安装方式：%s" % (label, name))


def self_check(skill_dir: Path, slug: str, skip_installer: bool,
               with_cli: bool, no_banner: bool, self_use=False):
    """结构自检：返回 (errors, warns)。自用模式只查技能本体，不要求发布件。"""
    errors, warns = [], []
    required = ["SKILL.md"]
    if not self_use:
        required += ["LICENSE", "README.md", "README.zh-CN.md",
                     "CHANGELOG.md", "NOTICE", "package.json",
                     ".gitignore", ".npmignore", ".github/workflows/publish.yml"]
        if not skip_installer:
            required += ["install.sh", "bin/install.js"]
    if with_cli:
        required += ["scripts/%s.py" % cli_module(slug),
                     "scripts/test_%s.py" % cli_module(slug)]
    for r in required:
        if not (skill_dir / r).is_file():
            errors.append("缺少必需文件: %s" % r)

    # 残留占位符
    for f in skill_dir.rglob("*"):
        if f.is_file() and f.suffix in (".md", ".json", ".sh", ".yml", ".yaml", ".js", ".py"):
            text = f.read_text(encoding="utf-8", errors="ignore")
            if PLACEHOLDER_RE.search(text):
                errors.append("存在未替换占位符: %s" % f.relative_to(skill_dir))

    # frontmatter 与版本
    skill = skill_dir / "SKILL.md"
    if skill.is_file():
        fm = parse_frontmatter(skill.read_text(encoding="utf-8"))
        if fm.get("name") != slug:
            errors.append("SKILL.md frontmatter name=%r 与目录名不一致" % fm.get("name"))
        for k in ("description", "version", "license"):
            if not fm.get(k):
                errors.append("SKILL.md frontmatter 缺少 %s" % k)
        skill_v = fm.get("version")
        pkg_v = None

        pkg = skill_dir / "package.json"
        if pkg.is_file():
            try:
                data = json.loads(pkg.read_text(encoding="utf-8"))
            except Exception as e:
                errors.append("package.json 解析失败: %s" % e)
                data = {}
            if data.get("name") != "@yottameta/" + slug:
                errors.append("package.json name=%r 与 @yottameta/%s 不一致"
                              % (data.get("name"), slug))
            pkg_v = data.get("version")
            if skill_v and pkg_v and str(skill_v) != str(pkg_v):
                errors.append("版本不一致：package.json=%s vs SKILL.md=%s"
                              % (pkg_v, skill_v))

        chg = skill_dir / "CHANGELOG.md"
        if chg.is_file():
            cm = re.search(r"^##\s*v?([0-9]+\.[0-9]+\.[0-9]+)", 
                           chg.read_text(encoding="utf-8"), re.M)
            if cm and pkg_v and cm.group(1) != str(pkg_v):
                errors.append("版本不一致：package.json=%s vs CHANGELOG 顶部=%s"
                              % (pkg_v, cm.group(1)))
        elif pkg_v:
            warns.append("缺少 CHANGELOG.md（发布规范建议提供）")

    # README 四方式（发布件要求；自用模式跳过）
    if not self_use:
        for name in ("README.md", "README.zh-CN.md"):
            rp = skill_dir / name
            if rp.is_file():
                check_readme_install(rp.read_text(encoding="utf-8", errors="ignore"),
                                     name, errors, warns)
        rp = skill_dir / name
        if rp.is_file():
            check_readme_install(rp.read_text(encoding="utf-8", errors="ignore"),
                                 name, errors, warns)

    # 围栏平衡（粗略）
    for f in skill_dir.rglob("*.md"):
        if f.is_file():
            t = f.read_text(encoding="utf-8", errors="ignore")
            if t.count("```") % 2 != 0:
                errors.append("Markdown 代码围栏不配对: %s" % f.relative_to(skill_dir))
    return errors, warns


def cmd_create(args) -> int:
    try:
        slug = normalize_slug(args.skill_name)
        zh = validate_zh(args.zh)
        desc = validate_meta_text("--desc 描述", args.desc, _META_MAX_LEN["desc"])
        summary = validate_meta_text("--summary 摘要",
                                     args.summary or args.desc,
                                     _META_MAX_LEN["summary"])
    except ValueError as e:
        print("[ERROR] %s" % e, file=sys.stderr)
        return 2

    out_root = Path(args.out).expanduser().resolve()
    out = out_root / slug
    if out.exists():
        print("[ERROR] 目标目录已存在: %s" % out, file=sys.stderr)
        return 2
    if not TEMPLATE_DIR.is_dir():
        print("[ERROR] 模板目录不存在: %s" % TEMPLATE_DIR, file=sys.stderr)
        return 2

    subs = {
        "skill_name": slug,
        "install_command": "npx -y @yottameta/" + slug,
        "zh_name": zh,
        "zh_name_yaml": yaml_quote(zh),
        "cli_module": cli_module(slug),
        "description": desc,
        "description_yaml": yaml_quote(desc),
        "summary": summary,
        "year": str(date.today().year),
    }

    out.mkdir(parents=True)
    created = render(TEMPLATE_DIR, out, subs,
                     skip_installer=args.skip_installer,
                     with_cli=args.with_cli,
                     no_banner=args.no_banner,
                     self_use=args.self_use)
    if not args.self_use:
        adjust_package_json(out, args.skip_installer, args.no_banner)

    try:
        verify_generated_frontmatter(out, slug, desc)
    except (ValueError, OSError) as e:
        print("[ERROR] %s" % e, file=sys.stderr)
        return 2

    errors, warns = self_check(out, slug, args.skip_installer,
                               args.with_cli, args.no_banner,
                               self_use=args.self_use)
    print("created: %s" % out)
    print("files: %d" % len(created))
    for w in warns:
        print("[WARN ] %s" % w)
    if errors:
        for e in errors:
            print("[ERROR] %s" % e, file=sys.stderr)
        print("脚手架自检未通过，请修正后重跑自检。", file=sys.stderr)
        return 2
    print("OK: 脚手架合格，可继续开发 SKILL.md / scripts / references。")
    print("下一步:")
    print("  1) 编辑 SKILL.md 的正文（触发与边界 / 核心流程 / 渐进披露）")
    if args.with_cli:
        print("  2) 实现 scripts/%s.py 并补测试" % cli_module(slug))
    if args.self_use:
        print("  自用模式：未生成发布件（README 中英 / package.json / CHANGELOG /")
        print("  LICENSE / NOTICE / install.sh / publish.yml）。若要发布，请重跑 create")
        print("  不带 --self-use，或按发布规范补齐发布件后跑 publish-guard check。")
    else:
        print("  3) 发布前跑 publish-guard: python yotta_publish_guard.py check %s" % out)
    return 0


def build_parser():
    ap = argparse.ArgumentParser(
        prog=TOOL_NAME,
        description="%s —— 端到端造技能脚手架（零依赖 Python 3.8+）" % CN_NAME,
    )
    ap.add_argument("--version", action="version", version="%(prog)s " + VERSION)
    sub = ap.add_subparsers(dest="command", required=True)

    pc = sub.add_parser("create", help="生成合规技能目录")
    pc.add_argument("skill_name", help="技能名（yotta- 前缀小写连字符）")
    pc.add_argument("--zh", required=True, help="中文名（元X 规范，如 元造）")
    pc.add_argument("--desc", required=True, help="SKILL.md 描述（做什么 + 何时触发 + 边界）")
    pc.add_argument("--summary", default="", help="一句话简介（README 用，缺省=desc）")
    pc.add_argument("--out", default=".", help="输出父目录（缺省=当前目录）")
    pc.add_argument("--with-cli", action="store_true", help="同时生成 CLI 骨架 + 测试")
    pc.add_argument("--no-banner", action="store_true", help="跳过 assets/ 素材目录")
    pc.add_argument("--skip-installer", action="store_true",
                    help="不生成 install.sh / bin/install.js（并从 package.json 去掉 bin）")
    pc.add_argument("--self-use", action="store_true",
                    help="自用模式：只生成技能本体（SKILL.md / references / 可选 CLI），"
                         "不生成任何发布件（README 中英 / package / CHANGELOG / LICENSE / "
                         "NOTICE / install.sh / publish.yml）")
    pc.set_defaults(func=cmd_create)
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
