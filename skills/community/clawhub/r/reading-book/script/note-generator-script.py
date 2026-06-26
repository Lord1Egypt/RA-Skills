"""
笔记生成脚本
根据章节内容生成结构化Markdown学习笔记
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Any


class NoteGenerator:
    """笔记生成器"""
    
    def __init__(self):
        self.template = """# 📖 {book_title} - Chapter {chapter}

> **Chapter**: {chapter}
> **Title**: {title}
> **Source**: {book_title} ({book_version}) - {author}
> **学习日期**: {learning_date}
> **标签**: #{tag} #Chapter{chapter} #{topic}

---

## 📋 本章概览

**核心主题**: {core_theme}

本章讲解：
{points}

---

## 🎯 核心概念

{concepts_section}

---

## 📊 本章框架

```mermaid
mindmap
  root((Chapter {chapter}))
{mindmap_content}
```

---

## 💡 核心金句

{quotes}

---

## 📝 思考题

{questions}

---

## 🎓 学习收获

### 知识收获
{knowledge_harvest}

### 技能提升
{skill_improvement}

### 思维转变
{mindset_change}

---

_学习笔记由梅梅整理 · {learning_date}_ ✨
_Progress: Chapter {chapter}/{total_chapters}_ 📖
_Next: Chapter {next_chapter} - {next_title}_
"""
    
    def generate_note(self, chapter_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成学习笔记
        Args:
            chapter_data: 章节数据
        Returns:
            dict: 包含笔记内容和提取的概念
        """
        # 分析章节内容
        analysis = self.analyze_content(chapter_data)
        
        # 生成笔记内容
        note_content = self.render_note(chapter_data, analysis)
        
        # 提取概念用于Neo4j
        concepts_data = self.extract_concepts_for_neo4j(analysis)
        
        return {
            "success": True,
            "note_content": note_content,
            "concepts": concepts_data["concepts"],
            "relationships": concepts_data["relationships"],
            "note_file": f"F:\\Obsidian\\{chapter_data['book_title']}\\Ch{chapter_data['chapter']:02d}-{self.sanitize_filename(chapter_data['title'])}.md"
        }
    
    def analyze_content(self, chapter_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析章节内容
        Args:
            chapter_data: 章节数据
        Returns:
            dict: 分析结果
        """
        paragraphs = chapter_data.get('paragraphs', [])
        full_text = '\n'.join(paragraphs)
        
        # 提取核心主题
        core_theme = self.extract_core_theme(full_text, paragraphs)
        
        # 提取要点
        points = self.extract_key_points(paragraphs)
        
        # 提取核心概念
        concepts = self.extract_core_concepts(paragraphs, chapter_data)
        
        # 提取金句
        quotes = self.extract_quotes(paragraphs)
        
        # 生成思考题
        questions = self.generate_questions(concepts, core_theme)
        
        # 生成学习收获
        harvest = self.generate_harvest(concepts, points)
        
        # 提取关键词作为topic
        topic = self.extract_topic(core_theme, concepts)
        
        return {
            "core_theme": core_theme,
            "points": points,
            "concepts": concepts,
            "quotes": quotes,
            "questions": questions,
            "harvest": harvest,
            "topic": topic
        }
    
    def extract_core_theme(self, full_text: str, paragraphs: List[str]) -> str:
        """
        提取核心主题
        """
        # 使用前几个段落概括核心主题
        first_few = '\n'.join(paragraphs[:3])
        
        # 查找包含"本章"、"本章将"、"本章讲解"等关键词的句子
        theme_patterns = [
            r'本章[讲论介](.{10,100})',
            r'This chapter (.{10,100})',
            r'In this chapter (.{10,100})'
        ]
        
        for pattern in theme_patterns:
            match = re.search(pattern, full_text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        # 如果没找到，用第一句话
        if paragraphs:
            first_sentence = re.split(r'[.!?。！？]', paragraphs[0])[0]
            if len(first_sentence) > 10:
                return first_sentence
        
        return "需要根据内容总结核心主题"
    
    def extract_key_points(self, paragraphs: List[str]) -> List[str]:
        """
        提取要点
        """
        points = []
        
        # 查找列表格式的内容
        list_patterns = [
            r'^\s*[-•·]\s+(.+)$',
            r'^\s*\d+[.)、]\s+(.+)$',
            r'^\s*[a-zA-Z][.)]\s+(.+)$'
        ]
        
        for para in paragraphs:
            for pattern in list_patterns:
                match = re.match(pattern, para.strip())
                if match:
                    point = match.group(1).strip()
                    if len(point) > 5 and len(point) < 200:
                        points.append(f"- {point}")
        
        # 如果提取的要点太少，从段落中提取
        if len(points) < 3:
            for para in paragraphs[:5]:
                if len(para) > 20 and len(para) < 150:
                    points.append(f"- {para}")
        
        return points[:5] if len(points) > 5 else points
    
    def extract_core_concepts(self, paragraphs: List[str], chapter_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        提取核心概念
        """
        concepts = []
        full_text = '\n'.join(paragraphs)
        
        # 概念定义模式
        definition_patterns = [
            r'(\w+(?:\s+\w+){0,5})\s*[是指is defined as是指定义]+(.{10,150})',
            r'(\w+(?:\s+\w+){0,5})\s*[:：]\s*(.{10,150})',
            r'(\w+(?:\s+\w+){0,5})\s+(?:是指|is defined as|refers to)\s+(.{10,150})'
        ]
        
        for pattern in definition_patterns:
            for match in re.finditer(pattern, full_text, re.IGNORECASE):
                concept_name = match.group(1).strip()
                definition = match.group(2).strip()
                
                # 评估重要性
                importance = self.assess_importance(concept_name, full_text)
                
                if len(concept_name) > 2 and len(definition) > 10:
                    concepts.append({
                        "name": concept_name,
                        "definition": definition,
                        "importance": importance
                    })
        
        # 去重
        seen = set()
        unique_concepts = []
        for c in concepts:
            if c['name'].lower() not in seen:
                seen.add(c['name'].lower())
                unique_concepts.append(c)
        
        return unique_concepts[:10]  # 限制数量
    
    def assess_importance(self, concept_name: str, full_text: str) -> str:
        """
        评估概念重要性
        """
        concept_lower = concept_name.lower()
        
        # 出现频率
        count = full_text.lower().count(concept_lower)
        
        # 特征判断
        has_quote = ' " ' in full_text or " ' " in full_text
        has_formula = any(c in full_text for c in ['=', '∑', '∫', '√'])
        
        # 综合评分
        score = 0
        if count >= 5:
            score += 2
        if count >= 3:
            score += 1
        if has_quote:
            score += 1
        if has_formula:
            score += 1
        
        if score >= 4:
            return "5star"
        elif score >= 2:
            return "4star"
        else:
            return "3star"
    
    def extract_quotes(self, paragraphs: List[str]) -> List[str]:
        """
        提取金句
        """
        quotes = []
        full_text = '\n'.join(paragraphs)
        
        # 查找引用格式
        quote_pattern = r'["\"]([^\"]{20,200})["\"]'
        
        for match in re.finditer(quote_pattern, full_text):
            quote = match.group(1).strip()
            if len(quote) > 30:
                quotes.append(f"> \"{quote}\"")
        
        return quotes[:3] if len(quotes) > 3 else quotes
    
    def generate_questions(self, concepts: List[Dict], theme: str) -> List[str]:
        """
        生成思考题
        """
        questions = []
        
        # 基于核心主题
        if theme:
            questions.append(f"如何理解\"{theme}\"这一核心思想？")
        
        # 基于概念
        if len(concepts) > 0:
            questions.append(f"{concepts[0]['name']}的定义是什么？它有什么应用场景？")
        
        if len(concepts) > 1:
            questions.append(f"{concepts[0]['name']}和{concepts[1]['name']}之间有什么关系？")
        
        # 默认问题
        if len(questions) < 3:
            questions.extend([
                "本章提到的核心观点对你有什么启发？",
                "如何将本章内容应用到实际工作中？"
            ])
        
        return questions[:3]
    
    def generate_harvest(self, concepts: List[Dict], points: List[str]) -> Dict[str, List[str]]:
        """
        生成学习收获
        """
        return {
            "knowledge": [
                f"掌握了{c['name']}的定义和应用" for c in concepts[:3]
            ],
            "skills": [
                "提升了专业分析能力",
                "增强了逻辑思维能力"
            ],
            "mindset": [
                "建立了系统化的知识框架",
                "培养了批判性思维"
            ]
        }
    
    def extract_topic(self, theme: str, concepts: List[Dict]) -> str:
        """
        提取主题标签
        """
        if theme:
            # 从主题中提取关键词
            words = re.findall(r'\w+', theme)
            if words:
                return words[0]
        
        if concepts:
            return concepts[0]['name'].split()[0]
        
        return "Knowledge"
    
    def render_note(self, chapter_data: Dict[str, Any], analysis: Dict[str, Any]) -> str:
        """
        渲染笔记内容
        """
        # 构建概念段落
        concepts_section = ""
        for idx, concept in enumerate(analysis['concepts'], 1):
            concepts_section += f"""
### 概念 {idx}: {concept['name']}

**定义**: {concept['definition']}

**重要性**: {'⭐⭐⭐⭐⭐' if concept['importance'] == '5star' else '⭐⭐⭐⭐' if concept['importance'] == '4star' else '⭐⭐⭐'}

---

"""
        
        # 构建思维导图
        mindmap_content = ""
        for concept in analysis['concepts'][:5]:
            mindmap_content += f"    {concept['name']}\n"
        
        # 构建金句
        quotes_section = "\n\n".join(analysis['quotes'][:3])
        
        # 构建思考题
        questions_section = "\n".join(
            f"{i+1}. {q}" for i, q in enumerate(analysis['questions'])
        )
        
        # 构建学习收获
        harvest = analysis['harvest']
        knowledge_harvest = "\n".join(f"- ✅ {k}" for k in harvest['knowledge'])
        skill_improvement = "\n".join(f"- 📊 {s}" for s in harvest['skills'])
        mindset_change = "\n".join(f"- 🔄 {m}" for m in harvest['mindset'])
        
        # 构建要点
        points_section = "\n".join(analysis['points'][:5]) if analysis['points'] else "- 需要根据内容提取要点"
        
        # 渲染模板
        note = self.template.format(
            book_title=chapter_data['book_title'],
            chapter=chapter_data['chapter'],
            title=chapter_data['title'],
            book_version=chapter_data.get('book_version', 'Unknown'),
            author=chapter_data.get('author', 'Unknown'),
            learning_date=datetime.now().strftime("%Y-%m-%d"),
            tag=analysis['topic'],
            topic=analysis['topic'],
            core_theme=analysis['core_theme'],
            points=points_section,
            concepts_section=concepts_section,
            mindmap_content=mindmap_content,
            quotes=quotes_section,
            questions=questions_section,
            knowledge_harvest=knowledge_harvest,
            skill_improvement=skill_improvement,
            mindset_change=mindset_change,
            total_chapters=chapter_data.get('total_chapters', 'Unknown'),
            next_chapter=chapter_data['chapter'] + 1,
            next_title="待定"
        )
        
        return note
    
    def extract_concepts_for_neo4j(self, analysis: Dict[str, Any], chapter: int = 1, book_title: str = "") -> Dict[str, Any]:
        """
        提取概念和关系用于Neo4j
        """
        concepts = []
        relationships = []
        
        # 构建概念节点
        for concept in analysis['concepts']:
            concepts.append({
                "name": concept['name'],
                "category": f"{book_title}/Core Concepts",
                "chapter": chapter,
                "description": concept['definition'],
                "importance": concept['importance']
            })
        
        # 构建关系（基于概念顺序）
        if len(concepts) >= 2:
            for i in range(len(concepts) - 1):
                relationships.append({
                    "from": concepts[i]['name'],
                    "to": concepts[i+1]['name'],
                    "type": "RELATED_TO",
                    "description": f"{concepts[i]['name']} related to {concepts[i+1]['name']}"
                })
        
        return {
            "concepts": concepts,
            "relationships": relationships
        }
    
    def sanitize_filename(self, filename: str) -> str:
        """
        清理文件名，移除不合法字符
        """
        # 移除或替换不合法字符
        illegal_chars = '<>:"/\\|?*'
        for char in illegal_chars:
            filename = filename.replace(char, '_')
        
        # 限制长度
        if len(filename) > 50:
            filename = filename[:50]
        
        return filename
    
    def generate_full_book_summary(self, summary_data: Dict[str, Any]) -> str:
        """
        生成全书总结报告
        """
        template = """# 🎉《{book_title}》全书学习完成报告

> **书籍**: {book_title} ({book_version})
> **作者**: {author}
> **学习完成日期**: {completion_date}
> **学习方式**: 逐章笔记 + Neo4j 知识图谱

---

## ✅ 学习统计

| 指标 | 完成 |
|------|------|
| **学习章节** | {completed_chapters} 章 ✅ |
| **Obsidian 笔记** | {note_count} 个文件 ✅ |
| **Neo4j 概念** | {total_concepts} 个概念 ✅ |
| **Neo4j 关系** | {total_relationships} 个关系 ✅ |
| **总字数** | {total_kb}KB 笔记 ✅ |
| **学习时长** | ~{duration_hours} 小时 ✅ |

---

## 💡 全书核心思想总结

{core_ideas}

---

## 🎯 实践应用指南

### 行动清单
{action_items}

---

_学习报告由梅梅整理 · {completion_date}_ ✨
"""
        
        # 这里简化处理，实际应该根据汇总数据生成
        return template.format(
            book_title=summary_data.get('book_title', 'Unknown'),
            book_version=summary_data.get('book_version', 'Unknown'),
            author=summary_data.get('author', 'Unknown'),
            completion_date=datetime.now().strftime("%Y-%m-%d"),
            completed_chapters=summary_data.get('completed_chapters', 0),
            note_count=summary_data.get('note_count', 0),
            total_concepts=summary_data.get('total_concepts', 0),
            total_relationships=summary_data.get('total_relationships', 0),
            total_kb=summary_data.get('total_kb', 0),
            duration_hours=summary_data.get('duration_hours', 0),
            core_ideas="根据学习内容总结核心思想",
            action_items="- [ ] 应用1\n- [ ] 应用2\n- [ ] 应用3"
        )


# 使用示例
if __name__ == "__main__":
    generator = NoteGenerator()
    
    # 示例章节数据
    chapter_data = {
        "book_title": "Security Analysis",
        "chapter": 1,
        "title": "Security Analysis: Scope and Limitations",
        "book_version": "6th Edition",
        "author": "Benjamin Graham",
        "total_chapters": 40,
        "paragraphs": [
            "Security analysis is the study of the value of securities.",
            "The intrinsic value is a key concept in security analysis.",
            "This chapter will discuss the scope and limitations of security analysis."
        ]
    }
    
    result = generator.generate_note(chapter_data)
    if result['success']:
        print("笔记生成成功!")
        print(f"提取了 {len(result['concepts'])} 个概念")
        print(f"构建了 {len(result['relationships'])} 个关系")
        print(f"笔记文件: {result['note_file']}")
    else:
        print("笔记生成失败!")
