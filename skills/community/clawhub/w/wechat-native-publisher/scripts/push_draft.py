# -*- coding: utf-8 -*-
"""
wechat-native-publisher 主推送脚本（双流水线 + 环境自检引导）

两条流水线，同一终点「草稿箱」：
  A) 通用 md/txt 流水线（推荐，0 代码）：
       python push_draft.py --config cfg.json --md article.md --theme signature [--no-push]
     md 支持 frontmatter(title/cover/author/digest/sign_name/sign_slogan)，
     图片用 ![图注](相对路径或URL)，自动上传并替换为微信素材 URL。
  B) HTML 直输流水线（用户/AI已排好版的HTML）：
       python push_draft.py --config cfg.json --html article.html [--no-push]
     HTML 支持注释 frontmatter(<!-- title: ... author: ... digest: ... cover: ... -->)，
     正文为 <body> 内内容（或全文），图片自动上传并替换为微信素材 URL。
     要求HTML符合微信白名单规则（section/rgb/span leaf，无table/div/hex等），
     发布前自检会拦截不符合规则的内容。
  C) 组件模块流水线（进阶，Python 组装）：
       python push_draft.py --config cfg.json --build examples.article [--no-push]
     --build 模块需导出 TITLE/AUTHOR/DIGEST/COVER/ILLUSTRATIONS/build_content(images)

环境自检：
       python push_draft.py --check-env [--config cfg.json]
  无凭据时所有命令都会打印新手引导（AppID/Secret / 认证 / IP 白名单 / errcode 对照）。

通用参数：--theme(仅 md) / --title / --author / --digest / --cover(覆盖)
          --no-push 只上传+自检，不建草稿；--no-validate 跳过自检；--force 放行 BLOCK。

凭据不在本文件内：--config 指定，或环境变量 WECHAT_PUSH_CONFIG，或当前目录 config.json。
"""
import os, sys, argparse, importlib, json, tempfile, re

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)        # renderer/theme/md2render/wx_api/validate
sys.path.insert(0, SKILL_ROOT)  # examples

import requests  # noqa: E402
import md2render  # noqa: E402
import profile  # noqa: E402  (wnp_profile.json 排版规范)
from wx_api import get_access_token, upload_thumb, upload_img, add_draft, get_draft_count  # noqa: E402
from validate import validate_content, print_report  # noqa: E402


# ---- 环境自检：errcode → 人类可读的修复指引 ----
ENV_GUIDE = """开始前你需要准备：
  ① 已认证的公众号（草稿箱接口需要认证订阅号/服务号）
  ② 公众号后台 → 设置与开发 → 基本配置：记下 AppID 与 AppSecret
  ③ 服务器公网出口 IP 加入同页「IP白名单」（查出口 IP：myip.ipip.net）
最小 config.json：
  {"appid": "wx1234567890abcdef", "appsecret": "32位secret"}
写好后放当前目录，或用 --config / 环境变量 WECHAT_PUSH_CONFIG 指定。"""
ERRCODE_GUIDE = {
    "40013": "AppID 错误：检查 config.json 的 appid 是否与后台一致。",
    "40125": "AppSecret 错误：可能是复制不全或已重置。可在后台重新生成。",
    "40164": "IP 不在白名单：把报错信息里的 IP 加入 设置与开发→基本配置→IP白名单，再重试。",
    "40165": "IP 白名单格式错误：检查是否多空格/换行。",
    "48001": "接口权限不足：草稿箱接口需公众号已认证；确认认证状态。",
    "45009": "接口调用超过限额：当日调用次数用尽，明天再试或检查是否有死循环调用。",
    "-1": "微信系统繁忙：稍后重试；连续失败多为 IP 白名单或凭据问题。",
}


def print_env_guide(config_path=None):
    print("\n[env] 公众号推送环境自检")
    print("=" * 56)
    if config_path:
        print(f"[env] config: {config_path}")
        try:
            cfg = json.load(open(config_path, encoding="utf-8"))
            appid = str(cfg.get("appid", "") or "")
            secret = str(cfg.get("appsecret", "") or "")
            print(f"[env] appid: {appid[:6]}...{appid[-4:] if len(appid) > 10 else ''}  "
                  f"appsecret: {'已填' if secret else '缺失'}")
            if not appid or not secret:
                print("[env] 缺 appid/appsecret → 请补全后重试")
        except Exception as e:
            print(f"[env] config 读取失败：{e}")
            return False
    else:
        print("[env] 未找到 config.json（依次找 --config / WECHAT_PUSH_CONFIG / 当前目录）")
        print(f"[env] {ENV_GUIDE}")
        return False
    return True


