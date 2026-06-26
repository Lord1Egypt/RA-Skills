# AWS Metrics & Performance

DQL timeseries patterns for AWS CloudWatch-sourced metrics. Use during investigation to determine whether a resource is saturated, erroring, or slow.

## Query Template

The `timeseries` command with `by: { dt.smartscape_source.id}` splits results by Dynatrace entity, and a pipe `| filter` stage scopes the series to a specific resource. The `By.<DimensionName>` suffix in the metric key is the CloudWatch dimension used to align the metric to the entity.

```dql-template
timeseries cpu = avg(cloud.aws.ec2.CPUUtilization.By.InstanceId), by: { dt.smartscape_source.id},
  from: <PROBLEM_START - 30m>, to: <PROBLEM_END + 15m>
| filter dt.smartscape_source.id == toSmartscapeId("<ROOT_CAUSE_ENTITY_ID>")
```

Replace `cloud.aws.ec2.CPUUtilization.By.InstanceId` with the relevant metric key, and `<ROOT_CAUSE_ENTITY_ID>` with the Dynatrace entity ID (e.g. `AWS_EC2_INSTANCE-1F335452CC14B245`). Omit the `| filter` clause to get all instances of that metric.

> **Time windows:** The template above uses `<PROBLEM_START>` and `<PROBLEM_END>` for scoping queries to a specific incident window. The per-service examples below use `from: now()-1h` for simplicity — substitute your incident timestamps when investigating a specific problem.

---

## EC2 Metrics

| Metric key | Description | Unit | Investigation threshold |
|---|---|---|---|
| `cloud.aws.ec2.CPUUtilization.By.InstanceId` | CPU utilization | % | > 85% sustained |
| `cloud.aws.ec2.NetworkIn.By.InstanceId` | Inbound network traffic | Bytes | Spike or drop vs baseline |
| `cloud.aws.ec2.NetworkOut.By.InstanceId` | Outbound network traffic | Bytes | Spike or drop vs baseline |
| `cloud.aws.ec2.StatusCheckFailed.By.InstanceId` | Instance or system status check failures | Count | > 0 |
| `cloud.aws.ec2.DiskReadOps.By.InstanceId` | Disk read operations | Count | Spike vs baseline |
| `cloud.aws.ec2.DiskWriteOps.By.InstanceId` | Disk write operations | Count | Spike vs baseline |

Check CPU utilization for a specific instance:

```dql-template
timeseries cpu = avg(cloud.aws.ec2.CPUUtilization.By.InstanceId), by: { dt.smartscape_source.id},
  from: now()-1h
| filter dt.smartscape_source.id == toSmartscapeId("<ROOT_CAUSE_ENTITY_ID>")
```

Check status check failures (non-zero = instance-level problem):

```dql-template
timeseries checks = max(cloud.aws.ec2.StatusCheckFailed.By.InstanceId), by: { dt.smartscape_source.id},
  from: now()-1h
| filter dt.smartscape_source.id == toSmartscapeId("<ROOT_CAUSE_ENTITY_ID>")
```

---

## Lambda Metrics

| Metric key | Description | Unit | Investigation threshold |
|---|---|---|---|
| `cloud.aws.lambda.Invocations.By.FunctionName` | Total function invocations | Count | Drop vs baseline (may indicate upstream issue) |
| `cloud.aws.lambda.Errors.By.FunctionName` | Function execution errors | Count | > 0 during incident |
| `cloud.aws.lambda.Duration.By.FunctionName` | Execution duration | Milliseconds | Approaching timeout limit |
| `cloud.aws.lambda.Throttles.By.FunctionName` | Throttled invocations | Count | > 0 (concurrency limit hit) |
| `cloud.aws.lambda.ConcurrentExecutions.By.FunctionName` | Concurrent executions in flight | Count | Near account/function concurrency limit |

Check error rate and duration together:

```dql-template
timeseries {errors = sum(cloud.aws.lambda.Errors.By.FunctionName),
           duration = avg(cloud.aws.lambda.Duration.By.FunctionName)},
           by: { dt.smartscape_source.id},
  from: now()-1h
| filter dt.smartscape_source.id == toSmartscapeId("<LAMBDA_ROOT_CAUSE_ENTITY_ID>")
```

> **Note:** `<LAMBDA_ROOT_CAUSE_ENTITY_ID>` is the Dynatrace entity ID for the Lambda function (e.g., `AWS_LAMBDA_FUNCTION-ABC123`).

---

## RDS Metrics

| Metric key | Description | Unit | Investigation threshold |
|---|---|---|---|
| `cloud.aws.rds.CPUUtilization.By.DBInstanceIdentifier` | Database CPU utilization | % | > 85% sustained |
| `cloud.aws.rds.DatabaseConnections.By.DBInstanceIdentifier` | Active database connections | Count | Near `max_connections` limit |
| `cloud.aws.rds.FreeStorageSpace.By.DBInstanceIdentifier` | Free storage remaining | Bytes | Trending toward 0 |
| `cloud.aws.rds.ReadLatency.By.DBInstanceIdentifier` | Average read I/O latency | Seconds | > 0.020s (20ms) for production workloads |
| `cloud.aws.rds.WriteLatency.By.DBInstanceIdentifier` | Average write I/O latency | Seconds | > 0.020s (20ms) for production workloads |

Check CPU and connections for a specific RDS instance:

```dql-template
timeseries {cpu = avg(cloud.aws.rds.CPUUtilization.By.DBInstanceIdentifier),
           connections = avg(cloud.aws.rds.DatabaseConnections.By.DBInstanceIdentifier)},
           by: { dt.smartscape_source.id},
  from: now()-1h
| filter dt.smartscape_source.id == toSmartscapeId("<RDS_ROOT_CAUSE_ENTITY_ID>")
```

