# WordPal

WordPal 是一个嵌入在聊天入口中的英语学习 companion，住在你 agent 里的词汇伴练。它能读取近期 memory 个性化挑词，采用FSRS算法重复调度复习，题型也能随掌握度从认知到输出递进。

## 功能概览

- `session-context.js`: 聚合基础学习配置、今日进度、近期记忆摘要与 `learner_memory`
- `next-question.js`: 统一出题入口，返回题型规划与题面约束
- `show-hint.js`: 答错后生成一次性 hint_token，强制 B-3 解析流程在提交前完成
- `submit-answer.js`: 统一答题提交入口，返回评分结果与进度
- `profile.js`: 读写基础学习配置（`user_profile`）
- `push-plan.js`: 将 `push_times` 转换为 learn 注册计划
- `session-summary.js`: 按 `op_id` 输出结构化学习总结
- `report-stats.js`: 输出总量、趋势与风险词统计

## 安装说明

### 环境要求

- Node.js `>= 22.5.0`
- macOS / Linux / Windows
- 如需通过 CLI 安装/发布：`clawhub`

`node:sqlite` 为 Node 内置模块，本仓库无外部依赖，不需要 `npm install` 即可运行。

### 1. 通过 ClawHub 安装

```bash
clawhub install wordpal
```

`clawhub` 默认将技能安装到：`~/.openclaw/skills/wordpal`（managed 全局目录）。

如需安装到自定义工作目录：

```bash
clawhub install wordpal --workdir <your-workdir> --dir skills
```

### 2. 确认 Node 版本

```bash
node --version
```

## 数据目录约定

- 默认 workspace：`~/.openclaw/workspace/wordpal`
- 词库文件：`~/.openclaw/workspace/wordpal/vocab.db`
- 基础学习配置：`vocab.db` 的 `user_profile` 表
- 记忆摘要目录：`~/.openclaw/workspace/memory`

可通过 `--workspace-dir` 与 `--memory-dir` 覆盖默认目录。

## 项目结构

```text
.
├── package.json
├── README.md
├── SKILL.md
├── references/
│   ├── onboarding.md
│   ├── learn.md
│   └── report.md
└── scripts/
    ├── next-question.js
    ├── profile.js
    ├── push-plan.js
    ├── report-stats.js
    ├── session-context.js
    ├── session-summary.js
    ├── show-hint.js
    ├── submit-answer.js
    └── lib/
        ├── errors.js
        ├── output.js
        ├── cli/
        │   └── helpers.js
        ├── core/
        │   ├── fsrs-scheduler.js
        │   ├── input-guard.js
        │   └── vocab-db.js
        ├── services/
        │   ├── learner-memory.js
        │   ├── next-question.js
        │   ├── push-plan.js
        │   ├── question-plan.js
        │   ├── report-stats.js
        │   ├── select-review.js
        │   ├── session-context.js
        │   ├── session-summary.js
        │   ├── show-hint.js
        │   ├── stage-word.js
        │   ├── submit-answer.js
        │   ├── update-word.js
        │   ├── user-profile.js
        │   └── validate-new-words.js
        └── utils/
            └── date.js
```

## License

[MIT](./LICENSE)
