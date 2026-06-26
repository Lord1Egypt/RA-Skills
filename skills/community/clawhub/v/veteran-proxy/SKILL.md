---
name: veteran
description: 需要访问的网络资源无法直接访问的时候，需要启动网络代理服务，通过代理访问网络资源的时候使用。管理 veteran 节点代理客户端，包括订阅更新、节点列表查看、启动/停止 SOCKS5 代理、查看运行状态、配置分流规则等。当用户需要操作 veteran 代理工具、询问 veteran 命令用法、配置订阅、设置分流规则、或排查代理问题时使用。
---

# veteran — 节点代理客户端

一个跨平台代理客户端，支持订阅管理、多节点切换、SOCKS5/HTTP 代理、分流规则。

## 安装

### macOS / Linux（Homebrew）

```bash
brew install veteran-cli/homebrew-veteran/veteran
```

### npm（跨平台）

```bash
# 全局安装（可在任意目录使用 veteran 命令）
npm install -g veteran

# 或临时使用
npx veteran list
```


## 快速开始

```bash
# 1. 更新订阅（也可设置 VETERAN_SUB_URL 环境变量后直接 `veteran sub`）
veteran sub -u "https://your-subscription-url"

# 2. 查看节点
veteran list

# 3. 启动代理（默认后台运行，端口 1088）
veteran run -n 1

# 4. 查看状态
veteran status

# 5. 停止
veteran stop
```

## 命令参考

### `veteran sub` — 更新订阅

```
veteran sub [-u <订阅URL>]
```

| 参数 | 说明 |
|------|------|
| `-u`, `--url` | 订阅链接 URL（未指定时从 `VETERAN_SUB_URL` 环境变量读取） |

可通过环境变量预设订阅地址，之后直接执行 `veteran sub` 即可：
```bash
export VETERAN_SUB_URL="https://your-subscription-url"
veteran sub
```

支持协议：`vless://` `vmess://` `ss://` `trojan://` `hysteria2://`

### `veteran list` / `veteran ls` — 列出节点

```
veteran list
```

显示所有已订阅节点的索引、协议类型、名称和服务器地址。`ls` 是 `list` 的别名。

### `veteran run` — 启动代理

```
veteran run -n <节点> [-p <端口>] [-m <模式>] [-f] [--rule ...] [--rule-file ...]
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-n`, `--node` | 节点索引(从1开始)或名称（必填） | - |
| `-p`, `--port` | 本地监听端口 | `1088` |
| `-m`, `--mode` | 分流模式（见下表） | `2` |
| `-f`, `--foreground` | 前台运行（输出到终端） | 默认后台 |
| `--rule` | 自定义规则，可重复 | - |
| `--rule-file` | 从文件加载规则 | - |

默认以**后台守护进程**方式运行，日志写入 `~/.veteran/veteran-{port}.log`。使用 `-f` 可强制前台运行。

#### 节点选择

`-n` 支持：
- **索引**：从 1 开始的数字（如 `-n 1`）
- **名称**：精确或模糊匹配（如 `-n "Hong Kong"`）

#### 分流模式

| 值 | 说明 |
|----|------|
| `0` | 绕过中国大陆地址 |
| `1` | 绕过局域网地址 |
| `2` | 绕过中国大陆和局域网地址（默认） |
| `3` | 全局代理 |
| `4` | 自定义规则（需配合 `--rule` 或 `--rule-file`） |

### `veteran status` — 查看状态

```
veteran status
```

输出每个运行实例的 PID、端口、启动时间和 SOCKS5 代理地址（`127.0.0.1:<port>`）。

### `veteran stop` — 停止代理

```
veteran stop [-p <端口>]
```

| 参数 | 说明 |
|------|------|
| `-p`, `--port` | 要停止的端口（不指定则停止所有） |

### `veteran version` — 查看版本

```
veteran version
```

---

## 分流规则

### 命令行方式：`--rule`

```bash
veteran run -n 1 -m 4 \
  --rule "DOMAIN-SUFFIX,google.com,PROXY" \
  --rule "IP-CIDR,10.0.0.0/8,DIRECT" \
  --rule "FINAL,PROXY"
```

### 文件方式：`--rule-file`

```bash
veteran run -n 1 -m 4 --rule-file ./rules.json
```

#### 规则文件格式 (JSON)

```json
{
  "china_domain": ["baidu", "zhihu", "weibo"],
  "china_cidr": ["114.114.114.0/24"],
  "private_cidr": [
    "10.0.0.0/8",
    "172.16.0.0/12",
    "192.168.0.0/16",
    "127.0.0.0/12"
  ],
  "custom_rule": [
    "DOMAIN-SUFFIX,google.com,PROXY",
    "DOMAIN-SUFFIX,github.com,PROXY",
    "DOMAIN,www.baidu.com,DIRECT",
    "DOMAIN-KEYWORD,facebook,PROXY",
    "IP-CIDR,192.168.1.0/24,DIRECT",
    "IP,8.8.8.8,PROXY",
    "FINAL,PROXY"
  ]
}
```

