# 系统安全基线检查项说明

系统模式（--target system）按平台执行只读基线检查，全部为查询类命令，不修改任何配置。

## Windows 检查项

| 检查 | 命令（只读） | 关注点 |
|---|---|---|
| 注册表启动项 | reg query（Run / RunOnce / Wow6432Node） | 新增/异常启动项，指向临时目录者高危 |
| 计划任务 | schtasks /query | 非系统内置任务需人工确认 |
| 服务 | wmic service（wmic 不可用时降级 sc query） | 自动启动服务是否合理 |
| 防火墙 | netsh advfirewall show allprofiles state | 配置文件是否开启 |
| 共享目录 | net share | 非默认共享暴露面 |
| 管理员组成员 | net localgroup administrators | 成员是否最小化 |
| 持久化点 | reg query（登录脚本、全局注入点、环境变量） | 全局持久化点被修改即高危 |
| 浏览器凭据位置 | 路径存在性检查 | 仅提示位置，不扫描内容 |

## Linux 检查项

| 检查 | 命令（只读） | 关注点 |
|---|---|---|
| SUID/SGID 文件 | find -perm /6000 | 可写目录下的特权位文件高危 |
| 全局可写目录 | find -perm -0002 | 可被低权限用户劫持 |
| 启动项 | systemctl list-unit-files / cron 目录 | 启用服务与定时任务 |
| SSH 配置 | 读取 sshd_config / ~/.ssh/config | 允许 root 登录、密码认证、代理命令 |
| 开放端口 | ss -tln（降级 /proc/net/tcp） | 对外监听端口 |
| 用户 crontab | crontab -l | 持久化脚本 |
| PATH 劫持 | 环境变量 PATH 分析 | PATH 含可写目录可致命令劫持 |
| CIS：空密码账号 | 读取 /etc/shadow | 密码字段为空 = 无需密码可登录，高危 |
| CIS：sudo NOPASSWD | 读取 /etc/sudoers 与 /etc/sudoers.d | 免密提权条目（NOPASSWD），中危 |
| CIS：内核参数加固 | sysctl（suid_dumpable / ASLR / ICMP 重定向 / IP 转发） | 内核参数是否处于安全基线值 |
| CIS：登录历史 | lastb -n 50 / last -n 10 | 失败登录（暴力破解迹象）与近期登录核查 |

## 平台说明

- --platform auto 按当前系统选择；也可显式指定 windows / linux。
- 非目标平台的命令不可用属预期，会以 info 提示跳过，不会报错。
- 所有输出默认脱敏；环境变量值、凭据内容一律不打印。
