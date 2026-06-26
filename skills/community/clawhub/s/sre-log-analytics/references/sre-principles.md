# Google SRE Core Principles | Google SRE 核心原则

English | [中文](#中文-1)

---

## English

### Error Budget

Error budget is a core tool in SRE used to balance innovation speed and reliability:

- **Error Budget = 1 - Service Level Objective (SLO)**  
  Example: SLO is 99.9% availability → Error budget is 0.1%
- When the error budget is exhausted, stop new feature releases and focus on stability
- When the error budget is sufficient, you can safely accelerate releases

### Application in Log Analysis

1. **Error Rate Calculation**: Count the proportion of error requests in total requests and compare it with the error budget
2. **Risk Assessment**:
   - If the error rate is still within the budget: It is recommended to continue monitoring, no need to stop delivery
   - If the error rate is close to/exceeds the budget: It is recommended to prioritize stability issues
3. **Priority Sorting**: Issues that affect the error budget have higher priority than those that do not

### Service Level Objective (SLO) and Service Level Indicator (SLI)

#### Common SLI Types

1. **Availability**: Successful requests / Total requests
2. **Latency**: Proportion of requests completed within the specified threshold
3. **Throughput**: Number of successfully processed requests per second
4. **Data Integrity**: Proportion of correctly stored/retrieved data

#### Checkpoints in Log Analysis

- Is there a continuous decline in availability metrics?
- Is there a trend of gradually increasing latency?
- Is there a regular traffic peak causing resource bottlenecks?

### The Four Golden Signals of Monitoring

Google SRE proposes four key monitoring dimensions that log analysis needs to cover:

#### 1. Latency

- Definition: The time it takes for a service to process a request
- Log checkpoints:
  - Are there a lot of slow requests?
  - Are slow requests concentrated on specific interfaces?
  - Does P95/P99 latency exceed the standard?

#### 2. Traffic

- Definition: Current service load size
- Log checkpoints:
  - Is there a sudden increase/decrease in request volume?
  - Does the traffic peak accompany an increase in error rate?
  - Can it handle peak traffic?

#### 3. Errors

- Definition: Service error rate
- Log checkpoints:
  - Is the error rate within an acceptable range?
  - Is the error type distribution reasonable?
  - Are there new types of errors?

#### 4. Saturation

- Definition: The degree of saturation of service resources
- Log checkpoints:
  - Are CPU, memory, disk, and network saturated?
  - Is there an OOM (Out of Memory)?
  - Is the connection pool exhausted?
  - Are database connections full?

### Troubleshooting Principles

#### 1. Narrow the Range Step by Step

1. From whole to part: Look at the overall error rate first, then locate the specific service/interface
2. From the time dimension: Determine the start time of the problem and associate recent changes
3. From the dependency dimension: Check whether it is caused by upstream/downstream dependencies

#### 2. Hypothesis Verification Method

1. Propose possible cause hypotheses
2. Find evidence in the logs to support or refute
3. Repeat until the root cause is found

#### 3. Common Root Cause Classification

- **Change induced**: New code deployment, configuration change, dependency upgrade
- **Resource exhaustion**: Memory leak, connection leak, disk full
- **Traffic change**: Sudden traffic hotspot, cache invalidation
- **Dependency failure**: Third-party service outage, database master switch
- **Infrastructure**: Hardware failure, network partition

### Suggestion Output Framework

Based on SRE principles, improvement suggestions should be divided into three levels:

#### Short-term (Execute Immediately)

- Roll back recent changes
- Emergency capacity expansion
- Rate limiting protection
- Restart abnormal processes

#### Mid-term (Within a few days to a week)

- Improve monitoring and alerts
- Adjust capacity planning
- Add error retry/circuit breaker
- Optimize slow queries

#### Long-term (Within a few weeks to months)

- Architecture optimization (redundancy, multi-AZ)
- Establish error budget mechanism
- Automated scaling/failover
- Performance engineering optimization

---

## 中文

### 错误预算 (Error Budget)

错误预算是 SRE 中用于平衡创新速度和可靠性的核心工具：

- **错误预算 = 1 - 服务水平目标 (SLO)**  
  例如：SLO 为 99.9% 可用性 → 错误预算为 0.1%
- 当错误预算耗尽时，停止新功能发布，专注于稳定性
- 当错误预算剩余充足时，可以安全加速发布

### 在日志分析中的应用

1. **错误率计算**：统计错误请求占总请求比例，与错误预算对比
2. **风险评估**：
   - 如果错误率仍在预算内：建议持续监控，无需停止交付
   - 如果错误率已接近/超出预算：建议优先处理稳定性问题
3. **优先级排序**：影响错误预算的问题优先级高于不影响的问题

### 服务水平目标 (SLO) 与 服务水平指标 (SLI)

#### 常见 SLI 类型

1. **可用性**：成功请求 / 总请求
2. **延迟**：请求在指定阈值内完成的比例
3. **吞吐量**：每秒成功处理的请求数
4. **数据完整性**：正确存储/检索的数据比例

#### 在日志分析中的检查点

- 是否有持续性的可用性指标下降？
- 是否存在延迟逐渐升高的趋势？
- 是否有规律性的流量高峰导致资源瓶颈？

### 监控四黄金信号

Google SRE 提出的四个关键监控维度，日志分析需要覆盖：

#### 1. 延迟 (Latency)

- 定义：服务处理请求所花费的时间
- 日志检查点：
  - 是否有大量慢请求？
  - 慢请求是否集中在特定接口？
  - P95/P99 延迟是否超标？

#### 2. 流量 (Traffic)

- 定义：服务当前的负载大小
- 日志检查点：
  - 请求量是否有突增/突降？
  - 流量高峰是否伴随错误率上升？
  - 是否能应对峰值流量？

#### 3. 错误 (Errors)

- 定义：服务错误率
- 日志检查点：
  - 错误率是否在可接受范围内？
  - 错误类型分布是否合理？
  - 是否有新增的错误类型？

#### 4. 饱和度 (Saturation)

- 定义：服务资源的饱和程度
- 日志检查点：
  - CPU、内存、磁盘、网络是否饱和？
  - 是否有 OOM (Out of Memory)？
  - 连接池是否耗尽？
  - 数据库连接是否打满？

### 排查原则

#### 1. 逐步缩小范围

1. 从整体到局部：先看整体错误率，再定位具体服务/接口
2. 从时间维度：确定问题开始时间，关联最近的变更
3. 从依赖维度：检查是否是上游/下游依赖引起

#### 2. 假设验证法

1. 提出可能的原因假设
2. 从日志中找证据支持或反驳
3. 重复直到找到根因

#### 3. 常见根因分类

- **变更引发**：新代码部署、配置变更、依赖升级
- **资源耗尽**：内存泄漏、连接泄漏、磁盘满
- **流量变化**：突发流量热点、缓存失效
- **依赖故障**：第三方服务宕机、数据库主库切换
- **基础设施**：硬件故障、网络分区

### 建议输出框架

基于 SRE 原则，改善建议应分为三个层级：

#### 短期（立即执行）

- 回滚最近变更
- 紧急扩容
- 限流保护
- 重启异常进程

#### 中期（未来几天到一周）

- 完善监控告警
- 调整容量规划
- 增加错误重试/熔断
- 优化慢查询

#### 长期（未来几周到几个月）

- 架构优化（冗余、多可用区）
- 建立错误预算机制
- 自动化扩容/故障转移
- 性能优化工程
