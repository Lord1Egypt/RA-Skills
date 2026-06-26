"""Tests for ticket parser."""

from repro_pack.parser.ticket_parser import parse_ticket


class TestMarkdownTicket:
    def test_parse_title(self, clean_ticket):
        info = parse_ticket(clean_ticket)
        assert "Dashboard Timeout" in info.title

    def test_parse_sections(self, clean_ticket):
        info = parse_ticket(clean_ticket)
        assert len(info.sections) > 0

    def test_parse_description(self, clean_ticket):
        info = parse_ticket(clean_ticket)
        assert "timeout" in info.description.lower() or len(info.description) > 0


class TestPlainTicket:
    def test_parse_plain_text(self):
        text = "The login page is broken. Users cannot sign in since 10am."
        info = parse_ticket(text)
        assert info.title != ""
        assert info.description == text.strip()

    def test_parse_empty(self):
        info = parse_ticket("")
        assert info.title == ""
