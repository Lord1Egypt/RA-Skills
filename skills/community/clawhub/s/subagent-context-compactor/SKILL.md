---
name: subagent-context-compactor
description: 上下文压缩代理，采用分层压缩策略，基于内存使用触发机制。处理HOT/WARM/COLD三层数据，优化token使用。当用户需要压缩对话上下文、优化内存使用、管理会话历史、减少token消耗时使用此技能。特别适用于长时间对话、复杂任务处理、需要保留重要历史信息的场景。
---

# 上下文压缩技能

专门负责压缩上下文的代理，采用分层压缩策略，基于内存使用触发机制。处理HOT/WARM/COLD三层数据，优化token使用。

## 🎯 技能概述

这是一个智能上下文压缩系统，能够：
1. 实时监控会话上下文使用情况
2. 自动触发压缩优化
3. 分层管理历史信息
4. 减少token消耗，提高会话效率

## 📋 使用场景

**立即使用此技能当用户：**
- 说"压缩上下文"、"优化内存"、"减少token使用"
- 提到"长时间对话"、"会话历史太长"
- 需要"保留重要信息，删除冗余内容"
- 处理"复杂任务，需要上下文管理"
- 遇到"token限制"或"上下文窗口不足"
- 想要"自动清理对话历史"

## 🏗️ 系统架构

### 三层数据管理
1. **HOT层** - 实时信息（最近1天，最高重要性）
2. **WARM层** - 近期信息（最近7天，中等重要性）
3. **COLD层** - 历史信息（最近30天，参考重要性）

### 触发机制
- **内存触发**：Token使用率 > 70% 或消息数 > 50
- **时间触发**：每小时自动检查
- **事件触发**：会话开始/结束、任务完成
- **手动触发**：用户命令触发

## 🚀 快速开始

### 启动压缩系统
```bash
# 启动完整系统
./start_system.sh

# 启动监控服务
./start_monitor.sh

# 检查系统状态
./check_status.sh
```

### 基本命令
```bash
# 查看压缩状态
python3 integration.py --status

# 手动触发压缩
python3 integration.py --compress

# 查看压缩历史
python3 integration.py --history
```

## 📁 文件结构

```
context-compactor/
├── SKILL.md                    # 技能说明文件
├── README.md                   # 详细文档
├── config.json                 # 配置文件
├── requirements.txt            # Python依赖
├── start_system.sh             # 启动脚本
├── stop_system.sh              # 停止脚本
├── check_status.sh             # 状态检查
├── start_monitor.sh            # 监控启动
├── stop_monitor.sh             # 监控停止
├── compactor.py                # 核心压缩逻辑
├── hierarchical_compactor.py   # 分层压缩器
├── monitor.py                  # 监控服务
├── integration.py              # 集成服务
├── api_server.py               # API服务器
├── test_compaction.py          # 测试脚本
└── logs/                       # 日志目录
```

## ⚙️ 配置说明

配置文件 `config.json` 包含以下关键设置：

```json
{
  "compaction": {
    "hot_layer": {"max_items": 20, "importance_threshold": 0.7},
    "warm_layer": {"max_items": 100, "importance_threshold": 0.4},
    "cold_layer": {"max_items": 500, "importance_threshold": 0.2}
  },
  "triggers": {
    "memory_threshold": 0.7,
    "message_threshold": 50,
    "time_interval_hours": 1
  }
}
```

## 🔧 集成到OpenClaw

### 1. 添加到心跳检查
编辑 `HEARTBEAT.md`，添加：
```markdown
# 上下文压缩检查
- 检查压缩系统状态
- 查看最近压缩报告
- 优化配置参数
```

### 2. 创建定时任务
使用cron设置定期压缩：
```bash
# 每小时检查一次
0 * * * * cd /path/to/context-compactor && python3 integration.py --check
```

### 3. 集成到会话管理
在会话开始时自动启动监控：
```bash
# 在会话初始化脚本中添加
./start_monitor.sh
```

## 📊 监控和报告

系统提供详细的监控和报告功能：

### 实时监控
- Token使用率
- 消息数量统计
- 压缩触发次数
- 系统性能指标

### 压缩报告
- 压缩前后对比
- Token节省统计
- 重要性分布
- 时间线分析

### 查看报告
```bash
# 生成详细报告
python3 integration.py --report

# 查看最近压缩
python3 integration.py --recent 5
```

## 🛠️ 高级功能

### 自定义压缩策略
```python
# 在config.json中调整
{
  "compaction_strategy": "aggressive",  # 可选: conservative, balanced, aggressive
  "preserve_keywords": ["重要", "决策", "任务", "偏好"],
  "remove_patterns": ["重复", "冗余", "无关"]
}
```

### 重要性评估算法
系统使用多种因素评估信息重要性：
1. **时间因素** - 越新的信息越重要
2. **内容因素** - 包含决策、任务、偏好的信息
3. **交互因素** - 用户明确标记的重要信息
4. **结构因素** - 对话结构中的关键节点

### 智能保留机制
- **决策点** - 保留所有决策和选择
- **任务定义** - 保留任务描述和要求
- **用户偏好** - 保留用户明确表达的偏好
- **错误修正** - 保留错误和修正过程

## 🔍 故障排除

### 常见问题

**Q: 压缩系统没有启动？**
```bash
# 检查进程
ps aux | grep compactor

# 查看日志
tail -f logs/compactor.log
```

**Q: 压缩效果不明显？**
```bash
# 调整配置
python3 integration.py --config --memory-threshold 0.6

# 查看详细统计
python3 integration.py --stats
```

**Q: 系统占用资源过多？**
```bash
# 调整监控间隔
python3 integration.py --config --interval 300

# 限制压缩频率
python3 integration.py --config --max-compactions 10
```

### 日志查看
```bash
# 查看系统日志
tail -f logs/system.log

# 查看压缩日志
tail -f logs/compaction.log

# 查看错误日志
tail -f logs/error.log
```

## 📈 性能优化

### 最佳实践
1. **定期清理** - 每天自动清理旧日志
2. **监控调整** - 根据使用情况调整阈值
3. **备份配置** - 定期备份重要配置
4. **性能测试** - 定期运行性能测试

### 资源管理
```bash
# 设置资源限制
ulimit -n 1024

# 监控内存使用
watch -n 5 'free -m'

# 查看磁盘使用
df -h .
```

## 🤝 贡献和扩展

### 添加新功能
1. 在 `compactor.py` 中添加新的压缩算法
2. 在 `monitor.py` 中添加新的监控指标
3. 在 `integration.py` 中添加新的集成功能

### 自定义扩展
```python
# 创建自定义压缩器
class CustomCompactor:
    def compress(self, context):
        # 自定义压缩逻辑
        pass
```

## 📚 相关资源

- [OpenClaw文档](https://docs.openclaw.ai)
- [上下文管理最佳实践](https://docs.openclaw.ai/context-management)
- [Token优化指南](https://docs.openclaw.ai/token-optimization)

## 🎉 开始使用

现在就开始优化您的对话上下文吧！系统已经准备就绪，只需简单的命令即可启动：

```bash
# 克隆技能到本地
git clone <repository-url> context-compactor

# 安装依赖
pip install -r requirements.txt

# 启动系统
./start_system.sh

# 享受高效的上下文管理！
```

**记住：** 好的上下文管理是高效对话的关键。让这个技能帮助您保持对话的清晰和高效！