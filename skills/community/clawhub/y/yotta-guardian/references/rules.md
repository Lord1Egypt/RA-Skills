
# 规则目录（yotta-guardian）

> 本文件说明元盾的规则分层与内置规则清单。规则数据在 scripts/guardian_rules.py，匹配逻辑在 scripts/yotta_guardian.py。

## 一、规则分层

| 层 | 作用于 | 说明 |
|---|---|---|
| 文本模式 | exec 命令 / write 内容 | 正则匹配危险形态（下载即执行、编码执行、反向 shell、向系统文件追加内容等） |
| argv 级 | exec / run / shell | 先做包装解包（shell `-c` / `cmd /c` / `powershell -Command` / sudo / env / nohup / timeout 等，深度上限 3），再按「动词 + 标志 + 目标」分析（递归删除、格式化设备、提权、防火墙、服务、持久化等） |
| 敏感路径 | write / edit / read | 目标路径规范化后按系统核心 / 用户敏感 / 越界分级 |
| 放行规则 | 命令 / 路径 | 命中则高危可降级为警告（critical 不受影响） |

## 二、文本模式规则（TEXT_PATTERNS）

| 规则号 | 严重级 | 作用域 | 说明 |
|---|---|---|---|
| CMD-PIPE-SHELL | critical | both | curl 下载内容通过管道交给 shell 执行 |
| CMD-PIPE-WGET | critical | both | wget 下载内容通过管道交给 shell 执行 |
| CMD-PS-ENCODED | critical | both | PowerShell 编码命令执行 |
| CMD-B64-EXEC | critical | both | 解码后执行编码内容 |
| CMD-REV-BASH | critical | both | bash /dev/tcp 反向 shell |
| CMD-REV-NC | critical | both | netcat 反向 shell（-e 参数） |
| CMD-CHMOD-SETID | high | both | chmod 设置 setuid / setgid / sticky 权限位（4 位特殊位形态） |
| CMD-CHMOD-777 | high | both | chmod 设置全权限位 |
| CMD-SUDOERS-ECHO | critical | both | 向 sudoers 写入内容（提权持久化） |
| CMD-PASSWD-FILE | critical | both | 向 passwd 写入内容（账户持久化） |
| CMD-SSH-EXFIL | high | command | 读取 SSH 私钥后外传 |
| CTX-PRIVKEY | high | content | 写入私钥材料 |
| CTX-SECRET-TOKEN | medium | content | 写入疑似密钥 / 令牌 |

作用域说明：both = 命令与内容都扫；command = 仅命令文本；content = 仅写入内容。

## 三、argv 级规则（按动词分组，匹配逻辑在引擎）

| 规则号 | 严重级 | 触发示例（动词形态） |
|---|---|---|
| ARG-RM-SYSTEM | critical | 递归删除系统关键路径（/、/etc、/usr、/home、/boot、/dev、/var、C: 等） |
| ARG-RM-SYS-SUB | high | 递归删除系统目录下路径（如 /var 之下） |
| ARG-RM-ABS | high | 递归删除项目外绝对路径 |
| ARG-RM-REL | medium | 递归删除相对路径目标 |
| ARG-FMT-DEVICE | critical | 格式化块设备 / 磁盘（/dev/sd*、C:） |
| ARG-FMT-TARGET | high | 格式化其他目标 |
| ARG-DD-DEVICE | critical | dd 直接写入块设备 / 磁盘 |
| ARG-DD-FILE | high | dd 写入磁盘镜像目标 |
| ARG-POWER | high | 系统电源 / 重启操作 |
| ARG-CHMOD-777 | high/critical | chmod 设置全权限位（对系统关键路径为 critical） |
| ARG-CHMOD-SETID | high | chmod 设置 setuid / setgid / sticky |
| ARG-CHOWN-SYSTEM | critical | chown 修改系统关键路径属主 |
| ARG-CHOWN-REC | medium | 递归修改文件属主 |
| ARG-PRIV-ACCOUNT | high | 账户管理（useradd / userdel / groupadd 等） |
| ARG-PRIV-GROUP | high | 把用户加入管理员组 |
| ARG-PRIV-PASSWD | high | 修改账户口令 |
| ARG-PRIV-SU | medium | 切换用户身份 |
| ARG-PRIV-SUDOERS | high | 编辑 sudoers |
| ARG-PRIV-NET | high | 把用户加入 Windows 管理员组 |
| ARG-FW-FLUSH | high | 清空防火墙规则 |
| ARG-FW-UFW | high | 禁用 / 重置防火墙 |
| ARG-FW-NETSH | high | 关闭 Windows 防火墙 |
| ARG-FW-CHANGE | medium | 修改防火墙规则 |
| ARG-SVC-STOP | medium | 停止 / 禁用系统服务 |
| ARG-SVC-START | medium | 启用系统服务 |
| ARG-SVC-SC | high | 删除 / 停止 Windows 服务 |
| ARG-CRON | high | 修改 / 删除 crontab（持久化） |
| ARG-REG-RUN | high | 修改注册表启动项 |
| ARG-REG | medium | 修改注册表 |
| ARG-SCHTASKS | high | 创建 / 修改计划任务（持久化） |
| ARG-REV-NC | critical | netcat 反向 shell |
| ARG-REV-SOCAT | critical | socat 执行远程命令（反向 shell） |
| ARG-PS-ENCODED | critical | PowerShell 编码命令执行 |

