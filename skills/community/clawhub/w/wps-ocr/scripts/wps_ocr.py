#!/usr/bin/env python3
import argparse
import base64
import json
import os
import re
import sys
import socket
import ipaddress
from typing import Tuple, Dict, Any, Optional
from dataclasses import dataclass
from urllib.parse import urlparse
from pathlib import Path

import requests
from requests.exceptions import Timeout, ConnectionError

# --- Configuration constants ---
API_URL = "https://aiwrite.wps.cn/pdf/parse/web/claw-skill"
ALLOWED_TARGET_HOST = "aiwrite.wps.cn"

# URL safety configuration
MAX_URL_LENGTH = 2048
ALLOWED_PROTOCOLS = {"http", "https"}
SUPPORTED_IMAGE_EXT = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}  # Supported image extensions
SUPPORTED_PDF_EXT = {'.pdf'}  # Supported PDF extension
MAX_FILE_SIZE = 10 * 1024 * 1024  # Maximum file size: 10MB

# Dangerous domain keywords
DANGEROUS_KEYWORDS = ["localhost", "internal", "intranet", "admin", "test"]

@dataclass
class OCRResult:
    """OCR result"""
    code: int
    message: Optional[str]
    md_text: str

    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps({
            "code": self.code,
            "message": self.message,
            "markdown_text": self.md_text
        }, ensure_ascii=False, indent=2)


class URLValidator:
    """URL safety validator"""

    @staticmethod
    def validate(url: str) -> Tuple[bool, Optional[str]]:
        """
        Validate the safety of the URL
        Returns: (is_valid, error_message)
        """
        if not url or not isinstance(url, str):
            return False, "URL cannot be empty"

        url = url.strip()

        if len(url) > MAX_URL_LENGTH:
            return False, f"URL exceeds maximum length of {MAX_URL_LENGTH} characters"

        try:
            parsed = urlparse(url)
        except Exception as e:
            return False, f"Invalid URL format: {str(e)}"

        if parsed.scheme.lower() not in ALLOWED_PROTOCOLS:
            return False, f"Protocol '{parsed.scheme}' not allowed."

        hostname = parsed.hostname
        if not hostname:
            return False, "URL must contain a valid hostname"

        # 1. Basic keyword filtering
        hostname_lower = hostname.lower()
        for keyword in DANGEROUS_KEYWORDS:
            if keyword in hostname_lower:
                return False, f"Hostname contains restricted keyword: {keyword}"

        # 2. [Enhanced] Security check after DNS resolution (prevents DNS Rebinding / SSRF)
        # Even if the hostname appears to be a public domain, verify its resolved IP
        is_safe, err_msg = URLValidator._validate_dns_resolution(hostname)
        if not is_safe:
            return False, err_msg

        return True, None

    @staticmethod
    def _validate_dns_resolution(hostname: str) -> Tuple[bool, str]:
        """
        [Security Critical] Resolve domain and verify all associated IPs are public IPs.
        Prevents DNS Rebinding attacks.
        """
        try:
            # Get all resolution records (IPv4 & IPv6)
            addr_info = socket.getaddrinfo(hostname, None, socket.AF_UNSPEC, socket.SOCK_STREAM)

            for family, sock_type, proto, canon_name, sockaddr in addr_info:
                ip = sockaddr[0]
                try:
                    ip_obj = ipaddress.ip_address(ip)
                    # Reject private, loopback, link-local, multicast addresses
                    if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local or ip_obj.is_multicast:
                        return False, f"Security Block: {hostname} resolves to private/internal IP {ip}"
                except ValueError:
                    continue
            return True, "OK"
        except socket.gaierror:
            # If resolution fails, allow it (will be handled by requests later) or block
            # For strict security, consider blocking unresolvable domains
            return True, "OK"

    @staticmethod
    def _is_ip_address(hostname: str) -> bool:
        ipv4_pattern = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
        return bool(re.match(ipv4_pattern, hostname))

    @staticmethod
    def _is_private_ip(ip: str) -> bool:
        # This function is kept as a backup; main logic is in _validate_dns_resolution
        private_patterns = [
            r"^127\.", r"^10\.", r"^172\.(1[6-9]|2[0-9]|3[0-1])\.",
            r"^192\.168\.", r"^169\.254\.", r"^0\.", r"^224\.", r"^240\."
        ]
        return any(re.match(p, ip) for p in private_patterns)

