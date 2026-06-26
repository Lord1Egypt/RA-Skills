# ClawHub 简报模板

> 4 个维度对应 4 套简报结构，每个维度 6-10 个推荐

## 通用头部

```markdown
# 🦞 ClawHub 每日洞察 | 2026-06-03（{维度名}）

> 📊 数据日期：2026-06-03 | 🎯 推荐维度：{维度} | 📦 抓取数量：{N}个 | 🆕 新增推荐：{N}个

## 🎯 TL;DR

今天推荐 **{N}** 个 Skill，其中 **{M}** 个匹配你的关注场景。

[一句话总结今日亮点]

---
```

## D1 趋势（Trending）

**主题**：今日热装（installsCurrent 高）

```markdown
## 🔥 今日热装 Top 5

| 排名 | Skill | 作者 | 当前活跃 | 累计下载 | 活跃度 |
| --- | --- | --- | --- | --- | --- |
| 1 | [Self-Improving Agent](url) | pskoett | 6,347 | 456k | 1.4% |
| ... |

> 💡 活跃度 = installsCurrent / installsAllTime，反映"今天大家还在用什么"

## 🎯 痛点匹配（你的关注）

### 🤖 自动化办公
- **Gog** (作者: steipete) - Google Workspace 全套 CLI
  > 价值: 把 Gmail/Calendar/Drive 都装进 AI Agent
  > 下一步: 试试用 Gog 接管你的 Gmail 工作流

### 🧠 AI 增强
- **Self-Improving Agent** (作者: pskoett) - AI 自我进化
  > 价值: AI 越用越聪明，自动记忆错误和优化
  > 下一步: 把它加入你的 Skill 库，下次任务自动调用

## 📅 7 天推荐回顾

- 6/3 (今天): 5 个 - 重点在 AI 增强
- 6/1: 4 个 - 重点在 自动化办公
- 5/30: 5 个 - 重点在 数据采集
- ...

## 🆕 今日新增
- 5 个新推荐（去重后）
- 3 个被过滤（已在 7 天内推荐过）
```

---

## D2 质量（Quality）

**主题**：被埋没的金子（star_rate 高 + downloads 中等）

```markdown
## ⭐ 口碑精品 Top 8

| 排名 | Skill | 作者 | ⭐ | 📥 | 口碑率 |
| --- | --- | --- | --- | --- | --- |
| 1 | [Skill A](url) | author | 100 | 5,000 | 2.0% |
| 2 | [Skill B](url) | author | 80 | 4,500 | 1.78% |
| ... |

> 💡 口碑率 = ⭐ ÷ 📥 × 100%，高于 0.81% 即为高于平均

## 🏆 详细分析（Top 3）

### 1. Skill A ⭐ 100 / 📥 5,000 (口碑率 2.0%)
- **它做什么**: [...]
- **解决什么问题**: [...]
- **下一步行动**: [...]

### 2. Skill B
[同上结构]

## 🎯 痛点匹配

[同 D1 痛点匹配结构]

## 📅 回顾

[同 D1 回顾结构]
```

---

## D3 新星（Newcomers）

**主题**：7 天内新创建/更新的潜力股

```markdown
## 🚀 7 天内新星 Top 5

| 排名 | Skill | 作者 | 年龄 | 活跃安装 | ⭐ | 价值 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | [New Skill A](url) | author | 3 天 | 120 | 12 | 描述... |
| ... |

> 💡 新星 = 创建时间 < 30 天 且 installsCurrent > 20

## 🔥 新星焦点（Top 2）

### 1. New Skill A (3 天前)
- **它做什么**: [...]
- **为什么值得关注**: [...]
- **下一步行动**: [...]

## 🎯 痛点匹配

[同 D1 痛点匹配结构]

## 📅 回顾

[同 D1 回顾结构]
```

---

## D4 全景（Panorama）

**主题**：分类全景 + 社区热议

```markdown
## 💬 本周热议 Top 3

| 排名 | Skill | 作者 | 评论数 | 主题 |
| --- | --- | --- | --- | --- |
| 1 | [Hot Skill A](url) | author | 200+ | 用户在讨论... |
| ... |

> 💡 热议 = comments 数高，反映社区活跃

## 🏆 9 大分类王者

| 分类 | 冠军 Skill | ⭐ | 📥 | 能力标签 |
| --- | --- | --- | --- | --- |
| MCP Tools | [...] | [...] | [...] | [...] |
| Prompts | [...] | [...] | [...] | [...] |
| Workflows | [...] | [...] | [...] | [...] |
| Dev Tools | [...] | [...] | [...] | [...] |
| Data & APIs | [...] | [...] | [...] | [...] |
| Security | [...] | [...] | [...] | [...] |
| Automation | [...] | [...] | [...] | [...] |
| Other | [...] | [...] | [...] | [...] |

## 🎯 痛点匹配

[同 D1 痛点匹配结构]

## 📅 回顾

[同 D1 回顾结构]
```

---

## 通用页脚

```markdown
---

## 📌 数据说明

- **数据源**: ClawHub Convex API (`wry-manatee-359.convex.cloud`)
- **抓取数量**: {N} 个 Skill
- **时间窗口**: 最近 7 天去重
- **筛选规则**:
  - 趋势维度: installsCurrent > 100
  - 质量维度: star_rate > 0.5%
  - 新星维度: createdAt < 30 天
  - 全景维度: comments > 50

## 📎 相关链接

- ClawHub 官网: https://clawhub.ai
- 完整数据集: [飞书云文档链接]
- 历史报告: [目录索引]

## 🦞 反馈

觉得推荐不准？编辑 `references/pain-points.md` 调整你的痛点优先级。
```

---

## 简报总长度

- **推荐数**: 8-10 个（用户已确认）
- **页面数**: 飞书云文档 1 页（不超过 200 blocks）
- **执行时间**: 抓取 + 指标 + 推荐 < 30 秒

## 飞书消息卡片

```json
{
  "header": {
    "title": {"tag": "plain_text", "content": "🦞 ClawHub 每日洞察"},
    "template": "blue"
  },
  "elements": [
    {
      "tag": "div",
      "text": {
        "tag": "lark_md",
        "content": "**✅ {日期} | {维度}维度**\n推荐 {N} 个新 Skill"
      }
    },
    {"tag": "hr"},
    {
      "tag": "div",
      "text": {
        "tag": "lark_md",
        "content": "**🎯 今日亮点**\n• {Skill1}\n• {Skill2}\n• {Skill3}"
      }
    },
    {
      "tag": "action",
      "actions": [
        {
          "tag": "button",
          "text": {"tag": "plain_text", "content": "📄 查看完整简报"},
          "type": "primary",
          "url": "{飞书文档 URL}"
        }
      ]
    },
    {
      "tag": "note",
      "elements": [
        {"tag": "plain_text", "content": "📅 {日期} | 4 维度轮换 | 7 天去重"}
      ]
    }
  ]
}
```