## 四、敏感路径规则（PATH_PATTERNS）

| 规则号 | 严重级 | 说明 |
|---|---|---|
| PATH-ETC-CORE | critical | 写入系统核心配置文件（passwd / shadow / sudoers / group / fstab / hosts 等） |
| PATH-ETC-ADMIN | critical | 写入系统管理目录（sudoers.d / cron.d / systemd / init.d / rc.d） |
| PATH-BOOT | critical | 写入 /boot 启动分区 |
| PATH-DEVICE | critical | 直接写入块设备 |
| PATH-PROC-SYS | critical | 写入 /proc 或 /sys 内核接口 |
| PATH-WIN-CONFIG | critical | 写入 Windows 注册表配置库（system32\\config） |
| PATH-WIN-HOSTS | critical | 写入 Windows hosts 文件 |
| PATH-WIN-BOOT | critical | 写入 Windows 启动文件 |
| PATH-ETC-ANY | high | 写入 /etc 任意位置 |
| PATH-SSH-AUTH | high | 写入 SSH 授权 / 私钥文件 |
| PATH-RC-FILES | high | 写入 shell / 凭据配置文件（bashrc / zshrc / profile / netrc / gitconfig / npmrc 等） |
| PATH-AWS-CRED | high | 写入云服务凭据文件 |
| PATH-CRON-SPOOL | high | 写入 cron 任务队列 |
| PATH-WIN-SYS32 | high | 写入 Windows 系统目录 |
| PATH-STARTUP | high | 写入系统启动项目录 |
| PATH-SECRET-FILE | medium | 写入疑似凭据 / 密钥文件（.env / pem / key 等） |

引擎另有一条通用规则 OUT-001（medium）：写入当前工作目录之外的目标。

## 五、放行规则

- 默认放行模式（ALLOW_PATTERNS）：明确安全的只读 / 查询命令前缀（ls / git status / 版本查询等），命中后高危可降级为警告。
- 命令行放行：--allow "模式"（命令正则，可重复）、--allow-path "路径"（写路径前缀，可重复）。
- critical 规则**不可**被放行规则覆盖（需人工确认后换用更低风险方案或 loose 策略仍会拒绝）。

## 六、自定义规则文件（--config）

```json
{
  "policy": "default",
  "allow": ["^git "],
  "allow_paths": ["./tmp"],
  "deny": ["^evil"],
  "verifier": { "command": ["python3", "/path/verifier.py"], "timeout": 30 }
}
```

- policy: default / strict / loose
- allow: 命令正则放行模式
- allow_paths: 写路径放行前缀
- deny: 自定义拒绝模式（命中记 CFG-DENY，严重级 high）
- verifier: 意图验证器配置（heuristic: true 或 command 数组），见 intent-verifier.md
