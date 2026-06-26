<a id="short-cut-main"></a>
## ⚡ 快捷叫车流程（总入口 + 快捷下单）

适用于以下用户诉求：
- "回家"
- "去公司"、"上班"
- "接孩子"
- 其他可映射为固定场景终点的快捷叫车表达

### 1. 全局约束
**⚠️必须先阅读以下文档**
- [异常处理流程](./references/error_handling.md)
- [接口契约](./references/api-contract.md)
- [常用地址 Schema](./addr-schema.md)
- [快捷叫车 Schema](./short-cut-schema.md)
- [订单状态模版](./references/state-schema.md)
- [设置快捷场景流程](./short-cut-setup-workflow.md)

#### 1.1 决策流程（整体强约束）

```markdown
用户表达进入快捷叫车
   ↓
场景是否可归一化为「回家 / 去公司 / 接孩子」？
   ├─ 否 → 回退到 [打车主流程](./references/takecar-workflow.md#takecar-main-flow)
   └─ 是 → 调用 [`short-cut-keys`](./api-contract.md#cmd_short_cut_keys) / [`addr-keys`](./api-contract.md#cmd_addr_keys)
           ↓
        先调用 [`short-cut-keys`](./api-contract.md#cmd_short_cut_keys) 再语义匹配，是否命中该场景记录？
           ├─ 否 → 进入 [设置快捷场景流程](./short-cut-setup-workflow.md#short-cut-setup-main)
           └─ 是 → 进入 [快捷下单主流程](#short-cut-flow)
                  ↓
               先调用 [`addr-keys`](./api-contract.md#cmd_addr_keys) 再语义匹配，是否命中终点地址别名？
                  ├─ 否 → 进入 [设置快捷场景流程](./short-cut-setup-workflow.md#short-cut-setup-main)
                  └─ 是 → 再调用 [`short-cut-get-value`](./api-contract.md#cmd_short_cut_get_value) / [`addr-get-value`](./api-contract.md#cmd_addr_get_value) 读取该场景记录的起点与偏好车型后执行快捷下单
```

