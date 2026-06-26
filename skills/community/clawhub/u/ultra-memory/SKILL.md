---
name: ultra-memory
description: >
  ultra-memory 给 AI Agent 提供跨会话记忆。每次操作后自动记录，会话结束后可恢复，支持按关键词检索历史操作。
  【必须触发-中文】用户说以下任意词：记住、别忘了、记录一下、不要忘记、上次我们做了什么、帮我回忆、继续上次的、从上次继续、记忆、帮我记、追踪进度
  【必须触发-英文】用户说以下任意词：remember、don't forget、recall、what did we do、pick up where we left off、continue from last time、memory、keep track、track progress、log this
  【隐式触发-A+B】同时满足以下两条时触发：(A)消息含持续性任务动词：开发、实现、处理、完成、构建、develop、implement、create、fix；(B)消息中包含项目名词（专有名词/文件名/系统名）
  【不触发】用户只问一个问题无后续；单次咨询无操作步骤；说"随便聊聊"、"just chatting"；明确说"不用记录"
---

# Ultra Memory — 多模型记忆操作手册

AI Agent 的操作记忆系统，每次操作后记录，跨会话持久化，可检索可进化。

## 前置说明

脚本位于 `$SKILL_DIR/scripts/`，直接调用，不需要生成，不需要理解内部架构。

- `ULTRA_MEMORY_HOME` 默认值为 `~/.ultra-memory/`
- `SKILL_DIR` 解析顺序见步骤零

---

## 步骤零：环境探测

**每次触发条件满足后，第一件事执行此步骤，决定运行模式。**

### 1. 解析 SKILL_DIR

```bash
# 按顺序尝试，取第一个找到 init.py 的路径
for _d in \
  "${SKILL_DIR}" \
  "${ULTRA_MEMORY_SKILL_DIR}" \
  "${HOME}/ultra-memory" \
  "${HOME}/.openclaw/workspace/skills/ultra-memory" \
  "$(npm root -g 2>/dev/null)/ultra-memory"; do
  if [ -f "${_d}/scripts/init.py" ]; then
    export SKILL_DIR="${_d}"
    echo "SCRIPT_AVAILABLE:${SKILL_DIR}"
    break
  fi
done
```

### 2. 判断运行模式

| 输出 | 运行模式 | 后续行为 |
|------|---------|---------|
| `SCRIPT_AVAILABLE:<路径>` | **脚本模式** | 按步骤一至七正常执行 |
| 无任何输出 / 命令不可执行 | **无脚本模式** | 跳转到附录 E 执行，不再调用任何脚本 |

无脚本模式的典型场景：claude.ai web、无文件系统的在线 LLM 平台。

---

## 步骤一：会话初始化

### 触发条件

满足 frontmatter 中任意触发规则时，第一件事执行此步骤。

### 执行命令

```bash
python3 $SKILL_DIR/scripts/init.py --project <项目名> --resume [--scope <scope>]
```

**参数说明：**
- `--project`：项目名称。从用户最近一条消息中提取最显著的名词作为值；无法提取则用 `default`。
- `--resume`：必须加此参数，让脚本尝试恢复同项目的最近会话。
- `--scope`（可选）：隔离空间，用于多用户或多 Agent 场景。格式：`user:alice`、`agent:bot1`、`project:myapp`。不同 scope 的记忆完全隔离，互不干扰。省略时使用默认共享空间。

### 成功标志

| 输出中的字符串 | 模型必须执行的动作 |
|-------------|----------------|
| `MEMORY_READY` | 确认初始化成功 |
| `session_id: sess_xxxxx` | 从该行冒号后提取值，保存为 `SESSION_ID` |

### 有上次会话摘要时

将摘要内容告知用户，并询问："要从这里继续吗？"

---

## 步骤二：操作记录

### 触发条件

**每次**用户与 AI 之间发生以下任意事件后，立即调用：

| 刚发生了什么 | op_type |
|-------------|---------|
| 调用了任何工具 | `tool_call` |
| 创建或修改了文件 | `file_write` |
| 读取了文件 | `file_read` |
| 执行了 shell 命令 | `bash_exec` |
| 做出了重要判断或选择方案 | `reasoning` |
| 用户给出了新指令或改变了目标 | `user_instruction` |
| 做出了技术或方案决策 | `decision` |
| 发生了错误或需要回退 | `error` |
| 完成了一个明确的阶段目标 | `milestone` |

