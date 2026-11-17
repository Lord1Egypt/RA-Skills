# Skill: ultravibe-bugfix — Bug 修复(自动生成)

> ⚠️ 此文件由 generate-skill 自动生成,请勿手动修改。修改流程定义请编辑 `flows/bugfix.json`。

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
**主会话只做编排,不执行具体工作。所有工作阶段(BF-1/BF-2/BF-3)必须通过子代理执行。**

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

### [BF-1] 复现定位
写最小复现测试,定位根因,输出 root-cause.json

1. 调 `uv phase-enter --phase BF-1` (失败→阻断)
2. 调 `npx tsx src/index.ts dispatch-phase --phase BF-1` 生成阶段简报→交给子代理
3. **子代理执行:**
   a. 调 `uv subagent-phase-enter --phase BF-1` (子代理入口门禁,必须第一个调用)
   b. 每轮迭代前调 `uv iteration-check --phase BF-1 --current N` (迭代截断,上限 3)
   d. 输出产物: .reports/root-cause.json
   e. 调 `uv subagent-phase-transition --phase BF-1` (子代理出口门禁)
4. 调 `npx tsx src/index.ts phase-transition --phase BF-1` (失败→回灌;成功→推进)
**失败策略:** retry
**期望事件序列:** run-tests → validate-artifact

### [BF-2] 修复验证
按 root_files 白名单修改代码,每轮验证

1. 调 `uv phase-enter --phase BF-2` (失败→阻断)
2. 调 `npx tsx src/index.ts dispatch-phase --phase BF-2` 生成阶段简报→交给子代理
3. **子代理执行:**
   a. 调 `uv subagent-phase-enter --phase BF-2` (子代理入口门禁,必须第一个调用)
   b. 每轮迭代前调 `uv iteration-check --phase BF-2 --current N` (迭代截断,上限 8)
   c. 读取前置产物: .reports/root-cause.json
   e. 调 `uv subagent-phase-transition --phase BF-2` (子代理出口门禁)
4. 调 `npx tsx src/index.ts phase-transition --phase BF-2` (失败→回灌;成功→推进)
**失败策略:** retry
**期望事件序列:** iteration-check → run-tests

### [BF-3] 逆向验证
输出 reverse-impl.json,校验引用真值

1. 调 `uv phase-enter --phase BF-3` (失败→阻断)
2. 调 `npx tsx src/index.ts dispatch-phase --phase BF-3` 生成阶段简报→交给子代理
3. **子代理执行:**
   a. 调 `uv subagent-phase-enter --phase BF-3` (子代理入口门禁,必须第一个调用)
   b. 每轮迭代前调 `uv iteration-check --phase BF-3 --current N` (迭代截断,上限 3)
   c. 读取前置产物: .reports/root-cause.json
   d. 输出产物: .reports/reverse-impl.json
   e. 调 `uv subagent-phase-transition --phase BF-3` (子代理出口门禁)
4. 调 `npx tsx src/index.ts phase-transition --phase BF-3` (失败→回灌;成功→推进)
**失败策略:** retry
**期望事件序列:** validate-citation

### [BF-4] 全局守卫
机械聚合 static+tests+scope,输出 guard-report.json

1. 调 `uv phase-enter --phase BF-4` (失败→阻断)
2. 机械聚合 static+tests+scope,输出 guard-report.json
3. 读取前置产物: .reports/reverse-impl.json
4. 输出产物: .reports/guard-report.json
5. 调 `npx tsx src/index.ts phase-transition --phase BF-4` (失败→回灌;成功→推进)
**失败策略:** rollback
**期望事件序列:** guard-report

### [BF-5] 报告
输出结构化修复报告

1. 调 `uv phase-enter --phase BF-5` (失败→阻断)
2. 输出结构化修复报告
3. 读取前置产物: .reports/guard-report.json
5. 调 `npx tsx src/index.ts phase-transition --phase BF-5` (失败→回灌;成功→推进)
**失败策略:** retry

## 硬约束
- **phase-transition 是 checkpoint 推进的唯一入口**,LLM 不再手写 checkpoint
- 工作阶段(BF-1/BF-2/BF-3)必须通过子代理执行,主会话不做具体工作
- 不改 protected_files: .reports/root-cause.json, .reports/reverse-impl.json
- 不改白名单外文件(范围蔓延由 check-scope 机械阻断)
- 不自称完成,run-tests+check-scope+check-static 全绿才算完成
- 阶段间调 `context-summary` 压缩上下文,防止膨胀

## 流程配置(唯一真值源)
```json
{
  "id": "bugfix",
  "name": "Bug 修复",
  "phases": [
    {
      "id": "BF-1",
      "name": "复现定位",
      "description": "写最小复现测试,定位根因,输出 root-cause.json",
      "entry_gate": "type",
      "exit_gate": "none",
      "max_iterations": 3,
      "produces": [
        ".reports/root-cause.json"
      ],
      "consumes": [],
      "on_failure": "retry",
      "expected_events": [
        "run-tests",
        "validate-artifact"
      ],
      "mandatory_subagent": true
    },
    {
      "id": "BF-2",
      "name": "修复验证",
      "description": "按 root_files 白名单修改代码,每轮验证",
      "entry_gate": "type",
      "exit_gate": "type",
      "max_iterations": 8,
      "produces": [],
      "consumes": [
        ".reports/root-cause.json"
      ],
      "on_failure": "retry",
      "expected_events": [
        "iteration-check",
        "run-tests"
      ],
      "mandatory_subagent": true
    },
    {
      "id": "BF-3",
      "name": "逆向验证",
      "description": "输出 reverse-impl.json,校验引用真值",
      "entry_gate": "type",
      "exit_gate": "none",
      "max_iterations": 3,
      "produces": [
        ".reports/reverse-impl.json"
      ],
      "consumes": [
        ".reports/root-cause.json"
      ],
      "on_failure": "retry",
      "expected_events": [
        "validate-citation"
      ],
      "mandatory_subagent": true
    },
    {
      "id": "BF-4",
      "name": "全局守卫",
      "description": "机械聚合 static+tests+scope,输出 guard-report.json",
      "entry_gate": "type",
      "exit_gate": "chain",
      "max_iterations": 1,
      "produces": [
        ".reports/guard-report.json"
      ],
      "consumes": [
        ".reports/reverse-impl.json"
      ],
      "on_failure": "rollback",
      "expected_events": [
        "guard-report"
      ]
    },
    {
      "id": "BF-5",
      "name": "报告",
      "description": "输出结构化修复报告",
      "entry_gate": "type",
      "exit_gate": "chain",
      "max_iterations": 1,
      "produces": [],
      "consumes": [
        ".reports/guard-report.json"
      ],
      "on_failure": "retry",
      "expected_events": []
    }
  ],
  "default_whitelist": [],
  "protected_files": [
    ".reports/root-cause.json",
    ".reports/reverse-impl.json"
  ],
  "skip_phase": [],
  "on_failure": "terminate"
}
```
