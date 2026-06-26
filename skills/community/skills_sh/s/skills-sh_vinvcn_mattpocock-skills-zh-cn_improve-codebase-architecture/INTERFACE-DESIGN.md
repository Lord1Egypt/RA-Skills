# Interface Design

当用户想为选中的 deepening candidate 探索替代 interfaces 时，使用这个 parallel sub-agent pattern。基于 “Design It Twice”（Ousterhout）：你的第一个想法很可能不是最好的。

使用 [LANGUAGE.md](LANGUAGE.md) 中的词汇：**module**、**interface**、**seam**、**adapter**、**leverage**。

## Process

### 1. Frame the problem space

在生成 sub-agents 前，先为选中的 candidate 写一段面向用户的问题空间说明：

- 新 interface 必须满足的 constraints
- 它依赖哪些 dependencies，以及它们属于哪个 category（见 [DEEPENING.md](DEEPENING.md)）
- 一个粗略 illustrative code sketch，用来让 constraints 具体化；这不是 proposal，只是帮助理解 constraints

把它展示给用户，然后立即进入 Step 2。用户阅读和思考时，sub-agents 并行工作。

### 2. Spawn sub-agents

使用 Agent tool 并行生成 3+ 个 sub-agents。每个都必须为 deepened module 产出一个**根本不同**的 interface。

给每个 sub-agent 单独的 technical brief（file paths、coupling details、[DEEPENING.md](DEEPENING.md) 中的 dependency category、seam 后面是什么）。brief 独立于 Step 1 中面向用户的问题空间说明。给每个 agent 不同的 design constraint：

- Agent 1: "Minimize the interface — aim for 1–3 entry points max. Maximise leverage per entry point."
- Agent 2: "Maximise flexibility — support many use cases and extension."
- Agent 3: "Optimise for the most common caller — make the default case trivial."
- Agent 4 (if applicable): "Design around ports & adapters for cross-seam dependencies."

在 brief 中同时包含 [LANGUAGE.md](LANGUAGE.md) 词汇和 CONTEXT.md 词汇，让每个 sub-agent 使用 architecture language 和项目 domain language 一致命名。

每个 sub-agent 输出：

1. Interface（types、methods、params，以及 invariants、ordering、error modes）
2. Usage example，展示 callers 如何使用它
3. Implementation 在 seam 后面隐藏什么
4. Dependency strategy 和 adapters（见 [DEEPENING.md](DEEPENING.md)）
5. Trade-offs：哪里 leverage 高，哪里薄

### 3. Present and compare

顺序展示 designs，让用户能吸收每个方案，然后用 prose 比较。按 **depth**（interface 上的 leverage）、**locality**（change 集中在哪里）和 **seam placement** 对比。

比较后给出你自己的 recommendation：你认为哪个 design 最强，以及为什么。如果不同 designs 的元素可以很好组合，就提出 hybrid。要有判断力；用户要的是明确判断，不是菜单。
