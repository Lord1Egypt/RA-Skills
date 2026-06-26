#!/usr/bin/env python3
"""
腾讯云邮件推送(SES)工具脚本
封装域名管理、发信地址管理、邮件发送和状态查询等功能。

环境变量:
  TENCENTCLOUD_SECRET_ID   - 腾讯云 SecretId (必需)
  TENCENTCLOUD_SECRET_KEY  - 腾讯云 SecretKey (必需)
  SES_REGION               - 地域，默认 ap-guangzhou，可选 ap-hongkong
  SES_ENDPOINT             - SDK 接入点，默认 ses.tencentcloudapi.com

用法:
  python ses_tool.py <command> [args...]

命令:
  list-domains                           列出所有发信域名
  get-domain <domain>                    获取域名配置详情
  create-domain <domain>                 创建发信域名
  verify-domain <domain>                 请求验证域名
  list-addresses                         列出所有发信地址
  create-address <email> [sender_name]   创建发信地址
  send-template <from> <to> <subject> <template_id> [template_data_json] [options]
                                         使用模板发送邮件（to 支持逗号分隔多个收件人，最多50人）
  send-simple <from> <to> <subject> <html_or_text> [options]
                                         发送简单邮件(默认HTML, --text表示纯文本)
                                         （to 支持逗号分隔多个收件人，最多50人）
  get-status <message_id> <date>         查询邮件发送状态(date格式: YYYY-MM-DD)
  list-templates [--offset N] [--limit N] [--status 0|1|2]
                                         列出邮件模板(支持分页和按状态筛选)
  get-template <template_id>             获取模板详情
  create-template <name> <html_or_text> [--text] [--file]
                                         创建邮件模板(--file表示从文件读取内容)
  update-template <template_id> <name> <html_or_text> [--text] [--file]
                                         更新邮件模板
  delete-template <template_id>          删除邮件模板

发送邮件公共选项 (send-template / send-simple):
  --cc <email>[,<email>...]              抄送人（逗号分隔，最多20人）
  --bcc <email>[,<email>...]             密送人（逗号分隔，最多20人）
  --reply-to <email>                     回复地址
  --attachments <path>[,<path>...]       附件文件路径（逗号分隔，总大小≤4MB）
  --unsubscribe <0-10>                   退订链接语言（0:不加 1:简中 2:英文 3:繁中
                                         4:西班牙 5:法语 6:德语 7:日语 8:韩语
                                         9:阿拉伯 10:泰语）
  --trigger-type <0|1>                   邮件触发类型（0:非触发类 1:触发类，如验证码）

全局选项:
  --dry-run                              预览模式：仅验证参数并输出请求预览(JSON)，不实际调用 API
"""

import json
import os
import re
import sys
import base64
import binascii
from datetime import datetime

try:
    from tencentcloud.common import credential
    from tencentcloud.common.profile.client_profile import ClientProfile
    from tencentcloud.common.profile.http_profile import HttpProfile
    from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
    from tencentcloud.ses.v20201002 import ses_client, models
except ImportError:
    print("错误: 请先安装腾讯云 SDK: pip install tencentcloud-sdk-python", file=sys.stderr)
    sys.exit(1)


def get_client():
    """创建 SES 客户端"""
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")
    region = os.environ.get("SES_REGION", "ap-guangzhou")
    endpoint = os.environ.get("SES_ENDPOINT", "ses.tencentcloudapi.com")

    if not secret_id or not secret_key:
        print("错误: 请设置环境变量 TENCENTCLOUD_SECRET_ID 和 TENCENTCLOUD_SECRET_KEY", file=sys.stderr)
        sys.exit(1)

    cred = credential.Credential(secret_id, secret_key)
    http_profile = HttpProfile()
    http_profile.endpoint = endpoint
    http_profile.scheme = os.environ.get("SES_SCHEME", "https")
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile

    return ses_client.SesClient(cred, region, client_profile)


def list_domains():
    """列出所有发信域名"""
    client = get_client()
    req = models.ListEmailIdentitiesRequest()
    resp = client.ListEmailIdentities(req)
    data = json.loads(resp.to_json_string())

    identities = data.get("EmailIdentities", [])
    if not identities:
        print("当前没有发信域名。")
        return data

    print(f"共 {data.get('Total', len(identities))} 个发信域名：")
    print(f"{'域名':<30} {'可发信':<8} {'信誉等级':<10} {'日发送量':<10}")
    print("-" * 65)
    for item in identities:
        # SendingEnabled 表示「可发信」（已验证且未被封禁），而非单纯「已验证」
        sendable = "✅ 是" if item.get("SendingEnabled") else "❌ 否"
        reputation = item.get("CurrentReputationLevel", "N/A")
        daily_quota = item.get("DailyQuota", "N/A")
        print(f"{item['IdentityName']:<30} {sendable:<8} {reputation:<10} {daily_quota:<10}")

    return data


