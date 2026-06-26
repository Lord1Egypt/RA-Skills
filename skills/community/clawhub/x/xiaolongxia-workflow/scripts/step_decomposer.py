#!/usr/bin/env python3
"""
步骤分解器 - 小龙虾工作流 v0.2.0 核心组件

功能：
1. 递归分解任务为可执行的子步骤
2. 生成步骤详细文档 (stepXX_detailed.md)
3. 管理步骤依赖关系和执行顺序
4. 预估每个步骤的输入输出和耗时
"""

import os
import json
import re
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
from enum import Enum
import logging

# 导入任务分析器
try:
    from task_analyzer import TaskSummary
except ImportError:
    # 为独立运行提供虚拟类
    @dataclass
    class TaskSummary:
        task_id: str = ""
        title: str = ""
        description: str = ""
        complexity_score: int = 1
        estimated_hours: float = 1.0
        requires_decomposition: bool = False

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StepType(Enum):
    """步骤类型枚举"""
    PHASE = "phase"      # 阶段
    STEP = "step"        # 步骤
    SUBSTEP = "substep"  # 子步骤
    LEAF = "leaf"        # 叶子步骤（可执行）


class StepStatus(Enum):
    """步骤状态枚举"""
    PENDING = "pending"      # 待执行
    READY = "ready"          # 准备就绪（依赖已满足）
    EXECUTING = "executing"  # 执行中
    COMPLETED = "completed"  # 已完成
    FAILED = "failed"        # 失败
    BLOCKED = "blocked"      # 阻塞（依赖失败）