### 执行命令

```bash
python3 $SKILL_DIR/scripts/log_op.py \
  --session $SESSION_ID \
  --type <op_type> \
  --summary "<用一句话描述刚才做了什么，50字内>" \
  --detail '{"key": "value"}' \
  --tags "tag1,tag2"
```

`--detail` 和 `--tags` 可省略，`--summary` 和 `--type` 必填。

### 示例

```bash
# 执行 bash 命令后
python3 $SKILL_DIR/scripts/log_op.py \
  --session $SESSION_ID \
  --type bash_exec \
  --summary "执行 pip install pandas，成功，版本 2.2.0" \
  --detail '{"cmd": "pip install pandas", "exit_code": 0}'

# 完成阶段目标后
python3 $SKILL_DIR/scripts/log_op.py \
  --session $SESSION_ID \
  --type milestone \
  --summary "数据清洗模块完成，通过全部单元测试"
```

### 成功标志

命令返回 exit code 0。

看到 `COMPRESS_SUGGESTED`：立即执行步骤四。

---

## 步骤三：记忆检索

### 触发条件

用户问及以下任意问题时立即执行：
之前、上次、那个函数、那个文件、那个命令、我们做过、怎么写的、什么名字、previously、last time、what was、how did we、that function、that file

### 执行命令

```bash
python3 $SKILL_DIR/scripts/recall.py \
  --session $SESSION_ID \
  --query "<从用户问题中提取的关键词>" \
  --top-k 5
```

**高级用法：**

```bash
# 时间旅行：查询指定时间点的知识状态（如"上周我们的决策是什么"）
python3 $SKILL_DIR/scripts/recall.py \
  --session $SESSION_ID \
  --query "..." \
  --as-of 2026-03-01T00:00:00Z

# 实体历史：查看同名实体的所有版本变迁
python3 $SKILL_DIR/scripts/recall.py \
  --session $SESSION_ID \
  --history "clean_df"
```

### 结果展示

将脚本输出原样展示给用户，不加工。

---

## 步骤四：摘要压缩

### 触发条件

满足以下**任意条件**时，立即执行：

1. 步骤二中脚本输出了 `COMPRESS_SUGGESTED`
2. 用户说：总结一下、目前进展、Summary、summarize
3. 当前对话已超过 **30 轮**

### 执行命令

```bash
python3 $SKILL_DIR/scripts/summarize.py --session $SESSION_ID
```

条数不足时强制执行：
```bash
python3 $SKILL_DIR/scripts/summarize.py --session $SESSION_ID --force
```

### 成功标志

命令返回 exit code 0，输出包含 `摘要压缩完成`。

---

## 步骤五：跨会话恢复

### 触发条件

用户说以下任意表达时触发：
继续昨天的、接着上次、从上次开始、继续之前的、continue from last、pick up where、resume、continue yesterday

### 执行命令

```bash
python3 $SKILL_DIR/scripts/restore.py --project <项目名>
```

### 从输出提取信息

| 输出中的字符串 | 模型必须执行的动作 |
|-------------|----------------|
| `SESSION_ID=sess_xxxxx` | 从等号后提取值，更新为新的 `SESSION_ID` |
| `TASK_STATUS=complete` | 告知用户"上次任务已完成" |
| `TASK_STATUS=in_progress` | 告知用户"上次任务进行中" |
| `💬 <自然语言总结>` | 直接说给用户 |
| `📌 <继续建议>` | 直接说给用户 |

将恢复内容告知用户，询问："要从这里继续吗？"

---

## 步骤六：记忆进化

记忆进化在操作间隙进行，不打断主任务。

### 6A：用户画像积累

**触发条件（满足任意一条，立即更新）：**

1. 用户纠正了 AI 生成的代码风格
2. 用户在两个方案中选择了其中一个
3. 用户说出自己的技术栈（含"我用"、"我们用"、"我们的项目用"、"we use"、"our stack"）
4. 用户表示某种工作方式更顺手
5. 用户明确描述了自己的偏好

