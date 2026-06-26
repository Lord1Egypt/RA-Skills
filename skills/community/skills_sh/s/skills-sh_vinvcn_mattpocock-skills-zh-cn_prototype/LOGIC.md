# Logic Prototype

一个很小的交互式 terminal app，让用户手动驱动 state model。用于问题围绕 **business logic、state transitions 或 data shape** 的场景，也就是纸面上看起来合理，但只有跑过真实 cases 才会感觉哪里不对的东西。

## When this is the right shape

- "I'm not sure if this state machine handles the edge case where X then Y."
- "Does this data model actually let me represent the case where..."
- "I want to feel out what the API should look like before writing it."
- 任何用户想**按按钮并观察 state 变化**的情况。

如果问题是 “what should this look like”，这是错误分支。使用 [UI.md](UI.md)。

## Process

### 1. State the question

写代码前，先写下你正在 prototype 哪个 state model、回答什么问题。一段即可，放在 prototype 的 README，或文件顶部 comment。回答错问题的 logic prototype 纯属浪费；把问题显式写出来，这样无论用户现在旁观，还是之后 AFK 回来看，都能检查。

### 2. Pick the language

使用 host project 使用的语言。如果项目没有明显 runtime（例如 docs repo），询问用户。

匹配项目现有 tooling conventions；不要为了 prototype 增加新的 package manager 或 runtime。

### 3. Isolate the logic in a portable module

把真正的 logic，也就是回答问题的那部分，放在一个小而纯粹的 interface 后面，让它之后可以被拿出来放进真实 codebase。包在外面的 TUI 是 throwaway；logic module 不应该是。

合适形状取决于问题：

- **Pure reducer** — `(state, action) => state`。适合 actions 是离散 events、state 是单个值的场景。
- **State machine** — 显式 states 和 transitions。适合 “现在到底哪些 actions 合法” 本身就是问题的一部分。
- **一组作用于 plain data type 的 pure functions**。适合没有隐式 current state，只有 transformations 的场景。
- **Class 或带清晰 method surface 的 module**，当 logic 确实拥有持续的 internal state。

选择最适合问题的形状，而不是最容易接到 TUI 上的形状。保持 pure：不要 I/O，不要 terminal code，不要用 `console.log` 做 control flow。TUI import 它并调用它；不要反向依赖。

这让 prototype 在自身生命周期之后仍有价值。当问题被回答后，验证过的 reducer / machine / function set 可以被搬进真实 module；TUI shell 删除。

### 4. Build the smallest TUI that exposes the state

把它做成**轻量 TUI**：每个 tick 清屏（`console.clear()` / `print("\033[2J\033[H")` / 等价方式），并重新渲染整帧。用户应该始终看到一个稳定 view，而不是不断增长的 scrollback。

每一帧按顺序包含两部分：

1. **Current state**，pretty-printed 且 diff-friendly（每行一个 field，或 formatted JSON）。对 field names 或 section headers 使用 **bold**，对不太重要的 context（timestamps、IDs、derived values）使用 **dim**。原生 ANSI escape codes 就可以：`\x1b[1m` bold，`\x1b[2m` dim，`\x1b[0m` reset。除非项目已经有 styling library，否则不用引入。
2. **Keyboard shortcuts**，列在底部：`[a] add user  [d] delete user  [t] tick clock  [q] quit`。可以让 key 加粗、description 变 dim，或反过来；只要读起来清楚。

Behaviour：

1. **Initialise state** — 一个 in-memory object/struct。启动时渲染第一帧。
2. **一次读取一个 keystroke（或一行）**，dispatch 到 handler 来 mutate state。
3. **每个 action 后重新渲染**完整帧；不要 append，要 replace。
4. **循环直到 quit。**

整帧应能放进一个屏幕。

### 5. Make it runnable in one command

把 script 加到项目现有 task runner（`package.json` scripts、`Makefile`、`justfile`、`pyproject.toml`）。用户应该运行 `pnpm run <prototype-name>` 或等价命令；永远不需要记路径。

如果 host project 没有 task runner，就把命令写在 prototype README 顶部。

### 6. Hand it over

给用户 run command。让他们自己驱动；真正有趣的时刻是他们说 “wait, that shouldn't be possible” 或 “huh, I assumed X would be different” 的时候。这些是*想法*里的 bug，也正是 prototype 的目的。如果他们想添加新 actions，就添加。Prototypes 会演进。

### 7. Capture the answer

Prototype 完成任务后，唯一值得保留的是问题的答案。如果用户在线，询问它教会了他们什么。如果不在线，在 prototype 旁边留下 `NOTES.md`，让答案可以在 prototype 被删除前补上（或由你在看过 session 后补上）。

## Anti-patterns

- **不要加 tests。** 需要 tests 的 prototype 已经不再是 prototype。
- **不要接真实 database。** 除非问题专门关于 persistence，否则使用 in-memory store。
- **不要 generalise。** 不要做 “what if we wanted to support X later”。Prototype 回答一个问题。
- **不要把 logic 和 TUI 混在一起。** 如果 reducer / state machine 引用了 `console.log`、prompts 或 terminal escape codes，它就不再 portable。让 TUI 作为 pure module 外面的薄 shell。
- **不要把 TUI shell 发到 production。** Shell 是为手动 terminal 驱动优化的。它背后的 logic module 才是值得保留的部分。
