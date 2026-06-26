"""Tests for User-Agent parser."""

from repro_pack.extractor.user_agent import parse_user_agent, find_user_agents


class TestParseUA:
    def test_chrome_macos(self, ua_string):
        info = parse_user_agent(ua_string)
        assert info.browser == "Chrome"
        assert info.browser_version.startswith("122")
        assert info.os == "macOS"
        assert info.device == "desktop"

    def test_firefox(self):
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"
        info = parse_user_agent(ua)
        assert info.browser == "Firefox"
        assert info.os == "Windows"

    def test_safari_iphone(self):
        ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Mobile/15E148 Safari/604.1"
        info = parse_user_agent(ua)
        assert info.os == "iOS"
        assert info.device == "mobile"

    def test_edge(self):
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
        info = parse_user_agent(ua)
        assert info.browser == "Edge"

    def test_android(self):
        ua = "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.90 Mobile Safari/537.36"
        info = parse_user_agent(ua)
        assert info.os == "Android"
        assert info.device == "mobile"


class TestFindUAs:
    def test_find_in_log(self):
        text = """some log line
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36
another log line"""
        results = find_user_agents(text)
        assert len(results) == 1
        assert results[0].browser == "Chrome"

    def test_find_multiple(self):
        text = """Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"""
        results = find_user_agents(text)
        assert len(results) == 2

    def test_find_none(self):
        results = find_user_agents("no user agent strings here")
        assert results == []
