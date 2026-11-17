# 服务与版本指纹（yotta-recon）

> 本文件说明内置指纹识别逻辑与已知风险映射，便于核对与扩展。

## 一、识别方式

指纹识别 = **banner 抓取 + 按端口协议探测**，最终从响应文本中推断产品与版本：

1. 连接成功后先读取服务端主动 banner（如 SSH / FTP / SMTP / Redis 等协议会主动打招呼）；
2. 按端口类型发探测包：HTTP 发 GET，Redis 发 PING，SMTP 发 EHLO；
3. 无主动 banner 且非常见服务端口时，试探一次 HTTP（非标准端口上的 Web 服务很常见）；
4. 从响应文本匹配产品与版本（正则规则，见 scripts/yotta_recon.py 的 identify_service）。

## 二、内置识别规则（product 推断）

| 协议/特征 | 识别结果 |
|---|---|
| Server: Apache/2.4.7 | apache + 版本 |
| Server: nginx/1.18.0 | nginx + 版本 |
| Server: Microsoft-IIS/10.0 | microsoft-iis + 版本 |
| SSH-2.0-OpenSSH_8.9p1 | openssh + 版本 |
| SSH-2.0-dropbear_2020.81 | dropbear + 版本 |
| 220 ProFTPD 1.3.5e | proftpd + 版本 |
| 220 (vsFTPd 2.3.4) | vsftpd + 版本 |
| 220 ... ESMTP Postfix | postfix（无版本则 null） |
| 220 ... ESMTP Exim | exim |
| +OK Dovecot ready | dovecot-pop3 |
| * OK ... Dovecot | dovecot-imap |
| +PONG（Redis 响应） | redis |
| MySQL 握手包（0x0a 开头） | mysql + 版本 |
| TLS 握手（0x16 开头） | tls |
| 含 PostgreSQL | postgresql |

## 三、已知风险映射（仅提示、不利用）

以下为内置映射：版本指纹命中时在报告中标注风险等级并提示「请人工核实」。
不含利用细节，不保证目标真实受影响——版本号可能被伪装或已打补丁。

| 产品/版本前缀 | 等级 | 说明 |
|---|---|---|
| ProFTPD 1.3.5 | high | CVE-2015-3306（mod_copy） |
| vsftpd 2.3.4 | high | CVE-2011-2523 |
| OpenSSH 5.x / 6.x | medium | 已停止维护 |
| OpenSSH 7.x | low | 较旧，建议核实 |
| Apache 2.4.7 / 2.2.x | low | 较旧，建议核实升级 |
| nginx 1.0.x | low | 已停止维护 |
| PHP 5.x | medium | 已停止维护 |
| MySQL 5.5 / 5.6 | low | 已停止维护 |
| ProFTPD 1.3.3 | medium | 较旧 |
| vsftpd 2.3.2 | medium | CVE-2011-0993 等 |

## 四、扩展方式

指纹规则与风险映射集中在 scripts/yotta_recon.py 的 identify_service / KNOWN_RISKS 中，
按需添加正则与映射即可，无需改其它模块。
