#!/usr/bin/env python3
"""
Typecho 博客自动发布脚本 (增强版)
支持：文件读取、草稿模式、标签、日志记录

使用方法:
    python3 publish_post.py "文章标题" "文章内容" [分类 1，分类 2] [--draft]
    python3 publish_post.py --file article.md [--draft]
    python3 publish_post.py --help

例如:
    python3 publish_post.py "测试文章" "这是测试内容" "AI，生活"
    python3 publish_post.py --file article.md --draft

安全说明:
- 账号密码存储在 .env 文件中，权限为 600 (仅所有者可读写)
- 脚本自动读取 .env 文件中的配置
"""
import xmlrpc.client
from xmlrpc.client import DateTime
import sys
import os
import re
import requests
import urllib.request
import datetime
# from datetime import datetime  # 已删除，避免覆盖模块名

# 日志文件
LOG_FILE = os.path.join(os.path.dirname(__file__), 'publish_log.txt')

def log_message(message, show=True):
    """记录日志到文件和控制台"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    
    if show:
        print(message)
    
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        if show:
            print(f"⚠️  日志记录失败：{str(e)}")

def load_env():
    """加载 .env 文件（支持多级查找）"""
    config = {}
    
    # 可能的位置（从具体到一般）
    possible_paths = [
        os.path.join(os.path.dirname(__file__), '.env'),  # 当前目录
        os.path.join(os.path.dirname(__file__), '..', '.env'),  # 上一级目录
        os.path.join(os.path.dirname(__file__), '..', '..', '.env'),  # 上两级目录
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '.env'),  # 技能目录的父目录
        os.path.expanduser('~/.openclaw/workspace/.env'),  # 工作区根目录
    ]
    
    for env_path in possible_paths:
        env_path = os.path.abspath(env_path)
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        if key not in config:  # 已存在的配置优先
                            config[key.strip()] = value.strip()
    
    return config

def read_file_content(filepath):
    """从文件读取内容"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception as e:
        log_message(f"❌ 读取文件失败：{str(e)}", show=True)
        return None

def parse_markdown_header(content):
    """
    解析 Markdown/YAML 风格的头部
    格式:
    ---
    title: 文章标题
    categories: 分类 1, 分类 2
    tags: 标签 1, 标签 2
    ---
    正文内容...
    """
    if not content.startswith('---'):
        return None, content, None, None
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        return None, content, None, None
    
    header = parts[1].strip()
    body = parts[2].strip()
    
    title = None
    categories = None
    tags = None
    
    for line in header.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            if key == 'title':
                title = value
            elif key == 'categories':
                categories = [c.strip() for c in value.split(',')]
            elif key == 'tags':
                tags = [t.strip() for t in value.split(',')]
    
    return title, body, categories, tags


def markdown_to_html(content):
    """
    将 Markdown 转换为 HTML（增强版 - 修复段落处理）
    
    修复重点：
    1. 正确处理普通段落（不要重复包裹 <p>）
    2. 处理段落之间的空行
    3. 保留列表项内的 Markdown 语法
    """
    import re
    
    lines = content.split('\n')
    html_lines = []
    in_code_block = False
    in_list = False
    list_type = None
    in_paragraph = False
    paragraph_lines = []
    
    def flush_paragraph():
        """将积累的段落的行转换为 HTML"""
        nonlocal paragraph_lines, in_paragraph
        if paragraph_lines:
            text = ' '.join(paragraph_lines)
            # 处理段落内的 Markdown
            text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
            text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
            text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
            # 先处理图片语法 ![alt](url) -> <img src="url" alt="alt">
            text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1">', text)
            # 再处理链接语法 [text](url) -> <a href="url">text</a>
            text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
            text = re.sub(r'~~(.+?)~~', r'<del>\1</del>', text)
            html_lines.append(f'<p>{text}</p>')
            paragraph_lines = []
            in_paragraph = False
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # 代码块处理
        if stripped.startswith('```'):
            flush_paragraph()
            if not in_code_block:
                in_code_block = True
                lang_match = re.match(r'^```(\w*)', stripped)
                lang = lang_match.group(1) if lang_match else ''
                html_lines.append(f'<pre><code class="language-{lang}">')
            else:
                in_code_block = False
                html_lines.append('</code></pre>')
            continue
        
        if in_code_block:
            html_lines.append(line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))
            continue
        
        # 空行 - 结束当前段落或列表
        if not stripped:
            flush_paragraph()
            if in_list:
                html_lines.append(f'</{list_type}>')
                in_list = False
            continue
        
        # 标题 - 结束当前段落和列表
        if re.match(r'^#{1,6}\s', line):
            flush_paragraph()
            if in_list:
                html_lines.append(f'</{list_type}>')
                in_list = False
            
            match = re.match(r'^(#{1,6})\s+(.+)', line)
            if match:
                level = len(match.group(1))
                text = match.group(2)
                html_lines.append(f'<h{level}>{text}</h{level}>')
            continue
        
        # 无序列表
        if re.match(r'^[-*]\s+', line):
            flush_paragraph()
            if not in_list or list_type != 'ul':
                if in_list:
                    html_lines.append(f'</{list_type}>')
                html_lines.append('<ul>')
                in_list = True
                list_type = 'ul'
            
            text = re.sub(r'^[-*]\s+', '', line)
            # 处理列表项内的 Markdown
            text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
            text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
            text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
            html_lines.append(f'<li>{text}</li>')
            continue
        
        # 有序列表
        if re.match(r'^\d+\.\s+', line):
            flush_paragraph()
            if not in_list or list_type != 'ol':
                if in_list:
                    html_lines.append(f'</{list_type}>')
                html_lines.append('<ol>')
                in_list = True
                list_type = 'ol'
            
            text = re.sub(r'^\d+\.\s+', '', line)
            # 处理列表项内的 Markdown
            text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
            text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
            text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
            html_lines.append(f'<li>{text}</li>')
            continue
        
        # 引用块
        if line.startswith('> '):
            flush_paragraph()
            text = line[2:]
            text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
            text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
            html_lines.append(f'<blockquote><p>{text}</p></blockquote>')
            continue
        
        # 普通文本 - 积累到段落
        if not in_paragraph:
            in_paragraph = True
        
        paragraph_lines.append(stripped)
    
    # 清理未结束的内容
    flush_paragraph()
    if in_list:
        html_lines.append(f'</{list_type}>')
    if in_code_block:
        html_lines.append('</code></pre>')
    
    return '\n'.join(html_lines)



