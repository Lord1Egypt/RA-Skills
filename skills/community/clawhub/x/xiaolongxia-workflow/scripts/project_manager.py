#!/usr/bin/env python3
"""
项目管理器 - 小龙虾工作流 MVP 核心组件

功能：
1. 创建标准项目文件夹结构
2. 生成任务概要文档
3. 管理项目文件操作
4. 提供备份基础功能
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import logging

# 导入任务分析器
try:
    from task_analyzer import TaskSummary
except ImportError:
    # 为独立运行提供虚拟类
    from dataclasses import dataclass
    from typing import List
    
    @dataclass
    class TaskSummary:
        task_id: str
        original_description: str
        title: str
        description: str
        objectives: List[str]
        constraints: List[str]
        expected_outputs: List[str]
        complexity_score: int
        estimated_hours: float
        deadline: Optional[str]
        requires_decomposition: bool
        keywords: List[str]
        created_at: str
        updated_at: str
        
        def to_markdown(self):
            return f"# {self.title}\n\n{self.description}"

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProjectManager:
    """项目管理器"""
    
    def __init__(self, task_summary: TaskSummary, config_path: Optional[str] = None):
        """
        初始化项目管理器
        
        Args:
            task_summary: 任务概要对象
            config_path: 配置文件路径
        """
        self.task_summary = task_summary
        self.config = self._load_config(config_path)
        
        # 项目基础目录
        self.base_dir = Path(self.config.get('project_base_dir', '/root/.openclaw/workspace/projects'))
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        # 项目路径
        self.project_dir = self._get_project_dir()
        
        logger.info(f"项目管理器初始化完成，项目目录: {self.project_dir}")
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """加载配置文件"""
        default_config = {
            'project_base_dir': '/root/.openclaw/workspace/projects',
            'backup': {
                'enabled': False,
                'local_backup_dir': '/root/.openclaw/backups'
            }
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                # 深度合并
                self._merge_configs(default_config, user_config)
            except Exception as e:
                logger.warning(f"加载配置文件失败，使用默认配置: {e}")
        
        return default_config
    
    def _merge_configs(self, default: Dict[str, Any], user: Dict[str, Any]):
        """深度合并配置字典"""
        for key, value in user.items():
            if key in default and isinstance(default[key], dict) and isinstance(value, dict):
                self._merge_configs(default[key], value)
            else:
                default[key] = value
    
    def _get_project_dir(self) -> Path:
        """获取项目目录路径"""
        # 使用任务ID作为目录名
        safe_id = self.task_summary.task_id.replace(':', '_').replace(' ', '_')
        project_dir = self.base_dir / safe_id
        
        # 如果目录已存在，添加后缀
        counter = 1
        original_dir = project_dir
        while project_dir.exists():
            project_dir = original_dir.parent / f"{original_dir.name}_{counter}"
            counter += 1
        
        return project_dir
    
    def create_project(self) -> Path:
        """
        创建项目文件夹结构
        
        Returns:
            Path: 项目目录路径
        """
        logger.info(f"创建项目: {self.project_dir}")
        
        # 创建目录结构
        directories = [
            self.project_dir,
            self.project_dir / 'steps',
            self.project_dir / 'final_output',
            self.project_dir / 'backup',
            self.project_dir / 'logs'
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            logger.debug(f"创建目录: {directory}")
        
        # 生成核心文档
        self._create_task_summary()
        self._create_top_level_plan()
        self._create_config_file()
        self._create_readme()
        
        # 创建初始备份
        if self.config.get('backup', {}).get('enabled', False):
            self._create_backup()
        
        logger.info(f"项目创建完成: {self.project_dir}")
        return self.project_dir
    
    def _create_task_summary(self):
        """创建任务概要文档"""
        summary_file = self.project_dir / 'task_summary.md'
        
        # 使用任务分析器生成的Markdown
        content = self.task_summary.to_markdown()
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"创建任务概要: {summary_file}")
    
    def _create_top_level_plan(self):
        """创建顶层方案文档"""
        plan_file = self.project_dir / 'top_level_plan.md'
        
        # 根据复杂度生成不同的方案
        if self.task_summary.complexity_score >= 7:
            plan_content = self._generate_detailed_plan()
        elif self.task_summary.complexity_score >= 4:
            plan_content = self._generate_medium_plan()
        else:
            plan_content = self._generate_simple_plan()
        
        with open(plan_file, 'w', encoding='utf-8') as f:
            f.write(plan_content)
        
        logger.info(f"创建顶层方案: {plan_file}")
    
    def _generate_detailed_plan(self) -> str:
        """生成详细方案（复杂度≥7）"""
        return f"""# 顶层方案: {self.task_summary.title}

