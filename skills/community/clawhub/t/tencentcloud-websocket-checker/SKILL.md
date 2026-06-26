---
name: tencentcloud-websocket-checker
description: "腾讯云 WebSocket 连接延迟检测与性能诊断工具。当用户需要检测 WebSocket 建连延迟、分析 ws/wss 连接各阶段耗时（DNS解析、TCP握手、TLS握手、WebSocket Upgrade）、排查连接慢的问题、对比不同协议/地域的连接性能、或者进行 WebSocket 相关的网络诊断时，使用此技能。即使用户只是提到'ws连接慢'、'websocket 延迟高'、'TLS握手太慢'、'检测ws建连时间'、'测试wss连接'、'腾讯云TTS连接慢'等相关话题，也应该触发此技能。此技能提供一套完整的 shell 脚本工具包，位于 /data/ai-platform/ai-dev-tools/tencentcloud_websocket_checker/ 目录下。"
---

# WebSocket 连接延迟检测技能

本技能提供一套完整的 WebSocket 连接延迟检测和性能诊断工具，能够精确测量 WebSocket 建连过程中各阶段的耗时，帮助快速定位连接瓶颈。

## 工具包位置

所有文件位于 `/data/ai-platform/ai-dev-tools/tencentcloud_websocket_checker/` 目录：

```
tencentcloud_websocket_checker/          ← Skill 根目录
├── SKILL.md                       # AI Skill 定义文件（本文件）
├── evals/
│   └── evals.json                 # Skill 测试用例
├── references/
│   ├── examples.md                # Skill 参考 - 使用示例
│   └── troubleshooting.md         # Skill 参考 - 故障排查
├── ws_check.sh                    # 主检测脚本
├── install_dependencies.sh        # 依赖自动安装脚本
├── config.env                     # 可自定义配置文件
├── test_cases.sh                  # 测试用例脚本
├── run.sh                         # 快速运行入口
├── VERSION                        # 版本信息（v1.0.0）
├── CHECKSUM.md5                   # MD5 文件校验和
├── utils/
│   ├── batch_check.sh             # 批量检测脚本
│   └── report_generator.sh        # CSV/JSON 报告生成
└── docs/
    ├── README.md                  # 功能介绍和使用说明
    ├── EXAMPLES.md                # 使用示例大全
    └── TROUBLESHOOTING.md         # 故障排查指南
```

## 核心功能

### 1. 主检测脚本 `ws_check.sh`

这是核心工具，基于 curl 的 `-w` 格式化输出精确测量 WebSocket 连接各阶段耗时。

**基本用法：**
```bash
# 自动识别协议
./ws_check.sh wss://example.com/websocket
./ws_check.sh ws://example.com/websocket

# 指定协议（-p 优先级最高）
./ws_check.sh -p wss example.com/websocket
./ws_check.sh -p ws wss://example.com/websocket   # 实际使用 ws

# 指定测试轮数（默认3轮，范围1-10）
./ws_check.sh wss://example.com/websocket 5
```

**测量的阶段：**
- 🔍 **DNS 解析** — `time_namelookup`
- 🤝 **TCP 握手** — `time_connect - time_namelookup`
- 🔒 **TLS 握手**（仅 wss）— `time_appconnect - time_connect`
- 🔄 **WS Upgrade** — `time_starttransfer - time_appconnect`（wss）或 `time_starttransfer - time_connect`（ws）

**输出内容：**
- 连接基本信息（域名、端口、协议、路径）
- DNS 诊断详情（IP 地址、CNAME）
- 每轮测试的详细耗时
- 性能分析报告表格（平均/最小/最大、占比、评级、条形图）
- 瓶颈分析与优化建议
- ASCII 连接时序图

**性能评级标准（默认阈值，可在 config.env 中自定义）：**