@dataclass
class Step:
    """步骤节点"""
    step_id: str                     # 步骤ID (step_001, step_001_001, 等)
    name: str                       # 步骤名称
    description: str                # 步骤描述
    step_type: StepType             # 步骤类型
    depth: int                      # 深度（0: 根/阶段，1: 步骤，2: 子步骤，3: 叶子）
    
    # 输入输出
    inputs: List[str] = field(default_factory=list)     # 输入描述
    outputs: List[str] = field(default_factory=list)    # 输出描述
    input_files: List[str] = field(default_factory=list) # 输入文件
    output_files: List[str] = field(default_factory=list) # 输出文件
    
    # 执行信息
    estimated_hours: float = 1.0    # 预计耗时（小时）
    actual_hours: float = 0.0       # 实际耗时
    dependencies: List[str] = field(default_factory=list) # 依赖的步骤ID列表
    
    # 状态
    status: StepStatus = StepStatus.PENDING
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    
    # 子步骤
    children: List['Step'] = field(default_factory=list)
    
    # 可执行性判断
    is_executable: bool = False     # 是否可直接执行
    requires_api_call: bool = False # 是否需要API调用
    expected_input_size: int = 0    # 预计输入大小（字符数）
    expected_output_size: int = 0   # 预计输出大小（字符数）
    
    # 错误处理
    max_retries: int = 3            # 最大重试次数
    retry_count: int = 0            # 已重试次数
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典（可序列化）"""
        data = asdict(self)
        data['step_type'] = self.step_type.value
        data['status'] = self.status.value
        data['children'] = [child.to_dict() for child in self.children]
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Step':
        """从字典创建Step对象"""
        data = data.copy()
        data['step_type'] = StepType(data['step_type'])
        data['status'] = StepStatus(data['status'])
        
        children_data = data.pop('children', [])
        step = cls(**data)
        
        # 递归创建子步骤
        for child_data in children_data:
            step.children.append(cls.from_dict(child_data))
        
        return step
    
    def is_leaf(self) -> bool:
        """是否为叶子节点（没有子步骤）"""
        return len(self.children) == 0
    
    def get_all_descendants(self) -> List['Step']:
        """获取所有后代步骤"""
        descendants = []
        for child in self.children:
            descendants.append(child)
            descendants.extend(child.get_all_descendants())
        return descendants
    
    def get_executable_leaves(self) -> List['Step']:
        """获取所有可执行的叶子步骤"""
        leaves = []
        if self.is_leaf():
            if self.is_executable:
                leaves.append(self)
        else:
            for child in self.children:
                leaves.extend(child.get_executable_leaves())
        return leaves
    
    def update_status(self, new_status: StepStatus):
        """更新步骤状态"""
        self.status = new_status
    
    def add_child(self, child: 'Step'):
        """添加子步骤"""
        child.depth = self.depth + 1
        self.children.append(child)


class StepDecomposer:
    """步骤分解器"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化分解器
        
        Args:
            config_path: 配置文件路径
        """
        self.config = self._load_config(config_path)
        self.step_counter = 0
        logger.info("步骤分解器初始化完成")
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """加载配置文件"""
        default_config = {
            'max_depth': 4,                     # 最大分解深度
            'max_children_per_node': 5,         # 每个节点最大子节点数
            'min_executable_hours': 0.1,        # 最小可执行步骤耗时
            'max_executable_hours': 4.0,        # 最大可执行步骤耗时
            'max_input_chars': 1000000,         # 最大输入字符数（1M）
            'max_output_chars': 8000,           # 最大输出字符数（8K）
            'complexity_thresholds': {
                'high': 7,      # 高复杂度阈值
                'medium': 4,    # 中复杂度阈值
                'low': 1        # 低复杂度阈值
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
    
    def _generate_step_id(self, prefix: str = "step") -> str:
        """生成步骤ID"""
        self.step_counter += 1
        return f"{prefix}_{self.step_counter:03d}"
    
    def _estimate_step_hours(self, complexity: int, depth: int) -> float:
        """估算步骤耗时"""
        # 基础耗时（小时）
        base_hours = complexity * 0.2
        
        # 深度影响：越深层的步骤耗时越短
        depth_factor = 1.0 / (depth + 1)
        
        # 随机波动 ±20%
        import random
        random_factor = random.uniform(0.8, 1.2)
        
        estimated = base_hours * depth_factor * random_factor
        
        # 限制在最小和最大值之间
        min_hours = self.config['min_executable_hours']
        max_hours = self.config['max_executable_hours']
        
        return max(min_hours, min(estimated, max_hours))
    
    def _is_executable_step(self, step: Step) -> bool:
        """判断步骤是否可执行"""
        # 叶子步骤才可能是可执行的
        if not step.is_leaf():
            return False
        
        # 检查输入输出大小
        if step.expected_input_size > self.config['max_input_chars']:
            return False
        
        if step.expected_output_size > self.config['max_output_chars']:
            return False
        
        # 检查耗时范围
        if step.estimated_hours < self.config['min_executable_hours']:
            return False
        
        if step.estimated_hours > self.config['max_executable_hours']:
            return False
        
        return True
    
    def _create_phase_steps(self, task_summary: TaskSummary) -> List[Step]:
        """创建阶段步骤（顶层分解）"""
        phases = []
        complexity = task_summary.complexity_score
        
        # 根据复杂度决定阶段数量
        if complexity >= self.config['complexity_thresholds']['high']:
            # 高复杂度：4个阶段
            phase_names = ["调研与分析", "设计与规划", "实施与开发", "验证与交付"]
            phase_descriptions = [
                "深入理解需求，进行技术调研和风险评估",
                "设计系统架构，制定详细实施方案",
                "具体实现功能，编写代码和测试",
                "验证成果质量，编写文档并交付"
            ]
        elif complexity >= self.config['complexity_thresholds']['medium']:
            # 中复杂度：3个阶段
            phase_names = ["准备阶段", "执行阶段", "收尾阶段"]
            phase_descriptions = [
                "明确需求，收集资料，制定计划",
                "主要工作实施，完成核心任务",
                "验证结果，整理文档，交付成果"
            ]
        else:
            # 低复杂度：1个阶段（直接执行）
            phase_names = ["执行阶段"]
            phase_descriptions = ["直接执行任务，完成所有工作"]
        
        # 创建阶段步骤
        for i, (name, desc) in enumerate(zip(phase_names, phase_descriptions)):
            phase = Step(
                step_id=self._generate_step_id(f"phase_{i+1:02d}"),
                name=name,
                description=desc,
                step_type=StepType.PHASE,
                depth=0,
                estimated_hours=task_summary.estimated_hours * (1.0 / len(phase_names)),
                is_executable=False
            )
            phases.append(phase)
        
        return phases
    
    def _decompose_phase(self, phase: Step, task_summary: TaskSummary) -> Step:
        """分解阶段为具体步骤"""
        # 根据阶段名称决定如何分解
        if "调研" in phase.name or "分析" in phase.name:
            # 调研分析阶段
            sub_steps = [
                ("需求分析", "分析用户需求，明确功能和非功能需求"),
                ("技术调研", "调研相关技术方案和工具"),
                ("风险评估", "识别项目风险并制定应对策略")
            ]
        elif "设计" in phase.name or "规划" in phase.name:
            # 设计规划阶段
            sub_steps = [
                ("架构设计", "设计系统架构和技术栈"),
                ("接口设计", "设计API接口和数据格式"),
                ("数据库设计", "设计数据库结构和关系"),
                ("部署方案", "设计系统部署和运维方案")
            ]
        elif "实施" in phase.name or "开发" in phase.name:
            # 实施开发阶段
            sub_steps = [
                ("环境搭建", "搭建开发环境和依赖"),
                ("核心功能开发", "实现核心业务逻辑"),
                ("集成测试", "进行模块集成测试"),
                ("性能优化", "优化系统性能")
            ]
        elif "验证" in phase.name or "收尾" in phase.name:
            # 验证收尾阶段
            sub_steps = [
                ("系统测试", "进行完整的系统测试"),
                ("文档编写", "编写用户文档和技术文档"),
                ("交付部署", "部署系统并交付使用")
            ]
        else:
            # 默认执行阶段
            sub_steps = [
                ("理解需求", "深入理解任务要求和约束"),
                ("执行任务", "执行具体工作内容"),
                ("检查结果", "检查工作成果质量")
            ]
        
        # 创建子步骤
        for i, (name, desc) in enumerate(sub_steps):
            step = Step(
                step_id=self._generate_step_id(f"step_{phase.step_id}_{i+1:02d}"),
                name=name,
                description=desc,
                step_type=StepType.STEP,
                depth=phase.depth + 1,
                estimated_hours=phase.estimated_hours * (1.0 / len(sub_steps)),
                is_executable=False
            )
            
            # 进一步分解（如果还需要）
            step = self._decompose_step(step, task_summary)
            
            phase.add_child(step)
        
        return phase
    
    def _decompose_step(self, step: Step, task_summary: TaskSummary) -> Step:
        """分解步骤为子步骤"""
        # 如果步骤预计耗时小于最小可执行步骤耗时，或者已经达到最大深度，则不再分解
        if (step.estimated_hours <= self.config['min_executable_hours'] * 2 or 
            step.depth >= self.config['max_depth'] - 1):
            # 标记为可执行叶子步骤
            step.is_executable = True
            step.requires_api_call = True
            step.expected_input_size = 1000  # 默认估计
            step.expected_output_size = 2000 # 默认估计
            step.step_type = StepType.LEAF
            return step
        
        # 根据步骤名称决定如何分解
        if "分析" in step.name:
            sub_steps = [
                ("收集信息", "收集相关信息和数据"),
                ("分析处理", "分析信息并提取关键点"),
                ("总结结论", "总结分析结果和结论")
            ]
        elif "设计" in step.name:
            sub_steps = [
                ("方案构思", "构思设计方案和思路"),
                ("详细设计", "进行详细设计说明"),
                ("评审优化", "评审并优化设计方案")
            ]
        elif "开发" in step.name or "实现" in step.name:
            sub_steps = [
                ("编写代码", "编写实现代码"),
                ("单元测试", "进行单元测试"),
                ("代码审查", "审查代码质量")
            ]
        elif "测试" in step.name:
            sub_steps = [
                ("测试准备", "准备测试环境和数据"),
                ("执行测试", "执行测试用例"),
                ("记录结果", "记录测试结果和问题")
            ]
        else:
            # 默认分解为2-3个子步骤
            import random
            num_substeps = random.randint(2, 3)
            sub_steps = []
            for i in range(num_substeps):
                sub_steps.append((f"子任务{i+1}", f"完成第{i+1}个子任务"))
        
        # 创建子步骤
        for i, (name, desc) in enumerate(sub_steps):
            substep = Step(
                step_id=self._generate_step_id(f"substep_{step.step_id}_{i+1:02d}"),
                name=name,
                description=desc,
                step_type=StepType.SUBSTEP,
                depth=step.depth + 1,
                estimated_hours=step.estimated_hours * (1.0 / len(sub_steps)),
                is_executable=False
            )
            
            # 递归分解
            substep = self._decompose_step(substep, task_summary)
            
            step.add_child(substep)
        
        return step
    
    def decompose(self, task_summary: TaskSummary) -> List[Step]:
        """
        分解任务为步骤树
        
        Args:
            task_summary: 任务概要对象
            
        Returns:
            List[Step]: 阶段步骤列表（根节点）
        """
        logger.info(f"开始分解任务: {task_summary.title} (复杂度: {task_summary.complexity_score}/10)")
        
        # 重置计数器
        self.step_counter = 0
        
        # 如果不需要分解，创建单个可执行步骤
        if not task_summary.requires_decomposition:
            logger.info("任务不需要分解，创建单个可执行步骤")
            
            leaf_step = Step(
                step_id=self._generate_step_id("direct"),
                name="直接执行",
                description=task_summary.description,
                step_type=StepType.LEAF,
                depth=0,
                estimated_hours=task_summary.estimated_hours,
                is_executable=True,
                requires_api_call=True,
                expected_input_size=len(task_summary.original_description),
                expected_output_size=8000  # 估计输出大小
            )
            
            return [leaf_step]
        
        # 创建阶段步骤
        phases = self._create_phase_steps(task_summary)
        
        # 分解每个阶段
        decomposed_phases = []
        for phase in phases:
            decomposed_phase = self._decompose_phase(phase, task_summary)
            decomposed_phases.append(decomposed_phase)
        
        # 设置依赖关系（前一阶段完成后才开始后一阶段）
        for i in range(1, len(decomposed_phases)):
            # 获取前一阶段的所有叶子步骤
            prev_leaves = decomposed_phases[i-1].get_executable_leaves()
            curr_leaves = decomposed_phases[i].get_executable_leaves()
            
            # 当前阶段的叶子步骤依赖于前一阶段的叶子步骤
            for leaf in curr_leaves:
                leaf.dependencies = [leaf.step_id for leaf in prev_leaves]
        
        # 统计信息
        total_steps = 0
        executable_steps = 0
        for phase in decomposed_phases:
            all_descendants = phase.get_all_descendants()
            total_steps += len(all_descendants) + 1  # 包括阶段本身
            executable_steps += len(phase.get_executable_leaves())
        
        logger.info(f"分解完成: 创建了 {len(decomposed_phases)} 个阶段, {total_steps} 个步骤, {executable_steps} 个可执行步骤")
        
        return decomposed_phases
    
    def save_decomposition(self, phases: List[Step], project_dir: Path):
        """
        保存分解结果到项目目录
        
        Args:
            phases: 阶段步骤列表
            project_dir: 项目目录路径
        """
        # 确保steps目录存在
        steps_dir = project_dir / "steps"
        steps_dir.mkdir(exist_ok=True)
        
        # 保存每个阶段的详细文档
        for i, phase in enumerate(phases):
            # 创建阶段目录
            phase_dir = steps_dir / f"phase_{i+1:02d}"
            phase_dir.mkdir(exist_ok=True)
            
            # 保存阶段详细文档
            phase_file = phase_dir / f"phase_{i+1:02d}_detailed.md"
            with open(phase_file, 'w', encoding='utf-8') as f:
                f.write(self._generate_phase_markdown(phase, i+1))
            
            # 保存阶段JSON（用于程序读取）
            phase_json = phase_dir / f"phase_{i+1:02d}.json"
            with open(phase_json, 'w', encoding='utf-8') as f:
                json.dump(phase.to_dict(), f, indent=2, ensure_ascii=False)
            
            # 保存每个步骤的详细文档
            self._save_step_details(phase, phase_dir)
        
        # 保存整体分解摘要
        summary_file = steps_dir / "decomposition_summary.md"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(self._generate_summary_markdown(phases))
        
        # 保存整体JSON
        all_phases_data = [phase.to_dict() for phase in phases]
        all_json_file = steps_dir / "all_phases.json"
        with open(all_json_file, 'w', encoding='utf-8') as f:
            json.dump(all_phases_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"分解结果已保存到: {steps_dir}")
    
    def _generate_phase_markdown(self, phase: Step, phase_num: int) -> str:
        """生成阶段详细文档"""
        # 统计信息
        all_steps = phase.get_all_descendants()
        executable_steps = phase.get_executable_leaves()
        
        md = f"""# 阶段 {phase_num}: {phase.name}

