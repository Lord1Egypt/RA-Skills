---
name: web-auto-form
description: JSON 驱动的浏览器表单自动化工具，为 AI Agent 提供原生 function-calling 集成，支持表单填写、条件分支、数据提取与 PII 脱敏
version: 1.0.0
tags: [automation, browser, form, playwright, json-driven, ai-agent-tool]
metadata:
  clawdbot:
    emoji: "🌐"
    requires:
      bins:
        - python
      env: []
    os:
      - darwin
      - linux
      - win32
    homepage: https://github.com/DUZ1287/WebAutoForm
    install:
      - spec: "pip install web-auto-form"
        type: pip
      - spec: "playwright install chromium"
        type: shell
  openclaw:
    emoji: "🌐"
    requires:
      bins:
        - python
        - pip
        - playwright
      env: []
    os:
      - darwin
      - linux
      - win32
    homepage: https://github.com/DUZ1287/WebAutoForm
---

## 概述

**web-auto-form** 是一个 JSON 配置驱动的浏览器自动化引擎，专为表单填写、提交与结构化数据提取设计。你只需用 JSON 描述"做什么"，引擎自动处理浏览器生命周期、选择器解析、重试与错误恢复。它内置完整的 OpenAI/Claude function-calling JSON Schema，可被任何兼容 LLM 的 AI Agent 直接调用，无需额外封装。

核心价值：**零代码、确定性执行、AI Agent 原生集成、内置隐私脱敏。**

---

## 触发条件

当用户请求包含以下关键词或意图模式时，应调用 `web_auto_form` tool：

### 中文关键词
"填表"、"自动提交"、"网页操作"、"自动注册"、"登录"、"注册"、"报名"、"申请"、"批量录入"、"定时提交"、"表单测试"

### 英文关键词
"fill out form"、"submit form"、"auto-register"、"web automation"、"data entry"、"sign up"、"apply"、"form testing"、"batch submit"

### 意图模式
- 多步浏览器交互（navigate → fill → click → extract）
- 表单提交（含文件上传、下拉选择、复选框）
- 批量数据录入（同一表单、不同数据重复填写）
- 条件表单逻辑（根据页面状态分支执行）
- 结合 URL 的动作动词组合：navigate + fill + submit、open + select + click、register + upload + confirm

### 不应调用的场景
- 纯信息检索（应使用 WebFetch / WebSearch）
- 不涉及浏览器 UI 的纯 API 调用
- 需要人工验证码识别或生物特征验证的任务
- 无具体表单填写目标的大规模爬取

---

## 安全约束

| # | 约束 | 说明 |
|---|------|------|
| 1 | **consent 必填** | 每次调用必须包含 `consent_statement` 声明自动化目的，执行前记录于日志；非 headless 模式下展示并要求用户确认 |
| 2 | **禁止凭证收割** | 不得用于抓取登录页存储的凭据、密码管理器填充数据或窃取 session token |
| 3 | **无破坏性批量操作** | 单次调用上限 50 步，超出需逐批获得用户确认 |
| 4 | **不绕过安全控制** | 除非用户拥有明确授权（如自有测试环境），否则不自动化解验证码、2FA 绕过或反爬规避 |
| 5 | **域名建议白名单** | 默认允许所有 HTTPS URL；HTTP URL 执行前给出安全警告 |
| 6 | **PII 脱敏 — 全局开关** | `options.redact_pii`（默认 `true`）同时控制日志输出和提取文本的脱敏；可通过 `extract_schema.fields[].redact` 逐字段覆盖 |
| 7 | **浏览器沙箱** | `options.sandbox: true`（默认）强制沙箱模式，防止恶意页面逃逸。仅当对可信本地测试服务器运行时才可禁用 |
| 8 | **速率限制** | `options.step_delay_ms`（默认 500ms，最小 100ms）在每步之间强制执行，防止触发反爬保护 |
| 9 | **透明性** | 始终报告哪些步骤成功、跳过（optional）或失败——绝不静默吞掉错误 |

