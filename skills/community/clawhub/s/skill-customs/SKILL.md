---
name: yunlv-customs-scout
description: >-
  Use when user needs to find import/export trade data, competitor customers, or market intelligence from customs data.
  Use when searching for active buyers of specific products in target markets.
  Use when performing competitor client mining via trade records.
  Use when user mentions "海关数据", "进出口数据", "采购商", "竞争对手客户", "挖客户", "贸易数据", "Import Intel".
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
      tokens: 4000
      loaded: trigger
      description: "海关数据挖掘全流程、评分算法、输出格式、触达策略"
    - name: resources
      tokens: variable
      loaded: on-demand
      description: "数据过滤规则、客户评分模型、触达话术库"
  resource_paths:
    - references/data_filter_rules.md
    - references/customer_scoring_model.md
    - references/outreach_templates.md
metadata:
  yunlv:
    homepage: https://yunlvai.com
    primaryEnv: TRADEGPT_API_KEY
    category: customer-development
    subCategory: customs-data-mining
    tags: ["海关数据", "进出口数据", "贸易情报", "竞品客户挖掘", "B2B外贸", "采购商发现"]
    requires:
      env:
        - TRADEGPT_API_KEY
      bins:
        - python3
    apis:
      - name: 云旅AI MatchGPT API
        url: https://api.yunlvai.com
        purpose: "海关贸易数据查询与智能匹配"
        auth: Bearer Token (TRADEGPT_API_KEY)
      - name: 全球海关数据
        url: https://data.yunlvai.com
        purpose: "228+国家进出口贸易记录数据源"
        auth: Bearer Token
    emoji: "🔍"
    author: "云旅AI团队"
    pricing:
      free:
        features: ["每天5次免费查询", "基础贸易数据", "近3个月记录"]
      basic:
        price: 599
        currency: CNY
        period: month
        features: ["每月500次查询", "完整联系方式", "决策人挖掘", "邮件触达"]
      pro:
        price: 1999
        currency: CNY
        period: month
        features: ["无限查询", "竞品客户分析", "采购预测", "WhatsApp+邮件双通道触达"]
triggers:
  - "海关数据"
  - "进出口记录"
  - "竞争对手客户"
  - "挖采购商"
  - "竞品分析"
  - "贸易情报"
  - "进口商查询"
  - "采购记录"
  - "customs data"
  - "trade intelligence"
---

# 海关数据智能获客：竞品客户挖掘与贸易情报

> 海关数据是全球贸易的"数字金矿"，每笔进出口记录都包含采购商、供应商、产品规格、交易量和金额等关键信息。云旅AI海关数据智能获客技能，帮助外贸企业从228+国家的真实贸易记录中精准定位目标采购商，追踪竞品客户动态，抢占市场先机。

---

## 一、技能定位

**解决什么问题**：如何从海量海关数据中找到真实活跃的采购商，并从竞争对手手中抢夺客户？

**核心价值**：将"盲目开发"升级为"精准狙击"，客户开发效率提升 **400%**。

---

## 二、能做什么

### 【核心功能】

| 功能 | 说明 |
|------|------|
| 采购商发现 | 按产品/HS编码/国家发现真实采购商及采购量 |
| 竞品客户挖掘 | 输入竞争对手名称，挖掘其所有客户及合作深度 |
| 贸易轨迹追踪 | 追踪目标采购商的采购周期、供应商变更趋势 |
| 供应链可视化 | 呈现采购商的完整供应商结构和市场份额 |
| 采购需求预测 | 基于历史数据预测未来3-6个月采购窗口期 |
| 智能触达 | 自动生成个性化开发信，通过邮件/WhatsApp触达 |
| 竞争态势分析 | 分析目标市场的供应商格局、竞争强度、进入机会 |

### 【数据覆盖】

- 国家覆盖：228+ 国家/地区
- 贸易记录：320万+ 条年度贸易记录
- 企业数据：280万+ 海外采购商画像
- 产品品类：全品类覆盖（支持HS编码精确查询）

---

## 三、操作步骤

### 第1步：选择查询模式

**模式A - 产品/HS编码查询（最常用）**
```
查询条件：
- 产品关键词：LED panel light 或 HS编码：9405.11
- 目标市场：United States
- 时间范围：近12个月
- 采购量筛选：年进口额≥$100,000
```

**模式B - 竞争对手客户挖掘**
```
查询条件：
- 竞争对手公司：Philips Lighting
- 目标市场：Europe
- 想挖的客户类型：年采购额>50万美元的活跃客户
```

**模式C - 特定采购商深度调研**
```
查询条件：
- 目标采购商公司名：Acme Lighting Corp
- 调研维度：采购历史、供应商结构、采购周期
```

### 第2步：AI智能分析与筛选

系统自动执行：
1. **数据召回**：从228+国家海关数据库召回所有匹配记录
2. **信息补全**：匹配企业名称、联系方式、社交媒体、决策人
3. **评分排序**：MatchGPT从采购规模、活跃度、竞品依赖度、进入机会4维度评分
4. **竞品关系分析**：识别该采购商当前的供应商构成及合作深度
5. **触达时机推荐**：基于采购周期预测最佳接触时间窗口

### 第3步：输出结构化情报报告

