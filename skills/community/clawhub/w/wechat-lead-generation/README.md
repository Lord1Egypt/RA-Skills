# WeChat Lead Generation Skill for OpenClaw

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://openclaw.ai)

> 微信潜在客户抓取、分析与自动回复营销自动化

## ✨ 功能亮点

- 🔍 **多渠道抓取** - 好友/群聊/朋友圈/公众号文章
- 🧠 **智能分析** - 基于对话内容识别客户兴趣与购买意向
- 🤖 **自动回复** - 生成个性化跟进话术（可选）
- 💾 **线索存储** - 存入 agentmemory，支持长期追踪
- 📊 **评分系统** - 0-100 分智能评分，优先处理高意向客户

## 📦 安装

### 前置要求

- OpenClaw >= 2025.5.0
- Node.js 18+
- Python 3.10+
- 微信 cookie（如需要真实抓取）

### 安装步骤

```bash
# 1. 确保技能目录已存在（已创建）
cd ~/.openclaw/workspace/.agents/skills/wechat-lead-generation

# 2. 启用可执行权限
chmod +x bin/run

# 3. 在 openclaw.json 中启用技能
# 编辑 ~/.openclaw/workspace/openclaw.json:
#   "skills": { "enabled": ["wechat-lead-generation", ...] }

# 4. 重启 OpenClaw
openclaw gateway restart
```

## 🚀 快速开始

### 1. 测试运行（模拟数据）

```bash
cd ~/.openclaw/workspace
.agents/skills/wechat-lead-generation/bin/run \
  --source groups \
  --days_back 3 \
  --keywords "AI,机器人" \
  --analysis_depth detailed
```

预期输出：
```
✅ 线索分析完成
📄 报告: /Users/tom/.openclaw/workspace/output/wechat-lead-generation/leads-report-20260526_1230.md
```

### 2. 查看报告

```bash
cat output/wechat-lead-generation/leads-report-*.md
```

### 3. 启用自动回复（谨慎）

```bash
.agents/skills/wechat-lead-generation/bin/run \
  --source friends \
  --auto_reply true \
  --reply_template "你好{name}，注意到你对{interest}感兴趣，我们的产品可能适合你，想了解更多吗？"
```

## 🔧 参数详解

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `--source` | string | **必填** | 数据源: `friends`(好友私聊) / `groups`(群聊) / `moments`(朋友圈) / `articles`(公众号) |
| `--days_back` | int | 7 | 抓取最近 N 天数据 |
| `--keywords` | CSV | 无 | 仅保留包含关键词的内容，如 `"AI,机器人,chatbot"` |
| `--analysis_depth` | enum | `basic` | 分析深度: `basic`/`detailed`/`deep` |
| `--auto_reply` | bool | `false` | 是否自动生成回复草稿 |
| `--reply_template` | string | 内置模板 | 回复模板，支持 `{name}`, `{interest}`, `{product}` 变量 |

### 使用示例

#### 场景 1: 每日扫描 AI 群聊

```bash
# crontab 或 OpenClaw cron
openclaw cron add \
  --name "每日 AI 群聊线索扫描" \
  --schedule "0 9 * * *" \
  --payload.agentTurn.message "用 wechat-lead-generation 抓取 groups 中最近 1 天的 AI 相关对话，生成报告" \
  --delivery.announce.channel openclaw-weixin
```

#### 场景 2: 分析好友咨询（半自动）

```bash
# 先抓取分析，不自动回复
.agents/skills/wechat-lead-generation/bin/run \
  --source friends \
  --days_back 2 \
  --analysis_depth deep

# 人工审核报告后，对高评分线索单独发送回复
```

## 📊 输出报告结构

```
output/wechat-lead-generation/
├── leads-report-20260526_1230.md    # 主报告（Markdown）
├── artifacts/
│   ├── profiles.json                # 客户画像原始数据
│   ├── high_score_leads.json        # 高评分线索 (≥80分)
│   ├── replies.md                   # 自动回复草稿（如启用）
│   └── raw_messages.json            # 原始抓取内容
```

### 报告示例（Markdown）

```markdown
# 微信线索分析报告

**生成时间**: 2026-05-26 12:30
**数据来源**: groups
**时间范围**: 最近 3 天
**关键词过滤**: AI,机器人

## 📊 概览
| 指标 | 数量 |
|------|------|
| 总抓取数据 | 25 |
| 有效线索 | 8 |
| 高评分 (≥80) | 3 |
| 中等评分 (60-79) | 5 |

## 🔥 高评分线索 (≥80)
### 1. 张三 - 92分
**来源**: group (AI 爱好者群)
**兴趣**: AI, 购买意向
**内容**: 你们那个 AI 机器人怎么卖？...
**建议回复**:
```
你好张三！注意到你对AI机器人感兴趣，我们有...
```

...
```

## 🧮 评分算法

线索总分 100 分，权重分配：

- **关键词匹配 (30%)** - 内容中出现产品相关兴趣标签
- **意向强度 (30%)** - 购买、咨询、合作等信号
- **互动质量 (20%)** - 消息长度、表达清晰度
- **最近联系 (20%)** - 时间越近分数越高

**阈值建议**：
- `≥80` - 高意向，优先跟进
- `60-79` - 中等意向，可选跟进
- `<60` - 低意向，暂不处理

## ⚠️ 安全与合规

### 风险提示

- 微信自动化抓取和回复**可能违反**微信用户协议
- **建议**使用半自动模式（`--auto_reply false`），人工审核后再发送
- 避免高频操作（建议间隔 ≥ 30 秒，cron 任务间隔 ≥ 4 小时）
- 仅用于合法合规的客户跟进场景
- 使用测试账号或小号，防止主号被封

### 最佳实践

1. **先分析，后回复** - 先用 `auto_reply false` 生成报告，人工筛选
2. **控制频率** - cron 任务不要过于频繁（每天 ≤ 6 次）
3. **记录日志** - 保留所有自动回复记录，便于审计
4. **客户退订** - 尊重用户退出请求

## 🛠️ 开发与调试

### 日志查看

```bash
tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | grep wechat-lead-generation
```

### 本地测试（跳过 OpenClaw）

```bash
# 直接运行引擎
echo '{"source":"groups","days_back":1,"keywords":["AI"]}' | python3 engine.py
```

### 清空输出目录

```bash
rm -rf output/wechat-lead-generation/*
```

## 🔄 Roadmap

- [ ] v0.2.0 - 真实微信抓取（wechat-md-publish 集成）
- [ ] v0.3.0 - AI 深度分析（LLM 生成画像）
- [ ] v0.4.0 - 多账号轮询（分布式抓取）
- [ ] v0.5.0 - 可视化仪表盘（HTML 报告）
- [ ] v1.0.0 - CRM 导出（CSV / API）

## 🤝 贡献

欢迎 PR！请先阅读 `CONTRIBUTING.md`。

## 📄 License

MIT © Chace

## 💬 支持

- Issues: https://github.com/ling-qian/openclaw-skills/issues
- 文档: https://github.com/ling-qian/openclaw-skills/tree/main/wechat-lead-generation
- OpenClaw 社区: https://openclaw.ai/community

---

**⚠️ 使用本技能即表示你了解并接受相关风险。请合法合规使用。**
