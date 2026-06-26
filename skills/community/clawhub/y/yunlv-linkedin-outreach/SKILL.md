---
name: yunlv-linkedin-outreach
description: >-
  Use when user needs to generate personalized LinkedIn connection requests or outreach messages.
  Use when assisting LinkedIn lead generation and engagement.
  Use when writing professional B2B messages for LinkedIn prospects.
  Use when user mentions "LinkedIn开发信", "领英联系", "LinkedIn消息", "社交获客", "连接请求", "领英营销".
homepage: https://yunlvai.com
license: MIT-0
version: 1.0.0
progressive:
  layers:
    - name: metadata
      tokens: 200
      loaded: startup
      description: "技能基础配置、渠道说明、定价信息"
    - name: instructions
      tokens: 3500
      loaded: trigger
      description: "LinkedIn消息生成全流程、个性化策略、跟进序列设计"
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
    subCategory: linkedin-outreach
    tags: ["LinkedIn", "领英获客", "社交营销", "B2B开发", "连接请求", "社媒联系"]
    requires:
      env:
        - TRADEGPT_API_KEY
        - LINKEDIN_SESSION_TOKEN  # 可选
    apis:
      - name: 云旅AI MatchGPT API
        url: https://api.yunlvai.com
        purpose: "LinkedIn消息内容生成与优化"
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
        features: ["批量消息生成", "高级序列设计", "A/B测试优化", "回复分析"]
triggers:
  - "LinkedIn"
  - "领英"
  - "连接请求"
  - "LinkedIn消息"
  - "领英营销"
  - "社媒开发"
  - "社交获客"
  - "B2B社交"
  - "LinkedIn outreach"
---

# LinkedIn开发信生成：社媒场景个性化联系

> LinkedIn是全球最大的B2B社交平台，汇聚超9亿职业人士，是外贸企业开发决策人的黄金渠道。云旅AI LinkedIn开发信生成技能，基于MatchGPT驱动的个性化引擎，帮助外贸人快速生成高回复率的LinkedIn消息，辅助设计跟进序列，让社交获客效率提升10倍。

---

## 一、技能定位

**解决什么问题**：LinkedIn开发信不知道写什么、回复率低、跟进混乱？

**核心价值**：从"手写每封消息"升级到"AI批量生成个性化消息"，单个开发消息准备时间从 **15分钟** 压缩到 **30秒**。

---

## 二、能做什么

### 【核心功能】

| 功能 | 说明 |
|------|------|
| 个性化消息生成 | 基于目标客户的LinkedIn档案、公司动态、行业背景生成定制消息 |
| 多语言支持 | 英文、西班牙文、德文、法文、阿拉伯文、日文等15种语言 |
| 连接请求优化 | 300字符以内的连接请求话术优化，提升通过率 |
| 跟进序列设计 | 辅助生成3-5步跟进序列，覆盖首次联系到成交前所有节点 |
| 行业钩子库 | 内置50+行业痛点钩子（"I noticed..."类型） |
| 消息A/B测试 | 辅助生成2-3个版本消息供测试选择 |
| 语气风格选择 | 专业正式/轻松友好/数据驱动/关系导向四种风格 |

### 【效果数据】

- LinkedIn连接通过率：个性化消息 vs 模板消息，**38% vs 12%**
- 消息回复率：专业定制消息平均回复率 **25-35%**
- 支持语言：15种主流外贸语言

---

## 三、操作步骤

### 第1步：输入目标客户信息

**方式A - LinkedIn URL直接导入**
```
LinkedIn档案：https://www.linkedin.com/in/johnsmith-patio
目标产品：outdoor furniture
联系目的：建立联系 → 发送产品资料
消息语言：English
```

**方式B - 关键词描述（无需LinkedIn URL）**
```
目标客户画像：
- 职位：Purchasing Manager / VP of Procurement
- 公司类型：Outdoor furniture importer
- 所在地区：United States, East Coast
- 公司规模：50-200人
- LinkedIn活跃度：每周发帖
目标产品：rattan outdoor dining sets
我的差异化： factory direct pricing, 15 years experience
消息风格：专业友好
```

**方式C - 批量客户导入**
```
批量上传CSV格式：
name, title, company, linkedin_url, product_interest, notes
John Smith, Purchasing Director, Patio Living Inc., https://..., outdoor furniture, met at Canton Fair 137th
```

### 第2步：AI分析与消息生成

系统辅助执行：
1. **档案解析**：读取LinkedIn公开信息（职位、公司、行业、帖子、互动）
2. **个性化元素提取**：识别共同话题、行业痛点、公司动态作为钩子
3. **消息生成**：MatchGPT基于钩子库生成个性化消息（3个版本供选）
4. **合规检查**：检查字符数限制（连接请求300字符、私信500字符）、敏感词过滤
5. **序列设计**：生成从首次联系到第5次跟进的完整序列

### 第3步：输出消息内容

**连接请求消息示例：**
```
Hi John,

Congrats on Patio Living's expansion into the European market — I saw the news on LinkedIn last month.

I'm Alex from [Company], a specialist in outdoor furniture manufacturing with 15+ years serving North American brands. We've helped companies like yours reduce procurement costs by 20-30%.

Would love to share how we can support your growth plans. Open to a quick chat?

Best,
Alex
```
> 字符数：297 ✅（符合LinkedIn限制）

