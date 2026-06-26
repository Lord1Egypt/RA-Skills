# WebSocket 连接延迟检测工具

> 一站式 WebSocket 建连性能诊断工具，精确测量 DNS 解析、TCP 握手、TLS 握手、WebSocket Upgrade 各阶段耗时，快速定位连接瓶颈。

## 📦 工具包内容

```
tencentcloud_websocket_checker/          ← Skill 根目录
├── SKILL.md                     # AI Skill 定义文件
├── evals/
│   └── evals.json               # Skill 测试用例
├── references/
│   ├── examples.md              # Skill 参考 - 使用示例
│   └── troubleshooting.md       # Skill 参考 - 故障排查
├── ws_check.sh                  # 主检测脚本
├── install_dependencies.sh      # 依赖自动安装脚本
├── config.env                   # 可自定义配置文件
├── test_cases.sh                # 测试用例脚本
├── run.sh                       # 快速运行示例
├── VERSION                      # 版本信息
├── CHECKSUM.md5                 # 文件校验和
├── utils/
│   ├── batch_check.sh           # 批量检测脚本
│   └── report_generator.sh      # 报告生成脚本
└── docs/
    ├── README.md                # 本文件
    ├── EXAMPLES.md              # 使用示例大全
    └── TROUBLESHOOTING.md       # 故障排查指南
```

## 🚀 快速开始

### 1. 安装依赖

```bash
# 自动检测并安装所需工具
sudo bash install_dependencies.sh
```

### 2. 赋予执行权限

```bash
chmod +x ws_check.sh install_dependencies.sh test_cases.sh utils/*.sh
```

### 3. 运行检测

```bash
# 最简用法
./ws_check.sh wss://your-server.com/websocket

# 指定测试轮数
./ws_check.sh wss://your-server.com/websocket 5

# 使用 ws 协议
./ws_check.sh ws://your-server.com/websocket
```

## 🔧 功能特性

| 功能 | 说明 |
|------|------|
| **多阶段耗时测量** | DNS 解析、TCP 握手、TLS 握手、WS Upgrade 独立计时 |
| **协议自动识别** | 支持 `wss://` 和 `ws://` 自动识别及 `-p` 参数强制切换 |
| **多轮统计** | 支持多轮测试，输出平均/最小/最大值 |
| **性能评级** | 自动评定优秀/正常/偏慢，直观的条形图和百分比展示 |
| **瓶颈分析** | 自动识别最大瓶颈环节，给出针对性优化建议 |
| **DNS 诊断** | 独立的 DNS 解析详情，包括 IP 地址、CNAME 信息 |
| **连接时序图** | ASCII 时序图直观展示各阶段耗时分布 |
| **跨平台支持** | 支持 CentOS、Ubuntu、macOS |

## 📖 命令行参数

```
用法：./ws_check.sh [选项] <WebSocket URL> [测试轮数]

选项：
  -p, --protocol <ws|wss>  强制指定协议类型（优先级高于 URL 前缀）
  -h, --help               显示帮助信息

参数：
  WebSocket URL            目标 WebSocket 地址
  测试轮数                 可选，默认 3 轮（范围 1-10）
```

## ⚙️ 配置说明

编辑 `config.env` 可自定义以下参数：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `DEFAULT_ROUNDS` | 3 | 默认测试轮数 |
| `CURL_TIMEOUT` | 15 | 请求超时时间（秒） |
| `DNS_THRESHOLD_GOOD` | 50 | DNS 优秀阈值（ms） |
| `DNS_THRESHOLD_WARN` | 200 | DNS 警告阈值（ms） |
| `TCP_THRESHOLD_GOOD` | 100 | TCP 优秀阈值（ms） |
| `TLS_THRESHOLD_GOOD` | 200 | TLS 优秀阈值（ms） |
| `WS_THRESHOLD_GOOD` | 200 | WS Upgrade 优秀阈值（ms） |
| `TOTAL_THRESHOLD_GOOD` | 500 | 总耗时优秀阈值（ms） |

## 📊 输出说明

脚本输出包含以下部分：

1. **连接信息头** — 显示目标地址、协议类型、端口等基本信息
2. **DNS 诊断** — 独立的 DNS 解析结果，包含 IP 和 CNAME
3. **多轮测试结果** — 每轮的详细耗时数据
4. **性能分析报告** — 表格展示各阶段平均/最小/最大值、占比、评级
5. **瓶颈分析** — 自动识别瓶颈并提供优化建议
6. **连接流程时序图** — ASCII 可视化各阶段耗时

## 🔗 依赖要求

| 工具 | 最低版本 | 用途 |
|------|---------|------|
| curl | 7.x | HTTP 请求和耗时测量 |
| dig  | 9.x | DNS 解析诊断 |
| awk  | 4.x | 数据计算和格式化 |
| sed  | 4.x | 文本解析 |
| bash | 4.x | 脚本运行环境 |

## 📝 版本信息

- **当前版本**：v1.0.0
- **发布日期**：2025-03-18
- **许可证**：内部使用

## 📚 其他文档

- [EXAMPLES.md](./EXAMPLES.md) — 详细的使用示例
- [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) — 故障排查指南
- [SKILL.md](../SKILL.md) — AI Skill 定义文件
