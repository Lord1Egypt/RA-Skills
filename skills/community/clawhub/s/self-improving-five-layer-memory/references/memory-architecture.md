# 五层记忆架构详解

## 层级定义

| 层级 | 名称 | 载体 | 内容 | 维护频率 |
|:----:|------|------|------|----------|
| L1 | 核心层 | SOUL.md + IDENTITY.md + USER.md | 你是谁、底线、用户是谁 | 仅变更时更新 |
| L2 | 认知层 | MEMORY.md → 思维画像 | 用户决策风格、沟通偏好 | 周度蒸馏 |
| L3 | 行为层 | MEMORY.md → 行为习惯 | 用户工作节奏、期望 | 周度蒸馏 |
| L4 | 情境层 | HEARTBEAT.md + 自检文档 | 当前任务、检查项 | 心跳自动 |
| L5 | 潜意识层 | 成长箱 .learnings/ | 错误记录、偏差追踪 | 自动检测+月度晋升 |

## 知识图谱（KG）设计

### 推荐 Wing / Room 结构

```
wing: xiaodi_palace
├── room: identity         → 身份信息
├── room: backend_setup    → 配置、端口、路径
├── room: boss_norms       → 用户偏好、规则
├── room: decisions        → 历史决策记录
├── room: lessons          → 经验教训
└── room: diary            → 每日日记

wing: wing_xiaodi
└── room: diary            → 通用日记
```

### 常用 KG 三元组模式

```
（entity, predicate, object, valid_from）
（"老大", "prefers", "直接简洁", "2026-04-25"）
（"Gateway", "version", "2026.5.2", "2026-05-03"）
（"feishu", "in_plugins_allow", "must_keep", "2026-05-03"）
```

## 进化机制

成长箱 `.learnings/` 目录：

### 错误晋升流程
1. 每次犯错 → 记录到 `叮当_errors.md`（含日期、描述、根因）
2. 同类错误累积到 3 次 → 触发晋升检查
3. 分析是否需要升格为规则
4. 如需晋升 → 写入 AGENTS.md（工作规范）或 SOUL.md（底线规则）
5. 在 errors.md 中标记"✅ 已晋升"并引用规则文件

### 偏差追踪（SHADOW.md）
- 记录"说了没做"的偏差
- 每次检测到"忘了/没做/应该"等信号时自动追加
- 格式：`YYYY-MM-DD | 承诺内容 | 实际状态 | 根因分析`
- 用于周度蒸馏时的自我评估