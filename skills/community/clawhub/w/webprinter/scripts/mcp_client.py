#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""WebPrinter cloud print client."""

import argparse
import ipaddress
import json
import os
import socket
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Set, Union
from urllib.parse import urlparse

import requests


TOKEN_ENV_VAR = "WEBPRINTER_ACCESS_TOKEN"
BASE_URL = "https://any.webprinter.cn"
SKILL_VERSION = "1.0.10"
DEFAULT_TIMEOUT = 30
SUPPORTED_MEDIA_FORMATS = [
    "HTML",
    "PNG",
    "JPG",
    "PDF",
    "BMP",
    "WEBP",
    "WORD",
    "EXCEL",
    "PPT",
    "TEXT",
    "WPS",
    "ODF",
    "ODT",
    "ODS",
    "ODP",
    "ODG",
    "XPS",
    "PWG",
]
SUPPORTED_COLOR_MODES = ["COLOR", "MONOCHROME"]
MIN_COPIES = 1
MAX_COPIES = 99
PAPER_SIZE_DIMENSIONS = {
    "A0": {"width": 841.0, "height": 1189.0},
    "A1": {"width": 594.0, "height": 841.0},
    "A2": {"width": 420.0, "height": 594.0},
    "A3": {"width": 297.0, "height": 420.0},
    "A4": {"width": 210.0, "height": 297.0},
    "A5": {"width": 148.0, "height": 210.0},
    "A6": {"width": 105.0, "height": 148.0},
    "B4": {"width": 250.0, "height": 353.0},
    "B5": {"width": 176.0, "height": 250.0},
    "LETTER": {"width": 215.9, "height": 279.4},
    "LEGAL": {"width": 215.9, "height": 355.6},
    "TABLOID": {"width": 279.4, "height": 431.8},
}
PAPER_SIZE_ALIASES = {
    "a0": "A0",
    "a1": "A1",
    "a2": "A2",
    "a3": "A3",
    "a4": "A4",
    "a5": "A5",
    "a6": "A6",
    "b4": "B4",
    "b5": "B5",
    "letter": "LETTER",
    "usletter": "LETTER",
    "legal": "LEGAL",
    "uslegal": "LEGAL",
    "tabloid": "TABLOID",
    "ledger": "TABLOID",
}
IPAddress = Union[ipaddress.IPv4Address, ipaddress.IPv6Address]


def is_disallowed_ip(ip: IPAddress) -> bool:
    return (
        ip.is_private
        or ip.is_loopback
        or ip.is_link_local
        or ip.is_unspecified
        or ip.is_reserved
        or ip.is_multicast
    )


def resolve_hostname_ips(hostname: str) -> Set[IPAddress]:
    resolved_ips: Set[IPAddress] = set()
    try:
        addrinfo = socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        return resolved_ips

    for entry in addrinfo:
        sockaddr = entry[4]
        if not sockaddr:
            continue
        candidate = sockaddr[0]
        try:
            resolved_ips.add(ipaddress.ip_address(candidate))
        except ValueError:
            continue

    return resolved_ips


def validate_https_url(url: str) -> Optional[str]:
    """Allow only HTTPS document URLs and reject local/private targets."""
    parsed = urlparse(url)
    if parsed.scheme.lower() != "https":
        return "Only HTTPS document URLs are allowed."
    if not parsed.netloc:
        return "Document URL must include a hostname."

    hostname = parsed.hostname
    if not hostname:
        return "Document URL must include a valid hostname."

    normalized = hostname.lower()
    if normalized == "localhost" or normalized.endswith(".local"):
        return "Local hostnames are not allowed."

    try:
        ip = ipaddress.ip_address(hostname)
    except ValueError:
        resolved_ips = resolve_hostname_ips(hostname)
        if not resolved_ips:
            return None
        if any(is_disallowed_ip(candidate) for candidate in resolved_ips):
            return "Hostnames that resolve to private or local network IPs are not allowed."
        return None

    if is_disallowed_ip(ip):
        return "Private or local network URLs are not allowed."

    return None


