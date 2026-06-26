---
name: Vane Marketing - 品牌热点营销助手
slug: vane-marketing-content
version: 1.0.0
description: AI 智能品牌营销工具：输入品牌名称，自动采集全网数据、分析当日热点、生成小红书图文内容
author: 风向标
tags: [marketing, xiaohongshu, content-generation, brand-analysis, hot-topics]
requires:
  - capability: http
---

## 📋 隐私与透明度

**服务提供商**: Vane Marketing Platform
**计费平台**: 智灵 Skill 平台 (https://skills.zeelin.cn)
**数据处理**:
- 用户提交的品牌名称将用于采集全网公开数据
- 系统自动获取当日热点信息并进行匹配分析
- 生成的小红书图文内容基于 AI 分析结果

**数据保留**:
- 品牌分析数据保留 24 小时用于优化
- 请求日志保留 7 天用于故障排查
- 生成的内容不会被二次使用或分享

---

## 使用时机

当用户请求：
- 为品牌生成小红书内容
- 分析品牌与热点的结合
- 创作品牌营销文案
- 追热点营销内容
- 小红书图文创作

不适合：生成音乐、视频、代码开发等。

---

## ⚡ 计费规则

- 每次成功生成内容消耗 **100 额度**
- 品牌数据采集和热点分析包含在内
- 生成失败**不扣费**
- 用户需自行在 https://skills.zeelin.cn 注册账号并充值获取 App-Key

---

## 🔑 第一步（强制）：获取并验证用户 App-Key

**⚠️ 必须在任何创作操作之前完成此步骤，不得跳过！**

### 1-A. 检查是否已有 App-Key

Agent 应先询问用户是否已配置智灵 App-Key：

> 📊 **开始品牌分析前，我需要验证你的智灵账户额度。**
>
> 请提供你的智灵 App-Key（前往 https://skills.zeelin.cn 注册并创建应用获取）。
>
> 📌 每次生成内容消耗 **100 额度**。

### 1-B. 调用额度校验接口

使用用户提供的 App-Key 调用校验接口：

```
POST https://skills.zeelin.cn/v2/api/skill/detail
Header: app-key: <用户的 zeelin_app_key>
Header: Content-Type: application/json
Body:
{
  "query": "品牌营销内容生成: <品牌名称>",
  "skill-id": "zeelin_VaneMarketing_xxxxx"
}
```

### 1-C. 处理校验结果

**成功（code: 200）：**
```json
{
  "code": 200,
  "data": {
    "pre_order_id": "2026038787913be67748...",
    "remain_calls": 1000,
    "skill_id": "zeelin_VaneMarketing_xxxxx"
  }
}
```
→ 保存 `pre_order_id`（2小时内有效），告知用户余额并继续：
> ✅ 验证通过！当前余额 **1000 额度**，可生成 10 次内容。开始分析！

**余额不足（code: 402 或 remain_calls < 100）：**
→ 停止，提示用户充值：
> ❌ 你的智灵账户余额不足（当前剩余 XX 额度，生成一次需要 100 额度）。
> 请前往 https://skills.zeelin.cn 充值后再试。

**Key 不存在/无效（code: 404）：**
> ❌ App-Key 无效，请检查是否正确复制。前往 https://skills.zeelin.cn/console/apps 查看你的 Key。

---

## 📊 第二步：生成品牌营销内容

**基础 URL**: `http://127.0.0.1:8000` (生产环境请替换为实际域名)

**POST** `/gateway/vane_marketing/content`

### 请求示例

```bash
curl --location --request POST 'http://127.0.0.1:8000/gateway/vane_marketing/content' \
--header 'App-Key: S6YVomNq2PYl4bnjGYXDeaM1J9jhojwv' \
--header 'Content-Type: application/json' \
--data-raw '{
    "brand_name": "华为"
}'
```

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| brand_name | string | 是 | 品牌名称，如"华为"、"小米"等 |

### 响应示例

**成功返回：**
```json
{
  "success": true,
  "data": {
    "brand_info": {
      "name": "华为",
      "industry": "科技/通信",
      "keywords": ["5G", "手机", "科技创新"]
    },
    "hot_topics": [
      {
        "topic": "AI手机新趋势",
        "heat_score": 95,
        "match_score": 88
      }
    ],
    "xiaohongshu_content": {
      "title": "华为AI手机来了！这才是未来该有的样子✨",
      "content": "姐妹们！今天必须来分享...",
      "images": [
        "https://example.com/image1.jpg"
      ],
      "tags": ["华为", "AI手机", "科技好物"]
    }
  },
  "cost_balance": 100,
  "remain_calls": 900
}
```

**失败返回：**
```json
{
  "success": false,
  "error": "品牌信息采集失败",
  "code": "DATA_COLLECTION_ERROR"
}
```

---

## 📱 第三步：发布到小红书（可选）

⚠️ **重要警告**：

> **小红书平台禁止使用代理工具自动发布内容！**
>
> 使用自动发布功能可能导致：
> - 账号被限流或封禁
> - 内容被删除
> - 违反平台规则
>
> **强烈建议**：将生成的内容复制后，手动登录小红书 App 进行发布。

如用户坚持使用自动发布，需明确告知风险并获得确认后，可调用小红书发布 Skill（另一个独立 Skill，需单独配置）。

---

## 💡 使用流程

1. **验证 App-Key** → 确认余额充足
2. **输入品牌名称** → 系统自动采集数据
3. **AI 分析匹配** → 找到最佳热点结合点
4. **生成图文内容** → 小红书风格的标题、正文、标签
5. **手动发布** → 复制内容到小红书 App（推荐）

---

## 📢 完整对话示例

### 示例一：首次使用

**用户**："帮我为华为品牌生成小红书内容"

**Agent**：
> 📊 开始品牌分析前，我需要验证你的智灵账户额度。
>
> 请提供你的智灵 App-Key（前往 https://skills.zeelin.cn 注册获取）。每次生成消耗 100 额度。

**用户**："我的 key 是 S6YVomNq2PYl..."

**Agent**：（调用校验接口）
> ✅ 验证通过！当前余额 1000 额度，可生成 10 次内容。
>
> 正在为"华为"品牌采集数据和分析热点...

（调用内容生成接口）

> ✅ 已生成小红书图文内容：
>
> **标题**：华为AI手机来了！这才是未来该有的样子✨
>
> **正文**：（展示生成的内容）
>
> **标签**：#华为 #AI手机 #科技好物
>
> 💰 本次消耗 100 额度，剩余 900 额度
>
> ⚠️ **发布提醒**：小红书禁止代理发布，建议复制内容后手动发布到小红书 App，避免账号风险。

---

### 示例二：已有 Key 的用户

**用户**："key: xxx，帮我做小米的营销内容"

**Agent**：（直接验证并生成）
> ✅ 余额充足（1000 额度）。正在为"小米"生成内容...
>
> （展示生成结果）
>
> 💰 消耗 100 额度，剩余 900 额度
>
> 建议手动发布到小红书，避免封号风险。

---

## ⚠️ 错误处理

| 错误码 | 原因 | 处理方式 |
|--------|------|----------|
| 402 | 余额不足 | 提示用户充值 https://skills.zeelin.cn |
| 404 | App-Key 不存在 | 提示用户检查 Key |
| 401 | 未传 App-Key | 要求用户提供 Key |
| 429 | 请求频率过高 | 等待 60 秒后重试 |
| DATA_COLLECTION_ERROR | 品牌数据采集失败 | 检查品牌名称是否正确，稍后重试 |
| HOT_TOPIC_ERROR | 热点获取失败 | 系统繁忙，稍后重试 |
| CONTENT_GENERATION_ERROR | 内容生成失败 | 重新发起请求，失败不扣费 |

---

## 🔧 技术说明

### 工作流程

1. **品牌数据采集**：从全网公开数据源采集品牌相关信息
2. **热点分析**：获取当日热门话题并计算热度值
3. **智能匹配**：AI 分析品牌与热点的契合度
4. **内容生成**：基于小红书平台特点生成图文内容
5. **余额扣费**：成功生成后自动扣除 100 额度

### API 限制

- 请求频率：每分钟最多 10 次
- 超时时间：60 秒
- 品牌名称长度：1-50 字符

---

## 支持与反馈

- **智灵平台**：https://skills.zeelin.cn
- **问题反馈**：通过智灵平台工单系统联系
- **使用建议**：遵守小红书平台规则，手动发布内容