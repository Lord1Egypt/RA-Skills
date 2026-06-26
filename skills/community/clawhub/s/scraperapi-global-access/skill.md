---
name: scraperapi-global-access
description: 全球多国IP访问网站，支持25+国家代理、JS渲染、用户行为模拟、性能监控、断点续传。适用于广告验证、竞品分析、SEO监控、GA测试、CDN效果对比。
version: 1.0.0
author: 家庭助手
tags: [proxy, global, scraping, monitoring, performance]
requires:
  - axios
  - ScraperAPI API Key
allowed-tools: Bash(node:*)
---

# ScraperAPI 全球访问技能

通过 ScraperAPI 实现全球多国 IP 访问网站，支持 JS 渲染、用户行为模拟、性能监控。

## 功能特性

- ✅ **25+ 国家代理** - 覆盖北美、南美、欧洲、亚洲、大洋洲、非洲
- ✅ **JS 渲染** - 触发 Google Analytics、Facebook Pixel 等统计代码
- ✅ **用户行为模拟** - 模拟真实用户浏览路径（首页→工具页→价格页）
- ✅ **性能监控** - 记录响应时间，分析全球访问速度
- ✅ **断点续传** - 任务中断后可继续，不丢失进度
- ✅ **数据导出** - 自动生成 JSON 报告、CSV 数据、性能分析

## 使用场景

| 场景 | 说明 |
|------|------|
| **广告验证** | 验证广告在不同地区的投放效果 |
| **竞品分析** | 监控竞品网站在全球的可用性和性能 |
| **SEO 监控** | 检查网站在不同地区的 SEO 表现 |
| **GA 测试** | 验证 Google Analytics 是否正确触发 |
| **CDN 对比** | 对比不同 CDN 在全球的性能 |
| **可用性监控** | 定期检查网站在全球的可访问性 |

## 前置要求

### 1. 安装依赖

```bash
npm install axios
```

### 2. 获取 ScraperAPI Key

