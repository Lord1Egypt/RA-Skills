"""
Resume Generator - 核心生成逻辑
"""

from typing import Dict, List, Any, Optional
from datetime import datetime


class ResumeGenerator:
    """简历生成器"""
    
    TEMPLATES = {
        'simple': '简约技术型',
        'classic': '经典专业型', 
        'modern': '现代简洁型'
    }
    
    def __init__(self, data: Dict[str, Any]):
        """
        初始化简历生成器
        
        Args:
            data: 简历数据字典
        """
        self.data = self._validate_and_complete(data)
    
    def _validate_and_complete(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """验证并补全数据"""
        required = ['name', 'email']
        for field in required:
            if field not in data or not data[field]:
                raise ValueError(f"必填字段: {field}")
        
        # 设置默认值
        defaults = {
            'location': '',
            'education': [],
            'experience': [],
            'projects': [],
            'skills': [],
            'self_intro': ''
        }
        for key, value in defaults.items():
            if key not in data:
                data[key] = value
        
        return data
    
    def generate_markdown(self, template: str = 'simple') -> str:
        """
        生成Markdown格式简历
        
        Args:
            template: 模板类型 (simple/classic/modern)
        
        Returns:
            Markdown格式简历字符串
        """
        if template == 'simple':
            return self._markdown_simple()
        elif template == 'classic':
            return self._markdown_classic()
        elif template == 'modern':
            return self._markdown_modern()
        else:
            raise ValueError(f"未知模板: {template}")
    
    def _markdown_simple(self) -> str:
        """简约技术型模板"""
        lines = [
            f"# {self.data['name']}",
            "",
            f"📧 {self.data['email']} | 📱 {self.data.get('phone', '')} | 📍 {self.data.get('location', '')}",
            ""
        ]
        
        # 自我介绍
        if self.data.get('self_intro'):
            lines.extend([
                "## 个人简介",
                self.data['self_intro'],
                ""
            ])
        
        # 技术技能
        if self.data.get('skills'):
            lines.append("## 技术技能")
            for skill_group in self.data['skills']:
                category = skill_group.get('category', '其他')
                items = skill_group.get('items', [])
                if items:
                    lines.append(f"- **{category}**: {', '.join(items)}")
            lines.append("")
        
        # 教育经历
        if self.data.get('education'):
            lines.append("## 教育经历")
            for edu in self.data['education']:
                school = edu.get('school', '')
                major = edu.get('major', '')
                degree = edu.get('degree', '')
                year = edu.get('year', '')
                line = f"- {school} | {major} | {degree} | {year}"
                lines.append(line)
            lines.append("")
        
        # 工作经历
        if self.data.get('experience'):
            lines.append("## 工作经历")
            for exp in self.data['experience']:
                company = exp.get('company', '')
                title = exp.get('title', '')
                duration = exp.get('duration', '')
                description = exp.get('description', '')
                lines.append(f"### {company} | {title} | {duration}")
                if description:
                    for desc_line in description.split('\n'):
                        if desc_line.strip():
                            lines.append(desc_line)
                lines.append("")
        
        # 项目经历
        if self.data.get('projects'):
            lines.append("## 项目经历")
            for proj in self.data['projects']:
                name = proj.get('name', '')
                role = proj.get('role', '')
                tech = proj.get('tech', '')
                description = proj.get('description', '')
                outcome = proj.get('outcome', '')
                lines.append(f"### {name} ({role})")
                if tech:
                    lines.append(f"**技术栈**: {tech}")
                if description:
                    lines.append(description)
                if outcome:
                    lines.append(f"📈 {outcome}")
                lines.append("")
        
        return '\n'.join(lines)
    
    def _markdown_classic(self) -> str:
        """经典专业型模板"""
        lines = [
            "# " + self.data['name'],
            "",
            f"**邮箱**: {self.data['email']}    **电话**: {self.data.get('phone', '')}    **位置**: {self.data.get('location', '')}",
            "",
            "---",
            ""
        ]
        
        if self.data.get('self_intro'):
            lines.extend(["## 个人信息", self.data['self_intro'], ""])
        
        if self.data.get('skills'):
            lines.append("## 专业技能")
            for skill_group in self.data['skills']:
                category = skill_group.get('category', '')
                items = skill_group.get('items', [])
                if items and category:
                    lines.append(f"- {category}: {', '.join(items)}")
            lines.append("")
        
        if self.data.get('education'):
            lines.append("## 教育背景")
            for edu in self.data['education']:
                line = f"- {edu.get('year', '')} {edu.get('school', '')} | {edu.get('major', '')} | {edu.get('degree', '')}"
                lines.append(line)
            lines.append("")
        
        if self.data.get('experience'):
            lines.append("## 工作经历")
            for exp in self.data['experience']:
                lines.append(f"**{exp.get('company', '')}** - {exp.get('title', '')} ({exp.get('duration', '')})")
                desc = exp.get('description', '')
                if desc:
                    for line in desc.split('\n'):
                        if line.strip():
                            lines.append(f"  - {line.strip()}")
            lines.append("")
        
        if self.data.get('projects'):
            lines.append("## 项目经验")
            for proj in self.data['projects']:
                lines.append(f"**{proj.get('name', '')}** ({proj.get('role', '')})")
                lines.append(f"  - 技术: {proj.get('tech', '')}")
                if proj.get('description'):
                    lines.append(f"  - {proj.get('description')}")
            lines.append("")
        
        return '\n'.join(lines)
    
    def _markdown_modern(self) -> str:
        """现代简洁型模板"""
        lines = [
            f"# {self.data['name']}",
            "",
            f"📫 {self.data['email']}  |  📱 {self.data.get('phone', '')}  |  📍 {self.data.get('location', '')}",
            ""
        ]
        
        if self.data.get('self_intro'):
            lines.extend([
                "> " + self.data['self_intro'].replace('\n', '  \n> '),
                ""
            ])
        
        if self.data.get('skills'):
            lines.append("## 技术栈")
            skills_text = []
            for skill_group in self.data['skills']:
                items = skill_group.get('items', [])
                skills_text.extend(items)
            if skills_text:
                lines.append("```")
                lines.append(', '.join(skills_text))
                lines.append("```")
            lines.append("")
        
        if self.data.get('experience'):
            lines.append("## Experience")
            for exp in self.data['experience']:
                lines.append(f"### {exp.get('company', '')} · {exp.get('title', '')}")
                lines.append(f"*{exp.get('duration', '')}*")
                desc = exp.get('description', '')
                if desc:
                    for line in desc.split('\n'):
                        if line.strip():
                            lines.append(f"- {line.strip()}")
            lines.append("")
        
        if self.data.get('projects'):
            lines.append("## Projects")
            for proj in self.data['projects']:
                lines.append(f"### {proj.get('name', '')}")
                lines.append(f"**Role**: {proj.get('role', '')}  |  **Tech**: {proj.get('tech', '')}")
                if proj.get('description'):
                    lines.append(f"- {proj.get('description')}")
                if proj.get('outcome'):
                    lines.append(f"- 📈 {proj.get('outcome')}")
            lines.append("")
        
        return '\n'.join(lines)
    
    def generate_html(self, template: str = 'simple') -> str:
        """生成HTML格式简历"""
        md = self.generate_markdown(template)
        return self._markdown_to_html(md)
    
    def _markdown_to_html(self, markdown: str) -> str:
        """简单的Markdown到HTML转换"""
        html_lines = [
            '<!DOCTYPE html>',
            '<html lang="zh-CN">',
            '<head>',
            '  <meta charset="UTF-8">',
            '  <meta name="viewport" content="width=device-width, initial-scale=1.0">',
            '  <title>简历 - ' + self.data['name'] + '</title>',
            '  <style>',
            '    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;',
            '           max-width: 800px; margin: 40px auto; padding: 20px; color: #333; }',
            '    h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }',
            '    h2 { color: #34495e; margin-top: 30px; }',
            '    h3 { color: #7f8c8d; }',
            '    .contact { color: #666; margin-bottom: 20px; }',
            '    pre { background: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto; }',
            '    code { background: #f8f9fa; padding: 2px 5px; border-radius: 3px; }',
            '    ul { line-height: 1.8; }',
            '  </style>',
            '</head>',
            '<body>'
        ]
        
        # 简单的Markdown转HTML
        in_code_block = False
        for line in markdown.split('\n'):
            if line.startswith('```'):
                in_code_block = not in_code_block
                if in_code_block:
                    html_lines.append('<pre><code>')
                else:
                    html_lines.append('</code></pre>')
            elif in_code_block:
                html_lines.append(line)
            elif line.startswith('# '):
                html_lines.append(f'<h1>{line[2:]}</h1>')
            elif line.startswith('## '):
                html_lines.append(f'<h2>{line[3:]}</h2>')
            elif line.startswith('### '):
                html_lines.append(f'<h3>{line[4:]}</h3>')
            elif line.startswith('- '):
                html_lines.append(f'<li>{line[2:]}</li>')
            elif line.startswith('>'):
                html_lines.append(f'<blockquote>{line[1:].strip()}</blockquote>')
            elif line.strip():
                html_lines.append(f'<p>{line}</p>')
            else:
                html_lines.append('<br>')
        
        html_lines.extend([
            '</body>',
            '</html>'
        ])
        
        return '\n'.join(html_lines)
    
    def optimize_for_jd(self, job_description: str) -> str:
        """
        根据岗位描述优化简历
        
        Args:
            job_description: 岗位JD文本
        
        Returns:
            优化建议
        """
        # 提取关键词
        jd_lower = job_description.lower()
        keywords = []
        
        tech_keywords = [
            'python', 'java', 'javascript', 'go', 'rust', 'c++', 'sql', 'nosql',
            'react', 'vue', 'angular', 'node.js', 'django', 'flask', 'spring',
            'docker', 'kubernetes', 'jenkins', 'git', 'linux', 'aws', 'azure',
            'mysql', 'postgresql', 'mongodb', 'redis', 'kafka', 'rabbitmq',
            'api', 'rest', 'graphql', 'microservices', 'agile', 'scrum'
        ]
        
        for kw in tech_keywords:
            if kw in jd_lower:
                keywords.append(kw)
        
        suggestions = []
        suggestions.append("## 简历优化建议")
        suggestions.append("")
        
        if keywords:
            suggestions.append("### 关键词匹配")
            suggestions.append("岗位要求的关键技术：")
            for kw in keywords:
                suggestions.append(f"- **{kw}**: 确保在技能和工作描述中突出")
            suggestions.append("")
        
        # 检查缺失技能
        all_skills = []
        for skill_group in self.data.get('skills', []):
            all_skills.extend([s.lower() for s in skill_group.get('items', [])])
        
        missing = [kw for kw in keywords if kw not in ' '.join(all_skills)]
        if missing:
            suggestions.append("### 建议补充技能")
            suggestions.append("岗位要求但简历中未提及：")
            for kw in missing[:5]:
                suggestions.append(f"- {kw}")
            suggestions.append("")
        
        suggestions.append("### 优化策略")
        suggestions.append("1. 在工作描述中使用岗位JD中的关键词")
        suggestions.append("2. 量化成果（如：提升30%性能）")
        suggestions.append("3. 突出与岗位相关的项目经验")
        
        return '\n'.join(suggestions)


def generate_resume(data: Dict[str, Any], template: str = 'simple', format: str = 'markdown') -> str:
    """
    快速生成简历
    
    Args:
        data: 简历数据
        template: 模板类型
        format: 输出格式 (markdown/html)
    
    Returns:
        格式化后的简历字符串
    """
    generator = ResumeGenerator(data)
    
    if format == 'markdown':
        return generator.generate_markdown(template)
    elif format == 'html':
        return generator.generate_html(template)
    else:
        raise ValueError(f"不支持的格式: {format}")


if __name__ == '__main__':
    # 测试数据
    test_data = {
        'name': '张三',
        'email': 'zhangsan@example.com',
        'phone': '13800138000',
        'location': '北京',
        'education': [
            {'school': '北京大学', 'major': '计算机科学', 'degree': '硕士', 'year': '2020'}
        ],
        'experience': [
            {
                'company': '字节跳动',
                'title': '高级工程师',
                'duration': '2020.06 - 至今',
                'description': '- 负责抖音核心功能开发\n- 主导性能优化，提升30%加载速度'
            }
        ],
        'projects': [
            {
                'name': '电商系统',
                'role': '技术负责人',
                'tech': 'Python, Django, Redis',
                'description': '构建高并发电商平台，日均订单10万+',
                'outcome': '月GMV突破500万'
            }
        ],
        'skills': [
            {'category': '编程语言', 'items': ['Python', 'JavaScript', 'SQL']},
            {'category': '框架', 'items': ['Django', 'React', 'Vue']},
            {'category': '工具', 'items': ['Git', 'Docker', 'Jenkins']}
        ],
        'self_intro': '6年后端开发经验，擅长高并发系统设计'
    }
    
    generator = ResumeGenerator(test_data)
    print(generator.generate_markdown('simple'))