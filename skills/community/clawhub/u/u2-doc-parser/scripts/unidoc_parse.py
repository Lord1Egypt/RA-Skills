#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import sys
import uuid
import time
import json
import argparse
import requests
from pathlib import Path
from typing import Optional, Set
import mimetypes

# ------------------------------------------------------
# 作者: 张发
# 修改: ClawHub Skill Adapter
# 文件：unidoc_parse.py
# 创建: 2025/8/18
# 修改: 2025/3/10
# 功能：UniDoc 文档解析工具 - ClawHub Skill 实现
# 版本：1.0.0
# 说明：基于 UniDoc API 实现文档格式转换
# 版权所有：云知声智能科技股份有限公司
# ------------------------------------------------------


# API Endpoints
BASE_URL = os.getenv("UNIDOC_BASE_URL", "https://unidoc.uat.hivoice.cn")
API_KEY = os.getenv("UNIDOC_API_KEY", "")  # Optional API key for future use
SYNC_UPLOAD_URL = f"{BASE_URL}/syncUploadFile"
ASYNC_UPLOAD_URL = f"{BASE_URL}/asyncUploadFile"
EXPORT_URL = f"{BASE_URL}/exportFile"
STATUS_URL = f"{BASE_URL}/getFileStatus"

# Security Configuration
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB
ALLOWED_MIME_TYPES: Set[str] = {
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.ms-powerpoint',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'image/jpeg',
    'image/png',
    'image/gif',
    'image/bmp',
    'image/tiff',
    'text/plain',
    'text/markdown',
}
ALLOWED_EXTENSIONS: Set[str] = {
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
    '.jpg', '.jpeg', '.png', '.txt', '.md'
}


def sanitize_path(file_path: str) -> str:
    """
    清理路径，防止路径遍历攻击
    :param file_path: 文件路径
    :return: 清理后的绝对路径
    """
    # 转换为绝对路径并解析符号链接
    abs_path = os.path.abspath(file_path)
    real_path = os.path.realpath(abs_path)

    # 检查路径是否包含可疑模式
    if '..' in file_path and file_path != '..':
        print(f"[WARN] Path contains '..': {file_path}", file=sys.stderr)

    return real_path


def validate_input_file(file_path: str) -> None:
    """
    验证输入文件的安全性
    :param file_path: 文件路径
    :raises ValueError: 如果文件不安全
    """
    # 清理路径
    safe_path = sanitize_path(file_path)

    # 检查文件是否存在
    if not os.path.exists(safe_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # 检查是否为文件（不是目录或特殊文件）
    if not os.path.isfile(safe_path):
        raise ValueError(f"Path is not a file: {file_path}")

    # 检查文件是否可读
    if not os.access(safe_path, os.R_OK):
        raise PermissionError(f"File is not readable: {file_path}")

    # 检查文件大小
    file_size = os.path.getsize(safe_path)
    if file_size == 0:
        raise ValueError(f"File is empty: {file_path}")
    if file_size > MAX_FILE_SIZE:
        raise ValueError(f"File too large ({file_size / 1024 / 1024:.1f}MB, max {MAX_FILE_SIZE / 1024 / 1024}MB): {file_path}")

    # 检查文件扩展名
    ext = os.path.splitext(safe_path)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"File type not allowed: {ext}. Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}")

    # 检查 MIME 类型（可选，如果 mimetypes 可用）
    mime_type, _ = mimetypes.guess_type(safe_path)
    if mime_type and mime_type not in ALLOWED_MIME_TYPES:
        print(f"[WARN] Unusual MIME type '{mime_type}' for file: {file_path}", file=sys.stderr)


