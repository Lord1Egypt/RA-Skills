# -*- coding: utf-8 -*-
"""
init_profile — 买家「排版偏好确认」向导（首次使用第 0 步）

生成 wnp_profile.json：把你账号的主题色、品牌签名、渲染规范固定成一份
「排版规范」，之后 push_draft / make_preview 每次自动套用，不用重复回答。

两种用法：
  A) 交互向导（推荐首次用）：
       python init_profile.py
     会逐题询问：账号名/签名语 → 主题三选一或自定义配色 → 概念高亮/章节
     编号/文末签名/封面策略 → 打印「排版规范确认单」→ Y 落盘。
  B) 参数模式（可脚本化/测试）：
       python init_profile.py \
           --name 我的账号 --slogan "清醒，但不冷漠" \
           --theme mono \
           --concept highlight --numbering on --end-sign on --cover auto \
           --out wnp_profile.json --yes
      --theme custom 时需 --primary #RRGGBB --accent #RRGGBB。
      --theme 内置(signature/mono/paper)时 --primary/--accent 被忽略。

生成的 wnp_profile.json（给买家看结构，字段带注释）：
  theme     主题 id：signature | mono | paper | custom
  colors    {primary, accent}：实际生效的主色/强调色 hex（custom=买家输入；
            内置主题=该主题原始 hex，仅用于记录与封面取色展示）
  sign      {name, slogan}：文末品牌签名位（为空则不加）
  author    默认作者署名（frontmatter 写了 author 时以文章为准）
  rules     concept_highlight  ==高亮== 渲染：true=主题焦点荧光笔 / false=黑色加粗
            chapter_numbering ## 章节是否自动编号 01/02…
            end_sign          文末是否按 sign 追加签名块
  cover     auto_geo 无封面时是否自动生成几何占位封面

凭据(config.json)不在此文件内——排版规范与公众号凭据分离，各管各的。
"""
import argparse
import json
import os
import re
import sys

try:
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import theme  # noqa: E402

_HEX_RE = re.compile(r"^#?[0-9a-fA-F]{6}$")
_THEME_META = {
    "signature": "绿橙旗舰 · 绿主导(结构)+橙点缀(焦点) · 职场/观点/个人IP",
    "mono": "黑白极简 · 石墨黑结构+经典蓝唯一强调 · 通用职场/科技/方法论",
    "paper": "暖棕纸感 · 暖棕结构+陶土橙强调 · 读书/随笔/文化",
}


def _norm_hex(s, what="颜色"):
    s = (s or "").strip()
    if not s:
        raise ValueError(f"{what}不能为空（格式 #RRGGBB）")
    if not _HEX_RE.match(s):
        raise ValueError(f"{what}需为 #RRGGBB 格式（如 #2d9d5c），收到：{s}")
    return "#" + s.lstrip("#").lower()


def _theme_palette_demo(tid):
    """返回主题的 primary/accent 预览文本（含衍生 5 槽 rgb）"""
    t = theme.get_theme(tid)
    if not t:
        return ""
    c = t["colors"]
    return (f"[{tid}] {t.get('name','')} · {t.get('desc','')}\n"
            f"      结构主色 {c['GREEN']}  焦点强调 {c['ORANGE_ACCENT']}")


def _ask(question, default=None, valid=None):
    """交互式提问：显示默认值，合法范围校验"""
    suffix = f" [{default}]" if default else ""
    while True:
        ans = input(f"{question}{suffix}: ").strip()
        if not ans and default is not None:
            ans = default
        if valid is None or ans in valid:
            return ans
        print(f"  （请输入：{' / '.join(valid)}）")


def _on_off(ans):
    return ans == "on"


