#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能进化（知行环）· Skill Evolution — 统一安装器（跨平台 / 跨 AI 工具）

设计原则：项目自包含。

技能进化（知行环）不依赖任何 AI 工具的私有目录。安装时把运行时脚本与参考文档
复制进项目内的 .wiki/，生成的指令文件与 hook 全部使用项目内路径。
因此项目可以整体提交 Git，换机器 clone 后无需重新安装即可工作。

与旧版 install_claude_hook.py 的区别：
    旧版把 hook 指向 ~/.workbuddy/skills/<skill名>/，那是 WorkBuddy 的私有
    目录。纯 Claude Code / Codex 用户机器上该目录不存在，hook 会静默失效。
    本安装器把运行时复制到目标平台自己的位置，或项目内，并校验路径真实存在。

用法:
    python install.py --platform claude                 # 项目级自包含（默认，推荐）
    python install.py --platform codex                  # 同上，生成 AGENTS.md
    python install.py --platform claude --user          # 用户级，脚本装到 ~/.claude/scripts/skill-evolution/
    python install.py --platform claude --target DIR    # 指定项目目录
    python install.py --platform claude --no-hook       # 只生成文件，不装 hook
    python install.py --platform claude --uninstall     # 移除 hook（绝不删除 .wiki/ 数据）

平台与产物:
    claude    -> CLAUDE.md + .claude/settings.json (Stop hook)
    codex     -> AGENTS.md（Codex 无 hook 机制，不生成配置文件）
    workbuddy -> 只准备 .wiki/，指令由 WorkBuddy 的 SKILL.md 提供

容错设计:
    · 幂等：已存在的文件一律不覆盖（含 .wiki/ 数据、指令文件）。
    · 瞬时失败自动重试：Windows 上杀毒扫描 / 编辑器占用会导致 PermissionError，
      退避重试几次即可成功，避免"手动再跑一遍"。
    · 报错说人话：不抛原始 traceback，给「哪里出错 + 怎么办」。
      完整排查表见 references/anti-patterns.md。