**跟进序列示例（第1-5轮）：**
| 步骤 | 时间 | 消息类型 | 目的 |
|------|------|----------|------|
| 第1轮 | Day 0 | 连接请求 | 建立关系 |
| 第2轮 | Day 3 | 私信（连接通过后）| 价值传递 |
| 第3轮 | Day 7 | 产品案例分享 | 激发兴趣 |
| 第4轮 | Day 14 | 行业报告/数据 | 制造紧迫感 |
| 第5轮 | Day 28 | 限时优惠/Offer | 促进行动 |

### 第4步：手动发送

- **手动发送**：复制消息内容，粘贴到LinkedIn发送
- **复制粘贴发送**：用户复制生成内容到LinkedIn发送

---

## 四、适用场景

| 场景 | 使用方式 |
|------|----------|
| 广交会后跟进 | 展会上收集的名片，批量生成LinkedIn连接请求 |
| 海关数据客户联系 | 从CUSTOMS_SCOUT导出的采购商，找到LinkedIn决策人 |
| 竞品客户联系 | 锁定竞争对手的LinkedIn公司员工，主动连接 |
| 展会前预热 | 参展前在LinkedIn上联系目标采购商，邀约面谈 |
| 日常客户维护 | 对现有客户的LinkedIn动态点赞+评论，维护关系 |
| 新品发布推广 | 向目标客户的决策人发送产品更新通知 |

---

## 五、资源索引

- **LinkedIn消息模板库**: 见 `references/linkedin_message_templates.md`（何时读取：需要参考话术模板或批量生成时）
- **行业钩子库**: 见 `references/industry_hooks_library.md`（何时读取：生成个性化开篇钩子时）
- **跟进序列模板**: 见 `references/followup_sequence_templates.md`（何时读取：设计多轮跟进序列时）

---

## 六、注意事项

### ⚠️ LinkedIn政策合规
- **每日限制**：LinkedIn对连接请求有每日上限（约100条/天），注意控制发送频率
- **消息质量**：LinkedIn算法会降权低质量/垃圾消息，注意个性化
- **禁止行为**：禁止销售产品描述、禁止误导性内容、禁止批量相同消息

### ⚠️ 个性化质量
- 基础个性化（名字+公司）不等于真正个性化，建议提供更多背景信息
- 每周更新的LinkedIn帖子/动态是最好的个性化钩子来源

### ⚠️ 消息长度
- 连接请求：最多300字符
- 私信（1st-degree）：最多500字符
- InMail（2nd/3rd-degree）：最多200字符

---

## 七、使用示例

### 示例 1：针对采购总监的个性化连接请求
**用户需求**：发现一位美国户外家具进口商的采购总监John Smith，生成一条个性化LinkedIn连接请求

**执行结果**：
- 分析John的LinkedIn档案：最近发布了公司扩张欧洲市场的消息
- 生成3条个性化连接请求，以其公司动态作为开篇钩子
- 提供跟进序列（第1-5轮），覆盖建立联系到促进成交

### 示例 2：批量生成德国市场开发序列
**用户需求**：我们是一家LED照明出口商，批量生成50家德国批发商的采购经理

**执行结果**：
- 输入50个采购经理的LinkedIn档案URL
- 批量生成50条个性化连接请求（每条独特）+ 50条私信模板
- 生成统一的5步跟进序列，可批量执行

---

## 八、Common Rationalizations

| Rationalization | Reality |
|----------------|---------|
| "LinkedIn消息和邮件一样可以批量群发" | LinkedIn算法会检测重复内容，批量相同消息会被降权 |
| "消息越详细越好" | LinkedIn消息有严格字符限制，简洁有力更有效 |
| "一次联系就够了" | B2B销售平均需要5-8次联系才会回复，不要放弃跟进 |
| "LinkedIn只能用来连接" | LinkedIn也是内容营销和品牌建设的平台 |

---

## 九、Verification

完成LinkedIn开发信生成流程后：
- [ ] 确认消息内容个性化（非通用模板，每个钩子对应具体信息）
- [ ] 字符数符合LinkedIn限制（连接请求≤300，私信≤500）
- [ ] 无敏感词或误导性内容（通过合规检查）
- [ ] 跟进序列有明确的时间间隔和差异化内容
- [ ] 批量发送时确保消息多样性（避免相似度>70%）
- [ ] 已设置跟进提醒，不遗漏每个联系节点

---

## 十、Security & Privacy

### 存储根路径
```
./data/yunlv-skills/linkedinOutreach/
├── profiles/          # 导入的目标客户LinkedIn档案
├── messages/          # 生成的消息内容
├── sequences/          # 跟进序列配置
├── sent/              # 已发送记录
└── logs/               # 运行日志
```

### 数据处理原则
- **LinkedIn数据使用**：仅使用用户主动提供的LinkedIn档案信息，不主动采集
- **消息内容保护**：生成的消息内容不存储在第三方服务器
- **用户自配置**：LinkedIn消息发送需用户自行操作或配置第三方工具

### 权限边界声明
- ✅ **允许**：读取 `./skills/yunlv-skills/references/` 下的参考文件
- ✅ **允许**：调用云旅AI MatchGPT API生成消息内容
- ✅ **允许**：写入 `./data/yunlv-skills/linkedinOutreach/` 消息记录
- ✅ **允许**：生成LinkedIn消息内容供用户复制发送
- ❌ **禁止**：未经授权获取LinkedIn搜索结果（仅处理用户主动提供的档案）
- ❌ **禁止**：将用户LinkedIn联系数据共享给第三方
