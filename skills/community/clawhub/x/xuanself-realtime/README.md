# 俄罗斯血糖检测设备市场调研（即时版）

> **xuanself-realtime v3.0** | 2026-04-09 实战验证版

整合 SerpAPI 实时搜索 + Python 脚本化报告生成 + ast.literal_eval 智能解析 + Xuanself 10章节标准结构，输出可直接交付的 Word 报告。专为 Russia Country Manager 设计，彻底规避 Error 10004（Token 溢出）问题。

---

## 快速开始（3步完成报告）

### 第一步：配置 SerpAPI Key

编辑 `data/data_sources.json`，将 `YOUR_SERPAPI_KEY` 替换为你的实际 Key：

```json
{
  "serpapi": {
    "key": "你的SerpAPI密钥",
    "note": "serpapi.com 注册获取"
  }
}
```

> **没有 SerpAPI Key？** 访问 [serpapi.com](https://serpapi.com) 注册，免费套餐每月 100 次搜索。

### 第二步：安装 Python 依赖

```bash
cd ~/.workbuddy/skills/xuanself-realtime
pip install requests beautifulsoup4 lxml python-docx
```

或者直接：

```bash
pip install -r requirements.txt
```

### 第三步：运行报告生成

```bash
# 使用默认数据（demo 模式，直接出报告）
python scripts/run_report.py --input data/demo.json --output output/report.md

# 使用自有 SerpAPI 数据
python scripts/run_report.py --input your_raw_data.json --output output/glucose_2026.md
```

脚本会自动调用 `word_exporter.py` 生成 Word 文档，输出到同一目录（`.docx`）。

---

## 目录结构

```
xuanself-realtime/
├── SKILL.md              ← 完整技能说明（必读）
├── README.md             ← 本快速启动指南
├── skill.json            ← Clawhub 标准配置
├── MANIFEST.json         ← 发布清单
├── requirements.txt      ← Python 依赖
├── scripts/
│   ├── data_parser.py    ← 数据解析核心（ast.literal_eval 兜底）
│   ├── report_generator.py  ← 10章节 Markdown 报告生成器
│   ├── run_report.py     ← CLI 快捷入口
│   └── word_exporter.py ← Word 导出器 v2（专业排版）
├── data/
│   └── data_sources.json ← SerpAPI Key + 数据源索引
└── output/              ← 报告输出目录
```

---

## 触发词（对 AI 说这些即可激活）

- `生成俄罗斯血糖检测设备市场报告`
- `俄罗斯血糖仪市场调研即时版`
- `俄罗斯血糖检测实时报告`
- `生成俄罗斯血糖设备调研报告`
- `俄罗斯血糖仪实战报告`
- `俄罗斯医疗器械实时调研`

---

## 报告输出示例

运行后生成两个文件：

| 文件 | 说明 |
|:---|:---|
| `output/report.md` | Markdown 源文件（约 16KB） |
| `output/report.docx` | Word 专业排版文档（约 48KB） |

报告包含 Xuanself 标准 10 章节：

```
一、执行摘要
二、市场容量与规模
三、竞争格局分析
四、渠道与价格分析
五、患者群体数据（★必填）
六、医学研究进展（★必填）
七、政府机构动态与政策（★必填）
八、电商平台深度分析
九、招标与采购数据
十、市场进入建议
```

---

## 核心数据源

| 维度 | 数据来源 | 语言 |
|:---|:---|:---:|
| 患者统计 | IDF Diabetes Atlas (diabetesatlas.org) | EN |
| 市场规模 | IMEDA、公开财报、SerpAPI | RU/EN |
| 竞品价格 | SerpAPI (Yandex+Google)、Яндекс.Маркет | RU |
| 电商价格 | Яндекс.Маркет、Wildberries、Ozon | RU |
| 行业新闻 | Vademecum.ru、РБК、Коммерсантъ | RU |
| 政府政策 | Минздрав、ФФОМС、ГИСП | RU |
| 社媒情报 | VKontakte、Telegram（SerpAPI） | RU |
| 招标数据 | ЕИС zakupki.gov.ru | RU |

---

## 常见问题

### Q: 报错 "SERPAPI_KEY not found"
**A:** 编辑 `data/data_sources.json`，填入你的 SerpAPI Key。

### Q: 报错 "No module named 'docx'"
**A:** 运行 `pip install python-docx`。

### Q: 报告数据是旧的/不准确
**A:** 使用你自己的 SerpAPI 采集的最新数据替换 `data/demo.json`，重新运行 `run_report.py`。

### Q: BOM SyntaxError
**A:** 已内置自动 BOM 清理机制，`run_report.py` 会自动处理，无需手动操作。

---

## 技术要点（来自 2026-04-09 实战经验）

### 1. 规避 Error 10004（Token 溢出）
报告生成全部通过 Python 脚本执行，不通过 AI 直接输出。AI 只负责写脚本、执行脚本、读取结果。

### 2. ast.literal_eval 兜底解析
SerpAPI 采集的 JSON 中部分字段是 Python repr 格式（单引号），`json.loads()` 会失败。`data_parser.py` 智能处理：

```python
def smart_json(s):
    try: return json.loads(s)      # 标准 JSON
    except: pass
    try: return ast.literal_eval(s)  # Python repr 兜底
    except: return None
```

### 3. Word 排版特点
- ✅ 封面元信息表格（`**key**：value` 格式）
- ✅ 内联格式保留（**加粗**、*斜体*、`等宽`、超链接）
- ✅ 表格斑马纹 + 深蓝表头
- ✅ 章节自动分页
- ✅ 页眉（标题+日期）+ 页脚（机密声明）

---

xuanself-realtime v3.0 — 2026年4月9日实战验证版
