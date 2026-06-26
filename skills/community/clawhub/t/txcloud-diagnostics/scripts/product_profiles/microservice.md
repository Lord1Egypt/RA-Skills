# 微服务工具与平台

## 产品参数

| 产品 | Namespace | Dimension Key | ID 格式 | 核心指标 |
|------|-----------|--------------|---------|---------|
| API 网关 | `QCE/APIGATEWAY` | `serviceId` + `environmentName` | service-xxx | NumOfReq, ResponseTime, ClientError, ServerError, ConcurrentConnections, Servererror5xx |
| 微服务平台 TSF | `QCE/TSF` | `applicationId` | application-xxx | ReqCount, SuccCount, FailCount, AvgDurationMs |
| 微服务引擎 TSE (ZK) | `TSE/ZOOKEEPER` | `InstanceId` + `PodName` | 实例ID | AvgRequestLatency, RequestTotalCount, RequestFailCount, ZookeeperNumAliveConnections, ZookeeperNumZnode, JvmMemoryBytesUsedHeap |

## 指标决策表

| 问题现象 | 产品 | 推荐指标 |
|----------|------|---------|
| 网关错误多 | API 网关 | NumOfReq, ResponseTime, ClientError, ServerError, Servererror5xx |
| 网关限流 | API 网关 | NumOfReq, Clienterror429, ConcurrentConnections |
| 服务调用慢 | TSF | ReqCount, FailCount, AvgDurationMs |
| 注册中心异常 | TSE ZK | AvgRequestLatency, RequestFailCount, ZookeeperNumAliveConnections, ZookeeperOutstandingRequests |
| 笼统/不明确 | API 网关 | NumOfReq, ResponseTime, ServerError, Servererror5xx |

## 注意事项

- TSE 有多个子 namespace：`TSE/ZOOKEEPER`、`TSE/NACOS`、`TSE/POLARIS`，根据引擎类型选择
- API 网关 dimension 需 `serviceId` + `environmentName`，API 级别再加 `apiId`
