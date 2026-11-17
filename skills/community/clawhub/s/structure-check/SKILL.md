---
name: structure-check
description: Stop trusting "done." Structure Check mechanically verifies that everything the task required actually exists in the code — symbols defined, exports wired, functions actually called, no stub shells hiding behind a TODO. The agent writes a requirement checklist from the user's task, the tool checks every item, and the exit code decides (0 all pass / 1 something missing / 2 bad checklist). The agent may only quote the verdict, never overrule it. Zero dependencies, Node >= 18, comment-aware; full JS/TS support plus Python exists/notStub. Use after completing any coding task (trigger phrases - structure check, feature implemented, 触发词 - 结构检查, 功能是否实现, 实现核对, 检查代码结构, 交付核对).
version: 1.0.0
license: MIT
metadata:
  openclaw:
    emoji: "🧱"
    requires:
      env: []
      bins:
        - node
    primaryEnv: ""
    models: []
---

# Structure Check (requirement checklist, tool-decided)

把「功能是否实现」从模型的自我报告变成退出码裁决的机械核对。模型声称做完了不可信——本工具按要求清单逐条核对结构证据：**要求的东西在不在、导没导出、接没接上、是不是空壳**。

与其他守卫的分工：回归守卫（ai-code-verification-guard）管「改完后行为没变坏」；TDD 守卫（tdd-guard）管「开发顺序合规」；本工具管「结构存在性」。三者互补，可同时启用。

`scripts/structure-check.mjs` 随本技能分发，`<skill-path>` 指本技能安装目录。agent 只允许调用脚本并**逐字转述** `STRUCTURE CHECK` 输出块，无权改判结果。

## Hard rules

1. **任务完成后必须核对**：从用户需求/任务描述提取要求清单（每条一个 `desc` + 检查项），写成 JSON，然后在项目根执行：

   ```
   node <skill-path>/scripts/structure-check.mjs <checklist.json>
   ```

2. **清单必须有真实来源**——来自用户原话或任务描述里的明确要求（某个函数、某个导出、某处调用）。禁止凭空编造必然 PASS 的清单来自我证明。
3. **FAIL 的唯一处置是修代码**：按 reason 修复后重跑，直到全 PASS 或向用户如实说明。禁止删改清单条目来凑 PASS；只有用户明确变更需求时才允许改清单，且必须在回复中说明。
4. **不得改判**：输出块的 result 与退出码是唯一裁决，agent 只转述。

## Checklist format

```json
{
  "task": "实现购物车模块",
  "requirements": [
    { "desc": "Cart 类已定义",       "type": "exists",   "file": "src/cart.js",  "symbol": "Cart" },
    { "desc": "Cart 已导出",         "type": "exported", "file": "src/cart.js",  "symbol": "Cart" },
    { "desc": "addItem 在入口被调用", "type": "called",   "file": "src/index.js", "symbol": "addItem" },
    { "desc": "computeTotal 非空壳",  "type": "notStub",  "file": "src/cart.js",  "symbol": "computeTotal" }
  ]
}
```

`file` 相对执行时的工作目录解析；一个符号要核对多个文件就写多条要求。

## Check types

| type | PASS 条件 | 典型 FAIL 场景 |
|---|---|---|
| exists | 符号在本文件有定义（function/class/const/interface/type/enum/方法简写/def） | 要求的函数/类根本没写 |
| exported | 符号已导出（export / export default / module.exports / exports.x） | 定义了但没接上模块出口 |
| called | 符号在本文件存在调用点（排除定义行本身；new X() 算调用） | 导出了但没有任何地方使用（假接线） |
| notStub | 函数体非空壳 | 空体、裸 return、TODO/未实现抛错、Python 的 pass/... 冒充实现 |

## Verdict table (exit code decides; the agent has no discretion)

| result | Exit code | Disposal |
|---|---|---|
| PASS | 0 | 全部要求核实通过；逐字转述输出块 |
| FAIL | 1 | 至少一条要求未实现；修代码后重跑，禁止报告「已完成」 |
| UNVERIFIED | 2 | 清单或用法有问题（缺字段/非法 JSON/未知 type/缺参数）；修清单重跑 |

## Anti-patterns caught

- **虚报完成**：声称「已实现 X」但 X 根本不存在——exists FAIL。
- **空壳函数**：函数体去注释后只剩 `return` / `throw not implemented` / `pass` / `...`——notStub FAIL。
- **假接线**：函数已导出但整个文件没有任何调用点——called FAIL。
- **半接线**：定义了但没导出，其他模块拿不到——exported FAIL。
- **编造清单**：条目全部轻易 PASS 以自我证明——Hard rule 2；清单必须能追溯到任务要求。

## Scope & limits

- 机械正则核对，**不做语义分析**：逻辑对不对、行为有没有回归，归测试与回归守卫管。
- JS/TS 全量支持；Python 支持 exists / notStub；exported / called 目前是 JS/TS 形态。
- 检查前会先剥离注释，注释里写的代码不算数。
- 文件不存在按该条 FAIL，不豁免。

## Requirements

- Node.js ≥ 18，零依赖。
- 清单 JSON 由调用方（agent）生成并落盘；建议放临时目录，用完即删，勿提交进项目。
