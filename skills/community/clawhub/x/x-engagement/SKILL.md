---
name: x-engagement
version: 4.2.0-local
description: "X/Twitter 运营辅助。完整 onboarding → Persona 学习 → Browser Relay 浏览器控制 → 记忆系统 → 手动提醒模板 → For You 关注建议 → Following 互动建议"
---

# X 运营辅助 Skill v4.2

## 快速开始

**触发条件：**
- "刷推 [时间]"
- "运营推特 [时间]"
- "去X上互动 [时间]"

**首次运行：**
自动进入 Onboarding 流程（详见 `docs/onboarding.md`）

**后续运行：**
读取配置 → 生成互动建议 → 用户确认后执行

---

## 文档结构

```
x-engagement/
├── SKILL.md                    # 主入口（本文件）
├── docs/
│   ├── onboarding.md           # Onboarding 流程
│   ├── browser-operations.md   # 浏览器操作模块（基于 Browser Relay）
│   ├── comment-rules.md        # 评论规则（重要！防止错误）
│   ├── human-behavior.md       # 自然节奏与确认规范
│   ├── memory-system.md        # 记忆系统设计
│   ├── cron-jobs.md            # 手动提醒与维护
│   ├── comment-generation.md   # 评论生成逻辑
│   └── natural-language-parser.md # 自然语言时间解析
├── playbooks/
│   ├── comment-strategies.md   # 评论策略（有效/无效）
│   └── changelog.md            # 策略变更记录
├── data/
│   └── engagement/
│       └── YYYY-MM-DD.json     # 每日评论数据
├── templates/
│   ├── persona.md              # Persona 模板
│   ├── config.json             # 配置模板
│   └── daily-log.md            # 每日日志模板
└── scripts/
    ├── setup-cron.sh           # 生成手动提醒模板
    ├── check-cron.sh           # 检查本地运行状态
    └── daily-review.sh         # 每日复盘脚本
```

---

## 核心功能

### 1. Onboarding（首次运行）

**5个阶段：**
1. 浏览器连接 + 登录检查
2. 选择 Persona（自己或其他账号）
3. 学习 Persona（抓取100条 → 生成描述）
4. 刷推习惯配置
5. 保存配置

**详见：** `docs/onboarding.md`

---

### 2. 自然节奏与确认

**核心原则：** 保持自然节奏，但不追求伪装或规避检测。

**包含：**
- 阅读与判断节奏建议
- 点赞/关注/评论二次确认
- 频率限制
- 人工审核后再执行写操作

**详见：** `docs/human-behavior.md`

---

### 3. 记忆系统

**三层记忆：**

```
memory/daily/hotspots/
├── .onboarding_complete     # Onboarding 标记
├── .config.json             # 用户配置
├── personas/
│   └── [handle].md          # Persona 描述
├── events/                  # 重大事件（永久）
├── tables/                  # 每日热点（7天）
└── history/
    ├── comments/            # 评论历史（避免自相矛盾）
    └── daily/               # 每日日志
```

**关键功能：**
- 记录每次评论内容
- 记录用户说过的话（如"昨天出去吃饭了"）
- 评论前检查历史，避免矛盾

**详见：** `docs/memory-system.md`

---

### 4. 手动提醒与维护

**默认策略：**
- 不自动安装 cron
- 不自动修改 `crontab`
- 仅生成手动提醒模板

**可手动执行的维护项：**
- 每日热点总结
- 记忆清理预览
- 记忆清理执行（需显式 `--apply`）

**生成手动模板：**
```bash
./scripts/setup-cron.sh
```

**详见：** `docs/cron-jobs.md`

---

### 5. 刷推流程

**⚠️ 重要规则（必须遵守）：**

1. **只在 Following 的 Recent 页面评论**（不是 Popular）
2. **评论前检查历史**（避免重复评论同一博主）
3. **记录所有评论**（保存到历史文件）
4. **评论发送前必须得到用户确认**

**详见：** `docs/comment-rules.md`（必读！）

