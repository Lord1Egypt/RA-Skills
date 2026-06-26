# -*- coding: utf-8 -*-
"""
多平台群机器人消息推送
支持：企业微信、钉钉、飞书
配置文件：webhook-config.json
"""
import json
import urllib.request
import base64
import hashlib
import os
import pathlib

# 配置文件路径 - 当前目录下的 webhook-config.json
CONFIG_PATH = pathlib.Path("webhook-config.json")


def load_config():
    """加载配置文件"""
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(
            f"[配置错误] 配置文件不存在: {CONFIG_PATH}\n"
            "请先创建 webhook-config.json 文件，参考 SKILL.md 中的配置格式。"
        )
    
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_key(platform, group_name):
    """根据平台和群名称获取 webhook key"""
    try:
        config = load_config()
    except FileNotFoundError:
        raise  # 直接抛出，让调用方统一处理
    
    platform_lower = platform.lower()
    if platform_lower not in ["wechat", "dingtalk", "feishu"]:
        raise ValueError(f"[参数错误] 不支持的平台: {platform}，仅支持 wechat / dingtalk / feishu")
    
    platform_config = config.get(platform_lower, {})
    group_config = platform_config.get(group_name, {})
    key = group_config.get("key")
    
    if not key:
        raise KeyError(
            f"[配置错误] 未在 webhook-config.json 中找到群 '{group_name}' 的 key。\n"
            f"请在 {platform} 下添加 '{group_name}' 的配置，参考：\n"
            f'  "{group_name}": {{"key": "你的webhook key"}}'
        )
    
    placeholder_keys = ["YOUR_WECHAT_KEY_HERE", "YOUR_DINGTALK_KEY_HERE", "YOUR_FEISHU_KEY_HERE"]
    if key in placeholder_keys:
        raise ValueError(
            f"[配置错误] 群 '{group_name}' 的 key 仍是占位符，请替换为真实的 webhook key。"
        )
    
    return key


# ========== 企业微信 ==========

def send_wechat_text(key, content, mentioned_list=None, mentioned_mobile_list=None):
    """发送企业微信文本消息
    
    Args:
        key: webhook key
        content: 消息内容
        mentioned_list: 被 @ 的用户 userid 列表，如 ["userid1", "userid2"]
        mentioned_mobile_list: 被 @ 的用户手机号列表，如 ["13800001111"]
    
    注意：要 @ 某人，需要在 mentioned_list 或 mentioned_mobile_list 中指定，
    而不是简单地在内容中写 @名字
    """
    url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key}"
    text_data = {"content": content}
    
    if mentioned_list:
        text_data["mentioned_list"] = mentioned_list
    if mentioned_mobile_list:
        text_data["mentioned_mobile_list"] = mentioned_mobile_list
    
    data = {
        "msgtype": "text",
        "text": text_data
    }
    
    req = urllib.request.Request(url, data=json.dumps(data, ensure_ascii=False).encode('utf-8'))
    req.add_header("Content-Type", "application/json; charset=utf-8")
    
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode('utf-8'))


def send_wechat_image(key, image_path):
    """发送企业微信图片消息（base64 + md5 方式）"""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"图片文件不存在: {image_path}")
    
    with open(image_path, 'rb') as f:
        data = f.read()
        md5 = hashlib.md5(data).hexdigest()
        b64 = base64.b64encode(data).decode('utf-8')
    
    url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key}"
    msg = {
        "msgtype": "image",
        "image": {"base64": b64, "md5": md5}
    }
    
    req = urllib.request.Request(url, data=json.dumps(msg).encode('utf-8'))
    req.add_header("Content-Type", "application/json; charset=utf-8")
    
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode('utf-8'))


def send_wechat(group_name, content, at_mobiles=None):
    """发送企业微信消息（从配置文件读取 key）
    
    Args:
        group_name: 群名称（在 webhook-config.json 中配置的名称）
        content: 消息内容
        at_mobiles: 需要 @ 的手机号列表，如 ["13800001111"]
                   这些人的手机号会在消息中显示被 @
    
    示例：
        send_wechat("OpenClawTest", "会议通知", at_mobiles=["13800001111"])
    """
    key = get_key("wechat", group_name)
    
    mentioned_mobile_list = at_mobiles if at_mobiles else None
    
    # 如果内容中有 @xxx 格式但没有提供 at_mobiles，
    # 企业微信不会触发 @ 效果，需要通过 mentioned_mobile_list 来实现
    return send_wechat_text(key, content, mentioned_mobile_list=mentioned_mobile_list)


def send_wechat_image_by_name(group_name, image_path):
    """发送企业微信图片（从配置文件读取 key）"""
    key = get_key("wechat", group_name)
    return send_wechat_image(key, image_path)


