# -*- coding: utf-8 -*-
"""
wechat-native-publisher 渲染器组件库
把「公众号可存活的微信原生富文本」封装成可组合的组件函数。

微信富文本存活要点（务必遵守，否则浏览器预览与微信端必然不一致）：
- 容器用 <section> —— 不能用 <table>（边框清不掉）/ <div>（背景色被清）
- 横排用 display:flex + align-items / justify-content
- 文本节点包 <span leaf="">，颜色/强调加在 span 上
- 颜色用 rgb() 格式，不要用 hex
- 图标用内联 <svg>（lucide 风格 stroke=currentColor），微信可保留
- 卡片浮起用 box-shadow: rgba(x,0,0,0.15) 0 2px 4px
"""
import html as _html_mod
import theme as TH

BODY_FONT = "'PingFang SC','Microsoft YaHei','Hiragino Sans GB','Source Han Serif SC','Noto Serif CJK SC',serif"


def _esc(value):
    """HTML 转义纯文本值（安全边界：文本类组件入口统一转义）。
    任何来自 md 标题 / frontmatter / profile 的字符串，在进入 HTML 前必须过这里。"""
    return _html_mod.escape(str(value), quote=False)


# ---- 微信原生基础节点 ----
def _sp(text, style=""):
    """微信文本节点：包 <span leaf="">，颜色/强调都加在这里。
    注意：_sp 接收的是已转义/受控的 HTML 片段；纯文本请先用 _esc()。"""
    return f'<span leaf="" style="box-sizing:border-box;{style}">{text}</span>'


def _sec(inner, style=""):
    """微信容器：<section>，背景/边框/圆角加在这里"""
    return f'<section style="box-sizing:border-box;{style}">{inner}</section>'


# ---- 三个 lucide 内联 SVG icon（参考稿原样提取，微信可保留） ----
ICON_LIKE = ('<svg fill="none" height="20" stroke="currentColor" stroke-width="1.8" '
             'viewbox="0 0 24 24" width="20"><path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"></path></svg>')
ICON_VIEW = ('<svg fill="none" height="20" stroke="currentColor" stroke-width="1.8" '
             'viewbox="0 0 24 24" width="20"><circle cx="12" cy="12" r="3"></circle><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11 8-11-8z"></path></svg>')
ICON_SHARE = ('<svg fill="none" height="20" stroke="currentColor" stroke-linecap="round" '
              'stroke-linejoin="round" stroke-width="1.8" viewbox="0 0 24 24" width="20">'
              '<path d="M4 18v-4a8 8 0 0 1 8-8h8"></path><polyline points="16 2 20 6 16 10"></polyline></svg>')


# ---- 正文文本组件 ----
def p(text):
    """普通段落 - 行距大、段距宽"""
    return f'<p style="box-sizing:border-box;margin:0 0 26px 0;font-size:16px;line-height:2.15;color:{TH.BODY};text-align:justify;">{_sp(text)}</p>'


def key(text):
    """重点词 - 绿色加粗 + 绿色下划线（微信可靠：用 border-bottom，不用 text-decoration）"""
    return f'<span leaf="" style="box-sizing:border-box;color:{TH.GREEN_DARK};font-weight:700;border-bottom:2px solid {TH.GREEN};padding-bottom:1px;">{text}</span>'


def strong(text):
    """普通加粗 - 黑色加粗"""
    return f'<strong style="box-sizing:border-box;color:{TH.BODY};font-weight:700;">{_sp(text)}</strong>'


def concept(text):
    """自创概念 - 橙色荧光笔底 + 深橙字（内容焦点）"""
    return f'<span leaf="" style="box-sizing:border-box;background:{TH.ORANGE_BG};color:{TH.ORANGE_TEXT};font-weight:700;padding:2px 4px;border-radius:3px;">{text}</span>'


def num_badge(n):
    """序号徽章 - 绿色圆形，绿底白字"""
    return (f'<span style="box-sizing:border-box;display:inline-block;width:26px;height:26px;'
            f'line-height:26px;text-align:center;background:{TH.GREEN};color:rgb(255,255,255);'
            f'border-radius:50%;font-size:14px;font-weight:700;vertical-align:middle;'
            f'margin-right:10px;">{_sp(n)}</span>')


