---
name: yunlv-price-monitor
description: >-
  Use when user needs to monitor competitor pricing, track market price trends, or analyze price changes.
  Use when setting up price alerts for specific products or markets.
  Use when preparing pricing strategy reports for B2B export businesses.
  Use when user mentions "竞品价格", "价格监控", "价格趋势", "定价策略", "市场价格", "价格分析", "price monitoring", "competitive pricing".
homepage: https://yunlvai.com
license: MIT-0
version: 1.0.0
progressive:
  layers:
    - name: metadata
      tokens: 200
      loaded: startup
      description: "技能基础配置、数据源说明、定价信息"
    - name: instructions
      tokens: 3500
      loaded: trigger
      description: "价格监控全流程、趋势分析、预警配置、策略建议"
    - name: resources
      tokens: variable
      loaded: on-demand
      description: "竞品列表模板、价格分析报告模板、定价策略指南"
  resource_paths:
    - references/competitor_list_template.md
    - references/price_analysis_report.md
    - references/pricing_strategy_guide.md
metadata:
  yunlv:
    homepage: https://yunlvai.com
    primaryEnv: TRADEGPT_API_KEY
    category: data-analysis
    subCategory: price-intelligence
    tags: ["竞品价格", "价格监控", "市场定价", "价格趋势", "定价策略", "B2B定价", "市场情报"]
    requires:
      env:
        - TRADEGPT_API_KEY
      bins:
        - python3
    apis:
      - name: 云旅AI TradeGPT API
        url: https://api.yunlvai.com
        purpose: "价格数据分析和策略建议生成"
        auth: Bearer Token (TRADEGPT_API_KEY)
      - name: 海关价格数据
        url: https://data.yunlvai.com
        purpose: "进出口交易价格记录"
        auth: Bearer Token
    emoji: "📊"
    author: "云旅AI团队"
    pricing:
      free:
        features: ["每周手动查询5次", "基础价格数据", "单产品分析"]
      basic:
        price: 299
        currency: CNY
        period: month
        features: ["每日自动监控", "10个竞品追踪", "价格趋势图", "邮件预警"]
      pro:
        price: 899
        currency: CNY
        period: month
        features: ["实时监控", "无限竞品追踪", "深度分析报告", "WhatsApp预警", "定价建议"]
triggers:
  - "竞品价格"
  - "价格监控"
  - "价格趋势"
  - "定价策略"
  - "市场价格"
  - "价格分析"
  - "price monitoring"
  - "competitive pricing"
  - "price intelligence"
---

# 竞品价格监控：市场定价情报与智能预警

> 在B2B外贸战场上，价格是决定订单归属的核心武器。云旅AI竞品价格监控技能，帮助外贸企业实时追踪目标市场价格动态，自动识别价格变化趋势，智能预警价格异动，让企业永远比竞争对手快一步做出定价决策。

---

## 一、技能定位

**解决什么问题**：竞争对手价格变化了，我该怎么调整？市场价格趋势如何，我该什么时候报价？

**核心价值**：从"被动跟随竞品调价"升级为"主动预判市场走向"，定价决策周期从**周级**压缩到**小时级**。

---

## 二、能做什么

### 【核心功能】

| 功能 | 说明 |
|------|------|
| 竞品价格追踪 | 持续监控10-50个竞品在多个平台的价格变化 |
| 历史价格趋势 | 可视化展示近6-24个月的价格走势 |
| 价格异动预警 | 竞品价格大幅波动时自动预警（邮件/WhatsApp） |
| 市场份额分析 | 基于价格数据估算各品牌市场份额变化 |
| 定价策略建议 | 基于市场数据给出动态定价建议（进攻型/防守型） |
| 交叉对比分析 | 我方产品 vs 竞品价格矩阵分析 |
| 季节性规律 | 识别产品价格的季节性波动规律 |
| 成本-价格联动 | 分析原材料成本变化对终端价格的影响 |

### 【数据来源】

