[English](README.md) | [中文](README_CN.md)

# 远程 Skill 测试

一个 Agent Skill，用于自动化在远程跳板机上端到端测试其他 agent skill。在本地更新 skill 后，本 skill 通过 SSH 连接远程主机，更新已安装的 skill，在专用测试目录中运行目标 skill，取回生成的报告，并与上一次运行结果进行对比。

## 问题背景

本地编辑 skill 后的测试流程目前需要大量手动操作：

- **手动部署** — SSH 到跳板机，`npx skills add` 更新，切换到正确目录。
- **手动执行** — 打开 OpenCode，输入提示词，处理交互确认。
- **手动对比** — 找到上次报告，目视对比结构和内容差异，在脑中映射回 SKILL.md 的改动。

在迭代开发 skill 时，这个过程繁琐且容易出错。

## 核心功能

1. **收集 SSH 配置、目标 skill 名称和测试提示词** — 从用户处获取（不在文件中存储凭据）。测试提示词可在对话中直接提供，或从上下文构建。
2. **创建带时间戳的测试目录** — 在远程主机上创建 `~/skill-tests/{时间戳}-{skill名称}/`。
3. **在测试目录中安装所有 skill（project level）** — 通过 `npx skills add panlm/skills -y` 安装全部 skill（非全局）。skill 之间存在依赖关系（如 `aws-fis-experiment-execute` 运行时会加载 `app-service-log-analysis`），因此必须安装全部 skill 以避免依赖缺失。
4. **执行目标 skill** — 通过 `opencode run --dangerously-skip-permissions` 加用户提供的 prompt（自动追加自动确认后缀）。所有输出（stdout + stderr）通过 `tee` 保存到 `opencode-run.log` 便于诊断。
5. **取回生成的报告和执行日志** — 通过 `scp` 拉回到本地 `./test-results/{skill名称}/{时间戳}/`，文件名保持与远程一致。
6. **查找上一次运行的报告** — 在远程主机搜索 `~/skill-tests/*-{skill名称}/` 目录，找到后将上次报告也 SCP 到**同一个本地运行目录**中。当次报告和上次报告并排存放，原始文件名不变，方便直接对比。
7. **对比报告** — 检查结构合规性（对照 SKILL.md 模板）、与上次的结构差异、关联 SKILL.md 的 git 变更。
8. **输出分析** — 合规性表格、变化摘要、结论（通过 / 部分通过 / 未通过）。

## 关键设计决策

1. **通用框架，不限于 FIS。** 适用于仓库中的任何 skill。用户在对话中直接提供测试提示词；本 skill 只负责编排远程执行和报告对比。

2. **SSH 配置运行时询问。** 任何 IP 地址、用户名、密钥路径都不存储在提交的文件中。每次运行时向用户询问（或用户可以提供 SSH config alias）。

3. **测试提示词由用户直接提供。** 用户在对话中直接给出测试 prompt（或由上下文构建）。自动确认指令由本 skill 自动追加，确保远程 agent 以非交互方式运行，无需等待用户确认。

4. **带 skill 名称的时间戳目录。** 远程测试目录使用 `{时间戳}-{skill名称}` 格式，方便找到同一 skill 的上次运行结果进行对比。

5. **结构对比，非数据对比。** 不同运行的报告会有不同的时间戳、资源 ID 和指标数据。对比聚焦于结构合规性（章节、字段、表格），并将结构变化与 SKILL.md 的更新关联。

6. **OpenCode `run` 非交互执行。** 使用 `opencode run --dangerously-skip-permissions "prompt"` 非交互模式运行 — 无 TUI、无需手动操作、无权限提示。所有输出通过 `tee` 保存到 `opencode-run.log` 便于诊断。

7. **Project level 安装全部 skill。** 在测试目录内通过 `npx skills add panlm/skills -y` 安装全部 skill（非全局）。skill 之间存在依赖关系（如 `aws-fis-experiment-execute` 会加载 `app-service-log-analysis`），必须安装全部 skill 以避免依赖缺失。每次测试运行在 project level 隔离，不影响其他环境。

8. **报告和日志按次运行存储在本地。** 每次测试运行保存到 `./test-results/{skill名称}/{时间戳}/`，当次报告、上次报告、执行日志和测试分析全部存放在同一目录中，文件名与远程一致，每次运行自包含，方便审查。