**执行方式 — 方式 A（MCP 工具，推荐）：**

调用 `memory_profile`，`action=update`，`updates` 填写观察到的偏好字段。

**执行方式 — 方式 B（直接修改文件）：**

```bash
# 文件路径：$ULTRA_MEMORY_HOME/semantic/user_profile.json
# 只更新观察到的字段，不覆盖已有字段，使用 JSON merge 方式
```

**user_profile.json 可更新字段：**

```json
{
  "tech_stack": ["观察到的技术栈"],
  "language": "zh-CN 或 en",
  "work_style": {
    "confirm_before_implement": true,
    "prefers_concise_code": true
  },
  "observed_patterns": ["倾向先确认方案再实现"]
}
```

### 6B：知识沉淀

**触发条件（满足任意一条，立即写入知识库）：**

1. 解决了一个报错或 bug（记录问题现象 + 解决方案）
2. 做出了技术选型决策（选了什么 + 为什么）
3. 发现了某个工具或库的使用技巧
4. 完成了一个可复用的代码模式

**文件路径：**

```
$ULTRA_MEMORY_HOME/semantic/knowledge_base.jsonl
```

**执行方式 — 方式 A（MCP 工具，推荐）：**

调用 `memory_knowledge_add`，`title` 必填（20字内），`content` 必填（200字内），`project` 和 `tags` 可选。

**执行方式 — 方式 B（直接追加）：**

追加写入 `knowledge_base.jsonl`，每行一条 JSON，不覆盖。

**knowledge_base.jsonl 格式：**

```json
{"ts": "2026-04-07T10:00:00Z", "project": "项目名", "title": "20字内标题", "content": "200字内描述", "tags": ["tag1"]}
```

### 6C：里程碑记录

**触发条件 — 用户说出以下任意表达，立即记录：**

中文：好了、完成了、搞定了、做完了、弄好了、可以了、没问题了、测试通过、上线了

英文：done、finished、completed、it works、all good、passed、deployed、ready

**执行命令：**

```bash
python3 $SKILL_DIR/scripts/log_op.py \
  --session $SESSION_ID \
  --type milestone \
  --summary "<用户刚完成的事情，一句话描述>"
```

---

## 步骤七：元反思与进化

记忆积累不等于进化。进化需要对记忆做二次加工：提炼模式、纠正偏差、淘汰噪音。

### 7A：定期元反思

**触发条件（满足任意一条）：**

1. 当前会话里程碑累计达到 **5 个**（从 init.py 返回的 op_count 判断，每次 milestone 后检查）
2. 用户说：回顾一下、总结经验、我们学到了什么、reflect、what have we learned、review progress
3. 距上次元反思超过 **3 天**（从 user_profile.json 的 `last_reflection` 字段判断，不存在则视为从未反思过）

**执行步骤（按顺序执行，不可跳过）：**

**第一步：读取近期知识库**
```bash
# 读取最近 20 条知识库条目
tail -20 $ULTRA_MEMORY_HOME/semantic/knowledge_base.jsonl
```

**第二步：读取近期会话摘要**
```bash
# 读取当前会话摘要
cat $ULTRA_MEMORY_HOME/sessions/$SESSION_ID/summary.md 2>/dev/null || echo "暂无摘要"
```

**第三步：模型自主提炼（核心步骤）**

基于读取到的内容，模型执行以下判断，每一项都必须完成：

| 判断项 | 执行动作 |
|-------|---------|
| 发现两条或以上内容相似的知识条目 | 合并为一条更精炼的条目，写入 knowledge_base.jsonl，原条目加 `"merged": true` 标记 |
| 发现某个知识点在多次操作中反复出现 | 将其标记为 `"importance": "high"`，写回该条目 |
| 发现某条知识点超过 30 天未被检索且不是 high importance | 将其标记为 `"stale": true` |
| 发现用户行为与 user_profile.json 记录不符 | 更新 user_profile.json 对应字段，加 `"corrected_at"` 时间戳 |
| 总结出一个新的用户工作规律 | 追加到 user_profile.json 的 `observed_patterns` 数组 |

