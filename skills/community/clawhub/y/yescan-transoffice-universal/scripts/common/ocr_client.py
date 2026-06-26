#!/usr/bin/env python3
"""
OCR 客户端核心模块 - 处理 API 请求和响应
"""
import os
import json
import base64
import binascii
from typing import Dict, Any, Optional
from dataclasses import dataclass

import requests

from .constants import (
    API_URL,
    REQUEST_TIMEOUT,
    HTTP_OK,
    ERROR_MSG_MAX_LENGTH,
    ERR_MSG_A0211_QUOTA_INSUFFICIENT,
)
from .validators import URLValidator, FileValidator


@dataclass
class OCRResult:
    """OCR 识别结果 - 直接返回 API 原始响应"""
    code: str
    message: Optional[str]
    data: Optional[Dict[str, Any]]

    def to_json(self) -> str:
        """返回完整的 API 响应结构"""
        return json.dumps({
            "code": self.code,
            "message": self.message,
            "data": self.data
        }, ensure_ascii=False, indent=2)


class CredentialManager:
    """凭证管理器，负责加载和验证 API 密钥"""

    @staticmethod
    def load() -> str:
        """从环境变量加载 API 密钥"""
        api_key = os.getenv("SCAN_WEBSERVICE_KEY", "").strip()
        if api_key:
            return api_key
        raise ValueError(
            "SCAN_WEBSERVICE_KEY 未配置，请访问 https://scan.quark.cn/business → 开发者后台 → 登录/注册账号 → 查看API Key"
        )


class QuarkOCRClient:
    """夸克 OCR 客户端，提供图片识别功能"""

    def __init__(self, api_key: str, scene: str, data_type: str):
        """
        初始化 OCR 客户端

        Args:
            api_key: API 密钥
            scene: 场景名称（如 general-ocr, idcard-ocr 等）
            data_type: 数据类型（image 或 pdf）
        """
        self.api_key = api_key
        self.scene = scene
        self.data_type = data_type
        self.session = requests.Session()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def recognize(self, image_url: str = None, image_path: str = None, base64_data: str = None) -> OCRResult:
        """
        识别图片内容

        Args:
            image_url: 公网图片 URL
            image_path: 本地文件路径（自动转 BASE64）
            base64_data: base64 字符串

        Returns:
            OCRResult: 识别结果
        """
        provided_params = sum(param is not None for param in [image_url, image_path, base64_data])
        if provided_params != 1:
            return OCRResult(
                code="INVALID_INPUT",
                message="Exactly one of image_url, image_path, or base64_data must be provided",
                data=None
            )

        if base64_data:
            return self._recognize_base64(base64_data)
        elif image_path:
            return self._recognize_local_file(image_path)
        else:
            is_valid, error_msg = URLValidator.validate(image_url)
            if not is_valid:
                return OCRResult(code="URL_VALIDATION_ERROR", message=f"URL validation failed: {error_msg}", data=None)
            param = self._build_request_param(image_url=image_url)
            response = self._send_request(param)
            return self._parse_response(response)

    def _recognize_base64(self, base64_data: str) -> OCRResult:
        """处理 base64 字符串，支持两种格式"""
        base64_content = base64_data.strip()

        if base64_content.startswith('data:'):
            try:
                if ';base64,' in base64_content:
                    base64_content = base64_content.split(';base64,', 1)[1]
                else:
                    return OCRResult(
                        code="BASE64_FORMAT_ERROR",
                        message="Invalid Data URL format, expected format: data:image/jpeg;base64,<base64_string>",
                        data=None
                    )
            except (ValueError, IndexError) as e:
                return OCRResult(
                    code="BASE64_PARSE_ERROR",
                    message=f"Failed to parse Data URL: {str(e)}",
                    data=None
                )

        try:
            base64.b64decode(base64_content)
        except (ValueError, binascii.Error) as e:
            return OCRResult(code="BASE64_DECODE_ERROR", message=f"Invalid base64 string: {str(e)}", data=None)

        param = self._build_request_param(base64_data=base64_content)
        response = self._send_request(param)
        return self._parse_response(response)

    def _recognize_local_file(self, file_path: str) -> OCRResult:
        """处理本地文件：读取文件并转为 BASE64 后调用 OCR"""
        file_path = os.path.expanduser(file_path.strip())

        is_valid, error_msg = FileValidator.validate(file_path)
        if not is_valid:
            return OCRResult(code="FILE_ERROR", message=f"File validation failed: {error_msg}", data=None)

        try:
            with open(file_path, 'rb') as f:
                file_content = f.read()
            base64_content = base64.b64encode(file_content).decode('utf-8')
        except (IOError, OSError) as e:
            return OCRResult(code="FILE_READ_ERROR", message=f"Failed to read file: {str(e)}", data=None)

        param = self._build_request_param(base64_data=base64_content)
        response = self._send_request(param)
        return self._parse_response(response)

    def _build_request_param(self, image_url: str = None, base64_data: str = None) -> Dict[str, Any]:
        """构建请求参数"""
        param = {
            "aiApiKey": self.api_key,
            "dataType": self.data_type,
            "scene": self.scene
        }

        if base64_data:
            param["dataBase64"] = base64_data
        else:
            param["dataUrl"] = image_url

        return param

    def _send_request(self, param: Dict[str, Any]) -> requests.Response:
        """发送 HTTP 请求到 OCR API"""
        headers = {"Content-Type": "application/json", "X-Appbuilder-From": "openclaw"}
        response = self.session.post(
            API_URL,
            json=param,
            headers=headers,
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True
        )
        return response

    def _parse_response(self, response: requests.Response) -> OCRResult:
        """解析 API 响应，直接返回原始响应"""
        if response.status_code != HTTP_OK:
            error_msg = response.text[:ERROR_MSG_MAX_LENGTH] if response.text else "No error message"
            return OCRResult(
                code="HTTP_ERROR",
                message=f"HTTP {response.status_code}: {error_msg}",
                data=None
            )
        try:
            body = response.json()
        except json.JSONDecodeError as e:
            return OCRResult(
                code="JSON_PARSE_ERROR",
                message=f"Failed to parse JSON: {str(e)}",
                data=None
            )

        code = body.get("code", "unknown")
        message = body.get("message")
        data = body.get("data")

        if code == "A0211":
            message = ERR_MSG_A0211_QUOTA_INSUFFICIENT

        return OCRResult(code=code, message=message, data=data)