> **Note:** `<RDS_ROOT_CAUSE_ENTITY_ID>` is the Dynatrace entity ID for the RDS instance (e.g., `AWS_RDS_DBINSTANCE-ABC123`).

---

## SQS Metrics

| Metric key | Description | Unit | Investigation threshold |
|---|---|---|---|
| `cloud.aws.sqs.ApproximateNumberOfMessagesVisible.By.QueueName` | Messages waiting to be processed | Count | Growing over time (consumer lag) |
| `cloud.aws.sqs.NumberOfMessagesSent.By.QueueName` | Messages sent per period | Count | Drop vs baseline |
| `cloud.aws.sqs.ApproximateAgeOfOldestMessage.By.QueueName` | Age of oldest unprocessed message | Seconds | Exceeds your SLA threshold |

Check queue depth over time:

```dql-template
timeseries {depth = max(cloud.aws.sqs.ApproximateNumberOfMessagesVisible.By.QueueName),
           age = max(cloud.aws.sqs.ApproximateAgeOfOldestMessage.By.QueueName)},
           by: { dt.smartscape_source.id},
  from: now()-1h
| filter dt.smartscape_source.id == toSmartscapeId("<SQS_ROOT_CAUSE_ENTITY_ID>")
```

> **Note:** `<SQS_ROOT_CAUSE_ENTITY_ID>` is the Dynatrace entity ID for the SQS queue (e.g., `AWS_SQS_QUEUE-ABC123`).

---

## ALB Metrics

| Metric key | Description | Unit | Investigation threshold |
|---|---|---|---|
| `cloud.aws.applicationelb.RequestCount.By.LoadBalancer` | Total requests processed | Count | Drop vs baseline |
| `cloud.aws.applicationelb.TargetResponseTime.By.LoadBalancer` | Average response time from targets | Seconds | > p99 baseline |
| `cloud.aws.applicationelb.HTTPCode_ELB_5XX_Count.By.LoadBalancer` | 5xx errors from targets | Count | > 0 during incident |
| `cloud.aws.applicationelb.HealthyHostCount.By.TargetGroup` | Healthy targets per target group | Count | Drop (indicates unhealthy instances) |

> **Important:** `HealthyHostCount.By.TargetGroup` is scoped to a target group entity — use the Dynatrace entity ID for the target group as `<ROOT_CAUSE_ENTITY_ID>` when running that query.

Check request count and 5xx errors for a load balancer:

```dql-template
timeseries {requests = sum(cloud.aws.applicationelb.RequestCount.By.LoadBalancer),
           errors5xx = sum(cloud.aws.applicationelb.HTTPCode_ELB_5XX_Count.By.LoadBalancer)},
           by: { dt.smartscape_source.id},
  from: now()-1h
//| filter dt.smartscape_source.id == toSmartscapeId("<ROOT_CAUSE_ENTITY_ID>")
```
> **Important:**  If this returns empty the load balancer might not have any traffic during the selected time window.

Check healthy host count for a specific target group:

```dql-template
timeseries healthy = min(cloud.aws.applicationelb.HealthyHostCount.By.LoadBalancer.TargetGroup),
  by: { dt.smartscape_source.id , TargetGroup},
  from: now()-1h
| filter dt.smartscape_source.id == toSmartscapeId("<ROOT_CAUSE_ENTITY_ID>")
```

---

## ECS Metrics

| Metric key | Description | Unit | Investigation threshold                                                                                                                              |
|---|---|---|------------------------------------------------------------------------------------------------------------------------------------------------------|
| `cloud.aws.ecs.CPUUtilization.By.ClusterName.ServiceName` | ECS service CPU utilization | % | > 85% sustained                                                                                                                                      |
| `cloud.aws.ecs.MemoryUtilization.By.ClusterName.ServiceName` | ECS service memory utilization | % | > 85% sustained                                                                                                                                      |
| `cloud.aws.ecs_containerinsights.RunningTaskCount.By.ClusterName.ServiceName` | Number of running tasks | Count | Drop vs desired count (task crash loop or placement failure) **Important:** This metric is part of ECS Container Insights and might not be available |

Check CPU and memory for an ECS service:

```dql-template
timeseries {cpu = avg(cloud.aws.ecs.CPUUtilization.By.ClusterName.ServiceName),
           mem = avg(cloud.aws.ecs.MemoryUtilization.By.ClusterName.ServiceName)},
           by: { dt.smartscape_source.id},
  from: now()-1h
| filter dt.smartscape_source.id == toSmartscapeId("<ECS_CLUSTER_ROOT_CAUSE_ENTITY_ID>")
```

> **Note:** `<ECS_CLUSTER_ROOT_CAUSE_ENTITY_ID>` is the Dynatrace entity ID for the ECS cluster (e.g., `AWS_ECS_CLUSTER-ABC123`).

---

## DynamoDB Metrics

| Metric key | Description | Unit | Investigation threshold |
|---|---|---|---|
| `cloud.aws.dynamodb.ConsumedReadCapacityUnits.By.TableName` | Read capacity consumed | Count | Approaching provisioned RCU limit |
| `cloud.aws.dynamodb.ConsumedWriteCapacityUnits.By.TableName` | Write capacity consumed | Count | Approaching provisioned WCU limit |
| `cloud.aws.dynamodb.SystemErrors.By.TableName` | DynamoDB system errors | Count | > 0 |
| `cloud.aws.dynamodb.SuccessfulRequestLatency.By.Operation.TableName` | Successful request latency | Milliseconds | > 10ms (single-digit millisecond expected) |

Check capacity consumption and latency for a table:

```dql-template
timeseries {reads = avg(cloud.aws.dynamodb.ConsumedReadCapacityUnits.By.TableName),
           writes = avg(cloud.aws.dynamodb.ConsumedWriteCapacityUnits.By.TableName),
           latency = avg(cloud.aws.dynamodb.SuccessfulRequestLatency.By.Operation.TableName)},
           by: { dt.smartscape_source.id, TableName},
  from: now()-1h
| filter dt.smartscape_source.id == toSmartscapeId("<DYNAMODB_TABLE_ROOT_CAUSE_ENTITY_ID>")
```

