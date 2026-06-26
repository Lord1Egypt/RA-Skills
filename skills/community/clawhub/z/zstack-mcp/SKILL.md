---
name: zstack-mcp
description: ZStack Cloud MCP Server integration for OpenClaw. Enables AI to query and execute ZStack APIs (2000+ endpoints) with authentication management and read-only safety.
homepage: https://github.com/zstackio/zstack-mcp-server
license: MIT
metadata:
  {
    "openclaw":
      {
        "emoji": "☁️",
        "requires": { "bins": ["mcporter", "zstack-mcp-server"] },
        "install":
          [
            {
              "id": "pip",
              "kind": "pip",
              "package": "zstack-mcp-server",
              "label": "Install ZStack MCP Server (pip)",
            },
          ],
        "license": {
          "terms": "MIT",
          "accepted": true
        }
      },
  }
---

# ZStack MCP Skill

让 OpenClaw 通过 MCP 协议调用 ZStack Cloud 2000+ API。

## 快速开始

### 1. 安装依赖

```bash
# 安装 ZStack MCP Server（推荐用 pipx 隔离环境）
pipx install zstack-mcp-server

# 或使用 pip
pip install zstack-mcp-server
```

### 2. 配置认证

```bash
# 运行配置脚本（交互式，会自动测试登录）
bash ~/clawd/skills/zstack-mcp/scripts/configure.sh
```

脚本会提示输入：
- ZStack API 地址（如 `http://172.20.0.36:8080`）
- 用户名（默认 admin）
- 密码

配置保存到 `~/clawd/skills/zstack-mcp/config/zstack.env`

### 3. 注册到 mcporter

```bash
# 自动注册到 ~/clawd/config/mcporter.json
bash ~/clawd/skills/zstack-mcp/scripts/register-mcp.sh
```

## 使用示例

### 搜索 API

```bash
# 搜索包含关键词的 API
mcporter call zstack-mcp.search_api --args '{"keywords":["Query","Vm"]}'

# 按分类过滤
mcporter call zstack-mcp.search_api --args '{"keywords":["Vm"],"category":"vm"}'
```

### 获取 API 详情

```bash
mcporter call zstack-mcp.describe_api --args '{"api_name":"QueryVmInstance"}'
```

### 执行 API

```bash
# 查询所有虚拟机
mcporter call zstack-mcp.execute_api --args '{"api_name":"QueryVmInstance","parameters":{"conditions":[]}}'

# 查询运行中的 VM（使用 conditions 过滤）
mcporter call zstack-mcp.execute_api --args '{"api_name":"QueryVmInstance","parameters":{"conditions":[{"name":"state","op":"=","value":"Running"}]}}'

# 指定返回字段（减少响应大小）
mcporter call zstack-mcp.execute_api --args '{"api_name":"QueryVmInstance","parameters":{"conditions":[],"fields":["uuid","name","cpuNum","memorySize","state"]}}'

# 分页查询
mcporter call zstack-mcp.execute_api --args '{"api_name":"QueryVmInstance","parameters":{"conditions":[],"limit":20,"start":0}}'
```

### 监控指标

```bash
# 搜索监控指标
mcporter call zstack-mcp.search_metrics --args '{"keywords":["cpu","vm"]}'

# 获取监控数据
mcporter call zstack-mcp.get_metric_data --args '{"namespace":"ZStack/VM","metric_name":"cpuUtilization","labels":["VMUuid=xxx"]}'
```

### 写操作（需显式启用）

```bash
# 编辑配置文件添加环境变量
# ZSTACK_ALLOW_ALL_API="true"

# 创建虚拟机（危险操作！）
mcporter call zstack-mcp.execute_api --args '{"api_name":"CreateVmInstance","parameters":{"name":"test-vm",...}}'
```

## 配置说明

### 认证方式