def upload_image_to_typecho(image_url_or_path, config=None):
    """上传图片到 Typecho 服务器，返回服务器上的真实 URL"""
    if config is None:
        config = load_env()
    
    XMLRPC_URL = config.get('BLOG_URL', 'http://yuanblog.tk:9980') + config.get('BLOG_XMLRPC', '/index.php/action/xmlrpc')
    USERNAME = config.get('BLOG_USERNAME', 'admin')
    PASSWORD = config.get('BLOG_PASSWORD', '')
    
    server = xmlrpc.client.ServerProxy(XMLRPC_URL)
    
    try:
        if image_url_or_path.startswith('http'):
            log_message(f"📥 下载网络图片：{image_url_or_path}")
            resp = requests.get(image_url_or_path, timeout=10)
            resp.raise_for_status()
            image_data = resp.content
            filename = os.path.basename(image_url_or_path.split('?')[0]) or 'image.png'
        else:
            if not os.path.exists(image_url_or_path):
                log_message(f"❌ 本地图片不存在：{image_url_or_path}")
                return None
            log_message(f"📥 读取本地图片：{image_url_or_path}")
            with open(image_url_or_path, 'rb') as f:
                image_data = f.read()
            filename = os.path.basename(image_url_or_path)
        
        media_obj = {'name': filename, 'type': 'image/png' if filename.endswith('.png') else 'image/jpeg', 'bits': xmlrpc.client.Binary(image_data)}
        
        log_message(f"📤 正在上传图片到服务器：{filename}")
        upload_result = server.metaWeblog.newMediaObject('', USERNAME, PASSWORD, media_obj)
        
        if 'url' in upload_result:
            log_message(f"✅ 图片上传成功：{upload_result['url']}")
            return upload_result['url']
        else:
            log_message(f"❌ 图片上传失败：{upload_result}")
            return None
    except Exception as e:
        log_message(f"❌ 图片上传异常：{str(e)}")
        return None

def process_markdown_images(markdown_content, config=None):
    """处理 Markdown 中的图片链接，上传到服务器并替换"""
    image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    matches = re.findall(image_pattern, markdown_content)
    
    for alt, url in matches:
        should_upload = (not url.startswith('http')) or ('github.com' in url or 'githubusercontent.com' in url)
        if should_upload:
            log_message(f"🔄 处理图片：{url}")
            server_url = upload_image_to_typecho(url, config)
            if server_url:
                old_markdown = f'![{alt}]({url})'
                new_markdown = f'![{alt}]({server_url})'
                markdown_content = markdown_content.replace(old_markdown, new_markdown)
                log_message(f"✅ 图片链接已替换：{server_url}")
    return markdown_content

