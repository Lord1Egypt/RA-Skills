import pytest
import os
import sys
sys.path.insert(0, '/root/.openclaw/workspace/skills/website-screenshot-tool')

from scripts.website_screenshot import WebsiteScreenshot, ScreenshotScheduler

class TestWebsiteScreenshot:
    def setup_method(self):
        self.tool = WebsiteScreenshot(output_dir="test_screenshots")
    
    def teardown_method(self):
        import shutil
        if os.path.exists("test_screenshots"):
            shutil.rmtree("test_screenshots")
        for f in ["test_history.json"]:
            if os.path.exists(f):
                os.remove(f)
    
    def test_capture_returns_dict(self):
        result = self.tool.capture("example.com", output_name="test1")
        assert isinstance(result, dict)
        assert "url" in result
        assert "file_path" in result
    
    def test_capture_adds_https(self):
        result = self.tool.capture("example.com", output_name="test2")
        assert result["url"].startswith("https://")
    
    def test_capture_preserves_https(self):
        result = self.tool.capture("https://example.com", output_name="test3")
        assert result["url"] == "https://example.com"
    
    def test_capture_auto_name(self):
        result = self.tool.capture("example.com")
        assert result["file_path"].endswith(".png")
        assert "example_com" in result["file_path"]
    
    def test_capture_history_recorded(self):
        before = len(self.tool.get_history())
        self.tool.capture("example.com")
        assert len(self.tool.get_history()) == before + 1
    
    def test_capture_batch(self):
        urls = ["site1.com", "site2.com"]
        results = self.tool.capture_batch(urls)
        assert len(results) == 2
        assert all(isinstance(r, dict) for r in results)
    
    def test_capture_responsive(self):
        results = self.tool.capture_responsive("example.com", output_name="resp")
        assert len(results) == 3
        assert all(r["device"] in ["desktop", "tablet", "mobile"] for r in results)
    
    def test_capture_responsive_custom_devices(self):
        devices = [
            {"name": "tv", "width": 3840, "height": 2160},
            {"name": "watch", "width": 200, "height": 200},
        ]
        results = self.tool.capture_responsive("example.com", devices=devices)
        assert len(results) == 2
        assert results[0]["device"] == "tv"
    
    def test_compare(self):
        diff = self.tool.compare("a.com", "b.com", output_name="diff")
        assert isinstance(diff, dict)
        assert "screenshot_before" in diff
        assert "screenshot_after" in diff
        assert "identical" in diff
        assert isinstance(diff["identical"], bool)
    
    def test_export_history(self):
        self.tool.capture("example.com")
        self.tool.export_history("test_history.json")
        assert os.path.exists("test_history.json")
        
        import json
        with open("test_history.json") as f:
            data = json.load(f)
        assert len(data) >= 1


class TestScreenshotScheduler:
    def setup_method(self):
        self.tool = WebsiteScreenshot(output_dir="test_scheduled")
        self.scheduler = ScreenshotScheduler(self.tool)
    
    def teardown_method(self):
        import shutil
        if os.path.exists("test_scheduled"):
            shutil.rmtree("test_scheduled")
    
    def test_add_job(self):
        self.scheduler.add_job("example.com", interval_minutes=30)
        assert len(self.scheduler.jobs) == 1
        assert self.scheduler.jobs[0]["url"] == "https://example.com"
        assert self.scheduler.jobs[0]["interval"] == 30
    
    def test_run_pending_first_time(self):
        self.scheduler.add_job("example.com", interval_minutes=60)
        results = self.scheduler.run_pending()
        assert len(results) >= 1
    
    def test_run_pending_not_due(self):
        self.scheduler.add_job("example.com", interval_minutes=60)
        self.scheduler.run_pending()  # first run
        results = self.scheduler.run_pending()  # immediate second run should be empty
        assert len(results) == 0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