def dot(text):
    """项目符号 - 绿色小圆点 + 文本"""
    d = (f'<span style="box-sizing:border-box;display:inline-block;width:7px;height:7px;'
         f'background:{TH.GREEN};border-radius:50%;margin-right:9px;vertical-align:middle;"></span>')
    return d + text


def quote_lead(text):
    """开篇引语 - 浅绿虚线圆角卡片"""
    return _sec(
        _sp(text, f"font-size:15px;line-height:2.0;color:{TH.GREEN_DARK};font-weight:600;text-align:center;"),
        f"background:{TH.GREEN_BG};border:1px dashed {TH.GREEN_BORDER};border-radius:10px;"
        f"padding:22px 26px;margin:0 0 40px 0;"
    )


def summary_box(headline, body_lines=None):
    """
    首屏摘要框 - 橙色为主的特殊框（对标稿"A小标+摘要"结构）
    橙色左边粗条 + 浅橙底 + 橙色边框 + 「摘要 READ FIRST」小标。
    headline 里的「重点概念」等词需自行用 concept() 高亮。
    """
    tag = (
        f'<section style="box-sizing:border-box;display:flex;align-items:center;'
        f'margin:0 0 16px 0;">'
        f'<span style="box-sizing:border-box;font-size:13px;font-weight:800;'
        f'color:{TH.ORANGE_TEXT};letter-spacing:3px;">{_sp("摘 要")}</span>'
        f'<section style="box-sizing:border-box;width:1.5px;height:13px;'
        f'background:{TH.ORANGE_ACCENT};margin:0 12px 0 14px;flex-shrink:0;"></section>'
        f'<span style="box-sizing:border-box;font-size:11px;color:{TH.GRAY};'
        f'letter-spacing:2px;font-weight:500;">{_sp("READ FIRST")}</span>'
        f'</section>'
    )
    head = (f'<section style="box-sizing:border-box;font-size:17px;font-weight:700;'
            f'color:{TH.BODY};line-height:1.8;">{headline}</section>')
    body = ""
    if body_lines:
        items = "".join(
            f'<section style="box-sizing:border-box;margin-top:12px;font-size:14.5px;'
            f'line-height:1.9;color:rgb(80,80,80);">{line}</section>'
            for line in body_lines
        )
        body = f'<section style="box-sizing:border-box;border-top:1px dashed {TH.ORANGE_CARD_BRD};margin-top:18px;padding-top:4px;">{items}</section>'
    return _sec(
        tag + head + body,
        f"background:{TH.ORANGE_CARD_BG};border:1px solid {TH.ORANGE_CARD_BRD};"
        f"border-left:5px solid {TH.ORANGE_ACCENT};border-radius:12px;"
        f"padding:26px 26px 24px 26px;margin:0 0 44px 0;"
    )


def h1(title):
    """主标题 - 大号粗体 + 绿色装饰条（title 为纯文本，内部转义）"""
    title_p = (f'<p style="box-sizing:border-box;margin:0 0 14px 0;font-size:26px;font-weight:700;'
               f'color:{TH.BODY};letter-spacing:0.5px;line-height:1.4;">{_sp(_esc(title))}</p>')
    bar = (f'<section style="box-sizing:border-box;width:52px;height:4px;background:{TH.GREEN};'
           f'border-radius:2px;margin:0 0 40px 0;"></section>')
    return title_p + bar


def part_header(num, en_label, cn_label):
    """
    对标稿章节头（flex 横排，微信可存活）：
      [ 01  ] │  你看不见的那个房间
      [ PART ]    ORIGIN
    左：绿色圆角方块数字徽章 + PART ｜ 竖线 ｜ 右侧加粗标题 + 英文小标
    """
    left = (
        f'<section style="box-sizing:border-box;flex-shrink:0;">'
        f'<section style="box-sizing:border-box;background:{TH.GREEN};color:rgb(255,255,255);'
        f'font-size:26px;font-weight:800;line-height:1;width:56px;height:56px;'
        f'display:flex;align-items:center;justify-content:center;border-radius:12px;'
        f'letter-spacing:-1px;">{_sp(num)}</section>'
        f'<p style="box-sizing:border-box;margin:9px 0 0 0;font-size:10px;font-weight:700;'
        f'color:{TH.GREEN_DARK};letter-spacing:4px;text-align:center;">{_sp("PART")}</p>'
        f'</section>'
    )
    bar = (f'<section style="box-sizing:border-box;width:1px;height:56px;background:{TH.GRAY_LT};'
           f'margin:0 22px;flex-shrink:0;"></section>')
    right = (
        f'<section style="box-sizing:border-box;flex:1;">'
        f'<p style="box-sizing:border-box;margin:0 0 6px 0;font-size:20px;font-weight:700;'
        f'color:{TH.BODY};line-height:1.4;">{_sp(cn_label)}</p>'
        f'<p style="box-sizing:border-box;margin:0;font-size:12px;letter-spacing:2px;'
        f'color:{TH.ORANGE_TEXT};font-weight:600;">{_sp(en_label)}</p>'
        f'</section>'
    )
    return (f'<section style="box-sizing:border-box;display:flex;align-items:center;'
            f'margin:56px 0 30px 0;">{left}{bar}{right}</section>')


