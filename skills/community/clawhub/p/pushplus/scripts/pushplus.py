#!/usr/bin/env python3
"""
PushPlus 消息推送脚本
支持多种推送渠道：微信、邮件、短信、企业微信、钉钉、飞书等

更新日志:
- 2026-05: 新增 clawbot (微信ClawBot) 渠道
- 2025-01: 新增多渠道发送接口，webhook参数改为option（兼容旧参数），新增voice/app/extension渠道
"""

import argparse
import json
import sys
import os
import urllib.request
import urllib.error
from typing import Optional, Dict, Any, List


# API 基础地址
API_BASE_URL = "https://www.pushplus.plus/send"
API_BATCH_URL = "https://www.pushplus.plus/batchSend"

# 环境变量名
ENV_TOKEN = "PUSHPLUS_TOKEN"
VALID_TEMPLATES = {"html", "txt", "json", "markdown", "cloudMonitor", "jenkins", "route", "pay"}
VALID_CHANNELS = {"wechat", "webhook", "cp", "mail", "sms", "extension", "voice", "app", "clawbot"}


def get_token_from_env() -> Optional[str]:
    """
    从环境变量获取 Token
    
    Returns:
        Token 字符串或 None
    """
    return os.environ.get(ENV_TOKEN)


def _validate_non_empty_text(field_name: str, value: Optional[str]) -> str:
    """校验必填文本参数"""
    if value is None or not str(value).strip():
        raise ValueError(f"{field_name} 不能为空")
    return str(value).strip()


def _validate_template(template: str) -> str:
    """校验模板类型"""
    normalized_template = _validate_non_empty_text("template", template)
    if normalized_template not in VALID_TEMPLATES:
        raise ValueError(f"template 不合法，可选值: {', '.join(sorted(VALID_TEMPLATES))}")
    return normalized_template


def _validate_channel(channel: str) -> str:
    """校验单渠道类型"""
    normalized_channel = _validate_non_empty_text("channel", channel)
    if normalized_channel not in VALID_CHANNELS:
        raise ValueError(f"channel 不合法，可选值: {', '.join(sorted(VALID_CHANNELS))}")
    return normalized_channel


def _validate_channels(channels: List[str]) -> List[str]:
    """校验多渠道参数"""
    if not channels:
        raise ValueError("channels 不能为空列表")

    normalized_channels = []
    for channel in channels:
        normalized_channels.append(_validate_channel(channel))
    return normalized_channels


def _validate_options_length(channels: List[str], options: Optional[List[str]]) -> None:
    """校验多渠道配置参数数量"""
    if options is None:
        return
    if len(options) != len(channels):
        raise ValueError("options 数量必须与 channels 数量一致；若某个渠道无需参数，请保留空位")


