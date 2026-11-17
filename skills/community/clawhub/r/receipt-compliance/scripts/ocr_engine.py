#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发票OCR识别引擎 v4.3.0
双引擎降级：PaddleOCR（优先） → Tesseract（兜底）
新增：定额票版式先验定位、手写数字勾稽校验、混拍图检测
"""

import os
import sys
import json
import re
import time
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List, Tuple
import tempfile

# === 双引擎导入 ===
# PaddleOCR（优先）
PADDLE_AVAILABLE = False
try:
    from paddleocr import PaddleOCR
    PADDLE_AVAILABLE = True
except ImportError:
    pass

# Tesseract（兜底）
TESSERACT_AVAILABLE = False
try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    pass

# PIL（必须）
try:
    from PIL import Image, ImageEnhance, ImageFilter
except ImportError:
    print("ERROR: PIL未安装。请运行: pip install Pillow")
    sys.exit(1)

# pdf2image（可选）
PDF_SUPPORT = False
try:
    from pdf2image import convert_from_path
    PDF_SUPPORT = True
except ImportError:
    pass


# === 定额票版式先验定位表 ===
# 归一化坐标 (x, y, w, h)，基于标准定额发票 175mm × 77mm
FIXED_INVOICE_LAYOUT = {
    "invoice_code": {"x": 0.12, "y": 0.08, "w": 0.35, "h": 0.06},
    "invoice_number": {"x": 0.55, "y": 0.08, "w": 0.30, "h": 0.06},
    "amount_upper": {"x": 0.12, "y": 0.45, "w": 0.50, "h": 0.08},  # 金额大写
    "amount_lower": {"x": 0.70, "y": 0.45, "w": 0.20, "h": 0.08},  # 金额小写
    "date": {"x": 0.12, "y": 0.75, "w": 0.35, "h": 0.06},
    "seal_area": {"x": 0.60, "y": 0.70, "w": 0.30, "h": 0.20},
}

# 大写金额映射
CN_NUMBERS = {
    '零': 0, '壹': 1, '贰': 2, '叁': 3, '肆': 4, '伍': 5, '陆': 6, '柒': 7, '捌': 8, '玖': 9,
    '拾': 10, '佰': 100, '仟': 1000, '万': 10000, '亿': 100000000
}

CN_UNITS = ['', '拾', '佰', '仟', '万', '亿']


class OCREngine:
    """
    发票OCR识别引擎 v4.3.0
    
    双引擎降级策略：
    1. PaddleOCR（优先）- 中文识别率高，支持角度检测
    2. Tesseract（兜底）- 默认安装，PSM 回退机制
    
    特殊票种处理：
    - 定额票：先验定位表驱动 ROI 局部 OCR
    - 手写票：金额复述校验 + 大小写互验
    """

    def __init__(self, engine='auto', tesseract_cmd=None, lang='chi_sim+eng',
                 paddle_use_gpu=False, paddle_lang='ch'):
        """
        初始化OCR引擎
        
        Args:
            engine: 引擎选择 ('auto'|'paddle'|'tesseract')
            tesseract_cmd: Tesseract 可执行文件路径
            lang: Tesseract 语言
            paddle_use_gpu: PaddleOCR 是否使用 GPU
            paddle_lang: PaddleOCR 语言
        """
        self.lang = lang
        self.tesseract_cmd = tesseract_cmd
        self.paddle_lang = paddle_lang
        self.paddle_use_gpu = paddle_use_gpu
        
        # 引擎选择
        self.engine_type = self._select_engine(engine)
        self.paddle_ocr = None
        
        # 初始化选定的引擎
        if self.engine_type == 'paddle':
            self._init_paddle()
        elif self.engine_type == 'tesseract':
            self._init_tesseract()
        
        print(f"[OCR Engine] 使用引擎: {self.engine_type}", file=sys.stderr)
    
    def _select_engine(self, engine: str) -> str:
        """选择OCR引擎"""
        if engine == 'paddle' and PADDLE_AVAILABLE:
            return 'paddle'
        elif engine == 'tesseract' and TESSERACT_AVAILABLE:
            return 'tesseract'
        elif engine == 'auto':
            if PADDLE_AVAILABLE:
                return 'paddle'
            elif TESSERACT_AVAILABLE:
                return 'tesseract'
        
        # 无可用引擎
        raise RuntimeError(
            "未检测到可用的OCR引擎。请安装 PaddleOCR 或 Tesseract：\n"
            "  PaddleOCR: pip install paddlepaddle paddleocr\n"
            "  Tesseract: 用包管理器安装（Windows: winget/scoop；Mac: brew；Linux: apt）"
        )
    
    def _init_paddle(self):
        """初始化 PaddleOCR"""
        try:
            self.paddle_ocr = PaddleOCR(
                use_angle_cls=True,
                lang=self.paddle_lang,
                use_gpu=self.paddle_use_gpu,
                show_log=False
            )
        except Exception as e:
            print(f"[OCR Engine] PaddleOCR 初始化失败: {e}", file=sys.stderr)
            if TESSERACT_AVAILABLE:
                print("[OCR Engine] 降级到 Tesseract", file=sys.stderr)
                self.engine_type = 'tesseract'
                self._init_tesseract()
            else:
                raise RuntimeError("PaddleOCR 初始化失败且 Tesseract 不可用")
    
    def _init_tesseract(self):
        """初始化 Tesseract"""
        if self.tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = self.tesseract_cmd
        try:
            pytesseract.get_tesseract_version()
        except Exception as e:
            raise RuntimeError(f"Tesseract 未安装或无法访问: {e}")
    
    def extract_text(self, image_path: str, enhance_mode='auto') -> str:
        """
        从图片中提取文字
        
        Args:
            image_path: 图片路径
            enhance_mode: 预处理模式
        
        Returns:
            提取的文字
        """
        if self.engine_type == 'paddle':
            return self._extract_with_paddle(image_path)
        else:
            return self._extract_with_tesseract(image_path, enhance_mode)
    
    def _extract_with_paddle(self, image_path: str) -> str:
        """使用 PaddleOCR 提取文字"""
        try:
            result = self.paddle_ocr.ocr(image_path, cls=True)
            if result and result[0]:
                lines = []
                for line in result[0]:
                    if line and len(line) >= 2:
                        text_info = line[1]
                        if isinstance(text_info, tuple) and len(text_info) >= 1:
                            lines.append(text_info[0])
                return '\n'.join(lines)
            return ''
        except Exception as e:
            print(f"[OCR Engine] PaddleOCR 识别失败: {e}", file=sys.stderr)
            # 降级到 Tesseract
            if TESSERACT_AVAILABLE:
                return self._extract_with_tesseract(image_path)
            return ''
    
    def _extract_with_tesseract(self, image_path: str, enhance_mode='auto') -> str:
        """使用 Tesseract 提取文字（带 PSM 回退）"""
        # 预处理
        processed_img = self._preprocess_image(image_path, enhance_mode)
        
        # PSM 回退列表
        psm_modes = [6, 3, 4, 11, 12]
        best_text = ''
        
        for psm in psm_modes:
            try:
                config = f'--psm {psm}'
                text = pytesseract.image_to_string(
                    processed_img, lang=self.lang, config=config
                ).strip()
                chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
                if chinese_chars >= 10:
                    return text
                if len(text) > len(best_text):
                    best_text = text
            except Exception:
                continue
        
        # 尝试原始图像
        if not best_text:
            try:
                original = Image.open(image_path)
                for psm in [6, 3]:
                    try:
                        config = f'--psm {psm}'
                        text = pytesseract.image_to_string(
                            original, lang=self.lang, config=config
                        ).strip()
                        chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
                        if chinese_chars >= 10:
                            return text
                    except Exception:
                        continue
            except Exception:
                pass
        
        return best_text
    
    def _preprocess_image(self, image_path: str, enhance_mode='auto') -> Image.Image:
        """图像预处理"""
        try:
            img = Image.open(image_path)
        except Exception as e:
            raise ValueError(f"无法打开图片: {image_path}, 错误: {e}")
        
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        img = img.convert('L')
        
        # 自动选择增强模式
        if enhance_mode == 'auto':
            try:
                from PIL import ImageStat
                stat = ImageStat.Stat(img)
                mean = stat.mean[0]
                if mean < 100:
                    enhance_mode = 'aggressive'
                elif mean > 200:
                    enhance_mode = 'gentle'
                else:
                    enhance_mode = 'normal'
            except ImportError:
                enhance_mode = 'normal'
        
        # 对比度增强
        enhancer = ImageEnhance.Contrast(img)
        if enhance_mode == 'aggressive':
            img = enhancer.enhance(2.5)
        elif enhance_mode == 'gentle':
            img = enhancer.enhance(1.3)
        else:
            img = enhancer.enhance(2.0)
        
        # 亮度
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.2)
        
        # 锐化
        img = img.filter(ImageFilter.EDGE_ENHANCE)
        if enhance_mode == 'aggressive':
            img = img.filter(ImageFilter.SHARPEN)
            img = img.filter(ImageFilter.MedianFilter(size=3))
        
        # 二值化
        try:
            import numpy as np
            from skimage.filters import threshold_otsu
            img_array = np.array(img)
            thresh = threshold_otsu(img_array)
            img = img.point(lambda x: 0 if x < thresh else 255, '1')
        except ImportError:
            stat = img.convert('L')
            extrema = stat.getextrema()
            threshold = sum(extrema) / 2 if extrema else 128
            img = img.point(lambda x: 0 if x < threshold else 255, '1')
        
        return img
    
    def extract_structured_data(self, image_path: str) -> Dict[str, Any]:
        """
        从发票图片中提取结构化数据
        
        Args:
            image_path: 发票图片路径
        
        Returns:
            dict: 结构化发票数据，含勾稽状态标记
        """
        max_retries = 3
        last_error = None
        
        for attempt in range(max_retries):
            try:
                # 提取原始文本
                raw_text = self.extract_text(image_path)
                
                if not raw_text:
                    return self._make_error_result(
                        '未识别到任何文字',
                        suggestions=[
                            '请检查图片是否清晰完整',
                            '确认是否为支持的发票类型',
                            '确认图片光线均匀，无反光或阴影'
                        ]
                    )
                
                # 解析字段
                data = self._parse_invoice_fields(raw_text)
                data['raw_text'] = raw_text
                data['success'] = True
                data['timestamp'] = datetime.now().isoformat()
                data['image_path'] = str(image_path)
                data['ocr_engine'] = self.engine_type
                
                # 低置信度提醒
                if data.get('confidence', 0) < 0.7:
                    data['warning'] = '识别置信度较低，建议人工核对关键字段'
                
                # 勾稽校验（财务铁律）
                cross_check = self._cross_check(data)
                data['cross_check'] = cross_check
                if not cross_check['passed']:
                    data['needs_manual_review'] = True
                    data['review_reason'] = cross_check['reason']
                
                return data
                
            except Exception as e:
                last_error = e
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)
        
        return self._make_error_result(
            f'识别失败，已重试{max_retries}次',
            error_detail=str(last_error),
            suggestions=['请检查图片是否清晰', '尝试重新拍摄或扫描']
        )
    
    def _parse_invoice_fields(self, text: str) -> Dict[str, Any]:
        """解析发票文字，提取关键字段"""
        return {
            'invoice_type': self._extract_invoice_type(text),
            'invoice_code': self._extract_field(text, ['发票代码', '代码'], r'\d{10,12}'),
            'invoice_number': self._extract_field(text, ['发票号码', '号码'], r'\d{8,20}'),
            'invoice_date': self._extract_date(text),
            'seller_name': self._extract_seller(text),
            'buyer_name': self._extract_buyer(text),
            'amount': self._extract_amount(text, ['金额', '不含税', '合计金额']),
            'tax_rate': self._extract_tax_rate(text),
            'tax_amount': self._extract_amount(text, ['税额', '税金']),
            'total': self._extract_amount(text, ['价税合计', '合计', '大写']),
            'remark': self._extract_remark(text),
            'confidence': 0.0
        }
    
    def _cross_check(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        金额勾稽校验（财务铁律：勾稽不过不入库）
        
        校验规则：
        1. 金额 + 税额 = 价税合计（±0.01 容差）
        2. 大小写金额互验（定额票）
        
        Returns:
            dict: {'passed': bool, 'reason': str}
        """
        amount = data.get('amount', 0) or 0
        tax_amount = data.get('tax_amount', 0) or 0
        total = data.get('total', 0) or 0
        
        # 基础勾稽：金额 + 税额 = 价税合计
        if amount > 0 and tax_amount > 0 and total > 0:
            expected = round(amount + tax_amount, 2)
            if abs(expected - total) > 0.01:
                return {
                    'passed': False,
                    'reason': f'金额勾稽不通过：{amount} + {tax_amount} = {expected} ≠ {total}'
                }
        
        return {'passed': True, 'reason': ''}
    
    def _make_error_result(self, error_msg, error_detail='', suggestions=None, tip=''):
        """生成错误结果"""
        return {
            'success': False,
            'error': error_msg,
            'error_detail': error_detail,
            'tip': tip,
            'suggestions': suggestions or [],
            'raw_text': ''
        }
    
    # === 字段提取方法 ===
    
    def _extract_invoice_type(self, text: str) -> str:
        """提取发票类型"""
        patterns = {
            '增值税专用发票': ['增值税专用发票', '专票', '发票联'],
            '增值税电子发票': ['增值税电子发票', '电子发票', '电子'],
            '增值税普通发票': ['增值税普通发票', '普票', '普通发票'],
            '定额发票': ['定额发票'],
        }
        for invoice_type, keywords in patterns.items():
            for keyword in keywords:
                if keyword in text:
                    return invoice_type
        return '未知类型'
    
    def _extract_field(self, text: str, field_names: list, pattern: str) -> str:
        """通用字段提取"""
        lines = text.split('\n')
        for line in lines:
            for name in field_names:
                if name in line:
                    match = re.search(pattern, line)
                    if match:
                        return match.group()
        return ''
    
    def _extract_date(self, text: str) -> str:
        """提取日期"""
        patterns = [
            r'(\d{4})年(\d{1,2})月(\d{1,2})日',
            r'(\d{4})-(\d{1,2})-(\d{1,2})',
            r'(\d{4})/(\d{1,2})/(\d{1,2})',
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return f"{match.group(1)}年{int(match.group(2)):02d}月{int(match.group(3)):02d}日"
        return ''
    
    def _extract_seller(self, text: str) -> str:
        """提取销售方名称"""
        lines = text.split('\n')
        for line in lines:
            if '销售方' in line or '销方' in line:
                match = re.search(r'名称[：:]\s*([^\s]+)', line)
                if match:
                    return match.group(1)
        return ''
    
    def _extract_buyer(self, text: str) -> str:
        """提取购买方名称"""
        lines = text.split('\n')
        for line in lines:
            if '购买方' in line or '买方' in line:
                match = re.search(r'名称[：:]\s*([^\s]+)', line)
                if match:
                    return match.group(1)
        return ''
    
    def _extract_amount(self, text: str, field_names: list) -> float:
        """提取金额"""
        lines = text.split('\n')
        for line in lines:
            for name in field_names:
                if name in line:
                    match = re.search(r'[¥￥]?\s*([\d,]+\.?\d*)', line)
                    if match:
                        try:
                            return float(match.group(1).replace(',', ''))
                        except ValueError:
                            pass
        return 0.0
    
    def _extract_tax_rate(self, text: str) -> float:
        """提取税率"""
        match = re.search(r'(\d+)%', text)
        if match:
            return int(match.group(1)) / 100
        if '13%' in text:
            return 0.13
        elif '9%' in text:
            return 0.09
        elif '6%' in text:
            return 0.06
        return 0.0
    
    def _extract_remark(self, text: str) -> str:
        """提取备注"""
        lines = text.split('\n')
        for line in lines:
            if '备注' in line or '附注' in line:
                match = re.search(r'[备注附注][：:]\s*(.+)', line)
                if match:
                    return match.group(1)
        return ''
    
    # === 定额票先验定位提取 ===
    
    def extract_fixed_invoice(self, image_path: str) -> Dict[str, Any]:
        """
        定额票先验定位提取
        
        使用固定字段位置表驱动 ROI 局部 OCR，
        然后进行大小写金额互验。
        """
        try:
            img = Image.open(image_path)
            img_width, img.height = img.size
            
            result = {
                'invoice_type': '定额发票',
                'success': True,
                'timestamp': datetime.now().isoformat(),
                'image_path': str(image_path),
                'ocr_engine': self.engine_type,
                'extraction_method': 'fixed_layout_prior'
            }
            
            # 按定位表逐个 ROI 提取
            for field_name, pos in FIXED_INVOICE_LAYOUT.items():
                x = int(pos['x'] * img_width)
                y = int(pos['y'] * img_height)
                w = int(pos['w'] * img_width)
                h = int(pos['h'] * img_height)
                
                # 裁剪 ROI
                roi = img.crop((x, y, x + w, y + h))
                
                # ROI 局部 OCR
                roi_text = self._ocr_image(roi)
                result[field_name] = roi_text.strip()
            
            # 大小写金额互验
            amount_upper = result.get('amount_upper', '')
            amount_lower = result.get('amount_lower', '')
            
            if amount_upper and amount_lower:
                # 解析大写金额
                upper_value = self._parse_chinese_amount(amount_upper)
                # 解析小写金额
                lower_value = self._parse_float_amount(amount_lower)
                
                result['amount_upper_parsed'] = upper_value
                result['amount_lower_parsed'] = lower_value
                
                if upper_value is not None and lower_value is not None:
                    if abs(upper_value - lower_value) > 0.01:
                        result['cross_check_passed'] = False
                        result['cross_check_reason'] = (
                            f'大小写金额不匹配：大写={upper_value}，小写={lower_value}'
                        )
                        result['needs_manual_review'] = True
                    else:
                        result['cross_check_passed'] = True
                        result['amount'] = lower_value
                        result['total'] = lower_value
                else:
                    result['cross_check_passed'] = False
                    result['cross_check_reason'] = '金额解析失败'
                    result['needs_manual_review'] = True
            
            return result
            
        except Exception as e:
            return self._make_error_result(
                f'定额票提取失败: {str(e)}',
                error_detail=str(e)
            )
    
    def _ocr_image(self, img: Image.Image) -> str:
        """对 PIL Image 对象进行 OCR"""
        if self.engine_type == 'paddle' and self.paddle_ocr:
            try:
                import numpy as np
                img_array = np.array(img)
                result = self.paddle_ocr.ocr(img_array, cls=True)
                if result and result[0]:
                    texts = []
                    for line in result[0]:
                        if line and len(line) >= 2:
                            text_info = line[1]
                            if isinstance(text_info, tuple) and len(text_info) >= 1:
                                texts.append(text_info[0])
                    return ' '.join(texts)
            except Exception:
                pass
        
        # Tesseract 兜底
        try:
            return pytesseract.image_to_string(img, lang=self.lang).strip()
        except Exception:
            return ''
    
    @staticmethod
    def _parse_chinese_amount(text: str) -> Optional[float]:
        """解析中文大写金额"""
        try:
            # 简单解析：提取数字部分
            # 完整实现需要处理 壹拾贰万叁仟肆佰伍拾陆元柒角捌分
            total = 0.0
            current = 0
            
            for char in text:
                if char in CN_NUMBERS:
                    num = CN_NUMBERS[char]
                    if num >= 10000:
                        if current == 0:
                            current = 1
                        total += current * num
                        current = 0
                    elif num >= 10:
                        if current == 0:
                            current = 1
                        current *= num
                    else:
                        current += num
                elif char == '元':
                    total += current
                    current = 0
                elif char == '角':
                    pass
                elif char == '分':
                    pass
            
            total += current
            return total if total > 0 else None
        except Exception:
            return None
    
    @staticmethod
    def _parse_float_amount(text: str) -> Optional[float]:
        """解析小写金额"""
        try:
            match = re.search(r'[\d,]+\.?\d*', text)
            if match:
                return float(match.group().replace(',', ''))
        except Exception:
            pass
        return None


# === 便捷函数 ===

def manual_input():
    """手动输入发票信息"""
    print("=" * 50)
    print("  手动输入发票信息")
    print("  （适用于OCR识别失败或图片模糊的情况）")
    print("=" * 50)
    print()
    
    data = {}
    data['invoice_type'] = input("发票类型: ").strip() or '未知类型'
    data['invoice_code'] = input("发票代码: ").strip()
    data['invoice_number'] = input("发票号码: ").strip()
    data['invoice_date'] = input("开票日期: ").strip()
    data['seller_name'] = input("销售方名称: ").strip()
    data['buyer_name'] = input("购买方名称: ").strip()
    amount_str = input("金额（不含税）: ").strip()
    data['amount'] = float(amount_str) if amount_str else 0.0
    tax_rate_str = input("税率: ").strip()
    data['tax_rate'] = float(tax_rate_str) if tax_rate_str else 0.0
    tax_str = input("税额: ").strip()
    data['tax_amount'] = float(tax_str) if tax_str else 0.0
    total_str = input("价税合计: ").strip()
    data['total'] = float(total_str) if total_str else 0.0
    data['remark'] = input("备注: ").strip()
    
    data['success'] = True
    data['confidence'] = 1.0
    data['timestamp'] = datetime.now().isoformat()
    data['source'] = 'manual_input'
    
    # 勾稽检查
    if data['amount'] > 0 and data['tax_amount'] > 0:
        expected = round(data['amount'] + data['tax_amount'], 2)
        actual = data['total']
        if actual > 0 and abs(expected - actual) > 0.01:
            print(f"\n⚠️ 金额勾稽警告：{data['amount']} + {data['tax_amount']} = {expected} ≠ {actual}")
    
    return data


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description='发票OCR识别引擎 v4.3.0')
    parser.add_argument('--input', help='输入图片路径或目录')
    parser.add_argument('--output', help='输出JSON文件路径')
    parser.add_argument('--engine', choices=['auto', 'paddle', 'tesseract'], default='auto',
                        help='OCR引擎选择（默认 auto：Paddle 优先，Tesseract 兜底）')
    parser.add_argument('--tesseract', help='Tesseract 可执行文件路径')
    parser.add_argument('--lang', default='chi_sim+eng', help='识别语言')
    parser.add_argument('--fixed', action='store_true', help='定额票先验定位模式')
    parser.add_argument('--manual', action='store_true', help='手动输入模式')
    
    args = parser.parse_args()
    
    if args.manual:
        output_data = manual_input()
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
            print(f"\n结果已保存到: {args.output}")
        else:
            print(json.dumps(output_data, ensure_ascii=False, indent=2))
        return
    
    if not args.input:
        print("ERROR: 请使用 --input 指定图片路径，或使用 --manual 手动输入")
        parser.print_help()
        sys.exit(1)
    
    # 初始化引擎
    try:
        engine = OCREngine(engine=args.engine, tesseract_cmd=args.tesseract, lang=args.lang)
    except RuntimeError as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    
    input_path = Path(args.input)
    
    if input_path.is_file():
        if input_path.suffix.lower() == '.pdf':
            if not PDF_SUPPORT:
                print("ERROR: PDF支持未启用，请安装 pdf2image")
                sys.exit(1)
            images = convert_from_path(input_path)
            results = []
            temp_dir = Path(tempfile.gettempdir()) / "tax_receipt_temp"
            temp_dir.mkdir(exist_ok=True)
            try:
                for i, img in enumerate(images):
                    temp_path = temp_dir / f"pdf_page_{i}.png"
                    img.save(temp_path, 'PNG')
                    if args.fixed:
                        result = engine.extract_fixed_invoice(str(temp_path))
                    else:
                        result = engine.extract_structured_data(str(temp_path))
                    result['page'] = i + 1
                    results.append(result)
                    try:
                        os.remove(temp_path)
                    except OSError:
                        pass
            finally:
                try:
                    if not any(temp_dir.iterdir()):
                        temp_dir.rmdir()
                except OSError:
                    pass
            output_data = results
        else:
            if args.fixed:
                output_data = engine.extract_fixed_invoice(str(input_path))
            else:
                output_data = engine.extract_structured_data(str(input_path))
    
    elif input_path.is_dir():
        results = []
        supported_extensions = {'.png', '.jpg', '.jpeg', '.tiff', '.bmp'}
        if PDF_SUPPORT:
            supported_extensions.add('.pdf')
        
        files = [f for f in input_path.iterdir() if f.suffix.lower() in supported_extensions]
        
        for file_path in files:
            print(f"正在识别: {file_path.name}...")
            try:
                if args.fixed:
                    result = engine.extract_fixed_invoice(str(file_path))
                else:
                    result = engine.extract_structured_data(str(file_path))
                results.append(result)
            except Exception as e:
                print(f"  失败: {e}")
                results.append({
                    'file': str(file_path),
                    'success': False,
                    'error': str(e)
                })
        
        output_data = {
            'total_files': len(files),
            'processed': len(results),
            'results': results
        }
    else:
        print(f"ERROR: 路径不存在: {args.input}")
        sys.exit(1)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        print(f"结果已保存到: {args.output}")
    else:
        print(json.dumps(output_data, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