---

## 安装与依赖

```bash
pip install web-auto-form
playwright install chromium
```

Python 3.9+ 所需。引擎基于 Playwright 构建，Chromium 浏览器通过上述第二条命令安装。

---

## 快速开始

最小可运行 JSON 配置（3 步：填写姓名 → 填写邮箱 → 点击提交）：

```json
{
  "url": "https://example.com/apply",
  "consent_statement": "自动化填写个人数据。",
  "steps": [
    {"action": "fill", "selector": "#name",  "value": "张三"},
    {"action": "fill", "selector": "#email", "value": "zhangsan@example.com"},
    {"action": "click", "selector": "button[type='submit']"}
  ]
}
```

运行方式：

```bash
# CLI
web_auto_form run my_form.json

# 命令行覆盖数据变量
web_auto_form run my_form.json --data user.name=李四

# 有头模式 + 调试
web_auto_form run my_form.json --no-headless --debug
```

Python API：

```python
from web_auto_form import run, run_from_path

result = run(config_dict)       # 从 dict 执行
result = run_from_path("config.json")  # 从文件执行
print(result["status"])         # "success" | "partial" | "failed"
print(result["extracted"])      # {"field_name": "extracted value", ...}
```

---

## 完整配置参考

### 顶层字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `url` | string | 是 | 起始 URL（HTTPS 或 HTTP，后者触发安全警告） |
| `consent_statement` | string | 是 | 自动化目的声明，记录于日志 |
| `steps` | StepConfig[] | 是 | 有序动作列表（1–50 步） |
| `data` | object | 否 | 模板变量字典，通过 `{{key}}` 语法访问，支持嵌套点号 |
| `extract_schema` | ExtractSchemaConfig | 否 | 执行完成后的结构化提取规则 |
| `options` | OptionsConfig | 否 | 全局执行设置 |

### 全局选项

| 选项 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `headless` | bool | `true` | 无头模式运行浏览器 |
| `viewport_width` | int | `1280` | 视口宽度（px） |
| `viewport_height` | int | `800` | 视口高度（px） |
| `user_agent` | string | — | 自定义 User-Agent 字符串 |
| `locale` | string | `"en-US"` | 浏览器 locale |
| `step_delay_ms` | int | `500` | 步骤间强制延迟（最小 100ms，最大 10000ms） |
| `max_retries` | int | `1` | 可重试错误的全局最大重试次数（1–5） |
| `retry_on` | string[] | `["NETWORK_ERROR"]` | 全局可重试错误类型列表 |
| `sandbox` | bool | `true` | 浏览器沙箱模式 |
| `redact_pii` | bool | `true` | 全局 PII 脱敏开关（日志 + 提取输出） |
| `debug` | bool | `false` | 保存每步截图、HTML 快照和 Playwright trace |
| `debug_output_path` | string | `"./web_auto_form_debug_<timestamp>/"` | 调试产物输出目录 |
| `keep_open` | bool | `false` | 完成后保持浏览器打开 |
| `upload_enforce_extension` | bool | `false` | 当 `file_name` 扩展名与 MIME 不匹配时是否阻止上传 |

---

## 13 种 Action 类型详解

### 导航与交互类

#### `navigate` — 页面导航

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `action` | `"navigate"` | 是 | — |
| `value` | string | 是 | 目标 URL |
| `timeout_ms` | int | 否 | 导航超时（默认 30000ms，最大 60000ms） |
| `description` | string | 否 | 步骤描述（支持 `{{}}` 模板） |

#### `fill` — 输入框填写

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `action` | `"fill"` | 是 | — |
| `selector` | string | 是 | 目标输入框选择器 |
| `value` | string | 是 | 要输入的文本（支持 `{{}}` 模板） |
| `selector_type` | string | 否 | 显式指定选择器类型（`css`/`xpath`/`id`/`name`/`placeholder`/`data-testid`） |
| `selector_fallbacks` | string[] | 否 | 备用选择器链 |
| `timeout_ms` | int | 否 | 等待元素出现超时（默认 5000ms） |
| `optional` | bool | 否 | 找不到元素时是否跳过（默认 `false`） |
| `on_skip` | string | 否 | optional 步骤跳过行为（`log`/`abort`/`set_default`） |
| `description` | string | 否 | 步骤描述 |