> **Note:** `<DYNAMODB_TABLE_ROOT_CAUSE_ENTITY_ID>` is the Dynatrace entity ID for the DynamoDB table (e.g., `AWS_DYNAMODB_TABLE-ABC123`).


Check if provisioned capacity is being approached:

```dql-template
timeseries {readsProvisioned = avg(cloud.aws.dynamodb.ProvisionedReadCapacityUnits.By.TableName),
    writesProvisioned = avg(cloud.aws.dynamodb.ProvisionedWriteCapacityUnits.By.TableName),
    readsConsumed = avg(cloud.aws.dynamodb.ConsumedReadCapacityUnits.By.TableName),
    writesConsumed = avg(cloud.aws.dynamodb.ConsumedWriteCapacityUnits.By.TableName)},
  by: { dt.smartscape_source.id, TableName},
  from: now()-1h
| filter dt.smartscape_source.id == toSmartscapeId("<DYNAMODB_TABLE_ROOT_CAUSE_ENTITY_ID>")
```    

> **Note:** `<DYNAMODB_TABLE_ROOT_CAUSE_ENTITY_ID>` is the Dynatrace entity ID for the DynamoDB table (e.g., `AWS_DYNAMODB_TABLE-ABC123`).
> **Note:** `This can be empty if the table is using on_demand instead of provisioned throughput`).


---

## NLB Metrics

| Metric key | Description | Unit | Investigation threshold |
|---|---|---|---|
| `cloud.aws.networkelb.ActiveFlowCount.By.LoadBalancer` | Active concurrent TCP flows | Count | Spike vs baseline |
| `cloud.aws.networkelb.NewFlowCount.By.LoadBalancer` | New TCP flows per period | Count | Spike vs baseline |
| `cloud.aws.networkelb.ProcessedBytes.By.LoadBalancer` | Bytes processed by the NLB | Bytes | Spike or drop vs baseline |
| `cloud.aws.networkelb.TCP_Client_Reset_Count.By.LoadBalancer` | Client-initiated TCP resets | Count | > 0 sustained (client-side issues) |
| `cloud.aws.networkelb.TCP_Target_Reset_Count.By.LoadBalancer` | Target-initiated TCP resets | Count | > 0 sustained (target-side issues) |
| `cloud.aws.networkelb.TCP_ELB_Reset_Count.By.LoadBalancer` | NLB-generated TCP resets | Count | > 0 (NLB idle timeout or config issue) |
| `cloud.aws.networkelb.HealthyHostCount.By.LoadBalancer` | Healthy registered targets | Count | Drop vs expected target count |
| `cloud.aws.networkelb.UnHealthyHostCount.By.LoadBalancer` | Unhealthy registered targets | Count | > 0 |
| `cloud.aws.networkelb.HealthyHostCount.By.LoadBalancer.TargetGroup` | Healthy targets per target group | Count | Drop vs expected target count |
| `cloud.aws.networkelb.UnHealthyHostCount.By.LoadBalancer.TargetGroup` | Unhealthy targets per target group | Count | > 0 |
| `cloud.aws.networkelb.ConsumedLCUs.By.LoadBalancer` | Load balancer capacity units consumed | Count | Approaching account LCU limit |

Check TCP resets and flow counts for a specific NLB:

```dql-template
timeseries {clientResets = sum(cloud.aws.networkelb.TCP_Client_Reset_Count.By.LoadBalancer),
           targetResets = sum(cloud.aws.networkelb.TCP_Target_Reset_Count.By.LoadBalancer),
           elbResets = sum(cloud.aws.networkelb.TCP_ELB_Reset_Count.By.LoadBalancer)},
           by: { dt.smartscape_source.id},
  from: now()-1h
| filter dt.smartscape_source.id == toSmartscapeId("<NLB_ROOT_CAUSE_ENTITY_ID>")
```

> **Note:** `<NLB_ROOT_CAUSE_ENTITY_ID>` is the Dynatrace entity ID for the Network Load Balancer (e.g., `AWS_ELASTICLOADBALANCINGV2_LOADBALANCER-ABC123`).

Check healthy vs unhealthy targets per target group:

```dql
timeseries {healthy = min(cloud.aws.networkelb.HealthyHostCount.By.LoadBalancer.TargetGroup),
           unhealthy = max(cloud.aws.networkelb.UnHealthyHostCount.By.LoadBalancer.TargetGroup)},
           by: { dt.smartscape_source.id, TargetGroup},
  from: now()-1h
```

---

## ElastiCache Metrics

| Metric key | Description | Unit | Investigation threshold |
|---|---|---|---|
| `cloud.aws.elasticache.CPUUtilization.By.CacheClusterId` | CPU utilization | % | > 90% sustained |
| `cloud.aws.elasticache.EngineCPUUtilization.By.CacheClusterId` | Redis engine CPU utilization | % | > 90% sustained (single-threaded bottleneck) |
| `cloud.aws.elasticache.DatabaseMemoryUsagePercentage.By.CacheClusterId` | Memory usage percentage | % | > 85% (eviction risk) |
| `cloud.aws.elasticache.CurrConnections.By.CacheClusterId` | Current client connections | Count | Near `maxclients` limit |
| `cloud.aws.elasticache.CacheHits.By.CacheClusterId` | Cache hit count | Count | Drop vs baseline (cache invalidation or cold start) |
| `cloud.aws.elasticache.CacheMisses.By.CacheClusterId` | Cache miss count | Count | Spike vs baseline |
| `cloud.aws.elasticache.Evictions.By.CacheClusterId` | Evicted items due to memory pressure | Count | > 0 sustained (memory pressure) |
| `cloud.aws.elasticache.ReplicationLag.By.CacheClusterId` | Replica lag behind primary | Seconds | > 1s (read consistency risk) |
| `cloud.aws.elasticache.FreeableMemory.By.CacheClusterId` | Available memory on the host | Bytes | Trending toward 0 |
| `cloud.aws.elasticache.NetworkBytesIn.By.CacheClusterId` | Inbound network throughput | Bytes | Spike or near network limit |
| `cloud.aws.elasticache.NetworkBytesOut.By.CacheClusterId` | Outbound network throughput | Bytes | Spike or near network limit |
| `cloud.aws.elasticache.SwapUsage.By.CacheClusterId` | Swap space used | Bytes | > 0 sustained (memory exhaustion) |

