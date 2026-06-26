---
name: site-analyzer/whois
description: WHOIS 查询子 skill。查询域名或 IP 的注册信息，包括注册商、注册/到期时间、注册人组织、Name Server、IP 段归属（netname/orgname）等，结构化提取关键字段。当用户要查域名归属、注册时间、IP 段所有者时使用。
---

# WHOIS 查询

## 快速调用

```bash
# 查询域名
python3 ./04_whois.py <domain>

# 查询 IP（返回 IP 段归属）
python3 ./04_whois.py <ip>

# JSON 输出
python3 ./04_whois.py <domain> --json
```

## 输出说明（域名）

```
=== WHOIS: <domain> ===

  registrar        : <注册商名称>
  registrar_url    : <注册商官网>
  creation_date    : <注册时间>
  expiry_date      : <到期时间>
  updated_date     : <最后更新>
  status           : clientDeleteProhibited, ...
  name_servers     : NS1.xxx, NS2.xxx
  registrant_org   : <注册人组织>
  registrant_country: CN
```

## 输出说明（IP）

```
  netname  : <IP 段名称>
  orgname  : <所属组织>
  inetnum  : <IP 段范围>
  country  : CN
  descr    : <描述>
```

## 注意

- `whois` 命令需已安装（TencentOS: `yum install -y whois`）
- 部分域名（如 .cn）由 CNNIC 管理，字段格式略有不同
- 部分字段可能因隐私保护（GDPR/proxy）而被隐藏