**第四步：写入反思记录**
```bash
python3 $SKILL_DIR/scripts/log_op.py \
  --session $SESSION_ID \
  --type reasoning \
  --summary "元反思完成：<一句话描述本次提炼了什么>" \
  --tags "reflection,evolution"
```

**第五步：更新反思时间戳**

将 `user_profile.json` 的 `last_reflection` 字段更新为当前 UTC 时间（ISO 格式）。

**第六步：告知用户（简短）**

用一句话告知用户反思结果。不需要展示完整报告，一句话即可，不打断主任务。

---

### 7B：错误修正

**触发条件（满足任意一条）：**

1. 用户说：不对、你记错了、不是这样的、纠正一下、wrong、that's not right、correct that
2. 用户描述的信息与 user_profile.json 中的记录明显矛盾

**执行步骤：**

**第一步：定位错误记录**
```bash
cat $ULTRA_MEMORY_HOME/semantic/user_profile.json
```

**第二步：模型判断需要修正的字段**

找到与用户当前描述矛盾的字段。

**第三步：修正并记录**

更新 user_profile.json 对应字段，同时在该字段旁追加：
```json
"_correction_note": "用户于 <日期> 纠正，原值为 <旧值>"
```

**第四步：记录修正操作**
```bash
python3 $SKILL_DIR/scripts/log_op.py \
  --session $SESSION_ID \
  --type decision \
  --summary "用户画像修正：<字段名> 从 <旧值> 改为 <新值>" \
  --tags "correction,profile"
```

**第五步：告知用户**

"好的，我已经更新了记录，<字段名> 现在是 <新值>。"

---

### 7C：知识蒸馏（每月一次）

**触发条件（必须同时满足，按顺序检查）：**

**先决条件（任一不满足则直接跳过，不读时间戳）：**

```bash
# 检查知识库是否存在且条目数 ≥ 10
[ -f "$ULTRA_MEMORY_HOME/semantic/knowledge_base.jsonl" ] \
  && [ "$(wc -l < "$ULTRA_MEMORY_HOME/semantic/knowledge_base.jsonl")" -ge 10 ] \
  && echo "KB_SUFFICIENT" || echo "KB_SKIP"
```

输出 `KB_SKIP` → 立即跳过本步骤，不执行后续任何检查。

**时间条件（先决条件通过后才检查）：**

读取 `user_profile.json` 的 `last_distillation` 字段：
- 字段不存在：视为"本机首次蒸馏"，触发一次
- 字段存在且距今 > **30 天**：触发
- 字段存在且距今 ≤ 30 天：跳过

> **为什么先检查知识库再检查时间戳：** 换机器或清存储后知识库为空，若先检查时间戳会因字段缺失而触发，但步骤一统计条目数后立即跳过，造成每次会话都执行无效检查。倒序检查后空库直接短路，不会误触发。

在步骤七 7A 执行完毕后，额外执行本步骤。

**执行步骤：**

**第一步：统计知识库规模（已在触发条件中完成，此处直接读结果）**

**第二步：提取高价值条目**

读取全部 knowledge_base.jsonl，筛选满足以下任意条件的条目：
- `"importance": "high"`
- `tags` 中包含 `"reusable"` 或 `"pattern"`
- 同一 `title` 关键词出现超过 2 次

**第三步：生成项目级知识摘要**

基于筛选出的条目，生成一段 200 字以内的项目级知识摘要，格式：

```json
{"ts": "<当前UTC时间>", "type": "distillation", "period": "<YYYY-MM>", "project": "<项目名>", "summary": "<200字以内的知识摘要>", "source_count": <来源条目数>, "tags": ["distillation"]}
```

追加写入 `knowledge_base.jsonl`。

**第四步：更新蒸馏时间戳**

将 `user_profile.json` 的 `last_distillation` 更新为当前 UTC 时间。

---

## 信号对照表

| 脚本输出 | 立即执行 |
|---------|---------|
| `MEMORY_READY` | 确认成功，继续主任务 |
| `session_id: sess_xxxxx` | 保存为 SESSION_ID |
| `COMPRESS_SUGGESTED` | 执行 summarize.py --session $SESSION_ID |
| `SESSION_ID=sess_xxxxx` | 更新 SESSION_ID 为该值 |
| 非零退出码 | 静默跳过，继续主任务 |
| `op_count` 达到 5 的倍数且含 milestone | 触发步骤 7A |
| user_profile.json `last_reflection` 距今 > 3 天 | 下次会话初始化后触发步骤 7A |

