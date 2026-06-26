"""
微博热搜获取脚本 - Weibo Hot Search Scraper

通过浏览器自动化技术，实时抓取微博平台各分类下的热门搜索词条。
支持实时、生活、文娱、社会四大分类。

用法:
    python weibo_hot_search.py --category life
    python weibo_hot_search.py --url https://s.weibo.com/top/summary?cate=realtimehot

Author: Kimi (金米) 📈
"""

import json
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException


# 微博热搜分类 URL 映射
CATEGORIES = {
    '实时': 'https://s.weibo.com/top/summary?cate=realtimehot',
    '生活': 'https://s.weibo.com/top/summary?cate=life',
    '文娱': 'https://s.weibo.com/top/summary?cate=entrank',
    '社会': 'https://s.weibo.com/top/summary?cate=socialevent'
}


def get_driver(headless=True, browser='chrome'):
    """
    配置并返回 WebDriver 实例
    
    Args:
        headless: 是否使用无头模式（True=不显示浏览器界面）
        browser: 浏览器类型 ('chrome' or 'edge')
    
    Returns:
        webdriver instance
    """
    options = Options()
    
    # 添加反检测配置
    if headless:
        options.add_argument('--headless')
    
    # Windows 平台特殊处理
    if sys.platform == 'win32':
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
    else:
        # Linux 平台需要额外配置
        if browser == 'chrome':
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
    
    try:
        if browser.lower() == 'edge':
            driver = webdriver.Edge(options=options)
        else:  # chrome (default)
            driver = webdriver.Chrome(options=options)
            
        return driver
        
    except Exception as e:
        print(f"[ERROR] WebDriver 初始化失败：{e}")
        raise


def get_weibo_hot_search(url, headless=True):
    """
    获取微博热搜词条
    
    Args:
        url: 微博热搜页面 URL
        headless: 是否使用无头模式（True=不显示浏览器界面）
    
    Returns:
        dict: 包含热搜数据的字典
            {
                "code": int,       # 状态码 (200=成功)
                "message": str,   # 消息提示
                "data": [         # 热搜词条列表
                    {
                        "title": str,    # 热搜标题
                        "hot": str       # 热度值（数字字符串）
                    },
                    ...
                ]
            }
    """
    
    driver = None
    
    try:
        # 创建浏览器实例
        driver = get_driver(headless=headless)
        
        # 访问页面
        print(f"[INFO] 正在访问：{url}")
        driver.get(url)
        
        # 等待页面加载完成（最多 10 秒）
        wait = WebDriverWait(driver, 10)
        
        # 尝试等待元素出现，如果失败则继续执行
        try:
            wait.until(EC.presence_of_element_located((By.ID, "pl_top_realtimehot")))
        except TimeoutException:
            print("[WARNING] 页面主容器加载超时，尝试获取可用内容...")
        
        # 查找热搜数据
        hot_searches = []
        items = driver.find_elements(By.CSS_SELECTOR, "#pl_top_realtimehot table tbody tr td.td-02 a")
        hot_counts = driver.find_elements(By.CSS_SELECTOR, "#pl_top_realtimehot table tbody tr td.td-02 span")
        
        # 遍历获取数据
        for idx, item in enumerate(items):
            title = item.text.strip()
            
            if title:  # 只添加有标题的条目
                hot_value = "未知"
                if idx < len(hot_counts):
                    hot_value = hot_counts[idx].text.strip()
                
                hot_searches.append({
                    "title": title,
                    "hot": hot_value
                })
        
        # 检查结果是否有效
        if not hot_searches:
            print("[WARNING] 未找到热搜数据，尝试备用选择器...")
            
            # 备用方案：直接查找所有链接和热度数字
            all_links = driver.find_elements(By.CSS_SELECTOR, "#pl_top_realtimehot a[href]")
            results = []
            
            for i, link in enumerate(all_links):
                title = link.text.strip()
                if title:
                    # 尝试从上下文获取热度值
                    parent = link.find_element(By.XPATH, f".//ancestor::td[1]/following-sibling::td/span")
                    hot_value = "未知"
                    try:
                        hot_value = parent.text.strip()
                    except Exception:
                        pass
                    
                    results.append({
                        "title": title,
                        "hot": hot_value
                    })
                    
            # 如果备用方案也失败，返回空结果
            if not results:
                return {
                    "code": 500,
                    "message": "未找到热搜数据",
                    "data": []
                }
            
            hot_searches = results
        
        print(f"[INFO] 成功获取 {len(hot_searches)} 条热搜词条")
        
        return {
            "code": 200,
            "message": "success",
            "data": hot_searches
        }
        
    except TimeoutException:
        return {
            "code": 504,
            "message": "页面加载超时 (10s)",
            "data": []
        }
        
    except WebDriverException as e:
        error_msg = str(e)
        if "net::ERR_CONNECTION" in error_msg or "connection refused" in error_msg:
            return {
                "code": 502,
                "message": "网络连接失败，请检查网络状态",
                "data": []
            }
        else:
            return {
                "code": 503,
                "message": f"浏览器错误：{error_msg}",
                "data": []
            }
            
    except Exception as e:
        return {
            "code": 500,
            "message": str(e),
            "data": []
        }
        
    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass


