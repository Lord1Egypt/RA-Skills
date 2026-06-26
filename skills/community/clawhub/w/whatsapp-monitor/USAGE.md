# WhatsApp Monitor Skill 使用指南

## 技能概述

这是一个 OpenClaw Skill，用于实时监控 WhatsApp 消息，根据关键词过滤，并将匹配的消息批量导出到飞书多维表格。

## 安装步骤

### 1. 安装 Python 依赖

```bash
cd ~/.openclaw/skills/whatsapp-monitor
pip install -r requirements.txt
```

或一键安装依赖并自检：
```bash
pip install -r requirements.txt && python test_skill.py
```

在 **Linux / macOS** 上也可使用项目根目录的 `install_deps.sh`（逐个安装常用包并运行 `test_skill.py`）。首次使用需赋予执行权限：`chmod +x install_deps.sh`，然后 `./install_deps.sh`。

### 2. 配置 WhatsApp 监控

编辑 `config/whatsapp-targets.json`：

```json
{
  "version": "1.0",
  "targets": [
    {
      "name": "工作团队群",
      "type": "group",
      "identifier": "工作群聊的ID或名称",
      "enabled": true,
      "keywords": ["紧急", "截止", "问题", "帮忙", "会议"],
      "keyword_patterns": ["紧急.*", ".*截止.*", "会议.*[0-9]{1,2}:[0-9]{2}"],
      "priority": "high"
    }
  ],
  "monitoring": {
    "scan_interval_minutes": 5,
    "batch_size": 10,
    "max_age_hours": 24,
    "alert_on_high_priority": true
  }
}
```

### 3. 配置飞书集成

编辑 `config/feishu-settings.json`：

```json
{
  "feishu": {
    "app_id": "你的飞书应用ID",
    "app_secret": "你的飞书应用密钥",
    "table_app_token": "多维表格应用token",
    "table_token": "表格token"
  }
}
```

## 使用方法

### 方式一：命令行运行

```bash
# 测试配置
python scripts/monitor.py --test-config

# 查看状态
python scripts/monitor.py --status

# 启动监控
python scripts/monitor.py --start

# 强制导出
python scripts/monitor.py --export
```

### 方式二：可选启动脚本

**Linux / macOS**

除上文命令行外，可使用项目根目录下的 Bash 脚本（首次建议：`chmod +x install_deps.sh start_monitor.sh run_skill.sh`）：

| 脚本 | 作用 |
|------|------|
| `install_deps.sh` | 安装核心依赖并运行 `test_skill.py` |
| `start_monitor.sh` | 交互菜单：测试配置、启动监控、查看状态、强制导出；会先 `cd` 到脚本所在目录，可在任意路径执行该脚本 |
| `run_skill.sh` | 命令行子命令入口：`start`、`status`、`test`、`export`、`config`、`setup`、`help` |

`run_skill.sh` 与 OpenClaw 目录约定：若已设置环境变量 `OPENCLAW_HOME`，技能根目录为 `$OPENCLAW_HOME/skills/whatsapp-monitor`；**未设置时则使用当前工作目录**，请先 `cd` 到技能目录再执行。

示例：

```bash
cd ~/.openclaw/skills/whatsapp-monitor   # 或你的克隆路径
./run_skill.sh test
./start_monitor.sh                         # 交互菜单
```

### 方式三：OpenClaw Skill 调用

在 OpenClaw 中直接调用：

```bash
# 加载技能
openclaw skills load whatsapp-monitor

# 运行技能
openclaw skills run whatsapp-monitor --start
```

## OpenClaw 集成

### 作为独立服务运行

创建 OpenClaw cron 任务定时运行监控：

```yaml
# config/cron.yaml
jobs:
  - name: "whatsapp-monitor"
    schedule: "*/5 * * * *"  # 每5分钟运行一次
    # 将 youruser 改为本机 Linux 用户名
    command: "cd /home/youruser/.openclaw/skills/whatsapp-monitor && python scripts/monitor.py --start"
```

### 作为 OpenClaw 技能调用

在 OpenClaw 聊天中：
```
@openclaw 启动 WhatsApp 监控
```

或使用技能命令：
```
whatsapp-monitor start
```

## 技能功能