def check_env(config_path=None):
    """探测凭据与网络：尝试拿 access_token，成功则绿灯，失败给 errcode 指引"""
    ok = print_env_guide(config_path)
    if not ok:
        return 1
    try:
        token = get_access_token(config_path)
        print(f"[env] access_token 获取成功: {token[:24]}...")
        cnt = get_draft_count(token)
        print(f"[env] 草稿箱总数: {cnt.get('total_count', '未知')}（确认网络与权限均通）")
        print("[env] 状态：OK，可以推送。")
        return 0
    except RuntimeError as e:
        msg = str(e)
        m = re.search(r'"(?:errcode|errcode)"\s*:\s*(-?\d+)', msg)
        code = m.group(1) if m else None
        print(f"[env] 获取 access_token 失败：{msg[:200]}")
        if code in ERRCODE_GUIDE:
            print(f"[env] 指引：{ERRCODE_GUIDE[code]}")
        else:
            print("[env] 指引：检查 appid/appsecret 是否复制完整；确认公众号已认证；"
                  "服务器配置已启用且 IP 已加白名单。")
        return 2


# ---- 图片落地助手（md 里的图片可能是本地相对路径或 http URL） ----
_TEMPS = []

# 安全常量
_MAX_IMAGE_BYTES = 20 * 1024 * 1024  # 单张图片最大 20MB
_ALLOWED_IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"}
_ALLOWED_PORTS = {80, 443}

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


def _is_private_ip(ip_str):
    """检查IP是否为私有/回环/链路本地/保留地址（SSRF防护）"""
    import ipaddress
    try:
        ip = ipaddress.ip_address(ip_str)
    except ValueError:
        return True  # 无法解析的视为不安全
    return (ip.is_private or ip.is_loopback or ip.is_link_local
            or ip.is_multicast or ip.is_reserved or ip.is_unspecified)


def _validate_remote_url(url):
    """验证远程URL安全性，返回解析后的公共IP列表（防DNS重绑定）"""
    from urllib.parse import urlparse
    import socket

    parsed = urlparse(url)
    if parsed.scheme.lower() not in ("http", "https"):
        raise RuntimeError(f"不支持的URL协议：{parsed.scheme}（仅支持http/https）")

    hostname = parsed.hostname
    if not hostname:
        raise RuntimeError(f"URL缺少主机名：{url}")

    # 检查端口
    port = parsed.port
    if port is not None and port not in _ALLOWED_PORTS:
        raise RuntimeError(f"不允许的端口：{port}（仅允许80/443）")

    # 解析主机名到IP（只解析一次，防止DNS重绑定）
    try:
        addr_infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        raise RuntimeError(f"无法解析主机名：{hostname}")

    public_ips = []
    for family, type_, proto, canonname, sockaddr in addr_infos:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise RuntimeError(f"主机名 {hostname} 解析到私有/内部IP {ip}，已拒绝（SSRF防护）")
        public_ips.append(ip)

    if not public_ips:
        raise RuntimeError(f"主机名 {hostname} 未解析到任何公共IP")

    return hostname, public_ips


class _PinnedDNS:
    """上下文管理器：临时锁定DNS解析，防止requests二次解析导致DNS重绑定"""
    def __init__(self, hostname, pinned_ips):
        self.hostname = hostname
        self.pinned_ips = pinned_ips
        self._original_getaddrinfo = None

    def __enter__(self):
        import socket
        self._original_getaddrinfo = socket.getaddrinfo
        pinned = self.pinned_ips
        target_host = self.hostname

        def patched_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
            if host == target_host:
                # 强制返回验证过的IP，防止DNS重绑定
                results = []
                for ip in pinned:
                    if ":" in ip:  # IPv6
                        results.append((socket.AF_INET6, socket.SOCK_STREAM, 6, "", (ip, port or 0, 0, 0)))
                    else:  # IPv4
                        results.append((socket.AF_INET, socket.SOCK_STREAM, 6, "", (ip, port or 0)))
                return results
            return self._original_getaddrinfo(host, port, family, type, proto, flags)

        socket.getaddrinfo = patched_getaddrinfo
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        import socket
        socket.getaddrinfo = self._original_getaddrinfo
        return False


