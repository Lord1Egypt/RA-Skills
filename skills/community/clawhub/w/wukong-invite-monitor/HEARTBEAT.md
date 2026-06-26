# 心跳推送配置指南

## 概述

心跳推送功能会在发现新邀请码时，自动通过飞书推送通知。

## 配置步骤

### 1. 确保监控已启动

```bash
# 设置基础监控
./setup-cron.sh 5
```

### 2. 添加心跳检查任务

```bash
# 创建 cron 配置文件
cat > /tmp/wukong-cron.txt << 'EOF'
# 悟空邀请码监控 - 基础检查
*/5 * * * * cd ~/.openclaw/workspace/skills/wukong-invite-monitor/scripts && python3 monitor_lite.py check >> /tmp/wukong-monitor.log 2>&1

# 心跳推送检查
*/5 * * * * cd ~/.openclaw/workspace/skills/wukong-invite-monitor/scripts && python3 heartbeat-check.py >> /tmp/wukong-heartbeat.log 2>&1
EOF

# 应用配置
crontab /tmp/wukong-cron.txt
```

### 3. 验证配置

```bash
# 查看 cron 任务
crontab -l | grep wukong

# 测试心跳检查
python3 heartbeat-check.py
```

## 工作原理

```
Cron 监控（每分钟）
    ↓ 检查官网图片版本
    ↓ 发现变化 → 下载图片 + OCR 识别
    ↓ 写入通知文件 /tmp/wukong-new-code-notify.txt

心跳检查（每 5 分钟）
    ↓ 检查通知文件
    ↓ 发现新内容 → 推送飞书消息
    ↓ 更新已查看状态
```

## 官方更新时间段

心跳检查只在以下时间段工作：
- **上午**: 9:00-12:00（每个整点后 5 分钟）
- **下午**: 14:00-18:00（每个整点后 5 分钟）

非官方时间不检查，零消耗。

## 通知格式

```
🎉 悟空邀请码更新通知
━━━━━━━━━━━━━━━━━━━━━━━
📅 时间：2026-03-21 20:30:00
🔢 版本：v28 → v29
📝 内容：大圣闹瑶池
💾 图片已保存
━━━━━━━━━━━━━━━━━━━━━━━
[监控时间] 2026-03-21 20:35:00
```

## 资源消耗

| 项目 | 消耗 |
|------|------|
| **检查频率** | 每 5 分钟（仅官方时间） |
| **每天检查** | 约 100 次 |
| **Token 消耗** | 平时 0，推送时 ~200 tokens/次 |
| **每天总消耗** | < 2000 tokens（按 1-2 次更新） |

## 文件说明

| 文件 | 说明 |
|------|------|
| `/tmp/wukong-monitor.log` | 监控日志 |
| `/tmp/wukong-new-code-notify.txt` | 通知文件 |
| `/tmp/wukong-watched-state.json` | 已查看状态 |
| `/tmp/wukong-heartbeat.log` | 心跳日志 |

## 故障排查

### 心跳检查不工作

```bash
# 检查是否在官方时间
python3 -c "from datetime import datetime; h=datetime.now().hour; print(f'当前小时：{h}, 官方时间：{h in [9,10,11,12,14,15,16,17,18]}')"

# 检查通知文件
cat /tmp/wukong-new-code-notify.txt

# 检查已查看状态
cat /tmp/wukong-watched-state.json
```

### 重复通知

检查状态文件是否正常更新：

```bash
cat /tmp/wukong-watched-state.json
```

### 停止心跳推送

```bash
crontab -e
# 删除包含 heartbeat-check.py 的行
```

## 自定义配置

### 修改检查频率

```bash
# 每 10 分钟检查一次
*/10 * * * * python3 heartbeat-check.py
```

### 修改通知方式

编辑 `heartbeat-check.py` 中的消息格式：

```python
message = {
    "msg_type": "text",
    "content": {
        "text": content + f"\n\n[监控时间] {timestamp}"
    }
}
```

---

**提示**: 心跳推送功能依赖于基础监控，请先确保 `monitor_lite.py` 正常运行。
