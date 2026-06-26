#!/usr/bin/env python3
"""
Typecho 博客图片上传工具
使用 XML-RPC 和 HTTP POST 上传图片
"""
import xmlrpc.client
import os
import sys
from datetime import datetime

def load_env():
    """加载 .env 文件"""
    config = {}
    env_paths = [
        os.path.expanduser('~/.openclaw/workspace/.env'),
        os.path.join(os.path.dirname(__file__), '..', '.env'),
    ]
    for path in env_paths:
        if os.path.exists(path):
            with open(path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        k, v = line.split('=', 1)
                        config[k.strip()] = v.strip()
    return config

def upload_image(image_path, title=None):
    """
    上传图片到 Typecho 博客
    返回图片 URL
    """
    config = load_env()
    BLOG_URL = config.get('BLOG_URL', 'http://yuanblog.tk:9980')
    USERNAME = config.get('BLOG_USERNAME', 'admin')
    PASSWORD = config.get('BLOG_PASSWORD', '')
    
    if not os.path.exists(image_path):
        print(f"❌ 图片不存在：{image_path}")
        return None
    
    # 读取图片
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    # 获取图片信息
    file_name = os.path.basename(image_path)
    file_type = 'image/jpeg' if image_path.endswith('.jpg') else 'image/png'
    
    if not title:
        title = file_name
    
    print(f"📷 准备上传图片：{file_name}")
    print(f"   大小：{len(image_data)} 字节")
    print(f"   类型：{file_type}")
    
    # Typecho 使用 XML-RPC 的 metaWeblog.newMediaObject
    XMLRPC_URL = f"{BLOG_URL}/index.php/action/xmlrpc"
    server = xmlrpc.client.ServerProxy(XMLRPC_URL)
    
    try:
        # 准备上传数据
        upload_data = {
            'name': file_name,
            'type': file_type,
            'bits': xmlrpc.client.Binary(image_data)
        }
        
        # 调用上传接口
        result = server.metaWeblog.newMediaObject('', USERNAME, PASSWORD, upload_data)
        
        if result:
            url = result.get('url', '')
            print(f"✅ 图片上传成功！")
            print(f"   URL: {url}")
            return url
        else:
            print("❌ 上传失败，返回结果为空")
            return None
            
    except Exception as e:
        print(f"❌ 上传失败：{e}")
        return None

def create_post_with_image(title, content, image_path, categories=None):
    """
    创建带图片的文章
    """
    # 先上传图片
    image_url = upload_image(image_path, title)
    
    if not image_url:
        print("❌ 图片上传失败，中止")
        return False
    
    # 将图片插入内容
    image_html = f'<p><img src="{image_url}" alt="{title}" title="{title}"></p>'
    full_content = image_html + "\n\n" + content
    
    # 发布文章
    from publish_post import publish_post
    return publish_post(title, full_content, categories)

def publish_article_with_image(title, content, image_path, categories=None, tags=None, publish_now=True):
    """
    发布带图片的文章
    
    Args:
        title: 文章标题
        content: 文章内容
        image_path: 图片路径
        categories: 分类列表
        tags: 标签列表
        publish_now: 是否立即发布
    """
    from publish_post import publish_post
    
    # 上传图片
    image_url = upload_image(image_path, title)
    if not image_url:
        return False
    
    # 插入图片到内容开头
    image_html = f'<p><img src="{image_url}" alt="{title}" title="{title}"></p>'
    full_content = image_html + "\n\n" + content
    
    # 发布文章
    return publish_post(title, full_content, categories, tags, publish_now)

if __name__ == "__main__":
    import sys
    
    # 测试上传
    test_image = "/tmp/test_blog_image.jpg"
    
    if len(sys.argv) > 1:
        test_image = sys.argv[1]
    
    if os.path.exists(test_image):
        print("🚀 开始测试图片上传...")
        url = upload_image(test_image, "测试图片")
        if url:
            print(f"\n✅ 测试成功！图片 URL: {url}")
        else:
            print("\n❌ 测试失败")
    else:
        print(f"❌ 测试图片不存在：{test_image}")
