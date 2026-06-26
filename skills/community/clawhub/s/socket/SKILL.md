---
name: socket
description: Helps with the socket abstraction, socket options, blocking vs non-blocking I/O, and multiplexing (select, poll, epoll). Use when the user asks about socket APIs, SO_* options, Unix domain sockets, or how to structure TCP/UDP server code at the socket level.
---

# Socket

本 Skill 帮助理解和使用**套接字（socket）**这一层抽象：类型与选项、阻塞/非阻塞、I/O 多路复用，以及与 TCP/UDP 的关系。具体 TCP/UDP 收发示例见 tcp / udp 两个 Skill。

---

## 何时使用

当用户提到或需要：

- socket API 概念（AF_INET、SOCK_STREAM、SOCK_DGRAM）
- socket 选项（SO_REUSEADDR、缓冲区大小、超时等）
- 阻塞 vs 非阻塞、select / poll / epoll / kqueue
- Unix 域套接字（本地进程间通信）
- 如何选 TCP 还是 UDP、如何组织服务端 socket 代码

---

## Socket 类型与协议族

- **AF_INET** + **SOCK_STREAM**：TCP，可靠流式；需 connect/listen/accept。
- **AF_INET** + **SOCK_DGRAM**：UDP，无连接数据报；用 sendto/recvfrom。
- **AF_UNIX**（或 AF_LOCAL） + **SOCK_STREAM** / **SOCK_DGRAM**：Unix 域套接字，本机进程间通信，用文件路径作为地址。

选型：要可靠、有序、长连接用 TCP；要低延迟、可容忍丢包用 UDP；本机 IPC 可考虑 Unix domain。

---

## 常用 Socket 选项

| 选项（常见名） | 作用 | 典型用法 |
|----------------|------|----------|
| SO_REUSEADDR   | 允许 bind 到处于 TIME_WAIT 的端口 | 服务端重启快速复用同一端口 |
| SO_REUSEPORT   | 多进程/线程同端口监听（部分 OS） | 负载均衡或多 worker |
| SO_RCVBUF / SO_SNDBUF | 接收/发送缓冲区大小 | 高吞吐或大延迟时调大 |
| SO_RCVTIMEO / SO_SNDTIMEO | 收/发超时 | 避免无限阻塞 |
| TCP_NODELAY    | 禁用 Nagle（仅 TCP） | 低延迟小包场景 |

设置方式依语言而异：Python `setsockopt()`，Go `SetReadDeadline` 等，按用户语言给出对应 API。

---

## 阻塞与非阻塞

- **阻塞**：read/recv 时无数据会一直等；写缓冲区满时 write/send 会等。实现简单，但一线程一连接时扩展性差。
- **非阻塞**：读不到/写不下立即返回错误（如 EAGAIN/EWOULDBLOCK），由调用方重试或配合 I/O 多路复用。
- **超时**：通过 SO_RCVTIMEO/SO_SNDTIMEO 或 select/poll 的超时，在阻塞模式下也能限制等待时间。

高并发服务端通常用非阻塞 + I/O 多路复用或异步 API（如 asyncio、libuv、Go net 的 goroutine）。

---

## I/O 多路复用（简要）

单线程/进程同时等待多个 socket 可读/可写：

- **select**：跨平台，有 fd 数量上限和性能限制；参数为读/写/异常 fd 集合与超时。
- **poll**：以 pollfd 数组替代 fd_set，无最大 fd 限制，接口更清晰；Linux/BSD 常见。
- **epoll**（Linux）/ **kqueue**（BSD/macOS）：边缘触发或水平触发，适合大量连接。

各语言往往有封装（如 Python `selectors`、Node 的 libuv、Go 的 net 包），按用户语言给出推荐用法而非手写 C。

---

## Unix 域套接字

- **地址**：文件路径（如 `/tmp/app.sock`）或抽象命名（Linux）。
- **优点**：无需经过网络栈，本机通信更高效；可用文件权限控制访问。
- **流程**：服务端 socket + bind(path) + listen（STREAM）或直接 recvfrom（DGRAM）；客户端 connect(path) 或 sendto(path)。

Windows 上无原生 AF_UNIX（较新版本有 AF_UNIX），跨平台需考虑替代（如 TCP localhost 或命名管道）。

---

## 与 TCP / UDP Skill 的关系

- **具体 TCP 连接、测试、代码示例**：见 **tcp** Skill。
- **具体 UDP 收发、测试、代码示例**：见 **udp** Skill。
- 本 Skill 侧重：socket 抽象、选项、阻塞/非阻塞、多路复用、Unix domain；遇到“怎么设 SO_REUSEADDR”“select 怎么用”“Unix socket 怎么建”等用本 Skill。

---

## 常见注意点

- 服务端关闭时先 close 已 accept 的 client socket，再 close listen socket；客户端确保不再写后再 close，避免 RST。
- 收发包要处理返回值（短写、0 表示对端关闭等），并做好错误与边界处理。
- 生产环境不写死 IP/端口/路径，用配置或环境变量。
