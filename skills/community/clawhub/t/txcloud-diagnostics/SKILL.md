---
name: txcloud-diagnostics
description: 用于腾讯云云产品异常诊断。当用户反馈腾讯云相关的任何异常、产品/实例不可用等情况时，根据反馈的实例和异常信息，自动拉取监控等数据进行分析诊断，输出原因和建议。
---

# 腾讯云云产品诊断

**⚠️ 所有脚本在 skill 目录下执行**：先 `cd skills/txcloud-diagnostics/`

## 诊断流程

### Step 1: 预获取

1. 从对话提取**产品类型、实例 ID、地域、问题现象、问题时间段**（地域和问题时间段缺失必须追问，不得猜测）
2. **通过实例 ID 前缀识别产品**（见下方 ID 前缀表），再查**产品路由表** → **必须先 read 对应 profile 文件**，从中获取 namespace、dimension-key、核心指标。**禁止凭记忆填写 namespace/dimension-key，必须从 profile 文件中读取**
3. **跨产品场景**（如"A 访问 B 超时/报错"）：**优先诊断被访问方 B**，诊断完 B 后若未找到原因再诊断 A。一次只诊断一个产品
4. 结合 profile 指标决策表 + 用户问题现象，预选 3~8 个诊断指标
5. 执行：

```bash
python3 scripts/prefetch.py --instance-id <id> --product <product> \
  --region <region> --namespace <namespace> --dimension-key <dim-key>
```

- `status: "ok"` → 进 Step 2
- `status: "auth_failed"` → 执行凭证授权（见下方），成功后重试
- `status: "error"` → 根据 message 提示用户

### Step 2: 执行诊断

```bash
python3 scripts/diagnose.py \
  --instance-id <id> --region <region> \
  --namespace <namespace> --dimension-key <dim-key> \
  --metrics '<指标1,指标2,...>' \
  --problem-start '<ISO8601+08:00>' --problem-end '<ISO8601+08:00>'
```

可选：`--pad-before`/`--pad-after`（默认15分钟），`--extra-dims`（CCN 等多维度产品必传）。

**时间处理**：用户说的时间默认为 **北京时间（UTC+8）**，直接用 `+08:00` 后缀。例：用户说"19点左右" → `--problem-start '2026-03-28T18:30:00+08:00' --problem-end '2026-03-28T19:30:00+08:00'`。**不要做 UTC 转换**。

指标选择优先用 profile 决策表，通用匹配：慢→latency、错误→error/fail、流量→traffic/bandwidth、连接→conn。

**输出规范**：**全流程禁止输出中间思考/排查过程**。用户只看到以下内容：

- **需要授权时**：只输出授权链接 + "请点击登录授权并回复验证码"，不要解释为什么需要授权、不要暴露 tccli 报错信息
- **诊断进行中**：不输出任何内容（静默执行），不要说"让我先..."、"正在读取..."、"prefetch 成功"等
- **诊断完成后**：只输出最终报告，格式如下：

```
📋 诊断结论：<一句话结论>

| 实例 | 指标1 | 指标2 | ... | 状态 |
|------|-------|-------|-----|------|
| xxx  | 数据  | 数据  | ... | ✅/❌ |

建议：
1. <具体可执行动作>
2. <具体可执行动作>
```

**禁止**：输出思考过程、暴露 tccli/脚本报错细节、重复展示同一数据、编造未查证的信息

### 诊断失败自纠

当 diagnose.py 返回失败（API错误或数据为空）时，**不要直接报错放弃**，按以下顺序自主尝试（**总耗时不超过 10 分钟**，超时如实告知用户当前进展和失败原因）：

1. **namespace 不对** → 用 tccli 查实际可用的 namespace：
   ```bash
   tccli monitor DescribeBaseMetrics --cli-unfold-argument --region <region> --Namespace <当前namespace> --output json
   ```
   如果返回 0 个指标，换同产品的其他已知 namespace 重试（如 TDSQL-C：`QCE/CYNOSDB_MYSQL` ↔ `QCE/TDMYSQL`）

2. **实例 ID 格式不对** → 用户给的可能是集群 ID 而非实例 ID，通过产品 API 查询实际实例：
   ```bash
   tccli cynosdb DescribeClusterInstanceGrps --region <region> --ClusterId <集群ID> --output json
   ```
   从返回的 `InstanceSet` 中取 `InstanceId`（如 `cynosdbmysql-ins-xxx`）

3. **dimension-key 不对** → 从 DescribeBaseMetrics 返回的 `MetricSet[0].Dimensions` 中确认实际维度名

