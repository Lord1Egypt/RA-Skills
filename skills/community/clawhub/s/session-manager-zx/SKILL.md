# Session Manager for OpenClaw

🧹 自动管理 OpenClaw 会话，定期清理不活跃的会话，保持系统整洁！

---

## 📦 安装

```bash
# 本地安装
cd ~/.openclaw/workspace/skills
git clone <session-manager-repo> session-manager
```

---

## 🚀 快速开始

### 一键安装

```bash
cd ~/.openclaw/workspace/skills/session-manager
./install.sh
```

### 手动配置

```bash
# 1. 创建会话清理脚本
openclaw session init

# 2. 配置定时清理任务（每天凌晨 2 点）
openclaw cron add --name "会话清理" \
  --schedule "0 2 * * *" \
  --message "清理不活跃的 OpenClaw 会话"
```

---

## 📋 功能

### 1. 自动会话清理

- ✅ 清理超过 N 天未使用的会话
- ✅ 保留重要会话（可配置白名单）
- ✅ 安全删除，避免误删

### 2. 会话监控

- ✅ 列出所有会话及其最后活动时间
- ✅ 统计会话数量和磁盘占用
- ✅ 生成清理报告

### 3. 定时任务

- ✅ 每日自动清理（默认 2:00 AM）
- ✅ 可配置清理策略
- ✅ 支持手动触发

### 4. 反向代理配置（新增）✨

- ✅ 为每个用户创建独立端口
- ✅ 自动绑定会话参数
- ✅ 完整的访问日志
- ✅ 支持 WebSocket

### 5. 多用户批量创建（新增）✨

- ✅ 批量创建多个用户
- ✅ 自动分配端口
- ✅ 生成访问链接列表

---

## ⚙️ 配置选项

### 系统依赖

**反向代理功能需要 Nginx：**

```bash
# 方式 1：自动安装（推荐）
# setup-proxy.sh 会自动检测并安装 Nginx
./scripts/setup-proxy.sh teacher 8081

# 方式 2：手动预安装
sudo apt update && sudo apt install -y nginx
nginx -v  # 验证安装
```

**其他功能无需额外依赖：**
- 会话清理：仅需 bash
- 会话监控：仅需 bash, jq
- 定时任务：OpenClaw cron

### 环境变量

本 Skill 使用以下环境变量（可选）：

```bash
# 会话目录（默认：~/.openclaw/agents/main/sessions）
export OPENCLAW_SESSIONS_DIR="~/.openclaw/agents/main/sessions"

# 配置目录（默认：~/.openclaw/session-manager）
export SESSION_MANAGER_CONFIG="~/.openclaw/session-manager"
```

⚠️ **安全提醒**：
- 不要将敏感信息写入配置文件
- 使用环境变量管理敏感数据
- 不要将 `config.json` 提交到版本控制
- **Token 不要放在命令行**，使用环境变量
- **反向代理会修改系统 Nginx 配置**，需要 sudo 权限

### Token 安全配置

```bash
# ❌ 错误：不要在命令行明文传递 Token
./scripts/setup-proxy.sh teacher 8081 OPENCLAW_PORT YOUR_TOKEN_HERE

# ✅ 正确：使用环境变量
export OPENCLAW_WEBCHAT_TOKEN="your-secure-token"
./scripts/setup-proxy.sh teacher 8081
```

### 清理策略

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--max-age` | 7 | 保留最近 N 天的会话 |
| `--min-sessions` | 5 | 最少保留 N 个会话 |
| `--whitelist` | main,heartbeat | 白名单会话（永不删除） |

### cron 调度

```bash
# 每天凌晨 2 点清理
0 2 * * *

# 每周日凌晨 3 点清理  
0 3 * * 0

# 每 6 小时清理（测试用）
0 */6 * * *
```

---

## 📁 文件结构

```
session-manager/
├── SKILL.md              # 此文件
├── README.md             # 快速入门
├── LICENSE               # MIT 许可证
├── _meta.json            # ClawHub 元数据
├── install.sh            # 安装脚本
├── templates/
│   └── config.example.json # 配置模板
└── scripts/
    ├── cleanup-sessions.sh # 会话清理脚本
    ├── list-sessions.sh    # 会话列表
    ├── monitor-sessions.sh # 会话监控
    ├── setup-proxy.sh      # 反向代理配置（新增）
    └── create-users.sh     # 批量创建用户（新增）
