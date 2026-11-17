"""PaddleOCR 引擎封装 — 中文 OCR 最强方案"""

import os
from typing import Any, Dict, List, Optional

from .base import OCREngine, OCRResult, OCRFrameResult
from ..logger import get_logger

logger = get_logger(__name__)


class PaddleOCREngine(OCREngine):
    """
    PaddleOCR 引擎封装。
    
    特点：
    - 中文识别准确率最高（优于 Tesseract/EasyOCR）
    - 支持中英文混合识别
    - 支持方向检测
    - 支持 GPU 加速
    """
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.ocr_config = config.get("ocr", {})
        self.lang = self.ocr_config.get("lang", "ch")
        self.use_gpu = self.ocr_config.get("use_gpu", False)
        self.use_angle_cls = self.ocr_config.get("use_angle_cls", True)
        self.show_log = self.ocr_config.get("show_log", False)
        self._engine = None
    
    @property
    def name(self) -> str:
        return "paddleocr"
    
    @property
    def supported_languages(self) -> List[str]:
        return ["ch", "en", "japan", "korean", "fr", "german", "ru", "ar"]
    
    def load_model(self) -> bool:
        """
        加载 PaddleOCR 模型。
        
        需要 paddleocr + paddlepaddle：
        pip install paddlepaddle paddleocr
        """
        try:
            logger.info(f"加载 PaddleOCR 模型: lang={self.lang}, gpu={self.use_gpu}")
            
            from paddleocr import PaddleOCR
            
            self._engine = PaddleOCR(
                use_angle_cls=self.use_angle_cls,
                lang=self.lang,
                show_log=self.show_log,
                use_gpu=self.use_gpu,
            )
            
            self._loaded = True
            logger.info("PaddleOCR 模型加载完成")
            return True
            
        except ImportError:
            logger.error(
                "PaddleOCR 需要安装 paddlepaddle 和 paddleocr。\n"
                "  安装命令: pip install paddlepaddle paddleocr"
            )
            return False
        except Exception as e:
            logger.error(f"PaddleOCR 模型加载失败: {e}")
            return False
    
    def recognize(self, image_path: str, **kwargs) -> OCRFrameResult:
        """
        对图像执行 OCR 识别。
        
        Args:
            image_path: 图像文件路径
            **kwargs: 可选参数
            
        Returns:
            OCRFrameResult
        """
        if not os.path.exists(image_path):
            return OCRFrameResult()
        
        self.ensure_loaded()
        
        if not self._loaded:
            return OCRFrameResult()
        
        try:
            result = self._engine.ocr(image_path, cls=self.use_angle_cls)
            
            if not result or not result[0]:
                return OCRFrameResult()
            
            texts = []
            full_texts = []
            
            for line in result[0]:
                if line and len(line) >= 2:
                    bbox = line[0]  # [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
                    text_info = line[1]
                    
                    if isinstance(text_info, tuple) and len(text_info) >= 2:
                        text = text_info[0]
                        confidence = text_info[1]
                    else:
                        text = str(text_info)
                        confidence = 0.0
                    
                    texts.append(OCRResult(
                        bbox=bbox,
                        text=text,
                        confidence=round(float(confidence), 4),
                        lang=self.lang,
                    ))
                    full_texts.append(text)
            
            return OCRFrameResult(
                texts=texts,
                full_text=" ".join(full_texts),
                lang=self.lang,
            )
            
        except Exception as e:
            logger.error(f"PaddleOCR 识别失败: {e}")
            return OCRFrameResult()
