# Changelog

本文件记录 sevo-pipeline 的所有重要变更，格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/)。

## [1.0.0] - 2026-05-03

### 新增
- 后端全部 27 个 FR 的验收标准（AC）100% 覆盖
- 陌生人开箱即用验证通过（`npm install -g` → `sevo demo` 完整路径可走通）
- 810 条测试用例，74 个测试文件

### 变更
- README 重写为营销质量标准（tagline → 痛点 → 优势 → 快速体验 → 场景）

## [0.9.3] - 2026-04-30

### 新增
- 27 个 FR 全覆盖（含 FR-15 渐进式披露 L2/L3 实现）
- 810 条测试全绿

### 修复
- `sevo demo --okr` flag 补齐（陌生人走查 P1）

## [0.9.0] - 2026-04-28

### 新增
- FR-18 目标驱动 PDCA 闭环：OKR → SMART → PDCA 三层目标体系
- 目标状态机（draft → active → achieved/missed）
- PDCA 循环引擎（Plan → Do → Check → Act，最多 3 轮自动收敛）
- `sevo goal` CLI 命令族（create/list/update/link/pdca）
- 773 条测试全绿

### 修复
- TypeScript strict 模式 28 处空检查修复

## [0.7.0] - 2026-04-25

### 新增
- 门禁系统：需求评审门禁、架构评审门禁（三方会审）、商用化门禁
- 证据链：每个阶段的输入/输出/结论自动记录
- 交付账本（Ledger）：串联版本、证据、经验沉淀，支持 `sevo ledger` 查询
- 评审修复闭环：评审发现问题 → 自动生成修复任务 → 定向复验 → 最多 3 轮收敛
- 智能路由：L0/L1/L2 三级自动判定，微小改动走最小闭环

## [0.5.0] - 2026-04-22

### 新增
- 核心 5 阶段完整实现：Specify → Plan → Implement → Review → Release
- PipelineEngine 流程编排引擎：阶段状态机、自动推进、暂停/恢复/取消
- 并行阶段支持（测试用例/UX 验收/商用验收/架构契约同时执行）
- CLI 命令体系：`sevo create`、`sevo status`、`sevo advance`、`sevo list`
- `sevo init` 自动检测宿主环境、发现 Agent、分配角色
- 独立审计阶段：写代码的和审代码的职责分离

## [0.1.0] - 2026-04-18

### 新增
- 项目初始化，基础流水线框架
- Spec → Contract → Implement → Review → Deploy 五阶段骨架
- CLI 入口 `sevo`，支持 `--help` 和 `--version`
- OpenClaw Gateway 插件适配器
- MIT 协议
