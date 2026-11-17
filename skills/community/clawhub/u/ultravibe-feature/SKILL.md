# Skill: ultravibe-feature — 功能开发(自动生成)

> ⚠️ 此文件由 generate-skill 自动生成,请勿手动修改。修改流程定义请编辑 `flows/feature.json`。

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

## 前置(每次进入/续跑)
1. 调 `npx tsx src/index.ts preflight-check` 机械前置检查

2. 调 `npx tsx src/index.ts checkpoint read`(续跑入口)
3. 调 `npx tsx src/index.ts timeout-check`(超时熔断)
4. 调 `npx tsx src/index.ts phase-enter` 进入当前阶段(失败→阻断,禁止进入不合法阶段)

## A-2 架构声明
**主会话只做编排,不执行具体工作。所有工作阶段(FE-1/FE-2/FE-3)必须通过子代理执行。**

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

### [FE-1] SpecLock
需求冻结,输出 frozen-spec.json

1. 调 `uv phase-enter --phase FE-1` (失败→阻断)
2. 调 `npx tsx src/index.ts dispatch-phase --phase FE-1` 生成阶段简报→交给子代理
3. **子代理执行:**
   a. 调 `uv subagent-phase-enter --phase FE-1` (子代理入口门禁,必须第一个调用)
   b. 每轮迭代前调 `uv iteration-check --phase FE-1 --current N` (迭代截断,上限 3)
   d. 输出产物: .reports/frozen-spec.json
   e. 调 `uv subagent-phase-transition --phase FE-1` (子代理出口门禁)
4. 调 `npx tsx src/index.ts phase-transition --phase FE-1` (失败→回灌;成功→推进)
**失败策略:** retry
**期望事件序列:** validate-spec

### [FE-2] TDD 工程实现
逐需求点 TDD,先测试后实现

1. 调 `uv phase-enter --phase FE-2` (失败→阻断)
2. 调 `npx tsx src/index.ts dispatch-phase --phase FE-2` 生成阶段简报→交给子代理
3. **子代理执行:**
   a. 调 `uv subagent-phase-enter --phase FE-2` (子代理入口门禁,必须第一个调用)
   b. 每轮迭代前调 `uv iteration-check --phase FE-2 --current N` (迭代截断,上限 12)
   c. 读取前置产物: .reports/frozen-spec.json
   e. 调 `uv subagent-phase-transition --phase FE-2` (子代理出口门禁)
4. 调 `npx tsx src/index.ts phase-transition --phase FE-2` (失败→回灌;成功→推进)
**失败策略:** retry
**期望事件序列:** iteration-check → run-tests

### [FE-3] 逆向验证
输出 reverse-impl.json,校验引用真值

1. 调 `uv phase-enter --phase FE-3` (失败→阻断)
2. 调 `npx tsx src/index.ts dispatch-phase --phase FE-3` 生成阶段简报→交给子代理
3. **子代理执行:**
   a. 调 `uv subagent-phase-enter --phase FE-3` (子代理入口门禁,必须第一个调用)
   b. 每轮迭代前调 `uv iteration-check --phase FE-3 --current N` (迭代截断,上限 3)
   c. 读取前置产物: .reports/frozen-spec.json
   d. 输出产物: .reports/reverse-impl.json
   e. 调 `uv subagent-phase-transition --phase FE-3` (子代理出口门禁)
4. 调 `npx tsx src/index.ts phase-transition --phase FE-3` (失败→回灌;成功→推进)
**失败策略:** retry
**期望事件序列:** validate-citation

### [FE-4] 语义比对
机械比对 frozen-spec vs reverse-impl

1. 调 `uv phase-enter --phase FE-4` (失败→阻断)
2. 机械比对 frozen-spec vs reverse-impl
3. 读取前置产物: .reports/frozen-spec.json, .reports/reverse-impl.json
4. 输出产物: .reports/diff-report.json
5. 调 `npx tsx src/index.ts phase-transition --phase FE-4` (失败→回灌;成功→推进)
**失败策略:** retry
**期望事件序列:** semantic-diff → validate-artifact

