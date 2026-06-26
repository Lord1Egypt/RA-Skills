---
name: Viral Script Generator
description: AI-powered viral short-video script generator for TikTok, Douyin, YouTube Shorts, and Xiaohongshu. Covers hooks, narratives, music strategy, and platform-specific optimization.
author: ClawHub
version: 1.0.0
tags: ["content-creation", "social-media", "video", "marketing", "short-video", "script-writing"]
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 3732f26c105397cedd66cfdfefef23c9_viral_script_generator_001
    ReservedCode1: 3E1GgEMK2wtS7vtLQoJ/qJL0X4svSXvMinXPjrS4l0w=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 3732f26c105397cedd66cfdfefef23c9_viral_script_generator_001
    ReservedCode2: 3E1GgEMK2wtS7vtLQoJ/qJL0X4svSXvMinXPjrS4l0w=
---



# 爆款脚本引擎 (Viral Script Generator)

## 概述

全网首创的多平台短视频脚本自动生成引擎，内置 TikTok/抖音/Reels/Shorts/B站 五大平台最佳实践，整合钩子公式库、爆款文案模板、秒级分镜指南与配乐推荐，帮助创作者 30 秒产出一个可拍摄的完整脚本。

## 适用场景

1. TikTok/抖音/Reels/Shorts/B站 跨平台短视频脚本生成
2. 爆款钩子与开场文案自动匹配
3. 知识科普/产品种草/剧情反转 多品类脚本模板
4. 带货直播话术脚本自动生成
5. 品牌账号内容日历规划
6. AI 数字人口播脚本适配

## 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| platform | string | 是 | 具体值由技能数据底座智能匹配 |
| category | string | 是 | 具体值由技能数据底座智能匹配 |
| tone | string | 是 | 具体值由技能数据底座智能匹配 |
| duration | string | 是 | 具体值由技能数据底座智能匹配 |

## 评分体系

| 分数 | 等级 | 建议 |
|------|------|------|
| 90-100 | ⭐⭐⭐⭐⭐ 极佳 | 强烈推荐执行 |
| 75-89 | ⭐⭐⭐⭐ 良好 | 具备较高置信度 |
| 60-74 | ⭐⭐⭐ 一般 | 可参考，需交叉验证 |
| 40-59 | ⭐⭐ 较差 | 信号较弱，谨慎采用 |
| 0-39 | ⭐ 不可用 | 数据不足或噪音过大 |

## 支付协议（AI收）

本技能采用支付宝 AI 收 HTTP 402 协议，按次计费。

| 项目 | 值 |
|------|-----|
| 单价 | ¥0.50 / 次 |
| 支付协议 | `alipay_` 短链协议 |
| 网关地址 | `http://8.145.54.67:3000` |
| 技能路径 | `/skill/viral-script-generator` |
| 支付确认路径 | `/pay-confirm` |

### 支付流程

```
1. 客户端发起分析请求  POST /skill/viral-script-generator
2. 服务端返回 402 Payment Required
   Header: Payment-Needed: <Base64支付信息>
   Body: { step: "payment_required", short_link: "alipay_XXX", pay_url: "..." }
3. 用户完成支付宝支付
4. 客户端携带支付凭证回传  x-payment-credential
5. 服务端验证通过 → 执行分析 → 返回结果
```

### HTTP 请求头规范

| 头名称 | 说明 |
|--------|------|
| `Payment-Needed` | 服务端返回：Base64 编码的支付引导信息 |
| `x-payment-credential` | 客户端回传：支付完成后的 alipay_ 凭证字符串 |

## 数据底座

所有数据存储于 `references/viral-script-generator.json`，包含完整的分析模型参数、行业数据库、策略模板与案例库。

## 使用示例

### 请求

```bash
curl -X POST http://8.145.54.67:3000/skill/viral-script-generator \
  -H "Content-Type: application/json" \
  -d '{ ... }'
```

### 响应（支付后）

```json
{
  "status": "completed",
  "skill": "viral-script-generator",
  "data": { ... },
  "payment": { "status": "paid", "amount": "0.50" }
}
```

## 许可

MIT License
*（内容由AI生成，仅供参考）*


## 平台规格速查

| 平台 | 最佳时长 | 宽高比 | 钩子窗口 | 最大字数 | 典型CPM |
|------|---------|--------|---------|---------|---------|
| TikTok | 15-60s | 9:16 | 前1.5秒 | 2,200 | $4.50 |
| 抖音 | 15-45s | 9:16 | 前2秒 | 2,000 | $3.80 |
| Reels | 15-30s | 9:16 | 前1秒 | 2,200 | $6.20 |
| Shorts | 15-30s | 9:16 | 前2秒 | 5,000 | $5.50 |
| B站 | 2-5分钟 | 16:9 | 前5秒 | 20,000 | $3.00 |

