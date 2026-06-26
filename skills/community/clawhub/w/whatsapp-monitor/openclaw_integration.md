# OpenClaw WhatsApp Monitor Skill 集成指南

## 技能调用方式

### 1. 直接命令行调用

```bash
# 进入技能目录
cd ~/.openclaw/skills/whatsapp-monitor

# 启动监控
python scripts/monitor.py --start

# 查看状态
python scripts/monitor.py --status

# 测试配置
python scripts/monitor.py --test-config

# 强制导出
python scripts/monitor.py --export
```

### 2. 使用启动脚本

```bash
# Linux/macOS：直接使用 python（推荐）
python scripts/monitor.py --start
```

**Linux / macOS** 还可使用项目根目录的 Bash 脚本（需 `chmod +x`）：

- **`install_deps.sh`** — 安装依赖并运行 `test_skill.py`
- **`start_monitor.sh`** — 交互式菜单（测试 / 启动 / 状态 / 导出）
- **`run_skill.sh`** — 子命令入口；未设置 `OPENCLAW_HOME` 时以**当前工作目录**为技能根目录，已设置则使用 `$OPENCLAW_HOME/skills/whatsapp-monitor`

更完整的说明见 [USAGE.md](USAGE.md) 中「安装步骤」与「方式二：可选启动脚本」。

### 3. OpenClaw Agent 直接调用

在 OpenClaw 聊天界面中，可以直接通过 Agent 调用：

```
@openclaw 启动 WhatsApp 消息监控
```

或使用技能特定的命令模式。

## 技能配置

### 自动加载技能

要让 OpenClaw 自动识别这个技能，需要确保技能在正确的目录结构：

```
.openclaw/
├── skills/
│   └── whatsapp-monitor/
│       ├── SKILL.md
│       ├── config/
│       ├── scripts/
│       ├── references/
│       └── assets/
```

### 技能描述文件 (SKILL.md)

技能通过 `SKILL.md` 中的描述来触发。当前技能会在以下情况被触发：

- "monitor WhatsApp messages"
- "track WhatsApp keywords"
- "export WhatsApp to Feishu"
- "WhatsApp message monitoring"

## 自动化配置

### 定时任务配置

在 OpenClaw 中配置定时任务，自动运行监控：

```yaml
# 每5分钟检查一次
cron:
  - schedule: "*/5 * * * *"
    command: "cd /home/youruser/.openclaw/skills/whatsapp-monitor && python scripts/monitor.py --start"
    name: "whatsapp-monitor"
```

### 触发条件

技能可以配置在以下条件触发：

1. **关键词触发**：当对话中出现相关关键词时
2. **定时触发**：通过 cron 定时执行
3. **事件触发**：当收到 WhatsApp 消息时（需要配置 webhook）
4. **手动触发**：通过 OpenClaw 界面手动启动

## 与其他技能的协作

### 与通知技能结合

可以将监控结果转发到其他通知渠道：

```python
# 示例：将高优先级消息发送到 Slack
if message_priority == "high":
    slack_notify(message_content)
```

### 与数据分析技能结合

监控数据可以进一步分析：

```python
# 示例：分析消息趋势
analyze_message_patterns(matched_messages)
generate_daily_report()
```

## 技能参数配置

### 环境变量

可以在 OpenClaw 配置中设置环境变量：

```yaml
env:
  WHATSAPP_MONITOR_CONFIG_DIR: "/home/youruser/.openclaw/skills/whatsapp-monitor/config"
  WHATSAPP_MONITOR_LOG_DIR: "/home/youruser/.openclaw/skills/whatsapp-monitor/logs"
  WHATSAPP_MONITOR_DATA_DIR: "/home/youruser/.openclaw/skills/whatsapp-monitor/data"
```

将 `youruser` 替换为实际 Linux 用户名；若在 shell 中配置，也可用 `$HOME/.openclaw/skills/whatsapp-monitor/...`。

### 配置文件位置

技能会按以下顺序查找配置文件：

1. 环境变量指定的路径
2. 技能目录下的 `config/` 文件夹
3. 用户主目录下的 `.whatsapp-monitor/` 文件夹

## 调试和监控

### 日志文件

技能会生成详细的日志文件：

```
logs/whatsapp-monitor.log        # 主日志文件
logs/whatsapp-monitor.debug.log  # 调试日志
logs/whatsapp-monitor.error.log  # 错误日志
```

### 监控状态

可以通过以下方式查看技能状态：

```bash
# 查看进程状态
pgrep -af monitor.py || ps aux | grep -E '[m]onitor.py'

# 查看日志
tail -f logs/whatsapp-monitor.log

# 查看数据文件
ls data/*.json
```

## 性能优化

### 内存管理

技能设计了以下内存优化策略：

1. **消息缓存限制**：最多缓存 1000 条消息
2. **定期清理**：自动清理超过24小时的消息
3. **批量处理**：避免频繁的 API 调用

### 网络优化

1. **连接复用**：复用 HTTP 连接
2. **请求合并**：批量处理飞书 API 请求
3. **错误重试**：网络错误时自动重试

## 安全考虑

### 凭证安全

1. **API 密钥存储**：建议使用环境变量或加密存储
2. **配置文件权限**：限制配置文件的访问权限
3. **日志脱敏**：日志中不记录敏感信息

### 访问控制

1. **IP 白名单**：限制 API 访问来源
2. **速率限制**：避免 API 滥用
3. **审计日志**：记录所有操作

## 故障恢复

### 自动恢复机制

技能内置了以下恢复机制：

1. **连接重试**：网络断开后自动重连
2. **状态保存**：定期保存运行状态
3. **错误隔离**：单个目标失败不影响其他目标

### 手动恢复步骤

如果技能停止运行：

```bash
# 1. 检查错误日志
cat logs/whatsapp-monitor.error.log

# 2. 检查配置
cat config/whatsapp-targets.json
cat config/feishu-settings.json

# 3. 测试连接
python scripts/monitor.py --test-config

# 4. 重新启动
python scripts/monitor.py --start
```

## 升级和维护

### 版本升级

```bash
# 备份当前配置
mkdir -p config/backup && cp config/*.json config/backup/

# 更新代码
git pull origin main  # 如果有 Git 仓库

# 安装新依赖
pip install -r requirements.txt

# 测试升级
python scripts/monitor.py --test-config
```

### 数据迁移

如果需要迁移数据：

```bash
# 导出当前数据
python scripts/monitor.py --export

# 备份数据文件
mkdir -p data/backup && cp data/matched_messages.json data/backup/

# 恢复数据
cp data/backup/matched_messages.json data/
```

## 支持和反馈

### 问题报告

遇到问题时，请提供以下信息：

1. 错误日志 (`logs/whatsapp-monitor.error.log`)
2. 配置文件（脱敏后）
3. OpenClaw 版本
4. Python 版本

### 功能请求

如需新功能，请说明：

1. 功能描述
2. 使用场景
3. 期望行为

### 贡献代码

欢迎贡献代码改进：

1. Fork 仓库
2. 创建功能分支
3. 提交 Pull Request
4. 确保测试通过

## 许可证

本技能采用 MIT 许可证。详见 LICENSE 文件（如有）。