| 方式 | 配置 | 说明 |
|------|------|------|
| 用户名密码 | `ZSTACK_ACCOUNT` + `ZSTACK_PASSWORD` | 自动登录获取 Session，推荐 |
| Session ID | `ZSTACK_SESSION_ID` | 直接使用已有 Session，优先级更高 |

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `ZSTACK_API_URL` | ZStack API 地址 | 必填 |
| `ZSTACK_ACCOUNT` | 账户名 | admin |
| `ZSTACK_PASSWORD` | 密码 | 必填 |
| `ZSTACK_SESSION_ID` | Session UUID（优先级更高） | - |
| `ZSTACK_ALLOW_ALL_API` | 允许写操作 | false |
| `ZSTACK_QUERY_DEFAULT_LIMIT` | Query API 默认 limit | 50 |
| `ZSTACK_RESPONSE_SIZE_LIMIT` | 响应大小上限（字节） | 65536 |

### 配置文件位置

- **认证配置**: `~/clawd/skills/zstack-mcp/config/zstack.env`
- **MCP 配置**: `~/clawd/config/mcporter.json`（优先）或 `~/.team-os/mcp.json`

## 安全说明

- **默认只读**：只允许 `Query*`, `Get*`, `List*`, `Describe*`, `Check*`, `Count*` 等查询类 API
- **写操作需显式启用**：设置 `ZSTACK_ALLOW_ALL_API="true"`
- **响应限制**：默认 64KB 限制，防止撑爆模型上下文
- **Session 管理**：SessionID 会过期，建议使用用户名密码自动登录

## API 条件语法

Query 类 API 的 `conditions` 参数支持以下操作符：

| 操作符 | 含义 | 示例 |
|--------|------|------|
| `=` | 等于 | `name=test` |
| `!=` | 不等于 | `state!=Deleted` |
| `>` | 大于 | `cpuNum>4` |
| `>=` | 大于等于 | `memorySize>=1073741824` |
| `<` | 小于 | `createDate<2024-01-01` |
| `<=` | 小于等于 | - |
| `?=` | 模糊匹配 (LIKE) | `name?=%test%` |
| `!?=` | 模糊不匹配 | `name!?=%test%` |
| `~=` | 正则匹配 | `name~=.*test.*` |
| `!~=` | 正则不匹配 | - |
| `=null` | 为空 | `description=null` |
| `!=null` | 不为空 | - |
| `in` | 在列表中 | `state?=Running,Stopped` |
| `not in` | 不在列表中 | `state!?=Deleted,Destroyed` |

示例：
```json
{
  "conditions": [
    {"name": "uuid", "op": "?=", "value": "ae6e57a0%"},
    {"name": "state", "op": "in", "value": "Running,Stopped"}
  ]
}
```

## 故障排查

```bash
# 1. 检查 mcporter 配置
mcporter config list

# 2. 测试 MCP 连接
mcporter call zstack-mcp.search_api --args '{"keywords":["Query"]}'

# 3. 查看 MCP server 日志
mcporter daemon status

# 4. 手动测试 ZStack API 连接
source ~/clawd/skills/zstack-mcp/config/zstack.env
curl -X POST "$ZSTACK_API_URL/zstack/api" \
  -H "Content-Type: application/json" \
  -d "{\"org.zstack.header.identity.APILoginMessage\":{\"accountName\":\"$ZSTACK_ACCOUNT\",\"password\":\"$ZSTACK_PASSWORD\"}}"
```

## 常见问题

**Q: 提示 "Unknown MCP server 'zstack-mcp'"**
- 检查配置文件路径：`cat ~/clawd/config/mcporter.json`
- 确认配置已加载：`mcporter config list`

**Q: 响应被截断**
- 使用 `fields` 参数精简返回字段
- 使用 `limit` 和 `start` 分页
- 增大 `ZSTACK_RESPONSE_SIZE_LIMIT`（不推荐）

**Q: Session 过期**
- 重新运行 `configure.sh` 获取新 SessionID
- 或使用用户名密码认证（自动登录）

## 多机器部署

```bash
# 通过 ClawHub 安装
clawhub install zstack-mcp

# 配置认证
bash ~/clawd/skills/zstack-mcp/scripts/configure.sh

# 注册到 mcporter
bash ~/clawd/skills/zstack-mcp/scripts/register-mcp.sh
```

## 参考

- [ZStack MCP Server](https://github.com/zstackio/zstack-mcp-server)
- [mcporter Skill](https://github.com/openclaw/openclaw/tree/main/skills/mcporter)
