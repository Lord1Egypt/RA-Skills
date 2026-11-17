# -*- coding: utf-8 -*-
"""
profile — wnp_profile.json（买家排版规范）的读取与应用

字段（由 init_profile.py 生成，见其 docstring）：
  theme    signature|mono|paper|custom
  colors   {primary, accent}
  sign     {name, slogan}
  author   默认署名
  rules    {concept_highlight, chapter_numbering, end_sign}
  cover    {auto_geo}

查找顺序：--profile 指定 > 环境变量 WNP_PROFILE > 当前目录 wnp_profile.json。
找不到不报错（无规范 = 用默认 signature + 全开规则，向后兼容）。
"""
import json
import os

_PROFILE_ENV = "WNP_PROFILE"
_DEFAULT_NAME = "wnp_profile.json"


def find_profile(path=None):
    """返回 profile 文件路径；找不到返回 None"""
    cands = []
    if path:
        cands.append(path)
    env = os.environ.get(_PROFILE_ENV)
    if env:
        cands.append(env)
    cands.append(_DEFAULT_NAME)  # 当前工作目录
    for c in cands:
        if c and os.path.exists(c):
            return c
    return None


def load(path):
    """读取并轻校验 profile；结构异常时抛 RuntimeError（指引重跑 init_profile）"""
    try:
        with open(path, encoding="utf-8") as f:
            prof = json.load(f)
    except Exception as e:
        raise RuntimeError(f"profile 读取失败：{path}（{e}）") from e
    if not isinstance(prof, dict) or "theme" not in prof:
        raise RuntimeError(
            f"profile 格式不对：{path}\n请用 init_profile.py 重新生成："
            f"python scripts/init_profile.py")
    return prof


def apply_theme_id(tid):
    """应用内置主题；非法/未知 id 回退 signature。返回实际生效 id"""
    import theme
    if tid not in theme.theme_names() and tid != "custom":
        tid = "signature"
    theme.apply_theme(tid)
    return tid


def apply_profile(prof):
    """按 profile 换肤（含 custom 衍生）。返回生效主题 id"""
    import theme
    tid = prof.get("theme", "signature")
    if tid == "custom":
        c = prof.get("colors") or {}
        theme.apply_custom(c.get("primary", "#2d9d5c"), c.get("accent", "#ff7849"))
        return "custom"
    return apply_theme_id(tid)


def resolve(path=None, cli_theme=None):
    """统一入口：查找+读取+换肤，返回 (prof|None, effective_theme, prof_path|None)

    优先级：CLI --theme 显式 > profile.theme > 默认 signature。
    副作用：已执行 theme.apply_theme/apply_custom（须在渲染前调用一次）。
    """
    p_path = find_profile(path)
    prof = load(p_path) if p_path else None
    if cli_theme:
        return prof, apply_theme_id(cli_theme), p_path
    if prof:
        return prof, apply_profile(prof), p_path
    return None, "signature", p_path
