---
name: site-analyzer/ip-info
description: IP 归属查询子 skill。批量查询 IP 的国家/城市/ISP/ASN，使用 ip-api.com（主）和 ipinfo.io（补充）双源合并。支持单个或多个 IP，自动跳过私有地址。当用户要查某个 IP 属于哪个机房、哪个运营商、哪个国家时使用。
---

# IP 归属查询 (ip-info)

## 快速调用

```bash
# 单个 IP
python3 ./02_ip_info.py <ip>

# 多个 IP
python3 ./02_ip_info.py <ip1> <ip2> <ip3>

# 从 stdin 批量输入
echo -e "1.2.3.4\n5.6.7.8" | python3 ./02_ip_info.py --stdin

# JSON 输出（供其他脚本使用）
python3 ./02_ip_info.py <ip> --json
```

## 输出说明

```
[<ip>]
  位置: <国家> · <省/地区> · <城市>
  组织: <ISP/运营商名>
  ASN:  AS<编号> <名称>
```

## 数据来源

| 来源 | 地址 | 说明 |
|------|------|------|
| ip-api.com | http://ip-api.com/json/{ip} | 主源，含 ISP/org/城市 |
| ipinfo.io | https://ipinfo.io/{ip}/json | 补充源，含 hostname |

两源数据合并，ip-api 优先，ipinfo 补充缺失字段。

## 注意

- 私有 IP（10.x / 172.16.x / 192.168.x）自动标注为内网，不发起查询
- 并发查询，多 IP 时不会串行等待