Check CPU, memory, and evictions for a cache cluster:

```dql-template
timeseries {cpu = avg(cloud.aws.elasticache.EngineCPUUtilization.By.CacheClusterId),
           memory = avg(cloud.aws.elasticache.DatabaseMemoryUsagePercentage.By.CacheClusterId),
           evictions = sum(cloud.aws.elasticache.Evictions.By.CacheClusterId)},
           by: { dt.smartscape_source.id},
  from: now()-1h
| filter dt.smartscape_source.id == toSmartscapeId("<ELASTICACHE_ROOT_CAUSE_ENTITY_ID>")
```

> **Note:** `<ELASTICACHE_ROOT_CAUSE_ENTITY_ID>` is the Dynatrace entity ID for the ElastiCache cluster (e.g., `AWS_ELASTICACHE_CLUSTER-ABC123`).

Check cache hit ratio to detect cache effectiveness issues:

```dql
timeseries {hits = sum(cloud.aws.elasticache.CacheHits.By.CacheClusterId),
           misses = sum(cloud.aws.elasticache.CacheMisses.By.CacheClusterId)},
           by: { dt.smartscape_source.id},
  from: now()-1h
```

---

## NAT Gateway Metrics

| Metric key | Description | Unit | Investigation threshold |
|---|---|---|---|
| `cloud.aws.natgateway.ActiveConnectionCount.By.NatGatewayId` | Active concurrent connections | Count | Near 55,000 limit per destination |
| `cloud.aws.natgateway.ConnectionAttemptCount.By.NatGatewayId` | Connection attempts per period | Count | Spike vs baseline |
| `cloud.aws.natgateway.ConnectionEstablishedCount.By.NatGatewayId` | Successfully established connections | Count | Drop vs attempt count (connection failures) |
| `cloud.aws.natgateway.ErrorPortAllocation.By.NatGatewayId` | Port allocation errors | Count | > 0 (NAT Gateway capacity exhaustion!) |
| `cloud.aws.natgateway.BytesInFromSource.By.NatGatewayId` | Bytes received from VPC sources | Bytes | Spike vs baseline |
| `cloud.aws.natgateway.BytesOutToDestination.By.NatGatewayId` | Bytes sent to external destinations | Bytes | Spike vs baseline |
| `cloud.aws.natgateway.PacketsDropCount.By.NatGatewayId` | Dropped packets | Count | > 0 (capacity or config issue) |
| `cloud.aws.natgateway.IdleTimeoutCount.By.NatGatewayId` | Connections closed due to idle timeout | Count | Spike (upstream keep-alive issue) |
| `cloud.aws.natgateway.PeakBytesPerSecond.By.NatGatewayId` | Peak bytes per second throughput | Bytes/s | Approaching NAT Gateway throughput limit |
| `cloud.aws.natgateway.PeakPacketsPerSecond.By.NatGatewayId` | Peak packets per second throughput | Count/s | Approaching NAT Gateway packet limit |

Check for port allocation errors and dropped packets (critical capacity indicators):

```dql-template
timeseries {portErrors = sum(cloud.aws.natgateway.ErrorPortAllocation.By.NatGatewayId),
           dropped = sum(cloud.aws.natgateway.PacketsDropCount.By.NatGatewayId),
           activeConns = max(cloud.aws.natgateway.ActiveConnectionCount.By.NatGatewayId)},
           by: { dt.smartscape_source.id},
  from: now()-1h
| filter dt.smartscape_source.id == toSmartscapeId("<NAT_GW_ROOT_CAUSE_ENTITY_ID>")
```

> **Note:** `<NAT_GW_ROOT_CAUSE_ENTITY_ID>` is the Dynatrace entity ID for the NAT Gateway (e.g., `AWS_EC2_NATGATEWAY-ABC123`). `ErrorPortAllocation > 0` means the NAT Gateway cannot allocate more source ports — consider adding additional NAT Gateways or reducing connection volume.

Check traffic throughput for a NAT Gateway:

```dql-template
timeseries {bytesIn = sum(cloud.aws.natgateway.BytesInFromSource.By.NatGatewayId),
           bytesOut = sum(cloud.aws.natgateway.BytesOutToDestination.By.NatGatewayId)},
           by: { dt.smartscape_source.id},
  from: now()-1h
| filter dt.smartscape_source.id == toSmartscapeId("<NAT_GW_ROOT_CAUSE_ENTITY_ID>")
```

---

## API Gateway Metrics

API Gateway has two flavors with different metric keys: **REST APIs** (prefix `cloud.aws.apigateway`) use `ApiName` dimensions, while **HTTP APIs** use `ApiId` dimensions. Error metric names also differ: `4XXError`/`5XXError` for REST, `4xx`/`5xx` for HTTP APIs.

