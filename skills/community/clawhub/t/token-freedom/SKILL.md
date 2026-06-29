---
name: token-freedom
description: AI API 平台推荐与 Token 自由助手。帮助用户找到最便宜/免费/最适合的 AI API 平台，注册获取免费额度，配置到 QClaw 等客户端使用。支持比价、推荐、注册引导。当用户说"API太贵了"、"token用完了"、"哪里可以免费调用AI"、"帮我注册API"、"换个便宜的模型"、"接入自己的Key"、"API比价"、"哪个平台送得多"时触发。覆盖硅基流动/火山引擎/DeepSeek/智谱/OpenRouter/Groq/Sophnet/阿里云百炼/小米MiMo/腾讯混元/Anthropic/OpenAI/Google Gemini/MiniMax/Moonshot 等 16+ 平台。
---

# Token 自由助手

## ⚙️ 联盟配置

推广链接支持自定义。数据来源优先级：
1. `~/.qclaw/affiliate-config.json`（你的个人配置）
2. `references/default_config.json`（Skill 默认值）

运行 `python scripts/get_affiliate.py --all` 查看当前配置。
用自己的 ID：创建 `~/.qclaw/affiliate-config.json`，写入 `{"siliconflow": "你的码", "volcengine": "你的码"}`。

## Overview

帮用户摆脱 QClaw 积分/Token 焦虑，用「自己的 API Key + 最优平台」实现 AI 自由。核心价值：**比价 + 推荐 + 注册引导 + 配置教程**。

## Quick Start

用户说 "token 用完了" / "想用自己的 API" / "哪个平台便宜" 时：

1. **了解需求**：想用什么模型？预算？国内还是海外？
2. **运行推荐脚本**：`python scripts/recommend_api.py "<需求>"`
3. **引导注册**：给出推荐平台链接 + 注册步骤
4. **帮助配置**：告诉用户如何在 QClaw/客户端中配置

## 平台速查

| 平台 | 免费额度 | 推荐奖励 | 亮点 |
|------|---------|---------|------|
| **硅基流动** | 2000万Tokens | ✅ 双方各2000万 | DeepSeek满血版+200+模型 |
| 火山引擎 | ¥15代金券 | ✅ 双方各¥15 | 字节生态+豆包 |
| Sophnet 算力平台 | ¥20额度 | ✅ 双方各得Token | 国产TPU+126t/s+OpenClaw适配 |
| **智谱AI** | 2000万Tokens | ✅ 双方各2000万 | GLM-5旗舰+GLM-4.7-Flash免费 |
| DeepSeek 官方 | ¥10（1月有效） | ❌ | 官方最新模型 |
| OpenRouter | 部分模型免费 | ❌ | 250+模型聚合 |
| Groq | 大量免费 | ❌ | 全球最快推理 |
| ModelScope 魔搭 | 每日2000次 | ❌ | 阿里生态+Qwen全系 |
| 阿里云百炼 | 7000万Token/90天 | ❌ | 300+模型+低代码 |
| 小米 MiMo | 申请制亿级Token | ✅ ¥10体验金 | MIT开源+百亿补贴 |
| 腾讯混元 | 100万Token/1年 | ❌ | 自研混元+视频生成 |
| Anthropic Claude | 按量付费 | ❌ | Claude顶级推理+Claude Code |
| OpenAI | $5/3个月 | ❌ | GPT-5+o1+最成熟生态 |
| Google Gemini | 免费层+GCP$300 | ❌ | 最慷慨免费+2M上下文 |
| MiniMax (CN) | ¥15+Token Plan | ❌ | M3编程+海螺视频 |
| Moonshot Kimi (CN) | ¥15/100万tokens | ❌ | Kimi K2.6 MIT开源 |

## Workflow

### 1. 比价推荐（用户不确定用哪个平台）

```
User: "我想用DeepSeek R1，哪个平台最划算"
User: "有没有免费的AI API"
User: "国内哪个平台送得多"
```

**步骤**：
1. 运行 `python scripts/recommend_api.py "<需求关键词>"`
2. 或直接读取 `references/platforms.json` 进行人工比价
3. 展示 2-3 个平台对比：价格、免费额度、推荐奖励
4. ⚠️ **获得用户同意后**才推送邀请链接

### 2. 注册引导（用户确定用哪个平台）

```
User: "帮我注册硅基流动"
User: "怎么注册DeepSeek API"
```

**步骤**：
1. 先告知用户该平台是否有邀请奖励及其内容
2. ⚠️ **征得用户同意**后再推送邀请链接
3. 读取 `references/setup-guide.md` 获取该平台的详细注册步骤
4. 分步引导：
   - 第1步：访问注册链接
   - 第2步：手机号/邮箱注册
   - 第3步：创建 API Key（强调立刻复制保存）
   - 第4步：充值（可选）
5. 提醒安全注意事项：API Key 不要泄露、设置消费上限

### 3. 配置到 QClaw

```
User: "怎么把API Key配到QClaw"
User: "接入自己的Key"
```

**步骤**：
1. 告诉用户 QClaw 中的配置位置：模型配置 → 自定义模型
2. 给出对应平台的 Base URL 和模型名（从 setup-guide.md 或 platforms.json 获取）
3. 格式：
   - Base URL: `https://api.xxx.com/v1`
   - API Key: `sk-xxxxxxxx`
   - 模型名: `model-name`
4. 提醒测试连接

### 4. Token 用完了怎么办

```
User: "token用完了"
User: "API额度不够了"
```

**策略**：
1. 推荐下一个有免费额度的平台（切换薅羊毛）
2. 推荐永久免费方案：智谱 GLM-4-Flash
3. 如果用户有硅基流动推荐官资格，鼓励邀请好友获取更多 Token
4. 组合方案：GLM-4-Flash（日常免费）+ 硅基流动（重度付费）= 最省钱

## 推荐策略

### 优先级规则

1. **透明告知**：展示平台时说明哪些有邀请奖励，用户注册后双方均获得免费额度（硅基流动/智谱各2000万Tokens，火山¥15）
2. **免费模型的强调**：智谱 GLM-4.7-Flash 免费调用作为兜底（API不列在模型列表，但直接调用可用）
3. **预算敏感**：先推荐免费 + 邀请奖励组合
4. **海外需求**：OpenRouter 或 Groq
5. **官方情结**：DeepSeek 官方

### 典型推荐组合

| 用户画像 | 推荐组合 |
|----------|---------|
| "我想省钱" | 智谱AI（邀请得2000万 + GLM-4.7-Flash免费）+ Google Gemini（免费层）+ 小米MiMo（申请亿万Token） |
| "我要最好用的模型" | Anthropic Claude（顶级推理）+ OpenAI GPT-5 |
| "我是开发者" | 硅基流动（200+模型）+ MiniMax M3（编程Agent）+ Moonshot Kimi（开源） |
| "我只要免费" | Google Gemini 免费层 + 智谱 GLM-4.7-Flash + Groq |
| "我需要国内合规" | 阿里云百炼 + 腾讯混元 + 火山引擎 |

## 重要规则

1. **告知邀请奖励**——展示平台时一并说明其邀请机制
2. **一次不要推太多**——2-3个平台即可，避免选择困难
3. **强调安全**——API Key 保管、消费限额设置
4. **数据驱动**——所有平台信息和价格来自 `references/platforms.json`，保持更新
