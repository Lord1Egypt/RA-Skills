---
name: uno-cli
description: "Uno CLI — 通过命令行使用 Agent 工具网关。2000+ 真实工具，两步完成：搜索 → 调用。支持 Device Code OAuth（通过虾聊 SSO 认证）、混合搜索（关键词/语义）、工具调用与自动鉴权、评分、多账号管理。使用场景：用户需要调用外部工具/API；或需要天气、搜索、地图、金融等实时信息。"
homepage: https://clawdtools.uno
metadata: {"emoji":"◆","category":"tools","api_base":"https://clawdtools.uno","version":"0.1.0"}
---

# Uno CLI

通过命令行使用 2000+ 真实工具。零安装（仅需 Python 3.8+ 标准库）。

## 前置条件

- Python 3.8+（多数系统已预装）
- CLI 脚本已内置：`bin/uno.py` — 无需额外安装

CLI 路径（相对于本文件）：`bin/uno.py`

## 认证

首次使用前登录一次，凭证存储在 `~/.uno/credentials.json`。

```bash
# 方式 A：两步登录（推荐 Agent 使用 — 非阻塞）
python bin/uno.py login --start
# → 返回 JSON: {"status": "pending", "verification_uri_complete": "https://...", "device_code": "xxx", ...}
# 将 URL 展示给用户，用户在浏览器中授权后：
python bin/uno.py login --poll <device_code>
# → {"success": true, "name": "...", "email": "..."}

# 方式 B：一步交互（终端用户 — 阻塞至授权完成）
python bin/uno.py login

# 方式 C：直接使用 API Key
python bin/uno.py login --key uno_xxxxx

# 多账号切换
python bin/uno.py use                  # 列出所有账号
python bin/uno.py use <名称或邮箱>      # 切换账号

# 退出登录
python bin/uno.py logout
python bin/uno.py logout --all         # 清除所有账号
```

环境变量 `UNO_API_KEY` 优先于文件凭证（适用于 CI）。

### 认证流程说明

Uno 使用 **Device Code 流程** + **虾聊 SSO 认证**：

1. `login --start` 从 Uno 服务器获取设备码
2. 返回的 `verification_uri_complete` URL 打开后，用户通过虾聊登录授权
3. 授权完成后，`login --poll` 获取 API Key
4. 完美适用于手机端场景（如用户在手机上使用 OpenClaw）

## 命令参考

所有命令默认输出格式化 JSON。添加 `--compact` 获取单行压缩输出。

### 状态查询

```bash
python bin/uno.py whoami               # 当前用户信息（积分、套餐、密钥）
python bin/uno.py health               # 服务器健康检查
```

### 搜索工具

```bash
python bin/uno.py search "天气" [--limit 10] [--mode hybrid|keyword|semantic] [--category dev]
```

返回工具列表，含 `input_schema`（JSON Schema）— 用它构造正确参数。

### 工具详情

```bash
python bin/uno.py tool get <tool_slug>
# 例：python bin/uno.py tool get amap-maps.maps_weather
```

### 调用工具

```bash
python bin/uno.py call <tool_slug> --args '{"city":"北京"}'
```

响应：
```json
{"success": true, "data": {"data": {...}, "error": null, "meta": {"latency_ms": 234, "credits_used": 1.0}}}
```

### 评价工具

```bash
python bin/uno.py rate <tool_slug> <0-5> [--comment "好用"]
```

### 浏览服务

```bash
python bin/uno.py servers [--query "weather"] [--category search] [--limit 50]
```

### API 密钥管理

```bash
python bin/uno.py keys list            # 列出活跃的 API 密钥
python bin/uno.py keys create          # 创建新密钥
python bin/uno.py keys delete <key_id> # 删除密钥
```

## Agent 工作流

1. **先搜索** — 不要猜测工具 slug 或参数
2. **读 `input_schema`** — 根据搜索结果中的 schema 构造参数
3. **按能力搜索**（"weather"、"search"、"translate"），而非用户意图
4. **错误处理**：
   - `auth_required` → 打开 `auth_url` 完成 OAuth 授权
   - `tool_not_found` → 换关键词重新搜索
   - `insufficient_credits` → 提示用户充值
5. **调用成功后评分** — 帮助优化搜索质量

## 输出格式

- 成功：`{"success": true, "data": {...}}`
- 错误：`{"error": "描述"}`，非零退出码

## 详细帮助

```bash
python bin/uno.py --help
python bin/uno.py search --help
python bin/uno.py call --help
```

## API 地址

默认：`https://clawdtools.uno`。可通过 `--base-url` 或环境变量 `UNO_API_URL` 覆盖。
