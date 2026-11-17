#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
new_skill.py — 从需求生成一份合规的技能骨架（生成即体检）

用法:
    python scripts/new_skill.py <skill-name> [选项]

常用示例:
    # 最小生成（市场字段齐全，建 scripts/ references/）
    python scripts/new_skill.py oa-todo-bg --display-name 待办查询 \
        --desc "无头登录 OA 拉取待办列表。当用户说「查待办」「OA 待办」时使用。" \
        --desc-zh "无头登录 OA，拉取待办列表" \
        --desc-en "Fetch the OA todo list headlessly" \
        --triggers 查待办,OA待办

    # 带依赖与配置模板
    python scripts/new_skill.py report-gen --dirs scripts,references,config,templates \
        --deps requests,openpyxl --config-fields endpoint,username,password

    # 只本机自用，不要市场字段
    python scripts/new_skill.py my-tool --mode local

交付定义:
    `--out` 默认就是本机技能目录（自动探测：脚本装在哪，就往那个技能目录里生成），
    所以**生成即安装**，重启会话即可用。探测不到时会要求显式传 --out，不会猜。
    把 --out 指到别处（工作区、临时目录）时骨架不会生效，此时加 --install 会额外装一份。

选项:
    --out <目录>            技能父目录（默认自动探测当前平台的技能目录）
    --display-name <名>     中文展示名（默认取 name 的破折号转空格形式）
    --display-name-en <名>  英文展示名（默认由 name 转 Title Case）
    --desc <文本>           description：做什么 / 何时触发 / 触发词（建议 60~200 字）
    --desc-zh <文本>        中文一句话介绍（30 字内）
    --desc-en <文本>        英文一句话介绍（首字母大写，结尾不加句号）
    --category <分类>       市场分类，默认 dev-programming；须落在平台 13 个枚举内，
                            否则上架后显示「未分类」（office-efficiency / content-creation /
                            dev-programming / data-analysis / design-media / ai-agent /
                            knowledge-management / business-ops / education / professional /
                            it-ops-security / life-service / pay-skill）
    --author <署名>         默认读取 ~/.workbuddy/skills 内已有技能的署名为参考，否则留 <你的署名>
    --triggers a,b,c        结构化触发词，逗号分隔；会同时补进 description
    --dirs scripts,references,templates,assets,config   要创建的子目录（默认 scripts,references）
    --deps requests,openpyxl    第三方依赖；给了就自动生成 scripts/setup.py
    --config-fields a,b     生成 config/settings.example.json 的空字段（配合 --dirs config）
    --mode market|local     默认 market（字段齐全，可上架）；local 只留本机必需字段
    --no-audit              生成后不自动体检
    --no-sync               不注入 scripts/sync.py 版本自检器（默认注入）
    --json                  机器可读输出
    --force                 目标目录已存在时覆盖（仅限看起来确实是技能目录的）

退出码:
    0 成功（含体检通过）| 1 生成成功但体检有 P1 | 2 生成成功但体检有 P0
    | 3 参数错误（技能名非法/目录已存在）| 4 写入失败
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True          # 不留 __pycache__
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _friendly import die, explain_exit, make_backup, use_utf8_stdout  # noqa: E402
from _paths import (PathResolutionError, SKILLS_HOME_ENV,  # noqa: E402
                    platform_root, skills_dir)

VALID_NAME = re.compile(r"^[a-z0-9][a-z0-9-]*$")
PREFIX_ENV = "SKILL_NAME_PREFIX"        # 用户级默认前缀：环境变量
PREFIX_CONFIG_NAME = "skill-gen.json"   # 用户级默认前缀：平台根下的可选配置
KNOWN_DIRS = ("scripts", "references", "templates", "assets", "config")


# ----------------------------------------------------------------- 工具函数

def normalize_name(raw: str) -> str:
    """把用户随手写的名字规整成 kebab-case（市场规范硬要求）。"""
    s = raw.strip().strip("/\\").lower()
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-{2,}", "-", s)
    s = re.sub(r"[^a-z0-9-]", "", s)
    return s.strip("-")