def _safe_resolve_local_path(src, base_dir):
    """安全解析本地文件路径，防止路径遍历"""
    # 解析base_dir的真实路径
    base_real = os.path.realpath(base_dir)

    if os.path.isabs(src):
        # 绝对路径：需要显式验证在授权目录下
        candidate = os.path.realpath(src)
    else:
        # 相对路径：基于base_dir解析
        candidate = os.path.realpath(os.path.join(base_dir, src))

    # 验证路径在base_dir之下（防止 ../ 路径遍历）
    if os.path.commonpath([candidate, base_real]) != base_real:
        raise RuntimeError(f"图片路径逃逸出授权目录：{src}（解析为 {candidate}，授权根目录 {base_real}）")

    # 验证文件存在且是常规文件
    if not os.path.exists(candidate):
        raise RuntimeError(f"图片文件不存在：{src}（已相对文章目录解析为 {candidate}）")
    if not os.path.isfile(candidate):
        raise RuntimeError(f"图片路径不是常规文件：{src}（可能是目录、设备或特殊文件）")

    # 验证文件扩展名
    ext = os.path.splitext(candidate)[1].lower()
    if ext not in _ALLOWED_IMAGE_EXTS:
        raise RuntimeError(f"不支持的图片格式：{ext}（支持：{', '.join(sorted(_ALLOWED_IMAGE_EXTS))}）")

    # 验证文件大小
    file_size = os.path.getsize(candidate)
    if file_size > _MAX_IMAGE_BYTES:
        raise RuntimeError(f"图片文件过大：{file_size} bytes（最大允许 {_MAX_IMAGE_BYTES} bytes）")

    return candidate


def _ensure_local(src, base_dir):
    """返回本地文件路径：本地路径 → 安全解析；http(s) URL → 安全下载到临时文件并登记清理"""
    if re.match(r"^https?://", src, re.I):
        # SSRF防护：验证URL安全性，只解析一次DNS，返回验证过的公共IP列表
        hostname, public_ips = _validate_remote_url(src)

        # 用_PinnedDNS锁定DNS解析，防止requests二次解析导致DNS重绑定。
        # 用独立 Session 且 trust_env=False：彻底禁用 HTTP(S)_PROXY / ALL_PROXY
        # 等环境代理（proxies={http:None} 不能完全覆盖 requests 的 env 合并逻辑），
        # 确保连接只走校验过的公共 IP 直连，代理无法改写目标路由。
        with _PinnedDNS(hostname, public_ips), requests.Session() as sess:
            sess.trust_env = False
            # 流式下载，限制大小，禁用重定向
            try:
                r = sess.get(src, timeout=(10, 30), stream=True, allow_redirects=False)
                r.raise_for_status()
            except requests.exceptions.TooManyRedirects:
                raise RuntimeError(f"URL重定向次数过多：{src}（已禁用重定向）")

            # 验证Content-Type
            content_type = r.headers.get("Content-Type", "").lower()
            if content_type and not any(ct in content_type for ct in ("image/", "application/octet-stream")):
                raise RuntimeError(f"远程资源不是图片：Content-Type={content_type}")

            # 流式下载，限制大小
            tmp = tempfile.NamedTemporaryFile(suffix=os.path.splitext(src)[1] or ".jpg",
                                              delete=False)
            total = 0
            for chunk in r.iter_content(chunk_size=8192):
                total += len(chunk)
                if total > _MAX_IMAGE_BYTES:
                    tmp.close()
                    os.remove(tmp.name)
                    raise RuntimeError(f"远程图片过大：超过 {_MAX_IMAGE_BYTES} bytes 限制")
                tmp.write(chunk)
            tmp.close()

        # 用Pillow验证下载的内容确实是图片
        try:
            from PIL import Image
            with Image.open(tmp.name) as img:
                img.verify()
        except Exception as e:
            os.remove(tmp.name)
            raise RuntimeError(f"下载的内容不是有效的图片文件：{e}")

        _TEMPS.append(tmp.name)
        return tmp.name

    # 本地路径：安全解析，防止路径遍历
    return _safe_resolve_local_path(src, base_dir)


