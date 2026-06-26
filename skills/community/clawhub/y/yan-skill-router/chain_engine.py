#!/usr/bin/env python3
"""
Skill Chain Engine v2 — 参考 multi-agent-orchestrator 的通信协议

核心改进：
1. ChainStep 增加 depends_on / input_mapping / skip_if_failed → 步骤间数据传递
2. SkillChain 增加 fallback_chain / step_results → 错误恢复
3. match_chain() 统一接口，消除 match() 重复
4. format_plan() 展示数据流而非仅步骤列表
5. 新增 scaffold() 生成标准 step 上下文脚本

用法:
    engine = ChainEngine()
    chain = engine.match_chain(["systematic_review"], query="...")
    plan = engine.format_plan(chain)
    agent_context = engine.scaffold(chain, step_index=0)
"""

import json
import warnings
from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


# =============================================================================
# 增强数据模型
# =============================================================================

@dataclass
class ChainStep:
    """
    链中的一步，包含步骤间数据传递协议
    
    参考 multi-agent-orchestrator:
    - Agent Characteristics → 由 skill/description 表达
    - Input Router → 由 depends_on + input_mapping 实现
    - Response Handling → 由 output_key 记录
    
    执行流程:
    wait_for(depends_on) → collect(inputs via input_mapping) → 
    execute(skill) → save(output_key) → check(skip_if_failed)
    """
    capability: str
    skill: str
    description: str
    order: int = 0

    # ── 步骤间数据传递协议（新增） ──
    depends_on: list[int] = field(default_factory=list)
    """当前步骤依赖的步骤序号（0-based），执行前必须等这些步骤完成"""
    
    input_mapping: dict[str, str] = field(default_factory=dict)
    """
    上一步输出 → 当前步骤输入的映射
    key = 当前步骤输入参数名
    value = {step_index}.{output_field} | "lit:..." | "query"
    例: {"articles": "0.articles", "query": "query"}
    """
    
    output_key: str = ""
    """当前步骤的输出键名，供下游 steps 引用"""
    
    skip_if_failed: bool = True
    """依赖的步骤失败时，当前是否跳过（False = 仍尝试执行）"""
    
    retry_count: int = 0
    """失败重试次数（0=不重试）"""

    # ── 执行状态（运行时填充） ──
    status: str = "pending"  # pending | running | done | failed | skipped
    output: str = ""


@dataclass
class SkillChain:
    """一条完整的 skill chain"""
    id: str
    name: str
    description: str
    steps: list[ChainStep]
    
    # ── 增强编排能力 ──
    fallback_chain: Optional[str] = None
    """主链失败时回退的 chain id"""
    
    parallel_groups: list[list[int]] = field(default_factory=list)
    """可并行执行的 step index 组（0-based）"""
    
    output: str = ""
    """最终产出描述"""
    
    match_score: float = 0.0
    """匹配度"""


# =============================================================================
# 链式路由引擎
# =============================================================================

