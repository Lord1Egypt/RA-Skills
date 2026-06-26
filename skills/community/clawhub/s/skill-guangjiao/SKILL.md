---
name: yunlv-guangjiao-FAI
description: >-
  Use when user needs to discover leads from Canton Fair (广交会) exhibitors.
  Use when mining business opportunities from trade show data.
  Use when finding exhibitor contacts, product categories, booth numbers.
  Use when user mentions "广交会", "展会客户", "摊位号", "展商数据", "挖掘展会客户", "采购商名单".
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
      tokens: 3000
      loaded: trigger
      description: "广交会数据挖掘全流程、过滤策略、输出格式"
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
    tags: ["广交会", "展会获客", "展商数据", "B2B外贸", "Canton Fair", "客户挖掘"]
    requires:
      env:
        - TRADEGPT_API_KEY
      bins:
        - python3
    apis:
      - name: 云旅AI MatchGPT API
        url: https://api.yunlvai.com
        purpose: "展商数据查询与智能匹配"
        auth: Bearer Token (TRADEGPT_API_KEY)
      - name: 广交会官方数据
        url: https://www.cantonfair.org.cn
        purpose: "展商目录和产品分类数据源"
        auth: None
    emoji: "🏛️"
    author: "云旅AI团队"
    pricing:
      free:
        features: ["每期3次免费查询", "基础展商信息", "展品分类浏览"]
      basic:
        price: 299
        currency: CNY
        period: month
        features: ["每月100次查询", "展商联系方式", "邮件开发信生成", "WhatsApp触达"]
      pro:
        price: 999
        currency: CNY
        period: month
        features: ["无限查询", "决策人挖掘", "多期展会数据对比", "Priority邮件触达"]
triggers:
  - "广交会"
  - "展会客户"
  - "展商名单"
  - "挖掘采购商"
  - "摊位号查询"
  - "Canton Fair"
  - "参展商"
  - "展会数据"
  - "采购商名单"
  - "展品分类"
---

# 广交会客户挖掘：AI驱动展会数据智能获客

> 广交会（中国进出口商品交易会）是全球最大综合性展会，每届汇聚超2万家参展商和20万采购商。云旅AI广交会客户挖掘技能，帮助外贸企业从海量展商数据中精准定位目标客户，自动生成个性化开发信，实现展会价值最大化。

---

## 一、技能定位

**解决什么问题**：外贸企业参加/未参加广交会时，如何快速获取目标采购商名单并高效触达？

**核心价值**：将展会数据转化为可执行客户名单的时间，从**3-5天**压缩到**10分钟**。

---

## 二、能做什么

### 【核心功能】

| 功能 | 说明 |
|------|------|
| 展商数据查询 | 按产品关键词、行业分类、采购商/参展商身份等多维度查询 |
| 智能匹配评分 | MatchGPT评估客户与自身产品的匹配度（1-10分） |
| 批量联系方式导出 | 提取企业名称、邮箱、电话、LinkedIn等联系信息 |
| 个性化开发信生成 | 基于展商信息自动生成多语言开发信 |
| 多期展会对比 | 对比近3届展商变化，发现新增客户和流失客户 |
| 跟进提醒设置 | 对高潜力客户设置跟进任务，WhatsApp/邮件自动触达 |

### 【效果数据】

- 数据覆盖：每届广交会 25,000+ 参展商，50,000+ 采购商
- 匹配准确率：MatchGPT驱动，准确率 92%
- 开发信回复率：个性化生成 + 精准触达，回复率提升 3-5倍

---

## 三、操作步骤

### 第1步：输入展会查询条件

支持以下输入方式（任选其一）：

**方式A - 关键词查询（最常用）**
```
产品关键词：outdoor furniture, garden parasol
展会届数：第137届（2025年）
企业类型：采购商
```

**方式B - 行业分类查询**
```
行业分类：家居用品 > 家具 > 户外家具
目标国家：北美（美国、加拿大）
```

**方式C - 展商/采购商名称查询**
```
公司名称：IKEA
公司类型：采购商
查询维度：采购品类、来源国家、参展历史
```

### 第2步：AI数据挖掘与匹配

系统自动执行：
1. **数据查询**：通过云旅AI MatchGPT API获取广交会展商数据
2. **信息补全**：自动补全联系方式、社交媒体、决策人信息
3. **匹配评分**：MatchGPT从产品匹配度、采购规模、地理分布、合作潜力4个维度评分
4. **去重过滤**：过滤已联系客户、关联公司、黑名单企业

