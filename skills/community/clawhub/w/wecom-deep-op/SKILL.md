---
name: wecom-deep-op
description: 基于微信官方插件 @wecom/wecom-openclaw-plugin v1.0.13+，封装的一站式企业微信自动化解决方案 - 你可以方便操作文档、日历、会议、待办、通讯录所有企业微信MCP能力，充分发挥OpenClaw与企业微信的协同能力。
version: 2.0.2
author: 老白
license: MIT
dependencies:
  - name: "@wecom/wecom-openclaw-plugin"
    version: ">=1.0.13"
    type: npm
    required: true
  - name: "openclaw"
    version: ">=0.5.0"
    type: core

---

# wecom-deep-op - 企业微信全能操作 Skill

> **基于微信官方插件 @wecom/wecom-openclaw-plugin v1.0.13+，一站式企业微信自动化解决方案**

`wecom-deep-op` 是对企业微信官方 MCP 服务的统一封装，你可以方便操作文档、日历、会议、待办、通讯录所有企业微信MCP能力，充分发挥 OpenClaw 与企业微信的协同能力。

**重要：请务必先阅读前置条件！**

---

## 📋 前置条件

---

## ✨ 核心优势

| 特性 | 说明 |
|------|------|
| **统一接口** | 不再需要记忆5个不同的MCP服务名，全部通过 `wecom-deep-op` 调用 |
| **前置检查** | 内置 `wecom-preflight` 自动检查，确保授权配置正确 |
| **完整功能** | 文档、日程、会议、待办、通讯录全覆盖 |
| **生产就绪** | 基于官方插件（v1.0.13）构建，稳定可靠 |
| **安全设计** | 不存储任何token，所有配置由用户自己管理 |

---

## 🚀 快速开始

### 1. 前置条件

- ✅ OpenClaw 已安装（v0.5.0+）
- ✅ Node.js 环境（v18+）
- ✅ 已安装 `@wecom/wecom-openclaw-plugin`（官方插件）
- ✅ 企业微信管理员已创建 BOT 并配置 MCP 权限

### 2. 安装 Skill

```bash
# 方法1: 从Clawhub安装（推荐）
clawhub install wecom-deep-op

# 方法2: 本地安装（开发中）
cd /path/to/wecom-deep-op
npm install
npm run build
```

### 3. 授权配置

**重要：** 本 Skill 不会也不应该包含任何企业微信的敏感凭证。你需要自己完成授权。

#### Step 1: 获取企业微信 BOT 的 MCP 权限