```

---

## 🔧 反向代理配置（新增）✨

### 单个用户配置

```bash
# 用法
./scripts/setup-proxy.sh <用户名> <端口>

# 示例
./scripts/setup-proxy.sh teacher 8081
./scripts/setup-proxy.sh usera 8082
```

### 批量创建用户

```bash
# 1. 创建用户列表
cat > users.txt << EOF
teacher
usera
userb
EOF

# 2. 批量创建
./scripts/create-users.sh users.txt 8081
```

### 访问链接

```
http://服务器 IP:8081/  # teacher 专属
http://服务器 IP:8082/  # usera 专属
http://服务器 IP:8083/  # userb 专属
```

### 管理命令

```bash
# 查看已配置用户
ls /etc/nginx/sites-available/openclaw-*

# 删除用户
sudo rm /etc/nginx/sites-enabled/openclaw-username
sudo systemctl reload nginx

# 查看访问日志
sudo tail -f /var/log/nginx/openclaw-teacher-access.log
```
    ├── list-sessions.sh    # 会话列表脚本
    └── monitor-sessions.sh # 会话监控脚本
```

---

## 🔧 使用示例

### 初始化配置

```bash
./scripts/init-config.sh
```

生成：
```json
{
  "maxAgeDays": 7,
  "minSessions": 5,
  "whitelist": ["main", "heartbeat"],
  "logFile": "~/.openclaw/session-cleanup.log"
}
```

### 手动触发清理

```bash
./scripts/cleanup-sessions.sh --max-age 14 --min-sessions 3
```

### 查看会话状态

```bash
./scripts/list-sessions.sh
```

输出：
```text
📋 会话列表 (共 8 个):
- main (最后活动: 2026-04-08 17:50)
- heartbeat (最后活动: 2026-04-08 17:45)  
- teacher (最后活动: 2026-04-08 17:52)
- qqbot:c2c:... (最后活动: 2026-04-07 10:00)
...
```

### 监控清理历史

```bash
./scripts/monitor-sessions.sh
```

---

## 🧩 与其他 Skills 配合

| Skill | 配合方式 |
|-------|----------|
| `memory-manager` | 共享清理策略，避免冲突 |
| `edge-tts` | 清理 TTS 缓存文件 |

---

## 📊 清理策略建议

### 个人使用
- `maxAgeDays`: 14 (保留 2 周)
- `minSessions`: 10 (最少保留 10 个)

### 团队使用  
- `maxAgeDays`: 7 (保留 1 周)
- `minSessions`: 20 (最少保留 20 个)

### 服务器环境
- `maxAgeDays`: 3 (保留 3 天)
- `minSessions`: 50 (最少保留 50 个)

---

## ⚠️ 注意事项

1. **安全第一** - 白名单中的会话永不删除
2. **备份建议** - 清理前建议备份重要会话
3. **磁盘空间** - 每个会话约占用 1-5MB
4. **权限设置** - 确保脚本有读写权限

---

## 🔍 故障排查

### 会话未清理

```bash
# 检查 cron 任务
openclaw cron list

# 手动运行清理
./scripts/cleanup-sessions.sh --dry-run

# 查看日志
cat ~/.openclaw/session-cleanup.log
```

### 权限错误

```bash
# 设置正确权限
chmod +x scripts/*.sh
chmod 600 config.json
```

### 配置无效

```bash
# 验证配置文件
cat ~/.openclaw/session-manager/config.json
```

---

## 📚 相关资源

- [OpenClaw Cron 文档](https://docs.openclaw.ai/cron)
- [OpenClaw Sessions 文档](https://docs.openclaw.ai/sessions)
- [会话管理最佳实践](https://docs.openclaw.ai/best-practices/sessions)

---

## 📝 更新日志

- **2026-04-08** - 初始版本
  - 会话清理功能
  - 定时任务配置
  - 监控工具

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

__