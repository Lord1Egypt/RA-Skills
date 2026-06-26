#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业微信消息发送脚本
严格按照企业微信文档规范，支持文本、markdown、markdown_v2、图片、图文等多种消息类型
针对text、markdown、markdown_v2类型的超长内容，支持拆分成多个内容进行发送
"""

import json
import urllib.request
import urllib.error
import ssl
import base64
import hashlib
import os
import sys
from pathlib import Path

# 消息长度限制（字节）
MESSAGE_LENGTH_LIMITS = {
    "text": 2048,
    "markdown": 4096,
    "markdown_v2": 4096
}

def send_wechat_message(content, msg_type="text", webhook_url=None, enable_chunking=True):
    """
    发送消息到企业微信
    
    参数:
        content: 消息内容（根据不同的消息类型，格式不同）
        msg_type: 消息类型 (text/markdown/markdown_v2/image/news)
        webhook_url: Webhook地址 (可选，使用默认配置)
        enable_chunking: 是否启用分片发送 (默认True)
    
    返回:
        dict: 发送结果
    """
    # 默认Webhook地址
    if webhook_url is None:
        webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your-key"
    
    # 检查是否需要分片发送
    if enable_chunking and msg_type in MESSAGE_LENGTH_LIMITS:
        content_length = len(content.encode('utf-8'))
        max_length = MESSAGE_LENGTH_LIMITS[msg_type]
        
        if content_length > max_length:
            # 需要分片发送
            return send_chunked_message(content, msg_type, webhook_url)
    
    # 构造消息数据
    message_data = construct_message_data(content, msg_type)
    
    if message_data is None:
        return {
            "success": False,
            "error": f"消息格式错误: 不支持的消息类型或内容格式"
        }
    
    try:
        # 发送HTTP请求
        data = json.dumps(message_data).encode('utf-8')
        req = urllib.request.Request(
            webhook_url,
            data=data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        # 创建SSL上下文 - 使用安全的默认验证
        ssl_context = ssl.create_default_context()
        
        # 注意：企业微信的Webhook使用官方证书，应该使用默认验证
        # 如果需要自定义CA证书，可以取消下面这行的注释，并指定正确的证书路径
        # ssl_context = ssl.create_default_context(cafile="/path/to/custom/ca-bundle.crt")
        
        with urllib.request.urlopen(req, timeout=10, context=ssl_context) as response:
            result = json.loads(response.read().decode('utf-8'))
        
        # 检查发送结果
        if result.get('errcode') == 0:
            return {
                "success": True,
                "message": "消息发送成功",
                "data": result
            }
        else:
            return {
                "success": False,
                "error": f"消息发送失败: {result.get('errmsg', '未知错误')}",
                "data": result
            }
            
    except urllib.error.URLError as e:
        return {
            "success": False,
            "error": f"网络连接失败: {e.reason}"
        }
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": f"JSON解析失败: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"发送异常: {str(e)}"
        }

def send_chunked_message(content, msg_type, webhook_url):
    """
    分片发送长消息
    
    参数:
        content: 长消息内容
        msg_type: 消息类型 (text/markdown/markdown_v2)
        webhook_url: Webhook地址
    
    返回:
        dict: 分片发送结果
    """
    results = []
    max_length = MESSAGE_LENGTH_LIMITS[msg_type]
    
    # 按长度分片
    chunks = []
    content_bytes = content.encode('utf-8')
    
    while len(content_bytes) > max_length:
        # 截取前max_length字节
        chunk_bytes = content_bytes[:max_length]
        # 解码为字符串，如果遇到截断的UTF-8字符则忽略错误
        chunk = chunk_bytes.decode('utf-8', errors='ignore')
        chunks.append(chunk)
        # 移除已处理的内容
        content_bytes = content_bytes[max_length:]
    
    # 添加剩余内容
    if content_bytes:
        chunk = content_bytes.decode('utf-8', errors='ignore')
        chunks.append(chunk)
    
    # 发送每片内容
    for i, chunk in enumerate(chunks):
        # 添加分片标记
        if i == 0:
            # 第一片
            marked_chunk = f"📋 消息分片（第1/{len(chunks)}）\n\n{chunk}"
        elif i == len(chunks) - 1:
            # 最后一片
            marked_chunk = f"{chunk}\n\n✅ 消息结束（共{len(chunks)}片）"
        else:
            # 中间片
            marked_chunk = f"📋 消息分片（第{i+1}/{len(chunks)}）\n\n{chunk}"
        
        # 发送分片
        result = send_wechat_message(marked_chunk, msg_type, webhook_url, enable_chunking=False)
        results.append(result)
    
    # 返回整体结果
    successful = sum(1 for r in results if r["success"])
    total = len(results)
    
    if successful == total:
        return {
            "success": True,
            "message": f"分片发送成功（共{total}片）",
            "chunk_count": total,
            "results": results
        }
    else:
        return {
            "success": False,
            "error": f"分片发送部分失败（成功{successful}/{total}片）",
            "chunk_count": total,
            "results": results
        }

def construct_message_data(content, msg_type):
    """
    构造消息数据
    
    参数:
        content: 消息内容
        msg_type: 消息类型
    
    返回:
        dict: 消息数据
    """
    if msg_type == "text":
        # 文本消息
        return {
            "msgtype": "text",
            "text": {
                "content": content,
                "mentioned_list": ["@all"],
                "mentioned_mobile_list": ["@all"]
            }
        }
    
    elif msg_type == "markdown":
        # markdown消息
        return {
            "msgtype": "markdown",
            "markdown": {
                "content": content
            }
        }
    
    elif msg_type == "markdown_v2":
        # markdown_v2消息
        if isinstance(content, dict):
            # 如果content是字典，包含template_id和template_data
            return {
                "msgtype": "markdown_v2",
                "markdown_v2": content
            }
        else:
            # 如果只是字符串内容
            return {
                "msgtype": "markdown_v2",
                "markdown_v2": {
                    "content": content
                }
            }
    
    elif msg_type == "image":
        # 图片消息
        image_data = process_image(content)
        if image_data:
            return {
                "msgtype": "image",
                "image": image_data
            }
        return None
    
    elif msg_type == "news":
        # 图文消息
        if isinstance(content, list):
            # content是articles列表
            return {
                "msgtype": "news",
                "news": {
                    "articles": content
                }
            }
        elif isinstance(content, dict):
            # content是单个article
            return {
                "msgtype": "news",
                "news": {
                    "articles": [content]
                }
            }
        return None
    
    else:
        return None

def process_image(image_path):
    """
    处理图片文件
    
    参数:
        image_path: 图片路径或URL
    
    返回:
        dict: 图片数据 (base64和md5)
    """
    try:
        # 判断是本地文件还是URL
        if image_path.startswith(('http://', 'https://')):
            # 从URL下载图片
            with urllib.request.urlopen(image_path, timeout=10) as response:
                image_content = response.read()
        else:
            # 读取本地图片文件
            if not os.path.exists(image_path):
                return None
            
            with open(image_path, 'rb') as f:
                image_content = f.read()
        
        # 计算MD5值
        md5_hash = hashlib.md5(image_content).hexdigest()
        
        # 编码为base64
        base64_content = base64.b64encode(image_content).decode('utf-8')
        
        return {
            "base64": base64_content,
            "md5": md5_hash
        }
        
    except Exception as e:
        print(f"图片处理失败: {e}")
        return None

def create_news_article(title, description, url, picurl):
    """
    创建图文消息的article
    
    参数:
        title: 标题
        description: 描述
        url: 跳转链接
        picurl: 图片链接
    
    返回:
        dict: article数据
    """
    return {
        "title": title[:128],  # 标题最长128字节
        "description": description[:512],  # 描述最长512字节
        "url": url,
        "picurl": picurl
    }

def main():
    """
    主函数 - 命令行调用
    """
    if len(sys.argv) < 3:
        print("使用方法: python send_message.py <消息类型> <消息内容> [Webhook地址]")
        print("消息类型: text, markdown, markdown_v2, image, news")
        print("示例:")
        print("  python send_message.py text \"测试消息\"")
        print("  python send_message.py markdown \"**标题**\\n内容\"")
        print("  python send_message.py image /path/to/image.png")
        print("  python send_message.py news \"标题\" \"描述\" \"https://example.com\" \"https://example.com/image.png\"")
        print("  python send_message.py text \"消息\" \"https://your-webhook\"")
        sys.exit(1)
    
    # 解析参数
    msg_type = sys.argv[1].lower()
    content = sys.argv[2]
    webhook_url = sys.argv[3] if len(sys.argv) > 3 else None
    
    # 处理特殊消息类型
    if msg_type == "news" and len(sys.argv) > 5:
        # 图文消息需要4个参数
        title = sys.argv[2]
        description = sys.argv[3]
        url = sys.argv[4]
        picurl = sys.argv[5]
        webhook_url = sys.argv[6] if len(sys.argv) > 6 else None
        
        content = create_news_article(title, description, url, picurl)
    
    # 发送消息
    result = send_wechat_message(content, msg_type, webhook_url)
    
    # 输出结果
    if result["success"]:
        print("✅ 消息发送成功！")
        print(f"📤 发送类型: {msg_type}")
        if "chunk_count" in result:
            print(f"📤 分片数量: {result['chunk_count']}")
        print(f"📤 发送内容: {str(content)[:50]}...")
    else:
        print(f"❌ 消息发送失败: {result['error']}")
        if "results" in result:
            print("分片发送详情:")
            for i, r in enumerate(result["results"]):
                status = "成功" if r["success"] else "失败"
                print(f"  第{i+1}片: {status}")
        sys.exit(1)

if __name__ == "__main__":
    main()