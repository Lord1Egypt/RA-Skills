# TunnelProxy - AI 实用技巧 (v0.3.3+)

## 目录

1. [理解新的会话模型](#1-理解新的会话模型)
2. [获取和使用一次性 PTY 会话](#2-获取和使用一次性-pty-会话)
3. [处理 PTY 回显问题](#3-处理-pty-回显问题)
4. [多行命令和脚本](#4-多行命令和脚本)
5. [大文件传输不截断](#5-大文件传输不截断)
6. [获取命令退出码](#6-获取命令退出码)
7. [处理超时](#7-处理超时)
8. [组合使用 - 先传脚本再执行](#8-组合使用---先传脚本再执行)
9. [环境变量传递](#9-环境变量传递)
10. [处理 PTY 粘性输出](#10-处理-pty-粘性输出)
11. [判断远程设备类型](#11-判断远程设备类型)
12. [调试 PTY 问题](#12-调试-pty-问题)
13. [故障速查表](#13-故障速查表)

---

## 1. 理解新的会话模型

1.  Agent 首先通过 HTTP API 注册并获取 Token。
2.  用 Token 请求一个**一次性 PTY 会话端口**。
3.  在 10 秒内用 `nc` 连接该端口，进入交互式 Shell。
4.  端口用完即弃，超时无人连接自动销毁。

```python
import requests

# 1. 注册 Agent 获取 Token
resp = requests.post("http://<host>:8080/api/register", json={
    "agent_id": "my-agent", "hostname": "ai", "username": "root", "os": "linux"
})
token = resp.json()["token"]

# 2. 请求一次性 PTY 会话端口
resp = requests.post("http://<host>:8080/api/session", json={"token": token})
port = resp.json()["port"]

# 3. 在 10 秒内连接！
import socket, time
time.sleep(0.5)  # 稍等端口监听
s = socket.socket()
s.connect(("<host>", port))
s.send(b"ls -la\n")
print(s.recv(4096).decode())
```

---

2. 获取和使用一次性 PTY 会话

HTTP API 优先： 对于简单的命令执行，推荐直接使用 HTTP API 提交命令并轮询结果，无需打开 PTY 会话。

```python
# 提交命令
resp = requests.post("http://<host>:8080/api/exec", json={
    "agent_id": "my-agent", "token": token, "cmd": "ls -la"
})
task_id = resp.json()["task_id"]

# 轮询结果
while True:
    result = requests.get(f"http://<host>:8080/api/result/{task_id}").json()
    if result["status"] == "complete":
        print(result["output"])
        break
    time.sleep(0.2)
```

PTY 会话： 仅当需要交互式操作（如 vim、ssh）或连续执行多条依赖命令时使用。

---

3. 处理 PTY 回显问题

PTY 默认会回显你发送的命令，导致输出混入命令本身。

解决方案：

```bash
# 方法 A：发送 stty -echo 关闭回显（推荐在 nc 连接后首先执行）
echo "stty -echo; ls -la" | nc 127.0.0.1 <动态端口>

# 方法 B：用 ; echo 标记分隔
echo "ls -la; echo '===END==='" | nc 127.0.0.1 <动态端口>
# 然后只取 ===END=== 之前的内容
```

---

4. 多行命令和脚本

```bash
# 用分号分隔
echo "cd /tmp; mkdir test; cd test; pwd" | nc 127.0.0.1 <动态端口>

# 用管道传递多行（推荐）
echo -e "line1\nline2\nline3" | nc 127.0.0.1 <动态端口>

# 执行复杂脚本（用 heredoc）
cat << 'EOF' | nc 127.0.0.1 <动态端口>
for i in 1 2 3; do
    echo "Number $i"
done
EOF
```

---

5. 大文件传输不截断

PTY 不适合传输大量二进制数据，用 HTTP 通道：

```python
# ✅ 正确：大文件用 HTTP API 的文件服务
import requests
# 下载文件
r = requests.get("http://127.0.0.1:8080/path/to/large.bin", stream=True)
with open("large.bin", "wb") as f:
    for chunk in r.iter_content(8192): f.write(chunk)

# ❌ 错误：用 PTY cat 会卡死
echo "cat /path/to/large.bin" | nc 127.0.0.1 <动态端口>  # 别这样
```

---

6. 获取命令退出码

```bash
# 方式1：在命令中捕获
echo "ls /tmp; echo EXIT_CODE=\$?" | nc 127.0.0.1 <动态端口>

# 方式2：用 && 和 || 链式判断
echo "test -f /etc/passwd && echo EXISTS || echo MISSING" | nc 127.0.0.1 <动态端口>
```

---

7. 处理超时

PTY 默认没有命令超时，需要在命令层处理：

```bash
# 用 timeout 命令
echo "timeout 5 ping google.com" | nc 127.0.0.1 <动态端口>

# 或用 curl 的 --max-time
echo "curl --max-time 10 https://slow-site.com" | nc 127.0.0.1 <动态端口>
```

---

8. 组合使用 - 先传脚本再执行

```python
# 1. 上传 Python 脚本 (通过 HTTP 文件上传)
import requests
with open("./my_script.py", "rb") as f:
    requests.post("http://127.0.0.1:8080/upload", data=f.read())

# 2. 通过 PTY 动态端口执行
import socket
s = socket.socket()
s.connect(("127.0.0.1", <动态端口>))
s.send(b"python3 /uploads/my_script.py\n")
result = s.recv(4096).decode()
```

---

9. 环境变量传递

```bash
# 在命令中设置临时环境变量
echo "export MY_VAR=hello; echo \$MY_VAR" | nc 127.0.0.1 <动态端口>

# 或用 env 命令
echo "env MY_VAR=hello bash -c 'echo \$MY_VAR'" | nc 127.0.0.1 <动态端口>
```

---

10. 处理 PTY 粘性输出

PTY 会保留前一个命令的 prompt 和输出：

```python
# 每次执行前清空缓冲区
def clean_exec(cmd):
    s = socket.socket()
    s.connect(("127.0.0.1", <动态端口>))
    # 先发送一个空命令清空
    s.send(b"\n")
    s.recv(4096)  # 吃掉残留
    # 再执行真实命令
    s.send(f"{cmd}\n".encode())
    result = s.recv(4096).decode()
    return result
```

---

11. 判断远程设备类型

```bash
# 检测 Android
echo "getprop ro.build.version.release" | nc 127.0.0.1 <动态端口>

# 检测 Linux 发行版
echo "cat /etc/os-release" | nc 127.0.0.1 <动态端口>

# 检测架构
echo "uname -m" | nc 127.0.0.1 <动态端口>
```

---

12. 调试 PTY 问题

```bash
# 看原始输出（包括控制字符）
echo "ls" | nc 127.0.0.1 <动态端口> | cat -A

# 测试回显状态
echo "echo TEST" | nc 127.0.0.1 <动态端口>
# 如果输出 "echo TEST" 说明回显开启

# 强制重置 PTY 状态
echo -e "stty sane\nreset\n" | nc 127.0.0.1 <动态端口>
```

---

13. 故障速查表

现象 原因 解决
invalid token Token 错误或未注册 检查 Agent 注册状态，重新获取 Token
connection refused (PTY) 动态端口已过期 端口仅 10 秒有效，重新请求 /api/session
输出为空 PTY 回显/缓冲区问题 加 ; echo MARKER 或使用 HTTP API 执行
输出有乱码 二进制数据混入 用 HTTP 通道传二进制
命令卡住 等待用户输入 确保命令不交互
结果被截断 socket.recv 太小 循环读取直到超时
上传失败 缺少 UPLOAD_MAGIC 检查环境变量
部分输出丢失 PTY 行缓冲 用 stdbuf -oL 禁用缓冲

---

核心原则

1. 简单命令用 HTTP API：稳定、可靠、无需管理会话生命周期。
2. 交互操作用动态 PTY：用完即弃，安全。
3. 大文件用 HTTP 文件服务：避免 PTY 通道阻塞。
4. Token 是唯一凭证：妥善保管，勿泄露。

参考链接

· TunnelProxy 项目：https://github.com/TurinFohlen/tunnel_proxy
· FRP 内网穿透：https://github.com/fatedier/frp
· PTY 原理：https://en.wikipedia.org/wiki/Pseudoterminal

```
