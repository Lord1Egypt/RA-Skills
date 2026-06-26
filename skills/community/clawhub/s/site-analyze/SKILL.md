---
name: site-analyzer
description: 站点综合分析工具，析出域名/IP的机房位置、ISP、网络路径、robots策略等完整站点画像。当用户要分析某个域名或IP的机房部署、归属、网络质量时触发。支持：分析源机房位置、ISP/ASN归属、GeoDNS/CDN检测、traceroute路径分析、延迟探测、robots.txt策略。首次使用自动探测本机网络环境作为参照基准。
---

# 站点分析 Skill

## 调用流程链

```
用户输入: <domain 或 IP>
         │
         ▼
┌─────────────────────────────────────────────────────┐
│  00_probe_env.sh  （首次/--force）                   │
│  探测本机出口 IP、归属、可用工具，写入               │
│  ~/.site-analyzer-env.json 作为分析基准              │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│  Phase 1：并发执行（3 路同时）                       │
│                                                     │
│  01_dig.py          02_ip_info.py*   06_robots.py   │
│  DNS 查询           (* dig 完后调用)  robots.txt     │
│  ├ UDP dig          IP 归属查询       抓取 + 解析     │
│  └ DoH 回退         双源合并                         │
│    (UDP 失败时)      ip-api + ipinfo                 │
│                                                     │
│  04_whois.py                                        │
│  WHOIS 注册信息                                      │
└─────────────────┬───────────────────────────────────┘
                  │ dig 返回 IP 列表
                  ▼
┌─────────────────────────────────────────────────────┐
│  Phase 2：对第一个 IP 串行执行                       │
│                                                     │
│  03_traceroute.py          05_ping.py               │
│  路由追踪                   延迟探测                  │
│  └ 每跳调用 02_ip_info.py   ├ ICMP ping              │
│    查公网 IP 归属            └ TCP:80/443 探测        │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│  汇总输出：站点画像                                  │
│  【IP 归属】【DNS 解析/GeoDNS】【WHOIS】              │
│  【robots.txt】【延迟】【Traceroute 摘要】            │
│  【结论：机房位置 · ISP · CDN · 注册信息】           │
└─────────────────────────────────────────────────────┘
```

**单独调用任意子 skill（按需）：**

```
domain/IP ──► 01_dig.py          → IP 列表 + CNAME 链 + GeoDNS 判断
IP        ──► 02_ip_info.py      → 国家/城市/ISP/ASN
domain/IP ──► 03_traceroute.py   → 逐跳路径 + 每跳归属
              └ --parse-text     → 解析粘贴的 traceroute 文本
domain/IP ──► 04_whois.py        → 注册商/时间/注册人
host      ──► 05_ping.py         → RTT + 丢包率（ICMP + TCP）
domain    ──► 06_robots.py       → 爬虫策略（Allow/Disallow/Sitemap）
```

---

## 子 Skill 索引

| 子 Skill | SKILL.md | 脚本 | 功能 |
|----------|----------|------|------|
| `site-analyzer/dig` | `sub/dig/` | `01_dig.py` | DNS 查询，UDP + DoH 回退，GeoDNS 检测 |
| `site-analyzer/ip-info` | `sub/ip-info/` | `02_ip_info.py` | IP 归属，ip-api + ipinfo 双源 |
| `site-analyzer/traceroute` | `sub/traceroute/` | `03_traceroute.py` | 路由追踪 + 逐跳归属，支持解析粘贴文本 |
| `site-analyzer/whois` | `sub/whois/` | `04_whois.py` | WHOIS 注册信息查询 |
| `site-analyzer/ping` | `sub/ping/` | `05_ping.py` | ICMP + TCP 延迟探测 |
| `site-analyzer/robots` | `sub/robots/` | `06_robots.py` | robots.txt 抓取与解析 |

---

## 快速调用

```bash
# 完整分析（自动串联全部子 skill）
python3 /projects/.openclaw/skills/site-analyzer/scripts/analyze.py <domain_or_ip>

# 单独调用
python3 .../scripts/01_dig.py <domain>
python3 .../scripts/02_ip_info.py <ip1> [ip2 ...]
python3 .../scripts/03_traceroute.py <target> [--max-hops 20]
python3 .../scripts/04_whois.py <domain_or_ip>
python3 .../scripts/05_ping.py <host> [--tcp-port 443]
python3 .../scripts/06_robots.py <domain>

# 解析粘贴的 traceroute 文本
echo "<traceroute_output>" | python3 .../scripts/03_traceroute.py --parse-text

# 重新探测本机网络环境
bash .../scripts/00_probe_env.sh --force
```

所有脚本支持 `--json` 输出结构化数据。

---

## DNS 策略

| 阶段 | 方式 | 服务器 |
|------|------|--------|
| 优先 | UDP dig | 阿里 223.5.5.5/223.6.6.6，Google 8.8.8.8/8.8.4.4 |
| 回退 | DNS over HTTPS | 阿里 dns.alidns.com，Google dns.google，Cloudflare cloudflare-dns.com |

UDP 全部返回空时自动切换 DoH，输出标注 `[via DoH]`。

---

## 输出：站点画像

```
【IP 归属】     IP 所在国家/城市/组织/ASN
【DNS 解析】    国内外解析结果对比，CNAME 链，GeoDNS 检测
【WHOIS】       注册商、注册/到期时间、注册人/国家
【robots.txt】  ✅允许 / ⚠️部分限制 / 🚫完全禁止
【延迟探测】    ICMP + TCP RTT（min/avg/max + 丢包率）
【Traceroute】  公网出口节点 + 目标节点位置
【站点画像】    综合结论（CDN/直连/机房位置/注册信息）
```

---

## 注意事项

- traceroute 中间跳 `* * *` 是路由不响应 ICMP，不影响结论，看首尾两端节点即可
- 私有 IP 自动标注内网，不查归属
- IP 归属数据库有误判（如 DoD 误判内网 IP），11.x/21.x 开头的 IP 通常是容器内网
- 脚本母本在 `scripts/`，子 skill 是副本在 `sub/<name>/`，修改后需同步两处