def interactive():
    """Q&A 向导，返回 profile dict"""
    print("═══ 公众号排版 · 排版偏好确认 ═══")
    print("（先回答几个问题，把主题色/品牌位/规范固定成你的排版规范）\n")

    # 1 账号与品牌位
    name = _ask("你的账号/署名是？（出现在作者与文末签名）", default="我的账号")
    slogan = input("签名语？（一句话，可留空：文末只署名不加副标语）: ").strip()
    author = name

    # 2 主题
    print("\n可选主题：")
    for tid in theme.theme_names():
        if tid == "custom":
            continue
        print("  " + _theme_palette_demo(tid))
    t_ans = _ask("选主题", default="signature",
                 valid=["signature", "mono", "paper", "custom", "1", "2", "3", "4"])
    tmap = {"1": "signature", "2": "mono", "3": "paper", "4": "custom"}
    tid = tmap.get(t_ans, t_ans)
    primary, accent = None, None
    if tid == "custom":
        print("自定义配色：给两个 #RRGGBB")
        while True:
            try:
                primary = _norm_hex(input("  结构主色（徽章/章节方块/列表/竖线）: "), "主色")
                accent = _norm_hex(input("  焦点强调色（荧光笔/概念/结尾卡）: "), "强调色")
                break
            except ValueError as e:
                print("  " + str(e))
        demo = theme.build_custom(primary, accent)
        print("  衍生预览（微信端 rgb，均自动计算）：")
        for k in ("GREEN", "GREEN_BG", "GREEN_DARK",
                  "ORANGE_ACCENT", "ORANGE_TEXT", "ORANGE_BG", "ORANGE_CARD_BG"):
            print(f"    {k:<15} {demo['colors'][k]}")
    else:
        t0 = theme.get_theme(tid)
        primary, accent = t0["hex"]["GREEN"], t0["hex"]["ORANGE_ACCENT"]

    # 3 渲染规范
    print("\n渲染规范（这些决定 md 语法长什么样）：")
    concept = _ask("==高亮== 标记怎么渲染？(highlight=橙色荧光笔 / bold=黑色加粗)",
                   default="highlight", valid=["highlight", "bold"])
    numbering = _ask("## 章节自动编号 01/02…？", default="on", valid=["on", "off"])
    end_sign = _ask("文末加签名块（署名+签名语）？", default="on", valid=["on", "off"])
    cover = _ask("正文没配封面图时自动生成同主题几何封面？", default="auto", valid=["auto", "manual"])

    return {
        "version": 1,
        "profile": name,
        "theme": tid,
        "colors": {"primary": primary, "accent": accent},
        "sign": {"name": name, "slogan": slogan},
        "author": author,
        "rules": {
            "concept_highlight": _on_off(concept),
            "chapter_numbering": _on_off(numbering),
            "end_sign": _on_off(end_sign),
        },
        "cover": {"auto_geo": cover == "auto"},
    }


