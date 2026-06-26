#!/usr/bin/env python3
"""
鲁棒执行器 - 小龙虾工作流 v0.3.0 核心组件

功能：
1. 集成错误分类器和恢复策略
2. 自动错误检测和恢复
3. 智能重试机制
4. 执行监控和报告
"""

import time
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime
import logging

from step_executor import StepExecutor, Step, ExecutionResult
from error_classifier import ErrorClassifier, ErrorInfo, RecoveryStrategy

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RobustStepExecutor(StepExecutor):
    """鲁棒执行器（带错误恢复）"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化鲁棒执行器
        
        Args:
            config_path: 配置文件路径
        """
        super().__init__(config_path)
        self.error_classifier = ErrorClassifier(config_path)
        self.recovery_attempts: Dict[str, List[Dict[str, Any]]] = {}  # 步骤ID -> 恢复尝试记录
        
        # 覆盖配置，启用实际执行
        self.config['use_mock_execution'] = False
        logger.info("鲁棒执行器初始化完成")
    
    def _classify_execution_error(self, result: ExecutionResult, step: Step) -> ErrorInfo:
        """分类执行错误"""
        error_message = result.error_message or "执行失败"
        
        # 构建错误上下文
        context = {
            'input_size': step.expected_input_size,
            'output_size': step.expected_output_size,
            'retry_count': step.retry_count,
            'step_type': step.step_type.value if hasattr(step.step_type, 'value') else str(step.step_type),
        }
        
        # 分类错误
        error_info = self.error_classifier.classify(error_message, context=context)
        return error_info
    
    def _apply_recovery_strategy(self, strategy: RecoveryStrategy, step: Step, 
                                project_dir: Path, error_info: ErrorInfo) -> bool:
        """应用恢复策略"""
        logger.info(f"应用恢复策略: {strategy.name} (步骤: {step.step_id})")
        
        # 记录恢复尝试
        if step.step_id not in self.recovery_attempts:
            self.recovery_attempts[step.step_id] = []
        
        attempt_record = {
            'strategy': strategy.name,
            'error_type': error_info.error_type.value,
            'start_time': datetime.now().isoformat(),
            'success': False,
            'notes': ''
        }
        
        # 执行恢复操作
        try:
            # 根据策略类型执行不同操作
            if strategy.name == "延迟重试":
                # 简单延迟后重试
                delay = strategy.estimated_time_seconds
                logger.info(f"延迟 {delay} 秒后重试...")
                time.sleep(delay)
                success = True
                
            elif strategy.name == "降低请求频率":
                # 降低并发度或增加间隔
                logger.info("降低请求频率...")
                self.config['max_concurrent_steps'] = max(1, self.config['max_concurrent_steps'] - 1)
                success = True
                
            elif strategy.name == "拆分输入":
                # 标记步骤需要拆分
                logger.info("标记步骤需要拆分输入...")
                step.requires_split = True
                success = True
                
            elif strategy.name == "压缩输入":
                # 标记步骤需要压缩
                logger.info("标记步骤需要压缩输入...")
                step.requires_compression = True
                success = True
                
            elif strategy.name == "切换端点":
                # 标记需要切换端点
                logger.info("标记需要切换端点...")
                step.requires_endpoint_switch = True
                success = True
                
            elif strategy.name == "增加超时时间":
                # 增加超时配置
                logger.info("增加超时时间...")
                self.config['default_timeout_minutes'] += 5
                success = True
                
            elif strategy.name == "优化请求":
                # 标记需要优化
                logger.info("标记需要优化请求...")
                step.requires_optimization = True
                success = True
                
            else:  # 基本重试
                logger.info("执行基本重试...")
                success = True
            
            attempt_record['success'] = success
            attempt_record['end_time'] = datetime.now().isoformat()
            attempt_record['notes'] = f"执行成功: {success}"
            
        except Exception as e:
            logger.error(f"恢复策略执行失败: {e}")
            attempt_record['success'] = False
            attempt_record['end_time'] = datetime.now().isoformat()
            attempt_record['notes'] = f"异常: {e}"
            success = False
        
        # 记录尝试
        self.recovery_attempts[step.step_id].append(attempt_record)
        
        # 学习记录
        actual_time = (datetime.fromisoformat(attempt_record['end_time']) - 
                      datetime.fromisoformat(attempt_record['start_time'])).total_seconds()
        self.error_classifier.record_recovery_result(strategy, success, actual_time)
        
        return success
    
    def _execute_step_with_recovery(self, step: Step, project_dir: Path) -> ExecutionResult:
        """执行步骤（带错误恢复）"""
        max_recovery_attempts = 3
        recovery_attempts = 0
        
        while recovery_attempts <= max_recovery_attempts:
            # 执行步骤
            result = super()._execute_step_real(step, project_dir)
            
            # 如果成功，返回结果
            if result.success:
                return result
            
            # 如果失败且已达到最大重试次数
            if step.retry_count >= step.max_retries:
                logger.warning(f"步骤 {step.step_id} 已达到最大重试次数，不再尝试恢复")
                return result
            
            # 分类错误
            error_info = self._classify_execution_error(result, step)
            
            # 获取恢复策略
            strategies = self.error_classifier.get_recovery_strategies(error_info)
            if not strategies:
                logger.warning(f"没有可用的恢复策略，步骤 {step.step_id} 失败")
                return result
            
            # 选择策略（考虑已尝试的策略）
            available_prerequisites = []  # 可以扩展
            strategy = self.error_classifier.recommend_strategy(error_info, available_prerequisites)
            
            if not strategy:
                logger.warning(f"没有推荐的恢复策略，步骤 {step.step_id} 失败")
                return result
            
            # 检查是否已尝试过此策略
            if step.step_id in self.recovery_attempts:
                attempted_strategies = [a['strategy'] for a in self.recovery_attempts[step.step_id]]
                if strategy.name in attempted_strategies:
                    logger.info(f"策略 {strategy.name} 已尝试过，尝试其他策略...")
                    # 尝试下一个策略
                    for alt_strategy in strategies:
                        if alt_strategy.name != strategy.name and alt_strategy.name not in attempted_strategies:
                            strategy = alt_strategy
                            break
                    else:
                        logger.warning(f"所有策略都已尝试，步骤 {step.step_id} 失败")
                        return result
            
            # 应用恢复策略
            recovery_success = self._apply_recovery_strategy(strategy, step, project_dir, error_info)
            
            if not recovery_success:
                logger.warning(f"恢复策略 {strategy.name} 执行失败")
                recovery_attempts += 1
                continue
            
            # 恢复策略成功，增加重试计数
            step.retry_count += 1
            recovery_attempts += 1
            
            logger.info(f"恢复策略 {strategy.name} 应用成功，准备重试步骤 (尝试 {recovery_attempts}/{max_recovery_attempts})")
        
        # 达到最大恢复尝试次数
        return result
    
    def _execute_step_real(self, step: Step, project_dir: Path) -> ExecutionResult:
        """
        实际执行步骤（重写父类方法，集成错误恢复）
        
        Args:
            step: 步骤对象
            project_dir: 项目目录
            
        Returns:
            ExecutionResult: 执行结果
        """
        # 如果配置使用模拟执行，调用父类方法
        if self.config.get('use_mock_execution', False):
            return super()._execute_step_real(step, project_dir)
        
        # 否则使用带恢复的执行
        return self._execute_step_with_recovery(step, project_dir)
    
    def get_recovery_stats(self) -> Dict[str, Any]:
        """获取恢复统计信息"""
        total_attempts = 0
        successful_attempts = 0
        by_strategy = {}
        
        for step_id, attempts in self.recovery_attempts.items():
            for attempt in attempts:
                total_attempts += 1
                if attempt['success']:
                    successful_attempts += 1
                
                strategy = attempt['strategy']
                by_strategy[strategy] = by_strategy.get(strategy, 0) + 1
        
        error_stats = self.error_classifier.get_error_stats()
        
        return {
            'total_recovery_attempts': total_attempts,
            'successful_recoveries': successful_attempts,
            'recovery_success_rate': successful_attempts / total_attempts if total_attempts > 0 else 0,
            'attempts_by_strategy': by_strategy,
            'error_stats': error_stats,
            'recent_attempts': list(self.recovery_attempts.values())[-5:] if self.recovery_attempts else []
        }
    
    def generate_enhanced_report(self, project_dir: Path) -> str:
        """生成增强报告（包含恢复信息）"""
        # 生成基本报告
        basic_report = super().generate_execution_report(project_dir)
        
        # 获取恢复统计
        recovery_stats = self.get_recovery_stats()
        
        # 添加恢复信息
        enhanced_report = basic_report + f"""

## 错误恢复统计

### 恢复尝试
- **总恢复尝试**: {recovery_stats['total_recovery_attempts']}
- **成功恢复**: {recovery_stats['successful_recoveries']}
- **恢复成功率**: {recovery_stats['recovery_success_rate']:.1%}

### 按策略统计
"""
        
        for strategy, count in recovery_stats['attempts_by_strategy'].items():
            enhanced_report += f"- **{strategy}**: {count} 次尝试\n"
        
        # 添加错误统计
        error_stats = recovery_stats['error_stats']
        if error_stats['total_errors'] > 0:
            enhanced_report += f"""
### 错误统计
- **总错误数**: {error_stats['total_errors']}
- **按类型分布**:
"""
            for error_type, count in error_stats.get('by_type', {}).items():
                enhanced_report += f"  - {error_type}: {count}\n"
        
        # 添加最近恢复尝试
        recent_attempts = recovery_stats.get('recent_attempts', [])
        if recent_attempts:
            enhanced_report += """
### 最近恢复尝试
| 步骤ID | 策略 | 成功 | 备注 |
|--------|------|------|------|
"""
            for attempts in recent_attempts:
                for attempt in attempts[-3:]:  # 每个步骤最近3次尝试
                    success_emoji = "✅" if attempt['success'] else "❌"
                    enhanced_report += f"| {attempt.get('step_id', 'N/A')} | {attempt['strategy']} | {success_emoji} | {attempt.get('notes', '')[:50]} |\n"
        
        enhanced_report += f"""
## 执行总结
鲁棒执行器成功处理了 {recovery_stats['total_recovery_attempts']} 次错误恢复尝试，整体恢复成功率为 {recovery_stats['recovery_success_rate']:.1%}。

**建议改进**:
1. 分析高频错误类型，优化步骤设计
2. 评估恢复策略效果，调整策略选择
3. 记录成功恢复模式，完善知识库

报告生成时间: {datetime.now().isoformat()}
"""
        
        # 保存增强报告
        report_file = project_dir / "enhanced_execution_report.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(enhanced_report)
        
        logger.info(f"增强报告已生成: {report_file}")
        
        return enhanced_report


