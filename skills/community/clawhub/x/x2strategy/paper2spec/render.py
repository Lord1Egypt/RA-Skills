"""Render pipeline outputs as human-readable Markdown.

Two renderers:
  content_to_markdown(PaperContent) → Markdown summary of parsed paper
  spec_to_markdown(ExtractionResult) → Markdown summary of extracted strategies
"""

from paper2spec.models import (
    ExtractionResult,
    Indicator,
    LogicStep,
    ExecutionPlan,
    PaperContent,
    StrategySpec,
)


def content_to_markdown(pc: PaperContent) -> str:
    """Render PaperContent as a readable Markdown summary."""
    lines = [f"# {pc.title or 'Untitled Paper'}", ""]

    if pc.abstract:
        lines += ["> " + pc.abstract.replace("\n", "\n> "), ""]

    for section, label in [
        (pc.methodology, "Methodology"),
        (pc.data_description, "Data Description"),
        (pc.signal_logic, "Signal Logic"),
    ]:
        if section:
            # Truncate very long sections for readability
            text = section if len(section) <= 3000 else section[:3000] + "\n\n*(truncated)*"
            lines += [f"## {label}", "", text, ""]

    if pc.formulas:
        lines += ["## Key Formulas", ""]
        for f in pc.formulas:
            lines += [f"- ${f}$"]
        lines.append("")

    stats = []
    if pc.full_text:
        stats.append(f"Full text: {len(pc.full_text):,} chars")
    if pc.tables:
        stats.append(f"Tables: {len(pc.tables)}")
    if pc.references:
        stats.append(f"References: {len(pc.references)}")
    if stats:
        lines += ["---", f"*{' | '.join(stats)}*", ""]

    return "\n".join(lines)


def spec_to_markdown(result: ExtractionResult) -> str:
    """Render ExtractionResult as a readable Markdown summary."""
    lines = [f"# {result.paper_title or 'Strategy Specification'}", ""]

    if result.num_detected > 1:
        lines += [
            f"> **{result.num_detected} independent strategies** detected in this paper.",
            "",
        ]

    for i, spec in enumerate(result.strategies):
        if result.num_detected > 1:
            lines += [f"---", "", f"## Strategy {i+1}: {spec.strategy_name}", ""]
        else:
            lines += [f"## {spec.strategy_name}", ""]

        lines += _render_strategy(spec)

    return "\n".join(lines)


def _render_strategy(spec: StrategySpec) -> list[str]:
    """Render a single StrategySpec into Markdown lines."""
    lines: list[str] = []

    # ── Overview ──
    lines += [f"**Type**: {spec.strategy_type}"]
    if spec.asset_class:
        lines += [f"**Asset Class**: {', '.join(spec.asset_class)}"]
    if spec.description:
        lines += ["", spec.description]
    lines.append("")

    # ── Data Requirements ──
    data_items: list[str] = []
    if spec.data_source:
        data_items.append(f"**Source**: {spec.data_source}")
    if spec.time_period:
        data_items.append(f"**Period**: {spec.time_period}")
    data_items.append(f"**Frequency**: {spec.data_frequency}")
    if spec.universe_assets:
        data_items.append(f"**Universe**: {', '.join(spec.universe_assets)}")
    if spec.universe_selection_criteria:
        data_items.append(f"**Filters**: {spec.universe_selection_criteria}")

    data_fields: list[str] = []
    if spec.price_data:
        data_fields.append("Price")
    if spec.volume_data:
        data_fields.append("Volume")
    if spec.fundamental_data:
        data_fields += spec.fundamental_data
    if spec.alternative_data:
        data_fields += spec.alternative_data
    if data_fields:
        data_items.append(f"**Data fields**: {', '.join(data_fields)}")
    data_items.append(f"**Lookback**: {spec.lookback_period} bars")

    lines += ["### Data Requirements", ""]
    for item in data_items:
        lines.append(f"- {item}")
    lines.append("")

    # ── Performance ──
    perf_items: list[str] = []
    if spec.expected_sharpe is not None:
        perf_items.append(f"Sharpe: {spec.expected_sharpe}")
    if spec.expected_return is not None:
        ret_pct = spec.expected_return * 100 if abs(spec.expected_return) < 1 else spec.expected_return
        perf_items.append(f"Annual Return: {ret_pct:.1f}%")
    if spec.max_drawdown is not None:
        dd_pct = spec.max_drawdown * 100 if abs(spec.max_drawdown) < 1 else spec.max_drawdown
        perf_items.append(f"Max Drawdown: {dd_pct:.1f}%")
    if perf_items:
        lines += ["### Expected Performance", ""]
        for item in perf_items:
            lines.append(f"- {item}")
        lines.append("")

    # ── Indicators ──
    if spec.indicators:
        lines += [f"### Indicators ({len(spec.indicators)})", ""]
        lines.append("| ID | Name | Category | Formula | Scope |")
        lines.append("|:---|:-----|:---------|:--------|:------|")
        for ind in spec.indicators:
            formula = ind.formula[:80] + "…" if len(ind.formula) > 80 else ind.formula
            lines.append(
                f"| `{ind.indicator_id}` | {ind.name} | {ind.category} | {formula} | {ind.scope} |"
            )
        lines.append("")

    # ── Logic Pipeline ──
    if spec.logic_pipeline:
        lines += [f"### Logic Pipeline ({len(spec.logic_pipeline)} steps)", ""]
        for step in spec.logic_pipeline:
            detail = f" — `{step.expression}`" if step.expression else ""
            lines.append(
                f"{step.step_id}. **{step.function}** ({step.scope}): "
                f"{step.description}{detail}  "
            )
            lines.append(f"   → output: `{step.output}` ({step.output_type})")
        lines.append("")

    # ── Execution Plan ──
    if spec.execution_plan:
        lines += [f"### Execution ({len(spec.execution_plan)} plans)", ""]
        for plan in spec.execution_plan:
            t = plan.trigger
            a = plan.action
            p = plan.position_sizing
            lines.append(f"**{plan.plan_id}**: {plan.description}")
            lines.append(f"- Trigger: {t.trigger_type}, {t.frequency}, delay={t.delay_bars} bar(s)")
            if a.logic:
                lines.append(f"- Action: `{a.logic}`")
            lines.append(f"- Sizing: {p.method}, exposure={p.total_exposure}, {p.long_short}")
            lines.append("")

    # ── Risk Management ──
    if spec.risk_management:
        lines += [f"### Risk Management ({len(spec.risk_management)} rules)", ""]
        for rule in spec.risk_management:
            lines.append(f"- {rule}")
        lines.append("")

    return lines
