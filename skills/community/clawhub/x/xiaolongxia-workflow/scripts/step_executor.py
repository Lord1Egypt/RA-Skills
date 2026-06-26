#!/usr/bin/env python3
"""
步骤执行器 - 小龙虾工作流 v0.2.0 核心组件

功能：
1. 执行叶子步骤（调用子代理或API）
2. 管理步骤依赖和执行顺序
3. 处理错误和重试
4. 记录执行结果和日志
"""

import os
import json
import time
import subprocess
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
from datetime import datetime
import logging

# 导入步骤分解器
try:
    from step_decomposer import Step, StepStatus, StepType
except ImportError:
    # 为独立运行提供虚拟类
    from enum import Enum
    
    class StepStatus(Enum):
        PENDING = "pending"
        READY = "ready"
        EXECUTING = "executing"
        COMPLETED = "completed"
        FAILED = "failed"
        BLOCKED = "blocked"
    
    class StepType(Enum):
        PHASE = "phase"
        STEP = "step"
        SUBSTEP = "substep"
        LEAF = "leaf"
    
    @dataclass
    class Step:
        step_id: str = ""
        name: str = ""
        description: str = ""
        step_type: StepType = StepType.LEAF
        depth: int = 0
        inputs: List[str] = field(default_factory=list)
        outputs: List[str] = field(default_factory=list)
        estimated_hours: float = 1.0
        actual_hours: float = 0.0
        dependencies: List[str] = field(default_factory=list)
        status: StepStatus = StepStatus.PENDING
        start_time: Optional[str] = None
        end_time: Optional[str] = None
        children: List['Step'] = field(default_factory=list)
        is_executable: bool = False
        requires_api_call: bool = False
        expected_input_size: int = 0
        expected_output_size: int = 0
        max_retries: int = 3
        retry_count: int = 0
        
        def is_leaf(self):
            return len(self.children) == 0
        
        def get_all_descendants(self):
            return []
        
        def get_executable_leaves(self):
            return [self] if self.is_executable else []
        
        def update_status(self, new_status):
            self.status = new_status

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ExecutionResult:
    """执行结果"""
    step_id: str
    success: bool
    output: str
    start_time: str
    end_time: str
    actual_hours: float
    error_message: Optional[str] = None
    retry_count: int = 0
    token_usage: Optional[Dict[str, int]] = None  # 输入/输出token统计
    output_files: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'step_id': self.step_id,
            'success': self.success,
            'output': self.output,
            'error_message': self.error_message,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'actual_hours': self.actual_hours,
            'retry_count': self.retry_count,
            'token_usage': self.token_usage,
            'output_files': self.output_files
        }


