#!/usr/bin/env python3
"""
思维导图生成器
将文本内容转换为思维导图格式（Mermaid / Markdown / XMind）
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# 配置
SKILL_DIR = Path(__file__).parent.parent
OUTPUT_DIR = SKILL_DIR / "data" / "mindmaps"


class MindMapGenerator:
    """思维导图生成器"""
    
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.root = None
    
    def extract_structure(self, content: str) -> Dict:
        """
        从文本中提取层次结构
        
        Args:
            content: 输入文本
        
        Returns:
            层次结构字典
        """
        lines = content.strip().split('\n')
        structure = {
            "title": "",
            "children": []
        }
        
        current_level = 0
        stack = [(structure, -1)]
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 检测标题层级
            level = 0
            if line.startswith('#'):
                level = line.count('#')
                text = line.lstrip('#').strip()
            elif re.match(r'^\d+[\.\、]', line):
                level = 1
                text = re.sub(r'^\d+[\.\、]\s*', '', line)
            elif re.match(r'^[\-\*\+]\s*', line):
                level = 2
                text = re.sub(r'^[\-\*\+]\s*', '', line)
            elif re.match(r'^\([一二三四五六七八九十]\)', line):
                level = 1
                text = re.sub(r'^\([一二三四五六七八九十]\)\s*', '', line)
            else:
                level = 2
                text = line
            
            # 第一行作为根节点
            if not structure["title"]:
                structure["title"] = text
                continue
            
            # 创建节点
            node = {
                "title": text,
                "children": []
            }
            
            # 找到父节点
            while stack and stack[-1][1] >= level:
                stack.pop()
            
            if stack:
                parent, _ = stack[-1]
                parent["children"].append(node)
            
            stack.append((node, level))
        
        return structure
    
    def to_mermaid(self, structure: Dict, direction: str = "TB") -> str:
        """
        转换为 Mermaid 思维导图格式
        
        Args:
            structure: 层次结构
            direction: 方向 (TB/LR)
        
        Returns:
            Mermaid 代码
        """
        lines = [f"mindmap"]
        lines.append(f"  root(({structure['title']}))")
        
        def add_nodes(node: Dict, indent: int = 2):
            for child in node.get("children", []):
                # 转义特殊字符
                title = child["title"].replace('"', "'").replace('(', '').replace(')', '')
                lines.append(f"  {'  ' * indent}{title}")
                if child.get("children"):
                    add_nodes(child, indent + 1)
        
        add_nodes(structure)
        
        return '\n'.join(lines)
    
    def to_markdown(self, structure: Dict) -> str:
        """
        转换为 Markdown 思维导图格式
        
        Args:
            structure: 层次结构
        
        Returns:
            Markdown 文本
        """
        lines = [f"# 🧠 {structure['title']}", ""]
        lines.append("```mermaid")
        lines.append(self.to_mermaid(structure))
        lines.append("```")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## 📋 详细内容")
        lines.append("")
        
        def add_markdown(node: Dict, level: int = 2):
            for i, child in enumerate(node.get("children", []), 1):
                prefix = "#" * min(level, 4)
                lines.append(f"{prefix} {i}. {child['title']}")
                
                if child.get("children"):
                    for j, sub in enumerate(child["children"], 1):
                        lines.append(f"  - {sub['title']}")
                
                lines.append("")
        
        add_markdown(structure)
        
        return '\n'.join(lines)
    
    def to_markmap(self, structure: Dict) -> str:
        """
        转换为 Markmap 格式（可直接在浏览器渲染）
        
        Args:
            structure: 层次结构
        
        Returns:
            Markmap HTML
        """
        def build_markdown_tree(node: Dict, level: int = 0) -> str:
            indent = "  " * level
            lines = [f"{indent}- {node['title']}"]
            for child in node.get("children", []):
                lines.append(build_markdown_tree(child, level + 1))
            return '\n'.join(lines)
        
        markdown_content = build_markdown_tree(structure)
        
        html = f'''<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>{structure['title']} - 思维导图</title>
  <script src="https://cdn.jsdelivr.net/npm/markmap-autoloader"></script>
  <style>
    body {{
      margin: 0;
      padding: 20px;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }}
    .markmap {{
      width: 100%;
      height: 80vh;
    }}
  </style>
</head>
<body>
  <h1>🧠 {structure['title']}</h1>
  <div class="markmap">
    <script type="text/template">
{markdown_content}
    </script>
  </div>
</body>
</html>'''
        
        return html
    
    def to_plantuml(self, structure: Dict) -> str:
        """
        转换为 PlantUML 思维导图格式
        
        Args:
            structure: 层次结构
        
        Returns:
            PlantUML 代码
        """
        lines = ["@startmindmap"]
        lines.append(f"* {structure['title']}")
        
        def add_nodes(node: Dict, level: int = 1):
            for child in node.get("children", []):
                prefix = "*" * (level + 1)
                lines.append(f"{prefix} {child['title']}")
                if child.get("children"):
                    add_nodes(child, level + 1)
        
        add_nodes(structure)
        
        lines.append("@endmindmap")
        
        return '\n'.join(lines)
    
    def generate_from_keywords(self, keywords: List[str], title: str = "主题") -> Dict:
        """
        从关键词列表生成思维导图结构
        
        Args:
            keywords: 关键词列表
            title: 根节点标题
        
        Returns:
            层次结构
        """
        structure = {
            "title": title,
            "children": []
        }
        
        # 按 3-5 个一组分组
        group_size = 4
        groups = [keywords[i:i+group_size] for i in range(0, len(keywords), group_size)]
        
        for i, group in enumerate(groups, 1):
            branch = {
                "title": f"分支 {i}",
                "children": [{"title": kw, "children": []} for kw in group]
            }
            structure["children"].append(branch)
        
        return structure


def generate_mindmap(
    content: str,
    title: Optional[str] = None,
    format: str = "mermaid",
    output_file: Optional[str] = None
) -> Tuple[str, str]:
    """
    生成思维导图
    
    Args:
        content: 输入内容
        title: 标题（可选）
        format: 输出格式 (mermaid/markdown/markmap/plantuml)
        output_file: 输出文件名（可选）
    
    Returns:
        (生成的内容, 文件路径)
    """
    generator = MindMapGenerator()
    structure = generator.extract_structure(content)
    
    # 如果有指定标题，覆盖提取的标题
    if title:
        structure["title"] = title
    
    # 根据格式生成
    if format == "mermaid":
        result = generator.to_mermaid(structure)
        ext = ".mmd"
    elif format == "markdown":
        result = generator.to_markdown(structure)
        ext = ".md"
    elif format == "markmap":
        result = generator.to_markmap(structure)
        ext = ".html"
    elif format == "plantuml":
        result = generator.to_plantuml(structure)
        ext = ".puml"
    else:
        result = generator.to_mermaid(structure)
        ext = ".mmd"
    
    # 保存文件
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    if not output_file:
        output_file = f"mindmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}{ext}"
    
    filepath = OUTPUT_DIR / output_file
    filepath.write_text(result, encoding='utf-8')
    
    return result, str(filepath)


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="思维导图生成器")
    parser.add_argument("content", nargs="?", help="输入内容")
    parser.add_argument("--file", "-f", help="从文件读取内容")
    parser.add_argument("--title", "-t", help="设置标题")
    parser.add_argument("--format", "-F", 
                       choices=["mermaid", "markdown", "markmap", "plantuml"],
                       default="markdown",
                       help="输出格式")
    parser.add_argument("--keywords", "-k", help="从逗号分隔的关键词生成")
    
    args = parser.parse_args()
    
    # 获取内容
    if args.file:
        content = Path(args.file).read_text(encoding='utf-8')
    elif args.keywords:
        keywords = [kw.strip() for kw in args.keywords.split(',')]
        generator = MindMapGenerator()
        structure = generator.generate_from_keywords(keywords, args.title or "主题")
        content = ""  # 将由 generate_from_keywords 处理
        
        # 直接生成
        if args.format == "mermaid":
            result = generator.to_mermaid(structure)
        elif args.format == "markdown":
            result = generator.to_markdown(structure)
        elif args.format == "markmap":
            result = generator.to_markmap(structure)
        else:
            result = generator.to_plantuml(structure)
        
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        ext = ".html" if args.format == "markmap" else (".md" if args.format == "markdown" else ".mmd")
        filepath = OUTPUT_DIR / f"mindmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}{ext}"
        filepath.write_text(result, encoding='utf-8')
        
        print(f"✅ 思维导图已生成")
        print(f"📄 文件路径: {filepath}")
        print("\n" + "="*50 + "\n")
        print(result)
        return
    elif args.content:
        content = args.content
    else:
        print("用法: python mindmap.py <内容>")
        print("      python mindmap.py --file <文件路径>")
        print("      python mindmap.py --keywords '关键词1,关键词2,关键词3'")
        sys.exit(1)
    
    # 生成思维导图
    result, filepath = generate_mindmap(content, args.title, args.format)
    
    print(f"✅ 思维导图已生成")
    print(f"📄 文件路径: {filepath}")
    print(f"📊 格式: {args.format}")
    print("\n" + "="*50 + "\n")
    print(result)


if __name__ == "__main__":
    main()