#!/usr/bin/env python3
"""
AI 写作模块
调用 Claude 或其他 AI 模型生成真实内容
"""

import os
from typing import Dict, List, Optional


class AIWriter:
    """AI 写作器"""
    
    def __init__(self, model: str = "claude"):
        """
        初始化 AI 写作器
        
        Args:
            model: 使用的模型，可选 'claude', 'gpt', 'local'
        """
        self.model = model
        self.api_key = self._get_api_key()
    
    def _get_api_key(self) -> Optional[str]:
        """获取 API Key"""
        if self.model == "claude":
            return os.getenv('ANTHROPIC_API_KEY')
        elif self.model == "gpt":
            return os.getenv('OPENAI_API_KEY')
        return None
    
    def write_section(self, title: str, word_count: int, 
                      key_points: List[str], context: str,
                      search_results: Optional[List[Dict]] = None) -> str:
        """
        写作单个章节
        
        Args:
            title: 章节标题
            word_count: 目标字数
            key_points: 关键点
            context: 上下文信息
            search_results: 搜索结果（用于事实支撑）
            
        Returns:
            生成的章节内容
        """
        # 构建提示词
        prompt = self._build_prompt(
            title=title,
            word_count=word_count,
            key_points=key_points,
            context=context,
            search_results=search_results
        )
        
        # 这里应该调用实际的 AI API
        # 目前返回模拟内容
        content = self._generate_mock_content(title, word_count, key_points)
        
        return content
    
    def _build_prompt(self, title: str, word_count: int,
                     key_points: List[str], context: str,
                     search_results: Optional[List[Dict]]) -> str:
        """构建写作提示词"""
        
        prompt = f"""请为公众号文章写作以下章节：

【章节标题】{title}
【目标字数】{word_count}字
【文章主题】{context}

【关键要点】
"""
        for i, point in enumerate(key_points, 1):
            prompt += f"{i}. {point}\n"
        
        if search_results:
            prompt += "\n【参考资料】\n"
            for i, result in enumerate(search_results[:3], 1):
                prompt += f"{i}. {result.get('title', '')}: {result.get('content', '')[:100]}...\n"
        
        prompt += f"""
【写作要求】
1. 语言流畅自然，适合公众号阅读
2. 段落分明，每段不超过3-4句话
3. 适当使用emoji增加可读性
4. 关键信息用**加粗**强调
5. 包含具体例子或数据支撑
6. 严格控制在{word_count}字左右
7. 直接输出内容，不要包含章节标题

请开始写作："""
        
        return prompt
    
    def _generate_mock_content(self, title: str, word_count: int, 
                              key_points: List[str]) -> str:
        """生成模拟内容（实际应调用 AI API）"""
        
        # 模拟生成内容
        lines = []
        
        # 开头
        lines.append(f"在探讨{title}之前，我们需要先理解其背景和意义。")
        
        # 展开关键点
        for point in key_points[:3]:
            lines.append(f"\n首先，关于{point}，这是一个值得深入探讨的话题。")
            lines.append(f"从实际角度来看，{point}对于理解整个主题至关重要。")
            lines.append(f"我们可以发现，{point}在当前环境下具有特殊的意义。")
        
        # 举例说明
        lines.append(f"\n举个例子来说，当我们观察实际应用场景时，会发现{title}的影响是深远的。")
        lines.append("这不仅体现在理论层面，更在实践中得到了验证。")
        
        # 总结
        lines.append(f"\n综上所述，{title}是一个多维度、多层次的话题。")
        lines.append("希望以上内容能够帮助你更好地理解这个主题。")
        
        content = "\n".join(lines)
        
        # 调整字数（简单截断或扩展）
        current_length = len(content)
        if current_length < word_count:
            # 补充内容
            while len(content) < word_count:
                content += f"\n\n进一步来说，{title}还有更多的层面值得探索。"
        elif current_length > word_count * 1.2:
            # 截断
            content = content[:int(word_count * 1.1)] + "..."
        
        return content
    
    def write_full_article(self, topic: str, outline: Dict,
                          search_summary: Optional[Dict] = None) -> List[Dict]:
        """
        写作完整文章
        
        Args:
            topic: 文章主题
            outline: 文章大纲
            search_summary: 搜索总结
            
        Returns:
            章节内容列表
        """
        print(f"\n✍️  开始写作文章: {topic}")
        print("=" * 60)
        
        sections = []
        total_sections = len(outline.get('sections', []))
        
        for i, section in enumerate(outline['sections'], 1):
            print(f"\n[{i}/{total_sections}] 写作: {section['title']}")
            print(f"    目标字数: {section['word_count']}字")
            
            # 写作章节
            content = self.write_section(
                title=section['title'],
                word_count=section['word_count'],
                key_points=section.get('key_points', []),
                context=topic,
                search_results=search_summary.get('results') if search_summary else None
            )
            
            sections.append({
                'title': section['title'],
                'content': content
            })
            
            actual_length = len(content.replace(' ', '').replace('\n', ''))
            print(f"    ✓ 完成 ({actual_length}字)")
        
        print("\n" + "=" * 60)
        print("✅ 文章写作完成!")
        
        return sections


if __name__ == "__main__":
    # 测试
    writer = AIWriter()
    
    # 测试单章节写作
    content = writer.write_section(
        title="人工智能的发展趋势",
        word_count=300,
        key_points=["技术进步", "应用拓展", "未来展望"],
        context="人工智能发展趋势分析"
    )
    
    print("\n生成的内容:")
    print(content[:500] + "...")
