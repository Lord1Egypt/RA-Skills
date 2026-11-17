---
name: xianmu-ims
description: 闲沐 IMS 智能体操作技能（单一入口，覆盖全部功能域）。当用户要初始化配置（初始化、新手指引、建分类、建位置、规划库位、开始使用）、日常管理库存（物品档案、入库、出库、移库、盘点、预警、采购、项目/BOM、供应商、库位、图片资料），或尚未安装闲沐 IMS 需要下载安装、设置 API Token 时使用——通过用户自建的闲沐 IMS 实例 MCP / REST API 完成。触发词：闲沐、IMS、库存、入库、出库、移库、盘点、预警、库存查询、初始化、引导设置、建分类、建位置、新手指引、开始使用、安装闲沐、下载闲沐、闲沐没装、激活。
version: 1.1.0
---

# 闲沐 IMS 智能体操作技能

通过用户部署的闲沐 IMS 实例（局域网/NAS/本机）的 MCP 或 REST API 操作闲沐 IMS。本技能是闲沐 IMS 智能体能力的**单一入口**，按功能域分文档维护：当前含「日常库存操作」与「初始化引导」两个域，后续新域按文末「扩充规则」并入。

## 使用前提

**步骤 0 · 连通性检测**：用户没给实例地址时，先探测默认地址 `curl -s http://127.0.0.1:8066/api/v1/health`（免认证）——返回 `"status": "up"` 即实例在线，顺手记下响应里的 `version` 与 `edition`；连不上先问用户实例地址（NAS / 远程部署很常见）再探一次；仍不通说明实例可能未安装，**不要硬问 Token**，转 [references/setup.md](references/setup.md) 走安装与接入引导。

实例可达后，向用户确认两件事（本会话内记住即可）：

1. **实例地址**（BASE，如 `http://<你的实例地址>:8066`，实例本机可用 `http://127.0.0.1:8066`）
2. **API Token**（可选但强烈建议）：用户在闲沐 IMS「设置 → API Token」新建，形如 `xmt_` 开头，明文只显示一次。Token 决定操作权限（viewer 只读 / member 可写 / admin 管理），并有每分钟 60 次限流保护。初始化引导的写入（建分类/位置）需要 **admin** Token，详见 [references/onboarding.md](references/onboarding.md)。实例未安装时的下载安装与 Token 设置引导见 [references/setup.md](references/setup.md)。

> 单人模式下实例不强制认证，无 Token 也能调用；但仍建议用户提供 Token（限流保护 + 操作审计）。

## 接入方式选择

闲沐 IMS 同时提供两种方式，同受 Token 限流约束；权益上 MCP 走 `feature.mcp`（**免费版权益内置，免费版 50 件条目内与专业版无差别**），裸 REST 走 `feature.api`（专业版权益，无权益返回 403 `EDITION_REQUIRED`）——**免费版用户优先走 MCP**，二选一即可：

- **客户端支持远程 HTTP MCP 时，优先用 MCP**：服务端原生 `BASE + /api/mcp`（Streamable HTTP），只填「实例地址 + Token」即得精选 **67 个工具**（读 21 / 写 46），零本地依赖，NAS / 远程实例同样可用。配置见文末「参考」。
- **客户端不支持（或不方便改配置）时，用本技能的 REST 方式**：即下文全部内容。

## 请求约定

- 所有接口前缀 `BASE + /api/v1`；认证用请求头 `Authorization: Bearer <Token>`。
- 成功响应是信封：`{"code": "OK", "message": "ok", "data": <业务数据>}` —— **业务数据一律从 `data` 里取**。
- 失败响应：`{"code": "<错误码>", "message": "<说明>", "details": …}`，HTTP 状态码同时给出。常见错误码：

