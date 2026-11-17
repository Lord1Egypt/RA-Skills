# -*- coding: utf-8 -*-
"""
单文件 HTML 打包脚本 —— 把本地图片全部转成 base64 内嵌，输出可分发的单文件 HTML。

用法:
    python -X utf8 scripts/inline_images.py                        # 自动命名
    python -X utf8 scripts/inline_images.py --topic Harness-Engineering
    python -X utf8 scripts/inline_images.py --out v3_5pct_Harness-Engineering.html
    python -X utf8 scripts/inline_images.py --keep-index           # 不删 index.html

默认流程:
    1. 读 index.html
    2. 内嵌所有本地图片引用（<img src> / CSS url() / <source srcset>）
    3. 写到 {工作区文件夹名}_{ASCII主题名}.html
    4. 三重校验通过 → 删除 index.html

退出码: 0 成功 / 1 失败（失败时两个文件都保留）
"""
import argparse
import base64
import mimetypes
import os
import re
import sys

# Windows 控制台 cp936，中文/符号输出会 UnicodeEncodeError
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

MIME_BY_EXT = {
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.webp': 'image/webp',
    '.svg': 'image/svg+xml',
    '.ico': 'image/x-icon',
    '.bmp': 'image/bmp',
    '.avif': 'image/avif',
}

RE_IMG_SRC = re.compile(r'(<img\b[^>]*?\bsrc\s*=\s*)(["\'])(.*?)\2', re.I | re.S)
RE_SOURCE = re.compile(r'(<source\b[^>]*?\b(?:src|srcset)\s*=\s*)(["\'])(.*?)\2', re.I | re.S)
RE_CSS_URL = re.compile(r'(url\(\s*)(["\']?)([^)"\']+)(\2\s*\))', re.I)


def is_local(ref):
    """只处理本地文件路径，跳过 data:/http(s):// //、锚点、空串"""
    r = (ref or '').strip()
    if not r:
        return False
    return not r.lower().startswith(('data:', 'http://', 'https://', '//', '#', 'mailto:'))


def to_data_uri(path):
    ext = os.path.splitext(path)[1].lower()
    mime = MIME_BY_EXT.get(ext) or mimetypes.guess_type(path)[0] or 'application/octet-stream'
    with open(path, 'rb') as f:
        raw = f.read()
    return 'data:%s;base64,%s' % (mime, base64.b64encode(raw).decode('ascii')), len(raw)


def sanitize_topic(topic, maxlen=32):
    """ASCII 化：保留字母数字，其余转 -，压缩连续连字符"""
    s = re.sub(r'[^A-Za-z0-9]+', '-', topic or '').strip('-')
    s = re.sub(r'-{2,}', '-', s)
    return s[:maxlen].strip('-') or 'page'