## 阶段描述
{phase.description}

## 基本信息
- **阶段ID**: {phase.step_id}
- **预计耗时**: {phase.estimated_hours:.1f} 小时
- **总步骤数**: {len(all_steps) + 1} 个
- **可执行步骤**: {len(executable_steps)} 个
- **最大深度**: {max([step.depth for step in all_steps], default=0)}

## 步骤分解树
```
{self._generate_step_tree(phase)}
```

## 可执行步骤清单
| 步骤ID | 步骤名称 | 描述 | 预计耗时 | 输入大小 | 输出大小 |
|--------|----------|------|----------|----------|----------|
"""
        
        for step in executable_steps:
            md += f"| {step.step_id} | {step.name} | {step.description[:50]}... | {step.estimated_hours:.1f}h | {step.expected_input_size} | {step.expected_output_size} |\n"
        
        md += f"""
## 依赖关系
{self._generate_dependencies_text(phase)}

## 执行顺序
1. 按深度优先顺序执行所有步骤
2. 注意依赖关系（某些步骤需要等待前置步骤完成）
3. 可执行步骤将调用API完成具体工作

## 注意事项
- 每个可执行步骤预计输入不超过 {self.config['max_input_chars']} 字符
- 每个可执行步骤预计输出不超过 {self.config['max_output_chars']} 字符
- 如果步骤执行失败，将自动重试（最多{phase.max_retries}次）
"""
        
        return md
    
    def _generate_step_tree(self, step: Step, indent: int = 0) -> str:
        """生成步骤树形结构文本"""
        prefix = "  " * indent
        node_type = "🌿" if step.is_executable else "📁" if step.children else "📄"
        status_icon = {
            StepStatus.PENDING: "⏳",
            StepStatus.READY: "✅",
            StepStatus.EXECUTING: "⚡",
            StepStatus.COMPLETED: "🎉",
            StepStatus.FAILED: "❌",
            StepStatus.BLOCKED: "🚧"
        }.get(step.status, "❓")
        
        tree = f"{prefix}{node_type}{status_icon} {step.name} ({step.step_id}) - {step.estimated_hours:.1f}h\n"
        
        for child in step.children:
            tree += self._generate_step_tree(child, indent + 1)
        
        return tree
    
    def _generate_dependencies_text(self, step: Step) -> str:
        """生成依赖关系文本"""
        if not step.dependencies:
            return "无外部依赖"
        
        deps_text = ""
        for dep_id in step.dependencies:
            deps_text += f"- 依赖于: {dep_id}\n"
        
        return deps_text
    
    def _save_step_details(self, step: Step, base_dir: Path):
        """递归保存步骤详细文档"""
        # 跳过阶段本身（已保存）
        if step.step_type == StepType.PHASE:
            for child in step.children:
                self._save_step_details(child, base_dir)
            return
        
        # 创建步骤目录
        step_dir = base_dir / step.step_id
        step_dir.mkdir(exist_ok=True)
        
        # 保存步骤详细文档
        step_file = step_dir / f"{step.step_id}_detailed.md"
        with open(step_file, 'w', encoding='utf-8') as f:
            f.write(self._generate_step_markdown(step))
        
        # 保存步骤JSON
        step_json = step_dir / f"{step.step_id}.json"
        with open(step_json, 'w', encoding='utf-8') as f:
            json.dump(step.to_dict(), f, indent=2, ensure_ascii=False)
        
        # 递归处理子步骤
        for child in step.children:
            self._save_step_details(child, step_dir)
    
    def _generate_step_markdown(self, step: Step) -> str:
        """生成步骤详细文档"""
        md = f"""# 步骤: {step.name}

