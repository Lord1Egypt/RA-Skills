#!/usr/bin/env python3
"""
基础测试 - 小龙虾工作流 MVP 测试
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# 添加脚本路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../scripts'))

from task_analyzer import TaskAnalyzer, TaskSummary
from project_manager import ProjectManager


def test_task_analyzer():
    """测试任务分析器"""
    print("🧪 测试任务分析器...")
    
    analyzer = TaskAnalyzer()
    
    # 测试用例
    test_cases = [
        {
            'task': '帮我设计一个完整的电商网站后端系统',
            'expected_complexity': (7, 10)  # 应该是高复杂度
        },
        {
            'task': '写一个Python脚本，读取CSV文件并计算平均值',
            'expected_complexity': (3, 6)   # 应该是中低复杂度
        },
        {
            'task': '查一下今天的天气',
            'expected_complexity': (1, 3)   # 应该是低复杂度
        }
    ]
    
    all_passed = True
    
    for i, test_case in enumerate(test_cases):
        print(f"\n测试用例 {i+1}: {test_case['task'][:50]}...")
        
        summary = analyzer.analyze(test_case['task'])
        
        # 检查基本属性
        assert hasattr(summary, 'task_id'), "缺少 task_id"
        assert hasattr(summary, 'complexity_score'), "缺少 complexity_score"
        assert hasattr(summary, 'requires_decomposition'), "缺少 requires_decomposition"
        
        # 检查复杂度范围
        min_expected, max_expected = test_case['expected_complexity']
        if min_expected <= summary.complexity_score <= max_expected:
            print(f"  ✅ 复杂度检查通过: {summary.complexity_score} (预期范围: {min_expected}-{max_expected})")
        else:
            print(f"  ❌ 复杂度检查失败: {summary.complexity_score} (预期范围: {min_expected}-{max_expected})")
            all_passed = False
        
        # 检查Markdown生成
        md = summary.to_markdown()
        assert md.startswith('# 任务概要:'), "Markdown格式错误"
        assert summary.task_id in md, "任务ID不在Markdown中"
        
        print(f"  ✅ Markdown生成检查通过")
        
        # 保存测试文件
        test_dir = Path(tempfile.mkdtemp(prefix='xlx_test_'))
        md_file = test_dir / f"test_{i+1}.md"
        md_file.write_text(md, encoding='utf-8')
        
        print(f"  ✅ 文件保存检查通过: {md_file}")
        
        # 清理
        shutil.rmtree(test_dir)
    
    if all_passed:
        print("\n✅ 任务分析器测试全部通过")
    else:
        print("\n❌ 任务分析器测试有失败")
    
    return all_passed


def test_project_manager():
    """测试项目管理器"""
    print("\n🧪 测试项目管理器...")
    
    # 创建虚拟任务概要
    from dataclasses import dataclass
    from typing import List
    
    @dataclass
    class TestTaskSummary:
        task_id: str = "test_task_20250317_1320_abcd"
        original_description: str = "测试任务：设计一个简单的TODO应用"
        title: str = "TODO应用设计"
        description: str = "设计一个包含前后端的简单TODO应用"
        objectives: List[str] = None
        constraints: List[str] = None
        expected_outputs: List[str] = None
        complexity_score: int = 6
        estimated_hours: float = 8.0
        deadline: str = None
        requires_decomposition: bool = True
        keywords: List[str] = None
        created_at: str = "2026-03-17T13:20:00+08:00"
        updated_at: str = "2026-03-17T13:20:00+08:00"
        
        def __post_init__(self):
            if self.objectives is None:
                self.objectives = ["完成前端界面", "完成后端API", "实现数据库"]
            if self.constraints is None:
                self.constraints = ["时间有限", "资源有限"]
            if self.expected_outputs is None:
                self.expected_outputs = ["可运行的TODO应用", "设计文档"]
            if self.keywords is None:
                self.keywords = ["TODO", "应用", "设计", "前后端"]
        
        def to_markdown(self):
            return f"# {self.title}\n\n{self.description}"
    
    # 使用临时目录
    with tempfile.TemporaryDirectory(prefix='xlx_project_') as tmpdir:
        # 修改配置使用临时目录
        import json
        config_path = Path(tmpdir) / 'test_config.json'
        config = {
            'project_base_dir': tmpdir
        }
        config_path.write_text(json.dumps(config), encoding='utf-8')
        
        # 创建项目管理器
        summary = TestTaskSummary()
        manager = ProjectManager(summary, str(config_path))
        
        # 创建项目
        project_dir = manager.create_project()
        
        # 检查项目目录
        assert project_dir.exists(), "项目目录未创建"
        assert (project_dir / 'task_summary.md').exists(), "任务概要文件未创建"
        assert (project_dir / 'top_level_plan.md').exists(), "顶层方案文件未创建"
        assert (project_dir / 'project_config.json').exists(), "配置文件未创建"
        assert (project_dir / 'steps').exists(), "steps目录未创建"
        assert (project_dir / 'final_output').exists(), "final_output目录未创建"
        assert (project_dir / 'backup').exists(), "backup目录未创建"
        
        print(f"  ✅ 项目目录结构检查通过: {project_dir}")
        
        # 检查文件内容
        summary_content = (project_dir / 'task_summary.md').read_text(encoding='utf-8')
        assert 'TODO应用设计' in summary_content, "任务概要内容不正确"
        
        plan_content = (project_dir / 'top_level_plan.md').read_text(encoding='utf-8')
        assert '顶层方案' in plan_content, "顶层方案内容不正确"
        
        config_content = json.loads((project_dir / 'project_config.json').read_text(encoding='utf-8'))
        assert config_content['task_id'] == summary.task_id, "配置文件内容不正确"
        
        print(f"  ✅ 文件内容检查通过")
        
        # 检查项目信息
        info = manager.get_project_info()
        assert info['project_dir'] == str(project_dir), "项目信息不正确"
        assert info['task_id'] == summary.task_id, "项目信息不正确"
        
        print(f"  ✅ 项目信息检查通过")
        
        # 清理测试
        manager.cleanup()
        assert not project_dir.exists(), "项目清理失败"
        
        print(f"  ✅ 项目清理检查通过")
    
    print("\n✅ 项目管理器测试全部通过")
    return True


def test_integration():
    """测试集成功能"""
    print("\n🧪 测试集成功能...")
    
    with tempfile.TemporaryDirectory(prefix='xlx_integration_') as tmpdir:
        # 创建配置
        import json
        config_path = Path(tmpdir) / 'config.json'
        config = {
            'project_base_dir': tmpdir,
            'complexity_keywords': ['设计', '系统', '开发']
        }
        config_path.write_text(json.dumps(config), encoding='utf-8')
        
        # 完整流程测试
        task = "帮我设计一个用户管理系统"
        
        # 1. 分析任务
        analyzer = TaskAnalyzer(str(config_path))
        summary = analyzer.analyze(task)
        
        print(f"  1. 任务分析完成: ID={summary.task_id}, 复杂度={summary.complexity_score}/10")
        
        # 2. 创建项目
        manager = ProjectManager(summary, str(config_path))
        project_dir = manager.create_project()
        
        print(f"  2. 项目创建完成: {project_dir}")
        
        # 3. 检查输出
        expected_files = [
            'task_summary.md',
            'top_level_plan.md',
            'project_config.json',
            'README.md'
        ]
        
        for file in expected_files:
            assert (project_dir / file).exists(), f"文件 {file} 不存在"
        
        print(f"  3. 文件检查通过")
        
        # 4. 验证内容
        config_content = json.loads((project_dir / 'project_config.json').read_text(encoding='utf-8'))
        assert config_content['status'] == 'created', "项目状态不正确"
        
        print(f"  4. 内容验证通过")
        
        # 清理
        shutil.rmtree(project_dir, ignore_errors=True)
        
        print(f"  5. 清理完成")
    
    print("\n✅ 集成测试全部通过")
    return True


def main():
    """主测试函数"""
    print("=" * 60)
    print("小龙虾工作流 MVP 测试套件")
    print("=" * 60)
    
    results = []
    
    try:
        results.append(('任务分析器', test_task_analyzer()))
    except Exception as e:
        print(f"❌ 任务分析器测试异常: {e}")
        results.append(('任务分析器', False))
    
    try:
        results.append(('项目管理器', test_project_manager()))
    except Exception as e:
        print(f"❌ 项目管理器测试异常: {e}")
        results.append(('项目管理器', False))
    
    try:
        results.append(('集成测试', test_integration()))
    except Exception as e:
        print(f"❌ 集成测试异常: {e}")
        results.append(('集成测试', False))
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 所有测试通过！MVP 功能正常。")
        return 0
    else:
        print("⚠️  部分测试失败，请检查问题。")
        return 1


if __name__ == "__main__":
    sys.exit(main())