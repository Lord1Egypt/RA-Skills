---
name: yanmu-report-generator
description: 股票研究专家研木的Skill — 将DCF和Comps分析结果生成专业券商研报（PDF或Word）
---

# 研木 · 报告生成器 (yanmu-report-generator)

## 功能
将金融数据采集 + DCF估值分析 + 可比公司估值分析结果，整合为专业排版的券商研究报告。

## 核心架构

### 多源数据输入
报告生成器需要**三个数据源同时输入**才能生成完整报告：
```
┌─────────────────┐    ┌────────────────┐    ┌──────────────────┐
│ financial-data  │    │   dcf-model    │    │   comps-model    │
│ (含历史业绩 +   │    │ (DCF估值 +     │    │ (可比公司估值 +   │
│  分析师预期)    │    │  敏感性分析)   │    │  雷达图/条形图)  │
└────────┬────────┘    └───────┬────────┘    └────────┬─────────┘
         │                     │                      │
         └──────────┬──────────┴──────────┬───────────┘
                    │                     │
                    ▼                     ▼
            ┌───────────────────────────────────┐
            │      generate_report.py            │
            │  - COMPANY_PROFILES (12支股票)      │
            │  - 动态模板（无硬编码）               │
            │  - 评级自动判断                      │
            └───────────────────────────────────┘
                     │
                     ▼
            ┌───────────────────┐
            │ 📄 PDF /  Word    │
            │ 专业券商研报       │
            └───────────────────┘
```

### COMPANY_PROFILES 系统
内置12支股票的公司档案，覆盖：
- `tagline` — 一句话定位（如"中国互联网科技超级平台"）
- `industry` — 所属行业
- `industry_median` — 行业中位数参考
- `business_segments` — 业务构成（板块、营收、占比、说明）
- `regional_revenue` — 地区构成
- `risk_factors` — 核心风险因素
- `net_cash` / `shares_outstanding` — 财务参数
- `consensus_target` / `consensus_eps_2026e` / `consensus_growth_2026e` — 分析师预期

### 评级自动判断
| 条件 | 评级 |
|:----|:----:|
| DCF目标价 > 当前价 | **买入 (BUY)** |
| DCF目标价 ≥ 当前价×0.8（20%以内） | **持有 (HOLD)** |
| DCF目标价 < 当前价×0.8（低于20%以上） | **减持 (SELL)** |

## 工作流程

### 1. 运行报告生成脚本
```bash
python3 {baseDir}/scripts/generate_report.py \
  --ticker <股票代码> \
  --company <公司名称> \
  --format pdf|docx \
  --dcf-data <dcf_output.json> \
  --comps-data <comps_output.json> \
  --financial-data <financial_data.json> \
  --chart-dir <图表目录> \
  --output <输出路径>
```

### 2. 参数说明
| 参数 | 必填 | 来源 | 说明 |
|------|:----:|------|------|
| `--ticker` | ✅ | 用户 | 股票代码 |
| `--format` | ✅ | 用户 | pdf / docx |
| `--dcf-data` | ✅ | dcf-model | DCF估值JSON |
| `--comps-data` | ✅ | comps-model | 可比公司估值JSON |
| `--financial-data` | ✅ | financial-data | 金融数据JSON（历史业绩+分析师预期） |
| `--chart-dir` | | 用户 | 图表目录（热力图/雷达图/条形图） |
| `--output` | | 用户 | 报告输出路径 |
| `--target-price` | ❌ | dcf-data | DCF目标价（自动获取） |
| `--current-price` | ❌ | dcf-data | 当前价（自动获取） |
| `--rating` | ❌ | 自动 | 不传则自动判断（买入/持有/减持） |

### 3. 报告结构
报告的每一章节都**动态生成**，不留硬编码：

| 章节 | 内容来源 |
|------|---------|
| **封面** | tagline(动态)、ticker、评级、目标价、涨幅 |
| **核心观点** | 自动判断的评级 + 涨幅 + 公司名 |
| **关键指标** | comps_data(动态提取PE/ROE/市值/毛利率) |
| **公司概况** | tagline + industry(动态) |
| **主营业务** | COMPANY_PROFILES.business_segments |
| **历史业绩** | financial_data.history（2023-2025年） |
| **DCF估值** | dcf-output（含假设、预测表、估值汇总、敏感性矩阵） |
| **可比公司** | comps-output（倍数对比、雷达图、行业排名） |
| **投资建议** | 自动评级的评级结论 |
| **风险提示** | COMPANY_PROFILES.risk_factors |

### 4. 输出路径
文件名格式：`<股票代码>_研究报告_<日期>.pdf|docx`

## 数据依赖关系
```
financial-data  → 历史业绩 + 分析师预期 + 实时股价
      ↓
dcf-model      →  FCF预测 + 敏感性分析 + 隐含股价
      ↓
comps-model    →  估值倍数对比 + 雷达图
      ↓
generate_report →  PDF/Word 研报
```

## 注意事项
- 三个JSON文件必须全部提供，否则对应章节会显示空白
- PDF中文渲染自动探测字体：优先内置字体，否则自动使用系统字体（macOS苹方/黑体、Windows微软雅黑/黑体、Linux Noto/文泉驿），无需手动配置
- 运行依赖：`pip3 install fpdf2 python-docx`（缺库时脚本会提示）
- 评级默认自动判断，也可通过 `--rating` 手动指定
