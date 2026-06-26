---
name: yunlv-pricing
description: >-
  Use when user needs to generate pricing strategy suggestions for B2B export businesses.
  Use when preparing market pricing reference reports and competitive positioning advice.
  Use when creating dynamic pricing recommendations based on market context.
  Use when user mentions "定价策略", "价格参考", "价格趋势", "市场定价", "价格分析", "定价建议", "pricing strategy", "pricing advice".
homepage: https://yunlvai.com
license: MIT-0
version: 1.0.7
progressive:
  layers:
    - name: metadata
      tokens: 200
      loaded: startup
      description: "技能基础配置、定价参考说明、策略信息"
    - name: instructions
      tokens: 3500
      loaded: trigger
      description: "定价策略生成全流程、趋势参考、建议配置、策略建议"
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
    tags: ["定价策略", "价格参考", "市场定价", "价格趋势", "定价建议", "B2B定价", "市场参考"]
    requires:
      env:
        - TRADEGPT_API_KEY
    apis:
      - name: 云旅AI TradeGPT API
        url: https://api.yunlvai.com
        purpose: "生成定价策略建议与市场参考分析"
        auth: Bearer Token (TRADEGPT_API_KEY)
    emoji: "📊"
    author: "云旅AI团队"
    pricing:
      free:
        features: ["每周生成5次参考建议", "基础定价参考", "单产品分析"]
      basic:
        price: 299
        currency: CNY
        period: month
        features: ["每日策略生成", "10个参考维度", "趋势参考图", "邮件建议内容"]
      pro:
        price: 899
        currency: CNY
        period: month
        features: ["实时策略建议", "无限参考维度", "深度分析报告", "WhatsApp建议内容", "定价建议"]
triggers:
  - "定价策略"
  - "价格参考"
  - "价格趋势"
  - "市场定价"
  - "定价建议"
  - "价格分析"
  - "pricing strategy"
  - "pricing advice"
  - "pricing recommendation"
---

# 定价策略顾问：市场参考与智能定价建议

> 在B2B外贸战场上，定价是决定订单归属的核心决策。云旅AI定价策略顾问，帮助外贸企业生成市场定价参考方案，辅助识别价格变化趋势，智能生成定价调整建议，让企业永远比竞争对手快一步做出定价决策。

---

## 一、技能定位

**解决什么问题**：市场定价如何制定？竞品价格变化时，我该怎么调整？定价决策周期太长？

**核心价值**：从"凭经验定价"升级为"数据辅助定价决策"，定价决策周期从**周级**压缩到**小时级**。

---

## 二、能做什么

### 【核心功能】

| 功能 | 说明 |
|------|------|
| 定价参考生成 | 基于市场参考信息生成10-50个维度的定价参考方案 |
| 趋势参考分析 | 可视化展示近6-24个月的市场价格走势参考 |
| 定价调整建议 | 市场价格大幅波动时生成调整建议供用户参考 |
| 市场份额参考 | 基于公开市场信息估算各品牌市场份额变化参考 |
| 定价策略建议 | 基于市场参考给出动态定价建议（进攻型/防守型） |
| 交叉对比参考 | 我方产品 vs 市场参考价格矩阵分析 |
| 季节性规律参考 | 辅助识别产品价格的季节性波动规律 |
| 成本-价格联动参考 | 辅助分析原材料成本变化对终端价格的影响参考 |

### 【参考信息来源】

- 云旅AI授权参考信息源（海关公开数据、B2B平台公开报价、行业公开报告）

---

## 三、操作步骤

### 第1步：描述定价需求

**方式A - 定价参考需求**
```
参考产品：
- 我方产品：LED Panel 60x60 40W
- 参考市场：美国 / 德国

参考维度：
- 市场定价区间（FOB/CIF）
- 最小起订量（MOQ）参考
- 付款条款参考
- 促销节奏参考

建议生成频率：每日
调整建议条件：市场参考变动超过±5%
```

**方式B - 市场趋势参考分析**
```
产品：LED Panel Light 60x60cm
目标市场：United States / Germany
时间范围：近24个月
分析维度：
- 月度平均价格走势参考
- 价格波动幅度参考（标准差）
- 季节性规律参考
- 汇率影响参考
```

