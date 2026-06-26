---
name: smart-web-scraper
description: 智能网页数据采集器。自动识别网页结构，批量抓取列表/表格/详情页数据，支持导出JSON/CSV/Excel。内置反爬策略适配。
---

# Smart Web Scraper - 智能网页数据采集器

## 功能特点

### 🔍 智能识别
- 自动识别列表页、详情页、表格数据
- 智能提取标题、价格、作者等关键字段
- 支持分页自动采集

### 🛡️ 反爬应对
- 随机User-Agent轮换
- 请求延迟随机化
- IP代理池支持（可选）
- 自动重试机制

### 📊 数据导出
- JSON批量导出
- CSV/Excel表格
- 数据库直存（MySQL/MongoDB）

## 安装

```bash
cd smart-web-scraper
npm install
```

## 使用方法

### 命令行采集
```bash
# 采集单页
node scraper.js --url "https://example.com/products" --selector ".product-item"

# 批量分页采集
node scraper.js --url "https://example.com/list" --pages 10 --output data.json

# 导出CSV
node scraper.js --url "https://example.com/products" --format csv --output products.csv
```

### 配置采集（config.json）
```json
{
  "target": {
    "url": "https://example.com/items",
    "pages": 5,
    "waitFor": ".loading"
  },
  "fields": [
    {"name": "title", "selector": ".title", "type": "text"},
    {"name": "price", "selector": ".price", "type": "text"},
    {"name": "image", "selector": "img", "type": "attr", "attr": "src"}
  ],
  "export": {
    "format": "json",
    "file": "output.json"
  }
}
```

## 示例场景

| 场景 | 命令 |
|------|------|
| 电商商品采集 | `node scraper.js --url "https://shop.example.com" --selector ".product"` |
| 房价数据 | `node scraper.js --config housing-config.json` |
| 职位列表 | `node scraper.js --url "https://jobs.example.com" --pages 20 --delay 2000` |

## 注意事项

- 遵守网站robots.txt规则
- 合理设置采集间隔
- 商业使用请确认授权