def _cleanup_temps():
    for t in _TEMPS:
        try:
            os.remove(t)
        except OSError:
            pass
    _TEMPS.clear()


# ---- md 流水线 ----
def run_md_pipeline(args, token):
    if not os.path.exists(args.md):
        raise RuntimeError(f"md/txt 文件不存在：{args.md}")
    md_dir = os.path.dirname(os.path.abspath(args.md))
    prof = getattr(args, "prof", None) or {}

    # 渲染规则来自 profile（theme 换肤已在 main() 的 profile.resolve 完成）
    rules = None
    if prof:
        r = prof.get("rules") or {}
        rules = {"concept_highlight": r.get("concept_highlight", True),
                 "chapter_numbering": r.get("chapter_numbering", True)}
    print(f"[md] 解析 {os.path.basename(args.md)} （theme={args.theme}）")
    res = md2render.parse(open(args.md, encoding="utf-8").read(),
                          title=args.title, cover=args.cover, rules=rules)

    TITLE = args.title or res["title"]
    AUTHOR = args.author or res["author"] or prof.get("author", "") or ""
    DIGEST = args.digest or res["digest"] or ""
    if not TITLE:
        raise RuntimeError("未取到标题：请在 frontmatter 写 title，或 --title 指定（.txt 文件必须 --title）。")

    # 摘要/作者长度预检（微信字段限制，超限会推送失败或截断）
    if len(AUTHOR) > 8:
        print(f"[warn] author 超过 8 个汉字（微信限制），将被截断：{AUTHOR}")
    if len(DIGEST) > 120:
        print(f"[warn] digest 超过 120 字（微信限制），将被截断。")
    if len(TITLE) > 64:
        print(f"[warn] title 超过 64 字（微信限制），将被截断。")

    # 封面：frontmatter/--cover → 本地/URL → 上传 thumb；缺失则自动生成几何占位封面
    cover_auto = not getattr(args, "no_cover_auto", False)
    if prof:
        cover_auto = cover_auto and bool(prof.get("cover", {}).get("auto_geo", True))
    cover_src = res["cover"]
    cover_local = None
    if cover_src:
        print("[1/5] 封面 -> 素材库")
        cover_local = _ensure_local(cover_src, md_dir)
        print(f"      {cover_local}")
    elif cover_auto:
        print("[1/5] 无封面 -> 自动生成几何占位封面")
        import make_cover
        # 用不可预测的临时文件名，防止符号链接攻击
        cover_tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False, prefix="wnp_cover_")
        cover_tmp.close()
        cover_local = cover_tmp.name
        make_cover.geometric_cover(
            TITLE, args.cover_subtitle or "", (args.author or AUTHOR)[:8], "",
            cover_local, theme_id=args.theme)
        _TEMPS.append(cover_local)
        print(f"      theme={args.theme}")
    else:
        raise RuntimeError("缺少封面：请 --cover 指定 / frontmatter 写 cover，"
                           "或让系统自动生成（去掉 --no-cover-auto；若 profile 的"
                           "cover.auto_geo=false 则在 init_profile 改回 auto）。")
    thumb = upload_thumb(token, cover_local)
    print(f"      thumb_media_id: {thumb[:24]}...")

    # 正文插图：上传并把 __WXIMG_N__ token 换成微信 URL
    print("[2/5] 正文插图 -> 素材库")
    html = res["html"]
    for img in res["images"]:
        url = upload_img(token, _ensure_local(img["src"], md_dir))
        html = html.replace(img["token"], url)
        print(f"      {img['token']} -> {url[:44]}...")
    print(f"      {len(res['images'])} 张插图完成")

    print(f"[3/5] 正文组装：{res['chars']} 字，html {len(html)} 字符")
    # profile 签名位：frontmatter 未写 sign_name 且 profile 开了 end_sign 才追加
    if prof and (prof.get("rules") or {}).get("end_sign", True):
        sgn = prof.get("sign") or {}
        if sgn.get("name") and not res.get("sign_rendered"):
            import renderer as R
            html += R.signature(name=sgn["name"], slogan=sgn.get("slogan", ""))
            print(f"      追加 profile 签名：{sgn['name']}")
    return {"title": TITLE, "author": AUTHOR, "digest": DIGEST,
            "content": html, "thumb": thumb, "no_validate": None}