| Metric key | Description | Unit | Investigation threshold |
|---|---|---|---|
| `cloud.aws.apigateway.Count.By.ApiName` | Total REST API calls | Count | Drop vs baseline |
| `cloud.aws.apigateway.4XXError.By.ApiName` | REST API 4xx client errors | Count | Spike vs baseline |
| `cloud.aws.apigateway.5XXError.By.ApiName` | REST API 5xx server errors | Count | > 0 during incident |
| `cloud.aws.apigateway.Latency.By.ApiName` | Overall REST API latency | Milliseconds | > p99 baseline |
| `cloud.aws.apigateway.IntegrationLatency.By.ApiName` | Backend integration latency | Milliseconds | > p99 baseline (backend bottleneck) |
| `cloud.aws.apigateway.Count.By.ApiId` | Total HTTP API calls | Count | Drop vs baseline |
| `cloud.aws.apigateway.4xx.By.ApiId` | HTTP API 4xx client errors | Count | Spike vs baseline |
| `cloud.aws.apigateway.5xx.By.ApiId` | HTTP API 5xx server errors | Count | > 0 during incident |
| `cloud.aws.apigateway.Latency.By.ApiId` | Overall HTTP API latency | Milliseconds | > p99 baseline |
| `cloud.aws.apigateway.IntegrationLatency.By.ApiId` | Backend integration latency | Milliseconds | > p99 baseline (backend bottleneck) |
| `cloud.aws.apigateway.DataProcessed.By.ApiId` | Data processed by HTTP API | Bytes | Spike vs baseline |

Check REST API error rates and latency:

```dql-template
timeseries {calls = sum(cloud.aws.apigateway.Count.By.ApiName),
           errors4xx = sum(cloud.aws.apigateway.4XXError.By.ApiName),
           errors5xx = sum(cloud.aws.apigateway.5XXError.By.ApiName),
           latency = avg(cloud.aws.apigateway.Latency.By.ApiName)},
           by: { dt.smartscape_source.id},
  from: now()-1h
| filter dt.smartscape_source.id == toSmartscapeId("<APIGW_ROOT_CAUSE_ENTITY_ID>")
```

> **Note:** `<APIGW_ROOT_CAUSE_ENTITY_ID>` is the Dynatrace entity ID for the API Gateway (e.g., `AWS_APIGATEWAY_RESTAPI-ABC123`).

Check HTTP API error rates and latency:

```dql-template
timeseries {calls = sum(cloud.aws.apigateway.Count.By.ApiId),
           errors4xx = sum(cloud.aws.apigateway.4xx.By.ApiId),
           errors5xx = sum(cloud.aws.apigateway.5xx.By.ApiId),
           latency = avg(cloud.aws.apigateway.Latency.By.ApiId)},
           by: { dt.smartscape_source.id},
  from: now()-1h
| filter dt.smartscape_source.id == toSmartscapeId("<APIGW_ROOT_CAUSE_ENTITY_ID>")
```

---

## SNS Metrics

| Metric key | Description | Unit | Investigation threshold |
|---|---|---|---|
| `cloud.aws.sns.NumberOfMessagesPublished.By.TopicName` | Messages published to topic | Count | Drop vs baseline (producer issue) |
| `cloud.aws.sns.NumberOfNotificationsDelivered.By.TopicName` | Notifications successfully delivered | Count | Drop vs published count (delivery failure) |
| `cloud.aws.sns.NumberOfNotificationsFailed.By.TopicName` | Notifications that failed delivery | Count | > 0 (subscriber endpoint issue) |
| `cloud.aws.sns.PublishSize.By.TopicName` | Size of published messages | Bytes | Spike vs baseline (unexpected payload growth) |

Check publish volume and delivery failures for a topic:

```dql
timeseries {published = sum(cloud.aws.sns.NumberOfMessagesPublished.By.TopicName),
           delivered = sum(cloud.aws.sns.NumberOfNotificationsDelivered.By.TopicName),
           failed = sum(cloud.aws.sns.NumberOfNotificationsFailed.By.TopicName)},
           by: { dt.smartscape_source.id},
  from: now()-1h
```

Check delivery health for a specific topic:

```dql-template
timeseries {published = sum(cloud.aws.sns.NumberOfMessagesPublished.By.TopicName),
           delivered = sum(cloud.aws.sns.NumberOfNotificationsDelivered.By.TopicName),
           failed = sum(cloud.aws.sns.NumberOfNotificationsFailed.By.TopicName)},
           by: { dt.smartscape_source.id},
  from: now()-1h
| filter dt.smartscape_source.id == toSmartscapeId("<SNS_TOPIC_ROOT_CAUSE_ENTITY_ID>")
```

> **Note:** `<SNS_TOPIC_ROOT_CAUSE_ENTITY_ID>` is the Dynatrace entity ID for the SNS topic (e.g., `AWS_SNS_TOPIC-A281598EF3D8B475`). If `NumberOfNotificationsFailed` is non-zero, check the subscriber endpoint (Lambda, SQS, HTTP) for errors.

---

## S3 Metrics

S3 request metrics require a **CloudWatch request metrics filter** configured on the bucket. Without this filter, only storage-level metrics are available (via entity data — see `security-compliance.md`). All request metrics use the `.By.BucketName.FilterId` dimension pattern. The Dynatrace entity type is `AWS_S3_BUCKET`.