#### `click` — 元素点击

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `action` | `"click"` | 是 | — |
| `selector` | string | 是 | 目标元素选择器 |
| `selector_type` | string | 否 | 显式选择器类型 |
| `selector_fallbacks` | string[] | 否 | 备用选择器链 |
| `timeout_ms` | int | 否 | 等待元素出现超时 |
| `optional` | bool | 否 | 是否可选（默认 `false`） |
| `on_skip` | string | 否 | 可选步跳过行为 |
| `screenshot` | bool | 否 | 点击后截图（默认 `false`） |
| `description` | string | 否 | 步骤描述 |

#### `select` — 下拉选择

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `action` | `"select"` | 是 | — |
| `selector` | string | 是 | `<select>` 元素选择器 |
| `value` | string | 是 | 选项文本或 value 属性值 |
| `selector_type` / `selector_fallbacks` / `timeout_ms` / `optional` / `on_skip` / `description` | — | 否 | 同上 |

#### `check` — 复选框切换

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `action` | `"check"` | 是 | — |
| `selector` | string | 是 | checkbox/radio 选择器 |
| `value` | `"true"` / `"false"` | 是 | 选中或取消 |
| `selector_type` / `selector_fallbacks` / `timeout_ms` / `optional` / `on_skip` / `description` | — | 否 | 同上 |

#### `upload` — 文件上传

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `action` | `"upload"` | 是 | — |
| `selector` | string | 是 | `<input type="file">` 选择器 |
| `value` | string | 是 | 文件来源（见下方 4 种格式） |
| `file_name` | string | 否 | 覆盖上传文件名（支持 `{{}}` 模板） |
| `selector_type` / `selector_fallbacks` / `timeout_ms` / `optional` / `on_skip` / `description` | — | 否 | 同上 |

**文件来源 4 种格式：**

| 格式 | 示例 | 行为 |
|------|------|------|
| 本地路径 | `file:///documents/resume.pdf` | 从宿主机文件系统读取 |
| HTTPS URL | `https://cdn.example.com/resume.pdf` | 下载到临时文件后上传 |
| Data URI | `data:application/pdf;base64,JVBERi0...` | 内存解码后上传 |
| 相对路径 | `./uploads/resume.pdf` | 相对于工作目录解析 |

#### `press_key` — 键盘按键

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `action` | `"press_key"` | 是 | — |
| `value` | string | 是 | 按键名称（`"Enter"`, `"Tab"`, `"Escape"`, `"ArrowDown"` 等） |
| `selector` | string | 否 | 目标元素（省略则聚焦当前活跃元素） |
| `description` | string | 否 | 步骤描述 |

#### `scroll` — 页面滚动

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `action` | `"scroll"` | 是 | — |
| `value` | string | 是 | `"up"`, `"down"` 或像素值（如 `"500"`） |
| `selector` | string | 否 | 滚动到指定元素（省略则滚动页面） |
| `description` | string | 否 | 步骤描述 |

#### `handle_dialog` — 对话框处理

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `action` | `"handle_dialog"` | 是 | — |
| `value` | `"accept"` / `"dismiss"` | 是 | 接受或关闭浏览器原生对话框 |
| `description` | string | 否 | 步骤描述 |

### 流程控制类

#### `wait` — 等待

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `action` | `"wait"` | 是 | — |
| `type` | string | 否 | 等待子类型（默认 `"element"`） |
| `selector` | string | 条件 | `type=element` 时必填 |
| `value` | string | 条件 | `type=timeout` 或 `type=function` 时必填 |
| `timeout_ms` | int | 否 | 最大等待时间（默认 5000ms） |
| `description` | string | 否 | 步骤描述 |

