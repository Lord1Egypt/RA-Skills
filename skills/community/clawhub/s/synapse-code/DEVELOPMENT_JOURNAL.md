# Synapse Code 开发日记

## 项目起源

Synapse Code 项目始于 2026-04-08，目标是将 Pipeline 代码交付工作流 + Synapse 知识沉淀整合为 OpenClaw Skill，实现一体化完成项目初始化、代码交付、知识沉淀和影响分析。内建代码图谱引擎，越用越懂你的项目。

---

## 开发阶段

### Phase 1: ANKE Refactor
- 重构现有 ai-kb 目录结构
- 提取通用脚本（ingest.py, query.py, lint_wiki.py, scaffold.py）

### Phase 2: synapse-wiki 创建
- 创建独立的 synapse-wiki skill
- 实现 init/ingest/query/lint 命令
- 基线测试 4/4 通过

### Phase 3: synapse-code 创建
- 创建 synapse-code skill
- 整合 Pipeline 和 Synapse 工作流
- 实现 auto_log 功能
- 基线测试 3/3 通过

### Phase 4: 配置化与依赖整合 (v1.0.0)
- 创建 config.template.json，移除硬编码路径
- 将 auto_log.py 嵌入到 synapse-code（不再依赖外部 synapse-core）
- 创建 install.sh 安装脚本
- 创建 CHANGELOG.md 和 RELEASE.md

### Phase 5: GitNexus 内建
- 通过 package.json 将 GitNexus 声明为 npm 依赖
- 修改 install.sh 自动执行 npm install
- 修改 scripts 优先使用内建 bin
- 移除对外 GitNexus 依赖说明

---

## 关键决策

### 1. 目录结构统一
```
synapse-wiki/
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── RELEASE.md
├── .skillhub.json
├── install.sh
├── config.template.json
├── commands/
├── scripts/
└── tests/
```

### 2. GitNexus 内建策略
- 不重写代码分析引擎（成本过高）
- 通过 npm 依赖自动安装
- 对用户透明，对外只体现 synapse-code

### 3. 配置化路径
- 使用 config.json 而非硬编码
- 支持用户自定义 Pipeline workspace 位置

---

## 测试报告

| 技能 | 测试项 | 结果 |
|------|--------|------|
| synapse-wiki | init, ingest, lint, query | **4/4 通过** |
| synapse-code | init_syntax, infer, status | **3/3 通过** |

---

## 经验教训

### 有效做法
- 基线测试作为发布门禁
- install.sh 支持 --dry-run 和 --uninstall
- 文档先行（CHANGELOG/RELEASE 格式规范）

### 踩过的坑
1. **目录结构不一致** — synapse-wiki 最初没有 README.md 和 .skillhub.json
2. **GitNexus 依赖混淆** — 最初在 SKILL.md 声明为 required，后改为内建
3. **rsync 优于 cp** — 支持 --exclude 排除 node_modules

---

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0.0 | 2026-04-08 | 初始公开发布版本 |
| v1.1.0 | 2026-04-08 | 测试覆盖 + 文档完善 + 体验优化 |
| v1.1.1 | 2026-04-08 | 紧急 Bug 修复（lint_wiki.py 递归 + Node.js 兼容） |
| v1.1.2 | 2026-04-08 | IM 平台友好输出改造 |
| v1.1.4 | 2026-04-08 | CHANGELOG 对齐 |
| v1.1.5 | 2026-04-09 | 实验评估逻辑引入 |
| v1.1.6 | 2026-04-09 | 代码审计问题修复 |
| v1.1.7 | 2026-04-09 | P0 崩溃修复 + --help 支持 |
| v2.0.0 | 2026-04-10 | Brain/Hands 架构升级 + wiki 互操作 |

---

## 未来规划

### v2.0.1
- task_router ML 增强 — 基于历史路由改进分类准确率
- 子代理自动重试 — 失败任务智能重试
- 进度通知 — Telegram/飞书推送任务状态

### v2.0.2
- synapse-design — 设计创作 Skill
- synapse-analytics — 数据分析 Skill
- Brain Skill Marketplace
- 跨项目知识图谱
