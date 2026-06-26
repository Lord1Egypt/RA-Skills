---
name: site-analyzer/dig
description: DNS 查询子 skill。同时用国内（阿里 223.5.5.5/223.6.6.6）和国外（Google 8.8.8.8/8.8.4.4）DNS 解析域名，对比 A/AAAA 记录差异，检测 GeoDNS/CDN 流量调度。当用户要查某域名解析到哪些 IP、国内外解析是否一致时使用。
---

# DNS 查询 (dig)

## 快速调用

```bash
python3 ./01_dig.py <domain>
python3 ./01_dig.py <domain> --json
```

## 输入

- `domain`：域名，如 `baidu.com`、`example.com`

## 输出说明

```
=== DNS 查询: <domain> ===
唯一 IP 集合: <所有DNS返回的去重IP列表>

[alidns_1] 223.5.5.5
  A      <ip>    TTL=<ttl>

[google_1] 8.8.8.8
  A      <ip>    TTL=<ttl>
```

## 关键判断

- **国内/国外 DNS 返回不同 IP** → 存在 GeoDNS 或 CDN，流量在 DNS 层做了调度
- **TTL 很短（< 60s）** → 通常是 CDN 或动态 DNS
- **只有国外 DNS 能解析** → 域名可能未备案或有访问限制

## DNS 服务器

| 标识 | 地址 | 用途 |
|------|------|------|
| alidns_1 | 223.5.5.5 | 国内 |
| alidns_2 | 223.6.6.6 | 国内备用 |
| google_1 | 8.8.8.8 | 国外 |
| google_2 | 8.8.4.4 | 国外备用 |
