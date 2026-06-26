---
name: site-analyzer/traceroute
description: 路由追踪子 skill。执行 traceroute 并对每一跳的公网 IP 自动查询归属（国家/城市/ISP/ASN），输出完整路径画像。支持直接追踪目标，也支持解析用户粘贴的 traceroute 文本。当用户要分析流量路径、出口节点、机房位置或粘贴了一段 traceroute 输出时使用。
---

# 路由追踪 (traceroute)

## 快速调用

```bash
# 追踪域名或 IP（自动查每跳归属）
python3 ./03_traceroute.py <domain_or_ip>

# 限制最大跳数
python3 ./03_traceroute.py <target> --max-hops 15

# 解析用户粘贴的 traceroute 文本
echo "<traceroute_output>" | python3 ./03_traceroute.py --parse-text

# JSON 输出
python3 ./03_traceroute.py <target> --json
```

## 输出说明

```
=== Traceroute: <target> ===

   1  192.168.1.1          <1ms       内网
   2  10.200.16.1          1.2ms      内网
   3  113.96.4.153         3.5ms      China · Guangzhou  Chinanet AS4134
   ...
  18  203.119.26.5         45.2ms     Japan · Tokyo      NTT AS2914
```

## 关键分析点

- **第一个公网 IP** → 本机出口节点，判断流量从哪个运营商出境
- **跳数突增/延迟跳变** → 跨运营商或跨境点
- **连续 `* * *`** → 中间路由不响应 ICMP，不代表丢包（继续看后续跳）
- **最后一跳** → 目标机房位置和运营商

## 解析粘贴文本的场景

当用户直接发来一段 traceroute 输出时，用 `--parse-text` 模式：
```bash
# 从用户消息中提取 traceroute 文本保存为临时文件
cat > /tmp/tr.txt << 'EOF'
<用户粘贴的traceroute内容>
EOF
python3 ./03_traceroute.py --parse-text < /tmp/tr.txt
```
