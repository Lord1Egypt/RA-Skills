---
name: sandbox-manager
description: 百度 Agent Sandbox 沙箱管理。触发词:沙箱/sandbox/创建沙箱/沙箱实例/沙箱模板/code_test/browser_use/aio。
---

# 沙箱管理 Skill

百度 Agent Sandbox 沙箱创建和管理技能,支持快速创建、连接、管理沙箱实例。

**核心功能**:
- ✅ 快速创建沙箱实例(支持多种模板)
- ✅ 查询沙箱状态和信息
- ✅ 连接已有沙箱实例
- ✅ 沙箱生命周期管理(创建、启动、停止、销毁)
- ✅ 自动配置 API Key 和环境

## 沙箱模板说明

| 模板名称 | 用途 | 特性 |
|---------|------|------|
| `code_test` | 代码执行沙箱 | 支持多语言代码执行、终端操作 |
| `browser_use` | 浏览器自动化沙箱 | 支持浏览器操作、网页测试 |
| `aio` | All-In-One 全栈沙箱 | 浏览器 + 代码执行 + 终端 |
| `coding_agent` | 编码助手沙箱 | 内置 Zulu、Ducc 等 DevOps 工具 |

## 快速开始

### 1. 首次使用 - 配置 API Key

**获取 API Key**:
1. 访问 [OneTool 沙箱管理页面](https://console.cloud.baidu-int.com/aitools/sandbox-square)
2. 创建团队或个人空间
3. 进入空间后在『沙箱』模块点击『API Key 管理』
4. 获取你的 API Key

**配置 API Key**:
```bash
# Agent 会自动将 API Key 写入 ~/.env 文件
# 格式如下:
E2B_API_KEY=<your_api_key>
E2B_DOMAIN=agent-sandbox.baidu-int.com
```

### 2. 安装依赖

```bash
pip3.9 install e2b==1.11.2+baidu --index=https://pip.baidu-int.com/simple/
pip3.9 install e2b-code-interpreter==1.5.2 --index=https://pip.baidu-int.com/simple/
pip3.9 install load_dotenv==0.1.0 --index=https://pip.baidu-int.com/simple/
```

## 使用方式

### 方式一: 通过 Agent 自然语言创建

直接对 Agent 说:
- "创建一个沙箱,模板使用 code_test"
- "帮我创建一个浏览器沙箱"
- "创建一个 aio 沙箱,时长 2 小时"

Agent 会自动:
1. 检查 API Key 配置
2. 安装必要依赖
3. 创建沙箱实例
4. 返回沙箱访问地址和 ID

### 方式二: 通过命令行创建

```bash
cd ~/.openclaw/workspace/skills/sandbox-manager
python3.9 scripts/create_sandbox.py --template code_test --timeout 3600
```

## 核心命令

### 创建沙箱

```python
from e2b_code_interpreter import Sandbox
from dotenv import load_dotenv

load_dotenv()

# 创建沙箱
sbx = Sandbox(
    timeout=3600,  # 1小时
    template="code_test",  # 模板名称
    metadata={
        "agent-sandbox/creator": "caojiao",
        "agent-sandbox/name": "my-sandbox"
    }
)

print(f"沙箱ID: {sbx.sandbox_id}")
print(f"管理页面: https://8080-{sbx.sandbox_id}.agent-sandbox.baidu-int.com/")
```

### 连接已有沙箱

```python
from e2b_code_interpreter import Sandbox

# 通过 sandbox_id 连接
sbx = Sandbox(sandbox_id="al7hwm9s")

# 执行命令
result = sbx.commands.run("ls -la")
print(result.stdout)
```

### 查询沙箱信息

```python
info = sbx.get_info()
print(f"沙箱ID: {info.sandbox_id}")
print(f"模板: {info.template_id}")
print(f"过期时间: {info.end_at}")
print(f"日志链接: {info.metadata.get('logURL')}")
```

### 销毁沙箱

```python
sbx.kill()  # 立即销毁
```

## 沙箱能力

### 1. 代码执行

```python
# 执行 Python 代码
result = sbx.run_code(
    language="python",
    code="print('Hello, World!')"
)

# 执行 Shell 命令
result = sbx.commands.run("git clone ...")
```

### 2. 文件操作

```python
# 写入文件
sbx.files.write("test.txt", "Hello, Sandbox!")

# 读取文件
content = sbx.files.read("test.txt")

# 列出文件
files = sbx.files.list(path=".", depth=2)
```

### 3. 服务暴露

沙箱内启动的服务会自动暴露:
```
http://{port}-{sandboxId}.agent-sandbox.baidu-int.com
```

示例:
```python
# 启动 HTTP 服务
sbx.commands.run("python -m SimpleHTTPServer 8080", background=True)

# 访问地址: http://8080-{sandboxId}.agent-sandbox.baidu-int.com
```

## API 参考

### Sandbox 参数

| 参数 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `timeout` | int | 沙箱存活时间(秒),最大 86400(1天) | 600 |
| `template` | str | 沙箱模板名称 | 必填 |
| `sandbox_id` | str | 已有沙箱ID(用于连接) | 可选 |
| `metadata` | dict | 沙箱元数据 | 可选 |
| `envs` | dict | 环境变量 | 可选 |
| `request_timeout` | int | 请求超时时间(秒) | 600 |

### 常用方法

| 方法 | 说明 |
|------|------|
| `sbx.commands.run(cmd)` | 执行命令 |
| `sbx.files.read(path)` | 读取文件 |
| `sbx.files.write(path, content)` | 写入文件 |
| `sbx.files.list(path)` | 列出文件 |
| `sbx.run_code(language, code)` | 执行代码 |
| `sbx.get_info()` | 获取沙箱信息 |
| `sbx.kill()` | 销毁沙箱 |

## 注意事项

1. **沙箱存活时间**: 最大 1 天(86400 秒),超时自动销毁
2. **计费**: 不同规格沙箱产生不同费用,注意运行时长
3. **权限注入**: 需要提供 `COMATE_AUTH_TOKEN` 才能访问 iCode 等内部服务
4. **网络访问**: 沙箱出站流量受限(白名单机制)
5. **数据持久化**: 沙箱销毁后数据丢失,重要数据需提前保存

## 相关链接

- [沙箱管理平台](https://console.cloud.baidu-int.com/aitools/sandbox-square)
- [沙箱使用文档](https://ku.baidu-int.com/knowledge/HFVrC7hq1Q/_SKPgSwp2G/B8wSneaLSC/xBjsa6yz-ZsV4-)
- [API Key 管理](https://console.cloud.baidu-int.com/aitools/sandbox-square)
- [用户交流群](https://applink-infoflow.baidu.com/share/contact/open/?token=qPvbu4...): 群号 12143597

## 联系人

- 苏琳 (sulin01@baidu.com)
- 杨文才 (yangwencai@baidu.com)

---

_创建时间: 2026-04-29_
_创建人: caojiao 的数字助手 雀雀_