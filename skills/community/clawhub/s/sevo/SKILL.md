---
name: sevo
description: "SEVO — Agent 研发流水线。14 阶段全链路交付：需求规格 → 门禁评审 → 测试用例 → 验收编写 → 架构契约 → 编码实现 → 独立审计 → 回归验证 → 发布门禁 → 部署 → 终验 → 交付账本。"
---

# SEVO — Agent 研发流水线

Spec-Execute-Verify-Operate：面向 AI Agent 的软件交付生命周期。

## 14 阶段流水线

| # | Stage ID | 说明 |
|---|----------|------|
| 1 | spec | 需求规格与概念架构 |
| 2 | spec-review-gate | 需求评审门禁 |
| 3 | test-case-authoring | 测试用例编写（与 4/5/6 并行） |
| 4 | ux-acceptance-authoring | UX 开箱即用验收编写（并行） |
| 5 | commercial-acceptance-authoring | 商用验收编写（并行） |
| 6 | contract | 架构设计、ADR、技术契约（并行） |
| 7 | contract-review-gate | 架构评审门禁 |
| 8 | implement | 编码实现（TDD 循环） |
| 9 | review | 独立代码审计与安全审查 |
| 10 | regression | 回归测试与冒烟验证 |
| 11 | publish-generalization-gate | 发布通用化门禁 |
| 12 | deploy | 构建打包与发布 |
| 13 | verify | 清洁环境端到端终验 |
| 14 | ledger | 交付账本（版本、证据、经验回写） |

spec-review-gate 通过后，test-case-authoring / ux-acceptance-authoring / commercial-acceptance-authoring / contract 四路并行展开；implement 需等待 contract-review-gate 和 test-case-authoring 均通过后才激活。

## 智能路由

任务按复杂度自动分级：
- L0（微小改动）：跳过 spec/contract，直接进 implement → review → regression → verify → ledger
- L1/L2+（中大型）：走完整 14 阶段

## 核心机制

- 评审修复闭环（Review-Fix Loop）：评审发现问题 → 自动生成修复任务 → 修复后定向复验
- 主动澄清：spec/contract/implement 阶段内建模糊检测，歧义就地消解
- 终局收敛验收：逐条对照需求覆盖状态，未覆盖自动回到实现阶段补齐
- 单 Agent 完整降级：一个 Agent 也能走完整流程

## 集成

- OpenClaw 插件：`scripts/init.sh` 安装
- 独立使用：`npm install sevo-pipeline` 后通过 API 调用
- 宿主无关：通过适配器接口与运行环境交互

## 作者

yuchangxu1989@gmail.com