# ---- HTML 直输流水线（用户/AI已排好版的HTML） ----
def _parse_html_frontmatter(html_content):
    """从HTML注释中提取frontmatter：<!-- title: xxx author: xxx digest: xxx cover: xxx -->"""
    fm = {}
    # 匹配 <!-- ... --> 注释块
    for m in re.finditer(r"<!--(.*?)-->", html_content, flags=re.S):
        block = m.group(1).strip()
        for line in block.splitlines():
            line = line.strip()
            km = re.match(r"^([A-Za-z_]+)\s*:\s*(.*)$", line)
            if km:
                fm[km.group(1).lower()] = km.group(2).strip()
    return fm


def _extract_html_body(html_content):
    """提取<body>内的内容；没有<body>则返回全文（去掉注释frontmatter）"""
    m = re.search(r"<body[^>]*>(.*?)</body>", html_content, flags=re.S | re.I)
    if m:
        body = m.group(1)
    else:
        body = html_content
    # 去掉frontmatter注释块（避免进正文）
    body = re.sub(r"<!--\s*(?:title|author|digest|cover)\s*:.*?-->", "", body, flags=re.S | re.I)
    return body.strip()


def run_html_pipeline(args, token):
    if not os.path.exists(args.html):
        raise RuntimeError(f"HTML 文件不存在：{args.html}")
    html_dir = os.path.dirname(os.path.abspath(args.html))
    prof = getattr(args, "prof", None) or {}

    raw = open(args.html, encoding="utf-8").read()
    fm = _parse_html_frontmatter(raw)
    body_html = _extract_html_body(raw)
    # HTML消毒：防止活动内容注入（XSS），与预览流水线使用同一消毒器
    body_html = _sanitize_html(body_html)

    TITLE = args.title or fm.get("title", "")
    AUTHOR = args.author or fm.get("author", "") or prof.get("author", "") or ""
    DIGEST = args.digest or fm.get("digest", "") or ""
    if not TITLE:
        # 尝试从 <h1> 提取标题
        h1_m = re.search(r"<h1[^>]*>(.*?)</h1>", body_html, flags=re.S | re.I)
        if h1_m:
            TITLE = re.sub(r"<[^>]+>", "", h1_m.group(1)).strip()
    if not TITLE:
        raise RuntimeError("未取到标题：请在HTML注释写 title，或 --title 指定。")

    # 摘要/作者长度预检
    if len(AUTHOR) > 8:
        print(f"[warn] author 超过 8 个汉字（微信限制），将被截断：{AUTHOR}")
    if len(DIGEST) > 120:
        print(f"[warn] digest 超过 120 字（微信限制），将被截断。")
    if len(TITLE) > 64:
        print(f"[warn] title 超过 64 字（微信限制），将被截断。")

    # 封面：frontmatter/--cover → 本地/URL → 上传 thumb；缺失则自动生成几何占位封面
    cover_auto = not getattr(args, "no_cover_auto", False)
    if prof:
        cover_auto = cover_auto and bool(prof.get("cover", {}).get("auto_geo", True))
    cover_src = args.cover or fm.get("cover", "")
    cover_local = None
    if cover_src:
        print("[1/5] 封面 -> 素材库")
        cover_local = _ensure_local(cover_src, html_dir)
        print(f"      {cover_local}")
    elif cover_auto:
        print("[1/5] 无封面 -> 自动生成几何占位封面")
        import make_cover
        # 用不可预测的临时文件名，防止符号链接攻击
        cover_tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False, prefix="wnp_cover_")
        cover_tmp.close()
        cover_local = cover_tmp.name
        make_cover.geometric_cover(
            TITLE, args.cover_subtitle or "", (args.author or AUTHOR)[:8], "",
            cover_local, theme_id=args.theme or "signature")
        _TEMPS.append(cover_local)
        print(f"      theme={args.theme or 'signature'}")
    else:
        raise RuntimeError("缺少封面：请 --cover 指定 / HTML注释写 cover，"
                           "或让系统自动生成（去掉 --no-cover-auto）。")
    thumb = upload_thumb(token, cover_local)
    print(f"      thumb_media_id: {thumb[:24]}...")

    # 正文插图：扫描 <img src="...">，上传并替换为微信 URL
    print("[2/5] 正文插图 -> 素材库")
    html = body_html
    img_count = 0
    for img_m in re.finditer(r'<img\b[^>]*\bsrc="([^"]+)"[^>]*>', html, flags=re.I):
        src_raw = img_m.group(1).strip()          # 转义形态（匹配 html 原文，用于替换）
        src = re.sub(r"[\x00-\x1f\x7f]+", "", html.unescape(src_raw)).strip()  # 解码后用于下载
        # 跳过已经是微信CDN的图、data URI、空src
        if not src or src.startswith("data:") or "mmbiz" in src:
            continue
        try:
            local = _ensure_local(src, html_dir)
            url = upload_img(token, local)
            html = html.replace(f'src="{src_raw}"', f'src="{url}"', 1)
            img_count += 1
            print(f"      {src[:50]} -> {url[:44]}...")
        except Exception as e:
            print(f"      [warn] 图片上传失败 {src[:50]}: {e}")
    print(f"      {img_count} 张插图完成")

    print(f"[3/5] 正文组装：html {len(html)} 字符")
    # profile 签名位：profile 开了 end_sign 且 HTML 中没有签名标记才追加
    if prof and (prof.get("rules") or {}).get("end_sign", True):
        sgn = prof.get("sign") or {}
        if sgn.get("name") and "wnp_signature" not in html:
            import renderer as R
            html += R.signature(name=sgn["name"], slogan=sgn.get("slogan", ""))
            print(f"      追加 profile 签名：{sgn['name']}")
    return {"title": TITLE, "author": AUTHOR, "digest": DIGEST,
            "content": html, "thumb": thumb, "no_validate": None}