def chapter_header(num, text):
    """通用章节头 - 编号方块 + 大标题（md 解析 ## 标题 用，自动编号；num/text 均转义）"""
    badge = (f'<section style="box-sizing:border-box;flex-shrink:0;background:{TH.GREEN};'
             f'color:rgb(255,255,255);font-size:17px;font-weight:800;line-height:1;'
             f'width:38px;height:38px;display:flex;align-items:center;justify-content:center;'
             f'border-radius:9px;">{_sp(_esc(num))}</section>')
    title = (f'<p style="box-sizing:border-box;margin:0 0 0 14px;flex:1;font-size:20px;'
             f'font-weight:700;color:{TH.BODY};line-height:1.5;">{_sp(_esc(text))}</p>')
    return (f'<section style="box-sizing:border-box;display:flex;align-items:center;'
            f'margin:44px 0 26px 0;">{badge}{title}</section>')


def section_title(text):
    """节内小标题 - 绿色左侧竖条 + 加粗黑字（text 为纯文本，内部转义）"""
    return (f'<p style="box-sizing:border-box;margin:36px 0 18px 0;font-size:18px;font-weight:700;'
            f'color:{TH.BODY};line-height:1.5;border-left:4px solid {TH.GREEN};'
            f'padding-left:12px;">{_sp(_esc(text))}</p>')


def summary_title(text, en_label, cn_label):
    """
    写在最后标题 - flex 横排：/// ｜ 竖线 ｜ 标题 + 中英小标
    竖线紧跟标题左侧（用户要求"写在最后紧跟竖杠后面"）。
    text/en_label/cn_label 均为纯文本，内部转义。
    """
    slash = (f'<span style="box-sizing:border-box;font-size:24px;font-weight:800;'
             f'color:{TH.GREEN};letter-spacing:-2px;line-height:1;">{_sp("///")}</span>')
    bar = (f'<section style="box-sizing:border-box;width:1px;height:30px;background:{TH.GREEN};'
           f'margin:0 16px 0 18px;flex-shrink:0;"></section>')
    title_block = (
        f'<section style="box-sizing:border-box;flex:1;">'
        f'<p style="box-sizing:border-box;margin:0;font-size:20px;font-weight:700;'
        f'color:{TH.BODY};line-height:1.4;">{_sp(_esc(text))}</p>'
        f'<p style="box-sizing:border-box;margin:2px 0 0 0;font-size:12px;letter-spacing:2px;'
        f'color:{TH.ORANGE_TEXT};font-weight:600;">{_sp(_esc(en_label) + " · " + _esc(cn_label))}</p>'
        f'</section>'
    )
    return (f'<section style="box-sizing:border-box;display:flex;align-items:center;'
            f'margin:44px 0 20px 0;">{slash}{bar}{title_block}</section>')


def quote_card(text):
    """引用句卡片 - 浅绿底 + 绿色左边条 + 圆角"""
    return _sec(
        _sp(text, f"font-size:15px;line-height:2.0;color:{TH.BODY};"),
        f"background:{TH.GREEN_BG};border:1px solid {TH.GREEN_BORDER};"
        f"border-left:4px solid {TH.GREEN};border-radius:10px;"
        f"padding:20px 24px;margin:10px 0 32px 0;"
    )


