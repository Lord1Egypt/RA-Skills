#!/usr/bin/env python3
"""
结果处理器模块 - 处理图像增强结果并保存图片
"""
from .constants import SUCCESS_CODE
from .ocr_client import OCRResult
from .file_saver import FileSaver


def save_image_from_result(result: OCRResult) -> OCRResult:
    """从图像增强结果中提取并保存图片"""
    if result.code != SUCCESS_CODE:
        return result

    image_base64 = None
    if isinstance(result.data, dict) and "ImageInfo" in result.data:
        image_info_list = result.data["ImageInfo"]
        if isinstance(image_info_list, list) and len(image_info_list) > 0:
            image_info = image_info_list[0]
            if isinstance(image_info, dict) and "ImageBase64" in image_info:
                image_base64 = image_info["ImageBase64"]

    if image_base64:
        try:
            saver = FileSaver()
            save_res = saver.save_image_from_base64(image_base64)
            if save_res["code"] == 0:
                result.data = {"path": save_res["data"]["path"]}
            else:
                result = OCRResult(code=save_res["code"], message=save_res["msg"], data=save_res["data"])
        except (IOError, OSError) as e:
            result = OCRResult(code="FILE_SAVE_ERROR", message=f"File save failed: {e}", data={})

    return result
