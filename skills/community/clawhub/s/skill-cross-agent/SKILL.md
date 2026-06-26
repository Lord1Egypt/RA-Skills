---
name: cross-agent
version: 1.0.0
description: "跨机器Agent协作 - 通过SSH连接局域网内其他OpenClaw实例，实现多机任务分发"
author: OpenClaw
homepage: https://docs.openclaw.ai/skills/cross-agent
tags: [ssh, network, agent, collaboration, remote]
requirements:
  bins: [sshpass, ssh, scp, ping, nc]
  platforms: [linux]
commands:
  scan:
    description: "扫描局域网内在线设备"
    usage: "openclaw cross-agent scan [网段，如 192.168.3.0/24]"
    example: "openclaw cross-agent scan 192.168.3.0/24"
  
  test:
    description: "测试SSH连接到目标机器"
    usage: "openclaw cross-agent test <IP> [用户名] [密码]"
    example: "openclaw cross-agent test 192.168.3.54 admin 123456"
  
  sessions:
    description: "查看目标机器的OpenClaw会话"
    usage: "openclaw cross-agent sessions <IP> [用户名] [密码]"
    example: "openclaw cross-agent sessions 192.168.3.54 admin 123456"
  
  send:
    description: "发送任务指令给目标Agent"
    usage: "openclaw cross-agent send <IP> <任务消息> [用户名] [密码]"
    example: "openclaw cross-agent send 192.168.3.54 '请搜索Docker教程' admin 123456"
  
  get:
    description: "从目标机器获取文件"
    usage: "openclaw cross-agent get <IP> <远程路径> [本地路径] [用户名] [密码]"
    example: "openclaw cross-agent get 192.168.3.54 ~/Desktop/doc.md ~/Desktop/ admin 123456"
  
  put:
    description: "向目标机器发送文件"
    usage: "openclaw cross-agent put <IP> <本地路径> [远程路径] [用户名] [密码]"
    example: "openclaw cross-agent put 192.168.3.54 ~/file.txt ~/Desktop/ admin 123456"
  
  exec:
    description: "在目标机器执行任意命令"
    usage: "openclaw cross-agent exec <IP> <命令> [用户名] [密码]"
    example: "openclaw cross-agent exec 192.168.3.54 'ls -la' admin 123456"
  
  config:
    description: "配置默认连接参数"
    usage: "openclaw cross-agent config [--default-user USER] [--default-pass PASS] [--default-ip IP]"
    example: "openclaw cross-agent config --default-user admin --default-pass 123456"
  
  wizard:
    description: "交互式向导，引导完成跨机器协作"
    usage: "openclaw cross-agent wizard"
---

# 🔌 Cross-Agent 跨机器Agent协作

通过SSH连接到局域网内其他运行OpenClaw的机器，向其Agent发送任务指令。

## 🚀 快速开始

### 1. 扫描局域网设备
```bash
openclaw cross-agent scan 192.168.3.0/24
```

### 2. 测试SSH连接
```bash
openclaw cross-agent test 192.168.3.54 admin 123456
```

### 3. 发送任务
```bash
openclaw cross-agent send 192.168.3.54 "请搜索K230部署方案" admin 123456
```

### 4. 获取结果文件
```bash
openclaw cross-agent get 192.168.3.54 ~/Desktop/K230_部署方案.md ~/Desktop/ admin 123456
```

## ⚙️ 配置默认值

设置常用参数，后续命令可省略：
```bash
openclaw cross-agent config \
  --default-user admin \
  --default-pass 123456 \
  --default-ip 192.168.3.54
```

配置后简写：
```bash
openclaw cross-agent send "请搜索Docker教程"
```

## 📋 前提条件

### 目标机器必须：
1. ✅ 开启SSH服务（端口22）
2. ✅ 运行OpenClaw Gateway
3. ✅ 与本机在同一局域网

### 本机必须：
1. ✅ 安装sshpass: `sudo apt install sshpass`
2. ✅ 网络连通: `ping <目标IP>`

## 🔧 完整工作流示例

```bash
# 1. 扫描找到目标机器
openclaw cross-agent scan

# 2. 配置默认参数
openclaw cross-agent config --default-ip 192.168.3.54

# 3. 测试连接
openclaw cross-agent test

# 4. 查看目标会话
openclaw cross-agent sessions

# 5. 发送任务
openclaw cross-agent send "请生成一份Python爬虫教程"

# 6. 等待几秒...
sleep 10

# 7. 获取生成的文件
openclaw cross-agent get ~/Desktop/*.md ~/Desktop/

# 8. 查看内容
cat ~/Desktop/*.md
```

## 🐛 故障排除

| 问题 | 解决 |
|------|------|
| Permission denied | 检查用户名/密码 |
| Connection refused | 目标SSH未开启或防火墙阻挡 |
| Gateway token error | 使用scp/get/put传输文件 |
| Command not found | 目标机器未安装OpenClaw |

## 📚 更多帮助

- `openclaw cross-agent --help` - 查看所有命令
- `openclaw cross-agent <command> --help` - 查看具体命令帮助