### [FE-5] 全局守卫
机械聚合 static+tests+scope,输出 guard-report.json

1. 调 `uv phase-enter --phase FE-5` (失败→阻断)
2. 机械聚合 static+tests+scope,输出 guard-report.json
3. 读取前置产物: .reports/diff-report.json, .reports/frozen-spec.json
4. 输出产物: .reports/guard-report.json
5. 调 `npx tsx src/index.ts phase-transition --phase FE-5` (失败→回灌;成功→推进)
**失败策略:** rollback
**期望事件序列:** guard-report

## 硬约束
- **phase-transition 是 checkpoint 推进的唯一入口**,LLM 不再手写 checkpoint
- 工作阶段(FE-1/FE-2/FE-3)必须通过子代理执行,主会话不做具体工作
- 不改 protected_files: .reports/frozen-spec.json, .reports/reverse-impl.json
- 不改白名单外文件(范围蔓延由 check-scope 机械阻断)
- 不自称完成,run-tests+check-scope+check-static 全绿才算完成
- 阶段间调 `context-summary` 压缩上下文,防止膨胀

## 流程配置(唯一真值源)
```json
{
  "id": "feature",
  "name": "功能开发",
  "phases": [
    {
      "id": "FE-1",
      "name": "SpecLock",
      "description": "需求冻结,输出 frozen-spec.json",
      "entry_gate": "type",
      "exit_gate": "none",
      "max_iterations": 3,
      "produces": [
        ".reports/frozen-spec.json"
      ],
      "consumes": [],
      "on_failure": "retry",
      "expected_events": [
        "validate-spec"
      ],
      "mandatory_subagent": true
    },
    {
      "id": "FE-2",
      "name": "TDD 工程实现",
      "description": "逐需求点 TDD,先测试后实现",
      "entry_gate": "type",
      "exit_gate": "type",
      "max_iterations": 12,
      "produces": [],
      "consumes": [
        ".reports/frozen-spec.json"
      ],
      "on_failure": "retry",
      "expected_events": [
        "iteration-check",
        "run-tests"
      ],
      "mandatory_subagent": true
    },
    {
      "id": "FE-3",
      "name": "逆向验证",
      "description": "输出 reverse-impl.json,校验引用真值",
      "entry_gate": "type",
      "exit_gate": "none",
      "max_iterations": 3,
      "produces": [
        ".reports/reverse-impl.json"
      ],
      "consumes": [
        ".reports/frozen-spec.json"
      ],
      "on_failure": "retry",
      "expected_events": [
        "validate-citation"
      ],
      "mandatory_subagent": true
    },
    {
      "id": "FE-4",
      "name": "语义比对",
      "description": "机械比对 frozen-spec vs reverse-impl",
      "entry_gate": "type",
      "exit_gate": "none",
      "max_iterations": 5,
      "produces": [
        ".reports/diff-report.json"
      ],
      "consumes": [
        ".reports/frozen-spec.json",
        ".reports/reverse-impl.json"
      ],
      "on_failure": "retry",
      "expected_events": [
        "semantic-diff",
        "validate-artifact"
      ]
    },
    {
      "id": "FE-5",
      "name": "全局守卫",
      "description": "机械聚合 static+tests+scope,输出 guard-report.json",
      "entry_gate": "type",
      "exit_gate": "chain",
      "max_iterations": 1,
      "produces": [
        ".reports/guard-report.json"
      ],
      "consumes": [
        ".reports/diff-report.json",
        ".reports/frozen-spec.json"
      ],
      "on_failure": "rollback",
      "expected_events": [
        "guard-report"
      ]
    }
  ],
  "default_whitelist": [
    "src/",
    "tests/"
  ],
  "protected_files": [
    ".reports/frozen-spec.json",
    ".reports/reverse-impl.json"
  ],
  "skip_phase": [],
  "on_failure": "terminate"
}
```
