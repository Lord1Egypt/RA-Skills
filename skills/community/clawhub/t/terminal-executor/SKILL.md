# terminal-executor - 终端命令执行器

## 描述
执行终端命令并返回结果，支持sudo权限命令。

## 激活时机
当用户需要执行系统命令、安装软件、检查系统状态等终端操作时激活。

## 工具
- `exec`: 执行终端命令
- `sudo_exec`: 执行需要sudo权限的命令

## 使用示例
1. 检查系统信息: `exec("uname -a")`
2. 安装软件: `sudo_exec("apt install -y package")`
3. 查看进程: `exec("ps aux | grep process")`

## 安全注意事项
- 谨慎执行删除、格式化等危险命令
- 需要用户确认敏感操作
- 记录执行历史
