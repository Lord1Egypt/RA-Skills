<a id="short-cut-setup-main"></a>
## 🧩 设置快捷场景流程（未命中场景）

适用于以下触发条件：
- `short-cut.json` 中不存在用户归一化场景（回家 / 去公司 / 接孩子）
- `addr.json` 中不存在场景终点地址别名，无法直接执行快捷下单

### 1. 全局约束
**⚠️必须先阅读以下文档**
- [异常处理流程](./references/error_handling.md)
- [接口契约](./references/api-contract.md)
- [常用地址 Schema](./addr-schema.md)
- [快捷叫车 Schema](./short-cut-schema.md)
- [订单状态模版](./references/state-schema.md)
- [设置快捷场景流程](./short-cut-setup-workflow.md)

1. **流程串行化**：禁止与快捷下单流程并行执行；进入本流程后，必须先完成场景设置再下单。同一时刻全局只允许一个用户在执行此流程（若涉及多用户，必须按序列化顺序执行）。
2. **回写事务性**：凡标注"立即写回"的步骤，必须满足以下三层验证才能进入下一步：
   - **写前验证**：先通过 [`addr-keys`](./api-contract.md#cmd_addr_keys) / [`addr-get-value`](./api-contract.md#cmd_addr_get_value) 或 [`short-cut-keys`](./api-contract.md#cmd_short_cut_keys) / [`short-cut-get-value`](./api-contract.md#cmd_short_cut_get_value) 检查 `addr.json` 和 / 或 `short-cut.json` 当前状态，确认 JSON 结构完整、可解析、无损坏。
   - **写中确认**：实际调用 [`addr-upsert-value`](./api-contract.md#cmd_addr_upsert_value) 或 [`short-cut-upsert-value`](./api-contract.md#cmd_short_cut_upsert_value) 写入目标文件，确保每个字段按要求写入，且无部分写入。
   - **写后验证**：写入完成后立即再次调用 [`addr-get-value`](./api-contract.md#cmd_addr_get_value) 或 [`short-cut-get-value`](./api-contract.md#cmd_short_cut_get_value) 回读目标对象，验证写入值与预期完全一致；若不一致立即回滚并转入异常处理。
3. **原子性保证**：
   - 单次写回不得跨越多个编辑操作；如需多文件写入（如 [`addr-upsert-value`](./api-contract.md#cmd_addr_upsert_value) + [`short-cut-upsert-value`](./api-contract.md#cmd_short_cut_upsert_value) 同时更新），必须一次性原子完成，中途任何失败都得回滚所有已作改动。
   - 禁止异步或后台写回；所有写回都必须在前台同步完成，并等待验证结果后才能继续。
   - 禁止分段写入（今天写表1，明天补写表2），每个流程的所有写回必须在该流程结束前完成。
4. **地址相关请求**：必须先调用 `poi-search`，禁止在未检索前直接判断地点或使用缓存数据。
5. **下单与询价能力复用本文档**：
   - 地址检索：见 [3. 地址检索](#short-cut-setup-poi-search)
   - 价格预估：见 [4. 价格预估](#short-cut-setup-estimate)
   - 下单：见 [5. 下单](#short-cut-setup-order)

### 2. 主流程
```
进入设置快捷场景流程
   ↓
调用 [`addr-keys`](./api-contract.md#cmd_addr_keys) / [`short-cut-keys`](./api-contract.md#cmd_short_cut_keys) 并归一化场景键（回家 / 去公司 / 接孩子）
   ↓
终点地址记忆是否存在？
   ├─ 否 → 终点地址检索与确认 → 立即调用 [`addr-upsert-value`](./api-contract.md#cmd_addr_upsert_value)
   └─ 是 → 使用已有终点
   ↓
按地址检索确认起点
   ↓
询问用户是否固定该起点为当前场景默认起点
   ↓
若同意 → 立即调用 [`short-cut-upsert-value`](./api-contract.md#cmd_short_cut_upsert_value) 写入场景记录（必要时补调 [`addr-upsert-value`](./api-contract.md#cmd_addr_upsert_value) 写入起点地址对象）
   ↓
执行价格预估并让用户确认车型
   ↓
询问是否保存车型偏好（可选）
   ↓
若同意 → 立即写回该场景偏好车型
```

#### 2.1 Step 1：终点确认（地址别名不存在时）
1. 如果用户输入不是明确 POI 名称（如“家”“公司”“xx家”），先向用户确认可检索关键词。
2. 调用 [3. 地址检索](#short-cut-setup-poi-search) 搜索终点（使用 `poi-search --scene 2`，返回结果包含推荐下车点）。
3. 用户确认后，**必须立即执行以下完整写回流程**：见 [Step 1.1 写回](#short-cut-setup-writeback-step-11)
   - **写回前检查**：调用 [`addr-keys`](./api-contract.md#cmd_addr_keys)，确认文件可读、结构完整
   - **执行写回**：按 7.2.1 规范调用 [`addr-upsert-value`](./api-contract.md#cmd_addr_upsert_value) 完整写入地址对象
   - **写后验证**：调用 [`addr-get-value`](./api-contract.md#cmd_addr_get_value) 读取刚写入的对象，逐字段对比预期值，如不一致立即报错并停止后续操作
   - 验证成功后才能进入 Step 2

#### 2.2 Step 2：起点确认与场景固化
1. 按 [3. 地址检索](#short-cut-setup-poi-search) 确认起点（使用 `poi-search --scene 1`，返回结果包含推荐上车点）。
2. 询问用户：“以后是否每次都以这个起点发起叫车？”
3. 若用户同意，**必须立即执行以下完整写回流程**：见 [Step 1.2.2 写回](#short-cut-setup-writeback-step-122)
   - **写回前检查**：(1) 调用 [`addr-keys`](./api-contract.md#cmd_addr_keys) 和 [`short-cut-keys`](./api-contract.md#cmd_short_cut_keys) 验证两个文件都完整、可解析、无损坏；(2) 检查终点地址别名是否已出现在 [`addr-keys`](./api-contract.md#cmd_addr_keys) 返回结果中
   - **原子性准备**：若起点对应地址别名不存在，先在内存中预构建该地址对象完整数据，确保两个文件的写入能被视为一个原子操作
   - **执行写回**：按 7.2.2 规范一次性完成所有写入（必要时调用 [`addr-upsert-value`](./api-contract.md#cmd_addr_upsert_value) 补齐地址 + 调用 [`short-cut-upsert-value`](./api-contract.md#cmd_short_cut_upsert_value) 写入场景记录 + 必要的 `memory.md` 更新时间），中途任何失败都立即回滚
   - **写后验证**：(1) 调用 [`short-cut-get-value`](./api-contract.md#cmd_short_cut_get_value) 读取新增/更新的场景记录，验证 `from` 和 `to` 都能通过 [`addr-get-value`](./api-contract.md#cmd_addr_get_value) 找到对应对象；(2) 逐字段对比预期值，不一致立即报错
   - 验证成功后才能进入 Step 3
5. 写回完成后，后续询价/下单必须按该场景记录中的 `from`、`to` 地址别名调用 [`addr-get-value`](./api-contract.md#cmd_addr_get_value) 回查对应对象。

#### 2.3 Step 3：询价、偏好保存与下单
1. 按本文档 [4. 价格预估](#short-cut-setup-estimate) 执行询价并展示车型。
2. 用户确认车型后由脚本自动写入 `~/.config/tms-takecar/state.json`（流程仅读取）：
   - 通过 `create-order --price-estimate-keys '<JSON数组>'` 一步完成 `userSelect` 标记与下单；如需传入偏好可追加 `--user-prefer-labels '<JSON数组>'`
3. 询问用户是否保存本次车型偏好。
4. 若用户同意，**必须立即执行第一次写回**（偏好车型）：
   - **写回前检查**：先调用 [`short-cut-keys`](./api-contract.md#cmd_short_cut_keys)，再调用 [`short-cut-get-value`](./api-contract.md#cmd_short_cut_get_value)，验证该场景记录存在
   - **执行写回**：调用 [`short-cut-upsert-value`](./api-contract.md#cmd_short_cut_upsert_value) 更新该场景记录，不修改无关字段
   - **写后验证**：再次调用 [`short-cut-get-value`](./api-contract.md#cmd_short_cut_get_value) 读取该记录，确认 `preferred_car_type` 已更新为用户选中的值，不一致立即报错
   - 验证成功后才能进入下单
5. 询问用户现在是否要下单，用户确认后执行下一步。用户如果不下单则告知用户下次可以直接使用快捷下单
5. 按[快捷叫车流程](./references/short-cut-workflow.md#short-cut-main)，以当前场景下单。

---

<a id="short-cut-setup-poi-search"></a>
### 3. 地址检索

**流程**：
1. 调用 `poi-search` 搜索地点（必须传 `scene` 参数）：
   - 起点检索（上车点）使用 `scene=1`。
   - 终点检索（下车点）使用 `scene=2`。
   - 仅做普通地点搜索且不需要推荐上下车点时使用 `scene=0`。
2. 判断是否需要用户选择：

**需要用户选择**：
- 搜索结果返回多个不同地点。
- 多个同名但位置不同的地点。
- 用户表述宽泛且结果差异大。
- **核心原则**：不能100%确定用户表述的地点。

**自动匹配**：
- 搜索结果只有1个地点。

**当需要用户选择时，用 `poi-search` 填充以下模版回复用户**
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
- 如果用户输入新的keyword则重新调用[`poi-search --scene 1/2`](./api-contract.md#cmd_poi_search) 搜索地点
- 如果用户选择翻页或者说："更多"、"下一页"则调用[`poi-search --scene 1/2 --page-index <当前page-index++>`](./api-contract.md#cmd_poi_search) 进行翻页 
- 直到用户通过回复序号，回复地点名称等方式从返回值中做出选择再进行下一步

---

<a id="short-cut-setup-writeback"></a>
### 4. 记忆写入规范

所有写回 `~/.config/tms-takecar/addr.json`、`~/.config/tms-takecar/short-cut.json` 的操作，必须通过 [`addr-upsert-value`](./api-contract.md#cmd_addr_upsert_value) / [`short-cut-upsert-value`](./api-contract.md#cmd_short_cut_upsert_value) 执行。`memory.md` 不再保存地址与快捷叫车内容。**禁止省略写回步骤，禁止仅在对话中提到"已保存"而不实际调用对应接口写入文件。**

#### 4.1 写回格式定义

**常用地址格式**（通过 [`addr-upsert-value`](./api-contract.md#cmd_addr_upsert_value) 写入 `~/.config/tms-takecar/addr.json` 对应 key）：
```json
"{地址别名}": {
  "name": "{poi.name}",
  "address": "{poi.address}",
  "poiid": "{poi.poiid}",
  "citycode": "{poi.citycode}",
  "point_name": "{point.name}",
  "point_longitude": "{point.longitude}",
  "point_latitude": "{point.latitude}"
}
```
示例：
```json
"家": {
  "name": "万科翡翠滨江",
  "address": "深圳市南山区沙河西路3088号",
  "poiid": "B0FFXXXX01",
  "citycode": "440300",
  "point_name": "万科翡翠滨江北门",
  "point_longitude": 113.934528,
  "point_latitude": 22.521867
}
```

**快捷叫车格式**（通过 [`short-cut-upsert-value`](./api-contract.md#cmd_short_cut_upsert_value) 写入 `~/.config/tms-takecar/short-cut.json`）：
这里的 `from`、`to` 对应 `addr.json` 的 `{地址别名}`，不是 `{poi.name}`。
```json
"{归一化场景键}": {
  "preferred_car_type": "{偏好车型，无则空字符串}",
  "userPreferLabels": [],
  "from": "{起点地址别名}",
  "to": "{终点地址别名}"
}
```
示例：
```json
"回家": {
  "preferred_car_type": "便宜点的，最近的司机",
  "userPreferLabels": [1],
  "from": "公司",
  "to": "家"
},
"去公司": {
  "preferred_car_type": "",
  "userPreferLabels": [],
  "from": "家",
  "to": "公司"
}
```

#### 4.2 各步骤写回清单

##### <a id="short-cut-setup-writeback-step-11"></a> 7.2.1 Step 1.1 写回（终点地址记忆补齐）
1. 调用 [`addr-upsert-value`](./api-contract.md#cmd_addr_upsert_value) 更新场景对应地址别名：
   - 回家 → 家
   - 去公司 → 公司
   - 接孩子 → 接孩子
2. 写入字段：`name`、`address`、`poiid`、`citycode`、`point_name`、`point_longitude`、`point_latitude`。

##### <a id="short-cut-setup-writeback-step-122"></a> 7.2.2 Step 1.2.2 写回（场景行新增与偏好保存）
1. 起点确认且用户同意固定起点后，调用 [`short-cut-upsert-value`](./api-contract.md#cmd_short_cut_upsert_value) 新增或覆盖场景记录：
   - `"归一化场景键": {"preferred_car_type": "", "userPreferLabels": [], "from": "{起点地址别名}", "to": "{终点地址别名}"}`
   - 其中 `{起点地址别名}`、`{终点地址别名}` 必须能在 `addr.json` 中找到对应对象
2. 若起点对应地址别名不存在，同步调用 [`addr-upsert-value`](./api-contract.md#cmd_addr_upsert_value) 补写对应地址对象。
3. 用户同意保存偏好后，将该场景记录的 `preferred_car_type` 更新为选中车型描述；若存在下单阶段偏好，同时更新 `userPreferLabels`。

#### 7.3 写回约束（严格模式）
1. **串行化执行**：同一时间只能有一个写回操作进行；禁止并发调用会修改 `addr.json` / `short-cut.json` 的 [`addr-upsert-value`](./api-contract.md#cmd_addr_upsert_value) / [`short-cut-upsert-value`](./api-contract.md#cmd_short_cut_upsert_value)，每个写回必须原子性完成。
2. **来源唯一性**：地址字段（`poi.*`、`point.*`）仅允许来自用户最终确认的 `poi-search` + 推荐上下车点结果，禁止手填、猜测或复用旧候选数据。
3. **数据完整性**：
   - 地址对象必须包含 7 个字段（`name`、`address`、`poiid`、`citycode`、`point_name`、`point_longitude`、`point_latitude`），缺一不可。
   - 快捷叫车场景对象必须包含 4 个字段（`preferred_car_type`、`userPreferLabels`、`from`、`to`）；其中 `from` 和 `to` 不得为空，必须在 `addr.json` 中现存。
   - 禁止存储空值、`null` 或占位符，允许的唯一例外是 `preferred_car_type` 可为空字符串、`userPreferLabels` 可为空数组。
4. **键值一致性**：
   - `short-cut.json` 的所有地址别名引用必须是 `addr.json` 的现存 key。
   - 同一场景键在 `short-cut.json` 中全局唯一（不得重复出现）。
   - 禁止在 `addr.json` 中使用 POI 名称作为 key，仅允许 "家"、"公司"、"接孩子" 等语义键。
5. **文件完整性**：每次写回后必须再次调用 [`addr-keys`](./api-contract.md#cmd_addr_keys) / [`addr-get-value`](./api-contract.md#cmd_addr_get_value) 或 [`short-cut-keys`](./api-contract.md#cmd_short_cut_keys) / [`short-cut-get-value`](./api-contract.md#cmd_short_cut_get_value) 验证 JSON 格式完整、可解析、无多余残留字段。

#### 7.4 回写执行规则（原子性约束）
1. **写回必须完成后才能进入下一步**：标注"立即写回"的步骤必须确保文件落盘（disk sync），验证写入成功，再进入下一业务步骤（询价、下单、后续问询）。禁止异步写回或延迟写入。
2. **原子性保证**：单次写回操作必须是原子的：
   - 如果写回包含 [`addr-upsert-value`](./api-contract.md#cmd_addr_upsert_value) 地址对象新增 + [`short-cut-upsert-value`](./api-contract.md#cmd_short_cut_upsert_value) 场景记录新增，必须两步都成功，或都失败回滚。
   - 如果任何步骤校验失败，立即停止该次写回，不得部分写入。
   - 禁止跨流程的批量延迟写入；每个流程的写回必须在该流程内完成。
3. **时间戳一致性**：
   - 单次流程内多个写回操作必须使用同一时间戳（精确到分钟）。
   - 不得在不同时刻对同一行执行多次独立写回；必须先读取当前状态，整合所有变更，一次性写入。
   - 时间戳必须按 YYYY-MM-DD HH:mm 格式，且不得早于上次更新时间。
4. **覆盖规则与版本管理**：
   - 场景记录已存在：完整覆盖（不允许字段级部分更新），新值覆盖旧值，旧数据不可恢复。
   - 场景记录不存在：新增一条记录，初始状态需符合 7.3 条 3 的字段完整性要求。
   - 若检测到同一场景键出现重复来源或引用冲突，立即报错并转入异常处理，禁止自动清理。
5. **字段级写入规则**：
   - 地址对象：仅允许整对象新增或整对象覆盖，禁止部分字段更新（如只更新 `name`）。
   - 快捷叫车对象：允许只更新 `preferred_car_type` 或 `userPreferLabels`；其他字段变更必须进行整对象覆盖。
6. **回填规则与数据一致性**：写回完成立即读取并回填 `~/.config/tms-takecar/state.json`：
   - 必须先调用 [`short-cut-get-value`](./api-contract.md#cmd_short_cut_get_value) 读取场景记录，再按其中的 `from` / `to` 调用 [`addr-get-value`](./api-contract.md#cmd_addr_get_value) 查询地址对象。
   - 如果查询失败（key 不存在），立即转入异常处理流程，禁止使用 key 文本本身当参数。
   - 回填后的 `state.json` 中 `pickup` / `dropoff` 的值必须与 `addr.json` 的对应对象完全一致。
7. **失败与回退**：
   - 任一写回步骤的校验失败（key 不存在、字段缺失、JSON 损坏、时间戳冲突）时，立即停止后续调用，转入异常处理流程。
   - 异常处理流程：(1) 记录故障原因和当前状态；(2) 通知用户流程中断，建议检查 [`addr-keys`](./api-contract.md#cmd_addr_keys) / [`short-cut-keys`](./api-contract.md#cmd_short_cut_keys) 是否还能正常返回；(3) 禁止自动修复或猜测式回滚，需明确用户确认后才能重试。
8. **禁止行为清单**（严禁）：
   - 禁止在对话中口头确认已保存而不实际编辑文件。
   - 禁止跳过写回阶段直接进入下一业务步骤。
   - 禁止复用旧流程的 `state.json` 拷贝，每次写回后必须重新读取最新的地址对象。
   - 禁止猜测式补充缺失字段，缺失时必须向用户重新确认。
   - 禁止并发调用修改同一文件的不同 [`addr-upsert-value`](./api-contract.md#cmd_addr_upsert_value) / [`short-cut-upsert-value`](./api-contract.md#cmd_short_cut_upsert_value)。
   - 禁止保留历史版本或注释字段，JSON 必须保持清洁，仅包含当前有效数据。
