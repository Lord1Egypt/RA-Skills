# -*- coding: utf-8 -*-
"""
wechat-native-publisher 发布前自检（pre-push validation）

对标社区技能 wechat-official-account-typesetting-master 的 report 思路，
并结合本 skill 逆向得到的微信白名单知识做了本地化增强：

- BLOCK 级：微信端必然渲染失败/被清洗的结构 → 默认拦截推送
- CHECK 级：视觉或体验风险 → 打印警告，可继续推送

用法：
  1) 独立自检已有 HTML 文件：
       python validate.py --file <xxx.html>
  2) 自检文章模块（组装正文后检查，不推送）：
       python validate.py --build examples.article
  3) 推送前自动自检（push_draft.py --validate 触发，BLOCK 默认中止）

检查项一览：
  [B1] 高危标签 script/iframe/video/audio/form
  [B2] hex 颜色（微信富文本会清洗 hex，必须 rgb()）
  [B3] text-decoration（微信洗掉，下划线必须用 border-bottom）
  [B4] <table>（微信清边框不可控，本 skill 禁用于正文）
  [B5] 图片 src 缺失或本地相对路径（微信端不可达）
  [B6] position:fixed/absolute / animation / @media
  [C1] <div> 容器（背景色可能被清，应改 <section>）
  [C2] 重点标记过密（font-weight:700 次数 / 正文字数）
  [C3] 超长叶级段落（手机端超过 ~300 字建议拆段/加小标）
  [C4] 图片无 alt / 空 src
"""
import os, re, sys, json, importlib, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, SKILL_ROOT)

# ---- 基础工具 ----

def strip_tags(html_frag):
    """去掉标签与注释，返回纯文本（保留 &nbsp; 转为空格）"""
    t = re.sub(r"<!--.*?-->", "", html_frag, flags=re.S)
    t = re.sub(r"<[^>]+>", "", t)
    t = t.replace("&nbsp;", " ").replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    return t


def count_text_len(html_frag):
    return len(re.sub(r"\s+", "", strip_tags(html_frag)))


# ---- 单项检查 ----
# 每条返回 (code, level, message) 或 None

def ck_highrisk_tags(html):
    for tag in ["script", "iframe", "video", "audio", "form", "object", "embed"]:
        if re.search(rf"<{tag}\b", html, re.I):
            return ("B1", "BLOCK", f"检测到高危标签 <{tag}>：微信端会被剥离或产生不可控行为。")

