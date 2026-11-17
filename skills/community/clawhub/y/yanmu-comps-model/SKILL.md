---
name: yanmu-comps-model
description: 股票研究专家研木的Skill — 可比公司估值(Comps)，含PE/PB/ROE/利润率雷达图对比
---

> **运行依赖**：`pip3 install matplotlib numpy`（缺库时脚本会提示安装）

# 研木 · 可比公司估值 (yanmu-comps-model)

## 功能
基于目标公司及可比公司的财务数据，构建完整的可比公司估值分析：
1. **估值倍数对比** — PE/PB/PS/EV/EBITDA 横向对比
2. **盈利能力对比** — ROE/毛利率/净利率 行业排名
3. **雷达图可视化** — 多维度指标雷达图对比
4. **估值结论** — 相对估值溢价/折价判断

## 市场覆盖
支持三大市场，数据来自内置数据库（估值指标为主）：
| 市场 | 支持标的数 |
|------|:---------:|
| 🇨🇳 A股 | 10支（含宁德时代、茅台、比亚迪、光模块等） |
| 🇭🇰 港股 | 1支（腾讯控股） |
| 🇺🇸 美股 | 1支（NVIDIA） |

> 每次运行时自动从新浪财经获取实时股价，覆盖硬编码市值。

## 工作流程

### 1. 运行Comps模型
```bash
python3 {baseDir}/scripts/comps_model.py \
  --ticker <目标公司代码> \
  --comps <可比公司代码1,代码2,...> \
  --market <a-share|hk|us> \
  --output-dir <图表输出目录> \
  --format <text|json>
```

### 2. 实时行情覆盖
脚本内置 `_fetch_live_price()` 函数，自动获取实时股价并更新市值和PE。

### 3. 脚本输出

#### 控制台输出（text格式）
- **可比公司选取**：展示目标公司和对比公司
- **估值倍数对比表**：市值、PE(TTM)、PB、ROE、毛利率、净利率、营收增速
- **估值解读**：PE视角、PB-ROE视角分析
- **综合判断**：优质溢价/折价结论

#### JSON输出（json格式，供报告生成器使用）
```json
{
  "target": {
    "name": "公司名", "market_cap": xxx, "pe_ttm": xx,
    "pb": x.x, "roe": xx, "gross_margin": xx, ...
  },
  "comps": {
    "代码": { "name": "...", "market_cap": xxx, ... }
  }
}
```

#### 图表输出
- **雷达图**: `<ticker>_comps_radar.png` — 多维度对比可视化
- **条形图**: `<ticker>_comps_bar.png` — PE/PB对比

### 4. 分析维度
| 维度 | 指标 |
|------|------|
| 估值 | PE(TTM)、PB、PS、EV/EBITDA |
| 盈利能力 | ROE、毛利率、净利率 |
| 成长性 | 营收增速、净利增速 |
| 财务健康 | 资产负债率、净现金 |

## 注意事项
- 可比公司需从内置数据库中选择，暂不支持外部数据
- A股可比公司覆盖较全（10支），港股/美股仅各1支
