# uctoo_api_skill 重构方案

**文档版本**: 2.0  
**创建日期**: 2026-02-27  
**状态**: 设计中

---

## 一、重构目标

### 1.1 核心目标
将 `uctoo_api_skill` 从当前依赖 `uctoo_api_mcp_server` 的架构重构为**完全独立、自包含的 Agent Skill**，只需依赖 `agentskills-runtime` 即可运行，无需依赖其他 MCP 服务器或技能。

### 1.2 具体目标
- ✅ **完全独立运行**：无需 MCP 服务器，直接在 agentskills-runtime 中执行
- ✅ **符合官方最佳实践**：遵循 Claude 官方技能创建指南
- ✅ **集成门控系统**：利用门控系统检测执行环境能力
- ✅ **多脚本语言支持**：超越标准，支持 JavaScript、Cangjie 等多种脚本
- ✅ **渐进式披露设计**：遵循三层加载模式，优化上下文使用

---

## 二、当前架构分析

### 2.1 当前依赖关系
```
uctoo_api_skill (技能实现)
    ↓ 依赖
uctoo_api_mcp_server (MCP协议处理)
    ↓ 依赖
CangjieMagic框架 + agentskills增强
    ↓ 依赖
agentskills-runtime (运行时内核)
```

### 2.2 当前职责分工
| 组件 | 职责 | 问题 |
|------|------|------|
| `uctoo_api_skill` | 自然语言理解、API映射、认证管理 | 不直接发起HTTP请求 |
| `uctoo_api_mcp_server` | MCP协议通信、实际HTTP请求、响应格式化 | 与技能逻辑耦合 |

### 2.3 存在的问题
1. **依赖关系复杂**：需要同时运行两个项目
2. **职责不清**：HTTP请求逻辑分散在两个组件中
3. **不符合技能标准**：没有遵循官方的技能目录结构
4. **无法独立分发**：技能无法作为独立包发布和使用

---

## 三、重构后的架构设计

### 3.1 目标架构
```
uctoo_api_skill (完全独立的技能包)
    ↓ 直接依赖
agentskills-runtime (运行时内核 + 门控系统)
    ↓ 使用
大模型 API + 后端 API
```

### 3.2 技能目录结构（符合官方标准）
```
uctoo_api_skill/
├── SKILL.md                          # 必需：技能主文件（YAML frontmatter + Markdown）
├── scripts/                          # 可选：可执行脚本
│   ├── api_client.cj                # Cangjie语言的API客户端
│   ├── api_client.js                # JavaScript语言的API客户端（备选）
│   └── utils.cj                     # 通用工具函数
├── references/                       # 可选：参考文档
│   ├── api_spec.md                  # API规范文档
│   ├── uctoo_api_design.md          # uctoo API设计规范
│   └── examples.md                  # 使用示例
└── assets/                           # 可选：输出资源（如模板）
    └── response_template.json       # 响应模板
```

### 3.3 核心组件设计

#### 3.3.1 重构后的SKILL.md
**位置**: `SKILL.md`  
**设计原则**:
- 精简到500行以内
- 只包含核心指令
- 详细文档移至 `references/`
- 使用渐进式披露

```yaml
---
name: uctoo-api-skill
description: 完整的uctoo后端API集成技能。将自然语言请求转换为uctoo-backend API调用，支持用户管理、产品管理、订单管理等功能。使用时用户提及"uctoo"、"后端API"、"用户管理"、"产品"、"订单"等关键词。
license: MIT
compatibility:
  os:
    - Windows
    - Linux
    - macOS
  requires:
    - binary: cjpm
    - environment: BACKEND_URL
    - file: scripts/api_client.cj
metadata:
  author: UCToo Team
  version: "2.0.0"
  category: api-connector
  domain: backend-integration
---

# Uctoo API Skill

## 快速开始

### 基本用法
直接向我描述你想做什么，我会自动调用相应的API。

**示例:**
- "获取所有用户"
- "创建一个名为张三的新用户"
- "查找ID为123的产品"
- "删除订单456"

### 认证
首次使用前需要登录：
> "使用账号demo和密码123456登录"

## 核心功能

### 1. 用户管理
- 查询用户（单个/列表）
- 创建用户
- 更新用户信息
- 删除用户

### 2. 产品管理
- 查询产品
- 创建产品
- 更新产品
- 删除产品

### 3. 订单管理
- 查询订单
- 创建订单
- 更新订单状态
- 删除订单

### 4. 认证
- 用户登录
- Token管理
- 会话保持

## 详细文档

更多详细信息请参考：
- [API规范](references/api_spec.md) - 完整的API端点文档
- [使用示例](references/examples.md) - 丰富的使用场景示例
- [uctoo设计规范](references/uctoo_api_design.md) - API设计原则

## 执行流程

当你提出请求时，我会：
1. 理解你的自然语言需求
2. 识别意图（GET/CREATE/UPDATE/DELETE）
3. 提取必要参数
4. 使用 `scripts/api_client.cj` 执行API调用
5. 返回格式化的结果

## 错误处理

如果遇到问题：
- 认证失败：请先使用"登录"指令
- API错误：我会提供详细的错误信息
- 参数缺失：我会询问你补充必要信息
```

