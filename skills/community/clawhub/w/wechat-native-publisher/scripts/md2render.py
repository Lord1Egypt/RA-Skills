# -*- coding: utf-8 -*-
"""
md2render — md/txt → 微信组件 HTML 的确定性解析器（v1）

原则：一字不改。只做结构映射，不做语义改写、不增删内容。

输入格式（md 子集，均按微信可存活结构渲染）：
  ---            frontmatter（可选）：title / cover / author / digest
  # 标题         文章主标题：第一个 # 作为标题元信息（不进正文，防重复标题）
  ## 标题        章节头（自动编号 01/02…，renderer.chapter_header）
  ### 标题       节内小标题（renderer.section_title）
  > 引用         引用卡片（renderer.quote_card，连续多行合并）
  **加粗**       普通强调（renderer.strong，黑粗）
  ==高亮==       荧光笔高亮（renderer.concept，主题焦点色底）★ 推荐标记
  *斜体*         斜体
  `行内码`       行内等宽灰底
  ```语言        代码块（主题浅底等宽圆角）
  - 无序项       绿点列表
  1. 有序项      序号圆徽章列表
  --- 分隔线      主题色虚线与细线
  ![图注](本地路径或URL)   正文插图（单独一行；上传后自动换真实图床 URL）
  空行分段       普通段落

输出：{"title","author","digest","cover","chars","html","images":[{token,src,alt}]}
  html 中图片 src 为占位 token（__WXIMG_0__…），由推送侧上传后替换。
"""
import argparse
import html
import json
import os
import re
import sys

# 必须先 apply_theme 再渲染（theme 槽位动态读取，见 theme.py 说明）。
# 注意：本模块 import 时【不】apply 任何主题——renderer 已改为 TH.xxx 动态访问，
# 换肤由调用方（push_draft/make_preview/profile.resolve）唯一决定，避免覆盖调用方已换的主题。
DEFAULT_THEME = os.environ.get("WNP_THEME", "signature")
import theme  # noqa: E402
import renderer as R  # noqa: E402
import theme as TH  # noqa: E402  (属性访问取动态色)

# ---- 行模式 ----
_RE_FENCE = re.compile(r"^```")
_RE_ATX1 = re.compile(r"^#\s+(.*)$")
_RE_ATX2 = re.compile(r"^##\s+(.*)$")
_RE_ATX3 = re.compile(r"^###\s+(.*)$")
_RE_ATX4 = re.compile(r"^#{4,}\s+(.*)$")
_RE_QUOTE = re.compile(r"^>\s?(.*)$")
_RE_UL = re.compile(r"^[-*+]\s+(.*)$")
_RE_OL = re.compile(r"^(\d+)[.、]\s+(.*)$")
_RE_HR = re.compile(r"^([-*_])\s*\1\s*\1\s*$")
_RE_IMG = re.compile(r"^!\[([^\]]*)\]\((\S+)\)\s*$")
_FM_START = re.compile(r"^---\s*$")
_FM_KEY = re.compile(r"^([A-Za-z_]+)\s*:\s*(.*)$")

_INLINE = re.compile(r"(==.+?==|\*\*.+?\*\*|`[^`]+`|\*[^*\s][^*]*\*)")

CODE_FONT = "'SF Mono',Consolas,'Courier New',monospace"

# 渲染规则（买家 wnp_profile.json 可调；parse 每次调用时按 rules 覆盖）
_RULES = {"concept_highlight": True, "chapter_numbering": True}


def _esc(t):
    return html.escape(t, quote=False)


def _sp(text, style=""):
    return f'<span leaf="" style="box-sizing:border-box;{style}">{text}</span>'


def _sec(inner, style=""):
    return f'<section style="box-sizing:border-box;{style}">{inner}</section>'


def _code_inline(text):
    return (f'<code style="box-sizing:border-box;background:{TH.GREEN_BG};'
            f'color:{TH.GREEN_DARK};font-family:{CODE_FONT};font-size:13px;'
            f'border-radius:4px;padding:1px 5px;">{_esc(text)}</code>')


def _em(text):
    return (f'<span leaf="" style="box-sizing:border-box;font-style:italic;'
            f'color:{TH.BODY};">{_esc(text)}</span>')


