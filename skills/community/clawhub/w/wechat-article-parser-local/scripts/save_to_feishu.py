#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书文章收藏助手 - 增强版
自动提取文章内容并保存到飞书多维表格
"""

import json
import requests
import re
from datetime import datetime
from urllib.parse import urlparse
import subprocess

# 飞书应用配置（从环境变量读取）
import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

APP_ID = os.getenv("FEISHU_APP_ID", "")
APP_SECRET = os.getenv("FEISHU_APP_SECRET", "")
APP_TOKEN = os.getenv("FEISHU_APP_TOKEN", "")
TABLE_ID = os.getenv("FEISHU_TABLE_ID", "")


def get_tenant_access_token():
    """获取 tenant_access_token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {"Content-Type": "application/json"}
    data = {
        "app_id": APP_ID,
        "app_secret": APP_SECRET
    }
    
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    
    if result.get("code") == 0:
        return result.get("tenant_access_token")
    else:
        raise Exception(f"获取 token 失败: {result}")


def detect_source(url):
    """自动识别链接来源"""
    domain = urlparse(url).netloc.lower()
    
    if "zhihu.com" in domain:
        return "知乎"
    elif "mp.weixin.qq.com" in domain or "weixin.qq.com" in domain:
        return "微信公众号"
    elif "toutiao.com" in domain or "jinri" in domain:
        return "今日头条"
    elif "xiaohongshu.com" in domain or "xhs" in domain:
        return "小红书"
    elif "bilibili.com" in domain or "b23.tv" in domain:
        return "B站"
    elif "douyin.com" in domain:
        return "抖音"
    else:
        return "其他"


