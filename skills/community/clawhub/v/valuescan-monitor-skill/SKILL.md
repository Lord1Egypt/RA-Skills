---
name: valuescan-monitor-skill
description: ValueScan后台实时监控Skill。订阅Stream推送（大盘分析/代币信号），将数据持久化写入本地文件。
version: 1.0.0
user-invocable: true
category: Monitoring
license: MIT
homepage: https://www.valuescan.ai
dependencies:
  - python: ">=3.10"
  - node: ">=18"
tags:
  - cryptocurrency
  - monitoring
  - stream
  - realtime
credentials:
  api_key:
    description: ValueScan API Key
    required: true
  secret_key:
    description: ValueScan Secret Key
    required: true
---

# valuescan-monitor-skill

后台常驻监控 ValueScan Stream 推送，将大盘分析和代币信号实时写入本地文件。

## 首次安装

当用户首次使用监控相关指令时，若 `~/.vs-monitor/config.json` 不存在，Claude 按以下步骤引导安装：

1. 询问 **API Key**（ValueScan 开放平台获取）
2. 询问 **Secret Key**
3. 询问**数据输出目录**（如 `/Users/xxx/valuescan-monitor`）
4. 将以上内容写入 `~/.vs-monitor/config.json`：

```json
{
  "apiKey": "...",
  "secretKey": "...",
  "outputDir": "/path/to/output",
  "streamBaseUrl": "https://stream.valuescan.ai",
  "apiBaseUrl": "https://api.valuescan.io"
}
```

## 触发语与 Claude 动作

| 用户说 | Claude 动作 |
|--------|------------|
| 监控大盘分析 / 开始大盘监控 | 检查 `market.pid`，kill 旧进程后启动 `python monitor.py --market`，写 `~/.vs-monitor/market.pid` |
| 监控所有代币信号 | 检查 `signal.pid`，kill 旧进程后启动 `python monitor.py --signal`，写 `signal.pid` |
| 监控 BTC 信号 | 启动 `python monitor.py --signal --tokens=BTC`，写 `signal.pid` |
| 监控 ETH 和 SOL 信号 | 启动 `python monitor.py --signal --tokens=ETH,SOL`，写 `signal.pid` |
| 同时监控大盘和所有代币信号 | 启动两个独立进程，分别写 `market.pid` 和 `signal.pid` |
| 停止大盘监控 | 读取 `market.pid`，kill 对应进程，删除 PID 文件 |
| 停止信号监控 / 停止代币监控 | 读取 `signal.pid`，kill 对应进程，删除 PID 文件 |
| 停止所有监控 | kill 两个 PID，删除对应 PID 文件 |
| 查看监控状态 / 监控运行中吗 | 检查两个 PID 文件是否存在且进程存活，报告状态 |

## 进程管理

PID 文件目录：`~/.vs-monitor/`

| 模式 | PID 文件 |
|------|---------|
| 大盘分析 | `~/.vs-monitor/market.pid` |
| 代币信号 | `~/.vs-monitor/signal.pid` |

**启动前检查：**
```bash
# 检查进程是否存活
PID=$(cat ~/.vs-monitor/market.pid 2>/dev/null)
if [ -n "$PID" ] && kill -0 "$PID" 2>/dev/null; then
    kill "$PID"
fi
```

**后台启动：**
```bash
nohup python /path/to/vs-monitor-skill/script/monitor.py --market \
    --config=~/.vs-monitor/config.json > ~/.vs-monitor/market.log 2>&1 &
echo $! > ~/.vs-monitor/market.pid
```

## 文件写入规则

| 来源 | 路径 | 格式 |
|------|------|------|
| 大盘分析（market event） | `{outputDir}/大盘分析/大盘分析-YYYY-MM-DD.txt` | `[HH:MM:SS]\n{content}\n---\n` |
| 代币信号（signal event） | `{outputDir}/代币信号/YYYY-MM-DD/{symbol}.txt` | `[HH:MM:SS] [{type}]\n{content}\n---\n` |

- `symbol` 从 signal content JSON 的 `symbol` 字段取
- `type`：OPPORTUNITY / RISK / ANOMALY
- heartbeat / connected 事件忽略，不写文件
- 目录不存在时自动创建

## 脚本使用

### Python（推荐）

```bash
pip install sseclient-py requests
python monitor.py --market
python monitor.py --signal --tokens=BTC,ETH
```

### TypeScript

```bash
cd script && npm install
npx ts-node monitor.ts --market
npx ts-node monitor.ts --signal --tokens=BTC,ETH
```

## 认证签名

Stream SSE 使用 query params 认证：

```
timestamp = 当前毫秒时间戳
nonce     = 随机 UUID
sign      = HMAC-SHA256(key=secretKey, message=timestamp + nonce)
```

参数拼接到 SSE URL：`?apiKey=...&timestamp=...&nonce=...&sign=...`

## 安全注意事项

- **凭证存储**：API Key 和 Secret Key 将以明文存储在 `~/.vs-monitor/config.json`，请确保该目录权限受控
- **进程管理**：技能会创建后台进程并通过 PID 文件管理（kill 旧进程），PID 文件位于 `~/.vs-monitor/`
- **文件写入**：所有数据写入用户指定的 `outputDir`，请确保目录路径安全
- **隔离环境**：建议在容器、VM 或权限受限的账户中运行，以限制影响范围

## 已知限制

- 断线后进程退出，需 Claude 手动重启（不含自动重连）
- 同类型只允许一个进程（signal 或 market 各一个）
