#!/usr/bin/env python3
"""Minimal standard-library client for the VPCS public paper-check workflow.

The script intentionally exposes only two agent-facing operations:

* ``submit``: create an order, upload the document, bind the upload and return
  the order number plus browser URLs for payment/progress/reports.
* ``status``: query one order and return its current state plus the browser URL
  that best matches the next human action.

Payment, CAPTCHA, report reading and verification remain in the browser.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
import mimetypes
import re
import secrets
import sys
import urllib.error
import urllib.parse
import urllib.request
from email.utils import formatdate
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config.json"
DOMAIN_PATH = ROOT / "domains" / "cqccjy.json"

TERMINAL_STATUSES = {
    "REPORT_READY",
    "COMPLETED",
    "COMPLETE",
    "SUCCESS",
    "SUCCEEDED",
    "DONE",
}
PAID_STATUSES = {"PAID", "SUCCESS", "COMPLETED", "PAY_SUCCESS", "PAYED"}

# Common full names are accepted without a product-catalog request. Agents can
# also pass the short code directly (for example ``dxs`` or ``aigc``).
PRODUCT_ALIASES = {
    "维普查重大学生版": "dxs",
    "维普大学生版": "dxs",
    "维普查重研究生版": "yjs",
    "维普研究生版": "yjs",
    "维普查重编辑部版": "bjb",
    "维普查重职称版": "zc",
    "维普查重作业版": "zy",
    "维普查重科研版": "ky",
    "维普aigc检测": "aigc",
    "维普论文格式检测大学生版": "format_dxs",
    "维普格式检测大学生版": "format_dxs",
    "维普斟知智评大学生版": "zzzp_dxs",
    "维普斟知智评研究生版": "zzzp_yjs",
    "维普斟知智评期刊版": "zzzp_qkb",
}


class VpcsError(RuntimeError):
    """An actionable error without credentials, file contents or stack traces."""


def normalize_product(value: Any) -> str:
    text = str(value or "").strip()
    compact = re.sub(r"[\s·•,，。:：/\\()（）\[\]【】_\\-]+", "", text).lower()
    return PRODUCT_ALIASES.get(compact, text)


def load_settings() -> tuple[dict[str, Any], dict[str, Any]]:
    try:
        config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        domain = json.loads(DOMAIN_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise VpcsError(f"无法读取 Skill 配置: {exc}") from exc
    base_url = domain.get("base_url")
    if not isinstance(base_url, str) or not base_url.startswith("https://"):
        raise VpcsError("维普基域名必须是 HTTPS")
    if domain.get("owner_user_id") != 2:
        raise VpcsError("维普域名配置的业务归属不匹配")
    return config, domain


def endpoint(domain: dict[str, Any], name: str, **values: Any) -> str:
    path = (domain.get("api") or {}).get(name)
    if not isinstance(path, str) or not path.startswith("/"):
        raise VpcsError(f"未配置接口: {name}")
    try:
        path = path.format(**values)
    except KeyError as exc:
        raise VpcsError(f"接口缺少参数: {exc.args[0]}") from exc
    return domain["base_url"].rstrip("/") + path


def browser_urls(domain: dict[str, Any], order_no: Any | None = None) -> dict[str, str]:
    """Build only configured first-party browser pages.

    These are page URLs, not guessed API/download URLs. A report download URL
    is added only when the server returns a real HTTPS URL in an order result.
    """
    pages: dict[str, str] = {}
    for name in ("entry", "payment", "progress", "reports", "verify"):
        template = (domain.get("pages") or {}).get(name)
        if not isinstance(template, str):
            continue
        if "{order_no}" in template:
            if order_no in (None, ""):
                continue
            template = template.replace(
                "{order_no}", urllib.parse.quote(str(order_no), safe="")
            )
        pages[name] = template
    return pages


def unwrap(payload: Any) -> Any:
    if not isinstance(payload, dict):
        return payload
    code = payload.get("code")
    if code not in (None, 0, "0", 200, "200"):
        message = payload.get("msg") or payload.get("message") or "请求失败"
        raise VpcsError(f"服务端返回错误（{code}）: {message}")
    return payload.get("data", payload)


def find_value(data: Any, *keys: str) -> Any:
    if isinstance(data, dict):
        for key in keys:
            value = data.get(key)
            if value not in (None, ""):
                return value
        for value in data.values():
            found = find_value(value, *keys)
            if found not in (None, ""):
                return found
    elif isinstance(data, list):
        for value in data:
            found = find_value(value, *keys)
            if found not in (None, ""):
                return found
    return None


def as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        return value.strip().lower() not in {
            "",
            "0",
            "false",
            "no",
            "n",
            "off",
            "none",
            "null",
        }
    return bool(value)


def is_paid(order: Any) -> bool:
    flag = find_value(order, "paid", "isPaid", "is_paid")
    if isinstance(flag, bool):
        return flag
    status = find_value(
        order,
        "payStatus",
        "pay_status",
        "paymentStatus",
        "payment_status",
        "paymentFlowState",
    )
    return str(status or "").strip().upper() in PAID_STATUSES


class RestClient:
    def __init__(self, timeout: int = 30, dry_run: bool = False):
        self.timeout = max(int(timeout), 1)
        self.dry_run = dry_run

    def request(
        self,
        method: str,
        url: str,
        *,
        payload: Any = None,
        headers: dict[str, str] | None = None,
        raw: bool = False,
    ) -> Any:
        if not url.startswith("https://"):
            raise VpcsError("只允许向 HTTPS 接口或 OSS 地址发请求")
        request_headers = {
            "Accept": "application/json",
            "User-Agent": "vpcs-paper-check-skill/1.0",
        }
        request_headers.update(headers or {})
        if payload is None:
            body = None
        elif isinstance(payload, bytes):
            body = payload
        else:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            request_headers.setdefault("Content-Type", "application/json")
        if self.dry_run:
            return {
                "dry_run": True,
                "method": method.upper(),
                "url": url,
                "body_bytes": len(body or b""),
            }
        request = urllib.request.Request(
            url, data=body, headers=request_headers, method=method.upper()
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                data = response.read(3 * 1024 * 1024 + 1)
                if len(data) > 3 * 1024 * 1024:
                    raise VpcsError("接口响应超过 3 MB，已停止读取")
                if raw:
                    return data
                if not data:
                    return None
                try:
                    return unwrap(json.loads(data.decode("utf-8")))
                except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                    raise VpcsError("接口返回的不是 UTF-8 JSON") from exc
        except urllib.error.HTTPError as exc:
            detail = exc.read(600).decode("utf-8", errors="replace")
            raise VpcsError(f"HTTP {exc.code}: {detail}") from exc
        except (urllib.error.URLError, TimeoutError) as exc:
            raise VpcsError(f"网络请求失败: {exc}") from exc


def validate_file(path_value: str, config: dict[str, Any]) -> tuple[Path, bytes, str]:
    path = Path(path_value).expanduser()
    if not path.is_file():
        raise VpcsError(f"文件不存在: {path}")
    limits = config.get("limits") or {}
    max_bytes = int(limits.get("max_file_bytes", 50 * 1024 * 1024))
    if path.stat().st_size > max_bytes:
        raise VpcsError(f"文件超过 {max_bytes} 字节上限")
    supported = {str(item).lower() for item in limits.get("supported_extensions", [])}
    if supported and path.suffix.lower() not in supported:
        raise VpcsError(
            f"不支持的文件格式 {path.suffix}；支持: {', '.join(sorted(supported))}"
        )
    try:
        content = path.read_bytes()
    except OSError as exc:
        raise VpcsError(f"无法读取文件: {exc}") from exc
    return path, content, mimetypes.guess_type(path.name)[0] or "application/octet-stream"


def validate_metadata(args: argparse.Namespace, config: dict[str, Any]) -> None:
    limits = config.get("limits") or {}
    title = (args.title or "").strip()
    author = (args.author or "").strip()
    max_title = int(limits.get("max_title_chars", 128))
    min_author = int(limits.get("min_author_chars", 2))
    max_author = int(limits.get("max_author_chars", 20))
    if not title:
        raise VpcsError("请填写论文题目")
    if len(title) > max_title:
        raise VpcsError(f"论文题目不能超过 {max_title} 个字符")
    if not author:
        raise VpcsError("请填写作者")
    if len(author) < min_author or len(author) > max_author:
        raise VpcsError(f"作者名称需为 {min_author}-{max_author} 个字符")
    if not any(
        "一" <= char <= "鿿" or (char.isascii() and char.isalnum())
        for char in author
    ):
        raise VpcsError("作者名称不能是纯符号")


def make_visitor_key() -> str:
    return "vpcs-" + secrets.token_hex(16)


def upload_with_ticket(
    client: RestClient,
    ticket: dict[str, Any],
    content: bytes,
    content_type: str,
) -> str:
    """Upload using either a signed URL or the current Aliyun OSS ticket."""
    upload_url = ticket.get("uploadUrl") or ticket.get("upload_url")
    headers = {
        str(key): str(value) for key, value in (ticket.get("headers") or {}).items()
    }
    headers.setdefault("Content-Type", content_type)
    if upload_url:
        client.request(
            "PUT", str(upload_url), payload=content, headers=headers, raw=True
        )
        return str(ticket.get("objectKey") or ticket.get("object_key") or "")

    endpoint_value = str(ticket.get("endpoint") or "")
    bucket = str(ticket.get("bucketName") or "")
    object_key = str(ticket.get("uploadObjectKey") or "")
    access_id = str(ticket.get("accessKeyId") or "")
    access_secret = str(ticket.get("accessKeySecret") or "")
    security_token = str(ticket.get("securityToken") or "")
    if not all((endpoint_value, bucket, object_key, access_id, access_secret)):
        raise VpcsError("上传票据缺少 uploadUrl 或 OSS 临时字段")

    endpoint_value = (
        endpoint_value
        if endpoint_value.startswith("https://")
        else "https://" + endpoint_value
    )
    parsed = urllib.parse.urlsplit(endpoint_value)
    object_path = "/" + urllib.parse.quote(object_key.lstrip("/"), safe="/%:@")
    upload_url = urllib.parse.urlunsplit(
        (
            parsed.scheme,
            f"{bucket}.{parsed.netloc}",
            parsed.path.rstrip("/") + object_path,
            "",
            "",
        )
    )
    date = formatdate(usegmt=True)
    headers["Date"] = date
    if security_token:
        headers["x-oss-security-token"] = security_token
    canonical = {
        key.lower(): " ".join(str(value).strip().split())
        for key, value in headers.items()
        if key.lower().startswith("x-oss-")
    }
    canonical_headers = "".join(
        f"{key}:{canonical[key]}\n" for key in sorted(canonical)
    )
    string_to_sign = (
        "PUT\n\n"
        + headers["Content-Type"]
        + "\n"
        + date
        + "\n"
        + canonical_headers
        + f"/{bucket}{object_path}"
    )
    signature = base64.b64encode(
        hmac.new(
            access_secret.encode(), string_to_sign.encode(), hashlib.sha1
        ).digest()
    ).decode()
    headers["Authorization"] = f"OSS {access_id}:{signature}"
    if client.dry_run:
        return str(ticket.get("objectKey") or ticket.get("object_key") or object_key)
    try:
        request = urllib.request.Request(
            upload_url, data=content, headers=headers, method="PUT"
        )
        with urllib.request.urlopen(request, timeout=client.timeout) as response:
            if response.status not in (200, 201):
                raise VpcsError(f"OSS 上传失败: HTTP {response.status}")
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
        raise VpcsError(f"OSS 上传失败: {exc}") from exc
    return str(ticket.get("objectKey") or ticket.get("object_key") or object_key)


def choose_browser_url(
    urls: dict[str, str],
    data: Any,
) -> tuple[str | None, str]:
    status = str(find_value(data, "status") or "").strip().upper()
    paid = is_paid(data)
    can_download = as_bool(find_value(data, "canDownloadReport", "can_download_report"))
    can_submit = as_bool(find_value(data, "canSubmitDetect", "can_submit_detect"))
    if can_download or status in TERMINAL_STATUSES:
        return urls.get("reports"), "报告已可查看，打开报告页下载；需要确认来源时再去验真页。"
    if can_submit or paid or status in {"COUNTING", "PARSING", "DETECTING", "SUBMITTED"}:
        return urls.get("progress"), "打开进度页查看解析/检测状态，按页面提示继续。"
    return urls.get("payment"), "打开支付页由用户完成支付，支付后回到同一订单进度页。"


def result(
    action: str,
    domain: dict[str, Any],
    data: Any,
    *,
    order_no: Any | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resolved = str(order_no or find_value(data, "orderNo", "order_no", "bizNo") or "") or None
    urls = browser_urls(domain, resolved)
    if resolved:
        selected, next_action = choose_browser_url(urls, data)
    else:
        selected, next_action = urls.get("entry"), "打开维普入口继续操作。"
    report_url = find_value(
        data, "reportDownloadUrl", "report_download_url", "downloadUrl"
    )
    if isinstance(report_url, str) and report_url.startswith("https://"):
        urls["report_download"] = report_url
    payload: dict[str, Any] = {
        "action": action,
        "order_no": resolved,
        "status": find_value(data, "status"),
        "status_label": find_value(data, "statusLabel", "status_label"),
        "pay_status": find_value(
            data,
            "payStatus",
            "pay_status",
            "paymentStatus",
            "payment_status",
            "paymentFlowState",
        ),
        "word_count": find_value(data, "wordCount", "word_count", "actualWordCount"),
        "billing_word_count": find_value(data, "billingWordCount", "billing_word_count"),
        "need_supplement": as_bool(
            find_value(data, "needSupplement", "need_supplement")
        ),
        "can_supplement_pay": as_bool(
            find_value(data, "canSupplementPay", "can_supplement_pay")
        ),
        "fail_reason": find_value(data, "failReason", "fail_reason"),
        "browser_url": selected,
        "browser_action": "OPEN_BROWSER",
        "browser_urls": urls,
        "report_download_url": (
            report_url if isinstance(report_url, str) and report_url.startswith("https://") else None
        ),
        "next_action": next_action,
    }
    if extra:
        payload.update(extra)
    return payload


def load_order(client: RestClient, domain: dict[str, Any], order_no: str) -> Any:
    order_no = order_no.strip()
    if not order_no:
        raise VpcsError("订单号不能为空")
    return client.request("GET", endpoint(domain, "order", order_no=order_no))


def submit_order(
    client: RestClient,
    config: dict[str, Any],
    domain: dict[str, Any],
    args: argparse.Namespace,
) -> dict[str, Any]:
    validate_metadata(args, config)
    path, content, content_type = validate_file(args.file, config)
    product_type = normalize_product(args.product_type)
    if not product_type:
        raise VpcsError("请填写 --product-type")

    if client.dry_run:
        return result(
            "submit",
            domain,
            {"productType": product_type, "status": "WAIT_PAYMENT", "payStatus": "UNPAID"},
            extra={"dry_run": True, "file_name": path.name, "product_type": product_type},
        )

    draft = client.request(
        "POST",
        endpoint(domain, "create_draft"),
        payload={
            "productType": product_type,
            "detectMode": "AUTO",
            "title": args.title.strip(),
            "author": args.author.strip(),
            "publishDate": args.publish_date or None,
            "visitorKey": make_visitor_key(),
        },
    )
    order_no = find_value(draft, "orderNo", "order_no")
    if not order_no:
        raise VpcsError("建单接口没有返回订单号")

    ticket = client.request(
        "POST",
        endpoint(domain, "presign"),
        payload={"orderNo": order_no, "fileName": path.name},
    )
    if not isinstance(ticket, dict):
        raise VpcsError("上传接口没有返回有效票据")
    object_key = upload_with_ticket(client, ticket, content, content_type)
    if not object_key:
        raise VpcsError("上传票据没有返回 objectKey")

    completed = client.request(
        "POST",
        endpoint(domain, "complete_upload"),
        payload={
            "orderNo": order_no,
            "productType": product_type,
            "title": args.title.strip(),
            "author": args.author.strip(),
            "publishDate": args.publish_date or None,
            "objectKey": object_key,
            "fileName": path.name,
            "contentType": content_type,
            "fileSize": len(content),
        },
    )
    order = client.request("GET", endpoint(domain, "order", order_no=order_no))
    return result(
        "submit",
        domain,
        order or completed,
        order_no=order_no,
        extra={
            "file_name": path.name,
            "product_type": product_type,
            "uploaded": True,
        },
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="维普 VPCS 最小订单接口")
    parser.add_argument("--dry-run", action="store_true", help="只校验参数，不发网络请求")
    parser.add_argument("--timeout", type=int, default=30)
    sub = parser.add_subparsers(dest="command", required=True)

    def runtime_flags(command: argparse.ArgumentParser) -> None:
        command.add_argument("--dry-run", action="store_true", default=argparse.SUPPRESS)
        command.add_argument("--timeout", type=int, default=argparse.SUPPRESS)

    submit = sub.add_parser("submit", help="上传论文并返回订单号和浏览器链接")
    runtime_flags(submit)
    submit.add_argument("--product-type", required=True, help="产品编码或产品完整名称")
    submit.add_argument("--title", required=True, help="论文题目")
    submit.add_argument("--author", required=True, help="作者姓名")
    submit.add_argument("--file", required=True, help="待检测论文文件")
    submit.add_argument("--publish-date", help="页面要求时填写发表日期")

    status = sub.add_parser("status", help="查询订单状态并返回浏览器链接")
    runtime_flags(status)
    status.add_argument("--order-no", required=True, help="submit 返回的订单号")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        config, domain = load_settings()
        client = RestClient(args.timeout, args.dry_run)
        if args.command == "submit":
            output = submit_order(client, config, domain, args)
        elif args.command == "status":
            order = load_order(client, domain, args.order_no)
            output = result("status", domain, order, order_no=args.order_no)
        else:
            raise VpcsError("未知命令")
        print(json.dumps(output, ensure_ascii=False, indent=2, default=str))
        return 0
    except VpcsError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