### 第2步：AI生成定价策略

系统辅助执行：
1. **市场参考整合**：基于云旅AI参考信息源整合市场参考
2. **异常过滤**：过滤促销价/定制价等非基准参考
3. **趋势参考生成**：时间序列分析生成价格趋势参考
4. **竞争力参考**：计算我方产品相对市场参考的竞争力指数
5. **策略生成**：MatchGPT基于参考信息生成动态定价建议

### 第3步：输出定价参考报告

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

### 第4步：获取定价建议

- **邮件建议内容**：市场参考变动时，生成策略建议供用户查看
- **WhatsApp建议内容**：紧急建议（如市场大幅变动）生成调整建议
- **日报/周报**：定期生成定价参考汇总报告

---

## 四、适用场景

| 场景 | 使用方式 |
|------|----------|
| 日常定价参考 | 收到客户询价时，先参考市场定价再报价，避免报价过高或过低 |
| 价格战应对 | 市场价格变化时，AI分析是否需要调整及调整幅度 |
| 新市场定价 | 进入新市场时，参考市场现有价格区间制定定价策略 |
| 年度采购计划 | 根据历史趋势参考，判断原材料最佳采购时机 |
| 合同价格谈判 | 参考市场定价数据与客户谈判，获取更好条款 |
| 展会报价策略 | 参展前分析市场定价，制定差异化报价 |

---

## 五、资源索引

- **竞品参考配置模板**: 见 `references/competitor_list_template.md`（何时读取：配置参考维度时参考格式）
- **定价参考报告模板**: 见 `references/price_analysis_report.md`（何时读取：生成标准格式参考报告时）
- **定价策略指南**: 见 `references/pricing_strategy_guide.md`（何时读取：制定具体定价策略时）

---

## 六、注意事项

### ⚠️ 参考信息局限性
- B2B平台价格通常是参考价，实际成交价可能更低
- 海关公开数据有1-3个月延迟，不适合实时参考
- 跨境电商价格（B2C）与B2B价格不可直接对比

### ⚠️ 建议配置
- 建议阈值设置过低会产生噪音，设置过高可能错过重要变化
- 建议初始阈值±5%，运行1个月后根据参考调整

### ⚠️ 定价策略
- 价格数据只是决策参考，不应作为唯一定价依据
- 需综合考虑产品成本、账期、订单量、长期合作价值

---

## 七、使用示例

### 示例 1：LED灯具定价参考
**用户需求**：需要了解LED面板灯的市场定价参考和我的定价建议

**执行结果**：
- 市场参考价格走势（近期小幅下降3%）
- 我方相对市场的价格优势参考（20%）
- 建议：暂不调整，但加强非价格竞争（认证、交期、服务）
- 建议配置：市场参考变动超过5%时，生成调整建议

### 示例 2：德国市场定价参考
**用户需求**：我们计划进入德国市场，参考LED面板灯的市场定价区间

**执行结果**：
- 德国市场价格区间分析（低端$25-28/中端$30-35/高端$38+）
- 主要品牌份额和定价策略
- 我方进入建议定价（$30-32切入中端市场）

---

## 八、Common Rationalizations

| Rationalization | Reality |
|----------------|---------|
| "竞品降价我就必须跟价" | 只有在价格是唯一竞争维度时才需要调整，差异化竞争更有效 |
| "平台参考价就是真实成交价" | 平台报价往往含溢价空间，实际成交价通常低10-20% |
| "价格越低越好" | 价格战损害利润，差异化价值主张才能可持续 |
| "一次参考永久有效" | 市场价格持续变化，需要持续评估和动态调整 |

---

## 九、Verification

完成价格查询分析流程后：
- [ ] 确认参考信息来源可靠（海关公开数据/B2B平台/官网）
- [ ] 异常参考已过滤（促销价/定制价不纳入趋势参考）
- [ ] 建议阈值合理（避免过度建议或遗漏重要变化）
- [ ] 定价建议综合考虑成本和市场，而非仅参考市场
- [ ] 报告参考信息已核实（抽样对比原始信息来源）
- [ ] 已设置跟进任务（定价变化后的应对措施已落实）