- 海关进出口价格数据（真实交易价格）
- B2B平台公开报价（Alibaba/MIC/IndiaMART等）
- 行业报告和政府统计数据
- 竞品官网公开价格信息

---

## 三、操作步骤

### 第1步：配置监控任务

**方式A - 竞品价格追踪**
```
监控对象：
- 竞品1：Philips LED Lighting（Alibaba店铺）
- 竞品2：Osram LED（MIC店铺）
- 竞品3：Cree Lighting（官网）
- 我方产品：LED Panel 60x60 40W

监控维度：
- 价格（FOB/CIF）
- 最小起订量（MOQ）
- 付款条款
- 促销信息

监控频率：每日
预警条件：价格变动超过±5%
```

**方式B - 市场价格趋势分析**
```
产品：LED Panel Light 60x60cm
目标市场：United States / Germany
时间范围：近24个月
分析维度：
- 月度平均价格走势
- 价格波动幅度（标准差）
- 季节性规律
- 汇率影响分析
```

### 第2步：AI数据采集与分析

系统自动执行：
1. **多源数据采集**：从海关数据和授权B2B平台获取价格数据
2. **数据清洗**：过滤异常值（促销价/定制价），还原真实基准价
3. **趋势分析**：时间序列分析识别价格趋势和季节性规律
4. **竞品对比**：计算我方产品相对竞品的价格竞争力指数
5. **策略生成**：MatchGPT基于数据生成动态定价建议

### 第3步：输出价格分析报告

```json
{
  "report_type": "competitive_price_analysis",
  "product": "LED Panel Light 60x60cm 40W",
  "market": "United States",
  "period": "last_12_months",
  "my_product": {
    "name": "Our LED Panel 60x60",
    "fob_price": "$26.50",
    "moq": "100pcs",
    "price_trend": "stable",
    "price_competitiveness_index": 88
  },
  "competitors": [
    {
      "name": "Philips LED",
      "fob_price": "$32.00",
      "moq": "200pcs",
      "price_trend": "-3% (decreased 2 months ago)",
      "vs_my_product": "+20.8% higher",
      "threat_level": "medium"
    },
    {
      "name": "Cree Lighting",
      "fob_price": "$29.50",
      "moq": "100pcs",
      "price_trend": "stable",
      "vs_my_product": "+11.3% higher",
      "threat_level": "low"
    }
  ],
  "market_trend": {
    "direction": "slightly_decreasing",
    "monthly_change": "-1.2%",
    "seasonality": "Q4 (Oct-Dec) prices drop 5-8% due to inventory clearance"
  },
  "recommendations": [
    {
      "type": "defensive",
      "action": "我方价格维持$26.5，无需跟随Philips降价",
      "rationale": "Philips降价后绝对价格仍高20%，我方高端定位有空间"
    },
    {
      "type": "opportunity",
      "action": "11月前完成Q4订单（旺季前），建议增加报价频率",
      "rationale": "季节性规律显示Q4竞品价格下降，预计Q1需求回升"
    }
  ],
  "alerts": [
    {
      "competitor": "Philips LED",
      "alert_type": "price_drop",
      "change": "-3%",
      "action_required": "无需立即应对，继续观察1个月"
    }
  ]
}
```

### 第4步：配置自动预警

- **邮件预警**：竞品价格变动超阈值时，发送分析报告到指定邮箱
- **WhatsApp预警**：紧急预警（如竞品大幅降价）实时推送
- **日报/周报**：定期生成价格监控汇总报告

---

## 四、适用场景

| 场景 | 使用方式 |
|------|----------|
| 日常定价参考 | 收到客户询价时，先查市场价格再报价，避免报价过高或过低 |
| 竞品价格战应对 | 竞品突然降价，AI分析是否需要跟价及跟价幅度 |
| 新市场定价 | 进入新市场时，分析市场现有价格区间制定定价策略 |
| 年度采购计划 | 根据历史价格趋势，判断原材料最佳采购时机 |
| 合同价格谈判 | 拿着竞品价格数据与客户谈判，获取更好条款 |
| 展会报价策略 | 参展前分析竞品价格，制定差异化展会报价 |

