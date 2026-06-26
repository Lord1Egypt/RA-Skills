# 云服务商监控配置

## 通用说明

所有云服务商默认不启用——在 `.env` 中配置相应凭证后自动生效。

## 阿里云（Alibaba Cloud CMS）

### 环境变量

```bash
ALIBABA_ACCESS_KEY_ID=your_key_id
ALIBABA_ACCESS_KEY_SECRET=your_secret
ALIBABA_REGION=cn-hangzhou   # 你的区域，如 cn-qingdao、cn-shanghai
# 可选：只拉取指定指标（逗号分隔）
# 可用指标: CPUUtilization, MemoryUtilization, InternetInRate, InternetOutRate,
#           DiskReadBPS, DiskWriteBPS, SysOM_memMonInfo_util(需Agent)
ALIBABA_METRICS=CPUUtilization,MemoryUtilization,InternetInRate,DiskReadBPS
```

### SDK 安装（uv）

```bash
uv run --with aliyun-python-sdk-core --with aliyun-python-sdk-cms python3 script.py
```

### 命名空间与指标

| 服务 | 命名空间 | 可用指标 |
|------|----------|---------|
| ECS | `acs_ecs_dashboard` | CPUUtilization, InternetInRate, InternetOutRate, DiskReadBPS, DiskWriteBPS |
| RDS | `acs_rds_dashboard` | CpuUsage, MemoryUsage, DiskUsage, IOPSUsage, ConnectionUsage |
| SLB | `acs_slb_dashboard` | InstanceTrafficRX, InstanceTrafficTX, InstanceQps, InstanceRt |
| EIP | `acs_vpc_eip` | net_rx.rate, net_tx.rate, net_in.rate_percentage, net_out.rate_percentage |

> 注意：ECS 基础指标 `CPUUtilization`、`InternetInRate` 等无需云监控 Agent；但 `MemoryUtilization`、`MemoryUsed` 需要在 ECS 实例上安装云监控 Agent。

### API 调用要点

```python
# 返回值是 bytes，必须 .decode() 后再 json.loads()
data = json.loads(client.do_action_with_exception(req).decode("utf-8"))
# Datapoints 是 JSON 字符串，需要再次 json.loads()
pts = json.loads(data["Datapoints"])
# 分页用 NextToken + Length（不是 Page/PageSize）
# 时间参数必须是毫秒时间戳
```

### 元数据查询（查可用指标）

```python
from aliyunsdkcms.request.v20190101 import DescribeMetricMetaListRequest
req = DescribeMetricMetaListRequest.DescribeMetricMetaListRequest()
req.set_Namespace("acs_ecs_dashboard")
req.set_PageSize(200)
```

---

## 腾讯云（Tencent Cloud CAM）

### 环境变量

```bash
TENCENT_SECRET_ID=your_secret_id
TENCENT_SECRET_KEY=your_secret_key
TENCENT_REGION=ap-shanghai   # 你的区域，如 ap-beijing、ap-guangzhou
```

### 签名方式

TC3-HMAC-SHA256，Python 手写实现，无需腾讯云 SDK。

### CVM 监控

- **命名空间**：`QCE/CVM`
- **监控端点**：`monitor.tencentcloudapi.com`
- **实例端点**：`cvm.tencentcloudapi.com`

### 签名流程

```
1. CanonicalRequest = HTTP_METHOD + "\n" + CanonicalURI + "\n" + CanonicalQueryString + "\n" + HashedPayload
2. StringToSign = "TC3-HMAC-SHA256\n" + timestamp + "\n" + date + "\n" + hashed_canonical_request
3. Signature = TC3-HMAC-SHA256嵌套(secret_key, date, "tc3_request", StringToSign)
```

---

## 华为云（Huawei Cloud IAM）

### 环境变量

```bash
HUAWEI_ACCESS_KEY=your_access_key
HUAWEI_SECRET_KEY=your_secret_key
HUAWEI_REGION=cn-east-3   # 你的区域，如 cn-north-4、cn-south-1
```

### 认证方式

IAM Token：POST 到 `https://iam.{region}.myhuaweicloud.com/v3.0/OS-CREDENTIAL/credentials`

### 关键端点

| 用途 | 端点 |
|------|------|
| IAM Token | `https://iam.{region}.myhuaweicloud.com/v3.0/OS-CREDENTIAL/credentials` |
| ECS 列表 | `https://ecs.{region}.myhuaweicloud.com/v1/{project_id}/cloudservers` |
| 监控数据 | `https://ces.{region}.myhuaweicloud.com/V1.0/{project_id}/metric_analytics` |

### 命名空间

- ECS：`SYS.ECS`
- RDS：`SYS.RDS`
- ELB：`SYS.ELB`
