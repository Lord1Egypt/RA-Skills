#!/usr/bin/env python3
"""
Common - 夸克扫描王公共模块
提供 OCR 客户端、文件保存、验证器等公共功能
"""
from .constants import (
    API_URL,
    ALLOWED_IMAGE_EXTENSIONS,
    MAX_FILE_SIZE,
    REQUEST_TIMEOUT,
    HTTP_OK,
    ERROR_MSG_MAX_LENGTH,
    SUCCESS_CODE,
    ERR_MSG_A0211_QUOTA_INSUFFICIENT,
)
from .validators import URLValidator, FileValidator
from .ocr_client import OCRResult, CredentialManager, QuarkOCRClient
from .file_saver import FileSaver, SaveResult, ResponseCode, FileExtension, SubDirectory
from .scene_configs import SCENE_CONFIGS, get_scene_config, list_scenes
from .runner import run_ocr
from .result_handlers import save_image_from_result, save_document_from_result

__all__ = [
    # 常量
    "API_URL",
    "ALLOWED_IMAGE_EXTENSIONS",
    "MAX_FILE_SIZE",
    "REQUEST_TIMEOUT",
    "HTTP_OK",
    "ERROR_MSG_MAX_LENGTH",
    "SUCCESS_CODE",
    "ERR_MSG_A0211_QUOTA_INSUFFICIENT",
    # 验证器
    "URLValidator",
    "FileValidator",
    # OCR 客户端
    "OCRResult",
    "CredentialManager",
    "QuarkOCRClient",
    # 文件保存
    "FileSaver",
    "SaveResult",
    "ResponseCode",
    "FileExtension",
    "SubDirectory",
    # 场景配置
    "SCENE_CONFIGS",
    "get_scene_config",
    "list_scenes",
    # 执行器
    "run_ocr",
    # 结果处理器
    "save_image_from_result",
    "save_document_from_result",
]