**4 种等待子类型：**

| type | 行为 | `value` 字段 | Schema 约束 |
|------|------|-------------|-------------|
| `element`（默认） | 轮询直到 `selector` 出现在 DOM | 忽略 | — |
| `navigation` | 等待 URL 变化或 `load` 事件 | 忽略 | — |
| `timeout` | 无条件休眠 | **必填**：毫秒数字符串（如 `"3000"`） | 必须匹配 `^[0-9]+$` |
| `function` | 轮询直到 JS 表达式返回 truthy | **必填**：JS 表达式字符串 | 必须非空 |

#### `if` — 条件分支

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `action` | `"if"` | 是 | — |
| `condition` | object | 是 | 条件定义（见下方两种模式） |
| `then` | StepConfig[] | 是 | 条件为 true 时执行的步骤列表 |
| `else` | StepConfig[] | 否 | 条件为 false 时执行的步骤列表 |
| `description` | string | 否 | 步骤描述 |

**条件模式 1 — 基于状态（state-based）：**

检查元素的存在性/可见性/选中状态：

```json
"condition": { "selector": "#checkbox", "state": "checked" }
```

支持的 state 值：`exist`, `not_exist`, `visible`, `hidden`, `checked`

**条件模式 2 — 基于值（value-based）：**

比较元素属性值与期望值：

```json
"condition": {
  "selector": ".status",
  "attribute": "textContent",
  "operator": "eq",
  "expected_value": "已通过"
}
```

支持的 operator 值：`eq`, `ne`, `contains`, `matches_regex`

> **注意**：两种模式互斥。若同时提供 `state` 和 `operator`，`operator` 优先。嵌套深度上限 3 层。

#### `assert` — 断言

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `action` | `"assert"` | 是 | — |
| `selector` | string | 是 | 待验证的元素选择器 |
| `state` | string | 是 | 期望状态（`exist`, `not_exist`, `visible`, `hidden`, `enabled`, `disabled`, `checked`） |
| `on_fail` | string | 否 | 失败行为：`abort`（默认）/ `continue` / `retry` |
| `max_retries` | int | 否 | 步骤级重试次数覆盖（`on_fail=retry` 时有效） |
| `timeout_ms` | int | 否 | 等待状态满足的超时时间 |
| `description` | string | 否 | 步骤描述 |

#### `extract` — 运行时提取

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `action` | `"extract"` | 是 | — |
| `selector` | string | 是 | 提取目标元素选择器 |
| `attribute` | string | 否 | 提取目标（`text`/`innerHTML`/`value`/任意 HTML 属性，默认 `text`） |
| `description` | string | 否 | 步骤描述 |

> 与 `extract_schema` 不同，`extract` action 可在步骤序列中间实时提取。

### 通用步骤字段

以下字段适用于大部分交互类动作（`fill`, `select`, `check`, `click`, `upload` 等）：

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `selector_type` | string | 自动检测 | 显式指定选择器类型 |
| `selector_fallbacks` | string[] | — | 备用选择器链，按顺序尝试 |
| `timeout_ms` | int | `5000` | 等待元素出现的最长时间 |
| `optional` | bool | `false` | 找不到元素时是否跳过 |
| `on_skip` | string | `"log"` | 跳过行为：`log`/`abort`/`set_default` |
| `screenshot` | bool | `false` | 步骤执行后截图 |
| `max_retries` | int | 继承全局 | 步骤级重试次数（1–5） |
| `retry_on` | string[] | 继承全局 | 步骤级可重试错误类型 |
| `description` | string | — | 步骤描述（支持 `{{}}` 模板） |

---

## 选择器系统

### 自动类型检测

选择器通过前缀自动检测类型，无需显式声明 `selector_type`：

