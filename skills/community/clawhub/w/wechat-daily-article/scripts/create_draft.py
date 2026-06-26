#!/usr/bin/env python3
"""
微信公众号草稿创建脚本
Usage: python3 create_draft.py "<标题>" "<正文HTML>"
正文HTML中的占位符会被替换:
  COVERIMG_URL -> 封面微信URL
  CHAPIMG1_URL ~ CHAPIMG6_URL -> 章节微信URL
"""
import sys, os, json, urllib.request, urllib.parse, shutil, re
from html.parser import HTMLParser

APPID = os.environ.get('WECHAT_APPID', '')
APPSECRET = os.environ.get('WECHAT_APPSECRET', '')
UPLOAD_IMG_URL = 'https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={token}'
ADD_MATERIAL_URL = 'https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image'
DRAFT_URL = 'https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}'

def get_access_token():
    url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={APPSECRET}'
    with urllib.request.urlopen(url, timeout=10) as r:
        d = json.loads(r.read())
    if d.get('errcode'):
        raise Exception(f'token失败: {d}')
    return d['access_token']

def download_img(url, filepath):
    """下载网络图片到本地文件"""
    import ssl
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with urllib.request.urlopen(url, timeout=30, context=ctx) as r:
        data = r.read()
    with open(filepath, 'wb') as f:
        f.write(data)
    print(f'  下载: {url[:60]} -> {filepath}')