def get_domain(domain):
    """获取域名配置详情"""
    client = get_client()
    req = models.GetEmailIdentityRequest()
    req.EmailIdentity = domain
    resp = client.GetEmailIdentity(req)
    data = json.loads(resp.to_json_string())

    verified = data.get("VerifiedForSendingStatus", False)
    print(f"域名: {domain}")
    print(f"验证状态: {'✅ 已通过' if verified else '❌ 未通过'}")
    print()

    attributes = data.get("Attributes", [])
    if attributes:
        print("DNS 配置项：")
        print(f"{'类型':<6} {'域名':<40} {'状态':<6} {'期望值'}")
        print("-" * 100)
        for attr in attributes:
            status = "✅" if attr.get("Status") else "❌"
            print(f"{attr['Type']:<6} {attr['SendDomain']:<40} {status:<6} {attr['ExpectedValue']}")
            if attr.get("CurrentValue"):
                print(f"{'':>50} 当前值: {attr['CurrentValue']}")
    return data


def create_domain(domain, dry_run=False):
    """创建发信域名"""
    if dry_run:
        _output_dry_run("CreateEmailIdentity", {"EmailIdentity": domain}, {"domain": domain})
        return {"dry_run": True}

    client = get_client()
    req = models.CreateEmailIdentityRequest()
    req.EmailIdentity = domain
    resp = client.CreateEmailIdentity(req)
    data = json.loads(resp.to_json_string())

    print(f"✅ 发信域名 {domain} 创建成功！")
    print()

    attributes = data.get("Attributes", [])
    if attributes:
        print("请在您的 DNS 服务商中配置以下记录：")
        print(f"{'类型':<6} {'域名':<40} {'需要配置的值'}")
        print("-" * 100)
        for attr in attributes:
            print(f"{attr['Type']:<6} {attr['SendDomain']:<40} {attr['ExpectedValue']}")
        print()
        print("配置完成后，请使用 verify-domain 命令请求验证。")
    return data


def verify_domain(domain):
    """请求验证域名"""
    client = get_client()
    req = models.UpdateEmailIdentityRequest()
    req.EmailIdentity = domain
    resp = client.UpdateEmailIdentity(req)
    data = json.loads(resp.to_json_string())

    verified = data.get("VerifiedForSendingStatus", False)
    if verified:
        print(f"✅ 域名 {domain} 验证通过！可以用于发送邮件。")
    else:
        print(f"❌ 域名 {domain} 验证未通过。")
        attributes = data.get("Attributes", [])
        if attributes:
            print("\nDNS 配置状态：")
            for attr in attributes:
                status = "✅ 通过" if attr.get("Status") else "❌ 未通过"
                print(f"  {attr['Type']} {attr['SendDomain']} - {status}")
                if not attr.get("Status"):
                    print(f"    期望值: {attr['ExpectedValue']}")
                    if attr.get("CurrentValue"):
                        print(f"    当前值: {attr['CurrentValue']}")
                    else:
                        print(f"    当前值: (未检测到)")
            print("\n请检查 DNS 配置是否正确，DNS 传播可能需要一些时间。")
    return data


def list_addresses():
    """列出所有发信地址"""
    client = get_client()
    req = models.ListEmailAddressRequest()
    resp = client.ListEmailAddress(req)
    data = json.loads(resp.to_json_string())

    senders = data.get("EmailSenders", [])
    if not senders:
        print("当前没有发信地址。")
        return data

    print(f"共 {len(senders)} 个发信地址：")
    print(f"{'邮箱地址':<35} {'别名':<20} {'SMTP密码':<10}")
    print("-" * 70)
    for s in senders:
        pwd_type = "已设置" if s.get("SmtpPwdType") else "未设置"
        print(f"{s['EmailAddress']:<35} {s.get('EmailSenderName', ''):<20} {pwd_type:<10}")
    return data


def create_address(email, sender_name=None, dry_run=False):
    """创建发信地址"""
    if dry_run:
        params = {"EmailAddress": email}
        if sender_name:
            params["EmailSenderName"] = sender_name
        _output_dry_run("CreateEmailAddress", params, {"email": email, "sender_name": sender_name or "(无)"})
        return {"dry_run": True}

    client = get_client()
    req = models.CreateEmailAddressRequest()
    req.EmailAddress = email
    if sender_name:
        req.EmailSenderName = sender_name
    resp = client.CreateEmailAddress(req)
    data = json.loads(resp.to_json_string())
    alias_info = f"（别名: {sender_name}）" if sender_name else ""
    print(f"✅ 发信地址 {email} {alias_info} 创建成功！")
    return data


def _parse_send_options(args):
    """解析发送邮件的公共可选参数。

    支持的选项:
      --cc <emails>          抄送人（逗号分隔）
      --bcc <emails>         密送人（逗号分隔）
      --reply-to <email>     回复地址
      --attachments <paths>  附件文件路径（逗号分隔）
      --unsubscribe <0-10>   退订链接语言
      --trigger-type <0|1>   邮件触发类型
      --text                 纯文本模式（send-simple 专用）
      --dry-run              预览模式：仅验证参数并输出请求预览(JSON)，不实际调用 API

    返回 (options_dict, remaining_positional_args)
    """
    options = {
        "cc": None,
        "bcc": None,
        "reply_to": None,
        "attachments": None,
        "unsubscribe": None,
        "trigger_type": None,
        "is_text": False,
        "dry_run": False,
    }
    positional = []
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--cc" and i + 1 < len(args):
            options["cc"] = [e.strip() for e in args[i + 1].split(",") if e.strip()]
            i += 2
        elif arg == "--bcc" and i + 1 < len(args):
            options["bcc"] = [e.strip() for e in args[i + 1].split(",") if e.strip()]
            i += 2
        elif arg == "--reply-to" and i + 1 < len(args):
            options["reply_to"] = args[i + 1]
            i += 2
        elif arg == "--attachments" and i + 1 < len(args):
            options["attachments"] = [p.strip() for p in args[i + 1].split(",") if p.strip()]
            i += 2
        elif arg == "--unsubscribe" and i + 1 < len(args):
            unsub_val = args[i + 1]
            if not unsub_val.isdigit() or int(unsub_val) not in range(11):
                print(f"错误: --unsubscribe 的值必须为 0-10，收到: {unsub_val}", file=sys.stderr)
                sys.exit(1)
            options["unsubscribe"] = unsub_val
            i += 2
        elif arg == "--trigger-type" and i + 1 < len(args):
            trigger_val = args[i + 1]
            if trigger_val not in ("0", "1"):
                print(f"错误: --trigger-type 的值必须为 0 或 1，收到: {trigger_val}", file=sys.stderr)
                sys.exit(1)
            options["trigger_type"] = int(trigger_val)
            i += 2
        elif arg == "--text":
            options["is_text"] = True
            i += 1
        elif arg == "--dry-run":
            options["dry_run"] = True
            i += 1
        else:
            positional.append(arg)
            i += 1
    return options, positional