**For You 页面：**
1. 浏览（自然阅读节奏）
2. 关注建议（根据配置条件）

**Following 页面：**
1. 确保是 Recent（不是 Popular）
2. 点赞建议（有价值的推文）
3. 评论建议（2小时内，使用 persona 风格）
4. 用户确认后执行
5. 记录评论到历史（避免重复）

**详见：** `docs/comment-generation.md`

---

### 6. 浏览器操作（基于 Browser Relay）

**使用 `browser-relay-cli`：**
- 连接你们自己的 Browser Relay 运行时
- 复用本地已登录 Chrome/Chromium
- 支持 DOM 优先、截图兜底的受控操作
- 仓库：`https://github.com/jasonCodeSpace/browser-relay`

**核心操作：**
- 读取推文
- 生成评论建议
- 点赞/关注/评论确认后执行
- 滚动与截图验证

**安全边界：**
- 不默认安装持久任务
- 不默认自动发送评论
- 不把 Browser Relay 当 stealth bot

**详见：** `docs/browser-operations.md`

---

## 使用示例

### 首次使用

```
用户: 刷推
Bot: 开始 Onboarding...
     1. 检查浏览器...
     2. 请选择 persona...
     3. 学习中...
     4. 配置刷推习惯...
     5. 完成！开始刷推...
```

### 后续使用

```
用户: 刷推半小时
Bot: 读取配置...
     For You: 给出 6 个建议关注账号
     Following: 给出 6 条候选互动
     你确认后我再执行...
```

---

## 关键特性

| 特性 | 说明 |
|------|------|
| 完整 Onboarding | 5阶段引导，学习 persona |
| 自然节奏与确认 | 阅读节奏、二次确认、频率建议 |
| 记忆系统 | 评论历史、用户信息、热点表格 |
| 手动维护 | 无自动 cron，仅手动模板 |
| 避免矛盾 | 评论前检查历史记录 |
| Browser Relay 集成 | 使用本地 browser-relay-cli |

---

## 自我进化系统

### 核心理念

> 没有记忆的AI，只是一个聪明的工具。
> 有记忆且能进化的AI，才是会成长的伙伴。

### 进化闭环

```
采集数据 → 分析对比 → 得出结论 → 更新规则 → 下次执行
```

### 三大机制

**1. Playbook 系统**
- `playbooks/comment-strategies.md` - 记录有效/无效策略
- `playbooks/changelog.md` - 记录策略变更
- Agent 可以更新自己的规则

**2. 数据采集**
- `data/engagement/YYYY-MM-DD.json` - 每日评论数据
- 记录：时间、作者、内容、结果
- 用于后续分析和优化

**3. 每日复盘（22:00）**
- 统计今日数据
- 分析有效策略
- 更新 Playbook
- 生成明日建议
- 推送报告给用户

### 文件结构

```
x-engagement/
├── playbooks/
│   ├── comment-strategies.md  # 评论策略（有效/无效）
│   └── changelog.md           # 策略变更记录
├── data/
│   └── engagement/
│       └── YYYY-MM-DD.json    # 每日评论数据
└── scripts/
    └── daily-review.sh        # 每日复盘脚本
```

### 使用示例

**Agent 学习过程**：
1. 发现「妙啊」评论效果好
2. 在 Playbook 中记录：「妙啊」适用于技术分享，数据支撑：2026-03-02
3. 下次刷推时读取这条规则
4. 考虑在类似推文上使用相同策略

**进化效果**：
- Agent 越用越聪明
- 自动学习什么评论有效
- 持续优化策略
- 避免重复错误

---

## 必读文档

按顺序阅读：

1. `docs/onboarding.md` - 了解首次运行流程
2. `docs/human-behavior.md` - 了解人类行为模拟
3. `docs/memory-system.md` - 了解记忆系统
4. `docs/comment-generation.md` - 了解评论生成

---

*版本: 4.0.0*
*更新: 2026-03-02*
*改进: 结构化设计 + 记忆系统 + 定时任务 + 人类行为规范*