1. 登录 [企业微信管理后台](https://work.weixin.qq.com/)
2. 进入「应用管理」→ 「自建应用」→ 选择你的 BOT 应用
3. 在「权限管理」中开通以下 MCP 权限：
   - ✅ 文档管理（读写）
   - ✅ 日程管理（读写）
   - ✅ 会议管理（创建/查询/取消）
   - ✅ 待办事项（读写）
   - ✅ 通讯录查看（受限范围）
4. 保存后，复制 `uaKey` 参数（在 MCP 设置页面可见）

#### Step 2: 配置 OpenClaw

编辑 OpenClaw 配置文件（或通过 `mcporter`）：

```json
// ~/.openclaw/workspace/config/mcporter.json
{
  "mcpServers": {
    "wecom-deep-op": {
      "baseUrl": "https://qyapi.weixin.qq.com/mcp/bot/combined?uaKey=YOUR_UA_KEY"
    }
  }
}
```

**注意：**
- `YOUR_UA_KEY` 替换为企业微信 BOT 真实的 `uaKey`
- 该配置仅为示例，实际使用时会根据技能部署情况调整端点
- 所有 UA_KEY 必须通过环境变量或配置文件管理，**禁止硬编码**

#### Step 3: 测试连接

```bash
# 使用 mcporter 测试
mcporter --config ~/.openclaw/workspace/config/mcporter.json call wecom-deep-op.ping "{}"
```

期望返回：
```json
{
  "errcode": 0,
  "errmsg": "ok",
  "data": {
    "service": "wecom-deep-op",
    "version": "1.0.0",
    "status": "healthy"
  }
}
```

---

## 📚 使用指南

### 统一调用模式

所有操作都通过 `wecom_mcp` tool 调用：

```bash
# 语法
wecom_mcp call wecom-deep-op.<function_name> '<json_params>'

# 示例：创建文档
wecom_mcp call wecom-deep-op.doc_create '{"doc_name": "项目周报", "content": "# 周报\n\n..."}'

# 示例：查询日程
wecom_mcp call wecom-deep-op.schedule_list '{"start_time": "2026-03-21 00:00:00", "end_time": "2026-03-22 00:00:00"}'
```

---

### 📄 文档管理 (`doc_*`)

#### 创建文档
```bash
wecom_mcp call wecom-deep-op.doc_create '{"doc_type": 3, "doc_name": "会议纪要"}'
```
返回：`{ "errcode": 0, "docid": "xxx", "url": "https://..." }`

#### 读取文档
```bash
# 首次调用（开始导出）
wecom_mcp call wecom-deep-op.doc_get '{"docid": "DOCID", "type": 2}'

# 轮询（如果 task_done=false，用返回的 task_id 继续调用）
wecom_mcp call wecom-deep-op.doc_get '{"docid": "DOCID", "type": 2, "task_id": "xxx"}'
```

#### 编辑文档
```bash
wecom_mcp call wecom-deep-op.doc_edit '{"docid": "DOCID", "content": "# 新内容\n\nMarkdown格式", "content_type": 1}'
```

---

### 📅 日程管理 (`schedule_*`)

#### 创建日程
```bash
wecom_mcp call wecom-deep-op.schedule_create '{
  "summary": "项目评审会",
  "start_time": "2026-03-22 14:00:00",
  "end_time": "2026-03-22 16:00:00",
  "location": "会议室A",
  "description": "讨论Q1进展",
  "attendees": ["userid1", "userid2"]
}'
```

#### 查询日程
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
  "summary": "新的标题",
  "start_time": "2026-03-22 15:00:00"
}'
```

#### 取消日程
```bash
wecom_mcp call wecom-deep-op.schedule_cancel '{"schedule_id": "schedule_xxx"}'
```

---

### 📹 会议管理 (`meeting_*`)

#### 预约会议
```bash
wecom_mcp call wecom-deep-op.meeting_create '{
  "subject": "周会",
  "start_time": "2026-03-22 10:00:00",
  "end_time": "2026-03-22 11:00:00",
  "type": 2,
  "attendees": ["zhangsan", "lisi"]
}'
```

#### 查询会议
```bash
wecom_mcp call wecom-deep-op.meeting_list '{
  "start_time": "2026-03-21 00:00:00",
  "end_time": "2026-03-22 00:00:00"
}'
```

#### 取消会议
```bash
wecom_mcp call wecom-deep-op.meeting_cancel '{"meeting_id": "meeting_xxx"}'
```

#### 更新参会人
```bash
wecom_mcp call wecom-deep-op.meeting_update_attendees '{
  "meeting_id": "meeting_xxx",
  "add_attendees": ["wangwu"],
  "remove_attendees": ["lisi"]
}'
```

---

### ✅ 待办管理 (`todo_*`)

#### 创建待办
```bash
wecom_mcp call wecom-deep-op.todo_create '{
  "title": "审核合同",
  "due_time": "2026-03-23 18:00:00",
  "priority": 2,
  "desc": "请审核附件合同并反馈"
}'
```

#### 获取待办列表
```bash
wecom_mcp call wecom-deep-op.todo_list '{
  "status": 0,
  "limit": 50
}'
```

#### 获取待办详情
```bash
wecom_mcp call wecom-deep-op.todo_get '{"todo_id": "todo_xxx"}'
```

#### 更新待办状态
```bash
wecom_mcp call wecom-deep-op.todo_update_status '{
  "todo_id": "todo_xxx",
  "status": 2
}'  # 2=完成, 1=进行中, 0=未开始
```

#### 删除待办
```bash
wecom_mcp call wecom-deep-op.todo_delete '{"todo_id": "todo_xxx"}'
```

---

### 👥 通讯录 (`contact_*`)

#### 获取成员列表
```bash
wecom_mcp call wecom-deep-op.contact_get_userlist '{}'
```
返回：
```json
{
  "errcode": 0,
  "userlist": [
    {"userid": "zhangsan", "name": "张三", "alias": "Sam"},
    {"userid": "lisi", "name": "李四", "alias": ""}
  ]
}
```

⚠️ **限制**：只返回当前用户**可见范围内**的成员（通常≤100人，建议≤10人使用）

#### 搜索成员
```bash
wecom_mcp call wecom-deep-op.contact_search '{"keyword": "张三"}'
```
本地筛选模式下，Skill 会自动调用 `get_userlist` 并在结果中匹配姓名/别名。

---

## 🔧 错误处理

所有接口返回标准格式：

```json
{
  "errcode": 0,
  "errmsg": "ok",
  "data": { ... }  // 实际数据
}
```

**错误码说明**：
- `0`: 成功
- `非0`: 失败，参考 `errmsg` 并结合原始企业微信错误码

**重试策略**：
- 网络错误（超时、连接失败）：自动重试 1 次
- 业务错误（权限不足、参数错误）：停止并返回错误给用户
- 文档导出 `task_done=false`：需用户轮询（每3秒一次，最多10次）

---

## 🏗️ 架构说明

### 依赖关系

```
OpenClaw Plugin System
    └── @wecom/wecom-openclaw-plugin (官方插件 v1.0.13)
          ├── wecom-doc (文档)
          ├── wecom-schedule (日程)
          ├── wecom-meeting (会议)
          ├── wecom-todo (待办)
          └── wecom-contact (通讯录)
                ↑
          [本 Skill 聚合层]
                ↑
          wecom-deep-op (统一接口)