| Metric key | Description | Unit | Investigation threshold |
|---|---|---|---|
| `cloud.aws.s3.AllRequests.By.BucketName.FilterId` | Total requests to the bucket | Count | Drop vs baseline |
| `cloud.aws.s3.4xxErrors.By.BucketName.FilterId` | Client error responses (403, 404, etc.) | Count | Spike vs baseline (access denied or missing objects) |
| `cloud.aws.s3.5xxErrors.By.BucketName.FilterId` | Server error responses | Count | > 0 sustained (S3 service issue) |
| `cloud.aws.s3.GetRequests.By.BucketName.FilterId` | GET requests | Count | Spike vs baseline |
| `cloud.aws.s3.PutRequests.By.BucketName.FilterId` | PUT requests | Count | Spike vs baseline |
| `cloud.aws.s3.DeleteRequests.By.BucketName.FilterId` | DELETE requests | Count | Unexpected spike (data loss risk) |
| `cloud.aws.s3.HeadRequests.By.BucketName.FilterId` | HEAD requests | Count | Spike vs baseline |
| `cloud.aws.s3.ListRequests.By.BucketName.FilterId` | LIST requests | Count | High volume (expensive operation, cost impact) |
| `cloud.aws.s3.FirstByteLatency.By.BucketName.FilterId` | Time to first byte for requests | Milliseconds | > 200ms (S3 or network latency issue) |
| `cloud.aws.s3.TotalRequestLatency.By.BucketName.FilterId` | Total request duration including transfer | Milliseconds | > p99 baseline |
| `cloud.aws.s3.BytesDownloaded.By.BucketName.FilterId` | Bytes downloaded from the bucket | Bytes | Spike vs baseline (unexpected data egress, cost impact) |
| `cloud.aws.s3.BytesUploaded.By.BucketName.FilterId` | Bytes uploaded to the bucket | Bytes | Spike vs baseline |

Check request volume and error rates for all buckets:

```dql
timeseries {
  requests = sum(cloud.aws.s3.AllRequests.By.BucketName.FilterId),
  errors4xx = sum(cloud.aws.s3.4xxErrors.By.BucketName.FilterId),
  errors5xx = sum(cloud.aws.s3.5xxErrors.By.BucketName.FilterId)
},
by: { dt.smartscape_source.id },
from: now()-2h
```

Check latency for a specific bucket:

```dql-template
timeseries {
  firstByte = avg(cloud.aws.s3.FirstByteLatency.By.BucketName.FilterId),
  totalLatency = avg(cloud.aws.s3.TotalRequestLatency.By.BucketName.FilterId)
},
by: { dt.smartscape_source.id },
from: now()-24h
| filter dt.smartscape_source.id == toSmartscapeId("<S3_BUCKET_ENTITY_ID>")
```

> **Note:** `<S3_BUCKET_ENTITY_ID>` is the Dynatrace entity ID for the S3 bucket (e.g., `AWS_S3_BUCKET-8278109BE96166BE`). Per-operation metrics (`GetRequests`, `PutRequests`, etc.) are only available if the bucket's CloudWatch request metrics filter is configured to report them. If these return empty, check the S3 bucket metrics configuration in AWS.

---

## MSK (Managed Kafka) Metrics

MSK metrics are split across three dimension patterns: **cluster-level** (`.By.Cluster_Name`), **broker-level** (`.By.Broker_ID.Cluster_Name`), and **consumer-group-level** (`.By.Cluster_Name.Consumer_Group.Topic`). The Dynatrace entity type is `AWS_MSK_CLUSTER`.

### Cluster Health

| Metric key | Description | Unit | Investigation threshold |
|---|---|---|---|
| `cloud.aws.kafka.ActiveControllerCount.By.Cluster_Name` | Active controller brokers | Count | Must be exactly 1 (0 = no leader, >1 = split-brain) |
| `cloud.aws.kafka.OfflinePartitionsCount.By.Cluster_Name` | Partitions with no active leader | Count | > 0 (data unavailability!) |
| `cloud.aws.kafka.GlobalPartitionCount.By.Cluster_Name` | Total partitions across all topics | Count | Monitor growth over time |
| `cloud.aws.kafka.GlobalTopicCount.By.Cluster_Name` | Total topics in the cluster | Count | Monitor growth over time |
| `cloud.aws.kafka.KafkaDataLogsDiskUsed.By.Cluster_Name` | Aggregate data log disk usage | % | > 85% (broker storage exhaustion risk) |

Check cluster-level health — offline partitions and controller count are the most critical MSK indicators:

```dql-template
timeseries {
  offlinePartitions = max(cloud.aws.kafka.OfflinePartitionsCount.By.Cluster_Name),
  activeControllers = max(cloud.aws.kafka.ActiveControllerCount.By.Cluster_Name),
  globalPartitions = max(cloud.aws.kafka.GlobalPartitionCount.By.Cluster_Name),
  globalTopics = max(cloud.aws.kafka.GlobalTopicCount.By.Cluster_Name)
},
by: { dt.smartscape_source.id },
from: now()-2h
| filter dt.smartscape_source.id == toSmartscapeId("<MSK_CLUSTER_ENTITY_ID>")
```

> **Note:** `<MSK_CLUSTER_ENTITY_ID>` is the Dynatrace entity ID for the MSK cluster (e.g., `AWS_MSK_CLUSTER-4B5BA4FE313B7C3A`). `OfflinePartitionsCount > 0` means producers/consumers cannot read/write affected partitions — treat as a P1 incident.

### Broker Resource Utilization

| Metric key | Description | Unit | Investigation threshold |
|---|---|---|---|
| `cloud.aws.kafka.CpuUser.By.Broker_ID.Cluster_Name` | User-space CPU utilization | % | > 60% sustained (Kafka is single-threaded per partition) |
| `cloud.aws.kafka.CpuIdle.By.Broker_ID.Cluster_Name` | CPU idle percentage | % | < 20% (broker overloaded) |
| `cloud.aws.kafka.CpuSystem.By.Broker_ID.Cluster_Name` | System CPU utilization | % | > 10% sustained (kernel overhead) |
| `cloud.aws.kafka.CpuIoWait.By.Broker_ID.Cluster_Name` | CPU time waiting for I/O | % | > 10% (disk I/O bottleneck) |
| `cloud.aws.kafka.MemoryUsed.By.Broker_ID.Cluster_Name` | Memory in use | Bytes | Near total memory (OOM risk) |
| `cloud.aws.kafka.MemoryFree.By.Broker_ID.Cluster_Name` | Free memory | Bytes | Trending toward 0 |
| `cloud.aws.kafka.MemoryBuffered.By.Broker_ID.Cluster_Name` | Buffered memory | Bytes | Monitor for drops (page cache pressure) |
| `cloud.aws.kafka.MemoryCached.By.Broker_ID.Cluster_Name` | Cached memory | Bytes | Drop indicates page cache eviction (impacts read performance) |
| `cloud.aws.kafka.HeapMemoryAfterGC.By.Broker_ID.Cluster_Name` | JVM heap after garbage collection | Bytes | > 60% of heap size (GC pressure) |
| `cloud.aws.kafka.BurstBalance.By.Broker_ID.Cluster_Name` | EBS burst balance remaining | % | < 20% (I/O throttling imminent) |
| `cloud.aws.kafka.KafkaDataLogsDiskUsed.By.Broker_ID.Cluster_Name` | Per-broker data log disk usage | % | > 85% (broker storage exhaustion risk) |
| `cloud.aws.kafka.KafkaAppLogsDiskUsed.By.Broker_ID.Cluster_Name` | Application log disk usage | % | > 50% (log rotation issue) |