def _load_attachments(file_paths):
    """加载附件文件，返回 Attachment 对象列表。

    每个附件会被 Base64 编码。总附件大小限制在 4MB 以内（编码前）。
    """
    attachments = []
    total_size = 0
    for path in file_paths:
        if not os.path.exists(path):
            print(f"⚠️  附件文件不存在，跳过: {path}", file=sys.stderr)
            continue
        file_size = os.path.getsize(path)
        if total_size + file_size > 4 * 1024 * 1024:
            print(f"⚠️  附件总大小超过 4MB 限制，跳过: {path}", file=sys.stderr)
            continue
        total_size += file_size
        with open(path, "rb") as f:
            content = base64.b64encode(f.read()).decode("utf-8")
        filename = os.path.basename(path)
        att = models.Attachment()
        att.FileName = filename
        att.Content = content
        attachments.append(att)
        print(f"📎 附件: {filename} ({file_size / 1024:.1f} KB)")
    if total_size > 0:
        print(f"   附件总大小: {total_size / 1024:.1f} KB")
    return attachments


def _apply_send_options(req, options):
    """将公共发送选项应用到 SendEmailRequest 对象上。"""
    if options.get("cc"):
        req.Cc = options["cc"]
    if options.get("bcc"):
        req.Bcc = options["bcc"]
    if options.get("reply_to"):
        req.ReplyToAddresses = options["reply_to"]
    if options.get("unsubscribe") is not None:
        req.Unsubscribe = str(options["unsubscribe"])
    if options.get("trigger_type") is not None:
        req.TriggerType = options["trigger_type"]
    if options.get("attachments"):
        att_objects = _load_attachments(options["attachments"])
        if att_objects:
            req.Attachments = att_objects


def _print_send_options(options):
    """打印发送选项的摘要信息。"""
    if options.get("cc"):
        print(f"   抄送(CC): {', '.join(options['cc'])}")
    if options.get("bcc"):
        print(f"   密送(BCC): {', '.join(options['bcc'])}")
    if options.get("reply_to"):
        print(f"   回复地址: {options['reply_to']}")
    if options.get("unsubscribe") is not None:
        unsub_map = {
            "0": "不加入退订链接", "1": "简体中文", "2": "英文", "3": "繁体中文",
            "4": "西班牙语", "5": "法语", "6": "德语", "7": "日语",
            "8": "韩语", "9": "阿拉伯语", "10": "泰语",
        }
        unsub_desc = unsub_map.get(str(options["unsubscribe"]), str(options["unsubscribe"]))
        print(f"   退订链接: {unsub_desc}")
    if options.get("trigger_type") is not None:
        trigger_desc = "触发类（验证码等即时邮件）" if options["trigger_type"] == 1 else "非触发类（营销/通知）"
        print(f"   触发类型: {trigger_desc}")
    if options.get("attachments"):
        print(f"   附件数量: {len(options['attachments'])} 个")


def _output_dry_run(api_name, params, summary=None):
    """输出 dry-run 预览信息（JSON 格式到 stdout）。

    Args:
        api_name: API 名称，如 "SendEmail (Template)"
        params: 将要发送的请求参数字典
        summary: 可选的摘要信息字典，供人类快速阅读
    """
    preview = {
        "dry_run": True,
        "api": api_name,
        "params": params,
    }
    if summary:
        preview["summary"] = summary
    print(json.dumps(preview, ensure_ascii=False, indent=2))


