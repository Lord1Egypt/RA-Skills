#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
腾讯云短信 — 添加短信签名 (AddSmsSign)

创建短信签名并提交审核。仅企业认证用户可调用此接口。

需要环境变量: TENCENTCLOUD_SECRET_ID, TENCENTCLOUD_SECRET_KEY

用法:
    python add_sign.py --sign-name "腾讯云" --sign-type 0 --document-type 1 \
        --international 0 --sign-purpose 0 --proof-image /path/to/proof.jpg
"""

import argparse
import base64
import json
import os
import sys

# 确保路径可引入公共模块
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


def load_image_base64(file_path):
    """读取图片文件并返回 Base64 编码字符串。"""
    if not os.path.isfile(file_path):
        output_error("FILE_NOT_FOUND", f"图片文件不存在: {file_path}")
    with open(file_path, "rb") as f:
        raw = f.read()
    return base64.b64encode(raw).decode("utf-8")


def build_parser():
    parser = argparse.ArgumentParser(
        description="腾讯云短信 — 添加短信签名 (AddSmsSign)"
    )
    parser.add_argument("--sign-name", required=True, help="签名名称")
    parser.add_argument(
        "--sign-type", type=int, required=True,
        choices=[0, 4, 5],
        help="签名类型: 0=公司, 4=商标, 5=政府/机关事业单位/其他机构",
    )
    parser.add_argument(
        "--document-type", type=int, required=True,
        choices=[0, 1, 2, 3, 7],
        help="证明类型: 0=三证合一, 1=企业营业执照, 2=组织机构代码证书, 3=社会信用代码证书, 7=商标注册书",
    )
    parser.add_argument(
        "--international", type=int, required=True,
        choices=[0, 1],
        help="0=国内短信, 1=国际/港澳台短信",
    )
    parser.add_argument(
        "--sign-purpose", type=int, required=True,
        choices=[0, 1],
        help="签名用途: 0=自用, 1=他用",
    )
    parser.add_argument("--proof-image", required=True, help="资质证明图片文件路径")
    parser.add_argument("--commission-image", default=None, help="委托授权证明图片路径（他用时需要）")
    parser.add_argument("--remark", default="", help="申请备注")
    parser.add_argument(
        "--qualification-id", type=int, default=None,
        help="已审核通过的国内短信资质 ID（国内短信需填写）。前往 https://console.cloud.tencent.com/smsv2/enterprise 查看",
    )
    add_common_args(parser)
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    params = {
        "SignName": args.sign_name,
        "SignType": args.sign_type,
        "DocumentType": args.document_type,
        "International": args.international,
        "SignPurpose": args.sign_purpose,
        "ProofImage": load_image_base64(args.proof_image),
    }

    # 国内短信必须提供资质 ID
    if args.international == 0:
        if args.qualification_id is None:
            output_error(
                "MISSING_PARAM",
                "国内短信签名需要提供资质 ID (--qualification-id)。"
                "请前往 https://console.cloud.tencent.com/smsv2/enterprise 查看已审核通过的资质 ID",
            )
        params["QualificationId"] = args.qualification_id

    if args.commission_image:
        params["CommissionImage"] = load_image_base64(args.commission_image)
    if args.remark:
        params["Remark"] = args.remark

    if args.dry_run:
        # 预览模式：隐藏 Base64 图片内容，仅显示长度
        preview = dict(params)
        if "ProofImage" in preview:
            preview["ProofImage"] = f"<Base64, {len(params['ProofImage'])} chars>"
        if "CommissionImage" in preview:
            preview["CommissionImage"] = f"<Base64, {len(params['CommissionImage'])} chars>"
        output_json({"dry_run": True, "api": "AddSmsSign", "params": preview})
        return

    cred = get_credentials()
    client = build_client(cred, region=args.region)

    try:
        req = models.AddSmsSignRequest()
        req.from_json_string(json.dumps(params))
        resp = client.AddSmsSign(req)
        result = json.loads(resp.to_json_string())
        output_json(result)
    except TencentCloudSDKException as e:
        from _common import handle_api_error
        handle_api_error(e)
    except Exception as e:  # pylint: disable=broad-except
        output_error("UNEXPECTED_ERROR", str(e))


if __name__ == "__main__":
    main()
