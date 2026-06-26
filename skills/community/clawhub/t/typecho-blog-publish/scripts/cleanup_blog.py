#!/usr/bin/env python3
"""
Typecho 博客清理工具
- 批量清理重复/测试文章
- 通过修改文章状态实现软删除
"""

import xmlrpc.client
import sys
import os

def load_env():
    """加载 .env 文件"""
    config = {}
    
    # 可能的位置
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

def list_posts_to_keep_and_delete():
    """列出应该保留和删除的文章"""
    config = load_env()
    client, username, password = get_client(config)
    
    # 获取所有文章
    posts = client.metaWeblog.getRecentPosts('', username, password, 50)
    
    print("📋 博客文章分析")
    print("=" * 60)
    
    # 文章分类
    articles_to_keep = []
    articles_to_delete = []
    
    for post in posts:
        post_id = post['postid']
        title = post['title']
        
        # 判断是否应该保留（传递所有文章用于比较）
        if should_keep_article(title, post_id, posts):
            articles_to_keep.append((post_id, title))
        else:
            articles_to_delete.append((post_id, title))
    
    print(f"\n✅ 应该保留的文章 ({len(articles_to_keep)}篇):")
    for post_id, title in sorted(articles_to_keep):
        print(f"  ID {post_id}: {title[:50]}...")
    
    print(f"\n🗑️  应该删除的文章 ({len(articles_to_delete)}篇):")
    for post_id, title in sorted(articles_to_delete):
        print(f"  ID {post_id}: {title[:50]}...")
    
    return articles_to_keep, articles_to_delete

def should_keep_article(title, post_id, all_posts):
    """判断文章是否应该保留"""
    title = str(title)  # 确保是字符串
    
    # 1. 删除明显的测试文章
    if any(test_word in title for test_word in ["测试", "技能更新测试", "测试日期文章"]):
        return False
    
    # 2. 按类别保留最新的一篇
    article_categories = {
        "AI平行代理团队": ["打造你的AI平行代理团队", "AI平行代理"],
        "团子觉醒日记": ["团子觉醒日记"],
        "AI搞钱指南": ["AI搞钱实战指南"],
        "创业文章": ["创业第一天", "系统上线通知", "团子重新上线"]
    }
    
    # 找出每个类别的最新文章（最大ID）
    for category, keywords in article_categories.items():
        for keyword in keywords:
            if keyword in title:
                # 找到同类的所有文章
                same_category = []
                for p in all_posts:
                    p_title = str(p['title'])
                    if any(k in p_title for k in keywords):
                        same_category.append(p)
                
                # 按ID排序，只保留最大ID的那篇
                same_category.sort(key=lambda x: x['postid'], reverse=True)
                
                # 如果这是最新的一篇，保留
                if post_id == same_category[0]['postid']:
                    print(f"  📌 {category}: 保留 ID {post_id} (最新)")
                    return True
                else:
                    print(f"  🗑️  {category}: 删除 ID {post_id} (有更新版本)")
                    return False
    
    # 3. 默认保留（未知类型的文章）
    return True

def soft_delete_post(post_id, reason=""):
    """软删除文章（设为私有状态并添加标记）"""
    config = load_env()
    client, username, password = get_client(config)
    
    try:
        # 1. 获取文章
        post = client.metaWeblog.getPost(post_id, username, password)
        
        # 2. 修改内容（添加删除标记）
        original_content = post.get('description', '')
        deleted_content = f"""
<div style="background-color: #ffe6e6; padding: 10px; border-left: 5px solid #ff6666; margin: 20px 0;">
<strong>⚠️ 此文章已被标记为删除</strong><br>
原因：{reason}<br>
时间：{post.get('dateCreated', '')}<br>
原始标题：{post.get('title', '')}<br>
状态：私有（需要密码访问）
</div>
{original_content}
"""
        
        # 3. 更新文章（设为私有状态）
        post['description'] = deleted_content
        post['title'] = f"[已删除] {post.get('title', '')}"
        
        # Typecho 设为私有文章（首页不显示）
        post['post_status'] = 'private'
        post['wp_password'] = 'deleted_by_tuanzi_2026'  # 私有文章密码
        
        # 禁用互动
        post['mt_allow_pings'] = 0
        post['mt_allow_comments'] = 0
        
        result = client.metaWeblog.editPost(post_id, username, password, post, True)
        
        if result:
            print(f"✅ ID {post_id}: 已设为私有状态")
            return True
        else:
            print(f"❌ ID {post_id}: 操作失败")
            return False
            
    except Exception as e:
        print(f"❌ ID {post_id}: 错误 - {e}")
        return False

def main():
    """主函数"""
    print("🔄 Typecho 博客清理工具")
    print("=" * 60)
    
    if len(sys.argv) > 1 and sys.argv[1] == '--dry-run':
        print("📋 干运行模式（只列出，不执行）")
        keep, delete = list_posts_to_keep_and_delete()
        
        print("\n📝 执行命令进行删除:")
        print("python3 cleanup_blog.py --execute")
        return
    
    elif len(sys.argv) > 1 and sys.argv[1] == '--execute':
        print("🚀 执行清理操作...")
        keep, delete = list_posts_to_keep_and_delete()
        
        # 自动确认（非交互式环境）
        print(f"\n🗑️  开始清理 {len(delete)} 篇文章...")
        success_count = 0
        for post_id, title in delete:
            success = soft_delete_post(post_id, "重复/测试文章清理")
            if success:
                success_count += 1
        
        print(f"\n📊 清理完成：成功标记 {success_count}/{len(delete)} 篇文章")
        
    else:
        print("使用方法:")
        print("  python3 cleanup_blog.py --dry-run    # 列出要删除的文章（不执行）")
        print("  python3 cleanup_blog.py --execute    # 执行清理操作")
        print("\n安全说明:")
        print("  此工具不会永久删除文章，而是将其标记为[已删除]并设为草稿")
        print("  你可以通过Typecho后台恢复这些文章")

if __name__ == "__main__":
    main()