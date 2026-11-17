"""
Layer 2: 任务拆解器 (Task Decomposer)

职责：
- 接收策略阶段共识结果，拆解为可并行执行的子任务
- 输出 TaskDAG（含依赖关系、预算、超时）
- 循环依赖检测（拓扑排序验证）
- 确保子任务之间无数据依赖（如配置要求并行）
"""
from __future__ import annotations

import logging
from collections import Counter
from typing import Any, Dict, List, Optional

from schemas import (
    DecisionResult,
    StrategyRound,
    SubTask,
    TaskDAG,
    Tier,
    UserInput,
)

logger = logging.getLogger(__name__)


# ============================================================================
# 配置
# ============================================================================

# 各配置档次允许的最大子任务数
TIER_MAX_SUBTASKS: Dict[Tier, int] = {
    Tier.FULL: 5,
    Tier.BALANCED: 3,
    Tier.LIGHT: 1,
    Tier.SKILL_DISPATCH: 5,
}

# 各配置档次默认 token 预算
TIER_TOKEN_BUDGET: Dict[Tier, int] = {
    Tier.FULL: 8000,
    Tier.BALANCED: 4000,
    Tier.LIGHT: 2000,
    Tier.SKILL_DISPATCH: 4000,
}


# ============================================================================
# 拆解器
# ============================================================================

class TaskDecomposer:
    """任务拆解器 — 将策略决策转为 TaskDAG"""

    def __init__(
        self,
        enforce_parallel: bool = True,
        max_subtasks_override: Optional[int] = None,
    ):
        """
        Args:
            enforce_parallel: True=强制子任务无依赖（并行安全）
            max_subtasks_override: 覆盖默认最大子任务数
        """
        self.enforce_parallel = enforce_parallel
        self.max_subtasks_override = max_subtasks_override

    def decompose(
        self,
        strategy: Optional[StrategyRound],
        validated_input: UserInput,
        external_dag: Optional[TaskDAG] = None,
    ) -> TaskDAG:
        """
        拆解任务。

        三种拆解路径：
        1. external_dag 提供 → 只做校验
        2. strategy 中有明确拆解指令 → 按指令拆
        3. 无指令 → 按任务复杂度自动拆

        Args:
            strategy: 策略阶段共识结果
            validated_input: 校验后的用户输入
            external_dag: 外部传入的 TaskDAG（如子技能调度模式）

        Returns:
            TaskDAG: 校验通过的 DAG
        """
        # 路径 1：外部 DAG
        if external_dag is not None:
            logger.info("使用外部提供的 TaskDAG，执行校验")
            return self._validate_dag(external_dag, validated_input)

        # 路径 2 & 3：从策略拆解
        tier = self._extract_tier(strategy)
        max_subtasks = self.max_subtasks_override or TIER_MAX_SUBTASKS.get(tier, 3)
        token_budget = TIER_TOKEN_BUDGET.get(tier, 4000)

        dag = self._build_dag(validated_input, strategy, max_subtasks, token_budget)
        return self._validate_dag(dag, validated_input)

    # ------------------------------------------------------------------
    # 内部方法
    # ------------------------------------------------------------------

    def _get_default_tier(self) -> Tier:
        """获取默认配置档次（显式化，消除 _extract_tier(None) 的隐式默认值）"""
        return Tier.BALANCED

    def _extract_tier(self, strategy: Optional[StrategyRound]) -> Tier:
        """从策略中提取配置档次"""
        if not strategy or not strategy.decisions:
            return self._get_default_tier()

        # 取多数决策者的配置
        configs = [d.config for d in strategy.decisions]
        counter = Counter(configs)
        most_common = counter.most_common(1)
        if most_common:
            return most_common[0][0]
        return self._get_default_tier()

    def _build_dag(
        self,
        validated_input: UserInput,
        strategy: Optional[StrategyRound],
        max_subtasks: int,
        token_budget: int,
    ) -> TaskDAG:
        """从策略构建 TaskDAG"""
        subtasks: List[SubTask] = []

        # 从策略中提取各决策者的 top_findings 作为子任务方向
        task_directions: List[str] = []
        if strategy:
            for decision in strategy.decisions:
                task_directions.extend(decision.top_findings[:2])

        # 如果没有明确方向，按模板生成
        if not task_directions:
            task_directions = [f"分析: {validated_input.task_description}"]

        # 去重
        task_directions = list(dict.fromkeys(task_directions))

        # 限制数量
        task_directions = task_directions[:max_subtasks]

        for i, direction in enumerate(task_directions):
            subtask = SubTask(
                id=f"subtask-{i+1:02d}",
                goal=direction,
                completion_criteria=f"完成对 '{direction}' 的分析并产出结构化结论",
                output_format="Markdown 格式，包含结论、依据、不确定性说明",
                token_budget=token_budget,
                timeout_seconds=300,
                # enforce_parallel=True 时不设置 depends_on
            )
            subtasks.append(subtask)

        return TaskDAG(subtasks=subtasks)

    def _validate_dag(self, dag: TaskDAG, validated_input: UserInput) -> TaskDAG:
        """校验 TaskDAG"""
        # 并行约束检查
        if self.enforce_parallel:
            for subtask in dag.subtasks:
                if subtask.depends_on:
                    raise DAGValidationError(
                        f"子任务 '{subtask.id}' 设置了依赖 {subtask.depends_on}，"
                        f"但 enforce_parallel=True 要求所有子任务必须可并行执行",
                        dag=dag,
                    )

        # 数量检查 — 超出上限时返回新 TaskDAG 而非原地修改
        max_allowed = self.max_subtasks_override or TIER_MAX_SUBTASKS.get(
            self._get_default_tier(), 3
        )
        if len(dag.subtasks) > max_allowed:
            logger.warning(
                f"TaskDAG 包含 {len(dag.subtasks)} 个子任务，超过上限 {max_allowed}，"
                f"将截断"
            )
            return TaskDAG(subtasks=list(dag.subtasks[:max_allowed]))

        # Pydantic 自带环检测（在 TaskDAG model_validator 中）
        return dag


# ============================================================================
# 异常（re-export from exceptions.py）
# ============================================================================
from exceptions import DAGValidationError  # noqa: F401
