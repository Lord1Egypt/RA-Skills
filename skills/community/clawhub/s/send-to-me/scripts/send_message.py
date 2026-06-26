#!/usr/bin/env python3
"""
企业微信消息发送工具 (WeChat Work Message Sender)

本模块提供向企业微信发送文本消息的功能，支持多种配置方式和消息格式。

配置优先级：命令行参数 > 环境变量 > .env 文件 > 默认值

依赖:
    pip install python-dotenv

作者微信公众号：XiaoqiangClub
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from typing import Optional

try:
    from dotenv import load_dotenv
except ImportError:
    raise ImportError(
        "缺少依赖: python-dotenv\n"
        "请运行: pip install python-dotenv\n"
        "或参考: https://xiaoqiangclub.blog.csdn.net/article/details/144614019"
    )

load_dotenv()


def get_config_value(
    key: str, default: Optional[str] = None, required: bool = False
) -> Optional[str]:
    """
    获取配置值，按优先级依次尝试：环境变量 -> .env 文件 -> 默认值

    Args:
        key: 配置键名（如 WECOM_CORP_ID）
        default: 默认值
        required: 是否为必需配置

    Returns:
        配置值字符串

    Raises:
        ValueError: 当 required=True 且无法获取有效配置时
    """
    value = os.environ.get(key) or default

    if required and (not value or value.startswith("your_")):
        raise ValueError(
            f"缺少必需配置: {key}\n"
            f"请在 .env 文件中配置或设置环境变量。\n"
            f"参考文档: https://xiaoqiangclub.blog.csdn.net/article/details/144614019"
        )

    return value


def get_access_token(corp_id: str, corp_secret: str) -> Optional[str]:
    """
    获取企业微信 Access Token

    Args:
        corp_id: 企业 ID
        corp_secret: 应用密钥

    Returns:
        成功返回 access_token，失败返回 None
    """
    try:
        token_url = (
            f"https://qyapi.weixin.qq.com/cgi-bin/gettoken"
            f"?corpid={corp_id}&corpsecret={corp_secret}"
        )
        with urllib.request.urlopen(token_url, timeout=10) as response:
            token_data = json.loads(response.read().decode("utf-8"))

        access_token = token_data.get("access_token")
        if not access_token:
            print(f"❌ 获取 AccessToken 失败: {token_data.get('errmsg')}")
            return None

        return access_token

    except urllib.error.URLError as e:
        print(f"❌ 网络请求失败: {e}")
        return None
    except Exception as e:
        print(f"❌ 获取 AccessToken 异常: {e}")
        return None


def send_wechat_message(
    message: str,
    sender: str = "",
    wecom_corp_id: Optional[str] = None,
    wecom_corp_secret: Optional[str] = None,
    wecom_agent_id: Optional[int] = None,
    touser: str = "@all",
    toparty: str = "",
    totag: str = "",
) -> bool:
    """
    发送企业微信消息

    Args:
        message: 消息内容（支持 emoji 和换行）
        sender: 发送来源标识，如 "📦 数据备份服务"
        wecom_corp_id: 企业微信 CorpID（优先使用 .env 配置）
        wecom_corp_secret: 企业微信密钥
        wecom_agent_id: 企业微信应用 AgentID
        touser: 接收消息的用户，多个用户用 | 分隔，@all 表示所有人
        toparty: 接收消息的部门 ID
        totag: 接收消息的标签 ID

    Returns:
        发送成功返回 True，失败返回 False

    Note:
        touser、toparty、totag 至少要有一个非空，否则消息无法送达
    """
    wecom_corp_id = get_config_value("WECOM_CORP_ID", wecom_corp_id, required=True)
    wecom_corp_secret = get_config_value(
        "WECOM_CORP_SECRET", wecom_corp_secret, required=True
    )
    wecom_agent_id = wecom_agent_id or int(get_config_value("WECOM_AGENT_ID", "0") or 0)

    if not wecom_agent_id:
        raise ValueError(
            "缺少必需配置: WECOM_AGENT_ID\n"
            "请在 .env 文件中配置企业微信应用 AgentID。\n"
            "参考文档: https://xiaoqiangclub.blog.csdn.net/article/details/144614019"
        )

    access_token = get_access_token(wecom_corp_id, wecom_corp_secret)
    if not access_token:
        return False

    try:
        send_url = (
            f"https://qyapi.weixin.qq.com/cgi-bin/message/send"
            f"?access_token={access_token}"
        )

        content = f"{sender}\n{message}" if sender else message

        data = {
            "touser": touser,
            "toparty": toparty,
            "totag": totag,
            "msgtype": "text",
            "agentid": wecom_agent_id,
            "text": {"content": content},
            "safe": 0,
        }

        json_data = json.dumps(data, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(
            send_url,
            data=json_data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode("utf-8"))

        if result.get("errcode") == 0:
            print("☑️ 消息发送成功")
            return True
        else:
            print(f"❌ 消息发送失败: {result.get('errmsg')}")
            return False

    except urllib.error.URLError as e:
        print(f"❌ 消息发送失败（网络错误）: {e}")
        return False
    except Exception as e:
        print(f"❌ 消息发送失败: {e}")
        return False


def main():
    """命令行入口函数"""
    parser = argparse.ArgumentParser(
        description="发送企业微信消息",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
配置说明:
  配置文件优先级: 命令行参数 > 环境变量 > .env 文件

获取配置帮助: https://xiaoqiangclub.blog.csdn.net/article/details/144614019

示例:
  python scripts/send_message.py "Hello World"
  python scripts/send_message.py "任务完成" -s "📦 备份服务"
  python scripts/send_message.py "告警" -t "zhangsan|lisi"
  python scripts/send_message.py "部门通知" -p "2"
        """,
    )

    parser.add_argument("message", nargs="?", help="消息内容（支持 emoji 和换行）")

    parser.add_argument(
        "-s",
        "--sender",
        default="",
        help="消息发送来源，如 '📦 数据备份服务'（默认使用 .env 中的配置）",
    )

    parser.add_argument(
        "-c", "--corp-id", help="企业微信 CorpID（默认使用 .env 中的配置）"
    )

    parser.add_argument(
        "-k", "--corp-secret", help="企业微信应用密钥（默认使用 .env 中的配置）"
    )

    parser.add_argument(
        "-a",
        "--agent-id",
        type=int,
        help="企业微信应用 AgentID（默认使用 .env 中的配置）",
    )

    parser.add_argument(
        "-t",
        "--touser",
        default=None,
        help="接收消息的用户账号，多个用 | 分隔（默认 @all）",
    )

    parser.add_argument("-p", "--toparty", default="", help="接收消息的部门 ID")

    parser.add_argument("-g", "--totag", default="", help="接收消息的标签 ID")

    args = parser.parse_args()

    if not args.message:
        parser.print_help()
        sys.exit(1)

    sender = args.sender or get_config_value("WECOM_SENDER", "")
    touser = args.touser or get_config_value("WECOM_TOUSER", "@all")

    success = send_wechat_message(
        message=args.message,
        sender=sender,
        wecom_corp_id=args.corp_id,
        wecom_corp_secret=args.corp_secret,
        wecom_agent_id=args.agent_id,
        touser=touser,
        toparty=args.toparty,
        totag=args.totag,
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