def validate_output_path(output_path: str, force: bool = False) -> None:
    """
    验证输出路径的安全性
    :param output_path: 输出路径
    :param force: 是否强制覆盖（删除已存在的目录/文件）
    :raises ValueError: 如果路径不安全
    """
    if not output_path:
        return

    # 清理路径
    safe_path = sanitize_path(output_path)

    # 检查是否尝试覆盖系统文件
    system_paths = ['/etc/', '/sys/', '/proc/', '/dev/', '/root/']
    for sys_path in system_paths:
        if safe_path.startswith(sys_path):
            raise PermissionError(f"Cannot write to system directory: {output_path}")

    # 如果路径已存在
    if os.path.exists(safe_path):
        if os.path.isfile(safe_path):
            # 是文件，检查是否可写
            if not os.access(safe_path, os.W_OK):
                raise PermissionError(f"File exists but is not writable: {output_path}")
        else:
            # 是目录或其他类型
            path_type = "directory" if os.path.isdir(safe_path) else "non-file path"
            if force:
                print(f"[WARN] Removing existing {path_type}: {safe_path}", file=sys.stderr)
                try:
                    if os.path.isdir(safe_path):
                        import shutil
                        shutil.rmtree(safe_path)
                    else:
                        os.remove(safe_path)
                except OSError as e:
                    raise PermissionError(f"Cannot remove existing {path_type}: {output_path}") from e
            else:
                raise ValueError(
                    f"Path exists but is a {path_type}: {output_path}\n"
                    f"  Use --force to overwrite"
                )

    # 检查父目录是否可写
    parent_dir = os.path.dirname(safe_path)
    if parent_dir and not os.path.exists(parent_dir):
        # 尝试创建目录
        try:
            os.makedirs(parent_dir, exist_ok=True)
        except OSError as e:
            raise PermissionError(f"Cannot create output directory: {parent_dir}") from e
    elif parent_dir and not os.access(parent_dir, os.W_OK):
        raise PermissionError(f"Parent directory is not writable: {parent_dir}")


def check_environment_security(skip_interactive: bool = False) -> None:
    """
    检查环境安全性
    :param skip_interactive: 跳过交互式确认
    :raises RuntimeError: 如果环境不安全
    """
    # 检查 API 端点配置
    if BASE_URL.startswith("http://"):
        print(f"[WARN] Using HTTP (not HTTPS) for API endpoint: {BASE_URL}", file=sys.stderr)
        print("[WARN] This is insecure and not recommended!", file=sys.stderr)
        if not skip_interactive:
            try:
                response = input("Continue anyway? [y/N]: ").strip().lower()
                if response != 'y':
                    raise RuntimeError("Aborted: Unencrypted HTTP connection not allowed")
            except (EOFError, KeyboardInterrupt):
                raise RuntimeError("Aborted: Unencrypted HTTP connection not allowed")

    # 检查是否使用 UAT 环境
    if 'uat' in BASE_URL.lower():
        print(f"[INFO] Using UAT environment: {BASE_URL}", file=sys.stderr)
        print("[INFO] This is a test environment without authentication", file=sys.stderr)
        print("[WARN] Do NOT use with sensitive documents!", file=sys.stderr)


