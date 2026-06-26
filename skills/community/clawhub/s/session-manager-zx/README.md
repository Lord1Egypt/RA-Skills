# Session Manager for OpenClaw

🧹 自动管理 OpenClaw 会话，定期清理不活跃的会话

---

## 快速开始

### 1. 安装

```bash
cd ~/.openclaw/workspace/skills/session-manager
./install.sh
```

### 2. 系统依赖

**如果使用反向代理功能，需要 Nginx：**

```bash
# 自动安装（setup-proxy.sh 会自动检测）
sudo apt update && sudo apt install -y nginx

# 或手动安装后使用
nginx -v  # 验证安装
```

**其他功能无需额外依赖。**

### 2. 初始化

```bash
# 创建配置文件
./scripts/init-config.sh
```

### 3. 配置自动清理

```bash
# 已包含在 install.sh 中，自动创建 cron 任务
# 每天凌晨 2:00 自动清理
```

---

## 功能

- ✅ 自动清理超过 N 天未使用的会话
- ✅ 保留重要会话（白名单）
- ✅ 会话监控和统计
- ✅ 定时任务支持
- ✅ 清理报告生成

---

## 文件结构

```
session-manager/
├── SKILL.md
├── README.md
├── LICENSE
├── _meta.json
├── install.sh
├── templates/
│   └── config.example.json
└── scripts/
    ├── cleanup-sessions.sh
    ├── list-sessions.sh
    └── monitor-sessions.sh
```

---

## 管理命令

```bash
# 查看会话列表
./scripts/list-sessions.sh

# 手动清理
./scripts/cleanup-sessions.sh --max-age 7

# 监控状态
./scripts/monitor-sessions.sh

# 查看 cron 任务
openclaw cron list
```

---

## 许可证

MIT