def _inline(text):
    """行内标记解析：==高亮== → concept，**加粗** → strong，`code` → 等宽，*斜体* → 斜体"""
    parts = _INLINE.split(text)
    out = []
    for part in parts:
        if not part:
            continue
        if part.startswith("==") and part.endswith("==") and len(part) > 4:
            body = _esc(part[2:-2])
            out.append(R.concept(body) if _RULES["concept_highlight"] else R.strong(body))
        elif part.startswith("**") and part.endswith("**") and len(part) > 4:
            out.append(R.strong(_esc(part[2:-2])))
        elif part.startswith("`") and part.endswith("`") and len(part) > 2:
            out.append(_code_inline(part[1:-1]))
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            out.append(_em(part[1:-1]))
        else:
            out.append(_sp(_esc(part)))
    return "".join(out)


def _para(text):
    return (f'<p style="box-sizing:border-box;margin:0 0 26px 0;font-size:16px;'
            f'line-height:2.15;color:{TH.BODY};text-align:justify;">{_inline(text)}</p>')


def _bullet(text):
    d = (f'<span style="box-sizing:border-box;display:inline-block;width:7px;height:7px;'
         f'background:{TH.GREEN};border-radius:50%;margin-right:11px;'
         f'vertical-align:middle;flex-shrink:0;"></span>')
    body = _inline(text)
    return (f'<section style="box-sizing:border-box;display:flex;align-items:center;'
            f'margin:0 0 12px 0;font-size:16px;line-height:2.0;color:{TH.BODY};">'
            f'{d}'
            f'<span leaf="" style="box-sizing:border-box;flex:1;">{body}</span></section>')


def _ordered(n, text):
    badge = (f'<span style="box-sizing:border-box;display:inline-block;width:24px;height:24px;'
             f'line-height:24px;text-align:center;background:{TH.GREEN};color:rgb(255,255,255);'
             f'border-radius:50%;font-size:13px;font-weight:700;vertical-align:middle;'
             f'margin-right:10px;flex-shrink:0;">{_esc(str(n))}</span>')
    return (f'<section style="box-sizing:border-box;display:flex;align-items:center;'
            f'margin:0 0 12px 0;font-size:16px;line-height:2.0;color:{TH.BODY};">'
            f'{badge}'
            f'<span leaf="" style="box-sizing:border-box;flex:1;">{_inline(text)}</span></section>')


def _quote(blocks):
    body = "<br>".join(_inline(b) if b else _sp("") for b in blocks)
    return _sec(
        body,
        f"background:{TH.GREEN_BG};border:1px solid {TH.GREEN_BORDER};"
        f"border-left:4px solid {TH.GREEN};border-radius:10px;"
        f"padding:18px 22px;margin:10px 0 30px 0;font-size:15px;line-height:2.0;color:{TH.BODY};"
    )


def _code_block(lines, lang=""):
    code = _esc("\n".join(lines))
    head = ""
    if lang:
        head = (f'<p style="box-sizing:border-box;margin:0 0 10px 0;font-size:11px;'
                f'color:{TH.FOOT};letter-spacing:1px;font-family:{CODE_FONT};">{_esc(lang)}</p>')
    return _sec(
        head + code,
        f"background:{TH.GREEN_BG};border-radius:10px;padding:16px 18px;margin:6px 0 28px 0;"
        f"font-family:{CODE_FONT};font-size:13px;line-height:1.8;color:{TH.BODY};"
        f"white-space:pre-wrap;word-break:break-all;"
    )


def _img_block(token, alt):
    tag = (f'<section style="box-sizing:border-box;text-align:center;margin:18px 0 8px 0;">'
           f'<img src="{token}" style="box-sizing:border-box;width:100%;max-width:677px;'
           f'border-radius:10px;display:block;margin:0 auto;" alt="{_esc(alt) or "插图"}" /></section>')
    if alt:
        tag += (f'<p style="box-sizing:border-box;font-size:13px;line-height:1.8;'
                f'color:{TH.GREEN_DARK};text-align:center;margin:0 0 34px 0;'
                f'letter-spacing:0.5px;font-weight:500;">{_sp("— " + _esc(alt))}</p>')
    return tag


def _hr():
    return (f'<section style="box-sizing:border-box;border:0;border-top:1px dashed {TH.GREEN};'
            f'height:1px;margin:44px 0 30px 0;"></section>')


