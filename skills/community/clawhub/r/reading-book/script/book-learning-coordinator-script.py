"""
书籍学习协调脚本
协调管理书籍学习的完整流程，控制各模块顺序执行
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

# 导入子模块
from book_extractor_script import process_book
from note_generator_script import NoteGenerator
from neo4j_cypher_generator_script import Neo4jCypherGenerator
from neo4j_importer_script import Neo4jImporter


class BookLearningCoordinator:
    """书籍学习协调器"""
    
    def __init__(self):
        """初始化协调器"""
        self.note_generator = NoteGenerator()
        self.cypher_generator = Neo4jCypherGenerator()
        self.neo4j_importer = Neo4jImporter()
        
        # 学习状态
        self.learning_state = {
            "book_path": None,
            "book_title": None,
            "total_chapters": 0,
            "completed_chapters": 0,
            "failed_chapters": [],
            "start_time": None,
            "end_time": None,
            "progress_file": None
        }
    
    def validate_input(self, book_path: str) -> Dict[str, Any]:
        """
        验证书籍路径
        Args:
            book_path: 书籍路径
        Returns:
            dict: 验证结果
        """
        # 路径格式验证
        path_pattern = r"F:\\book\\([^\\]+)\\([^\\]+\.(docx|pdf))$"
        
        if not os.path.exists(book_path):
            return {
                "success": False,
                "error": f"文件不存在: {book_path}"
            }
        
        file_ext = os.path.splitext(book_path)[1].lower()
        if file_ext not in ['.docx', '.pdf']:
            return {
                "success": False,
                "error": f"不支持的文件格式: {file_ext}，仅支持.docx和.pdf"
            }
        
        return {
            "success": True,
            "file_type": file_ext
        }
    
    def extract_book_title(self, book_path: str) -> str:
        """
        从路径提取书名
        Args:
            book_path: 书籍路径
        Returns:
            str: 书名
        """
        return os.path.basename(os.path.dirname(book_path))
    
    def create_note_directory(self, book_title: str) -> str:
        """
        创建笔记目录
        Args:
            book_title: 书名
        Returns:
            str: 笔记目录路径
        """
        note_path = f"F:\\Obsidian\\{book_title}"
        
        if not os.path.exists(note_path):
            os.makedirs(note_path, exist_ok=True)
            print(f"Created: {note_path}")
        
        return note_path
    
    def initialize_progress_file(self, book_title: str, total_chapters: int) -> str:
        """
        初始化进度跟踪文件
        Args:
            book_title: 书名
            total_chapters: 总章节数
        Returns:
            str: 进度文件路径
        """
        progress_file = f"F:\\Obsidian\\{book_title}\\学习进度跟踪.md"
        
        content = f"""# 《{book_title}》学习进度

- **开始日期**: {datetime.now().strftime("%Y-%m-%d")}
- **总章节数**: {total_chapters} 章
- **已完成**: 0/{total_chapters}
- **状态**: 📖 进行中

## 章节进度