class UniDocParser:
    """UniDoc 文档解析器"""

    def __init__(
        self,
        target_type: str = "md",
        func: str = "unisound",
        uid: Optional[str] = None
    ):
        """
        初始化解析器
        :param target_type: 目标格式 (md/json)
        :param func: 转换方法
        :param uid: 用户ID
        """
        self.target_type = target_type
        self.func = func
        self.uid = uid or uuid.uuid4().hex

    def sync_convert_file(self, file_path: str) -> str:
        """
        同步转换文件
        :param file_path: 文件路径
        :return: 转换后的内容
        """
        # 上传文件
        body = {"uid": self.uid, "func": self.func}
        headers = {}
        if API_KEY:
            headers['Authorization'] = f'Bearer {API_KEY}'

        with open(file_path, 'rb') as file:
            files = {'file': file}
            response = requests.post(
                SYNC_UPLOAD_URL,
                data=body,
                files=files,
                headers=headers,
                timeout=60
            )

        # 检查 HTTP 状态
        if response.status_code != 200:
            raise ValueError(f"HTTP Error {response.status_code}: {response.text}")

        res = response.json()

        # 检查响应
        if "result" not in res or res.get("result") is None:
            raise ValueError(f"API Error: {res.get('message', 'Unknown error')}")

        file_id = res.get("result").get("fileId")

        # 获取转换后的文件内容
        return self._export_file(file_id)

    def async_convert_file(self, file_path: str, poll_interval: int = 1) -> str:
        """
        异步转换文件
        :param file_path: 文件路径
        :param poll_interval: 轮询间隔（秒）
        :return: 转换后的内容
        """
        # 上传文件
        body = {"uid": self.uid, "func": self.func}
        headers = {}
        if API_KEY:
            headers['Authorization'] = f'Bearer {API_KEY}'

        with open(file_path, 'rb') as file:
            files = {'file': file}
            response = requests.post(
                ASYNC_UPLOAD_URL,
                data=body,
                files=files,
                headers=headers,
                timeout=60
            )

        # 检查 HTTP 状态
        if response.status_code != 200:
            raise ValueError(f"HTTP Error {response.status_code}: {response.text}")

        res = response.json()

        # 检查响应
        if "result" not in res or res.get("result") is None:
            raise ValueError(f"API Error: {res.get('message', 'Unknown error')}")

        file_id = res.get("result")

        # 轮询任务状态
        task_status = None
        max_attempts = 300  # 最多轮询5分钟
        attempts = 0

        while task_status not in ["SUCCESS", "FAILED"]:
            if attempts >= max_attempts:
                raise TimeoutError("File conversion timed out after 5 minutes")

            params = {"fileId": file_id}
            response = requests.get(
                url=STATUS_URL,
                params=params,
                headers=headers,
                timeout=30
            )

            if response.status_code != 200:
                raise ValueError(f"HTTP Error {response.status_code} checking status")

            status_res = response.json()
            task_status = status_res.get("result", {}).get("status")

            if task_status not in ["SUCCESS", "FAILED"]:
                time.sleep(poll_interval)
            attempts += 1

        if task_status == "FAILED":
            raise RuntimeError("File conversion failed on server")

        # 获取转换后的文件内容
        return self._export_file(file_id)

    def _export_file(self, file_id: str) -> str:
        """
        导出转换后的文件
        :param file_id: 文件ID
        :return: 文件内容
        """
        headers = {}
        if API_KEY:
            headers['Authorization'] = f'Bearer {API_KEY}'

        params = {"fileId": file_id, "targetType": self.target_type}
        response = requests.get(
            url=EXPORT_URL,
            params=params,
            headers=headers,
            timeout=60
        )

        if response.status_code != 200:
            raise ValueError(f"HTTP Error {response.status_code}: {response.text}")

        export_res = response.json()
        file_url = export_res.get("result")

        if not file_url:
            raise ValueError(f"Export failed: {export_res.get('message', 'Unknown error')}")

        # 验证返回的 URL 是否安全
        if not isinstance(file_url, str) or not file_url.startswith(('http://', 'https://')):
            raise ValueError(f"Invalid file URL returned: {file_url}")

        content = requests.get(file_url, timeout=60).content.decode('utf-8')
        return content


