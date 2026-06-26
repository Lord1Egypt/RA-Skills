# -*- coding: utf-8 -*-
"""
tencentcloud-aigc-recog-text: 腾讯云 AI 生成文本识别 Skill
调用 TextModeration 接口，通过设置 Type=TEXT_AIGC 检测文本是否为 AI 生成。

用法：
  python main.py "待检测的文本内容"
  python main.py /path/to/textfile.txt
  python main.py --stdin < textfile.txt
  python main.py --file /path/to/textfile.txt
  python main.py --data-id my_id "文本内容"
"""

import json
import os
import sys
import base64  # noqa: E402

try:
    from tencentcloud.common import credential  # noqa: E402
    from tencentcloud.common.profile.client_profile import ClientProfile  # noqa: E402
    from tencentcloud.common.profile.http_profile import HttpProfile  # noqa: E402
    from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException  # noqa: E402
    from tencentcloud.tms.v20201229 import tms_client, models  # noqa: E402
except ImportError:
    print("错误: 缺少依赖 tencentcloud-sdk-python，请执行: pip install tencentcloud-sdk-python", file=sys.stderr)
    sys.exit(1)


# ============================================================
# 第一部分：凭证检测
# ============================================================

def get_credentials():
    """
    检查腾讯云 API 凭证环境变量。
    支持 TENCENTCLOUD_TOKEN 临时凭证（STS Token）。
    缺失时输出配置引导并退出。
    """
    secret_id = os.getenv("TENCENTCLOUD_SECRET_ID")
    secret_key = os.getenv("TENCENTCLOUD_SECRET_KEY")
    token = os.getenv("TENCENTCLOUD_TOKEN")

    if not secret_id or not secret_key:
        missing = []
        if not secret_id:
            missing.append("TENCENTCLOUD_SECRET_ID")
        if not secret_key:
            missing.append("TENCENTCLOUD_SECRET_KEY")
        error_msg = {
            "error": "CREDENTIALS_NOT_CONFIGURED",
            "message": f"缺少环境变量: {', '.join(missing)}",
            "guide": {
                "step1": "开通AI生成文本检测服务: https://console.cloud.tencent.com/cms/clouds/LLM",
                "step2": "获取 API 密钥: https://console.cloud.tencent.com/cam/capi",
                "step3_linux": (
                    'export TENCENTCLOUD_SECRET_ID="your_secret_id"\n'
                    'export TENCENTCLOUD_SECRET_KEY="your_secret_key"'
                ),
                "step3_windows": (
                    '$env:TENCENTCLOUD_SECRET_ID = "your_secret_id"\n'
                    '$env:TENCENTCLOUD_SECRET_KEY = "your_secret_key"'
                ),
            },
        }
        print(json.dumps(error_msg, ensure_ascii=False, indent=2))
        sys.exit(1)

    # 支持临时凭证（STS Token）
    if token:
        cred = credential.Credential(secret_id, secret_key, token)
    else:
        cred = credential.Credential(secret_id, secret_key)

    return cred


def get_biz_type():
    """
    从环境变量 TENCENTCLOUD_AIGC_RECOG_TEXT_BIZ_TYPE 获取审核策略编号（BizType）。
    每个用户都需要使用自己的 BizType，为空则报错退出。
    """
    biz_type = os.getenv("TENCENTCLOUD_AIGC_RECOG_TEXT_BIZ_TYPE", "").strip()

    if not biz_type:
        error_msg = {
            "error": "BIZ_TYPE_NOT_CONFIGURED",
            "message": "缺少环境变量: TENCENTCLOUD_AIGC_RECOG_TEXT_BIZ_TYPE",
            "guide": {
                "step1": "在腾讯云控制台获取文本AI生成检测配套策略: https://console.cloud.tencent.com/cms/clouds/manage",
                "step2_linux": 'export TENCENTCLOUD_AIGC_RECOG_TEXT_BIZ_TYPE="your_biz_type"',
                "step2_windows": '$env:TENCENTCLOUD_AIGC_RECOG_TEXT_BIZ_TYPE = "your_biz_type"',
            },
        }
        print(json.dumps(error_msg, ensure_ascii=False, indent=2))
        sys.exit(1)

    return biz_type


# ============================================================
# 第二部分：命令行参数解析
# ============================================================