def img(url, caption_text="", alt="插图"):
    """正文插图 - 微信素材库图 URL，宽度 100% 居中 + 圆角（可选图注）"""
    tag = (
        f'<section style="box-sizing:border-box;text-align:center;margin:16px 0 22px 0;">'
        f'<img src="{url}" style="box-sizing:border-box;width:100%;max-width:677px;'
        f'border-radius:10px;display:block;margin:0 auto;" alt="{alt}" />'
        f'</section>'
    )
    if caption_text:
        tag += caption(caption_text)
    return tag


def caption(text):
    """图注 - 居中绿色小字：— caption（text 为纯文本，内部转义）"""
    return (f'<p style="box-sizing:border-box;font-size:13px;line-height:1.8;color:{TH.GREEN_DARK};'
            f'text-align:center;margin:10px 0 38px 0;letter-spacing:0.5px;font-weight:500;">'
            f'{_sp("— " + _esc(text))}</p>')


def hr_dashed():
    """分隔线 - 绿色虚线"""
    return (f'<section style="box-sizing:border-box;border:0;border-top:1px dashed {TH.GREEN};'
            f'height:1px;margin:48px 0 28px 0;"></section>')


def signature(name="你的名字", slogan="", pre=""):
    """签名行 - 居中，主绿。name/slogan 为纯文本（可来自 profile/frontmatter），内部转义。"""
    slogan_line = ""
    if slogan:
        slogan_line = (f'<p style="box-sizing:border-box;margin:0 0 12px 0;font-size:15px;'
                       f'font-weight:500;color:{TH.GRAY};text-align:center;">{_sp(_esc(slogan))}</p>')
    return (
        f'<p style="box-sizing:border-box;margin:38px 0 6px 0;font-size:18px;font-weight:700;'
        f'color:{TH.GREEN};line-height:1.5;text-align:center;">{_sp(_esc(name))}</p>'
        f'{slogan_line}'
    )


def _icon_item(icon_svg, label):
    """结尾卡片里单个 icon + label，纵向排列（参考稿结构）"""
    return (
        f'<section style="box-sizing:border-box;display:flex;flex-direction:column;'
        f'align-items:center;width:88px;color:{TH.ORANGE_TEXT};">'
        f'<section style="box-sizing:border-box;width:44px;height:44px;display:flex;'
        f'align-items:center;justify-content:center;background:{TH.ORANGE_BG};'
        f'border-radius:12px;box-shadow:{TH.ORANGE_SHADOW} 0px 2px 4px;'
        f'border:1px solid {TH.ORANGE_ACCENT};">{icon_svg}</section>'
        f'<span leaf="" style="box-sizing:border-box;font-size:11px;font-weight:600;color:{TH.FOOT};'
        f'margin-top:6px;">{label}</span>'
        f'</section>'
    )


def end_card(line_before="如果这篇文章让你有所收获，<br>欢迎转发给",
             highlight="有需要的朋友",
             line_after="。"):
    """结尾卡片 - 橙色系圆角卡片 + 三个 SVG icon（赞/看/转）+ THANKS"""
    txt = (f'<section style="box-sizing:border-box;color:{TH.BODY};font-size:15px;'
           f'line-height:1.9;font-weight:600;text-align:center;padding:0 12px;">'
           f'{_sp(line_before)}'
           f'<span leaf="" style="box-sizing:border-box;background:{TH.ORANGE_BG};color:{TH.ORANGE_TEXT};'
           f'font-weight:700;padding:2px 4px;border-radius:3px;">{highlight}</span>'
           f'{_sp(line_after)}'
           f'</section>')
    icons = (f'<section style="box-sizing:border-box;display:flex;justify-content:center;'
             f'align-items:flex-start;margin-top:26px;">'
             f'{_icon_item(ICON_LIKE, "点赞")}{_icon_item(ICON_VIEW, "在看")}{_icon_item(ICON_SHARE, "转发")}'
             f'</section>')
    thanks = (f'<section style="box-sizing:border-box;font-size:11px;color:{TH.ORANGE_TEXT};'
              f'letter-spacing:4px;text-align:center;margin-top:24px;font-family:{BODY_FONT};">'
              f'{_sp("THANKS FOR READING")}</section>')
    return _sec(txt + icons + thanks,
                f"background:{TH.ORANGE_CARD_BG};border:1px solid {TH.ORANGE_CARD_BRD};"
                f"border-radius:14px;padding:30px 22px;margin:20px 0 10px 0;")
