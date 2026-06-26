# Serverless 类

## 产品参数

| 产品 | Namespace | Dimension Key | ID 格式 | 核心指标 |
|------|-----------|--------------|---------|---------|
| SCF 云函数 | `QCE/SCF_V2` | `functionName` + `namespace` + `version`/`alias` | 函数名 | Duration, Invocation, Error, Throttle, ConcurrentExecutions, Mem, FunctionErrorPercentage, Http2xx, Http4xx |
| CloudBase 云开发 | `QCE/TCB_DOCKER` | `envid` + `serviceid` + `versionid` | 环境ID | EnvCpuUsed, EnvMemUsed, EnvPodNum, EnvPodUnavailableNum, ServiceCpuUsed, ServiceMemUsed |

## 指标决策表

| 问题现象 | 产品 | 推荐指标 |
|----------|------|---------|
| 函数超时/慢 | SCF | Duration, Invocation, Error, Throttle, ConcurrentExecutions, Mem |
| 函数报错 | SCF | Error, FunctionErrorPercentage, Http4xx, Invocation, Duration |
| 被限流 | SCF | Throttle, ConcurrentExecutions, Invocation |
| 云开发资源 | CloudBase | EnvCpuUsed, EnvMemUsed, EnvPodNum, EnvPodUnavailableNum |
| 笼统/不明确 | SCF | Invocation, Duration, Error, Throttle, ConcurrentExecutions |

## 注意事项

- SCF dimension key 是 `functionName`（函数名），不是实例 ID
- SCF 需要 `functionName` + `namespace` + `version`/`alias` 三个维度
