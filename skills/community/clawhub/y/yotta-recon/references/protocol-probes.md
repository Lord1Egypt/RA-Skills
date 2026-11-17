# 协议探测说明（yotta-recon）

> 本文件说明引擎对常见协议的具体探测行为，便于理解输出与排查。

## 一、TCP connect 扫描

- 实现：socket.create_connection 逐个端口连接，成功即 open；失败（拒绝/超时）即 closed/filtered。
- 并发：ThreadPoolExecutor 控制并发数（--concurrency，默认 64）。
- 限速：--rate 指定每次连接间隔秒数，用于对目标保持温和（避免扫描风暴）。
- 超时：--timeout 毫秒，默认 1200。

## 二、banner 抓取

- 连接成功后立即尝试读取最多 2048 字节（超时 1.2s）。
- SSH / FTP / SMTP / POP3 / IMAP / MySQL 等服务会主动发送 banner。

## 三、协议探测

| 端口/特征 | 探测内容 |
|---|---|
| HTTP 类端口（80/443/8080/8443/3000/5000 等） | GET / HTTP/1.0，解析 Server / X-Powered-By 等头 |
| 6379（Redis） | PING，期待 +PONG |
| 25/587（SMTP） | 读 banner + EHLO recon |
| 未知端口无 banner | 试探一次 HTTP GET（仅当响应含 HTTP 特征才认定） |

## 四、平台与兼容

- Python 3.8+ 标准库，Windows / Linux / macOS 通用；
- Windows 控制台已做 UTF-8 加固（GBK 环境不崩）；
- 本机监听端口枚举：Linux/macOS 读 /proc/net/tcp（零外部依赖），Windows 用系统 netstat 只读查询。
