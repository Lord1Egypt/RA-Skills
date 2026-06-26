---
name: yunlv-contract-draft
description: >-
  Use when user needs to draft or review foreign trade contracts, sales agreements, or international commercial contracts.
  Use when generating Proforma Invoice (PI), Sales Contract (SC), or Memorandum of Understanding (MOU).
  Use when reviewing contract clauses for payment terms, delivery terms, or risk allocation.
  Use when user mentions "合同起草", "外贸合同", "PI", "形式发票", "销售合同", "合同审核", "MOU", "保密协议", "contract", "proforma invoice".
homepage: https://yunlvai.com
license: MIT-0
version: 1.0.2
progressive:
  layers:
    - name: metadata
      tokens: 200
      loaded: startup
      description: "技能基础配置、支持的合同类型、定价信息"
    - name: instructions
      tokens: 4500
      loaded: trigger
      description: "外贸合同起草全流程、合同类型选择、条款定制、风险审核"
    - name: resources
      tokens: variable
      loaded: on-demand
      description: "合同模板库、条款风险清单、国际商法参考"
  resource_paths:
    - references/contract_type_templates.md
    - references/clause_risk_checklist.md
    - references/international_commercial_law.md
metadata:
  yunlv:
    homepage: https://yunlvai.com
    primaryEnv: TRADEGPT_API_KEY
    category: compliance-risk
    subCategory: contract-drafting
    tags: ["合同起草", "外贸合同", "PI", "形式发票", "销售合同", "合同审核", "MOU", "保密协议", "国际商法", "Incoterms"]
    requires:
      env:
        - TRADEGPT_API_KEY
      bins:
        - python3
    apis:
      - name: 云旅AI TradeGPT API
        url: https://api.yunlvai.com
        purpose: "外贸合同内容生成与条款风险分析"
        auth: Bearer Token (TRADEGPT_API_KEY)
    emoji: "📝"
    author: "云旅AI团队"
    pricing:
      free:
        features: ["3份合同草稿", "基础PI生成", "标准条款"]
      basic:
        price: 299
        currency: CNY
        period: month
        features: ["无限合同起草", "多类型合同", "条款定制", "风险标注", "中英双语"]
      pro:
        price: 699
        currency: CNY
        period: month
        features: ["合同审核", "谈判策略", "多语言翻译", "专家审阅通道"]
triggers:
  - "合同起草"
  - "外贸合同"
  - "PI"
  - "形式发票"
  - "销售合同"
  - "合同审核"
  - "MOU"
  - "保密协议"
  - "NDA"
  - "contract"
  - "proforma invoice"
  - "Sales Contract"
  - "国际合同"
---

# 外贸合同智能起草：全类型合同一键生成

> 外贸合同是商业交易的法律保障，一份条款模糊或风险失衡的合同，可能让企业损失惨重。云旅AI外贸合同智能起草技能，支持PI/销售合同/MOU/NDA等全类型合同，精准嵌入Incoterms 2020、国际商法和国际贸易惯例，让外贸人5分钟生成专业合同。

---

## 一、技能定位

**解决什么问题**：外贸合同不知道哪些条款要写清楚？找律师起草太贵太慢？合同条款有漏洞不知道在哪里？

**核心价值**：从"拿着模板改"升级到"AI智能生成+风险标注"，合同起草时间从**2-3天**压缩到**5-30分钟**。

---

## 二、能做什么

### 【支持的合同类型】

| 类型 | 用途 | 典型场景 |
|------|------|----------|
| 📄 PI（形式发票） | 客户付款依据/形式发票 | 客户确认产品+价格，准备付款 |
| 📄 Sales Contract（销售合同） | 正式交易合同 | 大货订单，双方签署具有法律效力 |
| 📄 MOU（谅解备忘录） | 框架性协议 | 建立长期合作关系前期的框架约定 |
| 📄 NDA（保密协议） | 商业秘密保护 | 共享技术参数/报价前的保密约定 |
| 📄 L/C Amendment（信用证修改） | L/C条款变更 | 信用证条款与合同不符时的修改请求 |
| 📄 Quality Agreement（质量协议） | 质量标准约定 | 对产品质量标准、检验方法达成一致 |
| 📄 Agency Agreement（代理协议） | 代理权限约定 | 指定海外代理销售的合作条款 |
| 📄 OEM Agreement（代工协议） | 代工生产约定 | 品牌方委托工厂代工生产的协议 |

