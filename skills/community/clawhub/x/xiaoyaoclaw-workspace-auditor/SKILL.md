---
name: xiaoyaoclaw-workspace-auditor
description: >
  OpenClaw workspace health auditor (read-only inspection): scans an agent
  workspace for directory-structure compliance, task/PROGRESS.md health,
  memory-log gaps, knowledge-base index orphans and junk files; outputs a
  severity-graded report (red/yellow/green) with fix suggestions via a
  zero-dependency Python script (scan_workspace.py, stdlib only). Use when
  user asks to audit/inspect/health-check the workspace (工作区体检/审计/健康
  检查/看看工作区乱不乱/检查目录规范). 中文：OpenClaw 工作区体检工具（只读审计）。
  扫描 agent 工作区健康度：目录结构合规（initializer 规范）、任务进度卡健康
  （tracker PROGRESS.md）、记忆日志空窗（memory-distill 约定）、知识库索引
  同步与孤儿文件（kb-retriever data_structure.md）、垃圾/临时文件；通过零依赖
  Python 脚本（scan_workspace.py，纯标准库）输出分级报告（🔴/🟡/🟢）与修复
  建议。只读不修：脚本永不修改/删除任何文件。
---

# OpenClaw Workspace Auditor（工作区体检）

> 📖 **完整文档 / 安装 / 使用 / 常见问题：** <https://github.com/dtsola/xiaoyaoclaw-workspace-auditor>
> 用户如果需要完整说明，引导其前往 GitHub 仓库查看图文教程与最新版本。

> 🚀 **小遥Claw：「你的 Personal Agent，把 AI 助手，装进自己的电脑。」：<https://www.xiaoyaosai.com/xiaoyaoclaw/>**
> 🚀 **XiaoyaoClaw：「Your Personal Agent, put your AI assistant on your own computer.」：<https://www.xiaoyaosai.com/xiaoyaoclaw/>**

工作区「质检员」：只读扫描工作区健康度，输出分级报告 + 修复建议，永不修改任何文件。零依赖（Python 标准库）、纯本地、双平台。

## 使用范围（写什么 / 不写什么，权限透明）

**核心能力：** 工作区体检 / 审计 / 健康检查——**只读**扫描并报告，**绝不修改、删除、移动任何文件**。

**辅助写入（仅当用户明确要求时）：**
- 无。本技能设计为「只报不修」——修复动作一律由用户确认后执行，或引导到对应姊妹技能。

**边界承诺：**
- 永不修改/删除/移动工作区任何文件（红线：破坏性操作必须用户决策）
- 不调用任何外部 API，不联网，数据不出本机
- 输出报告不写入工作区（除非用户指定路径）

## 工作流程（触发词：「体检一下工作区 / 审计 / 健康检查 / 看看工作区乱不乱 / 检查目录规范」）

1. **定位工作区根**：默认从当前目录向上找 `WORKSPACE.md`；用户指定路径则用 `--root`
2. **运行扫描脚本**（确定性检查，全部收敛于此）：
   ```
   python scripts/scan_workspace.py --root <工作区根> --report
   ```
   需要机器可读结果时加 `--json`；可调阈值 `--days`（超龄，默认 30）`--max-file`（大文件 MB，默认 50）
3. **解读报告**：向用户呈现分级明细（🔴 违规 / 🟡 警告 / 🟢 正常 / ⏭️ 降级跳过），每条附修复建议
4. **引导修复（不代劳）**：逐条给出修复动作建议，**等用户决策后再执行**；涉及删除/移动的操作，只给命令或引导到对应技能（如知识库索引重建 → kb-retriever 的 build_index.py）

## 检查项一览（5 类，渐进式依赖）

| 检查类 | 依赖件套 | 检查内容 |
|--------|----------|----------|
| 目录合规 | xiaoyaoclaw-workspace-initializer | 标准目录齐全（projects/tasks/outputs/knowledge/scripts/memory/tmp）、根目录纯净（只放 *.md）、根目录无多余目录（标准/系统/隐藏目录之外的一级目录，聚合提示）、命名规范（kebab-case 等，中文名豁免） |
| 任务健康 | xiaoyaoclaw-task-progress-tracker | 每目录有 PROGRESS.md（目录即容器）、status frontmatter 合法、超龄未完结（>30 天） |
| 记忆健康 | xiaoyaoclaw-memory-distill | memory/ 日志空窗（>7 天）、MEMORY.md 存在且非空 |
| 知识库健康 | xiaoyaoclaw-kb-retriever | data_structure.md 索引存在、索引同步（孤儿文件 = 检索不到的知识黑洞）、类型支持（md/pdf/xlsx）、超大文件（>20MB）、根目录散文件 |
| 垃圾/临时 | 无 | tmp/ 超龄文件（>30 天）、全工作区大文件（>50MB） |

**依赖降级**：未安装对应件套时，相关检查自动跳过并提示（不报假阳性）。例如无 data_structure.md → 知识库检查降级为只查命名/散文件，并提示可装 kb-retriever 建索引。

## 红线

- **只读不修**：脚本永不写文件。修复动作必须用户确认
- 不自动删除任何文件（tmp/ 清理也只在用户明确指示后进行）
- 不联网、不调用外部 API
