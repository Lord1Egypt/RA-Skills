# 自动化框架示例

> 本文件是 ziniao-webdriver-doc 的 Level 2 参考文档。
> 仅在需要查看各语言/框架的示例代码与下载链接时加载。

## 概述

紫鸟 WebDriver 支持多种自动化框架和编程语言。所有示例代码均需替换以下信息后运行：
- 驱动程序路径（ChromeDriver 等）
- 客户端可执行程序路径
- Socket 端口号
- 用户登录信息（company, username, password）

**推荐使用 Selenium**：Playwright 和 Puppeteer 会被平台检测为自动化，需自行处理特征问题。

## 框架支持矩阵

| 框架 | 语言 | 示例文件 | 下载链接 | 备注 |
|------|------|---------|---------|------|
| Selenium | Python | ziniao_webdriver_http_py3.py | [下载](https://cdn-superbrowser-attachment.ziniao.com/webdriver/demo/20260119/ziniao_webdriver_http_py3.py) | 基础店铺访问示例，适合初学者 |
| Selenium | Python | ziniao_webdriver_demo | [GitHub](https://github.com/ziniao-open/ziniao_webdriver_demo) | 开源示例集：订单拉取、报表下载、评价导出 |
| Selenium | Java | webdriver-java-demo.zip | [下载](https://cdn-superbrowser-attachment.ziniao.com/webdriver/demo/20260119/webdriver-java-demo.zip) | 用 IDEA 打开后运行 |
| Selenium | C#.NET | webdriver-C#.net-demo.zip | [下载](https://cdn-superbrowser-attachment.ziniao.com/webdriver/demo/webdriver-CSharp-demo.zip) | Windows 环境 |
| Puppeteer | JavaScript | puppeteer_js_demo.zip | [下载](https://cdn-superbrowser-attachment.ziniao.com/webdriver/demo/20260119/puppeteer_js_demo.zip) | 通过 Puppeteer API 控制 |
| Playwright | Python | ziniao_playwright_http_py3.py | [下载](https://cdn-superbrowser-attachment.ziniao.com/webdriver/demo/20260119/ziniao_playwright_http_py3.py) | 会被检测为自动化，建议用 Selenium |
| Playwright | Java | playwright-java-demo.zip | [下载](https://cdn-superbrowser-attachment.ziniao.com/webdriver/demo/20260119/playwright-java-demo.zip) | 会被检测为自动化，建议用 Selenium |
| Playwright | JavaScript | playwright_js_demo.zip | [下载](https://cdn-superbrowser-attachment.ziniao.com/webdriver/demo/20260119/playwright_js_demo.zip) | 会被检测为自动化，建议用 Selenium |
| DrissionPage | Python | ziniao_drissionpage_http_py3.py | [下载](https://cdn-superbrowser-attachment.ziniao.com/webdriver/demo/20260119/ziniao_drissionpage_http_py3.py) | 通过 DrissionPage API 控制 |

## 连接示例（以 Selenium 为例）

### Python + Selenium

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# startBrowser 返回的 debuggingPort 和 core_version
debugging_port = 12345
core_version = "119.1.0.16"

# 根据 core_version 的大版本号选择对应 ChromeDriver
chrome_driver_path = "/path/to/chromedriver-119"

options = Options()
options.add_experimental_option("debuggerAddress", f"127.0.0.1:{debugging_port}")

service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

# 现在可以操作店铺浏览器窗口
print(driver.title)
```

### Java + Selenium

```java
ChromeOptions options = new ChromeOptions();
options.setExperimentalOption("debuggerAddress", "127.0.0.1:" + debuggingPort);

// 根据 core_version 选择对应版本 ChromeDriver
System.setProperty("webdriver.chrome.driver", "/path/to/chromedriver-" + majorVersion);

WebDriver driver = new ChromeDriver(options);
System.out.println(driver.getTitle());
```

## ChromeDriver 版本匹配

> **⚠ 紫鸟内核版本 ≠ 系统 Chrome 版本。** 不要使用系统安装的 Chrome 浏览器对应的 ChromeDriver，必须根据紫鸟 `startBrowser` 返回的 `core_version` 来匹配。

`startBrowser` 响应中的 `core_type` 和 `core_version` 决定了需要使用的 ChromeDriver 版本：
- `core_type: "Chromium"`, `core_version: "119.1.0.16"` → 使用 ChromeDriver 119.x
- 下载地址：https://googlechromelabs.github.io/chrome-for-testing/
- JSON API（自动化脚本可直接解析）：https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json

版本不匹配会导致连接失败，务必检查。

### 自动下载与缓存策略（Python 伪代码）

```python
import os, re, json, zipfile, io, platform
import requests

CACHE_DIR = "./chromedriver_cache"

def get_chromedriver_path(core_version: str) -> str:
    """根据紫鸟 core_version 获取匹配的 ChromeDriver 路径，自动下载缓存。"""
    major = core_version.split(".")[0]  # "119.1.0.16" → "119"
    
    exe_name = "chromedriver.exe" if platform.system() == "Windows" else "chromedriver"
    cached = os.path.join(CACHE_DIR, major, exe_name)
    
    if os.path.exists(cached):
        return cached
    
    # 查询可用版本
    resp = requests.get(
        "https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json"
    )
    resp.encoding = "utf-8"
    data = resp.json()
    
    # 找到该大版本的最新 chromedriver
    plat = {
        "Windows": "win64", "Darwin": "mac-x64", "Linux": "linux64"
    }[platform.system()]
    
    download_url = None
    for v in reversed(data["versions"]):
        if v["version"].startswith(major + ".") and "chromedriver" in v["downloads"]:
            for d in v["downloads"]["chromedriver"]:
                if d["platform"] == plat:
                    download_url = d["url"]
                    break
            if download_url:
                break
    
    if not download_url:
        raise RuntimeError(f"未找到大版本 {major} 的 ChromeDriver 下载地址")
    
    # 下载并解压
    os.makedirs(os.path.join(CACHE_DIR, major), exist_ok=True)
    zip_resp = requests.get(download_url)
    with zipfile.ZipFile(io.BytesIO(zip_resp.content)) as zf:
        for name in zf.namelist():
            if name.endswith(exe_name):
                with open(cached, "wb") as f:
                    f.write(zf.read(name))
                break
    
    if platform.system() != "Windows":
        os.chmod(cached, 0o755)
    
    return cached
```

### 缓存目录结构

```
chromedriver_cache/
├── 119/
│   └── chromedriver.exe
├── 120/
│   └── chromedriver.exe
└── ...
```

## GitHub 开源示例项目

仓库地址：https://github.com/ziniao-open/ziniao_webdriver_demo

包含以下场景示例：
1. **Demo 1**：电商订单自动拉取（热门推荐）
2. **Demo 2**：销售与流量业务报表下载
3. **Demo 3**：电商平台用户评价导出

克隆后替换配置信息即可运行。
