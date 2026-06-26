# 安全类 诊断

覆盖产品：WAF（Web 应用防火墙）、CWP（主机安全）、CFW（云防火墙）、TCSS（容器安全）

## 产品参数

| 产品 | Namespace | Dimension Key | 实例 ID 格式 |
|------|-----------|--------------|-------------|
| WAF | `QCE/WAF` | `instanceid` | waf-xxx |
| CWP 主机安全 | `QCE/CWP` | 需通过 API 确认 | 实例 ID |
| CFW 云防火墙 | `QCE/CFW` | 需通过 API 确认 | 实例 ID |
| TCSS 容器安全 | `QCE/TCSS` | 需通过 API 确认 | 实例 ID |

## 指标决策表

| 问题现象 | 推荐指标（WAF）|
|----------|---------|
| 请求被拦截 | 通过 DescribeBaseMetrics 确认可用的拦截/请求量/QPS 相关指标 |
| WAF 性能 | 通过 DescribeBaseMetrics 确认可用指标 |
| 笼统/不明确 | 通过 DescribeBaseMetrics 确认后选取请求量/拦截数/带宽相关指标 |

## 注意事项

- WAF 的 dimension key 是小写 `instanceid`
- CWP/CFW/TCSS 的精确 dimension key 需通过 DescribeBaseMetrics API 确认
