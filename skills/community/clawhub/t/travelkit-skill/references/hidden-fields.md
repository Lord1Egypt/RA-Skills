# hidden-fields ref

## 不得向用户暴露的内部字段

以下字段**永远不显示给普通用户**：

| 字段 | 说明 |
|------|------|
| `solutionId` | 航班方案内部 ID |
| `orderKey` | 订单创建密钥 |
| `externalOrderId` | 外部订单 ID |
| `confirm` | 确认标志字段 |
| `confirmProduction` | 生产环境确认字段 |
| `confirmOrderId` | 确认订单 ID |
| `confirmExternalOrderId` | 确认外部订单 ID |
| `confirmAmount` | 确认金额字段 |
| `idempotencyKey` | 幂等键 |
| 原始 `passengerIds` | 乘客内部 ID |
| 原始 `segmentIds` | 航段内部 ID |
| 内部 MCP 参数 | 所有工具调用的原始参数 |
| 原始 MCP JSON | 工具返回的原始 JSON 响应 |
| 认证 / 签名 / 内部网络细节 | API Key、签名、请求头等 |

### 可安全展示给用户的业务信息

| 类别 | 字段示例 |
|------|---------|
| 航班信息 | 完整航班号（不展示航空公司名称） |
| 路线 | 城市、机场名、IATA 代码、航站楼 |
| 时间 | 出发时间、到达时间 |
| 行程 | 飞行时长、经停次数 |
| 座位 | 舱位等级 |
| 费用 | 价格、货币单位 |
| 行李 | 行李额说明 |
| 规则 | 退改签规则（文本摘要）|
| 订单 | 订单号 |
| 支付 | 支付状态 |
| 出票 | 出票状态 |
| 文件 | 行程单文件类型 |
