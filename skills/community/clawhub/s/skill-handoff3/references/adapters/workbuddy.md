# WorkBuddy / WorkBuddy AI 适配（adapters/workbuddy.md）

覆盖 WorkBuddy 桌面端与 WorkBuddy AI，两者**除配置根不同外完全一致**。本文件是这类宿主的唯一实现说明；删掉它技能仍可运行（会退化到 `generic.md`）。

## 1. 五个接口

### 1.1 `agent_name`

**唯一权威判据：当前会话记录文件真实落在哪个配置根。**

```
取会话 id（见 1.2）
在 ~/.workbuddy/projects/ 与 ~/.workbuddy-ai/projects/ 下递归找 <id>.jsonl
  → ~/.workbuddy/     下找到 → agent_name = "WorkBuddy"
  → ~/.workbuddy-ai/  下找到 → agent_name = "WorkBuddy AI"
两边都存在或都不存在 → "未知 agent"，进缺口段，不挑
```

**不要猜项目 slug**——`projects/` 下的子目录名是项目路径的压缩形式，与其去推断压缩规则，不如直接递归找文件名（会话 id 唯一）。

**为什么不能用别的方法**（都是实测排除过的）：

| 方法 | 为何不可靠 |
|---|---|
| 扫全局进程名 | 两个客户端常同时运行（`WorkBuddy.exe` 与 `WorkBuddyAI.exe` 并存），只看得到「两个都在」 |
| 会话记录内的元数据 | 两者 `session-meta.meta` 完全相同（都是 `codebuddy.ai/hostKind: unopted`），**从内容分不出来** |
| 工具集特征 / 系统提示措辞 / 用户说了什么 | 纯猜测，无因果关系 |
| `$LIB` 里已有文件名 | 历史产物，可能一开始就标错了（已踩过两次） |

**环境变量只做定位加速，不单独定名**：`WORKBUDDY_CONFIG_DIR` / `CODEBUDDY_PROJECT_CONFIG_DIR` / `WORKBUDDY_DATA_FOLDER_NAME`。判定顺序 **先 `workbuddy-ai` 再 `.workbuddy`**（后者是前者的子串，顺序反了会把 `workbuddy-ai` 误判成 `workbuddy`）。与文件存在性冲突时**以文件为准**，并把冲突值写进缺口段。`CLIENT_INFO_PRODUCT_NAME` / `WORKBUDDY_PRODUCT_NAME` 只做核对。

**写入边界（通用，不针对某个客户端）**：WorkBuddy 与 WorkBuddy AI 是独立 agent，各自记忆目录属于对方、**只读、永不写**；判定结果的用途只是定 `mem_` 文件名与"参考记忆"时的读取来源，不构成对 `$LIB` 外任何目录的写入授权。写入只限 `$LIB` 内（见 SKILL.md 硬规则 10）。

### 1.2 `session_id`

取环境变量 `CODEBUDDY_SESSION_ID`，形如 `a224e4fd-1509-42b7-9eb2-7de8f4903e72`（十六进制 `8-4-4-4-12`）。

**这是本产品的私有格式，不是本技能的通用约定。** schema.md §1.2 的解析算法刻意**不用 UUID 正则**，正是为了不把这里写死成协议：文件名里的会话标识只是「最后一个下划线之后的原样字符串」，它是不是 UUID 与本技能无关。

取不到（变量缺失）→ 按 schema.md §1.3 用 `unknown-YYYYMMDD-HHMM`，且该文件不得进入 `已沉淀`。

### 1.3 `session_record_path`

```
<配置根>/projects/<项目 slug>/<session_id>.jsonl
```

配置根来自 1.1 的判定结果。**运行时拼出真实路径，不编造**。文件源段写这个绝对路径（schema.md §5 第 4 档）。

### 1.4 `record_format`

`jsonl`（明文，一行一 JSON）。**可 grep，允许自动补写。**

行结构与用户原话提取规则见 §2。

### 1.5 `token_output`

用 `model-call-parse` 技能取最新完整一轮的输出 token 数（脚本由该技能提供，路径运行时按其安装位置拼，不写死）。

- **只取最新一轮**，不加全场累计——落款要的是本轮输出；
- 取不到（技能不存在、执行失败、宿主无 python）→ 返回空，落款省略括号；
- **绝不因为取不到就中断动作**，也不写 `N/A` 冒充。

## 2. 会话记录格式与用户原话提取