Check broker CPU and memory to identify overloaded brokers:

```dql-template
timeseries cpu = avg(cloud.aws.kafka.CpuUser.By.Broker_ID.Cluster_Name),
           cpuIdle = avg(cloud.aws.kafka.CpuIdle.By.Broker_ID.Cluster_Name),
           memUsed = avg(cloud.aws.kafka.MemoryUsed.By.Broker_ID.Cluster_Name),
           heapAfterGC = avg(cloud.aws.kafka.HeapMemoryAfterGC.By.Broker_ID.Cluster_Name),
           by: { dt.smartscape_source.id },
  from: now()-2h
| filter dt.smartscape_source.id == toSmartscapeId("<MSK_CLUSTER_ENTITY_ID>")
```

Check disk usage and burst balance for storage pressure:

```dql-template
timeseries diskUsed = avg(cloud.aws.kafka.KafkaDataLogsDiskUsed.By.Broker_ID.Cluster_Name),
           burstBalance = min(cloud.aws.kafka.BurstBalance.By.Broker_ID.Cluster_Name),
           by: { dt.smartscape_source.id },
  from: now()-2h
| filter dt.smartscape_source.id == toSmartscapeId("<MSK_CLUSTER_ENTITY_ID>")
```

### Broker Throughput & Networking

| Metric key | Description | Unit | Investigation threshold |
|---|---|---|---|
| `cloud.aws.kafka.BytesInPerSec.By.Broker_ID.Cluster_Name` | Bytes received per second per broker | Bytes/s | Spike vs baseline or approaching throughput limit |
| `cloud.aws.kafka.BytesOutPerSec.By.Broker_ID.Cluster_Name` | Bytes sent per second per broker | Bytes/s | Spike vs baseline |
| `cloud.aws.kafka.MessagesInPerSec.By.Broker_ID.Cluster_Name` | Messages received per second per broker | Count/s | Spike vs baseline |
| `cloud.aws.kafka.ConnectionCount.By.Broker_ID.Cluster_Name` | Current client connections per broker | Count | Near broker connection limit |
| `cloud.aws.kafka.ClientConnectionCount.By.Broker_ID.Cluster_Name` | Client-initiated connections per broker | Count | Imbalanced across brokers |
| `cloud.aws.kafka.LeaderCount.By.Broker_ID.Cluster_Name` | Partition leaders on this broker | Count | Imbalanced across brokers (hot broker) |
| `cloud.aws.kafka.PartitionCount.By.Broker_ID.Cluster_Name` | Partitions on this broker | Count | Imbalanced across brokers |
| `cloud.aws.kafka.NetworkRxDropped.By.Broker_ID.Cluster_Name` | Dropped inbound network packets | Count | > 0 (network saturation) |
| `cloud.aws.kafka.NetworkRxErrors.By.Broker_ID.Cluster_Name` | Inbound network errors | Count | > 0 |
| `cloud.aws.kafka.NetworkTxDropped.By.Broker_ID.Cluster_Name` | Dropped outbound network packets | Count | > 0 (network saturation) |
| `cloud.aws.kafka.NetworkTxErrors.By.Broker_ID.Cluster_Name` | Outbound network errors | Count | > 0 |

Check throughput and connections across all brokers:

```dql
timeseries bytesIn = sum(cloud.aws.kafka.BytesInPerSec.By.Broker_ID.Cluster_Name),
           bytesOut = sum(cloud.aws.kafka.BytesOutPerSec.By.Broker_ID.Cluster_Name),
           connections = max(cloud.aws.kafka.ConnectionCount.By.Broker_ID.Cluster_Name),
           by: { dt.smartscape_source.id },
  from: now()-2h
```

### Topic-Level Throughput

| Metric key | Description | Unit | Investigation threshold |
|---|---|---|---|
| `cloud.aws.kafka.BytesInPerSec.By.Broker_ID.Cluster_Name.Topic` | Bytes received per second per topic per broker | Bytes/s | Identifies hot topics |
| `cloud.aws.kafka.BytesOutPerSec.By.Broker_ID.Cluster_Name.Topic` | Bytes sent per second per topic per broker | Bytes/s | Identifies hot consumer topics |

### Consumer Group Lag

| Metric key | Description | Unit | Investigation threshold |
|---|---|---|---|
| `cloud.aws.kafka.EstimatedMaxTimeLag.By.Cluster_Name.Consumer_Group.Topic` | Estimated time lag of the slowest consumer | Seconds | > SLA threshold (consumer falling behind) |
| `cloud.aws.kafka.MaxOffsetLag.By.Cluster_Name.Consumer_Group.Topic` | Maximum offset lag across consumer group partitions | Count | Growing over time (consumer not keeping up) |

Check consumer group lag by topic — critical for detecting consumer processing failures:

