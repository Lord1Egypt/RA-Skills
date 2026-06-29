# skill-sub 调用链数据结构

> 本文档定义 Chain / Step / retry_policy / failure_mode 的完整结构。
>
> **v1.20.0 新增**：Step 支持三种类型（skill / loop / branch），详见 Step 扩展类型章节。

---

## Chain（调用链）

```json
{
  "name": "string",           // 唯一名称
  "description": "string",     // 调用链描述
  "purpose": "string",        // 核心目的
  "user_intent": "string",    // 用户原始意图（用于意图匹配）
  "tags": ["string"],         // 标签（用于自动匹配）
  "auto_safe": true,          // 链是否可不经人工介入全自动执行（由 flow_validator 自动计算）
  "user_specified": false,    // 用户是否显式指定了所有 skill（true→自愈时跳过）
  "schedule": null,           // 调度配置（可选），见下方 Schedule 定义
  "created_at": "datetime",
  "updated_at": "datetime",
  "exec_count": 0,            // 执行次数
  "steps": [ ... ]            // Step 数组，见下文
}
```

---

## Schedule（调度配置）

> 链的调度元数据，任何平台可据此创建定时任务。不绑定具体平台。

```json
{
  "type": "cron",              // "cron" | "interval" | "once"
  "expression": "0 6 * * *",  // cron 表达式 / 间隔秒数 / 触发时间
  "description": "每天早上6点执行",  // 自然语言描述
  "registered": false          // 是否已在平台注册（创建时为 false，注册后改为 true）
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `type` | string | ✅ | `"cron"`（cron 表达式）、`"interval"`（间隔秒数）、`"once"`（单次执行） |
| `expression` | string | ✅ | cron 格式（如 `"0 6 * * *"`）或间隔秒数（如 `"86400"`）或 ISO 时间（如 `"2026-06-03T06:00:00"`） |
| `description` | string | ❌ | 自然语言描述，便于跨平台理解 |
| `registered` | bool | ❌ | 注册标记。创建时默认 `false`，平台注册后改为 `true` |

### 注册流程

1. 链创建时 `schedule.registered = false`
2. `chain_executor.py plan` 检测到 `registered == false` 时，在计划顶部输出 **强制注册提醒**
3. 平台读取 `schedule` 字段，完成注册后将 `registered` 置为 `true`
4. 已注册的链 `plan` 输出不再显示注册提醒

### type 说明

| type | expression 示例 | 含义 |
|------|----------------|------|
| `cron` | `"0 6 * * *"` | 每天早上 6 点 |
| `cron` | `"0 0 * * 1"` | 每周一零点 |
| `cron` | `"0 0 1 * *"` | 每月 1 日零点 |
| `interval` | `"3600"` | 每小时执行一次 |
| `interval` | `"86400"` | 每天执行一次 |
| `once` | `"2026-06-03T06:00:00"` | 2026年6月3日6点执行一次 |

### 使用方式

- **创建链时**：用户在意图中描述定时需求（如「每天早上6点跑这个链」），AI 自动填充 `schedule` 字段
- **已有链**：通过 `chain_manager.py schedule --name <链名> --cron "0 6 * * *" --desc "每天6点"` 添加/更新
- **平台侧**：读取 `chain_data.schedule`，按 `type` + `expression` 注册定时任务

---

## Step（步骤）

> **步骤类型**：通过 `type` 字段区分技能调用、循环、分支。默认 `type: "skill"`。
> `steps` / `if_steps` / `else_steps` 均为 Step 数组，支持递归嵌套。

### 通用字段（所有类型均含）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `index` | int | ✅ | 步骤序号（从 1 开始，全局唯一） |
| `type` | string | ✅ | `"skill"` / `"loop"` / `"branch"` |
| `step_name` | string | ✅ | 步骤名称（展示用） |
| `depends_on` | int[] | ❌ | 依赖的前置步骤索引，默认 `[index-1]` |
| `condition` | string | ❌ | 步骤级条件：非 `"always"` 时按需求值，为 `false` 则跳过本步骤 |
| `failure_mode` | object | ❌ | 失败处理（见下文） |
| `notes` | string | ❌ | 备注 |

---

### 类型 A：`"type": "skill"`（技能调用步骤）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `skill_name` | string | ✅ | 调用的技能名称（须已安装） |
| `action` | string | ✅ | 精炼动作描述（第一层执行用） |
| `skill_instruction` | string | ❌ | 对应 SKILL.md 中的指令名（第二层回退用） |
| `detail` | string | ❌ | 详细执行说明（第三层回退用） |
| `variables` | object | ❌ | 步骤级变量映射 `{"input": "{{step1.output}}", "output": "result"}` |
| `retry_policy` | object | ❌ | 重试策略（见下文） |

**示例：**

```json
{
  "index": 1,
  "type": "skill",
  "step_name": "代码审查",
  "skill_name": "code-review",
  "action": "审查 PR #123 的代码更新",
  "skill_instruction": "review-pr",
  "depends_on": [],
  "condition": "always",
  "variables": {"input": "{{pr_number}}", "output": "review_result"},
  "retry_policy": {"max_retries": 3, "error_types": ["network_error", "timeout"]},
  "failure_mode": {"on_exhaust": "ask", "is_milestone": false},
  "notes": "第一步，不依赖其他步骤"
}
```

---

### 类型 B：`"type": "loop"`（循环步骤）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `loop.mode` | string | ✅ | `"for_each"` 或 `"while"` |
| `loop.items` | string | 条件① | `for_each` 模式：表达式，求值结果为数组 |
| `loop.while_condition` | string | 条件① | `while` 模式：布尔表达式，求值结果为 `true`/`false` |
| `loop.loop_variable` | string | 条件② | `for_each` 模式：迭代变量名，循环体内用 `{{变量名}}` 引用当前元素 |
| `loop.steps` | Step[] | ✅ | 循环体（Step 数组，递归支持 skill/loop/branch） |
| `loop.max_iterations` | int | ❌ | 安全上限，默认 `10`；达到时按 `on_max_iteration` 处理 |
| `loop.on_max_iteration` | string | ❌ | `"break"`（中止循环）或 `"continue"`（记录警告并继续） |

> ① `for_each` 需要 `items` + `loop_variable`；`while` 需要 `while_condition`。
> ② 循环体内步骤可访问 `{{loop_variable}}`（for_each）及父步骤的 `variables`。

**示例 1：for_each 循环**

```json
{
  "index": 2,
  "type": "loop",
  "step_name": "批量代码审查",
  "loop": {
    "mode": "for_each",
    "items": "{{pr_file_list}}",
    "loop_variable": "file",
    "steps": [
      {
        "index": 2.1,
        "type": "skill",
        "step_name": "审查文件 {{file}}",
        "skill_name": "code-review",
        "action": "审查单个文件",
        "variables": {"input": "{{file}}", "output": "file_review"}
      }
    ],
    "max_iterations": 20,
    "on_max_iteration": "break"
  },
  "depends_on": [1],
  "failure_mode": {"on_exhaust": "ask", "is_milestone": false}
}
```

**示例 2：while 循环**

```json
{
  "index": 3,
  "type": "loop",
  "step_name": "重试直到成功",
  "loop": {
    "mode": "while",
    "while_condition": "{{retry_count}} < 3 && {{last_success}} == false",
    "steps": [
      {
        "index": 3.1,
        "type": "skill",
        "step_name": "尝试部署",
        "skill_name": "deploy",
        "action": "执行部署"
      }
    ],
    "max_iterations": 3,
    "on_max_iteration": "break"
  },
  "failure_mode": {"on_exhaust": "abort", "is_milestone": true}
}
```

---

### 类型 C：`"type": "branch"`（分支步骤）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `branch.condition` | string | ✅ | 布尔表达式，求值后为 `true` 或 `false` |
| `branch.if_steps` | Step[] | ✅ | 条件为 `true` 时执行的步骤数组 |
| `branch.else_steps` | Step[] | ❌ | 条件为 `false` 时执行的步骤数组（可选） |

> ① `if_steps` 和 `else_steps` 均为 Step 数组，递归支持 skill / loop / branch。
> ② 分支步骤本身不调用技能，仅做流程控制；`failure_mode` 作用于整个分支步骤（即 `if_steps` 全部失败时的行为）。

**示例：if-else 分支**

```json
{
  "index": 4,
  "type": "branch",
  "step_name": "按环境选择部署目标",
  "branch": {
    "condition": "{{env}} == 'production'",
    "if_steps": [
      {
        "index": 4.1,
        "type": "skill",
        "step_name": "生产环境部署",
        "skill_name": "deploy",
        "action": "部署到生产环境",
        "variables": {"input": "production"}
      }
    ],
    "else_steps": [
      {
        "index": 4.2,
        "type": "skill",
        "step_name": "预发环境部署",
        "skill_name": "deploy",
        "action": "部署到预发环境",
        "variables": {"input": "staging"}
      }
    ]
  },
  "depends_on": [1, 2, 3],
  "failure_mode": {"on_exhaust": "ask", "is_milestone": true}
}
```

---

## retry_policy（重试策略）

```json
{
  "max_retries": 3,              // 最大重试次数（默认从配置读取，默认 3）
  "error_types": ["file_locked", "network_error", "timeout", "auth_error"]
}
```

**错误类型说明：**

| 错误类型 | 重试间隔 | 说明 |
|---------|---------|------|
| `file_locked` | 0 秒 | 文件占用/锁定，立即重试 |
| `network_error` | 5 秒 | 网络不通/超时 |
| `timeout` | 5 秒 | 执行超时 |
| `auth_error` | - | 认证/权限错误，直接询问用户 |
| `other` | 2 秒 | 其他错误 |

---

## failure_mode（失败处理模式）

```json
{
  "on_exhaust": "ask",       // 重试耗尽后行为: "ask" | "skip" | "abort"
  "is_milestone": false      // 是否为里程碑步骤（可通过通用规则自动判断）
}
```

**on_exhaust 行为说明：**

| 值 | 说明 |
|-----|------|
| `ask` | 重试耗尽后询问用户 |
| `skip` | 跳过该步骤，继续后续步骤 |
| `abort` | 中止整条调用链 |

**里程碑行为：**
- **里程碑步骤失败** → 无论 `on_exhaust` 配置如何，**强制中止整条链**
- **里程碑步骤的 on_exhaust** → 建议设为 `abort`（validate 时会发出警告）
- **非里程碑步骤失败** → 按 `on_exhaust` 配置处理（ask/skip/abort）

---

## 类型 D：`"type": "adhesion"`（粘连点步骤）

> **v1.25.0 新增**。粘连点标记调用链中无法由 skill 自动化的缺口，
> 提供三种解决方案供 LLM 选择执行，保证调用链不断裂。

### 通用字段（继承 Step 通用字段）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `index` | int | ✅ | 步骤序号 |
| `type` | string | ✅ | 固定为 `"adhesion"` |
| `step_name` | string | ✅ | 步骤名称 |
| `depends_on` | int[] | ❌ | 依赖的前置步骤索引 |

### adhesion 专用字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `adhesion.reason` | string | ✅ | 粘连原因描述 |
| `adhesion.solutions` | array | ✅ | 解决方案数组，至少 1 个 |
| `adhesion.updated_at` | string | ❌ | 最后检查时间（自愈扫描时更新） |

### solutions[n] 字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `mode` | string | ✅ | `"manual"` / `"auto"` / `"hybrid"` |
| `description` | string | ✅ | 执行描述 |
| `constraints` | string | ❌ | 约束条件（manual/hybrid 使用） |
| `tool_name` | string | 条件① | mode=auto/hybrid 时，工具名称 |
| `script_path` | string | 条件① | mode=auto/hybrid 时，脚本路径（相对数据目录） |
| `llm_steps` | string | 条件② | mode=hybrid 时，LLM 执行步骤 |
| `tool_steps` | string | 条件② | mode=hybrid 时，工具执行步骤 |

> ① auto/hybrid 模式至少提供 tool_name 或 script_path 之一
> ② hybrid 模式必须同时提供 llm_steps + tool_steps

### 三种 solution mode 说明

| mode | 说明 | 适用场景 |
|------|------|---------|
| `manual` | LLM 直接手动执行步骤，不依赖脚本或新 skill | 一次性、高度灵活的判断任务 |
| `auto` | 通过自调用脚本工具执行，产生的脚本入数据目录管理 | 可标准化、重复执行的任务 |
| `hybrid` | LLM 描述流程步骤 + 约束 + 自调用工具协同执行 | 需要智能判断 + 自动化执行的复合任务 |

### 自愈流程

每次调用链执行时，AI 检查链中所有 `adhesion` 类型步骤：

1. 扫描技能库（`scripts/` 目录或已安装技能）查找是否有新 skill 能填补该缺口
2. 找到匹配 skill → 将 `adhesion` 步骤升级为 `skill` 类型步骤，保留原 `adhesion.solutions` 到 `notes` 字段
3. 未找到 → 按 `adhesion.solutions` 中的方案执行（优先 hybrid → auto → manual）

---

## 条件表达式语法

`condition` / `branch.condition` / `loop.while_condition` 支持以下语法：

| 语法 | 示例 | 说明 |
|------|------|------|
| 步骤状态 | `step_1_success` | 步骤 1 成功（返回码 0） |
| 步骤状态（否定） | `step_2_failed` | 步骤 2 失败 |
| 变量存在 | `variable_OUTPUT_exists` | 变量 `OUTPUT` 已定义 |
| 变量相等 | `{{env}} == 'production'` | 字符串比较 |
| 变量数值 | `{{retry_count}} < 3` | 数值比较（`<` `>` `<=` `>=` `==` `!=`） |
| 逻辑运算 | `step_1_success && step_2_success` | `&&`（与）、`||`（或）、`!`（非） |
| 布尔常量 | `always` | 总是执行（默认） |
| 布尔常量 | `never` | 永不执行 |