访问 [ScraperAPI Dashboard](https://dashboard.scraperapi.com/) 获取 API Key。

### 3. 配置环境变量

在工作目录创建 `.env` 文件：

```env
SCRAPER_API_KEY=your_api_key_here
```

## 快速开始

### 基础用法：单国访问

```bash
node scripts/single_visit.js --url https://example.com --country us
```

### 全球覆盖：25国测试

```bash
node scripts/global_coverage.js --url https://example.com
```

### 用户行为模拟

```bash
node scripts/user_journey.js --url https://example.com --countries us,uk,jp
```

### 性能监控

```bash
node scripts/performance_monitor.js --url https://example.com --interval 3600
```

## 脚本说明

### 1. `single_visit.js` - 单次访问

访问指定 URL，使用指定国家的代理。

**参数**：
- `--url` - 目标网址（必填）
- `--country` - 国家代码（默认：us）
- `--render` - 是否渲染 JS（默认：true）
- `--output` - 输出文件路径（可选）

**示例**：
```bash
node scripts/single_visit.js --url https://faceswap.cool --country jp --render true
```

### 2. `global_coverage.js` - 全球覆盖

使用 25 个国家的 IP 访问目标网站。

**参数**：
- `--url` - 目标网址（必填）
- `--render` - 是否渲染 JS（默认：true）
- `--interval` - 访问间隔（秒，默认：5）
- `--output-dir` - 输出目录（默认：./reports）

**示例**：
```bash
node scripts/global_coverage.js --url https://example.com --interval 3
```

**输出文件**：
- `global_report.json` - 完整 JSON 报告
- `global_results.csv` - 访问记录 CSV
- `performance_data.csv` - 性能数据 CSV

### 3. `user_journey.js` - 用户旅程模拟

模拟真实用户浏览多个页面。

**参数**：
- `--url` - 网站根 URL（必填）
- `--pages` - 页面路径列表（逗号分隔，默认：/,/pricing,/about）
- `--countries` - 国家代码列表（逗号分隔，默认：us,uk,jp）
- `--wait-min` - 最小停留时间（秒，默认：3）
- `--wait-max` - 最大停留时间（秒，默认：6）

**示例**：
```bash
node scripts/user_journey.js \
  --url https://example.com \
  --pages /,/tools/face-swap,/pricing \
  --countries us,uk,de,jp \
  --wait-min 3 \
  --wait-max 8
```

### 4. `performance_monitor.js` - 性能监控

定期访问网站，记录性能数据。

**参数**：
- `--url` - 目标网址（必填）
- `--interval` - 监控间隔（秒，默认：3600）
- `--countries` - 监控的国家（逗号分隔，默认：us,uk,de,jp,sg）
- `--duration` - 运行时长（秒，0=无限，默认：0）

**示例**：
```bash
# 每小时监控一次，持续 24 小时
node scripts/performance_monitor.js \
  --url https://example.com \
  --interval 3600 \
  --duration 86400
```

## 支持的国家代码

| 地区 | 国家代码 |
|------|---------|
| **北美** | us, ca, mx |
| **南美** | br, ar, cl |
| **欧洲** | gb, de, fr, it, es, nl, se, pl |
| **亚洲** | jp, kr, sg, in, id, th |
| **大洋洲** | au, nz |
| **非洲** | za, eg, ng |

完整列表见 [ScraperAPI 文档](https://www.scraperapi.com/documentation/)。

## 配置选项

### 全局配置文件

创建 `config.json`：

```json
{
  "scraperapi": {
    "apiKey": "your_api_key",
    "defaultRender": true,
    "timeout": 90000,
    "retries": 3
  },
  "monitoring": {
    "interval": 3600,
    "countries": ["us", "uk", "de", "jp", "sg"],
    "alertThreshold": 30000
  },
  "output": {
    "format": "json",
    "directory": "./reports",
    "keepHistory": true
  }
}
```

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `SCRAPER_API_KEY` | ScraperAPI 密钥 | 必填 |
| `SCRAPER_TIMEOUT` | 请求超时（毫秒） | 90000 |
| `SCRAPER_RENDER` | 默认是否渲染 JS | true |
| `OUTPUT_DIR` | 输出目录 | ./reports |

## 断点续传

所有脚本支持断点续传，中断后重新运行会自动继续：

```bash
# 第一次运行（中断）
node scripts/global_coverage.js --url https://example.com

# 重新运行（自动跳过已完成的国家）
node scripts/global_coverage.js --url https://example.com
```

进度保存在 `progress.json`，可手动删除以重新开始。

## 数据格式

### JSON 报告格式

```json
{
  "generatedAt": "2026-03-20T05:00:00.000Z",
  "summary": {
    "totalVisits": 37,
    "successfulVisits": 35,
    "failedVisits": 2,
    "successRate": "94.6%"
  },
  "globalCoverage": {
    "countries": 25,
    "regions": 6
  },
  "results": [
    {
      "success": true,
      "country": "美国",
      "countryCode": "us",
      "region": "北美",
      "page": "/",
      "title": "Example Site",
      "status": 200,
      "size": 188759,
      "responseTime": 38629,
      "timestamp": "2026-03-20T04:49:11.106Z"
    }
  ],
  "performanceData": [...]
}
```

### CSV 格式

```csv
Country,Region,Page,Status,ResponseTime,Title,Timestamp
美国,北美,/,Success,38629,"Example Site",2026-03-20T04:49:11.106Z
```

## 最佳实践

### 1. 避免触发反爬

```javascript
// ✅ 推荐：随机间隔
const waitTime = Math.random() * 3000 + 3000; // 3-6秒

// ❌ 不推荐：固定间隔
const waitTime = 2000; // 太规律
```

### 2. 合理使用 JS 渲染

```javascript
// ✅ 需要触发 GA 时开启
render: true

// ✅ 只抓取 HTML 时关闭（更快）
render: false
```

### 3. 错误处理

```javascript
try {
  const result = await visitPage(country, url);
  saveProgress(result);
} catch (error) {
  console.error('访问失败:', error.message);
  // 继续下一个，不中断整个任务
}
```

### 4. 性能优化

- 使用 `session_number` 参数复用会话
- 批量任务使用断点续传
- 定期清理旧的进度文件

## 故障排查

### 问题：API 返回 429 错误

**原因**：请求过快，超出配额。

**解决**：
1. 增加 `--interval` 参数
2. 检查 ScraperAPI 配额
3. 升级 ScraperAPI 套餐

### 问题：某些国家返回 500 错误

**原因**：目标网站在该地区不可用，或 ScraperAPI 代理问题。

**解决**：
1. 检查目标网站是否有地区限制
2. 重试几次（脚本会自动记录失败）
3. 联系 ScraperAPI 支持

### 问题：JS 渲染后仍看不到 GA 数据

**原因**：
1. GA 开启了 Bot Filtering
2. 需要用户同意 Cookie
3. GA 实时报告延迟

**解决**：
1. 检查 GA 设置中的 Bot Filtering
2. 增加页面停留时间
3. 等待 5-10 分钟查看实时报告

## 进阶用法

### 自定义国家列表

编辑 `scripts/countries.json`：

```json
{
  "custom": [
    { "country": "美国", "code": "us", "region": "北美" },
    { "country": "中国", "code": "cn", "region": "亚洲" }
  ]
}
```

### 集成到 OpenClaw Cron

```javascript
// 每天早上 9 点运行
{
  "name": "全球访问监控",
  "schedule": {
    "kind": "cron",
    "expr": "0 9 * * *",
    "tz": "Asia/Shanghai"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "运行 scraperapi-global-access skill，监控 https://example.com"
  },
  "sessionTarget": "isolated"
}
```

### 数据可视化

使用生成的 CSV 文件：

```bash
# 导入到 Excel/Google Sheets
# 或使用 Python 生成图表
python scripts/visualize.py performance_data.csv
```

## API 参考

### visitPage(country, url, options)

访问单个页面。

**参数**：
- `country` - 国家对象 `{ country, code, region }`
- `url` - 目标 URL
- `options` - 配置选项
  - `render` - 是否渲染 JS（默认：true）
  - `timeout` - 超时时间（默认：90000）
  - `sessionNumber` - 会话编号（可选）

**返回**：
```javascript
{
  success: true,
  country: "美国",
  countryCode: "us",
  region: "北美",
  page: "/",
  title: "Example",
  status: 200,
  size: 188759,
  responseTime: 38629,
  timestamp: "2026-03-20T04:49:11.106Z"
}
```

## 许可证

MIT License

## 更新日志

### v1.0.0 (2026-03-20)

- ✨ 初始版本
- ✅ 支持 25+ 国家代理
- ✅ JS 渲染支持
- ✅ 用户行为模拟
- ✅ 性能监控
- ✅ 断点续传
- ✅ 数据导出（JSON/CSV）

## 贡献

欢迎提交 Issue 和 Pull Request！

## 支持

- 📧 Email: support@example.com
- 💬 Discord: [OpenClaw Community](https://discord.com/invite/clawd)
- 📚 文档: [ClawHub](https://clawhub.com)
