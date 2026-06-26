import os
import sys
sys.path.insert(0, '/root/.openclaw/workspace/skills/website-screenshot-tool')

from scripts.website_screenshot import WebsiteScreenshot, ScreenshotScheduler

def demo_single_capture():
    print("=== Single Page Capture Demo ===\n")
    
    tool = WebsiteScreenshot(output_dir="demo_screenshots")
    
    # 基础截图（模拟模式，无需真实浏览器）
    print("1. Basic viewport capture:")
    result = tool.capture("example.com", output_name="basic")
    print(f"   URL: {result['url']}")
    print(f"   Success: {result['success']}")
    print(f"   Path: {result['file_path']}")
    
    # 全页面截图
    print("\n2. Full page capture:")
    result = tool.capture("example.com", output_name="full", full_page=True)
    print(f"   Full page: {result['full_page']}")
    print(f"   Success: {result['success']}")


def demo_responsive_capture():
    print("\n=== Responsive Capture Demo ===\n")
    
    tool = WebsiteScreenshot(output_dir="demo_screenshots")
    
    # 响应式截图
    print("3. Responsive screenshots:")
    results = tool.capture_responsive("example.com", output_name="responsive")
    
    for r in results:
        print(f"   Device: {r['device']}, Dimensions: {r['dimensions']}, Success: {r['success']}")


def demo_batch_capture():
    print("\n=== Batch Capture Demo ===\n")
    
    tool = WebsiteScreenshot(output_dir="demo_screenshots")
    
    # 批量截图
    urls = ["site1.com", "site2.com", "site3.com"]
    print(f"4. Batch capture of {len(urls)} URLs:")
    results = tool.capture_batch(urls)
    
    for r in results:
        print(f"   {r['url']}: Success={r['success']}")


def demo_comparison():
    print("\n=== Comparison Demo ===\n")
    
    tool = WebsiteScreenshot(output_dir="demo_screenshots")
    
    # 对比两个版本
    print("5. Visual comparison:")
    diff = tool.compare("v1.example.com", "v2.example.com", output_name="version_diff")
    print(f"   Before: {diff['screenshot_before']}")
    print(f"   After: {diff['screenshot_after']}")
    print(f"   Identical: {diff['identical']}")


def demo_scheduler():
    print("\n=== Scheduler Demo ===\n")
    
    tool = WebsiteScreenshot(output_dir="demo_screenshots")
    scheduler = ScreenshotScheduler(tool)
    
    # 添加定时任务
    print("6. Scheduled jobs:")
    scheduler.add_job("monitor.example.com", interval_minutes=60, output_name="hourly_check")
    
    print(f"   Jobs registered: {len(scheduler.jobs)}")
    print(f"   Job 1: URL={scheduler.jobs[0]['url']}, Interval={scheduler.jobs[0]['interval']}min")


def demo_history():
    print("\n=== History Demo ===\n")
    
    tool = WebsiteScreenshot(output_dir="demo_screenshots")
    
    # 生成一些记录
    tool.capture("a.com")
    tool.capture("b.com")
    tool.capture("c.com")
    
    print("7. History tracking:")
    print(f"   Total captures: {len(tool.get_history())}")
    
    # 导出历史
    tool.export_history("demo_history.json")
    print(f"   History exported to demo_history.json")
    
    # 清理
    if os.path.exists("demo_history.json"):
        os.remove("demo_history.json")


if __name__ == "__main__":
    demo_single_capture()
    demo_responsive_capture()
    demo_batch_capture()
    demo_comparison()
    demo_scheduler()
    demo_history()
    
    # 清理演示目录
    import shutil
    if os.path.exists("demo_screenshots"):
        shutil.rmtree("demo_screenshots")
