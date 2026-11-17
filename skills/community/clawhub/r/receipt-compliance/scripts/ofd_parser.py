#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OFD 版式文件解析器
针对中国自主 OFD 格式的发票文档解析
优先使用 ofdparser 库，不可用时提供降级方案
"""

import os
import sys
import json
import struct
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime


class OFDParser:
    """
    OFD 文件解析器
    
    OFD（Open Fixed-layout Document）是中国自主的版式文档格式，
    全电发票的版式文件采用 OFD 格式。本解析器提供两种方案：
    1. 使用 Python ofdparser 库（优先，支持文字提取）
    2. 降级方案：仅支持 OFD 文件结构查看，需配合 PDF 转换使用
    """
    
    def __init__(self, ofd_path: str):
        self.ofd_path = Path(ofd_path)
        self.has_library = False
        self._check_library()
    
    def _check_library(self):
        """检查 ofdparser 库是否可用"""
        try:
            import ofdparser
            self.has_library = True
            self.ofdparser = ofdparser
        except ImportError:
            self.has_library = False
    
    def parse(self) -> Dict[str, Any]:
        """
        解析 OFD 文件
        
        Returns:
            dict: 包含 pages_text、structure、info 等字段
        """
        if not self.ofd_path.exists():
            raise FileNotFoundError(f"OFD文件不存在: {self.ofd_path}")
        
        if self.has_library:
            return self._parse_with_library()
        else:
            return self._parse_fallback()
    
    def _parse_with_library(self) -> Dict[str, Any]:
        """使用 ofdparser 库解析"""
        try:
            ofd = self.ofdparser.OFD(self.ofd_path)
            
            result = {
                'success': True,
                'method': 'ofdparser',
                'page_count': len(ofd.pages) if hasattr(ofd, 'pages') else 0,
                'pages_text': [],
                'structure': {},
                'extractable': True,
            }
            
            # 提取每页文字
            if hasattr(ofd, 'pages'):
                for i, page in enumerate(ofd.pages):
                    page_text = ''
                    if hasattr(page, 'text'):
                        page_text = page.text
                    elif hasattr(page, 'get_text'):
                        page_text = page.get_text()
                    
                    if page_text:
                        result['pages_text'].append({
                            'page': i + 1,
                            'text': page_text
                        })
            
            return result
            
        except Exception as e:
            # 如果库解析失败，降级到自研方案
            return self._parse_fallback(str(e))
    
    def _parse_fallback(self, library_error: Optional[str] = None) -> Dict[str, Any]:
        """
        降级解析方案
        手动解析 OFD 文件结构（OFD 本质是 ZIP 格式的 XML 包）
        """
        result = {
            'success': True,
            'method': 'self_developed',
            'extractable': False,
            'pages_text': [],
            'structure': {},
            'note': '文字提取能力有限。如需完整文字识别，请安装 ofdparser 库',
            'install_hint': 'pip install ofdparser',
        }
        
        if library_error:
            result['library_error'] = library_error
        
        try:
            # OFD 本质是 ZIP 格式
            with zipfile.ZipFile(str(self.ofd_path), 'r') as zf:
                file_list = zf.namelist()
                result['structure']['files'] = file_list
                result['structure']['file_count'] = len(file_list)
                
                # 尝试读取主文档（通常根目录下）
                xml_contents = []
                for name in file_list:
                    if name.endswith('.xml') or name.endswith('.ofd'):
                        try:
                            with zf.open(name) as f:
                                content = f.read().decode('utf-8', errors='ignore')
                                xml_contents.append({
                                    'file': name,
                                    'content_preview': content[:500]  # 前500字符预览
                                })
                        except Exception:
                            pass
                
                result['structure']['xml_contents'] = xml_contents
                
                # 尝试用 OCR 方式提取（如果有图像层）
                images = [n for n in file_list if any(
                    ext in n.lower() for ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
                )]
                result['structure']['embedded_images'] = images
                
        except zipfile.BadZipFile:
            raise ValueError(f"文件不是有效的 OFD 格式: {self.ofd_path}")
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def extract_text(self) -> str:
        """提取所有文字内容（降级时返回空字符串）"""
        result = self.parse()
        
        if result.get('extractable'):
            texts = []
            for page in result.get('pages_text', []):
                texts.append(page.get('text', ''))
            return '\n'.join(texts)
        
        return ''
    
    def get_structure(self) -> Dict[str, Any]:
        """获取 OFD 文件结构"""
        result = self.parse()
        return result.get('structure', {})

    def to_invoice(self) -> Dict[str, Any]:
        """
        数电票 OFD 版式直读（v4.5.0）
        文字层可取时转 UnifiedInvoice；不可取时返回结构化降级信息。

        Returns:
            dict: {supported, data, validation_errors, message, ...}
        """
        result = self.parse()

        if not result.get('extractable'):
            return {
                "type": "full_electronic_ofd",
                "receipt_type": "vat_invoice",
                "supported": False,
                "data": result,
                "message": "OFD 文字层不可用，请安装 ofdparser 或转为 PDF 后直读",
                "alternatives": result.get('install_hint', ''),
            }

        try:
            from digital_invoice_reader import DigitalInvoiceTextParser
            text = self.extract_text()
            inv = DigitalInvoiceTextParser().parse(text)
            inv.source_format = "ofd"
            return {
                "type": "full_electronic_ofd",
                "receipt_type": "vat_invoice",
                "supported": True,
                "data": inv.to_dict(),
                "validation_errors": inv.validate(),
                "message": "数电票 OFD 直读完成",
            }
        except Exception as e:
            return {
                "type": "full_electronic_ofd",
                "receipt_type": "vat_invoice",
                "supported": False,
                "data": result,
                "message": f"OFD 转结构化失败: {e}",
                "alternatives": result.get('install_hint', ''),
            }


class PDFallbackExtractor:
    """
    降级方案：将 OFD 转为 PDF 后使用 OCR 提取
    需系统安装 OFD 阅读器（如数科阅读器、福昕 OFD）
    
    注意：此为辅助方案，要求用户手动安装 OFD 转 PDF 工具
    """
    
    CONVERSION_TOOLS = [
        {
            'name': '数科 OFD 阅读器',
            'url': 'https://www.sureway.com.cn/',
            'note': '免费 OFD 阅读软件，支持打印为 PDF',
        },
        {
            'name': '福昕 OFD 阅读器',
            'url': 'https://www.foxitsoftware.cn/ofd/',
            'note': '支持 OFD 转 PDF',
        },
        {
            'name': 'OFD 在线转换',
            'url': 'https://appzyler.com/ofd-to-pdf',
            'note': '在线转换（注意数据隐私风险）',
        },
    ]
    
    @classmethod
    def get_alternatives(cls) -> List[Dict[str, str]]:
        """获取可用的替代转换方案"""
        return cls.CONVERSION_TOOLS


def parse_ofd_invoice(ofd_path: str) -> Dict[str, Any]:
    """
    便捷函数：解析 OFD 发票文件
    
    Args:
        ofd_path: OFD 文件路径
    
    Returns:
        dict: 解析结果
    """
    parser = OFDParser(ofd_path)
    return parser.parse()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python ofd_parser.py <path_to_ofd>")
        sys.exit(1)
    
    ofd_path = sys.argv[1]
    try:
        result = parse_ofd_invoice(ofd_path)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"解析失败: {e}", file=sys.stderr)
        sys.exit(1)
