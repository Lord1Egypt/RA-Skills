# Amazon 数据爬虫技能

## 技能描述

爬取 Amazon 商品数据，生成结构化报告（Markdown + Excel）。支持商品搜索、数据提取、品牌分析、爆款识别。

**适用场景：**
- 电商选品调研
- 竞品价格监控
- 爆款商品分析
- 市场趋势研究

---

## 安装方法

### 方法 1：ClawHub 安装（推荐）

```bash
# 访问 ClawHub 页面
https://clawhub.ai/zuokun300/amazon-scraper

# 或使用 CLI 安装
clawhub install zuokun300/amazon-scraper
```

### 方法 2：手动安装

```bash
# 1. 克隆技能到 workspace
git clone https://github.com/zuokun300/amazon-scraper.git ~/.openclaw/workspace/skills/amazon-scraper

# 2. 安装依赖
pip3 install openpyxl requests --break-system-packages

# 3. 配置 Apify API Key
export APIFY_API_KEY="apify_api_xxxxx"
```

---

## 使用方法

### 基础用法

对 OpenClaw 说：

```
帮我爬取 Amazon 上的 "women fashion shoes"，生成 Excel 报告
```

### 高级用法

```
帮我爬取 Amazon 上的 "[关键词]"，需要：
- 抓取前 50 个商品
- 提取价格、评分、评论数
- 生成 Excel 和 Markdown 报告
- 分析品牌分布
```

### 自定义参数

```python
# 修改脚本中的参数
KEYWORDS = ["women fashion shoes", "men sneakers"]
MAX_PRODUCTS = 50
OUTPUT_DIR = "/path/to/output"
```

---

## 输出文件

### 1. Excel 报告 (`amazon-data.xlsx`)

包含两个 Sheet：

**Sheet 1: 商品数据**
| 列名 | 说明 |
|------|------|
| 排名 | 搜索排名 |
| 商品名称 | 完整标题 |
| 品牌 | 自动识别的品牌 |
| 类型 | 商品分类 |
| ASIN | Amazon 标准 ID |
| 价格 | 当前价格（需深度爬取） |
| 图片链接 | 可点击的主图链接 |
| Amazon 链接 | 可点击的商品页链接 |

**Sheet 2: 统计摘要**
- 品牌分布统计
- 价格区间分析
- 爆款识别

### 2. Markdown 报告 (`amazon-report.md`)

包含：
- 数据概览
- 爆款商品列表（表格）
- 商品详情链接

---

## 配置说明

### Apify API Key

**获取方法：**
1. 访问 https://console.apify.com/signup 注册
2. 登录后访问 https://console.apify.com/account/integrations
3. 复制 API Key

**配置方式：**
```bash
# 方式 1：环境变量
export APIFY_API_KEY="apify_api_xxxxx"

# 方式 2：修改脚本
APIFY_TOKEN = "apify_api_xxxxx"
```

**免费额度：** $5（约 500-1000 次商品爬取）

---

## 依赖项

```txt
openpyxl>=3.0.0
requests>=2.28.0
```

---

## 示例输出

### 爆款商品表格

| 排名 | 商品 | 品牌 | 类型 | ASIN |
|------|------|------|------|------|
| 1 | adidas Women's VL Court 3.0 | Adidas | Sneaker | B0C2JY169J |
| 2 | Adokoo Women's Fashion Sneakers | Adokoo | Sneaker | B0CH9FJY8V |
| 3 | Adidas Women's Vl Court 3.0 | Adidas | Sneaker | B0F1XH7M8F |

### 品牌分布统计

| 品牌 | 商品数量 | 占比 |
|------|---------|------|
| Adidas | 7 | 35% |
| ODOLY | 6 | 30% |
| LUCKY STEP | 5 | 25% |

---

## 进阶功能

### 1. 深度爬取（价格/评分/销量）

```bash
# 启用深度爬取模式
python3 amazon_scraper.py --deep
```

**额外数据：**
- 当前价格
- 用户评分（1-5 星）
- 评论总数
- 销量排名（BSR）
- 高清商品图片

### 2. 定时监控

```bash
# 配置 cron 每天执行
0 3 * * * python3 /path/to/amazon_scraper.py
```

**用途：**
- 价格变化监控
- 新品上架提醒
- 竞品动态追踪

### 3. 多关键词批量爬取

```python
KEYWORDS = [
    "women fashion shoes",
    "men sneakers",
    "kids boots",
    "running shoes"
]
```

---

## 注意事项

### 1. API 成本

- Apify 免费额度：$5/月
- 单次爬取成本：约 $0.002/商品
- 建议：合理控制爬取数量

### 2. 反爬措施

- Amazon 反爬严格，建议使用 Apify 等专业服务
- 不要高频爬取同一关键词
- 遵守 Amazon 服务条款

### 3. 数据准确性

- 价格可能实时变化
- 销量为估算值（基于评论数推算）
- 建议定期更新数据

---

## 常见问题

### Q: 为什么有些商品价格显示"待爬取"？

A: 基础模式只抓取搜索页数据，价格需要访问商品详情页。使用 `--deep` 参数启用深度爬取。

### Q: Apify 运行失败怎么办？

A: 检查：
1. API Key 是否正确
2. 网络连接是否正常
3. Apify 账户是否有余额

### Q: 如何自定义输出格式？

A: 修改 `generate_excel()` 和 `generate_report()` 函数，调整列名和样式。

---

## 更新日志

### v1.0.0 (2026-03-03)
- ✅ 基础爬取功能
- ✅ Excel + Markdown 报告生成
- ✅ 品牌分布统计
- ✅ 可点击链接

### TODO
- [ ] 深度爬取（价格/评分/销量）
- [ ] 图片下载功能
- [ ] 多语言支持
- [ ] 定时监控告警

---

## 作者与许可

- **作者:** Elden (@zuokun300)
- **许可:** MIT License
- **问题反馈:** https://github.com/zuokun300/amazon-scraper/issues

---

## 相关技能

- **web-scraping-router** - 爬虫工具路由技能
- **apify-scraper** - Apify 工业级爬虫模板
- **price-monitor** - 价格监控哨兵

---

*最后更新：2026-03-03*
