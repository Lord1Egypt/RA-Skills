"""
荞麦饼 Skills - 智能执行模块 v2.0
自适应执行引擎 + 预测性执行
"""

import asyncio
import time
from typing import Dict, List, Optional, Callable, Any, Union
from dataclasses import dataclass, field
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExecutionMode(Enum):
    """执行模式"""
    SIMPLE = "simple"           # 简单执行
    PARALLEL = "parallel"       # 并行执行
    PIPELINE = "pipeline"       # 流水线执行
    ADAPTIVE = "adaptive"       # 自适应执行


class TaskPriority(Enum):
    """任务优先级"""
    CRITICAL = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3


@dataclass
class Task:
    """任务定义"""
    id: str
    name: str
    func: Callable
    args: tuple = field(default_factory=tuple)
    kwargs: Dict = field(default_factory=dict)
    priority: TaskPriority = TaskPriority.NORMAL
    dependencies: List[str] = field(default_factory=list)
    timeout: float = 30.0
    retry_count: int = 3
    metadata: Dict = field(default_factory=dict)


@dataclass
class TaskResult:
    """任务结果"""
    task_id: str
    success: bool
    result: Any = None
    error: Optional[str] = None
    execution_time: float = 0.0
    retry_count: int = 0


@dataclass
class ExecutionPlan:
    """执行计划"""
    tasks: List[Task]
    mode: ExecutionMode
    estimated_time: float
    resources: Dict[str, Any]