def send_template_email(from_addr, to_addrs, subject, template_id, template_data=None, dry_run=False, **options):
    """使用模板发送邮件

    Args:
        from_addr: 发件人地址
        to_addrs: 收件人地址（字符串或列表）
        subject: 邮件主题
        template_id: 模板 ID
        template_data: 模板变量 JSON 字符串
        **options: 可选参数 (cc, bcc, reply_to, attachments, unsubscribe, trigger_type)
        dry_run: 预览模式，仅输出请求参数，不调用 API
    """
    to_list = to_addrs if isinstance(to_addrs, list) else [to_addrs]
    td = template_data or "{}"
    try:
        json.loads(td)
    except json.JSONDecodeError as e:
        print(f"❌ 错误: template_data 不是合法的 JSON 字符串: {e}", file=sys.stderr)
        print(f"   收到的值: {td[:200]}", file=sys.stderr)
        sys.exit(1)

    if dry_run:
        params = {
            "FromEmailAddress": from_addr,
            "Destination": to_list,
            "Subject": subject,
            "Template": {"TemplateID": int(template_id), "TemplateData": td},
        }
        if options.get("cc"):
            params["Cc"] = options["cc"]
        if options.get("bcc"):
            params["Bcc"] = options["bcc"]
        if options.get("reply_to"):
            params["ReplyToAddresses"] = options["reply_to"]
        if options.get("unsubscribe") is not None:
            params["Unsubscribe"] = str(options["unsubscribe"])
        if options.get("trigger_type") is not None:
            params["TriggerType"] = options["trigger_type"]
        if options.get("attachments"):
            params["Attachments"] = [os.path.basename(p) for p in options["attachments"]]
        summary = {
            "recipient_count": len(to_list),
            "recipients": to_list[:10],
            "template_id": int(template_id),
        }
        if len(to_list) > 10:
            summary["recipients_note"] = f"仅展示前 10 个，共 {len(to_list)} 个收件人"
        _output_dry_run("SendEmail (Template)", params, summary)
        return {"dry_run": True}

    client = get_client()
    req = models.SendEmailRequest()
    req.FromEmailAddress = from_addr
    req.Destination = to_list
    req.Subject = subject
    req.Template = models.Template()
    req.Template.TemplateID = int(template_id)
    req.Template.TemplateData = td

    _apply_send_options(req, options)

    resp = client.SendEmail(req)
    data = json.loads(resp.to_json_string())

    message_id = data.get("MessageId", "")
    print(f"✅ 模板邮件发送成功！")
    print(f"   MessageId: {message_id}")
    print(f"   发件人: {from_addr}")
    print(f"   收件人: {', '.join(req.Destination)}")
    _print_send_options(options)
    print(f"   主题: {subject}")
    print(f"   模板ID: {template_id}")
    return data


def send_simple_email(from_addr, to_addrs, subject, content, is_text=False, dry_run=False, **options):
    """发送简单邮件（HTML 或纯文本）

    Args:
        from_addr: 发件人地址
        to_addrs: 收件人地址（字符串或列表）
        subject: 邮件主题
        content: 邮件内容（HTML 或纯文本）
        is_text: 是否为纯文本
        **options: 可选参数 (cc, bcc, reply_to, attachments, unsubscribe, trigger_type)
        dry_run: 预览模式，仅输出请求参数，不调用 API
    """
    to_list = to_addrs if isinstance(to_addrs, list) else [to_addrs]
    content_type = "纯文本" if is_text else "HTML"

    if dry_run:
        params = {
            "FromEmailAddress": from_addr,
            "Destination": to_list,
            "Subject": subject,
            "Simple": {"type": content_type, "content_length": len(content.encode("utf-8"))},
        }
        if options.get("cc"):
            params["Cc"] = options["cc"]
        if options.get("bcc"):
            params["Bcc"] = options["bcc"]
        if options.get("reply_to"):
            params["ReplyToAddresses"] = options["reply_to"]
        if options.get("unsubscribe") is not None:
            params["Unsubscribe"] = str(options["unsubscribe"])
        if options.get("trigger_type") is not None:
            params["TriggerType"] = options["trigger_type"]
        if options.get("attachments"):
            params["Attachments"] = [os.path.basename(p) for p in options["attachments"]]
        summary = {
            "recipient_count": len(to_list),
            "recipients": to_list[:10],
            "content_type": content_type,
            "content_preview": content[:200] + ("..." if len(content) > 200 else ""),
        }
        if len(to_list) > 10:
            summary["recipients_note"] = f"仅展示前 10 个，共 {len(to_list)} 个收件人"
        _output_dry_run("SendEmail (Simple)", params, summary)
        return {"dry_run": True}

    client = get_client()
    req = models.SendEmailRequest()
    req.FromEmailAddress = from_addr
    req.Destination = to_list
    req.Subject = subject

    req.Simple = models.Simple()
    encoded = base64.b64encode(content.encode("utf-8")).decode("utf-8")
    if is_text:
        req.Simple.Text = encoded
    else:
        req.Simple.Html = encoded

    _apply_send_options(req, options)

    resp = client.SendEmail(req)
    data = json.loads(resp.to_json_string())

    message_id = data.get("MessageId", "")
    print(f"✅ {content_type}邮件发送成功！")
    print(f"   MessageId: {message_id}")
    print(f"   发件人: {from_addr}")
    print(f"   收件人: {', '.join(req.Destination)}")
    _print_send_options(options)
    print(f"   主题: {subject}")
    return data