## 项目概述
- **任务ID**: {self.task_summary.task_id}
- **复杂度**: {self.task_summary.complexity_score}/10
- **预计耗时**: {self.task_summary.estimated_hours} 小时
- **创建时间**: {self.task_summary.created_at}

## 阶段划分

### 阶段一：调研与分析（预计: {self.task_summary.estimated_hours * 0.2:.1f} 小时）
1. 需求分析
2. 技术调研
3. 风险评估

### 阶段二：设计与规划（预计: {self.task_summary.estimated_hours * 0.3:.1f} 小时）
1. 架构设计
2. 接口设计
3. 数据库设计
4. 部署方案

### 阶段三：实施与开发（预计: {self.task_summary.estimated_hours * 0.4:.1f} 小时）
1. 环境搭建
2. 核心功能开发
3. 集成测试
4. 性能优化

### 阶段四：验证与交付（预计: {self.task_summary.estimated_hours * 0.1:.1f} 小时）
1. 系统测试
2. 文档编写
3. 交付部署

## 里程碑
1. 完成调研报告
2. 完成设计方案
3. 完成核心功能
4. 完成测试验证
5. 项目交付

## 依赖关系
```mermaid
graph TD
    A[需求分析] --> B[架构设计]
    B --> C[环境搭建]
    C --> D[核心功能开发]
    D --> E[集成测试]
    E --> F[系统测试]
    F --> G[交付部署]
```

## 风险管理
- **技术风险**: 新技术学习成本
- **时间风险**: 估计可能偏差
- **资源风险**: 系统资源限制

## 下一步行动
1. 细化阶段一的具体步骤
2. 分配具体任务
3. 开始执行
"""
    
    def _generate_medium_plan(self) -> str:
        """生成中等方案（复杂度4-6）"""
        return f"""# 顶层方案: {self.task_summary.title}

## 项目概述
- **任务ID**: {self.task_summary.task_id}
- **复杂度**: {self.task_summary.complexity_score}/10
- **预计耗时**: {self.task_summary.estimated_hours} 小时
- **创建时间**: {self.task_summary.created_at}

## 步骤分解

### 步骤一：准备阶段
1. 理解需求
2. 收集资料
3. 制定计划

### 步骤二：执行阶段
1. 主要工作
2. 辅助工作
3. 检查点

### 步骤三：收尾阶段
1. 验证结果
2. 整理文档
3. 交付成果

## 时间安排
- 准备阶段: {self.task_summary.estimated_hours * 0.3:.1f} 小时
- 执行阶段: {self.task_summary.estimated_hours * 0.5:.1f} 小时
- 收尾阶段: {self.task_summary.estimated_hours * 0.2:.1f} 小时

## 关键交付物
1. 主要成果
2. 相关文档
3. 测试报告

## 下一步行动
1. 开始步骤一的详细分解
2. 准备必要资源
3. 开始执行
"""
    
    def _generate_simple_plan(self) -> str:
        """生成简单方案（复杂度≤3）"""
        return f"""# 顶层方案: {self.task_summary.title}

## 任务信息
- **任务ID**: {self.task_summary.task_id}
- **复杂度**: {self.task_summary.complexity_score}/10
- **预计耗时**: {self.task_summary.estimated_hours} 小时
- **创建时间**: {self.task_summary.created_at}

## 执行步骤
1. 理解任务要求
2. 执行核心操作
3. 检查结果质量
4. 交付最终成果

## 注意事项
- 注意时间控制
- 确保质量达标
- 及时沟通问题