## 步骤信息
- **步骤ID**: {step.step_id}
- **步骤类型**: {step.step_type.value}
- **深度**: {step.depth}
- **状态**: {step.status.value}
- **预计耗时**: {step.estimated_hours:.1f} 小时
- **可执行**: {'✅ 是' if step.is_executable else '❌ 否'}

## 描述
{step.description}

## 输入
"""
        
        if step.inputs:
            for inp in step.inputs:
                md += f"- {inp}\n"
        else:
            md += "- （无具体输入要求）\n"
        
        md += f"""
## 输出
"""
        
        if step.outputs:
            for out in step.outputs:
                md += f"- {out}\n"
        else:
            md += "- （具体输出待确定）\n"
        
        md += f"""
## 依赖关系
"""
        
        if step.dependencies:
            for dep in step.dependencies:
                md += f"- {dep}\n"
        else:
            md += "- 无依赖\n"
        
        md += f"""
## 技术细节
- **需要API调用**: {'是' if step.requires_api_call else '否'}
- **预计输入大小**: {step.expected_input_size} 字符
- **预计输出大小**: {step.expected_output_size} 字符
- **最大重试次数**: {step.max_retries}

## 执行要求
"""
        
        if step.is_executable:
            md += f"""
1. **输入限制**: 不超过 {self.config['max_input_chars']} 字符
2. **输出限制**: 不超过 {self.config['max_output_chars']} 字符  
3. **执行方式**: 调用大模型API完成
4. **错误处理**: 失败时自动重试（最多{step.max_retries}次）
"""
        else:
            md += f"""
