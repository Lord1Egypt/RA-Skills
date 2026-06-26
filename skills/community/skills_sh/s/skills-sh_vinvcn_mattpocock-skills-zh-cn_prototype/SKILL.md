---
name: prototype
description: Build a throwaway prototype to flesh out a design before committing to it. Routes between two branches — a runnable terminal app for state/business-logic questions, or several radically different UI variations toggleable from one route. Use when the user wants to prototype, sanity-check a data model or state machine, mock up a UI, explore design options, or says "prototype this", "let me play with it", "try a few designs".
---

# Prototype

Prototype 是**用来回答一个问题的 throwaway code**。问题决定形状。

## Pick a branch

先识别正在回答哪个问题：来自用户 prompt、周围代码，或在用户在线时直接询问：

- **"Does this logic / state model feel right?"** → [LOGIC.md](LOGIC.md)。构建一个很小的交互式 terminal app，推动 state machine 跑过纸面上难以推理的 cases。
- **"What should this look like?"** → [UI.md](UI.md)。在单一路由上生成几种差异很大的 UI variations，并通过 URL search param 和浮动底栏切换。

这两个分支会产出非常不同的 artifacts；选错会浪费整个 prototype。如果问题确实模糊且用户不可达，默认选择更匹配周围代码的分支（backend module → logic；page 或 component → UI），并在 prototype 顶部说明假设。

## Rules that apply to both

1. **从第一天就是 throwaway，并明确标记。** Prototype code 要靠近它实际会被使用的位置（放在被 prototype 的 module 或 page 旁边），这样上下文清楚；但命名要让随手读代码的人看出它是 prototype，不是 production。对 throwaway UI routes，遵守项目现有 routing convention；不要发明新的顶层结构。
2. **一个命令即可运行。** 使用项目现有 task runner 支持的东西：`pnpm <name>`、`python <path>`、`bun <path>` 等。用户必须能不动脑地启动它。
3. **默认不持久化。** State 保存在内存中。Persistence 是 prototype 要_检查_的东西，不该成为依赖。如果问题明确涉及 database，就用 scratch DB 或带有清晰 “PROTOTYPE — wipe me” 名称的本地文件。
4. **跳过 polish。** 不写 tests，不做超过“能跑起来”所需的 error handling，不做 abstractions。重点是快速学到东西，然后删掉。
5. **暴露 state。** 每次 action（logic）或每次 variant switch（UI）后，打印或渲染完整相关 state，让用户看到发生了什么变化。
6. **完成后删除或吸收。** 当 prototype 回答了问题，要么删掉它，要么把验证过的决策折进真实代码；不要让它在 repo 里腐烂。

## When done

Prototype 里唯一值得保留的是_答案_。把它和所回答的问题一起记录到持久位置（commit message、ADR、issue，或 prototype 旁边的 `NOTES.md`）。如果用户在线，这个记录可以是一段快速对话；如果不在线，留下 placeholder，让他们（或下一轮的你）在删除 prototype 前补上结论。
