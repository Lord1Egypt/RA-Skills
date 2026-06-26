# Changelog — usage-stats

## v1.0.0 — 2026-04-12

### 新增功能

- **Token 统计**：完整解析 input / output / cacheRead / cacheWrite / totalTokens
- **费用估算**：基于 usage.cost 字段计算总费用
- **模型分布**：按模型分组统计 token 消耗和调用次数
- **缓存命中率**：cacheRead / (cacheRead + cacheWrite) × 100%
- **工具调用排行**：统计所有工具（exec、browser、message 等）的调用频次，含 ASCII bar
- **错误分析**：自动识别错误类型（exit_code、pwsh_error、python_exception 等），提供根因和修复方案
- **会话详情**：每个会话的开始/结束时间、时长、token、轮次、错误数
- **日趋势**：每日会话量 / token / 错误量变化
- **时段热力图**：24 小时活跃分布，找出使用高峰
- **历史快照**：保存最近 90 条运行记录，支持环比趋势对比
- **exec 性能分析**：P50 / P95 / 均值 / 最值的命令执行耗时
- **消息角色分布**：user / assistant / system 各角色消息数量
- **会话结束原因**：stopReason 分布统计
- **文本长度统计**：平均消息字符数

### 修复的问题

- 时间戳支持 ISO 8601 字符串（`2026-03-25T14:39:40.681Z`）和 Unix 毫秒戳两种格式
- Windows PowerShell 环境中文路径写入乱码（`sys.stdout.reconfigure(encoding='utf-8')`）
- 读取空 JSONL 文件不报错
- JSON 解码失败时跳过损坏行

### 技术细节

- 脚本：Python 3，标准库，无第三方依赖
- 入口：`scripts/analyze_usage.py`
- 数据源：`~/.qclaw/agents/main/sessions/*.jsonl`
- 输出：`~/.qclaw/workspace/memory/usage_stats_latest.md`
- 历史：`~/.qclaw/workspace/memory/usage_stats_history.json`
- 平台：Windows（兼容 macOS/Linux）
