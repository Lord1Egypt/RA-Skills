---
name: srv-guard
description: |-
  服务器安全防护一体化能力：扫描漏洞、修复漏洞、感知攻击、防御攻击，并生成安全报告。
  当需要对 Linux 服务器进行安全加固、漏洞巡检、入侵检测或应急防御时加载此 Skill。
  触发词：服务器安全、漏洞扫描、漏洞修复、攻击感知、入侵检测、安全加固、封禁 IP。
  English triggers: server security hardening, vulnerability scan, patch/audit Linux config,
  intrusion detection, brute-force log analysis, block malicious IP, security report.
allowed-tools: Bash(python:*) Bash(ssh:*) Bash(sudo:*) read write edit glob grep
---

# server-security-guard — 服务器安全防护

> 防御性安全加固 Skill。在已获授权的服务器上执行漏洞巡检、自动修复、攻击感知与应急防御，输出可审计的安全报告。

## 核心原则

1. **仅防御用途** — 只对已获书面授权的服务器执行安全加固。禁止用于未授权系统、禁止植入后门、禁止开发攻击载荷。
2. **默认安全（dry-run）** — 修复与防御脚本默认 `--dry-run`，仅打印将执行的操作；需显式 `--apply` 才真正改动系统。
3. **最小副作用** — 改动范围最小化，写前检查目标状态，高风险操作可回滚，所有变更写入审计日志。
4. **能力边界诚实** — 扫描覆盖常见配置类漏洞，不声称替代专业 CVE 数据库或商业 IDS；修复只自动处理可安全自动化的项。
5. **Agent 判断 + 脚本执行** — Agent 负责理解上下文、权衡风险、决定修复策略；脚本负责确定性扫描、执行与校验。

## 工作流

### Phase 1: 漏洞扫描（只读）

```text
输入: 目标服务器（本地或 SSH）、扫描范围
执行: python scripts/vuln_scan.py --target <local|ssh://user@host> [--scope all|config|service|port|patch|ssh]
输出: scan-result.json（漏洞清单 + 严重度 + 证据）
```

扫描项见 `references/scan-checklist.md`。脚本检测目标系统工具可用性并优雅降级。

### Phase 2: 漏洞修复（默认 dry-run）

```text
输入: scan-result.json 或指定修复项
执行: python scripts/vuln_fix.py --target <local|ssh://user@host> --input scan-result.json [--apply] [--items item1,item2]
输出: fix-result.json（每项修复: 成功/失败/回滚信息）
```

修复手册见 `references/fix-playbook.md`。默认 dry-run（不传 `--apply` 即只打印不执行）。破坏性操作先备份。

输出状态：`fixed`（已改）/ `would_fix`（dry-run 下将要执行，尚未改）/ `skipped`（不可自动修复）/ `failed`。dry-run 绝不报告 `fixed`。

`--apply` 但目标用户非 root 时：脚本**拒绝执行**，退出码 3，输出 `status: requires_privilege` 且 `results` 为空——不会静默降级成 dry-run，调用方应视为“未修复”。

### Phase 3: 攻击感知（日志分析）

```text
输入: 目标服务器、时间窗口、检测规则集
执行: python scripts/attack_monitor.py --target <...> --window 24h [--rules brute-force,scan,anomaly]
输出: monitor-result.json（告警事件 + 来源 IP + 证据日志行）
```

攻击特征与检测规则见 `references/attack-signatures.md`。只读取日志，不修改系统。

### Phase 4: 攻击防御（默认 dry-run）

```text
输入: monitor-result.json 或指定恶意 IP/事件
执行: python scripts/attack_defend.py --target <local|ssh://user@host> --input monitor-result.json [--apply] [--action block|harden|alert] [--block-threshold high|medium] [--ips ip1,ip2]
输出: defend-result.json（封禁/加固操作记录 + 回滚命令）
```

防御策略见 `references/defense-strategies.md`。默认 dry-run（不传 `--apply` 即只打印不执行）。封禁操作生成回滚命令，便于误封后恢复。

- `--action block`：按严重度阈值封禁来源 IP；白名单支持任意前缀长度 CIDR（`/24`、`/32`、`::/0` 等），非法条目跳过。dry-run 下状态为 `would_block`（尚未封禁）。
- `--action harden`：改 sshd_config（禁用空口令 / root 密码登录）与 4 项内核参数；改配置前先备份，全部操作带回滚命令。状态区分 `ok` / `partial`（部分成功）/ `failed` / `would_harden`（dry-run）/ `no_candidates`，并附 `applied_count`、`failed_count`、`warnings`。

### Phase 5: 安全报告