| 错误码 | 含义 | 处理建议 |
|---|---|---|
| 连接失败（无 HTTP 响应/拒绝/超时） | 实例未启动、未安装或地址不对 | 先问实例地址重探；确认未装则按 [references/setup.md](references/setup.md) 引导安装并设置 Token |
| AUTH_REQUIRED (401) | Token 缺失/无效/已吊销 | 请用户重新创建 Token |
| FORBIDDEN (403) | 角色权限不足 | 写操作需要 member 及以上；报废（scrap）出库与初始化写入需要 admin；向用户说明 |
| EDITION_REQUIRED (403) | 无专业版权益（裸 REST / Webhook 调用） | 提示改用 MCP 工具面（免费版可用），或指引用户升级专业版 |
| LIMIT_EXCEEDED (403) | 免费版物品条目已达 50 件上限（新建档类操作） | 报告当前数量与上限；请用户删减条目或升级专业版（不限条目） |
| READONLY_MODE（仅 MCP） | 实例处于只读模式 | URL 带 `?mode=readonly` 或演示环境时写操作不可用；确认用户是否需要只读，再决定是否改用普通地址 |
| NOT_FOUND (404) | 物品/库位/任务/父节点不存在 | 换关键词重查；建子级报错多半是写入顺序错了（先建父再建子） |
| BAD_REQUEST (400) | 参数或命名冲突 | 如同级重名、同父同 code、大类缺 type、深度超限；按 message 提示修正 |
| DUPLICATE_ITEM (409) | 建档查重命中 | 向用户展示疑似重复项，确认后可用 `force: true` 强制建档 |
| OUT_OF_STOCK (409) | 库存不足 | 报告现有数量，不要擅自降低出库数 |
| IN_USE (409) | 对象仍被引用（删除时） | 分类/位置改用停用（`status="disabled"`），其余向用户说明占用方 |
| RATE_LIMITED (429) | 超过 60 次/分 | 等待几十秒重试，减少请求频率 |

- 分页统一参数 `page` / `page_size`，服务端上限 200，**建议 ≤50** 避免撑爆上下文。

## 工作流

按域路由；日常操作的细节与完整参数见 [references/api.md](references/api.md)。

### 1. 查库存
```
GET /api/v1/items?q=M3&low_stock=false&page=1&page_size=20
```
拿到列表后，需要某物品在各库位的分布再调 `GET /items/{id}/stocks`；需要流水调 `GET /stock/records?item_id={id}`。先精确后模糊：优先用型号/内部编号查询，减少分页轮次。

### 2. 入库（含建档）
- 已有物品：`POST /api/v1/stock/inbound`，body 至少给 `item_id` + `quantity`（+`total_price`、`supplier_id`、`location_id`、`remark` 按需）。
- 新物品一步到位：body 里不给 `item_id`，给 `new_item`（内联建档字段：`name`/`model`/`type`/`location_id`/`unit` 必填）+ `quantity`。
- 建档前先 `GET /items?q=<型号>` 查重，命中 `DUPLICATE_ITEM` 时把候选给用户确认。

### 3. 出库 / 移库 / 调整
- `POST /stock/outbound`：`item_id` + `quantity` + `purpose`（project/consume/scrap，scrap 需 admin）。
- `POST /stock/transfer`：`item_id` + `to_location_id`（多位置物品可加 `from_location_id`）。
- `POST /stock/adjust`：`item_id` + `counted_qty`（按实盘数调整，生成 adjust 流水）。

### 4. 盘点 / 预警
- 盘点：`GET /stocktakes` 找到进行中的任务 → `GET /stocktakes/{task_id}/lines?filter=pending` 看待盘行 → `PUT /stocktakes/{task_id}/lines/{line_id}` 录 `counted_qty`（实盘余额）。任务创建/确认/取消也有对应能力（MCP：`create_stocktake` / `confirm_stocktake` / `cancel_stocktake`；确认结案会按各行差异生成 adjust 流水，确认前先核对 diff 行）。
- 预警：`GET /alerts`（默认只回 active）→ 处理完后 `POST /alerts/{id}/acknowledge` 确认。