| 阶段 | 优秀 | 正常 | 偏慢 |
|------|------|------|------|
| DNS  | ≤50ms | ≤200ms | >200ms |
| TCP  | ≤100ms | ≤300ms | >300ms |
| TLS  | ≤200ms | ≤500ms | >500ms |
| WS   | ≤200ms | ≤500ms | >500ms |
| 总计 | ≤500ms | ≤1000ms | >1000ms |

### 2. 协议切换功能

脚本支持 `wss`（TLS加密）和 `ws`（明文）两种协议：

- **自动识别**：根据 URL 前缀 `wss://` 或 `ws://` 自动确定
- **强制指定**：`-p ws` 或 `-p wss`，优先级高于 URL 前缀
- **差异处理**：ws 模式跳过 TLS 握手环节，报告中不显示 TLS 相关内容

### 3. 批量检测 `utils/batch_check.sh`

从 URL 列表文件逐个执行检测：
```bash
# 创建 URL 列表
echo "wss://server1.example.com/ws" > urls.txt
echo "wss://server2.example.com/ws" >> urls.txt

# 批量检测
./utils/batch_check.sh urls.txt 3
```

### 4. 报告生成 `utils/report_generator.sh`

输出结构化 CSV/JSON 格式报告：
```bash
./utils/report_generator.sh wss://example.com/ws 5 csv > report.csv
./utils/report_generator.sh wss://example.com/ws 5 json > report.json
```

### 5. 依赖安装 `install_dependencies.sh`

自动检测操作系统（CentOS/Ubuntu/macOS）并安装所需工具：
```bash
sudo bash install_dependencies.sh
```

所需依赖：curl、dig（bind-utils/dnsutils）、awk（gawk）、sed

### 6. 配置文件 `config.env`

可自定义参数：默认轮数、超时时间、各阶段性能阈值、自定义请求头、DNS 服务器

## 常见使用场景

### 场景 1：快速检测单个 WebSocket 端点
```bash
./ws_check.sh wss://tts-international.tencentcloud.com/stream_ws?Action=TextToStreamAudioWS
```

### 场景 2：对比 TLS 开销
```bash
./ws_check.sh -p wss example.com/ws 5  # 带 TLS
./ws_check.sh -p ws  example.com/ws 5  # 不带 TLS
```

### 场景 3：定时巡检
```bash
# crontab 每小时检测
0 * * * * /path/to/ws_check.sh wss://your-server.com/ws 3 >> /var/log/ws_latency.log 2>&1
```

### 场景 4：CI/CD 发布前检查
```bash
RESULT=$(./ws_check.sh wss://production.example.com/ws 3 2>&1)
if echo "$RESULT" | grep -q "偏慢"; then
    echo "检测到性能问题，请确认后再发布"
    exit 1
fi
```

## 故障排查

遇到问题时，查阅 `TROUBLESHOOTING.md`。常见问题快速诊断：

```
连接失败？
├─ DNS 解析失败 → dig domain 检查 DNS
├─ TCP 不通 → telnet domain port 检查端口
├─ TLS 失败 → openssl s_client 检查证书
└─ WS 升级失败 → 检查 HTTP 状态码和请求路径

耗时偏长？
├─ DNS 偏慢 → 配置 DNS 缓存 / 换公共 DNS
├─ TCP 偏慢 → traceroute 检查网络路径
├─ TLS 偏慢 → 升级 TLS 1.3 / 启用 Session Resumption / 检查证书链
└─ WS 偏慢 → 检查服务端处理逻辑和中间代理
```

如需更详细的排查指南，读取 `docs/TROUBLESHOOTING.md`。
如需更多使用示例，读取 `docs/EXAMPLES.md`。

## 注意事项

1. 脚本需要 bash 4.0+ 环境运行
2. wss 协议需要 curl 编译了 SSL/TLS 支持
3. 测量结果受网络波动影响，建议多轮测试取平均值
4. 脚本通过发送 WebSocket Upgrade 请求头来模拟握手，测量的是到收到第一个响应字节的时间
5. HTTP 状态码 101 表示 WebSocket Upgrade 成功，其他状态码请参考故障排查指南
