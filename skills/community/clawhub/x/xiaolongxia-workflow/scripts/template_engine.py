#!/usr/bin/env python3
"""
模板引擎 - 小龙虾工作流 v0.2.0 核心组件

功能：
1. 加载和渲染模板文件
2. 支持变量替换、条件判断、循环
3. 内置模板（任务摘要、步骤计划、报告等）
4. 扩展自定义模板
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TemplateEngine:
    """模板引擎"""
    
    def __init__(self, template_dir: Optional[str] = None):
        """
        初始化模板引擎
        
        Args:
            template_dir: 模板目录路径
        """
        self.template_dir = self._resolve_template_dir(template_dir)
        self.templates: Dict[str, str] = {}
        self.load_builtin_templates()
        logger.info(f"模板引擎初始化完成，模板目录: {self.template_dir}")
    
    def _resolve_template_dir(self, template_dir: Optional[str]) -> Path:
        """解析模板目录路径"""
        if template_dir and os.path.exists(template_dir):
            return Path(template_dir)
        
        # 默认模板目录（相对于脚本位置）
        script_dir = Path(__file__).parent
        default_dir = script_dir.parent / "templates"
        
        if default_dir.exists():
            return default_dir
        
        # 如果不存在，创建默认模板目录
        default_dir.mkdir(parents=True, exist_ok=True)
        self._create_default_templates(default_dir)
        
        return default_dir
    
    def _create_default_templates(self, template_dir: Path):
        """创建默认模板"""
        # 任务摘要模板
        task_summary_template = """# 任务摘要

## 基本信息
- **任务ID**: {{task_id}}
- **任务描述**: {{task_description}}
- **复杂度**: {{complexity_score}}/10
- **预计耗时**: {{estimated_hours}} 小时
- **需要分层处理**: {{requires_decomposition}}

## 分析结果
{{analysis_notes}}

## 建议工作流
{{workflow_suggestion}}