#### 3.3.2 API客户端（Cangjie实现）
**位置**: `scripts/api_client.cj`  
**职责**: 直接发起HTTP请求，处理认证

```cangjie
package scripts

import std.net.http.{HttpClient, HttpRequest, HttpResponse}
import stdx.encoding.json.{JsonValue, JsonObject}
import std.collection.HashMap

public class UctooApiClient {
    private var _backendUrl: String
    private var _authToken: Option<String> = None()
    private let _httpClient: HttpClient
    
    public init(backendUrl: String) {
        _backendUrl = backendUrl
        _httpClient = HttpClient()
    }
    
    public func setAuthToken(token: String): Unit {
        _authToken = Some(token)
    }
    
    public func login(username: String, password: String): Result<String, String> {
        let request = HttpRequest.post("${_backendUrl}/api/uctoo/auth/login")
            .header("Content-Type", "application/json")
            .body(JsonObject()
                .set("username", username)
                .set("password", password)
                .toJson())
        
        let response = _httpClient.send(request)
        if response.statusCode != 200 {
            return Result.Error("Login failed: ${response.statusCode}")
        }
        
        let json = response.bodyAsJson()
        let token = json["access_token"]?.asString()
        if let t = token {
            _authToken = Some(t)
            return Result.Ok(t)
        }
        return Result.Error("No token in response")
    }
    
    public func getEntity(entityType: String, id: String): Result<JsonValue, String> {
        return _executeGet("/api/uctoo/${entityType}/${id}")
    }
    
    public func getEntities(entityType: String, limit: Int = 10, page: Int = 1): Result<JsonValue, String> {
        return _executeGet("/api/uctoo/${entityType}/${limit}/${page}")
    }
    
    public func createEntity(entityType: String, data: JsonObject): Result<JsonValue, String> {
        return _executePost("/api/uctoo/${entityType}/add", data)
    }
    
    public func updateEntity(entityType: String, data: JsonObject): Result<JsonValue, String> {
        return _executePost("/api/uctoo/${entityType}/edit", data)
    }
    
    public func deleteEntity(entityType: String, id: String): Result<JsonValue, String> {
        return _executePost("/api/uctoo/${entityType}/del", JsonObject().set("id", id))
    }
    
    private func _executeGet(path: String): Result<JsonValue, String> {
        var request = HttpRequest.get("${_backendUrl}${path}")
        
        if let token = _authToken {
            request = request.header("Authorization", "Bearer ${token}")
        }
        
        let response = _httpClient.send(request)
        return _handleResponse(response)
    }
    
    private func _executePost(path: String, data: JsonObject): Result<JsonValue, String> {
        var request = HttpRequest.post("${_backendUrl}${path}")
            .header("Content-Type", "application/json")
            .body(data.toJson())
        
        if let token = _authToken {
            request = request.header("Authorization", "Bearer ${token}")
        }
        
        let response = _httpClient.send(request)
        return _handleResponse(response)
    }
    
    private func _handleResponse(response: HttpResponse): Result<JsonValue, String> {
        if response.statusCode >= 200 && response.statusCode < 300 {
            return Result.Ok(response.bodyAsJson())
        }
        return Result.Error("API Error: ${response.statusCode} - ${response.bodyAsString()}")
    }
}
```

#### 3.3.3 参考文档
**位置**: `references/api_spec.md`