### 监控功能

1. **实时消息监控**：从 WhatsApp 获取最新消息
2. **关键词过滤**：支持简单关键词和正则表达式
3. **优先级管理**：按优先级处理不同重要度的消息
4. **批量处理**：收集到一定数量后批量导出

### 导出功能

1. **飞书多维表格**：自动创建和更新表格
2. **批量写入**：优化 API 调用，减少频率
3. **错误重试**：失败时自动重试
4. **日志记录**：详细的运行日志

## 配置说明

### WhatsApp 目标配置

| 字段 | 说明 | 示例 |
|------|------|------|
| name | 目标名称 | "工作团队群" |
| type | 类型（contact/group） | "group" |
| identifier | 聊天标识符 | "1234567890-1234567890@g.us" |
| enabled | 是否启用 | true |
| keywords | 关键词列表 | ["紧急", "重要"] |
| keyword_patterns | 正则表达式列表 | ["紧急.*", ".*截止.*"] |
| priority | 优先级（high/medium/low） | "high" |

### 监控配置

| 字段 | 说明 | 默认值 |
|------|------|------|
| scan_interval_minutes | 扫描间隔（分钟） | 5 |
| batch_size | 批量大小 | 10 |
| max_age_hours | 最大消息年龄（小时） | 24 |
| alert_on_high_priority | 高优先级告警 | true |

## 故障排除

### 常见问题

1. **依赖安装失败**
   ```bash
   # 使用国内镜像
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

2. **WhatsApp 连接失败**
   - 检查 OpenClaw WhatsApp 渠道是否启用
   - 确保设备已配对
   - 查看 `logs/whatsapp-monitor.log`

3. **飞书 API 错误**
   - 验证 App ID 和 App Secret
   - 检查多维表格权限
   - 确认网络连接

4. **消息不匹配**
   - 检查关键词拼写
   - 验证正则表达式语法
   - 查看消息内容格式

### 日志查看

```bash
# 查看监控日志
cat logs/whatsapp-monitor.log

# 实时查看日志
tail -f logs/whatsapp-monitor.log
```

## 高级功能

### 自定义正则表达式

支持复杂的正则表达式匹配：

```json
"keyword_patterns": [
  "紧急.*处理",          # 匹配以"紧急"开头，"处理"结尾
  "截止.*[0-9]{4}-[0-9]{2}-[0-9]{2}",  # 匹配包含日期的截止消息
  "会议.*([0-9]{1,2}:[0-9]{2}|明天|后天)"  # 匹配会议时间
]
```

### 多条件过滤

支持多个监控目标，每个目标可以有不同的关键词和优先级：

```json
"targets": [
  {
    "name": "工作群",
    "keywords": ["紧急", "问题"],
    "priority": "high"
  },
  {
    "name": "社交群", 
    "keywords": ["聚会", "活动"],
    "priority": "low"
  }
]
```

### 定时导出

除了批量阈值触发，还可以配置定时导出：

```json
"export": {
  "batch_threshold": 10,
  "schedule": "every 30 minutes",  # 每30分钟导出一次
  "force_export_at": ["09:00", "18:00"]  # 每天固定时间强制导出
}
```

## 更新和维护

### 更新技能

```bash
cd ~/.openclaw/skills/whatsapp-monitor
git pull origin main  # 如果有 Git 仓库
# 或手动更新文件
```

### 备份配置

```bash
# 备份配置文件
cp config/whatsapp-targets.json config/whatsapp-targets.json.backup
cp config/feishu-settings.json config/feishu-settings.json.backup

# 备份数据
cp data/matched_messages.json data/matched_messages.json.backup
```

### 重置技能

```bash
# 删除所有数据和日志
rm -f data/matched_messages.json
rm -f logs/whatsapp-monitor.log

# 重置配置文件
rm -f config/whatsapp-targets.json
rm -f config/feishu-settings.json
python scripts/setup.py
```

## 技术支持

如有问题，请：

1. 查看 `logs/whatsapp-monitor.log` 中的错误信息
2. 检查配置文件是否正确
3. 确保所有依赖已安装
4. 验证网络连接和 API 权限

如需进一步帮助，请联系技能开发者或查看 OpenClaw 文档。