def _clean(text):
    return text.replace("\r\n", "\n").replace("\r", "\n").strip("\n")


def parse(text, title=None, cover=None, rules=None):
    """
    解析 md/txt → dict。确定性映射，一字不改。
    txt 视为无标记纯文本（全段落），title/cover 需外部给。
    rules：可选 dict，键 concept_highlight / chapter_numbering（True/False）。
    """
    # 每次 parse 独立：先复位默认（全开），本次 rules 再覆盖，避免跨调用污染。
    _RULES.update({"concept_highlight": True, "chapter_numbering": True})
    if rules:
        _RULES.update({k: bool(v) for k, v in rules.items() if k in _RULES})
    text = _clean(text)
    empty = {"title": title or "", "author": "", "digest": "", "cover": cover or "",
             "chars": 0, "html": "", "images": [], "sign_rendered": False}
    if not text:
        return empty

    lines = text.split("\n")

    # ---- frontmatter（仅当第一行是 ---） ----
    # 键：title/cover/author/digest + sign_name/sign_slogan（文末品牌签名，缺省不渲染）
    meta = {"title": title or "", "cover": cover or "", "author": "", "digest": "",
            "sign_name": "", "sign_slogan": ""}
    if _FM_START.match(lines[0].strip()):
        i = 1
        while i < len(lines) and not _FM_START.match(lines[i].strip()):
            m = _FM_KEY.match(lines[i].strip())
            if m and m.group(1).lower() in meta:
                meta[m.group(1).lower()] = m.group(2).strip().strip('"\'')
            i += 1
        lines = lines[i + 1:] if i < len(lines) else []

    # ---- 块级扫描 ----
    blocks = []          # (kind, payload)
    i, nline = 0, len(lines)
    images, img_idx = [], 0
    title_from_h1, seen_h1 = None, False
    # 首个非空内容行是否为 #（跳过 frontmatter 后可能残留的空行）
    _k = 0
    while _k < len(lines) and not lines[_k].strip():
        _k += 1
    first_content_is_h1 = _k < len(lines) and bool(_RE_ATX1.match(lines[_k].strip()))

    def push_img(src, alt):
        nonlocal img_idx
        token = f"__WXIMG_{img_idx}__"
        images.append({"token": token, "src": src, "alt": alt})
        img_idx += 1
        return token

    def cur_line(idx):
        return lines[idx] if 0 <= idx < nline else ""

    while i < nline:
        line = lines[i].strip()
        i += 1
        if not line:
            continue

        # 图片（单独一行）
        m = _RE_IMG.match(line)
        if m:
            blocks.append(("img", push_img(m.group(2), m.group(1))))
            continue

        # 代码块
        if _RE_FENCE.match(line):
            lang = line[3:].strip()
            buf = []
            while i < nline and not _RE_FENCE.match(cur_line(i).strip()):
                buf.append(lines[i])
                i += 1
            if i < nline:
                i += 1
            while buf and not buf[0].strip():
                buf.pop(0)
            while buf and not buf[-1].strip():
                buf.pop()
            blocks.append(("cb", (lang, buf)))
            continue

        # ATX 标题
        m = _RE_ATX1.match(line)
        if m:
            t = m.group(1).strip()
            if not seen_h1 and first_content_is_h1 and title_from_h1 is None:
                title_from_h1 = t   # 首个 # = 标题元信息，不进正文
                seen_h1 = True
            else:
                blocks.append(("h1", t))
            continue
        m = _RE_ATX2.match(line)
        if m:
            blocks.append(("ch", m.group(1).strip()))
            continue
        m = _RE_ATX3.match(line)
        if m:
            blocks.append(("st", m.group(1).strip()))
            continue
        m = _RE_ATX4.match(line)
        if m:
            blocks.append(("st", m.group(1).strip()))
            continue

        # 分隔线
        if _RE_HR.match(line):
            blocks.append(("hr", None))
            continue

        # 引用（连续行）
        if _RE_QUOTE.match(line):
            buf = [_RE_QUOTE.match(line).group(1)]
            while i < nline:
                qm = _RE_QUOTE.match(cur_line(i))
                if qm:
                    buf.append(qm.group(1))
                    i += 1
                else:
                    break
            blocks.append(("qt", buf))
            continue

        # 无序列表（连续项）
        if _RE_UL.match(line):
            buf = []
            j = i - 1
            while j < nline:
                um = _RE_UL.match(cur_line(j))
                if um:
                    buf.append(um.group(1))
                    j += 1
                else:
                    break
            i = j
            blocks.append(("ul", buf))
            continue

        # 有序列表（连续项）
        if _RE_OL.match(line):
            buf = []
            j = i - 1
            while j < nline:
                om = _RE_OL.match(cur_line(j))
                if om:
                    buf.append((int(om.group(1)), om.group(2)))
                    j += 1
                else:
                    break
            i = j
            blocks.append(("ol", buf))
            continue

        # 普通段落：收集到空行 / 块级起始
        para = [line]
        while i < nline:
            ns = cur_line(i).strip()
            if not ns:
                break
            if (_RE_ATX1.match(ns) or _RE_ATX2.match(ns) or _RE_ATX3.match(ns)
                    or _RE_HR.match(ns) or _RE_IMG.match(ns) or _RE_FENCE.match(ns)
                    or _RE_UL.match(ns) or _RE_OL.match(ns) or _RE_QUOTE.match(ns)):
                break
            para.append(ns)
            i += 1
        blocks.append(("p", " ".join(para)))

    # ---- 渲染 ----
    parts = []
    ch_n, img_cursor = 0, 0
    for kind, payload in blocks:
        if kind == "h1":
            parts.append(R.h1(payload))
        elif kind == "ch":
            if _RULES["chapter_numbering"]:
                ch_n += 1
                parts.append(R.chapter_header(f"{ch_n:02d}", payload))
            else:
                # 无编号章节：绿左竖条大标题（买家不想要 01/02 时）
                parts.append(
                    f'<p style="box-sizing:border-box;margin:44px 0 26px 0;font-size:20px;'
                    f'font-weight:700;color:{TH.BODY};line-height:1.5;'
                    f'border-left:4px solid {TH.GREEN};padding-left:14px;">{_sp(_esc(payload))}</p>')
        elif kind == "st":
            parts.append(R.section_title(payload))
        elif kind == "p":
            parts.append(_para(payload))
        elif kind == "ul":
            for it in payload:
                parts.append(_bullet(it))
        elif kind == "ol":
            for n, it in payload:
                parts.append(_ordered(n, it))
        elif kind == "qt":
            parts.append(_quote(payload))
        elif kind == "cb":
            parts.append(_code_block(payload[1], payload[0]))
        elif kind == "img":
            img = images[img_cursor]
            img_cursor += 1
            parts.append(_img_block(img["token"], img["alt"]))
        elif kind == "hr":
            parts.append(_hr())

    # frontmatter 声明了签名才追加（品牌位由内容作者自己控制，保持一字不改）
    if meta.get("sign_name"):
        parts.append(R.signature(name=meta["sign_name"], slogan=meta.get("sign_slogan", "")))

    body_html = "".join(parts)
    plain = re.sub(r"<[^>]+>", "", body_html).replace("\n", "")
    return {
        "title": meta["title"] or title_from_h1 or title or "",
        "author": meta["author"] or "",
        "digest": meta["digest"] or "",
        "cover": meta["cover"] or cover or "",
        "chars": len(plain),
        "html": body_html,
        "images": images,
        "sign_rendered": bool(meta.get("sign_name")),
    }


def main():
    ap = argparse.ArgumentParser(description="md/txt → 微信组件 HTML")
    ap.add_argument("--file", required=True, help="输入 .md/.txt")
    ap.add_argument("--title", default=None, help="标题（缺省取 frontmatter/首个 #）")
    ap.add_argument("--cover", default=None, help="封面路径/URL（缺省取 frontmatter）")
    ap.add_argument("--theme", default=DEFAULT_THEME, help="主题 id")
    ap.add_argument("--out", default=None, help="输出 HTML 文件")
    args = ap.parse_args()

    if args.theme:
        theme.apply_theme(args.theme)
    with open(args.file, encoding="utf-8") as f:
        text = f.read()
    res = parse(text, title=args.title, cover=args.cover)
    summary = {k: v for k, v in res.items() if k != "html"}
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(res["html"])
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        print(f"html -> {args.out} ({len(res['html'])} chars)")
    else:
        print(json.dumps(summary, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
