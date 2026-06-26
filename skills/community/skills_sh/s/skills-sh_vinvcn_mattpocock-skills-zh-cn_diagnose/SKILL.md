---
name: diagnose
description: 面向棘手 bug 和性能回退的纪律化 diagnosis loop。Reproduce → minimise → hypothesise → instrument → fix → regression-test. Use when user says "diagnose this" / "debug this", reports a bug, says something is broken/throwing/failing, or describes a performance regression.
---

# Diagnose

处理困难 bug 的纪律。只有在理由明确时才跳过阶段。

## Phase 1 — Build a feedback loop

**这就是这个 skill 的核心。** 其他部分都是机械流程。如果你有一个快速、确定、agent 可运行的 pass/fail 信号来覆盖这个 bug，你就能找到原因；bisection、hypothesis-testing 和 instrumentation 都只是消费这个信号。没有它，盯着代码看再久也救不了你。

在这里投入不成比例的精力。**要主动。要有创造性。不要轻易放弃。**

### 构造反馈环的方式，按大致顺序尝试

1. **Failing test**，放在能触达 bug 的 seam 上，可以是 unit、integration、e2e。
2. 针对运行中 dev server 的 **Curl / HTTP script**。
3. 带 fixture input 的 **CLI invocation**，把 stdout 和已知正确 snapshot 做 diff。
4. **Headless browser script**（Playwright / Puppeteer），驱动 UI，并断言 DOM/console/network。
5. **Replay a captured trace.** 把真实 network request、payload 或 event log 存到磁盘，隔离重放到对应 code path。
6. **Throwaway harness.** 启动系统的最小子集（一个 service、mocked deps），用一次函数调用触发 bug code path。
7. **Property / fuzz loop.** 如果 bug 是“有时输出错误”，运行 1000 个随机输入来寻找失败模式。
8. **Bisection harness.** 如果 bug 出现在两个已知状态之间（commit、dataset、version），自动化“在状态 X 启动、检查、重复”，这样可以 `git bisect run`。
9. **Differential loop.** 对同一输入分别运行 old-version vs new-version（或两组 configs）并 diff 输出。
10. **HITL bash script.** 最后手段。如果必须有人点击，用 `scripts/hitl-loop.template.sh` 驱动_人_，让循环仍然结构化。捕获的输出再反馈给你。

构建正确的反馈环，bug 就已经修好 90%。

### 迭代反馈环本身

把反馈环当作一个产品。有了_某个_循环之后，问：

- 我能让它更快吗？（缓存 setup、跳过无关 init、缩小 test scope。）
- 我能让信号更尖锐吗？（断言具体症状，而不是“没有崩溃”。）
- 我能让它更确定吗？（固定时间、固定 RNG seed、隔离 filesystem、冻结 network。）

30 秒且 flaky 的循环只比没有循环好一点点。2 秒且确定的循环是调试超能力。

### 非确定性 bug

目标不是干净复现，而是**提高复现率**。把触发器循环 100 次，并行化、加压、缩窄 timing windows、注入 sleeps。50% flake 的 bug 可以调试；1% 不行。持续提高复现率，直到它可调试。

### 当你确实无法构建循环

停下来并明确说明。列出你尝试过的方式。向用户请求：(a) 可复现环境的访问权限，(b) 捕获的 artifact（HAR file、log dump、core dump、带时间戳的 screen recording），或 (c) 添加临时 production instrumentation 的许可。**不要**在没有循环时继续 hypothesise。

在你有一个可信的循环之前，不要进入 Phase 2。

## Phase 2 — Reproduce

运行循环。看到 bug 出现。

确认：

- [ ] 循环产生的是**用户**描述的 failure mode，而不是附近的另一个失败。Wrong bug = wrong fix。
- [ ] 失败能在多次运行中复现；对非确定性 bug，则复现率足够高，可以据此调试。
- [ ] 你已经捕获精确症状（error message、wrong output、slow timing），后续阶段能验证 fix 确实解决了它。

复现 bug 之前不要继续。

## Phase 3 — Hypothesise

在测试任何假设前，先生成 **3-5 个排序后的 hypotheses**。只生成一个假设会把你锚定在第一个看起来合理的想法上。

每个 hypothesis 必须是**可证伪的**：说明它产生的预测。

> 格式："If <X> is the cause, then <changing Y> will make the bug disappear / <changing Z> will make it worse."

如果你说不出预测，这个 hypothesis 就是 vibe。丢掉或收紧。

**在测试前把排序列表展示给用户。** 他们通常有 domain knowledge，可以瞬间重排（“我们刚部署了 #3 的改动”），或知道哪些假设已经被排除。这个 checkpoint 便宜但省时。不要阻塞在这里；如果用户 AFK，就按你的排序继续。

## Phase 4 — Instrument

每个 probe 都必须映射到 Phase 3 中的一个具体预测。**一次只改一个变量。**

工具偏好：

1. 如果环境支持，优先用 **Debugger / REPL inspection**。一个 breakpoint 胜过十条 log。
2. 在能区分 hypotheses 的边界上加 **targeted logs**。
3. 永远不要“log everything and grep”。

**给每条 debug log 加唯一前缀**，例如 `[DEBUG-a4f2]`。最后清理就变成一次 grep。无标签 log 会留下；有标签 log 会消失。

**Perf branch.** 对性能回退，logs 通常不合适。先建立 baseline measurement（timing harness、`performance.now()`、profiler、query plan），然后 bisect。先测量，再修复。

## Phase 5 — Fix + regression test

在 fix 之前写 regression test，但前提是存在**正确的 seam**。

正确 seam 是指 test 能在 call site 复现**真实 bug pattern**。如果唯一可用的 seam 太浅（bug 需要多个 caller 但测试只有单一 caller；unit test 无法复制触发 bug 的链路），那里的 regression test 会带来虚假信心。

**如果没有正确 seam，这本身就是发现。** 记录它。codebase architecture 正在阻止这个 bug 被锁住。把它标记到下一阶段。

如果存在正确 seam：

1. 把 minimised repro 转成这个 seam 上的 failing test。
2. 看它失败。
3. 应用 fix。
4. 看它通过。
5. 针对原始（未 minimised）场景重新运行 Phase 1 feedback loop。

## Phase 6 — Cleanup + post-mortem

宣布完成前必须做：

- [ ] 原始 repro 不再复现（重新运行 Phase 1 loop）
- [ ] Regression test 通过（或已记录没有 seam）
- [ ] 所有 `[DEBUG-...]` instrumentation 已删除（grep 前缀）
- [ ] Throwaway prototypes 已删除，或移到明确标记的 debug 位置
- [ ] 在 commit / PR message 中说明最终正确的 hypothesis，方便下一个调试者学习

**然后问：什么本可以防止这个 bug？** 如果答案涉及 architecture change（没有好的 test seam、callers 缠绕、隐藏 coupling），带着具体信息交给 `/improve-codebase-architecture` skill。建议应在 fix 落地后提出，而不是之前；现在你掌握的信息比开始时更多。
