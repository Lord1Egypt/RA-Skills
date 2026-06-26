"""
导出模块
支持导出为 Markdown、TXT、JSON 等格式
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict


class ArticleExporter:
    """文章导出器"""
    
    @staticmethod
    def export(article_data: Dict, output_path: str, format: str = 'markdown') -> str:
        """
        导出文章
        
        Args:
            article_data: 文章数据
            output_path: 输出路径
            format: 导出格式 (markdown/txt/json/html)
        
        Returns:
            输出文件路径
        """
        if format == 'markdown':
            return ArticleExporter._export_markdown(article_data, output_path)
        elif format == 'txt':
            return ArticleExporter._export_txt(article_data, output_path)
        elif format == 'json':
            return ArticleExporter._export_json(article_data, output_path)
        elif format == 'html':
            return ArticleExporter._export_html(article_data, output_path)
        else:
            raise ValueError(f"不支持的格式：{format}")
    
    @staticmethod
    def _export_markdown(data: Dict, output_path: str) -> str:
        """导出为 Markdown"""
        content = f"# {data.get('title', '无标题')}\n\n"
        
        if data.get('platform'):
            content += f"**平台**: {data['platform']}  \n"
        if data.get('author'):
            content += f"**作者**: {data['author']}  \n"
        if data.get('publish_time'):
            content += f"**发布时间**: {data['publish_time']}  \n"
        if data.get('word_count'):
            content += f"**字数**: {data['word_count']} 字  \n"
        if data.get('reading_time'):
            content += f"**阅读时间**: 约{data['reading_time']}分钟  \n"
        
        content += f"\n**原文链接**: {data.get('url', '')}  \n"
        content += f"\n---\n\n"
        
        # AI 总结
        if data.get('ai_summary') and data['ai_summary'].get('success'):
            summary = data['ai_summary']
            content += "## 📝 AI 总结\n\n"
            content += f"**概述**: {summary.get('overview', '')}\n\n"
            
            key_points = summary.get('key_points', [])
            if key_points:
                content += "**关键点**:\n\n"
                for i, point in enumerate(key_points, 1):
                    content += f"{i}. {point}\n"
                content += "\n"
            
            value = summary.get('value_assessment', {})
            if value:
                content += "**文章评估**:\n\n"
                content += f"- 可信度：{value.get('credibility', '未知')}\n"
                content += f"- 参考价值：{value.get('reference_value', '未知')}\n"
                if value.get('recommendation'):
                    content += f"- 建议：{value['recommendation']}\n"
                content += "\n"
        
        content += "## 📄 正文\n\n"
        content += data.get('content', '')
        
        # 写入文件
        output_file = Path(output_path)
        output_file.write_text(content, encoding='utf-8')
        
        return str(output_file)
    
    @staticmethod
    def _export_txt(data: Dict, output_path: str) -> str:
        """导出为 TXT"""
        content = f"{data.get('title', '无标题')}\n"
        content += "=" * 60 + "\n\n"
        
        if data.get('platform'):
            content += f"平台：{data['platform']}\n"
        if data.get('author'):
            content += f"作者：{data['author']}\n"
        if data.get('publish_time'):
            content += f"发布时间：{data['publish_time']}\n"
        if data.get('word_count'):
            content += f"字数：{data['word_count']}字\n"
        if data.get('reading_time'):
            content += f"阅读时间：约{data['reading_time']}分钟\n"
        
        content += f"\n原文链接：{data.get('url', '')}\n"
        content += "\n" + "=" * 60 + "\n\n"
        
        # AI 总结
        if data.get('ai_summary') and data['ai_summary'].get('success'):
            summary = data['ai_summary']
            content += "【AI 总结】\n\n"
            content += f"概述：{summary.get('overview', '')}\n\n"
            
            key_points = summary.get('key_points', [])
            if key_points:
                content += "关键点:\n"
                for i, point in enumerate(key_points, 1):
                    content += f"{i}. {point}\n"
                content += "\n"
        
        content += "\n【正文】\n\n"
        content += data.get('content', '')
        
        # 写入文件
        output_file = Path(output_path)
        output_file.write_text(content, encoding='utf-8')
        
        return str(output_file)
    
    @staticmethod
    def _export_json(data: Dict, output_path: str) -> str:
        """导出为 JSON"""
        output_file = Path(output_path)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return str(output_file)
    
    @staticmethod
    def _export_html(data: Dict, output_path: str) -> str:
        """导出为 HTML"""
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data.get('title', '无标题')}</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #333; }}
        .meta {{ color: #666; font-size: 0.9em; }}
        .summary {{ background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .content {{ line-height: 1.8; }}
    </style>
</head>
<body>
    <h1>{data.get('title', '无标题')}</h1>
    <div class="meta">
        <p>平台：{data.get('platform', '未知')}</p>
        <p>作者：{data.get('author', '未知')}</p>
        <p>发布时间：{data.get('publish_time', '未知')}</p>
        <p>字数：{data.get('word_count', 0)}字</p>
        <p>阅读时间：约{data.get('reading_time', 1)}分钟</p>
        <p>原文链接：<a href="{data.get('url', '')}" target="_blank">{data.get('url', '')}</a></p>
    </div>
"""
        
        # AI 总结
        if data.get('ai_summary') and data['ai_summary'].get('success'):
            summary = data['ai_summary']
            html += """
    <div class="summary">
        <h2>📝 AI 总结</h2>
        <p><strong>概述:</strong> """ + summary.get('overview', '') + """</p>
"""
            key_points = summary.get('key_points', [])
            if key_points:
                html += "<p><strong>关键点:</strong></p><ol>"
                for point in key_points:
                    html += f"<li>{point}</li>"
                html += "</ol>"
            
            html += """
    </div>
"""
        
        html += f"""
    <div class="content">
        <h2>📄 正文</h2>
        {data.get('content', '').replace(chr(10), '<br>')}
    </div>
</body>
</html>
"""
        
        output_file = Path(output_path)
        output_file.write_text(html, encoding='utf-8')
        
        return str(output_file)


def main():
    """测试导出"""
    test_data = {
        'title': '测试文章',
        'platform': '今日头条',
        'author': '测试作者',
        'publish_time': '2026-05-03',
        'word_count': 1000,
        'reading_time': 3,
        'url': 'https://example.com/article/1',
        'content': '这是测试文章内容...' * 50,
        'ai_summary': {
            'success': True,
            'overview': '这是一篇测试文章的概述',
            'key_points': ['关键点 1', '关键点 2', '关键点 3'],
            'value_assessment': {
                'credibility': '较高',
                'reference_value': '中等',
                'recommendation': '值得阅读'
            }
        }
    }
    
    # 测试导出为 Markdown
    output_path = 'test_export.md'
    result_path = ArticleExporter.export(test_data, output_path, 'markdown')
    print(f"导出 Markdown: {result_path}")
    
    # 测试导出为 TXT
    output_path = 'test_export.txt'
    result_path = ArticleExporter.export(test_data, output_path, 'txt')
    print(f"导出 TXT: {result_path}")
    
    # 测试导出为 JSON
    output_path = 'test_export.json'
    result_path = ArticleExporter.export(test_data, output_path, 'json')
    print(f"导出 JSON: {result_path}")


if __name__ == '__main__':
    main()
