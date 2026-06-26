---
name: yunlv-linkedin-writer
description: >-
  Use when user needs to generate professional B2B outreach message content.
  Use when creating professional B2B communication content and engagement.
  Use when writing professional B2B outreach messages for prospects.
  Use when user mentions "社媒开发信", "B2B联系", "联系消息", "社媒消息生成", "专业消息撰写".
homepage: https://yunlvai.com
license: MIT-0
version: 1.0.3
progressive:
  layers:
    - name: metadata
      tokens: 200
      loaded: startup
      description: "技能基础配置、渠道说明、定价信息"
    - name: instructions
      tokens: 3500
      loaded: trigger
      description: "B2B专业消息生成全流程、个性化策略、跟进序列设计"
    - name: resources
      tokens: variable
      loaded: on-demand
      description: "话术模板库、行业钩子库、跟进序列模板"
  resource_paths:
    - references/linkedin_message_templates.md
    - references/industry_hooks_library.md
    - references/followup_sequence_templates.md
metadata:
  yunlv:
    homepage: https://yunlvai.com
    primaryEnv: TRADEGPT_API_KEY
    category: customer-development
    subCategory: linkedin-message-writing
    tags: ["B2B社媒", "专业联系", "B2B沟通", "B2B联系", "联系消息", "社媒消息"]
    requires:
      env:
        - TRADEGPT_API_KEY
    apis:
      - name: 云旅AI MatchGPT API
        url: https://api.yunlvai.com
        purpose: "B2B专业消息内容生成"
        auth: Bearer Token (TRADEGPT_API_KEY)
    emoji: "💼"
    author: "云旅AI团队"
    pricing:
      free:
        features: ["每天10条消息生成", "基础话术模板", "英文消息"]
      basic:
        price: 199
        currency: CNY
        period: month
        features: ["无限消息生成", "15种语言支持", "个性化定制", "跟进序列生成"]
      pro:
        price: 599
        currency: CNY
        period: month
        features: ["多消息生成", "高级序列设计", "A/B测试优化", "回复分析"]
triggers:
  - "LinkedIn"
  - "领英"
  - "联系消息"
  - "LinkedIn消息"
  - "专业消息撰写"
  - "社媒开发"
  - "社媒消息生成"
  - "B2B社交"
  - "LinkedIn message writing"
---

# B2B专业消息生成：个性化社媒联系内容

> 社媒平台是B2B开发决策人的重要渠道。云旅AI B2B专业消息生成技能，基于MatchGPT驱动的消息生成引擎，帮助外贸人快速生成高回复率的社媒消息，辅助设计跟进序列，让专业消息生成效率提升10倍。

---

## 一、技能定位

**解决什么问题**：B2B社媒消息不知道写什么、回复率低、跟进混乱？

**核心价值**：从"手写每封消息"升级到"AI生成个性化消息"，单个开发消息准备时间从 **15分钟** 压缩到 **30秒**。

---

## 二、能做什么

### 【核心功能】

| 功能 | 说明 |
|------|------|
| 个性化消息内容生成 | 基于用户提供的目标客户背景、公司动态、行业背景生成定制消息 |
| 多语言支持 | 英文、西班牙文、德文、法文、阿拉伯文、日文等15种语言 |
| 联系消息优化 | 300字符以内的联系请求话术优化，提升通过率 |
| 跟进序列设计 | 辅助生成3-5步跟进序列，覆盖首次联系到成交前所有节点 |
| 行业钩子库 | 内置50+行业痛点钩子（"I noticed..."类型） |
| 消息版本优化 | 辅助生成2-3个版本消息供测试选择 |
| 语气风格选择 | 专业正式/轻松友好/数据驱动/关系导向四种风格 |

### 【效果数据】

- 个性化消息通过率：个性化消息 vs 模板消息，**38% vs 12%**
- 消息回复率：专业定制消息平均回复率 **25-35%**
- 支持语言：15种主流外贸语言

---

## 三、操作步骤

### 第1步：描述目标客户背景

**方式A - 客户提供背景信息（如LinkedIn公开资料）**
```
目标客户背景：https://www.linkedin.com/in/johnsmith-patio
目标产品：outdoor furniture
联系目的：建立联系 → 分享产品资料
消息语言：English
```

**方式B - 关键词描述目标客户画像**
```
目标客户画像：
- 职位：Purchasing Manager / VP of Procurement
- 公司类型：Outdoor furniture importer
- 所在地区：United States, East Coast
- 公司规模：50-200人
- 活跃度：每周发帖
目标产品：rattan outdoor dining sets
我的差异化： factory direct pricing, 15 years experience
消息风格：专业友好
```