## 下一步行动
直接开始执行
"""
    
    def _create_config_file(self):
        """创建项目配置文件"""
        config_file = self.project_dir / 'project_config.json'
        
        project_config = {
            'task_id': self.task_summary.task_id,
            'title': self.task_summary.title,
            'complexity_score': self.task_summary.complexity_score,
            'estimated_hours': self.task_summary.estimated_hours,
            'created_at': self.task_summary.created_at,
            'updated_at': self.task_summary.updated_at,
            'requires_decomposition': self.task_summary.requires_decomposition,
            'project_dir': str(self.project_dir),
            'workflow_version': '0.1.0',
            'status': 'created'
        }
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(project_config, f, indent=2, ensure_ascii=False)
        
        logger.info(f"创建项目配置: {config_file}")
    
    def _create_readme(self):
        """创建项目README"""
        readme_file = self.project_dir / 'README.md'
        
        readme_content = f"""# 项目: {self.task_summary.title}

## 项目状态
- **状态**: 已创建 🟡
- **创建时间**: {self.task_summary.created_at}
- **最后更新**: {self.task_summary.updated_at}

## 项目结构
```
{self.project_dir.name}/
├── task_summary.md          # 任务概要
├── top_level_plan.md        # 顶层方案
├── project_config.json      # 项目配置
├── steps/                   # 步骤目录
├── final_output/            # 最终输出
├── backup/                  # 备份文件
└── logs/                    # 日志文件
```

## 快速开始
1. 阅读 `task_summary.md` 了解任务详情
2. 查看 `top_level_plan.md` 了解执行计划
3. 按照计划开始执行

## 工作流信息
- **工作流版本**: 小龙虾分层任务工作流 v0.1.0
- **复杂度评估**: {self.task_summary.complexity_score}/10
- **建议流程**: {'完整分层流程' if self.task_summary.requires_decomposition else '直接执行'}

## 联系方式
- 如有问题，请参考小龙虾工作流文档
- 或联系项目负责人
"""
        
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        logger.info(f"创建README: {readme_file}")
    
    def _create_backup(self):
        """创建初始备份"""
        backup_dir = Path(self.config['backup']['local_backup_dir'])
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建时间戳备份
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = backup_dir / f"{self.task_summary.task_id}_{timestamp}.zip"
        
        try:
            # 创建zip备份（简化实现）
            import zipfile
            with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(self.project_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, self.project_dir.parent)
                        zipf.write(file_path, arcname)
            
            logger.info(f"创建备份: {backup_file}")
        except Exception as e:
            logger.error(f"备份创建失败: {e}")
    
    def get_project_info(self) -> Dict[str, Any]:
        """获取项目信息"""
        return {
            'project_dir': str(self.project_dir),
            'task_id': self.task_summary.task_id,
            'title': self.task_summary.title,
            'status': 'created',
            'files': {
                'task_summary': str(self.project_dir / 'task_summary.md'),
                'top_level_plan': str(self.project_dir / 'top_level_plan.md'),
                'config': str(self.project_dir / 'project_config.json')
            }
        }
    
    def cleanup(self):
        """清理项目（慎用）"""
        if self.project_dir.exists():
            shutil.rmtree(self.project_dir)
            logger.warning(f"已清理项目: {self.project_dir}")


def test_project_manager():
    """测试项目管理器"""
    print("🧪 测试项目管理器...")
    
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
    
    # 创建项目管理器
    summary = TestTaskSummary()
    manager = ProjectManager(summary)
    
    # 创建项目
    project_dir = manager.create_project()
    
    print(f"✅ 项目创建成功: {project_dir}")
    
    # 显示项目信息
    info = manager.get_project_info()
    print(f"\n📋 项目信息:")
    print(f"  任务ID: {info['task_id']}")
    print(f"  标题: {info['title']}")
    print(f"  状态: {info['status']}")
    print(f"  文件:")
    for name, path in info['files'].items():
        print(f"    - {name}: {path}")
    
    # 检查文件是否存在
    print(f"\n📁 文件检查:")
    for name, path in info['files'].items():
        exists = os.path.exists(path)
        print(f"  {name}: {'✅ 存在' if exists else '❌ 缺失'}")
    
    print(f"\n{'='*50}")
    print("✅ 项目管理器测试完成")
    
    # 询问是否清理
    response = input("\n是否清理测试项目？(y/N): ").strip().lower()
    if response == 'y':
        manager.cleanup()
        print("已清理测试项目")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_project_manager()
    else:
        print("用法:")
        print("  python project_manager.py test")
        print("\n注意: 完整使用需要先创建 TaskSummary 对象")
        sys.exit(1)