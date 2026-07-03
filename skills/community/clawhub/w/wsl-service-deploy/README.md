# WSL Service Deploy

在 Windows 宿主机上，**无需 SSH**，通过 `wsl.exe` 直接操控 WSL Ubuntu，用 `aptitude` 一键部署任意后端服务。

---

## 能做什么

| 你只需要说 | 技能自动完成 |
|-----------|-------------|
| "装 MySQL" | 搜索包名 → 用阿里源下载安装 → 设密码 → 启动 → 自启 → 验证 |
| "装 Redis" | 同上，外加绑定 0.0.0.0、设密码 |
| "装 Nginx" | 通用的 aptitude 部署流程，自动推断包名和配置路径 |
| "卸载 MySQL" | systemctl stop → aptitude purge → 清理数据目录 → 清理残留 |

**不只是 MySQL 和 Redis** — `aptitude search` 能搜到的包，都能用同一套流程装上。

---

## 怎么做到的

```
wsl.exe                   ← 从 Windows 直接调 WSL（需开安全策略）
  └─ echo root密码 | su -c  ← 切到 root，绕开 sudo 密码问题
       └─ aptitude install  ← 阿里云镜像源，下载飞快
            └─ systemctl enable  ← 配开机自启
```

全程本地操作，不依赖 SSH，不需要知道 WSL 的 IP。

---

## 快速开始

### 前提条件

1. WSL Ubuntu 已安装
2. WorkBuddy 安全中心已开启「系统级工具」策略
3. 镜像源已切到国内（技能会自动检查）

### 示例

```
# 安装 MySQL（root 密码设为 123456）
@skill:wsl-service-deploy 帮我装 MySQL

# 安装 Redis（密码 123456，允许远程连接）
@skill:wsl-service-deploy 装 Redis

# 装其他服务（自动搜索 aptitude）
@skill:wsl-service-deploy 装 PostgreSQL
```

---

## 目录结构

```
wsl-service-deploy/
├── SKILL.md                    # 核心工作流 + 通用部署流程 + 服务速查表
├── README.md                   # 你正在读的这个
└── references/
    └── wsl-commands.md         # 命令模板、环境参数、故障处理速查
```

---

## 技能亮点

- **通用性强** — 不是硬编码 MySQL/Redis，而是定义了一套可复用的部署推理链
- **零依赖** — 不用 sshpass、不用 expect、不用 paramiko，只靠系统自带的 `wsl.exe` 和 `su`
- **运行可靠** — 脚本先写后跑，后台执行 + 日志轮询，规避超时
- **故障处理完备** — dpkg 锁清理、残留进程查杀、引号转义规则都内置了

---

## 版本历史

| 日期 | 变更 |
|------|------|
| 2026-06-14 | 初始版本：MySQL + Redis 部署，通用 aptitude 流程，su -c root 通道 |
