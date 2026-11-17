# 闲沐 IMS 精选端点速查

与 `SKILL.md` 配套。所有路径相对 `{BASE}/api/v1`；认证头 `Authorization: Bearer <xmt_…>`。
所有 JSON 响应包在 `{"code":"OK","message":"ok","data":…}` 中，**业务数据在 `data`**。
以下端点与闲沐 IMS v1.77.0 实际路由逐一核对（2026-09-27）。

通用约定：
- 分页参数 `page`（默认 1）/ `page_size`（建议 ≤50，服务端上限 200）；列表返回 `{total, page, page_size, list}`。
- 角色要求：读 = viewer，写 = member，「报废」出库 = admin。Token 即用户角色。
- 日期参数格式支持 `YYYY-MM-DD` 或 `YYYY-MM-DD HH:MM:SS`。

## 读操作（viewer）

### GET /items — 物品列表/搜索
Query：`q`（关键词：内部编号精确→型号前缀→全文）、`type`、`category_id`、`location_id`、`tag`、`status`（默认 active）、`low_stock=true`、`supplier`、`series`、`sort`、`page`、`page_size`。

`list` 内物品对象关键字段：`id`、`internal_id`（如 PRT-000123）、`name`、`model`、`series`、`type`、`quantity`（当前总量）、`safety_stock`、`unit`、`location_id`、`location_path`（如 A1-B2-3 库位链）、`brand`、`supplier_id`、`tags`、`status`、`last_cost`、`avg_cost`、`params`、`thumbnail`。

```
curl -s -H "Authorization: Bearer $XMT" "$BASE/api/v1/items?q=M3%E8%9E%BA%E4%B8%9D&page=1&page_size=20"
```

### GET /items/{id} — 物品详情
在列表字段基础上增加：`description`、`batch_no`、`serial_no`、`calib_date`、`expiry_date`、`low_stock`，以及 `attachments[]`（图片/资料附件）、`active_alerts[]`（活跃预警）、`has_datasheet`、`thumbnail`。

### GET /items/{id}/stocks — 多位置库存分布
返回该物品在各库位的余额列表（含 `location_id`、`location_path`、`quantity`）。

### GET /stock/records — 全局库存流水
Query：`item_id`、`type`（`inbound` / `outbound` / `adjust` / `transfer_in` / `transfer_out` / `borrow_out` / `borrow_return` / `reversal`）、`operator_id`、`project_id`、`date_from`、`date_to`、`page`、`page_size`。
流水行字段：`id`、`item_id`、`type`、`quantity`、`balance_after`、`location_id`、`project_id`、`operator_id`、`occurred_at`、`remark`。

### GET /items/{id}/stock-records — 单物品流水
Query 同上（无 `item_id`）。

### GET /categories — 分类列表
### GET /locations/tree — 库位树（含层级 path）
### GET /suppliers — 供应商列表

### GET /alerts — 预警列表
Query：`status`（默认 `active`；可传 `acknowledged`/`resolved`/空=全部）、`type`（如 low_stock）、`page`、`page_size`。
行字段：`id`、`item_id`、`type`、`level`、`status`、`triggered_at`、`meta`，并附带 `item`（id/internal_id/name/model/quantity/unit/safety_stock）。

### GET /stocktakes — 盘点任务列表
Query：`status`（如 in_progress/confirmed/cancelled）、`page`、`page_size`。
任务字段：`id`、`name`、`location_id`、`location_path`、`status`、`line_total`、`counted_lines`、`diff_lines`、`created_at`、`confirmed_at`。

### GET /stocktakes/{task_id}/lines — 盘点行
Query：`filter`（`pending`=待盘 / `counted`=已盘 / `diff`=有差异 / 缺省=全部）、`page`、`page_size`。
行字段：`id`、`item_id`、`internal_id`、`name`、`model`、`unit`、`location_path`、`book_qty`（账面）、`counted_qty`（实盘）、`diff`、`status`。响应同时带 `task`（任务汇总）。

## 写操作（member）

### POST /items — 建档（201）
必填：`name`、`model`、`type`（如 PRT/TOOL，存大写截 8 字）、`location_id`、`unit`。
常用可选：`quantity`（期初数量，>0 生成 0 元期初入库流水）、`safety_stock`、`series`、`category_id`、`brand`、`params`（JSON 参数）、`package`、`description`、`supplier_id`、`purchase_url`、`tags`（字符串数组）、`custom_data`、`remark`、`batch_no`、`serial_no`、`calib_date`/`expiry_date`（YYYY-MM-DD）。
查重：同平台来源或同型号+类型已存在 → 409 `DUPLICATE_ITEM`，确认非重复后加 `"force": true` 强制建档。

```bash
curl -s -X POST "$BASE/api/v1/items" \
  -H "Authorization: Bearer $XMT" -H "Content-Type: application/json" \
  -d '{"name":"M3×8 内六角螺丝","model":"M3x8","type":"PRT","location_id":12,
       "unit":"颗","quantity":200,"safety_stock":50,"tags":["紧固件"]}'
```