def get_send_status(message_id, request_date):
    """查询邮件发送状态"""
    client = get_client()
    req = models.GetSendEmailStatusRequest()
    req.RequestDate = request_date
    req.Offset = 0
    req.Limit = 10
    req.MessageId = message_id

    resp = client.GetSendEmailStatus(req)
    data = json.loads(resp.to_json_string())

    status_list = data.get("EmailStatusList", [])
    if not status_list:
        print(f"未找到 MessageId={message_id} 在 {request_date} 的发送记录。")
        print("提示: 邮件状态可能需要几分钟才能查询到，请稍后重试。")
        return data

    send_status_map = {
        0: "处理成功",
        1001: "内部系统异常",
        1002: "内部系统异常",
        1003: "内部系统异常",
        1004: "内部系统异常(发信超时)",
        1005: "内部系统异常",
        1006: "触发频率控制",
        1007: "邮件地址在黑名单中",
        1008: "域名被收件人拒收",
        1010: "超出每日发送限制",
        1011: "无发送自定义内容权限",
        1013: "域名被收件人取消订阅",
        2001: "找不到相关记录",
        3007: "模板ID无效或不可用",
        3008: "被收信域名临时封禁",
        3009: "无权限使用该模板",
        3010: "TemplateData格式不正确",
        3014: "发件域名未认证",
        3020: "收件方邮箱类型在黑名单",
        3024: "邮箱地址格式预检查失败",
        3030: "退信率过高，临时限制发送",
        3033: "余额不足/账号欠费",
    }

    deliver_status_map = {
        0: "已进入发送队列",
        1: "邮件递送成功",
        2: "邮件被丢弃",
        3: "收件方ESP拒信",
        8: "延迟递送中",
    }

    for status in status_list:
        print(f"📧 邮件状态详情")
        print(f"   MessageId: {status.get('MessageId', 'N/A')}")
        print(f"   收件人: {status.get('ToEmailAddress', 'N/A')}")
        print(f"   发件人: {status.get('FromEmailAddress', 'N/A')}")

        send_code = status.get("SendStatus", -1)
        send_desc = send_status_map.get(send_code, f"未知状态({send_code})")
        print(f"   腾讯云处理状态: {send_desc} (code={send_code})")

        deliver_code = status.get("DeliverStatus", -1)
        deliver_desc = deliver_status_map.get(deliver_code, f"未知状态({deliver_code})")
        print(f"   收件方处理状态: {deliver_desc} (code={deliver_code})")

        if status.get("DeliverMessage"):
            print(f"   收件方描述: {status['DeliverMessage']}")

        req_time = status.get("RequestTime")
        if req_time:
            print(f"   请求时间: {datetime.fromtimestamp(req_time).strftime('%Y-%m-%d %H:%M:%S')}")

        deliver_time = status.get("DeliverTime")
        if deliver_time and deliver_time > 0:
            print(f"   递送时间: {datetime.fromtimestamp(deliver_time).strftime('%Y-%m-%d %H:%M:%S')}")

        print(f"   用户已打开: {'是' if status.get('UserOpened') else '否'}")
        print(f"   用户已点击: {'是' if status.get('UserClicked') else '否'}")
        print(f"   用户已退订: {'是' if status.get('UserUnsubscribed') else '否'}")
        print(f"   用户已举报: {'是' if status.get('UserComplained') else '否'}")
        print()

    return data


def list_templates(offset=0, limit=20, status_filter=None):
    """列出邮件模板（支持分页和状态筛选）"""
    client = get_client()
    req = models.ListEmailTemplatesRequest()
    req.Limit = limit
    req.Offset = offset
    resp = client.ListEmailTemplates(req)
    data = json.loads(resp.to_json_string())

    templates = data.get("TemplatesMetadata", [])
    total = data.get("TotalCount", len(templates))

    # 客户端侧按状态筛选（API 不支持服务端筛选）
    if status_filter is not None:
        templates = [t for t in templates if t.get("TemplateStatus") == status_filter]

    if not templates:
        if status_filter is not None:
            status_map = {0: "已通过", 1: "待审核", 2: "被拒绝"}
            print(f"当前页（offset={offset}, limit={limit}）没有状态为「{status_map.get(status_filter, status_filter)}」的模板。")
        else:
            print(f"当前页（offset={offset}, limit={limit}）没有模板。")
        return data

    status_map = {0: "✅ 已通过", 1: "⏳ 待审核", 2: "❌ 被拒绝"}

    # 分页信息（page_end 基于实际显示条数，而非过滤前的原始条数）
    page_start = offset + 1
    page_end = offset + len(templates)
    filter_info = ""
    if status_filter is not None:
        filter_names = {0: "已通过", 1: "待审核", 2: "被拒绝"}
        filter_info = f"（筛选: {filter_names.get(status_filter, status_filter)}，匹配 {len(templates)} 条）"

    print(f"模板总数: {total}，当前显示第 {page_start}-{page_end} 条{filter_info}：")
    print(f"{'模板ID':<12} {'模板名称':<25} {'状态':<12}")
    print("-" * 55)
    for t in templates:
        status = status_map.get(t.get("TemplateStatus"), f"未知({t.get('TemplateStatus')})")
        print(f"{t.get('TemplateID', 'N/A'):<12} {t.get('TemplateName', 'N/A'):<25} {status:<12}")
        if t.get("ReviewReason"):
            print(f"{'':>12} 审核原因: {t['ReviewReason']}")

    # 分页提示
    # 有状态筛选时，total 是未过滤的总数，不能直接用于判断是否还有下一页
    if status_filter is not None:
        # 客户端筛选模式：无法准确判断服务端是否还有更多符合条件的数据
        raw_count = len(data.get("TemplatesMetadata", []))
        if raw_count >= limit:
            print(f"\n💡 当前页原始数据已满（{raw_count} 条），可能还有更多，使用 --offset {offset + raw_count} 查看下一页")
        else:
            print(f"\n已显示当前页全部匹配模板。")
    else:
        if page_end < total:
            print(f"\n💡 还有更多模板，使用 --offset {page_end} 查看下一页")
        else:
            print(f"\n已显示全部模板。")

    return data


