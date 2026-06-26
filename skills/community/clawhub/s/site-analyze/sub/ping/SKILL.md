---
name: site-analyzer/ping
description: 延迟探测子 skill。同时执行 ICMP ping 和 TCP 端口连接延迟测试（默认 80/443），统计丢包率、min/avg/max RTT。TCP 探测使用 Python socket 实现，无需 root 权限。当用户要测某主机的网络延迟、连通性、丢包率时使用。
---

# 延迟探测 (ping)

## 快速调用

```bash
# 默认：ICMP + TCP:80 + TCP:443，各 5 次
python3 ./05_ping.py <host>

# 指定探测次数
python3 ./05_ping.py <host> --count 10

# 指定 TCP 端口
python3 ./05_ping.py <host> --tcp-port 8080 --tcp-port 443

# JSON 输出
python3 ./05_ping.py <host> --json
```

## 输出说明

```
=== Ping/延迟探测: <host> ===

  [ICMP]     loss=0%   min=1.2ms  avg=2.3ms  max=4.5ms
  [TCP:80]   loss=0%   min=1.5ms  avg=2.1ms  max=3.8ms
  [TCP:443]  loss=0%   min=1.6ms  avg=2.2ms  max=3.9ms
```

## 解读参考

| 指标 | 说明 |
|------|------|
| loss > 0% | 存在丢包，网络不稳定或目标限速 |
| ICMP 超时但 TCP 正常 | 目标屏蔽了 ICMP，不代表不通 |
| TCP 超时但 ICMP 正常 | 端口未开放或被防火墙拦截 |
| avg > 100ms | 跨境或远距离节点 |

## 注意

- ICMP ping 需要 ping 命令可用（容器内通常有限制）
- TCP 探测用 Python socket，无需特权，更可靠
- 如 ICMP 失败，以 TCP 结果为准