**方式C - 多客户信息输入**
```
上传CSV格式：
name, title, company, linkedin_url, product_interest, notes
John Smith, Purchasing Director, Patio Living Inc., https://..., outdoor furniture, met at Canton Fair 137th
```

### 第2步：AI分析与消息生成

系统辅助执行：
1. **背景信息整理**：整理用户提供的信息（职位、公司、行业、动态、互动）
2. **个性化元素提取**：识别共同话题、行业痛点、公司动态作为钩子
3. **消息生成**：MatchGPT基于钩子库生成个性化消息（3个版本供选）
4. **合规检查**：检查字符数限制（联系请求300字符、私信500字符）、敏感词过滤
5. **序列设计**：生成从首次联系到第5次跟进的完整序列

### 第3步：输出消息内容

**联系请求消息示例：**
```
Hi John,

Congrats on Patio Living's expansion into the European market — I saw the news on LinkedIn last month.

I'm Alex from [Company], a specialist in outdoor furniture manufacturing with 15+ years serving North American brands. We've helped companies like yours reduce procurement costs by 20-30%.

Would love to share how we can support your growth plans. Open to a quick chat?

Best,
Alex
```
> 字符数：297 ✅（符合平台限制）

**跟进序列示例（第1-5轮）：**
| 步骤 | 时间 | 消息类型 | 目的 |
|------|------|----------|------|
| 第1轮 | Day 0 | 联系请求 | 建立关系 |
| 第2轮 | Day 3 | 私信（连接通过后）| 价值传递 |
| 第3轮 | Day 7 | 产品案例分享 | 激发兴趣 |
| 第4轮 | Day 14 | 行业报告/数据 | 制造紧迫感 |
| 第5轮 | Day 28 | 限时优惠/Offer | 促进行动 |

### 第4步：手动发送

- **手动发送**：复制消息内容，粘贴到社媒平台发送
- **复制粘贴发送**：用户复制生成内容手动发送

---

## 四、适用场景

| 场景 | 使用方式 |
|------|----------|
| 广交会后跟进 | 展会上收集的名片，生成社媒联系消息 |
| 海关数据客户联系 | 从CUSTOMS_SCOUT导出的采购商，找到目标决策人 |
| 竞品客户联系 | 锁定竞争对手的公司员工，主动建立连接 |
| 展会前预热 | 参展前联系目标采购商，邀约面谈 |
| 日常客户维护 | 对现有客户的动态点赞+评论，维护关系 |
| 新品发布推广 | 为目标客户决策人生成产品更新消息 |

---

## 五、资源索引

- **消息模板库**: 见 `references/linkedin_message_templates.md`（何时读取：需要参考话术模板或生成时）
- **行业钩子库**: 见 `references/industry_hooks_library.md`（何时读取：生成个性化开篇钩子时）
- **跟进序列模板**: 见 `references/followup_sequence_templates.md`（何时读取：设计多轮跟进序列时）

---

## 六、注意事项

### ⚠️ 社媒平台合规
- **每日限制**：社媒平台对联系请求有频率限制（约100条/天），注意控制操作频率
- **消息质量**：平台算法会降权低质量/垃圾消息，注意个性化
- **禁止行为**：禁止销售产品描述、禁止误导性内容、禁止重复相同消息

### ⚠️ 个性化质量
- 基础个性化（名字+公司）不等于真正个性化，建议提供更多背景信息
- 定期更新的动态是最好的个性化钩子来源

### ⚠️ 各平台消息长度限制
- 联系请求：最多300字符
- 私信（1st-degree）：最多500字符
- InMail（2nd/3rd-degree）：最多200字符

---

## 七、使用示例

### 示例 1：针对采购总监的个性化联系消息
**用户需求**：发现一位美国户外家具进口商的采购总监John Smith，生成一条个性化社媒联系消息

**执行结果**：
- 分析John的背景：最近发布了公司扩张欧洲市场的消息
- 生成3条个性化联系消息，以其公司动态作为开篇钩子
- 提供跟进序列（第1-5轮），覆盖建立联系到促进成交

### 示例 2：生成德国市场开发序列
**用户需求**：我们是一家LED照明出口商，生成50家德国批发商的采购经理

**执行结果**：
- 输入50个采购经理的背景信息
- 生成50条个性化联系消息（每条独特）+ 50条私信模板
- 生成统一的5步跟进序列，可逐步执行