class AdaptiveExecutor:
    """自适应执行引擎 v2.0"""
    
    def __init__(self, max_workers: int = 10):
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.task_history: List[Dict] = []
        self.performance_metrics = {
            "total_tasks": 0,
            "successful_tasks": 0,
            "failed_tasks": 0,
            "avg_execution_time": 0.0
        }
    
    def analyze_complexity(self, task_description: str) -> Dict:
        """分析任务复杂度"""
        # 基于关键词和长度分析
        complexity_indicators = {
            "high": ["深度", "全面", "详细", "复杂", "多步骤", "系统性"],
            "medium": ["分析", "研究", "比较", "评估"],
            "low": ["简单", "快速", "查询", "获取"]
        }
        
        score = 0
        indicators = []
        
        for level, words in complexity_indicators.items():
            for word in words:
                if word in task_description:
                    score += 1 if level == "high" else (0.5 if level == "medium" else 0.2)
                    indicators.append(word)
        
        # 长度因子
        length_factor = min(len(task_description) / 100, 1.0)
        
        total_score = score + length_factor
        
        if total_score > 2:
            complexity = "high"
            suggested_mode = ExecutionMode.PIPELINE
        elif total_score > 0.5:
            complexity = "medium"
            suggested_mode = ExecutionMode.PARALLEL
        else:
            complexity = "low"
            suggested_mode = ExecutionMode.SIMPLE
        
        return {
            "complexity": complexity,
            "score": total_score,
            "indicators": indicators,
            "suggested_mode": suggested_mode,
            "estimated_time": self._estimate_time(complexity)
        }
    
    def _estimate_time(self, complexity: str) -> float:
        """估计执行时间"""
        estimates = {
            "high": 60.0,
            "medium": 30.0,
            "low": 10.0
        }
        return estimates.get(complexity, 30.0)
    
    def create_execution_plan(self, tasks: List[Task], context: Dict = None) -> ExecutionPlan:
        """创建执行计划"""
        context = context or {}
        
        # 分析整体复杂度
        total_complexity = sum(
            self.analyze_complexity(t.name)["score"] 
            for t in tasks
        )
        
        # 确定执行模式
        if total_complexity > len(tasks) * 1.5:
            mode = ExecutionMode.PIPELINE
        elif len(tasks) > 3:
            mode = ExecutionMode.PARALLEL
        else:
            mode = ExecutionMode.SIMPLE
        
        # 计算预估时间
        estimated_time = sum(
            self._estimate_time(self.analyze_complexity(t.name)["complexity"])
            for t in tasks
        )
        
        # 资源规划
        resources = {
            "workers_needed": min(len(tasks), self.max_workers),
            "memory_estimate": len(tasks) * 100,  # MB
            "estimated_time": estimated_time
        }
        
        return ExecutionPlan(
            tasks=tasks,
            mode=mode,
            estimated_time=estimated_time,
            resources=resources
        )
    
    def execute(self, plan: ExecutionPlan, progress_callback: Callable = None) -> List[TaskResult]:
        """执行计划"""
        logger.info(f"开始执行计划: {plan.mode.value}, 预计 {plan.estimated_time:.1f}s")
        
        if plan.mode == ExecutionMode.SIMPLE:
            return self._execute_simple(plan.tasks, progress_callback)
        elif plan.mode == ExecutionMode.PARALLEL:
            return self._execute_parallel(plan.tasks, progress_callback)
        elif plan.mode == ExecutionMode.PIPELINE:
            return self._execute_pipeline(plan.tasks, progress_callback)
        else:
            return self._execute_adaptive(plan, progress_callback)
    
    def _execute_simple(self, tasks: List[Task], callback: Callable = None) -> List[TaskResult]:
        """简单顺序执行"""
        results = []
        for i, task in enumerate(tasks):
            result = self._execute_single(task)
            results.append(result)
            if callback:
                callback(i + 1, len(tasks), task.name)
        return results
    
    def _execute_parallel(self, tasks: List[Task], callback: Callable = None) -> List[TaskResult]:
        """并行执行"""
        results = []
        futures = {}
        
        # 提交所有任务
        for task in tasks:
            future = self.executor.submit(self._execute_single, task)
            futures[future] = task
        
        # 收集结果
        completed = 0
        for future in as_completed(futures):
            task = futures[future]
            try:
                result = future.result(timeout=task.timeout)
            except Exception as e:
                result = TaskResult(
                    task_id=task.id,
                    success=False,
                    error=str(e)
                )
            results.append(result)
            completed += 1
            if callback:
                callback(completed, len(tasks), task.name)
        
        return results
    
    def _execute_pipeline(self, tasks: List[Task], callback: Callable = None) -> List[TaskResult]:
        """流水线执行（考虑依赖）"""
        results = {}
        remaining = {t.id: t for t in tasks}
        completed = 0
        
        while remaining:
            # 找出可以执行的任务（依赖已满足）
            ready = []
            for task_id, task in list(remaining.items()):
                if all(dep in results for dep in task.dependencies):
                    ready.append(task)
                    del remaining[task_id]
            
            if not ready:
                raise ValueError("任务依赖存在循环")
            
            # 并行执行就绪任务
            futures = {self.executor.submit(self._execute_single, t): t for t in ready}
            
            for future in as_completed(futures):
                task = futures[future]
                try:
                    result = future.result(timeout=task.timeout)
                except Exception as e:
                    result = TaskResult(
                        task_id=task.id,
                        success=False,
                        error=str(e)
                    )
                results[task.id] = result
                completed += 1
                if callback:
                    callback(completed, len(tasks), task.name)
        
        return [results[t.id] for t in tasks]
    
    def _execute_adaptive(self, plan: ExecutionPlan, callback: Callable = None) -> List[TaskResult]:
        """自适应执行（动态调整）"""
        # 先尝试并行
        start_time = time.time()
        results = self._execute_parallel(plan.tasks, callback)
        elapsed = time.time() - start_time
        
        # 如果超时或失败率高，切换到流水线
        failed_count = sum(1 for r in results if not r.success)
        
        if elapsed > plan.estimated_time * 1.5 or failed_count > len(results) * 0.3:
            logger.info("切换到流水线模式重试")
            results = self._execute_pipeline(plan.tasks, callback)
        
        return results
    
    def _execute_single(self, task: Task) -> TaskResult:
        """执行单个任务"""
        start_time = time.time()
        retry = 0
        
        while retry < task.retry_count:
            try:
                result = task.func(*task.args, **task.kwargs)
                execution_time = time.time() - start_time
                
                # 更新指标
                self._update_metrics(True, execution_time)
                
                return TaskResult(
                    task_id=task.id,
                    success=True,
                    result=result,
                    execution_time=execution_time,
                    retry_count=retry
                )
            except Exception as e:
                retry += 1
                logger.warning(f"任务 {task.name} 失败 (重试 {retry}/{task.retry_count}): {e}")
                time.sleep(0.5 * retry)  # 指数退避
        
        execution_time = time.time() - start_time
        self._update_metrics(False, execution_time)
        
        return TaskResult(
            task_id=task.id,
            success=False,
            error=f"重试 {task.retry_count} 次后仍失败",
            execution_time=execution_time,
            retry_count=retry
        )
    
    def _update_metrics(self, success: bool, execution_time: float):
        """更新性能指标"""
        self.performance_metrics["total_tasks"] += 1
        if success:
            self.performance_metrics["successful_tasks"] += 1
        else:
            self.performance_metrics["failed_tasks"] += 1
        
        # 更新平均时间
        total = self.performance_metrics["total_tasks"]
        current_avg = self.performance_metrics["avg_execution_time"]
        self.performance_metrics["avg_execution_time"] = (
            (current_avg * (total - 1) + execution_time) / total
        )
    
    def get_performance_report(self) -> Dict:
        """获取性能报告"""
        total = self.performance_metrics["total_tasks"]
        if total == 0:
            return {"message": "暂无执行记录"}
        
        success_rate = self.performance_metrics["successful_tasks"] / total
        
        return {
            "total_tasks": total,
            "success_rate": f"{success_rate:.1%}",
            "avg_execution_time": f"{self.performance_metrics['avg_execution_time']:.2f}s",
            "failed_tasks": self.performance_metrics["failed_tasks"],
            "recommendations": self._generate_recommendations(success_rate)
        }
    
    def _generate_recommendations(self, success_rate: float) -> List[str]:
        """生成优化建议"""
        recommendations = []
        
        if success_rate < 0.8:
            recommendations.append("成功率较低，建议检查任务配置或增加重试次数")
        
        if self.performance_metrics["avg_execution_time"] > 10:
            recommendations.append("平均执行时间较长，建议启用并行模式")
        
        if self.performance_metrics["failed_tasks"] > 10:
            recommendations.append("失败任务较多，建议启用自适应执行模式")
        
        return recommendations