# ---- 组件模块流水线（保留原能力） ----
def run_module_pipeline(args, token):
    mod = importlib.import_module(args.build)
    TITLE = getattr(mod, "TITLE", "未命名")
    AUTHOR = getattr(mod, "AUTHOR", "")
    DIGEST = getattr(mod, "DIGEST", "")
    COVER = getattr(mod, "COVER", None)
    ILLUSTRATIONS = getattr(mod, "ILLUSTRATIONS", [])
    build_content = getattr(mod, "build_content")

    print(f"[module] 文章模块：{args.build}")
    if not COVER:
        raise RuntimeError("文章模块缺 COVER（封面图路径）")
    print("[1/5] 封面 -> 素材库")
    thumb = upload_thumb(token, COVER)
    print(f"      thumb_media_id: {thumb[:24]}...")

    images = {}
    print("[2/5] 正文插图 -> 素材库")
    for ill in ILLUSTRATIONS:
        url = upload_img(token, ill["path"])
        images[ill["key"]] = url
        print(f"      {ill['key']} -> {url[:44]}...")
    print(f"      {len(images)} 张插图完成")

    print("[3/5] 正文组装")
    content = build_content(images)
    print(f"      正文 {len(content)} 字符")
    return {"title": TITLE, "author": AUTHOR, "digest": DIGEST,
            "content": content, "thumb": thumb, "no_validate": None}