def get_post_real_url(post_id, config=None):
    """获取文章的lorl真实 URL"""
    if config is None:
        config = load_env()
    
    XMLRPC_URL = config.get('BLOG_URL', 'http://yuanblog.tk:9980') + config.get('BLOG_XMLRPC', '/index.php/action/xmlrpc')
    USERNAME = config.get('BLOG_USERNAME', 'admin')
    PASSWORD = config.get('BLOG_PASSWORD', '')
    server = xmlrpc.client.ServerProxy(XMLRPC_URL)
    
    try:
        post = server.metaWeblog.getPost('', USERNAME, PASSWORD, post_id)
        if 'link' in post or 'permalink' in post:
            return post.get('link') or post.get('permalink')
        blog_url = config.get('BLOG_URL', 'http://yuanblog.tk:9980').rstrip('/')
        return f"{blog_url}/archives/{post_id}"
    except Exception as e:
        log_message(f"⚠️ 获取文章 URL 失败：{str(e)}")
        blog_url = config.get('BLOG_URL', 'http://yuanblog.tk:9980').rstrip('/')
        return f"{blog_url}/archives/{post_id}"


def optimize_markdown(content):
    """
    优化 Markdown 内容，提高 Typecho 兼容性
    """
    # 简单优化：确保段落之间有足够空行
    lines = content.split('\n')
    optimized = []
    
    for i, line in enumerate(lines):
        optimized.append(line)
        
        # 标题后加空行
        if line.startswith('#') and i < len(lines) - 1:
            if not lines[i+1].strip():
                pass
            else:
                optimized.append('')
    
    return '\n'.join(optimized)

def publish_post(title, content, categories=None, tags=None, publish_now=True, config=None):
    """
    通过 XML-RPC 发布文章到 Typecho 博客
    
    Args:
        title: 文章标题
        content: 文章内容
        categories: 分类列表
        tags: 标签列表
        publish_now: True=立即发布，False=保存为草稿
        config: 配置字典
    """
    if config is None:
        config = load_env()
    
    if categories is None:
        categories = ["技术"]
    
    XMLRPC_URL = config.get('BLOG_URL', 'http://yuanblog.tk:9980') + config.get('BLOG_XMLRPC', '/index.php/action/xmlrpc')
    USERNAME = config.get('BLOG_USERNAME', 'admin')
    PASSWORD = config.get('BLOG_PASSWORD', '')
    
    if not PASSWORD:
        log_message("❌ 错误：未找到密码！请检查 .env 文件是否包含 BLOG_PASSWORD。")
        return False
    
    # 清理标题中的引号
    if title.startswith('"') and title.endswith('"'):
        title = title[1:-1]
    elif title.startswith("'") and title.endswith("'"):
        title = title[1:-1]
    
    # 清理中文标点（防止URL问题）
    def clean_title_chars(text):
        replacements = {'：': ':', '；': ';', '，': ',', '。': '.'}
        for ch, en in replacements.items():
            text = text.replace(ch, en)
        return text
    
    cleaned_title = clean_title_chars(title)
    if cleaned_title != title:
        log_message(f"🔧 标题清理：{title} → {cleaned_title}")
        title = cleaned_title
    
    log_message(f"📝 准备发布文章：{title}")
    log_message(f"   分类：{', '.join(categories)}")
    if tags:
        log_message(f"   标签：{', '.join(tags)}")
    log_message(f"   模式：{'立即发布' if publish_now else '草稿'}")
    
    client = xmlrpc.client.ServerProxy(XMLRPC_URL)
    
    try:
        # 1. 登录并获取 Blog ID
        users = client.blogger.getUsersBlogs('', USERNAME, PASSWORD)
        if not users:
            log_message("❌ 登录失败：未找到博客")
            return False
        
        blog_id = users[0]['blogid']
        log_message(f"✅ 登录成功！Blog ID: {blog_id}")
        
                # 2. 将 Markdown 转换为 HTML（Typecho 需要 HTML 格式）
        # 【新增】先处理图片上传：在转换为 HTML 之前
        log_message("🖼️ 开始处理文章中的图片...")
        content = process_markdown_images(content, config)

        html_content = markdown_to_html(content)
        
        # 2. 准备文章数据
        post_data = {
            'title': title,
            'description': html_content,  # 主要内容
            'text': html_content,  # 备用字段
            'mt_text_more': '',  # 更多内容的部分
            'mt_allow_comments': 1,
            'mt_allow_pings': 0,
            'categories': ['default'],  # 强制使用默认分类
            # Typecho 特定字段
            'slug': '',  # URL 别名
            'allowComment': 1,
            'allowPing': 0,
        }
        
        # 添加正确的创建日期（避免未来时间问题）
        
        # 使用本地时间（默认已经是北京时间）
        now = datetime.datetime.now()
        post_data['dateCreated'] = DateTime(now)
        
