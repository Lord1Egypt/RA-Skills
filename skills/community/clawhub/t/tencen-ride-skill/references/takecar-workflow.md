<a id="takecar-main-flow"></a>
## 🚗 打车流程（必须严格按顺序执行）

### 全局执行约束
**的工具调用规则优先级高于通用对话习惯**
❌ 禁止在 workflow 约束的场景外自由回答地址、价格、订单等信息  
✅ 只能在工具调用后根据结果进行正常对话

**⚠️必须先阅读以下文档**
- [订单状态模版](./references/state-schema.md)
- [异常处理流程](./references/error_handling.md)
- [接口契约](./references/api-contract.md)

1. 每次调用工具前，必须先对照 [api_contract.md](./api_contract.md) 校验参数名和字段。
2. 若用户拒绝提供当前位置，统一回复：不提供当前位置信息则无法满足你的需求。
3. **状态文件初始化**：开启叫车流程前，若 `~/.config/tms-takecar/state.json` 已存在则调用[`delete-state`](./api-contract.md#cmd_delete_state)删除。
  - 删除命令：
  ```bash
  python3 ./scripts/tms_takecar.py delete-state
  ```
4. 地址相关请求（含上车点、下车点、模糊地名）必须先调用 [`poi-search`](./api-contract.md#cmd_poi_search)，**未调用前禁止输出地点判断、禁止直接要求用户补充更具体地址**。
5. [`poi-search`](./api-contract.md#cmd_poi_search) 的 `region` 填充规则：
     - 用户明确提到城市（如“北京的新街口”“上海人民广场”）时，优先把该城市填入 `--city-name`
     - 表达歧义（如“四川饭店”“xx驻京办事处”）时，先追问用户目的城市，再调用 `poi-search`
    - 用户未提及城市时，不传 `--city-name`，由脚本从 `~/.config/tms-takecar/env.json` 的 `resident_city` 回退
6. 禁止合并处理上下车点，必须按`### ⚠️ PLAN 计划与流程顺序强制要求`顺序逐步完成
7. 输出前必须自检：若本轮处于地址确认流程且未完成工具调用，只允许输出过渡语并立刻调用工具，不得输出自由解释。
8. 若违反本节规则，本轮回复视为无效，需要回到"先工具后回复"的流程重新执行。
9. 下游接口参数必须从 `~/.config/tms-takecar/state.json` 中读取上游结果填充，参数映射见 [state-schema.md — 下游接口参数取值映射](./state-schema.md#下游接口参数取值映射)。
10. **经纬度取值规则**：`estimate-price` 和 `create-order` 的经纬度参数必须取自候选项中的 `point_longitude` / `point_latitude`（即 `poi-search --scene 1/2` 返回的推荐点坐标）。

### ⚠️ PLAN 计划与流程顺序强制要求

**启动新的叫车流程，必须按以下顺序逐步制定计划并完成, 不能跳过或者合并**：

```
第一步：确定上车点（完成后才能进入第二步）
    ↓
第二步：确定下车点（完成后才能进入第三步）
    ↓
第三步：询价与车型确认
    ↓
第四步：下单
```

**错误示例**：
- ❌ "从武汉大学去机场" → 同时搜索"武汉大学"和"机场"
- ❌ "去机场" → 同时获取位置和搜索"机场"
- ❌ 未调用 [`poi-search`](./api-contract.md#cmd_poi_search) 直接回复：
    "上车点'华侨城'有点泛，请你先补充更具体位置（小区/门牌/地铁站）"

**正确做法**：
- ✅ "从武汉大学去机场" → 先搜索"武汉大学" → 再搜索"机场"
- ✅ "去机场" → 先获取位置 → 再搜索"机场"
- ✅ "华侨城"（上车点模糊）→ 先调用 [`poi-search(keyword=华侨城)`](./api-contract.md#cmd_poi_search) 返回候选列表，再按模版让用户选择

---

<a id="takecar-step-1-pickup"></a>
### 第一步：确定上车点

**流程**：
1. 调用 [`poi-search --scene 1`](./api-contract.md#cmd_poi_search) 搜索地点并返回推荐上车点
2. 判断是否需要用户选择：

**需要用户选择**：
- 搜索结果返回多个不同地点
- 多个同名但位置不同的地点
- 用户表述宽泛且结果差异大
- **核心原则**：不能100%确定用户表述的地点

**自动匹配**：
- 搜索结果只有1个地点

**当需要用户选择时，用[`poi-search --scene 1`](./api-contract.md#cmd_poi_search)填充以下模版回复用户**
**⚠️ 模版中的条目数严格按照[`poi-search --scene 1`](./api-contract.md#cmd_poi_search)返回值** 
**❌ 禁止自行替用户做出选择**
```markdown
### 请在以下地址中选择您的上车点

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

3. 用户确认后调用 [`select-poi`](./api-contract.md#cmd_select_poi) 收敛上车点：
    ```bash
    python3 ./scripts/tms_takecar.py select-poi --scene 1 --poiid <用户选择的poiid>
    ```
4. `pickup` 在 state 中仅保留 1 条候选（字段结构与 `poi-search` 返回 item 一致）。

---

<a id="takecar-step-2-dropoff"></a>
### 第二步：确定下车点

**⚠️ 前置条件**：必须在第一步上车点完全确定后才能开始
如果有缺失回到`### 第一步：确定上车点`

**流程**：
1. 调用 [`poi-search --scene 2`](./api-contract.md#cmd_poi_search) 搜索地点并返回推荐下车点
2. 判断是否需要用户选择：

**需要用户选择**：
- 搜索结果返回多个不同地点

**自动匹配**：
- 搜索结果只有1个地点


**当需要用户选择时，用[`poi-search --scene 2`](./api-contract.md#cmd_poi_search)填充以下模版回复用户**
**⚠️ 模版中的条目数严格按照[`poi-search --scene 2`](./api-contract.md#cmd_poi_search)返回值** 
**❌ 禁止自行替用户做出选择**
```markdown
### 请在以下地址中选择您的下车点

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


- 如果用户输入新的keyword则重新调用[`poi-search --scene 2`](./api-contract.md#cmd_poi_search) 搜索地点
- 如果用户选择翻页或者说："更多"、"下一页"则调用[`poi-search --scene 2 --page-index <当前page-index++>`](./api-contract.md#cmd_poi_search) 进行翻页 
- 直到用户通过回复序号，回复地点名称等方式从返回值中做出选择再进行下一步

直到用户从返回值中做出选择再进行下一步

3. 用户确认后调用 [`select-poi`](./api-contract.md#cmd_select_poi) 收敛下车点：
    ```bash
    python3 ./scripts/tms_takecar.py select-poi --scene 2 --poiid <用户选择的poiid>
    ```
---

<a id="takecar-step-3-estimate"></a>
### 第三步：询价与车型确认

**⚠️ 前置条件**：必须在第二步下车点完全确定后才能开始

#### 回复模版
**展示模版**：
```markdown
### 📋 行程预估
- 预估里程：{distance/1000:.1f} 公里
- 预估时长：{estimateTime/60} 分钟

### 🚗 可选车型
| 序号 | 车型 | 运力商 | 预估价格 | 优惠 |
|------|------|--------|----------|------|
| 1 | {riderInfo.riderDesc} | {sp.name} | ¥{estimatePrice/100:.2f} | {优惠信息} |
| 2 | ... | ... | ... | ... |

### 请回复"确认叫车"呼叫以上全部车型，或回复序号只呼叫部分车型（如"1,3"）
```

**优惠信息展示规则**：
- 有 `discountAmount > 0` 时展示：`减¥{discountAmount/100:.2f}`
- 有 `discountPercentage > 0` 且 `discountPercentage < 100` 时展示：`{discountPercentage/10}折`
- 无优惠时展示：`-`

#### 车型筛选规则

从用户原始叫车诉求中提取偏好，分为 **询价阶段可筛选** 和 **下单阶段参数** 两类：

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

**车型选择规则**：
- 列表只展示本轮可下单车型：筛选模式仅展示筛选后的车型；默认模式仅展示 `defaultChecked=1` 的车型
- 不展示全量车型，也不需要在列表中使用 `✅` 标记
- 用户回复"确认叫车"、"叫车"、"确认"等 → 使用当前展示列表中的全部车型下单
- 用户回复序号（如"1,3"） → 仅使用对应序号的车型下单
- 用户表达新的筛选诉求（如"太贵了，有没有30以内的"、"换个大一点的车"） → **不重新调用 [`estimate-price`](./api-contract.md#cmd_estimate_price)**，从本次询价的原始 `product` 列表中按新诉求重新筛选并展示
- 用户修改车型诉求后的每次回复，必须先完整输出一次上方「展示模版」的重筛车型列表，再补充说明文字；禁止只输出文字说明而不展示列表
- 若重筛结果为空，也必须先按「展示模版」展示默认车型列表（`defaultChecked=1`），再说明“未找到完全符合条件的车型”并引导调整条件

##### 筛选决策流程

```
询价结果返回 product 列表
    ↓
用户诉求中是否包含可筛选偏好？
    ├─ 否 → 【默认列表】展示 defaultChecked=1 的车型
    └─ 是 → 对 product 列表按偏好条件过滤
              ↓
          筛选结果是否为空？
              ├─ 否 → 【筛选列表】展示筛选后的车型
              └─ 是 → 【兜底】礼貌告知用户未找到符合条件的车型，
                       展示 defaultChecked=1 的默认车型列表，
                       引导用户调整条件（如调高预算或更换车型）
    ↓
用户诉求中是否包含不可筛选/不支持的偏好？（如"女司机"、"指定品牌"等）
    ├─ 否 → 正常展示
    └─ 是 → 在展示车型列表同时，礼貌告知"部分诉求暂时无法满足"
```

**组合诉求示例**：
- "叫个30元以内的" → 按价格筛选，展示筛选后列表
- "我想要个女司机" → 不可筛选，展示默认列表 + 告知暂不支持
- "叫个30元以内的，要女司机" → 按价格筛选展示 + 告知"女司机"暂不支持
- "我们5个人，舒服一点的" → 按座位数（≥5人→需6座车）+ 车型（舒适/商务）筛选
- "快一点来，30以内" → 按价格筛选展示，"快一点"记录到下单阶段参数

#### 流程：
1. 调用 [`estimate-price`](./api-contract.md#cmd_estimate_price) 询价：
   ```bash
  python3 ./scripts/tms_takecar.py estimate-price
   ```
2. 检查返回结果：
   - 如果 `cityStatus` 不为 `1`（上线），告知用户该城市当前不支持叫车服务，并展示 `cityMessage`，结束流程
   - 如果 `code` 不为 `0`，告知用户询价失败并展示 `message`，结束流程
3. 调用 [`estimate-price`](./api-contract.md#cmd_estimate_price) 成功后，读取 `~/.config/tms-takecar/state.json` 的 `estimate` 字段：
   - `estimateKey`：询价返回的预估 key
   - `distance`：预估里程
   - `estimateTime`：预估时长
4. 根据用户诉求筛选车型（见上方 **车型筛选规则**），确定最终展示列表
5. 向用户展示车型和价格（见上方 **展示模版**），**❌ 禁止自行替用户做出选择，❌ 禁止回复模版以外的内容**
6. 用户确认选择后（包括重新筛选后再次确认），提取命中的 `priceEstimateKey` 列表，进入第四步下单（将 `--price-estimate-keys` 传给 [`create-order`](./api-contract.md#cmd_create_order)，详见「第四步：下单」）


---

<a id="takecar-step-4-order"></a>
### 第四步：下单

**⚠️ 前置条件**：必须在第三步询价与车型确认完成后才能开始。

#### 决策流程图

```
用户确认下单
    ↓
🔧 [`create-order`](./api-contract.md#cmd_create_order)（创建订单）
    ↓
下单成功？（data.orderId 不为空）
    ├─ 是 → 更新 state.json，告知用户下单成功
    └─ 否 → 根据 unfinishedOrder、code 和 message 告知用户失败原因
```

#### 4.1 创建订单

1. 调用 [`create-order`](./api-contract.md#cmd_create_order) 创建订单：
   ```bash
    python3 ./scripts/tms_takecar.py create-order --price-estimate-keys '<JSON数组>' [--user-prefer-labels '<JSON数组>']
   ```
2. 判断下单结果：
   - `data.orderId` **不为空** → 下单成功
    - `data.orderId` **为空**（包含空字符串或字符串 `null`）→ 下单失败
    - `data.unfinishedOrder == true` → 有未完成订单，提示用户先完成或取消现有订单

#### 4.2 下单成功处理
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

#### 4.3 下单失败处理

- `data.unfinishedOrder == true`（有未完成订单）→ 告知用户存在未完成订单，需先完成或取消后再下单
- 其他失败 → 展示 `message` 告知用户失败原因，引导重试

#### `userPreferLabels` 参数说明

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

### 订单相关处理
查询、取消、询问司机位置等订单处理流程，参考： [订单处理流程](./references/order-workflow.md)

### 模版回复规则
**使用markdown模版回复用户时必须遵守以下规则**
- 当要求输出特定模版时，必须严格按照模版格式输出，禁止添加额外信息或修改模版结构。
- 模版中的字段必须保留，禁止删除或改名。
- 模版中的换行和标点符号必须保留，禁止修改为其他格式。
- 多条数据展示时，禁止合并成一句话或列表，必须保持模版的层级结构。
