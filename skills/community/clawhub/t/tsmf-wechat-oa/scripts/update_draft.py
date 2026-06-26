#!/usr/bin/env python3
"""
微信公众号草稿修改脚本
可以更新已存在的草稿内容
"""

import os
import sys
import json
import requests
import re

# 微信公众号配置 - 从环境变量读取
APP_ID = os.getenv('WECHAT_APP_ID', '')
APP_SECRET = os.getenv('WECHAT_APP_SECRET', '')

if not APP_ID or not APP_SECRET:
    print("⚠️  警告: 未设置微信凭证环境变量")
    print("   请设置: WECHAT_APP_ID 和 WECHAT_APP_SECRET")


def get_access_token():
    """获取 Access Token"""
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}"
    
    try:
        response = requests.get(url, timeout=30)
        result = response.json()
        
        if 'access_token' in result:
            print(f"✅ Access Token 获取成功！")
            return result['access_token']
        else:
            print(f"❌ 获取 Token 失败: {result}")
            return None
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return None


def get_draft_list(access_token, offset=0, count=20):
    """
    获取草稿列表
    API: POST https://api.weixin.qq.com/cgi-bin/draft/batchget
    """
    url = f"https://api.weixin.qq.com/cgi-bin/draft/batchget?access_token={access_token}"
    
    data = {
        "offset": offset,
        "count": count,
        "no_content": 1  # 不返回内容，只返回基本信息
    }
    
    try:
        print(f"📋 获取草稿列表...")
        response = requests.post(
            url,
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        result = response.json()
        
        if 'item' in result:
            print(f"✅ 获取成功，共 {result.get('total_count', 0)} 篇草稿")
            return result['item']
        else:
            print(f"❌ 获取失败: {result}")
            return []
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return []


def get_draft_content(access_token, media_id):
    """
    获取草稿详情
    API: POST https://api.weixin.qq.com/cgi-bin/draft/get
    """
    url = f"https://api.weixin.qq.com/cgi-bin/draft/get?access_token={access_token}"
    
    data = {
        "media_id": media_id
    }
    
    try:
        print(f"📖 获取草稿内容...")
        response = requests.post(
            url,
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        result = response.json()
        
        if 'news_item' in result:
            print(f"✅ 获取成功")
            return result['news_item'][0]  # 返回第一篇
        else:
            print(f"❌ 获取失败: {result}")
            return None
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return None


def update_draft(access_token, media_id, title, content, author="小爪 🐾", digest="", thumb_media_id=None):
    """
    更新草稿
    API: POST https://api.weixin.qq.com/cgi-bin/draft/update
    
    注意：微信的草稿修改实际上是"覆盖"，需要提供完整的文章信息
    """
    url = f"https://api.weixin.qq.com/cgi-bin/draft/update?access_token={access_token}"
    
    # 构建文章数据
    article = {
        "title": title,
        "content": content,
        "author": author,
        "digest": digest,
        "show_cover_pic": 1 if thumb_media_id else 0,
        "need_open_comment": 1,
        "only_fans_can_comment": 0
    }
    
    if thumb_media_id:
        article["thumb_media_id"] = thumb_media_id
    
    data = {
        "media_id": media_id,
        "index": 0,  # 要更新的文章索引，第一篇是 0
        "articles": article
    }
    
    try:
        print(f"✏️ 正在更新草稿...")
        print(f"   Media ID: {media_id}")
        print(f"   标题: {title}")
        
        response = requests.post(
            url,
            data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        result = response.json()
        
        if result.get('errcode') == 0:
            print(f"✅ 草稿更新成功！")
            return True
        else:
            print(f"❌ 更新失败")
            print(f"   错误码: {result.get('errcode', '未知')}")
            print(f"   错误信息: {result.get('errmsg', '未知错误')}")
            return False
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        import traceback
        traceback.print_exc()
        return False


def delete_draft(access_token, media_id):
    """
    删除草稿
    API: POST https://api.weixin.qq.com/cgi-bin/draft/delete
    """
    url = f"https://api.weixin.qq.com/cgi-bin/draft/delete?access_token={access_token}"
    
    data = {
        "media_id": media_id
    }
    
    try:
        print(f"🗑️ 删除草稿: {media_id}")
        response = requests.post(
            url,
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        result = response.json()
        
        if result.get('errcode') == 0:
            print(f"✅ 删除成功！")
            return True
        else:
            print(f"❌ 删除失败: {result}")
            return False
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return False


def markdown_to_html(markdown_content):
    """Markdown 转 HTML"""
    html = markdown_content
    
    # 标题
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    
    # 粗体
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    
    # 斜体
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    
    # 代码块
    html = re.sub(r'```(.+?)```', r'<pre><code>\1</code></pre>', html, flags=re.DOTALL)
    html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)
    
    # 段落
    lines = html.split('\n')
    new_lines = []
    in_paragraph = False
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if in_paragraph:
                new_lines.append('</p>')
                in_paragraph = False
            new_lines.append('')
        elif stripped.startswith('<') and stripped.endswith('>'):
            if in_paragraph:
                new_lines.append('</p>')
                in_paragraph = False
            new_lines.append(line)
        else:
            if not in_paragraph:
                new_lines.append('<p>')
                in_paragraph = True
            new_lines.append(line)
    
    if in_paragraph:
        new_lines.append('</p>')
    
    return '\n'.join(new_lines)


def list_drafts(access_token):
    """列出所有草稿"""
    drafts = get_draft_list(access_token)
    
    if not drafts:
        print("📭 草稿箱为空")
        return
    
    print("\n" + "=" * 60)
    print("📋 草稿列表")
    print("=" * 60)
    
    for idx, draft in enumerate(drafts, 1):
        news_item = draft.get('content', {}).get('news_item', [{}])[0]
        title = news_item.get('title', '无标题')
        author = news_item.get('author', '无作者')
        update_time = draft.get('update_time', '未知')
        media_id = draft.get('media_id', '')
        
        print(f"\n【{idx}】{title}")
        print(f"    作者: {author}")
        print(f"    Media ID: {media_id}")
        print(f"    更新时间: {update_time}")
    
    print("\n" + "=" * 60)
    return drafts


def main():
    """主函数 - 演示功能"""
    print("🚀 微信公众号草稿管理工具")
    print("=" * 60)
    
    # 获取 Access Token
    access_token = get_access_token()
    if not access_token:
        print("❌ 无法获取 Access Token")
        sys.exit(1)
    
    # 显示菜单
    print("\n📋 功能菜单:")
    print("   1. 查看草稿列表")
    print("   2. 查看草稿详情")
    print("   3. 更新草稿")
    print("   4. 删除草稿")
    print("   0. 退出")
    
    # 这里演示：列出草稿
    print("\n📝 正在获取草稿列表...")
    drafts = list_drafts(access_token)
    
    if drafts:
        print(f"\n💡 提示: 使用这些 Media ID 可以更新或删除草稿")
        print(f"   例如: python3 update_draft_demo.py <media_id>")
    
    return True


if __name__ == "__main__":
    # 如果有命令行参数，执行特定操作
    if len(sys.argv) > 1:
        command = sys.argv[1]
        access_token = get_access_token()
        
        if not access_token:
            sys.exit(1)
        
        if command == "list":
            list_drafts(access_token)
        elif command == "update" and len(sys.argv) > 2:
            media_id = sys.argv[2]
            # 这里可以添加更新逻辑
            print(f"更新草稿: {media_id}")
        elif command == "delete" and len(sys.argv) > 2:
            media_id = sys.argv[2]
            delete_draft(access_token, media_id)
        else:
            print("用法:")
            print("  python3 update_draft.py list          # 列出草稿")
            print("  python3 update_draft.py delete <id>   # 删除草稿")
    else:
        main()