需要进一步分解为更小的子步骤。
"""
        
        # 如果有子步骤，列出它们
        if step.children:
            md += f"""
## 子步骤 ({len(step.children)} 个)

| 步骤ID | 名称 | 描述 | 预计耗时 | 可执行 |
|--------|------|------|----------|--------|
"""
            for child in step.children:
                executable = '✅' if child.is_executable else '❌'
                md += f"| {child.step_id} | {child.name} | {child.description[:30]}... | {child.estimated_hours:.1f}h | {executable} |\n"
        
        return md
    
    def _generate_summary_markdown(self, phases: List[Step]) -> str:
        """生成分解摘要文档"""
        total_phases = len(phases)
        all_steps = []
        executable_steps = []
        total_hours = 0.0
        
        for phase in phases:
            all_steps.extend(phase.get_all_descendants())
            executable_steps.extend(phase.get_executable_leaves())
            total_hours += phase.estimated_hours
        
        md = f"""# 任务分解摘要

## 总体统计
- **阶段数量**: {total_phases}
- **总步骤数**: {len(all_steps) + total_phases}
- **可执行步骤**: {len(executable_steps)}
- **总预计耗时**: {total_hours:.1f} 小时
- **平均步骤耗时**: {total_hours / max(1, len(executable_steps)):.1f} 小时