### 5. 图片与资料
- 加图片：`POST /items/{id}/attachments`（multipart，`file_type=image`，≤20MB）；调整顺序/封面用 `PUT /items/{id}/attachments/order`（ids 须覆盖全部附件，第一张为封面）。
- 加资料：链接用 `POST /items/{id}/docs`（后台抓取，稍后 `GET /docs?item_id=` 看结果）；本地文件用 `POST /docs/upload`（后缀白名单 pdf/docx/txt/md/png/jpg/xlsx/csv/pptx/zip 等）。
- 一份资料可关联多个物品（多对多）：改显示名用 `PATCH /docs/{doc_id}`（body `{"title": "…"}`）；追加关联用 `POST /docs/{doc_id}/items`（body `{"item_id": 123}`，幂等）；解除关联用 `DELETE /docs/{doc_id}/items/{item_id}`（资料本身保留）。注意 `GET /docs?item_id=` 的含义是「**包含**该物品的资料」，不等于唯一归属；列表行里 `items[]` 才是全部关联物品。
- 删除物品**不会**删除它名下的资料，只会解除关联（资料降级为未关联的全局资料）；资料被删除只有 `DELETE /docs/{doc_id}` 一条路径。
- 删除图片/资料均为不可恢复操作，先向用户确认再调用。

### 6. 初始化引导（分类与位置一次配好）

用户表达「初始化 / 新手指引 / 帮我建分类、建位置 / 开始使用 / 规划库位」等意图时走本域：读 [references/onboarding.md](references/onboarding.md)，严格按其中五阶段流程执行（现状检测 → 场景选择 → 场景提问 → 配置预览 → 写入执行 → 收尾），全程最多 4 问、确认后才写入、幂等可重入。场景话术见 [references/scenarios.md](references/scenarios.md)，工具签名与命名规则见 [references/mcp-tools.md](references/mcp-tools.md)。**写入需 admin Token；本域只走 MCP 工具，不直接调 REST**。

### 其他能力

采购、项目/BOM、借用、基础档案（管理员）等域 MCP 工具面已覆盖，可直接按工具签名调用；服务端 `guide` 工具内置 stock/purchase/project/docs 四域操作规范与初始化五阶段引导（仅接 MCP 未装本技能的客户端可直取）。专属域指南按文末「扩充规则」陆续并入。

## 护栏（必须遵守）

1. **写操作前先复述确认**：入库/出库/移库/调整/建档/初始化写入前，向用户复述关键内容（物品 + 数量 + 目标库位，或配置预览），得到确认再调用。用户指令已非常明确时可省略复述直接执行。
2. **禁触端点**：不要调用设置（`/settings`，含 AI 密钥）、授权（`/license`）、Token/Webhook 管理、用户管理等系统端点；也不要调用物品删除/物理删除/并库/停用（`DELETE /items/{id}`、`/purge`、`/merge`、`/disable`）——这些留给用户在界面操作。
3. **出错不删数据**：有流水的物品不可删除只能停用；写错了提示用户在界面用「冲正」功能回退，Agent 不要自行尝试补救性反向操作。
4. **一次一步**：批量写入逐条执行，每条之间检查响应；某条失败（如 OUT_OF_STOCK）就停下报告，不要跳过继续。
5. **数量与单位照抄用户口径**，不主动换算；价格字段留 0 表示未计价。
6. **不编造工具与参数**：只用本文档和 references 列出的工具与端点，不确定就先查再调。
7. **不外发**：用户的回答与实例数据只用于操作当前实例，不发送到任何外部服务。

## 扩充规则（新功能域如何并入本技能）

本技能是闲沐 IMS 智能体能力的唯一入口，后续新功能域按以下固定流程并入：

1. **新增域文档**：`references/` 下新建域文档（如 `references/procurement.md`），细节全下放；「工作流」节加 2~5 行摘要 + 指针。
2. **触发词**：description 补该域触发词（整段控制在 ~500 字符内），只增不删。
3. **护栏**：域专属护栏写进域文档；全局性护栏并入本文「护栏」节。
4. **行数纪律**：本文正文 ≤ 200 行；域文档超 ~150 行或自成多轮体系时，评估升格为独立技能。
5. **版本递增**：新增域/功能章节 → 次版本 +1；话术与参考修正 → 修订号 +1；结构性重构/不兼容 → 主版本 +1。每次变更在「版本记录」表加一行。
6. **红线**：示例地址一律占位符（发布门禁拦截内网 IP / 个人绝对路径）；工具面以服务端 `mcp_server.py` 为准；不整抄官网 api.html；文件保持 CRLF + UTF-8 无 BOM。
7. **双源同文**：本技能的工作流要点与初始化话术，和服务端 `guide` 工具的话术常量（`server/app/core/guide_script.py`）同源维护——修改任一侧须同步另一侧。

