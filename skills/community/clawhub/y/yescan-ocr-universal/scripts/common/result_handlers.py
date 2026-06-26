#!/usr/bin/env python3
"""
结果处理器模块 - 处理 OCR 结果并保存文件
"""
from .ocr_client import OCRResult
from .file_saver import FileSaver


def save_image_from_result(result: OCRResult) -> OCRResult:
    """从 OCR 结果中提取并保存图片"""
    if result.code != "00000":
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


def save_document_from_result(result: OCRResult, config: dict) -> OCRResult:
    """从 OCR 结果中提取并保存文档（Word/Excel/PDF）"""
    if result.code != "00000":
        return result

    # 根据 scene 名称判断保存类型
    scene = config.get("scene", "")
    if scene == "image-to-word":
        doc_type = "word"
    elif scene == "image-to-excel":
        doc_type = "excel"
    elif scene == "image-to-pdf":
        doc_type = "pdf"
    else:
        doc_type = None

    if not doc_type:
        return result

    file_base64 = None
    if isinstance(result.data, dict) and "TypesetInfo" in result.data:
        typeset_info_list = result.data["TypesetInfo"]
        if isinstance(typeset_info_list, list) and len(typeset_info_list) > 0:
            typeset_info = typeset_info_list[0]
            if isinstance(typeset_info, dict) and "FileBase64" in typeset_info:
                file_base64 = typeset_info["FileBase64"]

    if file_base64:
        try:
            saver = FileSaver()
            if doc_type == "word":
                save_res = saver.save_word_from_base64(file_base64)
            elif doc_type == "pdf":
                save_res = saver.save_pdf_from_base64(file_base64)
            else:  # excel
                save_res = saver.save_excel_from_base64(file_base64)

            if save_res["code"] == 0:
                result.data = {"path": save_res["data"]["path"]}
            else:
                result = OCRResult(code=save_res["code"], message=save_res["msg"], data=save_res["data"])
        except (IOError, OSError) as e:
            result = OCRResult(code="FILE_SAVE_ERROR", message=f"File save failed: {e}", data={})

    return result
