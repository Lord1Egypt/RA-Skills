# CVM / 计算类 诊断

覆盖产品：CVM（云服务器）、Lighthouse（轻量应用）、ECM、HAI、AutoScaling

## 产品参数

| 产品 | Namespace | Dimension Key | 实例 ID 格式 |
|------|-----------|--------------|-------------|
| CVM | `QCE/CVM` | `InstanceId` | ins-xxx |
| Lighthouse | `QCE/LIGHTHOUSE` | `InstanceId` | lhins-xxx |
| ECM | `QCE/ECM` | `UUID` | UUID 格式 |
| HAI | `QCE/HAI` | `InstanceId` | hai-xxx |
| AutoScaling | `QCE/AUTOSCALING` | `AutoScalingGroupId` | asg-xxx |

## 指标决策表

| 问题现象 | 推荐指标 |
|----------|---------|
| CPU 高/卡顿/响应慢 | `CpuUsage,CpuLoadavg,MemUsage,TcpCurrEstab` |
| 内存不足/OOM | `MemUsage,MemUsed,CpuUsage,CpuLoadavg` |
| 磁盘满/IO 慢 | `CvmDiskUsage,CpuUsage,CpuLoadavg,MemUsage` |
| 网络异常/丢包 | `WanIntraffic,WanOuttraffic,LanIntraffic,LanOuttraffic,TcpCurrEstab` |
| 无法访问/宕机 | `CpuUsage,MemUsage,CvmDiskUsage,LanIntraffic,LanOuttraffic,TcpCurrEstab` |
| 笼统/不明确 | `CpuUsage,MemUsage,CpuLoadavg,CvmDiskUsage,LanIntraffic,LanOuttraffic` |

## 特殊逻辑

- **CVM 自动关联 CBS**：脚本检测到 namespace=QCE/CVM 且 ins-xxx 时，自动查询挂载的 CBS 云硬盘并采集磁盘 IO 指标，**无需手动指定**。
- **Lighthouse** 使用独立 namespace `QCE/LIGHTHOUSE`，指标与 CVM 类似。
- **OS 内部诊断**：当监控指标发现异常或用户要求深入排查时，可通过 TAT（自动化助手）远程执行命令，参见 SKILL.md 的 Step 6。

## 注意事项

- 指标名大小写敏感，务必通过 DescribeBaseMetrics 确认
- TAT 远程命令需实例已安装自动化助手 Agent（官方镜像默认已安装）
