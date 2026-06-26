---
name: tcp
description: Helps with TCP sockets, client/server connections, and network debugging. Use when the user needs to open TCP connections, write socket code, test ports, debug connection refused or timeouts, or work with raw TCP protocols.
---

# TCP

本 Skill 帮助处理 **TCP** 连接、套接字编程和常见网络调试：建立连接、收发数据、测试端口、以及排查连接失败或超时等问题。

---

## 何时使用

当用户提到或需要：

- 写 TCP 客户端/服务端（socket 编程）
- 测试某主机某端口是否可达（telnet、nc、PowerShell）
- 连接被拒绝、超时、半开连接等错误排查
- 基于 TCP 的自定义协议或简单服务
- 与 TCP 相关的防火墙、端口、绑定地址配置

---

## 快速测试连接与端口

### 命令行

- **PowerShell（Windows）**：
  ```powershell
  Test-NetConnection -ComputerName host -Port port
  ```
  或使用 .NET 套接字简单测端口（脚本中）：
  ```powershell
  $tcp = New-Object System.Net.Sockets.TcpClient; $tcp.Connect("host", port); $tcp.Close()
  ```

- **netcat（nc）**（若已安装）：
  ```bash
  nc -zv host port
  ```
  交互收发：
  ```bash
  nc host port
  ```

- **telnet**（多数系统已弃用或未默认安装，仅作备选）：
  ```bash
  telnet host port
  ```

根据用户当前 OS 优先给出可用方案（如 Windows 用 `Test-NetConnection` 或 PowerShell 脚本）。

---

## 客户端/服务端代码要点

### 通用流程

- **客户端**：创建 socket → connect(host, port) → send/recv → close。
- **服务端**：创建 socket → bind(address, port) → listen() → accept() → 与客户端 socket 通信 → close。

注意：不同语言 API 不同，只给思路或该语言下的最小示例，避免冗长。

### 常见语言速查

- **Python**：`socket.socket(socket.AF_INET, socket.SOCK_STREAM)`，`connect()`/`bind()`+`listen()`+`accept()`，`send()`/`recv()`。注意 `recv` 可能一次读不满，需循环或协议约定。
- **Node.js**：`net.createConnection(port, host)` 或 `net.createServer()`，事件 `data`/`end`/`error`。
- **Go**：`net.Dial("tcp", "host:port")`，`net.Listen("tcp", ":port")` + `Accept()`，`Read`/`Write`。
- **C#**：`TcpClient`/`TcpListener`，或 `Socket` 类。

按用户技术栈给出对应片段，并提醒：收发要处理缓冲与边界，服务端要处理多客户端（多线程/异步/select 等）和优雅关闭。

---

## 常见错误与排查

| 现象 | 可能原因 | 建议 |
|------|----------|------|
| Connection refused | 目标端口无服务监听、或防火墙拦截 | 确认服务已启动、监听地址和端口正确；检查本机/目标机防火墙 |
| Timeout | 网络不通、路由/防火墙丢弃、目标未监听 | 先 ping（若允许），再用端口检测工具测目标端口 |
| Address already in use | 端口被占用或 TIME_WAIT 未释放 | 换端口或等待；服务端可考虑 SO_REUSEADDR（依语言/OS） |
| Broken pipe / Connection reset | 对端关闭连接后本端仍写 | 检查关闭顺序与错误处理，写前判断连接是否仍有效 |

---

## 协议与数据

- **自定义协议**：需约定边界（长度前缀、分隔符、固定头等），避免粘包/半包处理错误。
- **调试**：可用 Wireshark、tcpdump 抓包；本地测试可用 `127.0.0.1` 或 `localhost`。

---

## 安全与注意

- 暴露在公网的服务要鉴权、限流，避免裸 TCP 直接暴露敏感能力。
- 生产环境避免在代码里写死 IP/端口，用配置或环境变量。
