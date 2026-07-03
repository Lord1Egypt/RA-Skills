#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
腾讯云短信 — 添加短信模板 (AddSmsTemplate)

创建短信正文模板并提交审核。仅企业认证用户可调用此接口。

需要环境变量: TENCENTCLOUD_SECRET_ID, TENCENTCLOUD_SECRET_KEY

用法:
    python add_template.py --template-name "验证码" \
        --template-content "您的验证码是{1}，{2}分钟内有效。" \
        --sms-type 3 --international 0 --remark "登录验证码"
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import (  # noqa: E402
    ensure_dependencies,
    get_credentials,
    build_client,
    output_json,
    output_error,
    add_common_args,
)

ensure_dependencies()

from tencentcloud.common.exception.tencent_cloud_sdk_exception import (  # noqa: E402
    TencentCloudSDKException,
)
from tencentcloud.sms.v20210111 import models  # noqa: E402


def build_parser():
    parser = argparse.ArgumentParser(
        description="腾讯云短信 — 添加短信模板 (AddSmsTemplate)"
    )
    parser.add_argument("--template-name", required=True, help="模板名称")
    parser.add_argument("--template-content", required=True, help="模板内容，变量使用 {1}、{2} 等")
    parser.add_argument(
        "--sms-type", type=int, required=True,
        choices=[1, 2, 3],
        help="短信类型: 1=营销, 2=通知, 3=验证码",
    )
    parser.add_argument(
        "--international", type=int, required=True,
        choices=[0, 1],
        help="0=国内短信, 1=国际/港澳台短信",
    )
    parser.add_argument("--remark", required=True, help="模板备注（申请原因、使用场景）")
    add_common_args(parser)
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    params = {
        "TemplateName": args.template_name,
        "TemplateContent": args.template_content,
        "SmsType": args.sms_type,
        "International": args.international,
        "Remark": args.remark,
    }

    if args.dry_run:
        output_json({"dry_run": True, "api": "AddSmsTemplate", "params": params})
        return

    cred = get_credentials()
    client = build_client(cred, region=args.region)

    try:
        req = models.AddSmsTemplateRequest()
        req.from_json_string(json.dumps(params))
        resp = client.AddSmsTemplate(req)
        result = json.loads(resp.to_json_string())
        output_json(result)
    except TencentCloudSDKException as e:
        from _common import handle_api_error
        handle_api_error(e)
    except Exception as e:  # pylint: disable=broad-except
        output_error("UNEXPECTED_ERROR", str(e))


if __name__ == "__main__":
    main()
