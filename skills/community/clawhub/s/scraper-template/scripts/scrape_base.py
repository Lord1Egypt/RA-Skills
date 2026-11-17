#!/usr/bin/env python3
"""
开放平台API抓取通用框架 v1.0
- 基于 Playwright 的 SPA 页面数据提取
- 支持树形菜单导航 + 表格数据解析
- 标准化输出格式

使用方法：
    子类化 OpenPlatformScraper，实现以下方法：
    - get_api_list() → [(api_id, api_name, data_key), ...]
    - extract_api_detail(page) → {method, path, params, ...}
"""
from playwright.sync_api import sync_playwright
import time, json, os, re
from pathlib import Path
from abc import ABC, abstractmethod


class OpenPlatformScraper(ABC):
    """开放平台抓取基类"""
    
    def __init__(self, base_url: str, output_dir: str, name: str = "unknown"):
        self.base_url = base_url
        self.output_dir = Path(output_dir)
        self.name = name
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    # ========== 抽象方法（子类必须实现） ==========
    
    @abstractmethod
    def expand_menu(self, page) -> dict:
        """
        展开页面导航菜单，发现所有 API 模块
        返回: {module_id: {name, api_count, sub_modules: {sub_id: {name, apis: []}}}}
        """
        pass
    
    @abstractmethod
    def navigate_to_api(self, page, api_key, api_info) -> bool:
        """
        导航到指定 API 详情页
        返回: 是否成功
        """
        pass
    
    @abstractmethod
    def extract_api_detail(self, page) -> dict:
        """
        从当前页面提取 API 详情
        返回: {method, path, title, request_params[], response_params[], response_example}
        """
        pass
    
    # ========== 通用方法（可复用） ==========
    
    def launch_browser(self):
        """启动浏览器"""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        self.page = self.browser.new_page(viewport={"width": 1440, "height": 1200})
        self.page.set_default_timeout(15000)
        
    def close_browser(self):
        """关闭浏览器"""
        if hasattr(self, 'browser'):
            self.browser.close()
        if hasattr(self, 'playwright'):
            self.playwright.stop()
    
    def load_page(self, timeout=30000):
        """加载基础页面"""
        self.page.goto(self.base_url, timeout=timeout)
        time.sleep(5)
    
    def extract_tables(self, page) -> list:
        """提取页面所有表格数据"""
        tables_data = []
        tables = page.query_selector_all("table")
        
        for table in tables:
            rows = table.query_selector_all("tr")
            if not rows:
                continue
            
            headers = [c.inner_text().strip() for c in rows[0].query_selector_all("th")]
            if not headers:
                headers = [c.inner_text().strip() for c in rows[0].query_selector_all("td")]
            
            data_rows = []
            for row in rows[1:]:
                cells = [c.inner_text().strip() for c in row.query_selector_all("td")]
                if cells:
                    data_rows.append(cells)
            
            tables_data.append({"headers": headers, "rows": data_rows})
        
        return tables_data
    
    def extract_api_paths(self, text: str) -> list:
        """从文本中提取 API 路径"""
        return list(set(re.findall(r'(/[a-zA-Z0-9_/]+(?:/[a-zA-Z0-9_{}_/]+)*)', text)))
    
    def detect_method(self, path: str, title: str = "") -> str:
        """从路径/标题推断 HTTP 方法"""
        text = (path + " " + title).lower()
        read_words = ["get", "query", "search", "list", "detail", "find", "info", "page", "fetch"]
        write_words = ["create", "add", "save", "update", "modify", "delete", "remove", "sync", 
                       "submit", "upload", "bind", "unbind", "issue", "grant", "revoke",
                       "enable", "disable", "freeze", "unfreeze"]
        
        for w in read_words:
            if w in text:
                return "GET"
        for w in write_words:
            if w in text:
                return "POST"
        return "POST"
    
    def extract_response_example(self, page) -> dict:
        """提取 JSON 响应示例"""
        code_blocks = page.query_selector_all("code") or page.query_selector_all("pre")
        best = None
        for block in code_blocks:
            text = block.inner_text().strip()
            try:
                obj = json.loads(text)
                if isinstance(obj, dict) and (best is None or len(obj) > len(best)):
                    best = obj
            except:
                pass
        return best
    
    def safe_click(self, node, force=False):
        """安全点击（处理不可见元素）"""
        try:
            if not force:
                node.scroll_into_view_if_needed()
                time.sleep(0.3)
            node.click(force=force)
            time.sleep(0.5)
            return True
        except Exception:
            try:
                node.click(force=True)
                time.sleep(0.5)
                return True
            except:
                return False
    
    def click_by_selector(self, selector, timeout=2):
        """通过 CSS 选择器点击"""
        node = self.page.query_selector(selector)
        if node:
            return self.safe_click(node)
        return False
    
    def click_by_text(self, text, element="*"):
        """通过文本匹配点击"""
        node = self.page.query_selector(f'{element}:has-text("{text}")')
        if node:
            return self.safe_click(node)
        return False
    
    # ========== 标准流程 ==========
    
    def scrape(self):
        """执行完整抓取流程"""
        print(f"🚀 开始抓取 {self.name} 开放平台")
        print(f"   URL: {self.base_url}")
        print(f"   输出: {self.output_dir}")
        
        self.launch_browser()
        
        try:
            # Step 1: 加载页面
            print("\n📂 加载页面...")
            self.load_page()
            
            # Step 2: 展开菜单 & 发现模块
            print("🔍 展开菜单 & 发现模块...")
            modules = self.expand_menu(self.page)
            
            # Step 3: 统计
            total_apis = 0
            for mid, mod in modules.items():
                for sid, sub in mod.get("sub_modules", {}).items():
                    total_apis += len(sub.get("apis", []))
                total_apis += len(mod.get("direct_apis", []))
            
            print(f"📊 发现 {len(modules)} 个大类，预估 {total_apis} 个接口")
            
            # Step 4: 逐模块抓取详情
            print(f"\n🔬 抓取 API 详情...")
            extracted = 0
            skipped = 0
            
            for mid, mod in modules.items():
                # 处理直接 API（无子模块）
                for api in mod.get("direct_apis", []):
                    try:
                        if self.navigate_to_api(self.page, api["key"], api):
                            time.sleep(2)
                            detail = self.extract_api_detail(self.page)
                            api["detail"] = detail
                            extracted += 1
                            path = detail.get("path", "?")[:30]
                            print(f"  ✅ {api['id']} {detail['method']} {path}")
                        else:
                            skipped += 1
                            print(f"  ❌ {api['id']} nav failed")
                    except Exception as e:
                        skipped += 1
                        print(f"  ❌ {api['id']} {e}")
                
                # 处理子模块 API
                for sid, sub in mod.get("sub_modules", {}).items():
                    for api in sub.get("apis", []):
                        try:
                            if self.navigate_to_api(self.page, api["key"], api):
                                time.sleep(2)
                                detail = self.extract_api_detail(self.page)
                                api["detail"] = detail
                                extracted += 1
                                path = detail.get("path", "?")[:30]
                                print(f"  ✅ {api['id']} {detail['method']} {path}")
                            else:
                                skipped += 1
                                print(f"  ❌ {api['id']} nav failed")
                        except Exception as e:
                            skipped += 1
                            print(f"  ❌ {api['id']} {e}")
            
            print(f"\n✅ 抓取完成: {extracted} 成功, {skipped} 跳过")
            
            # Step 5: 保存数据
            self.save_results(modules)
            
            return modules
            
        finally:
            self.close_browser()
    
    def save_results(self, modules: dict):
        """保存抓取结果"""
        # 保存全量数据
        full_path = self.output_dir / "_all_modules.json"
        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(modules, f, ensure_ascii=False, indent=2)
        print(f"📄 全量数据: {full_path}")
        
        # 分模块保存
        for mid, mod in modules.items():
            interfaces = []
            for api in mod.get("direct_apis", []):
                d = api.get("detail", {})
                interfaces.append({
                    "id": api["id"], "name": api["name"],
                    "method": d.get("method", "POST"), "path": d.get("path", ""),
                    "request_params": d.get("request_params", []),
                    "response_params": d.get("response_params", []),
                    "response_example": d.get("response_example"),
                })
            
            for sid, sub in mod.get("sub_modules", {}).items():
                for api in sub.get("apis", []):
                    d = api.get("detail", {})
                    interfaces.append({
                        "id": api["id"], "name": api["name"],
                        "method": d.get("method", "POST"), "path": d.get("path", ""),
                        "request_params": d.get("request_params", []),
                        "response_params": d.get("response_params", []),
                        "response_example": d.get("response_example"),
                    })
            
            if interfaces:
                safe_name = mod["name"].replace("/", "-")
                file_path = self.output_dir / f"{mid}_{safe_name}.json"
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump({
                        "module_id": mid, "module_name": mod["name"],
                        "interface_count": len(interfaces), "interfaces": interfaces,
                        "source": f"playwright_scraped_{self.name}",
                    }, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 分模块数据已保存到 {self.output_dir}")
