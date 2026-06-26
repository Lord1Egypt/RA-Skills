# Stealth.min.js 说明文档

## 📄 文件信息

- **文件名**: `stealth.min.js`
- **用途**: 浏览器反爬虫检测绕过脚本
- **大小**: 约 200KB (压缩版)

## 🔗 来源信息

- **生成工具**: `puppeteer-extra` 的 `extract-stealth-evasions`
- **原始仓库**: [`berstend/puppeteer-extra`](https://github.com/berstend/puppeteer-extra)
- **许可证**: MIT License
- **生成时间**: 2026-02-02

## 🛠️ 技术原理

该脚本包含多种反检测补丁(evasions)，主要功能包括：

### 🔧 核心补丁
- **navigator.webdriver** - 隐藏/修补webdriver标识
- **window.chrome** - 模拟Chrome浏览器环境
- **chrome.runtime/csi/loadTimes** - 补齐Chrome特有API
- **plugins/mimeTypes** - 补全浏览器插件信息

### 🎭 环境伪装
- **navigator.languages** - 修补语言设置
- **hardwareConcurrency** - 伪装硬件信息
- **WebGL vendor/renderer** - 显卡信息伪装
- **Notification/Permissions** - 权限行为修补
- **iframe/outerWidth/outerHeight** - 窗口尺寸细节修补

## 📋 使用方式

在Playwright中通过 `add_init_script()` 加载：

```python
from playwright.sync_api import sync_playwright
import os

# 获取stealth脚本路径
stealth_path = os.path.join(os.path.dirname(__file__), 'stealth.min.js')

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context()
    
    # 加载反检测脚本
    if os.path.exists(stealth_path):
        context.add_init_script(path=stealth_path)
    
    page = context.new_page()
    # ... 其他操作
```

## ⚖️ 法律说明

- ✅ **开源许可**: MIT License允许自由使用、修改和分发
- ✅ **社区项目**: 来自知名开源项目，广泛使用
- ⚠️ **使用责任**: 请确保使用符合目标网站的服务条款
- ⚠️ **地区法律**: 请遵守当地关于网络爬虫的法律法规

## 🔄 更新说明

如需更新到最新版本，可以：

1. 访问 [puppeteer-extra-plugin-stealth](https://github.com/berstend/puppeteer-extra/tree/master/packages/puppeteer-extra-plugin-stealth)
2. 使用该项目的工具重新生成stealth.min.js
3. 替换项目中的文件

---

*本文档说明了stealth.min.js的来源、用途和使用方式。该文件为第三方开源项目生成，遵循MIT许可证。*