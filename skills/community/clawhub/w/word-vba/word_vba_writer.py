#!/usr/bin/env python3
"""
Word文档写入模块 - 基于VBA/ActiveX (编码修复版)
支持创建doc和docx文件，可设置段落格式

作者: SuperMike
日期: 2026-03-04
"""

import win32com.client
import pythoncom
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
import json


class WordWriter:
    """Word文档写入器 - 使用COM接口调用Word VBA"""
    
    def __init__(self, visible: bool = False):
        """
        初始化Word写入器
        
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
            self.word_app.DisplayAlerts = 0
            print("[OK] Word应用启动成功")
            return True
        except Exception as e:
            print(f"[ERROR] Word应用启动失败: {e}")
            print("[提示] 请确保已安装Microsoft Word")
            return False
    
    def close(self):
        """关闭Word应用"""
        try:
            if self.document:
                self.document.Close(SaveChanges=False)
                self.document = None
            if self.word_app:
                self.word_app.Quit()
                self.word_app = None
            pythoncom.CoUninitialize()
            print("[OK] Word应用已关闭")
        except Exception as e:
            print(f"[WARN] 关闭Word时出错: {e}")
    
    def create_document(self) -> Any:
        """
        创建新的Word文档
        
        Returns:
            Word文档对象
        """
        if not self.word_app and not self._init_word():
            raise RuntimeError("无法初始化Word应用")
        
        try:
            self.document = self.word_app.Documents.Add()
            print("[OK] 新文档创建成功")
            return self.document
        except Exception as e:
            print(f"[ERROR] 创建文档失败: {e}")
            raise
    
    def open_document(self, file_path: str) -> Any:
        """
        打开现有Word文档
        
        Args:
            file_path: Word文档路径
            
        Returns:
            Word文档对象
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        if not self.word_app and not self._init_word():
            raise RuntimeError("无法初始化Word应用")
        
        try:
            self.document = self.word_app.Documents.Open(str(file_path.absolute()))
            print(f"[OK] 文档已打开: {file_path}")
            return self.document
        except Exception as e:
            print(f"[ERROR] 打开文档失败: {e}")
            raise
    
    def add_paragraph(self, 
                      document: Any, 
                      text: str, 
                      format_dict: Optional[Dict[str, Any]] = None,
                      style: Optional[str] = None) -> Any:
        """
        添加段落并设置格式
        
        Args:
            document: Word文档对象
            text: 段落文本
            format_dict: 格式设置字典
            style: 段落样式名称（如"标题 1"、"正文"）
            
        Returns:
            段落对象
        """
        try:
            # 添加段落
            para = document.Content.Paragraphs.Add()
            para.Range.Text = text + '\r'  # Word需要\r作为段落结束
            
            # 应用样式
            if style:
                try:
                    para.Style = document.Styles(style)
                except:
                    print(f"[WARN] 样式'{style}'不存在，使用默认样式")
            
            # 应用格式
            if format_dict:
                self._apply_format(para, format_dict)
            
            return para
            
        except Exception as e:
            print(f"[ERROR] 添加段落失败: {e}")
            raise
    
    def _apply_format(self, para: Any, format_dict: Dict[str, Any]):
        """应用格式设置到段落"""
        try:
            rng = para.Range
            font = rng.Font
            pf = para.ParagraphFormat
            
            # 字体设置
            if 'font_name' in format_dict:
                font.Name = format_dict['font_name']
            
            if 'font_name_far_east' in format_dict:
                font.NameFarEast = format_dict['font_name_far_east']
            
            if 'font_size' in format_dict:
                font.Size = format_dict['font_size']
            
            # 字形设置
            if 'bold' in format_dict:
                font.Bold = format_dict['bold']
            
            if 'italic' in format_dict:
                font.Italic = format_dict['italic']
            
            if 'underline' in format_dict:
                if format_dict['underline']:
                    font.Underline = 1  # wdUnderlineSingle
                else:
                    font.Underline = 0  # wdUnderlineNone
            
            # 颜色设置
            if 'color' in format_dict and format_dict['color']:
                font.Color = format_dict['color']
            
            # 对齐方式
            if 'alignment' in format_dict:
                alignment_map = {
                    'left': 0,      # wdAlignParagraphLeft
                    'center': 1,    # wdAlignParagraphCenter
                    'right': 2,     # wdAlignParagraphRight
                    'justify': 3    # wdAlignParagraphJustify
                }
                pf.Alignment = alignment_map.get(format_dict['alignment'], 0)
            
            # 行距设置
            if 'line_spacing' in format_dict:
                pf.LineSpacing = format_dict['line_spacing']
            
            if 'line_spacing_rule' in format_dict:
                line_spacing_map = {
                    'single': 0,
                    '1.5': 1,
                    'double': 2,
                    'at_least': 3,
                    'exactly': 4,
                    'multiple': 5
                }
                pf.LineSpacingRule = line_spacing_map.get(format_dict['line_spacing_rule'], 0)
            
            # 段前段后间距
            if 'space_before' in format_dict:
                pf.SpaceBefore = format_dict['space_before']
            
            if 'space_after' in format_dict:
                pf.SpaceAfter = format_dict['space_after']
            
            # 缩进设置
            if 'first_line_indent' in format_dict:
                pf.FirstLineIndent = format_dict['first_line_indent']
            
            if 'left_indent' in format_dict:
                pf.LeftIndent = format_dict['left_indent']
            
            if 'right_indent' in format_dict:
                pf.RightIndent = format_dict['right_indent']
            
            # 大纲级别
            if 'outline_level' in format_dict:
                para.OutlineLevel = format_dict['outline_level']
                
        except Exception as e:
            print(f"[WARN] 应用格式时出错: {e}")
    
    def add_heading(self, 
                    document: Any, 
                    text: str, 
                    level: int = 1,
                    format_dict: Optional[Dict[str, Any]] = None) -> Any:
        """
        添加标题
        
        Args:
            document: Word文档对象
            text: 标题文本
            level: 标题级别（1-9）
            format_dict: 额外格式设置
            
        Returns:
            段落对象
        """
        default_format = {
            'font_name': '黑体',
            'font_size': {1: 16, 2: 14, 3: 12}.get(level, 12),
            'bold': True,
            'outline_level': level
        }
        
        if format_dict:
            default_format.update(format_dict)
        
        return self.add_paragraph(document, text, default_format)
    
    def add_table(self, 
                  document: Any, 
                  rows: int, 
                  cols: int,
                  data: Optional[List[List[str]]] = None) -> Any:
        """
        添加表格
        
        Args:
            document: Word文档对象
            rows: 行数
            cols: 列数
            data: 表格数据（二维列表）
            
        Returns:
            表格对象
        """
        try:
            # 在文档末尾添加表格
            rng = document.Content
            rng.Collapse(Direction=0)  # wdCollapseEnd
            
            table = document.Tables.Add(rng, rows, cols)
            
            # 填充数据
            if data:
                for i, row_data in enumerate(data[:rows], 1):
                    for j, cell_text in enumerate(row_data[:cols], 1):
                        try:
                            table.Cell(i, j).Range.Text = str(cell_text)
                        except:
                            pass
            
            print(f"[OK] 表格添加成功: {rows}行 x {cols}列")
            return table
            
        except Exception as e:
            print(f"[ERROR] 添加表格失败: {e}")
            raise
    
    def insert_page_break(self, document: Any):
        """插入分页符"""
        try:
            rng = document.Content
            rng.Collapse(Direction=0)
            rng.InsertBreak(Type=7)  # wdPageBreak
        except Exception as e:
            print(f"[WARN] 插入分页符失败: {e}")
    
    def save_document(self, 
                      document: Any, 
                      file_path: str,
                      file_format: Optional[str] = None):
        """
        保存文档
        
        Args:
            document: Word文档对象
            file_path: 保存路径
            file_format: 文件格式（'docx'或'doc'），默认根据扩展名判断
        """
        try:
            file_path = Path(file_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 确定文件格式
            if file_format is None:
                ext = file_path.suffix.lower()
                if ext == '.doc':
                    file_format = 'doc'
                else:
                    file_format = 'docx'
            
            # 格式常量
            format_constants = {
                'docx': 16,   # wdFormatDocumentDefault
                'doc': 0,     # wdFormatDocument
                'pdf': 17,    # wdFormatPDF
                'rtf': 6      # wdFormatRTF
            }
            
            save_format = format_constants.get(file_format, 16)
            
            document.SaveAs2(
                FileName=str(file_path.absolute()),
                FileFormat=save_format
            )
            
            print(f"[OK] 文档已保存: {file_path}")
            
        except Exception as e:
            print(f"[ERROR] 保存文档失败: {e}")
            raise
    
    def write_from_json(self, json_path: str, output_docx: str):
        """
        从JSON文件恢复Word文档
        
        Args:
            json_path: JSON文件路径（由WordReader导出）
            output_docx: 输出Word文档路径
        """
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        doc = self.create_document()
        
        # 写入段落
        for para_info in data.get('paragraphs', []):
            text = para_info.get('text', '')
            fmt = para_info.get('format', {})
            pf = para_info.get('paragraph_format', {})
            
            # 合并格式
            format_dict = {**fmt, **pf}
            
            self.add_paragraph(doc, text, format_dict)
        
        # 写入表格
        for table_info in data.get('tables', []):
            rows = table_info.get('rows', 0)
            cols = table_info.get('columns', 0)
            content = table_info.get('content', [])
            
            if rows > 0 and cols > 0:
                self.add_table(doc, rows, cols, content)
        
        self.save_document(doc, output_docx)
        print(f"[OK] 已从JSON恢复文档: {output_docx}")


def test_write():
    """测试写入功能"""
    import tempfile
    
    print("=" * 60)
    print("Word写入功能测试")
    print("=" * 60)
    
    try:
        writer = WordWriter(visible=False)
        doc = writer.create_document()
        
        # 测试1: 添加标题
        print("\n[测试1] 添加标题...")
        writer.add_heading(doc, "一、测试文档标题", level=1)
        writer.add_heading(doc, "1.1 子标题", level=2)
        
        # 测试2: 添加正文
        print("[测试2] 添加正文段落...")
        writer.add_paragraph(doc, "这是第一段正文，使用宋体12号字。", {
            'font_name': '宋体',
            'font_size': 12,
            'alignment': 'justify'
        })
        
        writer.add_paragraph(doc, "这是第二段正文，使用楷体，左对齐。", {
            'font_name': '楷体',
            'font_size': 12,
            'alignment': 'left'
        })
        
        # 测试3: 添加格式文本
        print("[测试3] 添加格式文本...")
        writer.add_paragraph(doc, "这是粗体文字", {
            'font_name': '宋体',
            'font_size': 12,
            'bold': True
        })
        
        writer.add_paragraph(doc, "这是斜体文字", {
            'font_name': '宋体',
            'font_size': 12,
            'italic': True
        })
        
        writer.add_paragraph(doc, "这是居中文字", {
            'font_name': '宋体',
            'font_size': 12,
            'alignment': 'center'
        })
        
        # 测试4: 添加表格
        print("[测试4] 添加表格...")
        table_data = [
            ["姓名", "年龄", "职业"],
            ["张三", "28", "工程师"],
            ["李四", "32", "教师"],
            ["王五", "25", "医生"]
        ]
        writer.add_table(doc, 4, 3, table_data)
        
        # 测试5: 添加更多段落
        print("[测试5] 添加更多内容...")
        writer.add_paragraph(doc, "", {})
        writer.add_paragraph(doc, "以上表格展示了测试数据。", {
            'font_name': '宋体',
            'font_size': 12
        })
        
        # 保存文档
        temp_file = Path(tempfile.gettempdir()) / "word_vba_write_test.docx"
        writer.save_document(doc, str(temp_file))
        writer.close()
        
        print(f"\n[OK] 测试文档已保存: {temp_file}")
        
        # 验证文档是否存在
        if temp_file.exists():
            size = temp_file.stat().st_size
            print(f"[OK] 文件大小: {size} 字节")
            print("\n" + "=" * 60)
            print("所有写入测试通过！")
            print("=" * 60)
            
            # 清理
            temp_file.unlink(missing_ok=True)
            return True
        else:
            print("[ERROR] 文件未创建")
            return False
            
    except Exception as e:
        print(f"\n[ERROR] 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_write()
