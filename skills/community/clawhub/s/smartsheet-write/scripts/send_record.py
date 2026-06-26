#!/usr/bin/env python3
"""
send_record.py — 向企业微信智能表格 Webhook 写入数据

用法（命令行）：
  python send_record.py --webhook "https://qyapi.weixin.qq.com/..." --data '{"add_records":[...]}'
  python send_record.py --webhook "https://..." --file payload.json

用法（代码引用）：
  from scripts.send_record import send_to_smartsheet, date_to_ms

  # 日期转换
  ts = date_to_ms("2025-03-20")        # → "1742400000000"
  ts = date_to_ms("今天")               # → 今天零点的毫秒时间戳

  # 写入数据
  result = send_to_smartsheet(webhook_url, {
      "add_records": [{"values": {"fABCD1": "登录页白屏", "fABCD2": [{"text": "前端"}]}}]
  })
  print(result)  # {"errcode": 0, "errmsg": "ok", "add_records": [{"record_id": "..."}]}
"""

import json
import sys
import argparse
import urllib.request
import urllib.error
from datetime import datetime, timedelta


def date_to_ms(date_str: str) -> str:
    """
    将自然语言或标准格式日期转为毫秒时间戳字符串（本地时间）。

    支持格式：
      - "今天" / "明天" / "后天"
      - "2025-03-20"
      - "2025-03-20 14:30"
      - "2025-03-20T14:30:00"
      - "2025/03/20"
      - 纯数字字符串（已是时间戳）直接返回

    Returns:
        毫秒时间戳字符串，例如 "1742400000000"
    """
    date_str = date_str.strip()

    # 已是数字时间戳
    if date_str.isdigit():
        return date_str

    now = datetime.now()

    # 相对日期
    relative = {"今天": 0, "明天": 1, "后天": 2}
    if date_str in relative:
        dt = (now + timedelta(days=relative[date_str])).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        return str(int(dt.timestamp() * 1000))

    # 标准格式解析
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d %H:%M",
        "%Y/%m/%d",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M",
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return str(int(dt.timestamp() * 1000))
        except ValueError:
            continue

    raise ValueError(
        f"无法解析日期「{date_str}」，支持格式：今天/明天/后天、2025-03-20、2025-03-20 14:30 等"
    )


def send_to_smartsheet(webhook_url: str, payload: dict, timeout: int = 30) -> dict:
    """
    向企业微信智能表格 Webhook 发送数据。

    Args:
        webhook_url: 完整 Webhook URL，格式为
                     https://qyapi.weixin.qq.com/cgi-bin/wedoc/smartsheet/webhook?key=XXX
        payload:     符合智能表格格式的 dict，必须包含 add_records 或 update_records。
                     示例：
                     {
                       "add_records": [
                         {"values": {"fABCD1": "问题描述", "fABCD2": [{"text": "前端"}]}}
                       ]
                     }
        timeout:     请求超时秒数，默认 30

    Returns:
        API 响应 dict，包含 errcode、errmsg、add_records / update_records 等字段。
        errcode=0 表示成功。

    Raises:
        ValueError:              payload 格式错误
        urllib.error.URLError:   网络连接失败
        RuntimeError:            HTTP 层面错误（非 2xx 响应）
    """
    if not isinstance(payload, dict):
        raise ValueError("payload 必须是 dict")
    if "add_records" not in payload and "update_records" not in payload:
        raise ValueError("payload 必须包含 add_records 或 update_records 字段")

    # Webhook 域名检查，避免使用不稳定的 testapi
    if "testapi.work.weixin.qq.com" in webhook_url:
        import warnings
        warnings.warn(
            "检测到 testapi 域名，该域名不稳定，建议替换为 qyapi.weixin.qq.com",
            UserWarning,
            stacklevel=2,
        )

    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        webhook_url,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code}: {body}")

    return result


def _format_result(result: dict) -> str:
    """将 API 响应格式化为人类可读的摘要。"""
    errcode = result.get("errcode", 0)
    if errcode != 0:
        return f"❌ 写入失败 (errcode {errcode}): {result.get('errmsg', '未知错误')}"

    added = result.get("add_records", [])
    updated = result.get("update_records", [])
    parts = []
    if added:
        ids = [r.get("record_id", "?") for r in added]
        parts.append(f"新增 {len(added)} 条，record_id: {', '.join(ids)}")
    if updated:
        ids = [r.get("record_id", "?") for r in updated]
        parts.append(f"更新 {len(updated)} 条，record_id: {', '.join(ids)}")
    return "✅ " + "；".join(parts) if parts else "✅ 操作成功"


def main():
    parser = argparse.ArgumentParser(
        description="向企业微信智能表格写入数据",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  # 添加一条记录
  python send_record.py --webhook "https://qyapi.weixin.qq.com/..." \\
    --data '{"add_records": [{"values": {"fABCD1": "登录页白屏"}}]}'

  # 从文件读取 payload
  python send_record.py --webhook "https://qyapi.weixin.qq.com/..." --file payload.json

  # 日期转换
  python send_record.py --date "2025-03-20"
  python send_record.py --date "今天"
        """,
    )
    parser.add_argument("--webhook", help="Webhook 完整 URL")
    parser.add_argument("--data", help="JSON 字符串 payload")
    parser.add_argument("--file", help="JSON 文件路径")
    parser.add_argument("--date", help="测试日期转换，输出毫秒时间戳")
    args = parser.parse_args()

    # 日期转换模式
    if args.date:
        try:
            ts = date_to_ms(args.date)
            print(f"{args.date} → {ts}")
        except ValueError as e:
            print(f"错误: {e}", file=sys.stderr)
            sys.exit(1)
        return

    # 写入模式
    if not args.webhook:
        parser.error("写入模式需要提供 --webhook")

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            payload = json.load(f)
    elif args.data:
        payload = json.loads(args.data)
    else:
        parser.error("需要提供 --data 或 --file")

    result = send_to_smartsheet(args.webhook, payload)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print()
    print(_format_result(result))

    if result.get("errcode", 0) != 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