---

## 五、资源索引

- **竞品监控配置模板**: 见 `references/competitor_list_template.md`（何时读取：配置竞品列表时参考格式）
- **价格分析报告模板**: 见 `references/price_analysis_report.md`（何时读取：生成标准格式分析报告时）
- **定价策略指南**: 见 `references/pricing_strategy_guide.md`（何时读取：制定具体定价策略时）

---

## 六、注意事项

### ⚠️ 数据局限性
- B2B平台价格通常是参考价，实际成交价可能更低
- 海关数据有1-3个月延迟，不适合实时监控
- 跨境电商价格（B2C）与B2B价格不可直接对比

### ⚠️ 预警配置
- 预警阈值设置过低会产生噪音，设置过高可能错过重要变化
- 建议初始阈值±5%，运行1个月后根据数据调整

### ⚠️ 定价策略
- 价格数据只是决策参考，不应作为唯一定价依据
- 需综合考虑产品成本、账期、订单量、长期合作价值

---

## 七、使用示例

### 示例 1：LED灯具价格战监控
**用户需求**：Philips最近在降价，我需要知道他们的价格变化趋势和我的应对策略

**执行结果**：
- Philips近3个月价格走势图（小幅下降3%）
- 我方相对Philips的价格优势（20%）
- 建议：暂不跟价，但加强非价格竞争（认证、交期、服务）
- 预警配置：Philips若再降价超过5%，自动触发预警

### 示例 2：德国市场价格分析
**用户需求**：我们计划进入德国市场，分析LED面板灯的价格区间和竞争态势

**执行结果**：
- 德国市场价格区间分析（低端$25-28/中端$30-35/高端$38+）
- 主要品牌份额和定价策略
- 我方进入建议定价（$30-32切入中端市场）

---

## 八、Common Rationalizations

| Rationalization | Reality |
|----------------|---------|
| "竞品降价我就必须跟价" | 只有在价格是唯一竞争维度时才需要跟价，差异化竞争更有效 |
| "平台价格就是真实成交价" | 平台报价往往含溢价空间，实际成交价通常低10-20% |
| "价格越低越好" | 价格战损害利润，差异化价值主张才能可持续 |
| "一次分析永久有效" | 市场价格持续变化，需要持续监控和动态调整 |

---

## 九、Verification

完成价格监控分析流程后：
- [ ] 确认数据来源可靠（海关数据/B2B平台/官网）
- [ ] 异常价格已过滤（促销价/定制价不纳入趋势分析）
- [ ] 预警阈值合理（避免过度预警或遗漏重要变化）
- [ ] 定价建议综合考虑成本和市场，而非仅参考竞品
- [ ] 报告数据已核实（抽样对比原始数据来源）
- [ ] 已设置跟进任务（价格变化后的应对措施已落实）

---

## 十、Security & Privacy

### 存储根路径
```
./data/yunlv-skills/priceMonitor/
├── monitoring/        # 监控配置
├── reports/           # 生成的分析报告
├── alerts/            # 预警记录
└── logs/              # 运行日志
```

### 数据处理原则
- **价格数据保护**：竞品价格数据仅用于用户自身定价参考
- **最小化留存**：监控数据保留12个月后自动归档

### 权限边界声明
- ✅ **允许**：读取 `./skills/yunlv-skills/references/` 下的参考文件
- ✅ **允许**：调用云旅AI数据API获取价格数据
- ✅ **允许**：写入 `./data/yunlv-skills/priceMonitor/` 监控配置和报告
- ✅ **允许**：向用户指定邮箱/WhatsApp发送预警通知
- ❌ **禁止**：将竞品价格数据用于销售或提供给第三方
- ❌ **禁止**：未经授权抓取竞品网站价格数据