def confirm_sheet(prof):
    """排版规范确认单：把主题色 + 确定性映射 + 微信红线摆给买家确认"""
    tid = prof["theme"]
    if tid == "custom":
        demo = theme.build_custom(prof["colors"]["primary"], prof["colors"]["accent"])
        head = f"自定义配色（结构主色 {demo['colors']['GREEN']} / 焦点强调 {demo['colors']['ORANGE_ACCENT']}）"
    else:
        t0 = theme.get_theme(tid)
        head = (f"{t0.get('name','')}（结构主色 {t0['colors']['GREEN']} / "
                f"焦点强调 {t0['colors']['ORANGE_ACCENT']}）")
    r = prof["rules"]
    concept = "主题焦点荧光笔（橙色系）" if r["concept_highlight"] else "黑色加粗（不用荧光笔）"
    numbering = "自动编号 01/02…" if r["chapter_numbering"] else "不编号（绿左竖条大标题）"
    end_sign = "开" if r["end_sign"] else "关"
    cover = "无封面时自动生成同主题几何封面" if prof["cover"]["auto_geo"] else "必须自己给封面（不给会报错）"
    L = [
        "══════ 你的排版规范确认单 ══════",
        f"账号 / 署名 : {prof['profile']}",
        f"签名语      : {prof['sign']['slogan'] or '（无）'}     文末签名块: {end_sign}",
        f"主题        : {head}",
        "── 使用规范（md → 微信组件，确定性映射，一字不改）──",
        "  # 标题        → 文章标题元信息（不进正文，防重复标题）",
        f"  ## 标题       → 章节头（{numbering}）",
        f"  ==高亮==      → {concept}（推荐给想让人看见的关键词/自创概念）",
        "  **加粗**      → 黑色加粗    > 引用 → 引用卡    - / 1. → 圆点/序号列表",
        "  ![图注](图)   → 正文插图（自动传微信图床 + 图注）   --- → 主题色分隔线",
        "── 微信红线（发布前自动拦截，你不用记）──",
        "  ✗ 禁 table/div 容器   ✗ 禁 hex 颜色（只用 rgb）   ✗ 禁 text-decoration 下划线",
        f"── 封面策略 ──",
        f"  {cover}",
        "════════════════════════════",
    ]
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="生成 wnp_profile.json（排版偏好确认）")
    ap.add_argument("--name", default=None, help="账号/署名")
    ap.add_argument("--slogan", default="", help="签名语（可空）")
    ap.add_argument("--theme", default=None, help="signature/mono/paper/custom")
    ap.add_argument("--primary", default=None, help="custom 时结构主色 #RRGGBB")
    ap.add_argument("--accent", default=None, help="custom 时焦点强调色 #RRGGBB")
    ap.add_argument("--concept", default="highlight", choices=["highlight", "bold"])
    ap.add_argument("--numbering", default="on", choices=["on", "off"])
    ap.add_argument("--end-sign", default="on", choices=["on", "off"])
    ap.add_argument("--cover", default="auto", choices=["auto", "manual"])
    ap.add_argument("--out", default="wnp_profile.json", help="输出路径")
    ap.add_argument("--yes", action="store_true", help="跳过确认直接保存")
    args = ap.parse_args()

    # 参数模式（给了 --theme 或 --name 即视为非交互）
    param_mode = bool(args.theme or args.name)
    if param_mode:
        tid = args.theme or "signature"
        if tid not in ("signature", "mono", "paper", "custom"):
            ap.error(f"--theme 需为 signature/mono/paper/custom，收到 {tid}")
        if tid == "custom":
            try:
                primary = _norm_hex(args.primary, "主色(--primary)")
                accent = _norm_hex(args.accent, "强调色(--accent)")
            except ValueError as e:
                ap.error(str(e))
        else:
            t0 = theme.get_theme(tid)
            primary, accent = t0["hex"]["GREEN"], t0["hex"]["ORANGE_ACCENT"]
        prof = {
            "version": 1,
            "profile": args.name or "我的账号",
            "theme": tid,
            "colors": {"primary": primary, "accent": accent},
            "sign": {"name": args.name or "我的账号", "slogan": args.slogan or ""},
            "author": args.name or "",
            "rules": {
                "concept_highlight": args.concept == "highlight",
                "chapter_numbering": args.numbering == "on",
                "end_sign": args.end_sign == "on",
            },
            "cover": {"auto_geo": args.cover == "auto"},
        }
    else:
        prof = interactive()

    print()
    print(confirm_sheet(prof))
    print()
    if not (args.yes or param_mode):
        ok = input("确认无误？(Y 保存 / N 取消): ").strip().lower()
        if ok not in ("y", "yes", ""):
            print("已取消，未写入任何文件。")
            return 1

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(prof, f, ensure_ascii=False, indent=2)
    print(f"\n[saved] {args.out}")
    print("之后推送/预览会自动套用这份规范：")
    print("  python push_draft.py --config config.json --md 文章.md  [自动读当前目录 wnp_profile.json]")
    print("  换别的规范文件：--profile /环境变量 WNP_PROFILE 指定。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