### 【核心功能】

| 功能 | 说明 |
|------|------|
| 全类型合同生成 | 8种外贸合同类型一键生成 |
| Incoterms 2020精准 | FOB/CIF/DDP/EXW等术语选择及责任划分 |
| 付款条款定制 | T/T/LC/D/P多种付款方式及风险条款 |
| 风险条款标注 | 自动标注高风险条款并提供修改建议 |
| 中英双语输出 | 全套合同中英双语，可直接给海外客户签署 |
| 条款对比分析 | 我方合同 vs 客户修改稿，逐条对比差异 |
| 谈判策略建议 | 基于合同条款分析，提供谈判优先顺序 |

---

## 三、操作步骤

### 第1步：选择合同类型并输入基本信息

**方式A - PI形式发票生成（最常用）**
```
合同类型：PI（Proforma Invoice）
买方信息：
- 公司：Patio Living Inc.
- 地址：123 Commerce St, Los Angeles, CA 90001, USA
- 联系人：John Smith
- 邮箱：j.smith@patioliving.com

卖方信息：
- 公司：[我方公司名称]
- 地址：[我方公司地址]

产品信息：
| 产品名称 | 规格 | 数量 | 单价 | 总价 |
|---------|------|------|------|------|
| LED Panel 60x60 | 40W, 4000K, ETL | 500pcs | $28.50 | $14,250 |
| LED Panel 60x60 | 40W, 5000K, ETL | 300pcs | $28.50 | $8,550 |

总金额：$22,800
价格条款：FOB Shenzhen
目的港：Los Angeles, USA
装运期限：2025-06-30
付款条款：30% T/T deposit, 70% T/T before shipment
有效期：PI发出后30天内有效
银行信息：[我方银行账户信息]
```

**方式B - 销售合同起草**
```
合同类型：Sales Contract
交易背景：
- 老客户，长期合作
- 本次订单金额：$85,000
- 付款方式谈判：客户要求50% T/T deposit，50% L/C at sight

希望定稿的条款：
- 争议解决：CIETAC仲裁
- 适用法律：中国法律
- 违约金条款：违约方赔偿守约方损失
- 产品规格：以双方确认的规格书为准
```

**方式C - 合同审核**
```
审核类型：合同条款风险审核
合同类型：Sales Contract（客户提供）
合同版本：[粘贴合同全文]

需要审核的维度：
- 付款条款风险
- 货物风险转移点
- 违约责任是否对等
- 争议解决条款
- 知识产权保护
```

### 第2步：AI合同生成/分析

系统自动执行：
1. **条款完整性检查**：检查必备条款是否齐全
2. **风险识别**：识别不平等条款、模糊条款、风险条款
3. **Incoterms对齐**：确保价格条款与责任条款一致
4. **付款条款分析**：分析付款方式风险，给出建议
5. **法律合规性**：核查是否符合国际贸易惯例（Incoterms 2020/UCP 600/INCOTERMS）
6. **格式规范化**：整理为标准合同格式，中英双语

### 第3步：输出合同文档

