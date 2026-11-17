# -*- coding: utf-8 -*-
"""
wechat-native-publisher 本地预览生成
把 build_content() / md 解析出的微信正文 / 已排好版的HTML 包成完整 HTML，
用 base64 内嵌本地插图，方便不回公众号后台快速审稿。预览与微信端渲染结构一致。

用法：
python make_preview.py --md 文章.md --theme paper --out preview.html
python make_preview.py --html 已排版.html --out preview.html
python make_preview.py --build examples.article --out preview.html
python make_preview.py --md 文章.md --profile wnp_profile.json --out preview.html
  （--profile：套用买家排版规范，预览与推送完全一致；--theme 可覆盖 profile 主题）
"""
import os, sys, base64, argparse, importlib, re

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)         # renderer/theme/profile/md2render
sys.path.insert(0, SKILL_ROOT)   # examples

# 安全常量
_MAX_IMAGE_BYTES = 20 * 1024 * 1024  # 单张图片最大 20MB
_ALLOWED_IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"}

# HTML消毒：危险标签黑名单（会被完全移除，包括内容）
_DANGEROUS_TAGS = (
    "script", "iframe", "object", "embed", "form", "input", "button",
    "select", "textarea", "link", "meta", "base", "frame", "frameset",
    "noscript", "canvas", "svg", "math", "template", "slot"
)

# HTML消毒：危险属性前缀黑名单（会被移除）
_DANGEROUS_ATTR_PREFIXES = ("on", "formaction", "form", "xlink:href")


def _sanitize_html(html_content):
    """消毒HTML内容，防止活动内容注入（XSS）
    - 移除script/iframe/object等危险标签及其内容
    - 移除on*事件属性
    - 对所有 URL 属性做 scheme 白名单校验（http/https；data: 仅允许 img 的
      data:image/*;base64），javascript:/vbscript:/data:text/html 等一律清空。
      属性值先 html.unescape + 剥离控制字符，防止 &#106;avascript: 等编码绕过。
    - 移除 style 中的 expression() / behavior / url(javascript:)
    """
    import html as html_mod
    from urllib.parse import urlsplit

    # 1. 移除危险标签及其内容（非贪婪匹配，支持跨行）
    for tag in _DANGEROUS_TAGS:
        pattern = rf'<{tag}\b[^>]*>.*?</{tag}\s*>'
        html_content = re.sub(pattern, "", html_content, flags=re.S | re.I)
        pattern_self = rf'<{tag}\b[^>]*/?>'
        html_content = re.sub(pattern_self, "", html_content, flags=re.I)

    # 2. 移除危险属性（on*事件处理器等）
    for prefix in _DANGEROUS_ATTR_PREFIXES:
        pattern = rf'\s+{prefix}[a-zA-Z]*\s*=\s*("[^"]*"|\'[^\']*\'|[^\s>]+)'
        html_content = re.sub(pattern, "", html_content, flags=re.I)

    # 3. URL 属性强校验：统一处理 href/src/action/formaction/xlink:href/poster/background
    #    先解码 HTML 实体 + 去除控制字符，再按 scheme 白名单判定，危险值清空属性。
    def _fix_url(m):
        attr = m.group(1)
        token = m.group(2)
        if token[:1] in ("\"", "'"):
            quote = token[:1]
            raw = token[1:-1]
        else:
            quote = "\""
            raw = token
        val = re.sub(r"[\x00-\x1f\x7f]+", "", html_mod.unescape(raw)).strip()
        low = val.lower()
        scheme_m = re.match(r"^([a-z][a-z0-9+.\-]*):", low)
        if scheme_m:
            scheme = scheme_m.group(1)
            if scheme in ("http", "https"):
                return f'{attr}={quote}{html_mod.escape(val, quote=True)}{quote}'
            if (scheme == "data" and attr.lower() == "src"
                    and re.match(r"^data:image/[a-z0-9.+\-]+;base64,", low, re.I)
                    and "text/html" not in low):
                return f'{attr}={quote}{html_mod.escape(val, quote=True)}{quote}'
            # 危险 scheme（javascript/vbscript/data:text/html/...）→ 清空属性
            return f'{attr}={quote}{quote}'
        # 无 scheme：保留（相对/协议相对），仍做转义防引号逃逸
        return f'{attr}={quote}{html_mod.escape(val, quote=True)}{quote}'

    html_content = re.sub(
        r"""(?is)\b(href|src|action|formaction|xlink:href|poster|background)\s*=\s*("[^"]*"|'[^']*'|[^\s>]+)""",
        _fix_url, html_content)

    # 4. 移除 style 属性中的危险表达式
    def _fix_style(m):
        token = m.group(2)
        if token[:1] in ("\"", "'"):
            quote = token[:1]
            raw = token[1:-1]
        else:
            quote = "\""
            raw = token
        val = html_mod.unescape(raw)
        val = re.sub(r"[\x00-\x1f\x7f]+", "", val)
        low = val.lower()
        if re.search(r"expression\s*\(|behavior\s*:|-moz-binding|url\s*\(\s*['\"]?\s*(javascript|vbscript)", low):
            return f'style={quote}{quote}'
        return f'style={quote}{html_mod.escape(val, quote=True)}{quote}'

    html_content = re.sub(
        r"""(?is)\b(style)\s*=\s*("[^"]*"|'[^']*'|[^\s>]+)""",
        _fix_style, html_content)

    return html_content


