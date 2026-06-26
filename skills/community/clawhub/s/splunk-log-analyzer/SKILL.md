---
name: log-analyzer
description: 纯本地日志分析系统，支持日志统计、重复检测、错误分析和异常识别
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["streamlit"], "runtime": "python3" },
        "install":
          [
            {
              "id": "python",
              "kind": "pip",
              "package": "streamlit",
              "label": "Install Streamlit (pip)",
            },
            {
              "id": "pandas",
              "kind": "pip",
              "package": "pandas",
              "label": "Install Pandas (pip)",
            },
            {
              "id": "plotly",
              "kind": "pip",
              "package": "plotly",
              "label": "Install Plotly (pip)",
            },
          ],
        "emoji": "📊",
      },
  }
---

# Log Analyzer - 日志分析系统

纯本地日志文件分析工具，无需任何外部连接或云服务。

## 功能特性

### 3个核心功能

1. **📥 数据摄取诊断**
   - 日志统计（总文件数、总大小、总行数）
   - 重复日志识别和统计
   - 时间分布分析（按小时统计）
   - 重复率计算和 Top 重复日志展示

2. **⚡ 索引性能优化**
   - 日志统计分析
   - 错误类型统计和分布
   - 错误日志提取和展示
   - 最近错误列表

3. **🚨 错误与异常监控**
   - 错误日志检测和分类
   - 异常事件识别（基于时间戳统计分析）
   - 错误趋势可视化
   - 异常时间点标记

## 使用方法

### 方式 1: 直接运行

```bash
cd ~/.openclaw/workspace/skills/log-analyzer
streamlit run log-analyzer.py --server.port 8506
```

### 方式 2: 使用启动脚本

```bash
cd ~/.openclaw/workspace/skills/log-analyzer
./start-log-analyzer.sh
```

### 在 OpenClaw 中使用

当用户要求分析日志文件、检查日志错误、或进行日志统计时，自动启动此技能：

```
"分析 /var/log/app.log"
"检查这个日志文件有没有问题"
"帮我统计一下这些日志"
```

## 日志格式支持

支持标准格式的日志文件：

- **时间戳**: `[2024-03-10 14:30:00]`
- **日志级别**: `[ERROR|WARN|INFO|DEBUG|CRITICAL|FATAL]`
- **错误类型**: `[DB_ERROR|APP_ERROR|NETWORK_ERROR|AUTH_ERROR|TIMEOUT_ERROR]`
- **IP 地址**: `IP:192.168.1.1`
- **攻击类型**: `SQL_INJECTION|XSS|BRUTE_FORCE|PATH_TRAVERSAL`

## 配置选项

在 Web 界面中可以配置：

- **日志目录**: 指定要分析的日志文件目录
- **文件模式**: 选择要分析的文件类型（*.log, *.txt, *.csv）
- **最大文件数**: 限制分析的文件数量（1-100）
- **显示选项**: 控制图表和重复分析的显示

## 技术细节

### 依赖项

- Python 3.7+
- Streamlit
- Pandas
- Plotly

### 系统架构

```
LogParser
  ├─ parse_line()     - 解析单行日志
  └─ 模式匹配          - 支持多种日志格式

LogAnalyzer
  ├─ get_log_files()    - 获取日志文件列表
  ├─ analyze_log_stats() - 日志统计分析
  ├─ check_duplicates()  - 重复日志检查
  ├─ detect_errors()    - 错误检测
  └─ detect_anomalies() - 异常检测

ResultDisplay
  ├─ display_stats()    - 显示统计信息
  ├─ display_duplicates() - 显示重复信息
  ├─ display_errors()   - 显示错误信息
  └─ display_anomalies() - 显示异常
```

## 性能说明

- 纯本地运行，无需网络连接
- 支持大文件（通过文件大小统计）
- 自动去重（基于哈希值）
- 时间异常检测（基于标准差统计）

## 注意事项

1. 首次使用需要安装 Python 依赖包
2. 分析大量大文件可能需要较长时间
3. 建议限制分析文件数量以避免内存问题
4. 日志格式需要符合标准模式才能正确解析

## 默认访问地址

http://localhost:8506

可通过修改启动脚本中的端口参数来更改。
