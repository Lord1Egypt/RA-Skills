#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能进化（知行环）— 初始化 .wiki 目录结构（跨平台版）

用法:
    python wiki_init.py [项目根目录]

支持: Windows (CMD/PowerShell) / macOS / Linux —— 只要装了 Python 3.6+
这是跨平台首选入口；bash 用户也可用 scripts/wiki_init.sh。

设计要点:
  · 幂等：.wiki/ 已存在则原样保留，绝不覆盖既有数据。
  · 瞬时失败自动重试：Windows 上杀毒扫描 / 编辑器占用会导致 PermissionError，
    重试一两次即可成功，不该让用户手动再跑一遍。
  · 报错说人话：不抛原始 traceback，而是给「哪里出错 + 怎么办」。
    排查清单见 references/anti-patterns.md 的「报错速查表」。
"""

import os
import sys
import time
from datetime import date

# Windows 下 stdout 默认编码是 GBK(cp936)，输出中文会抛 UnicodeEncodeError。
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

TEMPLATES = {
    "knowledge/patterns.md": """# Wiki Knowledge — 模式库

> 本文件由 Wiki Maintainer 维护，记录从执行轨迹中提炼的失败模式与成功策略。
> 只增不减，永不重置。

## 失败模式

（暂无记录）

## 成功策略

（暂无记录）
""",
    "knowledge/evolution_log.md": """# 技能演化日志

> 记录每次 Wiki 维护和技能变更的历史。

（暂无记录）
""",
    "knowledge/impact_tracker.md": """# 提案影响追踪

> 记录每个技能提案的验证结果。

（暂无记录）
""",
    "meta/config.md": """# Wiki 配置

- **创建日期**：{date}
- **维护周期**：每 3-5 个任务后执行一次 Wiki Maintainer
- **进化周期**：每 5-10 个任务后执行一次 Skill Proposer
- **轨迹格式**：精简模式（每条 ≤10 行）
""",
}

# 需要创建的空目录（raw 存轨迹，skills 存可回滚技能）
EMPTY_DIRS = ["raw", "skills"]

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


def with_retry(fn):
    """
    执行文件操作，遇**瞬时** OSError 自动重试（退避 0.4s / 0.8s）。

    Windows 上常见的瞬时失败：杀毒软件正在扫描刚建的文件、编辑器短暂锁目录。
    这类失败重试即可成功；永久性错误（路径不存在、路径中间是文件）立即抛出，
    由调用方翻译成人话。
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


def explain_error(exc: Exception, path: str) -> str:
    """把系统异常翻译成「人话 + 怎么办」，最多 3 步。"""
    kind = type(exc).__name__
    if isinstance(exc, PermissionError):
        return (
            "没有写入权限，或文件正被其他程序占用。\n"
            "     怎么办：\n"
            "       1. 关掉打开着该目录的编辑器 / 资源管理器窗口；\n"
            "       2. 若装了杀毒软件，把项目目录加入白名单（或稍等几秒重跑）；\n"
            "       3. 仍失败则换一个你有写权限的目录。"
        )
    if isinstance(exc, FileNotFoundError):
        return (
            "路径不存在（多半是没站在项目根目录，或上级目录已被删除）。\n"
            "     注意：Windows 在「路径中间某段是普通文件」时也会误报为路径不存在，\n"
            "           若该路径其实存在，请检查沿途各段有没有被同名文件占位。\n"
            "     怎么办：\n"
            "       1. 先 cd 到项目根目录再执行；\n"
            "       2. 或直接传绝对路径：python wiki_init.py \"D:\\你的项目\""
        )
    if isinstance(exc, NotADirectoryError):
        return (
            "路径中间有一段是普通文件，不是目录。\n"
            "     怎么办：确认目标路径没有被同名文件占位（%s）" % path
        )
    if isinstance(exc, IsADirectoryError):
        return "本想写文件，但该路径下已存在同名目录。\n     怎么办：换个项目目录，或先移走同名目录。"
    if isinstance(exc, FileExistsError):
        return (
            "该位置已有同名的文件或目录，无法创建。\n"
            "     怎么办：\n"
            "       1. 若报错路径是 .wiki，多半是被同名文件占位，改名备份后重跑；\n"
            "       2. 其它情况先改名备份（别直接删，可能是你的数据），再重跑。"
        )
    if isinstance(exc, OSError) and getattr(exc, "errno", None) == 28:
        return "磁盘空间不足。\n     怎么办：清理磁盘后重跑。"
    return (
        "系统调用失败：%s: %s\n"
        "     怎么办：把这条提示连同上面的路径一起提供给 AI 助手，或查\n"
        "     references/anti-patterns.md 的「报错速查表」。" % (kind, exc)
    )


