"""Specification extractor — PaperContent → List[StrategySpec].

Multi-layer extraction architecture (inspired by production QSA pipeline):
  Layer 0: Strategy Detection (how many independent strategies in the paper?)
  Layer 1: Metadata + Data Requirements + Performance Metrics
  Layer 2: Indicators / Factors / Computed Signals
  Layer 3: Logic Pipeline (signal generation → trade signals)
  Layer 4: Execution Plan + Risk Management

Each layer is a focused LLM call with targeted prompts, producing
higher-quality structured output than a single monolithic call.

Multi-strategy support:
  When a paper contains N>1 independent strategies, Layer 0 detects them
  and Layers 1-4 run once per strategy with focused context injection.
"""

import asyncio
import json
import logging
import re
from typing import List, Optional

from paper2spec.llm import achat, chat
from paper2spec.models import (
    ExtractionResult,
    ExecutionAction,
    ExecutionPlan,
    ExecutionTrigger,
    Indicator,
    LogicStep,
    PaperContent,
    PositionSizing,
    StrategyBrief,
    StrategySpec,
)
from paper2spec.prompts import (
    LAYER0_STRATEGY_DETECTION_PROMPT,
    LAYER1_METADATA_AND_DATA_PROMPT,
    LAYER2_INDICATORS_PROMPT,
    LAYER3_LOGIC_PIPELINE_PROMPT,
    LAYER4_EXECUTION_PROMPT,
    SPECIFICATION_PROMPT,
    SYSTEM_PROMPT,
)

logger = logging.getLogger(__name__)

MAX_RETRIES = 2  # Retry once on JSON parse failure


# ── Public API ───────────────────────────────────────────────


def extract_spec(
    paper_content: PaperContent,
    *,
    model: Optional[str] = None,
    mode: str = "multilayer",
) -> ExtractionResult:
    """Synchronous: PaperContent → ExtractionResult (list of StrategySpec).

    Args:
        paper_content: Structured paper content from parser.
        model: Override LLM model string.
        mode: "multilayer" (4 focused calls, recommended) or "single" (1 call, legacy).
    """
    return asyncio.run(aextract_spec(paper_content, model=model, mode=mode))


async def aextract_spec(
    paper_content: PaperContent,
    *,
    model: Optional[str] = None,
    mode: str = "multilayer",
) -> ExtractionResult:
    """Async: PaperContent → ExtractionResult via multi-layer LLM extraction."""
    if mode == "single":
        spec = await _extract_single_call(paper_content, model=model)
        return ExtractionResult(
            strategies=[spec],
            paper_title=paper_content.title,
            num_detected=1,
        )

    # Layer 0: Detect strategies
    briefs = await _detect_strategies(paper_content, model=model)

    if len(briefs) <= 1:
        # Single strategy — run standard 4-layer extraction (no context injection)
        spec = await _extract_multilayer(paper_content, model=model)
        return ExtractionResult(
            strategies=[spec],
            paper_title=paper_content.title,
            num_detected=1,
        )

    # Multi-strategy — run 4-layer extraction per strategy in parallel
    logger.info("Multi-strategy paper: %d strategies detected", len(briefs))

    async def _extract_one(i: int, brief: StrategyBrief) -> StrategySpec:
        logger.info("━━━ Strategy %d/%d: %s ━━━", i + 1, len(briefs), brief.name)
        strategy_focus = _build_strategy_focus(brief)
        spec = await _extract_multilayer(
            paper_content, model=model, strategy_focus=strategy_focus
        )
        if not spec.strategy_name or spec.strategy_name == paper_content.title:
            spec.strategy_name = brief.name
        return spec

    specs = list(await asyncio.gather(
        *(_extract_one(i, brief) for i, brief in enumerate(briefs))
    ))

    return ExtractionResult(
        strategies=specs,
        paper_title=paper_content.title,
        num_detected=len(briefs),
    )


# ── Layer 0: Strategy Detection ──────────────────────────────


async def _detect_strategies(
    pc: PaperContent, *, model: Optional[str] = None
) -> List[StrategyBrief]:
    """Detect how many independent strategies a paper contains."""
    logger.info("Layer 0: Detecting strategies...")
    prompt = LAYER0_STRATEGY_DETECTION_PROMPT.format(
        title=pc.title,
        abstract=pc.abstract or pc.full_text[:2000],
        methodology=pc.methodology,
        signal_logic=pc.signal_logic,
    )
    result = await _call_llm_json(prompt, model=model)
    if not result:
        logger.warning("Layer 0 failed — falling back to single strategy")
        return [StrategyBrief(name=pc.title)]

    num = result.get("num_strategies", 1)
    raw_strategies = result.get("strategies", [])

    briefs = []
    for s in raw_strategies:
        if isinstance(s, dict):
            briefs.append(StrategyBrief(
                name=s.get("name", ""),
                strategy_type=s.get("strategy_type", "technical"),
                brief_description=s.get("brief_description", ""),
                differentiation=s.get("differentiation", ""),
                key_section_hints=s.get("key_section_hints", []),
            ))

    if not briefs:
        logger.warning("Layer 0 returned empty strategies list — falling back to single")
        return [StrategyBrief(name=pc.title)]

    logger.info("  → %d strategies detected: %s", len(briefs), [b.name for b in briefs])
    return briefs


