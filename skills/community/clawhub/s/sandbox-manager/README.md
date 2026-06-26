# Sandbox Manager Skill

百度 Agent Sandbox 沙箱管理工具,支持快速创建和管理沙箱实例。

## 快速开始

### 1. 配置 API Key

```bash
# 方式一: 通过脚本配置
python3.9 scripts/configure.py <your_api_key>

# 方式二: 手动写入 ~/.env
echo "E2B_API_KEY=<your_api_key>" > ~/.env
echo "E2B_DOMAIN=agent-sandbox.baidu-int.com" >> ~/.env
```

### 2. 创建沙箱

```bash
# 创建代码沙箱(默认)
python3.9 scripts/create_sandbox.py

# 创建浏览器沙箱
python3.9 scripts/create_sandbox.py --template browser_use

# 创建 All-In-One 沙箱
python3.9 scripts/create_sandbox.py --template aio --timeout 7200

# 指定名称和创建人
python3.9 scripts/create_sandbox.py --name my-sandbox --creator caojiao
```

### 3. 管理沙箱

```bash
# 连接沙箱
python3.9 scripts/manage_sandbox.py connect --sandbox-id al7hwm9s

# 查看沙箱信息
python3.9 scripts/manage_sandbox.py info --sandbox-id al7hwm9s

# 列出沙箱文件
python3.9 scripts/manage_sandbox.py files --sandbox-id al7hwm9s

# 执行命令
python3.9 scripts/manage_sandbox.py exec --sandbox-id al7hwm9s --command "ls -la"

# 销毁沙箱
python3.9 scripts/manage_sandbox.py kill --sandbox-id al7hwm9s
```

## 通过 Agent 使用

直接对雀雀说:

- "创建一个沙箱,模板使用 code_test"
- "帮我创建一个浏览器沙箱,时长 2 小时"
- "在沙箱 al7hwm9s 中执行命令 ls -la"
- "连接到沙箱 al7hwm9s"

## 沙箱模板

| 模板 | 说明 | 用途 |
|------|------|------|
| `code_test` | 代码执行沙箱 | 编写、运行、测试代码 |
| `browser_use` | 浏览器沙箱 | 自动化浏览器操作、网页测试 |
| `aio` | All-In-One | 浏览器 + 代码 + 终端一体化 |
| `coding_agent` | 编码助手 | 内置 Zulu、Ducc 等 DevOps 工具 |

## 访问沙箱

创建沙箱后会返回访问地址:

- **管理页面**: https://8200-{sandboxId}.agent-sandbox.baidu-int.com/
  - VSCode 视图
  - Terminal 视图
  - Jupyter 视图
  - 浏览器视图(仅 aio/browser_use)

- **MCP 服务**: https://8080-{sandboxId}.agent-sandbox.baidu-int.com/mcp

## 注意事项

1. **存活时间**: 最大 1 天(86400 秒),超时自动销毁
2. **计费**: 不同规格沙箱费用不同,注意运行时长
3. **权限**: 需要 COMATE_AUTH_TOKEN 才能访问 iCode 等内部服务
4. **网络**: 出站流量受限(白名单机制)
5. **数据**: 沙箱销毁后数据丢失,重要数据需提前保存

## 相关链接

- [沙箱管理平台](https://console.cloud.baidu-int.com/aitools/sandbox-square)
- [沙箱使用文档](https://ku.baidu-int.com/knowledge/HFVrC7hq1Q/_SKPgSwp2G/B8wSneaLSC/xBjsa6yz-ZsV4-)
- [用户交流群](https://applink-infoflow.baidu.com/share/contact/open/?token=qPvbu4...): 群号 12143597

## 更新日志

- 2026-04-29: 初始版本,支持创建、连接、管理沙箱