| 前缀 | 类型 | 示例 |
|------|------|------|
| `//` | XPath | `//div[@class='form']/input` |
| `#` | ID | `#email` |
| `[name=` | name 属性 | `[name='email']` |
| `[placeholder=` | placeholder 属性 | `[placeholder='Phone number']` |
| `[data-testid=` | data-testid 属性 | `[data-testid='email-input']` |
| （其他） | CSS 选择器 | `div.form > input[type='text']` |

### Fallback 链与 optional 逻辑

解析顺序：

1. 尝试主选择器 `selector`
2. 若主选择器失败，按序尝试 `selector_fallbacks[i]`
3. 任一选择器匹配，立即使用该元素执行
4. 仅当 **全部选择器**（主 + 所有 fallback）在 `timeout_ms` 内全部失败时，触发 `optional` 逻辑：
   - `optional: true` + `on_skip: "log"` → 记录警告，继续执行
   - `optional: true` + `on_skip: "abort"` → 终止执行
   - `optional: true` + `on_skip: "set_default"` → 使用 `value` 作为 fallback 值，继续执行
   - `optional: false` → 抛出 `ELEMENT_NOT_FOUND` 错误，终止

```json
{
  "action": "fill",
  "selector": "#email",
  "selector_fallbacks": ["[name='email']", "[data-testid='email-input']"],
  "value": "user@example.com"
}
```

### 最佳实践

- **优先使用 `data-testid` 或稳定的 CSS class**，避免自动生成的动态 ID（如 `id="input_123456"`）
- **为关键步骤提供 `selector_fallbacks`**（提交按钮、文件输入等）
- **XPath 仅用于 CSS 无法表达的关系**（如文本匹配、兄弟节点遍历），CSS 选择器更快、更可读
- **避免依赖 DOM 位置索引**的脆弱选择器（如 `div > div:nth-child(3) > input`），优先使用语义化属性

---

## 模板变量

`data` 对象支持 `{{key}}` 语法，通过点号访问嵌套字段。支持的字段包括：`value`, `selector`, `selector_fallbacks`, `file_name`, `description`, `extract_schema.fields[].selector`。

**注入安全**：选择器中的模板变量仅限于属性值位置，运行时校验渲染后的选择器无法逃逸其语法上下文（例如 `[name='{{x}}']` 中的变量将进行 HTML 实体转义）。

```json
{
  "data": {
    "user": {
      "name": "Zhang Wei",
      "email": "zhangwei@example.com"
    },
    "target_position": "Software Engineer"
  },
  "steps": [
    {"action": "fill", "selector": "[name='fullname']", "value": "{{user.name}}"},
    {"action": "fill", "selector": "[name='email']", "value": "{{user.email}}"},
    {"action": "select", "selector": "#position", "value": "{{target_position}}"}
  ]
}
```

CLI 中可通过 `--data` 覆盖模板变量：

```bash
web_auto_form run config.json --data user.name=李四 --data target_position="Product Manager"
```

---

## 结构化提取

`extract_schema` 在全部步骤完成后批量提取指定元素的内容：

