# Xuanself — 配置与移植说明

本文档说明如何在全新环境中配置 Xuanself 技能。

---

## 1. Python 依赖安装

```bash
# 核心依赖
pip install python-docx fake-useragent beautifulsoup4 lxml requests matplotlib pillow

# 可选：用于图表生成
pip install matplotlib pillow
```

---

## 2. API Key 配置

### SerpAPI（必需）

1. 访问 https://serpapi.com 注册并获取 API Key
2. 编辑 `data/data_sources.json`，找到 `serpapi.key` 字段，填入您的 Key：

```json
{
  "api_keys": {
    "serpapi": {
      "key": "YOUR_SERPAPI_KEY_HERE",
      "service": "SerpAPI (serpapi.com)",
      "used_for": "Yandex/Google 多语种搜索",
      "cost": "免费套餐100次/月；付费$75/月无限制"
    }
  }
}
```

### TGStat（可选，Telegram分析用）

```json
{
  "api_keys": {
    "tgstat": {
      "key": "YOUR_TGSTAT_TOKEN_HERE",
      "service": "TGStat (tgstat.ru)",
      "used_for": "Telegram频道/社群统计分析"
    }
  }
}
```

---

## 3. 目录结构

```
~/.workbuddy/skills/xuanself/   ← 技能根目录
├── SKILL.md                    技能主规范（AI阅读）
├── README.md                   用户快速指南
├── PORTING_NOTES.md            本文件
├── LICENSE                    MIT许可证
├── MANIFEST.json              发布文件清单
├── scripts/
│   ├── word_exporter.py        Word导出器 v2
│   └── run_report.py          快捷导出脚本
└── data/
    └── data_sources.json      数据源索引（需填入API Key）
```

---

## 4. 输出目录

默认输出目录为 `~/.workbuddy/skills/report-gama/output/`（与 report-gama 共享）。

如需独立输出目录，可修改 `scripts/word_exporter.py` 中的 `OUTPUT_DIR`：

```python
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
```

---

## 5. 与 report-gama 的关系

Xuanself 基于 report-gama 构建，共享以下资源：
- `report-gama/scripts/multi_lang_search.py` — 多语言搜索封装
- `report-gama/scripts/master.py` — 调研主控
- `report-gama/scripts/word_exporter.py` — Word导出器

如果未安装 report-gama，`scripts/word_exporter.py` 可独立运行（内置默认配置）。

---

## 6. 数据来源一览

| 数据类型 | 来源 | URL |
|:---|:---|:---|
| 患者统计 | IDF Diabetes Atlas | diabetesatlas.org |
| 患者统计 | 俄罗斯卫生部 | minzdrav.gov.ru |
| 患者统计 | НМИЦ内分泌中心 | endocrincentr.ru |
| 行业新闻 | Коммерсантъ | kommersant.ru |
| 政府动态 | kremlin.ru | kremlin.ru |
| 招标数据 | ЕИС | zakupki.gov.ru |
| 电商价格 | Wildberries | wildberries.ru |
| 电商价格 | Ozon | ozon.ru |

---

## 7. 常见问题

**Q：SerpAPI 免费套餐够用吗？**
A：100次/月对于单次报告生成足够。如需频繁使用，建议升级付费套餐。

**Q：可以不填 API Key 吗？**
A：可以，但搜索质量会下降（使用随机UA），部分功能受限。

**Q：数据源需要代理吗？**
A：俄罗斯网站（minzdrav.gov.ru、zakupki.gov.ru等）在中国可能需要VPN访问。
