# ZStack MCP Skill for OpenClaw

让 OpenClaw 通过 MCP 协议调用 ZStack Cloud 2000+ API。

## 功能

- ✅ API 搜索：根据关键词搜索 ZStack API
- ✅ API 执行：执行查询和写操作（需授权）
- ✅ 监控指标：搜索和获取监控数据
- ✅ 自动认证：用户名密码登录或 SessionID
- ✅ 安全保护：默认只读模式

## 安装

### 通过 ClawHub（推荐）

```bash
clawhub install zstack-mcp
```

### 手动安装

```bash
# 克隆或复制 skill 目录到 ~/clawd/skills/zstack-mcp

# 安装依赖
pip install zstack-mcp-server

# 配置认证
bash ~/clawd/skills/zstack-mcp/scripts/configure.sh

# 注册到 mcporter
bash ~/clawd/skills/zstack-mcp/scripts/register-mcp.sh
```

## 使用

```bash
# 搜索 API
mcporter call zstack-mcp.search_api keyword:VmInstance

# 查询虚拟机
mcporter call zstack-mcp.execute_api "apiName:QueryVmInstance"

# 获取监控数据
mcporter call zstack-mcp.search_metrics resourceType:VmInstance
```

## 文档

详见 [SKILL.md](SKILL.md)
