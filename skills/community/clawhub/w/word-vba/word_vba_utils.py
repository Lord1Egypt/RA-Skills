#!/usr/bin/env python3
"""
Word VBA 高级功能模块
提供批量处理、文档合并、模板填充等高级功能

作者: SuperMike
日期: 2026-03-04
"""

import win32com.client
import pythoncom
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Callable
import json
import re


class WordVBAUtils:
    """Word VBA 高级工具类"""
    
    def __init__(self, visible: bool = False):
        self.word_app = None
        self.visible = visible
        self.documents = []
        
    def _init_word(self) -> bool:
        """初始化Word应用"""
        try:
            pythoncom.CoInitialize()
            self.word_app = win32com.client.Dispatch("Word.Application")
            self.word_app.Visible = self.visible
            self.word_app.DisplayAlerts = 0
            return True
        except Exception as e:
            print(f"[ERROR] Word启动失败: {e}")
            return False
    
    def _close_word(self):
        """关闭Word应用"""
        try:
            for doc in self.documents:
                try:
                    doc.Close(SaveChanges=False)
                except:
                    pass
            if self.word_app:
                self.word_app.Quit()
                self.word_app = None
            pythoncom.CoUninitialize()
        except:
            pass
    
    def merge_documents(self, 
                       file_list: List[str], 
                       output_path: str,
                       add_page_breaks: bool = True,
                       keep_source_format: bool = True) -> str:
        """
        合并多个Word文档
        
        Args:
            file_list: 要合并的文档路径列表
            output_path: 输出文件路径
            add_page_breaks: 是否在每个文档后添加分页符
            keep_source_format: 是否保留源文档格式
            
        Returns:
            输出文件路径
        """
        if not self._init_word():
            raise RuntimeError("无法初始化Word")
        
        try:
            print(f"[INFO] 开始合并 {len(file_list)} 个文档...")
            
            # 创建新文档作为主文档
            main_doc = self.word_app.Documents.Add()
            self.documents.append(main_doc)
            
            for i, file_path in enumerate(file_list, 1):
                file_path = Path(file_path)
                if not file_path.exists():
                    print(f"[WARN] 文件不存在，跳过: {file_path}")
                    continue
                
                print(f"[{i}/{len(file_list)}] 正在插入: {file_path.name}")
                
                # 插入文件内容
                insert_range = main_doc.Content
                insert_range.Collapse(Direction=0)  # wdCollapseEnd
                
                # 使用InsertFile插入，可以保留格式
                insert_range.InsertFile(
                    FileName=str(file_path.absolute()),
                    ConfirmConversions=False
                )
                
                # 添加分页符
                if add_page_breaks and i < len(file_list):
                    insert_range = main_doc.Content
                    insert_range.Collapse(Direction=0)
                    insert_range.InsertBreak(Type=7)  # wdPageBreak
            
            # 保存合并后的文档
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            main_doc.SaveAs2(str(output_path.absolute()))
            
            print(f"[OK] 合并完成: {output_path}")
            return str(output_path)
            
        except Exception as e:
            print(f"[ERROR] 合并失败: {e}")
            raise
        finally:
            self._close_word()
    
    def fill_template(self,
                     template_path: str,
                     data: Dict[str, Any],
                     output_path: str,
                     placeholder_pattern: str = r'\{\{(.*?)\}\}') -> str:
        """
        填充模板文档
        
        Args:
            template_path: 模板文件路径（包含 {{key}} 占位符）
            data: 填充数据字典
            output_path: 输出文件路径
            placeholder_pattern: 占位符正则表达式，默认 {{key}}
            
        Returns:
            输出文件路径
        """
        if not self._init_word():
            raise RuntimeError("无法初始化Word")
        
        try:
            print(f"[INFO] 填充模板: {template_path}")
            
            # 打开模板
            template_path = Path(template_path)
            doc = self.word_app.Documents.Open(str(template_path.absolute()))
            self.documents.append(doc)
            
            # 查找并替换所有占位符
            replaced_count = 0
            for para in doc.Paragraphs:
                text = para.Range.Text
                matches = re.findall(placeholder_pattern, text)
                
                for key in matches:
                    key = key.strip()
                    if key in data:
                        placeholder = f"{{{{{key}}}}}"
                        value = str(data[key])
                        
                        # 使用Find替换
                        find_obj = doc.Content.Find
                        find_obj.Text = placeholder
                        find_obj.Replacement.Text = value
                        find_obj.Execute(Replace=2)  # wdReplaceAll
                        replaced_count += 1
            
            # 保存为新文档
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            doc.SaveAs2(str(output_path.absolute()))
            
            print(f"[OK] 填充完成，替换了 {replaced_count} 个占位符")
            print(f"[OK] 输出文件: {output_path}")
            
            return str(output_path)
            
        except Exception as e:
            print(f"[ERROR] 模板填充失败: {e}")
            raise
        finally:
            self._close_word()
    
    def batch_replace(self,
                     file_path: str,
                     replacements: Dict[str, str],
                     output_path: Optional[str] = None) -> str:
        """
        批量替换文档中的文本
        
        Args:
            file_path: 源文档路径
            replacements: 替换字典 {旧文本: 新文本}
            output_path: 输出路径，默认覆盖原文件
            
        Returns:
            输出文件路径
        """
        if not self._init_word():
            raise RuntimeError("无法初始化Word")
        
        try:
            print(f"[INFO] 批量替换: {file_path}")
            
            file_path = Path(file_path)
            doc = self.word_app.Documents.Open(str(file_path.absolute()))
            self.documents.append(doc)
            
            replace_count = 0
            for old_text, new_text in replacements.items():
                find_obj = doc.Content.Find
                find_obj.Text = old_text
                find_obj.Replacement.Text = new_text
                
                while find_obj.Execute(Replace=1):  # wdReplaceOne
                    replace_count += 1
            
            # 保存
            if output_path is None:
                output_path = file_path
            else:
                output_path = Path(output_path)
                output_path.parent.mkdir(parents=True, exist_ok=True)
            
            doc.SaveAs2(str(Path(output_path).absolute()))
            
            print(f"[OK] 替换了 {replace_count} 处文本")
            return str(output_path)
            
        except Exception as e:
            print(f"[ERROR] 替换失败: {e}")
            raise
        finally:
            self._close_word()
    
    def extract_headings(self, file_path: str) -> List[Dict[str, Any]]:
        """
        提取文档中的标题大纲
        
        Args:
            file_path: Word文档路径
            
        Returns:
            标题列表，包含级别和文本
        """
        if not self._init_word():
            raise RuntimeError("无法初始化Word")
        
        try:
            file_path = Path(file_path)
            doc = self.word_app.Documents.Open(str(file_path.absolute()))
            self.documents.append(doc)
            
            headings = []
            for para in doc.Paragraphs:
                outline_level = para.OutlineLevel
                if outline_level <= 9:  # 是标题
                    headings.append({
                        'level': outline_level,
                        'text': para.Range.Text.strip(),
                        'style': para.Style.NameLocal if para.Style else None
                    })
            
            return headings
            
        except Exception as e:
            print(f"[ERROR] 提取标题失败: {e}")
            raise
        finally:
            self._close_word()
    
    def generate_toc(self, file_path: str, output_path: Optional[str] = None) -> str:
        """
        为文档生成目录
        
        Args:
            file_path: 源文档路径
            output_path: 输出路径，默认覆盖原文件
            
        Returns:
            输出文件路径
        """
        if not self._init_word():
            raise RuntimeError("无法初始化Word")
        
        try:
            print(f"[INFO] 生成目录: {file_path}")
            
            file_path = Path(file_path)
            doc = self.word_app.Documents.Open(str(file_path.absolute()))
            self.documents.append(doc)
            
            # 在文档开头插入目录
            rng = doc.Content
            rng.Collapse(Direction=1)  # wdCollapseStart
            
            # 添加"目录"标题
            toc_para = doc.Content.Paragraphs.Add(rng)
            toc_para.Range.Text = "目录\r"
            toc_para.Style = doc.Styles("标题 1")
            
            # 插入目录域
            rng = doc.Content
            rng.Collapse(Direction=1)
            toc_field = doc.Fields.Add(rng, -1, "TOC \\o \"1-3\" \\h \\z \\u", True)
            
            # 更新目录
            toc_field.Update()
            
            # 保存
            if output_path is None:
                output_path = file_path
            else:
                output_path = Path(output_path)
                output_path.parent.mkdir(parents=True, exist_ok=True)
            
            doc.SaveAs2(str(Path(output_path).absolute()))
            
            print("[OK] 目录生成完成")
            return str(output_path)
            
        except Exception as e:
            print(f"[ERROR] 生成目录失败: {e}")
            raise
        finally:
            self._close_word()
    
    def compare_documents(self, 
                         doc1_path: str, 
                         doc2_path: str,
                         output_path: str) -> str:
        """
        比较两个文档的差异
        
        Args:
            doc1_path: 原始文档路径
            doc2_path: 修改后文档路径
            output_path: 比较结果输出路径
            
        Returns:
            输出文件路径
        """
        if not self._init_word():
            raise RuntimeError("无法初始化Word")
        
        try:
            print(f"[INFO] 比较文档...")
            
            doc1 = self.word_app.Documents.Open(str(Path(doc1_path).absolute()))
            doc2 = self.word_app.Documents.Open(str(Path(doc2_path).absolute()))
            self.documents.extend([doc1, doc2])
            
            # 创建比较文档
            compare_doc = self.word_app.CompareDocuments(
                OriginalDocument=doc1,
                RevisedDocument=doc2
            )
            self.documents.append(compare_doc)
            
            # 保存比较结果
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            compare_doc.SaveAs2(str(output_path.absolute()))
            
            print(f"[OK] 比较完成: {output_path}")
            return str(output_path)
            
        except Exception as e:
            print(f"[ERROR] 比较失败: {e}")
            raise
        finally:
            self._close_word()
    
    def batch_process(self,
                     file_list: List[str],
                     processor: Callable[[Any], None],
                     output_dir: str):
        """
        批量处理多个文档
        
        Args:
            file_list: 文档路径列表
            processor: 处理函数，接收文档对象作为参数
            output_dir: 输出目录
        """
        if not self._init_word():
            raise RuntimeError("无法初始化Word")
        
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            for i, file_path in enumerate(file_list, 1):
                file_path = Path(file_path)
                if not file_path.exists():
                    continue
                
                print(f"[{i}/{len(file_list)}] 处理: {file_path.name}")
                
                doc = self.word_app.Documents.Open(str(file_path.absolute()))
                
                # 执行处理
                processor(doc)
                
                # 保存
                output_path = output_dir / file_path.name
                doc.SaveAs2(str(output_path.absolute()))
                doc.Close()
                
        except Exception as e:
            print(f"[ERROR] 批量处理失败: {e}")
            raise
        finally:
            self._close_word()