### PUT /items/{id} — 全量更新档案
请求体与建档相同（全量字段语义：未传的可选字段会被清空，注意携带用户要保留的字段）。安全库存变化会自动重算库存预警。`last_cost` 仅在显式携带时生效。

### POST /stock/inbound — 入库
必填：`quantity`；物品二选一：`item_id`，或 `new_item`（建档字段同 POST /items，一次完成建档+入库）。
可选：`total_price`（本批总价，用于移动加权成本）、`shipping_fee`、`supplier_id`、`order_no`、`location_id`（入库到指定位置，缺省主位置）、`occurred_at`、`remark`。

```bash
curl -s -X POST "$BASE/api/v1/stock/inbound" \
  -H "Authorization: Bearer $XMT" -H "Content-Type: application/json" \
  -d '{"item_id":34,"quantity":100,"total_price":25.8,"supplier_id":3,"location_id":12,"remark":"补货"}'
```

### POST /stock/outbound — 出库
必填：`item_id`、`quantity`、`purpose`（`project`=项目领用 / `consume`=消耗 / `scrap`=报废，报废需 admin，可带 `project_id`）。
库存不足 → 409 `OUT_OF_STOCK`。

### POST /stock/transfer — 移库
必填：`item_id`、`to_location_id`。可选：`from_location_id`（多位置物品指定从哪个位置搬，缺省按主位置语义）。

### POST /stock/adjust — 按实盘调整
必填：`item_id`、`counted_qty`（实盘数，生成 adjust 流水补平差异）。可选：`remark`。

### POST /alerts/{id}/acknowledge — 确认预警
仅 `active` 状态可确认，否则 409 `CONFLICT`。

### PUT /stocktakes/{task_id}/lines/{line_id} — 录入实盘数
Body：`{"counted_qty": 123}`（不能为负）。返回 `{id, status, diff, counted_lines, diff_lines}`。

## 图片与资料（member）

### POST /items/{id}/attachments — 上传图片/文件
multipart 表单：`file`（≤20MB，BR-13）+ `file_type`（image/datasheet/other）。返回附件对象（含 `id`、`sort`、`url`、`thumbnail`）。

```bash
curl -s -X POST "$BASE/api/v1/items/34/attachments"   -H "Authorization: Bearer $XMT" -F "file=@板子.png" -F "file_type=image"
```

### PUT /items/{id}/attachments/order — 附件重排
Body `{"ids":[附件id…]}`，**必须与该物品现有全部附件一一对应**；列表第一张图片即封面。

### DELETE /attachments/{att_id} — 删除附件
磁盘文件同删，不可恢复；调用前先向用户确认。

### POST /items/{id}/docs — 添加资料链接
Body `{"url":"…"}`（自动补 https://）。服务端后台抓取正文转 markdown 存档，返回 `status:"fetching"` 的资料，稍后 `GET /docs?item_id=` 查看结果。

### POST /docs/upload — 上传资料文件
multipart 多文件 + 可选 `item_id`。后缀白名单：pdf/docx/doc/txt/md/markdown/png/jpg/jpeg/webp/gif/xlsx/xls/csv/pptx/zip，≤20MB；上传即 `ready`。

### GET /docs?item_id=&q=&page= — 资料列表/搜索
`item_id` 过滤「**包含**该物品的资料」（资料与物品为多对多，不是唯一归属）；`q` 支持标题与正文关键词。响应在 `{total, page, page_size, list}` 之外还有 `counts`（按来源/状态分组的角标数，随当前筛选口径）。行字段：`id`、`title`、`items[]`（全部关联物品，元素 `{id, name, internal_id}`）、`item_id` / `item_name`（取最早一条关联，兼容旧客户端的派生字段）、`source_type`（url/file）、`status`（fetching/ready/failed）、`ai_status`、`cover_url`、`char_count`。

### PATCH /docs/{doc_id} — 重命名资料
Body `{"title":"新名称"}`（不能为空）。只改显示名，来源文件名与原文/整理内容不动，返回更新后的资料行。

### POST /docs/{doc_id}/items — 资料关联到物品
Body `{"item_id":123}`；幂等（重复关联直接返回现状）。一份资料可关联多个物品，关联后该物品详情页的资料列表即包含它，返回更新后的资料行（含 `items[]`）。

### DELETE /docs/{doc_id}/items/{item_id} — 解除资料与物品的关联
只解除关联，**资料本身保留**；解除后不再关联任何物品时成为未关联的全局资料。

### DELETE /docs/{doc_id} — 删除资料
文件类同清落盘，不可恢复。另注：删除**物品**不会连带删除它名下的资料，只解除关联（资料降级为全局资料）——所以删物品后资料仍可用 `GET /docs?q=` 找到。

## 明确不碰的端点

以下端点与本技能无关，**不要调用**：
- 物品删除类：`DELETE /items/{id}`、`POST /items/{id}/purge`、`POST /items/purge-batch`、`POST /items/{id}/merge`、`POST /items/{id}/disable`
- 系统管理：`GET/PUT /settings`（含 AI 密钥）、`/license/*`、`/api-tokens*`、`/webhooks*`、`/notify/*`、用户管理
- 流水冲正：`POST /stock/records/{id}/reversal` —— 写错了请用户在界面操作冲正
