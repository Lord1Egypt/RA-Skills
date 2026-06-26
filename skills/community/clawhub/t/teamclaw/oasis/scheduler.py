"""
OASIS Forum - Discussion Scheduler

Parses YAML schedule definitions and yields execution steps
that control the order in which experts speak.

Either schedule_file or schedule_yaml is required. schedule_file
takes priority if both are provided. Even for simple all-parallel
scenarios, a minimal YAML suffices:
  version: 1
  repeat: true
  plan:
    - all_experts: true

Schedule YAML format:
  version: 1
  repeat: true          # true = 每轮重复整个 plan; false = plan 只执行一次
  discussion: false     # true = 论坛讨论模式(JSON回复/投票); false = 执行模式(agent直接执行任务，默认)
  plan:
    # 指定专家发言（按名称匹配）
    # 名称格式直接对应 engine 的专家类型（必须含 '#'）：
    #   "tag#temp#N"          → ExpertAgent (tag 查预设获取 name/persona)
    #   "tag#oasis#随机ID"    → SessionExpert (oasis, tag 查预设获取 name/persona)
    #   "标题#session_id"     → SessionExpert (普通 agent, 不注入)
    #   "name#ext#id"         → ExternalExpert (直连外部 OpenAI 兼容 API)
    #   任何 session 名 + "#new" → 强制创建全新 session（ID 替换为随机 UUID）
    - expert: "critical#temp#1"
      instruction: "请重点分析技术风险"    # 可选：给专家的具体指令

    # 外部 agent（直连 OpenAI 兼容 API，不经过本地 agent）
    - expert: "分析师#ext#analyst"
      api_url: "https://api.deepseek.com"    # 必填：外部服务 base URL
      api_key: "****"                      # 掩码 — 运行时从 OPENCLAW_API_KEY 环境变量自动读取
      model: "deepseek-chat"                 # 可选：模型名，默认 gpt-3.5-turbo
      headers:                               # 可选：额外 HTTP headers
        X-Custom-Auth: "token123"
      instruction: "从数据角度分析"           # 可选

    # OpenClaw agent（通过 x-openclaw-session-key 指定确定 session）
    - expert: "coder#ext#oc1"
      api_url: "http://127.0.0.1:18789"
      api_key: "****"
      model: "agent:main:test1"
      headers:
        x-openclaw-session-key: "agent:main:test1"  # 构建确定 session 号的关键 header

    # 多个专家同时并行发言
    - parallel:
        - expert: "创意专家"
          instruction: "从创新角度提出方案"
        - expert: "数据分析师"
        # 外部 agent 也可以在 parallel 中使用
        - expert: "GPT4专家#ext#gpt4"
          api_url: "https://api.openai.com"
          api_key: "****"
          model: "gpt-4"

    # 手动注入一条帖子（不经过 LLM）
    - manual:
        author: "主持人"
        content: "请大家聚焦到可行性方面讨论"
        reply_to: null

    # 所有专家并行（等同于不用 schedule 的默认行为）
    - all_experts: true

  # ── DAG 模式（单向无环图调度）──
  # 当 plan 中的步骤包含 id 和 depends_on 字段时，自动进入 DAG 模式。
  # 每个步骤的所有前驱步骤完成后，该步骤立即开始执行（最大化并行）。
  #
  # 示例:
  #   version: 1
  #   repeat: false
  #   plan:
  #     - id: step_a
  #       expert: "creative#temp#1"
  #     - id: step_b
  #       expert: "critical#temp#1"
  #     - id: step_c
  #       expert: "writer#temp#1"
  #       depends_on: [step_a, step_b]     # step_c 等待 step_a 和 step_b 都完成
  #     - id: step_d
  #       expert: "reviewer#temp#1"
  #       depends_on: [step_c]
  #
  # depends_on 为空列表或省略 → 该步骤没有前驱，立即执行。
  # DAG 必须是无环的，否则会抛出 ValueError。

Execution modes:
  repeat: true  -> plan 在每轮重复执行，max_rounds 控制总轮数
  repeat: false -> plan 中的步骤顺序执行一次即结束（忽略 max_rounds）

If no schedule is provided, the engine will raise a ValueError.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

import os

import yaml

# Placeholder mask used in YAML to indicate "use key from environment"
_API_KEY_MASK = "****"


class StepType(str, Enum):
    """Types of schedule steps."""
    EXPERT = "expert"           # Single expert speaks (sequential)
    PARALLEL = "parallel"       # Multiple experts speak in parallel
    ALL = "all_experts"         # All experts speak in parallel
    MANUAL = "manual"           # Inject a post manually (no LLM)


@dataclass
class ScheduleStep:
    """A single step in the discussion schedule."""
    step_type: StepType
    expert_names: list[str] = field(default_factory=list)   # for EXPERT / PARALLEL
    instructions: dict[str, str] = field(default_factory=dict)  # expert_name → instruction text
    manual_author: str = ""                                  # for MANUAL
    manual_content: str = ""                                 # for MANUAL
    manual_reply_to: Optional[int] = None                    # for MANUAL
    # External agent config: expert_name → {api_url, api_key, model}
    external_configs: dict[str, dict] = field(default_factory=dict)
    # DAG fields
    step_id: str = ""                                        # unique id for DAG dependency
    depends_on: list[str] = field(default_factory=list)      # list of step_ids this step waits for


@dataclass
class Schedule:
    """Parsed schedule with steps and config."""
    steps: list[ScheduleStep]
    repeat: bool = False  # True = repeat plan each round; False = run once
    discussion: bool = False  # True = forum discussion mode (JSON reply/vote); False = execute mode (agents just run tasks)
    is_dag: bool = False  # True when steps have id/depends_on fields (DAG execution mode)


def _extract_external_config(item: dict) -> dict:
    """Extract external agent config fields from a YAML step item.

    Supports:
      api_url: "https://api.example.com"      # external API base URL
      api_key: "sk-xxx" or "****"              # API key (masked = read from env)
      model: "gpt-4"                           # model name
      headers:                                 # extra HTTP headers (key: value)
        X-Custom-Header: "value"

    If api_key is the mask placeholder "****", it will be resolved to
    the OPENCLAW_API_KEY environment variable at parse time.
    """
    cfg: dict = {}
    if "api_url" in item:
        cfg["api_url"] = str(item["api_url"])
    if "api_key" in item:
        raw_key = str(item["api_key"])
        if raw_key == _API_KEY_MASK:
            # Resolve masked key from environment variable
            cfg["api_key"] = os.getenv("OPENCLAW_API_KEY", "")
        else:
            cfg["api_key"] = raw_key
    if "model" in item:
        cfg["model"] = str(item["model"])
    if "headers" in item and isinstance(item["headers"], dict):
        cfg["headers"] = {str(k): str(v) for k, v in item["headers"].items()}
    return cfg


def parse_schedule(yaml_content: str) -> Schedule:
    """
    Parse a YAML schedule string into a Schedule object.

    Raises ValueError on invalid format.
    """
    data = yaml.safe_load(yaml_content)
    if not isinstance(data, dict) or "plan" not in data:
        raise ValueError("Schedule YAML must contain a 'plan' key")

    plan = data["plan"]
    if not isinstance(plan, list):
        raise ValueError("'plan' must be a list of steps")

    repeat = bool(data.get("repeat", False))
    discussion = bool(data.get("discussion", False))

    steps: list[ScheduleStep] = []
    has_ids = False  # track whether any step has an 'id' field → DAG mode

    for i, item in enumerate(plan):
        if not isinstance(item, dict):
            raise ValueError(f"Step {i}: must be a dict, got {type(item).__name__}")

        # Extract DAG fields (common to all step types)
        step_id = str(item.get("id", ""))
        depends_on_raw = item.get("depends_on", [])
        if isinstance(depends_on_raw, str):
            depends_on = [depends_on_raw]
        elif isinstance(depends_on_raw, list):
            depends_on = [str(d) for d in depends_on_raw]
        else:
            depends_on = []
        if step_id:
            has_ids = True

        if "expert" in item:
            expert_name = str(item["expert"])
            instr_map = {}
            ext_configs = {}
            if "instruction" in item:
                instr_map[expert_name] = str(item["instruction"])
            if "api_url" in item or "headers" in item:
                ext_configs[expert_name] = _extract_external_config(item)
            steps.append(ScheduleStep(
                step_type=StepType.EXPERT,
                expert_names=[expert_name],
                instructions=instr_map,
                external_configs=ext_configs,
                step_id=step_id,
                depends_on=depends_on,
            ))

        elif "parallel" in item:
            names = []
            instr_map = {}
            ext_configs = {}
            for sub in item["parallel"]:
                if isinstance(sub, dict) and "expert" in sub:
                    ename = str(sub["expert"])
                    names.append(ename)
                    if "instruction" in sub:
                        instr_map[ename] = str(sub["instruction"])
                    if "api_url" in sub or "headers" in sub:
                        ext_configs[ename] = _extract_external_config(sub)
                elif isinstance(sub, str):
                    names.append(sub)
                else:
                    raise ValueError(f"Step {i}: parallel entries must have 'expert' key")
            if not names:
                raise ValueError(f"Step {i}: parallel list is empty")
            steps.append(ScheduleStep(
                step_type=StepType.PARALLEL,
                expert_names=names,
                instructions=instr_map,
                external_configs=ext_configs,
                step_id=step_id,
                depends_on=depends_on,
            ))

        elif "all_experts" in item:
            steps.append(ScheduleStep(
                step_type=StepType.ALL,
                step_id=step_id,
                depends_on=depends_on,
            ))

        elif "manual" in item:
            m = item["manual"]
            if not isinstance(m, dict) or "content" not in m:
                raise ValueError(f"Step {i}: manual must have 'content'")
            steps.append(ScheduleStep(
                step_type=StepType.MANUAL,
                manual_author=str(m.get("author", "主持人")),
                manual_content=str(m["content"]),
                manual_reply_to=m.get("reply_to"),
                step_id=step_id,
                depends_on=depends_on,
            ))

        else:
            raise ValueError(f"Step {i}: unknown step type, keys={list(item.keys())}")

    # Detect DAG mode: if any step has an 'id', it's a DAG schedule
    is_dag = has_ids

    # Validate DAG: check for cycles and invalid references
    if is_dag:
        _validate_dag(steps)

    return Schedule(steps=steps, repeat=repeat, discussion=discussion, is_dag=is_dag)


def _validate_dag(steps: list[ScheduleStep]) -> None:
    """Validate DAG: check that all depends_on references exist and there are no cycles."""
    id_set = {s.step_id for s in steps if s.step_id}

    # Check all depends_on references are valid
    for s in steps:
        for dep in s.depends_on:
            if dep not in id_set:
                raise ValueError(f"Step '{s.step_id}': depends_on references unknown step '{dep}'")

    # Check for cycles using Kahn's algorithm
    in_deg: dict[str, int] = {s.step_id: 0 for s in steps if s.step_id}
    adj: dict[str, list[str]] = {s.step_id: [] for s in steps if s.step_id}
    for s in steps:
        if not s.step_id:
            continue
        for dep in s.depends_on:
            adj[dep].append(s.step_id)
            in_deg[s.step_id] += 1

    queue = [sid for sid, deg in in_deg.items() if deg == 0]
    visited = 0
    while queue:
        node = queue.pop(0)
        visited += 1
        for neighbor in adj.get(node, []):
            in_deg[neighbor] -= 1
            if in_deg[neighbor] == 0:
                queue.append(neighbor)

    if visited < len(id_set):
        raise ValueError("DAG schedule contains a cycle — workflow must be acyclic")


def load_schedule_file(path: str) -> Schedule:
    """Load and parse a schedule from a YAML file path."""
    with open(path, "r", encoding="utf-8") as f:
        return parse_schedule(f.read())


def extract_expert_names(schedule: Schedule) -> list[str]:
    """Extract all unique expert names referenced in a schedule (preserving order).

    Scans EXPERT and PARALLEL steps for expert_names.
    ALL and MANUAL steps don't reference specific experts so are skipped.
    Returns a deduplicated list in order of first appearance.
    """
    seen: set[str] = set()
    result: list[str] = []
    for step in schedule.steps:
        if step.step_type in (StepType.EXPERT, StepType.PARALLEL):
            for name in step.expert_names:
                if name not in seen:
                    seen.add(name)
                    result.append(name)
    return result


def collect_external_configs(schedule: Schedule) -> dict[str, dict]:
    """Collect all external agent configs from schedule steps.

    Returns a dict mapping expert_name → {api_url, api_key?, model?}.
    If an expert appears in multiple steps with different configs, the first one wins.
    """
    configs: dict[str, dict] = {}
    for step in schedule.steps:
        for name, cfg in step.external_configs.items():
            if name not in configs:
                configs[name] = cfg
    return configs