**PI形式发票示例输出：**
```
═══════════════════════════════════════════════
         PROFORMA INVOICE
═══════════════════════════════════════════════
PI No.: PI-2025-0425-001
Date: April 25, 2025
Valid Until: May 25, 2025

SELLER:
[Company Name]
[Address]
Tel: +86-XXX-XXXX
Bank: [Bank Name]
Account: XXXXXXXXXXXX
Swift: XXXXXXXX

BUYER:
Patio Living Inc.
123 Commerce St, Los Angeles, CA 90001, USA
Attn: John Smith
Email: j.smith@patioliving.com

───────────────────────────────────────────────
No. | Product Description | QTY | Unit Price | Amount
───────────────────────────────────────────────
1   | LED Panel 60x60 40W 4000K ETL | 500pcs | USD 28.50 | USD 14,250.00
2   | LED Panel 60x60 40W 5000K ETL | 300pcs | USD 28.50 | USD 8,550.00
───────────────────────────────────────────────
TOTAL: USD 22,800.00
───────────────────────────────────────────────

Price Term:        FOB Shenzhen
Total Amount:       USD Twenty-Two Thousand Eight Hundred Only
Packing:            Export cartons, 1pc/ctn
Gross Weight:       ~500kg (TBD)
CBM:                ~3.5CBM (TBD)
Shipment Port:      Shenzhen, China
Destination Port:   Los Angeles, CA, USA
Latest Shipment:    By June 30, 2025
Payment Terms:      30% T/T deposit; 70% T/T before shipment
Partial Shipment:   Not allowed
Transshipment:      Not allowed
Insurance:          To be covered by BUYER
Quality:            As per buyer's approved sample

Special Clauses:
☑ Buyer acknowledges this PI and confirms order intent
☑ 30% deposit must be paid within 7 days of PI confirmation
☑ Order not confirmed until deposit received
☑ Seller reserves right to cancel if deposit not received within 15 days

Signature (Seller):
Name: _______________
Title: ______________
Date: _______________

Signature (Buyer):
Name: _______________
Title: ______________
Date: _______________
═══════════════════════════════════════════════
```

**合同风险审核报告：**
```json
{
  "review_type": "contract_risk_audit",
  "contract_type": "Sales Contract",
  "overall_risk_level": 2,
  "risk_label": "中等风险 - 3项条款需谈判",
  "clause_reviews": [
    {
      "clause": "Payment: 50% T/T deposit, 50% L/C at sight",
      "risk": "MEDIUM",
      "issue": "L/C at sight对卖方有风险，建议改为L/C 30 days or D/P",
      "suggestion": "坚持使用L/C at sight，但要求买方银行交单前不得拒付"
    },
    {
      "clause": "Arbitration: ICC Paris",
      "risk": "LOW",
      "issue": "ICC仲裁成本较高，中小订单不划算",
      "suggestion": "建议改为CIETAC（中国）或AAA（美国），成本更低"
    },
    {
      "clause": "Force Majeure: standard clause",
      "risk": "HIGH",
      "issue": "标准不可抗力条款对卖方不公平，未覆盖'船公司停航'等物流因素",
      "suggestion": "补充：港口拥堵/船公司停航/海关延误为不可抗力"
    }
  ],
  "negotiation_priority": [
    {"priority": 1, "clause": "不可抗力条款扩展", "why": "高风险，可能导致巨额损失" },
    {"priority": 2, "clause": "付款条款澄清", "why": "影响资金回笼" },
    {"priority": 3, "clause": "仲裁机构调整", "why": "降低成本" }
  ]
}
```

---

## 四、适用场景

| 场景 | 使用方式 |
|------|----------|
| 新订单-生成PI | 确认客户需求 → 生成PI → 发给客户确认并付款 |
| 正式订单-起草合同 | 客户确认PI → 起草正式销售合同 → 双方签署 |
| 客户修改合同-审核 | 客户提供修改版合同 → AI审核风险点 → 制定谈判策略 |
| 长期合作-MOU | 建立代理/长期合作前 → 签署MOU明确权责 |
| 技术保密-NDA | 共享技术资料前 → 签署NDA保护双方利益 |
| 展会现场签约 | 展会上口头谈定 → 现场生成PI → 客户现场确认 |

---

## 五、资源索引