def write_file(path: str, content: str, date_str: str) -> None:
    def _do():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        # encoding 必须显式指定 utf-8：
        # Windows 默认使用 GBK(cp936)，不指定会导致中文写入乱码或 UnicodeEncodeError
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(content.format(date=date_str))

    with_retry(_do)


def main() -> int:
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    wiki = os.path.join(root, ".wiki")

    # 幂等：已存在就原样保留。这是有意行为，不是错误（见 AP-17：别删 .wiki 重装）
    if os.path.isdir(wiki):
        print("[技能进化] .wiki 目录已存在，原样保留（不会覆盖你的数据）：%s" % wiki)
        print("           如需重建，请先手动移走该目录。")
        return 0

    if os.path.exists(root) and not os.path.isdir(root):
        print("[技能进化] 错误：目标路径不是目录：%s" % root)
        print("           怎么办：把参数换成项目目录，例如 python wiki_init.py \"D:\\你的项目\"")
        return 1

    # 提前检测「.wiki 被同名文件占位」这个高频坑。
    # 为什么不在 except 里分辨：Windows 上 .wiki 是文件时，创建 .wiki\raw 会返回
    # ERROR_PATH_NOT_FOUND，被 Python 映射成 FileNotFoundError，
    # 于是走进「路径不存在」分支，给出"先 cd 到项目根"这种**永远修不好**的建议。
    # （Linux 抛的是 NotADirectoryError，行为与 Windows 不同。）
    # 靠异常类型分支必然误诊，主动检测才能给出准确诊断。
    if os.path.exists(wiki) and not os.path.isdir(wiki):
        print("[技能进化] 初始化失败：%s" % wiki)
        print("     .wiki 已被同名**文件**占位，而它应该是一个目录。")
        print("     怎么办：")
        print("       1. 先确认这个文件没用（Windows: type \"%s\"；macOS/Linux: cat）" % wiki)
        print("       2. 改名备份留底（别直接删）：把 .wiki 改成 .wiki.bak")
        print("       3. 重跑本命令")
        return 1

    try:
        for d in EMPTY_DIRS:
            with_retry(lambda d=d: os.makedirs(os.path.join(wiki, d), exist_ok=True))
        date_str = date.today().isoformat()
        for rel, content in TEMPLATES.items():
            write_file(os.path.join(wiki, rel), content, date_str)
    except OSError as exc:
        print("[技能进化] 初始化失败：%s" % wiki)
        print("     %s" % explain_error(exc, wiki))
        return 1

    print("[技能进化] 初始化完成: %s" % wiki)
    print("   raw/        - 执行轨迹（按日期追加）")
    print("   knowledge/  - 持久化知识（patterns + evolution_log + impact_tracker）")
    print("   skills/     - 可复用技能（可回滚）")
    print("   meta/       - Wiki 配置")
    print()
    print("下一步（立刻可用，别等自动化）:")
    print("   把你已经知道的坑直接写进 .wiki/knowledge/patterns.md")
    print("   怎么用错会踩坑，见 references/anti-patterns.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