---

## 十、Security & Privacy

### 存储根路径
```
./data/yunlv-skills/priceMonitor/
├── monitoring/        # 查询配置
├── reports/           # 生成的分析报告
├── alerts/            # 提醒记录
└── logs/              # 运行日志（不含原始价格数据）
```

### 数据流透明声明 (Data Flow Transparency)

本技能的数据处理流程完全透明，所有数据传输均有明确目的：

| 数据流 | 方向 | 内容 | 用途 | 保护措施 |
|--------|------|------|------|----------|
| 用户 → 本技能 | 输入 | 定价需求（产品名称、参考维度） | 构建策略请求 | 本地处理 |
| 本技能 → 云旅AI API | 请求 | 产品关键词+定价场景描述 | 获取定价策略建议 | TLS 1.3加密传输 |
| 云旅AI API → 本技能 | 响应 | 定价策略建议（参考分析） | 生成用户报告 | 服务端不存储请求 |
| 本技能 → 用户 | 输出 | 格式化的定价参考报告+策略建议 | 辅助定价决策 | 数据保留在用户环境 |

**关键保证**：
- 📌 **API仅用于策略生成**：云旅AI API接收产品描述，返回定价建议。不传输任何原始商业数据
- 📌 **不传输原始商业数据**：不将用户的产品定价、客户信息等发送到任何外部服务
- 📌 **不建立价格数据库**：本技能不收集、不聚合、不转售任何用户数据
- 📌 **建议结果仅用户可见**：生成的报告保存在用户本地目录，不自动同步到云端

### 数据保护措施

- **加密传输**：所有API通信使用TLS 1.3加密，确保数据在传输过程中不被截获
- **不存储原始数据**：API返回的策略建议仅用于生成当前报告，不持久化存储在日志或缓存中
- **最小化留存**：使用记录保留30天，超期自动归档删除，日志中不记录原始参考数据
- **本地优先**：所有分析报告和策略建议保存在用户本地目录，不自动上传

### 合规声明

- **GDPR合规**：不处理欧盟公民个人数据，价格数据属于公开市场信息
- **PIPL合规**：不收集个人信息，竞品价格数据来源于公开渠道
- **数据主权**：所有数据保留在用户自有环境中，用户对数据拥有完全控制权

### 权限边界声明
- ✅ **允许**：读取 `./skills/yunlv-skills/references/` 下的参考文件
- ✅ **允许**：调用云旅AI API获取定价策略建议
- ✅ **允许**：写入 `./data/yunlv-skills/priceMonitor/` 用户自有数据
- ✅ **允许**：生成定价建议内容供用户查看
- ❌ **禁止**：将用户商业数据用于销售或提供给第三方
- ❌ **禁止**：自动采集或查询竞品网站的非公开数据
- ❌ **禁止**：在日志或输出中记录API请求的原始响应数据
- ❌ **禁止**：将多个用户的价格数据跨账户聚合分析

### 本技能不做的事 (What This Skill Does NOT Do)
- ❌ 不自动采集竞品网站数据（如采集Alibaba/MIC价格）
- ❌ 不将用户的产品定价信息发送到第三方
- ❌ 不建立跨用户的行业定价数据库
- ❌ 不自动执行调价操作（仅提供建议，由用户决策）
- ❌ 不存储或转发API返回的原始策略数据

---

## ⚠️ 不要在以下情况使用

- 需要法律专业意见时（请咨询律师）
- 涉及特殊行业监管时（请咨询行业专家）

---

## 交付标准

- 方案结构完整，覆盖所有章节
- 建议具体可执行，不含模糊表述
- 内容适配用户提供的行业和场景
- 输出格式清晰，便于直接使用

---

## 相关技能推荐

- **yunlv-product-desc** — 产品描述，突出差异化卖点支撑定价
- **yunlv-email-writer** — 外贸邮件，报价邮件专业呈现
- **yunlv-cantonfair** — 广交会，展会现场快速报价