#### 字段说明

| 字段 | 类型 | 作用 | 生效模式 |
|------|------|------|---------|
| `china_domain` | `string[]` | 包含关键词的域名直连 | 0, 2, 4 |
| `china_cidr` | `string[]` (CIDR格式) | IP 段直连 | 0, 2, 4 |
| `private_cidr` | `string[]` (CIDR格式) | 局域网地址直连 | 1, 2, 4 |
| `custom_rule` | `string[]` | 自定义规则（仅 `-m 4` 生效） | 4 |

#### 规则格式：`TYPE,VALUE,POLICY`

| TYPE | 说明 | 示例 |
|------|------|------|
| `DOMAIN-SUFFIX` | 域名后缀匹配 | `DOMAIN-SUFFIX,google.com,PROXY` |
| `DOMAIN-KEYWORD` | 域名关键词匹配 | `DOMAIN-KEYWORD,facebook,PROXY` |
| `DOMAIN` | 完整域名精确匹配 | `DOMAIN,www.baidu.com,DIRECT` |
| `IP-CIDR` | IP 网段匹配 | `IP-CIDR,10.0.0.0/8,DIRECT` |
| `IP` | 精确 IP 匹配 | `IP,8.8.8.8,PROXY` |
| `FINAL` | 默认兜底策略 | `FINAL,PROXY` |

POLICY 取值：

| 值 | 说明 |
|----|------|
| `DIRECT` | 直连，不走代理 |
| `PROXY` | 走代理 |
| `REJECT` | 拒绝连接 |

规则按优先级匹配：`DOMAIN` > `DOMAIN-SUFFIX` > `DOMAIN-KEYWORD` > `IP-CIDR` > `IP` > `FINAL`

---

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `VETERAN_SUB_URL` | 预设订阅地址，执行 `veteran sub` 时无需 `-u` | - |
| `VETERAN_ALLOW_MULTIPLE` | 设为 `true` 允许多实例（不同端口） | 禁用 |
| `VETERAN_DATA_DIR` | 数据目录 | `~/.veteran` |

---

## 多实例

```bash
# 允许在不同端口启动多个代理
export VETERAN_ALLOW_MULTIPLE=true
veteran run -n 1 -p 1088   # 节点1 → 端口1088
veteran run -n 2 -p 1089   # 节点2 → 端口1089
```

---

## 数据目录

```
~/.veteran/
├── nodes.json              # 节点列表缓存
├── veteran.log             # 管理命令日志
├── veteran-1088.log        # 端口1088运行日志
├── veteran-1088.pid        # 端口1088进程ID（JSON格式，含pid/port/startedAt）
├── veteran-1088.failed     # 端口1088启动失败信息（启动失败时临时生成）
└── veteran-1089.log        # 端口1089运行日志
```

---

## 浏览器配置

在浏览器或系统代理设置中配置 SOCKS5 代理：
- **地址**：`127.0.0.1`
- **端口**：指定端口（默认 `1088`）

---

## 支持的协议

| 协议 | 代理链接格式 | TLS | 传输层 |
|------|-------------|-----|--------|
| VLESS | `vless://uuid@host:port?params#name` | ✅ Reality/TLS | tcp/ws/grpc/h2/quic |
| VMess | `vmess://base64(json)` | ✅ TLS | tcp/ws/grpc/h2 |
| Shadowsocks | `ss://base64@host:port#name` | ❌ | tcp |
| Trojan | `trojan://pass@host:port?params#name` | ✅ TLS | tcp/ws/grpc |
| Hysteria2 | `hysteria2://pass@host:port#name` | ✅ | quic |

---

## 支持平台

| 系统 | amd64 | arm64 | 386 | armv7 | armv6 |
|------|-------|-------|-----|-------|-------|
| macOS (darwin) | ✅ | ✅ | ❌ | ❌ | ❌ |
| Linux | ✅ | ✅ | ✅ | ✅ | ✅ |
| Windows | ✅ | ✅ | ✅ | ❌ | ❌ |

---

## npm Programmatic API

```js
const veteran = require('veteran');

// 获取版本（async）
const ver = await veteran.version();
console.log(ver);

// 获取二进制路径
console.log(veteran.path());

// 执行命令（返回 child_process）
const child = await veteran.run(['list']);
```

---

## 常见问题

1. **端口被占用**：使用 `-p` 换端口
2. **已有实例运行**：使用 `VETERAN_ALLOW_MULTIPLE=true` 或先 `veteran stop`
3. **订阅更新失败**：检查订阅 URL 是否可访问
4. **节点未找到**：使用 `veteran list` 确认索引或名称
5. **二进制未下载**：检查网络连接；也可手动下载放入 PATH