def main():
    """主函数 - 命令行入口"""
    
    # 默认参数
    category = '生活'
    url = CATEGORIES.get(category)
    headless = True
    
    # 解析命令行参数
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        
        if arg == '--help':
            print("""微博热搜获取工具 - Weibo Hot Search Scraper

用法:
    python weibo_hot_search.py --category <分类>
    python weibo_hot_search.py --url <URL> [--headless] [--json]

参数说明:
    --category   指定热搜分类 (实时/生活/文娱/社会)
    --url        直接指定 URL（优先级更高）
    --headless   使用无头模式 (默认：True)
    --no-headless 显示浏览器界面 (便于调试)
    --json       输出 JSON 格式
    --help       显示此帮助信息

分类列表:
    - 实时    realtimehot
    - 生活    life
    - 文娱    entrank
    - 社会    socialevent
    
示例:
    python weibo_hot_search.py --category 实时 --json
    python weibo_hot_search.py --url https://s.weibo.com/top/summary?cate=life""")
            return
            
        elif arg == '--category':
            if len(sys.argv) > 2:
                category = sys.argv[2]
                url = CATEGORIES.get(category, None)
                
                if not url:
                    print(f"[ERROR] 未知的分类：{category}")
                    print("可用分类：实时/生活/文娱/社会")
                    return
                    
        elif arg == '--url':
            if len(sys.argv) > 2:
                url = sys.argv[2]
                
        elif arg in ['--headless', 'True']:
            headless = True
        elif arg in ['--no-headless', 'False']:
            headless = False
            
    # URL 验证
    if not url:
        print("[ERROR] 未指定有效的分类或 URL")
        return
        
    print(f"[INFO] 开始获取微博热搜...")
    print(f"[INFO] 分类：{category if 'category' in locals() else '自定义'}")
    print(f"[INFO] URL: {url}")
    
    # 执行抓取
    result = get_weibo_hot_search(url, headless=headless)
    
    # JSON 输出（如果请求了）
    output_format = 'text'
    if len(sys.argv) > 2 and '--json' in sys.argv:
        output_format = 'json'
        
    if output_format == 'json':
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # 人类可读格式输出
        print(f"\n{'='*60}")
        print(f"微博热搜 - {category}分类")
        print('='*60)
        
        if result['code'] == 200 and result['data']:
            for idx, item in enumerate(result['data'], 1):
                hot_display = f"[热度:{item['hot']}]" if item['hot'] != '未知' else ""
                print(f"{idx}. {item['title']}{hot_display}")
        else:
            print(f"获取失败：{result['message']}")
        
        print('='*60)


if __name__ == "__main__":
    main()
