# UCTOO API Skill (V2)

## 概述

这是 uctoo-api-skill 的 V2 版本，采用完全重构的架构，真正发挥大模型的语义理解和推理能力。

## 核心理念

### 从 V1 到 V2 的转变

**V1 (旧架构)**:
- 硬编码关键词提取
- 固定的 API 调用逻辑
- 大量的代码实现
- 脆弱且难以维护

**V2 (新架构)**:
- 大模型驱动的语义理解
- 灵活的 API 选择和参数组装
- 极简代码实现
- 易于维护和扩展

## 架构设计

### 分层架构

```
┌─────────────────────────────────────────────────────────┐
│                     用户输入                           │
│         "请使用 demo 账号 123456 登录"                │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              大模型（知识层 + 推理）                    │
│  ┌───────────────────────────────────────────────────┐ │
│  │ 1. 理解用户意图：需要登录                          │ │
│  │ 2. 识别参数：username=demo, password=123456      │ │
│  │ 3. 选择 API：POST /api/uctoo/auth/login           │ │
│  │ 4. 组装请求体：{"username":"demo","password":"123456"}│ │
│  │ 5. 调用 HTTP 工具执行请求                          │ │
│  │ 6. 解析响应并生成友好回复                          │ │
│  └───────────────────────────────────────────────────┘ │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│                 HTTP 工具（连接层）                     │
│              执行实际的 API 请求                        │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│                 UCTOO 后端 API                          │
└─────────────────────────────────────────────────────────┘
```

## 文件结构

```
uctoo-api-skill/
├── SKILL.md                          # 主技能文件（知识层）
├── README.md                         # 本文件
├── Main.cj                           # 入口点（用于测试）
├── references/                       # 参考文档
│   ├── api_spec.md                   # 完整的 API 规范
│   ├── examples.md                   # 使用示例
│   └── uctoo_api_design.md          # API 设计文档
├── scripts/                          # 脚本工具
│   ├── api_client.py                 # HTTP 客户端（主要使用）
│   ├── api_client.js                 # JavaScript 版本（备用）
│   └── test_api.py                   # API 测试脚本
├── src/                              # 源代码
│   └── uctoo_api_skill.cj           # 极简技能实现
└── backup-v1/                        # V1 版本备份
    └── ...
```

## 快速开始

### 1. 测试 API 连接

```bash
python scripts/test_api.py
```

### 2. 手动测试登录

```bash
python scripts/api_client.py POST "/api/uctoo/auth/login" '{"username":"demo","password":"123456"}'
```

### 3. 使用技能

技能会通过 Agentskills 运行时自动加载，大模型会根据 SKILL.md 中的说明来使用它。

## SKILL.md 结构

SKILL.md 采用渐进式披露（Progressive Disclosure）原则：

### Level 1: YAML Frontmatter
- 快速扫描信息
- 技能名称、描述、元数据
- 允许的工具列表

### Level 2: Markdown 主体
- 详细说明
- API 快速参考
- 使用示例
- 工作流程

### Level 3: 链接的参考文档
- 完整的 API 规范
- 更多使用示例
- 深入的技术文档

## 核心优势

1. **充分利用大模型能力**
   - 语义理解、推理、决策都由大模型完成
   - 能处理各种自然语言变体

2. **极高的灵活性**
   - 不需要硬编码每个 API 的处理逻辑
   - 大模型可以自适应各种用户输入

3. **易于维护**
   - API 变更只需更新文档
   - 不需要修改代码

4. **易于扩展**
   - 新增 API 只需在文档中添加说明
   - 大模型会自动学会使用新 API

5. **符合最佳实践**
   - 完全符合 Agentskills 标准
   - 采用渐进式披露原则

## 自动 Token 管理（V7.0+）

### 概述

从 V7.0 版本开始，系统实现了**会话级自动 Token 管理机制**，彻底解决了大模型在多轮对话中无法正确传递认证 Token 的问题。

### 架构设计

