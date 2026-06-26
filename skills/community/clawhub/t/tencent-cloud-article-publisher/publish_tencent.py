#!/usr/bin/env python3
"""腾讯云开发者社区文章发布脚本"""
import requests
import json
import re
import sys

def md_to_html(md_text):
    """简单 Markdown → HTML 转换"""
    html = md_text
    # 粗体 **text** → <strong>text</strong>
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    # 粗体 __text__ → <strong>text</strong>
    html = re.sub(r'__(.+?)__', r'<strong>\1</strong>', html)
    # 斜体 *text* → <em>text</em>
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    # 行内代码 `code` → <code>code</code>
    html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)
    # 换行 → <br/>
    html = html.replace('\n\n', '</p><p>').replace('\n', '<br/>')
    return f'<p>{html}</p>'

def publish_article(title, content_md, cookie_str, classify_ids=None):
    """直接发布文章到腾讯云开发者社区"""
    if classify_ids is None:
        classify_ids = [149]  # 默认技术类
    
    # 转换格式
    content_html = md_to_html(content_md)
    plain_text = re.sub(r'[*_`#>\[\]]', '', content_md)  # 纯文本
    
    # 生成摘要
    summary = content_md[:200].strip() if len(content_md) > 200 else content_md.strip()
    
    url = "https://cloud.tencent.com/developer/api/article/addArticle"
    headers = {
        "Cookie": cookie_str,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Referer": "https://cloud.tencent.com/developer/article/write-new",
        "Origin": "https://cloud.tencent.com",
    }
    payload = {
        "title": title,
        "content": content_html,
        "plain": plain_text,
        "summary": summary,
        "userSummary": summary,
        "sourceType": 1,
        "isOriginal": True,
        "classifyIds": classify_ids,
        "openComment": 1,
        "closeTextLink": 0
    }
    
    print(f"发布标题: {title}")
    print(f"内容长度: {len(content_md)} 字符")
    
    resp = requests.post(url, headers=headers, json=payload, timeout=15)
    result = resp.json()
    
    if "articleId" in result:
        article_id = result["articleId"]
        article_url = f"https://cloud.tencent.com/developer/article/{article_id}"
        print(f"✅ 发布成功！")
        print(f"   articleId: {article_id}")
        print(f"   URL: {article_url}")
        return {"success": True, "articleId": article_id, "url": article_url}
    else:
        print(f"❌ 发布失败: {result}")
        return {"success": False, "error": result.get("msg", "Unknown error")}

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python3 publish_tencent.py <标题> <正文> [cookie]")
        sys.exit(1)
    
    title = sys.argv[1]
    content = sys.argv[2]
    cookie = sys.argv[3] if len(sys.argv) > 3 else None
    
    if not cookie:
        print("请提供 Cookie 参数")
        sys.exit(1)
    
    result = publish_article(title, content, cookie)
    sys.exit(0 if result["success"] else 1)