def parse_document(
    file_path: str,
    format_type: str = "md",
    mode: str = "sync",
    func: str = "unisound",
    uid: Optional[str] = None,
    output_path: Optional[str] = None,
    skip_security_check: bool = False,
    force: bool = False
) -> str:
    """
    解析文档
    :param file_path: 文档路径
    :param format_type: 输出格式 (md/json)
    :param mode: 处理模式 (sync/async)
    :param func: 转换方法
    :param uid: 用户ID
    :param output_path: 输出文件路径（可选，不指定则输出到终端）
    :param skip_security_check: 跳过安全检查（不推荐）
    :param force: 强制覆盖已存在的输出路径
    :return: 转换后的内容
    """
    # 安全检查
    check_environment_security(skip_interactive=skip_security_check)

    # 验证输入文件
    validate_input_file(file_path)
    safe_path = sanitize_path(file_path)

    # 验证输出路径
    if output_path:
        validate_output_path(output_path, force=force)
        safe_output_path = sanitize_path(output_path)
    else:
        safe_output_path = None

    # 创建解析器
    parser = UniDocParser(target_type=format_type, func=func, uid=uid)

    # 根据模式选择转换方式
    print(f"[INFO] Parsing: {safe_path} ({mode.upper()} mode, {format_type.upper()} format)", file=sys.stderr)

    if mode == "async":
        content = parser.async_convert_file(safe_path)
    else:
        content = parser.sync_convert_file(safe_path)

    # 如果指定了输出路径，保存到文件
    if safe_output_path:
        # 确保目录存在
        parent_dir = os.path.dirname(safe_output_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)

        with open(safe_output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[INFO] Saved to: {safe_output_path}", file=sys.stderr)

    return content


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="UniDoc Document Parser - Convert documents using UniDoc API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert PDF to Markdown (output to terminal)
  %(prog)s document.pdf

  # Convert DOCX to JSON (async mode)
  %(prog)s document.docx --format json --mode async

  # Save output to file
  %(prog)s document.pdf --output output.md

  # Force overwrite existing output path
  %(prog)s document.pdf --output existing.md --force

Security Notes:
  - Documents are uploaded to an external API service
  - Do NOT use with sensitive or confidential documents
  - Only use with non-sensitive test documents
        """
    )

    parser.add_argument(
        "file",
        help="Path to the document file to parse"
    )

    parser.add_argument(
        "--format",
        choices=["md", "json"],
        default="md",
        help="Output format (default: md)"
    )

    parser.add_argument(
        "--mode",
        choices=["sync", "async"],
        default="sync",
        help="Processing mode: sync or async (default: sync)"
    )

    parser.add_argument(
        "--func",
        default="unisound",
        help="Conversion method/algorithm (default: unisound)"
    )

    parser.add_argument(
        "--output",
        default=None,
        help="Output file path (default: print to terminal)"
    )

    parser.add_argument(
        "--uid",
        default=None,
        help="Custom user ID (auto-generated if not provided)"
    )

    parser.add_argument(
        "--skip-security-check",
        action="store_true",
        help="Skip security warnings (not recommended)"
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Force overwrite if output path already exists (use with caution)"
    )

    args = parser.parse_args()

    # 安全警告（除非明确跳过）
    if not args.skip_security_check:
        print("\n" + "="*60, file=sys.stderr)
        print("⚠️  SECURITY WARNING", file=sys.stderr)
        print("="*60, file=sys.stderr)
        print(f"This tool will upload your file to: {BASE_URL}", file=sys.stderr)
        print("• This is an external API service", file=sys.stderr)
        print("• Do NOT use with sensitive, confidential, or private documents", file=sys.stderr)
        print("• Your files will be processed on third-party servers", file=sys.stderr)
        print("="*60 + "\n", file=sys.stderr)

    try:
        content = parse_document(
            file_path=args.file,
            format_type=args.format,
            mode=args.mode,
            func=args.func,
            uid=args.uid,
            output_path=args.output,
            skip_security_check=args.skip_security_check,
            force=args.force
        )

        # 默认输出到终端（除非指定了 --output）
        if not args.output:
            print(content)

        return 0

    except FileNotFoundError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1
    except PermissionError as e:
        print(f"✗ Permission Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"✗ Validation Error: {e}", file=sys.stderr)
        return 1
    except RuntimeError as e:
        print(f"✗ Runtime Error: {e}", file=sys.stderr)
        return 1
    except TimeoutError as e:
        print(f"✗ Timeout Error: {e}", file=sys.stderr)
        return 1
    except requests.exceptions.RequestException as e:
        print(f"✗ Network Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"✗ Unexpected Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
