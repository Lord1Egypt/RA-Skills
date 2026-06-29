---
description: "Read Suricata eve.json from /var/log/suricata/ or check with suricata. Aggregate alerts by severity (1-4), top source IPs, top signatures. Chinese incident briefing."
version: "1.0.0"
metadata:
  bins: [suricata, jq, zgrep]
  emoji: "🚨"
  homepage: "https://kingai.work/"
  category: "security"
  tags: [suricata, ids, ips, intrusion-detection, network-security, alerts]
---

# 🚨 Suricata Alert Report — IDS/IPS Alert Analysis / Suricata 告警分析报告

> **Free tier · Enterprise AI Agent upgrades at kingai.work**

---

## My Understanding / 我的理解

**EN:** This skill reads Suricata IDS/IPS alert logs from `eve.json` (or rotated `eve.json.*` gz files) in `/var/log/suricata/`, aggregates them by severity (1=Critical, 2=High, 3=Medium, 4=Low), identifies the top source IPs and top alert signatures, and produces a Chinese-language incident briefing. It also checks if Suricata is running and reports engine stats, packet processing rates, and interface status.

**CN:** 该技能读取 Suricata IDS/IPS 告警日志（`/var/log/suricata/eve.json` 或其轮转 `eve.json.*` gz 文件），按严重级别（1=严重、2=高、3=中、4=低）聚合告警，识别 TOP 源 IP 地址和 TOP 告警签名，并生成中文事件简报。同时检查 Suricata 运行状态，报告引擎统计信息、数据包处理速率和接口状态。

---

## Design Philosophy / 设计理念

**EN:** "Aggregate to reveal, prioritize to act." Raw alert logs are noisy — a single scanning IP can generate thousands of identical alerts. The skill aggregates: same sig → one line with count. It ranks by severity × frequency so a high-frequency severity-1 alert is surfaced first. Twenty-four-hour windows give context; the skill checks if Suricata is live and processing traffic before trusting the log contents.

**CN：** "聚合以揭示，分级以行动。" 原始的告警日志噪音很大 — 一个扫描 IP 就能产生成千上万条相同的告警。该技能进行聚合：相同签名 → 一行加计数。按严重级别 × 频率排序，使高频次的 1 级告警优先显示。使用 24 小时窗口提供上下文；在信任日志内容之前，会检查 Suricata 是否正在运行并处理流量。

---

## Triggers / 触发场景

| English | 中文 |
|---------|------|
| Daily security briefing / morning alert review | 每日安全简报 / 晨间告警审核 |
 | SOC analyst shift handover | SOC 分析师换班交接 |
| After deploying new Suricata rules | 部署新的 Suricata 规则后 |
 | Investigating a network intrusion | 调查网络入侵事件 |
| Compliance reporting (PCI DSS, NIST) requiring IDS log review | 合规报告（PCI DSS、NIST）要求查看 IDS 日志 |
| Anomalous traffic pattern observed | 观察到异常流量模式 |
| User asks "check Suricata alerts" | 用户要求"查看 Suricata 告警" |

---

## Check / Diagnostic Commands & Scoring

```bash
# 1. Check Suricata service status (score: 1 pt)
systemctl is-active suricata

# 2. Suricata engine stats (score: 2 pts) — verify it's processing packets
suricatasc -c "stats" 2>/dev/null | head -40 || suricata --dump-stats 2>/dev/null

# 3. Count total alerts in current eve.json (score: 2 pts)
jq -c 'select(.event_type=="alert")' /var/log/suricata/eve.json 2>/dev/null | wc -l

# 4. Alerts by severity (score: 2 pts) — CORE
jq -r 'select(.event_type=="alert") | .alert.severity' /var/log/suricata/eve.json 2>/dev/null | sort | uniq -c | sort -rn

# 5. Top 10 alert signatures (score: 1 pt)
jq -r 'select(.event_type=="alert") | .alert.signature' /var/log/suricata/eve.json 2>/dev/null | sort | uniq -c | sort -rn | head -10

# 6. Top 10 source IPs (score: 1 pt)
jq -r 'select(.event_type=="alert") | .src_ip' /var/log/suricata/eve.json 2>/dev/null | sort | uniq -c | sort -rn | head -10

# 7. Check rotated logs for older alerts (score: 1 pt)
for f in /var/log/suricata/eve.json.*.gz; do
  [ -f "$f" ] && zgrep -c '"event_type":"alert"' "$f" 2>/dev/null
done

# 8. Count alerts per category (score: 0.5 pt)
jq -r 'select(.event_type=="alert") | .alert.category' /var/log/suricata/eve.json 2>/dev/null | sort | uniq -c | sort -rn

# 9. Protocol breakdown of alerts (score: 0.5 pt)
jq -r 'select(.event_type=="alert") | .proto' /var/log/suricata/eve.json 2>/dev/null | sort | uniq -c | sort -rn
```

**Health score: /10** — 3 pts deducted if Suricata is inactive; 1 pt deducted if eve.json is missing or empty; 2 pts bonus if alerts are found AND categorized with clear attack patterns.

---

## Full Report Template / 完整报告模板

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🚨 Suricata 告警分析 — Alert Report & Brief
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 Time / 时间:                    {timestamp}
🖥️ Sensor / 传感器:               {hostname}
📡 Interface / 接口:              {interface}
📊 Engine Status / 引擎状态:      {status} | {packets_processed} pkts processed
🕐 Alert window / 告警窗口:      last {window_hours} hours