def ck_hex_color(html):
    m = re.search(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b", html)
    if m:
        return ("B2", "BLOCK", f"检测到 hex 颜色 {m.group(0)}：微信富文本会清洗 hex，必须改用 rgb()（见 theme.py）。")

def ck_text_decoration(html):
    if re.search(r"text-decoration\s*:", html, re.I):
        return ("B3", "BLOCK", "检测到 text-decoration：微信端会被清洗。下划线必须用 border-bottom 实现。")

def ck_table(html):
    if re.search(r"<table\b", html, re.I):
        return ("B4", "BLOCK", "检测到 <table>：微信端边框清洗不可控。本 skill 正文用 <section>+flex 组件，请勿使用表格布局。")

def ck_images(html):
    imgs = re.findall(r"<img\b[^>]*>", html, re.I)
    issues = []
    for i, tag in enumerate(imgs, 1):
        src_m = re.search(r'src="([^"]*)"', tag)
        if not src_m or not src_m.group(1).strip():
            issues.append(("B5", "BLOCK", f"第 {i} 张 <img> 缺少 src。"))
            continue
        src = src_m.group(1).strip()
        src = re.sub(r"[\x00-\x1f\x7f]+", "", src)
        low = src.lower()
        # 白名单：http(s) / 微信CDN / 仅图片的 data:image/*;base64。
        # 不放行裸 //（协议相对）与任意 data:（防 data:text/html 注入）。
        ok = (low.startswith(("http://", "https://"))
              or low.startswith("mmbiz")
              or bool(re.match(r"^data:image/[a-z0-9.+\-]+;base64,", low, re.I)))
        if not ok:
            issues.append(("B5", "BLOCK", f"第 {i} 张图片 src 不是合法 http(s)/微信CDN/图片data URI，微信端不可达：{src[:60]}"))
        if "alt=" not in tag:
            issues.append(("C4", "CHECK", f"第 {i} 张 <img> 缺少 alt 属性。"))
    return issues

def ck_position_anim(html):
    if re.search(r"position\s*:\s*(?:fixed|absolute)|animation\s*:|@media", html, re.I):
        return ("B6", "BLOCK", "检测到 position:fixed/absolute、animation 或 @media：微信端不稳定，请移除。")

def ck_div(html):
    if re.search(r"<div\b", html, re.I):
        return ("C1", "CHECK", "检测到 <div> 容器：背景色/圆角在微信端可能被清洗，建议统一用 <section>（renderer 已封装）。")

def ck_emphasis_density(html):
    """
    重点标记密度：只统计真正的『内容重点』——key() 的绿色下划线
    (border-bottom) 与 concept() 的橙荧光笔底。标题/徽章/引用的
    font-weight:700 属结构加粗，不算重点泛滥。
    """
    text_len = count_text_len(html)
    key_n = len(re.findall(r"border-bottom:\s*2px\s+solid", html))
    concept_n = len(re.findall(r"background:\s*rgb\(255,\s*236,\s*227\)", html))
    total = key_n + concept_n
    if text_len > 0 and total > 0:
        density = total / (text_len / 100)
        if total >= 45 or density > 3.0:
            return ("C2", "CHECK",
                    f"重点标记较密：重点词(key) {key_n} 处 + 概念高亮(concept) {concept_n} 处，"
                    f"共 {total} 处 / 正文约 {text_len} 字（约每百字 {density:.1f} 处）。"
                    f"若满屏都是重点=没有重点，建议删减 1/3。")

def ck_long_paragraph(html):
    """找不含子 section 的『叶级』section 块，统计其文本长度"""
    long_ones = []
    for m in re.finditer(r"<section\b[^>]*>(.*?)</section>", html, flags=re.S):
        frag = m.group(1)
        if "<section" not in frag:  # 叶级
            n = count_text_len(frag)
            if n > 300:
                long_ones.append(n)
    if long_ones:
        return ("C3", "CHECK", f"检测到 {len(long_ones)} 个超长段落（最长约 {max(long_ones)} 字），手机端建议拆段或加小标题。")

# ---- 汇总 ----

CHECKS = [
    ck_highrisk_tags, ck_hex_color, ck_text_decoration, ck_table,
    ck_images, ck_position_anim, ck_div, ck_emphasis_density,
    ck_long_paragraph,
]


def validate_content(html):
    """
    输入正文 HTML，返回 {risk, issues, stats}

    注意：make_preview.py 生成的完整预览页会带 <style> 预览壳（hex 颜色、
    <div> 布局等只给本地浏览器用，不会推送微信）。因此先剥离 <style> 块，
    只对『会进微信正文』的部分做检查。
    """
    stripped = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.S | re.I)
    issues = []
    for fn in CHECKS:
        try:
            res = fn(stripped)
        except Exception as e:  # noqa
            issues.append(("ERR", "CHECK", f"检查 {fn.__name__} 执行出错：{e}"))
            continue
        if isinstance(res, list):
            issues.extend(res)
        elif res:
            issues.append(res)
    blocks = [i for i in issues if i[1] == "BLOCK"]
    risk = "BLOCK" if blocks else ("CHECK" if issues else "PASS")
    stats = {
        "characters": count_text_len(stripped),
        "key": len(re.findall(r"border-bottom:\s*2px\s+solid", stripped)),
        "concept": len(re.findall(r"background:\s*rgb\(255,\s*236,\s*227\)", stripped)),
        "images": len(re.findall(r"<img\b", stripped, re.I)),
        "sections": len(re.findall(r"<section\b", stripped, re.I)),
    }
    return {"risk": risk, "issues": issues, "stats": stats}


def print_report(report, indent="  "):
    print(f"{indent}risk: {report['risk']}")
    if report["issues"]:
        for code, level, msg in report["issues"]:
            print(f"{indent}[{level}] ({code}) {msg}")
    st = report["stats"]
    print(f"{indent}stats: 正文{st['characters']}字 | key x{st['key']} | concept x{st['concept']} | img x{st['images']} | section x{st['sections']}")


def main():
    ap = argparse.ArgumentParser(description="公众号排版发布前自检")
    ap.add_argument("--file", default=None, help="自检已有 HTML 文件")
    ap.add_argument("--build", default=None, help="自检文章模块（组装正文后检查）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args()

    html = None
    if args.file:
        html = open(args.file, encoding="utf-8").read()
    elif args.build:
        mod = importlib.import_module(args.build)
        html = mod.build_content({})
    else:
        ap.error("需要 --file 或 --build")

    report = validate_content(html)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"validate: {args.file or args.build}")
        print_report(report)
    return 0 if report["risk"] != "BLOCK" else 2


if __name__ == "__main__":
    raise SystemExit(main())
