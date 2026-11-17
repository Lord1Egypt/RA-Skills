# 攻击特征与检测规则

> `attack_monitor.py` 的检测规则、日志来源与阈值。所有检测均为只读日志分析。

## 日志来源

| 系统 | 日志路径 | 用途 |
|------|----------|------|
| 通用 | `/var/log/auth.log`（Debian）、`/var/log/secure`（RHEL） | SSH 登录、sudo、su |
| 通用 | `/var/log/syslog`、`/var/log/messages` | 系统事件 |
| SSH | 上述 auth 日志 | 暴力破解、异常登录 |
| Web | `/var/log/nginx/access.log`、`/var/log/apache2/access.log` | Web 扫描、注入尝试 |
| 审计 | `/var/log/audit/audit.log`（若启用 auditd） | 系统调用审计 |
| fail2ban | `/var/log/fail2ban.log` | 已有封禁记录 |

日志不存在时标注 `log_unavailable` 并跳过对应规则，不伪造结果。

## 检测规则（--rules）

### brute-force — 暴力破解检测

| 参数 | 默认 | 说明 |
|------|------|------|
| `threshold` | 5 | 同一来源 IP 在 `window` 内认证失败次数 |
| `window` | 10m | 统计窗口 |
| `target` | sshd | 监控的服务（sshd/ftp/smtp） |

**匹配模式**（auth.log）:
- `Failed password for <user> from <ip> port <p> ssh2`
- `Invalid user <user> from <ip> port <p> ssh2`
- `authentication failure; logname= ... rhost=<ip>`

**输出事件**:
```json
{
  "type": "brute_force",
  "source_ip": "203.0.113.5",
  "target_user": "root",
  "failed_count": 42,
  "window": "10m",
  "first_seen": "2026-01-01T11:50:00Z",
  "last_seen": "2026-01-01T12:00:00Z",
  "evidence": ["auth.log:1234 Failed password...", "..."],
  "severity": "HIGH"
}
```

### scan — 端口扫描 / Web 扫描检测

| 参数 | 默认 |
|------|------|
| `port_threshold` | 10 | 同一 IP 在 `window` 内访问不同端口数 |
| `web_scan_patterns` | 见下 | Web 扫描特征 |

**端口扫描**: 同一 IP 短时间访问大量不同端口（基于 syslog 连接拒绝记录或 auditd）。

**Web 扫描模式**（nginx/apache access.log）:
- 路径包含: `/.env`, `/.git/`, `/wp-admin`, `/phpmyadmin`, `/%3Cscript`, `/etc/passwd`
- User-Agent: `sqlmap`, `nikto`, `nmap`, `masscan`, `dirbuster`, `gobuster`
- 大量 404 响应（同一 IP 在 window 内 > 20 个 404）

**输出事件**: `type=port_scan` 或 `type=web_scan`，含 `source_ip`、`hit_count`、`patterns_matched`。

### anomaly — 异常登录检测

| 规则 | 说明 | 严重度 |
|------|------|--------|
| 非工作时间登录 | 默认 22:00-06:00（可配置） | MEDIUM |
| 新地理位置登录 | 与历史登录 IP 段差异大（需历史基线） | MEDIUM |
| 首次出现 IP 登录成功 | 历史未见过的 IP 成功登录 | LOW |
| root 直接登录成功 | `Accepted password/key for root` | HIGH |
| 用户提权异常 | 短时间多次 `sudo` / `su root` 失败后成功 | HIGH |

**历史基线**: 首次运行无基线时，标注 `baseline_unavailable`，仅做规则匹配不做异常比对；后续运行以历史成功登录 IP 集为基线。

### login — 登录成功事件汇总

汇总 `window` 内所有成功登录事件，供人工复核。不视为告警，`severity=INFO`。

## 严重度映射

| 事件 | 严重度 |
|------|--------|
| 暴力破解（超阈值） | HIGH |
| 端口扫描 | MEDIUM |
| Web 扫描（含注入尝试） | HIGH |
| root 直接登录成功 | HIGH |
| 非工作时间登录 | MEDIUM |
| 提权异常 | HIGH |
| 首次 IP 登录 | LOW |

## 输出格式

```json
{
  "window": "24h",
  "from": "2026-01-01T00:00:00Z",
  "to": "2026-01-02T00:00:00Z",
  "rules_run": ["brute-force", "scan", "anomaly"],
  "logs_analyzed": ["/var/log/auth.log"],
  "logs_unavailable": ["/var/log/audit/audit.log"],
  "events": [/* 见上 */],
  "summary": {"total": 7, "high": 3, "medium": 3, "low": 1}
}
```

## 约束

- 只读取日志文件，不修改任何系统状态
- 大日志文件按 `window` 时间范围过滤后分析，不全量加载
- `evidence` 最多保留 5 条代表性日志行，避免输出膨胀
- IP 地址为日志中真实记录，不做地理定位（避免外部依赖）
