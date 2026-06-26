#!/usr/bin/env python3
"""
微信公众号文章写作主流程
支持自动写作和指定主题两种模式
"""

import os
import sys
import json
import argparse
from typing import Dict, List

# 导入自定义模块
sys.path.insert(0, os.path.dirname(__file__))
from outline_generator import OutlineGenerator, quick_outline
from html_writer import HTMLWriter, write_html_article
from content_validator import ContentValidator, verify_article_facts


class ArticleWriter:
    """文章写作主控类"""
    
    def __init__(self):
        self.outline_gen = OutlineGenerator()
        self.html_writer = HTMLWriter()
        self.validator = ContentValidator()
    
    def auto_write(self, topic: str, word_count: int = 1500) -> Dict:
        """
        自动写作模式
        
        Args:
            topic: 文章主题
            word_count: 目标字数
            
        Returns:
            包含 title, html_content, outline 的字典
        """
        print(f"\n🚀 开始自动写作: {topic}")
        print("=" * 60)
        
        # 1. 分析话题类型
        print("\n[1/5] 分析话题类型...")
        article_type, confidence = self.outline_gen.analyze_topic(topic)
        type_name = self.outline_gen.TEMPLATES[article_type]['name']
        print(f"   检测到类型: {type_name} (置信度: {confidence:.0%})")
        
        # 2. 生成搜索查询
        print("\n[2/5] 生成搜索查询...")
        queries = self.validator.generate_search_queries(topic, article_type)
        print(f"   搜索关键词: {', '.join(queries[:3])}")
        print("   ⚠️  提示: 实际搜索功能需要接入搜索 API")
        
        # 3. 生成大纲
        print("\n[3/5] 生成文章大纲...")
        outline = self.outline_gen.generate_outline(topic, word_count, article_type)
        print(f"   文章结构 ({outline['word_count']}字):")
        for i, section in enumerate(outline['sections'], 1):
            print(f"   {i}. {section['title']} ({section['word_count']}字)")
        
        # 4. 自动写作（模拟）
        print("\n[4/5] 自动写作内容...")
        print("   正在根据大纲生成内容...")
        
        # 构建章节内容
        sections = []
        for section in outline['sections']:
            # 这里应该调用 AI 写作，现在用占位内容
            content = self._generate_placeholder_content(section)
            sections.append({
                'title': section['title'],
                'content': content
            })
            print(f"   ✓ {section['title']}")
        
        # 5. 转换为 HTML
        print("\n[5/5] 转换为 HTML 排版...")
        html_content = self.html_writer.write_article(topic, sections)
        html_content = self.html_writer.add_footer(html_content, "小爪制作，需要审核")
        print("   ✓ HTML 生成完成")
        
        # 验证内容
        print("\n[验证] 检查内容准确性...")
        is_valid, warnings = verify_article_facts('\n'.join([s['content'] for s in sections]))
        if warnings:
            print(f"   ⚠️  发现 {len(warnings)} 处需要核实:")
            for w in warnings[:3]:
                print(f"      - {w}")
        else:
            print("   ✓ 未发现明显问题")
        
        print("\n" + "=" * 60)
        print("✅ 自动写作完成!")
        
        return {
            'title': topic,
            'html_content': html_content,
            'outline': outline,
            'article_type': article_type,
            'warnings': warnings
        }
    
    def guided_write(self, topic: str, word_count: int = 1500, 
                     style: str = None, requirements: str = None) -> Dict:
        """
        指定主题写作模式（半自动，可交互）
        
        Args:
            topic: 文章主题
            word_count: 目标字数
            style: 指定风格
            requirements: 特殊要求
            
        Returns:
            包含 title, html_content, outline 的字典
        """
        print(f"\n🎯 开始指定主题写作: {topic}")
        print("=" * 60)
        
        # 1. 确认需求
        print("\n[1/6] 确认写作需求...")
        if style:
            print(f"   指定风格: {style}")
        if requirements:
            print(f"   特殊要求: {requirements}")
        print(f"   目标字数: {word_count}字")
        
        # 2. 生成大纲（用户可修改）
        print("\n[2/6] 生成文章大纲...")
        outline = self.outline_gen.generate_outline(topic, word_count, style)
        
        print(f"\n📋 文章大纲 ({outline['type_name']}):")
        outline_text = self.outline_gen.outline_to_text(outline)
        print(outline_text)
        
        print("\n💡 提示: 在实际交互中，这里会询问用户是否修改大纲")
        
        # 3. 分段写作
        print("\n[3/6] 分段写作...")
        sections = []
        
        for i, section in enumerate(outline['sections'], 1):
            print(f"\n   写作第 {i} 部分: {section['title']}")
            print(f"   目标字数: {section['word_count']}字")
            print(f"   关键点: {', '.join(section['key_points'][:2])}")
            
            # 这里应该调用 AI 写作
            content = self._generate_placeholder_content(section)
            sections.append({
                'title': section['title'],
                'content': content
            })
            
            print(f"   ✓ 完成 ({len(content)}字)")
            print("   💡 提示: 实际交互中，这里会展示内容并询问是否修改")
        
        # 4. 转换为 HTML
        print("\n[4/6] 转换为 HTML 排版...")
        html_content = self.html_writer.write_article(topic, sections)
        
        # 5. 内容验证
        print("\n[5/6] 验证内容准确性...")
        is_valid, warnings = verify_article_facts('\n'.join([s['content'] for s in sections]))
        if warnings:
            print(f"   ⚠️  发现 {len(warnings)} 处需要核实")
        else:
            print("   ✓ 内容检查通过")
        
        # 6. 添加页脚
        print("\n[6/6] 添加页脚...")
        html_content = self.html_writer.add_footer(html_content, "小爪制作，需要审核")
        
        print("\n" + "=" * 60)
        print("✅ 指定主题写作完成!")
        
        return {
            'title': topic,
            'html_content': html_content,
            'outline': outline,
            'article_type': outline['type'],
            'warnings': warnings
        }
    
    def _generate_placeholder_content(self, section: Dict) -> str:
        """生成占位内容（实际应调用 AI 写作）"""
        title = section['title']
        word_count = section['word_count']
        key_points = section.get('key_points', [])
        
        # 简单的占位文本
        lines = [f"这是【{title}】部分的内容。"]
        
        if key_points:
            lines.append("\n本节要点:")
            for point in key_points:
                lines.append(f"- {point}")
        
        lines.append(f"\n（此处应写作约 {word_count} 字的详细内容）")
        lines.append("\n在实际使用中，这里会调用 AI 模型根据大纲生成具体内容。")
        
        return '\n'.join(lines)
    
    def save_article(self, result: Dict, output_dir: str = "_drafts") -> str:
        """保存文章到文件"""
        # 确保目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 生成文件名
        from datetime import datetime
        date_str = datetime.now().strftime("%Y-%m-%d")
        safe_title = result['title'][:20].replace(' ', '_').replace('/', '_')
        filename = f"{date_str}-{safe_title}.html"
        filepath = os.path.join(output_dir, filename)
        
        # 保存 HTML
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(result['html_content'])
        
        # 同时保存大纲 JSON
        outline_filename = f"{date_str}-{safe_title}.json"
        outline_filepath = os.path.join(output_dir, outline_filename)
        with open(outline_filepath, 'w', encoding='utf-8') as f:
            json.dump(result['outline'], f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 文章已保存:")
        print(f"   HTML: {filepath}")
        print(f"   大纲: {outline_filepath}")
        
        return filepath


def main():
    parser = argparse.ArgumentParser(description='微信公众号文章写作工具')
    parser.add_argument('topic', nargs='?', help='文章主题')
    parser.add_argument('--mode', '-m', choices=['auto', 'guided'], default='auto',
                        help='写作模式: auto(自动) 或 guided(指定主题)')
    parser.add_argument('--words', '-w', type=int, default=1500,
                        help='目标字数 (默认1500)')
    parser.add_argument('--style', '-s', help='指定文章风格')
    parser.add_argument('--output', '-o', default='_drafts',
                        help='输出目录')
    parser.add_argument('--no-save', action='store_true',
                        help='不保存文件，仅输出到控制台')
    
    args = parser.parse_args()
    
    if not args.topic:
        print("使用方法:")
        print("  python3 write_article.py '文章主题'")
        print("  python3 write_article.py '文章主题' --mode guided --words 2000")
        print("\n模式说明:")
        print("  auto    - 全自动写作，适合快速出稿")
        print("  guided  - 指定主题写作，可精细控制")
        return
    
    # 创建写作器
    writer = ArticleWriter()
    
    # 根据模式写作
    if args.mode == 'auto':
        result = writer.auto_write(args.topic, args.words)
    else:
        result = writer.guided_write(args.topic, args.words, args.style)
    
    # 保存文件
    if not args.no_save:
        filepath = writer.save_article(result, args.output)
        print(f"\n📝 下一步:")
        print(f"   推送草稿: python3 push_draft.py --file {filepath} --title \"{result['title']}\"")


if __name__ == "__main__":
    main()
