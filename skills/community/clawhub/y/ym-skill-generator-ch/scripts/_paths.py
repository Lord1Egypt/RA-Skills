"""平台无关的路径解析 —— 技能装到哪，就往哪写。

为什么代码里不该写死某个平台的技能目录：
    技能「被安装」到哪个目录，是平台（安装者）决定的 —— 把技能包交给平台说
    一句"装上"，它自然落到自己的技能目录里，跟包里写没写路径无关。一旦写死，
    换个平台装上就指向了不存在的目录，而且不报错。

那脚本要往技能目录里写东西时怎么知道目录在哪：
    脚本运行时自己就住在技能目录里，从 __file__ 反推即可 ——

        <平台根>/<技能目录>/<技能名>/scripts/xxx.py
        parents[3]   parents[2]  parents[1] parents[0]

    全程不需要知道平台叫什么，也不需要逐个候选目录去猜（猜会误判：一台机器上
    完全可能同时存在好几个平台的技能目录）。

反推不出来怎么办：
    抛 PathResolutionError，由调用方提示显式传参。**绝不静默回落到某个平台目录** ——
    静默回落等于在别的平台上把技能写到错误位置还一声不吭，比报错糟得多。
"""

from __future__ import annotations

import os
from pathlib import Path

SKILLS_HOME_ENV = "SKILLS_HOME"            # 显式指定技能目录
PLATFORM_ROOT_ENV = "SKILLS_PLATFORM_ROOT"  # 显式指定平台根

# 反推出的目录得「长得像技能目录」才认：至少这么多个子目录含 SKILL.md。
# 这是为了防止开发态误判 —— 从 git 仓库里直接跑脚本时，parents[2] 是项目目录。
_MIN_SKILL_SUBDIRS = 3


class PathResolutionError(RuntimeError):
    """定位不到技能目录 / 平台根。调用方应转成友好提示并要求显式传参。"""


def looks_like_skills_dir(p: Path) -> bool:
    """目录里有多个含 SKILL.md 的子目录，才算真的技能目录。"""
    try:
        if not p.is_dir():
            return False
        return sum(1 for c in p.iterdir()
                   if c.is_dir() and (c / "SKILL.md").exists()) >= _MIN_SKILL_SUBDIRS
    except OSError:
        return False


def resolve(script_file: str | Path | None = None) -> tuple[Path, Path] | None:
    """从脚本自身位置反推 (技能目录, 平台根)；看不出来返回 None。"""
    here = Path(script_file or __file__).resolve()
    if len(here.parents) < 4:
        return None
    skills, root = here.parents[2], here.parents[3]
    if not looks_like_skills_dir(skills):
        return None
    return skills, root


def skills_dir(script_file: str | Path | None = None,
               override: str | Path | None = None) -> Path:
    """技能目录。优先级：显式 override > 环境变量 > 自身位置反推 > 报错。"""
    if override:
        return Path(override).expanduser().resolve()
    env = os.environ.get(SKILLS_HOME_ENV, "").strip()
    if env:
        return Path(env).expanduser().resolve()
    r = resolve(script_file)
    if r:
        return r[0]
    raise PathResolutionError("脚本不在已安装的技能目录结构里，无法自动定位技能目录")


def platform_root(script_file: str | Path | None = None) -> Path:
    """平台根（技能目录的上一层），用于取 USER.md、skill-icons 这类兄弟目录。"""
    env = os.environ.get(PLATFORM_ROOT_ENV, "").strip()
    if env:
        return Path(env).expanduser().resolve()
    r = resolve(script_file)
    if r:
        return r[1]
    raise PathResolutionError("脚本不在已安装的技能目录结构里，无法自动定位平台根")


def platform_sub(dirname: str, script_file: str | Path | None = None,
                 fallback_home: bool = False) -> Path:
    """平台根下的兄弟目录，如 skill-icons / skill-backups。

    fallback_home=True 时定位不到就退到用户主目录下的同名目录 —— 只给「放错位置
    也不影响正确性」的东西用（图标、备份）。技能目录本身绝不开这个口子。
    """
    try:
        return platform_root(script_file) / dirname
    except PathResolutionError:
        if fallback_home:
            return Path.home() / dirname
        raise


def skills_dir_of(skill_path: str | Path) -> Path:
    """某个技能**被安装在**哪个技能目录里（= 它的父目录）。

    用于打包后"装回原处"：被打包的技能本来在哪个技能目录，就装回哪里。
    """
    p = Path(skill_path).resolve().parent
    if not looks_like_skills_dir(p):
        raise PathResolutionError("「%s」不在技能目录里，无法推断安装目标" % p)
    return p