# ========== 钉钉 ==========

def send_dingtalk_text(key, content, at_mobiles=None):
    """发送钉钉文本消息"""
    url = f"https://oapi.dingtalk.com/robot/send?access_token={key}"
    data = {
        "msgtype": "text",
        "text": {"content": content},
        "at": {"atMobiles": at_mobiles or []}
    }
    
    req = urllib.request.Request(url, data=json.dumps(data, ensure_ascii=False).encode('utf-8'))
    req.add_header("Content-Type", "application/json; charset=utf-8")
    
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode('utf-8'))


def send_dingtalk_markdown(key, title, content):
    """发送钉钉 Markdown 消息"""
    url = f"https://oapi.dingtalk.com/robot/send?access_token={key}"
    data = {
        "msgtype": "markdown",
        "markdown": {"title": title, "text": content}
    }
    
    req = urllib.request.Request(url, data=json.dumps(data, ensure_ascii=False).encode('utf-8'))
    req.add_header("Content-Type", "application/json; charset=utf-8")
    
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode('utf-8'))


def send_dingtalk_link(key, title, text, message_url, pic_url=""):
    """发送钉钉链接卡片"""
    url = f"https://oapi.dingtalk.com/robot/send?access_token={key}"
    data = {
        "msgtype": "link",
        "link": {
            "title": title,
            "text": text,
            "messageUrl": message_url,
            "picUrl": pic_url
        }
    }
    
    req = urllib.request.Request(url, data=json.dumps(data, ensure_ascii=False).encode('utf-8'))
    req.add_header("Content-Type", "application/json; charset=utf-8")
    
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode('utf-8'))


def send_dingtalk(group_name, content, at_mobiles=None):
    """发送钉钉消息（从配置文件读取 key）"""
    key = get_key("dingtalk", group_name)
    return send_dingtalk_text(key, content, at_mobiles)


# ========== 飞书 ==========

def send_feishu_text(key, content):
    """发送飞书文本消息"""
    url = f"https://open.feishu.cn/open-apis/bot/v2/hook/{key}"
    data = {
        "msg_type": "text",
        "content": {"text": content}
    }
    
    req = urllib.request.Request(url, data=json.dumps(data, ensure_ascii=False).encode('utf-8'))
    req.add_header("Content-Type", "application/json; charset=utf-8")
    
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode('utf-8'))


def send_feishu_post(key, title, content):
    """发送飞书富文本消息"""
    url = f"https://open.feishu.cn/open-apis/bot/v2/hook/{key}"
    data = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": title,
                    "content": [
                        [{"tag": "text", "text": content}]
                    ]
                }
            }
        }
    }
    
    req = urllib.request.Request(url, data=json.dumps(data, ensure_ascii=False).encode('utf-8'))
    req.add_header("Content-Type", "application/json; charset=utf-8")
    
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode('utf-8'))


def send_feishu(group_name, content):
    """发送飞书消息（从配置文件读取 key）"""
    key = get_key("feishu", group_name)
    return send_feishu_text(key, content)


# ========== 主函数 ==========

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 4:
        print("=== 多平台群消息推送 ===")
        print()
        print("用法:")
        print("  企业微信: python webhook_push.py wechat <群名称> <消息>")
        print("  钉钉:     python webhook_push.py dingtalk <群名称> <消息>")
        print("  飞书:     python webhook_push.py feishu <群名称> <消息>")
        print()
        print("示例:")
        print("  python webhook_push.py wechat OpenClawTest 测试消息")
        print("  python webhook_push.py dingtalk 项目群 测试消息")
        print("  python webhook_push.py feishu 项目群 测试消息")
        print()
        print(f"配置文件: {CONFIG_PATH}")
        print()
        print("常见错误:")
        print("  - 配置文件不存在 → 创建 webhook-config.json")
        print("  - 未找到群的key → 在配置文件中添加群配置")
        print("  - key是占位符 → 替换为真实webhook key")
        sys.exit(1)
    
    platform = sys.argv[1].lower()
    group_name = sys.argv[2]
    message = " ".join(sys.argv[3:])
    
    try:
        if platform == "wechat":
            result = send_wechat(group_name, message)
        elif platform == "dingtalk":
            result = send_dingtalk(group_name, message)
        elif platform == "feishu":
            result = send_feishu(group_name, message)
        else:
            print(f"[错误] 不支持的平台: {platform}")
            sys.exit(1)
        
        if result.get("errcode") == 0:
            print(f"[成功] 消息已发送到 {group_name}")
        else:
            print(f"[失败] 企业微信返回错误: {result}")
            sys.exit(1)
    except (KeyError, FileNotFoundError, ValueError) as e:
        print(f"\n[错误] {e}")
        sys.exit(1)