## 版本记录

| 版本 | 日期 | 变更摘要 |
|---|---|---|
| 1.0.0 | 2026-09-29 | 基线：合并原 `xianmu-ims`（日常操作）与 `xianmu-ims-init`（初始化引导）为单一技能；初始化引导流程移至 references/onboarding.md；确立「单技能 + 分域文档」架构与扩充规则 |
| 1.0.1 | 2026-09-29 | 增补：仅接 MCP 的客户端可调服务端 `guide` 工具获取同款引导与各域操作规范（双源同文义务入扩充规则）；修正盘点工作流表述（任务创建/确认/取消已有 MCP 工具） |
| 1.0.2 | 2026-09-29 | 修正：初始化引导「全新库」判定改为只看物品总数——出厂种子分类/位置是系统默认初始化内容，不作为已配置判据（与 `guide_script.py`、官网 skill.md 三处同文） |
| 1.0.3 | 2026-09-30 | 口径更新（配套产品 v1.88.0 / 10 号 v3.2.1）：MCP 免费放开——权益总述与参考区改双键口径（MCP 查 `feature.mcp` 免费可用、裸 REST 维持 `feature.api` 专业版），免费版优先引导走 MCP；错误码表补 `LIMIT_EXCEEDED`（免费版 50 条目上限）行、`EDITION_REQUIRED` 行改 REST 专属 |
| 1.0.4 | 2026-10-01 | 参考修正（配套产品 v1.90.0）：mcp-tools.md 的 `search_items` 参数说明补 `series` 支持逗号分隔多值（产品端系列筛选多选） |
| 1.0.5 | 2026-10-07 | 口径订正（配套官网 skill.md v1.0.1 三处同步）：onboarding.md 的 Token 前提与 `FORBIDDEN` 处置改「Token 权限跟随创建账号（创建时无角色选择），需管理员账号登录后创建/重建」 |
| 1.1.0 | 2026-10-12 | 新增「安装与接入引导」域（配套官网 skill.md 同源）：使用前提加步骤 0 连通性检测（`/api/v1/health` 免认证探测，未装不硬问 Token 转引导）；新增 references/setup.md（检测 → Windows 安装话术 → 用户亲手建 Token → 验证接入 → 激活码/AI 密钥分支 → 连接层错误对照）；错误码表补「连接失败」行；description 补安装类触发词 |

## 参考

- [references/setup.md](references/setup.md) —— 安装与接入引导（实例未安装/未运行时：连通性检测、Windows 安装话术、用户亲手建 Token、验证接入、激活码/AI 密钥分支）
- [references/api.md](references/api.md) —— REST 完整端点速查（参数/请求体/响应示例）
- [references/onboarding.md](references/onboarding.md) —— 初始化引导五阶段流程（分类与位置配置）
- [references/scenarios.md](references/scenarios.md) —— 初始化 7 场景模板（提问话术 + 分类/位置模板 + 默认值）
- [references/mcp-tools.md](references/mcp-tools.md) —— 初始化域 MCP 工具签名、返回结构与命名规则（10 工具子集）
- 机器可读接口定义：`GET BASE/api/openapi.json`（Swagger UI：`BASE/api/docs`）
- 变更感知：库存/预警/采购事件可由用户在「设置 → Webhook」订阅（HMAC 签名推送），适合接 n8n 等自动化平台
- 原生 MCP 接入：服务端 `BASE + /api/mcp`（Streamable HTTP），**已上线**（`feature.mcp` 权益，免费版权益内置——免费版 50 件条目内全量可用，超限返回 `LIMIT_EXCEEDED`）——请求头同样填 `Authorization: Bearer xmt_…`；URL 追加 `?mode=readonly` 即进入只读模式（写工具调用返回 `READONLY_MODE`），演示环境自动强制只读。工具面 67 个（读 21 / 写 46），覆盖查询、出入库、移库、盘点任务、预警、项目库与 BOM、采购、借用、基础档案（管理员）与图片资料管理；`guide` 工具可下发各域操作规范与初始化引导；不含物品删除/并库/项目删除/设置类端点
