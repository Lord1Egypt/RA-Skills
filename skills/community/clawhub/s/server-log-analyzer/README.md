# Server Log Analyzer

A comprehensive skill for analyzing server log files, detecting problems, extracting performance metrics, and providing actionable troubleshooting insights.

## Features

- **Multi-level Log Parsing**: Supports `[timestamp] module level line: message` format
- **Problem Detection**: Automatically identifies database failures, missing components, notification errors, etc.
- **Python Exception Tracking**: Extracts tracebacks, filters framework code, highlights your project code
- **Performance Metrics**: TPS, batch processing time, worker timing analysis
- **JSON Output**: Supports programmatic processing for automation

## Supported Systems

This skill is designed for:
- Python-based server applications
- OCR/grading systems
- Workflow processing systems
- Any system using structured logging

## Installation

### Via WorkBuddy Skill Market
1. Open WorkBuddy
2. Go to Skill Market
3. Search "server-log-analyzer"
4. Click Install

### Via ClawHub CLI
```bash
clawhub install server-log-analyzer
```

### Manual Installation
1. Download the skill package
2. Place in your WorkBuddy skills directory
3. Restart WorkBuddy

## Usage

### Command Line

```bash
# Analyze a log file
python scripts/log_analyzer.py /path/to/your/logfile.log

# Get JSON output for automation
python scripts/log_analyzer.py /path/to/your/logfile.log --json
```

### In WorkBuddy

Simply trigger the skill with natural language:

- "帮我分析服务器日志"
- "分析这个log文件，看看有什么问题"
- "检查一下性能指标"
- "analyze logs for errors"

## Log Format

The analyzer supports logs in this format:

```
[YYYY/MM/DD HH:MM:SS] module.path LEVEL line_number: message
```

Example:
```
[2026/04/15 12:08:03] app.workers.recognition INFO 45: Processing image batch
```

## Output Example

```
================================================================================
📊 Server Log Analysis Report
================================================================================

📁 Log File: /var/log/app.log
📝 Total Log Lines: 1,234
⏰ Time Range: 2026-04-15 10:00:00 ~ 2026-04-15 12:00:00
⏱️ Duration: 7200 seconds

----------------------------------------
📈 Overall Statistics
----------------------------------------
  INFO:       1,000 条
  WARNING:    200 条
  ERROR:      34 条
  ⛔ EXCEPTION: 3 个
  问题总计:   50 个

----------------------------------------
🚨 PYTHON EXCEPTION (Highest Priority)
----------------------------------------
  Total: 3 exceptions

  📊 Exception Type Distribution:
    - RuntimeError: 2 次
    - ValueError: 1 次

----------------------------------------
⚡ Performance Metrics
----------------------------------------
  Total Batches: 100
  Avg TPS: 138.50
  Max TPS: 250.00
  Avg Time: 0.72s/batch

----------------------------------------
🔍 Issue Summary (By Severity)
----------------------------------------
  🔴 HIGH: Database failures: 5 次
  🟡 MEDIUM: Classification errors: 10 次
  🟢 LOW: ID recognition failures: 35 次
```

## Requirements

- Python 3.7+
- No external dependencies required (uses standard library only)

## License

MIT-0 License - See LICENSE file for details

## Contributing

Issues and pull requests are welcome! Please feel free to submit improvements or bug reports.