def test_utils():
    """测试高级功能"""
    import tempfile
    from word_vba_writer import WordWriter
    
    print("=" * 60)
    print("Word VBA 高级功能测试")
    print("=" * 60)
    
    utils = WordVBAUtils()
    temp_dir = Path(tempfile.gettempdir())
    
    try:
        # 测试1: 创建测试文档
        print("\n[测试1] 创建测试文档...")
        writer = WordWriter()
        
        # 文档1
        doc1 = writer.create_document()
        writer.add_heading(doc1, "第一章 引言", level=1)
        writer.add_paragraph(doc1, "这是第一章的内容。", {'font_name': '宋体'})
        doc1_path = temp_dir / "test_doc1.docx"
        writer.save_document(doc1, str(doc1_path))
        
        # 文档2
        doc2 = writer.create_document()
        writer.add_heading(doc2, "第二章 方法", level=1)
        writer.add_paragraph(doc2, "这是第二章的内容。", {'font_name': '宋体'})
        doc2_path = temp_dir / "test_doc2.docx"
        writer.save_document(doc2, str(doc2_path))
        writer.close()
        
        print(f"[OK] 创建测试文档完成")
        
        # 测试2: 合并文档
        print("\n[测试2] 测试文档合并...")
        merged_path = utils.merge_documents(
            [str(doc1_path), str(doc2_path)],
            str(temp_dir / "merged.docx")
        )
        print(f"[OK] 合并完成: {merged_path}")
        
        # 测试3: 提取标题
        print("\n[测试3] 提取文档标题...")
        headings = utils.extract_headings(str(doc1_path))
        print(f"[OK] 找到 {len(headings)} 个标题:")
        for h in headings:
            print(f"  - 级别{h['level']}: {h['text'][:30]}")
        
        # 测试4: 模板填充
        print("\n[测试4] 测试模板填充...")
        
        # 创建模板
        template_writer = WordWriter()
        template_doc = template_writer.create_document()
        template_writer.add_paragraph(template_doc, "项目名称: {{project_name}}", {})
        template_writer.add_paragraph(template_doc, "负责人: {{leader}}", {})
        template_writer.add_paragraph(template_doc, "预算: {{budget}}万元", {})
        template_path = temp_dir / "template.docx"
        template_writer.save_document(template_doc, str(template_path))
        template_writer.close()
        
        # 填充数据
        data = {
            'project_name': '国家自然科学基金项目',
            'leader': '纪金豹',
            'budget': '50'
        }
        filled_path = utils.fill_template(
            str(template_path),
            data,
            str(temp_dir / "filled.docx")
        )
        print(f"[OK] 模板填充完成: {filled_path}")
        
        # 测试5: 批量替换
        print("\n[测试5] 测试批量替换...")
        replacements = {
            '第一章': 'Chapter 1',
            '第二章': 'Chapter 2'
        }
        replaced_path = utils.batch_replace(
            str(merged_path),
            replacements,
            str(temp_dir / "replaced.docx")
        )
        print(f"[OK] 替换完成: {replaced_path}")
        
        print("\n" + "=" * 60)
        print("所有高级功能测试通过！")
        print("=" * 60)
        
        # 清理
        for f in temp_dir.glob("test_doc*.docx"):
            f.unlink(missing_ok=True)
        for f in temp_dir.glob("merged.docx"):
            f.unlink(missing_ok=True)
        for f in temp_dir.glob("template.docx"):
            f.unlink(missing_ok=True)
        for f in temp_dir.glob("filled.docx"):
            f.unlink(missing_ok=True)
        for f in temp_dir.glob("replaced.docx"):
            f.unlink(missing_ok=True)
        
        return True
        
    except Exception as e:
        print(f"\n[ERROR] 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_utils()
