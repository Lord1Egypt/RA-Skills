# 上下文压缩系统

基于分层策略的智能上下文压缩系统，用于监控和优化OpenClaw会话的上下文使用。

## 功能特性

### 🎯 核心功能
- **实时监控**: 持续监控会话上下文使用情况
- **分层压缩**: HOT/WARM/COLD三层数据管理
- **智能触发**: 基于内存使用、时间和事件的触发机制
- **自动优化**: 根据阈值自动执行压缩
- **详细报告**: 完整的压缩统计和性能报告

### 📊 分层策略
| 层级 | 描述 | 保留时间 | 最大项目 | 重要性阈值 | 压缩方法 |
|------|------|----------|----------|------------|----------|
| **HOT** | 最近的关键信息 | 1天 | 20 | 0.7 | 总结 |
| **WARM** | 中等重要性的历史信息 | 7天 | 100 | 0.4 | 关键词提取 |
| **COLD** | 长期存储的参考信息 | 30天 | 500 | 0.2 | 归档 |

### ⚡ 触发机制
1. **内存触发**: Token使用率 > 70% 或消息数 > 50
2. **时间触发**: 每小时自动检查，或按计划时间
3. **事件触发**: 会话开始/结束、任务完成、错误发生

## 快速开始

### 1. 启动系统
```bash
cd ~/.openclaw/workspace/context-compactor
./start_system.sh
```

### 2. 检查状态
```bash
./check_status.sh
```

### 3. 停止系统
```bash
./stop_system.sh
```

## 系统架构

```
context-compactor/
├── monitor.py              # 监控服务
├── hierarchical_compactor.py # 分层压缩器
├── integration.py          # 集成服务
├── config.json            # 配置文件
├── start_system.sh        # 启动脚本
├── stop_system.sh         # 停止脚本
├── check_status.sh        # 状态检查
├── start_monitor.sh       # 监控启动
├── stop_monitor.sh        # 监控停止
├── logs/                  # 日志目录
├── context_compactor.db   # SQLite数据库
└── README.md             # 本文档
```

## 配置说明

### 主要配置项

#### 分层配置 (`tiers`)
```json
{
  "hot": {
    "retention_days": 1,
    "max_items": 20,
    "importance_threshold": 0.7
  }
}
```

#### 触发机制 (`trigger_mechanisms`)
```json
{
  "memory_based": {
    "enabled": true,
    "token_usage_threshold": 0.7,
    "message_count_threshold": 50
  }
}
```

#### 压缩方法 (`compression_methods`)
```json
{
  "summarization": {
    "enabled": true,
    "max_length_ratio": 0.3
  }
}
```

## 使用示例

### 手动触发压缩
```bash
python3 hierarchical_compactor.py --trigger manual
```

### 查看详细报告
```bash
python3 -c "
import json
with open('status.json', 'r') as f:
    data = json.load(f)
print(json.dumps(data, indent=2, ensure_ascii=False))
"
```

### 监控日志
```bash
tail -f logs/monitor.log
```

## 数据库结构

### `compaction_history` 表
记录所有压缩操作的历史。

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| timestamp | TEXT | 压缩时间 |
| tier | TEXT | 压缩层级 |
| trigger_type | TEXT | 触发类型 |
| items_before | INTEGER | 压缩前项目数 |
| items_after | INTEGER | 压缩后项目数 |
| tokens_before | INTEGER | 压缩前token数 |
| tokens_after | INTEGER | 压缩后token数 |
| compression_ratio | REAL | 压缩率 |
| details | TEXT | 详细信息 |

### `tiered_data` 表
存储分层后的数据。

| 字段 | 类型 | 说明 |
|------|------|------|
| id | TEXT | 唯一ID |
| tier | TEXT | 数据层级 |
| content | TEXT | 原始内容 |
| compressed_content | TEXT | 压缩后内容 |
| original_length | INTEGER | 原始长度 |
| compressed_length | INTEGER | 压缩后长度 |
| importance_score | REAL | 重要性评分 |
| timestamp | TEXT | 时间戳 |
| source | TEXT | 数据来源 |
| metadata | TEXT | 元数据 |
| created_at | TEXT | 创建时间 |
| last_accessed | TEXT | 最后访问时间 |

## 性能指标

### 监控指标
1. **Token使用率**: 当前会话的token使用百分比
2. **消息数量**: 当前会话的消息总数
3. **压缩率**: 压缩前后的长度比例
4. **节省Token**: 压缩节省的token总数
5. **处理时间**: 压缩操作的处理时间

### 优化目标
- 保持Token使用率 < 70%
- 单次压缩时间 < 5秒
- 压缩率目标: 30-50%
- 每小时最多压缩4次

## 故障排除

### 常见问题

#### 1. 系统无法启动
```bash
# 检查依赖
python3 --version

# 检查文件权限
chmod +x *.sh

# 查看错误日志
cat logs/integration.log
```

#### 2. 压缩不生效
```bash
# 检查配置阈值
grep "token_usage_threshold" config.json

# 检查当前使用率
./check_status.sh

# 手动触发测试
python3 hierarchical_compactor.py --trigger test
```

#### 3. 数据库问题
```bash
# 检查数据库文件
ls -la context_compactor.db

# 备份并重建数据库
cp context_compactor.db context_compactor.db.backup
rm context_compactor.db
```

### 日志级别
- **INFO**: 常规操作日志
- **WARNING**: 警告信息
- **ERROR**: 错误信息
- **DEBUG**: 调试信息（需要修改配置）

## 集成到OpenClaw

### 自动启动
编辑OpenClaw配置文件，添加自动启动：
```bash
# 在OpenClaw启动脚本中添加
cd ~/.openclaw/workspace/context-compactor
./start_system.sh &
```

### 心跳集成
在`HEARTBEAT.md`中添加压缩检查：
```markdown
## 定期检查
- [ ] 检查上下文压缩状态
- [ ] 查看压缩报告
- [ ] 清理旧日志
```

## 开发指南

### 添加新的压缩方法
1. 在`hierarchical_compactor.py`中添加新的压缩方法
2. 更新`config.json`中的压缩方法配置
3. 在`CompressionMethod`枚举中添加新方法

### 扩展触发机制
1. 在`monitor.py`中添加新的触发条件
2. 更新`config.json`中的触发配置
3. 实现相应的触发逻辑

### 自定义重要性计算
修改`calculate_importance`方法，添加自定义的重要性计算规则。

## 许可证

本项目基于MIT许可证开源。

## 支持

如有问题或建议，请：
1. 查看日志文件
2. 检查配置设置
3. 提交Issue报告

---

**提示**: 系统首次启动时会创建数据库和日志文件，可能需要几秒钟时间。