def _build_strategy_focus(brief: StrategyBrief) -> str:
    """Build the strategy_focus block injected into Layer 1-4 prompts."""
    lines = [
        f"\n>>> FOCUS ON THIS SPECIFIC STRATEGY <<<",
        f"Strategy Name: {brief.name}",
        f"Type: {brief.strategy_type}",
        f"Description: {brief.brief_description}",
    ]
    if brief.differentiation:
        lines.append(f"Differentiation: {brief.differentiation}")
    if brief.key_section_hints:
        lines.append(f"Relevant sections: {', '.join(brief.key_section_hints)}")
    lines.append(
        "Extract ONLY the indicators, logic, and execution details for THIS strategy. "
        "Ignore other strategies described in the paper."
    )
    return "\n".join(lines)


# ── Multi-layer extraction (recommended) ─────────────────────


async def _extract_multilayer(
    pc: PaperContent,
    *,
    model: Optional[str] = None,
    strategy_focus: str = "",
) -> StrategySpec:
    """4-layer extraction pipeline.

    Layer 1: Metadata + data requirements (fills spec basics)
    Layer 2: Indicators (what to compute)
    Layer 3: Logic pipeline (how to use indicators → trade signals)
    Layer 4: Execution plan + risk management (when/how to trade)
    """
    spec = StrategySpec()

    # ── Layer 1: Metadata + Data + Performance ──
    logger.info("Layer 1: Extracting metadata and data requirements...")
    prompt = LAYER1_METADATA_AND_DATA_PROMPT.format(
        title=pc.title,
        abstract=pc.abstract or pc.full_text[:2000],
        methodology=pc.methodology,
        data_description=pc.data_description,
        strategy_focus=strategy_focus,
    )
    l1 = await _call_llm_json(prompt, model=model)
    if l1:
        spec.strategy_name = l1.get("strategy_name", pc.title)
        spec.strategy_type = l1.get("strategy_type", "technical")
        spec.asset_class = l1.get("asset_class", ["equity"])
        spec.description = l1.get("description", "")
        spec.price_data = l1.get("price_data", True)
        spec.volume_data = l1.get("volume_data", False)
        spec.fundamental_data = l1.get("fundamental_data", [])
        spec.alternative_data = l1.get("alternative_data", [])
        spec.lookback_period = l1.get("lookback_period", 200)
        spec.data_frequency = l1.get("data_frequency", "daily")
        spec.data_source = l1.get("data_source", "")
        spec.time_period = l1.get("time_period", "")
        spec.universe_assets = l1.get("universe_assets", [])
        spec.universe_selection_criteria = l1.get("universe_selection_criteria", "")
        spec.expected_sharpe = l1.get("expected_sharpe")
        spec.expected_return = l1.get("expected_return")
        spec.max_drawdown = l1.get("max_drawdown")
        spec.expected_performance = l1.get("expected_performance", {})
        logger.info("  → %s (%s)", spec.strategy_name, spec.strategy_type)

    # ── Layer 2: Indicators ──
    logger.info("Layer 2: Extracting indicators...")
    prompt = LAYER2_INDICATORS_PROMPT.format(
        strategy_name=spec.strategy_name,
        strategy_type=spec.strategy_type,
        description=spec.description,
        signal_logic=pc.signal_logic,
        methodology=pc.methodology,
        strategy_focus=strategy_focus,
    )
    l2 = await _call_llm_json(prompt, model=model)
    if l2:
        raw_indicators = l2.get("indicators", [])
        spec.indicators = [
            Indicator(**{k: v for k, v in ind.items() if k in Indicator.__dataclass_fields__})
            for ind in raw_indicators
            if isinstance(ind, dict)
        ]
        logger.info("  → %d indicators", len(spec.indicators))

    # ── Layer 3: Logic Pipeline ──
    logger.info("Layer 3: Extracting logic pipeline...")
    indicators_summary = "\n".join(
        f"  - {ind.indicator_id}: {ind.name} ({ind.category}, {ind.scope}, output={ind.output_type})"
        for ind in spec.indicators
    ) or "  (no indicators extracted)"
    prompt = LAYER3_LOGIC_PIPELINE_PROMPT.format(
        strategy_name=spec.strategy_name,
        strategy_type=spec.strategy_type,
        indicators_summary=indicators_summary,
        signal_logic=pc.signal_logic,
        methodology=pc.methodology,
        strategy_focus=strategy_focus,
    )
    l3 = await _call_llm_json(prompt, model=model)
    if l3:
        raw_steps = l3.get("logic_pipeline", [])
        spec.logic_pipeline = [
            LogicStep(**{k: v for k, v in step.items() if k in LogicStep.__dataclass_fields__})
            for step in raw_steps
            if isinstance(step, dict)
        ]
        logger.info("  → %d logic steps", len(spec.logic_pipeline))

    # ── Layer 4: Execution Plan + Risk ──
    logger.info("Layer 4: Extracting execution plan...")
    logic_summary = "\n".join(
        f"  - {step.step_id}: {step.description} → output={step.output} ({step.output_type})"
        for step in spec.logic_pipeline
    ) or "  (no logic pipeline extracted)"
    prompt = LAYER4_EXECUTION_PROMPT.format(
        strategy_name=spec.strategy_name,
        strategy_type=spec.strategy_type,
        logic_summary=logic_summary,
        data_description=pc.data_description,
        methodology=pc.methodology,
        strategy_focus=strategy_focus,
    )
    l4 = await _call_llm_json(prompt, model=model)
    if l4:
        raw_plans = l4.get("execution_plan", [])
        spec.execution_plan = [_parse_execution_plan(p) for p in raw_plans if isinstance(p, dict)]
        spec.risk_management = l4.get("risk_management", [])
        logger.info("  → %d execution plans, %d risk rules", len(spec.execution_plan), len(spec.risk_management))

    logger.info(
        "Extraction complete: %s — %d indicators, %d logic steps, %d exec plans",
        spec.strategy_name,
        len(spec.indicators),
        len(spec.logic_pipeline),
        len(spec.execution_plan),
    )
    return spec


