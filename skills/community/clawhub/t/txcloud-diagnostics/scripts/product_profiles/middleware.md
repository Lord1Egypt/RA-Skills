# 中间件/微服务类 诊断

覆盖产品：TSE（微服务引擎）、TSF（微服务平台）、API Gateway（API 网关）、TCM（服务网格）

## 产品参数

| 产品 | Namespace | Dimension Key | 实例 ID 格式 |
|------|-----------|--------------|-------------|
| TSE (Polaris) | `TSE/POLARIS` | `instanceId` | polaris-xxx |
| TSE (Nacos) | `TSE/NACOS` | `instanceId` | nacos-xxx |
| TSE (Zookeeper) | `TSE/ZOOKEEPER` | `instanceId` | zk-xxx |
| TSF | `QCE/TSF` | `appid` | app-xxx |
| API Gateway | `QCE/APIGATEWAY` | `serviceId` | service-xxx |
| TCM | `QCE/TCM` | 需通过 API 确认 | mesh-xxx |

## 指标决策表

| 问题现象 | 推荐指标（通用）|
|----------|---------|
| 服务调用慢 | 通过 DescribeBaseMetrics 确认可用的延迟/QPS/错误率指标 |
| 网关错误多 | `NumOfReq,ApiCalledNum,NumOf4xx,NumOf5xx,ResponseTime` |
| 笼统/不明确 | 通过 DescribeBaseMetrics 确认后选取 CPU/内存/请求量/错误率相关指标 |

## 注意事项

- TSE 有多个子 namespace（POLARIS/NACOS/ZOOKEEPER/CONSULAPI/SRE），根据用户使用的引擎选择
- API Gateway 的 dimension key 是 `serviceId`