---

## 环境变量表

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `ULTRA_MEMORY_HOME` | `~/.ultra-memory/` | 记忆存储根目录；使用 scope 时自动切换到 `<HOME>/scopes/<scope>/` |
| `ULTRA_MEMORY_SESSION` | 空 | 当前会话 ID；配置后 Claude Code 自动捕获钩子（hook_capture.py）使用此值 |
| `SKILL_DIR` | clawbot 注入 | skill 安装目录；未定义时步骤零按 `~/ultra-memory` → `~/.openclaw/workspace/skills/ultra-memory` → `npm root -g` 顺序探测，均未找到则切换无脚本模式 |
| `ULTRA_MEMORY_SKILL_DIR` | 用户手动设置 | `SKILL_DIR` 的备用名，优先级低于 `SKILL_DIR`，高于路径探测 |
| `SESSION_ID` | init.py 执行后自动生成 | 当前会话 ID，保存后供后续所有命令使用 |

---

## 异常处理表

| 情况 | 处理方式 |
|------|---------|
| init.py 找不到上次会话 | 正常，作为新会话继续 |
| log_op.py 报会话不存在 | 重新执行 init.py，再记录 |
| SESSION_ID 丢失 | 执行 init.py --project <名> --resume 尝试恢复 |
| 任意脚本非零退出码 | **静默跳过**，不中断主任务 |
| summarize.py 条数不足 | 加 --force 参数重新执行 |
| 用户明确说"不用记录" | 立即停止记录，后续操作不再调用 log_op.py |
| knowledge_base.jsonl 不存在 | 跳过 7A 的知识库读取，仅基于摘要执行反思 |
| user_profile.json 解析失败 | 重新创建空文件，不中断进化流程 |

**最重要原则：记忆功能失败不能影响主任务。静默处理，不打印错误。**

---

## 完整执行流程

```
触发条件满足
  └─ init.py --project <名> --resume
       ├─ 提取 session_id → 保存为 SESSION_ID
       └─ 有上次摘要 → 告知用户，询问是否继续

执行任务（每次操作后）
  ├─ 执行操作
  ├─ log_op.py --session $SESSION_ID --type <type> --summary "..."
  ├─ 输出 COMPRESS_SUGGESTED → summarize.py --session $SESSION_ID
  └─ 观察到用户偏好/完成知识点 → 执行步骤六

用户问"之前做了什么"
  └─ recall.py --session $SESSION_ID --query "关键词"
       └─ 原样展示输出给用户

用户说"继续上次"（新会话）
  └─ restore.py --project <名>
       ├─ 提取新 SESSION_ID
       └─ 告知用户恢复内容，询问是否继续
```

---

进阶配置（过滤规则、LanceDB 向量检索升级、自动 hook 配置、安全注意事项等）见 `references/advanced-config.md`。

---

## 附录 A：检索行为说明

`recall.py` 同时在五层记忆中搜索，结果按相关度和时间综合排序：

- 近期操作权重高于久远操作（时间衰减）
- 关键词在多个层都命中时，该结果排名靠前
- 安装 `sentence-transformers` 后，召回精度会进一步提升（可选，完全本地运行）
- 输出为相关片段而非完整记录，节省上下文空间

---

## 附录 B：记忆分层

每条操作压缩后自动标记层级，影响 gc 清理策略：

| 层级 | 操作类型 | 说明 |
|------|----------|------|
| core | milestone / decision / error / user_instruction | 长期保留 |
| working | reasoning / file_write / bash_exec | 当前会话活跃 |
| peripheral | file_read / tool_call | 历史细节，可清理 |

summary.md 压缩后会显示各层计数。

---

## 附录 C：manage.py 管理工具

