# agent 适配层（adapters/index.md）

**要解决的问题**：技能要在多个 agent 里跑，而这几个东西**每个 agent 都不一样、且都是私有实现**——会话 id 长什么样、会话记录存在哪、记录是明文还是压缩、token 读数从哪取。旧版把这些硬写进 SKILL.md，结果是「WorkBuddy 的 UUID 格式成了通用协议」，换个 agent 就失效，且改一处要动主流程。

**解法**：主流程只认 **5 个接口**，具体实现分给 adapter 文件。SKILL.md / schema.md 里**不出现任何一家产品的字段名、路径、id 格式**。新增 agent = 加一个 md，不动主流程。

## 1. 五个接口

主流程需要知道的全部信息：

| 接口 | 返回 | 用途 | 取不到时 |
|---|---|---|---|
| `agent_name` | 官方显示名（`WorkBuddy` / `WorkBuddy AI` / `DeepSeek Harness` / `Claude Code`） | 文件名、条目、文件源段 | **必填**，取不到 → 标 `未知 agent` 进缺口段 |
| `session_id` | 该会话的唯一标识，**不含空格与下划线** | 文件名 | 用 `unknown-YYYYMMDD-HHMM`（见 schema.md §1.3） |
| `session_record_path` | 当前会话记录文件的绝对路径 | 文件源段、S3/S5 核对 | 空 → 该文件不可溯源，不冻结、不判缺口 |
| `record_format` | `jsonl` / `jsonl.gz` / `jsonl.zstd` / 其他 | 决定能否 grep 补历史 | 非明文 → **禁止自动补写**，只报缺口 |
| `token_output` | 最近一个完整轮的输出 token 数，或空 | 落款括号 | 空 → 省略括号 |

**外加两个可选接口**（只有补历史 / 缺档扫描用）：

| 接口 | 返回 | 用途 |
|---|---|---|
| `record_dir` | 该 agent 所有会话记录的根目录 | S6 缺档扫描、查缺口时定位 |
| `user_turn_extract` | 从记录行提取用户原话的规则 | 补历史时捞命中行 |

## 2. 契约（所有 adapter 必须遵守）

1. **失败要返回空值并说明原因，不许抛错中断主流程**——adapter 拿不到信息，技能要能降级继续，而不是整个动作失败。
2. **不猜**：取不到就是取不到，返回空。**禁止**「扫一遍进程列表挑个像的」「看目录里已有文件名反推」。这两条是旧版两次错标事故的直接成因。
3. **不许改来源数据**：adapter 只读会话记录，**永不写入**。
4. **路径必须运行时获取**，不许在 adapter 文件里写死具体机器的绝对路径（技能本体不写绝对路径，adapter 也不例外——写的是「去哪找」的规则，不是「在这」的常量）。
5. **降级必须无损**：拿不到私有能力时，核心功能（写文件、读文件、渲染报告）照常工作。少掉的只能是便利（token 读数、自动补写），不能是正确性。

## 3. 已有 adapter

| 文件 | 覆盖 | 会话 id | 记录格式 | token 读数 |
|---|---|---|---|---|
| [workbuddy.md](workbuddy.md) | WorkBuddy / WorkBuddy AI 系 | `CODEBUDDY_SESSION_ID`（十六进制 UUID） | `jsonl` | `model-call-parse` 脚本 |
| [deepseek-harness.md](deepseek-harness.md) | DeepSeek Harness（DSH） | 从记录路径派生 | `jsonl.zstd` | `projcache` 读数（不稳定） |
| [generic.md](generic.md) | 其余一切（Claude Code / Codex / Cursor / Gemini / Trae / Kimi …） | 现场探测 | 现场探测 | 通常取不到 |

adapter 选择固定为按宿主环境变量自动匹配。**探测失败 → 用 `generic` 并回报一行**，不中断。

## 4. 新增 agent 的步骤

1. 在 `adapters/` 下新建 `<名字>.md`，按 `generic.md` 的结构填全五个接口；
2. 只写「去哪找 / 长什么样」，**不写解析器代码**（本技能零脚本）；
3. 在 §3 表格加一行；
4. **不动 SKILL.md、不动 schema.md**——如果发现必须改主流程才能支持，说明接口设计有问题，应该改接口而不是打补丁。

## 5. 为什么分文件而不是一张大表

一张大表看似紧凑，但每次改某个 agent 的探测规则都要动同一份文件，而这些规则彼此无关、改动频率也不一致。分文件后：

- 用户只用 WorkBuddy 时，`adapters/workbuddy.md` 是唯一相关文件，其余可以整份删掉而技能照常工作（每个 adapter 都是**可丢弃**的）；
- 新 agent 的支持可以单独增删，不产生「表格里删了一行但下面还有半句引用」的残留；
- 各家的私有细节（DSH 的 `session.v4.jsonl.zstd`、WorkBuddy 的双配置根）互不污染。