def test_robust_executor():
    """测试鲁棒执行器"""
    print("🧪 测试鲁棒执行器...")
    
    # 创建虚拟步骤
    from step_decomposer import Step, StepType
    
    test_step = Step(
        step_id="test_robust_step_001",
        name="鲁棒测试步骤",
        description="这是一个测试鲁棒执行器的步骤",
        step_type=StepType.LEAF,
        depth=3,
        inputs=["测试输入"],
        outputs=["测试输出"],
        estimated_hours=0.5,
        is_executable=True,
        requires_api_call=True,
        expected_input_size=1000,
        expected_output_size=2000,
        max_retries=5
    )
    
    # 创建执行器
    executor = RobustStepExecutor()
    
    # 创建测试项目目录
    import tempfile
    from pathlib import Path
    
    with tempfile.TemporaryDirectory(prefix='xlx_robust_') as tmpdir:
        project_dir = Path(tmpdir) / "test_project"
        project_dir.mkdir()
        
        # 创建必要的目录结构
        (project_dir / "steps").mkdir()
        (project_dir / "outputs").mkdir()
        (project_dir / "logs").mkdir()
        
        print("✅ 鲁棒执行器初始化完成")
        
        # 测试错误分类集成
        print("测试错误分类集成...")
        error_msg = "Rate limit exceeded"
        error_info = executor.error_classifier.classify(error_msg, 429)
        print(f"  错误分类: {error_info.error_type.value}")
        print(f"  推荐策略: {executor.error_classifier.recommend_strategy(error_info).name}")
        
        # 测试恢复统计
        stats = executor.get_recovery_stats()
        print(f"  恢复统计: {stats['total_recovery_attempts']} 次尝试")
        
        print("\n✅ 鲁棒执行器测试完成")
    
    return True


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_robust_executor()
    else:
        print("用法:")
        print("  python robust_executor.py test")
        print("\n注意: 完整使用需要与工作流集成")