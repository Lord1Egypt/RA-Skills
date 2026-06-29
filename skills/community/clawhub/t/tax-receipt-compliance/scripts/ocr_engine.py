#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发票OCR识别引擎 - 基于Tesseract的本地化处理方案
企业自主配置，数据本地处理，不依赖第三方API
"""

import os
import sys
import json
import re
import time
import argparse
from pathlib import Path
from datetime import datetime
import tempfile

# 尝试导入PIL
try:
    from PIL import Image, ImageEnhance, ImageFilter
except ImportError:
    print("ERROR: PIL未安装。请运行: pip install Pillow")
    sys.exit(1)

# 尝试导入pytesseract
try:
    import pytesseract
except ImportError:
    print("ERROR: pytesseract未安装。请运行: pip install pytesseract")
    sys.exit(1)

# 尝试导入pdf2image（PDF支持）
try:
    from pdf2image import convert_from_path
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False


class OCREngine:
    """发票OCR识别引擎"""

    def __init__(self, tesseract_cmd=None, lang='chi_sim+eng'):
        """
        初始化OCR引擎

        Args:
            tesseract_cmd: Tesseract可执行文件路径（可选，默认系统PATH）
            lang: 识别语言（默认中文简体+英文）
        """
        self.lang = lang
        self.tesseract_cmd = tesseract_cmd

        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

        # 验证Tesseract是否可用
        self._verify_tesseract()

    def _verify_tesseract(self):
        """验证Tesseract OCR是否已安装"""
        try:
            pytesseract.get_tesseract_version()
        except Exception as e:
            raise RuntimeError(
                f"Tesseract OCR未安装或无法访问: {e}\n"
                "请运行安装脚本 install_tesseract.sh 或 install_tesseract.ps1\n"
                "或手动安装: https://github.com/UB-Mannheim/tesseract/wiki"
            )

    def preprocess_image(self, image_path):
        """
        图像预处理：灰度化 → 去噪 → 二值化 → 纠偏

        Args:
            image_path: 图片文件路径

        Returns:
            预处理后的PIL Image对象
        """
        try:
            img = Image.open(image_path)
        except Exception as e:
            raise ValueError(f"无法打开图片文件: {image_path}, 错误: {e}")

        # 转换为灰度图
        if img.mode != 'L':
            img = img.convert('L')

        # 对比度增强（自适应：根据图片亮度调整增强系数）
        enhancer = ImageEnhance.Contrast(img)
        # 计算平均亮度，暗图片增强更多
        stat = img.convert('L')
        extrema = stat.getextrema()
        avg_brightness = sum(extrema) / 2 if extrema else 128
        # 暗图片(亮度<100)增强更多，亮图片(亮度>180)增强较少
        if avg_brightness < 100:
            enhance_factor = 2.5
        elif avg_brightness > 180:
            enhance_factor = 1.5
        else:
            enhance_factor = 2.0
        img = enhancer.enhance(enhance_factor)

        # 锐化
        img = img.filter(ImageFilter.SHARPEN)

        # 二值化（自适应阈值）
        # 使用简单的全局阈值，生产环境可考虑自适应阈值
        threshold = 128
        img = img.point(lambda x: 0 if x < threshold else 255, '1')

        return img

    def extract_text(self, image_path):
        """
        从图片中提取文字（支持PSM回退机制）

        Args:
            image_path: 图片文件路径

        Returns:
            识别到的文字内容
        """
        # 预处理
        processed_img = self.preprocess_image(image_path)

        # PSM模式回退列表：6(统一文本块) → 3(自动分页) → 4(单列可变) → 11(稀疏文本) → 12(稀疏文本+OSD)
        psm_modes = [6, 3, 4, 11, 12]
        best_text = ''
        best_psm = None

        for psm in psm_modes:
            try:
                config = f'--psm {psm}'
                text = pytesseract.image_to_string(
                    processed_img,
                    lang=self.lang,
                    config=config
                ).strip()
                # 如果识别到中文字符数>10，认为结果可用
                chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
                if chinese_chars >= 10:
                    return text
                # 记录最佳结果（字符数最多）
                if len(text) > len(best_text):
                    best_text = text
                    best_psm = psm
            except Exception:
                continue

        # 如果所有PSM都未识别到足够中文，返回最佳结果
        if best_text:
            return best_text

        # 尝试原始图像（未预处理）- 某些情况下预处理反而降低质量
        try:
            original_img = Image.open(image_path)
            for psm in [6, 3]:
                try:
                    config = f'--psm {psm}'
                    text = pytesseract.image_to_string(
                        original_img,
                        lang=self.lang,
                        config=config
                    ).strip()
                    chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
                    if chinese_chars >= 10:
                        return text
                except Exception:
                    continue
        except Exception:
            pass

        return best_text

    def extract_structured_data(self, image_path):
        """
        从发票图片中提取结构化数据（带重试机制）

        Args:
            image_path: 发票图片路径

        Returns:
            dict: 结构化发票数据
        """
        max_retries = 3
        last_error = None

        for attempt in range(max_retries):
            try:
                # 提取原始文本
                raw_text = self.extract_text(image_path)

                if not raw_text:
                    # 提供更详细的错误诊断
                    error_msg = '未识别到任何文字。'
                    tip = ''
                    suggestions = []
                    try:
                        img = Image.open(image_path)
                        w, h = img.size
                        # 图片尺寸检查
                        if w < 200 or h < 200:
                            tip = '图片尺寸过小，建议分辨率≥800x600。'
                            suggestions.append('请使用更高分辨率的图片（建议800x600以上）')
                        # 图片模式检查
                        if img.mode == 'RGBA':
                            tip += ' 图片带透明背景，建议转换为JPG格式。'
                            suggestions.append('图片带有透明背景，请转换为JPG或PNG格式')
                        elif img.mode == 'RGB':
                            # 检查是否偏色或过暗
                            extrema = img.getextrema()
                            if extrema:
                                avg_brightness = sum(sum(c) / len(c) for c in extrema) / len(extrema)
                                if avg_brightness < 80:
                                    tip += ' 图片过亮或过暗。'
                                    suggestions.append('图片亮度不均衡，建议在光线均匀的环境下拍摄')
                        # 检查Tesseract语言包
                        try:
                            langs = pytesseract.get_languages()
                            if 'chi_sim' not in langs:
                                suggestions.append('未检测到中文语言包，请重新安装Tesseract并勾选中文语言包')
                        except Exception:
                            pass
                    except Exception as e:
                        suggestions.append(f'图片文件可能损坏或格式不支持: {e}')

                    if not suggestions:
                        suggestions = [
                            '请检查图片是否清晰完整',
                            '确认是否为支持的发票类型（增值税专票/普票/电子票）',
                            '确认图片光线均匀，无反光或阴影',
                            '尝试重新拍摄或扫描发票'
                        ]

                    return {
                        'success': False,
                        'error': error_msg,
                        'tip': tip,
                        'suggestions': suggestions,
                        'raw_text': ''
                    }

                # 解析发票字段
                structured_data = self._parse_invoice_fields(raw_text)
                structured_data['raw_text'] = raw_text
                structured_data['success'] = True
                structured_data['timestamp'] = datetime.now().isoformat()
                structured_data['image_path'] = str(image_path)

                # 低置信度提醒（阈值0.7）
                if structured_data.get('confidence', 0) < 0.7:
                    structured_data['warning'] = '识别置信度较低，建议人工核对关键字段（发票代码、号码、金额）'

                return structured_data

            except Exception as e:
                last_error = e
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # 指数退避：1秒、2秒、4秒
                    print(f"识别失败，正在重试 ({attempt+1}/{max_retries})，等待{wait_time}秒...")
                    time.sleep(wait_time)

        # 最终失败，返回友好提示
        return {
            'success': False,
            'error': f'识别失败，已重试{max_retries}次',
            'error_detail': str(last_error),
            'suggestions': [
                '请检查图片是否清晰',
                '尝试重新拍摄或扫描',
                '确认是否为支持的发票类型（增值税专票/普票/电子票）',
                '检查Tesseract中文语言包是否安装完整'
            ],
            'tip': '如持续失败，建议手动输入发票信息'
        }

    def _parse_invoice_fields(self, text):
        """
        解析发票文字，提取关键字段

        Args:
            text: OCR识别到的原始文字

        Returns:
            dict: 解析后的字段
        """
        data = {
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
            'remark': self._extract_remark(text)
        }

        # 估算置信度（简化版）
        data['confidence'] = self._calculate_confidence(data)

        return data

    def _extract_invoice_type(self, text):
        """提取发票类型"""
        patterns = {
            '增值税专用发票': ['增值税专用发票', '专票', '发票联'],
            '增值税电子发票': ['增值税电子发票', '电子发票', '电子'],
            '增值税普通发票': ['增值税普通发票', '普票', '普通发票'],
        }

        for invoice_type, keywords in patterns.items():
            for keyword in keywords:
                if keyword in text:
                    return invoice_type
        return '未知类型'

    def _extract_field(self, text, field_names, pattern):
        """通用字段提取"""
        lines = text.split('\n')
        for line in lines:
            for name in field_names:
                if name in line:
                    # 尝试在行中查找匹配模式
                    match = re.search(pattern, line)
                    if match:
                        return match.group()
        return ''

    def _extract_date(self, text):
        """提取日期"""
        # 匹配格式：2026年06月28日 或 2026-06-28 或 2026/06/28
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

    def _extract_seller(self, text):
        """提取销售方名称"""
        lines = text.split('\n')
        for line in lines:
            if '销售方' in line or '销方' in line:
                # 提取公司名称（通常在"名称："之后）
                match = re.search(r'名称[：:]\s*([^\s]+)', line)
                if match:
                    return match.group(1)
        return ''

    def _extract_buyer(self, text):
        """提取购买方名称"""
        lines = text.split('\n')
        for line in lines:
            if '购买方' in line or '买方' in line:
                match = re.search(r'名称[：:]\s*([^\s]+)', line)
                if match:
                    return match.group(1)
        return ''

    def _extract_amount(self, text, field_names):
        """提取金额"""
        lines = text.split('\n')
        for line in lines:
            for name in field_names:
                if name in line:
                    # 匹配金额格式：¥10000.00 或 10000.00 或 10,000.00
                    match = re.search(r'[¥￥]?\s*([\d,]+\.?\d*)', line)
                    if match:
                        amount = match.group(1).replace(',', '')
                        try:
                            return float(amount)
                        except ValueError:
                            pass
        return 0.0

    def _extract_tax_rate(self, text):
        """提取税率"""
        match = re.search(r'(\d+)%', text)
        if match:
            return int(match.group(1)) / 100
        # 常见税率
        if '13%' in text:
            return 0.13
        elif '9%' in text:
            return 0.09
        elif '6%' in text:
            return 0.06
        return 0.0

    def _extract_remark(self, text):
        """提取备注或附注"""
        lines = text.split('\n')
        for line in lines:
            if '备注' in line or '附注' in line:
                match = re.search(r'[备注附注][：:]\s*(.+)', line)
                if match:
                    return match.group(1)
        return ''

    def _calculate_confidence(self, data):
        """计算识别置信度（简化版）"""
        # 排除 confidence 本身和 raw_text、image_path 等非字段信息
        exclude_keys = {'confidence', 'raw_text', 'image_path', 'success', 'timestamp'}
        field_data = {k: v for k, v in data.items() if k not in exclude_keys}
        filled_fields = sum(1 for v in field_data.values() if v and v != 0.0)
        total_fields = len(field_data)
        return round(filled_fields / total_fields, 2) if total_fields > 0 else 0.0


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description='发票OCR识别引擎')
    parser.add_argument('--input', required=True, help='输入图片路径或目录')
    parser.add_argument('--output', help='输出JSON文件路径（可选）')
    parser.add_argument('--tesseract', help='Tesseract可执行文件路径')
    parser.add_argument('--lang', default='chi_sim+eng', help='识别语言')

    args = parser.parse_args()

    # 初始化OCR引擎
    try:
        engine = OCREngine(tesseract_cmd=args.tesseract, lang=args.lang)
    except RuntimeError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    # 处理单个文件或目录
    input_path = Path(args.input)

    if input_path.is_file():
        # 单文件模式
        if input_path.suffix.lower() == '.pdf':
            if not PDF_SUPPORT:
                print("ERROR: PDF支持未启用，请安装pdf2image: pip install pdf2image")
                sys.exit(1)
            # PDF处理
            images = convert_from_path(input_path)
            results = []
            temp_dir = Path(tempfile.gettempdir()) / "tax_receipt_temp"
            temp_dir.mkdir(exist_ok=True)
            try:
                for i, img in enumerate(images):
                    temp_path = temp_dir / f"pdf_page_{i}.png"
                    img.save(temp_path, 'PNG')
                    result = engine.extract_structured_data(temp_path)
                    result['page'] = i + 1
                    results.append(result)
                    try:
                        os.remove(temp_path)
                    except OSError:
                        pass  # 清理失败不影响主流程
            finally:
                # 清理临时目录
                try:
                    if not any(temp_dir.iterdir()):
                        temp_dir.rmdir()
                except OSError:
                    pass
            output_data = results
        else:
            output_data = engine.extract_structured_data(input_path)

    elif input_path.is_dir():
        # 目录模式
        results = []
        supported_extensions = {'.png', '.jpg', '.jpeg', '.tiff', '.bmp'}
        if PDF_SUPPORT:
            supported_extensions.add('.pdf')

        for file_path in input_path.iterdir():
            if file_path.suffix.lower() in supported_extensions:
                print(f"正在识别: {file_path.name}...")
                try:
                    result = engine.extract_structured_data(file_path)
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

    # 输出结果
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        print(f"结果已保存到: {args.output}")
    else:
        print(json.dumps(output_data, ensure_ascii=False, indent=2))

    # 识别完成后给出友好提示
    if isinstance(output_data, dict) and output_data.get('success'):
        confidence = output_data.get('confidence', 0)
        if confidence >= 0.8:
            print("\n✅ 识别效果良好，置信度较高，可直接使用。", file=sys.stderr)
        elif confidence >= 0.6:
            print("\n⚠️ 识别置信度一般，建议核对关键字段（发票代码、号码、金额）。", file=sys.stderr)
        else:
            print("\n❌ 识别置信度较低，建议重新拍摄或手动输入发票信息。", file=sys.stderr)
    elif isinstance(output_data, dict) and not output_data.get('success'):
        print(f"\n❌ 识别失败: {output_data.get('error', '未知错误')}", file=sys.stderr)
        if output_data.get('tip'):
            print(f"💡 提示: {output_data['tip']}", file=sys.stderr)
        if output_data.get('suggestions'):
            print("📋 建议操作:", file=sys.stderr)
            for i, s in enumerate(output_data['suggestions'], 1):
                print(f"   {i}. {s}", file=sys.stderr)


if __name__ == '__main__':
    main()
