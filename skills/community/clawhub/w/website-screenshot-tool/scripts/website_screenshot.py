import os
import json
import time
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from urllib.parse import urlparse

class WebsiteScreenshot:
    """Website Screenshot Automation Tool - 网站自动化截图工具"""
    
    def __init__(self, output_dir: str = "screenshots", default_width: int = 1920, 
                 default_height: int = 1080):
        self.output_dir = output_dir
        self.default_width = default_width
        self.default_height = default_height
        self.history: List[Dict] = []
        
        os.makedirs(output_dir, exist_ok=True)
    
    def capture(self, url: str, output_name: Optional[str] = None,
                full_page: bool = False, width: Optional[int] = None,
                height: Optional[int] = None, delay: int = 2) -> Dict:
        """
        捕获网站截图
        
        Args:
            url: 目标网址
            output_name: 输出文件名（不含扩展名），None则自动生成
            full_page: 是否截取完整页面
            width: 视口宽度
            height: 视口高度
            delay: 加载后等待秒数
        
        Returns:
            Dict 包含 file_path, url, timestamp, dimensions
        """
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        if output_name is None:
            domain = urlparse(url).netloc.replace('.', '_')
            output_name = f"{domain}_{int(time.time())}"
        
        output_path = os.path.join(self.output_dir, f"{output_name}.png")
        
        # 使用 Playwright/Selenium 或回退到命令行工具
        result = self._capture_with_playwright(
            url, output_path, full_page, 
            width or self.default_width, 
            height or self.default_height,
            delay
        )
        
        entry = {
            "url": url,
            "file_path": output_path,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "full_page": full_page,
            "dimensions": f"{width or self.default_width}x{height or self.default_height}",
            "success": result,
        }
        self.history.append(entry)
        return entry
    
    def _capture_with_playwright(self, url: str, output_path: str, full_page: bool,
                                  width: int, height: int, delay: int) -> bool:
        """使用 Playwright 截图"""
        try:
            from playwright.sync_api import sync_playwright
            
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page(viewport={"width": width, "height": height})
                page.goto(url, wait_until="networkidle")
                
                if delay > 0:
                    time.sleep(delay)
                
                if full_page:
                    page.screenshot(path=output_path, full_page=True)
                else:
                    page.screenshot(path=output_path)
                
                browser.close()
                return True
                
        except ImportError:
            # Playwright 未安装，尝试使用 selenium
            return self._capture_with_selenium(url, output_path, full_page, width, height, delay)
        except Exception as e:
            print(f"Playwright error: {e}")
            return False
    
    def _capture_with_selenium(self, url: str, output_path: str, full_page: bool,
                                width: int, height: int, delay: int) -> bool:
        """使用 Selenium 截图（回退方案）"""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.chrome.service import Service
            
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument(f"--window-size={width},{height}")
            chrome_options.add_argument("--disable-gpu")
            
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(url)
            
            if delay > 0:
                time.sleep(delay)
            
            if full_page:
                # 获取完整页面高度
                total_height = driver.execute_script("return document.body.scrollHeight")
                driver.set_window_size(width, total_height)
                time.sleep(0.5)
            
            driver.save_screenshot(output_path)
            driver.quit()
            return True
            
        except ImportError:
            print("Neither playwright nor selenium is installed.")
            print("Install with: pip install playwright && playwright install")
            return False
        except Exception as e:
            print(f"Selenium error: {e}")
            return False
    
    def capture_batch(self, urls: List[str], full_page: bool = False,
                      delay: int = 2) -> List[Dict]:
        """批量截图多个网站"""
        results = []
        for i, url in enumerate(urls):
            print(f"Capturing [{i+1}/{len(urls)}]: {url}")
            result = self.capture(url, full_page=full_page, delay=delay)
            results.append(result)
        return results
    
    def capture_responsive(self, url: str, output_name: Optional[str] = None,
                           devices: Optional[List[Dict]] = None) -> List[Dict]:
        """
        响应式截图 - 模拟多种设备尺寸
        
        默认设备: Desktop, Tablet, Mobile
        """
        if devices is None:
            devices = [
                {"name": "desktop", "width": 1920, "height": 1080},
                {"name": "tablet", "width": 768, "height": 1024},
                {"name": "mobile", "width": 375, "height": 812},
            ]
        
        results = []
        for device in devices:
            name = f"{output_name or urlparse(url).netloc}_{device['name']}"
            result = self.capture(
                url, output_name=name,
                width=device["width"], height=device["height"]
            )
            result["device"] = device["name"]
            results.append(result)
        
        return results
    
    def compare(self, url1: str, url2: str, output_name: str = "comparison") -> Dict:
        """
        对比两个网页的视觉差异
        
        截图两个URL并生成差异报告
        """
        import hashlib
        
        shot1 = self.capture(url1, output_name=f"{output_name}_before")
        shot2 = self.capture(url2, output_name=f"{output_name}_after")
        
        # 如果截图失败，返回差异未知
        identical = False
        if shot1.get("success") and shot2.get("success"):
            def file_hash(path):
                with open(path, 'rb') as f:
                    return hashlib.md5(f.read()).hexdigest()
            identical = file_hash(shot1["file_path"]) == file_hash(shot2["file_path"])
        
        return {
            "url_before": shot1.get("url", url1),
            "url_after": shot2.get("url", url2),
            "screenshot_before": shot1.get("file_path"),
            "screenshot_after": shot2.get("file_path"),
            "identical": identical,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
    
    def get_history(self) -> List[Dict]:
        """获取截图历史记录"""
        return self.history
    
    def export_history(self, output_path: str = "screenshot_history.json") -> None:
        """导出历史记录为JSON"""
        with open(output_path, 'w') as f:
            json.dump(self.history, f, indent=2)


class ScreenshotScheduler:
    """截图定时任务调度器"""
    
    def __init__(self, screenshot_tool: WebsiteScreenshot):
        self.tool = screenshot_tool
        self.jobs: List[Dict] = []
    
    def add_job(self, url: str, interval_minutes: int, 
                output_name: Optional[str] = None) -> None:
        """添加定时截图任务"""
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        self.jobs.append({
            "url": url,
            "interval": interval_minutes,
            "output_name": output_name,
            "last_run": None,
        })
    
    def run_pending(self) -> List[Dict]:
        """执行所有到期的任务"""
        now = time.time()
        results = []
        
        for job in self.jobs:
            if job["last_run"] is None or \
               (now - job["last_run"]) >= job["interval"] * 60:
                result = self.tool.capture(job["url"], job["output_name"])
                job["last_run"] = now
                results.append(result)
        
        return results


if __name__ == "__main__":
    # 演示
    tool = WebsiteScreenshot(output_dir="demo_screenshots")
    
    # 单页截图
    result = tool.capture("example.com", output_name="demo_single")
    print(json.dumps(result, indent=2))
    
    # 响应式截图
    results = tool.capture_responsive("example.com", output_name="demo_responsive")
    for r in results:
        print(f"Device: {r['device']}, Saved: {r['file_path']}")
    
    # 导出历史
    tool.export_history()
    print(f"\nHistory exported to screenshot_history.json")
    print(f"Total screenshots: {len(tool.get_history())}")
    
    # 清理
    import shutil
    if os.path.exists("demo_screenshots"):
        shutil.rmtree("demo_screenshots")
    if os.path.exists("screenshot_history.json"):
        os.remove("screenshot_history.json")
