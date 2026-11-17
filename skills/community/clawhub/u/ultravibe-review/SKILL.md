# Skill: ultravibe-review — 代码审查(自动生成)

> ⚠️ 此文件由 generate-skill 自动生成,请勿手动修改。修改流程定义请编辑 `flows/review.json`。

## 输入
- 用户描述
- 若 `.reports/checkpoint-summary.json` 存在→从 next_phase 续跑

## 参考
- @see `.codex/skills/ultravibe-common/contract.md`
- @see `.codex/skills/ultravibe-common/checkpoint.md`
- @see `.codex/skills/ultravibe-common/scope.md`
- @see `.codex/skills/ultravibe-common/citation.md`
- @see `.codex/skills/ultravibe-common/preflight.md`
- @see `.codex/skills/ultravibe-common/gate.md`

## ⚠️ 只读声明
**全程只读,禁止:** 修改/创建/删除文件、git commit、运行会改变状态的命令。
**允许:** 阅读代码、运行只读命令(git log/rg/npx tsc --noEmit)

## 前置(每次进入/续跑)
1. 调 `npx tsx src/index.ts preflight-check` 机械前置检查
   (跳过 git 可用性检查)
2. 调 `npx tsx src/index.ts checkpoint read`(续跑入口)
3. 调 `npx tsx src/index.ts timeout-check`(超时熔断)
4. 调 `npx tsx src/index.ts phase-enter` 进入当前阶段(失败→阻断,禁止进入不合法阶段)

## A-2 架构声明
**主会话只做编排,不执行具体工作。所有工作阶段(RV-1/RV-2/RV-3)必须通过子代理执行。**

主会话职责:
1. phase-enter(验证入口)
2. dispatch-phase(生成阶段简报,交给子代理)
3. 等待子代理完成
4. phase-transition(验证出口+推进)

子代理职责:
1. 接收 dispatch-phase 简报
2. 执行阶段具体工作(写代码/测试/产物)
3. 调 subagent-phase-enter/transition(门禁链)

## 阶段

### [RV-1] 架构审查
梳理模块分层,检查接口设计,输出 arch-review.json

1. 调 `uv phase-enter --phase RV-1` (失败→阻断)
2. 调 `npx tsx src/index.ts dispatch-phase --phase RV-1` 生成阶段简报→交给子代理
3. **子代理执行:**
   a. 调 `uv subagent-phase-enter --phase RV-1` (子代理入口门禁,必须第一个调用)
   d. 输出产物: .reports/arch-review.json
   e. 调 `uv subagent-phase-transition --phase RV-1` (子代理出口门禁)
4. 调 `npx tsx src/index.ts phase-transition --phase RV-1` (失败→回灌;成功→推进)
**失败策略:** retry

### [RV-2] 缺陷扫描
查找逻辑缺陷、边界条件遗漏,输出 defect-scan.json

1. 调 `uv phase-enter --phase RV-2` (失败→阻断)
2. 调 `npx tsx src/index.ts dispatch-phase --phase RV-2` 生成阶段简报→交给子代理
3. **子代理执行:**
   a. 调 `uv subagent-phase-enter --phase RV-2` (子代理入口门禁,必须第一个调用)
   d. 输出产物: .reports/defect-scan.json
   e. 调 `uv subagent-phase-transition --phase RV-2` (子代理出口门禁)
4. 调 `npx tsx src/index.ts phase-transition --phase RV-2` (失败→回灌;成功→推进)
**失败策略:** retry

### [RV-3] 安全合规
注入风险、硬编码、依赖漏洞、许可证(机械: check-static + audit-deps)

1. 调 `uv phase-enter --phase RV-3` (失败→阻断)
2. 调 `npx tsx src/index.ts dispatch-phase --phase RV-3` 生成阶段简报→交给子代理
3. **子代理执行:**
   a. 调 `uv subagent-phase-enter --phase RV-3` (子代理入口门禁,必须第一个调用)
   d. 输出产物: .reports/security-review.json, .reports/dependency-audit.json
   e. 调 `uv subagent-phase-transition --phase RV-3` (子代理出口门禁)
4. 调 `npx tsx src/index.ts phase-transition --phase RV-3` (失败→回灌;成功→推进)
**失败策略:** retry
**期望事件序列:** check-static → audit-deps

### [RV-4] 聚合报告
汇总三份报告,输出 review-report.json

1. 调 `uv phase-enter --phase RV-4` (失败→阻断)
2. 汇总三份报告,输出 review-report.json
3. 读取前置产物: .reports/arch-review.json, .reports/defect-scan.json, .reports/security-review.json
4. 输出产物: .reports/review-report.json
5. 调 `npx tsx src/index.ts phase-transition --phase RV-4` (失败→回灌;成功→推进)
**失败策略:** retry

## 硬约束
- **phase-transition 是 checkpoint 推进的唯一入口**,LLM 不再手写 checkpoint
- 工作阶段(RV-1/RV-2/RV-3)必须通过子代理执行,主会话不做具体工作
- 不改白名单外文件(范围蔓延由 check-scope 机械阻断)
- 不自称完成,run-tests+check-scope+check-static 全绿才算完成
- 阶段间调 `context-summary` 压缩上下文,防止膨胀

## 流程配置(唯一真值源)
```json
{
  "id": "review",
  "name": "代码审查",
  "phases": [
    {
      "id": "RV-1",
      "name": "架构审查",
      "description": "梳理模块分层,检查接口设计,输出 arch-review.json",
      "entry_gate": "none",
      "exit_gate": "none",
      "max_iterations": 1,
      "produces": [
        ".reports/arch-review.json"
      ],
      "consumes": [],
      "on_failure": "retry",
      "expected_events": [],
      "mandatory_subagent": true
    },
    {
      "id": "RV-2",
      "name": "缺陷扫描",
      "description": "查找逻辑缺陷、边界条件遗漏,输出 defect-scan.json",
      "entry_gate": "none",
      "exit_gate": "none",
      "max_iterations": 1,
      "produces": [
        ".reports/defect-scan.json"
      ],
      "consumes": [],
      "on_failure": "retry",
      "expected_events": [],
      "mandatory_subagent": true
    },
    {
      "id": "RV-3",
      "name": "安全合规",
      "description": "注入风险、硬编码、依赖漏洞、许可证(机械: check-static + audit-deps)",
      "entry_gate": "none",
      "exit_gate": "none",
      "max_iterations": 1,
      "produces": [
        ".reports/security-review.json",
        ".reports/dependency-audit.json"
      ],
      "consumes": [],
      "on_failure": "retry",
      "expected_events": [
        "check-static",
        "audit-deps"
      ],
      "mandatory_subagent": true
    },
    {
      "id": "RV-4",
      "name": "聚合报告",
      "description": "汇总三份报告,输出 review-report.json",
      "entry_gate": "none",
      "exit_gate": "chain",
      "max_iterations": 1,
      "produces": [
        ".reports/review-report.json"
      ],
      "consumes": [
        ".reports/arch-review.json",
        ".reports/defect-scan.json",
        ".reports/security-review.json"
      ],
      "on_failure": "retry",
      "expected_events": []
    }
  ],
  "default_whitelist": [],
  "protected_files": [],
  "skip_phase": [],
  "on_failure": "terminate"
}
```
