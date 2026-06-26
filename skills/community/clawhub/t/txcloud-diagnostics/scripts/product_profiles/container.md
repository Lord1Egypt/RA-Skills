# 容器类

## 产品参数

| 产品 | Namespace | Dimension Key | ID 格式 | 核心指标 |
|------|-----------|--------------|---------|---------|
| TKE 容器服务 (Pod) | `QCE/TKE2` | `tke_cluster_instance_id` + `pod_name`/`namespace` 等 | cls-xxx | K8sPodCpuCoreUsed, K8sPodRateCpuCoreUsedLimit, K8sPodMemUsageBytes, K8sPodRateMemUsageLimit, K8sPodNetworkReceiveBytesBw, K8sPodNetworkTransmitBytesBw, K8sPodRestartTotal, K8sPodDiskUsage |

## 指标决策表

| 问题现象 | 推荐指标 |
|----------|---------|
| Pod 资源不足 | K8sPodCpuCoreUsed, K8sPodRateCpuCoreUsedLimit, K8sPodMemUsageBytes, K8sPodRateMemUsageLimit |
| Pod 异常/重启 | K8sPodRestartTotal, K8sPodStatusReady, K8sPodCpuCoreUsed, K8sPodMemUsageBytes |
| 网络问题 | K8sPodNetworkReceiveBytesBw, K8sPodNetworkTransmitBytesBw, K8sPodNetworkTcpUsageTotal |
| 磁盘问题 | K8sPodDiskUsage, K8sPodFsReadBytes, K8sPodFsWriteBytes |
| 笼统/不明确 | K8sPodCpuCoreUsed, K8sPodMemUsageBytes, K8sPodRestartTotal, K8sPodDiskUsage |

## 注意事项

- TKE 仅支持 `DescribeStatisticData` 接口（非 `GetMonitorData`）
- 维度组合灵活：可按 cluster + namespace + pod_name 等多级筛选