```bash
# 列出所有会话
python3 $SKILL_DIR/scripts/manage.py list
python3 $SKILL_DIR/scripts/manage.py list --project my-project

# 跨所有会话全文搜索
python3 $SKILL_DIR/scripts/manage.py search "pandas 数据清洗"
python3 $SKILL_DIR/scripts/manage.py search "error" --limit 50

# 全局统计（操作数、tier 分布、项目分布、知识库规模）
python3 $SKILL_DIR/scripts/manage.py stats

# 导出完整记忆备份
python3 $SKILL_DIR/scripts/manage.py export --format json --output backup.json
python3 $SKILL_DIR/scripts/manage.py export --format markdown --output memory.md

# 垃圾回收：清理 90 天未活跃且无核心操作的会话（默认预演）
python3 $SKILL_DIR/scripts/manage.py gc
python3 $SKILL_DIR/scripts/manage.py gc --days 30 --no-dry-run  # 实际执行

# 补写 tier 分层标记（历史数据迁移）
python3 $SKILL_DIR/scripts/manage.py tier
python3 $SKILL_DIR/scripts/manage.py tier --session sess_xxxxx

# 列出所有隔离 scope（多用户/多 Agent）
python3 $SKILL_DIR/scripts/manage.py scopes
```

---

## 附录 D：REST API 认证（可选）

启动 REST 服务器时可配置 Bearer Token 保护：

```bash
# 方式 1：命令行参数
python3 $SKILL_DIR/platform/server.py --token your-secret-token

# 方式 2：环境变量
ULTRA_MEMORY_TOKEN=your-secret-token python3 $SKILL_DIR/platform/server.py

# 客户端调用时携带 Header：
# Authorization: Bearer your-secret-token
```

不配置 token 时服务器维持原有行为（仅监听 127.0.0.1，局域网不可访问）。

---

## 附录 E：无脚本降级模式

**适用场景：** claude.ai web 对话、无文件系统的在线 LLM 平台、`$SKILL_DIR` 探测失败的任意环境。

此模式不依赖文件系统、Python 脚本或任何外部工具，完全依赖 AI 自身维护结构化记忆 prompt。

---

### E1：会话内记忆结构

AI 在内心维护以下结构（不主动输出给用户，仅在需要时引用）：

```
MEMORY_STATE:
  project: <项目名>
  started: <ISO时间>
  ops: []           # 近 20 条操作；格式: {seq, type, summary}
  milestones: []    # 里程碑列表（长期保留）
  decisions: []     # 关键决策（长期保留）
  knowledge: []     # 知识点，最多 10 条
  profile:
    tech_stack: []
    observed_patterns: []
```

**核心原则：ops 满 20 条时，将最旧的非 milestone/decision 操作合并进 milestones 或丢弃。**

---

### E2：操作记录（替代 log_op.py）

每次发生 E2 触发事件（见主文步骤二的触发条件表）后，AI 在内心更新 `MEMORY_STATE.ops`。无需输出，不增加对话轮数。

---

### E3：记忆检索（替代 recall.py）

用户询问历史时，AI 直接扫描 `MEMORY_STATE` 内所有字段，提取相关条目回答。

---

### E4：摘要压缩（替代 summarize.py）

对话超过 **30 轮** 或用户说"总结一下"时，AI 执行内部压缩：

1. 将 `ops` 中重要性低的条目合并进 `milestones`/`decisions`
2. 清空 `ops`，仅保留最近 5 条
3. 向用户简述压缩结果（一句话）

---

### E5：跨会话限制（必须向用户说明）

首次进入无脚本模式时，AI 主动告知用户：

> "当前运行在无脚本模式，记忆仅在本次对话有效，关闭后无法恢复。如需跨会话持久化，请在 Claude Code 或安装了 ultra-memory 的环境中使用。"

此说明只输出一次，不重复。

---

### E6：功能对比

| 功能 | 脚本模式 | 无脚本模式 |
|------|---------|----------|
| 操作记录 | ✅ 持久化文件 | ✅ 会话内维护 |
| 关键词检索 | ✅ BM25 + 向量 | ✅ AI 直接扫描 |
| 摘要压缩 | ✅ 自动 | ✅ 手动触发 |
| 跨会话恢复 | ✅ | ❌ |
| 用户画像积累 | ✅ 持久化 | ⚠️ 仅当前会话 |
| 知识蒸馏 | ✅ | ❌ |
| 多 scope 隔离 | ✅ | ❌ |