# ── Single-call extraction (legacy, simpler) ─────────────────


async def _extract_single_call(
    pc: PaperContent, *, model: Optional[str] = None
) -> StrategySpec:
    """Original single-prompt extraction (kept for comparison / fallback)."""
    prompt = SPECIFICATION_PROMPT.format(
        title=pc.title,
        methodology=pc.methodology,
        signal_logic=pc.signal_logic,
        data_description=pc.data_description,
    )
    raw = await achat(prompt, system=SYSTEM_PROMPT, model=model, max_tokens=8192)
    spec_dict = _parse_json_response(raw)
    return StrategySpec.from_dict(spec_dict)


# ── LLM call with retry + JSON extraction ────────────────────


async def _call_llm_json(
    prompt: str, *, model: Optional[str] = None
) -> Optional[dict]:
    """Call LLM and parse JSON response, with retry on parse failure."""
    for attempt in range(MAX_RETRIES + 1):
        try:
            raw = await achat(prompt, system=SYSTEM_PROMPT, model=model, max_tokens=8192)
            return _parse_json_response(raw)
        except (ValueError, json.JSONDecodeError) as e:
            if attempt < MAX_RETRIES:
                logger.warning("JSON parse failed (attempt %d/%d): %s", attempt + 1, MAX_RETRIES + 1, e)
                await asyncio.sleep(1)
            else:
                logger.error("JSON parse failed after %d attempts: %s", MAX_RETRIES + 1, e)
                return None
    return None


# ── Execution plan parsing helper ─────────────────────────────


def _parse_execution_plan(d: dict) -> ExecutionPlan:
    """Parse a raw dict into an ExecutionPlan with nested dataclasses."""
    trigger_d = d.get("trigger", {})
    action_d = d.get("action", {})
    sizing_d = d.get("position_sizing", {})

    return ExecutionPlan(
        plan_id=d.get("plan_id", ""),
        description=d.get("description", ""),
        trigger=ExecutionTrigger(
            trigger_type=trigger_d.get("trigger_type", "time_driven"),
            frequency=trigger_d.get("frequency", "monthly"),
            signal_lookup=trigger_d.get("signal_lookup", ""),
            delay_bars=trigger_d.get("delay_bars", 1),
            price_type=trigger_d.get("price_type", "open"),
        ),
        action=ExecutionAction(
            signal_source=action_d.get("signal_source", ""),
            logic=action_d.get("logic", ""),
            default_action=action_d.get("default_action", "hold"),
        ),
        position_sizing=PositionSizing(
            method=sizing_d.get("method", "equal_weight"),
            max_position_pct=sizing_d.get("max_position_pct"),
            total_exposure=sizing_d.get("total_exposure", 1.0),
            long_short=sizing_d.get("long_short", "long_only"),
        ),
    )


# ── JSON parsing ──────────────────────────────────────────────


def _parse_json_response(text: str) -> dict:
    """Extract and parse JSON from LLM output, handling markdown fences."""
    text = text.strip()

    # Try direct parse
    if text.startswith("{"):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

    # Try extracting from markdown code fence
    m = re.search(r"```(?:json)?\s*\n?(.*?)```", text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1).strip())
        except json.JSONDecodeError:
            pass

    # Last resort: find outermost { ... }
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start : end + 1])
        except json.JSONDecodeError:
            pass

    raise ValueError(f"Could not parse JSON from LLM response:\n{text[:500]}")