"""

import argparse
import json
import os
import shutil
import sys
import time
from datetime import date
from pathlib import Path

# Windows 下 stdout 默认是 GBK(cp936)，输出中文会抛 UnicodeEncodeError。
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

# 识别本框架 hook 的特征串。
# 必须包含 "wiki_remind"：项目级安装使用项目内相对路径
# （python ".wiki/scripts/wiki_remind.py"），命令里不含 skill 名，
# 只靠 skill 名匹配会导致去重与卸载双双失效 —— 故以脚本名为主判据。
# 同时保留旧名 "wikiskill"：本 skill 由 wikiskill + rsi-knowledge +
# rsi-self-improvement-designer 三合一而来，保留旧名才能识别并卸载
# 整合之前安装的 hook，避免重复注入。
HOOK_MARKERS = ("skill-evolution", "wikiskill", "wiki_remind")

# 运行时文件（复制到目标位置，保证自包含）
RUNTIME_FILES = ["wiki_init.py", "wiki_init.sh", "wiki_init.ps1",
                 "wiki_remind.py", "wiki_remind.sh"]

# 参考文档（复制进项目 .wiki/references/）
# 前四个是经验沉淀（.wiki 运行时）所必需；后三个是 RSI 判据、自改进设计手册
# 与反模式清单，一并复制以便项目内的联合自改进闭环自包含、不依赖 skill 安装目录。
REFERENCE_FILES = ["workflow.md", "platforms.md", "automation.md", "templates.md",
                   "rsi-framework.md", "design-playbook.md", "anti-patterns.md"]

# 瞬时失败重试次数与退避基数（秒）
RETRY_TIMES = 3
RETRY_DELAY = 0.4

# 只对"重试可能成功"的错误重试；永久性错误立即失败，不白等。
# errno: 13=EACCES 11=EAGAIN 16=EBUSY 26=ETXTBSY
# winerror: 5=拒绝访问 32=文件被占用 33=文件被锁定
TRANSIENT_ERRNOS = {11, 13, 16, 26}
TRANSIENT_WINERRORS = {5, 32, 33}


def is_transient(exc: Exception) -> bool:
    """判断是否属于"稍等重试就能成功"的瞬时故障。"""
    if isinstance(exc, PermissionError):
        return True
    if isinstance(exc, OSError):
        if getattr(exc, "errno", None) in TRANSIENT_ERRNOS:
            return True
        if getattr(exc, "winerror", None) in TRANSIENT_WINERRORS:
            return True
    return False

PLATFORM_SPECS = {
    "claude": {
        "instruction": "CLAUDE.md",
        "template": "CLAUDE.template.md",
        "user_dir": ".claude",
        "supports_hook": True,
    },
    "codex": {
        "instruction": "AGENTS.md",
        "template": "AGENTS.template.md",
        "user_dir": ".codex",
        "supports_hook": False,
    },
    "workbuddy": {
        "instruction": None,
        "template": None,
        "user_dir": ".workbuddy",
        "supports_hook": False,
    },
}


def with_retry(fn):
    """
    执行文件操作，遇**瞬时** OSError 自动重试（退避 0.4s / 0.8s）。

    Windows 上常见的瞬时失败：杀毒软件正在扫描刚复制的文件、编辑器短暂锁目录，
    报 errno 13 / winerror 32。这类失败重试即可成功，不该让用户手动再跑一遍。

    永久性错误（路径不存在、路径中间是文件、磁盘满）**立即抛出**，不浪费等待时间，
    由调用方翻译成人话。判定逻辑见 is_transient()。
    """
    last = None
    for attempt in range(RETRY_TIMES):
        try:
            return fn()
        except OSError as exc:
            if not is_transient(exc):
                raise
            last = exc
            if attempt < RETRY_TIMES - 1:
                time.sleep(RETRY_DELAY * (attempt + 1))
    raise last


def explain_error(exc: Exception, path) -> str:
    """把系统异常翻译成「人话 + 怎么办」，最多 3 步。"""
    kind = type(exc).__name__
    if isinstance(exc, PermissionError):
        return (
            "没有写入权限，或文件正被其他程序占用。\n"
            "       怎么办：\n"
            "         1. 关掉打开着该目录的编辑器 / 资源管理器窗口；\n"
            "         2. 若装了杀毒软件，把项目目录加入白名单（或稍等几秒重跑）；\n"
            "         3. 仍失败则换一个你有写权限的目录重装。"
        )
    if isinstance(exc, FileNotFoundError):
        return (
            "路径不存在（多半是 --target 指错了，或上级目录已被删除）。\n"
            "       注意：Windows 在「路径中间某段是普通文件」时也会误报为路径不存在，\n"
            "             若该路径其实存在，请检查沿途各段有没有被同名文件占位。\n"
            "       怎么办：\n"
            "         1. 确认目录真的存在，或用绝对路径；\n"
            "         2. 不传 --target 时默认用当前目录，先 cd 到项目根。"
        )
    if isinstance(exc, NotADirectoryError):
        return "路径中间有一段是普通文件，不是目录。\n       怎么办：检查 %s 是否被同名文件占位。" % path
    if isinstance(exc, FileExistsError):
        return (
            "该位置已有同名的文件或目录，无法创建。\n"
            "       怎么办：\n"
            "         1. 若报错路径是 .wiki，多半是被同名文件占位，改名备份后重跑；\n"
            "         2. 其它情况先改名备份（别直接删，可能是你的数据），再重跑。"
        )
    if isinstance(exc, OSError) and getattr(exc, "errno", None) == 28:
        return "磁盘空间不足。\n       怎么办：清理磁盘后重跑。"
    return (
        "系统调用失败：%s: %s\n"
        "       怎么办：把这条提示连同上面的路径一起提供给 AI 助手，或查\n"
        "       references/anti-patterns.md 的「报错速查表」。" % (kind, exc)
    )


def write_text(path: Path, text: str) -> None:
    """始终以 UTF-8 + LF 写文本（newline 参数在 3.10 才有，故不用 write_text）。"""
    def _do():
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(str(path), "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
    with_retry(_do)


def source_dirs() -> tuple:
    """定位本 skill 的 scripts/ 与 references/ 目录（解压到任意位置均可）。"""
    here = Path(__file__).resolve().parent
    skill_root = here.parent
    return skill_root / "scripts", skill_root / "references"


def detect_python() -> str:
    """
    检测可用的 Python 启动命令。

    Windows 上可能只有 py -3 而没有 python；macOS/Linux 上可能只有 python3。
    写死 python 会让 hook 在这类机器上静默失效。
    """
    for cmd in ("python", "python3", "py -3"):
        exe = cmd.split()[0]
        if shutil.which(exe):
            return cmd
    return "python"  # 检测不到则退回最常见写法


def create_wiki_skeleton(target: Path) -> bool:
    """创建 .wiki/ 骨架。已存在则原样保留（绝不覆盖用户数据）。"""
    created = not (target / ".wiki").exists()
    for sub in ("raw", "knowledge", "skills", "meta", "scripts", "references"):
        with_retry(lambda sub=sub: (target / ".wiki" / sub).mkdir(parents=True, exist_ok=True))

    if created:
        files = {
            "knowledge/patterns.md": "# 模式库\n\n## 失败模式\n\n（暂无记录）\n\n## 成功策略\n\n（暂无记录）\n",
            "knowledge/evolution_log.md": "# 技能演化日志\n\n（暂无记录）\n",
            "knowledge/impact_tracker.md": "# 提案影响追踪\n\n（暂无记录）\n",
            "meta/config.md": "# Wiki 配置\n\n- **创建日期**：%s\n- **维护周期**：每 3-5 个任务后执行一次 Wiki Maintainer\n"
                             % date.today().isoformat(),
        }
        for rel, content in files.items():
            p = target / ".wiki" / rel
            if not p.exists():
                write_text(p, content)
    return created


def copy_runtime(target: Path, scripts_src: Path, refs_src: Path) -> tuple:
    """
    复制运行时脚本与参考文档进项目。

    返回 (copied, missing)：missing 里的源文件在包里就不存在。
    之所以要报出来而不是静默跳过：静默跳过会让用户以为"装好了"，
    实际缺文件却在运行时才暴露。
    """
    copied, missing = [], []
    pairs = ([(scripts_src / n, target / ".wiki" / "scripts" / n, "scripts/" + n)
              for n in RUNTIME_FILES]
             + [(refs_src / n, target / ".wiki" / "references" / n, "references/" + n)
                for n in REFERENCE_FILES])
    for src, dst, label in pairs:
        if src.exists():
            with_retry(lambda s=src, d=dst: shutil.copy2(str(s), str(d)))
            copied.append(label)
        else:
            missing.append(label)
    return copied, missing


SELF_CONTAINED_INIT = """如果 `.wiki/` 不存在，任选一种方式创建：