```markdown
# Uctoo API 规范

## 端点列表

### 用户管理 (uctoo_user)
- `GET /api/uctoo/uctoo_user/{id}` - 获取单个用户
- `GET /api/uctoo/uctoo_user/{limit}/{page}` - 获取用户列表
- `POST /api/uctoo/uctoo_user/add` - 创建用户
- `POST /api/uctoo/uctoo_user/edit` - 更新用户
- `POST /api/uctoo/uctoo_user/del` - 删除用户

### 产品管理 (product)
- `GET /api/uctoo/product/{id}` - 获取单个产品
- `GET /api/uctoo/product/{limit}/{page}` - 获取产品列表
- `POST /api/uctoo/product/add` - 创建产品
- `POST /api/uctoo/product/edit` - 更新产品
- `POST /api/uctoo/product/del` - 删除产品

### 订单管理 (order)
- `GET /api/uctoo/order/{id}` - 获取单个订单
- `GET /api/uctoo/order/{limit}/{page}` - 获取订单列表
- `POST /api/uctoo/order/add` - 创建订单
- `POST /api/uctoo/order/edit` - 更新订单
- `POST /api/uctoo/order/del` - 删除订单

### 认证
- `POST /api/uctoo/auth/login` - 用户登录

## 请求/响应格式

详细的JSON schema请参考 [uctooAPI设计规范.md](../../../../backend/docs/uctooAPI设计规范.md)
```

---

## 四、门控系统集成

### 4.1 门控规则定义
在 `SKILL.md` 的 `compatibility.requires` 中定义执行需求：

```yaml
compatibility:
  os:
    - Windows
    - Linux
    - macOS
  requires:
    # 检查Cangjie环境
    - binary: cjpm
    - binary: cangjie
    
    # 检查环境变量
    - environment: BACKEND_URL
    
    # 检查必需文件
    - file: scripts/api_client.cj
    
    # 自定义检查（通过脚本）
    - custom: scripts/check_dependencies.cj
```

### 4.2 门控检查流程
```
技能加载
    ↓
门控系统检查
    ├─ 检查操作系统兼容性
    ├─ 检查二进制文件存在性 (cjpm, cangjie)
    ├─ 检查环境变量 (BACKEND_URL)
    ├─ 检查脚本文件存在
    └─ 执行自定义检查脚本
    ↓
通过 → 技能可用
失败 → 技能禁用，显示原因
```

### 4.3 多脚本语言支持
通过门控系统，技能可以支持多种语言的脚本：

```
scripts/
├── api_client.cj          # 首选：Cangjie实现
├── api_client.js          # 备选：JavaScript实现
└── api_client.py          # 备选：Python实现
```

门控系统会自动检测可用的语言，并选择最优的实现。

---

## 五、渐进式披露实现

### 5.1 三层加载模式
| 层级 | 内容 | 加载时机 | Token消耗 |
|------|------|----------|-----------|
| Level 1 | YAML frontmatter (name, description) | 始终加载 | ~100 tokens |
| Level 2 | SKILL.md 主体 | 技能触发时加载 | <5000 tokens |
| Level 3 | references/, scripts/ | 按需加载 | 无限 |