class StepExecutor:
    """步骤执行器"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化执行器
        
        Args:
            config_path: 配置文件路径
        """
        self.config = self._load_config(config_path)
        self.results: Dict[str, ExecutionResult] = {}
        self.currently_executing: List[str] = []
        logger.info("步骤执行器初始化完成")
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """加载配置文件"""
        default_config = {
            'max_concurrent_steps': 1,           # 最大并发执行步骤数
            'default_timeout_minutes': 30,       # 默认超时时间（分钟）
            'retry_delay_seconds': 5,            # 重试延迟（秒）
            'max_retries': 3,                    # 最大重试次数
            'output_dir': 'outputs',             # 输出目录
            'log_dir': 'logs',                   # 日志目录
            'use_mock_execution': True,          # 是否使用模拟执行（开发阶段）
            'mock_success_rate': 0.9,            # 模拟执行成功率
            'mock_execution_time_seconds': 2,    # 模拟执行时间（秒）
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
    
    def _check_dependencies_met(self, step: Step, executed_steps: List[str]) -> bool:
        """检查步骤的依赖是否都已满足"""
        if not step.dependencies:
            return True
        
        for dep_id in step.dependencies:
            if dep_id not in executed_steps:
                return False
        
        return True
    
    def _prepare_input_for_step(self, step: Step, project_dir: Path) -> str:
        """为步骤准备输入"""
        # 简单实现：使用步骤描述作为输入
        input_text = f"""
# 任务步骤: {step.name}

## 步骤描述
{step.description}

## 输入要求
{chr(10).join(f'- {inp}' for inp in step.inputs) if step.inputs else '无具体输入要求'}

## 输出要求
{chr(10).join(f'- {out}' for out in step.outputs) if step.outputs else '请完成该步骤，输出具体结果'}

## 注意事项
- 请确保输出完整、准确
- 如有需要，可以分多个部分输出
- 如果遇到问题，请说明具体问题
"""
        
        # 如果步骤有输入文件，读取文件内容
        if hasattr(step, 'input_files') and step.input_files:
            for input_file in step.input_files:
                file_path = project_dir / input_file
                if file_path.exists():
                    try:
                        content = file_path.read_text(encoding='utf-8')
                        input_text += f"\n\n## 输入文件 {input_file} 内容:\n{content[:1000]}"
                    except Exception as e:
                        logger.warning(f"读取输入文件失败: {e}")
        
        return input_text
    
    def _execute_step_mock(self, step: Step, project_dir: Path) -> ExecutionResult:
        """模拟执行步骤（开发阶段使用）"""
        start_time = datetime.now().isoformat()
        
        # 模拟执行时间
        import random
        import time as time_module
        
        execution_time = self.config['mock_execution_time_seconds']
        time_module.sleep(execution_time)
        
        # 模拟成功率
        success = random.random() < self.config['mock_success_rate']
        
        end_time = datetime.now().isoformat()
        actual_hours = execution_time / 3600.0
        
        if success:
            output = f"""# 步骤执行结果: {step.name}

## 执行状态
✅ 步骤执行成功

## 执行详情
- **步骤ID**: {step.step_id}
- **步骤名称**: {step.name}
- **执行时间**: {execution_time:.1f} 秒
- **开始时间**: {start_time}
- **结束时间**: {end_time}

## 输出内容
已成功完成步骤 "{step.name}"。

根据步骤描述 "{step.description}"，已完成相关工作。

### 具体成果
1. 完成了步骤要求的主要工作
2. 检查了工作质量
3. 验证了输出符合预期

### 输出文件
- `{step.step_id}_output.txt` - 文本输出
- `{step.step_id}_report.md` - 步骤报告

## 下一步建议
继续执行下一个步骤。
"""
            error_message = None
        else:
            output = f"""# 步骤执行结果: {step.name}

## 执行状态
❌ 步骤执行失败

## 错误详情
模拟执行失败（随机失败测试）

## 建议操作
1. 检查步骤输入是否正确
2. 重试执行（最多 {step.max_retries} 次）
3. 如果多次失败，考虑修改步骤设计
"""
            error_message = "模拟执行随机失败"
        
        result = ExecutionResult(
            step_id=step.step_id,
            success=success,
            output=output,
            error_message=error_message,
            start_time=start_time,
            end_time=end_time,
            actual_hours=actual_hours,
            retry_count=step.retry_count
        )
        
        return result
    
    def _execute_step_real(self, step: Step, project_dir: Path) -> ExecutionResult:
        """实际执行步骤（调用子代理或API）"""
        # TODO: 实现实际执行逻辑
        # 1. 调用OpenClaw子代理
        # 2. 或直接调用模型API
        # 3. 或执行shell命令
        
        # 目前返回模拟结果
        return self._execute_step_mock(step, project_dir)
    
    def _save_execution_result(self, result: ExecutionResult, project_dir: Path):
        """保存执行结果"""
        # 创建输出目录
        output_dir = project_dir / self.config['output_dir'] / result.step_id
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 保存结果JSON
        result_file = output_dir / "execution_result.json"
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)
        
        # 保存输出文本
        output_file = output_dir / "output.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result.output)
        
        # 更新结果字典
        self.results[result.step_id] = result
        
        logger.info(f"执行结果已保存: {result_file}")
    
    def _update_step_status(self, step: Step, result: ExecutionResult, project_dir: Path):
        """更新步骤状态"""
        # 更新步骤对象
        if result.success:
            step.update_status(StepStatus.COMPLETED)
        else:
            if step.retry_count >= step.max_retries:
                step.update_status(StepStatus.FAILED)
            else:
                step.update_status(StepStatus.PENDING)
        
        step.start_time = result.start_time
        step.end_time = result.end_time
        step.actual_hours = result.actual_hours
        step.retry_count = result.retry_count
        
        # 更新步骤JSON文件
        step_file = project_dir / "steps" / f"{step.step_id}.json"
        if step_file.exists():
            try:
                with open(step_file, 'r', encoding='utf-8') as f:
                    step_data = json.load(f)
                
                # 更新状态信息
                step_data['status'] = step.status.value
                step_data['start_time'] = step.start_time
                step_data['end_time'] = step.end_time
                step_data['actual_hours'] = step.actual_hours
                step_data['retry_count'] = step.retry_count
                
                with open(step_file, 'w', encoding='utf-8') as f:
                    json.dump(step_data, f, indent=2, ensure_ascii=False)
                
                logger.debug(f"步骤状态已更新: {step_file}")
            except Exception as e:
                logger.warning(f"更新步骤状态失败: {e}")
    
    def execute_step(self, step: Step, project_dir: Path) -> ExecutionResult:
        """
        执行单个步骤
        
        Args:
            step: 步骤对象
            project_dir: 项目目录
            
        Returns:
            ExecutionResult: 执行结果
        """
        logger.info(f"开始执行步骤: {step.name} ({step.step_id})")
        
        # 检查步骤是否可执行
        if not step.is_executable:
            logger.warning(f"步骤 {step.step_id} 不可执行，跳过")
            return ExecutionResult(
                step_id=step.step_id,
                success=False,
                output=f"步骤 {step.name} 不可执行",
                error_message="步骤不可执行",
                start_time=datetime.now().isoformat(),
                end_time=datetime.now().isoformat(),
                actual_hours=0.0
            )
        
        # 准备输入
        input_text = self._prepare_input_for_step(step, project_dir)
        
        # 检查输入大小
        input_size = len(input_text)
        if input_size > step.expected_input_size and step.expected_input_size > 0:
            logger.warning(f"输入大小 {input_size} 超过预期 {step.expected_input_size}")
        
        # 执行步骤
        if self.config['use_mock_execution']:
            result = self._execute_step_mock(step, project_dir)
        else:
            result = self._execute_step_real(step, project_dir)
        
        # 保存结果
        self._save_execution_result(result, project_dir)
        
        # 更新步骤状态
        self._update_step_status(step, result, project_dir)
        
        # 记录日志
        if result.success:
            logger.info(f"步骤执行成功: {step.step_id}")
        else:
            logger.warning(f"步骤执行失败: {step.step_id} - {result.error_message}")
        
        return result
    
    def execute_steps(self, steps: List[Step], project_dir: Path, 
                     max_concurrent: Optional[int] = None) -> Dict[str, ExecutionResult]:
        """
        执行多个步骤
        
        Args:
            steps: 步骤列表
            project_dir: 项目目录
            max_concurrent: 最大并发数（默认使用配置）
            
        Returns:
            Dict[str, ExecutionResult]: 步骤ID到执行结果的映射
        """
        if not steps:
            logger.warning("没有可执行的步骤")
            return {}
        
        # 确定并发数
        concurrent_limit = max_concurrent or self.config['max_concurrent_steps']
        
        # 过滤可执行步骤
        executable_steps = [step for step in steps if step.is_executable]
        if not executable_steps:
            logger.warning("没有可执行的步骤")
            return {}
        
        logger.info(f"开始执行 {len(executable_steps)} 个步骤，并发限制: {concurrent_limit}")
        
        # 简单实现：顺序执行
        # TODO: 实现并发执行和依赖管理
        for step in executable_steps:
            # 检查依赖是否满足
            executed_ids = list(self.results.keys())
            if not self._check_dependencies_met(step, executed_ids):
                logger.warning(f"步骤 {step.step_id} 依赖未满足，跳过")
                continue
            
            # 执行步骤
            result = self.execute_step(step, project_dir)
            
            # 如果失败且可以重试，增加重试计数
            if not result.success and step.retry_count < step.max_retries:
                step.retry_count += 1
                logger.info(f"步骤 {step.step_id} 准备重试 ({step.retry_count}/{step.max_retries})")
                
                # 延迟后重试
                import time
                time.sleep(self.config['retry_delay_seconds'])
                
                result = self.execute_step(step, project_dir)
        
        return self.results
    
    def load_steps_from_project(self, project_dir: Path) -> List[Step]:
        """
        从项目目录加载步骤
        
        Args:
            project_dir: 项目目录
            
        Returns:
            List[Step]: 步骤列表
        """
        steps_dir = project_dir / "steps"
        if not steps_dir.exists():
            logger.warning(f"步骤目录不存在: {steps_dir}")
            return []
        
        # 加载all_phases.json
        all_phases_file = steps_dir / "all_phases.json"
        if not all_phases_file.exists():
            logger.warning(f"全阶段文件不存在: {all_phases_file}")
            return []
        
        try:
            with open(all_phases_file, 'r', encoding='utf-8') as f:
                phases_data = json.load(f)
            
            # 转换为Step对象
            from step_decomposer import Step as StepClass
            steps = []
            for phase_data in phases_data:
                phase = StepClass.from_dict(phase_data)
                steps.extend(phase.get_executable_leaves())
            
            logger.info(f"从项目加载了 {len(steps)} 个可执行步骤")
            return steps
        except Exception as e:
            logger.error(f"加载步骤失败: {e}")
            return []
    
    def generate_execution_report(self, project_dir: Path) -> str:
        """生成执行报告"""
        if not self.results:
            return "暂无执行结果"
        
        total_steps = len(self.results)
        successful_steps = sum(1 for r in self.results.values() if r.success)
        failed_steps = total_steps - successful_steps
        total_hours = sum(r.actual_hours for r in self.results.values())
        
        report = f"""# 步骤执行报告

## 执行统计
- **总步骤数**: {total_steps}
- **成功步骤**: {successful_steps}
- **失败步骤**: {failed_steps}
- **成功率**: {successful_steps/total_steps*100:.1f}%
- **总耗时**: {total_hours:.2f} 小时
- **平均步骤耗时**: {total_hours/total_steps*3600:.1f} 秒

## 步骤详情
| 步骤ID | 步骤名称 | 状态 | 耗时(小时) | 重试次数 | 开始时间 | 结束时间 |
|--------|----------|------|------------|----------|----------|----------|
"""
        
        for step_id, result in self.results.items():
            status = "✅ 成功" if result.success else "❌ 失败"
            report += f"| {step_id} | ... | {status} | {result.actual_hours:.3f} | {result.retry_count} | {result.start_time[11:19]} | {result.end_time[11:19]} |\n"
        
        report += f"""
## 失败分析
"""
        
        failed_results = [r for r in self.results.values() if not r.success]
        if failed_results:
            for result in failed_results:
                report += f"""
### 步骤 {result.step_id}
- **错误信息**: {result.error_message}
- **重试次数**: {result.retry_count}
"""
        else:
            report += "无失败步骤。\n"
        
        report += f"""
## 建议
1. 审查失败步骤，确定是否需要重试或修改设计
2. 分析耗时较长的步骤，考虑优化
3. 检查输出质量，确保符合预期

## 报告生成时间
{datetime.now().isoformat()}
"""
        
        # 保存报告
        report_file = project_dir / "execution_report.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"执行报告已生成: {report_file}")
        
        return report