def send_message(
    token: str,
    content: str,
    title: Optional[str] = None,
    topic: Optional[str] = None,
    template: str = "html",
    channel: str = "wechat",
    webhook: Optional[str] = None,
    option: Optional[str] = None,
    callback_url: Optional[str] = None,
    timestamp: Optional[int] = None,
    to: Optional[str] = None,
    pre: Optional[str] = None,
    verbose: bool = False
) -> Dict[str, Any]:
    """
    发送 PushPlus 消息
    
    Args:
        token: 用户 Token 或消息 Token
        content: 消息内容
        title: 消息标题（可选）
        topic: 群组编码，用于一对多消息（可选）
        template: 消息模板，默认 html，可选 txt, json, markdown, cloudMonitor, jenkins, route, pay
        channel: 推送渠道，默认 wechat，可选 webhook, cp, mail, sms, extension, voice, app, clawbot
        webhook: Webhook 编码（已废弃，请使用 option 参数，但为兼容保留）
        option: 渠道配置参数（原 webhook 参数，多个渠道用逗号分隔）
        callback_url: 回调地址（可选）
        timestamp: 时间戳（毫秒），用于防重复（可选）
        to: 好友令牌，支持多人（逗号分隔），实名用户最多10人，会员100人
        pre: 预处理编码（可选）
        verbose: 是否打印详细信息
        
    Returns:
        API 返回的 JSON 数据
    """
    normalized_token = _validate_non_empty_text("token", token)
    normalized_content = _validate_non_empty_text("content", content)
    normalized_template = _validate_template(template)
    normalized_channel = _validate_channel(channel)

    # 构建请求数据
    payload = {
        "token": normalized_token,
        "content": normalized_content,
        "template": normalized_template,
        "channel": normalized_channel
    }
    
    if title:
        payload["title"] = title
    if topic:
        payload["topic"] = topic
    
    # option 优先，兼容 webhook 参数
    if option:
        payload["option"] = option
    elif webhook:
        payload["option"] = webhook
        
    if callback_url:
        payload["callbackUrl"] = callback_url
    if timestamp:
        payload["timestamp"] = timestamp
    if to:
        payload["to"] = to
    if pre:
        payload["pre"] = pre
    
    # 设置请求头
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "PushPlus-Python-Script/1.1"
    }
    
    # 编码数据
    data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    
    if verbose:
        print(f"请求 URL: {API_BASE_URL}")
        print(f"请求数据: {data.decode('utf-8')}")
    
    # 创建请求
    req = urllib.request.Request(
        API_BASE_URL,
        data=data,
        headers=headers,
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            if verbose:
                print(f"响应状态: {response.status}")
                print(f"响应内容: {json.dumps(result, ensure_ascii=False, indent=2)}")
            return result
    except urllib.error.HTTPError as e:
        error_msg = f"HTTP 错误: {e.code}"
        try:
            error_body = json.loads(e.read().decode('utf-8'))
            error_msg += f" - {error_body.get('msg', '')}"
        except:
            pass
        raise Exception(error_msg)
    except urllib.error.URLError as e:
        raise Exception(f"URL 错误: {e.reason}")
    except Exception as e:
        raise Exception(f"请求失败: {str(e)}")


def send_batch_message(
    token: str,
    content: str,
    channels: List[str],
    title: Optional[str] = None,
    topic: Optional[str] = None,
    template: str = "html",
    options: Optional[List[str]] = None,
    callback_url: Optional[str] = None,
    timestamp: Optional[int] = None,
    to: Optional[str] = None,
    pre: Optional[str] = None,
    verbose: bool = False
) -> Dict[str, Any]:
    """
    多渠道发送 PushPlus 消息（batchSend 接口）
    
    Args:
        token: 用户 Token 或消息 Token
        content: 消息内容
        channels: 渠道列表，如 ["wechat", "webhook", "extension"]
        title: 消息标题（可选）
        topic: 群组编码（可选）
        template: 消息模板，默认 html
        options: 渠道配置参数列表，与 channels 一一对应
        callback_url: 回调地址（可选）
        timestamp: 时间戳（毫秒）（可选）
        to: 好友令牌（可选）
        pre: 预处理编码（可选）
        verbose: 是否打印详细信息
        
    Returns:
        API 返回的 JSON 数据，包含各渠道的消息流水号
    """
    normalized_token = _validate_non_empty_text("token", token)
    normalized_content = _validate_non_empty_text("content", content)
    normalized_template = _validate_template(template)
    normalized_channels = _validate_channels(channels)
    _validate_options_length(normalized_channels, options)

    # 构建请求数据
    payload = {
        "token": normalized_token,
        "content": normalized_content,
        "template": normalized_template,
        "channel": ",".join(normalized_channels)
    }
    
    if title:
        payload["title"] = title
    if topic:
        payload["topic"] = topic
    if options:
        payload["option"] = ",".join(options)
    if callback_url:
        payload["callbackUrl"] = callback_url
    if timestamp:
        payload["timestamp"] = timestamp
    if to:
        payload["to"] = to
    if pre:
        payload["pre"] = pre
    
    # 设置请求头
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "PushPlus-Python-Script/1.1"
    }
    
    # 编码数据
    data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    
    if verbose:
        print(f"请求 URL: {API_BATCH_URL}")
        print(f"请求数据: {data.decode('utf-8')}")
    
    # 创建请求
    req = urllib.request.Request(
        API_BATCH_URL,
        data=data,
        headers=headers,
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            if verbose:
                print(f"响应状态: {response.status}")
                print(f"响应内容: {json.dumps(result, ensure_ascii=False, indent=2)}")
            return result
    except urllib.error.HTTPError as e:
        error_msg = f"HTTP 错误: {e.code}"
        try:
            error_body = json.loads(e.read().decode('utf-8'))
            error_msg += f" - {error_body.get('msg', '')}"
        except:
            pass
        raise Exception(error_msg)
    except urllib.error.URLError as e:
        raise Exception(f"URL 错误: {e.reason}")
    except Exception as e:
        raise Exception(f"请求失败: {str(e)}")


# ==================== 便捷函数 ====================

def send_simple_message(token: str, content: str, title: str = "通知") -> Dict[str, Any]:
    """
    发送简单消息（使用默认参数）
    
    Args:
        token: 用户 Token
        content: 消息内容
        title: 消息标题
        
    Returns:
        API 返回结果
    """
    return send_message(token=token, content=content, title=title)


def send_wechat_message(token: str, content: str, title: str = "通知", topic: str = None) -> Dict[str, Any]:
    """
    发送微信消息
    
    Args:
        token: 用户 Token
        content: 消息内容
        title: 消息标题
        topic: 群组编码（可选）
        
    Returns:
        API 返回结果
    """
    return send_message(
        token=token,
        content=content,
        title=title,
        topic=topic,
        channel="wechat"
    )


def send_email_message(token: str, content: str, title: str, topic: str = None) -> Dict[str, Any]:
    """
    发送邮件消息
    
    Args:
        token: 用户 Token
        content: 邮件内容
        title: 邮件标题
        topic: 群组编码（可选）
        
    Returns:
        API 返回结果
    """
    return send_message(
        token=token,
        content=content,
        title=title,
        topic=topic,
        channel="mail"
    )


def send_markdown_message(token: str, content: str, title: str = "通知", topic: str = None) -> Dict[str, Any]:
    """
    发送 Markdown 格式消息
    
    Args:
        token: 用户 Token
        content: Markdown 格式内容
        title: 消息标题
        topic: 群组编码（可选）
        
    Returns:
        API 返回结果
    """
    return send_message(
        token=token,
        content=content,
        title=title,
        topic=topic,
        template="markdown"
    )


def send_json_message(token: str, data: dict, title: str = "JSON通知", topic: str = None) -> Dict[str, Any]:
    """
    发送 JSON 格式消息
    
    Args:
        token: 用户 Token
        data: 字典数据
        title: 消息标题
        topic: 群组编码（可选）
        
    Returns:
        API 返回结果
    """
    content = json.dumps(data, ensure_ascii=False, indent=2)
    return send_message(
        token=token,
        content=content,
        title=title,
        topic=topic,
        template="json"
    )


def send_dingtalk_message(token: str, content: str, title: str = "通知", webhook: str = None) -> Dict[str, Any]:
    """
    发送钉钉消息（通过 webhook 渠道）
    
    Args:
        token: 用户 Token
        content: 消息内容
        title: 消息标题
        webhook: 钉钉 webhook 编码（在 PushPlus 中配置）
        
    Returns:
        API 返回结果
    """
    return send_message(
        token=token,
        content=content,
        title=title,
        channel="webhook",
        option=webhook
    )


def send_feishu_message(token: str, content: str, title: str = "通知", webhook: str = None) -> Dict[str, Any]:
    """
    发送飞书消息（通过 webhook 渠道）
    
    Args:
        token: 用户 Token
        content: 消息内容
        title: 消息标题
        webhook: 飞书 webhook 编码（在 PushPlus 中配置）
        
    Returns:
        API 返回结果
    """
    return send_message(
        token=token,
        content=content,
        title=title,
        channel="webhook",
        option=webhook
    )


def send_work_wechat_message(token: str, content: str, title: str = "通知", webhook: str = None) -> Dict[str, Any]:
    """
    发送企业微信消息（通过 webhook 渠道）
    
    Args:
        token: 用户 Token
        content: 消息内容
        title: 消息标题
        webhook: 企业微信 webhook 编码（在 PushPlus 中配置）
        
    Returns:
        API 返回结果
    """
    return send_message(
        token=token,
        content=content,
        title=title,
        channel="webhook",
        option=webhook
    )


def send_sms_message(token: str, content: str, title: str = "短信通知") -> Dict[str, Any]:
    """
    发送短信消息（需要积分，1条短信=10积分=0.1元）
    
    Args:
        token: 用户 Token
        content: 短信内容
        title: 短信标题
        
    Returns:
        API 返回结果
    """
    return send_message(
        token=token,
        content=content,
        title=title,
        channel="sms"
    )


def send_voice_message(token: str, content: str, title: str = "语音通知") -> Dict[str, Any]:
    """
    发送语音消息（需要积分，1条语音=30积分=0.3元）
    
    Args:
        token: 用户 Token
        content: 语音内容
        title: 语音标题
        
    Returns:
        API 返回结果
    """
    return send_message(
        token=token,
        content=content,
        title=title,
        channel="voice"
    )


def send_app_message(token: str, content: str, title: str = "通知") -> Dict[str, Any]:
    """
    发送 App 渠道消息（支持安卓、鸿蒙、iOS）
    
    Args:
        token: 用户 Token
        content: 消息内容
        title: 消息标题
        
    Returns:
        API 返回结果
    """
    return send_message(
        token=token,
        content=content,
        title=title,
        channel="app"
    )


def send_extension_message(token: str, content: str, title: str = "通知") -> Dict[str, Any]:
    """
    发送插件渠道消息（浏览器扩展插件、桌面应用程序）
    
    Args:
        token: 用户 Token
        content: 消息内容
        title: 消息标题
        
    Returns:
        API 返回结果
    """
    return send_message(
        token=token,
        content=content,
        title=title,
        channel="extension"
    )


def send_template_message(token: str, content: str, title: str, template: str, **kwargs) -> Dict[str, Any]:
    """
    发送模板消息
    
    Args:
        token: 用户 Token
        content: 消息内容
        title: 消息标题
        template: 模板类型（html, txt, json, markdown, cloudMonitor, jenkins, route, pay）
        **kwargs: 其他参数（topic, channel, option 等）
        
    Returns:
        API 返回结果
    """
    return send_message(
        token=token,
        content=content,
        title=title,
        template=template,
        **kwargs
    )


def main():
    """命令行入口点"""
    parser = argparse.ArgumentParser(
        description='PushPlus 消息推送工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s -t YOUR_TOKEN -c "消息内容"
  %(prog)s -t YOUR_TOKEN -c "消息内容" --title "消息标题"
  %(prog)s -t YOUR_TOKEN -c "消息内容" --channel mail --title "邮件标题"
  %(prog)s -t YOUR_TOKEN -c "# Markdown内容" --template markdown
  %(prog)s -t YOUR_TOKEN -c "多渠道消息" --channels wechat,webhook --options ,webhook_code
        """
    )
    
    # 必填参数
    parser.add_argument('-t', '--token',
                        help='PushPlus Token（用户 Token 或消息 Token）。也可通过环境变量 PUSHPLUS_TOKEN 设置')
    parser.add_argument('-c', '--content', 
                        help='消息内容')
    
    # 可选参数
    parser.add_argument('--title', default='',
                        help='消息标题（可选）')
    parser.add_argument('--topic', default='',
                        help='群组编码，用于一对多消息（可选）')
    parser.add_argument('--template', default='html',
                        choices=['html', 'txt', 'json', 'markdown', 'cloudMonitor', 'jenkins', 'route', 'pay'],
                        help='消息模板（默认 html）')
    parser.add_argument('--channel', default='wechat',
                        choices=['wechat', 'webhook', 'cp', 'mail', 'sms', 'extension', 'voice', 'app', 'clawbot'],
                        help='推送渠道（默认 wechat）')
    parser.add_argument('--channels', default='',
                        help='多渠道发送，逗号分隔，如 "wechat,webhook,extension"')
    parser.add_argument('--webhook', default='',
                        help='Webhook 编码（已废弃，请使用 --option，但为兼容保留）')
    parser.add_argument('--option', default='',
                        help='渠道配置参数（原 webhook 参数，多个渠道时用逗号分隔）')
    parser.add_argument('--options', default='',
                        help='多渠道配置参数，逗号分隔，与 --channels 一一对应')
    parser.add_argument('--callback-url', default='',
                        help='回调地址（可选）')
    parser.add_argument('--timestamp', type=int, default=None,
                        help='时间戳（毫秒），用于防重复（可选）')
    parser.add_argument('--to', default='',
                        help='好友令牌，支持多人（逗号分隔），实名用户最多10人，会员100人')
    parser.add_argument('--pre', default='',
                        help='预处理编码（可选）')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='显示详细信息')
    
    args = parser.parse_args()
    
    # 从环境变量获取 token（如果命令行未提供）
    token = args.token or get_token_from_env()
    
    if not token:
        print("ERROR: 请提供 Token（通过 -t 参数或环境变量 PUSHPLUS_TOKEN 设置）", file=sys.stderr)
        return 1
    
    if not args.content:
        print("ERROR: 请提供消息内容（通过 -c 参数）", file=sys.stderr)
        return 1
    
    try:
        # 判断是否为多渠道发送
        if args.channels:
            # 多渠道发送
            channels = [c.strip() for c in args.channels.split(',') if c.strip()]
            options = None
            if args.options:
                options = [o.strip() for o in args.options.split(',')]
            
            result = send_batch_message(
                token=token,
                content=args.content,
                channels=channels,
                title=args.title or None,
                topic=args.topic or None,
                template=args.template,
                options=options,
                callback_url=args.callback_url or None,
                timestamp=args.timestamp,
                to=args.to or None,
                pre=args.pre or None,
                verbose=args.verbose
            )
            
            # 检查返回结果
            if result.get('code') == 200:
                print("SUCCESS: 多渠道消息推送请求已提交")
                data = result.get('data', [])
                for item in data:
                    print(f"   [{item.get('channel')}] 流水号: {item.get('shortCode')}")
                if args.verbose:
                    print(f"   响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
                return 0
            else:
                print("ERROR: 多渠道消息推送失败")
                print(f"   错误码: {result.get('code')}")
                print(f"   错误信息: {result.get('msg')}")
                if args.verbose:
                    print(f"   响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
                return 1
        else:
            # 单渠道发送
            result = send_message(
                token=token,
                content=args.content,
                title=args.title or None,
                topic=args.topic or None,
                template=args.template,
                channel=args.channel,
                webhook=args.webhook or None,  # 兼容旧参数
                option=args.option or None,
                callback_url=args.callback_url or None,
                timestamp=args.timestamp,
                to=args.to or None,
                pre=args.pre or None,
                verbose=args.verbose
            )
            
            # 检查返回结果
            if result.get('code') == 200:
                print("SUCCESS: 消息推送请求已提交")
                print(f"   消息流水号: {result.get('data')}")
                if args.verbose:
                    print(f"   响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
                return 0
            else:
                print("ERROR: 消息推送失败")
                print(f"   错误码: {result.get('code')}")
                print(f"   错误信息: {result.get('msg')}")
                if args.verbose:
                    print(f"   响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
                return 1
            
    except Exception as e:
        print(f"ERROR: 请求异常: {str(e)}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