| 章节 | 标题 | 笔记文件 | Neo4j概念数 | Neo4j关系数 | 状态 | 完成时间 |
|------|------|---------|------------|------------|------|---------|
"""
        
        with open(progress_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"初始化进度文件: {progress_file}")
        return progress_file
    
    def update_progress_file(self, progress_file: str, chapter_num: int, 
                            chapter_title: str, note_file: str, 
                            concepts_count: int, relationships_count: int,
                            success: bool):
        """
        更新进度文件
        """
        if not os.path.exists(progress_file):
            return
        
        with open(progress_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 找到章节进度表格，添加新行
        new_line = f"| Ch {chapter_num} | {chapter_title} | {note_file} | {concepts_count} | {relationships_count} | {'✅' if success else '❌'} | {datetime.now().strftime('%Y-%m-%d %H:%M')} |\n"
        
        # 在表格最后添加
        for i, line in enumerate(lines):
            if line.strip() == "" and i > len(lines) // 2:
                lines.insert(i, new_line)
                break
        
        # 更新完成计数
        self._update_completion_count(lines, success)
        
        with open(progress_file, 'w', encoding='utf-8') as f:
            f.writelines(lines)
    
    def _update_completion_count(self, lines: List[str], success: bool):
        """更新完成计数"""
        for i, line in enumerate(lines):
            if "- **已完成**:" in line:
                # 提取当前计数
                import re
                match = re.search(r'已完成\):\s*(\d+)/(\d+)', line)
                if match:
                    current = int(match.group(1))
                    total = int(match.group(2))
                    if success:
                        current += 1
                    lines[i] = line.replace(
                        f"{match.group(1)}/{match.group(2)}",
                        f"{current}/{total}"
                    )
                break
    
    def process_chapter(self, chapter_data: Dict[str, Any], book_title: str, 
                        book_info: Dict[str, Any], progress_file: str) -> Dict[str, Any]:
        """
        处理单个章节的完整学习流程
        Args:
            chapter_data: 章节数据
            book_title: 书名
            book_info: 书籍信息
            progress_file: 进度文件路径
        Returns:
            dict: 处理结果
        """
        chapter_num = chapter_data['chapter']
        chapter_title = chapter_data['title']
        
        print(f"\n{'='*60}")
        print(f"处理 Chapter {chapter_num}: {chapter_title}")
        print(f"{'='*60}")
        
        # Step 1: 调用 note-generator
        print("[Step 1/3] 生成学习笔记...")
        note_result = self.note_generator.generate_note({
            "book_title": book_title,
            "chapter": chapter_num,
            "title": chapter_title,
            "book_version": book_info.get('version', ''),
            "author": book_info.get('author', ''),
            "total_chapters": self.learning_state['total_chapters'],
            "paragraphs": chapter_data.get('paragraphs', [])
        })
        
        if not note_result['success']:
            print(f"❌ 笔记生成失败")
            return {
                "chapter": chapter_num,
                "success": False,
                "error": "Note generation failed",
                "stage": "note_generator"
            }
        
        print(f"✅ 笔记生成成功 ({len(note_result['concepts'])}个概念)")
        
        # Step 2: 调用 neo4j-cypher-generator
        print("[Step 2/3] 生成Cypher语句...")
        cypher_result = self.cypher_generator.generate_batches({
            "book_title": book_title,
            "chapter": chapter_num,
            "concepts": note_result['concepts'],
            "relationships": note_result['relationships']
        })
        
        if not cypher_result['success']:
            print(f"❌ Cypher生成失败")
            return {
                "chapter": chapter_num,
                "success": False,
                "error": "Cypher generation failed",
                "stage": "cypher_generator"
            }
        
        print(f"✅ Cypher生成成功 ({cypher_result['total_batches']}个批次)")
        
        # Step 3: 调用 neo4j-importer
        print("[Step 3/3] 导入到Neo4j...")
        import_result = self.neo4j_importer.import_batches(cypher_result)
        
        if not import_result['overall_success']:
            print(f"⚠️ Neo4j导入部分失败")
            # 记录但不终止，继续下一章节
        
        concepts_count = import_result.get('verification', {}).get('imported_concepts', 0)
        relationships_count = import_result.get('verification', {}).get('imported_relationships', 0)
        
        print(f"✅ 导入完成 ({concepts_count}概念, {relationships_count}关系)")
        
        # Step 4: 更新进度文件
        self.update_progress_file(
            progress_file,
            chapter_num,
            chapter_title,
            note_result['note_file'],
            concepts_count,
            relationships_count,
            import_result['overall_success']
        )
        
        return {
            "chapter": chapter_num,
            "success": import_result['overall_success'],
            "note_file": note_result['note_file'],
            "concepts_count": concepts_count,
            "relationships_count": relationships_count
        }
    
    def generate_full_book_summary(self, learning_state: Dict[str, Any], 
                                   chapter_results: List[Dict[str, Any]]) -> str:
        """
        生成全书总结报告
        """
        book_title = learning_state['book_title']
        
        # 统计
        total_concepts = sum(r.get('concepts_count', 0) for r in chapter_results)
        total_relationships = sum(r.get('relationships_count', 0) for r in chapter_results)
        successful = sum(1 for r in chapter_results if r.get('success'))
        
        # 生成报告
        summary_file = f"F:\\Obsidian\\{book_title}\\全书学习完成报告.md"
        
        content = f"""# 🎉《{book_title}》全书学习完成报告

> **书籍**: {book_title}
> **学习日期**: {learning_state['start_time']} ~ {learning_state['end_time']}
> **学习方式**: 逐章笔记 + Neo4j 知识图谱

---

## ✅ 学习统计

| 指标 | 完成 |
|------|------|
| **总章节数** | {learning_state['total_chapters']} 章 |
| **成功完成** | {successful} 章 ✅ |
| **失败跳过** | {learning_state['total_chapters'] - successful} 章 |
| **Obsidian 笔记** | {successful} 个文件 ✅ |
| **Neo4j 概念** | {total_concepts} 个概念 ✅ |
| **Neo4j 关系** | {total_relationships} 个关系 ✅ |
| **总耗时** | ~{learning_state.get('duration_hours', 0)} 小时 ✅ |

---

## 📁 笔记文件

