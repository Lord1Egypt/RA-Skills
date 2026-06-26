#!/usr/bin/env python3
"""
修复Typecho文章日期问题
将未来日期的文章改为当前日期
"""

import xmlrpc.client
import sys
import os
from datetime import datetime
from xmlrpc.client import DateTime

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

def parse_xmlrpc_date(date_str):
    """解析XML-RPC日期字符串"""
    try:
        # 格式: 20260328T03:29:00
        year = int(date_str[:4])
        month = int(date_str[4:6])
        day = int(date_str[6:8])
        hour = int(date_str[9:11])
        minute = int(date_str[12:14])
        second = int(date_str[15:17])
        return datetime(year, month, day, hour, minute, second)
    except:
        return None

def is_future_date(date_str, now=None):
    """判断是否是未来日期"""
    if now is None:
        now = datetime.now()
    
    post_date = parse_xmlrpc_date(date_str)
    if not post_date:
        return False
    
    return post_date > now

def fix_future_dates():
    """修复未来日期的文章"""
    config = load_env()
    client, username, password = get_client(config)
    
    print("🔄 开始修复文章日期...")
    print("=" * 60)
    
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")
    print(f"当前时间: {now_str}")
    
    try:
        # 获取所有文章
        posts = client.metaWeblog.getRecentPosts('', username, password, 20)
        print(f"📋 检查 {len(posts)} 篇文章")
        
        fixed_count = 0
        
        for post in posts:
            post_id = post['postid']
            title = post['title'][:40]
            date_str = post.get('dateCreated', '')
            
            if not date_str:
                continue
            
            # 检查是否是未来日期
            if is_future_date(date_str, now):
                print(f"\n📅 发现未来日期文章 ID {post_id}:")
                print(f"   标题: {title}...")
                print(f"   原日期: {date_str}")
                print(f"   当前日期: {now.strftime('%Y%m%dT%H:%M:%S')}")
                
                try:
                    # 更新为当前日期
                    post['dateCreated'] = DateTime(now)
                    result = client.metaWeblog.editPost(post_id, username, password, post, True)
                    
                    if result:
                        print(f"   ✅ 日期修复成功")
                        fixed_count += 1
                    else:
                        print(f"   ❌ 日期修复失败")
                        
                except Exception as e:
                    print(f"   ❌ 错误: {e}")
            else:
                # 正常日期（过去或现在）
                post_date = parse_xmlrpc_date(date_str)
                if post_date:
                    diff = now - post_date
                    if diff.days >= 0:
                        status = f"{diff.days}天前" if diff.days > 0 else f"{diff.seconds//3600}小时前"
                    else:
                        status = f"{-diff.days}天后"
                    print(f"  ID {post_id}: {date_str} ({status})")
        
        print("\n" + "=" * 60)
        print(f"📊 修复完成：成功修复 {fixed_count} 篇未来日期文章")
        
        if fixed_count > 0:
            print("\n🔗 建议刷新博客首页查看效果:")
            print("   http://yuanblog.tk:9980/")
            print("\n⚠️  注意：首页可能有缓存，需要等待一段时间")
        
        return fixed_count
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        return 0

def main():
    """主函数"""
    print("📅 Typecho 文章日期修复工具")
    print("=" * 60)
    print("修复未来日期的文章，使其立即显示在首页")
    
    # 执行修复
    fixed = fix_future_dates()
    
    if fixed == 0:
        print("\n🎉 没有需要修复的文章，所有日期都正常！")

if __name__ == "__main__":
    main()