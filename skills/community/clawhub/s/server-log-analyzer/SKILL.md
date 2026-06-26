---
name: server-log-analyzer
description: |
  Analyzes server log files to detect problems, extract performance metrics, and provide troubleshooting insights.
  Triggers: "analyze logs", "log analysis", "check errors", "performance analysis", "server logs",
  "traceback", "runtime error", "exception", "crash", "debug", "日志分析", "查看问题",
  "性能分析", "Python异常", "错误排查"
---

# Server Log Analyzer

Analyzes server log files to identify problems, extract performance metrics, and provide actionable insights for troubleshooting.

## Supported Log Formats

```
[YYYY/MM/DD HH:MM:SS] module.path LEVEL line_number: message
```

Example:
```
[2026/04/15 12:08:03] sanhai.flow.linear_data_flow INFO 127: flow_id:2044266474671067136 - Worker completed
```

## Usage

### Basic Analysis

```bash
python scripts/log_analyzer.py /path/to/your/logfile.log
```

### JSON Output (for automation)

```bash
python scripts/log_analyzer.py /path/to/your/logfile.log --json
```

## Features

### 1. Log Statistics
- Counts INFO, WARNING, ERROR, CRITICAL entries
- Shows time range and duration
- Module-level statistics

### 2. Problem Detection
Automatically detects common issues:

| Severity | Issue Type | Detection Pattern |
|----------|------------|-------------------|
| High | Database failures | `[DB] update/insert failed` |
| High | Missing components | `has no corrector` |
| Medium | Notification failures | `email notification failed` |
| Medium | Classification errors | `paper type error` |
| Low | ID recognition failures | `invalid student number` |

### 3. Python Exception Tracking
Extracts Python traceback information:
- Exception type and message
- Source file locations (filters out framework code)
- Key code location in your project

### 4. Performance Metrics
- TPS (Tasks Per Second)
- Batch processing time
- Worker-level timing

## Output Sections

| Section | Content |
|---------|---------|
| Summary | Log level counts, time range |
| Exceptions | Python exceptions (highest priority) |
| Performance | TPS, processing time |
| Issues | Problems by severity |
| Modules | Module call frequency |

## Performance Thresholds

| Metric | Normal | Warning | Critical |
|--------|--------|---------|----------|
| TPS | 50-300 | <20 | <10 |
| Batch Time | <2s | >5s | >10s |

## Notes

- Large log files (>10MB) may take longer to process
- Exception tracking filters out framework/library code
- Results are sorted by severity (exceptions first)
