"""
collectors/calendar.py — Calendar Event Collector

# ⚠️ EXPERIMENTAL: CalDAV collector is a stub implementation.
# Only ICS file parsing is functional.

Collects calendar events from iCal/ICS files or CalDAV servers.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from dataclasses import dataclass

from .base import MemoryCollector, RawMemory, CollectionResult, CollectorStatus

logger = logging.getLogger(__name__)


@dataclass
class CalendarConfig:
    """Calendar collector configuration."""
    source_type: str = "ics"
    ics_path: str = ""
    caldav_url: str = ""
    caldav_user: str = ""
    caldav_password: str = ""
    tenant_id: str = "work"
    reliability_score: float = 0.9


class CalendarCollector(MemoryCollector):
    """Calendar event collector.

    ✅ ICS file parsing: functional
    ⚠️ CalDAV mode: STUB — _fetch_caldav() returns empty list.
    """

    def __init__(self, config: CalendarConfig | dict | None = None):
        if isinstance(config, CalendarConfig):
            cfg = config
        else:
            d = config or {}
            cfg = CalendarConfig(**{k: v for k, v in d.items()
                                    if k in CalendarConfig.__dataclass_fields__})
        super().__init__(config={
            "source_type": cfg.source_type,
            "ics_path": cfg.ics_path,
            "tenant_id": cfg.tenant_id,
            "reliability_score": cfg.reliability_score,
        })
        self._cal_config = cfg
        # ICS parsing is implemented; CalDAV integration is placeholder
        self._is_implemented = (cfg.source_type == "ics")

    def get_source_id(self) -> str:
        return "calendar"

    def test_connection(self) -> dict:
        """Test calendar source connectivity.

        For ICS sources, checks if the file exists (real implementation).
        For CalDAV sources, returns NOT_IMPLEMENTED because _fetch_caldav
        is a placeholder that always returns empty results.
        """
        if self._cal_config.source_type == "ics":
            import os
            exists = os.path.exists(self._cal_config.ics_path)
            if not exists:
                logger.warning(
                    "Calendar: ICS 文件不存在: %s", self._cal_config.ics_path
                )
            return {
                "connected": exists,
                "not_implemented": False,
                "message": "ICS 文件可访问" if exists else f"ICS 文件不存在: {self._cal_config.ics_path}",
            }
        # CalDAV is placeholder
        logger.warning(
            "Calendar: test_connection 返回 NOT_IMPLEMENTED (CalDAV) — "
            "核心 API 集成（_fetch_caldav）为占位实现，尚未对接真实 CalDAV API"
        )
        self.status = CollectorStatus.NOT_IMPLEMENTED
        return {
            "connected": False,
            "not_implemented": True,
            "message": "Calendar CalDAV 收集器为占位实现，核心 API（_fetch_caldav）尚未对接真实 CalDAV 接口，无法获取数据",
        }

    async def collect(self, since: float | None = None) -> CollectionResult:
        result = CollectionResult(
            source=self.get_source_id(),
            started_at=time.time(),
            status=CollectorStatus.SYNCING,
        )

        try:
            if self._cal_config.source_type == "ics":
                events = self._parse_ics(since)
            else:
                events = self._fetch_caldav(since)
                if not events:
                    logger.warning(
                        "Calendar: collect() (CalDAV) 未获取到任何数据 — "
                        "_fetch_caldav 为占位实现，始终返回空列表。"
                        "请完成 CalDAV API 集成后再使用此收集器"
                    )
                    result.warnings.append(
                        "Calendar CalDAV 收集器尚未实现：核心 API（_fetch_caldav）为占位实现，"
                        "始终返回空列表。请完成 CalDAV 服务器 API 集成后再使用此收集器"
                    )

            result.total_available = len(events)
            for evt in events:
                result.items.append(evt)
                result.collected_count += 1

            self.last_sync = time.time()
            self._collect_count += result.collected_count
            result.status = CollectorStatus.IDLE

        except Exception as e:
            result.status = CollectorStatus.ERROR
            result.errors.append(str(e))
            self._error_count += 1

        result.finished_at = time.time()
        return result

    def _parse_ics(self, since: float | None) -> list[RawMemory]:
        """Parse events from an ICS file."""
        import os
        if not os.path.exists(self._cal_config.ics_path):
            return []

        events = []
        try:
            with open(self._cal_config.ics_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Simple ICS parsing (production would use icalendar library)
            in_event = False
            event_data: dict[str, str] = {}
            for line in content.splitlines():
                line = line.strip()
                if line == "BEGIN:VEVENT":
                    in_event = True
                    event_data = {}
                elif line == "END:VEVENT":
                    in_event = False
                    raw = self._event_to_raw(event_data)
                    if raw and (not since or raw.timestamp >= since):
                        events.append(raw)
                elif in_event and ":" in line:
                    key, _, value = line.partition(":")
                    event_data[key] = value
        except Exception as e:
            logger.error("ICS parsing failed: %s", e)

        return events

    # ⚠️ EXPERIMENTAL — 此方法为占位实现，尚未完成 API 对接，不建议在生产环境使用
    def _fetch_caldav(self, since: float | None) -> list[RawMemory]:
        """Fetch events from CalDAV server.

        ⚠️ 占位实现：始终返回空列表，API 集成待完成。
        生产环境应使用 caldav 库对接 CalDAV 服务器
        """
        logger.warning(
            "Calendar: _fetch_caldav 为占位实现，始终返回空列表。"
            "需对接 CalDAV 服务器 API"
        )
        return []

    def _event_to_raw(self, data: dict[str, str]) -> RawMemory | None:
        """Convert parsed event data to RawMemory."""
        summary = data.get("SUMMARY", "")
        description = data.get("DESCRIPTION", "")
        location = data.get("LOCATION", "")
        if not summary:
            return None

        content = summary
        if location:
            content += f"\n地点: {location}"
        if description:
            content += f"\n{description}"

        return RawMemory(
            content=content,
            source="calendar",
            source_id=f"cal_{data.get('UID', hash(summary) % 100000)}",
            timestamp=time.time(),
            metadata={
                "summary": summary,
                "location": location,
                "dtstart": data.get("DTSTART", ""),
                "dtend": data.get("DTEND", ""),
                "attendees": data.get("ATTENDEE", ""),
                "tenant_id": self._cal_config.tenant_id,
            },
        )
