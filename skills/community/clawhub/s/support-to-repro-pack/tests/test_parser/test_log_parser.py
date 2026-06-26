"""Tests for log parser."""

from repro_pack.parser.log_parser import parse_log
from repro_pack.parser.formats import detect_format, detect_file_format
from repro_pack.models import LogFormat


class TestFormatDetection:
    def test_detect_json(self):
        assert detect_format('{"timestamp":"2024-01-01","level":"INFO","message":"test"}') == LogFormat.JSON

    def test_detect_syslog(self):
        assert detect_format("Mar 25 10:00:01 server nginx[1234]: test") == LogFormat.SYSLOG

    def test_detect_plain(self):
        assert detect_format("2024-03-25 10:00:01 INFO some message") == LogFormat.PLAIN

    def test_detect_empty(self):
        assert detect_format("") == LogFormat.UNKNOWN

    def test_detect_file_format_json(self, json_log):
        assert detect_file_format(json_log) == LogFormat.JSON

    def test_detect_file_format_syslog(self, syslog):
        assert detect_file_format(syslog) == LogFormat.SYSLOG


class TestLogParser:
    def test_parse_json_log(self, json_log):
        entries = parse_log(json_log)
        assert len(entries) == 4
        assert entries[0].level == "INFO"
        assert entries[0].message == "Server started"
        assert entries[0].source == "main"

    def test_parse_syslog(self, syslog):
        entries = parse_log(syslog)
        assert len(entries) == 3
        assert entries[0].timestamp is not None
        assert "nginx" in (entries[0].source or "")

    def test_parse_plain_log(self):
        text = "2024-03-25 14:02:11 ERROR Something went wrong\n2024-03-25 14:02:12 INFO Recovery started"
        entries = parse_log(text)
        assert len(entries) == 2
        assert entries[0].level == "ERROR"
        assert entries[1].level == "INFO"

    def test_parse_extracts_timestamps(self, json_log):
        entries = parse_log(json_log)
        assert all(e.timestamp is not None for e in entries)

    def test_parse_empty(self):
        entries = parse_log("")
        assert entries == []

    def test_parse_preserves_line_numbers(self, json_log):
        entries = parse_log(json_log)
        assert entries[0].line_number == 1
        assert entries[1].line_number == 2
