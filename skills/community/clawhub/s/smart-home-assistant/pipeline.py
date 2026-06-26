from __future__ import annotations

from smart_home import fetcher, analyzer, formatter
from smart_home.models import PipelineConfig


def _validate_config(config: PipelineConfig) -> None:
    if not config.ha_url:
        raise ValueError("HA_URL is not configured. Set home_assistant.url in skill.yaml")
    if not config.ha_token:
        raise ValueError("HA_TOKEN is not configured. Set the HA_TOKEN environment variable")


def run_pipeline(
    config: PipelineConfig,
    formats: list[str] | None = None,
) -> dict[str, str]:
    """Execute the Fetch -> Analyze -> Format pipeline.

    Args:
        config: Pipeline configuration loaded from skill.yaml
        formats: Output formats to produce. Defaults to config.default_outputs.

    Returns:
        Dict mapping format name to formatted output string.
    """
    _validate_config(config)
    formats = formats or config.default_outputs

    # Stage 1: FETCH
    raw_states = fetcher.fetch_states(config.ha_url, config.ha_token)
    filtered = fetcher.filter_energy_entities(raw_states)
    entity_area_map = fetcher.fetch_entity_area_map(config.ha_url, config.ha_token)

    # Stage 2: ANALYZE
    result = analyzer.analyze(filtered, entity_area_map)

    # Stage 3: FORMAT
    known_entity_ids = {e["entity_id"] for e in raw_states}
    outputs: dict[str, str] = {}

    for fmt in formats:
        if fmt == "summary":
            outputs["summary"] = formatter.format_summary(result)
        elif fmt == "table":
            outputs["table"] = formatter.format_table(result)
        elif fmt == "automation":
            outputs["automation"] = formatter.format_automation(result, config, known_entity_ids)

    return outputs
