#!/usr/bin/env python3
"""
修复Typecho文章标题中的引号问题
批量清理已发布文章的标题引号
"""

import xmlrpc.client
import sys
import os

def load_env():
    """加载 .env 文件"""
    config = {}
    
    possible_paths = [
        os.path.join(os.path.dirname(__file__), '..', '.env'),
        os.path.join(os.path.dirname(__file__), '..', '..', '.env'),
        os.path.expanduser('~/.openclaw/workspace/.env'),
    ]
    
    for env_path in possible_paths:
        env_path = os.path.abspath(env_path)
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        if key not in config:
                            config[key.strip()] = value.strip()
    
    return config

def get_client(config):
    """获取 XML-RPC 客户端"""
    XMLRPC_URL = config.get('BLOG_URL', 'http://yuanblog.tk:9980') + config.get('BLOG_XMLRPC', '/index.php/action/xmlrpc')
    return xmlrpc.client.ServerProxy(XMLRPC_URL), config.get('BLOG_USERNAME', 'admin'), config.get('BLOG_PASSWORD', '')

def clean_title(title):
    """清理标题中的引号"""
    if not title:
        return title
    
    original = title
    
    # 清理双引号
    if title.startswith('"') and title.endswith('"'):
        title = title[1:-1]
    # 清理单引号
    elif title.startswith("'") and title.endswith("'"):
        title = title[1:-1]
    # 清理HTML实体
    elif title.startswith('&quot;') and title.endswith('&quot;'):
        title = title[6:-6]
    elif title.startswith('&amp;quot;') and title.endswith('&amp;quot;'):
        title = title[10:-10]
    
    if original != title:
        print(f"  🔧 {original} → {title}")
    
    return title

def fix_all_titles():
    """修复所有文章的标题"""
    config = load_env()
    client, username, password = get_client(config)
    
    print("🔄 开始修复文章标题...")
    print("=" * 60)
    
    try:
        # 获取所有文章
        posts = client.metaWeblog.getRecentPosts('', username, password, 50)
        print(f"📋 找到 {len(posts)} 篇文章")
        
        fixed_count = 0
        
        for post in posts:
            post_id = post['postid']
            original_title = post['title']
            cleaned_title = clean_title(original_title)
            
            # 如果标题被清理过
            if original_title != cleaned_title:
                print(f"\n📝 修复 ID {post_id}:")
                print(f"   原标题: {original_title}")
                print(f"   新标题: {cleaned_title}")
                
                try:
                    # 更新文章
                    post['title'] = cleaned_title
                    result = client.metaWeblog.editPost(post_id, username, password, post, True)
                    
                    if result:
                        print(f"   ✅ 修复成功")
                        fixed_count += 1
                    else:
                        print(f"   ❌ 修复失败")
                        
                except Exception as e:
                    print(f"   ❌ 错误: {e}")
        
        print("\n" + "=" * 60)
        print(f"📊 修复完成：成功修复 {fixed_count}/{len(posts)} 篇文章")
        
        if fixed_count > 0:
            print("\n🔗 建议刷新博客首页查看效果:")
            print("   http://yuanblog.tk:9980/")
        
        return fixed_count
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        return 0

def main():
    """主函数"""
    print("🔧 Typecho 文章标题清理工具")
    print("=" * 60)
    
    if len(sys.argv) > 1 and sys.argv[1] == '--dry-run':
        print("📋 干运行模式（只显示，不执行）")
        config = load_env()
        client, username, password = get_client(config)
        
        posts = client.metaWeblog.getRecentPosts('', username, password, 20)
        
        print(f"\n找到 {len(posts)} 篇文章:")
        for post in posts:
            post_id = post['postid']
            title = post['title']
            cleaned = clean_title(title)
            
            if title != cleaned:
                print(f"  ID {post_id}: {title} → {cleaned}")
            else:
                print(f"  ID {post_id}: {title} (无需清理)")
        
        print(f"\n📝 执行命令进行修复:")
        print("python3 fix_titles.py")
        return
    
    # 执行修复
    fixed = fix_all_titles()
    
    if fixed == 0:
        print("\n🎉 没有需要修复的文章，所有标题都已干净！")

if __name__ == "__main__":
    main()