- **合同类型模板库**: 见 `references/contract_type_templates.md`（何时读取：需要特定类型合同参考模板时）
- **条款风险清单**: 见 `references/clause_risk_checklist.md`（何时读取：合同审核时，逐条检查风险）
- **国际商法参考**: 见 `references/international_commercial_law.md`（何时读取：理解Incoterms 2020/UCP 600/争议解决等法律背景）

---

## 六、注意事项

### ⚠️ 法律效力声明
- AI生成合同仅供参考，不能替代律师起草的正式法律文件
- 涉及重大金额或复杂交易的合同，建议由专业律师审核
- 合同双方均需在理解条款基础上自愿签署

### ⚠️ Incoterms 2020准确性
- 价格条款（FOB/CIF/DDP等）需与责任划分一致
- FOB不等于目的港费用由买方承担——这些额外费用需明确约定

### ⚠️ 付款条款风险
- T/T大额付款建议分批，30%+70%是最常见的安全结构
- L/C需明确开证行资信，开证行资信差则L/C保障有限
- 避免接受100% L/C at sight以外的高风险L/C条款

---

## 七、使用示例

### 示例 1：快速生成PI
**用户需求**：美国客户John确认了500pcs LED面板灯的订单，总金额$22,800，FOB深圳，30%+70%付款，6月底发货

**执行结果**：
- 生成标准PI格式，含完整产品信息、价格条款、装运信息、付款信息
- 中英双语版本，可直接发给客户
- 特殊条款标注：30%定金7天内支付等关键节点

### 示例 2：合同风险审核
**用户需求**：客户发来了修改后的销售合同，主要改了付款条款和争议解决条款，帮我审核

**执行结果**：
- 逐条审核所有修改点
- 识别3个风险点（付款条款风险、不抗力条款扩展不足、违约金上限）
- 给出谈判优先顺序和话术建议

---

## 八、Common Rationalizations

| Rationalization | Reality |
|----------------|---------|
| "老客户不需要签正式合同" | 口头协议无法律保障，老客户纠纷处理成本更高 |
| "合同模板改一改就够了" | 模板≠适合每笔交易，条款必须量身定制 |
| "付款条款越灵活越好" | 付款条款过于宽松是外贸企业坏账的主要来源 |
| "AI合同可以替代律师" | AI合同是工具不是替代品，重大合同必须律师审核 |

---

## 九、Verification

完成合同起草/审核流程后：
- [ ] 确认合同类型选择正确（PI≠正式合同，法律效力不同）
- [ ] Incoterms 2020术语使用准确（FOB/CIF/DDP责任划分清晰）
- [ ] 付款条款风险已评估（高风险条款已标注）
- [ ] 金额数字无误（中英文大写一致）
- [ ] 双方公司信息准确（名称/地址/联系方式）
- [ ] 特殊条款已明确（不可抗力/违约金/争议解决）
- [ ] 中英双语版本内容一致

---

## 十、Security & Privacy

### 存储根路径
```
./data/yunlv-skills/contractDraft/
├── drafts/           # 合同草稿
├── signed/          # 已签署合同存档
├── reviews/         # 审核报告
└── logs/            # 运行日志
```

### 数据处理原则
- **合同内容保密**：生成的合同内容严格保密，不存储在第三方服务器
- **最小化留存**：草稿合同保留6个月，已签署合同由用户自行保管
- **数据隔离**：不同用户的合同数据完全隔离，不可跨用户访问

### 权限边界声明
- ✅ **允许**：读取 `./skills/yunlv-skills/references/` 下的参考文件
- ✅ **允许**：调用云旅AI TradeGPT API生成合同内容
- ✅ **允许**：写入 `./data/yunlv-skills/contractDraft/` 合同草稿
- ❌ **禁止**：将用户合同数据用于模型训练或提供给第三方
- ❌ **禁止**：AI合同直接替代律师意见（需注明仅供参考）

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

- **yunlv-compliance-check** — 合规检查，确保合同条款合规
- **yunlv-customs-scout** — 海关情报，识别高风险交易方
- **yunlv-email-writer** — 外贸邮件，发送合同给客户