def upload_img_file(token, filepath):
    """uploadimg: 上传图片，返回永久URL (mmbiz.qpic.cn)"""
    if not os.path.exists(filepath):
        raise Exception(f'文件不存在: {filepath}')
    boundary = '----FormBoundary7MA4YWxkTrZu0gW'
    with open(filepath, 'rb') as f:
        fd = f.read()
    fname = os.path.basename(filepath)
    body = (
        f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{fname}"\r\nContent-Type: image/png\r\n\r\n'
    ).encode() + fd + f'\r\n--{boundary}--\r\n'.encode()
    req = urllib.request.Request(
        UPLOAD_IMG_URL.format(token=token), data=body,
        headers={'Content-Type': f'multipart/form-data; boundary={boundary}'}, method='POST'
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        result = json.loads(r.read())
    if result.get('errcode'):
        raise Exception(f'uploadimg失败: {result}')
    return result['url']

def upload_material(token, filepath):
    """add_material: 上传永久素材，返回media_id（字段名必须用'media'）"""
    if not os.path.exists(filepath):
        raise Exception(f'文件不存在: {filepath}')
    boundary = '----FormBoundary7MA4YWxkTrZu0gW'
    with open(filepath, 'rb') as f:
        fd = f.read()
    fname = os.path.basename(filepath)
    body = (
        f'--{boundary}\r\nContent-Disposition: form-data; name="media"; filename="{fname}"\r\nContent-Type: image/png\r\n\r\n'
    ).encode() + fd + f'\r\n--{boundary}--\r\n'.encode()
    req = urllib.request.Request(
        ADD_MATERIAL_URL.format(token=token), data=body,
        headers={'Content-Type': f'multipart/form-data; boundary={boundary}'}, method='POST'
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        result = json.loads(r.read())
    if result.get('errcode'):
        raise Exception(f'add_material失败: {result}')
    return result['media_id']

def create_draft(token, title, html_content, thumb_media_id):
    payload = {
        'articles': [{
            'title': title,
            'author': 'jimo',
            'digest': '',
            'content': html_content,
            'content_source_url': '',
            'thumb_media_id': thumb_media_id,
            'need_open_comment': 0,
            'only_fans_can_comment': 0
        }]
    }
    data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(
        DRAFT_URL.format(token=token), data=data,
        headers={'Content-Type': 'application/json'}, method='POST'
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())

def clean_title_from_body(html, title):
    """去除正文中的标题重复：去掉<title>标签，去掉body开头重复的h1/p标题"""
    # 去掉<title>xxx</title>
    html = re.sub(r'<title>[^<]*</title>', '', html, flags=re.IGNORECASE)
    if not title:
        return html
    # 去掉纯文本标题（AI直接写在body开头的）
    t = title.strip()
    # 去掉<h1>xxx</h1>或<h2>xxx</h2>（全文范围内，包含样式的）
    html = re.sub(r'<h[12][^>]*>' + re.escape(t) + r'</h[12]>', '', html, flags=re.IGNORECASE)
    # 去掉<p>纯标题文本</p>
    html = re.sub(r'<p[^>]*>' + re.escape(t) + r'</p>', '', html, flags=re.IGNORECASE)
    return html

def beautify_html(html):
    """给HTML内容添加专业排版样式（先替换闭标签，再替换开标签，避免部分匹配问题）"""
    body_style = (
        "font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','LXGW WenKai',"
        "'Noto Serif SC','Hiragino Sans GB','Microsoft YaHei',sans-serif;"
        "font-size:17px;line-height:2;letter-spacing:0.5px;color:#2c2c2c;text-align:justify;"
        "-webkit-font-smoothing:antialiased;"
    )
    p_style = "font-size:17px;line-height:2;text-indent:2em;margin:16px 0;color:#2c2c2c;"
    p_first_style = "font-size:17px;line-height:2;margin:16px 0;color:#2c2c2c;"
    h2_style = (
        "font-size:20px;font-weight:800;color:#fff;"
        "background:linear-gradient(135deg,#e07b2a,#c96a1a);"
        "padding:14px 18px;margin:36px 0 20px 0;border-radius:12px;line-height:1.5;"
        "box-shadow:0 4px 15px rgba(224,123,42,0.3);letter-spacing:1px;text-align:center;"
    )
    h3_style = (
        "font-size:17px;font-weight:700;color:#c96a1a;"
        "background:linear-gradient(to right,#fff8f0,#fffaf5);"
        "padding:12px 16px;margin:28px 0 16px 0;border-left:5px solid #e07b2a;"
        "border-radius:0 10px 10px 0;line-height:1.6;box-shadow:0 2px 10px rgba(224,123,42,0.12);"
    )
    strong_style = "font-weight:700;color:#d44a0a;background:#ffe0b2;padding:0 3px;border-radius:3px;"
    em_style = "font-style:normal;color:#888;background:#f5f5f5;padding:2px 6px;border-radius:4px;"
    img_style = "max-width:100%;height:auto;display:block;margin:20px auto;border-radius:12px;box-shadow:0 4px 20px rgba(0,0,0,0.12);"
    blockquote_style = (
        "border-left:5px solid #4caf50;"
        "background:linear-gradient(135deg,#f6ffed,#fff);"
        "padding:16px 20px;margin:20px 0;border-radius:0 12px 12px 0;"
        "color:#555;font-size:16px;line-height:2;"
        "box-shadow:0 3px 12px rgba(76,175,80,0.15);"
    )
    hr_style = "border:none;text-align:center;margin:32px 0;color:#ccc;font-size:14px;letter-spacing:12px;"

    p_count = [0]

    # 第一步：先把所有结束标签转成特殊占位符（避免部分匹配）
    html = html.replace('</p>', '\x00PEND\x00')
    html = html.replace('</h2>', '\x00H2END\x00')
    html = html.replace('</h3>', '\x00H3END\x00')
    html = html.replace('</strong>', '\x00STRONGEND\x00')
    html = html.replace('</b>', '\x00BEND\x00')
    html = html.replace('</em>', '\x00EMEND\x00')
    html = html.replace('</i>', '\x00IEND\x00')
    html = html.replace('</blockquote>', '\x00BQEND\x00')
    html = html.replace('</ul>', '\x00ULEND\x00')
    html = html.replace('</ol>', '\x00OLEND\x00')
    html = html.replace('</li>', '\x00LIEND\x00')
    html = html.replace('</body>', '\x00BODYEND\x00')
    html = html.replace('</section>', '\x00SECTIONEND\x00')

    # 第二步：处理开始标签
    # p标签（计数器）
    def replace_p_start(m):
        p_count[0] += 1
        style = p_first_style if p_count[0] == 1 else p_style
        return f'<p style="{style}">'
    html = re.sub(r'<p>', replace_p_start, html)

    # h2/h3
    html = re.sub(r'<h2>', f'<h2 style="{h2_style}">', html)
    html = re.sub(r'<h3>', f'<h3 style="{h3_style}">', html)

    # 装饰h2内容
    html = re.sub(r'>([^<]+)\x00H2END\x00', r'>◆ \1 ◆</h2>', html)
    # 装饰h3内容
    html = re.sub(r'>([^<]+)\x00H3END\x00', r'>📍 \1</h3>', html)

    # img
    def replace_img(m):
        tag = m.group(0)
        if 'style=' in tag:
            return re.sub(r'style="[^"]*"', f'style="{img_style}"', tag)
        return tag.replace('<img ', f'<img style="{img_style}" ', 1)
    html = re.sub(r'<img[^>]+/?>', replace_img, html)

    # strong/b/em/i
    html = re.sub(r'<(strong|b)([^>]*)>', lambda m: f'<{m.group(1)}{m.group(2)} style="{strong_style}">', html)
    html = re.sub(r'<(em|i)([^>]*)>', lambda m: f'<{m.group(1)}{m.group(2)} style="{em_style}">', html)

    # blockquote
    html = re.sub(r'<blockquote>', f'<blockquote style="{blockquote_style}">', html)
    html = re.sub(r'\x00BQEND\x00', '💡 </blockquote>', html)

    # hr
    html = re.sub(r'<hr\b', f'<hr style="{hr_style}"', html)

    # body/section
    html = re.sub(r'<body([^>]*)>', f'<body\\1 style="{body_style}">', html)
    html = re.sub(r'<section([^>]*)>', f'<section\\1 style="{body_style}">', html)

    # 第三步：恢复结束标签
    html = html.replace('\x00PEND\x00', '</p>')
    html = html.replace('\x00H2END\x00', '</h2>')
    html = html.replace('\x00H3END\x00', '</h3>')
    html = html.replace('\x00STRONGEND\x00', '</strong>')
    html = html.replace('\x00BEND\x00', '</b>')
    html = html.replace('\x00EMEND\x00', '</em>')
    html = html.replace('\x00IEND\x00', '</i>')
    html = html.replace('\x00BQEND\x00', '</blockquote>')
    html = html.replace('\x00ULEND\x00', '</ul>')
    html = html.replace('\x00OLEND\x00', '</ol>')
    html = html.replace('\x00LIEND\x00', '</li>')
    html = html.replace('\x00BODYEND\x00', '</body>')
    html = html.replace('\x00SECTIONEND\x00', '</section>')

    return html


def _get_text_content(html):
    """提取HTML片段的纯文本内容（用于判断语义）"""
    return re.sub(r'<[^>]+>', '', html).strip()


def restructure_content(html):
    """将连续长段落拆分成带结构的小节，增加小标题（不破坏现有标签结构）"""
    def make_subheading(m):
        p_content = m.group(1)
        text = _get_text_content(p_content)
        if len(text) < 60:
            return m.group(0)
        lead_words = ['美食推荐', '必吃清单', '景点攻略', '交通指南', '住宿推荐',
                      '实用信息', '注意事项', '亮点', '特色', '必吃', '必去',
                      '推荐', '攻略', '打卡', '收藏']
        for w in lead_words:
            if w in text:
                inner_text = _get_text_content(p_content)[:18]
                return f'<h3>{inner_text}</h3><p>{p_content.strip()}</p>'
        return m.group(0)
    # 严格匹配：只匹配普通的纯文本p标签（不含嵌套标签）
    result = re.sub(r'<p>([^<]+)</p>', make_subheading, html)
    return result


def highlight_content(html):
    """给关键信息加粗高亮（仅处理纯文本节点，避免破坏标签结构）"""
    def replace_in_text(m):
        text = m.group(1)
        for word in ['好吃到哭', '绝绝子', '太香了', '爆火', '出片', '宝藏', 'yyds',
                     '封神', '天花板', '绝了', '无敌', '超级赞', '强烈推荐',
                     '必去', '必吃', '值得', '私藏', '隐藏', '小众', '美到窒息']:
            if word in text and f'<strong>{word}</strong>' not in text:
                text = text.replace(word, f'<strong>{word}</strong>')
        def repl_num(m2):
            num_text = m2.group(0)
            return f'<strong>{num_text}</strong>'
        text = re.sub(
            r'[0-9]+[多个几半]+[^\s\.,;!?]{0,5}|[0-9]+[\.。][0-9]+[^\s\.,;!?]{0,3}',
            repl_num, text
        )
        return text
    # 只处理标签之间的纯文本：>text<
    html = re.sub(r'>([^<]+)<', replace_in_text, html)
    return html


def convert_lists(html):
    """将纯文本列表转换成带图标的<ul>列表（仅处理裸文本行）"""
    def make_list(m):
        prefix = m.group(1)
        items_text = m.group(2)
        items = re.split(r'[、，,]\s*', items_text)
        items = [it.strip() for it in items if it.strip() and len(it) > 1]
        clean_items = []
        for it in items:
            if re.match(r'^<[^>]+>', it):
                continue
            clean_items.append(f'<li>👉 {it}</li>')
        if len(clean_items) >= 2:
            return f'{prefix}<ul>{"".join(clean_items)}</ul>'
        return m.group(0)
    html = re.sub(
        r'^([\s\n]*)([\d\u4e00-\u9fff]+[.、)）][^<\n]{5,}(?:[、，,][^<\n]{3,}){2,})',
        make_list, html, flags=re.MULTILINE
    )
    return html


def inject_emoji(html):
    """自动给HTML段落注入emoji，按内容语义在段落开头添加"""
    emoji_map = [
        ('美食', '🍜'), ('小吃', '🥟'), ('甜品', '🍰'), ('火锅', '🍲'),
        ('烧烤', '🍖'), ('烤肉', '🥩'), ('海鲜', '🦐'), ('寿司', '🍣'),
        ('咖啡', '☕'), ('奶茶', '🧋'), ('面包', '🥖'),
        ('蔬菜', '🥦'), ('沙拉', '🥗'), ('素菜', '🥬'),
        ('肉', '🥩'), ('鸡', '🍗'), ('鱼', '🐟'), ('蛋', '🥚'),
        ('茶', '🍵'), ('早茶', '🍵'), ('点心', '🥮'),
        ('旅行', '🧳'), ('旅游', '🗺️'), ('景点', '🏞️'), ('攻略', '📝'),
        ('打卡', '📍'), ('拍照', '📸'), ('酒店', '🏨'), ('民宿', '🏠'),
        ('出行', '✈️'), ('航班', '🛫'), ('火车', '🚄'), ('自驾', '🚗'),
        ('春天', '🌸'), ('樱花', '🌸'), ('桃花', '🌸'), ('油菜花', '🌼'),
        ('日出', '🌅'), ('日落', '🌇'), ('星空', '🌌'), ('海边', '🏖️'),
        ('雪山', '🏔️'), ('森林', '🌲'), ('草原', '🌿'),
        ('古镇', '🏘️'), ('城市', '🏙️'), ('乡村', '🏡'),
        ('文化', '🎎'), ('历史', '📜'), ('传统', '🏮'),
        ('活动', '🎉'), ('节日', '🎊'), ('广交会', '🏛️'),
        ('推荐', '✅'), ('必吃', '🔥'), ('必去', '🔥'), ('人气', '🔥'), ('热门', '🔥'),
        ('好吃到哭', '😋'), ('绝绝子', '👏'), ('太香了', '🤤'), ('爆火', '📈'),
        ('出片', '📷'), ('宝藏', '💎'), ('yyds', '🏆'), ('封神', '👑'),
        ('天花板', '🏆'), ('绝了', '👍'), ('无敌', '💪'), ('超级赞', '🙌'),
        ('强烈推荐', '💯'), ('值得', '✨'), ('私藏', '💎'),
        ('隐藏', '🔮'), ('小众', '🌟'), ('美到窒息', '😍'),
        ('避坑', '⚠️'), ('注意', '❗'), ('提醒', '🔔'),
        ('实用', '💡'), ('技巧', '💡'), ('指南', '📖'),
        ('好处', '👍'), ('特色', '✨'), ('亮点', '💡'),
        ('惊喜', '😲'), ('满足', '😊'), ('幸福', '🥰'),
        ('排队', '⏳'), ('性价比', '💰'), ('免费', '🆓'),
    ]
    emoji_chars = set(e for _, e in emoji_map)

    def add_emoji_to_line(line):
        """如果行内已有emoji则不重复添加，找到第一个关键词对应的emoji插入行首"""
        if any(c in emoji_chars for c in line):
            return line
        for kw, emo in emoji_map:
            if kw in line:
                return emo + ' ' + line
        return line

    def process_tag(match):
        """处理带内容的标签块（p/h2/h3/li/blockquote等），在内部文本前加emoji"""
        tag = match.group(1)  # 标签名
        attrs = match.group(2)  # 属性
        content = match.group(3)  # 内容
        inner_text = re.sub(r'<[^>]+>', '', content)
        text = inner_text.strip()
        if text and any(kw for kw, _ in emoji_map if kw in text):
            for kw, emo in emoji_map:
                if kw in text:
                    # 把emoji插入到标签开始后的第一个文本节点
                    new_content = re.sub(
                        r'([^<]*?)(' + re.escape(kw) + r')',
                        r'\1' + emo + r' \2',
                        content, count=1
                    )
                    return f'<{tag}{attrs}>{new_content}</{tag}>'
        return match.group(0)

    # 只对特定正文标签注入emoji（避免污染样式标签）
    content_tags = ('p', 'h2', 'h3', 'li', 'blockquote', 'div', 'section')
    for t in content_tags:
        html = re.sub(
            rf'<({t})([^>]*)>(.*?)</{t}>',
            process_tag,
            html, flags=re.DOTALL
        )
    return html

def main():
    if len(sys.argv) < 3:
        print('用法: python3 create_draft.py "<标题>" "<HTML文件路径>"')
        sys.exit(1)

    title = sys.argv[1]
    html_arg = sys.argv[2]
    
    # 如果第二个参数是文件路径，读取文件；否则当作HTML内容直接使用
    if os.path.exists(html_arg):
        with open(html_arg, encoding='utf-8') as f:
            html_content = f.read()
        print(f'从文件读取HTML: {html_arg}')
    else:
        html_content = html_arg
        print(f'直接使用HTML内容 (长度: {len(html_content)})')

    print(f'标题: {title}')
    print(f'获取 access_token...')
    token = get_access_token()
    print(f'✅ token获取成功\n')

    # 找所有本地图片路径
    # 从HTML中提取所有本地文件路径（/tmp/xxx.png）
    img_paths = []
    for m in set(re.findall(r'/tmp/[\w\-]+\.png', html_content)):
        if os.path.exists(m):
            img_paths.append(m)
            print(f'  找到图片: {m}')

    if not img_paths:
        print('HTML中未找到本地图片路径（如 /tmp/xxx.png）')
        print('请先生成图片并把路径写入HTML')
        sys.exit(1)

    print(f'\n上传 {len(img_paths)} 张图片...')

    # 处理网络图片URL：先下载到本地，再上传
    url_to_local = {}
    for url in set(re.findall(r'https?://[^\s"\'<>]+\.(?:jpg|jpeg|png|gif|webp)', html_content)):
        fname = os.path.basename(url.split('?')[0])
        local_path = f'/tmp/{fname}'
        try:
            download_img(url, local_path)
            url_to_local[url] = local_path
            img_paths.append(local_path)
        except Exception as e:
            print(f'  下载失败 {url}: {e}')

    # 上传每张图片并建立本地路径->URL的映射
    path_to_url = {}
    for path in img_paths:
        url = upload_img_file(token, path)
        fname = os.path.basename(path)
        print(f'  {fname} -> {url[:60]}')
        path_to_url[path] = url

    # 替换HTML中的网络图片URL为下载后的本地路径（准备上传）
    for url, local_path in url_to_local.items():
        if url in html_content:
            html_content = html_content.replace(url, local_path)
            print(f'  替换网络URL -> 本地路径: {os.path.basename(local_path)}')

    # 替换HTML中的所有本地图片路径为上传后的URL
    for local_path, url in path_to_url.items():
        if local_path in html_content:
            html_content = html_content.replace(local_path, url)
            print(f'  替换本地路径 {os.path.basename(local_path)} -> {url[:40]}...')

    # 兼容旧的占位符格式（COVERIMG_URL / CHAPIMG1_URL）
    for placeholder, url in path_to_url.items():
        fname = os.path.basename(placeholder)
        if 'cover' in fname.lower():
            ph = 'COVERIMG_URL'
        else:
            m = re.search(r'chap(\d+)', fname.lower())
            ph = f'CHAPIMG{m.group(1)}_URL' if m else None
        if ph and ph in html_content:
            html_content = html_content.replace(ph, path_to_url[placeholder])
            print(f'  替换占位符 {ph} -> {path_to_url[placeholder][:40]}...')

    # 上传封面作为永久素材（thumb_media_id）
    cover_path = [p for p in img_paths if 'cover' in p.lower()]
    if cover_path:
        print(f'\n上传封面为永久素材...')
        thumb_media_id = upload_material(token, cover_path[0])
        print(f'  thumb_media_id: {thumb_media_id}')
    else:
        print(f'\n无封面图，使用chap1作为永久素材...')
        # 用add_material上传第一张图作为封面
        thumb_media_id = upload_material(token, img_paths[0])
        print(f'  thumb_media_id: {thumb_media_id}')

    # 去除正文中的标题重复
    print('\n清理标题重复...')
    html_content = clean_title_from_body(html_content, title)
    print('  标题重复已清理')

    # 自动注入emoji
    print('\n注入emoji...')
    html_content = inject_emoji(html_content)
    print('  emoji注入完成')

    # 排版美化
    print('\n排版美化...')
    html_content = beautify_html(html_content)
    print('  排版完成（字体17px、行高1.9、字间距0.5px、两端对齐）')

    # 创建草稿
    print('\n创建草稿...')
    result = create_draft(token, title, html_content, thumb_media_id)

    # 成功判断：无errcode字段 或 errcode==0
    if 'errcode' not in result or result.get('errcode') == 0:
        print(f"✅ 草稿创建成功!")
        print(f"media_id: {result.get('media_id', 'N/A')}")
    else:
        print(f"❌ 草稿创建失败: {result}")
        sys.exit(1)

if __name__ == '__main__':
    import re
    main()
