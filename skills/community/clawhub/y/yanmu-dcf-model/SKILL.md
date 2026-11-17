---
name: yanmu-dcf-model
description: 股票研究专家研木的Skill — DCF估值建模，含5年FCF预测、终值折现、敏感性分析热力图
---

> **运行依赖**：`pip3 install matplotlib numpy`（缺库时脚本会提示安装）

# 研木 · DCF估值建模 (yanmu-dcf-model)

## 功能
基于采集的财务数据，构建完整的DCF估值模型：
1. **5年详细FCF预测（2026-2030）** — 营收、NOPAT、Capex、NWC变化、FCF
2. **终值折现** — Gordon永续增长模型 (g=2.5%)
3. **敏感性分析矩阵** — WACC (7.5%-10.5%) × 永续增长率 (1.5%-3.5%) 交叉表，含热力图

## 市场覆盖
同金融数据采集，支持A股/港股/美股的实时行情覆盖：
- 每次运行时自动从新浪财经API获取最新股价
- 覆盖内置硬编码的静态价格
- 获取成功后联动更新市值和PE(TTM)

## 工作流程

### 1. 运行DCF模型
```bash
python3 {baseDir}/scripts/dcf_model.py \
  --ticker <股票代码> \
  --market <a-share|hk|us> \
  --wacc <WACC值，默认自动计算> \
  --growth <永续增长率，默认2.5%> \
  --output-dir <图表输出目录> \
  --format <text|json>
```

### 2. 实时行情覆盖
脚本内置 `_fetch_live_price()` 函数，与金融数据采集共用同一套行情接口。

### 3. 模型输出

#### 控制台输出（text格式）
- **核心结论卡片**：DCF隐含价格 vs 当前价格 + 隐含上涨空间
- **DCF模型假设**：WACC计算明细（Rf、Beta、MRP、Ke、Kd）
- **5年FCF预测表**：营收、增速、NOPAT、Capex、NWC变动、FCF、FCF利润率
- **DCF估值汇总**：各年FCF现值 + 终值现值 + 企业价值 + 股权价值
- **敏感性分析矩阵**：WACC × 永续增长率交叉表

#### JSON输出（json格式，供报告生成器使用）
```json
{
  "company": "公司名",
  "ticker": "代码",
  "wacc": 7.93,
  "terminal_growth": 0.025,
  "projections": [
    {"year": "2026E", "revenue": 7956, "revenue_growth": 10.5, "nopat": 1750, "fcf": 1275, ...}
  ],
  "dcf_result": {
    "total_pv_fcfs": 6344,
    "pv_terminal": 25116,
    "enterprise_value": 31460,
    "terminal_value_pct": 79.8,
    "implied_price": 356.33
  }
}
```

#### 图表输出
- **敏感性热力图**: `<ticker>_sensitivity_heatmap.png`

### 4. 模型假设
| 参数 | 说明 |
|------|------|
| 无风险利率 (Rf) | 2.50%（10年期中国国债） |
| Beta | 行业特征系数（从内置数据库获取） |
| 市场风险溢价 (MRP) | 6.00%（中国市场标准假设） |
| WACC | CAPM模型自动计算 |
| 预测期 | 5年 (2026-2030) |
| 永续增长率 (g) | 2.5%（可调） |
| 营收增速 | 基于分析师一致预期和历史增速 |
| FCF利润率 | 基于历史趋势逐步调整 |

## 注意事项
- 港股和美股的数据来自课程内置数据库，部分假设参数可能不完全准确
- 敏感性分析矩阵覆盖 WACC 7.5%-10.5%、g 1.5%-3.5% 区间