4. **指标名不对** → 从 DescribeBaseMetrics 返回的 `MetricSet` 中确认实际可用的指标名（注意大小写）

5. **数据为空但无报错** → 该时间段确实没有监控数据（实例空闲/新建/已停机），如实告知用户

---

## 凭证授权

当 prefetch.py 返回 `auth_failed` 时执行：

```bash
nohup python3 -u scripts/tccli_auth_daemon.py > /tmp/tccli_daemon.log 2>&1 &
sleep 5 && cat /tmp/tccli_daemon.log && cat /tmp/tccli_auth_link.txt
```

提取链接生成超链接发给用户一键点击登录。提示用户回传验证码（一段 `eyJ...` 开头的 base64 长字符串）
**授权环节只对用户输出**：授权链接 + "请点击登录并回复验证码"。**不要输出** auth_failed 原因、tccli 配置状态、credential 为空等内部信息。
将用户回复的base64 长字符串内容完整写入 `/tmp/tccli_auth_input_code.txt`
```bash
echo '<用户回复的验证码>' > /tmp/tccli_auth_input_code.txt
sleep 5 && cat /tmp/tccli_daemon.log
```

日志出现 `AUTH_SUCCESS` 即成功，重新执行 Step 1。

---

## 产品路由表

| 产品关键字 | Profile |
|------------|---------|
| cvm、云服务器、lighthouse、轻量应用、cdh | `scripts/product_profiles/compute.md` |
| tke、容器、tcr | `scripts/product_profiles/container.md` |
| scf、云函数、tcb、云开发 | `scripts/product_profiles/serverless.md` |
| ckafka、kafka、tdmq、rabbitmq、cmq、rocketmq、pulsar | `scripts/product_profiles/mq.md` |
| apigateway、api网关、tse、tsf | `scripts/product_profiles/microservice.md` |
| cbs、cos、cfs、chdfs、goosefs、cls、日志、ci | `scripts/product_profiles/storage.md` |
| clb、负载均衡、nat、vpn、dc、专线、ccn、云联网 | `scripts/product_profiles/network.md` |
| cdb、mysql、cynosdb、tdsql、mariadb、dcdb、postgres、sqlserver、mongodb、redis、memcached、keewidb | `scripts/product_profiles/database.md` |
| es、elasticsearch、emr、oceanus、dlc、cdw | `scripts/product_profiles/bigdata.md` |
| cdn、ecdn、gaap、edgeone、ecm | `scripts/product_profiles/cdn.md` |
| live、直播、vod、waf、cfw、ddos | `scripts/product_profiles/media_security.md` |

### 实例 ID 前缀速查

| 前缀 | 产品 | product 参数 |
|------|------|-------------|
| `ins-` | CVM | cvm |
| `lhins-` | Lighthouse | lighthouse |
| `cdb-` | CDB MySQL | cdb |
| `cynosdbmysql-` | TDSQL-C MySQL | tdsql-c |
| `tdsql-` / `tdsqlshard-` | TDSQL / DCDB | tdsql |
| `postgres-` | PostgreSQL | postgres |
| `mssql-` | SQL Server | sqlserver |
| `crs-` | **Redis** | redis |
| `cmgo-` | MongoDB | mongodb |
| `keewidb-` | KeeWiDB | keewidb |
| `lb-` | CLB | clb |
| `ckafka-` | CKafka | ckafka |
| `es-` | Elasticsearch | es |
| `emr-` | EMR | emr |

---
其它实例id搜索参考 [腾讯云官网](https://cloud.tencent.com/document/product)

## tccli 注意事项

- **参数格式**：`tccli <service> <Action> --cli-unfold-argument --ParamName value`（注意 `--cli-unfold-argument`）
- **管道解析 JSON 不稳定**：优先用 `> /tmp/xxx.json` 保存文件再用 Python 读取，**不要用 `| python3`**
---

## 约束

- **单次诊断总耗时不超过 10 分钟**（含自纠重试），超时立即输出已有结论并告知用户
- 监控数据仅保留 **15 天**，时间格式 ISO 8601 + 时区
- **严禁编造数据**。获取失败或为空如实告知，不确定标注"未确认"
- **禁止无限循环**：同一操作（如 tccli 命令）最多重试 2 次，2 次仍失败则输出错误信息并停止
- **tccli 命令失败时**：不要反复猜测参数格式，改用 prefetch.py / diagnose.py 脚本完成诊断
- **过程中禁止自己创建新脚本、直接修改原脚本等操作**
