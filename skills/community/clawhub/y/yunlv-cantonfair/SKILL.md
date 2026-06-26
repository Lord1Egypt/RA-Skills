---
name: yunlv-cantonfair
description: >-
  Use when user needs to generate Canton Fair lead discovery strategies and outreach plans.
  Use when generating trade show customer development strategies.
  Use when creating personalized outreach content, product categories, booth information references.
  Use when user mentions "广交会", "展会获客策略", "摊位号", "展商开发", "展会客户开发策略", "采购商开发策略".
homepage: https://yunlvai.com
license: MIT-0
version: 1.0.7
progressive:
  layers:
    - name: metadata
      tokens: 200
      loaded: startup
      description: "技能基础配置、数据源说明、定价信息"
    - name: instructions
      tokens: 3000
      loaded: trigger
      description: "广交会获客策略生成全流程、过滤策略、输出格式"
    - name: resources
      tokens: variable
      loaded: on-demand
      description: "展商分类表、邮件模板、跟进策略"
  resource_paths:
    - references/canton_fair_categories.md
    - references/outreach_templates.md
    - references/followup_strategy.md
metadata:
  yunlv:
    homepage: https://yunlvai.com
    primaryEnv: TRADEGPT_API_KEY
    category: customer-development
    subCategory: trade-show-mining
    tags: ["广交会", "展会获客", "展商开发", "B2B外贸", "Canton Fair", "获客策略"]
    requires:
      env:
        - TRADEGPT_API_KEY
    apis:
      - name: 云旅AI MatchGPT API
        url: https://api.yunlvai.com
        purpose: "生成展会获客策略与个性化开发内容"
        auth: Bearer Token (TRADEGPT_API_KEY)
    emoji: "🏛️"
    author: "云旅AI团队"
    pricing:
      free:
        features: ["每期3次策略生成", "基础展商信息", "展品分类浏览"]
      basic:
        price: 299
        currency: CNY
        period: month
        features: ["每月100次策略生成", "展商联系信息整理", "邮件开发信生成", "WhatsApp消息内容模板"]
      pro:
        price: 999
        currency: CNY
        period: month
        features: ["无限策略生成", "决策人信息整理", "多期展会变化参考", "Priority邮件内容生成"]
triggers:
  - "广交会"
  - "展会获客策略"
  - "展商开发策略"
  - "采购商开发策略"
  - "展会信息参考"
  - "Canton Fair"
  - "参展商"
  - "展会数据"
  - "采购商名单"
  - "展品分类"
---

# 广交会获客顾问：AI驱动展会客户开发策略生成

> 广交会（中国进出口商品交易会）是全球最大综合性展会，每届汇聚超2万家参展商和20万采购商。云旅AI广交会获客顾问技能，帮助外贸企业辅助生成精准的展会客户开发策略，生成个性化开发信，实现展会价值最大化。

---

## 一、技能定位

**解决什么问题**：外贸企业参加/未参加广交会时，如何获取客户开发策略并高效联系？

**核心价值**：将展会信息转化为可执行获客策略的时间，从**3-5天**压缩到**10分钟**。

---

## 二、能做什么

### 【核心功能】

| 功能 | 说明 |
|------|------|
| 展商信息参考 | 按产品关键词、行业分类、采购商/参展商身份等多维度参考 |
| 客户匹配度评估建议 | MatchGPT评估客户与自身产品的匹配度（1-10分） |
| 联系信息结构化整理 | 整理企业名称、邮箱、电话、LinkedIn等联系信息 |
| 个性化开发信生成 | 基于展商信息辅助生成多语言开发信 |
| 多期展会变化参考 | 对比近3届展商变化，参考新增客户和流失客户 |
| 跟进建议配置 | 对高潜力客户生成跟进建议 |

### 【效果数据】

- 参考信息覆盖：每届广交会 25,000+ 参展商，50,000+ 采购商
- 匹配评估准确率：MatchGPT驱动，准确率 92%
- 开发信回复率：个性化生成 + 精准联系，回复率提升 3-5倍

---

## 三、操作步骤

### 第1步：描述获客需求

支持以下输入方式（任选其一）：

**方式A - 关键词需求描述（最常用）**
```
产品关键词：outdoor furniture, garden parasol
展会届数：第137届（2025年）
企业类型：采购商
```

**方式B - 行业分类参考**
```
行业分类：家居用品 > 家具 > 户外家具
目标国家：北美（美国、加拿大）
```

**方式C - 展商/采购商名称参考**
```
公司名称：IKEA
公司类型：采购商
参考维度：采购品类、来源国家、参展历史
```

### 第2步：AI策略生成与匹配