def get_template(template_id):
    """获取模板详情"""
    client = get_client()
    req = models.GetEmailTemplateRequest()
    req.TemplateID = int(template_id)
    resp = client.GetEmailTemplate(req)
    data = json.loads(resp.to_json_string())

    status_map = {0: "✅ 已通过", 1: "⏳ 待审核", 2: "❌ 被拒绝"}
    print(f"模板名称: {data.get('TemplateName', 'N/A')}")
    print(f"模板状态: {status_map.get(data.get('TemplateStatus'), '未知')}")

    content = data.get("TemplateContent", {})
    if content.get("Html"):
        try:
            html = base64.b64decode(content["Html"], validate=True).decode("utf-8")
            print(f"\nHTML 内容:\n{html}")
        except (binascii.Error, UnicodeDecodeError, ValueError):
            print(f"\nHTML (Base64): {content['Html']}")
    if content.get("Text"):
        try:
            text = base64.b64decode(content["Text"], validate=True).decode("utf-8")
            print(f"\n纯文本内容:\n{text}")
        except (binascii.Error, UnicodeDecodeError, ValueError):
            print(f"\n纯文本 (Base64): {content['Text']}")
    return data


def _read_template_content(content_or_path, is_file=False):
    """读取模板内容，支持直接传入内容或从文件读取"""
    if is_file:
        file_path = content_or_path
        if not os.path.exists(file_path):
            print(f"❌ 文件不存在: {file_path}", file=sys.stderr)
            sys.exit(1)
        file_size = os.path.getsize(file_path)
        if file_size > 500 * 1024:
            print(f"⚠️  文件大小 {file_size / 1024:.1f} KB，腾讯云模板上限为 500 KB", file=sys.stderr)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        print(f"📄 从文件读取模板内容: {file_path} ({file_size / 1024:.1f} KB)")
        return content
    return content_or_path


def create_template(name, content, is_text=False, dry_run=False):
    """创建邮件模板"""
    if dry_run:
        content_type = "纯文本" if is_text else "HTML"
        content_size = len(content.encode("utf-8"))
        variables = list(set(re.findall(r"\{\{(\w+)\}\}", content))) if "{{" in content else []
        params = {"TemplateName": name, "ContentType": content_type, "ContentSize": f"{content_size / 1024:.1f} KB"}
        summary = {"name": name, "content_type": content_type, "content_size": f"{content_size / 1024:.1f} KB"}
        if variables:
            summary["template_variables"] = variables
        _output_dry_run("CreateEmailTemplate", params, summary)
        return {"dry_run": True}

    client = get_client()
    req = models.CreateEmailTemplateRequest()
    req.TemplateName = name

    req.TemplateContent = models.TemplateContent()
    encoded = base64.b64encode(content.encode("utf-8")).decode("utf-8")
    if is_text:
        req.TemplateContent.Text = encoded
    else:
        req.TemplateContent.Html = encoded

    resp = client.CreateEmailTemplate(req)
    data = json.loads(resp.to_json_string())

    template_id = data.get("TemplateID", "N/A")
    content_type = "纯文本" if is_text else "HTML"
    content_size = len(content.encode("utf-8"))
    print(f"✅ {content_type}邮件模板创建成功！")
    print(f"   模板ID: {template_id}")
    print(f"   模板名称: {name}")
    print(f"   内容大小: {content_size / 1024:.1f} KB")
    print(f"   状态: ⏳ 待审核（模板需审核通过后方可使用）")
    if "{{" in content:
        variables = list(set(re.findall(r"\{\{(\w+)\}\}", content)))
        if variables:
            print(f"   模板变量: {', '.join(variables)}")
            example_data = json.dumps({v: "值" for v in variables}, ensure_ascii=False)
            print(f"   发送时传入: '{example_data}'")
    return data


def update_template(template_id, name, content, is_text=False, dry_run=False):
    """更新邮件模板"""
    if dry_run:
        content_type = "纯文本" if is_text else "HTML"
        content_size = len(content.encode("utf-8"))
        params = {
            "TemplateID": int(template_id),
            "TemplateName": name,
            "ContentType": content_type,
            "ContentSize": f"{content_size / 1024:.1f} KB",
        }
        summary = {"template_id": int(template_id), "name": name, "content_type": content_type}
        _output_dry_run("UpdateEmailTemplate", params, summary)
        return {"dry_run": True}

    client = get_client()
    req = models.UpdateEmailTemplateRequest()
    req.TemplateID = int(template_id)
    req.TemplateName = name

    req.TemplateContent = models.TemplateContent()
    encoded = base64.b64encode(content.encode("utf-8")).decode("utf-8")
    if is_text:
        req.TemplateContent.Text = encoded
    else:
        req.TemplateContent.Html = encoded

    resp = client.UpdateEmailTemplate(req)
    data = json.loads(resp.to_json_string())

    content_type = "纯文本" if is_text else "HTML"
    content_size = len(content.encode("utf-8"))
    print(f"✅ {content_type}邮件模板更新成功！")
    print(f"   模板ID: {template_id}")
    print(f"   模板名称: {name}")
    print(f"   内容大小: {content_size / 1024:.1f} KB")
    print(f"   状态: ⏳ 更新后需重新审核")
    return data