def title_case(name: str) -> str:
    return " ".join(w.capitalize() for w in name.split("-") if w)


def _prefix_from_config() -> tuple[str, str]:
    """平台根下可选的本机配置：{"name_prefix": "xxx-"}。定位不到/没配就当没有。"""
    try:
        cfg = platform_root() / PREFIX_CONFIG_NAME
    except PathResolutionError:
        return "", ""
    try:
        data = json.loads(cfg.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return "", ""
    v = str(data.get("name_prefix", "") or "").strip()
    return v, (str(cfg) if v else "")


def resolve_prefix(cli_prefix: str | None, no_prefix: bool) -> tuple[str, str]:
    """决定技能名前缀，返回 (前缀原值, 来源说明)。

    **脚本不内置任何个人前缀** —— 生成器是要分发给别人用的，命名习惯属于使用者本人，
    写成默认值等于把一个人的习惯塞进所有人的技能包里。想固定用某个前缀，自己配：

        优先级：--no-prefix（明确不加） > 命令行 --prefix（显式空串也算「不加」）
                > 环境变量 SKILL_NAME_PREFIX > 平台根 skill-gen.json 的 name_prefix > 不加
    """
    if no_prefix:
        return "", "命令行 --no-prefix"
    if cli_prefix is not None:
        return cli_prefix, "命令行 --prefix"
    env = os.environ.get(PREFIX_ENV, "").strip()
    if env:
        return env, "环境变量 " + PREFIX_ENV
    v, src = _prefix_from_config()
    if v:
        return v, src
    return "", ""


def guess_author() -> str:
    """署名默认值：先读平台根下 USER.md 的姓名，再退回系统用户名。

    不要从其它已装技能里抓 author —— 那会把市场技能作者的署名
    错安到当前技能头上（实测抓到过别人的名字）。
    """
    try:
        t = (platform_root() / "USER.md").read_text(encoding="utf-8", errors="replace")
        m = re.search(r"姓名[：:]\s*\**\s*([^\n*（(]+)", t)
        if m:
            v = m.group(1).strip().strip("*_ ")
            if v:
                return v
    except (OSError, PathResolutionError):
        pass
    return Path.home().name or "unknown"


def is_inside(child: Path, parent: Path) -> bool:
    """child 是否位于 parent 之内（判断骨架是否已落在本机技能目录里）。"""
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except (ValueError, OSError):
        return False


def install_copy(src: Path, name: str, force: bool):
    """把生成的骨架复制一份到技能目录，让技能立刻可用。"""
    dest = skills_dir() / name
    if dest.exists():
        if not force:
            print("安装跳过 : 已存在 %s（要覆盖请加 --force）" % dest)
            return None
        if not (dest / "SKILL.md").exists():
            print("安装跳过 : %s 已存在且不含 SKILL.md，拒绝覆盖" % dest)
            return None
        # 先备份再覆盖：旧版是 rmtree 后 copytree，中途失败本机技能就没了
        bak = make_backup(dest)
        print("安装     : 旧版已备份到 %s" % bak)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dest)
    return dest


def yaml_quote(s: str) -> str:
    """单行标量：含 YAML 敏感字符时加引号。"""
    if s == "":
        return '""'
    if re.search(r"[:#\[\]{}&*!|>'\"%@`]", s) or s[0] in "-? " or s[-1] == " ":
        return '"%s"' % s.replace('"', '\\"')
    return s


def yaml_str(s: str) -> str:
    """长文本一律写成单行双引号标量。

    平台侧解析器（SkillHub 自带 CLI）只支持 `key: value` 与 `key: [a, b]`，
    `>-` 折叠块会被读成字面量 ">-"、多行列表会被读成空串 —— 上传成功但内容是空的。
    折成一行对完整 YAML 解析器同样合法，两边都安全。
    """
    return '"%s"' % (s or "").replace("\\", "\\\\").replace('"', '\\"')