def main():
    ap = argparse.ArgumentParser(description="公众号草稿箱一键推送（md 通用流水线 / 组件模块流水线）")
    ap.add_argument("--config", default=None, help="公众号凭据 config.json 路径")
    ap.add_argument("--md", default=None, help="md/txt 文件（通用流水线）")
    ap.add_argument("--html", default=None, help="已排好版的 HTML 文件（HTML直输流水线）")
    ap.add_argument("--build", default=None, help="文章模块名，如 examples.article（进阶流水线）")
    ap.add_argument("--profile", default=None, help="wnp_profile.json 排版规范路径（缺省自动找当前目录）")
    ap.add_argument("--theme", default=None, help="主题 id：signature/mono/paper/custom（覆盖 profile）")
    ap.add_argument("--title", default=None, help="标题（覆盖 frontmatter）")
    ap.add_argument("--author", default=None, help="作者（覆盖 frontmatter/profile）")
    ap.add_argument("--digest", default=None, help="摘要（覆盖 frontmatter）")
    ap.add_argument("--cover", default=None, help="封面路径/URL（覆盖 frontmatter）")
    ap.add_argument("--cover-subtitle", default=None, help="自动生成封面时的副标题")
    ap.add_argument("--no-cover-auto", action="store_true", help="缺少封面时不自动生成（直接报错）")
    ap.add_argument("--check-env", action="store_true", help="只做环境自检")
    ap.add_argument("--no-push", action="store_true", help="上传+自检后不建草稿，仅打印正文")
    ap.add_argument("--no-validate", action="store_true", help="跳过发布前自检")
    ap.add_argument("--force", action="store_true", help="自检 BLOCK 时仍继续推送")
    args = ap.parse_args()

    try:
        if args.check_env:
            raise SystemExit(check_env(args.config))

        if not args.md and not args.html and not args.build:
            print("请指定 --md <文章.md>（通用）、--html <已排版.html>（HTML直输）或 --build <模块>（进阶）。--check-env 可先自检环境。")
            raise SystemExit(2)

        # 排版规范：读 wnp_profile.json 并换肤（CLI --theme 覆盖 profile；custom 自动衍生配色）
        args.prof, args.theme, prof_path = profile.resolve(args.profile, args.theme)
        if prof_path:
            tid_label = args.theme + ("（自定义配色）" if args.theme == "custom" else "")
            print(f"[profile] 套用排版规范 {prof_path} → theme={tid_label}")

        # --no-push 预览模式：在凭据检查、获取access_token和上传图片之前就拦截
        # 直接调用 make_preview 生成本地HTML预览，不产生任何网络请求
        if args.no_push:
            import subprocess
            preview_script = os.path.join(HERE, "make_preview.py")
            preview_cmd = [sys.executable, preview_script]
            if args.md:
                preview_cmd += ["--md", args.md]
            elif args.html:
                preview_cmd += ["--html", args.html]
            elif args.build:
                preview_cmd += ["--build", args.build]
            if args.theme:
                preview_cmd += ["--theme", args.theme]
            if args.title:
                preview_cmd += ["--title", args.title]
            if args.cover:
                preview_cmd += ["--cover", args.cover]
            # 用不可预测的临时文件名，防止符号链接攻击
            preview_tmp = tempfile.NamedTemporaryFile(suffix=".html", delete=False, prefix="wnp_preview_")
            preview_tmp.close()
            preview_out = preview_tmp.name
            preview_cmd += ["--out", preview_out]
            print("[no-push] 生成本地预览（不获取access_token，不上传图片）...")
            result = subprocess.run(preview_cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"[FAIL] 预览生成失败：{result.stderr}")
                raise SystemExit(1)
            print(result.stdout)
            print(f"[DONE] 预览已生成：{preview_out}")
            print("      用浏览器打开即可查看排版效果，无任何网络请求。")
            return

        # 任何推送前先做凭据存在性检查（缺则打印新手引导再退出）
        cfg_found = print_env_guide(args.config)
        if not cfg_found:
            raise SystemExit(2)

        token = get_access_token(args.config)
        print("[0/5] access_token:", token[:20] + "...")

        if args.md:
            art = run_md_pipeline(args, token)
        elif args.html:
            art = run_html_pipeline(args, token)
        else:
            art = run_module_pipeline(args, token)

        # 发布前自检
        if not args.no_validate:
            print("[4/5] 发布前自检...")
            report = validate_content(art["content"])
            print_report(report)
            if report["risk"] == "BLOCK" and not args.force:
                print("\n[ABORT] 自检发现 BLOCK 级问题，已中止。修复后重试；确要推送可加 --force。")
                return

        article = {
            "title": art["title"],
            "author": art["author"],
            "digest": art["digest"],
            "content": art["content"],
            "content_source_url": "",
            "thumb_media_id": art["thumb"],
            "need_open_comment": 1,
            "only_fans_can_comment": 0,
        }
        media_id = add_draft(token, article)
        print("[5/5] 新增草稿 media_id:", media_id)
        cnt = get_draft_count(token)
        print("      当前草稿总数:", cnt.get("total_count"))
        print("\n[DONE] 已进入草稿箱，请到 公众号后台 → 草稿箱 查看排版效果。")
        print("      排版确认后只需点「发布」，正文 0 编辑。")
    except RuntimeError as e:
        print(f"\n[FAIL] {e}")
        raise SystemExit(1)
    except KeyboardInterrupt:
        print("\n[ABORT] 用户中断")
        raise SystemExit(130)
    finally:
        _cleanup_temps()


if __name__ == "__main__":
    main()
