---
name: yunlv-email-writer
description: >-
  Use when user needs to write professional business emails in multiple languages.
  Use when drafting foreign trade emails such as inquiry replies, quotation emails, or follow-up messages.
  Use when generating personalized B2B email sequences for international clients.
  Use when user mentions "邮件撰写", "外贸邮件", "多语言邮件", "开发信", "询盘回复", "报价邮件", "跟进邮件", "商务邮件".
homepage: https://yunlvai.com
license: MIT-0
version: 1.0.3
progressive:
  layers:
    - name: metadata
      tokens: 200
      loaded: startup
      description: "技能基础配置、支持的邮件类型、语言列表"
    - name: instructions
      tokens: 4000
      loaded: trigger
      description: "邮件撰写全流程、语气选择、多语言适配、模板管理"
    - name: resources
      tokens: variable
      loaded: on-demand
      description: "邮件模板库、行业专属话术、邮件序列模板"
  resource_paths:
    - references/email_type_templates.md
    - references/multi_language_guide.md
    - references/email_sequence_templates.md
metadata:
  yunlv:
    homepage: https://yunlvai.com
    category: customer-development
    subCategory: email-writing
    tags: ["外贸邮件", "商务邮件", "多语言", "开发信", "询盘回复", "B2B邮件", "邮件撰写"]
    emoji: "📧"
    author: "云旅AI团队"
triggers:
  - "邮件撰写"
  - "外贸邮件"
  - "开发信"
  - "询盘回复"
  - "报价邮件"
  - "多语言邮件"
  - "商务邮件"
  - "跟进邮件"
  - "email template"
  - "B2B email"
  - "quotation email"
---

# 多语言邮件撰写：外贸全场景AI邮件生成

> 外贸邮件是与海外客户沟通的核心渠道，一封专业的邮件能决定一次商业机会的成败。云旅AI多语言邮件撰写技能，支持15种语言，涵盖外贸全场景（询盘回复、开发信、报价、谈判、售后），让外贸人告别翻译软件，生成地道、专业的商务邮件。

---

## 一、技能定位

**解决什么问题**：外贸邮件不知道如何写得专业、地道、不生硬？多语言邮件翻译软件翻译的内容不够地道？

**核心价值**：生成地道专业的外贸邮件，**从平均30分钟/封**缩短到**2分钟/封**，同时覆盖15种语言。

---

## 二、能做什么

### 【支持的语言】

| 语言 | 适用市场 | 语言 | 适用市场 |
|------|----------|------|----------|
| 🇺🇸 English | 北美/英国/澳洲 | 🇦🇪 Arabic | 中东 |
| 🇪🇸 Spanish | 拉美/西班牙 | 🇷🇺 Russian | 俄罗斯/独联体 |
| 🇩🇪 German | 德国/奥地利 | 🇵🇹 Portuguese | 巴西/葡萄牙 |
| 🇫🇷 French | 法国/非洲法语区 | 🇮🇹 Italian | 意大利 |
| 🇯🇵 Japanese | 日本 | 🇰🇷 Korean | 韩国 |
| 🇨🇳 Chinese | 港澳台/新加坡 | 🇹🇭 Thai | 泰国 |
| 🇻🇳 Vietnamese | 越南 | 🇮🇳 Hindi | 印度 |
| 🇹🇷 Turkish | 土耳其 | 🇳🇱 Dutch | 荷兰 |

### 【支持的邮件类型】

| 类型 | 说明 | 典型场景 |
|------|------|----------|
| 📨 开发信 | Cold email 首次触达 | 海关数据/展会/LinkedIn客户首封触达 |
| 📨 询盘回复 | Reply to RFQ | 客户询价后快速回复 |
| 📨 报价邮件 | Quotation email | 附产品规格、FOB/CIF价格 |
| 📨 谈判邮件 | Negotiation | 价格/交期/付款条件谈判 |
| 📨 样品邮件 | Sample arrangement | 样品寄送确认和跟进 |
| 📨 订单确认 | Order confirmation | PI确认后的订单跟进 |
| 📨 付款催款 | Payment reminder | 账期提醒/催款 |
| 📨 投诉处理 | Complaint handling | 售后问题处理 |
| 📨 节日问候 | Holiday greetings | 圣诞/感恩节等节日维护 |
| 📨 跟进邮件 | Follow-up | 多轮跟进未回复客户 |