系统辅助执行：
1. **信息整合**：通过云旅AI MatchGPT API整合广交会展商信息
2. **联系信息结构化整理**：通过云旅AI MatchGPT API整理联系信息（匹配率约70%）
3. **匹配评分**：MatchGPT从产品匹配度、采购规模、地理分布、合作潜力4个维度评分
4. **智能过滤建议**：过滤已联系客户、关联公司、黑名单企业

### 第3步：输出获客策略报告

```json
{
  "query": "outdoor furniture",
  "fair_session": "137th",
  "total_found": 847,
  "filtered_leads": 156,
  "high_priority": 23,
  "results": [
    {
      "rank": 1,
      "company_name": "Patio Living Inc.",
      "country": "United States",
      "company_type": "Importer",
      "match_score": 9.2,
      "products_interest": ["outdoor dining sets", "garden umbrellas"],
      "estimated_annual_volume": "$5M-$10M",
      "contact_person": "John Smith",
      "contact_role": "Purchasing Director",
      "email": "j.smith@patioliving.com",
      "phone": "+1-555-0123",
      "linkedin": "linkedin.com/in/johnsmith-patio",
      "booth_number": "A区 8.1 K15",
      "attended_fairs": ["136th", "135th", "134th"],
      "recommendation": "🌟🌟🌟 重点开发：连续3届参展，采购量大，建议直接电话联系"
    }
  ]
}
```

### 第4步：生成开发信内容

选中目标客户后，系统辅助：
- 生成个性化开发信（英文/西班牙文/阿拉伯文等）
- 生成邮件或WhatsApp联系消息供用户复制发送
- 提示用户48小时后可二次跟进

---

## 四、适用场景

| 场景 | 使用方式 |
|------|----------|
| 展会前预热 | 参考目标采购商，生成邀约面谈消息 |
| 展会中快速识别 | 扫展时用摊位号快速参考公司背景 |
| 展会后跟进 | 将展会上收集的名片参考，快速建档 |
| 被动获客 | 从未参展但有采购记录的采购商中参考 |
| 新市场开拓 | 特定国家+特定品类的采购商定向参考 |

---

## 五、资源索引

- **广交会展品分类表**: 见 `references/canton_fair_categories.md`（何时读取：需要按行业分类精确参考时）
- **个性化开发信模板**: 见 `references/outreach_templates.md`（何时读取：生成联系邮件时）
- **展会客户跟进策略**: 见 `references/followup_strategy.md`（何时读取：制定展会后跟进计划时）

---

## 六、注意事项

### ⚠️ 参考信息时效性
- 广交会参考信息更新周期：每届展会结束后7天内更新
- 联系信息匹配率约 70%，建议配合LinkedIn二次验证

### ⚠️ 合规边界
- 建议单次个性化联系不超过 50 家客户
- 个性化邮件内容，非批量模板直发

### ⚠️ 评估参考性
- 匹配评分基于公开数据+AI推断，重要客户请人工核实

---

## 七、使用示例

### 示例 1：生成户外家具采购商开发策略
**用户需求**：我们是做户外家具的，生成第137届广交会上的北美采购商开发策略

**执行结果**：
- 参考到 847 家相关展商，过滤得 156 家目标客户
- 高优先级（评分≥8分）23 家，整理完整联系信息
- 生成英文开发信 23 封，WhatsApp消息内容模板首选

### 示例 2：展会现场快速参考
**用户需求**：展会现场遇到一家德国公司，摊位号 A12.1-25，快速了解这家公司

**执行结果**：
- 参考公司背景：年营业额、采购品类、供应商来源
- 判断匹配度：9.1分（高度匹配户外家具）
- 给出建议切入点：德国高端户外市场，我司价格有30%优势

---

## 八、Common Rationalizations

| Rationalization | Reality |
|----------------|---------|
| "广交会参考信息包含所有采购商联系方式" | 参考覆盖率约70%，需配合社媒二次验证 |
| "匹配评分高就一定能成交" | 评分仅供参考，最终转化依赖产品竞争力和跟进策略 |
| "展会后跟进效果不如展会前邀约" | 两者效果相当，关键在于是否在决策窗口期联系 |
| "批量群发开发信效率最高" | 个性化联系回复率是群发的3-5倍 |

---

## 九、Security & Privacy

### 存储根路径
```
./data/yunlv-skills/cantonFair/
├── queries/           # 策略生成记录（不含原始展商数据）
├── leads/             # 筛选后的客户名单
├── messages/          # 生成的消息内容
└── logs/              # 运行日志（不含联系方式）
```

### 数据流透明声明 (Data Flow Transparency)

本技能的数据处理流程完全透明，所有数据传输均有明确目的：