| 章节 | 标题 | 笔记文件 | 概念数 | 关系数 | 状态 |
|------|------|---------|-------|-------|------|
"""
        
        for result in chapter_results:
            if 'note_file' in result:
                content += f"| Ch {result['chapter']} | | {result['note_file']} | {result.get('concepts_count', 0)} | {result.get('relationships_count', 0)} | {'✅' if result.get('success') else '❌'} |\n"
        
        content += """

---

## 💡 全书核心思想总结

### 核心理念 1
> "需要根据学习内容总结核心思想"

**应用**:
- 应用1
- 应用2

---

## 🎯 实践应用指南

### 行动清单
- [ ] 应用1
- [ ] 应用2
- [ ] 应用3

---

_学习报告由梅梅整理 · {datetime.now().strftime("%Y-%m-%d")}_ ✨
"""
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"\n全书总结报告已生成: {summary_file}")
        return summary_file
    
    def start_learning(self, book_path: str, resume_from: Optional[int] = None) -> Dict[str, Any]:
        """
        开始学习流程
        Args:
            book_path: 书籍路径
            resume_from: 从指定章节继续（可选）
        Returns:
            dict: 学习结果
        """
        print("\n" + "="*60)
        print("开始书籍学习流程")
        print("="*60)
        
        # Step 1: 验证输入
        print("\n[Step 1/5] 验证书籍路径...")
        validation = self.validate_input(book_path)
        if not validation['success']:
            print(f"❌ 验证失败: {validation['error']}")
            return {"success": False, "error": validation['error']}
        
        print(f"✅ 验证通过 (格式: {validation['file_type']})")
        
        # Step 2: 提取书名
        book_title = self.extract_book_title(book_path)
        print(f"✅ 书名: {book_title}")
        
        # Step 3: 调用 book-extractor
        print("\n[Step 2/5] 提取章节内容...")
        extractor_result = process_book(book_path, book_title)
        
        if not extractor_result['success']:
            print(f"❌ 章节提取失败: {extractor_result['error']}")
            return {"success": False, "error": extractor_result['error']}
        
        chapters = extractor_result['chapters']
        total_chapters = len(chapters)
        print(f"✅ 提取成功 ({total_chapters} 个章节)")
        
        # Step 4: 初始化学习环境
        print("\n[Step 3/5] 初始化学习环境...")
        self.create_note_directory(book_title)
        progress_file = self.initialize_progress_file(book_title, total_chapters)
        
        # 更新状态
        self.learning_state.update({
            "book_path": book_path,
            "book_title": book_title,
            "total_chapters": total_chapters,
            "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "progress_file": progress_file
        })
        
        print(f"✅ 学习环境初始化完成")
        
        # Step 5: 逐章学习
        print("\n[Step 4/5] 开始逐章学习...")
        chapter_results = []
        
        start_chapter = resume_from if resume_from else 1
        
        for chapter in chapters:
            if chapter['chapter'] < start_chapter:
                continue
            
            result = self.process_chapter(
                chapter,
                book_title,
                extractor_result['book_info'],
                progress_file
            )
            
            chapter_results.append(result)
            
            if result['success']:
                self.learning_state['completed_chapters'] += 1
            else:
                self.learning_state['failed_chapters'].append(result['chapter'])
        
        # Step 6: 生成全书总结
        print("\n[Step 5/5] 生成全书总结...")
        self.learning_state['end_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        summary_file = self.generate_full_book_summary(
            self.learning_state,
            chapter_results
        )
        
        # 输出最终统计
        print("\n" + "="*60)
        print("学习完成！")
        print("="*60)
        print(f"书籍: {book_title}")
        print(f"总章节: {total_chapters}")
        print(f"成功: {self.learning_state['completed_chapters']}")
        print(f"失败: {len(self.learning_state['failed_chapters'])}")
        print(f"笔记: F:\\Obsidian\\{book_title}")
        print(f"总结: {summary_file}")
        
        return {
            "success": True,
            "book_title": book_title,
            "total_chapters": total_chapters,
            "completed_chapters": self.learning_state['completed_chapters'],
            "failed_chapters": self.learning_state['failed_chapters'],
            "chapter_results": chapter_results,
            "summary_file": summary_file,
            "progress_file": progress_file
        }


# 使用示例
if __name__ == "__main__":
    coordinator = BookLearningCoordinator()
    
    # 开始学习
    result = coordinator.start_learning(
        book_path=r"F:\book\Security Analysis\Security Analysis.docx"
    )
    
    if result['success']:
        print("\n✅ 学习流程成功完成!")
    else:
        print(f"\n❌ 学习流程失败: {result.get('error', 'Unknown error')}")