def main():
    ap = argparse.ArgumentParser(description='把 HTML 里的本地图片全部 base64 内嵌，输出单文件 HTML')
    ap.add_argument('--src', default='index.html', help='源 HTML（默认 index.html）')
    ap.add_argument('--out', default=None, help='输出文件名（默认 {文件夹}_{主题}.html）')
    ap.add_argument('--topic', default=None, help='ASCII 主题名，用于自动命名')
    ap.add_argument('--keep-index', action='store_true', help='保留源文件，不删除')
    args = ap.parse_args()

    src = args.src
    if not os.path.exists(src):
        print('[错误] 找不到源文件: %s' % src)
        return 1

    if args.out:
        out = args.out
    else:
        folder = os.path.basename(os.path.abspath('.')) or 'page'
        out = '%s_%s.html' % (folder, sanitize_topic(args.topic))
    if not out.lower().endswith('.html'):
        out += '.html'
    if os.path.abspath(out) == os.path.abspath(src):
        print('[错误] 输出文件不能与源文件同名')
        return 1

    base_dir = os.path.dirname(os.path.abspath(src))
    orig_html = open(src, encoding='utf-8', errors='ignore').read()
    orig_size = os.path.getsize(src)
    html = orig_html

    cache = {}        # 绝对路径 -> data URI
    missing = []      # 缺失 / 读取失败的引用
    inlined = []      # 成功内嵌的绝对路径

    def resolve(ref):
        p = ref.strip()
        if p.startswith('file://'):
            p = p[7:]
        p = p.replace('\\', '/')
        if p.startswith('./'):
            p = p[2:]
        return os.path.normpath(os.path.join(base_dir, p))

    def build_uri(ref):
        absp = resolve(ref)
        if absp in cache:
            return cache[absp]
        if not os.path.isfile(absp):
            if ref not in missing:
                missing.append(ref)
            return None
        try:
            uri, _ = to_data_uri(absp)
        except Exception as e:
            print('[警告] 读取失败 %s : %s' % (ref, e))
            if ref not in missing:
                missing.append(ref)
            return None
        cache[absp] = uri
        inlined.append(absp)
        return uri

    def sub_attr(m):
        head, quote, ref = m.group(1), m.group(2), m.group(3)
        if not is_local(ref):
            return m.group(0)
        uri = build_uri(ref)
        return (head + quote + uri + quote) if uri else m.group(0)

    def sub_srcset(m):
        head, quote, value = m.group(1), m.group(2), m.group(3)
        parts, changed = [], False
        for token in value.split(','):
            token = token.strip()
            if not token:
                continue
            bits = token.split()
            if is_local(bits[0]):
                uri = build_uri(bits[0])
                if uri:
                    bits[0] = uri
                    changed = True
            parts.append(' '.join(bits))
        return (head + quote + ', '.join(parts) + quote) if changed else m.group(0)

    def sub_css(m):
        head, quote, ref, tail = m.group(1), m.group(2), m.group(3), m.group(4)
        if not is_local(ref):
            return m.group(0)
        uri = build_uri(ref)
        return (head + quote + uri + quote + tail) if uri else m.group(0)

    html = RE_IMG_SRC.sub(sub_attr, html)
    html = RE_SOURCE.sub(sub_srcset, html)
    html = RE_CSS_URL.sub(sub_css, html)

    open(out, 'w', encoding='utf-8').write(html)
    out_size = os.path.getsize(out)

    print('[内嵌] 成功 %d 张 / 缺失 %d 张' % (len(inlined), len(missing)))
    if missing:
        print('[缺失清单]')
        for m_ in missing:
            print('  - %s' % m_)
    print('[体积] %.1f KB -> %.1f KB (%.2fx)' % (
        orig_size / 1024.0, out_size / 1024.0, (out_size / float(orig_size)) if orig_size else 0))

    # ---------- 三重校验 ----------
    new_html = open(out, encoding='utf-8', errors='ignore').read()
    problems = []
    if 'zh-header' not in new_html:
        problems.append('缺少 zh-header 结构')
    if '</main>' not in new_html:
        problems.append('缺少 </main>')
    n_old = len(re.findall(r'<article[^>]*id="ch-\d+"', orig_html))
    n_new = len(re.findall(r'<article[^>]*id="ch-\d+"', new_html))
    if n_old != n_new:
        problems.append('章节计数不一致：原 %d -> 新 %d' % (n_old, n_new))
    n_data = new_html.count('data:image/')
    if len(inlined) and n_data < len(inlined):
        problems.append('data:image 数量不足：内嵌 %d -> 实际 %d' % (len(inlined), n_data))

    if problems:
        print('\n[失败] 三重校验未通过，两个文件都保留（未删除 %s）：' % src)
        for p in problems:
            print('  - %s' % p)
        return 1

    print('[校验] 通过（</main> + zh-header + 章节 %d + data:image %d 处）' % (n_new, n_data))

    if args.keep_index:
        print('[保留] --keep-index 指定，未删除 %s' % src)
    else:
        try:
            os.remove(src)
            print('[清理] 已删除中间产物 %s' % src)
        except OSError as e:
            print('[警告] 删除 %s 失败: %s（可手工删除）' % (src, e))

    print('[完成] 单文件交付物: %s' % os.path.abspath(out))
    return 0


if __name__ == '__main__':
    sys.exit(main())
