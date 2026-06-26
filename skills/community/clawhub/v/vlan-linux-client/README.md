# VLAN Linux Client Skill

VLAN.CN 虚拟组网 Linux 客户端管理技能

## 功能特性

- ✅ 安装指导：支持主流 Linux 发行版
- ✅ 账号管理：登录码/用户名密码登录
- ✅ 组网连接：连接、断开、管理虚拟网络
- ✅ 服务控制：启动、停止、重启、状态查询
- ✅ 故障诊断：日志调试、网络路径分析

## 快速开始

### 安装 VLAN 客户端
```bash
curl -kfsSL http://dl.vlan.cn/vlan2.0/linux/install.sh | sh
```

### 登录
```bash
# 推荐方式 - 登录码登录
vlancli login <login_code>

# 或用户名密码登录
vlancli login <username> <password>
```

### 连接组网
```bash
vlancli start
vlancli getvlanlist
vlancli connect <VlanID>
```

## 支持的 Linux 发行版

| 发行版 | 最低版本 |
|--------|----------|
| Ubuntu | 18.04+ |
| Debian | 10+ |
| CentOS | 7+ |
| Fedora | 30+ |
| Arch Linux | 最新 |

## 文件结构

```
vlan-linux-client/
├── SKILL.md      # 技能主文档（命令参考和使用指南）
└── README.md     # 本文件（快速入门）
```

## 相关资源

- 官方文档：https://www.vlan.cn/guide/linux-client
- 管理后台：https://www.vlan.cn
