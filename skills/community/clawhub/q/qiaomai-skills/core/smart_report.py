"""
荞麦饼 Skills - 智能报告系统
多格式智能生成 + 自适应模板
"""

import json
import re
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
import html


class ReportFormat(Enum):
    """报告格式"""
    MARKDOWN = "markdown"
    PDF = "pdf"
    HTML = "html"
    JSON = "json"
    WORD = "word"
    EXCEL = "excel"


class ReportType(Enum):
    """报告类型"""
    RESEARCH = "research"           # 研究报告
    ANALYSIS = "analysis"           # 分析报告
    SUMMARY = "summary"             # 总结报告
    COMPARISON = "comparison"       # 对比报告
    TECHNICAL = "technical"         # 技术文档
    BUSINESS = "business"           # 商业报告
    ACADEMIC = "academic"           # 学术论文
    NEWS = "news"                   # 新闻稿


@dataclass
class ReportSection:
    """报告章节"""
    title: str
    content: str
    level: int = 1  # 标题级别
    metadata: Dict = field(default_factory=dict)


@dataclass
class ReportData:
    """报告数据"""
    title: str
    type: ReportType
    sections: List[ReportSection] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


class TemplateLibrary:
    """模板库"""
    
    TEMPLATES = {
        ReportType.RESEARCH: {
            "structure": [
                {"title": "研究背景", "level": 1},
                {"title": "研究方法", "level": 1},
                {"title": "研究发现", "level": 1},
                {"title": "结论与建议", "level": 1},
            ],
            "style": "academic",
            "citation": True
        },
        ReportType.ANALYSIS: {
            "structure": [
                {"title": "分析目标", "level": 1},
                {"title": "数据来源", "level": 1},
                {"title": "分析过程", "level": 1},
                {"title": "关键发现", "level": 1},
                {"title": "建议措施", "level": 1},
            ],
            "style": "professional",
            "citation": False
        },
        ReportType.SUMMARY: {
            "structure": [
                {"title": "核心要点", "level": 1},
                {"title": "详细内容", "level": 1},
                {"title": "行动建议", "level": 1},
            ],
            "style": "concise",
            "citation": False
        },
        ReportType.COMPARISON: {
            "structure": [
                {"title": "对比对象", "level": 1},
                {"title": "对比维度", "level": 1},
                {"title": "详细对比", "level": 1},
                {"title": "结论", "level": 1},
            ],
            "style": "structured",
            "citation": False
        },
        ReportType.TECHNICAL: {
            "structure": [
                {"title": "概述", "level": 1},
                {"title": "技术细节", "level": 1},
                {"title": "实现方案", "level": 1},
                {"title": "性能评估", "level": 1},
                {"title": "总结", "level": 1},
            ],
            "style": "technical",
            "citation": True
        },
        ReportType.BUSINESS: {
            "structure": [
                {"title": "执行摘要", "level": 1},
                {"title": "市场分析", "level": 1},
                {"title": "竞争格局", "level": 1},
                {"title": "战略建议", "level": 1},
            ],
            "style": "business",
            "citation": False
        },
        ReportType.ACADEMIC: {
            "structure": [
                {"title": "摘要", "level": 1},
                {"title": "引言", "level": 1},
                {"title": "文献综述", "level": 1},
                {"title": "研究方法", "level": 1},
                {"title": "结果", "level": 1},
                {"title": "讨论", "level": 1},
                {"title": "结论", "level": 1},
                {"title": "参考文献", "level": 1},
            ],
            "style": "academic",
            "citation": True
        },
        ReportType.NEWS: {
            "structure": [
                {"title": "导语", "level": 1},
                {"title": "主体内容", "level": 1},
                {"title": "背景信息", "level": 1},
                {"title": "相关链接", "level": 1},
            ],
            "style": "journalistic",
            "citation": False
        }
    }
    
    @classmethod
    def get_template(cls, report_type: ReportType) -> Dict:
        """获取模板"""
        return cls.TEMPLATES.get(report_type, cls.TEMPLATES[ReportType.RESEARCH])
    
    @classmethod
    def list_templates(cls) -> List[str]:
        """列出所有模板"""
        return [t.value for t in cls.TEMPLATES.keys()]