```dql
timeseries lag = max(cloud.aws.kafka.EstimatedMaxTimeLag.By.Cluster_Name.Consumer_Group.Topic),
           offsetLag = max(cloud.aws.kafka.MaxOffsetLag.By.Cluster_Name.Consumer_Group.Topic),
           by: { dt.smartscape_source.id, Consumer_Group, Topic },
  from: now()-2h
```

> **Interpretation:** If `EstimatedMaxTimeLag` is growing while `BytesInPerSec` is stable, the consumer is falling behind and needs scaling or debugging. If both lag and ingest rate spike, the issue may be upstream traffic growth rather than consumer failure.

---

## Metric Discovery

When investigating a service not listed above, or when you need to verify which metrics are actually available on the tenant, use these discovery queries.

Find all available metrics for a given AWS service prefix:

```dql-template
fetch metric.series
| filter startsWith(metric.key, "cloud.aws.<SERVICE_PREFIX>")
| summarize count = count(), by: { metric.key }
| sort count desc
```

> Replace `<SERVICE_PREFIX>` with any prefix (e.g., `s3`, `kafka`, `networkelb`, `elasticache`, `natgateway`, `apigateway`) to discover metrics for a specific service.

Find all AWS metrics available on the tenant:

```dql
fetch metric.series
| filter startsWith(metric.key, "cloud.aws.")
| summarize count = count(), by: { metric.key }
| sort count desc
| limit 200
```

---

## Combining Entity Queries with Metrics

Find a set of entities by filter, then query metrics for all of them. Example: are all EC2 instances in a VPC experiencing high CPU, or just one?

**Step 1 — Find resource IDs for the group:**

```dql-template
smartscapeNodes "AWS_EC2_INSTANCE"
| filter aws.vpc.id == "<VPC_ID>"
| fields name, aws.resource.id
```

**Step 2 — Query metrics for all instances in the group (no filter = all series):**

```dql
timeseries cpu = avg(cloud.aws.ec2.CPUUtilization.By.InstanceId),
           by: { dt.smartscape_source.id},
  from: now()-1h
```

Cross-reference the `dt.smartscape_source.id` dimension values against the entity IDs from Step 1 to identify which instances in the VPC are affected.

### Cross-Service Correlation Patterns

When investigating an incident, a single service's metrics rarely tell the whole story. Use these patterns to correlate metrics across connected services and identify the actual bottleneck.

#### SQS + Lambda Consumer Health

When a Lambda function consumes from SQS, correlate queue depth growth with Lambda errors and throttles to identify consumer bottlenecks.

**Query SQS queue depth and message age:**

```dql
timeseries {
  queue_depth = max(cloud.aws.sqs.ApproximateNumberOfMessagesVisible.By.QueueName),
  queue_age = max(cloud.aws.sqs.ApproximateAgeOfOldestMessage.By.QueueName)
},
by: { dt.smartscape_source.id },
from: now()-6h
```

**Query Lambda consumer errors and performance:**

```dql
timeseries {
  errors = sum(cloud.aws.lambda.Errors.By.FunctionName),
  throttles = sum(cloud.aws.lambda.Throttles.By.FunctionName),
  duration = avg(cloud.aws.lambda.Duration.By.FunctionName)
},
by: { dt.smartscape_source.id },
from: now()-6h
```

Run both queries over the same time window. If queue depth grows while Lambda errors or throttles increase, the consumer is failing. If queue depth grows with no Lambda activity, the consumer may have been disconnected.

#### ALB + Backend Saturation

When ALB response time degrades, check whether backend targets are saturated.

**Query ALB response time and error rates:**

```dql
timeseries {
  response_time = avg(cloud.aws.applicationelb.TargetResponseTime.By.LoadBalancer),
  requests = sum(cloud.aws.applicationelb.RequestCount.By.LoadBalancer),
  errors_5xx = sum(cloud.aws.applicationelb.HTTPCode_ELB_5XX_Count.By.LoadBalancer)
},
by: { dt.smartscape_source.id },
from: now()-2h
```

**Query ECS backend resource utilization:**

```dql
timeseries {
  cpu = avg(cloud.aws.ecs.CPUUtilization.By.ClusterName.ServiceName),
  mem = avg(cloud.aws.ecs.MemoryUtilization.By.ClusterName.ServiceName)
},
by: { dt.smartscape_source.id },
from: now()-2h
```

If ALB 5xx errors spike while ECS CPU or memory is at 85%+, the service needs scaling. If ALB response time degrades but the backend looks healthy, the issue may be network or DNS.

#### RDS + Application Performance

When application errors spike, check whether the database is the bottleneck.

**Query RDS latency, connections, and CPU:**

```dql
timeseries {
  read_latency = avg(cloud.aws.rds.ReadLatency.By.DBInstanceIdentifier),
  write_latency = avg(cloud.aws.rds.WriteLatency.By.DBInstanceIdentifier),
  connections = avg(cloud.aws.rds.DatabaseConnections.By.DBInstanceIdentifier),
  cpu = avg(cloud.aws.rds.CPUUtilization.By.DBInstanceIdentifier)
},
by: { dt.smartscape_source.id },
from: now()-2h
```

If read or write latency spikes above 20ms while connections are near the instance limit, the database is saturated. If CPU is low but latency is high, the bottleneck is likely I/O rather than compute — check `FreeStorageSpace` and IOPS metrics.

> **Correlation tip:** Always query both sides of a dependency over the same time window (`from` / `to`). Mismatched windows make it impossible to confirm whether two signals are actually correlated.

---

## Metric Availability Note

Not all metrics are ingested by default — depends on which services are enabled in the AWS integration configuration. If a timeseries query returns no data:

1. Verify the entity exists: run the `smartscapeNodes` query from Step 1 of `rca-workflow.md`
2. Confirm the metric is collected in the AWS integration settings

Do **not** interpret empty timeseries results as "no problem" — it may mean the metric is not configured for this resource type.
