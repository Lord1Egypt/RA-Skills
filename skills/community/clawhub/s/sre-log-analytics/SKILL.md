---
name: system-log-analytics
description: 系统日志分析技能，基于 Google SRE 框架对特定时间段的日志进行检查、总结系统运行情况、分析主要报错异常，并给出改善意见。使用场景：需要检查系统日志、分享运行总结、排查异常问题、获取优化建议。System log analytics skill, based on Google SRE framework, checks logs for specific time periods, summarizes system operation, analyzes major errors and exceptions, and provides improvement suggestions. Usage scenarios: need to check system logs, share operation summary, troubleshoot exceptions, get optimization suggestions.
---

# System Log Analytics | 系统日志分析

English | [中文](#中文-1)

---

## English

### Overview

This skill provides a systematic log analysis workflow based on Google SRE (Site Reliability Engineering) framework.

**Trigger Conditions:**
Use this skill when:
- User asks to "check logs"
- User asks to "analyze system operation"
- User asks to "summarize errors"
- User asks to "share a log report"
- Need to troubleshoot abnormal system problems

### Core Capabilities

#### 1. Time Range Filtering
Support filtering logs by the following methods:
- Specify absolute time range (`YYYY-MM-DD` to `YYYY-MM-DD`)
- Relative time range (today, yesterday, last 3 days, last week, last hour, etc.)
- Read by line offset for large log files

#### 2. Exception Classification and Aggregation
Classify exceptions based on SRE best practices:
- **Availability exceptions**: Service outage, 5xx errors, connection timeout
- **Latency exceptions**: Slow queries, high request latency
- **Resource exceptions**: High CPU/memory usage, disk full, OOM
- **Rate limiting & degradation**: Circuit breaker triggered, traffic throttled
- **Dependency exceptions**: Third-party service call failure, database connection error

#### 3. Health Scoring
Give a 1-5 system health score based on error rate and exception frequency:
- **5 points**: Running well, no serious exceptions
- **4 points**: Minor issues exist, does not affect overall availability
- **3 points**: Moderate exceptions exist, needs attention
- **2 points**: Serious exceptions exist, affects partial services
- **1 point**: Service unavailable, needs immediate handling

#### 4. Improvement Suggestions
Provide suggestions based on Google SRE principles:
- **Short-term measures**: Emergency handling plan
- **Mid-term measures**: Monitoring and alert optimization, capacity planning adjustment
- **Long-term measures**: Architecture optimization, redundancy design, error budget adjustment

### Workflow

#### Step 1: Get Logs
1. Determine the log file path (system logs are usually in `/var/log/`, application logs are determined by deployment location)
2. Filter log content according to time range
   - Use `grep`/`awk` for timestamp filtering (logic description only)
   - For large log files, use `tail`/`head` for segmented reading

#### Step 2: Structured Analysis
Analysis dimensions based on Google SRE framework:

| Analysis Dimension | Check Content |
|-------------------|---------------|
| Error Rate | Proportion of error logs in total logs |
| Error Type Distribution | Aggregate statistics by error type |
| Error Timing | Time distribution of errors, whether sudden |
| Resource Usage | Whether resource exhaustion exists |
| Dependency Status | Whether it is caused by external dependency failure |

#### Step 3: Exception Aggregation
Merge similar exceptions to avoid duplicate reporting:
- Group by error keyword
- Count the number of occurrences of each group of exceptions
- Sort by impact (descending order of severity)

#### Step 4: Generate Report
Output structured report including:
1. **Analysis Overview**: Analysis time range, log file, data volume
2. **Health Score**: Overall health score
3. **Operation Summary**: Overview of normal operation
4. **Exception Details**: Sorted list of exceptions by severity
5. **Improvement Suggestions**: Short-term/mid-term/long-term suggestions

See [references/report-template.md](./references/report-template.md) for reference output template.

#### Step 5: Share Report
According to user needs:
- Output the report directly in the conversation
- If you need to save, you can export it as a Markdown file
- Can be further created as a Feishu cloud document for sharing

### Filtering Logic Description

Below is the **logic description** for common log filtering operations, no actual scripts included:

#### 1. Filter by Time Range

```
Logic Steps:
1. Input: log_file_path, start_time, end_time
2. Initialize empty result list
3. For each line in log_file:
   a. Extract timestamp string from the line
   b. Parse timestamp to datetime object
   c. If start_time <= datetime <= end_time:
       i. Add line to result list
4. Output: result list
```

#### 2. Extract Error Logs

```
Logic Steps:
1. Input: log_lines
2. Initialize empty error list
3. Define error keywords: ["ERROR", "FATAL", "SEVERE", "Exception", "Error:"]
4. For each line in log_lines:
   a. If any keyword matches the line:
       i. Add line to error list
5. Output: error list, error_count = len(error_list)
```

#### 3. Aggregate Exceptions by Keyword

```
Logic Steps:
1. Input: error_lines
2. Initialize empty aggregation dictionary
3. For each line in error_lines:
   a. Extract error type keyword from line (e.g., OOM, connection refused, timeout)
   b. If keyword exists in aggregation:
       i. aggregation[keyword].count += 1
       ii. Add line to aggregation[keyword].samples
   c. Else:
       i. Create new entry in aggregation with count = 1, samples = [line]
4. Sort aggregation by count descending (or by severity)
5. Output: sorted aggregation result
```

---

## 中文

### 概述

本技能基于 Google SRE (Site Reliability Engineering) 框架，提供系统化的日志分析工作流。

**触发条件：**
当以下情况时使用本技能：
- 用户要求「检查日志」
- 用户要求「分析系统运行情况」
- 用户要求「总结报错」
- 用户要求「分享日志报告」
- 需要排查系统异常问题

### 核心能力

#### 1. 时间范围过滤
支持按以下方式筛选日志：
- 指定绝对时间范围（`YYYY-MM-DD` 到 `YYYY-MM-DD`）
- 相对时间范围（今天、昨天、近 3 天、近一周、近一小时等）
- 对于大日志文件，按行数偏移读取

#### 2. 异常分类与聚合
基于 SRE 最佳实践对异常进行分类：
- **可用性异常**：服务宕机、5xx 错误、连接超时
- **延迟异常**：慢查询、请求耗时过高
- **资源异常**：CPU/内存使用率过高、磁盘满、OOM
- **限流降级**：触发熔断、流量被限流
- **依赖异常**：第三方服务调用失败、数据库连接错误

#### 3. 运行状况评分
基于错误率、异常频次给出 1-5 的系统健康评分：
- **5 分**：运行良好，无严重异常
- **4 分**：存在轻微问题，不影响整体可用性
- **3 分**：存在中度异常，需要关注
- **2 分**：存在严重异常，影响部分服务
- **1 分**：服务不可用，需要立即处理

#### 4. 改善建议输出
根据分析结果，结合 Google SRE 原则给出建议：
- **短期措施**：紧急处理方案
- **中期措施**：监控告警优化、容量规划调整
- **长期措施**：架构优化、冗余设计、错误预算调整

### 工作流

#### 步骤 1: 获取日志
1. 确定日志文件路径（系统日志通常在 `/var/log/`，应用日志根据部署位置确定）
2. 根据时间范围过滤日志内容
   - 使用 `grep`/`awk` 进行时间戳筛选（仅逻辑描述）
   - 对于大日志文件，使用 `tail`/`head` 分段读取

#### 步骤 2: 结构化分析
基于 Google SRE 框架分析维度：

| 分析维度 | 检查内容 |
|---------|---------|
| 错误率 | 错误日志占总日志比例 |
| 错误类型分布 | 按错误类型聚合统计 |
| 错误时序 | 错误发生的时间分布，是否突发 |
| 资源使用 | 是否存在资源耗尽情况 |
| 依赖状态 | 是否因外部依赖故障引发 |

#### 步骤 3: 异常聚合
将同类异常合并，避免重复报告：
- 按错误关键词分组聚合
- 统计每组异常发生次数
- 按影响程度排序（严重程度降序）

#### 步骤 4: 生成报告
输出结构化报告，包含：
1. **分析概览**：分析时间范围、日志文件、数据量
2. **健康评分**：整体健康状况评分
3. **运行总结**：正常运行情况概述
4. **异常详情**：按严重程度排序的异常列表
5. **改善建议**：分短期/中期/长期给出建议

参考输出模板请见 [references/report-template.md](./references/report-template.md)

#### 步骤 5: 分享报告
根据用户需求：
- 直接在对话中输出报告
- 如果需要保存，可以导出为 Markdown 文件
- 可进一步创建为飞书云文档分享

### 过滤逻辑描述

以下是常见日志过滤操作的**逻辑描述**，不包含实际脚本：

#### 1. 按时间范围过滤

```
逻辑步骤:
1. 输入: 日志文件路径, 开始时间, 结束时间
2. 初始化空结果列表
3. 遍历日志文件每一行:
   a. 从行中提取时间戳字符串
   b. 将时间戳解析为日期时间对象
   c. 如果 开始时间 <= 日期时间 <= 结束时间:
       i. 将行添加到结果列表
4. 输出: 结果列表
```

#### 2. 提取错误日志

```
逻辑步骤:
1. 输入: 日志行列表
2. 初始化空错误列表
3. 定义错误关键词: ["ERROR", "FATAL", "SEVERE", "Exception", "Error:"]
4. 遍历日志每一行:
   a. 如果任何关键词匹配该行:
       i. 将行添加到错误列表
5. 输出: 错误列表, 错误计数 = len(错误列表)
```

#### 3. 按关键词聚合异常

```
逻辑步骤:
1. 输入: 错误行列表
2. 初始化空聚合字典
3. 遍历每个错误行:
   a. 从行中提取错误类型关键词 (例如: OOM, connection refused, timeout)
   b. 如果关键词已在聚合中:
       i. 聚合[关键词].count += 1
       ii. 将行添加到聚合[关键词].samples
   c. 否则:
       i. 在聚合中创建新条目，count = 1, samples = [line]
4. 按计数降序排序聚合 (或按严重程度)
5. 输出: 排序后的聚合结果
```
