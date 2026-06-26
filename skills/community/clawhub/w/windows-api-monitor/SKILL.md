# Windows专用API使用监控技能

## 概述
这是一个专门为Windows环境设计的API使用监控技能，用于替代依赖macOS CodexBar的model-usage技能。它直接读取OpenClaw日志文件来统计模型使用情况，实现"严格控制API使用效率"的目标。

## 技能信息
- **名称**: windows-api-monitor
- **版本**: 1.0.0
- **作者**: 阿康的私人助理
- **创建日期**: 2026-03-22
- **适用平台**: Windows (Windows 10/11)
- **依赖**: Python 3.8+, OpenClaw v1.0+

## 功能特性
✅ **Windows原生支持** - 针对Windows文件系统和日志结构优化
✅ **实时监控** - 支持实时或定期模型使用统计
✅ **多维度分析** - 按模型、按会话、按时间统计
✅ **效率报告** - 生成简洁易读的使用报告
✅ **历史追踪** - 追踪历史使用趋势
✅ **告警机制** - 可设置使用阈值告警

## 安装说明
无需额外安装，技能已配置完整：
```
技能位置: C:\Users\Administrator\.openclaw\workspace\skills\windows-api-monitor
```

## 使用方法

### 基础命令
```bash
# 1. 查看当前会话的API使用情况
python scripts/api_monitor.py --mode current

# 2. 查看今日使用统计
python scripts/api_monitor.py --mode today

# 3. 查看本周使用统计
python scripts/api_monitor.py --mode week

# 4. 查看所有会话统计
python scripts/api_monitor.py --mode all

# 5. 按模型排序查看
python scripts/api_monitor.py --mode all --sort cost

# 6. 查看指定模型的详细使用
python scripts/api_monitor.py --model deepseek-ai

# 7. 生成使用报告文件
python scripts/api_monitor.py --mode all --output report.txt
```

### 高级功能
```bash
# 1. 设置使用阈值告警（例如：每100次调用告警）
python scripts/api_monitor.py --alerts --threshold 100

# 2. 查看成本最高的会话
python scripts/api_monitor.py --mode sessions --limit 10

# 3. 导出为JSON格式（用于自动化处理）
python scripts/api_monitor.py --mode today --format json

# 4. 清理旧日志文件
python scripts/api_monitor.py --cleanup --days 30
```

### 自动检查 - "够用/不够用"判断 (Windows编码兼容版)
专为"严格控制API调用"需求设计，自动判断剩余量：

#### 一键检查命令（最简单）
```bash
# 方法1：运行PowerShell脚本（推荐）
scripts/check_api.ps1

# 方法2：运行批处理脚本
scripts/check_api_fixed.bat

# 方法3：Python命令
python scripts/auto_checker.py --simple --both
```

#### 自动判断功能 (Windows兼容)
```bash
# 1. 简单检查（够用/不够用 + 剩余量）
python scripts/auto_checker.py --simple --both
# 输出示例：
# [今日] [OK] 充足 - 剩余量充足，可放心使用 (剩余85.0%)
# [本周] [OK] 充足 - 本周剩余量充足 (剩余72.5%)

# 2. 详细报告
python scripts/auto_checker.py --report --both

# 3. 持续自动监控（每30分钟检查一次）
python scripts/auto_monitor.py --continuous --interval 30

# 4. JSON格式（适合自动化处理）
python scripts/auto_checker.py --json

# 5. 仅显示告警
python scripts/auto_checker.py --alerts
```

#### 输出说明 (Windows编码兼容)
- **[OK] 够用**: 剩余量 > 20%
- **[WARN] 不够用**: 剩余量 ≤ 20%
- **[ERROR] 耗尽**: 剩余量 ≤ 0%

#### 剩余量显示 (Windows编码兼容)
- **剩余百分比**: 85.0%
- **剩余调用次数**: 850次
- **剩余令牌数**: 850,000
- **预计可用天数**: 7天

### 自动化监控
```bash
# 每日定时监控（可添加到计划任务）
python scripts/daily_check.py

# 实时监控模式（持续监控API使用）
python scripts/auto_monitor.py --continuous --interval 30  # 每30分钟检查一次
```

## 文件结构
```
windows-api-monitor/
├── SKILL.md                      # 技能说明文档
├── scripts/
│   ├── api_monitor.py           # 主监控脚本
│   ├── daily_check.py           # 每日检查脚本
│   ├── realtime_monitor.py      # 实时监控脚本
│   └── utils/
│       ├── log_parser.py        # 日志解析工具
│       ├── report_generator.py  # 报告生成工具
│       └── alerts.py            # 告警工具
├── references/
│   ├── windows_logs.md          # Windows日志文件位置说明
│   └── openclaw_usage.md        # OpenClaw使用统计文档
├── templates/
│   ├── report_template.md       # 报告模板
│   └── alert_template.md        # 告警模板
└── config/
    └── settings.yaml            # 配置文件
```

## 监控数据源
本技能从以下位置收集API使用数据：
1. **OpenClaw会话日志**: `~/.openclaw/logs/*.log`
2. **模型调用记录**: `~/.openclaw/cache/model_usage/*.json`
3. **系统日志**: Windows Event Logs (OpenClaw相关)
4. **实时会话**: 通过OpenClaw CLI接口获取

## 输出示例
```
=== API使用监控报告 (2026-03-22) ===

📊 今日使用统计：
- 总调用次数: 87
- 总令牌数: 12,450
- 估计成本: ~¥0.56

📈 按模型统计：
1. deepseek-ai: 45次 (¥0.31) - 51.7%
2. glm-5: 28次 (¥0.18) - 32.2%
3. 其他: 14次 (¥0.07) - 16.1%

⏰ 时间分布：
- 高峰期: 10:00-12:00 (38次)
- 稳定期: 14:00-18:00 (32次)
- 低峰期: 20:00-08:00 (17次)

⚠️ 告警信息：无异常
```

## 配置说明
编辑 `config/settings.yaml` 自定义监控行为：
```yaml
# 基础配置
monitor:
  interval: 300  # 监控间隔（秒）
  retention_days: 30  # 数据保留天数

# 告警配置
alerts:
  enabled: true
  threshold_calls: 100  # 单日调用阈值
  threshold_tokens: 10000  # 单日令牌阈值
  notify_method: log  # 通知方式: log, email, webhook

# 报告配置
reports:
  daily_enabled: true
  weekly_enabled: true
  monthly_enabled: true
  output_dir: ./reports
```

## 故障排除
### 常见问题
1. **无法读取日志文件**: 检查文件权限和路径是否正确
2. **数据不更新**: 确认OpenClaw正在运行并生成日志
3. **报告生成失败**: 检查Python依赖是否安装完整

### 调试模式
```bash
python scripts/api_monitor.py --debug --verbose
```

## 更新日志
### v1.0.0 (2026-03-22)
- 初始版本发布
- 支持基础监控功能
- Windows原生优化
- 多维度分析报告

## 注意事项
1. 本技能仅监控OpenClaw API使用，不涉及其他应用
2. 数据为估计值，实际成本以官方账单为准
3. 建议定期清理旧日志文件以释放磁盘空间
4. 重要告警建议结合其他监控手段验证

## 相关技能
- **model-usage**: macOS环境的替代方案
- **healthcheck**: 系统健康检查
- **skill-creator**: 技能创建工具