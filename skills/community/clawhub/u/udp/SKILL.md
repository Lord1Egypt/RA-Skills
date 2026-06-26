---
name: udp
description: Helps with UDP sockets, datagram send/receive, and network debugging. Use when the user needs to send or receive UDP packets, write UDP client/server code, test UDP ports, or debug packet loss and firewall issues.
---

# UDP

本 Skill 帮助处理 **UDP** 数据报、套接字编程和常见调试：收发报文、测试端口、以及排查丢包、无响应或防火墙等问题。

---

## 何时使用

当用户提到或需要：

- 写 UDP 客户端/服务端（无连接、sendto/recvfrom）
- 测试某主机某 UDP 端口是否在收发（nc -u、脚本）
- 丢包、无响应、防火墙导致 UDP 不通等排查
- 基于 UDP 的协议（如 DNS、自定义游戏/传感器协议）
- 广播、组播（multicast）的简单用法

---

## UDP 与 TCP 的区别（简要）

- **无连接**：无需先 connect，可直接向任意 (host, port) 发 sendto；也可先 connect 固定对端再 send/recv。
- **不保证可靠**：不保证送达、顺序、不重复；适合可容忍丢包或自建重传的场景（如实时音视频、游戏、传感器）。
- **单包边界**：每次 sendto 对应一个 datagram，recvfrom 一次收一个包，无粘包问题（但包可能丢或乱序）。

---

## 快速测试 UDP

### 命令行

- **netcat（nc）**（若已安装）：
  ```bash
  nc -u host port
  ```
  发一条即收（需对端有响应）：
  ```bash
  echo "hello" | nc -u -w1 host port
  ```

- **PowerShell（Windows）**：
  ```powershell
  $udp = New-Object System.Net.Sockets.UdpClient
  $bytes = [Text.Encoding]::UTF8.GetBytes("hello")
  $udp.Send($bytes, $bytes.Length, "host", port)
  $udp.Close()
  ```
  收包需异步或单独脚本，通常配合简单服务端测试。

- **注意**：UDP 无“连接建立”，`Test-NetConnection` 默认测 TCP；测 UDP 往往要本机发包看对端是否回复或抓包确认。

根据用户 OS 和是否已安装 nc 给出对应方案。

---

## 客户端/服务端代码要点

### 通用流程

- **发送端**：创建 socket(SOCK_DGRAM) → sendto(data, (host, port))；可选 connect() 固定对端后只用 send()。
- **接收端**：创建 socket(SOCK_DGRAM) → bind(address, port) → recvfrom() 得到数据和来源地址；回复则对来源地址 sendto()。

无需 listen/accept；一个 socket 可收发多个对端（用 recvfrom 返回的地址区分）。

### 常见语言速查

- **Python**：`socket.socket(socket.AF_INET, socket.SOCK_DGRAM)`，`sendto()`/`recvfrom()`；服务端先 `bind()` 再 `recvfrom()`。
- **Node.js**：`dgram.createSocket("udp4")`，`send()`+`bind()`，事件 `message`（带 msg、rinfo）。
- **Go**：`net.Dial("udp", "host:port")` 或 `net.ListenPacket("udp", ":port")`，`ReadFrom`/`WriteTo`。
- **C#**：`UdpClient`，`Send()`/`Receive()` 或 `SendAsync`/`ReceiveAsync`；服务端 `Bind()` 后 `Receive(ref remoteEP)`。

按用户技术栈给出最小示例，并提醒：UDP 不保证送达，应用层需自己处理超时、重传或丢包逻辑（若需要可靠语义）。

---

## 常见问题与排查

| 现象 | 可能原因 | 建议 |
|------|----------|------|
| 发出去没响应 | 对端未监听、防火墙丢弃、或对端不回复 | 确认对端服务已起并绑定正确端口；检查本机与对端防火墙/安全组是否放行 UDP 该端口 |
| 收不到包 | 未 bind 或 bind 地址不对、防火墙、路由 | 服务端必须先 bind；检查监听 0.0.0.0 还是某网卡 IP；抓包确认是否有到达 |
| 丢包严重 | 缓冲区满、网络拥塞、应用处理慢 | 适当增大 recv 缓冲区；提高处理速度或做队列；避免在 recv 回调里做重活 |
| Address already in use | 端口被占用或 SO_REUSEADDR 未设 | 换端口或设置 SO_REUSEADDR（依语言/OS），便于重启快速复用端口 |

---

## 广播与组播（简要）

- **广播**：向子网广播地址（如 192.168.1.255）sendto；需设置 SO_BROADCAST；仅本地子网。
- **组播**：加入组播组后 sendto 组播地址；需设置组播选项（如 IP_ADD_MEMBERSHIP）；跨子网需路由器支持。

按用户需求给出该语言下的关键 API 名和选项，不展开协议细节。

---

## 安全与注意

- UDP 无连接，易被伪造来源；对公网服务要做应用层鉴权与校验，防止滥用或放大攻击。
- 生产环境 IP/端口用配置或环境变量，不写死在代码里。
