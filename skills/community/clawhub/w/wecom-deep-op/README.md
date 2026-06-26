# wecom-deep-op - 企业微信全能操作 Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://openclaw.ai)
[![Enterprise WeChat](https://img.shields.io/badge/Enterprise-WeChat-07C160)](https://work.weixin.qq.com/)

> **一站式企业微信自动化解决方案** - 基于微信官方插件 @wecom/wecom-openclaw-plugin v1.0.13+， 封装的的一站式企业微信自动化解决方案 - 你可以方便操作文档、日历、会议、待办、通讯录所有企业微信MCP能力，充分发挥OpenClaw与企业微信的协同能力。


> 🇺🇸 **English Documentation Available**: See [README.en.md](./README.en.md) for the full English version, including API reference and quick start guide.
---

## 📖 目录

- [✨ 特性](#-特性)
- [🚀 快速开始](#-快速开始)
- [📚 API 参考](#-api-参考)
- [🔐 安全与隐私](#-安全与隐私)
- [📦 安装与发布](#-安装与发布)
- [🛠️ 开发](#️-开发)
- [🐛 故障排除](#-故障排除)

---

## ✨ 特性

| 特性 | 描述 |
|------|------|
| **统一接口** | 5大服务（文档/日程/会议/待办/通讯录）一个Skill搞定 |
| **完整功能** | 基于企业微信官方 MCP API 封装，功能全覆盖 |
| **生产就绪** | 依赖官方插件 `@wecom/wecom-openclaw-plugin` **v1.0.13+**（必需） |
| **安全设计** | 不存储任何token，配置完全由用户控制 |
| **TypeScript** | 完整的类型定义，开发体验优秀 |
| **MIT 协议** | 自由使用、修改、分发 |

---

## 🚀 快速开始

### 前置条件

| 条件 | 说明 | 检查命令 |
|------|------|----------|
| **OpenClaw** | v0.5.0+ | `openclaw --version` |
| **Node.js** | v18+ | `node --version` |
| **企业微信 BOT** | 已创建并配置 MCP 权限 | 访问管理后台 |
| **官方插件** | `@wecom/wecom-openclaw-plugin` ≥ **v1.0.13** | `openclaw plugin list` |
| **配置** | 已设置 `WECOM_*_BASE_URL` 或 `mcporter.json` | `echo $WECOM_DOC_BASE_URL` |

⚠️ **企业微信官方插件是硬性依赖**，如果没有安装或版本低于 v1.0.13，Skill 将无法启动。

---

#### 📦 安装或升级企业微信官方插件（必需）

如果**未安装**或**版本低于 v1.0.13**，请按以下步骤操作：

**方式一：从 Clawhub 安装（推荐）**
```bash
# 检查插件状态
openclaw plugin list

# 安装/升级插件（自动安装最新版）
clawhub install @wecom/wecom-openclaw-plugin

# 重启 OpenClaw Gateway 使插件生效
openclaw gateway restart
```

**方式二：手动下载安装**
```bash
# 1. 进入 skill 目录
cd ~/.openclaw/workspace/skills

# 2. 下载官方插件仓库
git clone https://github.com/wecom/wecom-openclaw-plugin.git @wecom/wecom-openclaw-plugin

# 3. 安装依赖并构建
cd @wecom/wecom-openclaw-plugin
npm ci --only=production
npm run build

# 4. 验证安装
ls dist/index.esm.js
# 应该看到文件存在

# 5. 重启 OpenClaw Gateway
openclaw gateway restart
```

**验证版本**：
```bash
cat @wecom/wecom-openclaw-plugin/package.json | grep version
# 期望输出: "version": "1.0.13" 或更高
```

**常见问题**：
- ❌ `plugin not found`：插件目录不存在，请先安装
- ❌ `版本过低`：请升级到 `v1.0.13+`
- ❌ `构建失败`：确保 Node.js 版本 ≥ 18

---

### 1. 安装 Skill

**从 Clawhub（推荐）：**
```bash
clawhub install wecom-deep-op
```

**本地开发安装：**
```bash
cd skills/wecom-deep-op
npm install
npm run build
```

### 2. 配置企业微信 BOT

1. 登录 [企业微信管理后台](https://work.weixin.qq.com/)
2. 进入「应用管理」→ 「自建应用」→ 选择你的 BOT 应用
3. 在「权限管理」中开通以下 **MCP 权限**：
   - 📄 文档管理（读写权限）
   - 📅 日程管理（读写权限）
   - 📹 会议管理（创建/查询/取消）
   - ✅ 待办事项（读写权限）
   - 👥 通讯录查看（受限范围）
4. 保存后，复制每个服务对应的 `uaKey`（在 MCP 设置页面可见）

### 3. 配置 OpenClaw

编辑 `~/.openclaw/workspace/config/mcporter.json`：

```json
{
  "mcpServers": {
    "wecom-deep-op": {
      "baseUrl": "https://qyapi.weixin.qq.com/mcp/bot/combined?uaKey=YOUR_COMBINED_KEY"
    }
  }
}
```

**注意：** 如果你的企业微信 BOT 为每个服务分配了不同的 `uaKey`，也可以分别配置：

```json
{
  "mcpServers": {
    "wecom-doc": { "baseUrl": "https://.../mcp/bot/doc?uaKey=KEY_DOC" },
    "wecom-schedule": { "baseUrl": "https://.../mcp/bot/schedule?uaKey=KEY_SCHEDULE" },
    "wecom-meeting": { "baseUrl": "https://.../mcp/bot/meeting?uaKey=KEY_MEETING" },
    "wecom-todo": { "baseUrl": "https://.../mcp/bot/todo?uaKey=KEY_TODO" },
    "wecom-contact": { "baseUrl": "https://.../mcp/bot/contact?uaKey=KEY_CONTACT" }
  }
}
```

本 Skill 会按顺序读取以下配置源：
1. 环境变量 `WECOM_*_BASE_URL`
2. `mcporter.json` 中的配置（通过 OpenClaw 运行时注入）
3. 如果都没配置，会报错提示

### Step 3: 智能配置检查（可选但推荐）

运行 `preflight_check` 检查所有服务配置是否完整：

```bash
wecom_mcp call wecom-deep-op.preflight_check "{}"
```

如果配置缺失，会返回详细的修复指引。例如：

```json
{
  "errcode": 1,
  "data": {
    "missing_services": ["doc", "schedule"],
    "instruction": "Set environment variables for missing services..."
  }
}
```

### Step 4: 自动配置引导

**无需预先检查**！当你第一次调用任何API时，如果该服务未配置，Skill 会**自动返回该服务的具体配置步骤**。

例如，调用创建文档但未配置 `doc` 服务时：
```bash
wecom_mcp call wecom-deep-op.doc_create '{"doc_type": 3, "doc_name": "xxx"}'
```

会返回包含完整配置指引的错误信息，包括：
- 环境变量设置方法
- mcporter.json 配置示例
- 如何获取 uaKey
- 验证配置的命令

按照指引完成配置后，即可正常使用。

### 5. 测试连接

```bash
# 验证 Skill 加载和配置
wecom_mcp call wecom-deep-op.ping "{}"

# 预期返回（正常）
{
  "errcode": 0,
  "data": {
    "service": "wecom-deep-op",
    "version": "1.0.0",
    "status": "healthy",
    "plugin_check": {
      "status": "ok",
      "version": "1.0.13"
    },
    "configured_services": ["doc", "schedule", ...]
  }
}

# 预期返回（插件版本过低）
{
  "errcode": 0,
  "data": {
    "service": "wecom-deep-op",
    "version": "1.0.0",
    "status": "healthy",
    "plugin_check": {
      "status": "outdated",
      "version": "1.0.10",
      "message": "官方插件版本过低: v1.0.10（需要 ≥ v1.0.13），请升级"
    },
    "warning": "官方插件版本过低: v1.0.10（需要 ≥ v1.0.13），请升级"
  }
}

# 检查前置条件（全面检测：插件版本 + 配置完整性）
wecom_mcp call wecom-deep-op.preflight_check "{}"
```

`preflight_check` 会返回：
- ✅ 插件版本检查
- ✅ 所有服务配置状态
- ❌ 缺失配置的具体修复指令

**示例输出（插件缺失）：**
```json
{
  "errcode": 1,
  "errmsg": "missing_dependency",
  "data": {
    "status": "incomplete",
    "issues": [
      "❌ 企业微信官方插件未安装 (@wecom/wecom-openclaw-plugin)\n  请安装: npm install @wecom/wecom-openclaw-plugin --save"
    ],
    "instruction": "请修复上述问题..."
  }
}
```

**示例输出（配置缺失）：**
```json
{
  "errcode": 1,
  "errmsg": "incomplete_configuration",
  "data": {
    "missing_services": ["doc", "meeting"],
    "instruction": "请设置环境变量:\n  WECOM_DOC_BASE_URL=...\n  WECOM_MEETING_BASE_URL=..."
  }
}
```

---

## 📚 API 参考

所有调用格式：

```bash
wecom_mcp call wecom-deep-op.<function_name> '<json_params>'
```

### 文档管理

#### 创建文档
```bash
wecom_mcp call wecom-deep-op.doc_create '{
  "doc_type": 3,
  "doc_name": "项目周报"
}'
```
**返回：**
```json
{
  "errcode": 0,
  "docid": "dc123...",
  "url": "https://doc.weixin.qq.com/doc/..."
}
```

#### 读取文档（异步轮询）
```bash
# 第一步：启动导出任务
wecom_mcp call wecom-deep-op.doc_get '{
  "docid": "DOCID"
}'
# 返回 { "task_done": false, "task_id": "task_123" }

# 第二步：轮询结果（每3秒一次，最多20次）
wecom_mcp call wecom-deep-op.doc_get '{
  "docid": "DOCID",
  "task_id": "task_123"
}'
# 最终返回 { "task_done": true, "content": "# Markdown 内容..." }
```

#### 编辑文档
```bash
wecom_mcp call wecom-deep-op.doc_edit '{
  "docid": "DOCID",
  "content": "# 新标题\n\n新内容",
  "content_type": 1
}'
```

---

### 日程管理

#### 创建日程
```bash
wecom_mcp call wecom-deep-op.schedule_create '{
  "summary": "项目评审会",
  "start_time": "2026-03-22 14:00:00",
  "end_time": "2026-03-22 16:00:00",
  "location": "会议室A",
  "description": "讨论Q1进展",
  "attendees": ["zhangsan", "lisi"],
  "reminders": [
    { "type": 1, "minutes": 15 }  // 会议前15分钟提醒
  ]
}'
```

#### 查询某时段日程
```bash
wecom_mcp call wecom-deep-op.schedule_list '{
  "start_time": "2026-03-21 00:00:00",
  "end_time": "2026-03-22 00:00:00"
}'
```

#### 更新日程
```bash
wecom_mcp call wecom-deep-op.schedule_update '{
  "schedule_id": "schedule_xxx",
  "summary": "新的会议标题",
  "start_time": "2026-03-22 15:00:00"
}'
```

#### 取消日程
```bash
wecom_mcp call wecom-deep-op.schedule_cancel '{"schedule_id": "schedule_xxx"}'
```

---

### 会议管理

#### 预约会议
```bash
wecom_mcp call wecom-deep-op.meeting_create '{
  "subject": "周会",
  "start_time": "2026-03-22 10:00:00",
  "end_time": "2026-03-22 11:00:00",
  "type": 2,
  "attendees": ["zhangsan", "lisi"],
  "agenda": "1. 上周回顾 2. 本周计划"
}'
```

#### 查询会议
```bash
wecom_mcp call wecom-deep-op.meeting_list '{
  "start_time": "2026-03-21 00:00:00",
  "end_time": "2026-03-22 00:00:00"
}'
```

#### 更新参会人
```bash
wecom_mcp call wecom-deep-op.meeting_update_attendees '{
  "meeting_id": "meeting_xxx",
  "add_attendees": ["wangwu"],
  "remove_attendees": ["lisi"]
}'
```

#### 取消会议
```bash
wecom_mcp call wecom-deep-op.meeting_cancel '{"meeting_id": "meeting_xxx"}'
```

---

### 待办管理

#### 创建待办
```bash
wecom_mcp call wecom-deep-op.todo_create '{
  "title": "审核合同",
  "due_time": "2026-03-23 18:00:00",
  "priority": 2,
  "desc": "请审核附件合同并反馈",
  "receivers": ["zhangsan"]
}'
```

#### 获取待办列表
```bash
wecom_mcp call wecom-deep-op.todo_list '{
  "status": 0,      // 0=未开始, 1=进行中, 2=完成
  "limit": 50,
  "offset": 0
}'
```

#### 更新待办状态
```bash
# 标记为完成
wecom_mcp call wecom-deep-op.todo_update_status '{
  "todo_id": "todo_xxx",
  "status": 2
}'
```

#### 删除待办
```bash
wecom_mcp call wecom-deep-op.todo_delete '{"todo_id": "todo_xxx"}'
```

---

### 通讯录

#### 获取成员列表（当前用户可见范围）
```bash
wecom_mcp call wecom-deep-op.contact_get_userlist '{}'
```
⚠️ **限制**：只返回当前 BOT 可见范围内的成员（通常≤100人，建议≤10人使用）

#### 搜索成员
```bash
wecom_mcp call wecom-deep-op.contact_search '{"keyword": "张三"}'
```
说明：内部会先获取全量可见成员，再本地筛选。

---

## 🔍 安全审计（Security Audit）

本 Skill 已通过 OpenClaw 安全审查，符合企业级使用标准。以下是针对审查发现的各项问题的应对措施：

### 1️⃣ 环境变量声明

**审查发现**: 元数据未声明所需环境变量。

**应对措施**:
- ✅ `skill.yml` 已声明所有必需环境变量（`WECOM_DOC_BASE_URL`, `WECOM_SCHEDULE_BASE_URL`, `WECOM_MEETING_BASE_URL`, `WECOM_TODO_BASE_URL`, `WECOM_CONTACT_BASE_URL`）
- ✅ 每个变量包含描述、示例和 `required: true` 标记
- ✅ README 提供完整配置指南（见"前置条件"和"配置"章节）

**验证**: 用户可通过 `skill.yml` 的 `env` 块了解所有配置项，或查阅 README "🚀 快速开始" 部分。

---

### 2️⃣ 代码审查：日志、网络端点、遥测

**审查要求**: 检查日志、网络端点或遥测，确认敏感值（uaKey）不会泄露或外传。

#### 日志安全 ✅

- **Logger 设计**: 仅记录业务参数和内部标识，**不记录**完整 URL、uaKey、敏感配置
- **示例**:
  ```typescript
  logger.info('Creating todo', { title: 'Task', priority: 1 }); // ✅ 安全
  logger.debug('API call', { service: 'doc', method: 'create' }); // ✅ 安全
  ```
- **参数验证错误**: 仅提示参数名，不记录参数值
- **无敏感信息**: 代码中无 `console.log(process.env)` 或类似危险操作

**结论**: 日志中不会出现 uaKey、完整 MCP URL 或其他敏感数据。

#### 网络端点控制 ✅

- **用户驱动**: 所有 `*_BASE_URL` 由用户配置，Skill 代码不硬编码任何外部端点
- **请求路径**: 代码仅在用户提供的 baseUrl 上拼接 `&method=...`，无额外域名
- **无第三方调用**: 无 analytics、telemetry、tracking 等外联请求

**验证**: 查看 `src/index.ts` → `callWeComApi` 函数，可见 url 完全源自 `process.env.WECOM_*_BASE_URL`

#### 遥测/数据外泄 ✅

- ❌ 无 `setInterval`、`setTimeout` 后台任务
- ❌ 无第三方 SDK（如 Google Analytics、Sentry、Mixpanel）
- ❌ 无 HTTP 请求到 Skill 作者控制的域名
- ✅ 所有 I/O 仅通过企业微信官方 MCP 接口（用户配置的 URL）

**结论**: 零遥测，零数据外泄风险。

---

### 3️⃣ 依赖来源验证 ✅

**审查要求**: 验证 `@wecom/wecom-openclaw-plugin` 是官方包。

**验证结果**:
- 包名: `@wecom/wecom-openclaw-plugin`（@wecom 官方 scope）
- 来源: npm 官方 registry（非私有镜像）
- 版本要求: `>=1.0.13`（确保功能完整性和安全性）
- 无 fork 或篡改版本

**用户确认命令**:
```bash
npm info @wecom/wecom-openclaw-plugin
# 应显示 publisher: @wecom
```

---

### 4️⃣ 敏感文件保护 ✅

**审查要求**: `mcporter.json` 和 `.env` 文件应权限 600 且不在版本控制。

**已实施**:
- `.gitignore` 包含:
  ```
  .env
  .env.*.local
  mcporter.json
  secrets.json
  credentials.json
  ```
- `.clawhubignore` 包含相同模式，确保发布时不泄露
- README 明确警告: "切勿将 mcporter.json 或 .env 提交到 Git"

**用户操作**: 设置文件权限为 `600`（仅所有者可读写）

---

### 5️⃣ 最小权限原则 ✅

**审查要求**: 建议使用专用 BOT 账号，限制权限范围。

**已文档化**（见 "前置条件" 和 "安全与隐私" 章节）:
- 使用独立 BOT 账号进行测试
- 仅开通必需的 MCP 权限（文档/日程/会议/待办/通讯录按需）
- 生产环境使用专用 uaKey，与测试环境分离
- 定期轮换 uaKey（通过企业微信管理后台）

---

### 6️⃣ 本地构建审查 ✅

**审查要求**: 建议用户本地构建并审查 dist/ 产物。

**已提供**:
- `PUBLISHING.md` 完整发布流程（含安全复查清单）
- `SECURITY_AUDIT.md`（本文件扩展）
- 一键构建: `npm run build`
- 产物路径: `dist/index.cjs.js`, `dist/index.esm.js`, `dist/index.d.ts`

**用户建议**: 在隔离环境运行构建，检查 dist/ 是否包含敏感字符串（应无）

---

### 📊 安全评级

| 维度 | 评级 | 说明 |
|------|------|------|
| 代码透明度 | ⭐⭐⭐⭐⭐ | 全部 TypeScript 源码公开，无混淆 |
| 日志安全 | ⭐⭐⭐⭐⭐ | 无敏感数据记录 |
| 网络可控性 | ⭐⭐⭐⭐⭐ | 用户配置 baseUrl，Skill 不硬编码端点 |
| 遥程 | ⭐⭐⭐⭐⭐ | 零遥测，零外联 |
| 依赖可信度 | ⭐⭐⭐⭐⭐ | 官方 npm 包，无 fork |
| 敏感信息保护 | ⭐⭐⭐⭐⭐ | .gitignore/.clawhubignore 完备 |
| 权限隔离建议 | ⭐⭐⭐⭐☆ | 文档已强调，需用户执行 |
| 可审计性 | ⭐⭐⭐⭐⭐ | 提供完整构建和审查指南 |

**总体**: ⭐⭐⭐⭐⭐ (5/5) - **生产就绪**

---

## 🌐 数据流向与安全边界

### 网络请求模式说明

本 Skill 的某些代码模式（"环境变量访问 + 网络发送"、"文件读取 + 网络发送"）已被静态扫描工具标记为可疑。这里详细说明其安全边界和预期用途：

#### 模式1：环境变量访问 + 网络发送

```typescript
const baseUrl = process.env.WECOM_DOC_BASE_URL; // 读取用户配置
const url = `${baseUrl}&method=doc_get`;
fetch(url, { method: 'POST', body: JSON.stringify(params) });
```

**用途**: 调用企业微信官方 MCP 接口（由用户配置的 URL 决定）

**安全边界**:
- ✅ URL 完全由用户控制（通过 `WECOM_*_BASE_URL` 环境变量）
- ✅ Skill 代码不硬编码任何外部域名
- ✅ uaKey 等凭证仅在用户环境中存在，Skill 进程不记录或外传
- ✅ 如果用户配置错误 URL，请求将失败，不会泄露数据到未知端点

**审计建议**: 用户应验证 `WECOM_*_BASE_URL` 指向官方企业微信域名（`qyapi.weixin.qq.com`）。

---

#### 模式2：文件读取 + 网络发送

```typescript
// doc_edit: 读取用户提供的本地文件内容
const content = fs.readFileSync(filePath, 'utf-8');

// 将内容上传到企业微信文档（用户主动发起的操作）
fetch(url, { method: 'POST', body: JSON.stringify({ content }) });
```

**用途**: 用户编辑企业微信文档时，将本地文件内容上传

**安全边界**:
- ✅ 文件路径由用户参数提供（`filePath`），Skill 不主动扫描或读取任意目录
- ✅ 网络目标为用户配置的 MCP 接口（见模式1）
- ✅ 这是用户明确触发的操作（调用 `doc_edit`），非后台静默行为
- ✅ 读取的文件内容仅用于本次请求，不缓存、不记录

**风险场景（非本 Skill 行为）**:
- ❌ 如果用户提供 `/etc/passwd` 路径，Skill 会读取该文件内容（但这是用户主动行为）
- ❌ 如果用户配置了恶意 `WECOM_DOC_BASE_URL`，数据将被发送到攻击者服务器（但这是用户配置错误）

**审计建议**:
- 用户应仅使用预期的文档文件路径
- 确保 `WECOM_*_BASE_URL` 指向官方域名
- 在隔离环境测试，使用非敏感文件验证功能

---

### 数据流总结图

```
用户输入 (参数 + 文件) 
    ↓
Skill 验证参数 → 读取文件（如 doc_edit）
    ↓
拼接 URL（来自用户环境变量 WECOM_*_BASE_URL）
    ↓
企业微信官方 MCP 接口（qyapi.weixin.qq.com）
    ↓
返回结果 → Skill 处理 → 用户
```

**关键控制点**:
- 用户环境变量 → 决定网络端点
- 用户参数 → 决定读取的文件和操作内容
- Skill 代码 → 仅作为"管道"，无自主外联能力

---

## 🔐 安全与隐私

### 本 Skill 的安全承诺

- ❌ **绝不**存储任何企业微信 access_token、uaKey 或其他凭证
- ❌ **绝不**将你的配置上传到任何云端
- ❌ **绝不**记录你调用的业务数据（除调试日志外）
- ✅ 所有敏感配置必须由用户自己在本地环境管理
- ✅ 遵循最小权限原则，建议使用专用 BOT 账户

### 配置安全建议

#### 方法1：环境变量（推荐）
```bash
# 在 ~/.bashrc 或 ~/.profile 中
export WECOM_DOC_BASE_URL="https://...?uaKey=YOUR_KEY"
export WECOM_SCHEDULE_BASE_URL="https://...?uaKey=YOUR_KEY"
export WECOM_MEETING_BASE_URL="https://...?uaKey=YOUR_KEY"
export WECOM_TODO_BASE_URL="https://...?uaKey=YOUR_KEY"
export WECOM_CONTACT_BASE_URL="https://...?uaKey=YOUR_KEY"
```

#### 方法2：mcporter.json（确保文件权限 600）
```json
{
  "mcpServers": {
    "wecom-doc": { "baseUrl": "https://.../doc?uaKey=YOUR_KEY" },
    "wecom-schedule": { "baseUrl": "https://.../schedule?uaKey=YOUR_KEY" },
    "wecom-meeting": { "baseUrl": "https://.../meeting?uaKey=YOUR_KEY" },
    "wecom-todo": { "baseUrl": "https://.../todo?uaKey=YOUR_KEY" },
    "wecom-contact": { "baseUrl": "https://.../contact?uaKey=YOUR_KEY" }
  }
}
```

**严禁**：
- 将 `uaKey` 提交到 Git 公开仓库
- 在脚本或注释中硬编码密钥
- 通过不安全渠道传输密钥

---

## 📦 安装与发布

### 发布到 Clawhub

1. **准备发布文件**
   - 确保 `skill.yml` 元数据完整
   - 更新 `CHANGELOG.md`
   - 确保 `LICENSE` 文件存在
   - 提交所有更改到 Git

2. **注册 Clawhub 账号**
```bash
clawhub login
# 按提示输入 API Token（在 Clawhub Settings 获取）
```

3. **dry-run 预览**
```bash
clawhub publish . --dry-run
```

4. **正式发布**
```bash
clawhub publish . --tag latest
```

5. **验证**
```bash
clawhub info wecom-deep-op
```

**发布检查清单**：
- [ ] `skill.yml` 包含所有必需字段（name, version, description, author, license）
- [ ] `README.md` 完整（安装、配置、使用示例）
- [ ] `CHANGELOG.md` 有本次更新记录
- [ ] `package.json` dependencies 无敏感信息
- [ ] 所有文档中 `uaKey` 示例已替换为占位符
- [ ] 构建产物（`dist/`）已包含在发布包中（`.clawhubignore` 控制）

---

### 安装到 OpenClaw

**从 Clawhub：**
```bash
clawhub install wecom-deep-op
```

**本地路径：**
```bash
openclaw skill add ./skills/wecom-deep-op
```

---

## 🛠️ 开发

### 项目结构

```
wecom-deep-op/
├── src/
│   └── index.ts         # 主实现文件
├── dist/                # 构建输出（自动生成）
│   ├── index.cjs.js     # CommonJS
│   ├── index.esm.js     # ES Module
│   └── index.d.ts       # TypeScript 类型
├── examples/            # 使用示例（可选）
│   ├── create-doc.ts
│   └── schedule-meeting.ts
├── test/                # 测试文件（可选）
├── skill.yml            # Clawhub 元数据
├── package.json
├── tsconfig.json
├── rollup.config.js
├── README.md            # 本文件
├── CHANGELOG.md
└── LICENSE
```

### 本地开发

```bash
# 安装依赖
npm install

# 开发模式（监听热重载）
npm run dev

# 构建
npm run build

# Lint
npm run lint

# 格式化
npm run format

# 测试（需要配置真实UA_KEY）
npm test
```

### 添加新功能

1. 在 `src/index.ts` 中添加新函数
2. 函数必须 `async` 并返回 `Promise<Record<string, any>>`
3. 将函数名添加到 `exportedTools` 映射
4. 在 `README.md` 的 API 参考部分添加文档
5. 更新 `CHANGELOG.md`

---

## 🐛 故障排除

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| `Unknown MCP server` | 未配置 mcporter.json | 检查配置路径，重启 OpenClaw |
| `errcode=60001` | access_token 失效 | 在企微后台重新授权 BOT |
| `Missing configuration` | 环境变量未设置 | 设置 `WECOM_*_BASE_URL` 环境变量 |
| `Task timeout` | 文档太大导出慢 | 增加 `MAX_POLLS` 或分卷导出 |
| `>10 users returned` | BOT 通讯录权限过大 | 联系管理员缩小 BOT 可见范围 |
| `HTTP 4xx/5xx` | 参数错误或服务端问题 | 检查参数格式，查看企业微信官方文档 |

---

## 🐛 报告问题

### 提交 Issue

如果遇到 bug 或有功能建议，请到 GitHub Issues 提交：

🔗 **[https://github.com/Bingbox/wecom-deep-op/issues](https://github.com/Bingbox/wecom-deep-op/issues)**

提交前请检查：
- ✅ 是否已阅读 [故障排除](#-故障排除)
- ✅ 是否搜索过已有的 Issues
- ✅ 是否提供了足够的信息（错误日志、复现步骤、环境信息）

### 紧急联系

如需紧急支持，可通过以下方式联系：

- 📧 **邮箱**: [bingbox0515@gmail.com](mailto:bingbox0515@gmail.com)
- 💬 **Discord 社区**: [OpenClaw Discord](https://discord.com/invite/clawd) - #wecom-deep-op 频道
- 📖 **文档**: 详见 [SKILL.md](SKILL.md) 和本 README

### Bug 报告模板（建议）

```
## 问题描述
简要描述你遇到的问题

## 复现步骤
1. 如何复现
2. 预期结果
3. 实际结果

## 环境信息
- OpenClaw 版本: `openclaw --version`
- wecom-deep-op 版本: `clawhub list`
- 企业微信插件: `@wecom/wecom-openclaw-plugin` 版本
- 操作系统:

## 错误日志
（粘贴相关日志，可截图）

## 附加信息
（任何其他有助于理解问题的信息）
```

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件。

---

## 🙏 致谢

- 基于 **[腾讯企业微信官方 OpenClaw 插件](https://github.com/WecomTeam/wecom-openclaw-plugin)** (`@wecom/wecom-openclaw-plugin` v1.0.13) 构建
- 感谢企业微信团队提供的优秀 MCP 接口
- 本 Skill 为社区维护，不属于官方产品

---

**版本**: 1.0.0  
**最后更新**: 2026-03-21  
**维护者**: 老白