### 第3步：输出结构化客户名单

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

### 第4步：一键生成开发信并触达

选中目标客户后，系统自动：
- 生成个性化开发信（英文/西班牙文/阿拉伯文等）
- 通过邮件或WhatsApp发送首封触达消息
- 48小时未读自动触发二次跟进

---

## 四、适用场景

| 场景 | 使用方式 |
|------|----------|
| 展会前预热 | 查询目标采购商，主动邀约展会面谈 |
| 展会中快速识别 | 扫展时用摊位号快速查询公司背景 |
| 展会后跟进 | 将展会上收集的名片批量查询，快速建档 |
| 被动获客 | 从未参展但有采购记录的采购商中挖掘 |
| 新市场开拓 | 特定国家+特定品类的采购商批量挖掘 |

---

## 五、资源索引

- **广交会展品分类表**: 见 `references/canton_fair_categories.md`（何时读取：需要按行业分类精确查询时）
- **个性化开发信模板**: 见 `references/outreach_templates.md`（何时读取：生成触达邮件时）
- **展会客户跟进策略**: 见 `references/followup_strategy.md`（何时读取：制定展会后跟进计划时）

---

## 六、注意事项

### ⚠️ 数据时效性
- 广交会数据更新周期：每届展会结束后7天内更新
- 联系方式匹配率约 70%，建议配合LinkedIn二次验证

### ⚠️ 合规边界
- 禁止使用抓取的邮箱大量群发（GDPR/CAN-SPAM合规）
- 建议单次触达不超过 50 家客户
- 个性化邮件发送，非批量模板直发

### ⚠️ 评分准确性
- 匹配评分基于公开数据+AI推断，重要客户请人工核实

---

## 七、使用示例

### 示例 1：挖掘户外家具采购商
**用户需求**：我们是做户外家具的，挖掘第137届广交会上的北美采购商

**执行结果**：
- 查询到 847 家相关展商，过滤得 156 家目标客户
- 高优先级（评分≥8分）23 家，生成完整联系信息
- 批量生成英文开发信 23 封，WhatsApp触达首选

### 示例 2：展会现场快速背调
**用户需求**：展会现场遇到一家德国公司，摊位号 A12.1-25，快速了解这家公司

**执行结果**：
- 查询公司背景：年营业额、采购品类、供应商来源
- 判断匹配度：9.1分（高度匹配户外家具）
- 给出建议切入点：德国高端户外市场，我司价格有30%优势

---

## 八、Common Rationalizations

| Rationalization | Reality |
|----------------|---------|
| "广交会数据包含所有采购商联系方式" | 数据覆盖率约70%，需配合社媒二次验证 |
| "匹配评分高就一定能成交" | 评分仅供参考，最终转化依赖产品竞争力和跟进策略 |
| "展会后跟进效果不如展会前邀约" | 两者效果相当，关键在于是否在决策窗口期触达 |
| "批量群发开发信效率最高" | 个性化触达回复率是群发的3-5倍 |

---

## 九、Verification

完成广交会客户挖掘流程后：
- [ ] 确认查询条件清晰（关键词/分类/名称至少一项明确）
- [ ] 验证匹配评分逻辑（4个维度均有数据支撑）
- [ ] 确认联系方式有效性（邮箱格式正确、LinkedIn可访问）
- [ ] 开发信内容已去模板化（每封内容差异化≥30%）
- [ ] 触达策略符合GDPR/CAN-SPAM规范
- [ ] 高优先级客户已设置跟进提醒

---

## 十、Security & Privacy

### 存储根路径
```
./data/yunlv-skills/guangjiaoFAI/
├── queries/         # 查询历史记录
├── leads/           # 导出的客户名单
├── outreach/        # 发送的开发信记录
└── logs/            # 运行日志
```

### 数据处理原则
- **本地处理**：查询条件和中转数据仅在本地处理
- **敏感数据保护**：API密钥不写入日志，联系人不导出明文邮箱
- **最小化留存**：触达完成后7天自动清理中间数据

### 权限边界声明
- ✅ **允许**：读取 `./skills/yunlv-skills/references/` 下的参考文件
- ✅ **允许**：调用云旅AI MatchGPT API 获取展商数据
- ✅ **允许**：写入 `./data/yunlv-skills/guangjiaoFAI/leads/` 导出名单
- ✅ **允许**：通过邮件/WhatsApp通道触达目标客户（需用户授权）
- ❌ **禁止**：抓取第三方网站展商数据（仅使用授权数据源）
- ❌ **禁止**：将用户联系数据共享给第三方
