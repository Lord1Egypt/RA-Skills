# trading-monitor 配置参考

## 分析深度选择

| 级别 | 内容 | 适用场景 | Token消耗 |
|------|------|---------|----------|
| basic | 持仓+大盘+简要建议 | 快速检查 | ~5k |
| standard | +新闻+板块分析+操作建议 | 日常盯盘 | ~10k |
| full | +资金流向+龙虎榜+明确指令 | 重要决策 | ~15k |

## 推荐部署方案

### 方案A：标准盯盘（推荐新手）
```powershell
.\setup.ps1 -Channel feishu -Target "ou_xxx" -Interval 15 -AnalysisDepth standard
```
- 每15分钟分析一次
- 包含新闻和板块分析
- 14:53收盘前分析

### 方案B：高频盯盘（活跃交易者）
```powershell
.\setup.ps1 -Channel feishu -Target "ou_xxx" -Interval 5 -AnalysisDepth full -IncludePreMarket
```
- 每5分钟分析一次
- 深度分析含资金流向
- 包含8:30开盘前准备

### 方案C：低频监控（长线持仓）
```powershell
.\setup.ps1 -Channel feishu -Target "ou_xxx" -Interval 30 -AnalysisDepth basic
```
- 每30分钟快速检查
- 简要分析，省token
- 不含新闻搜索

## Cron表达式速查

| 表达式 | 含义 |
|--------|------|
| `*/5 9-15 * * 1-5` | 每5分钟（9:00-15:00，周一至周五）|
| `*/15 9-15 * * 1-5` | 每15分钟 |
| `*/30 9-15 * * 1-5` | 每30分钟 |
| `0 9,10,11,13,14 * * 1-5` | 每小时整点（跳过12点午休）|
| `53 14 * * 1-5` | 每天14:53 |
| `30 8 * * 1-5` | 每天8:30 |
| `0 15 * * 1-5` | 每天15:00 |

## 管理命令

```powershell
# 查看所有任务状态
.\manage.ps1 list

# 查看系统配置
.\manage.ps1 status

# 手动触发一次测试
.\manage.ps1 test

# 停止所有任务
.\manage.ps1 stop
```

## 自定义分析内容

编辑 `setup.ps1` 中的 `$analysisTemplates` 变量，修改分析指令。例如加入你的持仓股票：

```
1.查询海科新源、华宝新能、神剑股份行情
2.查询大盘指数
...
```

## 故障排查

1. 任务报 "exec denied" → `openclaw config set tools.exec.security full`
2. 任务不触发 → `openclaw cron list` 检查 enabled 状态
3. 分析结果没推送 → 检查 `--channel` 和 `--to` 参数
4. 超时 → 增加 `--timeout-seconds` 到 600
