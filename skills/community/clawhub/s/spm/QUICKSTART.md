# SPM — 5 分钟快速上手

> 不读 SKILL.md 也能开始用。读完这篇就能跑第一个 SPM 项目。

---

## 1. 安装（30 秒）

```bash
git clone https://github.com/zhbcher/openclaw-spm.git ~/.openclaw/workspace/spm
```

已安装就跳过。

---

## 2. 启动第一个项目

在 OpenClaw 对话中说：

> 用 SPM 帮我做一个 **JWT 用户认证系统**（Node.js + Express）

SPM 会自动进入 Phase 1（需求澄清），问你 3 个问题。**诚实回答就行。**

---

## 3. 你参与的两个关键节点

整个流程中你只需要在 **两个地方** 做决策，其余 SPM 自动跑：

| 节点 | 你要做什么 | 耗时 |
|------|-----------|------|
| Phase 1→2 交接 | 审批设计文档 + WBS 计划 | 2 分钟 |
| 选择执行模式 | "Subagent 自动执行" 或 "我一步步确认" | 5 秒 |

选完就开始跑了。✅

---

## 4. 常用对话速查

| 你说 | SPM 做的事 |
|------|-----------|
| "帮我做一个 XXX" | 启动完整 5 阶段流程 |
| "继续上次的项目" | 读 WBS 台账，从断点恢复 |
| "跳过 TDD" | 照做。SPM 的铁律只是默认值 |
| "我只想设计" | 只跑 Phase 1+2，不执行 |
| "并行执行" | 无依赖的任务同时派 subagent |

---

## 5. 三种项目类型

在对话开始或 `config/default.yaml` 中设置：

| 类型 | 用于 | SPM 行为区别 |
|------|------|------------|
| `code` | 软件项目 | 标准 TDD → test → coverage |
| `docs` | 文档/技能/SKILL.md | 格式验证替代 TDD |
| `config` | 纯配置文件 | 格式验证 + Schema 校验 |

---

## 6. 读懂 SPM 唯一的核心文件

`docs/spm/ledger.md` 就是一切。看这张表就知道进度：

```
| ID | Work Package | Dependencies | Context Brief | Exit Criteria | Evidence | Status |
|----|-------------|-------------|----------|---------------|----------|--------|
| 1  | DB Schema   | -           | ...      | 迁移脚本执行  | ✅ OK    | done   |
| 2  | JWT 中间件  | 1           | ...      | token签发通过 | ...      | doing  |
```

- `Status` 列告诉你哪些做完了
- `Evidence` 列有实际命令输出 → 不是 agent 瞎说的
- `Context Brief` 让新 subagent 不看历史也能执行

---

## 7. 常见问题

**Q: SPM 能在已有项目上用吗？**

能。告诉它"在现有项目基础上做 XXX"，它会跳过脚手架直接进入需求阶段。

**Q: 中断了怎么办？**

直接说"继续"。SPM 读台账 → 找最后一个 `done` → 从下一个 `todo` 继续。

**Q: 计划需要改？**

正常。说"Task 3 太大了，拆一下"→ SPM 走 mutation 协议：split → 记录 Mutation Log → 重新审查。

**Q: 我的项目不是 Node.js？**

SPM 不限制语言。`docker-patterns`、`python-patterns` 等都可以接。TDD 用对应语言的测试框架就行。

---

## 接下来

- 深入阅读：[SKILL.md](SKILL.md) — 完整架构和工作流
- 单任务执行：[references/TASK-EXECUTION.md](references/TASK-EXECUTION.md)
- 质量工具：[docs/quality-enhancements.md](docs/quality-enhancements.md)
