# System Log Analytics | 系统日志分析

English | [中文](#系统日志分析-1)

---

## English

### Overview

This skill provides a systematic log analysis workflow based on Google SRE (Site Reliability Engineering) framework:
- Read system/application logs for a specified time period
- Classify and summarize system operating status
- Identify and aggregate major errors and exceptions
- Provide actionable improvement suggestions based on SRE principles
- Generate shareable analysis reports

**When to use:**
Use this skill when user asks to "check logs", "analyze system operation", "summarize errors", or "share a log report".

### Table of Contents

- [SKILL.md](./SKILL.md) - Skill specification and workflow
- [references/sre-principles.md](./references/sre-principles.md) - Google SRE core principles reference
- [references/report-template.md](./references/report-template.md) - Standard analysis report template

### Core Capabilities

1. **Time Range Filtering**
   - Absolute time range (YYYY-MM-DD to YYYY-MM-DD)
   - Relative time range (today, yesterday, last 3 days, last week, last hour, etc.)
   - Read logs by line offset for large files

2. **Exception Classification and Aggregation**
   Classify exceptions based on SRE best practices:
   - **Availability exceptions**: Service outage, 5xx errors, connection timeout
   - **Latency exceptions**: Slow queries, high request latency
   - **Resource exceptions**: High CPU/memory usage, disk full, OOM
   - **Rate limiting & degradation**: Circuit breaker triggered, traffic throttled
   - **Dependency exceptions**: Third-party service call failure, database connection error

3. **Health Scoring**
   Give a 1-5 system health score based on error rate and exception frequency:
   - 5 points: Running well, no serious exceptions
   - 4 points: Minor issues exist, does not affect overall availability
   - 3 points: Moderate exceptions exist, needs attention
   - 2 points: Serious exceptions exist, affects partial services
   - 1 point: Service unavailable, needs immediate attention

4. **Improvement Suggestions**
   Provide suggestions based on Google SRE principles:
   - **Short-term measures**: Emergency handling plan
   - **Mid-term measures**: Monitoring and alert optimization, capacity planning adjustment
   - **Long-term measures**: Architecture optimization, redundancy design, error budget adjustment

### Example Filtering Logic (No Actual Scripts)

Below is the **logical description** of how to filter logs by time. Implement according to your environment:

```
# Logic Description: Filter logs by time range
#
# Input: log_file_path, start_time, end_time
# Output: filtered_log_content
#
# Steps:
# 1. Read log file line by line
# 2. Extract timestamp from each line
# 3. Parse timestamp to comparable format
# 4. Keep lines where timestamp is between start_time and end_time
# 5. Return filtered lines
```

```
# Logic Description: Extract error level logs
#
# Input: filtered_log_content
# Output: error_lines, error_count
#
# Steps:
# 1. Match common error keywords: ERROR, error, SEVERE, FATAL, Exception
# 2. Collect all matching lines
# 3. Count total error lines
# 4. Return error lines and count
```

---

## 系统日志分析

### 概述

本技能基于 Google SRE (Site Reliability Engineering) 框架，提供系统化的日志分析工作流：
- 读取指定时间段的系统日志/应用日志
- 分类总结系统运行状态
- 识别和聚合主要报错与异常
- 基于 SRE 原则给出可落地的改善建议
- 生成可分享的分析报告

**使用场景：**
当用户要求「检查日志」、「分析系统运行情况」、「总结报错」、「分享日志报告」时使用本技能。

### 目录

- [SKILL.md](./SKILL.md) - 技能规范和工作流
- [references/sre-principles.md](./references/sre-principles.md) - Google SRE 核心原则参考
- [references/report-template.md](./references/report-template.md) - 标准分析报告模板

### 核心能力

1. **时间范围过滤**
   - 指定绝对时间范围（`YYYY-MM-DD` 到 `YYYY-MM-DD`）
   - 相对时间范围（今天、昨天、近 3 天、近一周、近一小时等）
   - 通过日志文件行数偏移读取大文件

2. **异常分类与聚合**
   基于 SRE 最佳实践对异常进行分类：
   - **可用性异常**：服务宕机、5xx 错误、连接超时
   - **延迟异常**：慢查询、请求耗时过高
   - **资源异常**：CPU/内存使用率过高、磁盘满、OOM
   - **限流降级**：触发熔断、流量被限流
   - **依赖异常**：第三方服务调用失败、数据库连接错误

3. **运行状况评分**
   基于错误率、异常频次给出 1-5 的系统健康评分：
   - 5 分：运行良好，无严重异常
   - 4 分：存在 minor 问题，不影响整体可用性
   - 3 分：存在中度异常，需要关注
   - 2 分：存在严重异常，影响部分服务
   - 1 分：服务不可用，需要立即处理

4. **改善建议输出**
   根据分析结果，结合 Google SRE 原则给出建议：
   - **短期措施**：紧急处理方案
   - **中期措施**：监控告警优化、容量规划调整
   - **长期措施**：架构优化、冗余设计、错误预算调整

### 示例过滤逻辑（无实际脚本）

以下是按时间过滤日志的**逻辑描述**，根据你的环境实现即可：

```
# 逻辑描述：按时间范围过滤日志
#
# 输入：日志文件路径, 开始时间, 结束时间
# 输出：过滤后的日志内容
#
# 步骤：
# 1. 逐行读取日志文件
# 2. 从每行提取时间戳
# 3. 解析时间戳为可比较格式
# 4. 保留时间戳在开始时间和结束时间之间的行
# 5. 返回过滤后的行
```

```
# 逻辑描述：提取错误级别日志
#
# 输入：过滤后的日志内容
# 输出：错误行列表, 错误计数
#
# 步骤：
# 1. 匹配常见错误关键词：ERROR, error, SEVERE, FATAL, Exception
# 2. 收集所有匹配行
# 3. 统计错误总行数
# 4. 返回错误行和计数
```