class ChainEngine:
    """
    链式路由引擎 v2
    
    match_chain(cap_names, query) 是唯一入口
    format_plan(chain) 输出含数据流
    scaffold(chain, step_index) 生成 step 上下文
    """

    def __init__(self, chains_path: str = None):
        if chains_path is None:
            chains_path = str(Path(__file__).parent / "chains.json")
        self.chains_path = chains_path
        self._raw_data = None  # match_chain 用内存态，不重复读磁盘
        self._load_chains()

    def _load_chains(self):
        """加载 chains.json → 内存态 + 已解析链缓存"""
        with open(self.chains_path, encoding="utf-8") as f:
            self._raw_data = json.load(f)
        self.chains: list[SkillChain] = []
        for c in self._raw_data["chains"]:
            self.chains.append(self._parse_chain(c))

    def _parse_chain(self, c: dict) -> SkillChain:
        """字典 → SkillChain，处理新旧 schema 兼容"""
        steps = []
        for i, s in enumerate(c.get("steps", [])):
            steps.append(ChainStep(
                capability=s.get("capability", ""),
                skill=s.get("skill", ""),
                description=s.get("description", ""),
                order=i + 1,
                depends_on=s.get("depends_on", list(range(i)) if i > 0 else []),
                input_mapping=s.get("input_mapping", {}),
                output_key=s.get("output_key", f"step_{i}_output"),
                skip_if_failed=s.get("skip_if_failed", True),
                retry_count=s.get("retry_count", 0),
            ))
        return SkillChain(
            id=c["id"],
            name=c["name"],
            description=c.get("description", ""),
            steps=steps,
            fallback_chain=c.get("fallback_chain"),
            parallel_groups=c.get("parallel_groups", []),
            output=c.get("output", ""),
        )

    def match_chain(self, cap_names: list[str], query: str = "") -> Optional[SkillChain]:
        """
        唯一入口：cap_names + query → 最匹配 chain
        
        匹配策略（参考 multi-agent-orchestrator 的 Classifier）：
        - trigger_caps 硬匹配（权重最高）
        - trigger_keywords 软匹配
        - step capability 重叠（补充）

        使用 self._raw_data 内存态，不重复读磁盘。
        
        注意：depends_on 和 order 的 index 差异：
        - depends_on: 0-based（指向 steps 列表索引）
        - order: 1-based（显示用）
        - format_plan 输出混合两者：Step1(1-based) + step0.output(0-based)
        """
        if self._raw_data is None:
            return None

        cap_set = set(cap_names)
        q_lower = query.lower()
        best = None
        best_score = 0.0

        for c in self._raw_data["chains"]:
            score = 0.0
            tcaps = set(c.get("trigger_caps", []))
            tkws = c.get("trigger_keywords", [])

            # trigger_caps 匹配：最硬的条件
            overlap = tcaps & cap_set
            if tcaps and overlap:
                score += len(overlap) * 10

            # trigger_keywords 匹配：query 中包含关键词
            for kw in tkws:
                if kw in q_lower:
                    score += 8

            # 步骤中的 capability 重叠（补充）
            step_caps = {s.get("capability", "") for s in c.get("steps", [])}
            step_overlap = step_caps & cap_set
            score += len(step_overlap) * 3

            if score > best_score:
                best_score = score
                chain = self._parse_chain(c)
                chain.match_score = score
                best = chain

        return best if best_score > 0 else None

    # ── match() 已废弃，统一用 match_chain() ──
    def match(self, cap_names: list[str], query: str = "") -> Optional[SkillChain]:
        """已废弃：请使用 match_chain()"""
        warnings.warn("match() 已废弃，请使用 match_chain()", DeprecationWarning, stacklevel=2)
        return self.match_chain(cap_names, query)

    def format_plan(self, chain: SkillChain) -> str:
        """
        生成含数据流的执行计划
        
        输出格式参考 multi-agent-orchestrator 的 Routing Diagram:
        
        [Orchestration Plan]
        链: 系统综述 → 输出: meta分析报告
        
        Step1 [literature_search] 检索文献
          → output: articles
          └── depends: (无)
        
        Step2 [systematic_review] Meta分析
          ← input.articles = step1.articles  (数据流)
          → output: meta_result
          └── depends: step1
        """
        if not chain:
            return ""

        # 并行组映射
        parallel_map = {}
        for group_id, indices in enumerate(chain.parallel_groups):
            for idx in indices:
                if idx < len(chain.steps):
                    parallel_map[idx] = group_id

        lines = [
            "[Orchestration Plan]",
            f"  链: {chain.name}",
            f"  描述: {chain.description}",
            f"  最终输出: {chain.output or '未指定'}",
        ]

        if chain.fallback_chain:
            lines.append(f"  ⚡ 回退链: {chain.fallback_chain}")

        lines.append("")
        lines.append("  执行步骤:")

        for i, step in enumerate(chain.steps):
            tag = ""
            if i in parallel_map:
                tag = " [并行]"

            lines.append(f"")
            lines.append(f"  Step{i+1}{tag}: [{step.capability}] {step.skill}")
            lines.append(f"    {step.description}")

            # 数据流：输入
            if step.input_mapping:
                for param, source in step.input_mapping.items():
                    if source == "$query":
                        lines.append(f"    ← input.{param} = 用户原始query")
                    elif source.startswith("lit:"):
                        lines.append(f"    ← input.{param} = {source[4:]}")
                    else:
                        lines.append(f"    ← input.{param} = {source}")
            elif i > 0:
                lines.append(f"    ← input = step{i}.output (默认传递)")

            # 数据流：输出
            if step.output_key:
                lines.append(f"    → output: {step.output_key}")

            # 依赖关系
            if step.depends_on:
                dep_names = [f"step{d+1}" for d in step.depends_on]
                lines.append(f"    └── 依赖: {', '.join(dep_names)}")
            else:
                lines.append(f"    └── 依赖: 无")

            if step.retry_count > 0:
                lines.append(f"    └── 重试: 最多{step.retry_count}次")

        # 并行组说明
        if chain.parallel_groups:
            lines.append("")
            lines.append("  ⚡ 可并行执行的组:")
            for g in chain.parallel_groups:
                names = [f"Step{i+1}" for i in g if i < len(chain.steps)]
                lines.append(f"    {' + '.join(names)}")

        return "\n".join(lines)

    # =========================================================================
    # 新增: 生成 step 上下文脚本
    # =========================================================================

    def scaffold(self, chain: SkillChain, step_index: int) -> str:
        """
        生成 step 的执行上下文脚本
        
        返回格式：假设当前 agent 是 step[step_index]，
        包含输入数据来源、输出格式要求、上下游通信提示。
        
        用途：在 multi-step 场景下，给每个 skill 注入其"在 chain 中的位置"
        """
        if not chain or step_index >= len(chain.steps):
            return ""

        step = chain.steps[step_index]

        # 收集上游输出信息
        upstream = []
        for dep_idx in step.depends_on:
            if dep_idx < len(chain.steps):
                dep = chain.steps[dep_idx]
                upstream.append(f"  step{dep_idx+1}.{dep.output_key} ({dep.skill}: {dep.description})")

        # 收集下游消费者信息
        downstream = []
        for j, s in enumerate(chain.steps):
            if step_index in s.depends_on:
                downstream.append(f"  step{j+1} ({s.skill}: {s.description})")

        sections = [
            f"# Context: Step {step.order} of {len(chain.steps)} — {chain.name}",
            f"# 角色: {step.skill}",
            f"# 职责: {step.description}",
            "",
        ]

        if upstream:
            sections.append("# 上游输入:")
            sections.extend(upstream)
            sections.append("")

        if step.input_mapping:
            sections.append("# 输入映射:")
            for param, source in step.input_mapping.items():
                sections.append(f"  {param} ← {source}")
            sections.append("")

        sections.append("# 输出要求:")
        sections.append(f"  输出字段: {step.output_key}")
        sections.append(f"  下游消费者: {'、'.join(d[2:] for d in downstream) if downstream else '最终输出'}")

        if downstream:
            sections.append("")
            sections.append("# 下游依赖此输出的步骤:")
            sections.extend(downstream)

        if step.retry_count > 0:
            sections.append("")
            sections.append(f"# 重试策略: 最多 {step.retry_count} 次")

        return "\n".join(sections)


# =============================================================================
# 测试
# =============================================================================

if __name__ == "__main__":
    engine = ChainEngine()

    from capability_taxonomy import CapabilityTaxonomy
    cap = CapabilityTaxonomy()

    test_queries = [
        ("做一篇新生儿低血糖的系统综述", ["systematic_review"]),
        ("帮我在PubMed上搜一下脓毒症脑病的文献然后发到邮箱", ["literature_search", "email"]),
        ("做儿童过敏性疾病的文献计量分析", ["bibliometric"]),
        ("最新新生儿复苏指南", ["guideline"]),
    ]

    for query, _ in test_queries:
        detected = cap.detect(query)
        chain = engine.match_chain(detected, query)
        print(f"\n{'=' * 60}")
        print(f"Query: {query}")
        print(f"  CapTax: {detected}")
        if chain:
            print(f"  匹配链: {chain.name} (score={chain.match_score})")
            print()
            print(engine.format_plan(chain))
            # 展示第一个 step 的上下文
            if chain.steps:
                print()
                print("  --- scaffold for Step1 ---")
                print(engine.scaffold(chain, 0))
        else:
            print("  → 无匹配 chain")
        print()