# ----------------------------------------------------------------- 内容生成

def build_frontmatter(a, name: str, dirs, deps) -> str:
    # 平台只认驼峰 displayName 当展示名（下划线 display_name 它不认，缺了商店里直接
    # 显示英文 slug）。展示名也越简洁越好，去掉「 · 功能列举」后缀。
    display = a.display_name.split(" · ")[0].strip() or a.display_name
    lines = ["---"]
    lines.append("name: %s" % name)
    lines.append("slug: %s" % name)                      # 平台 CLI 发布必填，与 name 保持一致
    lines.append("display_name: %s" % yaml_quote(a.display_name))
    if a.mode == "market":
        lines.append("display_name_en: %s" % yaml_quote(a.display_name_en))
    lines.append("displayName: %s" % yaml_quote(display))
    lines.append("description: %s" % yaml_str(a.desc))
    if a.mode == "market":
        lines.append("description_zh: %s" % yaml_str(a.desc_zh))
        lines.append("description_en: %s" % yaml_str(a.desc_en))
        lines.append("summary: %s" % yaml_str(a.desc_zh))
        lines.append("category: %s" % a.category)
    lines.append("version: 0.1.0")
    lines.append("author: %s" % yaml_quote(a.author))
    tags = [t.strip() for t in (a.triggers or []) if t.strip()][:5]
    if tags:                                             # 列表用内联写法：块列表平台同样读不到
        lines.append("tags: [%s]" % ", ".join(tags))
    if a.triggers:
        lines.append("trigger:")
        for t in a.triggers:
            lines.append("  - %s" % t)
    lines.append("agent_created: true")
    lines.append("---")
    return "\n".join(lines)


def build_body(a, name: str, dirs, deps, with_sync: bool = True) -> str:
    has = lambda d: d in dirs  # noqa: E731
    out = []
    out.append("# %s (%s)\n" % (a.display_name, name))
    out.append("一句话说明它替用户省掉了什么。\n")
    out.append("## 何时使用\n")
    for t in (a.triggers or ["<场景一>", "<场景二>"]):
        out.append("- 用户提到「%s」时" % t)
    out.append("")

    if with_sync and has("scripts"):
        # 第 0 步自检：技能是文件快照，落后了不会自己变新，动手前先核对一次
        out.append("## 第 0 步 · 版本自检（每次动手前先跑）\n")
        out.append("```bash")
        out.append("python scripts/sync.py --json")
        out.append("```\n")
        out.append("只读比对线上版本：退出码 `0` 最新 · `10` 有新版建议重装 · "
                   "`20` 主版本不同必须重装 · `30` 联网失败按旧版继续。\n")
        out.append("本技能不自动更新自己 —— 换版本只有一条路：用户明确重装 "
                   "（`skillhub install %s`）。\n" % name)

    # 运行前提：只写真实存在的东西，避免引用缺失
    pre = []
    if deps:
        pre.append("- 依赖：%s；首次使用先跑 `python scripts/setup.py`" % "、".join(
            "`%s`" % d for d in deps))
    else:
        pre.append("- 依赖：无第三方依赖（如后续引入，记得补 `scripts/setup.py`）")
    if has("config"):
        pre.append("- 配置：真实值放 `~/.workbuddy/%s_config.json`，对外只留 "
                   "`config/settings.example.json` 空模板" % name)
    if pre:
        out.append("## 运行前提\n")
        out.extend(pre)
        out.append("")

    out.append("## 执行步骤\n")
    out.append("当用户需要 <做什么> 时，按以下步骤执行：\n")
    out.append("1. **<步骤名>** — 说明输入、命令与判断条件。")
    out.append("2. **<步骤名>** — 说明失败时的行为（缺依赖/缺配置/无网络）。")
    out.append("3. **<步骤名>** — 产出交付给用户，并说明输出文件放在哪。")
    out.append("")

    if dirs:
        out.append("## 目录说明\n")
        desc_map = {
            "scripts": "执行逻辑（主脚本、`scripts/sync.py` 版本自检、`scripts/setup.py` 依赖安装）",
            "references": "按需加载的参考文档（字段表、接口约定、踩坑记录）",
            "templates": "可复制的骨架 / 报告模板",
            "assets": "产出用资源（图片、字体、样板稿），不读进上下文",
            "config": "只放 `*.example.*` 空模板，真实配置放 `~/.workbuddy/`",
        }
        for d in dirs:
            out.append("- `%s/` — %s" % (d, desc_map.get(d, "自定义资源目录")))
        out.append("")

    out.append("## 常见坑\n")
    out.append("1. 把本次实现时踩到的坑写进来（现象 + 原因 + 规避），这是技能最值钱的部分。")
    out.append("")
    return "\n".join(out)