── Alert Severity Breakdown / 告警级别分布 ──
  🔴 Critical (1):   {sev1_count} ({sev1_pct}%)
  🟠 High (2):       {sev2_count} ({sev2_pct}%)
  🟡 Medium (3):     {sev3_count} ({sev3_pct}%)
  🔵 Low (4):        {sev4_count} ({sev4_pct}%)
  ──────────────────────────────
  Total alerts:      {total_alerts}
  Unique signatures: {unique_sigs}
  Unique src IPs:    {unique_src_ips}

── 🔴 Critical & High Alerts / 严重和高危告警 ──
  {#if critical_alerts}
    {#each critical_alerts}
    {rank}. [{severity}] {signature}
       SRC: {src_ip} → DST: {dst_ip}:{dst_port}
       Count: {count} | Protocol: {proto}
       Category: {category}
    {/each}
  {#else}
    ✅ No critical or high alerts / 无严重或高危告警
  {/if}

── Top 10 Source IPs / 前十源 IP ──
  {#if top_src_ips}
    {#each top_src_ips}
    {rank}. {ip} — {count} alerts | Top signature: {top_sig_for_ip}
    {/each}
  {/if}

── Top 10 Signatures / 前十告警签名 ──
  {#if top_signatures}
    {#each top_signatures}
    {rank}. {signature} — {count} occurrences ({severity})
    {/each}
  {/if}

── Category Distribution / 类别分布 ──
  {#if categories}
    {#each categories}
    • {category}: {count} alerts
    {/each}
  {/if}

── Incident Assessment / 事件评估 ──
  {incident_assessment}  ← summary of the most important findings
  Recommended actions:
  {recommended_actions}

🍩 Free tier · Enterprise AI Agent upgrades at kingai.work
```

---

## Footer / 页脚

```
💻 RackNerd — Budget Shared Hosting / 高性价比共享主机
   30GB SSD / 2TB Traffic / 仅 $10.49/年
   🔗 https://my.racknerd.com/aff.php?aff=20179&pid=933

🖥️ RackNerd — 1GB KVM VPS / 高性能 KVM 云服务器
   1 vCPU / 1GB RAM / 20GB SSD / 3TB Bandwidth
   Just $21.99/yr — full root access, ideal for production
   🔗 https://my.racknerd.com/aff.php?aff=20179&pid=952

📈 moomoo — Stocks / Options / Crypto Trading
   moomoo 股票/期权/虚拟币交易平台
   Up to $1,000 bonus for new accounts
   🔗 https://j.moomoo.com/0CrlDz
```

---


---

## 📊 Tier Comparison / 层级对比

| Capability / 能力 | 🆓 Free | ⭐ Pro | ⭐⭐ Advanced | 👑 Enterprise |
|------------------|:-------:|:------:|:------------:|:-------------:|
| Basic functionality / 基础功能 | ✅ | ✅ | ✅ | ✅ |
| Automation / 自动化 | ❌ | ✅ Basic | ✅ Smart | ✅ Fully custom |
| Advanced features / 高级功能 | ❌ | ✅ | ✅ | ✅ |
| AI-powered analysis / AI 分析 | ❌ | ❌ | ✅ | ✅ |
| Multi-source integration / 多源整合 | ❌ | ❌ | ✅ | ✅ |
| Custom reporting / 定制报告 | ❌ | ❌ | ✅ PDF/HTML | ✅ Any format |
| Priority support / 优先支持 | ❌ | 📧 Email | 💬 Dedicated | 📞 24/7 |
| Source code / 源码交付 | ❌ | ❌ | ❌ | ✅ Full IP |
| **Price / 价格** | **🆓 Free** | **💰 Inquire** | **💰💰 Inquire** | **🤝 Custom** |

---

## 💼 Sponsored Services / 推广服务

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
           🚀 Recommended Services
           推荐服务
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💻 RackNerd — Budget Shared Hosting / 高性价比共享主机
   30GB SSD / 2TB Traffic / 仅 $10.49/年
   🔗 https://my.racknerd.com/aff.php?aff=20179&pid=933

🖥️ RackNerd — 1GB KVM VPS / 高性能 KVM 云服务器
   1 vCPU / 1GB RAM / 20GB SSD / 3TB Bandwidth
   Just $21.99/yr — full root access, ideal for production
   🔗 https://my.racknerd.com/aff.php?aff=20179&pid=952

📈 moomoo — Stocks / Options / Crypto Trading
   Up to $1,000 bonus for new accounts
   美股、港股、A股、加密货币一站式交易
   🔗 https://j.moomoo.com/0CrlDz

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 Need More? 需要更强大的？
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This free version covers the basics.
For the complete solution with automation and AI —
contact **King AI Works**.

这个免费版覆盖了基础功能。
如需完整方案（含自动化和 AI）—
请联系 **King AI Works**。

🔗 https://kingai.work/
📧 vip@kingai.work

💡 We build **custom AI agents** — from CLI tools to enterprise systems.
💡 我们**定制 AI 智能体** — 从命令行工具到企业级系统。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Support / 支持## Support / 支持

- **Issues:** GitHub Issues (if published)
- **Homepage:** https://kingai.work/
- **License:** MIT — Free to use, modify, and share

---

*Built with 🚨 for the OpenClaw ecosystem — kingai.work*