```text
执行: python scripts/security_report.py --scan scan-result.json [--fix fix-result.json] [--monitor monitor-result.json] [--defend defend-result.json] --output report.html
输出: report.html（基于 assets/report-template.html 生成）
```

## 决策规则

| 任务类型 | 执行方式 |
|----------|----------|
| 仅了解安全状况 | Phase 1 + Phase 5（只读扫描 + 报告） |
| 扫描并修复 | Phase 1 → 2 → 5，修复前人工确认 dry-run 输出 |
| 持续监控攻击 | Phase 3 定时执行 + Phase 5，可结合 cron |
| 应急响应攻击 | Phase 3 → 4 → 5，防御前人工确认封禁列表 |
| 全面安全加固 | Phase 1 → 2 → 3 → 4 → 5，逐阶段确认 |

## 脚本

| 脚本 | 用途 | 默认模式 |
|------|------|----------|
| `scripts/vuln_scan.py` | 漏洞扫描 | 只读 |
| `scripts/vuln_fix.py` | 漏洞修复 | dry-run |
| `scripts/attack_monitor.py` | 攻击感知 | 只读 |
| `scripts/attack_defend.py` | 攻击防御 | dry-run |
| `scripts/security_report.py` | 生成 HTML 报告 | 只读 |
| `scripts/web_ui.py` | 本机网页端扫描、dry-run 预览、确认后修复 | 默认只预览；用户二次确认后才执行 |

所有脚本：基于自身文件位置解析 Skill 内资源（不依赖 cwd）、UTF-8 编码、JSON 输出到 stdout、进度/错误到 stderr、非零退出码表示失败、支持 `--help`。

### 网页端一键修复（HTTPS，仅本机）

```bash
python scripts/web_ui.py                     # 默认 https://127.0.0.1:8765
python scripts/web_ui.py --port 9000         # 自定义本机端口
python scripts/web_ui.py --cert c.crt --key c.key   # 使用自有证书
python scripts/web_ui.py --no-tls            # 退回 HTTP（不推荐，仅调试）
```

**HTTPS 默认开启**：

- 首次启动自动生成自签名证书（SAN 覆盖 `127.0.0.1`、`::1`、`localhost`），存放在 `~/.server-security-guard/tls.crt` 与 `tls.key`（私钥 0600，目录 0700），可用 `SSG_STATE_DIR` 改位置；剩余有效期不足 7 天时自动重新生成。
- 生成优先用系统 `openssl`，缺失时回退 Python `cryptography`；两者都没有则报错并提示用 `--cert/--key`。
- 最低 TLS 1.2（实测协商 TLS 1.3，TLS 1.1 被拒）；同一端口明文 HTTP 请求会被直接断开，不存在明文监听。
- 浏览器会提示自签名证书不受信任——确认指纹后继续即可；若系统走了 HTTP 代理，请把 `127.0.0.1` 加入代理例外，否则代理会返回 502。
- `--no-tls` 会打印显式警告：令牌与 sudo 密码将以明文经过回环。

打开启动时打印的本机 URL。界面流程：扫描 → 选择支持自动修复的项目 → 查看 dry-run 命令 → 点击确认并输入 `APPLY` → 执行。

安全设计要点：

- 只绑定 loopback（`127.0.0.1`/`localhost`/`::1`），启动参数拒绝非 loopback 地址；不要通过反向代理/端口转发暴露到网络。
- 页面 token 每次启动随机生成，放在 URL fragment（不发送给服务端、不进访问日志）；API 使用 bearer token；Host/Origin 均按 authority 解析校验（支持 `[::1]:port` 形式）。
- **预览绑定**：`/api/preview` 返回一次性 `confirm_token`（默认 5 分钟有效），服务端把目标 + 所选项目 + 每步命令/回滚压成摘要保存；`/api/apply` 必须带上该令牌，且会重新生成预览比对摘要，不一致（计划或系统状态变化）、过期、或重复使用都会被拒绝。仅凭 `APPLY` 三个字母不足以执行。
- 并发上限 2，超出返回 429；扫描会话 30 分钟过期。
- 目标非 root 时 apply 返回 409 + `status: requires_privilege`，页面明确显示未做任何变更。

**管理员权限（可选勾选）**：

- 勾选「以管理员权限修复」后必须填写 sudo 密码；**仅 `local` 目标可用**，远程主机请改用 root 登录或已配置 `NOPASSWD` 的 sudo 账号。
- 密码只在本次请求内使用：经 loopback 传输，作为 stdin 传给 `sudo -S -p '' --`，**不进 argv、不进环境变量、不写日志/审计/会话、不落盘**，用后从页面输入框清除。
- 连续 3 次密码错误锁定 5 分钟（返回 401）；本机没有 `sudo` 命令时直接报错，不会静默降级。
- 提权路径下 preview 与 apply 都走 sudo，保证「预览看到的命令」与「实际执行」一致（否则摘要校验会拒绝）。
- 更安全的替代方案：直接用 root 启动 `sudo python scripts/web_ui.py`，全程不传输密码。