class PredictiveExecutor:
    """预测性执行器"""
    
    def __init__(self):
        self.execution_patterns: Dict[str, Dict] = {}
    
    def learn_pattern(self, task_type: str, context: Dict, result: Dict):
        """学习执行模式"""
        if task_type not in self.execution_patterns:
            self.execution_patterns[task_type] = {
                "count": 0,
                "avg_time": 0,
                "success_rate": 0,
                "context_features": []
            }
        
        pattern = self.execution_patterns[task_type]
        pattern["count"] += 1
        
        # 更新平均时间
        old_avg = pattern["avg_time"]
        new_time = result.get("execution_time", 0)
        pattern["avg_time"] = (old_avg * (pattern["count"] - 1) + new_time) / pattern["count"]
        
        # 更新成功率
        success = 1 if result.get("success") else 0
        old_rate = pattern["success_rate"]
        pattern["success_rate"] = (old_rate * (pattern["count"] - 1) + success) / pattern["count"]
    
    def predict(self, task_type: str, context: Dict) -> Dict:
        """预测执行结果"""
        if task_type not in self.execution_patterns:
            return {"confidence": 0, "prediction": "unknown"}
        
        pattern = self.execution_patterns[task_type]
        
        return {
            "confidence": min(pattern["count"] / 10, 1.0),  # 置信度随样本增加
            "predicted_time": pattern["avg_time"],
            "predicted_success_rate": pattern["success_rate"],
            "recommendation": self._get_recommendation(pattern)
        }
    
    def _get_recommendation(self, pattern: Dict) -> str:
        """获取建议"""
        if pattern["success_rate"] < 0.5:
            return "建议调整执行策略或检查输入参数"
        elif pattern["avg_time"] > 30:
            return "建议启用并行执行或优化任务"
        else:
            return "当前策略效果良好"


# 便捷函数
def create_executor(max_workers: int = 10) -> AdaptiveExecutor:
    """创建执行器"""
    return AdaptiveExecutor(max_workers=max_workers)


def quick_execute(funcs: List[Callable], mode: ExecutionMode = ExecutionMode.ADAPTIVE) -> List[Any]:
    """快速执行多个函数"""
    tasks = [
        Task(id=f"task_{i}", name=f"Task {i}", func=f)
        for i, f in enumerate(funcs)
    ]
    
    executor = AdaptiveExecutor()
    plan = executor.create_execution_plan(tasks)
    plan.mode = mode
    
    results = executor.execute(plan)
    return [r.result for r in results if r.success]


if __name__ == "__main__":
    # 测试
    def sample_task(name: str, duration: float = 1.0):
        time.sleep(duration)
        return f"{name} completed"
    
    tasks = [
        Task(id="1", name="任务1", func=sample_task, args=("Task1", 0.5)),
        Task(id="2", name="任务2", func=sample_task, args=("Task2", 0.3)),
        Task(id="3", name="任务3", func=sample_task, args=("Task3", 0.7)),
    ]
    
    executor = AdaptiveExecutor()
    plan = executor.create_execution_plan(tasks)
    
    print(f"执行模式: {plan.mode.value}")
    print(f"预计时间: {plan.estimated_time:.1f}s")
    
    def progress(current, total, name):
        print(f"进度: [{current}/{total}] {name}")
    
    results = executor.execute(plan, progress)
    
    for r in results:
        print(f"{r.task_id}: {'✓' if r.success else '✗'} {r.execution_time:.2f}s")
    
    print("\n性能报告:")
    print(executor.get_performance_report())