SETUP_PY = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""安装 {name} 的第三方依赖。

用法:
    python scripts/setup.py

注意：部分环境下 `python -m pip` 会异常退出，此时改用 `pip install ...`。
"""

import subprocess
import sys
import time

PACKAGES = [{pkgs}]
MIRROR = "https://pypi.tuna.tsinghua.edu.cn/simple"
RETRIES = 3
TIMEOUT = 180


def run(cmd):
    try:
        r = subprocess.run(cmd, timeout=TIMEOUT)
    except (subprocess.TimeoutExpired, OSError):
        return False
    return r.returncode == 0


def main() -> int:
    if not PACKAGES:
        print("无第三方依赖，无需安装。")
        return 0
    # 三种装法依次兜底：直连 → 裸 pip（部分环境下 `python -m pip` 会异常退出）→ 国内镜像
    attempts = [[sys.executable, "-m", "pip", "install", *PACKAGES],
                ["pip", "install", *PACKAGES],
                [sys.executable, "-m", "pip", "install", "-i", MIRROR, *PACKAGES]]
    for i in range(RETRIES):
        for cmd in attempts:
            print("执行：" + " ".join(cmd))
            if run(cmd):
                print("[OK] 依赖安装完成。")
                return 0
            print("    没成功，换下一种方式重试 …")
        if i < RETRIES - 1:
            time.sleep(2 * (i + 1))
    print("[X] 自动安装失败，请手动执行下面任意一条：")
    print("    " + " ".join(attempts[0]))
    print("    " + " ".join(attempts[-1]))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
'''

CONFIG_EXAMPLE = '''{{
  "_comment": "复制为 settings.json 填入真实值。真实配置建议放 ~/.workbuddy/{name}_config.json，不要提交到仓库。",
{fields}
}}
'''


def build_setup_py(name: str, deps) -> str:
    return SETUP_PY.format(name=name, pkgs=", ".join('"%s"' % d for d in deps))


def build_config_example(name: str, fields) -> str:
    lines = ['  "%s": ""' % f for f in fields]
    return CONFIG_EXAMPLE.format(name=name, fields=",\n".join(lines))


# ----------------------------------------------------------------- 主流程

def _rename_with_retry(tmp: Path, target: Path, tries: int = 5, delay: float = 0.4):
    """Windows 下目标路径常被短暂锁定：本机工具（杀软实时扫描、技能目录 watcher）会在
    新路径刚出现的瞬间去打开它，撞进这个竞争窗口的 rename 就报 WinError 5「访问被拒绝」。
    实测特征：同一名字稳定失败、换个名字就能成功、过一会儿再跑又好了。
    这种竞争等一下就好，按递增间隔重试几次即可，不重试就会误报「权限不足」。"""
    last: BaseException | None = None
    for i in range(tries):
        try:
            tmp.rename(target)
            return
        except PermissionError as e:
            last = e
            time.sleep(delay * (i + 1))
    raise last  # type: ignore[misc]


def sync_py_text() -> str:
    """取本生成器自带的版本自检器原文，原样复制进新技能。

    刻意**不做模板替换**：sync.py 自己会从 SKILL.md 的 frontmatter 与目录名
    反推 slug / 展示名 / 版本号，一份文件通用；复制而非改写，将来改自检器
    只需要改一处。
    """
    src = Path(__file__).resolve().parent / "sync.py"
    try:
        return src.read_text(encoding="utf-8")
    except OSError as e:
        raise RuntimeError("读取自带版本自检器失败（%s）：%s" % (src, e))


def write_all(target: Path, a, name: str, dirs, deps, fields, force: bool, with_sync: bool = True):
    """先建临时目录，全部写成功后再替换目标。

    旧实现是**先把目标目录整个删掉再重建**：中途任何一步失败（权限、磁盘满、
    文件被占用），旧技能已经没了。改成「临时目录 + 备份 + 原子替换」之后，
    失败时旧目录原封不动。
    """
    created = []
    if target.exists():
        if not force:
            raise FileExistsError(target)
        if not (target / "SKILL.md").exists():
            # 只覆盖「看起来确实是技能目录」的目录，避免误删无关文件夹
            raise ValueError("目标已存在且不含 SKILL.md，拒绝覆盖：%s" % target)

    tmp = target.parent / (".%s.tmp-%d" % (target.name, os.getpid()))
    if tmp.exists():
        shutil.rmtree(tmp, ignore_errors=True)  # skill-audit: ignore 只清理自己刚建的临时目录
    tmp.mkdir(parents=True)
    try:
        (tmp / "SKILL.md").write_text(
            build_frontmatter(a, name, dirs, deps) + "\n\n"
            + build_body(a, name, dirs, deps, with_sync=with_sync and "scripts" in dirs),
            encoding="utf-8")
        created.append("SKILL.md")

        for d in dirs:
            (tmp / d).mkdir(parents=True, exist_ok=True)
            created.append("%s/" % d)

        if with_sync and "scripts" in dirs:
            (tmp / "scripts" / "sync.py").write_text(sync_py_text(), encoding="utf-8")
            created.append("scripts/sync.py")

        if deps and "scripts" in dirs:
            (tmp / "scripts" / "setup.py").write_text(
                build_setup_py(name, deps), encoding="utf-8")
            created.append("scripts/setup.py")

        if fields and "config" in dirs:
            (tmp / "config" / "settings.example.json").write_text(
                build_config_example(name, fields), encoding="utf-8")
            created.append("config/settings.example.json")

        backup = None
        if target.exists():
            backup = make_backup(target)      # 先备份旧版，再让新版就位
        _rename_with_retry(tmp, target)
        if backup:
            created.append("(覆盖) 旧版已备份到 %s" % backup)
    except BaseException:
        shutil.rmtree(tmp, ignore_errors=True)  # skill-audit: ignore 同上，回滚半成品
        raise

    return created


def main() -> int:
    use_utf8_stdout()

    ap = argparse.ArgumentParser(description="从需求生成合规的技能骨架")
    ap.add_argument("skill_name")
    ap.add_argument("--out", default=None, help="技能父目录，默认自动探测（WorkBuddy 上为 ~/.workbuddy/skills）")
    ap.add_argument("--prefix", default=None,
                    help="技能名前缀（个人/团队标识），**默认不加**；传空串等价于 --no-prefix。"
                         "想固定用某个前缀：设环境变量 %s，或在平台根建 %s 写 "
                         '{"name_prefix": "xxx-"}' % (PREFIX_ENV, PREFIX_CONFIG_NAME))
    ap.add_argument("--no-prefix", action="store_true",
                    help="明确不加前缀（优先级最高，连本机配置的前缀也一起忽略）")
    ap.add_argument("--display-name", default=None)
    ap.add_argument("--display-name-en", default=None)
    ap.add_argument("--desc", default=None, help="description：做什么/何时触发/触发词")
    ap.add_argument("--desc-zh", default=None)
    ap.add_argument("--desc-en", default=None)
    ap.add_argument("--category", default="dev-programming",
                    help="市场分类，默认 dev-programming；取值须落在平台 13 个枚举内，"
                         "否则上架后显示「未分类」（枚举见 audit_skill.SKILLHUB_CATEGORIES）")
    ap.add_argument("--author", default=None)
    ap.add_argument("--triggers", default="")
    ap.add_argument("--dirs", default="scripts,references")
    ap.add_argument("--deps", default="")
    ap.add_argument("--config-fields", default="")
    ap.add_argument("--mode", choices=["market", "local"], default="market")
    ap.add_argument("--no-audit", action="store_true")
    ap.add_argument("--no-sync", action="store_true",
                    help="不注入 scripts/sync.py 版本自检器（默认每个带 scripts/ 的技能都会注入）")
    ap.add_argument("--install", action="store_true",
                    help="骨架生成在技能目录之外时，额外复制一份到 ~/.workbuddy/skills 让它本机可用")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    raw_name = args.skill_name.strip().lower()
    name = normalize_name(args.skill_name)
    if not name or not VALID_NAME.match(name) or len(name) > 64:
        if re.search(r"[\u4e00-\u9fff]", args.skill_name):
            how = ("目录名只能用英文（平台硬要求），中文名请用 --display-name \"%s\" 单独给；"
                   "例如：new_skill.py oa-todo --display-name \"%s\""
                   % (args.skill_name, args.skill_name))
        else:
            how = ("目录名要求：小写字母开头，只含小写字母 / 数字 / 连字符，长度 ≤ 64；"
                   "例如 oa-todo、pdf-tools。中文展示名用 --display-name 单独给")
        die(3, "这个名字不能当目录名：%r" % args.skill_name, how)
    if name != raw_name:
        print("技能名已规整：%r -> %r" % (args.skill_name, name))

    # 前缀是**可选项**：用户没指定、本机也没配，就保持裸名。
    raw_prefix, prefix_src = resolve_prefix(args.prefix, args.no_prefix)
    prefix = re.sub(r"[^a-z0-9]+", "-", raw_prefix.strip().lower()).strip("-")
    prefix = (prefix + "-") if prefix else ""
    if prefix and not name.startswith(prefix):
        name = prefix + name
        print("已加前缀：%s（来源：%s；不想加用 --no-prefix）" % (name, prefix_src or "默认配置"))
    elif prefix:
        print("技能名已带 `%s` 前缀，保持不变" % prefix)

    dirs = [d.strip() for d in args.dirs.split(",") if d.strip()]
    unknown = [d for d in dirs if d not in KNOWN_DIRS]
    if unknown:
        die(3, "未知子目录：%s" % ", ".join(unknown),
            "可选值只有：%s；不认识的目录不建，避免事后发现放错地方" % ", ".join(KNOWN_DIRS))
    deps = [d.strip() for d in args.deps.split(",") if d.strip()]
    fields = [f.strip() for f in args.config_fields.split(",") if f.strip()]
    if fields and "config" not in dirs:
        dirs.append("config")

    triggers = [t.strip() for t in re.split(r"[,，]", args.triggers) if t.strip()]
    args.triggers = triggers          # 必须回写：否则下游会把整串按字符遍历
    dirs = [d for d in KNOWN_DIRS if d in dirs]     # 统一成规范顺序展示

    # 展示名不带前缀（前缀是技术标识，不该出现在给人看的名字里）
    bare = name[len(prefix):] if prefix and name.startswith(prefix) else name
    args.display_name = args.display_name or title_case(bare)
    args.display_name_en = args.display_name_en or title_case(bare)
    args.author = args.author or guess_author()
    if not args.desc:
        # 同样不能用尖括号（漏改过一处）：check_market 把含 <> 的展示字段判成 P1，
        # 于是「纯脚本生成」不给人填任何东西时也会红一次。
        args.desc = ("待填写：一句话说清这个技能解决什么问题。当用户提到「%s」"
                     "时使用。" % "」「".join(triggers or ["触发词A", "触发词B"]))
    elif triggers:
        miss = [t for t in triggers if t not in args.desc]
        if miss:
            args.desc = args.desc.rstrip() + " 也适用于「%s」这类说法。" % "」「".join(miss)
    # 占位值一律**不用尖括号**：check_market 会把含 <> 的展示字段判成 P1，
    # 于是「生成即体检」每次都报两条 P1 —— 骨架还没填内容就先红一次。
    args.desc_zh = args.desc_zh or "待填写：30 字以内的中文一句话介绍"
    args.desc_en = args.desc_en or "TODO: One-line English introduction"

    try:
        default_parent = skills_dir()
    except PathResolutionError as e:
        if not args.out:
            die(3, "定位不到技能目录：%s" % e,
                "显式传入 --out <技能父目录>，或设置环境变量 %s" % SKILLS_HOME_ENV)
        default_parent = None          # 用户自己指定了目录，就不再需要自动定位
    parent = Path(args.out).expanduser().resolve() if args.out else default_parent
    target = parent / name

    print("技能名   : %s" % name)
    print("目标目录 : %s" % target)
    print("模式     : %s" % ("技能市场分发规范" if args.mode == "market" else "本机自用"))
    try:
        created = write_all(target, args, name, dirs, deps, fields, args.force,
                            with_sync=not args.no_sync)
    except FileExistsError:
        die(3, "目标已存在：%s" % target,
            "确认覆盖加 --force（只会覆盖含 SKILL.md 的技能目录；覆盖前旧版会自动备份）")
    except ValueError as e:
        die(3, str(e), "换一个技能名，或确认它真是技能目录后加 --force")
    except OSError as e:
        die(4, "写入失败：%s" % target, "", exc=e)

    print("已创建   : %s" % "、".join(created))

    # ---- 落在技能目录之外时，本机不会生效，按需补装一份 ----
    in_skill_dir = is_inside(target, default_parent) if default_parent else True
    installed = None
    if in_skill_dir:
        installed = target
    elif args.install:
        installed = install_copy(target, name, args.force)

    # ---- 生成即体检：闭环 ----
    verdict = 0
    summary = None
    if not args.no_audit:
        from audit_skill import audit  # noqa: E402  同目录脚本
        rep = audit(target, market=(args.mode == "market"))
        p0, p1, p2 = rep.count("P0"), rep.count("P1"), rep.count("P2")
        summary = {"P0": p0, "P1": p1, "P2": p2, "verdict": rep.worst}
        print("生成后体检: P0=%d  P1=%d  P2=%d" % (p0, p1, p2))
        for f in rep.findings():
            if f["severity"] in ("P0", "P1"):
                print("  [%s] %s :: %s" % (f["severity"], f["rule"], f["hint"][:70]))
        if p0:
            verdict = 2
        elif p1:
            verdict = 1
        else:
            print("  骨架合规，可以开始填内容。")

    if installed:
        print("\n技能已就绪：%s" % installed)
        print("  若未立刻出现在可用技能列表，重启会话即可被识别。")
    else:
        print("\n!! 本机还没有这个技能：%s 不在技能安装目录内。" % parent)
        print("   要立刻可用，重跑时加 --install，或去掉 --out 用默认目录。")

    print("\n下一步：")
    print("  1. 打开 %s，把「待填写 / TODO」占位全部替换成真实内容" % (target / "SKILL.md"))
    print("  2. 补上「常见坑」——把本次实现踩到的坑写进去")
    print("  3. python scripts/audit_skill.py \"%s\" --market" % target)
    print("  4. python scripts/pack_skill.py \"%s\"" % target)
    print("  （改版本号用 python scripts/bump.py \"%s\" -m \"说明\"）" % target)

    if verdict:
        print("\n" + explain_exit(verdict))

    if args.json:
        print(json.dumps({"name": name, "path": str(target),
                          "installed": str(installed) if installed else None,
                          "created": created, "audit": summary}, ensure_ascii=False))
    return verdict


if __name__ == "__main__":
    raise SystemExit(main())
