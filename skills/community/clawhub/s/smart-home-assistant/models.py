from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Device:
    entity_id: str
    name: str
    watts: float
    area: str


@dataclass
class AreaAnalysis:
    name: str
    devices: list[Device]

    @property
    def total_watts(self) -> float:
        return sum(d.watts for d in self.devices)


@dataclass
class AnalysisResult:
    timestamp: str
    total_consumption_w: float
    highest_consumer: Device | None
    areas: list[AreaAnalysis]


@dataclass
class PipelineConfig:
    ha_url: str
    ha_token: str
    threshold_watts: float = 2000
    time_after: str = "06:00"
    time_before: str = "22:00"
    require_occupancy: str = "off"
    action: str = "turn_off"
    default_outputs: list[str] = field(default_factory=lambda: ["summary", "table"])