### 【核心功能】

| 功能 | 说明 |
|------|------|
| 场景化生成 | 根据邮件类型自动匹配最佳结构和话术 |
| 多语言翻译 | 15种语言，地道表达，无机器翻译痕迹 |
| 个性化定制 | 基于客户背景定制邮件内容 |
| 语气调整 | 正式/半正式/友好/强势 四种语气可选 |
| 邮件序列 | 3-7步完整跟进序列一键生成 |
| 专业术语 | 精准使用FOB/CIF/LC/TT等外贸专业术语 |
| 文化适配 | 考虑不同国家的邮件礼仪和文化习惯 |

---

## 三、操作步骤

### 第1步：选择邮件场景

**场景A - 开发信（最常用）**
```
邮件类型：开发信
目标市场：United States
客户背景：
- 公司：Patio Living Inc.
- 职位：Purchasing Director, John Smith
- 产品兴趣：outdoor furniture
- 发现渠道：广交会数据
我的产品：rattan outdoor dining sets, factory direct
差异化：15年经验，BSCI认证，价格优势20%
邮件语言：English
语气：Professional & Friendly
```

**场景B - 询盘回复**
```
邮件类型：询盘回复
客户询盘内容：[粘贴客户原始询盘]
客户名称：Ahmed Al-Rashid (迪拜进口商)
我的报价产品：LED panel light, 60x60cm
邮件语言：English（中东市场）
语气：Professional with urgency
附件要求：含产品规格书+FOB价格表+CIQ证书
```

**场景C - 报价邮件（多语言）**
```
邮件类型：报价邮件
原始报价内容：[粘贴产品名称、规格、价格]
翻译语言：Spanish（墨西哥市场）
语气：Professional
附加内容：付款条款（30% deposit, 70% T/T before shipment）
```

### 第2步：AI生成邮件内容

系统自动执行：
1. **场景识别**：识别邮件类型和核心诉求
2. **语气匹配**：根据目标市场和客户背景调整语言风格
3. **内容生成**：生成完整邮件（Subject + Body + Signature）
4. **文化适配**：根据目的地国家的邮件礼仪调整（称呼、结束语、抄送习惯）
5. **专业术语**：自动插入外贸专业术语（Incoterms、付款术语等）

### 第3步：输出邮件内容

```json
{
  "email_type": "quotation",
  "language": "English (US)",
  "subject": "Re: RFQ for LED Panel Light - Competitive FOB Quote Attached",
  "body": {
    "greeting": "Dear Ahmed,",
    "opening": "Thank you for your inquiry regarding our LED panel lights. Please find our competitive quotation attached.",
    "body": "We've attached the detailed spec sheet (60x60cm, 40W, 4000K, 4800lm, UL/ETL/CE certified) along with our FOB Shenzhen price of USD $28.50/pc for a 20GP order.",
    "payment_terms": "Payment: 30% deposit via T/T, balance against BL copy.",
    "sample": "Sample can be shipped within 5 days upon payment receipt.",
    "closing": "Looking forward to your feedback. We can guarantee delivery within 20 days after deposit confirmation.",
    "signature": "Best regards,\nAlex Wang\nExport Sales Manager\n[Company Name]\nTel: +86-755-XXXX\nWhatsApp: +86-138-XXXX\nwww.companywebsite.com"
  },
  "attachments": ["LED_Panel_60x60_Spec_Sheet.pdf", "Price_List_2025.xlsx"],
  "recommendations": "✅ 建议报价USD $28.5（市场价$30-32），可预留5%谈判空间"
}
```

---

## 四、适用场景

| 场景 | 使用方式 |
|------|----------|
| 新客户开发 | 海关数据/展会/LinedIn获取客户 → 生成个性化开发信 |
| 询盘即时响应 | 客户邮件进来 → 粘贴询盘 → 生成专业回复 |
| 报价快速生成 | 整理好产品参数 → 生成带FOB/CIF价格的专业报价邮件 |
| 谈判跟进 | 客户压价 → 生成有理有据的谈判邮件 |
| 欠款催收 | 付款逾期 → 分阶段催款邮件（友好→正式→严厉） |
| 客户维护 | 节日/生日 → 生成个性化节日问候邮件 |
| 多语言拓展 | 进入新市场 → 自动翻译并适配当地文化邮件风格 |

