# Shit Journal Scraper

自动化抓取并分析学术刊物 [shitjournal.org](https://shitjournal.org) 的研究论文，利用 AI 进行深度拆解。

## 功能特性

- **SPA 自动渲染**：内置 Playwright 无头浏览器环境，完美模拟真实访问，绕过前后端分离应用的 CSR 动态渲染限制。
- **深度数据提取**：精确解析文章标题、摘要内容、DOI 标识符及发布时间。
- **智能 AI 拆解**：自动调用 LLM 对提取的摘要进行核心观点提炼与深度拆解。
- **自动化输出**：支持将分析结果直接输出为 JSON 格式，方便集成到知识管理系统或工作流中。
- **环境自适应**：自动管理浏览器驱动依赖，零配置上手。

## 技术栈与依赖

- **Runtime**: Node.js
- **渲染引擎**: Playwright (Chromium)
- **解析引擎**: JSDOM
- **开发与构建**: Git, NPM

## 安装与配置

### 1. 安装依赖
```bash
npm install playwright jsdom
npx playwright install chromium
```

### 2. 本地运行
```bash
# 执行抓取任务
node index.js
```

## 代码实现逻辑

本 Skill 通过 `index.js` 实现核心逻辑：
1. **浏览器启动**：使用 `playwright` 启动 Chromium 无头模式。
2. **DOM 抓取**：通过 `goto` 访问目标网站，等待 JS 渲染后获取完整 HTML。
3. **数据解析**：使用 `jsdom` 构建 DOM 树，根据 `a[href^="/preprints"]` 选择器精准提取文章节点信息。
4. **异常处理**：内置完善的错误捕获机制，确保抓取失败时返回标准化错误 JSON。

```javascript
// index.js 核心片段：解析器示例
async function extractArticles(html) {
    const dom = new JSDOM(html);
    const document = dom.window.document;
    return Array.from(document.querySelectorAll('a[href^="/preprints"]')).map(el => ({
        title: el.querySelector('h4')?.textContent.trim(),
        abstract: el.querySelector('p')?.textContent.trim(),
        doi: el.querySelector('span:last-child')?.textContent.trim()
    })).filter(art => art.title && art.abstract);
}
```

## 贡献与开源
- 仓库地址: [https://github.com/Excalibur9527/shit-journal-scraper](https://github.com/Excalibur9527/shit-journal-scraper)
- 许可协议: MIT

---
*Created by OpenClaw Assistant for Excalibur9527.*