记录为 JSONL，每行 `{type, role, content[], payload}`，`type` 常见 `message` / `reasoning` / `function_call` / `function_call_result` / `session-meta`。`timestamp` 是**毫秒整数**（如 `1794582146873`），换算秒要 `/1000`——**这是补历史比对时间的关键，忘了会差三个数量级**。

**用户原话提取规则（实测 82MB / 18361 行会话得出，必须照做，否则会把系统注入当决策）**：

1. `content` 是**数组**，用户文字在 `{type:"input_text"|"text", text:"..."}` 里——不是裸字符串，也不只有 `text` 一种 type。
2. 以下三类是**系统注入，必须丢弃**：
   - `text` 以 `<cb_summary>` / `<conversation_history_summary>` 开头的压缩摘要；
   - 以 `<system-reminder>` 开头的提醒；
   - 单独的 `Please continue with the conversation based on the summarized context above.` 续接提示。
3. 真实用户原话在 `<user_query>...</user_query>` **标签内部**——取标签内容（去掉包裹标签本身），不整段取 `text`。一个 `text` 里可能有多段 `<user_query>`，逐段取。
4. 实测分布（82MB / 18361 行）：`user_query` 311 条（真原话）、`summary_drop` 17、`other_inject` 21、`plain` 12。**禁止**用「`startswith('<')` 就过滤」这类偷懒规则——会误杀全部 311 条原话。
5. 提取后再按关键词筛；**扫全文件不花 token，只有命中行进上下文**。

## 3. 可选接口

### 3.1 `record_dir`

```
~/.workbuddy/projects/     （WorkBuddy）
~/.workbuddy-ai/projects/  （WorkBuddy AI）
```

S6 缺档扫描只扫**当前 agent 的那个根**，不扫另一个（别人的会话不归我管），更不扫全盘。

### 3.2 `user_turn_extract`

即 §2 的规则。补历史时用它从命中行里取原话。

## 4. 平台能力与不采用的特性

### 4.1 实际用到的

1. **description 软自动触发**：常驻指针写在 `description` 里，模型每轮都能看见——五个动作的调用形式与触发词已外置到 `references/commands.md`，由模型按需加载。触发靠「常驻指针 + 动作表」，不是后台钩子，也不是靠超长 description 堆触发词。
2. **渐进披露**：`references/` 按需加载，不占常驻预算。
3. **`model-call-parse` 取 token**：宿主私有增强，其他 agent 取不到就省略括号，功能不减。

### 4.2 明确不用的平台特性（防复发）

`hooks`（受 admin-trusted 闸门约束）、`context: fork`（在独立 subagent 里跑、**不访问对话历史**，与「读本轮做记忆」互斥）、内联 shell 命令（是脚本，破坏跨 agent 通用）、变量占位符 `${CODEBUDDY_SESSION_ID}`（未设置时原样保留、不被替换，跨宿主会把字面量原样塞进上下文）、`skillOverrides`（CLI 功能、桌面端未验证）、`agent_created`（只是「允许自动改删」标记，与触发无关）——一律不用。

### 4.3 三套规范别混

本机技能装在 `~/.workbuddy/skills/`，CLI 文档讲的是 `~/.codebuddy/skills/`——配置目录不同，不要混写。开放平台打包字段（8 必填）只在上架市场时才需要；三级渐进披露已是本技能采用的规范。

## 5. 补充：库里已有文件名不是判据（防复发）

这一条已实际踩过两次，写在这里而不是只在 schema.md：

- 目录里已有的 `mem_*.md` 文件名、以及它「文件源」段写的 agent 名，**都不能**用来推断当前 agent；
- 尤其防「空库里只有一个历史文件」——首次启用、目录刚建、只剩一个文件时最容易被它的名字带跑，此时**必须**照 1.1 重新判定；
- 判定结果与目录实际文件不一致时：**按判定结果写进正确的文件**（不存在就新建），**旧文件一律不动**（不删、不改名、不合并、不往里写），并用一句话告诉用户「判定为 X，库里已有 mem_Y.md，已写入 mem_X.md，旧文件未改动，是否合并由你决定」；
- 绝不静默沿用旧文件名（整库归属错位），也绝不静默新建第二个文件而不告知（记忆分裂）；
- 改名 / 合并 / 删除只能由用户明确要求后执行，按「不覆盖、不合并」处理。

本版改为一会话一文件后，同一会话**连续**写同一文件，这个坑的频率下降了，但**首轮判定**仍是首次进入任何项目时的必经步骤，规则不能省。