def delete_template(template_id, dry_run=False):
    """删除邮件模板"""
    if dry_run:
        _output_dry_run("DeleteEmailTemplate", {"TemplateID": int(template_id)}, {"template_id": int(template_id)})
        return {"dry_run": True}

    client = get_client()
    req = models.DeleteEmailTemplateRequest()
    req.TemplateID = int(template_id)
    resp = client.DeleteEmailTemplate(req)
    data = json.loads(resp.to_json_string())
    print(f"✅ 模板 {template_id} 已删除。")
    return data


def print_usage():
    print(__doc__)


def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    # 全局提取 --dry-run 标志
    dry_run = "--dry-run" in sys.argv
    if dry_run:
        sys.argv.remove("--dry-run")

    cmd = sys.argv[1]

    try:
        if cmd == "list-domains":
            list_domains()
        elif cmd == "get-domain":
            if len(sys.argv) < 3:
                print("用法: ses_tool.py get-domain <domain>")
                sys.exit(1)
            get_domain(sys.argv[2])
        elif cmd == "create-domain":
            if len(sys.argv) < 3:
                print("用法: ses_tool.py create-domain <domain>")
                sys.exit(1)
            create_domain(sys.argv[2], dry_run=dry_run)
        elif cmd == "verify-domain":
            if len(sys.argv) < 3:
                print("用法: ses_tool.py verify-domain <domain>")
                sys.exit(1)
            verify_domain(sys.argv[2])
        elif cmd == "list-addresses":
            list_addresses()
        elif cmd == "create-address":
            if len(sys.argv) < 3:
                print("用法: ses_tool.py create-address <email> [sender_name]")
                sys.exit(1)
            sender_name = sys.argv[3] if len(sys.argv) > 3 else None
            create_address(sys.argv[2], sender_name, dry_run=dry_run)
        elif cmd == "send-template":
            if len(sys.argv) < 6:
                print(
                    "用法: ses_tool.py send-template <from> <to> <subject> <template_id> "
                    "[template_data_json] [options]"
                )
                print()
                print("参数:")
                print("  <to>                   收件人地址（多个用逗号分隔，最多50人）")
                print()
                print("选项:")
                print("  --cc <emails>          抄送人（逗号分隔，最多20人）")
                print("  --bcc <emails>         密送人（逗号分隔，最多20人）")
                print("  --reply-to <email>     回复地址")
                print("  --attachments <paths>  附件文件路径（逗号分隔，总大小≤4MB）")
                print("  --unsubscribe <0-10>   退订链接语言（0:不加 1:简中 2:英文 3:繁中 ...）")
                print("  --trigger-type <0|1>   邮件触发类型（0:非触发 1:触发类）")
                print()
                print("示例:")
                print('  ses_tool.py send-template "from@x.com" "to@x.com" "主题" 12345')
                print('  ses_tool.py send-template "from@x.com" "a@x.com,b@x.com" "主题" 12345')
                print(
                    '  ses_tool.py send-template "from@x.com" "to@x.com" "主题" 12345 '
                    '\'{"name":"张三"}\' --cc "a@x.com,b@x.com"'
                )
                print(
                    '  ses_tool.py send-template "from@x.com" "to@x.com" "主题" 12345 '
                    '--reply-to "reply@x.com" --unsubscribe 1'
                )
                print(
                    '  ses_tool.py send-template "from@x.com" "to@x.com" "主题" 12345 '
                    '--attachments "/path/a.pdf,/path/b.png"'
                )
                sys.exit(1)
            from_addr = sys.argv[2]
            to_addrs = [e.strip() for e in sys.argv[3].split(",") if e.strip()]
            subject_arg = sys.argv[4]
            template_id = sys.argv[5]
            # 剩余参数：可能有 template_data_json 和 --options
            remaining = sys.argv[6:]
            options, positional = _parse_send_options(remaining)
            # positional 中的第一个（如果有）作为 template_data
            template_data = positional[0] if positional else "{}"
            options.pop("dry_run", None)
            send_template_email(
                from_addr,
                to_addrs,
                subject_arg,
                template_id,
                template_data,
                dry_run=dry_run,
                **options,
            )
        elif cmd == "send-simple":
            if len(sys.argv) < 6:
                print("用法: ses_tool.py send-simple <from> <to> <subject> <content> [options]")
                print()
                print("参数:")
                print("  <to>                   收件人地址（多个用逗号分隔，最多50人）")
                print()
                print("选项:")
                print("  --text                 发送纯文本（默认HTML）")
                print("  --cc <emails>          抄送人（逗号分隔，最多20人）")
                print("  --bcc <emails>         密送人（逗号分隔，最多20人）")
                print("  --reply-to <email>     回复地址")
                print("  --attachments <paths>  附件文件路径（逗号分隔，总大小≤4MB）")
                print("  --unsubscribe <0-10>   退订链接语言（0:不加 1:简中 2:英文 3:繁中 ...）")
                print("  --trigger-type <0|1>   邮件触发类型（0:非触发 1:触发类）")
                print()
                print("示例:")
                print('  ses_tool.py send-simple "from@x.com" "to@x.com" "主题" "<h1>Hello</h1>"')
                print('  ses_tool.py send-simple "from@x.com" "a@x.com,b@x.com,c@x.com" "主题" "<h1>Hello</h1>"')
                print('  ses_tool.py send-simple "from@x.com" "to@x.com" "主题" "Hello" --text')
                print(
                    '  ses_tool.py send-simple "from@x.com" "to@x.com" "主题" "<h1>Hi</h1>" '
                    '--cc "a@x.com" --bcc "b@x.com"'
                )
                print(
                    '  ses_tool.py send-simple "from@x.com" "to@x.com" "主题" "<h1>Hi</h1>" '
                    '--attachments "/path/a.pdf"'
                )
                sys.exit(1)
            from_addr = sys.argv[2]
            to_addrs = [e.strip() for e in sys.argv[3].split(",") if e.strip()]
            if not to_addrs:
                print("错误: 收件人地址不能为空", file=sys.stderr)
                sys.exit(1)
            subject_arg = sys.argv[4]
            # 从剩余参数中剥离标志，取第一个位置参数作为邮件内容
            remaining = sys.argv[5:]
            options, positional = _parse_send_options(remaining)
            if not positional:
                print("错误: 缺少邮件内容参数", file=sys.stderr)
                sys.exit(1)
            content = positional[0]
            is_text = options.pop("is_text", False)
            options.pop("dry_run", None)
            send_simple_email(from_addr, to_addrs, subject_arg, content, is_text, dry_run=dry_run, **options)
        elif cmd == "get-status":
            if len(sys.argv) < 4:
                print("用法: ses_tool.py get-status <message_id> <date:YYYY-MM-DD>")
                sys.exit(1)
            get_send_status(sys.argv[2], sys.argv[3])
        elif cmd == "list-templates":
            # 解析可选参数: --offset N --limit N --status 0|1|2
            offset = 0
            limit = 20
            status_filter = None
            args = sys.argv[2:]
            i = 0
            while i < len(args):
                if args[i] == "--offset" and i + 1 < len(args):
                    offset = int(args[i + 1])
                    i += 2
                elif args[i] == "--limit" and i + 1 < len(args):
                    limit = int(args[i + 1])
                    i += 2
                elif args[i] == "--status" and i + 1 < len(args):
                    status_filter = int(args[i + 1])
                    i += 2
                else:
                    print(f"未知参数: {args[i]}")
                    print("用法: ses_tool.py list-templates [--offset N] [--limit N] [--status 0|1|2]")
                    print("  --offset  起始偏移量（默认 0）")
                    print("  --limit   每页数量（默认 20，最大 100）")
                    print("  --status  按状态筛选: 0=已通过, 1=待审核, 2=被拒绝")
                    sys.exit(1)
            list_templates(offset=offset, limit=min(limit, 100), status_filter=status_filter)
        elif cmd == "get-template":
            if len(sys.argv) < 3:
                print("用法: ses_tool.py get-template <template_id>")
                sys.exit(1)
            get_template(sys.argv[2])
        elif cmd == "create-template":
            if len(sys.argv) < 4:
                print("用法: ses_tool.py create-template <name> <html_or_text> [--text] [--file]")
                print("  --file  从文件路径读取模板内容（适合大模板）")
                print("  --text  创建纯文本模板（默认为HTML）")
                print()
                print("示例:")
                print('  ses_tool.py create-template "欢迎邮件" "<h1>你好 {{name}}</h1>"')
                print('  ses_tool.py create-template "欢迎邮件" /path/to/template.html --file')
                print('  ses_tool.py create-template "通知" "你好 {{name}}" --text')
                sys.exit(1)
            is_text = "--text" in sys.argv
            is_file = "--file" in sys.argv
            # 从剩余参数中剥离标志，取第一个位置参数作为内容/路径
            remaining_args = [a for a in sys.argv[3:] if a not in ("--text", "--file")]
            if not remaining_args:
                print("错误: 缺少模板内容或文件路径参数", file=sys.stderr)
                sys.exit(1)
            content = _read_template_content(remaining_args[0], is_file)
            create_template(sys.argv[2], content, is_text, dry_run=dry_run)
        elif cmd == "update-template":
            if len(sys.argv) < 5:
                print("用法: ses_tool.py update-template <template_id> <name> <html_or_text> [--text] [--file]")
                print("  --file  从文件路径读取模板内容（适合大模板）")
                print("  --text  更新为纯文本模板（默认为HTML）")
                sys.exit(1)
            is_text = "--text" in sys.argv
            is_file = "--file" in sys.argv
            # 从剩余参数中剥离标志，取第一个位置参数作为内容/路径
            remaining_args = [a for a in sys.argv[4:] if a not in ("--text", "--file")]
            if not remaining_args:
                print("错误: 缺少模板内容或文件路径参数", file=sys.stderr)
                sys.exit(1)
            content = _read_template_content(remaining_args[0], is_file)
            update_template(sys.argv[2], sys.argv[3], content, is_text, dry_run=dry_run)
        elif cmd == "delete-template":
            if len(sys.argv) < 3:
                print("用法: ses_tool.py delete-template <template_id>")
                sys.exit(1)
            delete_template(sys.argv[2], dry_run=dry_run)
        else:
            print(f"未知命令: {cmd}")
            print_usage()
            sys.exit(1)
    except TencentCloudSDKException as e:
        print(f"❌ 腾讯云 API 错误: {e}", file=sys.stderr)
        sys.exit(1)
    except (OSError, ValueError, UnicodeError) as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