```
┌─────────────────────────────────────────────────────────────┐
│                    WebSocket Session                         │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                 SessionContext                        │    │
│  │  - setCurrentSession(sessionId)                       │    │
│  │  - getAccessToken() → TokenManager.getAccessToken()   │    │
│  └─────────────────────────────────────────────────────┘    │
│                            │                                 │
│                            ▼                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                   TokenManager                        │    │
│  │  - setToken(sessionId, tokenInfo)                     │    │
│  │  - getAccessToken(sessionId)                          │    │
│  │  - parseLoginResponse(response)                       │    │
│  │  - isLoginEndpoint(url)                               │    │
│  └─────────────────────────────────────────────────────┘    │
│                            │                                 │
│                            ▼                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                     HttpTool                          │    │
│  │  1. 检测登录请求 → 自动保存 token                      │    │
│  │  2. 检测非登录请求 → 自动注入 Authorization header     │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### 核心组件

| 组件 | 文件 | 功能 |
|------|------|------|
| TokenInfo | `src/tool/token_manager.cj` | Token 信息封装，包含过期时间检查 |
| TokenManager | `src/tool/token_manager.cj` | Token 存储和管理，支持多会话 |
| SessionContext | `src/tool/token_manager.cj` | 当前会话上下文，线程安全 |
| HttpTool | `src/tool/http_tool.cj` | 自动 token 保存和注入 |

### 工作流程

#### 1. 登录时自动保存 Token

```cangjie
// HttpTool 检测到登录请求
if (tokenManager.isLoginEndpoint(url)) {
    // 解析响应并保存 token
    let tokenInfoOpt = tokenManager.parseLoginResponse(responseJson)
    match (tokenInfoOpt) {
        case Some(tokenInfo) =>
            tokenManager.setToken(sessionId, tokenInfo)
            LogUtils.info("[HttpTool] Auto-saved token for session")
        case None => ()
    }
}
```

#### 2. 后续请求自动注入 Authorization

```cangjie
// HttpTool 检测到非登录请求
if (!hasAuthorization && !tokenManager.isLoginEndpoint(url)) {
    let tokenOpt = sessionContext.getAccessToken()
    match (tokenOpt) {
        case Some(token) =>
            headers.add("Authorization", "Bearer ${token}")
            LogUtils.info("[HttpTool] Auto-injected Authorization header")
        case None => ()
    }
}
```

#### 3. 会话结束时清理

```cangjie
// WebSocket 会话关闭时
tokenManager.removeToken(sessionId)
sessionContext.clearCurrentSession()
```

### 优势

1. **对模型透明**：大模型无需关心 token 管理，只需正常调用 API
2. **可靠性高**：不依赖大模型的记忆能力，避免 token 丢失或格式错误
3. **支持多用户**：每个 WebSocket 会话独立管理 token
4. **自动过期处理**：TokenInfo 包含过期时间，自动检查 token 有效性
5. **线程安全**：使用 Mutex 保护共享状态

### 使用示例

用户只需正常对话，系统自动处理认证：

```
用户: 请使用 demo 账号 123456 登录
助手: 登录成功！用户信息：...

用户: 编辑 id 为 fd0a410a-xxx 的实体，将 link 改为 uctoo.com
助手: 编辑成功！  # 系统自动注入了 Authorization header
```

### 技术细节

- **登录端点检测**：通过 URL 中是否包含 `/auth/login` 或 `/auth/signin` 判断
- **Token 解析**：从 JSON 响应中提取 `access_token`、`refresh_token`、`user.id`、`user.username`
- **默认过期时间**：24 小时（86400000 毫秒）
- **Header 注入格式**：`Authorization: Bearer {token}`

## 工作原理

### 1. 技能激活
当用户提及 "uctoo"、"登录"、"用户管理" 等关键词时，技能会被激活。

### 2. 大模型理解
大模型读取 SKILL.md 中的说明，理解：
- 有哪些 API 可用
- 如何调用这些 API
- 需要什么参数
- 如何处理响应

### 3. 决策与执行
大模型根据用户需求：
1. 选择合适的 API
2. 从用户输入中提取参数
3. 调用 Python 脚本发送 HTTP 请求
4. 解析 API 响应
5. 生成友好的自然语言回复

## 与 V1 的对比

| 特性 | V1 | V2 |
|------|-----|-----|
| 代码量 | 大量（10+ 文件） | 极少（2 个文件） |
| 语义理解 | 硬编码关键词 | 大模型自然语言理解 |
| API 选择 | 固定逻辑 | 大模型动态决策 |
| 参数提取 | 正则表达式 | 大模型智能提取 |
| 可维护性 | 低（需改代码） | 高（只需改文档） |
| 可扩展性 | 低 | 高 |
| 灵活性 | 低 | 极高 |

## 注意事项

1. **Token 管理**
   - 登录成功后，大模型会保存 access_token
   - 后续请求需要使用这个 token

2. **API 格式**
   - 所有 API 都使用 `/api/uctoo/` 前缀
   - POST 请求的请求体必须是有效的 JSON

3. **错误处理**
   - 大模型会自动处理 API 错误
   - 向用户提供友好的错误信息和解决方案

## 下一步

- 测试通过聊天界面使用技能
- 验证登录功能
- 测试基本的 CRUD 操作
- 根据实际使用情况优化 SKILL.md

## 参考资料

- [Agentskills 最佳实践](https://github.com/vercel-labs/agent-skills)
- [UCTOO API 设计规范](../../../../apps/backend/docs/uctooAPI设计规范.md)
- [重构方案文档](./REFACTORING_PLAN_v2.md)