**方式 A — 用项目内脚本**（已随项目存在，无需任何外部依赖）：

```bash
# Windows PowerShell / macOS / Linux / Git Bash
python .wiki/scripts/wiki_init.py
```
```cmd
:: Windows CMD
python .wiki\\scripts\\wiki_init.py
```
```powershell
# Windows PowerShell（无 Python 时的备选）
powershell -ExecutionPolicy Bypass -File .wiki\\scripts\\wiki_init.ps1
```

> 本项目已自包含「技能进化（知行环）」运行时，`.wiki/scripts/` 下的脚本可直接执行。
> 不依赖 WorkBuddy / Claude Code / Codex 的任何全局目录。

**方式 B — 手动创建**（脚本不可用时直接执行）：
```bash
mkdir -p .wiki/raw .wiki/knowledge .wiki/skills .wiki/meta
printf '# 模式库\\n\\n## 失败模式\\n\\n（暂无记录）\\n\\n## 成功策略\\n\\n（暂无记录）\\n' > .wiki/knowledge/patterns.md
printf '# 技能演化日志\\n\\n（暂无记录）\\n' > .wiki/knowledge/evolution_log.md
printf '# 提案影响追踪\\n\\n（暂无记录）\\n' > .wiki/knowledge/impact_tracker.md
```"""

SELF_CONTAINED_REF = """- 闭环全图与四问评分卡（权威源）：`.wiki/references/workflow.md`
- ① 选域 / ⑦ 升阶（HCI、L1–L5）：`.wiki/references/rsi-framework.md`
- 全链自改进设计五步：`.wiki/references/design-playbook.md`
- **反模式清单与报错速查（别这样做 / 报错怎么办）**：`.wiki/references/anti-patterns.md`
- 平台适配：`.wiki/references/platforms.md`
- 自动化方案：`.wiki/references/automation.md`
- 模板集合：`.wiki/references/templates.md`
- 原论文：WikiSkill, arXiv:2608.27454（经验怎么存、怎么迭代）；RSI 路线图, arXiv:2609.11873（改进算不算数、能自动到哪）"""


def replace_section(text: str, start_marker: str, end_marker: str, new_body: str) -> str:
    """按 HTML 注释标记替换片段；找不到标记则原样返回。"""
    s = text.find(start_marker)
    e = text.find(end_marker)
    if s == -1 or e == -1 or e < s:
        return text
    # 保留起始标记所在行之前的内容，替换两标记之间的正文
    head = text[:s + len(start_marker)]
    tail = text[e:]
    return head + "\n" + new_body + "\n" + tail


def render_instruction(template_path: Path) -> str:
    """把模板渲染为自包含版本（去掉对 ~/.workbuddy 的依赖）。"""
    text = template_path.read_text(encoding="utf-8")
    text = replace_section(text, "<!-- INIT_SECTION_START -->",
                           "<!-- INIT_SECTION_END -->", SELF_CONTAINED_INIT)
    text = replace_section(text, "<!-- REF_SECTION_START -->",
                           "<!-- REF_SECTION_END -->", SELF_CONTAINED_REF)
    return text


def remind_command(project_level: bool, project_root: Path, user_script: Path = None) -> str:
    """
    构造 hook 命令。

    项目级用相对路径 —— 项目移动或 clone 到别处仍有效。
    用户级用绝对路径 —— 用户级配置会应用到所有项目，相对路径会指向错误目录。
    Windows 用 wiki_remind.py（cmd/PowerShell 无 bash），Unix 用 .sh。
    """
    if project_level:
        rel = ".wiki/scripts/wiki_remind.py" if os.name == "nt" else ".wiki/scripts/wiki_remind.sh"
        return '%s "%s"' % (detect_python() if os.name == "nt" else "bash", rel)
    script = user_script
    if os.name == "nt":
        return '%s "%s"' % (detect_python(), script)
    return 'bash "%s"' % script


def is_skill_evolution_command(command: str) -> bool:
    """判断一条 hook 命令是否属于技能进化（知行环）。"""
    low = command.lower()
    return any(m in low for m in HOOK_MARKERS)


def collect_skill_hooks(settings: dict) -> list:
    """
    收集所有属于本框架的 hook 命令。

    返回 [(group_index, hook_index, command), ...]。
    之所以要拿到命令原文而不只是布尔值：整合前的用户级安装会把 hook 指向
    ~/.claude/scripts/wikiskill/wiki_remind.py，若只判断"存在同类 hook"
    就跳过，旧路径会被永久保留，运行时再也升不上去。
    """
    found = []
    for gi, group in enumerate(settings.get("hooks", {}).get("Stop", [])):
        if not isinstance(group, dict):
            continue
        for hi, h in enumerate(group.get("hooks", [])):
            if not isinstance(h, dict):
                continue
            cmd = h.get("command", "")
            if is_skill_evolution_command(cmd):
                found.append((gi, hi, cmd))
    return found


def strip_skill_hooks(settings: dict) -> None:
    """移除所有属于本框架的 hook 项，同组内的其他 hook 原样保留。"""
    stop = settings.get("hooks", {}).get("Stop", [])
    kept = []
    for group in stop:
        if not isinstance(group, dict):
            kept.append(group)
            continue
        inner = [h for h in group.get("hooks", [])
                 if not (isinstance(h, dict)
                         and is_skill_evolution_command(h.get("command", "")))]
        if inner:
            group["hooks"] = inner
            kept.append(group)

    if kept:
        settings["hooks"]["Stop"] = kept
    else:
        settings["hooks"].pop("Stop", None)
        if not settings["hooks"]:
            settings.pop("hooks", None)


def merge_hook(settings_path: Path, command: str) -> str:
    """
    合并而非覆盖：保留已有 permissions / 其他 hooks。

    已存在同类 hook 时不再无条件跳过。命令不一致（典型情形：整合前用户级
    安装留下的 wikiskill 路径）说明这是升级前的旧 hook，必须替换成新命令，
    否则 hook 会一直调用旧目录里的运行时快照。
    """
    settings = {}
    if settings_path.exists():
        try:
            settings = json.loads(with_retry(
                lambda: settings_path.read_text(encoding="utf-8")))
        except json.JSONDecodeError:
            return ("错误：%s 不是合法 JSON，已中止以免损坏配置。\n"
                    "       怎么办：从备份恢复该文件，或删掉它后重跑（会重新生成）。"
                    % settings_path)

    existing = collect_skill_hooks(settings)
    if existing and all(cmd == command for _, _, cmd in existing):
        return "跳过：%s 中已存在相同命令的 hook。" % settings_path

    old = [cmd for _, _, cmd in existing]
    if old:
        strip_skill_hooks(settings)

    settings.setdefault("hooks", {}).setdefault("Stop", []).append(
        {"hooks": [{"type": "command", "command": command}]})
    write_text(settings_path,
               json.dumps(settings, indent=2, ensure_ascii=False) + "\n")

    if old:
        return ("已升级 hook（替换旧命令，其余配置保留）：%s\n  旧：%s\n  新：%s"
                % (settings_path, "；".join(old), command))
    return "已安装 hook：%s\n  命令：%s" % (settings_path, command)


def remove_hook(settings_path: Path) -> str:
    if not settings_path.exists():
        return "跳过：配置文件不存在 %s" % settings_path
    try:
        settings = json.loads(with_retry(
            lambda: settings_path.read_text(encoding="utf-8")))
    except json.JSONDecodeError:
        return ("错误：%s 不是合法 JSON，已中止。\n"
                "       怎么办：从备份恢复该文件后重跑。" % settings_path)

    existing = collect_skill_hooks(settings)
    if not existing:
        return "跳过：未找到技能进化（知行环）的 hook %s" % settings_path

    # 复用 strip_skill_hooks，而非按组删除：一个 Stop 组里可能同时含有本框架的
    # hook 和用户自己的 hook（例如手工把两者放在一起）。按组删除会把用户自己的
    # hook 一起干掉，且与升级路径（merge_hook）的行为不一致。
    strip_skill_hooks(settings)
    write_text(settings_path, json.dumps(settings, indent=2, ensure_ascii=False) + "\n")
    return ("已移除 %d 条技能进化（知行环）hook（同组其他 hook 与其余配置保持不变）：%s"
            % (len(existing), settings_path))


def install_user_level(platform: str, scripts_src: Path, want_hook: bool) -> int:
    """
    用户级安装：运行时复制到平台自己的目录，不依赖 WorkBuddy。

    claude -> ~/.claude/scripts/skill-evolution/
    codex  -> ~/.codex/scripts/skill-evolution/
    """
    spec = PLATFORM_SPECS[platform]
    dest = Path.home() / spec["user_dir"] / "scripts" / "skill-evolution"
    with_retry(lambda: dest.mkdir(parents=True, exist_ok=True))

    missing = []
    for name in RUNTIME_FILES:
        src = scripts_src / name
        if src.exists():
            with_retry(lambda s=src, n=name: shutil.copy2(str(s), str(dest / n)))
        else:
            missing.append(name)

    print("[用户级] 运行时已复制到：%s" % dest)
    if missing:
        print("        缺失源文件（可忽略，多为 .sh 在 Windows 上不需要）：%s"
              % ", ".join(missing))

    # 整合前的用户级安装会把运行时放在 <平台目录>/scripts/wikiskill/。
    # 新 hook 指向新目录，旧目录不再被引用，但不会自动删除 —— 明确提示，
    # 避免用户以为两个目录里哪份在生效。
    legacy = Path.home() / spec["user_dir"] / "scripts" / "wikiskill"
    if legacy.exists():
        print("        检测到整合前的旧运行时：%s" % legacy)
        print("        新 hook 不再引用它，确认提醒正常后即可删除该目录。")

    if not want_hook or not spec["supports_hook"]:
        if not spec["supports_hook"]:
            print("        平台 %s 无 hook 机制，跳过 hook 安装。" % platform)
        return 0

    settings_path = Path.home() / spec["user_dir"] / "settings.json"
    script = dest / ("wiki_remind.py" if os.name == "nt" else "wiki_remind.sh")

    # 用户级配置可能含 API token 等敏感信息，写入前明确告知
    if settings_path.exists():
        print("        注意：将修改已有配置 %s（其余内容保留）" % settings_path)
    print(merge_hook(settings_path, remind_command(False, None, script)))
    print("        生效条件：重启会话后，项目存在 .wiki/ 时输出记录提醒。")
    return 0


def install(args) -> int:
    spec = PLATFORM_SPECS[args.platform]
    scripts_src, refs_src = source_dirs()

    if not scripts_src.exists():
        print("[错误] 找不到 scripts/ 目录：%s" % scripts_src)
        print("       怎么办：确认 install.py 仍在 skill-evolution 包内的 scripts/ 下，")
        print("               从解压后的完整目录里执行，别单独把 install.py 拷出来。")
        return 1

    if args.user:
        return install_user_level(args.platform, scripts_src, not args.no_hook)

    # ---- 项目级：自包含 ----
    target = Path(args.target).resolve() if args.target else Path.cwd()
    if not target.exists():
        print("[错误] 目标目录不存在：%s" % target)
        print("       怎么办：确认路径拼写，或先 cd 到项目根目录再执行。")
        return 1
    if not target.is_dir():
        print("[错误] --target 指向的不是目录：%s" % target)
        print("       怎么办：--target 要传项目目录，不是某个文件。")
        return 1

    # 提前检测「.wiki 被同名文件占位」这个高频坑。
    # 为什么不在 except 里分辨：此时 mkdir 抛的是 WinError 183(FileExistsError)，
    # 而 Windows 上若占位文件在路径中间，还会被误报成"路径不存在"——
    # 靠异常类型分支必然给错建议。主动检测才能给出准确诊断。
    wiki_dir = target / ".wiki"
    if wiki_dir.exists() and not wiki_dir.is_dir():
        print("[错误] .wiki 已被同名**文件**占位，而它应该是一个目录：")
        print("       %s" % wiki_dir)
        print("       怎么办：")
        print("         1. 先确认这个文件没用（Windows: type \"%s\"；macOS/Linux: cat）" % wiki_dir)
        print("         2. 改名备份留底（别直接删）：把 .wiki 改成 .wiki.bak")
        print("         3. 重跑本命令")
        return 1

    print("=== 技能进化（知行环）安装（项目级 · 自包含）===")
    print("目标项目：%s" % target)
    print()

    try:
        fresh = create_wiki_skeleton(target)
        print("[1/4] .wiki/ 骨架：%s" % ("已创建" if fresh else "已存在，原样保留"))

        copied, missing = copy_runtime(target, scripts_src, refs_src)
        print("[2/4] 运行时复制：%d 个文件 -> .wiki/scripts/ 与 .wiki/references/"
              % len(copied))
        if missing:
            print("      注意：包里缺少这些源文件，未复制：%s" % ", ".join(missing))
            print("      这不影响使用（多为你主动精简过包），但项目内会引用不到它们。")

        if spec["instruction"]:
            tpl = refs_src / spec["template"]
            if tpl.exists():
                out = target / spec["instruction"]
                if out.exists():
                    print("[3/4] %s 已存在，跳过以免覆盖你的修改（需更新请手动删除后重跑）"
                          % spec["instruction"])
                else:
                    write_text(out, render_instruction(tpl))
                    print("[3/4] 已生成 %s（自包含，路径均指向项目内）" % spec["instruction"])
            else:
                print("[3/4] 跳过：模板不存在 %s" % tpl)
        else:
            print("[3/4] 跳过：%s 平台不需要额外指令文件（指令由该平台的 SKILL.md 提供）"
                  % args.platform)

        if args.no_hook or not spec["supports_hook"]:
            reason = "已用 --no-hook 指定" if args.no_hook else "平台无 hook 机制"
            print("[4/4] 跳过 hook 安装（%s）" % reason)
        else:
            settings_path = target / spec["user_dir"] / "settings.json"
            print("[4/4] " + merge_hook(settings_path, remind_command(True, target)))
    except OSError as exc:
        print()
        print("[错误] 安装中断 —— %s" % target)
        print("       %s" % explain_error(exc, target))
        print("       已写入的文件都保留着；修好上述问题后重跑本命令即可（不会覆盖已有内容）。")
        return 1

    print()
    print("完成。项目现已自包含，可整体提交 Git，换机器 clone 后无需重装。")
    print()
    print("下一步：")
    if spec["instruction"]:
        print("  1. 在编辑器里打开 %s，把项目名称/描述改成你自己的" % spec["instruction"])
    else:
        print("  1. 本平台不生成指令文件（指令由 %s 的 SKILL.md 提供），无需额外配置"
              % args.platform)
    print("  2. 别等自动流程 —— 直接把已知的坑手动写进 .wiki/knowledge/patterns.md")
    print("  3. 想避开常见坑，扫一眼 .wiki/references/anti-patterns.md")
    return 0


def uninstall(args) -> int:
    spec = PLATFORM_SPECS[args.platform]
    print("=== 技能进化（知行环）卸载 ===")

    try:
        if args.user:
            settings_path = Path.home() / spec["user_dir"] / "settings.json"
            print(remove_hook(settings_path))
            dest = Path.home() / spec["user_dir"] / "scripts" / "skill-evolution"
            if dest.exists():
                print("运行时目录仍保留：%s（如需彻底删除请手动移除）" % dest)
        else:
            target = Path(args.target).resolve() if args.target else Path.cwd()
            settings_path = target / spec["user_dir"] / "settings.json"
            print(remove_hook(settings_path))
            print("已保留 .wiki/ 与 %s —— 经验数据不自动删除。"
                  % (spec["instruction"] or "指令文件"))
    except OSError as exc:
        print("[错误] 卸载中断")
        print("       %s" % explain_error(exc, ""))
        return 1
    return 0


def main() -> int:
    p = argparse.ArgumentParser(
        description="技能进化（知行环）统一安装器（项目自包含，不依赖 WorkBuddy）")
    p.add_argument("--platform", choices=sorted(PLATFORM_SPECS), default="claude",
                   help="目标 AI 工具，默认 claude")
    p.add_argument("--target", help="项目目录，默认当前目录")
    p.add_argument("--user", action="store_true",
                   help="用户级安装（脚本装到 ~/.claude/scripts/skill-evolution/），默认项目级")
    p.add_argument("--no-hook", action="store_true", help="只生成文件，不安装 hook")
    p.add_argument("--uninstall", action="store_true", help="移除 hook（不删除 .wiki/ 数据）")

    args = p.parse_args()
    if args.user and args.target:
        print("[错误] --user 与 --target 不可同时使用（用户级不针对单个项目）。")
        print("       怎么办：二选一 —— 用户级用 --user；只装某个项目用 --target <目录>。")
        return 1
    return uninstall(args) if args.uninstall else install(args)


if __name__ == "__main__":
    sys.exit(main())