### 5.2 实现要点
1. **SKILL.md 保持精简**：<500行
2. **详细内容移至 references/**：API文档、示例等
3. **明确的引用链接**：在 SKILL.md 中指明何时使用哪个参考文件
4. **脚本按需执行**：scripts/ 中的代码可以被执行而无需全部读入上下文

---

## 六、实施计划

### 阶段一：架构重构（1-2天）
**任务**:
1. [ ] 创建新的目录结构
2. [ ] 重构 SKILL.md 符合官方标准
3. [ ] 提取参考文档到 references/
4. [ ] 创建独立的 API 客户端脚本

**交付物**:
- 新的目录结构
- 重构后的 SKILL.md
- references/ 目录下的文档
- scripts/api_client.cj

### 阶段二：门控系统集成（1天）
**任务**:
1. [ ] 在 SKILL.md 中定义 requires 规则
2. [ ] 创建依赖检查脚本
3. [ ] 测试门控检查流程
4. [ ] 添加多语言脚本支持

**交付物**:
- 完整的 compatibility 配置
- 依赖检查脚本
- 多语言脚本实现

### 阶段三：测试验证（1天）
**任务**:
1. [ ] 单元测试 API 客户端
2. [ ] 集成测试完整流程
3. [ ] 测试门控系统
4. [ ] 验证独立运行能力

**交付物**:
- 测试用例
- 测试报告
- 验证文档

### 阶段四：文档完善（0.5天）
**任务**:
1. [ ] 更新 README.md
2. [ ] 创建部署指南
3. [ ] 编写使用示例
4. [ ] 更新 DEPLOYMENT.md

**交付物**:
- 完整的文档
- 使用示例
- 部署指南

---

## 七、关键技术决策

### 7.1 HTTP客户端实现
**决策**: 使用Cangjie标准库的 `std.net.http.HttpClient`  
**理由**:
- 无需外部依赖
- 与运行时内核语言一致
- 性能最优

**备选方案**:
- JavaScript实现（通过Node.js）
- Python实现（通过Python解释器）

### 7.2 认证管理
**决策**: 在脚本层管理token  
**理由**:
- 符合技能自包含原则
- 无需外部状态存储
- 简化架构

### 7.3 错误处理
**决策**: 提供结构化的错误信息  
**理由**:
- 便于AI理解和处理
- 提供可操作的反馈
- 支持重试逻辑

---

## 八、与官方最佳实践对比

| 特性 | Claude官方要求 | 当前状态 | 重构后目标 |
|------|---------------|---------|-----------|
| SKILL.md 存在 | ✅ 必需 | ✅ 已有 | ✅ 保持 |
| YAML frontmatter | ✅ 必需 | ✅ 已有 | ✅ 增强 |
| 渐进式披露 | ✅ 推荐 | ❌ 未实现 | ✅ 实现 |
| scripts/ 目录 | ✅ 可选 | ❌ 缺失 | ✅ 添加 |
| references/ 目录 | ✅ 可选 | ❌ 缺失 | ✅ 添加 |
| assets/ 目录 | ✅ 可选 | ❌ 缺失 | ✅ 添加 |
| 无 README.md | ✅ 要求 | ❌ 存在 | ⚠️ 移至外部 |
| 精简SKILL.md | ✅ <500行 | ❌ 过大 | ✅ 重构 |
| 门控系统 | ❌ 无标准 | ❌ 缺失 | ✅ 超越标准 |
| 多语言支持 | ❌ 仅Python | ❌ 仅Cangjie | ✅ 多语言 |

---

## 九、风险与缓解

### 9.1 技术风险
| 风险 | 影响 | 概率 | 缓解措施 |
|------|------|------|---------|
| Cangjie HTTP客户端不完善 | 高 | 中 | 准备JavaScript备选实现 |
| 门控系统集成复杂 | 中 | 低 | 分阶段实现，先基础后高级 |
| 向后兼容问题 | 中 | 中 | 保留旧接口，提供迁移指南 |

### 9.2 运维风险
| 风险 | 影响 | 概率 | 缓解措施 |
|------|------|------|---------|
| 环境配置复杂 | 中 | 低 | 提供.env示例，详细文档 |
| 部署步骤增加 | 低 | 中 | 自动化部署脚本 |

---

## 十、成功标准

### 10.1 功能标准
- [ ] 技能可以独立运行，无需 MCP 服务器
- [ ] 所有现有功能（用户、产品、订单管理）正常工作
- [ ] 认证流程完整
- [ ] 门控系统正确检测环境
- [ ] 支持至少两种脚本语言（Cangjie + JavaScript）

### 10.2 质量标准
- [ ] SKILL.md < 500行
- [ ] 完整的单元测试覆盖
- [ ] 集成测试通过
- [ ] 文档完整准确

### 10.3 性能标准
- [ ] API响应时间 < 2秒
- [ ] 技能加载时间 < 1秒
- [ ] 内存占用合理

---

## 附录

### A. 参考资料
- [Claude官方技能创建指南](../../../agentskills/docs/The-Complete-Guide-to-Building-Skill-for-Claude.md)
- [skill-creator 官方示例](../../skills/skill-creator/SKILL.md)
- [uctoo API设计规范](../../../../backend/docs/uctooAPI设计规范.md)
- [门控系统设计文档](../../../specs/004-agent-skill-runtime/skill_execution_design.md)

### B. 相关文件
- 当前实现: `src/`
- 当前文档: `README_zh_CN.md`, `DEPLOYMENT.md`
- 目标结构: 见本方案第3.2节
