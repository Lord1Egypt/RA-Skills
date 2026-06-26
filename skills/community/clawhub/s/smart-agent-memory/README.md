# smart-agent-memory

## 这是什么
`smart-agent-memory` 是一个跨平台的 Agent 长期记忆技能,目标是让 Agent 在本地工作区内形成**可读、可搜、可维护**的长期记忆体系。

当前准确能力边界:
- 使用 Node.js CLI 管理记忆
- 支持分层读取:先 index,再按需 context
- 支持事实、教训、实体、会话摘要等写入与查询
- 支持温度模型、归档、反思、提炼
- 支持通过 `setup` 为工作区注入 BOOTSTRAP 启动指令

## 核心能力

### 1. 分层记忆读取
推荐顺序:
1. `index`
2. 判断需要什么
3. `context`
4. 再行动

避免一次性全量读所有 memory。

### 2. 事实 / 教训 / 实体管理
- `remember`
- `recall`
- `learn`
- `entity`
- `facts`
- `lessons`
- `entities`

### 3. Skill 经验记忆
支持按 skill 记录与读取经验:
- `remember ... --skill <name>`
- `skill-mem <name>`
- `skill-list`

### 4. 会话生命周期
- `session-start`
- `session-end`

适合在 session 开始与结束时调用。

### 5. 维护能力
- `gc`
- `reflect`
- `stats`
- `temperature`
- `extract`
- `search`

## 初始化(必须)
本技能**有初始化步骤**。

安装后请先执行一次:
```bash
node ~/.openclaw/skills/smart-agent-memory/scripts/memory-cli.js setup
```

作用:
- 自动发现 `~/.openclaw/workspace*` 工作区
- 为工作区注入 `BOOTSTRAP.md` 记忆启动指令
- 幂等,可重复执行

如果你新增了工作区,再执行一次 `setup` 即可。

## 使用方法

### 1. 会话开始
```bash
node ~/.openclaw/skills/smart-agent-memory/scripts/memory-cli.js session-start
```
用于加载记忆概览与近期上下文。

### 2. 会话中记录信息
```bash
node ~/.openclaw/skills/smart-agent-memory/scripts/memory-cli.js remember "关键信息" --tags tag1,tag2
node ~/.openclaw/skills/smart-agent-memory/scripts/memory-cli.js learn --action "..." --context "..." --outcome positive --insight "..."
```

### 3. 会话结束
```bash
node ~/.openclaw/skills/smart-agent-memory/scripts/memory-cli.js session-end "本次做了什么"
```

### 4. 按需查询
```bash
node ~/.openclaw/skills/smart-agent-memory/scripts/memory-cli.js index
node ~/.openclaw/skills/smart-agent-memory/scripts/memory-cli.js context --tag <tag>
node ~/.openclaw/skills/smart-agent-memory/scripts/memory-cli.js recall <query>
node ~/.openclaw/skills/smart-agent-memory/scripts/memory-cli.js search <query>
```

## 配置与存储说明

### 运行依赖
- `node`

### 默认存储位置
- `~/.openclaw/workspace/memory/`

### 存储形态
根据当前说明文件,技能描述覆盖以下层次:
- Markdown
- JSON
- SQLite / FTS5(在支持环境中)

README 在描述时应保持谨慎:
- 以当前 `SKILL.md` 声明与 CLI 能力为准
- 不把尚未验证的底层实现细节写成外部承诺

## 使用模式

### 1. 个人模式
单 agent 直接使用:setup → session-start → remember/learn → session-end。

### 2. 共享工作区模式
多个 agent 共用一个 workspace 时,可以共享记忆目录,但仍应按角色边界写入,避免噪音。

### 3. 团队模式
在多 agent 团队中,把它当长期记忆底座即可;团队协作约束应由团队模板或团队规范承载,而不是写死在记忆技能本体里。

## 推荐工作流

### 日常最小闭环
1. `setup`(首次)
2. `session-start`
3. 中途 `remember` / `learn`
4. 需要时 `index` / `context` / `recall`
5. `session-end`
6. 定期 `gc` / `reflect`

### 定期维护
- 每日:`reflect`
- 每周:`gc`
- 按需:`extract`

## 限制与边界
- 本地记忆系统,不替代外部知识库
- 记忆质量依赖持续写入高质量 fact / lesson / session summary
- 不建议每轮对话全量加载记忆

## 相关文件
- `SKILL.md`
- `scripts/memory-cli.js`
- `lib/`

## 最近一次修改（中文）
- **v2.1.0 / 2026-03-29**
- README 改为使用周期驱动（初始化 → 使用 → 维护）
- 补充个人模式 / 共享工作区模式 / 团队模式三层使用说明
- 团队协作约束改为由团队规范承载，不写死在记忆技能本体里