## 钩子公式库

| 类别 | 模板数 | 适用场景 | 典型开口语 |
|------|-------|---------|-----------|
| 好奇缺口 | 5 | 教育/金融/健康 | "99%的人都不知道..." |
| 争议引爆 | 5 | 观点/评论/新闻 | "冒死说句大实话..." |
| 情绪共鸣 | 5 | 故事/心理/激励 | "这一刻改变了我的一生" |
| 价值承诺 | 5 | 教程/评测/省钱 | "3分钟学会XX技能" |
| 热点借势 | 5 | 新闻/评论/搞笑 | "我也来试试这个..." |

## 60 秒标准脚本结构

| 阶段 | 时间 | 字数 | 目标 | 典型内容 |
|------|------|------|------|---------|
| HOOK | 0-3s | 30字 | 留住用户 | 问题/争议/反直觉/情感冲击 |
| SETUP | 3-8s | 80字 | 建立语境 | 交代背景/为什么你要看下去 |
| VALUE | 8-45s | 400字 | 交付核心价值 | 教程/分析/故事/对比 |
| CLIMAX | 45-55s | 100字 | 情绪高点 | 结果揭示/反转/金句 |
| CTA | 55-60s | 60字 | 引导行动 | 关注/收藏/评论/分享 |

## 走红算法因子

| 因子 | 权重 | 说明 |
|------|------|------|
| 互动率 | 30% | 点赞+评论+分享 / 播放量 |
| 完播率 | 25% | 完整看完的视频占比 |
| 分享率 | 20% | 分享数 / 播放量 |
| 评论情绪 | 15% | 评论的正负面情感分析 |
| 收藏率 | 10% | 收藏数 / 播放量 |

## 数据底座

`viral-script-generator.json` 包含：五大平台规范、25 个钩子模板、七种品类制作指南、五种叙事框架、四大互动触发器、2026 热门配乐库、按粉丝量级基准数据、周排期与发布日历、三个完整脚本示例。



## 音乐策略

### 调性心理效应
- 大调：明快、活力、积极 — 适合教程、评测、生活技巧
- 小调：情感、戏剧、悬念 — 适合故事、蜕变、前后对比

### 节奏匹配
- 快节奏（>120BPM）：紧迫感、兴奋 — 适合钩子、混剪、倒计时
- 中速（80-120BPM）：专注、教育 — 适合讲解、教程、分析
- 慢速（<80BPM）：电影感、情感 — 适合揭示、结尾、励志

### 音效设计
- Whoosh转场：覆盖跳切和场景变化
- 文字弹窗同步：增强列表类内容的精致感
- 相机快门：强调揭示和产品时刻
- 打碟刮擦：喜剧节拍、期待反转

### 版权安全音乐源
Epidemic Sound / Artlist / Soundstripe / Uppbeat（免费层） / YouTube音频库 / TikTok内置音效库

## 发布策略

### 最佳发布时段
- TikTok：周二、四、五 / 7-9am、12-2pm、7-10pm
- Reels：周一、三、四 / 6-8am、11am-1pm、8-10pm
- Shorts：周五、六、日 / 12-4pm

### 走红阈值
- TikTok：24小时内100K+播放且互动率>10%
- Reels：24小时内50K+播放且互动率>8%
- Shorts：24小时内20K+播放且互动率>6%

## 内容品类适配

| 品类 | 最佳风格 | B-Roll建议 | 推荐配乐 | 典型CPM |
|------|---------|-----------|---------|---------|
| 科技评测 | 活力快节奏 | 产品特写/对比/功能演示 | 电子/合成波 | $8-15 |
| 美妆时尚 | 精致美学 | 质地特写/前后对比/穿搭配 | 流行/R&B | $5-12 |
| 美食烹饪 | 治愈满足 | ASMR备料/成品切面/试吃反应 | 爵士/原声 | $6-14 |
| 健身运动 | 激励热血 | 动作示范/体型对比/训练剪辑 | 嘻哈/EDM | $7-15 |
| 财经商业 | 专业权威 | 图表动画/数据可视化/新闻头条 | 影视/氛围 | $12-25 |
| 知识教育 | 清晰引导 | 图解叠加/文字动画/类比图示 | 氛围/古典 | $8-18 |
| 搞笑娱乐 | 混乱高能 | 反应镜头/变焦/音效/接梗 | 搞笑/梗音 | $3-8 |

## 三个完整脚本示例
- 科技评测60s：AI耳机实时翻译评测
- 金融教育60s：定期存款隐形亏损
- 搞笑反应60s：奶奶看健身视频
