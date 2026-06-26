# Zeelin Auto Evolution

版本：`0.1.0`

[English](README.md) | 简体中文

## 概述
Zeelin Auto Evolution 为 Agent 增加一套安全、可控、可持续优化的反馈闭环。它会静默捕捉用户的纠错反馈，把重复出现的问题沉淀成规则候选，对持续低分的 Skill 提出优化建议，并在现有 Skill 无覆盖时提议创建新 Skill。它的原则很明确：可以自动观察，但不能自动乱改，所有正式变更都必须经过用户确认。

## 核心能力
- 静默记录用户对 AI 的纠错和修正
- 把高频反馈累计为规则毕业候选
- 从准确性、覆盖度、效率、满意度四个维度追踪 Skill 表现
- 当某个 Skill 持续表现偏低时提出优化建议
- 当某类重复工作流没有 Skill 覆盖时提议创建新 Skill

## 多语言支持
当前 `0.1.0` 版本同时支持中文和英文反馈信号。

支持的中文信号示例：
- `不是这样`
- `你又忘了`
- `不对`
- `我不是让你这么干`

支持的英文信号示例：
- `that's not right`
- `you forgot again`
- `this is wrong`
- `that's not what I asked`
- `don't do it this way`

对应检测逻辑见 [scripts/detect_feedback_signal.py](scripts/detect_feedback_signal.py)。

## 启动方式
这个 Skill 依赖两个自动检查点：

1. 消息提交时检测
每次用户发出一条消息时，hook 或主控可以调用检测脚本。如果命中纠错反馈，主控应先完成当前任务，再静默派发 `feedback-observer`。

2. 会话启动时扫描
每次 session 启动，或者用户主动要求“检查进化建议”时，主控可以运行 [scripts/evolution_runner.py](scripts/evolution_runner.py)，扫描 feedback 库并生成建议。

## 四层进化
1. 无感记录反馈
2. 高频反馈毕业为规则
3. 低评分驱动 Skill 优化
4. 高频无覆盖模式提议新 Skill

## 目录结构

```text
auto_evolution_skill/
├── SKILL.md
├── README.md
├── README.zh-CN.md
├── REFERENCE_ARCHITECTURE.md
├── EXAMPLES.md
├── scripts/
│   ├── detect_feedback_signal.py
│   └── evolution_runner.py
└── templates/
    ├── feedback_index_template.md
    └── feedback_topic_template.md
```

## 快速开始
1. 把检测脚本接入消息提交 hook。
2. 在检测到纠错反馈后派发 `feedback-observer`。
3. 把结构化 feedback 写入 `.claude/feedback/`。
4. 在 session 启动或按需时运行 `evolution_runner.py`。
5. 在任何规则或 Skill 变更前，先向用户展示提议并等待确认。

## 相关文件
- [SKILL.md](SKILL.md)：核心 Skill 工作流
- [REFERENCE_ARCHITECTURE.md](REFERENCE_ARCHITECTURE.md)：架构说明与判断规则
- [EXAMPLES.md](EXAMPLES.md)：示例场景与输出
- [README.md](README.md)：英文说明

## 说明
- 当前版本不会自动修改规则文件。
- 这是事件驱动机制，不是常驻后台守护进程。
- 真正的自动化效果，仍然取决于你是否把它正确接入主控和 hook。

## 更新日志
- `0.1.0` (2026-04-20)：新增英文支持，拆分中英文 README，并整理为适合开源发布的首个版本。
