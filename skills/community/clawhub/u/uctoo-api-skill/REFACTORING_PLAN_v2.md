# UCTOO API Skill 重构方案

## 概述

本文档描述了对 `uctoo-api-skill` 的完全重构方案，采用 Agentskills 最佳实践，真正发挥大模型的语义理解和推理能力。

## 重构核心理念

### 当前问题
1. **硬编码关键词提取**：使用固定程序提取用户名、密码等参数，脆弱且容易出错
2. **固定的 API 调用逻辑**：无法灵活应对用户的自然语言需求
3. **缺乏语义理解**：没有充分利用大模型的优势

### 重构方向
1. **大模型驱动**：将语义理解、参数提取、API 选择等任务完全交给大模型
2. **极简架构**：只提供必要的工具和 API 规范说明
3. **渐进式披露**：遵循 Agentskills 的三级披露原则
4. **知识层 + 连接层分离**：SKILL.md 作为知识层，HTTP 工具作为连接层

## 技术架构

### 架构图

```
┌─────────────────────────────────────────────────────────┐
│                     用户输入                              │
│         "请使用 demo 账号 123456 登录"                  │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              大模型（知识层 + 推理）                     │
│  ┌───────────────────────────────────────────────────┐  │
│  │ 1. 理解用户意图：需要登录                          │  │
│  │ 2. 识别参数：username=demo, password=123456      │  │
│  │ 3. 选择 API：POST /api/uctoo/auth/login           │  │
│  │ 4. 组装请求体：{"username":"demo","password":"123456"}│  │
│  │ 5. 调用 HTTP 工具执行请求                          │  │
│  │ 6. 解析响应并生成友好回复                          │  │
│  └───────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│                 HTTP 工具（连接层）                      │
│              执行实际的 API 请求                        │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│                 UCTOO 后端 API                          │
└─────────────────────────────────────────────────────────┘
```

## 技能文件结构

```
uctoo-api-skill/
├── SKILL.md                          # 主技能文件（知识层）
├── references/
│   ├── api-spec.md                   # API 完整规范
│   ├── authentication-guide.md       # 认证指南
│   └── examples.md                   # 使用示例
└── src/
    └── uctoo_api_skill.cj            # 极简实现（仅提供 HTTP 工具）
```

## SKILL.md 设计

### YAML Frontmatter（第一级披露）

```yaml
---
name: uctoo-api-skill
description: 完整的 uctoo 后端 API 集成技能。将自然语言请求转换为 uctoo-backend API 调用，支持用户管理、产品管理、订单管理、登录认证等功能。使用时用户提及 "uctoo"、"后端API"、"用户管理"、"产品"、"订单"、"登录"、"认证" 等关键词。
license: MIT
compatibility: 需要网络访问 uctoo 后端 API
metadata:
  author: UCToo Team
  version: "2.0.0"
  category: api-integration
allowedTools: Bash(python:*)
---
```

### 主体内容（第二级披露）

```markdown
# UCTOO API Skill

## 概述

本技能帮助您通过自然语言与 uctoo 后端 API 进行交互。您只需用普通语言描述您的需求，我会自动理解并调用相应的 API。

## 可用工具

### HTTP 请求工具

使用以下 Python 脚本发送 HTTP 请求到 uctoo 后端：

```python
import requests
import json
import sys

BACKEND_URL = "https://javatoarktsapi.uctoo.com"

def make_request(method, endpoint, data=None, token=None):
    url = f"{BACKEND_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, params=data)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=data)
        else:
            return json.dumps({"error": f"Unsupported method: {method}"})
        
        return response.text
    except Exception as e:
        return json.dumps({"error": str(e)})

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Usage: python api_client.py <method> <endpoint> [data_json] [token]"}))
        sys.exit(1)
    
    method = sys.argv[1]
    endpoint = sys.argv[2]
    data = json.loads(sys.argv[3]) if len(sys.argv) > 3 else None
    token = sys.argv[4] if len(sys.argv) > 4 else None
    
    result = make_request(method, endpoint, data, token)
    print(result)