| 数据流 | 方向 | 内容 | 用途 | 保护措施 |
|--------|------|------|------|----------|
| 用户 → 本技能 | 输入 | 获客需求描述（产品关键词、行业分类） | 构建策略生成请求 | 本地处理 |
| 本技能 → 云旅AI API | 请求 | 产品关键词+筛选参数 | 获取获客策略建议 | TLS 1.3加密传输 |
| 云旅AI API → 本技能 | 响应 | 匹配评分+市场参考信息 | 生成客户名单 | 服务端不存储请求 |
| 本技能 → 用户 | 输出 | 格式化的获客策略+开发信内容 | 辅助展会获客 | 数据保留在用户环境 |

**关键保证**：
- 📌 **API仅用于内容生成**：云旅AI API接收策略生成需求，返回获客策略建议。联系方式等敏感信息不发送到外部
- 📌 **不传输个人隐私数据**：展商联系信息仅在用户本地展示，不转发到任何第三方服务
- 📌 **不建立联系人数据库**：本技能不收集、不聚合、不转售任何展商联系信息
- 📌 **消息内容用户可控**：生成的开发信由用户审核后手动发送，技能不自动发送任何消息

### 数据保护措施

- **加密传输**：所有API通信使用TLS 1.3加密，确保数据在传输过程中不被截获
- **不存储原始数据**：API返回的展商数据仅用于当前查询，不持久化存储在日志或缓存中
- **最小化留存**：查询记录保留30天，超期自动归档删除，日志中不记录联系方式
- **本地优先**：所有客户名单和开发信保存在用户本地目录，不自动上传

### 合规声明

- **GDPR合规**：展商信息来源于公开展会数据，使用时遵守GDPR第6条合法利益原则
- **CAN-SPAM合规**：生成的开发信包含退订选项，建议单次个性化联系
- **PIPL合规**：不收集中国公民个人信息用于非授权目的
- **数据主权**：所有数据保留在用户自有环境中，用户对数据拥有完全控制权

### 权限边界声明
- ✅ **允许**：读取 `./skills/yunlv-skills/references/` 下的参考文件
- ✅ **允许**：调用云旅AI API获取聚合后的获客策略建议
- ✅ **允许**：写入 `./data/yunlv-skills/cantonFair/` 用户自有数据
- ✅ **允许**：生成开发信内容供用户复制发送
- ❌ **禁止**：自动发送邮件或消息到展商邮箱
- ❌ **禁止**：将展商联系信息用于非授权营销或提供给第三方
- ❌ **禁止**：在日志或输出中记录展商的邮箱、电话等联系方式
- ❌ **禁止**：跨用户聚合展商数据进行转售

### 本技能不做的事 (What This Skill Does NOT Do)
- ❌ 不自动发送邮件或WhatsApp消息（仅生成内容供用户手动发送）
- ❌ 不爬取或采集广交会官网的非公开数据
- ❌ 不将展商联系信息转发到任何第三方服务
- ❌ 不建立跨用户的展商信息数据库
- ❌ 不绕过LinkedIn或展会平台的访问限制

---

## 十、Verification

完成广交会获客策略生成后：
- [ ] 确认获客需求描述清晰（关键词/分类/名称至少一项明确）
- [ ] 验证匹配评分逻辑（4个维度均有数据支撑）
- [ ] 确认联系信息有效性（邮箱格式正确、LinkedIn可访问）
- [ ] 开发信内容已去模板化（每封内容差异化≥30%）
- [ ] 联系策略符合GDPR/CAN-SPAM规范
- [ ] 高优先级客户已设置跟进提醒

---

## 十、Security & Privacy

### 存储根路径
```
./data/yunlv-skills/guangjiaoFAI/
├── queries/         # 策略生成历史记录
├── leads/           # 导出的客户名单
├── outreach/        # 生成的开发信记录
└── logs/            # 运行日志
```

### 数据处理原则
- **本地处理**：获客需求描述和中转数据仅在本地处理
- **敏感数据保护**：API密钥不写入日志
- **最小化留存**：联系完成后7天定期清理中间数据

### 权限边界声明
- ✅ **允许**：读取 `./skills/yunlv-skills/references/` 下的参考文件
- ✅ **允许**：调用云旅AI MatchGPT API 生成获客策略
- ✅ **允许**：写入 `./data/yunlv-skills/guangjiaoFAI/leads/` 导出名单
- ✅ **允许**：生成邮件和WhatsApp联系消息内容供用户复制发送
- ❌ **禁止**：查询第三方网站展商数据（仅使用授权数据源）
- ❌ **禁止**：将用户联系数据共享给第三方

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

- **yunlv-email-writer** — 外贸邮件，展会邀请函和展后跟进邮件
- **yunlv-product-desc** — 产品描述，展会展示的专业产品介绍
- **yunlv-pricing** — 定价策略，展会现场快速报价支持
