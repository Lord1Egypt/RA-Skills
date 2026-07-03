#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
腾讯云短信 — 发送短信 (SendSms)

发送验证码、通知类或营销短信，支持国内短信与国际/港澳台短信。
支持通过群发 Excel 模板文件批量发送。

需要环境变量: TENCENTCLOUD_SECRET_ID, TENCENTCLOUD_SECRET_KEY

用法:
    # 直接指定手机号发送
    python send_sms.py --phone-number-set "+8618501234444" "+8618501234445" \
        --sdk-app-id "1400006666" --template-id "1110" \
        --sign-name "腾讯云" --template-param-set "4370"

    # 从群发 Excel 模板文件批量发送（每个号码可有独立模板变量）
    python send_sms.py --from-file "/path/to/群发模板.xlsx" \
        --sdk-app-id "1400006666" --template-id "1110" \
        --sign-name "腾讯云"
"""

import argparse
import json
import os
import sys
import time

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


MAX_PHONE_NUMBERS = 200
MAX_PHONES_PER_SECOND = 200  # 脚本侧保守限流：每秒提交号码数不超过 200


class _RateLimiter:
    """基于滑动窗口的号码提交速率限制器。

    确保在任意 1 秒窗口内提交的号码总数不超过 MAX_PHONES_PER_SECOND。
    """

    def __init__(self, max_phones_per_second=MAX_PHONES_PER_SECOND):
        self._limit = max_phones_per_second
        self._window_start = time.monotonic()
        self._window_count = 0

    def wait_if_needed(self, phone_count):
        """在发送前调用，必要时阻塞等待以遵守速率限制。"""
        now = time.monotonic()
        elapsed = now - self._window_start

        # 如果距离窗口起点已超过 1 秒，重置窗口
        if elapsed >= 1.0:
            self._window_start = now
            self._window_count = 0

        # 如果本窗口内加上本批号码会超限，等到下一个窗口
        if self._window_count + phone_count > self._limit:
            sleep_time = 1.0 - (time.monotonic() - self._window_start)
            if sleep_time > 0:
                time.sleep(sleep_time)
            self._window_start: float = time.monotonic()
            self._window_count = 0

        self._window_count += phone_count


def build_parser():
    parser = argparse.ArgumentParser(
        description="腾讯云短信 — 发送短信 (SendSms)"
    )
    # 手机号来源：--phone-number-set 或 --from-file 二选一
    phone_group = parser.add_mutually_exclusive_group(required=True)
    phone_group.add_argument(
        "--phone-number-set", nargs="+",
        help="手机号列表（E.164 格式，如 +8618501234444），单次最多 200 个",
    )
    phone_group.add_argument(
        "--from-file",
        help="群发 Excel 模板文件路径（.xlsx），从模板读取手机号和模板变量",
    )
    parser.add_argument("--sdk-app-id", required=True, help="短信 SdkAppId")
    parser.add_argument("--template-id", required=True, help="已审核通过的模板 ID")
    parser.add_argument("--sign-name", default="", help="已审核通过的签名内容（国内短信必填）")
    parser.add_argument(
        "--template-param-set", nargs="*", default=None,
        help="模板参数列表（空格分隔），参数个数需与模板匹配（使用 --from-file 时忽略此参数）",
    )
    parser.add_argument("--extend-code", default="", help="短信码号扩展号")
    parser.add_argument("--session-context", default="", help="用户 session 上下文，会原样返回")
    parser.add_argument("--sender-id", default="", help="国际/港澳台短信 Sender ID")
    parser.add_argument(
        "--international", type=int, default=0, choices=[0, 1],
        help="短信类型：0=国内短信（默认），1=国际/港澳台短信（仅 --from-file 模式使用）",
    )
    add_common_args(parser)
    return parser


def _parse_excel_file(file_path, international, template_id=None):
    """解析 Excel 群发模板文件。

    如果提供了 template_id，会自动查询模板实际变量数量，
    确保只取模板需要的变量列数，忽略多余列。
    """
    from parse_bulk_template import (
        parse_excel, ensure_openpyxl, query_template_variable_count,
    )
    ensure_openpyxl()

    expected_var_count = None
    template_content = None
    if template_id:
        expected_var_count, template_content = query_template_variable_count(
            template_id, international=international,
        )

    return parse_excel(
        file_path,
        international=bool(international),
        expected_var_count=expected_var_count,
        template_content=template_content,
    )


def _build_batches_from_excel(parsed):
    """将 Excel 解析结果按模板变量分组，相同变量的号码合并为一批。"""
    groups = {}
    for rec in parsed["records"]:
        key = tuple(rec["template_params"])
        groups.setdefault(key, []).append(rec["phone"])
    batches = []
    for params_tuple, phones in groups.items():
        for i in range(0, len(phones), MAX_PHONE_NUMBERS):
            batches.append({
                "phones": phones[i:i + MAX_PHONE_NUMBERS],
                "template_params": list(params_tuple),
            })
    return batches


def _build_send_params(args, phones, template_params):
    """根据 args 与本批号码/模板变量，构建 SendSms 的请求参数。"""
    params = {
        "PhoneNumberSet": phones,
        "SmsSdkAppId": args.sdk_app_id,
        "TemplateId": args.template_id,
    }
    if args.sign_name:
        params["SignName"] = args.sign_name
    if template_params and any(template_params):
        params["TemplateParamSet"] = template_params
    if args.extend_code:
        params["ExtendCode"] = args.extend_code
    if args.session_context:
        params["SessionContext"] = args.session_context
    if args.sender_id:
        params["SenderId"] = args.sender_id
    return params


def _annotate_send_status(result):
    """为 SendStatusSet 每条状态追加可读描述。"""
    if "SendStatusSet" not in result:
        return
    for status in result["SendStatusSet"]:
        code = status.get("Code", "")
        if code == "Ok":
            status["StatusDesc"] = "发送成功"
        else:
            status["StatusDesc"] = f"发送失败: {status.get('Message', code)}"


def _call_send_sms(client, params):
    """调用 SendSms 接口并返回解析后的结果。"""
    req = models.SendSmsRequest()
    req.from_json_string(json.dumps(params))
    resp = client.SendSms(req)
    result = json.loads(resp.to_json_string())
    _annotate_send_status(result)
    return result


def _dry_run_from_file(args, parsed, batches):
    """--from-file 模式的预览输出。"""
    total_phones = parsed["total_records"]
    preview = {
        "dry_run": True,
        "api": "SendSms",
        "source_file": parsed["file"],
        "sms_type": parsed["type"],
        "total_recipients": total_phones,
        "batch_count": len(batches),
        "batches_preview": [],
        "sign_name": args.sign_name or "(未指定，国际短信可为空)",
        "template_id": args.template_id,
        "estimated_sms_count": total_phones,
    }
    for idx, b in enumerate(batches[:5], 1):
        preview["batches_preview"].append({
            "batch": idx,
            "phone_count": len(b["phones"]),
            "phones_sample": b["phones"][:3],
            "template_params": b["template_params"],
        })
    if len(batches) > 5:
        preview["batches_preview_note"] = f"仅展示前 5 批，共 {len(batches)} 批"
    if parsed.get("warnings"):
        preview["warnings"] = parsed["warnings"]
    output_json(preview)


def _send_batches(args, parsed, batches):
    """--from-file 模式的实际批量发送。"""
    cred = get_credentials()
    client = build_client(cred, region=args.region)
    rate_limiter = _RateLimiter()
    all_results = []
    for idx, batch in enumerate(batches, 1):
        rate_limiter.wait_if_needed(len(batch["phones"]))
        params = _build_send_params(args, batch["phones"], batch["template_params"])
        try:
            result = _call_send_sms(client, params)
            all_results.append({"batch": idx, "result": result})
        except TencentCloudSDKException as e:
            from _common import handle_api_error
            handle_api_error(e)
        except Exception as e:  # pylint: disable=broad-except
            all_results.append({"batch": idx, "error": str(e)})
    output_json({
        "source_file": parsed["file"],
        "total_batches": len(batches),
        "results": all_results,
    })


def _run_from_file(args):
    """--from-file 模式入口。"""
    parsed = _parse_excel_file(
        args.from_file, args.international, template_id=args.template_id,
    )
    batches = _build_batches_from_excel(parsed)
    if args.dry_run:
        _dry_run_from_file(args, parsed, batches)
        return
    _send_batches(args, parsed, batches)


def _dry_run_direct(args, params):
    """直接指定手机号模式的预览输出。"""
    phone_count = len(args.phone_number_set)
    preview = {
        "dry_run": True,
        "api": "SendSms",
        "params": params,
        "summary": {
            "recipient_count": phone_count,
            "recipients_preview": args.phone_number_set[:5],
            "sign_name": args.sign_name or "(未指定，国际短信可为空)",
            "template_id": args.template_id,
            "template_params": args.template_param_set or [],
            "estimated_sms_count": phone_count,
        },
    }
    if phone_count > 5:
        preview["summary"]["recipients_preview_note"] = (
            f"仅展示前 5 个，共 {phone_count} 个号码"
        )
    if phone_count > MAX_PHONE_NUMBERS:
        preview["summary"]["warning"] = (
            f"号码数量 {phone_count} 超过单次上限 {MAX_PHONE_NUMBERS}，需分批发送"
        )
    output_json(preview)


def _run_direct(args):
    """直接指定手机号模式入口。"""
    if len(args.phone_number_set) > MAX_PHONE_NUMBERS:
        output_error(
            "PARAM_ERROR",
            f"单次发送手机号不能超过 {MAX_PHONE_NUMBERS} 个，"
            f"当前 {len(args.phone_number_set)} 个",
        )
    params = _build_send_params(
        args, args.phone_number_set, args.template_param_set,
    )
    if args.dry_run:
        _dry_run_direct(args, params)
        return

    cred = get_credentials()
    client = build_client(cred, region=args.region)
    try:
        result = _call_send_sms(client, params)
        output_json(result)
    except TencentCloudSDKException as e:
        from _common import handle_api_error
        handle_api_error(e)
    except Exception as e:  # pylint: disable=broad-except
        output_error("UNEXPECTED_ERROR", str(e))


def main():
    parser = build_parser()
    args = parser.parse_args()
    if args.from_file:
        _run_from_file(args)
    else:
        _run_direct(args)


if __name__ == "__main__":
    main()