def extract_article_content(url):
    """
    使用 OpenClaw 的 web_fetch 功能提取文章内容
    返回: (title, content, summary)
    """
    try:
        # 调用 openclaw CLI 的 web_fetch 功能
        # 使用 markdown 模式获取内容
        cmd = [
            "openclaw", "web-fetch",
            "--url", url,
            "--mode", "markdown",
            "--max-chars", "5000"
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            content = result.stdout
            
            # 提取标题（通常在第一行）
            lines = content.split('\n')
            title = lines[0].strip('#').strip() if lines else url
            
            # 生成摘要（取前300字）
            content_text = '\n'.join(lines[1:]).strip()
            summary = content_text[:300] + "..." if len(content_text) > 300 else content_text
            
            print(f"✅ 内容提取成功")
            print(f"   标题: {title}")
            print(f"   正文长度: {len(content_text)} 字符")
            
            return title, content_text, summary
        else:
            print(f"⚠️  web_fetch 失败，尝试备用方法...")
            return extract_with_requests(url)
            
    except Exception as e:
        print(f"⚠️  提取失败: {e}")
        return extract_with_requests(url)


def extract_with_requests(url):
    """备用方法：使用 requests 直接获取"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = response.apparent_encoding
        
        html = response.text
        
        # 提取 title - 多种方法
        title = None
        
        # 方法1: 标准 title 标签
        title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
        if title_match:
            title = title_match.group(1).strip()
        
        # 方法2: 微信公众号专用 - rich_media_title
        if not title or len(title) < 3:
            wechat_title = re.search(r'<h1[^>]*class="rich_media_title"[^>]*>(.*?)</h1>', html, re.IGNORECASE | re.DOTALL)
            if wechat_title:
                title = wechat_title.group(1).strip()
                title = re.sub(r'<[^>]+>', '', title).strip()
        
        # 方法3: meta 标签
        if not title or len(title) < 3:
            og_title = re.search(r'<meta[^>]*property="og:title"[^>]*content="([^"]*)"', html, re.IGNORECASE)
            if og_title:
                title = og_title.group(1).strip()
        
        # 方法4: 微信 msg_title
        if not title or len(title) < 3:
            msg_title = re.search(r'var\s+msg_title\s*=\s*["\']([^"\']+)["\']', html)
            if msg_title:
                title = msg_title.group(1).strip()
        
        # 清理标题
        if title:
            title = re.sub(r'\s*[-_|]\s*(知乎|微信公众号|今日头条).*$', '', title)
            title = title.strip()
        
        # 如果还是没有标题，用 URL
        if not title or len(title) < 2:
            title = None  # 返回 None 让后续处理
        
        # 简单提取正文（移除 HTML 标签）
        content = re.sub(r'<script.*?</script>', '', html, flags=re.DOTALL)
        content = re.sub(r'<style.*?</style>', '', content, flags=re.DOTALL)
        content = re.sub(r'<[^>]+>', '', content)
        content = re.sub(r'\s+', ' ', content).strip()
        
        summary = content[:300] + "..." if len(content) > 300 else content
        
        return title, content, summary
        
    except Exception as e:
        print(f"❌ 备用方法也失败: {e}")
        return None, "", "无法提取内容"


def get_existing_fields(token):
    """获取表格已有的字段列表"""
    api_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/fields"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(api_url, headers=headers)
    result = response.json()

    if result.get("code") == 0:
        items = result.get("data", {}).get("items", [])
        return {item["field_name"]: item for item in items}
    else:
        print(f"   ⚠️  获取字段列表失败: {result}")
        return {}


def ensure_fields_exist(token):
    """检查并自动创建缺失的字段"""
    print("\n🔧 检查表格字段...")

    # 期望的字段定义：field_name -> (type, 说明)
    # 飞书字段类型: 1=文本, 2=数字, 3=单选, 5=日期, 7=复选框, 11=人员, 15=超链接, 13=电话, 17=附件, 18=关联, 20=公式, 22=地理位置
    required_fields = {
        "文本": {"field_name": "文本", "type": 1},          # 文本
        "链接": {"field_name": "链接", "type": 15},         # 超链接
        "来源": {"field_name": "来源", "type": 3},          # 单选
        "保存时间": {"field_name": "保存时间", "type": 5},   # 日期
        "摘要": {"field_name": "摘要", "type": 1},          # 文本
        "正文": {"field_name": "正文", "type": 1},          # 文本
    }

    existing = get_existing_fields(token)

    api_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/fields"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    created_count = 0
    for field_name, field_def in required_fields.items():
        if field_name not in existing:
            response = requests.post(api_url, headers=headers, json=field_def)
            result = response.json()
            if result.get("code") == 0:
                created_count += 1
                print(f"   ✅ 创建字段: {field_name}")
            else:
                print(f"   ❌ 创建字段失败 [{field_name}]: {result.get('msg', '')}")
        else:
            print(f"   ✔️  字段已存在: {field_name}")

    if created_count > 0:
        print(f"   📋 共创建了 {created_count} 个新字段")
    else:
        print(f"   📋 所有字段已就绪")


def clean_empty_rows(token):
    """清理表格中的空白行"""
    print("\n🧹 检查并清理空白行...")

    api_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        # 分页获取所有记录
        empty_ids = []
        page_token = None

        while True:
            params = {"page_size": 100}
            if page_token:
                params["page_token"] = page_token

            response = requests.get(api_url, headers=headers, params=params)
            result = response.json()

            if result.get("code") != 0:
                print(f"   ⚠️  获取记录失败，跳过清理")
                return

            records = result.get("data", {}).get("items", [])

            for record in records:
                record_id = record.get("record_id")
                fields = record.get("fields", {})

                # 检查是否为空白行（标题和链接都为空）
                title_field = fields.get("文本", "")
                link_field = fields.get("链接", {})

                if isinstance(link_field, dict):
                    link_text = link_field.get("link", "")
                else:
                    link_text = str(link_field)

                is_empty = (
                    (not title_field or len(str(title_field).strip()) < 2) and
                    (not link_text or len(link_text.strip()) < 5)
                )

                if is_empty:
                    empty_ids.append(record_id)

            # 检查是否有下一页
            if not result.get("data", {}).get("has_more", False):
                break
            page_token = result.get("data", {}).get("page_token")

        # 批量删除空白行
        if empty_ids:
            delete_url = f"{api_url}/batch_delete"
            delete_headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            # 飞书批量删除最多500条
            for i in range(0, len(empty_ids), 500):
                batch = empty_ids[i:i+500]
                response = requests.post(delete_url, headers=delete_headers, json={"records": batch})
                delete_result = response.json()
                if delete_result.get("code") == 0:
                    print(f"   🗑️  批量删除 {len(batch)} 个空白行")
                else:
                    print(f"   ⚠️  批量删除失败: {delete_result.get('msg', '')}")
            print(f"   ✅ 清理完成，共删除 {len(empty_ids)} 个空白行")
        else:
            print(f"   ✅ 没有空白行，表格整洁")

    except Exception as e:
        print(f"   ⚠️  清理过程出错: {e}")


def save_article_to_feishu(url, title=None, content=None, summary=None):
    """保存文章到飞书多维表格"""
    
    print(f"\n📖 开始处理文章...")
    print(f"   链接: {url}")
    
    # 如果没有提供内容，自动提取
    if not content:
        auto_title, auto_content, auto_summary = extract_article_content(url)
        title = title or auto_title
        content = auto_content
        summary = summary or auto_summary
    
    # 检查标题是否为空
    if not title or len(title.strip()) < 2:
        print(f"\n⚠️  警告：无法自动提取标题！")
        print(f"   建议：手动指定标题")
        print(f"   用法：python feishu_article_saver.py \"{url}\" \"文章标题\"")
        return False
    
    # 获取访问令牌
    token = get_tenant_access_token()

    # 自动检查并创建缺失字段
    ensure_fields_exist(token)

    # 清理空白行
    clean_empty_rows(token)
    
    # 自动识别来源
    source = detect_source(url)
    
    # 准备数据
    current_time = int(datetime.now().timestamp() * 1000)
    
    fields = {
        "文本": title,
        "链接": {
            "link": url
        },
        "来源": source,
        "保存时间": current_time
    }

    # 摘要和正文分开保存
    if summary:
        fields["摘要"] = summary
    if content:
        fields["正文"] = content
    
    # 发送请求
    api_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "fields": fields
    }
    
    response = requests.post(api_url, headers=headers, json=data)
    result = response.json()
    
    if result.get("code") == 0:
        print(f"\n✅ 保存成功！")
        print(f"   📝 标题: {title}")
        print(f"   🏷️  来源: {source}")
        print(f"   📊 摘要: {len(summary) if summary else 0} 字符")
        print(f"   📄 正文: {len(content) if content else 0} 字符")
        return True
    else:
        print(f"\n❌ 保存失败: {result}")
        return False


def main():
    """主函数"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python feishu_article_saver.py <URL> [标题]")
        print("\n示例:")
        print("  python feishu_article_saver.py 'https://mp.weixin.qq.com/s/xxxxx'")
        print("  python feishu_article_saver.py 'https://zhuanlan.zhihu.com/p/123' '自定义标题'")
        return
    
    url = sys.argv[1]
    title = sys.argv[2] if len(sys.argv) > 2 else None
    
    save_article_to_feishu(url, title)


if __name__ == "__main__":
    main()
