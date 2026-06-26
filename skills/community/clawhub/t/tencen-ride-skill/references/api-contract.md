# 腾讯出行接口待确认项

当前 skill 的可执行入口已经统一为 `python3 ./scripts/tms_takecar.py`（路径相对于 SKILL.md 所在目录）。

## Python 脚本接口

### 命令入口

```bash
python3 ./scripts/tms_takecar.py <subcommand> [options]
```

### 默认请求参数（HTTP）

- 默认 API Base URL：`https://test.weixin.go.qq.com`
- 所有实际 HTTP 请求都会自动注入以下 body 固定字段：
	- `seqId`: 动态生成（数字字符串，用于请求链路追踪）
	- `timestamp`: 动态生成（当前毫秒时间戳）
	- `wxAppId`: `wx65cc950f42e8fff1`
	- `token`: 来自 `~/.config/tms-takecar/env.json` 的 `token` 字段（由 `save-token` 持久化）

### 鉴权错误码约定

- 当接口返回以下任一错误码时，统一按 token 缺失或无效处理，并返回退出码 `1`：
	- `errCode = 10`
	- `errCode = 35`

### 子命令

所有子命令出现非 `0` 退出码时，统一按 [异常处理流程](./error_handling.md#error-handling-main) 执行，不在调用点自行扩展处理分支。
<a id="preflight"></a>
1. `preflight` <a id="cmd_preflight"></a>
	- 作用：检查 Python 运行环境、`TMS_SKILL_TOKEN` 与常住城市是否就绪
	- 输入：无
	- 输出：JSON，包含 `python_ok`、`python_version`、`platform`、`token_present`、`resident_city`、`resident_city_present`、`next_actions`
	- 退出码：
	  - `0`：`next_actions` 仅包含 `ready`
	  - `1`：存在缺失项（如 `setup_token`、`setup_resident_city`）

2. `save-token <token>` <a id="cmd_save_token"></a>
	- 作用：将 `TMS_SKILL_TOKEN` 持久化到 `~/.config/tms-takecar/env.json`
	- 输入参数：
	  - 位置参数 `token`：要保存的 token
	  - 可选参数 `--config-file`：显式指定配置文件路径，默认 `~/.config/tms-takecar/env.json`
	- 成功输出：JSON，包含 `saved`、`config_file`
	- 退出码：`0`

3. `delete-token` <a id="cmd_delete_token"></a>
	- 作用：从 `~/.config/tms-takecar/env.json` 清空本地保存的 `TMS_SKILL_TOKEN`
	- 输入参数：
	  - 可选参数 `--config-file`：显式指定配置文件路径，默认 `~/.config/tms-takecar/env.json`
	- 成功输出：JSON，包含 `deleted`、`config_file`
	- 退出码：`0`

4. `set-resident-city <city_name>` <a id="cmd_set_resident_city"></a>
	- 作用：写入或更新常住城市
	- 输入参数：
	  - 位置参数 `city_name`：常住城市名称，推荐完整格式（如 `北京市`）
	  - 可选参数 `--env-file`：显式指定 env 配置文件路径，默认 `~/.config/tms-takecar/env.json`
	- 成功输出：JSON，包含 `updated`、`resident_city`、`env_file`
	- 退出码：
	  - `0`：成功
	  - `2`：参数错误（如空城市）

5. `get-resident-city` <a id="cmd_get_resident_city"></a>
	- 作用：读取常住城市
	- 输入参数：
	  - 可选参数 `--env-file`：显式指定 env 配置文件路径，默认 `~/.config/tms-takecar/env.json`
	- 成功输出：JSON，包含 `resident_city`、`resident_city_present`、`env_file`
	- 退出码：`0`

6. `delete-state` <a id="cmd_delete_state"></a>
	- 作用：删除 `~/.config/tms-takecar/state.json`
	- 输入参数：
	  - 可选参数 `--state-file`：显式指定状态文件路径，默认 `~/.config/tms-takecar/state.json`
	- 成功输出：JSON，包含 `deleted`、`state_file`
	- 退出码：`0`

7. `addr-keys` <a id="cmd_addr_keys"></a>
	- 作用：返回 `~/.config/tms-takecar/addr.json` 中的全部 key
	- 输入参数：
	  - 可选参数 `--addr-file`：显式指定地址文件路径，默认 `~/.config/tms-takecar/addr.json`
	- 成功输出：JSON，包含 `keys`、`count`、`addr_file`
	- 说明：这是 `addr.json` 的 `getAllKeys` / “返回全部 keys” 接口
	- 退出码：`0`

8. `addr-get-value <key>` <a id="cmd_addr_get_value"></a>
	- 作用：按 key 读取 `~/.config/tms-takecar/addr.json` 中的 value
	- 输入参数：
	  - 位置参数 `key`：地址别名，例如 `家`、`公司`、`小宝学校`
	  - 可选参数 `--addr-file`：显式指定地址文件路径，默认 `~/.config/tms-takecar/addr.json`
	- 成功输出：JSON，包含 `key`、`found`、`value`、`addr_file`
	- 说明：这是 `addr.json` 的 `getValuesByKey` 接口；当 key 不存在时，返回 `found=false` 且 `value=null`
	- 退出码：
	  - `0`：成功
	  - `2`：参数错误（如 key 为空）

9. `addr-upsert-value <key> <value_json>` <a id="cmd_addr_upsert_value"></a>
	- 作用：按 key 新增或更新 `~/.config/tms-takecar/addr.json` 中的 value
	- 输入参数：
	  - 位置参数 `key`：地址别名，例如 `家`、`公司`、`小宝学校`
	  - 位置参数 `value_json`：JSON object 字符串，推荐直接传 `poi-search` 单条 item 结果
	  - 可选参数 `--addr-file`：显式指定地址文件路径，默认 `~/.config/tms-takecar/addr.json`
	- 成功输出：JSON，包含 `updated`、`created`、`key`、`value`、`file`、`addr_file`
	- 说明：这是 `addr.json` 的 `upsertValue` 接口；`created=true` 表示新建，`created=false` 表示覆盖已有值
	- 退出码：
	  - `0`：成功
	  - `2`：参数错误（如 `value_json` 不是 JSON object）

10. `addr-sync-to-state <key> --scene <1|2>` <a id="cmd_addr_sync_to_state"></a>
	- 作用：将 `addr.json` 中指定 key 的地址对象同步到 `~/.config/tms-takecar/state.json` 的 `pickup` 或 `dropoff`
	- 输入参数：
	  - 位置参数 `key`：地址别名，例如 `家`、`公司`、`小宝学校`
	  - 必选参数 `--scene`：`1` 表示写入 `pickup`，`2` 表示写入 `dropoff`
	  - 可选参数 `--addr-file`：显式指定地址文件路径，默认 `~/.config/tms-takecar/addr.json`
	  - 可选参数 `--state-file`：显式指定状态文件路径，默认 `~/.config/tms-takecar/state.json`
	- 成功输出：JSON，包含 `updated`、`key`、`scene`、`scene_key`、`state_file`、`addr_file`
	- 联动写入：
	  - 将目标地址对象规范化后写入 `state.json` 的 `pickup` 或 `dropoff`，格式与 `poi-search` 返回 item 一致
	  - 成功后会重置下游字段 `estimate=null`、`userPreferLabels=[]`、`orderId=null`
	- 退出码：
	  - `0`：成功
	  - `2`：参数错误（如 key 不存在、scene 非法、地址对象缺少 `poiid`）

11. `short-cut-keys` <a id="cmd_short_cut_keys"></a>
	- 作用：返回 `~/.config/tms-takecar/short-cut.json` 中的全部 key
	- 输入参数：
	  - 可选参数 `--short-cut-file`：显式指定快捷场景文件路径，默认 `~/.config/tms-takecar/short-cut.json`
	- 成功输出：JSON，包含 `keys`、`count`、`short_cut_file`
	- 说明：这是 `short-cut.json` 的 `getAllKeys` / “返回全部 keys” 接口
	- 退出码：`0`

12. `short-cut-get-value <key>` <a id="cmd_short_cut_get_value"></a>
	- 作用：按 key 读取 `~/.config/tms-takecar/short-cut.json` 中的 value
	- 输入参数：
	  - 位置参数 `key`：归一化场景键，例如 `回家`、`去公司`、`接孩子`
	  - 可选参数 `--short-cut-file`：显式指定快捷场景文件路径，默认 `~/.config/tms-takecar/short-cut.json`
	- 成功输出：JSON，包含 `key`、`found`、`value`、`short_cut_file`
	- 说明：这是 `short-cut.json` 的 `getValuesByKey` 接口；当 key 不存在时，返回 `found=false` 且 `value=null`
	- 退出码：
	  - `0`：成功
	  - `2`：参数错误（如 key 为空）

13. `short-cut-upsert-value <key> <value_json>` <a id="cmd_short_cut_upsert_value"></a>
	- 作用：按 key 新增或更新 `~/.config/tms-takecar/short-cut.json` 中的 value
	- 输入参数：
	  - 位置参数 `key`：归一化场景键，例如 `回家`、`去公司`、`接孩子`
	  - 位置参数 `value_json`：JSON object 字符串，例如 `{"preferred_car_type":"","from":"公司","to":"家"}`
	  - 可选参数 `--short-cut-file`：显式指定快捷场景文件路径，默认 `~/.config/tms-takecar/short-cut.json`
	- 成功输出：JSON，包含 `updated`、`created`、`key`、`value`、`file`、`short_cut_file`
	- 说明：这是 `short-cut.json` 的 `upsertValue` 接口；`created=true` 表示新建，`created=false` 表示覆盖已有值
	- 退出码：
	  - `0`：成功
	  - `2`：参数错误（如 `value_json` 不是 JSON object）

14. `poi-search` <a id="cmd_poi_search"></a>
	- 作用：按关键字检索 POI，并按场景合并推荐上下车点（两步流程）
	- 内部流程：
	  1. 调用基础检索接口 `/mcp/open/tms/lbs/suggestion` 获取 POI 列表
	  2. 当 `scene=1` 或 `scene=2` 时，对每个 POI 结果分别调用二级接口：
	     - `scene=1`（上车点）：`/mcp/open/tms/recommend/taxi/getOnPoints`
	     - `scene=2`（下车点）：`/mcp/open/tms/recommend/taxi/getDropOffPointV2`
	  3. 组合基础 POI 信息与推荐点信息，输出扁平化列表
	- 输入参数：
	  - `--keyword`：检索关键字，必填
	  - `--city-name`：城市名，非必填，默认 `""`。映射为 API 字段 `region`。当该参数为空时，脚本回退读取 `~/.config/tms-takecar/env.json` 中的 `resident_city`。
	  - 城市解析约束：用户明确提到城市（如“北京的新街口”“上海人民广场”）时应优先由 agent 填充 `--city-name`；若表达歧义（如“四川饭店”“xx驻京办事处”）必须先追问所在城市，再调用 `poi-search`。
	  - `--page-size`：分页大小，非必填，默认 `3`。映射为 API 字段 `pageSize`
	  - `--page-index`：页码索引（1-based），非必填，默认 `1`。映射为 API 字段 `pageIndex`
	  - `--scene`：场景参数，非必填，默认 `0`。取值：`0`-普通检索，`1`-检索+推荐上车点，`2`-检索+推荐下车点；其他值报错。映射为 API 字段 `policy`（`0→0, 1→10, 2→11`）
	  - `--state-file`：显式指定状态文件路径，默认 `~/.config/tms-takecar/state.json`
	- 基础检索 API（步骤 1）：
	  - 路径：`/mcp/open/tms/lbs/suggestion`
	  - 请求 payload：`keyword`、`region`、`policy`、`pageIndex`、`pageSize`
	  - 响应解析：`data.data.dataList[]`，每个元素含 `id`、`title`、`address`、`adcode`、`location.lat`、`location.lng`
	- 上车点 API（步骤 2，scene=1）：
	  - 路径：`/mcp/open/tms/recommend/taxi/getOnPoints`
	  - 请求 payload：`lat`、`lng`（来自步骤 1）、`maxCount: 1`、`appId: "0"`、`appChannelId: "0"`、`geoPointAsFallback: true`、`geoPointWhenNoAbsorb: true`
	  - 响应解析：`data.data.points[0]` → `title`、`location.lat`、`location.lng`
	- 下车点 API（步骤 2，scene=2）：
	  - 路径：`/mcp/open/tms/recommend/taxi/getDropOffPointV2`
	  - 请求 payload：`poiId`（来自步骤 1 的 `id`）、`endLat`、`endLng`（来自步骤 1）、`appId: "0"`、`appChannelId: "0"`、`checkSubPoi: true`
	- 响应解析优先级：
	    1. `data.data.parkingSuggestions.points` 非空时：展开 `subPoints`（`point_name = parent.title + "-" + sub.title`）；无 `subPoints` 时直接使用 point（`point_name = point.title`）
	    2. `parkingSuggestions.points` 为空时：取 `data.data.dropOffPoints.pointList[0]`（注意：是 `data.data.dropOffPoints`，不是 `parkingSuggestions.dropOffPoints`）
	- 成功输出：
	  - 实际调用成功时返回 `{"mode": "searched", "result": ...}`
	  - `scene=1/2` 时会自动写入 `~/.config/tms-takecar/state.json` 的 `pickup` 或 `dropoff` 数组：按 `poiid` 去重追加（已存在则覆盖）
	- 返回数据约定：
	  - `result.body.items` 为扁平化地点列表，每个 item 包含：
	    - POI 字段：`name`、`address`、`longitude`、`latitude`、`poiid`、`citycode`
	    - 推荐点字段：`point_name`、`point_longitude`、`point_latitude`
	  - `scene=0` 时推荐点字段为空字符串
	  - `scene=1` 时推荐点字段为上车点信息（每个 POI 最多 1 条推荐点）
	  - `scene=2` 时推荐点字段为下车点信息（每个 POI 可能展开为多条，如机场的多个航站楼出入口）
	  - `result.body.page_index` 为当前返回页码索引
	- 退出码：
	  - 缺少 `TMS_SKILL_TOKEN`：`1`
	- 脚本内未配置接口基地址：`2`
	- HTTP 错误：`3`
	- 网络错误：`4`

15. `build-static-map-url` <a id="cmd_build_static_map_url"></a>
	- 作用：根据若干 marker 经纬度和 marker 枚举，生成腾讯静态地图 URL
	- 输入参数：
	  - `--markers-json`：必填，JSON array；每个元素为 `{"latitude": ..., "longitude": ..., "marker": "起|终|P"}`
    - 使用系统预设 markers，支持 3 种枚举：
	    - `起` → `color:red|label:起`
	    - `终` → `color:green|label:终`
	    - `P` → `color:blue|label:P`
	- 成功输出：JSON，格式为 `{"url": "<static_map_url>"}`
	- 退出码：
	  - `0`：成功
	  - `1`：缺少 token
	  - `2`：参数错误

16. `select-poi` <a id="cmd_select_poi"></a>
	- 作用：根据用户选择的 `poiid` 收敛 `pickup`/`dropoff` 候选，仅保留 1 条记录
	- 输入参数：
	  - `--poiid`：用户选择的 POI ID，必填
	  - `--scene`：对应 poi-search 场景，必填，取值 `1`（pickup）或 `2`（dropoff）
	  - `--state-file`：显式指定状态文件路径，默认 `~/.config/tms-takecar/state.json`
	- 成功输出：JSON，包含 `updated`、`scene`、`poiid`、`state_file`
	- 联动写入：成功后会重置下游字段 `estimate=null`、`userPreferLabels=[]`、`orderId=null`
	- 退出码：
	  - 参数错误：`2`
	  - 成功：`0`

17. `estimate-price` <a id="cmd_estimate_price"></a>
	- 作用：根据起终点进行打车价格预估
	- 目标接口：`/mcp/open/tms/takecar/estimate/price`
	- 输入参数：
	  - 可选参数 `--state-file`：显式指定状态文件路径，默认 `~/.config/tms-takecar/state.json`
	- 参数来源：起终点、城市编码、POI 信息全部由脚本从 state 文件读取（`pickup` / `dropoff` 收敛后的唯一候选）
	- 偏好来源：`state.userPreferLabels`（由上游流程写入），询价成功后回写到 `estimate.userPreferLabels`
	- 成功输出：
	  - 实际调用成功时返回 `{"mode": "estimated", "result": ...}`
	  - 成功后自动写入 `~/.config/tms-takecar/state.json` 的 `estimate` 字段（含 `estimateKey`、`distance`、`estimateTime`、`products`、`userPreferLabels`）
	- 返回数据约定：
	  - `result.body.code`：响应状态码，0 表示成功
	  - `result.body.message`：响应消息
	  - `result.body.data.cityStatus`：城市状态，0-已下线，1-上线，2-灰度中，3-暂停服务
	  - `result.body.data.cityMessage`：城市状态说明
	  - `result.body.data.distance`：预估里程，单位米
	  - `result.body.data.estimateTime`：预估时长，单位秒
	  - `result.body.data.estimateKey`：预估 key，下单时需要
	  - `result.body.data.product`：预估列表，每个元素包含：
	    - `riderInfo.rideType`：车型（1-普通经济型，2-超惠经济型，3-优选型，4-舒适型，5-商务型，6-豪华型，7-出租车）
	    - `riderInfo.riderClassify`：运力类目（1-经济型，2-优享型，3-舒适型，4-商务型，5-豪华型，6-出租车，7-超惠型）
	    - `riderInfo.riderDesc`：车型描述
	    - `priceEstimate`：运力预估列表，每个元素包含：
	      - `estimatePrice`：预估价，单位分
	      - `defaultChecked`：是否默认勾选（1 是 0 否）
	      - `discountAmount`：优惠金额，单位分
	      - `discountPercentage`：折扣力度（0-100）
	      - `discountType`：折扣类型（1-优惠券，2-折扣券）
	      - `priceEstimateKey`：运力预估 key
	      - `sp.code`：运力商 ID
	      - `sp.name`：运力商名称
	      - `sp.aliasName`：运力商别名
	  - 结果裁剪规则：仅保留上述字段；`riderInfo.rideType` 不在 `1~7` 枚举范围内的条目直接丢弃
	- 退出码：
	  - 缺少 `TMS_SKILL_TOKEN`：`1`
	  - 脚本内未配置接口基地址：`2`
	  - HTTP 错误：`3`
	  - 网络错误：`4`

17. `create-order` <a id="cmd_create_order"></a>
	- 作用：创建打车订单（包含风控校验）
	- 目标接口：`/mcp/open/tms/takecar/risk/verify/book/order`
	- 输入参数：
	  - 可选参数 `--state-file`：显式指定状态文件路径，默认 `~/.config/tms-takecar/state.json`
	  - 可选参数 `--price-estimate-keys`：JSON 数组字符串，示例：`'["mock-price-key-eco-001"]'`。若提供，脚本先更新 `state.json` 中 `estimate.products[].userSelect`，再构造请求
	  - 可选参数 `--user-prefer-labels`：JSON 整数数组字符串，示例：`'[1, 3]'`。若提供，脚本先更新 `state.json` 中 `estimate.userPreferLabels`，再构造请求
	- 参数来源：起终点、城市编码、POI 信息全部由脚本从 state 文件读取（`pickup` / `dropoff` 收敛后的唯一候选）
	- `productStr`：脚本内部根据 `estimate.products` 中 `userSelect=1` 的条目自动构造
	- 固定字段：请求中额外包含 `departureTime`（当前毫秒时间戳）、`orderServiceType=1`、`isNeedReEstimate=true`
	- 位置字段：
	  - 坐标使用已收敛候选中的 `point_latitude` / `point_longitude`
	  - `toId` 使用终点 `poiid`
	  - `fromName` / `toName` 优先使用 `point_name`，为空时回退到 `name`
	- 成功输出：
	  - 实际调用成功时返回 `{"mode": "ordered", "result": ...}`
	- 返回数据约定：
	  - `result.body.code`：响应状态码，`0` 表示成功
	  - `result.body.message`：响应消息
	  - `result.body.data.orderId`：订单 ID；为空、空字符串或字符串 `null` 都表示下单失败
	  - `result.body.data.unfinishedOrder`：是否存在未完成订单
	- 下单结果判定：
	  - `data.orderId` 不为空 → 下单成功
	  - `data.orderId` 为空 → 下单失败，需结合 `code` 和 `message` 判断原因
	  - `data.unfinishedOrder == true` → 有未完成订单，禁止重复下单
	- 退出码：
	  - 缺少 `TMS_SKILL_TOKEN`：`1`
	  - 脚本内未配置接口基地址：`2`
	  - HTTP 错误：`3`
	  - 网络错误：`4`

18. `query-ongoing-order` <a id="cmd_query_ongoing_order"></a>
	- 作用：查询当前用户是否有进行中的订单
	- 输入参数：无
	- 成功输出：
	  - 实际调用成功时返回 `{"mode": "queried", "result": ...}`
	- 返回数据约定（`result.body.data`）：
	  - `hasOnGoingOrder`：是否有进行中的订单
	  - `orderId`：进行中订单 ID
	  - `status`：订单状态（`assigning`、`accepted`、`driver_arrived`、`in_trip`、`trip_finished`、`completed`、`cancelled`、`reassigning`）
	  - `orderDesc`：订单状态描述
	  - `vehicleColor`：车辆颜色
	  - `licensePlates`：车牌号
	  - `supplierName`：运力商名称
	  - `startName/startLng/startLat`：出发地名称与经纬度
	  - `endName/endLng/endLat`：目的地名称与经纬度
	  - `cancelFee`：取消费（元）
	  - `unpaidFee`：待支付费用（元）
	- 退出码：
	  - 缺少 `TMS_SKILL_TOKEN`：`1`
	  - 脚本内未配置接口基地址：`2`
	  - HTTP 错误：`3`
	  - 网络错误：`4`

19. `cancel-order` <a id="cmd_cancel_order"></a>
	- 作用：取消进行中的订单
	- 内部流程：
	  1. 先调用 `query-ongoing-order` 获取当前订单 ID
	  2. 如果没有进行中的订单，返回错误码 `5`
	  3. 默认先用 `confirm=false` 调用取消接口查询取消费
	  4. 当 `waiverFee=true` 时，脚本自动用相同参数并将 `confirm=true` 再次调用取消接口完成取消
	  5. 当 `waiverFee=false` 时，脚本返回取消费用并等待用户确认；agent 需在用户确认后调用 `cancel-order --confirm`
	- 输入参数：
	  - `--confirm`：确认取消。仅在脚本已提示存在取消费用、且用户明确确认后使用
	  - `--reason`：取消原因，非必填
	- 成功输出：
	  - 实际调用成功时返回 `{"mode": "cancelled", "result": ...}`
	  - 查询到取消费且需要用户确认时返回 `{"mode": "cancel_fee_required", "amount": <分>, "amount_yuan": <元>, "message": ... , "result": ...}`
	- 返回数据约定（`result.body.data`）：
	  - `amount`：取消费，单位分
	  - `waiverFee`：是否免取消费
	- 退出码：
	  - 缺少 `TMS_SKILL_TOKEN`：`1`
	  - 脚本内未配置接口基地址：`2`
	  - HTTP 错误：`3`
	  - 网络错误：`4`
	  - 没有进行中的订单：`5`
	  - 需要用户确认取消费：`6`

20. `query-order` <a id="cmd_query_order"></a>
	- 作用：查询打车订单状态及司机、车辆信息
	- 目标接口：`/mcp/open/tms/takecar/order/detail`
	- 内部流程：
	  1. 先调用 `query-ongoing-order` 获取当前订单 ID
	  2. 如果有进行中的订单，使用获取到的订单 ID 查询详情
	  3. 如果没有进行中的订单，返回错误码 `5`
	- 输入参数：无
	- 成功输出：
	  - 实际调用成功时返回 `{"mode": "queried", "result": ...}`
	- 返回数据约定（`result.body.data`）：
	  - `orderId`：订单 ID
	  - `status`：订单状态枚举字符串
	  - `statusDesc`：订单状态可读描述（展示给用户）
	  - `acceptTime`：司机接单时间（字符串，格式 `YYYY-MM-DD HH:mm:ss`，未接单时为空）
	  - `cancelTime`：取消时间（字符串，未取消时为空）
	  - `driver.name`：司机姓名
	  - `driver.phone`：司机手机号（脱敏）
	  - `driver.avatar`：司机头像 URL
	  - `vehicle.brand`：车辆品牌
	  - `vehicle.color`：车辆颜色
	  - `vehicle.model`：车辆型号
	  - `vehicle.plate`：车牌号
	  - `vehicle.picture`：车辆图片 URL
	  - `position.startName`：出发地名称
	  - `position.startAddress`：出发地地址
	  - `position.startLat/startLng`：出发地经纬度
	  - `position.endName`：目的地名称
	  - `position.endAddress`：目的地地址
	  - `position.endLat/endLng`：目的地经纬度
	  - `estimateDistance`：预估路程（米）
	  - `estimateDuration`：预估时长（秒）
	  - `estimatePrice`：预估金额（元）
	  - `distance`：已行驶路程（米，行程结束前为 0）
	  - `cost.totalAmount`：实际费用（元，行程结束前为 0）
	  - `cost.refundAmount`：退款金额（元）
	- 退出码：
	  - 缺少 `TMS_SKILL_TOKEN`：`1`
	  - 脚本内未配置接口基地址：`2`
	  - HTTP 错误：`3`
	  - 网络错误：`4`
	  - 没有进行中的订单：`5`

21. `query-driver-location` <a id="cmd_query_driver_location"></a>
	- 作用：在司机接单后、行程结束前，查询司机实时位置
	- 目标接口：`/mcp/open/tms/takecar/passenger/order/driverPassengerDisplay`
	- 内部流程：
	  1. 先调用 `query-ongoing-order` 获取当前订单 ID
	  2. 如果没有进行中的订单，返回错误码 `5`
	  3. 脚本从 `state.json` 读取 `routeId`、`trafficId` 参数（默认值均为 `0`）
	  4. 使用获取到的订单 ID 和参数查询司机位置
	- 输入参数：无
	- 成功输出：
	  - 实际调用成功时返回 `{"mode": "queried", "result": ...}`
	- 返回数据约定（`result.body`，经过脚本转换后）：
	  - `code`：响应状态码
	  - `message`：响应描述
	  - `data.orderStatus`：订单状态（详见下表）
	  - `data.eta`：预计到达时间，单位分钟（不可用时为 `null`）
	  - `data.eda`：预计到达距离，单位米（不可用时为 `null`）
	  - `data.driverLocation`：司机位置信息对象（不可用时为 `null`）
	    - `location`：司机当前坐标原始字符串，格式 `longitude,latitude`
	    - `latitude`：由 `location` 第 1 段解析得到（脚本当前实现）
	    - `longitude`：由 `location` 第 2 段解析得到（脚本当前实现）
	    - `direction`：司机行驶方向，单位度
	    - `locationTime`：位置上报时间戳，单位毫秒
	- 订单状态值（orderStatus）：
	  - `0`：预估中
	  - `1`：正在派单
	  - `2`：等待接驾（司机已接单）
	  - `3`：司机已到达
	  - `4`：行程开始（行程中）
	  - `5`：行程结束，计费结束
	  - `6`：订单待支付
	  - `7`：订单已支付
	  - `8`：司机已取消
	  - `9`：服务商取消
	  - `10`：系统取消
	  - `11`：乘客已取消
	  - `12`：取消费待支付
	  - `13`：取消费已支付
	  - `14`：订单待退款
	  - `15`：订单已退款
	  - `16`：预约成功（预约单）
	  - `21`：改派中
	- 返回数据处理：
	  - 若 `data.resData.driverPassengerDisplay.driverLocationInfo` 中的 `eta` 和 `eda` 都不存在，脚本检查 `orderStatus`：
	    - 若 `orderStatus` 不属于 `2, 3, 4`，脚本返回错误结果并告知用户当前订单状态不支持查询司机位置
	    - 若属于，则返回空位置信息
	- 退出码：
	  - 缺少 `TMS_SKILL_TOKEN`：`1`
	  - 脚本内未配置接口基地址：`2`
	  - HTTP 错误：`3`
	  - 网络错误：`4`
	  - 没有进行中的订单：`5`

### 环境变量

1. `TMS_SKILL_TOKEN`
	- 用于请求鉴权
	- 唯一数据来源：`~/.config/tms-takecar/env.json` 的 `token` 字段

## API 测试要求

- 每当新增或修改一个会发起 HTTP 请求的接口时，必须同步补充或更新对应的单元测试。
- 新增测试优先放在 [tests/test_tms_takecar_api.py](../tests/test_tms_takecar_api.py)；如果是某个具体业务分支的补充，再按需补到对应的命令测试文件。
- 最低覆盖项必须包括：
	- 缺少 token 时的退出路径。
	- token 错误或接口返回 401/403 等鉴权失败时的错误路径。
	- 业务成功路径。
	- 可选参数、默认值和边界值场景。
	- 响应为空、非 JSON、超时或网络错误等解析与传输边界。
- 所有 HTTP 测试都必须使用 mock，不得依赖真实网络请求。