```

### 技术实现

- **Skill 类型**: OpenClaw Skill (Plugin Extension)
- **运行环境**: Node.js (v18+)
- **通信协议**: MCP (Model Context Protocol)
- **底层 SDK**: `@wecom/aibot-node-sdk` (v1.0.3)
- **构建工具**: Rollup (输出 ESM + CommonJS)

---

## 🔐 安全与隐私

### 本 Skill 不会：
- ❌ 存储任何企业微信 access_token 或凭证
- ❌ 将你的配置上传到任何云端
- ❌ 记录你调用的具体业务数据（日志除外）
- ❌ 包含任何租户特定的信息

### 你需要负责：
- ✅ 安全保管 `uaKey`（等同于密码）
- ✅ 在企业微信控制台定期审计 BOT 权限
- ✅ 使用环境变量或加密配置文件存储 `uaKey`
- ✅ 不要将 `mcporter.json` 提交到公开仓库

### 建议配置方式

```bash
# 将 uaKey 放入环境变量（推荐）
export WECOM_UA_KEY="your_ua_key_here"

# mcporter.json 中引用环境变量
{
  "mcpServers": {
    "wecom-deep-op": {
      "baseUrl": "https://qyapi.weixin.qq.com/mcp/bot/combined?uaKey=${WECOM_UA_KEY}"
    }
  }
}
```

---

## 🛠️ 开发与发布

### 开发环境

```bash
cd skills/wecom-deep-op
npm install
npm run dev   # 监听模式
npm test      # 运行测试
```

### 构建

```bash
npm run build
# 输出:
# - dist/index.cjs.js
# - dist/index.esm.js
# - dist/index.d.ts
```

### Lint & Format

```bash
npm run lint
npm run format
```

---

## 📦 发布到 Clawhub

### 1. 准备发布清单

- [ ] 完善 `skill.yml`（元数据）
- [ ] 编写 `README.md`（详细使用说明）
- [ ] 添加 `CHANGELOG.md`
- [ ] 确保 `LICENSE` 文件存在（MIT）
- [ ] 编写示例脚本（`examples/` 目录）
- [ ] 生成 TypeScript 类型定义（`npm run build`）
- [ ] 在 `skill.yml` 中声明依赖：`@wecom/wecom-openclaw-plugin`

### 2. 注册 Clawhub 账号

```bash
# 登录 Clawhub CLI
clawhub login
# 按照提示输入 API Token（在 Clawhub Settings 获取）
```

### 3. 发布

```bash
#  dry-run 预览
clawhub publish . --dry-run

# 真实发布
clawhub publish . --tag latest
```

发布后，其他用户可通过以下方式安装：
```bash
clawhub install wecom-deep-op
# 或
openclaw skill add wecom-deep-op
```

---

## 📝 与其他技能的集成

### 与 `wecom-preflight` 协同

首次调用前，建议用户先运行：

```bash
wecom_mcp call wecom-preflight.check '{}'
```

该 Skill 会：
1. 检查 `mcporter.json` 配置是否存在
2. 验证 wecom-deep-op 是否在白名单
3. 如缺失，提供修复命令

### 与 `wecom-get-todo-list` 的差异

`wecom-deep-op` 是**底层 MCP 的直接包装**，适合需要精细控制的场景。
`wecom-get-todo-list` 是**业务导向的上层技能**，提供更高级的筛选和展示。

你可以同时使用两者，根据场景选择：
- 简单任务：用 `wecom-deep-op.todo_list`
- 复杂查询（过滤+分页）：用 `wecom-get-todo-list`

---

## 🐛 故障排除

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| `Unknown MCP server` | mcporter.json 未配置 | 检查配置路径，确保 `wecom-deep-op` 在 `mcpServers` 中 |
| `errcode=60001` | access_token 失效 | 重新授权 BOT，确保 MCP 权限已开启 |
| `task_done=false` 一直轮询 | 文档过大，导出超时 | 增加 `wait_timeout` 参数，或分卷导出 |
| `超过10人`错误 | 通讯录可见范围太大 | 联系管理员缩小 BOT 的通讯录权限范围 |
| 调用超时 | 网络问题或响应慢 | 检查企业微信网络连通性，调整 `yieldMs` |

---

## 📄 许可证

MIT License - 详见 `LICENSE` 文件。

---

## 🙏 致谢

- 基于 **腾讯企业微信官方 OpenClaw 插件** (`@wecom/wecom-openclaw-plugin`) 构建
- 感谢企业微信团队提供优秀的 MCP 接口
- 本 Skill 为社区封装，不属于官方产品

---

**维护者**: 白小圈 (市场调研专家 AI 助手)
**版本**: 1.0.0
**最后更新**: 2026-03-21