class SmartReportGenerator:
    """智能报告生成器"""
    
    def __init__(self):
        self.templates = TemplateLibrary()
    
    def generate(self, data: ReportData, format: ReportFormat = ReportFormat.MARKDOWN) -> str:
        """生成报告"""
        if format == ReportFormat.MARKDOWN:
            return self._to_markdown(data)
        elif format == ReportFormat.HTML:
            return self._to_html(data)
        elif format == ReportFormat.JSON:
            return self._to_json(data)
        elif format == ReportFormat.PDF:
            return self._to_pdf(data)
        else:
            return self._to_markdown(data)
    
    def _to_markdown(self, data: ReportData) -> str:
        """生成 Markdown"""
        lines = []
        
        # 标题
        lines.append(f"# {data.title}")
        lines.append(f"\n> 生成时间: {data.created_at}")
        lines.append(f"> 报告类型: {data.type.value}\n")
        
        # 元数据
        if data.metadata:
            lines.append("## 元数据")
            for key, value in data.metadata.items():
                lines.append(f"- **{key}**: {value}")
            lines.append("")
        
        # 章节
        for section in data.sections:
            prefix = "#" * section.level
            lines.append(f"{prefix} {section.title}")
            lines.append("")
            lines.append(section.content)
            lines.append("")
        
        return "\n".join(lines)
    
    def _to_html(self, data: ReportData) -> str:
        """生成 HTML"""
        sections_html = ""
        for section in data.sections:
            tag = f"h{section.level + 1}"
            sections_html += f"<{tag}>{html.escape(section.title)}</{tag}>\n"
            sections_html += f"<p>{html.escape(section.content)}</p>\n"
        
        html_template = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{html.escape(data.title)}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #333; border-bottom: 2px solid #4CAF50; padding-bottom: 10px; }}
        h2 {{ color: #555; margin-top: 30px; }}
        h3 {{ color: #666; }}
        p {{ line-height: 1.6; color: #444; }}
        .meta {{ color: #888; font-size: 0.9em; margin-bottom: 20px; }}
    </style>
</head>
<body>
    <h1>{html.escape(data.title)}</h1>
    <div class="meta">
        <p>生成时间: {data.created_at}</p>
        <p>报告类型: {data.type.value}</p>
    </div>
    {sections_html}
</body>
</html>"""
        return html_template
    
    def _to_json(self, data: ReportData) -> str:
        """生成 JSON"""
        return json.dumps(asdict(data), ensure_ascii=False, indent=2)
    
    def _to_pdf(self, data: ReportData) -> bytes:
        """生成 PDF（简化版，实际应使用 reportlab 等库）"""
        # 这里返回 Markdown 作为占位
        # 实际实现应使用 reportlab 或 weasyprint
        return self._to_markdown(data).encode('utf-8')
    
    def auto_generate(self, content: str, report_type: ReportType = None) -> ReportData:
        """自动识别类型并生成报告"""
        # 识别报告类型
        if report_type is None:
            report_type = self._detect_type(content)
        
        # 获取模板
        template = self.templates.get_template(report_type)
        
        # 解析内容
        sections = self._parse_content(content, template)
        
        # 生成标题
        title = self._generate_title(content, report_type)
        
        return ReportData(
            title=title,
            type=report_type,
            sections=sections,
            metadata={
                "auto_generated": True,
                "template": report_type.value
            }
        )
    
    def _detect_type(self, content: str) -> ReportType:
        """检测报告类型"""
        indicators = {
            ReportType.RESEARCH: ["研究", "调研", "分析", "趋势"],
            ReportType.TECHNICAL: ["技术", "实现", "架构", "代码"],
            ReportType.BUSINESS: ["商业", "市场", "竞争", "战略"],
            ReportType.ACADEMIC: ["论文", "文献", "方法", "实验"],
            ReportType.COMPARISON: ["对比", "比较", "vs", "差异"],
            ReportType.SUMMARY: ["总结", "摘要", "要点", "概述"],
        }
        
        scores = {t: 0 for t in ReportType}
        content_lower = content.lower()
        
        for report_type, words in indicators.items():
            for word in words:
                if word in content_lower:
                    scores[report_type] += 1
        
        return max(scores, key=scores.get) if max(scores.values()) > 0 else ReportType.RESEARCH
    
    def _parse_content(self, content: str, template: Dict) -> List[ReportSection]:
        """解析内容到章节"""
        sections = []
        structure = template.get("structure", [])
        
        # 简单分段
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        
        for i, item in enumerate(structure):
            if i < len(paragraphs):
                sections.append(ReportSection(
                    title=item["title"],
                    content=paragraphs[i],
                    level=item["level"]
                ))
            else:
                sections.append(ReportSection(
                    title=item["title"],
                    content="（待补充）",
                    level=item["level"]
                ))
        
        # 添加剩余内容
        if len(paragraphs) > len(structure):
            remaining = '\n\n'.join(paragraphs[len(structure):])
            sections.append(ReportSection(
                title="补充内容",
                content=remaining,
                level=1
            ))
        
        return sections
    
    def _generate_title(self, content: str, report_type: ReportType) -> str:
        """生成标题"""
        # 尝试提取第一行作为标题
        first_line = content.strip().split('\n')[0][:50]
        
        type_names = {
            ReportType.RESEARCH: "研究报告",
            ReportType.ANALYSIS: "分析报告",
            ReportType.SUMMARY: "总结报告",
            ReportType.COMPARISON: "对比分析",
            ReportType.TECHNICAL: "技术文档",
            ReportType.BUSINESS: "商业报告",
            ReportType.ACADEMIC: "学术论文",
            ReportType.NEWS: "新闻稿"
        }
        
        if len(first_line) > 10:
            return f"{first_line} - {type_names.get(report_type, '报告')}"
        else:
            return f"{type_names.get(report_type, '报告')} - {datetime.now().strftime('%Y-%m-%d')}"
    
    def batch_generate(self, contents: List[str], formats: List[ReportFormat]) -> Dict[str, str]:
        """批量生成多格式报告"""
        results = {}
        
        for i, content in enumerate(contents):
            data = self.auto_generate(content)
            
            for fmt in formats:
                key = f"report_{i}_{fmt.value}"
                results[key] = self.generate(data, fmt)
        
        return results


class ReportOptimizer:
    """报告优化器"""
    
    def optimize(self, content: str, target_length: int = None) -> str:
        """优化报告内容"""
        # 去除冗余
        content = self._remove_redundancy(content)
        
        # 调整长度
        if target_length:
            content = self._adjust_length(content, target_length)
        
        # 格式化
        content = self._format_content(content)
        
        return content
    
    def _remove_redundancy(self, content: str) -> str:
        """去除冗余内容"""
        # 去除重复句子
        sentences = re.split(r'[。！？]', content)
        unique_sentences = []
        seen = set()
        
        for s in sentences:
            s_clean = re.sub(r'\s+', '', s)
            if s_clean and s_clean not in seen:
                seen.add(s_clean)
                unique_sentences.append(s)
        
        return '。'.join(unique_sentences)
    
    def _adjust_length(self, content: str, target: int) -> str:
        """调整内容长度"""
        current = len(content)
        
        if current > target * 1.2:
            # 需要压缩
            return self._compress(content, target)
        elif current < target * 0.8:
            # 需要扩展
            return self._expand(content, target)
        
        return content
    
    def _compress(self, content: str, target: int) -> str:
        """压缩内容"""
        # 提取关键句
        sentences = re.split(r'[。！？]', content)
        
        # 简单策略：保留前70%的句子
        keep_count = int(len(sentences) * 0.7)
        return '。'.join(sentences[:keep_count])
    
    def _expand(self, content: str, target: int) -> str:
        """扩展内容"""
        # 添加过渡语句
        expansion = "\n\n（此处可进一步展开详细说明）"
        return content + expansion
    
    def _format_content(self, content: str) -> str:
        """格式化内容"""
        # 统一标点
        content = content.replace('，', ', ').replace('。', '. ')
        # 去除多余空格
        content = re.sub(r'\s+', ' ', content)
        return content.strip()


# 便捷函数
def create_generator() -> SmartReportGenerator:
    """创建生成器"""
    return SmartReportGenerator()


def quick_report(content: str, format: str = "markdown") -> str:
    """快速生成报告"""
    generator = SmartReportGenerator()
    
    format_map = {
        "markdown": ReportFormat.MARKDOWN,
        "html": ReportFormat.HTML,
        "json": ReportFormat.JSON,
        "pdf": ReportFormat.PDF
    }
    
    fmt = format_map.get(format, ReportFormat.MARKDOWN)
    data = generator.auto_generate(content)
    return generator.generate(data, fmt)


if __name__ == "__main__":
    # 测试
    sample_content = """
人工智能正在快速发展。深度学习技术取得了重大突破。
自然语言处理能力显著提升。计算机视觉应用日益广泛。
未来AI将在更多领域发挥重要作用。
"""
    
    generator = SmartReportGenerator()
    
    # 自动识别类型并生成
    data = generator.auto_generate(sample_content)
    print(f"识别类型: {data.type.value}")
    print(f"生成标题: {data.title}")
    
    # 生成 Markdown
    md_report = generator.generate(data, ReportFormat.MARKDOWN)
    print("\n--- Markdown 报告 ---")
    print(md_report[:500])
    
    # 生成 HTML
    html_report = generator.generate(data, ReportFormat.HTML)
    print("\n--- HTML 报告预览 ---")
    print(html_report[:500])
