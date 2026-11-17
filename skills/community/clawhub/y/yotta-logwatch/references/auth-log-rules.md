# auth 日志检测规则（元察 · 元）

分析 /var/log/auth.log、/var/log/secure、journal 中 sshd / login / sudo 等认证日志。本文件说明元察的 auth 检测规则与阈值，供人工复核与调参。

## 输入形态

典型行（syslog）：

```
Jan  5 12:00:01 host sshd[100]: Failed password for root from 203.0.113.5 port 50000 ssh2
Jan  5 12:00:04 host sshd[103]: Accepted password for root from 203.0.113.5 port 50003 ssh2
Jan  5 12:00:05 host sudo: root : TTY=pts/0 ; USER=root ; COMMAND=/bin/bash
```

引擎自动识别 `Failed password` / `authentication failure` 为失败登录，`Accepted password` / `Accepted publickey` 为成功登录，`sudo:` + `COMMAND=` / `not in sudoers` 为 sudo 事件。来源 IP 从 `from <ip>` 提取。

## 检测规则

| 规则 | 触发条件 | 默认严重度 | 说明 / 复核建议 |
|---|---|---|---|
| brute_force | 同来源失败登录次数 >= `--max-fail`（默认 5），或在 `--window`（默认 300 秒）内达标 | low→high（次数越多越高） | 核实来源是否合法；临时封禁；确认是否存在弱口令账户 |
| credential_stuffing | 同来源在日志中尝试了 2 个及以上不同用户名 | high | 撞库 / 用户名枚举；启用来源限速与失败锁定 |
| abnormal_login | 同来源先失败后成功登录 | high | 爆破成功后接管；立即核查会话、重置密码 |
| root_login | 以 root 身份直接登录 | medium | 若来源非预期应重点核查；改用受限账户 + sudo |
| sudo_escalation | `sudo:` + `COMMAND=` / `session opened for user` | medium | 核对执行者与命令；确保 sudoers 最小化授权 |
| sudo_attempt | `sudo:` + `not in sudoers` | high | 越权尝试；横向移动 / 提权迹象；核查来源与 sudoers |
| invalid_user | 出现 `invalid user` | medium | 对不存在的账户发起登录；用户名枚举前兆 |

## 阈值与调参

- `--max-fail`：同来源失败登录计数阈值。调低更敏感（易误报），调高更稳健。
- `--window`：聚合时间窗（秒）。用于判断一定时间内连续失败；日志没有时间时会退化为按来源全量计数。

## 复核建议

- 判定「爆破」前，先核对来源是否为公司 / 合法运维跳板、是否被误报；
- 异常登录（failed→success）优先级最高，优先排查该来源后续行为；
- sudo 事件应结合执行者身份、命令内容、时间与业务合理性能否解释。