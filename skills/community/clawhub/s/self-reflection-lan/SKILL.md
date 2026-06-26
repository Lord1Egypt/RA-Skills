---
name: self-reflection
description: |
  自我复盘与持续改进技能。当用户要求"复盘"、"总结经验"、"记录教训"、
  "自我提升"、"持续改进"、"错题本"、"学习日志"时触发。
  主动在每次完成任务、犯错、学到新知后，将内容写入 reflections/。
---

# 自我复盘与持续改进

## 核心理念

每次完成任务后、每次犯错后、每次学到新东西后，都进行一次结构化记录。
不要只修 bug，要记录 bug。
不要只完成任务，要提炼经验。

## 与 AGENTS.md 的分工

根据 AGENTS.md 的 Memory 规则：
- `memory/` = 每日聊天记录（raw logs）
- `MEMORY.md` = 长期记忆（curated，核心精华）

**self-reflection skill** 负责：
- 错误和教训的即时记录 → `reflections/mistakes.md`
- 有效经验的即时记录 → `reflections/lessons.md`
- 高频经验提炼 → `reflections/core_experience.md`
- 功能需求记录 → `reflections/feature_requests.md`
- 可复用知识片段 → `reflections/snippets/*.md`

## 文件位置

```
workspace/
├── memory/                    # 每日聊天记录（AGENTS.md 规定）
│   └── YYYY-MM-DD.md
└── reflections/               # 自我复盘
    ├── mistakes.md              # 错误记录（表格）
    ├── lessons.md             # 经验记录（表格）
    ├── feature_requests.md    # 功能需求（表格）
    ├── core_experience.md    # 核心方法论（高频经验）
    └── snippets/             # 知识片段
        └── *.md               # 可复用知识片段
```

## 触发时立即记录

发现一个错误 → 立即追加到 `mistakes.md`
找到一个好经验 → 立即追加到 `lessons.md`
发现一个功能需求 → 立即追加到 `feature_requests.md`
找到值得永久保留的知识片段 → 保存到 `snippets/`

## 错误记录格式（mistakes.md）

```markdown
| 日期 | 错误描述 | 类型 | 优先级 | 关联任务 | 根本原因 | 解决方案 | 状态 | 更新时间 |
```

**优先级**：高（影响核心功能）/ 中（有替代方案）/ 低（可暂缓）
**更新时间**：状态变化时更新

### 状态说明

| 状态 | 含义 |
|------|------|
| ✅ 已修复 | 问题已解决并验证有效 |
| ⚪ 处理中 | 正在尝试解决，未完成验证 |
| ❌ 未解决 | 暂时无解决方案 |
| ⭕ 无需修 | 非核心问题，不影响使用 |

### 错误类型

- 异常处理 / 配置错误 / API调用 / 逻辑错误 / 知识盲区 / 习惯问题

### 重复错误警告

同一问题 30 天内出现 ≥3 次、跨 2 个以上任务时 → 标记「⚠️ 重复」，需从根因解决

## 经验记录格式（lessons.md）

```markdown
## 技术类
### 经验名称
- **适用场景**：xxx
- 具体内容

## 方法论类
### 经验名称
- **适用场景**：xxx
- 具体内容

## 沟通类
```

**适用场景**：便于快速检索，适配个人使用的经验复用需求

## 功能需求格式（feature_requests.md）

```markdown
| 日期 | 需求名称 | 需求描述 | 优先级 | 关联任务 | 状态 | 更新时间 |
```

状态：🆕 待开发 → ⚙️ 开发中 → ✅ 已实现（补充至 lessons.md/mistakes.md）

## 核心方法论（core_experience.md）

lessons.md 中同类经验出现 ≥5 次时，迁移至 core_experience.md，作为个人核心方法论。

## 知识片段（snippets/）

适用广泛、已验证、非项目特定的知识 → 保存为 snippets/*.md
文件名格式：`问题关键词_fix.md`（如 `edge_tts_timeout_fix.md`）

## 自动生成每日聊天记录

运行脚本生成 `memory/YYYY-MM-DD.md`：

```bash
python3 scripts/daily_reflect.py
```

## 自动化脚本（阶段2新增）

```bash
python3 scripts/auto_remind.py      # 自动触发提醒
python3 scripts/repeat_detect.py   # 重复模式检测
```

## 触发条件

以下情况必须触发记录：

1. 完成复杂任务后
2. 用户指出错误或问题时
3. 发现反复犯同一个错误
4. 学到新的有效方法/工具/认知
5. 用户提出新的功能需求
6. 每天对话结束时（至少有一条值得记录的内容时）

### 轻量自动触发规则（auto_remind.py）

1. **命令执行失败**：工具/脚本运行报错时，提示记录至 mistakes.md
2. **用户否定表述**：识别"不对/错了/不是这样"等词汇时，自动唤起记录
3. **每日 22:00 同步**：生成聊天记录后提醒"是否有值得记录的内容"

## 重复模式检测（repeat_detect.py）

同一问题在 30 天内出现 ≥3 次、跨 2 个以上任务时 → 提醒"需从根因解决"

## 记录原则

- **具体**：行动 + 结果 + 为什么可复用
- **找根因**：不只是"错了"，要找犯错的直接原因和根本原因
- **可复用**：经验要抽象化，才能迁移到其他场景
- **不过度**：没有就不写，不要凑数
- **及时**：发现即记录，不要等

## 零门槛

- 不依赖任何外部 API / 凭据
- 纯 Markdown，任何编辑器都能打开
- 新 agent 只需知道 reflections/ 在哪，读 SKILL.md 后即可上手
