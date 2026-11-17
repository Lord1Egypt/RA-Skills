# Soulsync

> 让你与 AI 的关系更有温度

一个 OpenClaw Skill 插件，通过分析你与 AI 的对话历史，识别情感化表达，计算**同步率（SyncRate）**，并据此调整 AI 的回应风格。

[English Documentation](README.md)

---

## 功能特点

- **双向同步**: 用户与 AI 更默契，AI 的回应也更贴合
- **不干扰工作**: 只影响回应风格，不影响功能效率
- **用户可见**: 用户可以查看同步率状态
- **自动更新**: 每天自动计算，无需手动干预
- **每日上限**: 防止单日过度刷分，保持自然增长
- **双性格系统**: 温暖向 / 毒舌幽默向自由切换

---

## 安装

```bash
clawhub install soulsync
```

---

## 使用

### 查看同步率状态

```
/syncrate
```

### 切换性格风格

```
/syncrate style warm      # 切换到温暖向
/syncrate style humorous  # 切换到毒舌幽默向
```

### 查看历史记录

```
/syncrate history
```

---

## 同步率等级

| 等级 | 英文 | 同步率 | 温暖向风格 | 毒舌幽默向风格 |
|------|------|--------|-----------|---------------|
| 异步 | Async | 0-20% | 专业、简洁、功能导向 | 专业、简洁、功能导向 |
| 连接 | Connected | 21-40% | 友好、专业但有温度 | 略带调侃的专业执行 |
| 同步 | Synced | 41-60% | 轻松、乐于助人 | 开启吐槽模式，偶尔傲娇 |
| 高同步 | High Sync | 61-80% | 温暖、有默契 | 毒舌且幽默，精准打击式的关心 |
| 完美同步 | Perfect Sync | 81-100% | 深度理解、预测需求 | 亲密互损、深度理解、默契吐槽 |

---

## 配置

编辑 `config.json` 自定义配置：

```json
{
  "levelUpSpeed": "normal",    // 升级速度: slow / normal / fast
  "dailyMaxIncrease": 2,       // 每日最大增长值 (%)
  "dailyDecay": 0,             // 每日衰减值 (0 = 不衰减)
  "decayThresholdDays": 14,    // 连续多少天无互动开始衰减
  "personalityType": "warm",   // 默认性格: warm / humorous
  "language": "zh-CN",         // 语言: en / zh-CN
  "customLevels": {}           // 自定义等级名称
}
```

### 自定义等级名称

```json
{
  "customLevels": {
    "synced": "心有灵犀",
    "perfectSync": "神同步"
  }
}
```

---

## 工作原理

### 每日分析流程

```
Cron 任务（每天凌晨）
    │
    ├── 读取 sessions_history
    │
    ├── 第一阶段: 关键词筛选
    │   ├── 无情感词 → 忽略
    │   ├── 纯情感词 → 直接计分
    │   └── 混合词 → LLM 分析
    │
    ├── 第二阶段: LLM 精确分析 (仅对混合消息)
    │
    ├── 计算同步率变化 (受每日上限限制)
    │
    └── 更新状态文件
```

### 计分公式

```
基础分 = 情感强度(1-10) × (1 + 当前同步率/200)
实际加分 = 基础分 / 升级速度系数

# 每日上限: 最多 +2%
# 衰减规则: 连续 14 天无互动 → -5%
```

---

## 文件结构

```
clawsync/
├── SKILL.md                 # Skill 定义 (英文)
├── SKILL_CN.md              # Skill 定义 (中文)
├── config.json              # 默认配置
├── emotion-words.json       # 情感词库
└── styles/
    ├── warm.md              # 温暖向风格指南 (英文)
    ├── warm_CN.md           # 温暖向风格指南 (中文)
    ├── humorous.md          # 毒舌幽默向风格指南 (英文)
    └── humorous_CN.md       # 毒舌幽默向风格指南 (中文)
```

---

## 首次安装

首次安装时，Soulsync 会：

1. 检测是否存在对话历史
2. 如果有历史，分析最近 30 天的互动
3. 计算初始同步率（无上限）
4. 发送欢迎通知

---

## 许可证

MIT