class FileValidatorAndReader:
    """File validation and reading utility: validate extension, file size, read PDF/image file content"""

    def __init__(self, max_file_size: int = MAX_FILE_SIZE):
        self.max_file_size = max_file_size
        self.supported_ext = SUPPORTED_IMAGE_EXT.union(SUPPORTED_PDF_EXT)

    @staticmethod
    def _validate_file_exists(file_path: str) -> None:
        """Validate if file exists"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"file not exist: {file_path}")
        if not os.path.isfile(file_path):
            raise IsADirectoryError(f"the path is not a file: {file_path}")

    def _validate_file_ext(self, file_path: str) -> None:
        """Validate if file extension is supported"""
        file_ext = Path(file_path).suffix.lower()  # Convert to lower case to avoid case issues (e.g., .PNG/.png)
        if file_ext not in self.supported_ext:
            raise ValueError(
                f"file type not supported: {file_ext}, support file type：{', '.join(self.supported_ext)}"
            )

    def _validate_file_size(self, file_path: str) -> None:
        """Validate if file size exceeds limit"""
        file_size = os.path.getsize(file_path)
        if file_size > self.max_file_size:
            raise OverflowError(
                f"file size limited：{file_size/1024/1024:.2f}MB（max support file size is {self.max_file_size/1024/1024}MB）"
            )

    @staticmethod
    def get_file_type(file_path: str) -> Tuple[str, str]:
        """Get file type (image/pdf)"""
        file_ext = Path(file_path).suffix.lower()
        if file_ext in SUPPORTED_IMAGE_EXT:
            return "image", file_ext
        elif file_ext in SUPPORTED_PDF_EXT:
            return "pdf", file_ext
        else:
            raise ValueError(f"unknown file type：{file_ext}")

    def read_file(self, file_path: str) -> str:
        """
        Read file content, perform full validation first, then read
        :param file_path: path to the file
        :return: file content as base64-encoded string (str)
        """
        # 1. Perform all validations
        self._validate_file_exists(file_path)
        self._validate_file_ext(file_path)
        self._validate_file_size(file_path)

        # 2. Read file content
        try:
            file_type, file_ext = self.get_file_type(file_path)
            with open(file_path, mode='rb', encoding=None) as f:
                content = f.read()
                base64_str = base64.b64encode(content).decode('utf-8')
                base64_str = f"data:{file_type}/{file_ext.lstrip('.')};base64,{base64_str}"
                return base64_str
        except Exception as e:
            raise IOError(f"read file failed：{str(e)}") from e


class CredentialManager:
    @staticmethod
    def load() -> str:
        c_sec = os.getenv("WPS_OCR_ACCESS_KEY", "").strip()
        if c_sec:
            return c_sec
        raise ValueError("Credentials missing: WPS_OCR_ACCESS_KEY required")


class WPSOCRClient:
    def __init__(self, client_secret: str):
        self.client_secret = client_secret
        self.session = requests.Session()

        # Explicitly verify that the hardcoded API URL matches the expected domain
        parsed_api = urlparse(API_URL)
        if parsed_api.hostname != ALLOWED_TARGET_HOST and not parsed_api.hostname.endswith("." + ALLOWED_TARGET_HOST):
            raise RuntimeError(
                f"Security Configuration Error: API_URL hostname '{parsed_api.hostname}' is not allowed.")

    def recognize_url(self, image_url: str) -> OCRResult:
        is_valid, error_msg = URLValidator.validate(image_url)
        if not is_valid:
            return OCRResult(code=400, message=f"URL validation failed: {error_msg}", md_text="")

        param = self._build_request_param(url=image_url, file_data='')
        response = self._send_request(param)
        return self._parse_response(response)

    def recognize_file(self, file_path: str) -> OCRResult:
        file_tool = FileValidatorAndReader()
        try:
            file_content = file_tool.read_file(file_path)
            param = self._build_request_param(url='', file_data=file_content)
            response = self._send_request(param)
            return self._parse_response(response)
        except Exception as e:
            return OCRResult(code=400, message=f"URL validation failed: {e}", md_text="")

    @staticmethod
    def _build_request_param(url: str, file_data: str) -> Dict[str, Any]:
        if url and url != '':
            return {"url": url}
        return {"url": file_data}

    def _send_request(self, param: Dict[str, Any]) -> requests.Response:
        headers = {"Content-Type": "application/json", "Authorization": self.client_secret}
        # 1. Use hardcoded API_URL (already confirmed as whitelisted domain)
        # 2. allow_redirects=False prevents 302 redirects to internal networks
        # 3. timeout prevents DoS
        response = self.session.post(
            API_URL,
            json=param,
            headers=headers,
            timeout=60,
            allow_redirects=False  # Critical: disable redirects
        )
        return response

    @staticmethod
    def _parse_response(response: requests.Response) -> OCRResult:
        if response.status_code >= 500:
            error_msg = response.text[:200] if response.text else "No error message"
            return OCRResult(response.status_code, message=f"HTTP {response.status_code}: {error_msg}", md_text="")
        try:
            body = response.json()
        except json.JSONDecodeError as e:
            return OCRResult(code=500, message=f"Failed to parse JSON: {str(e)}", md_text="")
        if response.status_code != 200:
            detail = body.get("detail")
            return OCRResult(code=response.status_code, message=detail, md_text="")
        md_text = body.get("markdown_text")
        return OCRResult(code=0, message="ok", md_text=md_text)


def main():
    parser = argparse.ArgumentParser(description="WPS OCR - Secure JSON Output")
    parser.add_argument("--url", "-u", required=False, help="File URL")
    parser.add_argument("--path", "-p", required=False, help="Local File Path")
    args = parser.parse_args()

    try:
        client_secret = CredentialManager.load()
        client = WPSOCRClient(client_secret)
        if args.url :
            result = client.recognize_url(args.url)
            print(result.to_json())
        elif args.path :
            result = client.recognize_file(args.path)
            print(result.to_json())
        else :
            print(OCRResult(code=400, message="url or path required", md_text="").to_json())
    except ValueError as e:
        print(OCRResult(code=400, message=str(e), md_text="").to_json())
        sys.exit(1)
    except Timeout:
        print(OCRResult(code=408, message="Request timed out", md_text="").to_json())
        sys.exit(1)
    except ConnectionError as e:
        print(OCRResult(code=504, message=f"Network failed: {str(e)}", md_text="").to_json())
        sys.exit(1)
    except Exception as e:
        print(OCRResult(code=500, message=f"Unexpected error: {str(e)}", md_text="").to_json())
        sys.exit(1)


if __name__ == "__main__":
    main()
