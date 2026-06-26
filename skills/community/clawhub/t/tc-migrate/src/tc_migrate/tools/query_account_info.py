#!/usr/bin/env python3
"""
查询腾讯云账号的 UIN 信息。

用法：
    python -m tc_migrate.tools.query_account_info --secret-id AKIDxxx --secret-key xxx

输出：
    账号 UIN、OwnerUin、AppId
"""

import argparse
import sys

from tencentcloud.common import credential
from tencentcloud.cam.v20190116 import cam_client, models as cam_models


def query_account_info(secret_id: str, secret_key: str) -> dict:
    """查询账号 UIN 信息，返回 dict"""
    cred = credential.Credential(secret_id, secret_key)
    cam = cam_client.CamClient(cred, "")
    req = cam_models.GetUserAppIdRequest()
    resp = cam.GetUserAppId(req)
    return {
        "uin": str(resp.Uin),
        "owner_uin": str(resp.OwnerUin),
        "app_id": str(resp.AppId) if resp.AppId else "",
    }


def main():
    parser = argparse.ArgumentParser(description="查询腾讯云账号 UIN 信息")
    parser.add_argument("--secret-id", required=True, help="SecretId")
    parser.add_argument("--secret-key", required=True, help="SecretKey")
    args = parser.parse_args()

    try:
        info = query_account_info(args.secret_id, args.secret_key)
        print(f"UIN:      {info['uin']}")
        print(f"OwnerUin: {info['owner_uin']}")
        if info["app_id"]:
            print(f"AppId:    {info['app_id']}")
    except Exception as e:
        print(f"❌ 查询失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
