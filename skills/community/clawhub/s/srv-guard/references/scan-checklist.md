# 漏洞扫描清单

> `vuln_scan.py` 的扫描项定义、判断标准与严重度分级。所有扫描项均为只读检测。

## 严重度分级

| 级别 | 含义 | 示例 |
|------|------|------|
| CRITICAL | 可被远程利用获取初始访问或提权 | SSH 允许 root 登录 + 弱口令、对外开放的未授权服务 |
| HIGH | 显著扩大攻击面或泄露敏感信息 | 过期未打补丁的高危软件、全局可读的私钥文件 |
| MEDIUM | 配置不当，结合其他漏洞可被利用 | 密码策略过弱、不必要服务运行、SSH 允许密码登录 |
| LOW | 加固建议，单独难以直接利用 | 未设置 banner、默认端口未改（信息泄露类） |
| INFO | 信息性发现 | 已安装软件清单、开放端口列表 |

## 扫描范围（--scope）

> **状态标记**：✅ 已实现 | ⏳ 规划中（当前版本不输出）

### config — 配置类

| ID | 检测项 | 判断标准 | 严重度 | 状态 |
|----|--------|----------|--------|------|
| CFG-01 | SSH PermitRootLogin | `PermitRootLogin yes` → HIGH | HIGH | ✅ |
| CFG-02 | SSH PasswordAuthentication | `PasswordAuthentication yes` → MEDIUM | MEDIUM | ✅ |
| CFG-03 | SSH PermitEmptyPasswords | `PermitEmptyPasswords yes` → CRITICAL | CRITICAL | ✅ |
| CFG-04 | SSH 协议版本 | `Protocol 1` → CRITICAL | CRITICAL | ⏳ |
| CFG-05 | SSH MaxAuthTries | > 6 → LOW（暴力破解容忍度高） | LOW | ⏳ |
| CFG-06 | 全局可读私钥 | `*.pem`/`id_rsa` 权限 > 0600 → HIGH | HIGH | ✅ |
| CFG-07 | /etc/passwd 空口令字段 | 第二字段为空 → CRITICAL | CRITICAL | ✅ |
| CFG-08 | sudo 免密配置 | `NOPASSWD` 用于高风险命令 → HIGH | HIGH | ✅ |
| CFG-09 | 文件权限 | `/etc/shadow` 非 0640 → HIGH | HIGH | ⏳ |
| CFG-10 | umask | 默认 umask > 022 → LOW | LOW | ⏳ |

### service — 服务类

| ID | 检测项 | 判断标准 | 严重度 | 状态 |
|----|--------|----------|--------|------|
| SVC-01 | 不必要服务运行 | telnet/rsh/rlogin/tftp → CRITICAL；ftp → HIGH | CRITICAL/HIGH | ✅ |
| SVC-02 | 对外开放高危端口 | 23/21/3389 对 0.0.0.0 监听 → HIGH | HIGH | ⏳ |
| SVC-03 | 未使用的服务自启 | enabled 且非必要 → MEDIUM | MEDIUM | ⏳ |
| SVC-04 | Docker daemon 无 TLS | 2375 对外开放（无 TLS）→ CRITICAL | CRITICAL | ⏳ |
| SVC-05 | 数据库对外暴露 | 3306/5432/27017 对 0.0.0.0 → HIGH | HIGH | ⏳ |
| SVC-06 | Redis 无认证 | 6379 对外 + 无 requirepass → CRITICAL | CRITICAL | ⏳ |

### port — 端口类

| ID | 检测项 | 判断标准 | 严重度 | 状态 |
|----|--------|----------|--------|------|
| PRT-01 | 监听地址 | 非 127.0.0.1/::1 的监听 → INFO（需人工判断） | INFO | ✅ |
| PRT-02 | 知名高危端口 | 见 SVC-02 | HIGH | ⏳ |
| PRT-03 | 端口与进程映射 | 无法关联进程的监听端口 → MEDIUM | MEDIUM | ⏳ |

### patch — 补丁类

| ID | 检测项 | 判断标准 | 严重度 | 状态 |
|----|--------|----------|--------|------|
| PCH-01 | 可用安全更新 | apt/yum 可升级的安全包数量 > 0 → HIGH | HIGH | ✅ |
| PCH-02 | 内核版本 | 运行内核与已安装最新内核不一致 → MEDIUM（需重启） | MEDIUM | ⏳ |
| PCH-03 | 已知高危软件版本 | bash Shellshock、sudo CVE-2021-3156 等 → CRITICAL | CRITICAL | ⏳ |

### ssh — SSH 专项（config 子集，独立便于 --scope ssh）

见 CFG-01 ~ CFG-05。额外：

| ID | 检测项 | 判断标准 | 严重度 | 状态 |
|----|--------|----------|--------|------|
| SSH-06 | authorized_keys 权限 | > 0600 → MEDIUM | MEDIUM | ⏳ |
| SSH-07 | 弱主机密钥 | ssh-rsa/ssh-dss → MEDIUM | MEDIUM | ⏳ |

## 输出格式

每个发现包含：

```json
{
  "id": "CFG-01",
  "title": "SSH PermitRootLogin 已启用",
  "severity": "HIGH",
  "scope": "config",
  "evidence": "文件 /etc/ssh/sshd_config 第 32 行: PermitRootLogin yes",
  "remediation_ref": "fix-playbook.md#cfg-01",
  "auto_fixable": true
}
```

`evidence` 必须指向真实配置项/文件/命令输出，便于人工复核。`auto_fixable=false` 的项需人工判断（如业务必需的服务）。

## 优雅降级

- 目标无 `systemctl` → 用 `service`/`chkconfig` 回退
- 目标无 `apt` → 用 `yum`/`dnf` 回退
- 无权限读取某文件 → 标注 `permission_required` 并跳过，不中断整体扫描
- SSH 连接失败 → 明确报错，不伪造结果