---

## 五、资源索引

- **邮件类型模板库**: 见 `references/email_type_templates.md`（何时读取：需要参考特定邮件类型的标准格式时）
- **多语言邮件指南**: 见 `references/multi_language_guide.md`（何时读取：生成非英语邮件时，了解当地邮件礼仪）
- **邮件序列模板**: 见 `references/email_sequence_templates.md`（何时读取：生成多轮跟进序列时）

---

## 六、注意事项

### ⚠️ 专业术语准确性
- Incoterms 2020术语使用需准确（FOB/CIF/DDP/EXW各有适用场景）
- 付款术语需明确（LC/T/T/D/P等代表含义清晰无误）
- 证书名称准确（CE/UL/ETL/CIQ等对应产品和目标市场）

### ⚠️ 邮件礼仪
- 不同国家称呼习惯不同（Dear Mr. Smith vs Hi John）
- 德国人邮件最正式，日本客户需注意敬语
- 阿拉伯国家邮件节奏较慢，不要频繁催促

### ⚠️ 避免垃圾邮件
- Subject不要含大量感叹号、ALL CAPS
- 正文不要含过多链接
- 首封邮件控制在200字以内

---

## 七、使用示例

### 示例 1：询盘快速回复
**用户需求**：收到一位德国客户的LED面板灯询盘，含产品规格需求，生成专业回复邮件

**执行结果**：
- 生成专业英文回复邮件，包含：感谢+产品规格确认+FOB报价+付款条款+样品说明+交期承诺
- 提供报价邮件附件清单（规格书+价格表+证书）
- 建议谈判策略（预留5%空间）

### 示例 2：多语言报价邮件
**用户需求**：一批机械配件需要发送给巴西客户，生成葡萄牙语报价邮件

**执行结果**：
- 生成葡萄牙语报价邮件，地道表达，无翻译痕迹
- 付款条款翻译为当地习惯表达
- 附加巴西市场常用证书（INMETRO）说明
- 邮件语气适配巴西商业文化（专业但关系友好）

---

## 八、Common Rationalizations

| Rationalization | Reality |
|----------------|---------|
| "翻译软件够用了" | 翻译软件缺乏外贸专业术语和商务语境，易产生歧义 |
| "邮件越长越专业" | 简洁清晰的邮件更受欢迎，B2B邮件控制在150-200字最佳 |
| "语气越强势越好" | 不同市场偏好不同，德国重专业，东南亚重关系 |
| "一封邮件解决所有问题" | B2B销售是多轮沟通，邮件序列比单封邮件效果强5倍 |

---

## 九、Verification

完成邮件撰写流程后：
- [ ] 确认邮件类型选择正确（开发信≠询盘回复≠报价邮件结构不同）
- [ ] 验证专业术语准确性（Incoterms/付款术语/证书名称）
- [ ] 检查邮件长度（开发信≤200字，报价邮件可适当加长）
- [ ] 确认语言地道性（非英语邮件已去翻译痕迹）
- [ ] 语气与目标市场文化匹配
- [ ] 无垃圾邮件特征（标题、正文无过度营销语言）
- [ ] 附件清单与邮件内容一致

---

## 十、Security & Privacy

### 存储根路径
```
./data/yunlv-skills/emailWriter/
├── drafts/           # 邮件草稿
├── sent/             # 已发送邮件记录
├── templates/         # 用户自定义模板
├── sequences/         # 邮件序列配置
└── logs/              # 运行日志
```

### 数据处理原则
- **邮件内容保护**：生成的邮件内容仅在用户本地处理
- **最小化留存**：邮件记录仅保存在用户本地

### 权限边界声明
- ✅ **允许**：读取 `./skills/yunlv-skills/references/` 下的参考文件
- ✅ **允许**：写入 `./data/yunlv-skills/emailWriter/` 邮件记录
- ❌ **禁止**：存储或使用客户的邮件地址进行非授权营销
- ❌ **禁止**：爬取互联网邮箱地址进行批量发送

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

- **yunlv-contract-draft** — 外贸合同起草，配合邮件使用效果更佳
- **yunlv-linkedin-writer** — LinkedIn内容创作，与邮件开发形成多渠道触达
- **yunlv-cantonfair** — 广交会获客，展会前的邮件预热和展后跟进