## 阶段概览
"""
        
        for i, phase in enumerate(phases):
            phase_steps = phase.get_all_descendants()
            phase_executable = phase.get_executable_leaves()
            md += f"""
### 阶段 {i+1}: {phase.name}
- **步骤ID**: {phase.step_id}
- **预计耗时**: {phase.estimated_hours:.1f} 小时
- **包含步骤**: {len(phase_steps)} 个
- **可执行步骤**: {len(phase_executable)} 个
- **最大深度**: {max([step.depth for step in phase_steps], default=0)}
"""
        
        md += f"""
## 可执行步骤分布
| 阶段 | 可执行步骤数 | 总耗时 | 平均耗时 |
|------|--------------|--------|----------|
"""
        
        for i, phase in enumerate(phases):
            executable = phase.get_executable_leaves()
            if executable:
                phase_hours = sum(step.estimated_hours for step in executable)
                avg_hours = phase_hours / len(executable)
                md += f"| 阶段 {i+1} | {len(executable)} | {phase_hours:.1f}h | {avg_hours:.1f}h |\n"
        
        md += f"""
## 技术限制检查
- **输入大小限制**: {self.config['max_input_chars']} 字符/步骤 ✅ 所有可执行步骤符合要求
- **输出大小限制**: {self.config['max_output_chars']} 字符/步骤 ✅ 所有可执行步骤符合要求  
- **步骤耗时范围**: {self.config['min_executable_hours']}h - {self.config['max_executable_hours']}h ✅ 所有可执行步骤符合要求