这个“一键”是**确认后执行**，不会绕过 dry-run 或人工确认。UI 调用原有 `vuln_fix.py`，不新增修复能力；当前仅支持自动修复列表中的项目，其余仍需人工处理。仅对有授权的主机使用。

## 资源导航

| 资源 | 路径 | 用途 |
|------|------|------|
| 扫描清单 | `references/scan-checklist.md` | 扫描项、判断标准、严重度分级 |
| 修复手册 | `references/fix-playbook.md` | 每类漏洞的修复步骤、风险评估、回滚方法 |
| 攻击特征 | `references/attack-signatures.md` | 检测规则、日志来源、阈值 |
| 防御策略 | `references/defense-strategies.md` | 封禁/加固策略、防火墙操作、回滚 |
| 报告模板 | `assets/report-template.html` | HTML 报告模板 |
| Linux 全链路自测 | `tests/linux_e2e.sh` | 真实 Linux 上验证扫描/修复/回滚/报告/HTTPS，用法见 `tests/README.md` |
| Linux 补充测试 | `tests/linux_extra.sh` | 网页端 sudo 提权真实 apply + iptables 真实封禁/回滚 |

### 已知覆盖边界（勿超范围承诺）

`references/scan-checklist.md` 与 `references/fix-playbook.md` 描述的是完整检查/修复清单，脚本尚未全部实现自动化。当前情况：

- **扫描已实现**：CFG-01~09、SVC-01/02/04/05/06、PRT-01、PCH-01/02
- **扫描未实现**（清单有、脚本无，需人工核查）：CFG-10、SVC-03、PRT-02、PRT-03、PCH-03、SSH-06、SSH-07
- **自动修复已实现**：CFG-01、CFG-02、CFG-03、CFG-06、CFG-07、SVC-01
- **仅能人工修复**（脚本会记为 `skipped` 并说明）：CFG-04/09、SVC-04/06、PCH-01/03 等

向用户汇报时必须区分"已扫描/未扫描"与"已修复/需人工"，不得把清单条目当作已覆盖能力。

> **验证状态**：已在 **Ubuntu 22.04.5 LTS（内核 6.8）真实虚拟机**上验证：
> - `tests/linux_e2e.sh` 33 项全过：扫描命中 CFG-01/02/03/05/06/08、PCH-01/02；dry-run `would_fix`；`--apply` 真实改 sshd_config；备份=改动前快照；回滚逐字节一致；检出暴力破解；封禁/加固 dry-run；报告无占位符；HTTPS + 拒绝 TLS1.1；运行后无残留（备份/规则/配置均复原）
> - `tests/linux_extra.sh` 10 项全过：网页端 sudo 提权真实 apply（`elevated: true`，文件确实被改）、iptables 真实封禁 + `--rollback` 后规则移除
> - **远程 `ssh://` 目标已真实联通**（Windows → Ubuntu VM，密钥认证）：扫描 53 项发现、CFG-06 系统路径均标为不可自动修复、注入日志检出暴力破解（198.51.100.77，13 次）、dry-run 带回滚命令、封禁 dry-run 识别 iptables 后端
> - Windows 侧另有 7 个单元/集成套件（备份语义、状态语义、确认令牌、伪 sudo、TLS 等）
> - 仍未验证：`harden --apply` 真实执行、远程目标的 `--apply`（需 root 登录）、网页端在真实浏览器里的交互

## 安全约束

以下操作**禁止**：
- 对未获书面授权的服务器执行任何操作
- 植入后门、rootkit、持久化恶意载荷
- 开发攻击工具、生成漏洞利用代码
- 在脚本中硬编码凭证、密钥、目标 IP
- 跳过 dry-run 直接对生产服务器 `--apply` 而无人工确认
- 删除与安全加固无关的文件

以下操作**优先**：
- 修复/防御前先 dry-run 并由人工确认
- 破坏性操作前备份原配置
- 所有变更写入审计日志（`/var/log/security-guard-audit.log`）
- 封禁操作同时生成回滚命令
- 扫描结果包含证据（具体配置项/日志行），便于人工复核

## 权限说明

- 扫描与监控：普通用户可读取的日志/配置即可；部分项需 root（脚本会标注并跳过）
- 修复与防御：需 root/sudo。脚本检测权限不足时明确提示，不静默跳过
- SSH 远程：通过 `ssh` 执行，需已配置免密或使用 ssh-agent，不在脚本中存储密码