def _escape_html(text):
    """HTML转义，防止title等文本中的HTML注入"""
    import html as html_mod
    return html_mod.escape(text, quote=True)


def _safe_resolve_local_path(src, base_dir):
    """安全解析本地文件路径，防止路径遍历"""
    base_real = os.path.realpath(base_dir)

    if os.path.isabs(src):
        candidate = os.path.realpath(src)
    else:
        candidate = os.path.realpath(os.path.join(base_dir, src))

    # 验证路径在base_dir之下（防止 ../ 路径遍历）
    if os.path.commonpath([candidate, base_real]) != base_real:
        print(f"[warn] 图片路径逃逸出授权目录，已跳过：{src}")
        return None

    # 验证文件存在且是常规文件
    if not os.path.exists(candidate) or not os.path.isfile(candidate):
        return None

    # 验证文件扩展名
    ext = os.path.splitext(candidate)[1].lower()
    if ext not in _ALLOWED_IMAGE_EXTS:
        print(f"[warn] 不支持的图片格式，已跳过：{ext}")
        return None

    # 验证文件大小
    if os.path.getsize(candidate) > _MAX_IMAGE_BYTES:
        print(f"[warn] 图片文件过大，已跳过：{src}")
        return None

    return candidate


def to_data_uri(path):
    ext = "png" if path.lower().endswith(".png") else "jpeg"
    # 安全检查：验证文件大小
    if os.path.getsize(path) > _MAX_IMAGE_BYTES:
        print(f"[warn] 图片过大，跳过base64编码：{path}")
        return path  # 返回原路径，不编码
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"data:image/{ext};base64,{b64}"


def _extract_html_body(html_content):
    """提取<body>内的内容；没有<body>则返回全文（去掉注释frontmatter）"""
    m = re.search(r"<body[^>]*>(.*?)</body>", html_content, flags=re.S | re.I)
    if m:
        body = m.group(1)
    else:
        body = html_content
    body = re.sub(r"<!--\s*(?:title|author|digest|cover)\s*:.*?-->", "", body, flags=re.S | re.I)
    return body.strip()