```

**使用方式：**
```bash
python scripts/api_client.py <method> <endpoint> [data_json] [token]
```

## API 快速参考

### 认证相关

| 功能 | 方法 | 端点 | 请求体 | 需要认证 |
|------|------|------|--------|----------|
| 登录 | POST | `/api/uctoo/auth/login` | `{"username":"...","password":"..."}` | 否 |
| 退出登录 | POST | `/api/uctoo/auth/logout` | - | 是 |

### 标准 CRUD 操作（以 entity 表为例）

| 操作 | 方法 | 端点 | 需要认证 |
|------|------|------|----------|
| 新增 | POST | `/api/uctoo/entity/add` | 是 |
| 更新 | POST | `/api/uctoo/entity/edit` | 是 |
| 删除 | POST | `/api/uctoo/entity/del` | 是 |
| 查询单条 | GET | `/api/uctoo/entity/:id` | 是 |
| 查询多条 | GET | `/api/uctoo/entity/:limit/:page` | 是 |

**注意：** 将 `/uctoo/entity` 替换为实际的数据库名和表名，如 `/uctoo/user`、`/uctoo/product` 等。

## 工作流程

### 1. 理解用户需求
仔细阅读用户的自然语言请求，理解他们想要做什么。

### 2. 确定是否需要认证
- 如果是登录、注册等操作，不需要 token
- 如果是其他操作，需要先登录获取 token

### 3. 选择合适的 API
根据用户需求选择对应的 API 端点和 HTTP 方法。

### 4. 组装请求参数
从用户请求中提取必要的参数，构建 JSON 请求体。

### 5. 执行 HTTP 请求
使用提供的 Python 脚本发送请求。

### 6. 解析并回复用户
解析 API 响应，用友好的自然语言向用户说明结果。

## 使用示例

### 示例 1：用户登录

**用户请求：**
```
请使用 demo 账号 123456 登录
```

**执行步骤：**
1. 理解用户需要登录
2. 提取参数：username=demo, password=123456
3. 调用登录 API：
```bash
python scripts/api_client.py POST "/api/uctoo/auth/login" '{"username":"demo","password":"123456"}'
```
4. 解析响应，保存 token 供后续使用
5. 向用户确认登录成功

### 示例 2：查询用户列表

**用户请求：**
```
列出所有用户
```

**执行步骤：**
1. 理解用户需要查询用户列表
2. 确认已有有效的 token
3. 调用查询 API：
```bash
python scripts/api_client.py GET "/api/uctoo/user/10/0" "" "your_token_here"
```
4. 解析响应，向用户展示用户列表

## 错误处理

如果 API 返回错误：
1. 向用户清晰地说明错误信息
2. 提供可能的解决方案
3. 如果需要，建议用户重新登录或检查参数

## 参考文档

如需更详细的 API 规范，请参考：
- `references/api-spec.md` - 完整的 API 规范文档
- `references/authentication-guide.md` - 认证详细指南
- `references/examples.md` - 更多使用示例
```

## 极简实现（src/uctoo_api_skill.cj）

```cangjie
package uctoo_api_skill

import std.collection.HashMap
import std.convert.*
import std.fs.*
import std.path.*
import std.process.*
import stdx.encoding.json.*

import magic.core.skill.*
import magic.log.LogUtils
import magic.utils.*

public class UctooApiSkill <: Skill {
    public init() {
        super(
            name: "uctoo-api-skill",
            description: "完整的 uctoo 后端 API 集成技能。将自然语言请求转换为 uctoo-backend API 调用，支持用户管理、产品管理、订单管理等功能。"
        )
    }

    public override func execute(parameters: HashMap<String, JsonValue>): String {
        LogUtils.info("[UctooApiSkill] Executing with parameters: ${parameters}")
        
        let query = if let Some(q) <- parameters.get("query") {
            q.asString().getValue()
        } else if let Some(r) <- parameters.get("request") {
            r.asString().getValue()
        } else {
            ""
        }
        
        if query == "" {
            return "{\"status\": \"error\", \"message\": \"Query parameter is required\"}"
        }
        
        LogUtils.info("[UctooApiSkill] Query: ${query}")
        
        // 注意：实际的 API 调用由大模型通过 SKILL.md 中描述的 Python 脚本完成
        // 这里只是一个占位符，大模型会根据 SKILL.md 中的指令来执行
        return "{\"status\": \"success\", \"message\": \"Skill activated. Please refer to SKILL.md for detailed instructions.\"}"
    }
}

public class UctooApiSkillFactory <: SkillFactory {
    public init() {
        super()
    }

    public override func create(): Skill {
        return UctooApiSkill()
    }
}
```

## 优势

1. **充分利用大模型能力**：语义理解、推理、决策都由大模型完成
2. **灵活性高**：可以处理各种自然语言变体
3. **易于维护**：API 变更只需更新 SKILL.md 中的文档
4. **可扩展性强**：新增 API 只需在文档中添加说明
5. **符合最佳实践**：遵循 Agentskills 的渐进式披露原则

## 迁移计划

### 阶段 1：创建新技能结构
1. 创建新的 SKILL.md 文件
2. 编写 API 规范文档到 references/
3. 创建极简的 Skill 实现

### 阶段 2：测试验证
1. 测试登录功能
2. 测试基本的 CRUD 操作
3. 验证错误处理

### 阶段 3：部署上线
1. 替换旧的 uctoo-api-skill
2. 更新文档
3. 监控运行情况

## 总结

这个重构方案将彻底改变 uctoo-api-skill 的工作方式，从硬编码的关键词提取转变为由大模型驱动的智能 API 集成。这不仅能解决当前的问题，还能为未来的功能扩展提供更大的灵活性。
