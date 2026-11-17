# 防御策略

> `attack_defend.py` 的封禁/加固策略、防火墙操作与回滚。默认 dry-run。

## 防御动作（--action）

### block — 封禁恶意 IP

**输入**: monitor-result.json 中的事件，或 `--ips` 显式指定。

**封禁策略**:

| 后端 | 检测顺序 | 封禁命令 | 回滚命令 |
|------|----------|----------|----------|
| firewalld | `systemctl is-active firewalld` | `firewall-cmd --add-source=<ip> --zone=drop --permanent` | `firewall-cmd --remove-source=<ip> --zone=drop --permanent` |
| ufw | `which ufw` | `ufw deny from <ip>` | `ufw delete deny from <ip>` |
| iptables | `which iptables` | `iptables -I INPUT -s <ip> -j DROP` | `iptables -D INPUT -s <ip> -j DROP` |
| nftables | `which nft` | `nft add rule inet filter input ip saddr <ip> drop` | `nft delete rule ...` |

按顺序检测第一个可用的后端。无可用后端 → 报错，不伪造成功。

**封禁阈值**: 默认仅封禁 `severity >= HIGH` 事件的来源 IP；`--block-threshold medium` 可放宽。

**白名单保护**: `--whitelist` 指定的 IP/网段永不封禁（防止误封管理员/内网）。默认白名单: `127.0.0.0/8`, `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`（可覆盖）。

白名单支持任意前缀长度的 IPv4/IPv6 CIDR（`/24`、`/25`、`/32`、`2001:db8::/32`）与裸单 IP；非法条目直接跳过，不会因为写错网段而误封。

**输出**:
```json
{
  "action": "block",
  "backend": "iptables",
  "blocked_ips": [{"ip": "203.0.113.5", "reason": "brute_force", "event_id": "evt-001"}],
  "skipped_ips": [{"ip": "10.0.0.5", "reason": "in_whitelist"}],
  "rollback_commands": ["iptables -D INPUT -s 203.0.113.5 -j DROP"],
  "dry_run": true
}
```

### harden — 加固配置

`attack_defend.py --action harden` 自身实现的低风险加固（不依赖 monitor 结果，也不调用 `vuln_fix.py`）。与 block 区别: harden 改配置/内核参数，block 改防火墙。

实际执行的 4 类操作:

| 操作 | 命令要点 | 回滚 |
|------|----------|------|
| `ssh_no_empty_pass` | `PermitEmptyPasswords yes` → `no`，reload sshd | 从备份 `cp` 回并 reload |
| `ssh_no_root_password` | `PermitRootLogin yes` → `prohibit-password`（仍允许密钥登录） | 从备份 `cp` 回并 reload |
| `sysctl_no_redirect` ×2 | `net.ipv4.conf.{all,default}.accept_redirects=0` | `sysctl -w ...=1` |
| `sysctl_no_source_route` ×2 | `net.ipv4.conf.{all,default}.accept_source_route=0` | `sysctl -w ...=1` |

安全约束:
- 改 `sshd_config` 前先 `cp -a` 备份为 `/etc/ssh/sshd_config.guard-bak.<时间戳>`；备份失败则不执行 SSH 类加固（其余内核参数仍按原逻辑尝试），结果状态会如实标记。
- reload 走 `systemctl reload sshd || ssh || openssh-server` 兼容链，Debian 与 RHEL 服务名差异不会导致失败。
- 只改显式 `yes` 的行；配置缺失时不新增指令。
- 仅 `sysctl -w` 临时生效，重启后失效——需持久化请人工追加到 `/etc/sysctl.d/`。

**状态与回滚（诚实优先）**:

| 字段 | 含义 |
|------|------|
| `status` | `ok` 全部生效 / `partial` 部分生效 / `failed` 全部失败 / `would_harden` dry-run 未改 / `no_candidates` 无需加固 |
| `applied_count` / `failed_count` | 实际生效与失败的步数，`partial` 时必须一起看 |
| `rollback_commands` | **只为实际生效的操作生成**：备份还原仅在确实写入过 sshd_config 后出现；sysctl 回滚使用执行前读取的原值（原值读取失败则不给该条回滚，改在 `warnings` 里要求人工核对） |
| `warnings` | 原值未知、单步失败、备份失败等需要人工注意的情况 |

`do_block` 同理：dry-run 下 `status` 为 `would_block`，不代表已封禁。

**不自动执行**: 软件升级、服务禁用、锁定账户、改私钥权限（这些走 `vuln_fix.py --items`，需人工确认）。

### alert — 仅告警不处置

生成告警记录到 `/var/log/security-guard-audit.log`，不封禁不加固。用于需要人工研判的场景。

## 审计日志

所有防御操作（无论 dry-run 或 apply）写入审计日志:

```
[2026-01-01T12:00:00Z] ACTION=block IP=203.0.113.5 REASON=brute_force DRY_RUN=true BY=server-security-guard
[2026-01-01T12:01:00Z] ACTION=block IP=203.0.113.5 REASON=brute_force DRY_RUN=false APPLIED=true BY=server-security-guard
```

日志路径: `/var/log/security-guard-audit.log`（需 root 创建；无权限则降级到脚本运行目录的 `security-guard-audit.log` 并标注）。

## 回滚

每个 apply 操作在 defend-result.json 中记录 `rollback_commands`。脚本支持:

```bash
python scripts/attack_defend.py --rollback defend-result.json --apply
```

按记录的回滚命令逆序执行，恢复封禁/加固。回滚本身也写审计日志。

## 安全约束

- **永不封禁白名单 IP**，即使显式 `--ips` 指定也拒绝并告警（白名单匹配基于单个 IP 地址）
- **apply 模式无交互确认**：脚本不弹确认、也没有 `--yes` 跳过开关。工作流要求 Agent 必须先跑 dry-run 并把封禁列表展示给人工确认，再执行 `--apply`
- **不做定时解封**：脚本没有 `--expire` 之类参数。需要限时封禁时，用 cron/systemd timer 到点执行 `attack_defend.py --rollback <defend-result.json> --apply`（回滚命令已记录在结果里）
- **封网段需谨慎**：`--ips` 不做网段校验，传入 CIDR 会原样交给防火墙后端（firewalld/ufw/iptables 都接受 CIDR），等于可能一次封掉整个网段——必须人工确认后再传

## 与 fail2ban 的关系

若目标已运行 fail2ban，`attack_monitor.py` 会读取 fail2ban 日志作为补充证据；`attack_defend.py` 的封禁与 fail2ban 并行（不冲突，iptables 规则独立）。建议: 持续防护优先用 fail2ban，本 Skill 用于一次性应急响应和加固。
