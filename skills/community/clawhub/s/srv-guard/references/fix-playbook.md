# 漏洞修复手册

> `vuln_fix.py` 的修复步骤、风险评估与回滚方法。每项修复对应 `scan-checklist.md` 的一个 ID。

## 修复原则

1. **默认 dry-run** — 打印将执行的命令，不改动系统

> **权限语义**：`--apply` 时若目标用户非 root，脚本**拒绝执行并以退出码 3 结束**，输出 `status: requires_privilege`（`results` 为空，`summary` 全零），不会静默降级为 dry-run。调用方必须把这种情况当作“未修复”处理。

> **dry-run 语义**：状态为 `would_fix`，消息带 `[DRY-RUN]` 前缀；`backup_files` 与 `rollback_commands` 给出**计划值**（备份路径形如 `<file>.guard-bak.<时间戳>`，`--apply` 时才真正创建）。因此预览阶段就能核对回滚手段。
2. **先备份** — 修改配置文件前复制到 `<file>.guard-bak.<timestamp>`
3. **可回滚** — 每项修复记录回滚命令，写入 fix-result.json
4. **不越界** — 只修复 `--items` 指定或 scan-result 中 `auto_fixable=true` 的项
5. **需重启的项标注** — 不自动重启，在结果中标注 `reboot_required`

## 修复项

> **状态标记**：✅ 已实现 | ⏳ 规划中（当前版本不输出）

### CFG-01: SSH PermitRootLogin ✅

- **风险**: 允许 root 直接 SSH 登录，爆破成功即获 root
- **修复**: `sshd_config` 中 `PermitRootLogin yes` → `PermitRootLogin no`，重载 sshd
- **命令**:
  ```bash
  sed -i 's/^PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
  systemctl reload sshd
  ```
- **回滚**: 恢复备份文件并 `systemctl reload sshd`
- **注意**: 确保有普通用户 sudo 权限，否则可能锁死 root 远程管理

### CFG-02: SSH PasswordAuthentication ✅

- **风险**: 允许密码登录，易遭暴力破解
- **修复**: `PasswordAuthentication yes` → `no`（前提: 已配置密钥登录）
- **前置检查**: 至少一个 `authorized_keys` 存在且非空，否则**拒绝修复**并告警
- **回滚**: 恢复备份

### CFG-03: SSH PermitEmptyPasswords ✅

- **风险**: 允许空口令登录
- **修复**: `PermitEmptyPasswords yes` → `no`
- **回滚**: 恢复备份

### CFG-04: SSH Protocol 1 ⏳

- **风险**: SSHv1 已知不安全
- **修复**: 删除或改为 `Protocol 2`（现代 OpenSSH 默认仅 v2，该行可删除）
- **回滚**: 恢复备份

### CFG-06: 私钥文件权限 ✅

- **修复**: `chmod 600 <keyfile>`
- **回滚**: 记录原权限并恢复

### CFG-07: /etc/passwd 空口令 ✅

- **风险**: 账户无密码即可登录
- **修复**: `passwd -l <user>` 锁定账户
- **回滚**: `passwd -u <user>`（需确认账户应有密码）
- **注意**: 不锁定系统必需账户（如 nobody）

### CFG-09: /etc/shadow 权限 ⏳

- **修复**: `chmod 640 /etc/shadow; chown root:shadow /etc/shadow`（Debian 系）或 `chmod 000`（RHEL 系）
- **回滚**: 记录原权限恢复

### SVC-01: 不必要服务 ✅

- **修复**: `systemctl stop <svc>; systemctl disable <svc>`
- **业务确认**: telnet/rsh/rlogin/tftp 直接禁用；ftp 需人工确认是否业务必需
- **回滚**: `systemctl enable --now <svc>`

### SVC-04: Docker daemon 无 TLS ⏳

- **修复**: 禁用 `tcp://0.0.0.0:2375`，仅保留 unix socket 或配置 TLS
- **注意**: 修改 `/etc/docker/daemon.json` 后需重启 docker，标注 `reboot_required=false, service_restart=docker`

### SVC-06: Redis 无认证 ⏳

- **修复**: `redis.conf` 设置 `requirepass`（生成随机强密码）+ `bind 127.0.0.1`
- **回滚**: 恢复 redis.conf
- **注意**: 需通知使用 Redis 的应用更新连接配置

### PCH-01: 安全更新 ⏳

- **修复**: `apt-get update && apt-get upgrade -y`（Debian）或 `yum update -y`（RHEL）
- **风险**: 更新可能影响业务兼容性，**默认不自动 apply**，dry-run 列出将升级的包
- **回滚**: 记录升级前版本，必要时手动降级（不保证自动回滚）
- **注意**: 标注 `reboot_required` 若包含内核更新

### PCH-03: 已知高危软件版本 ⏳

- **修复**: 针对特定 CVE 的包升级（如 `sudo` CVE-2021-3156 → 升级 sudo 包）
- **回滚**: 记录原版本

## 不自动修复的项

以下项 `auto_fixable=false`，仅报告，需人工处理：

- 业务必需的服务（ftp 等，需确认）
- 涉及业务连接配置变更的（如 Redis 加密码需应用配合）
- 内核版本不一致（需重启，由运维决定窗口）
- umask、banner 等低风险加固建议

## 输出格式

```json
{
  "item_id": "CFG-01",
  "status": "fixed|skipped|failed",
  "dry_run": true,
  "commands": ["sed -i ...", "systemctl reload sshd"],
  "backup_files": ["/etc/ssh/sshd_config.guard-bak.20260101_120000"],
  "rollback_commands": ["cp <bak> /etc/ssh/sshd_config", "systemctl reload sshd"],
  "reboot_required": false,
  "message": "已禁用 root SSH 登录"
}
```