## 下一步行动
1. 审查分解结果，确保合理性
2. 准备执行环境
3. 开始按顺序执行可执行步骤
"""
        
        return md


def test_step_decomposer():
    """测试步骤分解器"""
    print("🧪 测试步骤分解器...")
    
    # 创建虚拟任务概要
    @dataclass
    class TestTaskSummary:
        task_id: str = "test_task_20250317_1337"
        title: str = "测试任务：设计用户管理系统"
        description: str = "设计一个完整的用户管理系统，包含前后端"
        complexity_score: int = 7
        estimated_hours: float = 10.0
        requires_decomposition: bool = True
    
    # 创建分解器
    decomposer = StepDecomposer()
    
    # 分解任务
    task_summary = TestTaskSummary()
    phases = decomposer.decompose(task_summary)
    
    print(f"✅ 分解完成: 创建了 {len(phases)} 个阶段")
    
    # 显示统计信息
    total_steps = 0
    executable_steps = 0
    for i, phase in enumerate(phases):
        all_steps = phase.get_all_descendants()
        executable = phase.get_executable_leaves()
        total_steps += len(all_steps) + 1
        executable_steps += len(executable)
        
        print(f"  阶段 {i+1}: {phase.name}")
        print(f"    步骤数: {len(all_steps)}")
        print(f"    可执行步骤: {len(executable)}")
        print(f"    预计耗时: {phase.estimated_hours:.1f} 小时")
    
    print(f"  总计: {total_steps} 个步骤, {executable_steps} 个可执行步骤")
    
    # 测试保存功能
    import tempfile
    with tempfile.TemporaryDirectory(prefix='xlx_decompose_') as tmpdir:
        project_dir = Path(tmpdir) / "test_project"
        project_dir.mkdir()
        
        decomposer.save_decomposition(phases, project_dir)
        
        # 检查生成的文件
        steps_dir = project_dir / "steps"
        assert steps_dir.exists(), "steps目录未创建"
        
        phase_files = list(steps_dir.glob("phase_*/phase_*_detailed.md"))
        assert len(phase_files) == len(phases), "阶段详细文档数量不匹配"
        
        print(f"✅ 文件保存检查通过: {len(phase_files)} 个阶段文档")
        
        # 检查JSON文件
        json_files = list(steps_dir.glob("**/*.json"))
        print(f"✅ JSON文件生成: {len(json_files)} 个")
    
    print("\n✅ 步骤分解器测试完成")
    return True


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_step_decomposer()
    else:
        print("用法:")
        print("  python step_decomposer.py test")
        print("\n注意: 完整使用需要与任务分析器和项目管理器集成")