def _local_imgs_to_base64(html_body, base_dir):
    """把HTML中的本地图片路径转成base64 data URI（预览用，含路径遍历防护）"""
    import html as html_mod
    for img_m in re.finditer(r'<img\b[^>]*\bsrc="([^"]+)"[^>]*>', html_body, flags=re.I):
        src_raw = img_m.group(1).strip()          # 转义形态（匹配 html 原文）
        src = re.sub(r"[\x00-\x1f\x7f]+", "", html_mod.unescape(src_raw)).strip()
        if not src or src.startswith("data:") or src.startswith("http") or "mmbiz" in src:
            continue
        # 安全解析本地路径，防止路径遍历
        safe_path = _safe_resolve_local_path(src, base_dir)
        if safe_path:
            data_uri = to_data_uri(safe_path)
            html_body = html_body.replace(f'src="{src_raw}"', f'src="{data_uri}"', 1)
    return html_body


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--md", default=None, help="md/txt 文件（通用流水线离线预览）")
    ap.add_argument("--html", default=None, help="已排好版的 HTML 文件（HTML直输流水线离线预览）")
    ap.add_argument("--theme", default=None, help="主题 id：signature/mono/paper/custom（覆盖 profile）")
    ap.add_argument("--profile", default=None, help="wnp_profile.json 排版规范（缺省自动找当前目录）")
    ap.add_argument("--build", default=None, help="文章模块（组件流水线预览）")
    ap.add_argument("--out", default="preview.html", help="输出预览 HTML")
    ap.add_argument("--title", default=None, help="标题覆盖（配合 --md）")
    ap.add_argument("--cover", default=None, help="封面覆盖（配合 --md）")
    args = ap.parse_args()

    inputs = [x for x in [args.md, args.html, args.build] if x]
    if len(inputs) > 1:
        ap.error("--md / --html / --build 三选一")
    if not inputs:
        ap.error("需要 --md / --html / --build 之一")

    # 排版规范：读 profile 并换肤（CLI --theme 覆盖；两分支共用同一主题色）
    import profile
    args.prof, args.theme, prof_path = profile.resolve(args.profile, args.theme)
    if prof_path:
        print(f"[profile] 套用 {prof_path} → theme={args.theme}")

    if args.md:
        import md2render
        text = open(args.md, encoding="utf-8").read()
        base = os.path.dirname(os.path.abspath(args.md))
        prof = args.prof or {}
        rules = None
        if prof:
            r = prof.get("rules") or {}
            rules = {"concept_highlight": r.get("concept_highlight", True),
                     "chapter_numbering": r.get("chapter_numbering", True)}
        res = md2render.parse(text, title=args.title, cover=args.cover, rules=rules)
        # 本地图片 → base64 data URI；远程图保持原 URL（含路径遍历防护）
        for img in res["images"]:
            safe_path = _safe_resolve_local_path(img["src"], base)
            if safe_path:
                img["src"] = to_data_uri(safe_path)
        html_body = res["html"]
        for img in res["images"]:
            html_body = html_body.replace(img["token"], img["src"])
        # profile 签名位（与 push_draft 同一规则，保证预览=推送）
        if prof and (prof.get("rules") or {}).get("end_sign", True):
            sgn = prof.get("sign") or {}
            if sgn.get("name") and not res.get("sign_rendered"):
                import renderer as R
                html_body += R.signature(name=sgn["name"], slogan=sgn.get("slogan", ""))
        TITLE = _escape_html(res["title"] or "预览")
    elif args.html:
        raw = open(args.html, encoding="utf-8").read()
        base = os.path.dirname(os.path.abspath(args.html))
        html_body = _extract_html_body(raw)
        # HTML消毒：防止活动内容注入（XSS）
        html_body = _sanitize_html(html_body)
        html_body = _local_imgs_to_base64(html_body, base)
        # 从注释frontmatter或<title>提取标题，并HTML转义
        title_m = re.search(r"<!--.*?title\s*:\s*(.+?)(?:\n|-->)", raw, flags=re.S | re.I)
        if title_m:
            TITLE = _escape_html(title_m.group(1).strip())
        else:
            t_m = re.search(r"<title>(.*?)</title>", raw, flags=re.S | re.I)
            TITLE = _escape_html(t_m.group(1).strip()) if t_m else "预览"
    else:
        mod = importlib.import_module(args.build or "examples.article")
        TITLE = _escape_html(getattr(mod, "TITLE", "预览"))
        ILLUSTRATIONS = getattr(mod, "ILLUSTRATIONS", [])
        build_content = getattr(mod, "build_content")
        # 本地插图 -> base64 data URI（预览能看到图，含路径遍历防护）
        images = {}
        for ill in ILLUSTRATIONS:
            safe_path = _safe_resolve_local_path(ill["path"], SKILL_ROOT)
            if safe_path:
                images[ill["key"]] = to_data_uri(safe_path)
        html_body = build_content(images)

    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{TITLE}</title>
<style>
  body {{ margin:0; background:#f2f2f2; font-family:'PingFang SC','Microsoft YaHei',sans-serif; }}
  .article {{ max-width:677px; margin:32px auto; background:#fff; padding:40px 28px; }}
</style></head>
<body><div class="article">{html_body}</div></body></html>"""

    with open(args.out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"saved preview: {args.out}  ({len(html)} chars)")


if __name__ == "__main__":
    main()