## 工作流程概览

```
步骤 1:  收集 SSH 配置 + skill 名称 + 测试提示词
          ↓
步骤 2:  SSH → mkdir ~/skill-tests/{时间戳}-{skill名称}/
          ↓
步骤 3:  SSH → cd 测试目录 && npx skills add panlm/skills -y（project level，安装全部 skill 以满足依赖）
          ↓
步骤 4:  SSH → cd 测试目录 && opencode run --dangerously-skip-permissions "prompt" | tee opencode-run.log
          ↓
步骤 5:  SCP → 取回报告文件 + opencode-run.log 到本地 ./test-results/{skill名称}/{时间戳}/
          ↓
步骤 6:  SSH → 在远程查找上一次 ~/skill-tests/*-{skill名称}/ 目录
          ├── 找到 → SCP 上次报告到同一个本地运行目录
          └── 未找到 → 首次运行，跳过对比
          ↓
步骤 7:  分析：结构合规性 + 与上次差异 + 关联 SKILL.md 变更
          ↓
步骤 8:  输出结果 + 结论（通过 / 部分通过 / 未通过）
```

## 报告对比维度

对比**不会**比较数据值（时间戳、资源 ID、指标）。聚焦于：

| 维度 | 检查内容 |
|---|---|
| **结构合规性** | 报告是否包含 SKILL.md 要求的所有章节/字段/表格 |
| **结构差异** | 与上次运行相比，哪些 H2/H3 章节被添加/删除 |
| **SKILL.md 关联** | 报告结构变化是否与近期 SKILL.md 编辑匹配 |

### 结论标准

| 结论 | 含义 |
|---|---|
| **通过** | 所有必需章节存在；结构变化与 SKILL.md 更新匹配 |
| **部分通过** | 大部分章节存在；部分 SKILL.md 变更未反映或有意外变化 |
| **未通过** | 缺少必需章节；或 SKILL.md 变更完全未反映 |

## 前置条件

- **ssh / scp** — 远程访问（用户运行时提供凭据）
- **npx** — 远程主机已安装
- **opencode** — 远程主机已安装并配置 LLM provider 访问
- **git** — 读取 SKILL.md 变更历史

## 错误处理

| 错误 | 原因 | 解决方法 |
|---|---|---|
| SSH 连接被拒绝 | 错误的 host/user/key | 与用户确认 SSH 配置 |
| `npx: command not found` | 远程未安装 Node.js | 在远程主机安装 Node.js |
| `opencode: command not found` | 远程未安装 OpenCode | 在远程主机安装 OpenCode |
| `opencode run` 超时 | Skill 执行时间太长 | 增加 SSH 超时；检查远程日志 |
| 未生成报告 | Skill 执行失败或 prompt 有误 | 检查远程 opencode session 输出 |
| 未找到上次报告 | 该 skill 首次运行 | 跳过对比，仅检查结构合规性 |

## 安全规则

| 规则 | 说明 |
|---|---|
| **不存储凭据** | SSH 配置运行时询问，不提交到文件 |
| **不暴露敏感数据** | IP 地址、主机名、用户名不出现在提交的文件中 |
| **不修改远程文件** | 仅创建测试目录和运行 `opencode run` |
| **不删除远程内容** | 保留所有历史测试结果供对比 |

## 使用示例

```
"Test the aws-fis-experiment-execute skill remotely"
"远程测试 aws-fis-experiment-prepare skill"
"到跳板机上验证 execute skill 的更新效果"
"Run remote test for eks-workload-best-practice-assessment"
```

## 目录结构

```
others/remote-skill-test/
├── SKILL.md          # Skill 主定义文件（Agent 执行指令）
├── README.md         # 英文文档
└── README_CN.md      # 本文件（中文）
```

## 已知限制

- 需要远程主机已安装并配置 OpenCode 及有效的 LLM provider API key。
- `opencode run` 以非交互模式运行 — 真正需要人工判断的 skill 可能无法产生正确结果。
- 长时间运行的 skill（如 FIS 实验超过 10 分钟）可能导致 SSH 超时。如需要可使用 `ssh -o ServerAliveInterval=60`。
- 报告对比仅限结构层面 — 无法评估报告内容（洞察、建议）的质量是否提升。
- 某 skill 首次运行时无上次报告可对比 — 仅检查结构合规性。
