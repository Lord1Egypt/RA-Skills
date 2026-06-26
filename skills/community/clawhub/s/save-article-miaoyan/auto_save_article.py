#!/usr/bin/env python3
"""
微信文章自动保存触发器
监听微信消息中的文章链接，自动调用 save-article-miaoyan skill
"""

import re
import subprocess
import sys

def is_wechat_article_url(text: str) -> str:
    """检测是否是微信公众号文章链接"""
    # 匹配微信公众号文章 URL
    pattern = r'https://mp\.weixin\.qq\.com/s/[a-zA-Z0-9_-]+'
    match = re.search(pattern, text)
    return match.group(0) if match else None

def save_article(url: str) -> dict:
    """调用 save-article-miaoyan skill"""
    skill_path = "/Users/andy/.qclaw/workspace/skills/save-article-miaoyan/save_article.sh"
    
    try:
        result = subprocess.run(
            ["bash", skill_path, url],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            return {
                "success": True,
                "output": result.stdout,
                "url": url
            }
        else:
            return {
                "success": False,
                "error": result.stderr,
                "url": url
            }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "处理超时（30秒）",
            "url": url
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "url": url
        }

def process_message(message: str) -> dict:
    """处理微信消息"""
    # 检测文章链接
    url = is_wechat_article_url(message)
    
    if not url:
        return {
            "detected": False,
            "message": "未检测到微信文章链接"
        }
    
    # 自动保存
    result = save_article(url)
    
    if result["success"]:
        return {
            "detected": True,
            "saved": True,
            "url": url,
            "reply": f"✅ 已保存文章到 Miaoyan/待学习\n\n{result['output']}"
        }
    else:
        return {
            "detected": True,
            "saved": False,
            "url": url,
            "error": result["error"],
            "reply": f"❌ 保存失败: {result['error']}"
        }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 auto_save_article.py '<message_text>'")
        sys.exit(1)
    
    message = sys.argv[1]
    result = process_message(message)
    
    import json
    print(json.dumps(result, ensure_ascii=False, indent=2))
