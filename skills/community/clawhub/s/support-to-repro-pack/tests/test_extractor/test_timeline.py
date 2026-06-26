"""Tests for timeline building."""

from repro_pack.extractor.timeline import build_timeline, timeline_to_markdown
from repro_pack.models import LogEntry


class TestBuildTimeline:
    def _make_entries(self):
        return [
            LogEntry(timestamp="2024-03-25T10:00:01Z", level="INFO", message="Server started", line_number=1),
            LogEntry(timestamp="2024-03-25T10:00:05Z", level="ERROR", message="Connection failed to database", line_number=2),
            LogEntry(timestamp="2024-03-25T10:00:06Z", level="WARN", message="Retrying connection attempt 1", line_number=3),
            LogEntry(timestamp="2024-03-25T10:00:10Z", level="INFO", message="Normal operation resumed", line_number=4),
        ]

    def test_filters_interesting_events(self):
        entries = self._make_entries()
        events = build_timeline(entries)
        # "Connection failed" and "Retrying" should be included
        assert len(events) >= 2

    def test_include_all(self):
        entries = self._make_entries()
        events = build_timeline(entries, include_all=True)
        assert len(events) == 4

    def test_sorted_by_timestamp(self):
        entries = [
            LogEntry(timestamp="2024-03-25T10:00:10Z", message="later error event", line_number=1),
            LogEntry(timestamp="2024-03-25T10:00:01Z", message="earlier error event", line_number=2),
        ]
        events = build_timeline(entries, include_all=True)
        assert events[0].timestamp < events[1].timestamp

    def test_skips_entries_without_timestamp(self):
        entries = [
            LogEntry(timestamp=None, message="no timestamp error event", line_number=1),
            LogEntry(timestamp="2024-03-25T10:00:01Z", message="has timestamp error", line_number=2),
        ]
        events = build_timeline(entries, include_all=True)
        assert len(events) == 1

    def test_empty_entries(self):
        events = build_timeline([])
        assert events == []


class TestTimelineMarkdown:
    def test_renders_table(self):
        from repro_pack.models import TimelineEvent
        events = [
            TimelineEvent(timestamp="2024-03-25T10:00:01Z", event="Test event", level="ERROR"),
        ]
        md = timeline_to_markdown(events)
        assert "| Timestamp" in md
        assert "Test event" in md

    def test_empty_events(self):
        md = timeline_to_markdown([])
        assert "No timeline" in md