```json
{
  "extract_schema": {
    "fields": [
      {"name": "confirmation_message", "selector": ".success-message", "attribute": "text", "redact": false},
      {"name": "application_id", "selector": ".app-id", "attribute": "text", "redact": false},
      {"name": "user_email_displayed", "selector": ".confirmation-email", "attribute": "text", "redact": true}
    ],
    "screenshot": true
  }
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | 是 | 输出结果中的字段名 |
| `selector` | string | 是 | CSS/XPath 选择器（支持 `{{}}` 模板） |
| `attribute` | string | 否 | 提取目标：`"text"`（默认）/ `"innerHTML"` / `"value"` / 任意 HTML 属性名 |
| `redact` | bool | 否 | 逐字段覆盖全局 `redact_pii` 设置。`false` 保留原始值 |

> 如需在步骤序列中间提取数据，使用 `extract` action 而非 `extract_schema`。

---

## 输出格式

工具返回标准 JSON 结构：

```json
{
  "status": "success | partial | failed",
  "consent_logged": "Automating a job application form submission...",
  "steps_executed": 14,
  "steps_skipped": 1,
  "steps_failed": 0,
  "results": [
    {"step": 0, "action": "wait", "status": "ok", "duration_ms": 1200},
    {"step": 1, "action": "fill", "status": "ok", "duration_ms": 340},
    {"step": 12, "action": "assert", "status": "ok", "duration_ms": 800, "retries": 2}
  ],
  "step_screenshots": [
    {"step": 10, "screenshot": "base64-encoded-png"}
  ],
  "extracted": {
    "confirmation_message": "Your application has been submitted successfully.",
    "application_id": "APP-20260527-0042",
    "user_email_displayed": "***@***.***"
  },
  "final_screenshot": "base64-encoded-png-or-null",
  "debug_artifacts": null,
  "errors": []
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `status` | string | `"success"` — 全部步骤成功；`"partial"` — 部分 optional 步骤跳过但无错误；`"failed"` — 存在步骤失败 |
| `steps_executed` | int | 实际执行的步骤数 |
| `steps_skipped` | int | 跳过的 optional 步骤数 |
| `steps_failed` | int | 失败的步骤数 |
| `results` | array | 每个步骤的执行结果（含耗时） |
| `extracted` | object | 结构化提取输出（key 来自 `extract_schema.fields[].name`） |
| `errors` | array | 错误详情列表 |

---

## 重试策略

区分瞬时错误与永久错误，在全局和步骤两级控制：

### 错误分类

| 错误类型 | 行为 | 默认是否重试 |
|----------|------|-------------|
| `NETWORK_ERROR` | 连接重置、DNS 失败、网络层超时 | 是 |
| `TIMEOUT` | 在 `timeout_ms` 内找不到元素、JS 条件未满足 | 否 |
| `NAVIGATION_FAILED` | 页面未加载、重定向循环、HTTP 5xx | 是 |
| `ELEMENT_NOT_FOUND` | 所有选择器（主+fallback）均失败且 `optional=false` | 否 |
| `ASSERTION_FAILED` | `assert` 动作检测到非预期状态 | 取决于 `on_fail` |

### 两级配置

**全局级**（`options` 中设置，适用于所有步骤）：

```json
"options": {
  "max_retries": 2,
  "retry_on": ["NETWORK_ERROR", "NAVIGATION_FAILED"]
}
```

**步骤级**（覆盖全局，仅对当前步骤有效）：

```json
{
  "action": "assert",
  "selector": ".success-message",
  "state": "visible",
  "on_fail": "retry",
  "max_retries": 3,
  "description": "重试最多 3 次确认成功消息出现"
}
```

### 断言重试语义

当 `on_fail: "retry"` 时，引擎仅重新执行 assert 步骤本身（重新检查元素状态），最多 `max_retries` 次，每次间隔 `step_delay_ms`。全部重试失败后 fallback 为 `abort`。输出 `results` 中记录实际重试次数。

---

## 调试模式

当 `options.debug: true` 时，引擎在 `debug_output_path`（默认 `./web_auto_form_debug_<timestamp>/`）生成以下产物：

| 产物 | 说明 |
|------|------|
| **每步截图** | PNG 格式，记录每个步骤执行后的页面状态 |
| **HTML 快照** | 每个步骤执行后的完整 DOM 快照 |
| **Playwright Trace** | 完整的 Playwright 追踪日志，可用 `playwright show-trace` 回放 |
| **浏览器保持打开** | `debug` 模式下默认 `keep_open: true`，便于手动检查 |

---

## 与竞品对比

| 维度 | web-auto-form | Playwright | Selenium | Browser-Use |
|------|-------------|------------|----------|-------------|
| **工作方式** | JSON 配置 | 编写代码 | 编写代码 | 自然语言 |
| **学习曲线** | 零门槛 | 中等 | 陡峭 | 零门槛 |
| **最适合** | 批量表单填写、数据录入、注册自动化、CI 表单测试、**LLM Agent 工具** | 现代 Web 测试、复杂 SPA 场景 | 遗留企业系统、跨浏览器测试 | 一次性探索任务、调研爬取 |
| **AI Agent 集成** | **原生支持** — 内置 JSON 工具模式和系统提示 | 需自行封装 | 需自行封装 | 内置（但间接） |
| **确定性** | 100% 确定性 | 确定性 | 确定性 | 非确定性（LLM 决策） |
| **执行速度** | 快（无 LLM 推理开销） | 快 | 中等 | 慢（每步调用 LLM） |
| **隐私脱敏** | **内置** — 自动脱敏邮箱、电话、身份证号 | 手动处理 | 手动处理 | 手动处理 |
| **条件逻辑** | JSON 声明式 `if`/`else` | 代码驱动 | 代码驱动 | 提示词驱动 |
| **选择器韧性** | 自动检测 + fallback 链 | 手动处理 | 手动处理 | LLM 驱动（不可靠） |
| **调试产物** | 每步自动截图 + HTML 快照 + Playwright Trace | Trace viewer | 手动截图 | 有限 |
| **单次运行成本** | 免费（本地执行） | 免费 | 免费 | 每步产生 LLM API 费用 |

**选型一句话：**
- 填**表单** → web-auto-form
- 写**测试** → Playwright
- **IE11/老旧系统** → Selenium
- **一次性探索** → Browser-Use

---

## 限制与上限

| 约束项 | 硬限制 |
|--------|--------|
| 单次调用最大步骤数 | 50 |
| 嵌套深度上限（if/else） | 3 层 |
| 单步最大超时 | 60,000 ms（1 分钟） |
| 最大总执行时间 | 300,000 ms（5 分钟） |
| 单步最大重试次数 | 5 |
| 最大文件上传大小 | 50 MB |
| 最小步骤延迟 | 100 ms |
| 默认步骤延迟 | 500 ms |
| CLI 单次运行超时 | 5 分钟 |
| 最大视口宽度 | 3840 px |
| 最大视口高度 | 2160 px |

---

## 完整工作流示例

以下示例展示模板变量、条件分支、选择器回退、文件上传、断言、结构化提取等全部特性（来自 `examples/job_application.json`）：

```json
{
  "url": "https://example.com/apply",
  "consent_statement": "自动化提交职位申请表，用于个人数据录入。",
  "data": {
    "user": {
      "name": "Zhang Wei",
      "email": "zhangwei@example.com",
      "phone": "+86 138-0000-1234"
    },
    "resume_path": "file:///documents/resume.pdf",
    "target_position": "Software Engineer"
  },
  "steps": [
    {
      "action": "wait",
      "selector": "form#application",
      "type": "element",
      "timeout_ms": 10000,
      "description": "等待申请表加载完成"
    },
    {
      "action": "fill",
      "selector": "#fullname",
      "value": "{{user.name}}",
      "description": "填写姓名"
    },
    {
      "action": "fill",
      "selector": "input[name='email']",
      "value": "{{user.email}}",
      "description": "填写邮箱"
    },
    {
      "action": "fill",
      "selector": "[placeholder='Phone number']",
      "selector_fallbacks": ["input[type='tel']", "input[name='phone']"],
      "value": "{{user.phone}}",
      "optional": true,
      "on_skip": "log",
      "description": "填写电话（可选字段，带选择器回退）"
    },
    {
      "action": "select",
      "selector": "#position",
      "value": "{{target_position}}",
      "description": "选择目标职位"
    },
    {
      "action": "if",
      "condition": { "selector": "#has_experience", "state": "checked" },
      "then": [
        {
          "action": "fill",
          "selector": "#years_experience",
          "value": "5",
          "description": "填写工作年限"
        }
      ],
      "else": [
        {
          "action": "check",
          "selector": "#fresh_graduate",
          "value": "true",
          "optional": true,
          "description": "标记为应届毕业生"
        }
      ],
      "description": "根据工作经验动态显示不同字段"
    },
    {
      "action": "upload",
      "selector": "input[type='file']",
      "value": "{{resume_path}}",
      "file_name": "{{user.name}}_Resume.pdf",
      "description": "上传简历"
    },
    {
      "action": "check",
      "selector": "#agree-terms",
      "value": "true",
      "description": "同意条款"
    },
    {
      "action": "click",
      "selector": "button[type='submit']",
      "selector_fallbacks": ["input[type='submit']", "[data-testid='submit-btn']"],
      "description": "点击提交（带多重回退选择器）"
    },
    {
      "action": "wait",
      "type": "navigation",
      "timeout_ms": 10000,
      "description": "等待提交后页面跳转"
    },
    {
      "action": "assert",
      "selector": ".error-message",
      "state": "not_exist",
      "on_fail": "abort",
      "description": "验证无错误消息"
    },
    {
      "action": "assert",
      "selector": ".success-message",
      "state": "visible",
      "timeout_ms": 15000,
      "on_fail": "retry",
      "max_retries": 3,
      "description": "确认成功消息出现（最多重试 3 次）"
    }
  ],
  "extract_schema": {
    "fields": [
      {"name": "confirmation_message", "selector": ".success-message", "attribute": "text", "redact": false},
      {"name": "application_id", "selector": ".app-id", "attribute": "text", "redact": false},
      {"name": "user_email_displayed", "selector": ".confirmation-email", "attribute": "text", "redact": true}
    ],
    "screenshot": true
  },
  "options": {
    "headless": false,
    "step_delay_ms": 500,
    "viewport_width": 1280,
    "viewport_height": 900,
    "sandbox": true,
    "redact_pii": true,
    "debug": false
  }
}
```

此示例完整覆盖了：模板变量 `{{user.name}}`、选择器 fallback 链、optional 步骤 + `on_skip`、状态条件分支 `if/else`、文件上传、多重断言（含 `retry` 策略）、结构化提取（含逐字段 `redact` 覆盖）、导航等待。

---

## AI Agent 集成要点

### 作为 Function-Calling Tool 使用

本 Skill 对应的完整 JSON Schema 定义在 [web_auto_form_tool.json](web_auto_form_tool.json)，可直接接入任何兼容 OpenAI/Claude function-calling 的 Agent 管道。

**集成方式**：
1. 将 `web_auto_form_tool.json` 的内容注册为 Agent 的 tool definition
2. 将本文档的触发条件部分纳入 Agent 的 system prompt
3. Agent 收到匹配的用户请求后，构造符合 Schema 的 JSON 配置作为 tool call arguments
4. 在 Agent 端执行 `web_auto_form run`（或 Python API `run()`），将返回的 JSON 结果传回 Agent 上下文

### Python API 快速集成

```python
from web_auto_form import run

# Agent 将 LLM 生成的配置传给引擎
config = {
    "url": "https://example.com/form",
    "consent_statement": "Agent-driven form submission",
    "steps": [
        {"action": "fill", "selector": "#name", "value": "Alice"},
        {"action": "click", "selector": "button[type='submit']"}
    ]
}

result = run(config)
# 将 result 返回给 LLM 上下文，让 Agent 基于提取结果继续对话
```

---

## 项目资源

| 资源 | 路径 |
|------|------|
| JSON Tool Schema | [web_auto_form_tool.json](web_auto_form_tool.json) |
| System Prompt 集成指南 | [SYSTEM_PROMPT.md](SYSTEM_PROMPT.md) |
| 步骤参考（全部参数） | [docs/STEPS.md](docs/STEPS.md) |
| 选择器指南 | [docs/SELECTORS.md](docs/SELECTORS.md) |
| PII 脱敏详解 | [docs/PII_REDACTION.md](docs/PII_REDACTION.md) |
| AI Agent 集成指南 | [docs/AI_AGENT_INTEGRATION.md](docs/AI_AGENT_INTEGRATION.md) |
| 示例配置 | [examples/](examples/) |
| 在线 Playground | [playground/](playground/) |