# 图片已处理

        
        # 添加标签
        if tags:
            post_data['mt_keywords'] = ', '.join(tags)
        
        # 3. 发布文章
        log_message(f"📡 正在发布到：{XMLRPC_URL}")
        post_id = client.metaWeblog.newPost(blog_id, USERNAME, PASSWORD, post_data, publish_now)
        
        blog_url = XMLRPC_URL.replace('/index.php/action/xmlrpc', '')
        log_message(f"✅ 文章发布成功！文章 ID: {post_id}")
    
        # 【新增】获取文章真实 URL
        real_url = get_post_real_url(post_id, config)
        log_message(f"🔗 文章链接：{real_url}")
    # 【新增】检查文章是否可访问
        log_message(f"⚠️ 文章可能为草稿状态：{real_url}")
        log_message("👉 请登录后台手动发布：http://yuanblog.tk:9980/admin/write-post.php?cid=" + str(post_id))
    
    # 移除旧的链接打印（避免重复）
    # link_message = f"🔗 文章链接：http://yuanblog.tk:9980/archives/{post_id}.html"
    # log_message(link_message, show=False)
        log_message(f"🔗 文章链接：{blog_url}/archives/{post_id}.html")
        return True
        
    except xmlrpc.client.Fault as e:
        log_message(f"❌ XML-RPC 错误：{e}")
        return False
    except Exception as e:
        log_message(f"❌ 未知错误：{e}")
        return False

def publish_from_file(filepath, categories=None, tags=None, publish_now=True):
    """从文件读取内容并发布"""
    content = read_file_content(filepath)
    if not content:
        return False
    
    log_message(f"📄 从文件读取：{filepath}")
    
    # 尝试解析头部
    title, body, header_cats, header_tags = parse_markdown_header(content)
    
    if title:
        log_message(f"✅ 解析到头信息：标题={title}")
        # 使用头部的分类和标签（如果提供了的话）
        final_categories = categories if categories else (header_cats or ["技术"])
        final_tags = tags if tags else header_tags
        return publish_post(title, body, final_categories, final_tags, publish_now)
    else:
        # 使用文件名作为标题
        title = os.path.splitext(os.path.basename(filepath))[0]
        log_message(f"⚠️  未找到头部信息，使用文件名作为标题：{title}")
        return publish_post(title, content, categories, tags, publish_now)

def print_help():
    """打印帮助信息"""
    print("""
📝 Typecho 博客自动发布工具

用法:
  python3 publish_post.py "标题" "内容" ["分类 1，分类 2"] [--draft]
  python3 publish_post.py --file article.md [--draft]
  python3 publish_post.py --help

选项:
  --file <文件路径>    从文件读取内容（支持 Markdown 头部）
  --draft             保存为草稿，不立即发布
  --help              显示帮助信息

示例:
  # 直接发布
  python3 publish_post.py "测试文章" "这是内容" "AI，科技"
  
  # 从文件发布
  python3 publish_post.py --file article.md
  
  # 保存为草稿
  python3 publish_post.py --file article.md --draft

文件格式 (可选):
  ---
  title: 文章标题
  categories: 分类 1, 分类 2
  tags: 标签 1, 标签 2
  ---
  正文内容...
""")

if __name__ == "__main__":
    log_message("=" * 60)
    
    config = load_env()
    
    # 检查帮助
    if '--help' in sys.argv or '-h' in sys.argv:
        print_help()
        sys.exit(0)
    
    # 检查参数
    if len(sys.argv) < 2:
        print("❌ 参数不足！")
        print_help()
        sys.exit(1)
    
    # 从文件发布
    if '--file' in sys.argv:
        file_idx = sys.argv.index('--file')
        if file_idx + 1 >= len(sys.argv):
            log_message("❌ 错误：--file 后需跟文件路径")
            sys.exit(1)
        
        filepath = sys.argv[file_idx + 1]
        publish_now = '--draft' not in sys.argv
        
        if os.path.exists(filepath):
            # 解析分类参数
            categories = None
            tags = None
            if len(sys.argv) > file_idx + 2:
                # 检查是否有分类参数（不以 -- 开头）
                next_arg = sys.argv[file_idx + 2]
                if not next_arg.startswith('--'):
                    cats = next_arg.split(',')
                    categories = [c.strip() for c in cats]
            
            success = publish_from_file(filepath, categories, tags, publish_now)
        else:
            log_message(f"❌ 文件不存在：{filepath}")
            sys.exit(1)
    
    # 直接发布
    elif len(sys.argv) >= 3:
        title = sys.argv[1]
        content = sys.argv[2]
        categories = None
        publish_now = '--draft' not in sys.argv
        
        if len(sys.argv) > 3:
            next_arg = sys.argv[3]
            if not next_arg.startswith('--'):
                categories = [c.strip() for c in next_arg.split(',')]
        
        success = publish_post(title, content, categories, publish_now=publish_now, config=config)
    
    else:
        print("❌ 参数错误！")
        print_help()
        sys.exit(1)
    
    log_message("=" * 60)
    sys.exit(0 if success else 1)
