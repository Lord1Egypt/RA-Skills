# 交易记忆管理技能

> PAI 交易系统的记忆记录和管理技能
> @version 1.0.0

## 🎯 目标
- 标准化交易决策记录格式
- 自动提炼经验教训
- 支持历史决策检索和对比

## 📋 记忆类型

### 1. 交易日志 (Daily Trading Log)
位置：`memory/trading/YYYY-MM-DD.md`

内容：
- 每次决策的时间戳
- 决策内容 (BUY/SELL/HOLD)
- 置信度和理由
- 执行结果

### 2. 状态快照 (State Snapshot)
位置：`memory/crypto_trading_state.json`

内容：
- 最后决策时间
- 周期计数
- 当日统计
- 系统状态

### 3. 规则库 (Trading Rules)
位置：`memory/trading_rules.md`

内容：
- R001-R006 规则详情
- 规则触发条件
- 历史验证结果

### 4. 错误清单 (Mistakes)
位置：`memory/trading_mistakes.md`

内容：
- M001-M010 常见错误
- 错误原因分析
- 预防措施

## 🔧 工具
- `memory_evaluator.py` - 记忆质量评估
- `auto_memory_manager.py` - 自动记忆管理

## 📊 记忆维护协议

### 每日 (23:00)
- 评估当日记忆质量
- 提炼高价值记忆到 MEMORY.md
- 标记待归档的低价值记忆

### 每周 (周六 23:00)
- 归档旧记忆文件 (>30 天)
- 清理重复/低质量记忆
- 更新记忆系统统计

## 📁 相关文件
- `/Users/zst/clawd/MEMORY.md` - 长期记忆
- `/Users/zst/clawd/memory/` - 日常记忆目录