强约束：
- ⚠️ 禁止跳步、禁止并行分支、禁止合并执行多个步骤。**命中已保存场景时走本流程；未命中时必须切换到设置快捷场景流程，且需要用户确认的部分不得跳过**
- 命中某一判断分支后，只允许执行该分支对应动作，不得同轮切换分支。
- ⚠️ 凡是文档标注“立即写回”的步骤，必须先通过 [`addr-upsert-value`](./api-contract.md#cmd_addr_upsert_value) 或 [`short-cut-upsert-value`](./api-contract.md#cmd_short_cut_upsert_value) 实际写入 `addr.json` / `short-cut.json`，再进入下一步。
- 任一步骤失败、字段缺失或契约校验不通过，立即回退到 [异常处理流程](./references/error_handling.md)。

1. 必须通过 [`addr-keys`](./api-contract.md#cmd_addr_keys)、[`addr-get-value`](./api-contract.md#cmd_addr_get_value)、[`short-cut-keys`](./api-contract.md#cmd_short_cut_keys)、[`short-cut-get-value`](./api-contract.md#cmd_short_cut_get_value) 读取 `addr.json` 与 `short-cut.json`，并优先使用其中的常用地址和快捷叫车配置。
2. `short-cut.json` 中的 `from`、`to` 字段表示 `addr.json` 中的地址别名（如 `家`、`公司`、`接孩子`），不是 `poi.name` 文本。
3. 进入询价或下单前，必须先调用 [`addr-keys`](./api-contract.md#cmd_addr_keys) 获取全部 key，再做语义匹配命中目标地址别名，最后调用 [`addr-get-value`](./api-contract.md#cmd_addr_get_value) 读取对应对象，并将该对象的地址字段填充到 `~/.config/tms-takecar/state.json`（`pickup`/`dropoff`）。
4. 地址匹配采用语义对齐，但读取流程必须严格遵守“先 [`*-keys`](./api-contract.md#cmd_addr_keys) 、后匹配、再 [`*-get-value`](./api-contract.md#cmd_addr_get_value)”；禁止跳过 keys 接口直接猜测 key。
5. 语义对齐示例（不限于）：
   - "公司" = "单位" = "上班"
   - "爸妈家" = "父母家"
   - "回家" = "家"
6. 匹配方法必须严谨：优先做语义归一化和同义词映射，禁止仅凭字符串包含、模糊正则或任意子串命中直接判定目标 key。
7. 若多个 key 都可能匹配，或无法稳定唯一命中，必须使用以下模版回复用户并等待用户选择后继续。
**❌ 禁止自行替用户做出选择，❌ 禁止回复模版以外的内容**
```markdown
 1 - {short-cut.key[1]}
📍 {short-cut.key[1].from} -> {short-cut.key[1].to}
---
{n} - {short-cut.key[n]}
📍 {short-cut.key[n].from} -> {short-cut.key[n].to}

**请告诉我你具体是想用以上哪条路线。或者给我更精准的起点和终点。**
```
8. **状态文件初始化**：开启叫车流程前，—若 `~/.config/tms-takecar/state.json` 已存在则调用`delete-state`删除。
  - 删除命令：
  ```bash
  python3 ./scripts/tms_takecar.py delete-state
  ```
9. 地址相关请求（含上车点、下车点、模糊地名）必须先调用 `poi-search`，**未调用前禁止输出地点判断、禁止直接要求用户补充更具体地址**。
10. 地址相关信息若未命中记忆，必须切换到 [设置快捷场景流程](./short-cut-setup-workflow.md#short-cut-setup-main)，并复用「3. 地址检索」让用户确认。
11. 下单相关话术与字段，必须使用「4. 价格预估」与「5. 下单」的模板和约束。

### 2. 场景归一化规则

将用户输入先归一化为场景键，再执行后续流程：

| 用户表达 | 归一化场景键 | 默认终点记忆键 |
| --- | --- | --- |
| 回家、回去、回住处 | 回家 | 家 |
| 去公司、上班、去单位 | 去公司 | 公司 |
| 接孩子、去接娃、接小孩 | 接孩子 | 接孩子 |

若无法归一化到明确场景，回退到 [打车主流程](./references/takecar-workflow.md#takecar-main-flow)。

<a id="short-cut-poi-search"></a>
### 3. 地址检索
**流程**：
1. 调用 `poi-search` 搜索地点（必须传 `scene` 参数）：
   - 起点检索（上车点）使用 `scene=1`
   - 终点检索（下车点）使用 `scene=2`
   - 仅做普通地点搜索且不需要推荐上下车点时使用 `scene=0`
   - 用户明确提到城市（如“北京的新街口”“上海人民广场”）时，优先填充 `--city-name`
   - 表达歧义（如“四川饭店”“xx驻京办事处”）时，先追问城市，再调用 `poi-search`
   - 用户未提及城市时，不传 `--city-name`，由脚本从 `~/.config/tms-takecar/env.json` 的 `resident_city` 回退
2. 判断是否需要用户选择：

**需要用户选择**：
- 搜索结果返回多个不同地点
- 多个同名但位置不同的地点
- 用户表述宽泛且结果差异大
- **核心原则**：不能100%确定用户表述的地点

**自动匹配**：
- 搜索结果只有1个地点

**当需要用户选择时，用`poi-search`填充以下模版回复用户**
**⚠️ 模版中的条目数严格按照`poi-search`返回值** 
**❌ 禁止自行替用户做出选择**
```markdown
### 请在以下地址中选择您的地址

📍 **1. {items[0].name}: {items[0].address}**  
🅿️ **{items[0].point_name}**  
---
📍 **2. {items[1].name}: {items[1].address}**  
🅿️ **{items[1].point_name}**  
---
📍 **{n}. {items[n].name}: {items[n].address}**  
🅿️ **{items[n].point_name}**  
---

### 你可以回复：”1“ 或者 "{items[0].name}"
### 你也可以回复：”更多“或者告诉我更确切的地址
```

- 如果用户输入新的keyword则重新调用[`poi-search --scene 1`](./api-contract.md#cmd_poi_search) 搜索地点
- 如果用户选择翻页或者说："更多"、"下一页"则调用[`poi-search --scene 1 --page-index <当前page-index++>`](./api-contract.md#cmd_poi_search) 进行翻页 
- 直到用户通过回复序号，回复地点名称等方式从返回值中做出选择再进行下一步
- 用户确认后调用 [`select-poi`](./api-contract.md#cmd_select_poi) 收敛上车点：
    ```bash
    python3 ./scripts/tms_takecar.py select-poi --scene 1 --poiid <用户选择的poiid>
    ```

<a id="short-cut-estimate"></a>
### 4. 价格预估

#### 4.1 车型筛选规则

从 [`short-cut-get-value`](./api-contract.md#cmd_short_cut_get_value) 返回的场景记录中提取 `preferred_car_type`，分为 **询价阶段可筛选** 和 **下单阶段参数** 两类：

**询价阶段可筛选的诉求**：

| 诉求类型 | 示例 | 筛选字段 | 筛选逻辑 |
|----------|------|----------|----------|
| 价格 | "30元以内" | `estimatePrice` | `estimatePrice / 100 <= 用户指定金额` |
| 车型 | "舒服一点的"、"后排宽敞一点的" | `rideType` | 根据语义匹配对应车型（舒适→rideType 4，豪华→rideType 6，商务→rideType 5 等） |
| 座位数 | "我们有5个人" | `riderDesc` | 从 `riderDesc` 中提取座位数，筛选 `可坐人数 >= 用户人数` 的车型。`riderDesc`未提及座位数时默认5座车 |

**下单阶段参数（询价阶段不做筛选）**：

| 诉求类型 | 示例 | 处理方式 |
|----------|------|----------|
| 接驾时间 | "快一点的" | 确认下单后作为 `userPreferLabels` 参数提供 |
| 接驾距离 | "找个最近的司机" | 确认下单后作为 `userPreferLabels` 参数提供 |
| 新能源/油车 | "想要个电车" | 确认下单后作为 `userPreferLabels` 参数提供 |


##### 4.2.1 筛选决策流程

```
询价结果返回 product 列表
    ↓
[`short-cut-get-value`](./api-contract.md#cmd_short_cut_get_value) 返回的当前场景记录中，`preferred_car_type` 是否包含可筛选偏好？
    ├─ 否 → 【默认列表】使用 defaultChecked=1 的车型的`priceEstimateKey` 
    └─ 是 → 对 product 列表按偏好条件过滤
              ↓
          筛选结果是否为空？
              ├─ 否 → 保存筛选后的车型的 `priceEstimateKey` 
              └─ 是 → 保存defaultChecked=1 `priceEstimateKey` 
```

**组合诉求示例**：
- "叫个30元以内的" → 按价格筛选，state.json保存筛选后列表
- "我想要个女司机" → 不可筛选，state.json保存默认列表
- "叫个30元以内的，要女司机" → state.json保存按价格筛选后列表 
- "我们5个人，舒服一点的" → state.json保存按座位数（≥5人→需6座车）+ 车型（舒适/商务）筛选后列表
- "快一点来，30以内" → state.json保存按价格筛选后列表，"快一点"记录到下单阶段参数

#### 4.3 流程：
1. 通过快捷场景与常用地址接口读取数据：
   - 先调用 [`short-cut-keys`](./api-contract.md#cmd_short_cut_keys) 获取全部场景 key
   - 对场景 key 做语义归一化匹配，唯一命中后调用 [`short-cut-get-value`](./api-contract.md#cmd_short_cut_get_value) 读取当前场景记录
   - 从当前场景记录读取 `from`、`to`
   - 对 `from`、`to` 分别调用 [`addr-get-value`](./api-contract.md#cmd_addr_get_value) 读取对应地址对象
2. 如果`from`调用 [`addr-get-value`](./api-contract.md#cmd_addr_get_value)返回空，执行[3. 地址检索](#short-cut-poi-search)，由用户确认起点。
   否则调用[`addr-sync-to-state {from} --scene 1`](./api-contract.md#cmd_addr_sync_to_state)同步起点数据。**⚠️这里的key是`from`**
3. 如果`to`调用 [`addr-get-value`](./api-contract.md#cmd_addr_get_value)返回空，进入 [设置快捷场景流程](./short-cut-setup-workflow.md#short-cut-setup-main)。
   否则调用[`addr-sync-to-state {to} --scene 2`](./api-contract.md#cmd_addr_sync_to_state)同步终点数据。**⚠️这里的key是`to`**
4. 调用 [`estimate-price`](./api-contract.md#cmd_estimate_price) 询价：
   ```bash
  python3 ./scripts/tms_takecar.py estimate-price
   ```
5. 检查返回结果：
   - 如果 `cityStatus` 不为 `1`（上线），告知用户该城市当前不支持叫车服务，并展示 `cityMessage`，结束流程
   - 如果 `code` 不为 `0`，告知用户询价失败并展示 `message`，结束流程
6. 调用 [`estimate-price`](./api-contract.md#cmd_estimate_price) 成功后，读取 `~/.config/tms-takecar/state.json` 的 `estimate` 字段：
   - `estimateKey`：询价返回的预估 key
   - `distance`：预估里程
   - `estimateTime`：预估时长
7. 根据用户诉求筛选车型（见上方 **车型筛选规则**），确定最终展示列表
8. 向用户展示车型和价格（见上方 **展示模版**），**❌ 禁止自行替用户做出选择，❌ 禁止回复模版以外的内容**
9. 用户确认选择后（包括重新筛选后再次确认），提取命中的 `priceEstimateKey` 列表，进入「5. 下单」（将 `--price-estimate-keys` 传给 [`create-order`](./api-contract.md#cmd_create_order)，详见「5. 下单」）

<a id="short-cut-order"></a>
### 5. 下单
```
用户确认下单
    ↓
🔧 create-order（创建订单）
    ↓
下单成功？（data.orderId 不为空）
    ├─ 是 → 更新 state.json，告知用户下单成功
    └─ 否 → 根据 code 和 message 告知用户失败原因
```
<a id="short-cut-place-order"></a>
#### 5.1 创建订单

1. 调用 [`create-order`](./api-contract.md#cmd_create_order) 创建订单：
   ```bash
    python3 ./scripts/tms_takecar.py create-order --price-estimate-keys '<JSON数组>' [--user-prefer-labels '<JSON数组>']
   ```
2. 判断下单结果：
   - `data.orderId` **不为空** → 下单成功
    - `data.orderId` **为空**（包含空字符串或字符串 `null`）→ 下单失败
    - `data.unfinishedOrder == true` → 有未完成订单，提示用户先完成或取消现有订单

#### 5.2 下单成功处理
1. 使用以下模版告知用户下单成功
**❌ 禁止回复模版以外的内容**
**回复模版**：
```markdown
订单已创建，正在为你安排车辆。

🧾 订单号：{orderId}
📍 {fromName} → {toName}
🚗 车型：{riderDesc}
💰 预估费用：约 {price} 元
⏱️ 行程预计：约 {estimateTime} 分钟

💬 发送「查询订单」可查看当前订单状态
```

#### 5.3 下单失败处理

- `data.unfinishedOrder == true`（有未完成订单）→ 告知用户存在未完成订单，需先完成或取消后再下单
- 其他失败 → 展示 `message` 告知用户失败原因，引导重试

#### 5.4 `userPreferLabels` 参数说明

从用户的原始打车诉求中自动解析并填充，**无需询问用户**：

| 枚举值 | 含义 | 触发关键词示例 |
|-----|----|---------|
| `1` | 接驾距离更近（地理位置上离起点更近） | "附近的"、"近一点"、"最近的" |
| `2` | 接驾最快（最快到达接驾点） | "最快的"、"快点来"、"尽快"、"5分钟内接驾" |
| `3` | 电车 | "电车"、"新能源"、"纯电" |
| `4` | 油车 | "油车"、"燃油车" |

**规则**：
- **必填字段**：每次调用都必须传入该字段
- 可多选，无偏好时传空数组 `[]`
- 禁止给用户透出 `userPreferLabels` 标签编号信息，只需透出文字信息即可
- **话术规范**：
  - 包含偏好时，在下单过渡语中将用户原始需求文字透出。例如：用户说"要一辆附近的电车" → 过渡语："正在帮你叫车，会尽可能为你安排一辆附近的电车"
  - 不包含偏好时，过渡语直接说："正在为你创建订单"

---

<a id="short-cut-flow"></a>
### 6. 快捷下单主流程（仅命中已保存场景）

#### 6.1 Step 0：读取记忆并做流程分流

1. 通过 [`short-cut-keys`](./api-contract.md#cmd_short_cut_keys) / [`addr-keys`](./api-contract.md#cmd_addr_keys) 读取快捷场景与常用地址
2. 将用户表达归一化为场景键（回家 / 去公司 / 接孩子）。
3. 调用 [`short-cut-keys`](./api-contract.md#cmd_short_cut_keys) 获取全部场景 key，并做语义匹配判断是否存在对应场景记录：
   - 不存在：立即切换到 [设置快捷场景流程](./short-cut-setup-workflow.md#short-cut-setup-main)
   - 存在：继续执行本章 6.2
4. 对命中的场景 key 调用 [`short-cut-get-value`](./api-contract.md#cmd_short_cut_get_value)，再对其中终点地址别名调用 [`addr-get-value`](./api-contract.md#cmd_addr_get_value) 查找终点地址对象：
   - 未命中：立即切换到 [设置快捷场景流程](./short-cut-setup-workflow.md#short-cut-setup-main)
   - 命中：继续执行本章 6.2

---

#### 6.2 Step 1：场景行存在，执行快捷下单

1. 调用 [`short-cut-get-value`](./api-contract.md#cmd_short_cut_get_value) 读取当前场景记录。
2. 读取该记录的 `from`、`to`（两者均为 `addr.json` 的地址别名）。
3. 分别调用 [`addr-get-value`](./api-contract.md#cmd_addr_get_value) 读取上述两个地址别名对应的对象，并调用[`addr-sync-to-state {from/to} --scene 1/2`](./api-contract.md#cmd_addr_sync_to_state)同步起点/终点数据。
4. 若`to`无对应地址对象或字段缺失，立即切换到 [设置快捷场景流程](./short-cut-setup-workflow.md#short-cut-setup-main)。

##### 6.2.1 Step 1.1：起点存在

1. 使用当前场景的 `起点` 与已确认终点进入叫车。
2. 判断该行 `偏好车型`：

- 有 `偏好车型`：
   1. 先执行「4. 价格预估」，按场景表格中的车型偏好规则筛选可下单车型，如筛选后车型列表为空，则回退为 `defaultChecked=1` 的默认可下单车型。过程中无需询问用户。
   2. 再执行「5. 下单」(#short-cut-order)下单。

- 无 `偏好车型`：
   1. 调用 `estimate-price` 后，按 `defaultChecked=1` 的默认可下单车型。
   2. 静默执行「5. 订单」(#short-cut-order) **⚠️不额外让用户再选车型**。
   3. 下单结果仍按「5. 下单」(#short-cut-order) 成功/失败模板回复。

##### 6.2.2 Step 1.2：起点不存在

1. ⚠️ 如果用户的地址不是明确的poi名称，比如：“家”、“公司”、“xx家”，禁止直接用于keyword。需要向用户确认具体的地址作为下一步「3. 地址检索」(#short-cut-poi-search)的keyword
2. 先按「3. 地址检索」确认起点（调用 `poi-search --scene 1`，返回结果包含推荐上车点）。
3. 后续流程与 6.2.1 相同。

---
### 7. 订单相关处理
查询、取消、询问司机位置等订单处理流程，参考： [订单处理流程](./references/order-workflow.md)
