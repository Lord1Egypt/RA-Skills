# 邮件域名 DNS 认证指南

## 目录

- [概述](#概述)
- [主域名与非主域名](#主域名与非主域名)
- [1. MX 验证（Mail Exchange）](#1-mx-验证mail-exchange)
- [2. SPF 验证（Sender Policy Framework）](#2-spf-验证sender-policy-framework)
  - [配置方法](#配置方法-1)
  - [记录格式详解](#记录格式详解)
  - [常见 ESP 的 SPF include 域名](#常见-esp-的-spf-include-域名)
  - [多 ESP 共存示例](#多-esp-共存示例)
  - [SPF Flattening](#spf-flattening当-dns-lookup-超限时)
- [3. DKIM 验证（DomainKeys Identified Mail）](#3-dkim-验证domainkeys-identified-mail)
  - [配置方法](#配置方法-2)
  - [密钥长度建议](#密钥长度建议)
- [4. DMARC 验证](#4-dmarc-验证domain-based-message-authentication-reporting--conformance)
  - [配置方法](#配置方法-3)
  - [策略等级](#策略等级)
  - [渐进式部署路径](#渐进式部署路径)
  - [常用标签](#常用标签)
- [5. DNS 配置完整示例](#5-dns-配置完整示例)
- [6. DNS 配置验证](#6-dns-配置验证)
- [7. DNS 传播检测](#7-dns-传播检测)
- [8. 常见问题与解决方案](#8-常见问题与解决方案)
- [9. CNAME 记录冲突说明](#9-cname-记录冲突说明)

---

## 概述

邮件域名认证是保障邮件安全性、防止邮件伪造以及提升邮件送达率的关键配置。完整的邮件域名认证需要配置以下四种 DNS 记录：

| 记录类型 | 全称 | 核心作用 |
|----------|------|----------|
| **SPF** | Sender Policy Framework | 声明授权的发信服务器，防止发件人伪造 |
| **DKIM** | DomainKeys Identified Mail | 通过加密签名验证邮件完整性与发件方身份 |
| **DMARC** | Domain-based Message Authentication, Reporting & Conformance | 基于 SPF 和 DKIM 结果制定处理策略，并提供报告机制 |
| **MX** | Mail Exchange | 指定接收邮件的服务器，用于接收退信通知等回复邮件 |

---

## 主域名与非主域名

在配置 DNS 记录前，请先确认您的发信域名类型。**主域名**和**非主域名**在 DNS 记录的主机记录填写方式上存在差异：

| 域名类型 | 示例 | 说明 |
|----------|------|------|
| **主域名** | `sampledomain.com` | 直接使用顶级域名作为发信域名 |
| **非主域名** | `abc.sampledomain.com` | 使用子域名作为发信域名 |

> 💡 **建议**：推荐使用非主域名（如 `mail.example.com`）作为发信域名，以避免与主域名现有的 DNS 记录产生冲突。

---

## 1. MX 验证（Mail Exchange）

### 作用

指定接收邮件的服务器。配置 MX 记录后，可正常接收退信通知等回复邮件。

### 配置方法

| 配置项 | 主域名 | 非主域名（如 `abc.sampledomain.com`） |
|--------|--------|---------------------------------------|
| **主机记录** | `@` | `abc` |
| **记录类型** | MX | MX |
| **记录值** | `mxbiz1.qq.com.` | `mxbiz1.qq.com.` |

> ⚠️ **注意**：
> - 记录值末尾**必须包含 `.`**（部分 DNS 服务商会自动添加，请在配置后确认最终记录中仅有一个 `.`）。
> - 如果您有自建邮件服务器，可将记录值替换为您的邮件服务器地址。

---

## 2. SPF 验证（Sender Policy Framework）

### 作用

声明哪些 IP 或服务器有权代表该域名发送邮件，是防止邮件伪造的第一道防线。

### 配置方法

| 配置项 | 主域名 | 非主域名（如 `abc.sampledomain.com`） |
|--------|--------|---------------------------------------|
| **主机记录** | `@` | `abc` |
| **记录类型** | TXT | TXT |
| **记录值** | `v=spf1 include:qcloudmail.com ~all` | `v=spf1 include:qcloudmail.com ~all` |

> ⚠️ **注意**：
> - 如果同时使用多个邮件推送服务商，须在记录值中保留所有服务商的域名。例如：`v=spf1 include:qcloudmail.com include:domain1.com ~all`。
> - **每个域名下仅允许存在一条 SPF 记录**，多条 SPF 记录会导致全部失效（RFC 规范要求）。

### 记录格式详解

```
v=spf1 [mechanisms...] [qualifier]all
```

#### 常见机制

| 机制 | 说明 | 是否消耗 DNS Lookup |
|------|------|:-------------------:|
| `include:domain` | 包含另一域名的 SPF 策略 | ✅ 是 |
| `ip4:x.x.x.x` | 允许指定的 IPv4 地址 | ❌ 否 |
| `ip6:x::x` | 允许指定的 IPv6 地址 | ❌ 否 |
| `a` / `a:domain` | 允许域名的 A 记录对应 IP | ✅ 是 |
| `mx` / `mx:domain` | 允许域名的 MX 记录对应 IP | ✅ 是 |
| `ptr` | 反向解析验证（已废弃，不建议使用） | ✅ 是 |
| `exists:domain` | 存在性检查 | ✅ 是 |
| `redirect=domain` | 重定向至另一 SPF 策略 | ✅ 是 |

#### 限定符（Qualifier）

| 符号 | 含义 | 推荐度 |
|------|------|--------|
| `-all` | 严格拒绝（Fail） | ⭐⭐⭐⭐⭐ 最终目标 |
| `~all` | 软拒绝（SoftFail） | ⭐⭐⭐⭐ 初期推荐 |
| `?all` | 中性（Neutral） | ⭐⭐ 安全性较低 |
| `+all` | 允许所有（Pass） | ❌ 极不安全，禁止使用 |

#### DNS Lookup 限制

**SPF 协议规定每次验证最多执行 10 次 DNS Lookup**（RFC 7208）。超过此限制将导致 SPF PermError，验证直接失败。

### 常见 ESP 的 SPF include 域名

| 邮件服务商 | include 域名 |
|-----------|-------------|
| 腾讯云 SES | `qcloudmail.com` |
| 阿里云邮件推送 | `spf1.dm.aliyun.com` |
| Amazon SES | `amazonses.com` |
| SendGrid | `sendgrid.net` |
| Mailgun | `mailgun.org` |
| Google Workspace | `_spf.google.com` |
| Microsoft 365 | `spf.protection.outlook.com` |
| Zoho Mail | `zoho.com` |
| Postmark | `postmarkapp.com` |

### 多 ESP 共存示例

```
v=spf1 include:qcloudmail.com include:_spf.google.com include:spf.protection.outlook.com ~all
```

### SPF Flattening（当 DNS Lookup 超限时）

将 `include` 递归解析为具体的 `ip4` / `ip6` 地址，从而减少 DNS Lookup 次数。

> ⚠️ **注意**：使用 SPF Flattening 后需定期更新记录，因为邮件服务商的 IP 地址可能随时变更。

---

## 3. DKIM 验证（DomainKeys Identified Mail）

### 作用

通过非对称加密签名验证邮件内容在传输过程中未被篡改，同时确认发件方身份的真实性。

### 配置方法

| 配置项 | 主域名 | 非主域名（如 `abc.sampledomain.com`） |
|--------|--------|---------------------------------------|
| **主机记录** | `qcloud._domainkey` | `qcloud._domainkey.abc` |
| **记录类型** | TXT | TXT |
| **记录值** | 从腾讯云 SES 控制台获取的 DKIM 公钥值 | 从腾讯云 SES 控制台获取的 DKIM 公钥值 |

> ⚠️ **重要提示**：
> - **腾讯云 SES 的 DKIM 验证仅支持 TXT 记录模式，不支持 CNAME 模式**。即使 CNAME 指向的目标域名已配置了正确的 DKIM TXT 记录，腾讯云 SES 也无法通过 CNAME 方式完成验证。
> - 如果 `qcloud._domainkey` 主机记录下已存在 CNAME 记录，**必须先删除 CNAME 记录**，再添加 TXT 记录。CNAME 与 TXT 记录存在冲突，详见 [CNAME 记录冲突说明](#9-cname-记录冲突说明)。
> - DKIM 记录值由腾讯云 SES 在创建发信域名时自动生成，每个域名的记录值不同。
> - 可通过 `ses_tool.py get-domain <domain>` 命令获取腾讯云要求的 DKIM 记录值。
> - 请勿将其他 ESP（如阿里云）的 DKIM 公钥误配为腾讯云的 DKIM 记录。

### 记录格式

```
选择器._domainkey.域名  TXT  "v=DKIM1; k=rsa; p=MIGf..."
```

**腾讯云 SES 的 DKIM 配置参数**：

| 参数 | 值 |
|------|-----|
| 选择器（Selector） | `qcloud` |
| 记录名 | `qcloud._domainkey.<您的域名>` |
| 记录类型 | TXT |
| 记录值 | 由腾讯云 SES 在创建域名时自动生成 |

### 密钥长度建议

| 密钥长度 | 安全等级 | 说明 |
|----------|:--------:|------|
| 2048 bit | ✅ 推荐 | 当前主流安全标准 |
| 1024 bit | ⚠️ 可接受 | 正在逐步淘汰 |
| < 1024 bit | ❌ 不安全 | 应立即升级 |

---

## 4. DMARC 验证（Domain-based Message Authentication, Reporting & Conformance）

### 作用

基于 SPF 和 DKIM 的验证结果，指示收件方如何处理未通过认证的邮件，并提供聚合报告机制。

### 配置方法

| 配置项 | 主域名 | 非主域名（如 `abc.sampledomain.com`） |
|--------|--------|---------------------------------------|
| **主机记录** | `_dmarc` | `_dmarc.abc` |
| **记录类型** | TXT | TXT |
| **记录值** | `v=DMARC1; p=none` | `v=DMARC1; p=none` |

> ⚠️ **注意**：
> - DMARC 记录中**必须包含 `v` 和 `p` 标签**。
> - 如需接收认证报告，可添加 `rua` 标签指定报告接收邮箱。

### 策略等级

| 策略 | 含义 | 适用阶段 |
|------|------|----------|
| `p=none` | 仅监控，不对邮件做任何处理 | 第一阶段：数据收集 |
| `p=quarantine` | 将未通过认证的邮件标记为垃圾邮件 | 第二阶段：初步防护 |
| `p=reject` | 直接拒绝未通过认证的邮件 | 第三阶段：严格防护 |

### 渐进式部署路径

```
阶段 1（1~2 周）：  v=DMARC1; p=none; rua=mailto:dmarc@example.com
  ↓ 确认所有合法发件源后
阶段 2（2~4 周）：  v=DMARC1; p=quarantine; pct=50; rua=mailto:dmarc@example.com
  ↓ 确认无误报后逐步提升比例
阶段 3（持续）：    v=DMARC1; p=reject; rua=mailto:dmarc@example.com
```

### 常用标签

| 标签 | 说明 | 默认值 |
|------|------|--------|
| `p` | 策略（必需） | — |
| `sp` | 子域名策略 | 继承 `p` 值 |
| `pct` | 策略应用百分比 | 100 |
| `rua` | 聚合报告接收地址 | 无 |
| `ruf` | 失败报告接收地址 | 无 |
| `adkim` | DKIM 对齐模式（`r`=宽松 / `s`=严格） | `r`（relaxed） |
| `aspf` | SPF 对齐模式（`r`=宽松 / `s`=严格） | `r`（relaxed） |
| `fo` | 失败报告选项 | `0` |

---

## 5. DNS 配置完整示例

### 主域名 `sampledomain.com` 配置清单

| 记录类型 | 主机记录 | 记录值 | 用途 |
|----------|----------|--------|------|
| MX | `@` | `mxbiz1.qq.com.` | 邮件接收服务器 |
| TXT | `@` | `v=spf1 include:qcloudmail.com ~all` | SPF 验证 |
| TXT | `qcloud._domainkey` | `v=DKIM1; k=rsa; p=MIGf...`（从控制台获取） | DKIM 验证 |
| TXT | `_dmarc` | `v=DMARC1; p=none` | DMARC 验证 |

### 非主域名 `abc.sampledomain.com` 配置清单

| 记录类型 | 主机记录 | 记录值 | 用途 |
|----------|----------|--------|------|
| MX | `abc` | `mxbiz1.qq.com.` | 邮件接收服务器 |
| TXT | `abc` | `v=spf1 include:qcloudmail.com ~all` | SPF 验证 |
| TXT | `qcloud._domainkey.abc` | `v=DKIM1; k=rsa; p=MIGf...`（从控制台获取） | DKIM 验证 |
| TXT | `_dmarc.abc` | `v=DMARC1; p=none` | DMARC 验证 |

---

## 6. DNS 配置验证

### 使用 dig 命令验证

DNS 记录配置完成后，可通过 `dig` 命令验证记录是否正确生效。以主域名 `sampledomain.com` 为例：

```bash
# 验证 MX 记录
dig mx +short sampledomain.com

# 验证 SPF 记录
dig txt +short sampledomain.com

# 验证 DMARC 记录
dig txt +short _dmarc.sampledomain.com

# 验证 DKIM 记录
dig txt +short qcloud._domainkey.sampledomain.com
```

返回值应与腾讯云 SES 控制台中显示的期望记录值一致。

### 使用 DNS 诊断工具验证

```bash
# 综合诊断（推荐，自动检查所有记录类型及 CNAME 冲突）
python3 ${SKILL_DIR}/scripts/dns_checker.py check-all <domain>

# 单项检查
python3 ${SKILL_DIR}/scripts/dns_checker.py check-spf <domain>
python3 ${SKILL_DIR}/scripts/dns_checker.py check-dkim <domain> [selector]
python3 ${SKILL_DIR}/scripts/dns_checker.py check-dmarc <domain>
python3 ${SKILL_DIR}/scripts/dns_checker.py check-mx <domain>
```

---

## 7. DNS 传播检测

### DNS 传播时间参考

| DNS 服务商 | 典型传播时间 |
|-----------|-------------|
| Cloudflare | 1 ~ 5 分钟 |
| AWS Route53 | 1 ~ 5 分钟 |
| 阿里云 DNS | 10 ~ 30 分钟 |
| DNSPod | 10 ~ 30 分钟 |
| GoDaddy | 15 ~ 60 分钟 |
| 传统 DNS 服务商 | 最长 48 小时 |

### TTL 设置建议

- TTL（Time To Live）决定 DNS 记录的缓存时间。
- 修改 DNS 记录前，建议先将 TTL 降低至 300 秒，以加速新记录的传播。
- 记录稳定生效后，可将 TTL 恢复至 3600 秒。

### 使用 DoH 检测的 DNS 节点

| 节点 | 覆盖区域 |
|------|----------|
| Google DNS（dns.google） | 全球 |
| Cloudflare DNS（cloudflare-dns.com） | 全球 |
| AliDNS（dns.alidns.com） | 中国大陆 |
| DNSPod（doh.pub） | 中国大陆 |

---

## 8. 常见问题与解决方案

### Q：主域名和非主域名该如何选择？

**A：** 推荐使用**非主域名**（如 `mail.example.com`）作为发信域名，原因如下：
- 不会影响主域名的现有 DNS 记录。
- 可避免与已有的 SPF 记录冲突（例如主域名已用于 Google Workspace 或 Microsoft 365）。
- 如果品牌一致性要求较高，也可选择使用主域名。

### Q：SPF DNS Lookup 超过 10 次怎么办？

**A：** 可使用 SPF Flattening 技术，将 `include` 递归解析为 `ip4` / `ip6` 地址，从而减少 DNS Lookup 次数。也可以清理不必要的 `include` 条目。

### Q：DKIM 验证失败，但记录已配置？

**A：** 请逐项排查以下问题：
1. Selector 名称是否正确（腾讯云 SES 使用 `qcloud`）。
2. 公钥值是否为腾讯云提供的值（请勿与其他 ESP 的密钥混淆）。
3. DNS 记录是否已完成全球传播。
4. 如果发信域名为非主域名（如 `abc.example.com`），主机记录应填 `qcloud._domainkey.abc`，而非 `qcloud._domainkey`。
5. 确认该主机记录下不存在 CNAME 记录（CNAME 与 TXT 记录冲突）。

### Q：DMARC 配置了 `p=reject` 后合法邮件被拒？

**A：** 建议按以下步骤处理：
1. 先将策略回退至 `p=quarantine` 或 `p=none`。
2. 检查 `rua` 聚合报告，确认被拒邮件的来源。
3. 确保所有合法发件源均已在 SPF 记录中完成授权。
4. 确认无误后再逐步恢复策略等级。

### Q：DNS 修改后多久生效？

**A：** 生效时间取决于以下因素：
1. DNS 服务商的传播速度（5 分钟 ~ 48 小时不等）。
2. 原有记录的 TTL 值（旧缓存到期后才会返回新值）。
3. 各地区 DNS 缓存策略差异。

### Q：多个邮件服务的 SPF 记录冲突？

**A：** 将所有 ESP 的 `include` 合并到**同一条** SPF 记录中：
```
v=spf1 include:qcloudmail.com include:_spf.google.com include:sendgrid.net ~all
```
**请勿创建多条 SPF 记录**，否则会导致全部 SPF 验证失效。

### Q：在 DNSPod 注册了域名但 dig 查不到？

**A：** 可能是域名实名认证尚未通过，注册局已暂停该域名的解析。请先确认域名实名认证已完成。

### Q：MX 记录配置后验证不通过？

**A：** 请检查以下几点：
1. 记录值末尾是否包含 `.`（如 `mxbiz1.qq.com.`）。
2. 部分 DNS 服务商会自动在 MX 记录值末尾添加 `.`，请确认最终记录中只有一个 `.`。
3. 如果使用非主域名，主机记录应填子域名前缀（如 `abc`），而非 `@`。

---

## 9. CNAME 记录冲突说明

### 什么是 CNAME 冲突？

根据 DNS 协议规范（RFC1034 和 RFC2181），**CNAME 记录具有最高优先级**。当同一主机记录同时存在 CNAME 和其他类型的 DNS 记录（TXT、MX、A、AAAA 等）时，递归 DNS 服务器会优先返回 CNAME 记录，导致其他记录无法被正常解析。

### 冲突规则

参考 [DNSPod 各记录类型说明及规则](https://cloud.tencent.com/document/product/302/38661)：

| 记录类型 | 与 CNAME 的关系 | 说明 |
|----------|:---------------:|------|
| **A** | ✘ 冲突 | 不能共存 |
| **AAAA** | ✘ 冲突 | 不能共存 |
| **TXT** | ✘ 冲突 | SPF、DKIM、DMARC 验证均使用 TXT 记录 |
| **MX** | ✘ 冲突 | 邮件接收依赖 MX 记录 |
| **SRV** | ✘ 冲突 | 不能共存 |
| **CAA** | ✘ 冲突 | 不能共存 |
| **NS** | ✔ 不冲突 | 可以共存 |
| **CNAME** | ↔ 可多条 | 同类型可共存 |

> **说明**：上表为主机记录为非 `@` 时的冲突规则。当主机记录为 `@` 时，部分 DNS 服务商（如 DNSPod）允许 CNAME 与 MX、TXT 记录共存，但此类配置可能导致解析结果不稳定，**不建议使用**。

### 对腾讯云 SES 域名验证的影响

腾讯云 SES 域名验证需要检查以下 DNS 记录，CNAME 冲突将直接导致验证失败：

| 验证项 | 记录类型 | 检查域名 | CNAME 冲突影响 |
|--------|----------|----------|:--------------:|
| SPF | TXT | `<domain>` | 域名存在 CNAME → SPF 验证失败 |
| DKIM | TXT | `qcloud._domainkey.<domain>` | 存在 CNAME → DKIM 验证失败 |
| DMARC | TXT | `_dmarc.<domain>` | 存在 CNAME → DMARC 验证失败 |
| MX | MX | `<domain>` | 域名存在 CNAME → MX 验证失败 |

> ⚠️ **特别说明**：腾讯云 SES 的 DKIM 验证**不支持 CNAME 模式**。即使 CNAME 指向的目标域名配置了正确的 DKIM TXT 记录，腾讯云 SES 也无法通过 CNAME 方式完成验证。必须使用 TXT 记录直接在 `qcloud._domainkey.<domain>` 下配置 DKIM 公钥。

### 如何排查 CNAME 冲突

**方式一：使用 DNS 诊断工具自动检测**

```bash
# 综合检查（自动检测所有相关域名的 CNAME 冲突）
python3 ${SKILL_DIR}/scripts/dns_checker.py check-all <domain>

# 单项检查（同样会自动检测 CNAME 冲突）
python3 ${SKILL_DIR}/scripts/dns_checker.py check-dkim <domain>
```

**方式二：使用 dig 命令手动检查**

```bash
# 检查发信域名是否存在 CNAME 记录
dig CNAME +short <domain>

# 检查 DKIM 域名是否存在 CNAME 记录
dig CNAME +short qcloud._domainkey.<domain>

# 检查 DMARC 域名是否存在 CNAME 记录
dig CNAME +short _dmarc.<domain>
```

若以上命令返回了 CNAME 记录值，则表示存在冲突，须先删除 CNAME 记录后再配置 TXT / MX 记录。

### 解决方案

| 方案 | 适用场景 | 操作步骤 |
|------|----------|----------|
| **方案一：删除 CNAME 记录**（推荐） | 该域名无需保留 CNAME 记录 | 直接删除 CNAME 记录，添加正确的 TXT / MX 记录 |
| **方案二：使用不同子域名** | 该域名的 CNAME 用于 CDN 等业务 | 使用其他子域名（如 `mail.example.com`）作为发信域名 |

**推荐优先采用方案一或方案二**。