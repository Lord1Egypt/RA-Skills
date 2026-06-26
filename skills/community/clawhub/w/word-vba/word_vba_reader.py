#!/usr/bin/env python3
"""
Word文档读取模块 - 基于VBA/ActiveX
支持读取doc和docx格式，包括文本和段落格式信息

作者: SuperMike
日期: 2026-03-04
"""

import win32com.client
import pythoncom
from pathlib import Path
from typing import Dict, List, Optional, Any
import json


class WordReader:
    """Word文档读取器 - 使用COM接口调用Word VBA"""
    
    def __init__(self, visible: bool = False):
        """
        初始化Word读取器
        
        Args:
            visible: 是否显示Word窗口，默认False（后台运行）
        """
        self.word_app = None
        self.visible = visible
        self.document = None
        
    def _init_word(self) -> bool:
        """初始化Word应用"""
        try:
            pythoncom.CoInitialize()
            self.word_app = win32com.client.Dispatch("Word.Application")
            self.word_app.Visible = self.visible
            self.word_app.DisplayAlerts = 0  # 不显示警告
            print("✓ Word应用启动成功")
            return True
        except Exception as e:
            print(f"✗ Word应用启动失败: {e}")
            return False
    
    def _close_word(self):
        """关闭Word应用"""
        try:
            if self.document:
                self.document.Close(SaveChanges=False)
                self.document = None
            if self.word_app:
                self.word_app.Quit()
                self.word_app = None
            pythoncom.CoUninitialize()
            print("✓ Word应用已关闭")
        except Exception as e:
            print(f"! 关闭Word时出错: {e}")
    
    def read_document(self, file_path: str) -> Dict[str, Any]:
        """
        读取Word文档内容和格式
        
        Args:
            file_path: Word文档路径（支持.doc和.docx）
            
        Returns:
            包含文档信息的字典
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        if not self._init_word():
            raise RuntimeError("无法初始化Word应用")
        
        try:
            print(f"正在打开文档: {file_path}")
            self.document = self.word_app.Documents.Open(str(file_path.absolute()))
            
            result = {
                'file_path': str(file_path),
                'file_name': file_path.name,
                'paragraph_count': self.document.Paragraphs.Count,
                'word_count': self.document.ComputeStatistics(0),  # wdStatisticWords
                'pages': self.document.ComputeStatistics(2),  # wdStatisticPages
                'paragraphs': [],
                'tables': []
            }
            
            # 读取所有段落
            print("正在读取段落内容...")
            for i, para in enumerate(self.document.Paragraphs, 1):
                para_info = self._extract_paragraph_info(para, i)
                result['paragraphs'].append(para_info)
                
                if i % 50 == 0:
                    print(f"  已读取 {i}/{result['paragraph_count']} 个段落")
            
            # 读取表格信息
            if self.document.Tables.Count > 0:
                print(f"发现 {self.document.Tables.Count} 个表格，正在读取...")
                for i, table in enumerate(self.document.Tables, 1):
                    table_info = self._extract_table_info(table, i)
                    result['tables'].append(table_info)
            
            print(f"✓ 文档读取完成: {result['paragraph_count']} 段落, "
                  f"{result['word_count']} 词, {result['pages']} 页")
            
            return result
            
        except Exception as e:
            print(f"✗ 读取文档时出错: {e}")
            raise
        finally:
            self._close_word()
    
    def _extract_paragraph_info(self, para, index: int) -> Dict[str, Any]:
        """提取段落信息"""
        try:
            # 获取Range对象以访问格式
            rng = para.Range
            font = rng.Font
            
            # 对齐方式映射
            alignment_map = {
                0: 'left',      # wdAlignParagraphLeft
                1: 'center',    # wdAlignParagraphCenter
                2: 'right',     # wdAlignParagraphRight
                3: 'justify'    # wdAlignParagraphJustify
            }
            
            # 行距规则映射
            line_spacing_map = {
                0: 'single',       # wdLineSpaceSingle
                1: '1.5',          # wdLineSpace1pt5
                2: 'double',       # wdLineSpaceDouble
                3: 'at_least',     # wdLineSpaceAtLeast
                4: 'exactly',      # wdLineSpaceExactly
                5: 'multiple'      # wdLineSpaceMultiple
            }
            
            # 大纲级别映射
            outline_level = para.OutlineLevel
            if outline_level <= 9:
                outline_name = f"标题{outline_level}"
            else:
                outline_name = "正文"
            
            return {
                'index': index,
                'text': para.Range.Text.strip(),
                'style': para.Style.NameLocal if para.Style else None,
                'outline_level': outline_level if outline_level <= 9 else None,
                'outline_name': outline_name,
                'format': {
                    'font_name': font.Name,
                    'font_name_far_east': font.NameFarEast,  # 中文字体
                    'font_size': font.Size,
                    'bold': font.Bold,
                    'italic': font.Italic,
                    'underline': font.Underline != 0,  # wdUnderlineNone = 0
                    'color': font.Color if hasattr(font, 'Color') else None,
                    'highlight': font.HighlightColorIndex if hasattr(font, 'HighlightColorIndex') else None
                },
                'paragraph_format': {
                    'alignment': alignment_map.get(para.Alignment, 'unknown'),
                    'line_spacing_rule': line_spacing_map.get(para.LineSpacingRule, 'unknown'),
                    'line_spacing': para.LineSpacing,
                    'space_before': para.SpaceBefore,
                    'space_after': para.SpaceAfter,
                    'first_line_indent': para.FirstLineIndent,
                    'left_indent': para.LeftIndent,
                    'right_indent': para.RightIndent
                },
                'is_empty': len(para.Range.Text.strip()) == 0,
                'is_in_table': para.Range.Information(12)  # wdWithInTable
            }
        except Exception as e:
            return {
                'index': index,
                'text': '[读取失败]',
                'error': str(e)
            }
    
    def _extract_table_info(self, table, index: int) -> Dict[str, Any]:
        """提取表格信息"""
        try:
            rows = table.Rows.Count
            cols = table.Columns.Count
            
            # 读取表格内容
            cells_content = []
            for row in range(1, rows + 1):
                row_data = []
                for col in range(1, cols + 1):
                    try:
                        cell_text = table.Cell(row, col).Range.Text.strip()
                        # 去掉单元格文本末尾的\r\x07
                        cell_text = cell_text.replace('\r', '').replace('\x07', '')
                        row_data.append(cell_text)
                    except:
                        row_data.append('')
                cells_content.append(row_data)
            
            return {
                'index': index,
                'rows': rows,
                'columns': cols,
                'content': cells_content
            }
        except Exception as e:
            return {
                'index': index,
                'error': str(e)
            }
    
    def read_text_only(self, file_path: str) -> str:
        """
        仅读取纯文本内容（不包含格式）
        
        Args:
            file_path: Word文档路径
            
        Returns:
            文档的纯文本内容
        """
        result = self.read_document(file_path)
        texts = []
        for para in result['paragraphs']:
            if para['text'] and not para['is_empty']:
                texts.append(para['text'])
        return '\n'.join(texts)
    
    def export_to_json(self, file_path: str, output_path: Optional[str] = None) -> str:
        """
        将Word文档导出为JSON格式
        
        Args:
            file_path: Word文档路径
            output_path: 输出JSON文件路径，默认为同名.json
            
        Returns:
            输出文件路径
        """
        result = self.read_document(file_path)
        
        if output_path is None:
            output_path = str(Path(file_path).with_suffix('.json'))
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"✓ 已导出到: {output_path}")
        return output_path


def test_read():
    """测试读取功能"""
    import tempfile
    
    print("=" * 60)
    print("Word读取功能测试")
    print("=" * 60)
    
    # 先创建一个测试文档
    print("\n[测试1] 创建测试文档...")
    try:
        from word_vba_writer import WordWriter
        writer = WordWriter()
        doc = writer.create_document()
        
        # 添加不同格式的段落
        writer.add_paragraph(doc, "标题：测试文档", {
            'font_name': '黑体',
            'font_size': 16,
            'bold': True,
            'alignment': 'center'
        })
        
        writer.add_paragraph(doc, "", {})  # 空行
        
        writer.add_paragraph(doc, "这是一段正文内容，用于测试读取功能。", {
            'font_name': '宋体',
            'font_size': 12,
            'alignment': 'justify'
        })
        
        writer.add_paragraph(doc, "这是粗体斜体文字", {
            'font_name': '宋体',
            'font_size': 12,
            'bold': True,
            'italic': True
        })
        
        # 保存到临时文件
        temp_file = Path(tempfile.gettempdir()) / "word_vba_test.docx"
        writer.save_document(doc, str(temp_file))
        writer.close()
        
        print(f"✓ 测试文档已创建: {temp_file}")
        
        # 读取测试
        print("\n[测试2] 读取测试文档...")
        reader = WordReader()
        result = reader.read_document(str(temp_file))
        
        print(f"\n文档统计:")
        print(f"  - 段落数: {result['paragraph_count']}")
        print(f"  - 词数: {result['word_count']}")
        print(f"  - 页数: {result['pages']}")
        
        print(f"\n段落详情:")
        for para in result['paragraphs'][:5]:  # 只显示前5个
            print(f"\n  [段落{para['index']}]")
            print(f"    文本: {para['text'][:50]}...")
            print(f"    字体: {para['format']['font_name_far_east'] or para['format']['font_name']}")
            print(f"    大小: {para['format']['font_size']}pt")
            print(f"    粗体: {para['format']['bold']}")
            print(f"    对齐: {para['paragraph_format']['alignment']}")
        
        # 导出JSON测试
        print("\n[测试3] 导出JSON...")
        json_path = reader.export_to_json(str(temp_file))
        
        print("\n" + "=" * 60)
        print("✓ 所有测试通过！")
        print("=" * 60)
        
        # 清理临时文件
        temp_file.unlink(missing_ok=True)
        Path(json_path).unlink(missing_ok=True)
        
        return True
        
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_read()
