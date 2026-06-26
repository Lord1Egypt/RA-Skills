#!/usr/bin/env python3
"""
客户端核心模块 - 处理 API 请求和响应
"""
import os
import json
import base64
import binascii
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass

import requests

from .constants import (
    REQUEST_TIMEOUT,
    HTTP_OK,
    ERROR_MSG_MAX_LENGTH,
    QUOTA_ERROR_CODE,
)
from .settings import API_URL, PLATFORM, VERSION, SKILL_NAME
from .validators import URLValidator, FileValidator
from .messages import CREDENTIAL_NOT_CONFIGURED, QUOTA_INSUFFICIENT


@dataclass
class OCRResult:
    """图像增强 API 通用响应结构。

    Note: 类名 'OCRResult' 为包内多场景共享的历史命名，
    本类与 OCR/文字识别无关，仅承载图像增强 API 的 code/message/data 三段响应。
    """
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
    """凭证管理器，负责加载和验证 API 密钥

    加载优先级：
      1. 系统环境变量 SCAN_WEBSERVICE_KEY
      2. 用户 HOME 目录下的 ~/.yescan_env 文件（沙箱环境用，KEY=VALUE 文本格式）
    """

    # 沙箱凭证兜底文件：HOME 根目录下的 .yescan_env，与其它 .env-aware 工具隔离
    CONFIG_FILE = Path.home() / ".yescan_env"

    @staticmethod
    def load() -> str:
        api_key = os.getenv("SCAN_WEBSERVICE_KEY", "").strip()
        if api_key:
            return api_key
        api_key = CredentialManager._read_from_file("SCAN_WEBSERVICE_KEY")
        if api_key:
            return api_key
        raise ValueError(CREDENTIAL_NOT_CONFIGURED)

    @staticmethod
    def _read_from_file(key: str) -> str:
        """从 ~/.yescan_env 读取 KEY=VALUE，缺失或异常返回空串"""
        config_file = CredentialManager.CONFIG_FILE
        if not config_file.exists():
            return ""
        try:
            for raw in config_file.read_text(encoding="utf-8").splitlines():
                line = raw.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                if k.strip() == key:
                    return v.strip().strip('"').strip("'")
        except (IOError, OSError):
            pass
        return ""


class QuarkOCRClient:
    """夸克扫描王图像增强 API 客户端。

    Note: 类名中的 'OCR' 为历史命名（包内多场景共享同一底层）。
    本客户端不执行文字识别（OCR），不返回任何识别文本；
    仅传输图片二进制至夸克图像增强 API，返回增强后的图片。
    """

    def __init__(self, api_key: str, scene: str, data_type: str, platform: str = None):
        """
        初始化 客户端

        Args:
            api_key: API 密钥
            scene: 场景名称
            data_type: 数据类型
            platform: 平台标识（可选，覆盖 settings.PLATFORM）
        """
        self.api_key = api_key
        self.scene = scene
        self.data_type = data_type
        self.platform = platform or PLATFORM
        self.session = requests.Session()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def recognize(self, image_url: str = None, image_path: str = None,
                  base64_data: str = None, input_configs: str = None) -> OCRResult:
        """调用夸克图像增强 API 处理图片。

        ⚠️ Privacy Notice：图片二进制会通过 HTTPS 上传至 scan-business.quark.cn；
        调用方需在处理含敏感信息（身份证、合同、医疗记录等）的图片前获得用户授权。

        本方法不执行 OCR/文字识别，仅返回增强后的图片二进制。

        Args:
            image_url: 公网图片 URL
            image_path: 本地图片文件路径（读取后转 BASE64 上传）
            base64_data: BASE64 字符串
            input_configs: 场景额外参数（JSON 字符串，映射至 inputConfigs 字段）

        Returns:
            OCRResult: API 响应结构（code / message / data）
        """
        provided_params = sum(param is not None for param in [image_url, image_path, base64_data])
        if provided_params != 1:
            return OCRResult(
                code="INVALID_INPUT",
                message="Exactly one of image_url, image_path, or base64_data must be provided",
                data=None
            )

        if base64_data:
            return self._recognize_base64(base64_data, input_configs)
        elif image_path:
            return self._recognize_local_file(image_path, input_configs)
        else:
            is_valid, error_msg = URLValidator.validate(image_url)
            if not is_valid:
                return OCRResult(code="URL_VALIDATION_ERROR", message=f"URL validation failed: {error_msg}", data=None)
            param = self._build_request_param(image_url=image_url, input_configs=input_configs)
            response = self._send_request(param)
            return self._parse_response(response)

    def _recognize_base64(self, base64_data: str, input_configs: str = None) -> OCRResult:
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

        param = self._build_request_param(base64_data=base64_content, input_configs=input_configs)
        response = self._send_request(param)
        return self._parse_response(response)

    def _recognize_local_file(self, file_path: str, input_configs: str = None) -> OCRResult:
        """读取本地图片文件，转 BASE64 后上传至夸克图像增强 API。

        ⚠️ Privacy Notice：本方法会读取本地文件原始字节并通过 HTTPS 外发至
        scan-business.quark.cn。调用方在传入路径前应确认用户已知悉
        数据将上传至第三方服务并获得明确授权。
        """
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

        param = self._build_request_param(base64_data=base64_content, input_configs=input_configs)
        response = self._send_request(param)
        return self._parse_response(response)

    def _build_request_param(self, image_url: str = None, base64_data: str = None,
                             input_configs: str = None) -> Dict[str, Any]:
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

        if input_configs:
            param["inputConfigs"] = input_configs

        return param

    def _send_request(self, param: Dict[str, Any]) -> requests.Response:
        """发送 HTTP 请求到夸克图像增强 API。

        ⚠️ 数据外发：本方法将图片二进制（BASE64 或公网 URL）发送到
        scan-business.quark.cn，服务端处理后不会永久保存。
        调用方需确保已获得用户授权。
        """
        headers = {"Content-Type": "application/json", "X-Appbuilder-From": self.platform}
        if VERSION:
            headers["X-Appbuilder-Version"] = VERSION
        if SKILL_NAME:
            headers["X-Appbuilder-Skill"] = SKILL_NAME
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

        if code == QUOTA_ERROR_CODE:
            message = QUOTA_INSUFFICIENT

        return OCRResult(code=code, message=message, data=data)