def test_step_executor():
    """测试步骤执行器"""
    print("🧪 测试步骤执行器...")
    
    # 创建虚拟步骤
    from step_decomposer import Step, StepStatus, StepType
    
    test_step = Step(
        step_id="test_step_001",
        name="测试步骤",
        description="这是一个测试步骤，用于验证执行器功能",
        step_type=StepType.LEAF,
        depth=3,
        inputs=["测试输入"],
        outputs=["测试输出"],
        estimated_hours=0.5,
        is_executable=True,
        requires_api_call=True,
        expected_input_size=1000,
        expected_output_size=2000,
        max_retries=3
    )
    
    # 创建执行器
    executor = StepExecutor()
    
    # 创建测试项目目录
    import tempfile
    from pathlib import Path
    
    with tempfile.TemporaryDirectory(prefix='xlx_executor_') as tmpdir:
        project_dir = Path(tmpdir) / "test_project"
        project_dir.mkdir()
        
        # 创建必要的目录结构
        (project_dir / "steps").mkdir()
        (project_dir / "outputs").mkdir()
        (project_dir / "logs").mkdir()
        
        # 执行步骤
        result = executor.execute_step(test_step, project_dir)
        
        print(f"✅ 步骤执行完成")
        print(f"   成功: {result.success}")
        print(f"   耗时: {result.actual_hours:.3f} 小时")
        print(f"   重试: {result.retry_count} 次")
        
        # 检查结果文件
        output_dir = project_dir / "outputs" / test_step.step_id
        assert output_dir.exists(), "输出目录未创建"
        
        result_file = output_dir / "execution_result.json"
        assert result_file.exists(), "结果文件未创建"
        
        print(f"✅ 结果文件检查通过: {result_file}")
        
        # 测试加载步骤
        # 需要先创建all_phases.json
        all_phases_file = project_dir / "steps" / "all_phases.json"
        all_phases_data = [test_step.to_dict()]
        with open(all_phases_file, 'w', encoding='utf-8') as f:
            json.dump(all_phases_data, f, indent=2)
        
        steps = executor.load_steps_from_project(project_dir)
        print(f"✅ 步骤加载: {len(steps)} 个步骤")
        
        # 测试批量执行
        results = executor.execute_steps([test_step], project_dir)
        print(f"✅ 批量执行: {len(results)} 个结果")
        
        # 测试报告生成
        report = executor.generate_execution_report(project_dir)
        assert "步骤执行报告" in report
        print(f"✅ 报告生成检查通过")
    
    print("\n✅ 步骤执行器测试完成")
    return True


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_step_executor()
    else:
        print("用法:")
        print("  python step_executor.py test")
        print("\n注意: 完整使用需要与步骤分解器和项目管理器集成")