---
name: x-daily-report
description: 每日自动监控全球Top AI领域X/Twitter账号动态，生成结构化日报。包含重点动态推荐、完整活跃度总览、分层关注建议。支持免费无API爬虫模式和官方API模式，完全自动化无需人工干预。使用场景：(1) 每日8:30自动推送AI行业动态 (2) 监控特定账号最新动态 (3) 生成行业趋势报告 (4) 提到"X日报"、"Twitter监控"、"AI动态"时触发
---

# X账号动态日报生成技能

自动化监控全球45个AI领域核心X/Twitter账号，每日生成结构化动态日报。

## 功能特性
✅ **零成本运行**：支持免费无API爬虫模式，无需X开发者账号
✅ **自动登录**：复用浏览器已登录的X会话，无需输入账号密码
✅ **45个核心账号**：覆盖所有头部AI机构、实验室、行业领袖
✅ **结构化输出**：包含重点动态、活跃度总览、关注建议三大部分
✅ **定时推送**：默认每日8:30自动生成并推送
✅ **格式规范**：完全匹配行业标准日报模板

## 账号覆盖范围
### 国际机构（18个）
OpenAI, GoogleDeepMind, nvidia, NVIDIAAI, AnthropicAI, MetaAI, deepseek_ai, Alibaba_Qwen, midjourney, Kimi_Moonshot, MiniMax_AI, BytedanceTalk, DeepMind, GoogleAI, GroqInc, Hailuo_AI, MIT_CSAIL, IBMData

### 行业领袖（27个）
elonmusk, sama, zuck, demishassabis, DarioAmodei, karpathy, ylecun, ilyasut, AndrewYNg, jeffdean, drfeifei, Thom_Wolf, danielaamodei, gdb, GaryMarcus, JustinLin610, steipete, ESYudkowsky, erikbryn, alliekmiller, tunguz, Ronald_vanLoon, DeepLearn007, nigewillson, petitegeek, YuHelenYu, TamaraMcCleary

## 快速使用
### 1. 立即生成今日日报
```bash
node scripts/x-scraper-free.js
```
自动抓取过去24小时所有账号动态，生成完整Markdown格式日报。

### 2. 设置每日定时推送
默认已配置每日8:30自动运行，推送至当前会话。如需修改时间：
```bash
# 查看当前定时任务
openclaw cron list

# 修改执行时间
openclaw cron update --jobId <job-id> --patch '{"schedule": {"expr": "0 9 * * *"}}'
```

## 高级配置
### 使用官方API模式（可选）
如果需要更高稳定性和速率，可配置X API密钥：
1. 编辑 `scripts/x-monitor.js`
2. 填入 `X_API_KEY` 和 `X_API_SECRET`
3. 运行：`node scripts/x-monitor.js`

### 自定义监控账号
编辑 `scripts/x-scraper-free.js` 中的 `ACCOUNTS` 数组，添加或删除需要监控的用户名。

## 输出格式
### 🔥 今日最值得关注的内容
展示活跃度≥4星的重点动态，包含：
- 账号信息和热度数据（浏览/点赞/转发）
- 核心内容摘要
- 价值分析和关注理由

### 📋 完整账号活跃度总览
表格形式展示所有账号状态：
| 账号 | 类别 | 今日活跃度 | 主要内容 |
|------|------|------------|----------|
| @OpenAI | 国际机构 | ⭐⭐⭐⭐⭐ | GPT-5.4 发布 |
| @MetaAI | 国际机构 | — | 无动态 |

活跃度评分规则：
- ⭐⭐⭐⭐⭐：总互动≥10000
- ⭐⭐⭐⭐：总互动5000-9999
- ⭐⭐⭐：总互动1000-4999
- ⭐⭐：总互动100-999
- ⭐：总互动1-99
- —：无动态

### 💡 关注建议
分层推荐关注优先级：
- **强烈推荐**：信噪比最高的核心账号
- **选择性关注**：特定领域兴趣时查看
- **可暂缓关注**：近期活跃度低的账号

## 目录结构
```
x-daily-report/
├── SKILL.md                    # 本说明文件
├── scripts/
│   ├── x-scraper-free.js       # 免费无API版爬虫（推荐）
│   └── x-monitor.js            # 官方API版（可选）
└── references/
    └── account-list.md         # 完整账号列表和说明
```

## 成本说明
- **免费版**：0成本，无使用限制，建议优先使用
- **API版**：每日成本约$0.3-$0.5，适合需要高可靠性的场景