def normalize_paper_size(paper_size: str) -> Optional[str]:
    normalized = "".join(ch for ch in paper_size.strip().lower() if ch.isalnum())
    return PAPER_SIZE_ALIASES.get(normalized)


def build_paper_config(
    paper_size: Optional[str] = None,
    width: Optional[float] = None,
    height: Optional[float] = None,
) -> Dict[str, float]:
    if paper_size:
        canonical_size = normalize_paper_size(paper_size)
        if not canonical_size:
            supported = ", ".join(PAPER_SIZE_DIMENSIONS.keys())
            raise ValueError(f"Unsupported paper size '{paper_size}'. Supported values: {supported}.")
        return dict(PAPER_SIZE_DIMENSIONS[canonical_size])

    if width is None or height is None:
        raise ValueError("Paper config requires either --paper-size or both --width and --height.")
    if width <= 0 or height <= 0:
        raise ValueError("Paper width and height must be positive numbers.")

    return {"width": float(width), "height": float(height)}


class CloudPrintClient:
    """WebPrinter API client."""

    def __init__(self) -> None:
        self.access_token = os.getenv(TOKEN_ENV_VAR, "").strip()
        self.session = requests.Session()
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": f"webprinter-skill/{SKILL_VERSION}",
        }
        if self.access_token:
            self.headers["Authorization"] = f"Bearer {self.access_token}"
        self.session.headers.update(self.headers)

    def _require_token(self) -> Optional[Dict[str, Any]]:
        if self.access_token:
            return None
        return {
            "error": f"Missing access token. Set the {TOKEN_ENV_VAR} environment variable before calling the API."
        }

    def _parse_response(self, response: requests.Response, raw_response: bool) -> Dict[str, Any]:
        if raw_response:
            task_id = response.text.strip()
            if not task_id:
                return {"error": "The API returned an empty task ID."}
            return {"success": True, "taskId": task_id}
        try:
            return response.json()
        except ValueError:
            return {
                "error": "The API returned a non-JSON response.",
                "status_code": response.status_code,
                "response_text": response.text[:500],
            }

    def _send_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        raw_response: bool = False,
    ) -> Dict[str, Any]:
        token_error = self._require_token()
        if token_error:
            return token_error

        url = f"{BASE_URL}{endpoint}"
        payload = data if data is not None else {}

        try:
            if method.upper() == "GET":
                response = self.session.get(url, timeout=DEFAULT_TIMEOUT)
            else:
                response = self.session.post(url, json=payload, timeout=DEFAULT_TIMEOUT)

            response.raise_for_status()
            return self._parse_response(response, raw_response)
        except requests.exceptions.RequestException as exc:
            return {"error": str(exc), "endpoint": endpoint}

    def query_printers(self) -> Dict[str, Any]:
        return self._send_request("POST", "/openapi/control/queryPrinters", {})

    def upload_file(self, file_path: str) -> Dict[str, Any]:
        token_error = self._require_token()
        if token_error:
            return token_error

        path = Path(file_path)
        if not path.exists():
            return {"error": f"File does not exist: {file_path}"}
        if not path.is_file():
            return {"error": f"Path is not a file: {file_path}"}

        try:
            with path.open("rb") as file_obj:
                files = {"file": (path.name, file_obj)}
                headers = {
                    "Accept": "application/json",
                    "Authorization": f"Bearer {self.access_token}",
                    "User-Agent": f"webprinter-skill/{SKILL_VERSION}",
                }
                response = self.session.post(
                    f"{BASE_URL}/openapi/mcpClient/uploadFileMCP",
                    files=files,
                    headers=headers,
                    timeout=60,
                )
                response.raise_for_status()
                return self._parse_response(response, raw_response=False)
        except requests.exceptions.RequestException as exc:
            return {"error": str(exc), "endpoint": "/openapi/mcpClient/uploadFileMCP"}
        except OSError as exc:
            return {"error": str(exc)}

    def query_printer_detail(
        self,
        printer_name: Optional[str] = None,
        share_sn: Optional[str] = None,
        device_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        data: Dict[str, Any] = {}
        if printer_name:
            data["printerName"] = printer_name
        if share_sn:
            data["shareSn"] = share_sn
        if device_type:
            data["deviceType"] = device_type
        return self._send_request("POST", "/openapi/control/queryPrinterDetail", data)

    def create_roaming_task(self, file_name: str, url: str, media_format: str) -> Dict[str, Any]:
        error = validate_https_url(url)
        if error:
            return {"error": error}
        data = {"fileName": file_name, "url": url, "mediaFormat": media_format}
        return self._send_request("POST", "/openapi/task/createRoamingTask", data, raw_response=True)

    def update_printer_side(self, task_id: str, side: str) -> Dict[str, Any]:
        data: Dict[str, Any] = {"taskId": task_id, "side": side}
        return self._send_request("POST", "/openapi/task/config/updatePrinterSideMCP", data)

    def update_printer_color(self, task_id: str, color: str) -> Dict[str, Any]:
        data: Dict[str, Any] = {"taskId": task_id, "color": color}
        return self._send_request("POST", "/openapi/task/config/updatePrinterColorMCP", data)

    def update_printer_copies(self, task_id: str, copies: int) -> Dict[str, Any]:
        data: Dict[str, Any] = {"taskId": task_id, "copies": copies}
        return self._send_request("POST", "/openapi/task/config/updatePrinterCopiesMCP", data)

    def update_printer_paper(self, task_id: str, paper: Dict[str, float]) -> Dict[str, Any]:
        data: Dict[str, Any] = {"taskId": task_id, "paper": paper}
        return self._send_request("POST", "/openapi/task/config/updatePrinterPaperMCP", data)

    def direct_print_document(
        self,
        file_name: str,
        url: str,
        media_format: str,
        device_name: str,
        control_sn: str,
    ) -> Dict[str, Any]:
        error = validate_https_url(url)
        if error:
            return {"error": error}
        data = {
            "fileName": file_name,
            "url": url,
            "mediaFormat": media_format,
            "deviceName": device_name,
            "controlSn": control_sn,
        }
        return self._send_request("POST", "/openapi/task/directPrintDocumentMCP", data)

    def check_install_progress(self) -> Dict[str, Any]:
        return self._send_request("POST", "/openapi/platform/checkInstallProgressMCP", {})


def print_result(result: Dict[str, Any]) -> None:
    print(json.dumps(result, indent=2, ensure_ascii=False))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="WebPrinter cloud print client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  python scripts/mcp_client.py check-install-progress
  python scripts/mcp_client.py query-printers
  python scripts/mcp_client.py upload-file --file-path "C:/path/to/document.pdf"
  python scripts/mcp_client.py create-roaming-task --file-name "document.pdf" --url "https://example.com/document.pdf" --media-format PDF
  python scripts/mcp_client.py update-printer-side --task-id "TASK_20240324_001" --side DUPLEX
  python scripts/mcp_client.py update-printer-color --task-id "TASK_20240324_001" --color COLOR
  python scripts/mcp_client.py update-printer-copies --task-id "TASK_20240324_001" --copies 2
  python scripts/mcp_client.py update-printer-paper --task-id "TASK_20240324_001" --paper-size A4
  python scripts/mcp_client.py update-printer-paper --task-id "TASK_20240324_001" --width 210 --height 297
  python scripts/mcp_client.py print-document --file-name "report.pdf" --url "https://example.com/report.pdf" --media-format PDF --device-name "HP LaserJet Pro" --control-sn "SERVER123456"

Token env var:
  {TOKEN_ENV_VAR}
        """,
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    subparsers.add_parser("check-install-progress", help="Check install and binding progress")
    subparsers.add_parser("query-printers", help="Query available printers")

    upload_parser = subparsers.add_parser("upload-file", help="Upload a local file")
    upload_parser.add_argument("--file-path", required=True, help="Path to a local file")

    detail_parser = subparsers.add_parser("query-printer-detail", help="Query printer capabilities")
    detail_parser.add_argument("--printer-name", help="Printer name")
    detail_parser.add_argument("--share-sn", help="Share or control SN")
    detail_parser.add_argument("--device-type", choices=["printer", "scanner", "camera"], help="Device type")

    roaming_parser = subparsers.add_parser("create-roaming-task", help="Create a roaming print task")
    roaming_parser.add_argument("--file-name", required=True, help="Document file name")
    roaming_parser.add_argument("--url", required=True, help="User-provided HTTPS document URL")
    roaming_parser.add_argument("--media-format", required=True, choices=SUPPORTED_MEDIA_FORMATS, help="Document format")

    side_parser = subparsers.add_parser("update-printer-side", help="Update duplex mode for an existing task")
    side_parser.add_argument("--task-id", required=True, help="Task ID")
    side_parser.add_argument("--side", required=True, choices=["ONESIDE", "DUPLEX", "TUMBLE"], help="Print side mode")

    color_parser = subparsers.add_parser("update-printer-color", help="Update color mode for an existing task")
    color_parser.add_argument("--task-id", required=True, help="Task ID")
    color_parser.add_argument("--color", required=True, choices=SUPPORTED_COLOR_MODES, help="Print color mode")

    copies_parser = subparsers.add_parser("update-printer-copies", help="Update copy count for an existing task")
    copies_parser.add_argument("--task-id", required=True, help="Task ID")
    copies_parser.add_argument(
        "--copies",
        required=True,
        type=int,
        choices=range(MIN_COPIES, MAX_COPIES + 1),
        metavar=f"[{MIN_COPIES}-{MAX_COPIES}]",
        help="Number of copies",
    )

    paper_parser = subparsers.add_parser("update-printer-paper", help="Update paper size for an existing task")
    paper_parser.add_argument("--task-id", required=True, help="Task ID")
    paper_group = paper_parser.add_mutually_exclusive_group(required=True)
    paper_group.add_argument(
        "--paper-size",
        help="Named paper size, such as A3, A4, A5, B4, B5, LETTER, LEGAL, or TABLOID",
    )
    paper_group.add_argument("--width", type=float, help="Paper width in millimeters")
    paper_parser.add_argument("--height", type=float, help="Paper height in millimeters")

    print_parser = subparsers.add_parser("print-document", help="Print directly to a specific printer")
    print_parser.add_argument("--file-name", required=True, help="Document file name")
    print_parser.add_argument("--url", required=True, help="User-provided HTTPS document URL")
    print_parser.add_argument("--media-format", required=True, choices=SUPPORTED_MEDIA_FORMATS, help="Document format")
    print_parser.add_argument("--device-name", required=True, help="Printer name")
    print_parser.add_argument("--control-sn", required=True, help="Control SN")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = CloudPrintClient()

    if args.command == "check-install-progress":
        result = client.check_install_progress()
    elif args.command == "query-printers":
        result = client.query_printers()
    elif args.command == "upload-file":
        result = client.upload_file(args.file_path)
    elif args.command == "query-printer-detail":
        result = client.query_printer_detail(
            printer_name=args.printer_name,
            share_sn=args.share_sn,
            device_type=args.device_type,
        )
    elif args.command == "create-roaming-task":
        result = client.create_roaming_task(
            file_name=args.file_name,
            url=args.url,
            media_format=args.media_format,
        )
    elif args.command == "update-printer-side":
        result = client.update_printer_side(
            task_id=args.task_id,
            side=args.side,
        )
    elif args.command == "update-printer-color":
        result = client.update_printer_color(task_id=args.task_id, color=args.color)
    elif args.command == "update-printer-copies":
        result = client.update_printer_copies(task_id=args.task_id, copies=args.copies)
    elif args.command == "update-printer-paper":
        try:
            paper = build_paper_config(
                paper_size=args.paper_size,
                width=args.width,
                height=args.height,
            )
        except ValueError as exc:
            print_result({"error": str(exc)})
            sys.exit(1)
        result = client.update_printer_paper(task_id=args.task_id, paper=paper)
    else:
        result = client.direct_print_document(
            file_name=args.file_name,
            url=args.url,
            media_format=args.media_format,
            device_name=args.device_name,
            control_sn=args.control_sn,
        )

    print_result(result)
    if "error" in result:
        sys.exit(1)


if __name__ == "__main__":
    main()
