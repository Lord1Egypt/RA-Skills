# Amazon 数据爬虫技能

🛒 爬取 Amazon 商品数据，生成结构化报告（Markdown + Excel）

## 快速开始

### 1. 获取 Apify API Key

访问 https://console.apify.com/account/integrations 获取

### 2. 安装依赖

```bash
pip3 install -r requirements.txt --break-system-packages
```

### 3. 运行爬虫

```bash
# 修改脚本中的关键词
# 然后运行：
python3 amazon_scraper.py
```

## 输出示例

- `amazon-data.xlsx` - Excel 数据表
- `amazon-report.md` - Markdown 报告

## 文档

完整文档见 [SKILL.md](./SKILL.md)

---

**作者:** Elden (@zuokun300)  
**许可:** MIT
