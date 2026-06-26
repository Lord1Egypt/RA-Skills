# 使用教程

## 快速开始

### 1. 安装依赖

```bash
pip3 install -r requirements.txt --break-system-packages
```

### 2. 获取 Apify API Key

1. 访问 https://console.apify.com/signup 注册账号
2. 登录后访问 https://console.apify.com/account/integrations
3. 复制 API Key（格式：`apify_api_xxxxx`）

### 3. 配置 API Key

**方式 1：环境变量（推荐）**
```bash
export APIFY_API_KEY="apify_api_xxxxx"
```

**方式 2：修改脚本**
编辑 `amazon_scraper.py`，找到这一行：
```python
APIFY_TOKEN = os.getenv("APIFY_API_KEY", "apify_api_xxxxx")
```
替换为你的 API Key。

### 4. 运行爬虫

```bash
# 基础用法（使用默认关键词）
python3 amazon_scraper.py

# 自定义关键词
python3 amazon_scraper.py -k "women sneakers"

# 多关键词
python3 amazon_scraper.py -k "women shoes" "men boots" "kids sneakers"

# 指定数量
python3 amazon_scraper.py -n 100

# 指定输出目录
python3 amazon_scraper.py -o ./my-output
```

## 参数说明

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| --keyword | -k | 搜索关键词（可多个） | women fashion shoes |
| --number | -n | 最大商品数量 | 50 |
| --output | -o | 输出目录 | ./output |

## 输出文件

运行成功后，会在输出目录生成两个文件：

### 1. Excel 文件（amazon-data-YYYYMMDD_HHMMSS.xlsx）

包含两个 Sheet：

**Sheet 1: 商品数据**
- 排名、商品名称、品牌、类型、ASIN
- 价格（预留，可手动填写）
- 图片链接（可点击）
- Amazon 链接（可点击）

**Sheet 2: 统计摘要**
- 品牌分布统计（数量和占比）

### 2. Markdown 文件（amazon-report-YYYYMMDD_HHMMSS.md）

包含：
- 数据概览
- 爆款商品列表（表格）
- 商品详情链接
- 品牌分布统计

## 输出示例

### Excel 预览

| 排名 | 商品名称 | 品牌 | 类型 | ASIN |
|------|---------|------|------|------|
| 1 | adidas Women's VL Court 3.0 | Adidas | Sneaker | B0C2JY169J |
| 2 | Adokoo Women's Fashion Sneakers | Adokoo | Sneaker | B0CH9FJY8V |

### 品牌统计

| 品牌 | 数量 | 占比 |
|------|------|------|
| Adidas | 7 | 35% |
| ODOLY | 6 | 30% |
| LUCKY STEP | 5 | 25% |

## 常见问题

### Q: 为什么报错 "No module named 'openpyxl'"？

A: 没有安装依赖。运行：
```bash
pip3 install -r requirements.txt --break-system-packages
```

### Q: Apify 启动失败？

A: 检查：
1. API Key 是否正确
2. 网络连接是否正常
3. Apify 账户是否有余额（免费额度 $5）

### Q: 爬取的数据不完整？

A: 可能原因：
1. Amazon 反爬拦截 - 建议降低爬取频率
2. Apify 额度不足 - 检查账户余额
3. 关键词太冷门 - 换个热门关键词试试

### Q: 如何自定义输出格式？

A: 编辑 `amazon_scraper.py`：
- 修改 `generate_excel()` 函数调整 Excel 格式
- 修改 `generate_markdown()` 函数调整 Markdown 格式

## 进阶用法

### 批量爬取多个品类

创建脚本 `batch_scrape.py`：
```python
from amazon_scraper import main

keywords_list = [
    ["women fashion shoes"],
    ["men sneakers"],
    ["kids boots"],
    ["running shoes"]
]

for keywords in keywords_list:
    main(keywords=keywords, max_products=50)
```

### 定时监控

配置 cron 每天执行：
```bash
# 编辑 crontab
crontab -e

# 添加（每天凌晨 3 点执行）
0 3 * * * cd /path/to/amazon-scraper && python3 amazon_scraper.py
```

### 数据可视化

用 Excel 或 Python 分析数据：
```python
import pandas as pd

# 读取 Excel
df = pd.read_excel("amazon-data.xlsx", sheet_name="商品数据")

# 品牌分布
brand_dist = df['品牌'].value_counts()
print(brand_dist)

# 绘制图表
brand_dist.plot(kind='bar')
```

## 成本说明

### Apify 定价

- **免费额度**: $5/月（约 500-1000 个商品）
- **付费套餐**: $49/月起（5000 个商品）

### 优化建议

1. 合理控制爬取数量（50-100 个通常够用）
2. 避免重复爬取相同关键词
3. 使用缓存（后续版本支持）

## 技术支持

- **GitHub Issues**: https://github.com/zuokun300/amazon-scraper/issues
- **作者邮箱**: zuokun300@gmail.com

---

*最后更新：2026-03-03*