```json
{
  "query_type": "competitor_mining",
  "competitor": "Philips Lighting",
  "target_market": "United States",
  "date_range": "last_12_months",
  "total_importers_found": 234,
  "active_importers": 187,
  "high_opportunity": 42,
  "top_opportunities": [
    {
      "rank": 1,
      "importer_name": "LumaMax Lighting Inc.",
      "country": "United States",
      "annual_import_value": "$4.5M",
      "import_frequency": "monthly",
      "current_suppliers": ["Philips ($3.2M)", "Osram ($0.8M)", "Others ($0.5M)"],
      "opportunity_score": 9.4,
      "why_vulnerable": "Philips占比71%，单一供应商依赖风险高，且我司价格优势约25%",
      "recommended_action": "以价格+样品切入，重点强调非Philips替代方案",
      "best_contact_window": "Q2采购淡季（4-5月），提前1个月触达",
      "contact_person": "Sarah Chen",
      "contact_role": "VP of Procurement",
      "email": "s.chen@lumamax.com",
      "phone": "+1-555-0188"
    }
  ]
}
```

### 第4步：一键触达

- **邮件开发信**：基于竞品替代逻辑生成个性化邮件（英文/德文/法文等）
- **WhatsApp触达**：针对美国/东南亚市场优先使用WhatsApp
- **LinkedIn连接**：针对决策人直接发送LinkedIn连接请求
- **跟进序列**：设置多轮跟进序列（3-7-15天），未读自动触发

---

## 四、适用场景

| 场景 | 使用方式 |
|------|----------|
| 新市场开拓 | 搜索某产品在某国家的所有采购商，按量级筛选 |
| 竞品客户抢夺 | 输入竞品名称，系统挖掘其所有客户及合作机会 |
| 现有客户深挖 | 追踪老客户的供应商变化趋势，预警流失风险 |
| 定价策略制定 | 了解目标市场的价格区间和竞品定价 |
| 展会前预判 | 参展前用海关数据预判哪些采购商会参展 |
| 供应商替代侦察 | 反向分析：我司的哪些客户被竞争对手挖角 |

---

## 五、资源索引

- **海关数据过滤规则**: 见 `references/data_filter_rules.md`（何时读取：需要自定义数据筛选条件时）
- **客户评分模型**: 见 `references/customer_scoring_model.md`（何时读取：理解评分逻辑或调整权重时）
- **竞品挖掘触达话术**: 见 `references/outreach_templates.md`（何时读取：生成竞品替代类开发信时）

---

## 六、注意事项

### ⚠️ 数据合规
- 海关数据仅用于B2B外贸合法商业开发
- 禁止将数据用于销售名单交易或非法竞争
- 各国数据开放程度不同，实际覆盖率视目标市场而定

### ⚠️ 联系方式准确性
- 联系方式匹配率约 65-75%，高价值客户建议用LinkedIn二次验证
- 决策人信息每周更新，建议重要客户每月复核

### ⚠️ 触达策略
- 竞品替代类话术效果最佳，但需确保产品对比数据准确
- 邮件发送遵守GDPR/CAN-SPAM规范

---

## 七、使用示例

### 示例 1：挖掘美国LED照明采购商
**用户需求**：我们是做LED面板灯的，挖掘近一年在美国市场年采购量超50万美元的采购商

**执行结果**：
- 查询到 187 家活跃采购商
- 高机会评分（≥8分）42 家，首选推荐 15 家
- 输出每家公司的采购量、供应商结构、触达窗口和联系方式

### 示例 2：抢夺Philips的欧洲客户
**用户需求**：Philips是我们最大的竞争对手，挖掘他们在欧洲的主要客户

**执行结果**：
- 识别 Philips 在欧洲的 156 家活跃客户
- 其中 23 家采购量超 200 万美元
- 分析每家的供应商依赖度和可切入角度
- 生成针对性的竞品替代开发信模板

---

## 八、Common Rationalizations

| Rationalization | Reality |
|----------------|---------|
| "海关数据包含所有采购商联系方式" | 联系方式匹配率约65-75%，中东/非洲覆盖率更低 |
| "从竞品手里挖客户很容易" | 需明确差异化优势，单纯价格战效果有限 |
| "采购量大就等于好客户" | 需综合考虑付款周期、账期要求、合规成本 |
| "海关数据实时更新" | 不同国家数据延迟1-6个月，美国数据最及时 |

---

## 九、Verification

完成海关数据客户挖掘流程后：
- [ ] 确认查询条件精准（产品/竞品/市场三要素至少两项明确）
- [ ] 验证评分逻辑（4个维度均有数据支撑，非主观臆断）
- [ ] 确认供应链分析准确（供应商份额之和约等于100%）
- [ ] 触达话术符合竞品替代逻辑（数据对比准确）
- [ ] 触达策略符合GDPR/CAN-SPAM规范
- [ ] 已设置跟进提醒，避免首次触达后无后续

---

## 十、Security & Privacy

### 存储根路径
```
./data/yunlv-skills/customsScout/
├── queries/         # 查询历史记录
├── reports/         # 生成的情报报告
├── leads/           # 导出的客户名单
├── outreach/        # 触达记录和开发信
└── logs/            # 运行日志
```

### 数据处理原则
- **本地处理**：查询条件和企业中转数据仅在本地处理
- **敏感数据保护**：API密钥和批量联系人数据不写入日志
- **数据时效**：海关数据默认保留近24个月，逾期自动归档

### 权限边界声明
- ✅ **允许**：读取 `./skills/yunlv-skills/references/` 下的参考文件
- ✅ **允许**：调用云旅AI海关数据API获取贸易记录
- ✅ **允许**：写入 `./data/yunlv-skills/customsScout/leads/` 导出名单
- ✅ **允许**：通过邮件/WhatsApp/LinkedIn通道触达目标客户（需用户授权）
- ❌ **禁止**：将海关数据用于销售名单交易或第三方数据服务
- ❌ **禁止**：抓取未授权的第三方数据源