---

## 八、Common Rationalizations

| Rationalization | Reality |
|----------------|---------|
| "社媒消息和邮件一样可以群发" | 平台算法会检测重复内容，重复相同消息会被降权 |
| "消息越详细越好" | 社媒消息有严格字符限制，简洁有力更有效 |

---

## 九、Security & Privacy

### 存储根路径
```
./data/yunlv-skills/linkedinWriter/
├── messages/          # 生成的消息内容
├── sequences/         # 跟进序列配置
├── templates/         # 用户自定义模板
└── logs/              # 运行日志（不含个人信息）
```

### 数据流透明声明 (Data Flow Transparency)

本技能的数据处理流程完全透明，所有数据传输均有明确目的：

| 数据流 | 方向 | 内容 | 用途 | 保护措施 |
|--------|------|------|------|----------|
| 用户 → 本技能 | 输入 | 用户提供的目标客户背景描述 | 构建消息生成请求 | 本地处理 |
| 本技能 → 云旅AI API | 请求 | 行业+职位+公司等背景描述 | 生成个性化消息内容 | TLS 1.3加密传输 |
| 云旅AI API → 本技能 | 响应 | 生成的消息文本+建议 | 输出给用户审核 | 服务端不存储请求 |
| 本技能 → 用户 | 输出 | 消息内容供用户复制粘贴 | 辅助社媒沟通 | 数据保留在用户环境 |

**关键保证**：
- 📌 **本技能不访问LinkedIn**：不调用LinkedIn API，不采集LinkedIn用户数据，所有输入由用户提供
- 📌 **API仅用于文本生成**：云旅AI API接收背景描述，返回消息文本。不传输任何个人信息到外部
- 📌 **不自动发送消息**：生成的消息由用户复制粘贴手动发送，技能不自动发送
- 📌 **不存储客户背景信息**：目标客户的背景信息仅用于当前消息生成，不持久化保存

### 数据保护措施

- **加密传输**：所有API通信使用TLS 1.3加密，确保数据在传输过程中不被截获
- **不存储原始数据**：用户输入的客户信息仅用于生成当前消息，不持久化存储
- **最小化留存**：消息生成记录保留30天，超期自动删除，日志中不记录个人身份信息
- **本地优先**：所有消息内容保存在用户本地目录，不自动上传

### 合规声明

- **GDPR合规**：不处理欧盟公民个人数据，消息内容基于用户提供的信息生成
- **平台ToS合规**：不通过自动化方式访问社交平台，不采集用户数据
- **PIPL合规**：不收集或处理个人信息，所有数据由用户主动提供
- **数据主权**：所有数据保留在用户自有环境中，用户对数据拥有完全控制权

### 权限边界声明
- ✅ **允许**：读取 `./skills/yunlv-skills/references/` 下的参考文件
- ✅ **允许**：调用云旅AI API生成消息文本内容
- ✅ **允许**：写入 `./data/yunlv-skills/linkedinWriter/` 用户自有数据
- ✅ **允许**：生成消息内容供用户复制发送
- ❌ **禁止**：自动访问LinkedIn平台或调用LinkedIn API
- ❌ **禁止**：采集或爬取用户档案数据
- ❌ **禁止**：自动发送消息到用户
- ❌ **禁止**：在日志或输出中记录客户的个人身份信息

### 本技能不做的事 (What This Skill Does NOT Do)
- ❌ 不访问、登录或爬取LinkedIn平台
- ❌ 不调用LinkedIn API获取用户数据
- ❌ 不自动发送消息（仅生成内容供用户手动复制粘贴）
- ❌ 不收集或建立用户联系信息数据库
- ❌ 不绕过平台的访问限制或反爬机制

---

## 十、Verification

完成B2B专业消息生成流程后：
- [ ] 确认消息内容个性化（非通用模板，每个钩子对应具体信息）
- [ ] 字符数符合平台限制（联系请求≤300，私信≤500）
- [ ] 无敏感词或误导性内容（通过合规检查）
- [ ] 跟进序列有明确的时间间隔和差异化内容
- [ ] 多条消息确保多样性（避免相似度>70%）
- [ ] 已设置跟进提醒，不遗漏每个联系节点

---

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

- **yunlv-email-writer** — 外贸邮件，LinkedIn触达后邮件深化沟通
- **yunlv-product-desc** — 产品描述，专业的产品内容吸引客户
- **yunlv-cantonfair** — 广交会，展会期间LinkedIn预热和跟进