def parse_args():
    """
    解析命令行参数。
    支持：位置参数（文本或文件路径）、--stdin、--file、--data-id、--biz-type
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="腾讯云 AI 生成文本识别（TextModeration TEXT_AIGC）"
    )
    parser.add_argument(
        "text", nargs="?", default=None,
        help="待检测的文本内容，或文本文件的路径（自动判断）"
    )
    parser.add_argument(
        "--stdin", action="store_true",
        help="从标准输入读取待检测文本"
    )
    parser.add_argument(
        "--file", dest="file_path", default=None,
        help="指定文本文件路径，读取其内容作为待检测文本"
    )
    parser.add_argument(
        "--data-id", dest="data_id", default=None,
        help="业务数据标识，用于关联检测结果（可选，最长 128 字符）"
    )

    args = parser.parse_args()
    return args


def get_input_text(args):
    """
    根据命令行参数获取待检测文本。
    优先级：--stdin > --file > 位置参数（自动判断文件路径 / 直接文本）
    """
    text = None

    if args.stdin:
        # 从标准输入读取
        text = sys.stdin.read()
    elif args.file_path:
        # 从指定文件读取
        if not os.path.isfile(args.file_path):
            print(json.dumps({
                "error": "FILE_NOT_FOUND",
                "message": f"指定的文件不存在: {args.file_path}",
            }, ensure_ascii=False, indent=2))
            sys.exit(1)
        with open(args.file_path, "r", encoding="utf-8") as f:
            text = f.read()
    elif args.text is not None:
        # 位置参数：自动判断是文件路径还是文本字符串
        if os.path.isfile(args.text):
            with open(args.text, "r", encoding="utf-8") as f:
                text = f.read()
        else:
            text = args.text
    else:
        # 未提供任何输入
        print(json.dumps({
            "error": "NO_INPUT",
            "message": "未提供待检测文本。",
            "usage": {
                "direct": 'python main.py "待检测的文本内容"',
                "file": 'python main.py /path/to/textfile.txt',
                "stdin": 'echo "文本" | python main.py --stdin',
                "file_flag": 'python main.py --file /path/to/textfile.txt',
            },
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    # 检查文本是否为空
    if not text or not text.strip():
        print(json.dumps({
            "error": "EMPTY_TEXT",
            "message": "输入文本为空，请提供有效的待检测文本。",
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    # 检查文本长度限制（10000 个 Unicode 字符）
    if len(text) > 10000:
        print(json.dumps({
            "error": "TEXT_TOO_LONG",
            "message": f"文本长度为 {len(text)} 个字符，超过 API 限制的 10000 个 Unicode 字符。请截断或分段检测。",
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    return text


# ============================================================
# 第三部分：API 调用与结果输出
# ============================================================

def call_text_moderation(cred, text, data_id=None, biz_type=None):
    """
    调用腾讯云 TextModeration 接口，设置 Type=TEXT_AIGC 进行 AI 生成文本识别。
    返回解析后的 JSON 结果。
    """
    # 配置 HTTP Profile
    http_profile = HttpProfile()
    http_profile.endpoint = "tms.tencentcloudapi.com"

    # 配置 Client Profile
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile

    # 创建客户端（Region 使用广州区域，TMS 服务默认区域）
    client = tms_client.TmsClient(cred, "ap-guangzhou", client_profile)

    # 构造请求
    req = models.TextModerationRequest()

    # 文本内容：UTF-8 编码后 Base64
    content_base64 = base64.b64encode(text.encode("utf-8")).decode("utf-8")
    req.Content = content_base64

    # 设置检测类型为 AI 生成文本识别
    req.Type = "TEXT_AIGC"

    # 可选参数
    if data_id:
        req.DataId = data_id
    if biz_type:
        req.BizType = biz_type

    # 发送请求
    resp = client.TextModeration(req)
    return resp


def format_output(resp):
    """
    解析 API 响应，以 JSON 格式输出结构化结果。
    """
    # 将响应转为字典
    resp_dict = json.loads(resp.to_json_string())

    result = {
        "suggestion": resp_dict.get("Suggestion", ""),
        "label": resp_dict.get("Label", ""),
        "score": resp_dict.get("Score", 0),
        "keywords": resp_dict.get("Keywords", []),
    }

    # 详细检测结果（如有）
    detail_results = resp_dict.get("DetailResults")
    if detail_results:
        result["detail_results"] = []
        for detail in detail_results:
            item = {
                "label": detail.get("Label", ""),
                "suggestion": detail.get("Suggestion", ""),
                "score": detail.get("Score", 0),
            }
            keywords = detail.get("Keywords")
            if keywords:
                item["keywords"] = keywords
            sub_label = detail.get("SubLabel")
            if sub_label:
                item["sub_label"] = sub_label
            result["detail_results"].append(item)

    # 风险详情（如有）
    risk_details = resp_dict.get("RiskDetails")
    if risk_details:
        result["risk_details"] = []
        for risk in risk_details:
            item = {
                "label": risk.get("Label", ""),
                "level": risk.get("Level", 0),
            }
            keywords = risk.get("Keywords")
            if keywords:
                item["keywords"] = keywords
            result["risk_details"].append(item)

    # 二级标签
    sub_label = resp_dict.get("SubLabel")
    if sub_label:
        result["sub_label"] = sub_label

    # 附加信息
    extra = resp_dict.get("Extra")
    if extra:
        result["extra"] = extra

    # DataId 回传
    data_id = resp_dict.get("DataId")
    if data_id:
        result["data_id"] = data_id

    # 请求 ID
    result["request_id"] = resp_dict.get("RequestId", "")

    return result


# ============================================================
# 主函数
# ============================================================

def main():
    args = parse_args()
    text = get_input_text(args)
    cred = get_credentials()
    biz_type = get_biz_type()

    try:
        resp = call_text_moderation(cred, text, args.data_id, biz_type)
        result = format_output(resp)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    except TencentCloudSDKException as err:
        print(json.dumps({
            "error": "API_ERROR",
            "code": err.code,
            "message": err.message,
            "request_id": err.requestId or "",
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    except Exception as err:
        print(json.dumps({
            "error": "UNEXPECTED_ERROR",
            "message": str(err),
        }, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
