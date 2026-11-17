"""本地 OCR 取字（PaddleOCR）。作为数字来源的基准，确定性强、不幻觉。

注意：重型依赖（paddleocr/cv2/fitz/numpy）均为懒加载，只有在真正执行 OCR 时才导入，
以便非模型模块（validate / ledger_builder）可独立运行与测试，且 VLM 未就绪时不会炸整个包。
"""
import os

_OCR = None


def get_ocr():
    global _OCR
    if _OCR is None:
        from paddleocr import PaddleOCR
        _OCR = PaddleOCR(use_angle_cls=True, lang="ch", show_log=False)
    return _OCR


def _pix_to_bgr(pix):
    import cv2
    import numpy as np
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    if pix.n == 4:
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
    else:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return img


def pdf_to_images(pdf_path, dpi=200):
    import fitz
    doc = fitz.open(pdf_path)
    return [_pix_to_bgr(page.get_pixmap(dpi=dpi)) for page in doc]


def ocr_image(img):
    """img: numpy BGR 数组。返回 [{'text','conf','bbox'}]。"""
    result = get_ocr().ocr(img, cls=True)
    lines = []
    if result and result[0]:
        for bbox, (text, conf) in result[0]:
            lines.append({"text": text, "conf": round(float(conf), 3), "bbox": bbox})
    return lines


def ocr_file(path):
    """统一入口：PDF 渲染每页后 OCR，图片直接 OCR。返回所有文本行。"""
    import cv2
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        lines = []
        for img in pdf_to_images(path):
            lines.extend(ocr_image(img))
        return lines
    img = cv2.imread(path)
    if img is None:
        return []
    return ocr_image(img)
