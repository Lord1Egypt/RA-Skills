# Traffic Monitor Skill
version: 1.0.0

监控服务器网络流量使用情况，定期报告月度流量消耗。

## 背景

服务器每月有 2T 流量限制，需要监控使用情况避免超额。

## 快速查询

```bash
# 查看当前月度流量
vnstat -m -i eth0

# 查看实时流量
vnstat -l -i eth0

# 查看日流量
vnstat -d -i eth0

# 查看流量摘要
traffic_report.py
```

## 技能脚本

### traffic_report.py

生成人类可读的流量报告：

```bash
python3 ~/.openclaw/skills/traffic-monitor/traffic_report.py
```

输出示例：
```
📊 本月流量统计
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📥 入站: 125.3 GB
📤 出站: 89.2 GB
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 总计: 214.5 GB / 2048 GB (10.5%)
⚠️  剩余: 1833.5 GB
```

## 心跳检查

可以在 HEARTBEAT.md 中添加流量检查：

```markdown
## 流量检查（每天一次）
- 运行 traffic_report.py
- 如果使用超过 80%，发送警告
```

## 配置

- **网卡**: eth0
- **月度限制**: 2TB (2048 GB)
- **警告阈值**: 80% (1638 GB)
- **数据存储**: /var/lib/vnstat/vnstat.db

## 注意事项

- vnstat 服务必须运行：`systemctl status vnstat`
- 首次安装需要几分钟收集数据
- 数据持久化存储，重启不丢失
- 统计的是网卡流量，包括所有出入站流量

## 相关命令

```bash
# 检查 vnstat 服务状态
systemctl status vnstat

# 重启 vnstat
systemctl restart vnstat

# 查看所有接口
vnstat --iflist

# 导出 JSON 格式
vnstat -m -i eth0 --json
```
