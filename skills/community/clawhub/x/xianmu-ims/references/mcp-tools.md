# MCP 工具速查（初始化引导域配套）

与闲沐 IMS v1.85.0 服务端实际工具面逐一核对（2026-09-29）。

本文件只列初始化引导用到的 10 个工具（读 4 / 写 6）；全量 67 工具面（读 21 / 写 46，含 guide 操作规范引导）见根 SKILL.md「参考」节。

## 连接与权限

- MCP 端点：`BASE + /api/mcp`（Streamable HTTP）；请求头 `Authorization: Bearer <xmt_…>`。
- 列表工具返回 `{total, list}`（分页的为 `{total, page, page_size, list}`）——**不要**解包裸数组。
- 业务错误以 `{"error": {"code": "…", "message": "…"}}` 返回（不抛异常）。
- 角色门槛：读工具 viewer 即可；create/update/delete 分类与位置需要 **admin**。
- 限频 60 次/分钟，按 Token 计。

## 读工具（4）

| 工具 | 签名 | 用途 |
|---|---|---|
| search_items | `search_items(q=None, type=None, category_id=None, location_id=None, tag=None, low_stock=False, status=None, series=None, sort=None, page=1, page_size=20)` | 只为取 `total`（物品总数），建议 `page_size=1`；`series` 支持逗号分隔多值（`series="胶水,螺丝"` 命中任一） |
| list_categories | `list_categories()` | 分类现状；行含 `id/parent_id/type/name/sort/status/item_count` |
| list_locations | `list_locations()` | 位置树；行含 `id/parent_id/level/code/name/path/status/storage_notes/children`；`total` 只数顶层区 |
| list_custom_fields | `list_custom_fields()` | 收尾提示时参考（MCP 不能写自定义字段） |

## 写工具（6，均 admin）

| 工具 | 签名 | 关键约束 |
|---|---|---|
| create_category | `create_category(name, parent_id=None, type=None, sort=0)` | parent_id 缺省＝建大类（必须传 type）；给 parent_id＝建子分类（类型随父级，仅两级）；同级重名 → `BAD_REQUEST` |
| update_category | `update_category(category_id, name=None, sort=None, status=None)` | status ∈ active/disabled；同级重名拒绝 |
| delete_category | `delete_category(category_id)` | 有子分类或被物品引用 → `IN_USE` |
| create_location | `create_location(code, parent_id=None, name=None, level=None, storage_notes=None)` | parent_id 缺省＝顶层区；层级按父节点自动推导（区→柜→格），**不要传 level**；同父同 code → `BAD_REQUEST`；path 自动拼接 |
| update_location | `update_location(location_id, name=None, storage_notes=None)` | code 与层级结构不可改；storage_notes 传空串清除 |
| delete_location | `delete_location(location_id)` | 有子位置或被物品引用 → `IN_USE` |

## 错误码

| code | HTTP | 含义与处置 |
|---|---|---|
| AUTH_REQUIRED | 401 | Token 缺失/无效/已吊销 → 请用户重建 |
| FORBIDDEN | 403 | 非 admin 调写工具 → 指引「设置 → API Token」换管理员 Token |
| LIMIT_EXCEEDED | 403 | 免费版物品条目已达 50 件上限（新建档类操作）→ 删减条目，或指引用户到 https://ims.miaoking.com/portal/buy 购买专业版（不限条目；错误消息自带此链接） |
| EDITION_REQUIRED | 403 | 裸 REST / Webhook 无专业版 feature.api 权益（MCP 不受此限，免费版权益内置 feature.mcp）→ 改走 MCP 或升级/客服指引 |
| READONLY_MODE | — | URL 带 `?mode=readonly` 或演示环境 → 写不可用 |
| NOT_FOUND | 404 | parent_id 不存在（多半是写入顺序错了：先建父再建子） |
| BAD_REQUEST | 400 | 同级重名 / 同父同 code / 大类缺 type / 深度超限 |
| IN_USE | 409 | 删除被引用对象 → 改停用（`update_category(status="disabled")`） |
| RATE_LIMITED | 429 | 超过 60 次/分 → 等几十秒重试 |

## 命名规则（初始化引导约定）

### 分类 type 码

- 语义命中复用：设备/仪器/工具类 → DEV；零件/元件/配件类 → PRT；消耗品类 → CON。
- 其余自定义大类从 X1 起递增（先 `list_categories()` 收集已占用 type，避开之）；码规则：大写字母数字、2~8 位（与网页端「设置 → 自定义大类」一致）。type 只影响内部编号前缀（如 X1-000012）。

### 位置 code

- 区：单字母 A/B/C…；种子已占用 A（默认区域）——首个场所改名复用 A，新场所从 B 起。
- 柜：两位序号 01/02…（在所属区内递增）。
- 格：两位序号 01/02…（在所属柜内递增）。
- code 仅需同级唯一，≤32 字符；name ≤64 字符；path 服务端自动拼（如 `/B/01/03`）。

### 上限

- 新增后大类 ≤ 10；位置节点 ≤ 15；层级 ≤ 3（bin 下不可再挂子节点）。
- 一次初始化调用量约 20~40 次，低于限频阈值。