## 关键步骤
{{#key_steps}}
- {{.}}
{{/key_steps}}

## 创建信息
- **创建时间**: {{created_at}}
- **项目目录**: {{project_dir}}
"""
        
        # 顶层方案模板
        top_level_plan_template = """# 顶层方案: {{task_name}}

## 概述
{{task_description}}

## 阶段划分
{{#phases}}
### 阶段 {{phase_number}}: {{phase_name}}
- **目标**: {{phase_goal}}
- **预计耗时**: {{estimated_hours}} 小时
- **关键交付物**: {{deliverables}}
- **依赖关系**: {{dependencies}}

{{/phases}}

## 总体时间线
- **总预计耗时**: {{total_hours}} 小时
- **阶段数**: {{phase_count}}
- **关键里程碑**: {{milestones}}

## 风险与缓解
{{#risks}}
- **{{risk_name}}**: {{risk_description}} (缓解: {{mitigation}})
{{/risks}}

## 成功标准
{{#success_criteria}}
- {{.}}
{{/success_criteria}}
"""
        
        # 步骤报告模板
        step_report_template = """# 步骤报告: {{step_name}}

## 步骤信息
- **步骤ID**: {{step_id}}
- **类型**: {{step_type}}
- **深度**: {{depth}}
- **预计耗时**: {{estimated_hours}} 小时
- **实际耗时**: {{actual_hours}} 小时

## 执行状态
{{status_emoji}} **状态**: {{status}}

{{#start_time}}
- **开始时间**: {{start_time}}
- **结束时间**: {{end_time}}
{{/start_time}}

## 输入
{{#inputs}}
- {{.}}
{{/inputs}}

## 输出
{{#outputs}}
- {{.}}
{{/outputs}}

## 执行详情
{{execution_details}}

{{#error_message}}
## 错误信息
{{error_message}}

### 恢复策略
{{recovery_strategy}}
{{/error_message}}

## 下一步
{{next_steps}}
"""
        
        # 保存模板文件
        templates = {
            'task_summary.md.tpl': task_summary_template,
            'top_level_plan.md.tpl': top_level_plan_template,
            'step_report.md.tpl': step_report_template,
        }
        
        for filename, content in templates.items():
            filepath = template_dir / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
        
        logger.info(f"创建了 {len(templates)} 个默认模板")
    
    def load_builtin_templates(self):
        """加载内置模板"""
        # 从模板目录加载所有模板文件
        if not self.template_dir.exists():
            logger.warning(f"模板目录不存在: {self.template_dir}")
            return
        
        for template_file in self.template_dir.glob("*.tpl"):
            try:
                with open(template_file, 'r', encoding='utf-8') as f:
                    template_name = template_file.stem  # 移除扩展名
                    self.templates[template_name] = f.read()
                logger.debug(f"加载模板: {template_name}")
            except Exception as e:
                logger.warning(f"加载模板失败 {template_file}: {e}")
    
    def load_template(self, template_name: str) -> Optional[str]:
        """
        加载模板
        
        Args:
            template_name: 模板名称（不带扩展名）
            
        Returns:
            Optional[str]: 模板内容，如果不存在则返回None
        """
        # 首先检查已加载的模板
        if template_name in self.templates:
            return self.templates[template_name]
        
        # 尝试从文件加载
        template_file = self.template_dir / f"{template_name}.tpl"
        if template_file.exists():
            try:
                with open(template_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.templates[template_name] = content
                return content
            except Exception as e:
                logger.warning(f"加载模板文件失败 {template_file}: {e}")
        
        logger.warning(f"模板未找到: {template_name}")
        return None
    
    def _render_simple_template(self, template: str, context: Dict[str, Any]) -> str:
        """渲染简单模板（支持变量替换和简单循环）"""
        # 首先处理循环块
        result = template
        
        # 处理 {{#list}}...{{/list}} 循环
        pattern = r'\{\{#(\w+)\}\}(.*?)\{\{/\1\}\}'
        
        def replace_loop(match):
            key = match.group(1)
            loop_content = match.group(2).strip()
            
            if key in context:
                items = context[key]
                if isinstance(items, list):
                    rendered_items = []
                    for item in items:
                        # 简单替换循环内的变量
                        if isinstance(item, dict):
                            rendered = loop_content
                            for item_key, item_value in item.items():
                                placeholder = f"{{{{{item_key}}}}}"
                                rendered = rendered.replace(placeholder, str(item_value))
                            rendered_items.append(rendered)
                        else:
                            # 简单值替换
                            placeholder = r'\{\{(\.)\}\}'
                            rendered = re.sub(placeholder, str(item), loop_content)
                            rendered_items.append(rendered)
                    return '\n'.join(rendered_items)
                elif isinstance(items, bool) and items:
                    # 布尔值为真，显示内容
                    return loop_content
                else:
                    # 值不存在或为假，不显示
                    return ''
            else:
                return ''
        
        result = re.sub(pattern, replace_loop, result, flags=re.DOTALL)
        
        # 处理条件块 {{#condition}}...{{/condition}}（布尔值）
        bool_pattern = r'\{\{#(\w+)\}\}(.*?)\{\{/\1\}\}'
        result = re.sub(bool_pattern, replace_loop, result, flags=re.DOTALL)
        
        # 处理变量替换 {{variable}}
        var_pattern = r'\{\{(\w+)\}\}'
        
        def replace_var(match):
            key = match.group(1)
            if key in context:
                return str(context[key])
            else:
                logger.debug(f"变量未找到: {key}")
                return match.group(0)  # 保持原样
        
        result = re.sub(var_pattern, replace_var, result)
        
        return result
    
    def render(self, template_name: str, context: Dict[str, Any]) -> Optional[str]:
        """
        渲染模板
        
        Args:
            template_name: 模板名称
            context: 上下文变量
            
        Returns:
            Optional[str]: 渲染结果，如果失败则返回None
        """
        template = self.load_template(template_name)
        if template is None:
            return None
        
        try:
            result = self._render_simple_template(template, context)
            logger.debug(f"模板渲染完成: {template_name}")
            return result
        except Exception as e:
            logger.error(f"模板渲染失败 {template_name}: {e}")
            return None
    
    def render_to_file(self, template_name: str, context: Dict[str, Any], 
                      output_path: str) -> bool:
        """
        渲染模板并保存到文件
        
        Args:
            template_name: 模板名称
            context: 上下文变量
            output_path: 输出文件路径
            
        Returns:
            bool: 是否成功
        """
        content = self.render(template_name, context)
        if content is None:
            return False
        
        try:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"模板输出已保存: {output_path}")
            return True
        except Exception as e:
            logger.error(f"保存模板输出失败 {output_path}: {e}")
            return False
    
    def get_available_templates(self) -> List[str]:
        """获取可用模板列表"""
        templates = list(self.templates.keys())
        
        # 添加文件系统中的模板
        if self.template_dir.exists():
            for template_file in self.template_dir.glob("*.tpl"):
                name = template_file.stem
                if name not in templates:
                    templates.append(name)
        
        return sorted(templates)


# 工具函数
def create_task_summary(context: Dict[str, Any], output_dir: str) -> Optional[str]:
    """
    创建任务摘要（快捷函数）
    
    Args:
        context: 任务上下文
        output_dir: 输出目录
        
    Returns:
        Optional[str]: 输出文件路径，如果失败则返回None
    """
    engine = TemplateEngine()
    
    output_path = Path(output_dir) / "task_summary.md"
    
    # 确保有必要的字段
    if 'task_id' not in context:
        context['task_id'] = f"task_{int(time.time())}"
    
    if 'created_at' not in context:
        from datetime import datetime
        context['created_at'] = datetime.now().isoformat()
    
    success = engine.render_to_file('task_summary', context, str(output_path))
    
    if success:
        return str(output_path)
    else:
        return None


def create_top_level_plan(context: Dict[str, Any], output_dir: str) -> Optional[str]:
    """
    创建顶层方案（快捷函数）
    
    Args:
        context: 任务上下文
        output_dir: 输出目录
        
    Returns:
        Optional[str]: 输出文件路径，如果失败则返回None
    """
    engine = TemplateEngine()
    
    output_path = Path(output_dir) / "top_level_plan.md"
    
    # 确保有必要的字段
    if 'phases' not in context:
        context['phases'] = []
    
    if 'total_hours' not in context:
        context['total_hours'] = sum(phase.get('estimated_hours', 0) for phase in context.get('phases', []))
    
    if 'phase_count' not in context:
        context['phase_count'] = len(context.get('phases', []))
    
    success = engine.render_to_file('top_level_plan', context, str(output_path))
    
    if success:
        return str(output_path)
    else:
        return None


def test_template_engine():
    """测试模板引擎"""
    print("🧪 测试模板引擎...")
    
    import tempfile
    from pathlib import Path
    import time
    
    # 创建临时目录
    with tempfile.TemporaryDirectory(prefix='xlx_template_') as tmpdir:
        template_dir = Path(tmpdir) / "templates"
        template_dir.mkdir()
        
        # 创建测试模板
        test_template = """# 测试模板

## 基本信息
- **名称**: {{name}}
- **年龄**: {{age}}
- **城市**: {{city}}

## 技能列表
{{#skills}}
- {{name}} ({{level}})
{{/skills}}

{{#has_projects}}
## 项目经验
{{#projects}}
### {{title}}
- **描述**: {{description}}
- **技术**: {{technologies}}
{{/projects}}
{{/has_projects}}

## 总结
{{summary}}
"""
        
        template_file = template_dir / "test_template.tpl"
        with open(template_file, 'w', encoding='utf-8') as f:
            f.write(test_template)
        
        # 初始化引擎
        engine = TemplateEngine(str(template_dir))
        
        # 测试上下文
        context = {
            'name': '张三',
            'age': 30,
            'city': '北京',
            'skills': [
                {'name': 'Python', 'level': '高级'},
                {'name': 'JavaScript', 'level': '中级'},
                {'name': 'Docker', 'level': '初级'},
            ],
            'has_projects': True,
            'projects': [
                {
                    'title': '电商平台',
                    'description': '开发全栈电商平台',
                    'technologies': 'Python, React, PostgreSQL'
                },
                {
                    'title': '数据分析系统',
                    'description': '构建大数据分析管道',
                    'technologies': 'PySpark, Airflow, AWS'
                }
            ],
            'summary': '资深全栈工程师，擅长复杂系统架构。'
        }
        
        # 测试渲染
        result = engine.render('test_template', context)
        
        if result:
            print("✅ 模板渲染成功")
            print("\n渲染结果预览:")
            print(result[:500])
            
            # 测试保存到文件
            output_file = Path(tmpdir) / "output.md"
            success = engine.render_to_file('test_template', context, str(output_file))
            
            if success and output_file.exists():
                print(f"✅ 文件保存成功: {output_file}")
            else:
                print("❌ 文件保存失败")
        else:
            print("❌ 模板渲染失败")
        
        # 测试内置模板渲染
        task_context = {
            'task_id': 'test_task_001',
            'task_description': '测试任务描述',
            'complexity_score': 6,
            'estimated_hours': 8.5,
            'requires_decomposition': True,
            'analysis_notes': '这是一个中等复杂度的任务，需要分层处理。',
            'workflow_suggestion': '建议采用简化分层流程，先设计架构，再逐步实现。',
            'key_steps': ['需求分析', '架构设计', '模块开发', '测试部署'],
            'created_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'project_dir': '/tmp/test_project'
        }
        
        task_result = engine.render('task_summary', task_context)
        if task_result:
            print("\n✅ 内置模板渲染成功")
        else:
            print("\n⚠️  内置模板渲染失败（可能模板不存在）")
        
        # 测试可用模板列表
        templates = engine.get_available_templates()
        print(f"\n📋 可用模板: {len(templates)} 个")
        for t in templates:
            print(f"   - {t}")
    
    print("\n✅ 模板引擎测试完成")
    return True


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_template_engine()
    else:
        print("用法:")
        print("  python template_engine.py test")
        print("\n注意: 完整使用需要与其他模块集成")