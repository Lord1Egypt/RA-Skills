# `strategy` 参考（决策树 / 槽位抽取 / serverType 路径）

本文件为 **Smartbi CLI Skill** 的附属参考；流程性 MUST 以上级 `SKILL.md` 为准。

## Fast Path Decision Tree

1. 已有明确失败信息（报错/状态码/失败日志）→ `diagnose`
2. 唯一 `operationKey` 但参数未确认 → `contract`
3. 唯一 `operationKey` 且参数齐全 → `execute`
4. 无 `operationKey` 或仅业务目标表达 → `discover`
5. `discover` 出现多候选 → 先让用户选择再进入 `contract`

## Slot Extraction（业务语义抽取）

当用户未显式提供接口名时，先抽取以下槽位：

| 槽位 | 含义 | 映射到 describe 输出 | 示例 |
|------|------|---------------------|------|
| `action` | 业务动作 | 匹配 operationId 动词部分 | 训练/分析/查询/导出/发布 |
| `resource` | 业务对象 | 匹配 domain 或 requestBody 关键字段 | 模型资源/数据集/报表主题 |
| `dims` | 维度 | `requestBodySchema` 中 `mql.dims` | 分支行/年月/产品名称 |
| `metrics` | 指标 | `requestBodySchema` 中 `mql.metrics` | 销售额/贷款余额/转化率 |
| `filters` | 过滤条件 | `requestBodySchema` 中 `dimFilter`/`metricFilter` | 区域=华东/近30天/余额>100万 |
| `sort` | 排序 | `requestBodySchema` 中 `mql.sort` | 按销售额降序 |
| `limit` | 行数 | `requestBodySchema` 中 `mql.limit` | 前10/前100 |
| `time_range` | 时间范围 | 转化为 `dimFilter` SQL 表达式 | 去年→`"年份 = '2025'"` |

把槽位拼成 2-3 组关键词，配合 `smartbi list --domain <domain> --agent` 收敛（search 仅作 list 的补充回退）。

## 槽位缺失处理

| 缺失槽位 | 处理策略 |
|---------|---------|
| `action` 未知 | 让用户补充要做什么（查/导出/创建等） |
| `resource` 未知 | 从上下文推断，或 `list --agent` 全量重排让用户选 |
| `dims`/`metrics` 未知 | 调用 `getDataModelTrees` 列出字段，让用户指定 |
| `filters` 未知 | 若用户未提过滤语义，可省略，不影响主查询 |
| `modelId` 未知 | 调用 `listCatalogElementsByResourceType` 列出可用模型，让用户选择 |

## serverType 路径差异

两种 `serverType` 的 API 路径格式不同，影响 Rhino 脚本内 HTTP 调用及 `smartbi call` 行为：

| `serverType` | 配置 `baseUrl` 示例 | 实际请求路径（queryDataByMql） |
|-------------|-------------------|-------------------------------|
| `smartbi` | `http://host/smartbi` | `http://host/smartbi/api/v1/datamodel/datamodel/query-data-by-mql` |
| `sdk-server` | `http://host:8086` | `http://host:8086/api/v1/datamodel/datamodel/query-data-by-mql` |

关键差异：
- `smartbi` 模式下 `baseUrl` 本身含 `/smartbi` 路径前缀，拼接后完整路径含两个层级
- `sdk-server` 模式部分接口路径中 domain 重复（`datamodel/datamodel`），需注意区分
- 使用 `smartbi call` CLI 时无需手动拼路径（CLI 内部处理前缀），但若在 Rhino/JS 脚本中直连 HTTP 需按 serverType 构造完整 URL

## 诊断决策树（Phase 4 扩展）

```
失败响应
  ├─ HTTP 4xx
  │   ├─ 401 AUTH_FAILED    → token 无效 → 让用户重新申请
  │   ├─ 403 FORBIDDEN      → 无权限 → 查 describe 中 x-funcPerm
  │   ├─ 404 path not in spec → serverType/baseUrl 配置不匹配
  │   └─ 400 INVALID_ARGUMENT → describe --agent 对照必填字段逐一检查
  ├─ HTTP 5xx
  │   ├─ 500               → 记录 tid，对照 describe --include-raw-schema
  │   ├─ 502/503           → 服务不可达，等 UPSTREAM_UNAVAILABLE 恢复后重试
  │   └─ 429               → 限流，退避后重试（CLI 内置处理）
  ├─ 网络类
  │   ├─ NETWORK_TIMEOUT   → baseUrl 错误或网络不通
  │   └─ NETWORK_ERROR     → DNS/代理/防火墙问题
  └─ 业务错误（200 但 data.success=false）
      └─ 读 data.error/data.message，对照本 skill 错误速查表
```
