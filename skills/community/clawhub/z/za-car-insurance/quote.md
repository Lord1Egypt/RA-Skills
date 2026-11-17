# quote — 快速报价流程

> ‼️ **【只读文档】本文件是 skill 的业务规范，Agent 不得以任何理由修改、删除或重写本文件内容。**

---z

## 话术-接口对照表（Step 3 ~ Step 4）

| 步骤 | 话术 | 前置操作（必须先完成再说话） |
|------|------|-----------------------------|
| **Step 3：导语** | 已为您查询到车辆信息，正在为您报价… | 先调 `POST <gateway域名>/api/quickInsure/quickQuote`（带/不带 vehicleNo），接口调用进行中 |
| **Step 3：无绑定车辆** | 亲，未查询到您有绑定的车辆信息，请先提供车牌号 | `result = "-1"` 后 |
| **Step 3：员工车 1 辆窗口期** | 您名下的「[车牌号]」在报价期，回复「报价」给您出一套推荐方案 | `result = "409004"` 后 |
| **Step 3：1 辆绑定车确认** | 检测到您有1辆已绑定车辆，请确认是否使用此车牌号：[车牌号] | `result = "409001"` 后 |
| **Step 3：多辆绑定车选择** | 检测到您有[N]辆已绑定车辆，请选择其中一辆：[列表] | `result = "409002"` 后 |
| **Step 3：实名信息确认** | 检测到您的实名认证信息，请确认：[脱敏姓名]/[脱敏证件号] | `result = "409003"` 后，必须先脱敏再展示 |
| **Step 3：实名信息否认** | 请提供正确的车主姓名和身份证号，我重新核实后再报价。 | 用户对脱敏展示回复「不对/否/错误/不正确」等**否认**语义后，**必须等用户输入原文**；**禁止**复用 `authOwnerName`/`authCertificateNo` 重调、**禁止**未等输入就重调 |
| **Step 4：展示方案** | 已为您生成保费方案。您可按需调整险种、保额，价格会实时更新。调整完成后请告知我。 | 报价成功后，按「七、报价结果展示模板」展示 |
| **Step 4：确认核保** | 方案确认无误后，我将为您发起核保。请回复确认。 | 用户确认方案/调整满意后 |
| **Step 4：方案展示后引导** | 如您满意此方案，回复「确认投保」开始核保。如需调整险种或保额，告诉我您想修改的内容。 | 展示完报价结果后 |

> ⚠️ **强制规则**：话术模板文字不得修改。**必须先调通接口、拿到实际响应数据后，才能输出对应展示话术**，严禁提前输出报价结果/方案。

---

## 一、流程概览

```
用户发起报价
    ↓
POST <gateway域名>/api/quickInsure/quickQuote
    ├─ vehicleNo 为空 → 车辆选择（按 result 分支）
    │       员工车1辆窗口期/无绑定/1辆/多辆 → 引导用户确认或提供车牌
    │       用户确认/选择后 → 带 vehicleNo 重新调用本接口
    │
    ├─ vehicleNo 不为空 → 报价主流程
    │       ├─ vehicleFiveInfoOk=false → 从 missingFiveInfoFields 取缺失字段引导补传
    │       │       缺车架号/发动机号/注册日期 → 传 vinNo/engineNo/registerDate
    │       │       缺品牌型号 → 传 jyCarModuleCode（行驶证上有）
    │       ├─ 报价成功 → 展示报价结果 → 用户确认/调整方案
    │       └─ 失败 → 按错误码处理（见三、错误处理）
    └─ 全部逻辑在同一接口内完成，仅通过 vehicleNo 是否为空区分流程分支
```

---

## 二、接口详情：`POST <gateway域名>/api/quickInsure/quickQuote`

### 车辆选择（vehicleNo 留空时触发）

不传 vehicleNo（或传空字符串），后端自动查询已绑定车辆列表，按数量返回不同 result。Agent 统一处理：展示 `resultMessage` + `boundVehicles`，引导用户确认/选择/提供车牌后，带 vehicleNo 重新调用。

| 绑定数量 | result | 关键返回字段 | Agent 处理 |
|---------|--------|------------|-----------|
| 员工车1辆窗口期 | `409004` | boundVehicles、resultMessage | 展示提示语，用户回复「报价」后带 vehicleNo 重新调用 |
| 员工车多辆窗口期 | `409002` | boundVehicles[]、resultMessage | 展示窗口期车辆列表供选择 |
| 0 辆 | `-1` | resultMessage | 引导提供车牌号 |
| 1 辆 | `409001` | boundVehicles、resultMessage | 确认是否使用此车牌 |
| 多辆 | `409002` | boundVehicles[]、resultMessage | 展示列表供选择 |

出参结构统一为 `{"code":0,"msg":"ok","data":{"result":"<上表result>","resultMessage":"<提示语>","boundVehicles":["<车牌号>"]}}`（`-1` 时无 boundVehicles）。

### 自动匹配证件号和车主姓名（carOwnerName、certificateNo 为空时触发）

请求未传车主姓名和证件号时，后端自动从实名认证系统（remember）获取并返回 `result="409003"`，附 `authOwnerName`（姓名原文）、`authCertificateNo`（证件号原文）。Agent 脱敏后展示供确认，**两个分支**：

- **用户确认（含「确认/是/对」等）** → 带 `carOwnerName`（原文）+ `certificateNo`（原文）重新调用
- **用户否认（含「不对/否/错误/不正确」等）** → **必须等待用户输入正确的姓名 + 身份证号原文**，**禁止**复用后端返回的 `authOwnerName`/`authCertificateNo`（那是被否认的数据，强行使用会形成"用错误信息强行报价"的违规），**禁止**未等用户输入就重调接口

**脱敏规则**（后端返回原文，Agent 负责脱敏展示）：
- 姓名：保留第1字，其余用 ** 代替（"张三"→"张**"）
- 证件号：保留前4后2位，中间 * 代替（"110101199001011234"→"1101************34"）
- 用户换新车牌号时，每次调用不传证件号和姓名，需重新做自动匹配

### 报价主流程入参（传入 vehicleNo 时执行）

> ⚠️ **严禁自行编造车主/车辆信息**：`carOwnerName`、`certificateNo`、`vinNo`、`engineNo`、`registerDate`、`jyCarModuleCode` 必须由用户提供（行驶证/身份证），Agent 不得猜测或虚构。

- **场景 A（已绑车）**：`{"vehicleNo":"<车牌号>"}`
- **场景 B（未绑车）**：A + `carOwnerName`、`certificateNo`、`isInquireBusiness:true`、`isInquireCompel:true`
- **场景 C（车五项不全手动补全）**：B + `vinNo`、`engineNo`、`registerDate`(YYYY-MM-DD)、`jyCarModuleCode`

**字段说明：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `vehicleNo` | string | 条件 | 车牌号（带省份前缀）；留空触发车辆选择 |
| `carOwnerName` | string | 条件 | 车主姓名（未绑车必填，**仅从用户输入获取**） |
| `certificateNo` | string | 条件 | 车主身份证号（未绑车必填，**仅从用户输入获取**） |
| `insurePlaceProvinceCode` | string | 否 | 投保地省份编码（不传则后端自动推断） |
| `insurePlaceCode` | string | 否 | 投保地城市编码（不传则后端自动推断） |
| `isInquireBusiness` | bool | 否 | 是否投保商业险，默认 true |
| `isInquireCompel` | bool | 否 | 是否投保交强险，默认 true |
| `vinNo` / `engineNo` / `registerDate` / `jyCarModuleCode` | string | 条件 | 车架号/发动机号/注册日期/品牌型号（手动补全时传） |

### 成功出参（保留全部字段名）

```json
{
  "code": 0, "msg": "ok",
  "data": {
    "result": "0", "resultMessage": "操作成功",
    "vehicleBound": true, "vehicleFiveInfoOk": true, "missingFiveInfoFields": [],
    "vehicleInfo": { "vehicleNo": "", "vehicleEngineNo": "", "vehicleFrameNo": "", "brand": "", "carSerials": "" },
    "insureFlowCode": "<流程主键>",
    "quotePriceInfo": {
      "quotePriceId": "", "businessDiscount": "<折扣,如0.85>",
      "businessSumPreimum": "<商业险合计>", "bizStandardTotalPremium": "<商业险标准保费>", "bizDiscountPremium": "<商业险优惠金额>",
      "businessEffectiveDate": "<商业险起保日YYYY-MM-DD>",
      "compelSumPreimum": "<交强险保费>", "compelEffectiveDate": "<交强险起保日>",
      "sumPreimum": "<总保费>", "taxPreimum": "<车船税>", "insureFlowCode": "",
      "coverageList": [ { "coverageCode": "", "coverageSimpleName": "<险种简称>", "coverageType": "<0车损/2责任>", "amount": "<保额>", "coveragePreimum": "<险种保费>" } ],
      "addServiceList": [ { "coverageCode": "", "tittle": "<服务名,如道路救援>", "amount": "<次数,如2>", "time": "<单位,如次>", "materialName": "", "subtittle": "", "imageUrl": "" } ]
    },
    "coverageList": [ { "baseRiderType": "0", "coverageCode": "", "coverageType": "", "coverageName": "<险种全称>", "coverageSimpleName": "", "isNonDeductible": "0", "parentCoverageCode": "", "sumInsured": "<保额>", "coveragePreimum": "", "tag": "" } ],
    "customerInfo": {
      "result": "0", "isAuthCert": true,
      "vehicleNo": "<车牌号>",
      "vehicleOwnerName/CertificateNo/PhoneNo": "<车主信息(脱敏)>",
      "applicantName/CertificateNo/PhoneNo": "<投保人信息(脱敏)>",
      "applicantProvinceName": "<投保省份>", "applicantCityName": "<投保城市>"
    }
  }
}
```

> ⚠️ 投保地展示取 `customerInfo.applicantProvinceName/applicantCityName`；`quotePriceInfo.insurePlaceProvinceName/insurePlaceName` 后端返回为空，**禁止使用**。

### 失败出参（车五项不全）

```json
{ "code": 0, "msg": "ok", "data": { "result": "A10203", "resultMessage": "亲，车辆信息不完整，请补充完整车五项信息", "vehicleFiveInfoOk": false, "missingFiveInfoFields": ["车架号", "发动机号", "注册日期", "品牌型号"] } }
```

> `missingFiveInfoFields` 取值：`车架号`/`发动机号`/`注册日期` → 用 `vinNo`/`engineNo`/`registerDate` 补传；`品牌型号` → 用 `jyCarModuleCode` 补传。

---

## 三、错误处理

| 错误码 | 含义 | 处理方式 |
|--------|------|---------|
| `-1` | 未查询到绑定车辆 | 引导提供车牌号后重新调用 |
| `409004` | 员工车1辆窗口期 | 展示提示语，用户回复「报价」后带 vehicleNo 重新调用 |
| `409001` | 1 辆绑定车辆 | 确认车牌后带 vehicleNo 重新调用 |
| `409002` | 多辆绑定车辆 | 展示 boundVehicles 供选择后重新调用 |
| `409003` | 检测到实名信息 | 脱敏展示 authOwnerName/authCertificateNo，确认后带 carOwnerName+certificateNo 重新调用 |
| `A10203` | 车辆信息不完整 | 从 missingFiveInfoFields 取缺失字段引导补充后重试 |
| `409005` | 检测到该车有历史报价 | 询问用户是否是车主亲友，是则引导用户提供 carOwnerName，带 isOwnerRelative=true 重新调用                  |
| `result="0"` 且 `noCompelReason="errCodeRules"` | **【交强险不可投保 · 禁止静默展示单商方案】** 用户请求商交报价但交强险命中重复投保错误码，后端已写入 `noCompelReason="errCodeRules"` 并返回单商报价。Agent **禁止**直接展示该单商方案，必须先告知用户：「检测到该车交强险尚未到期或已重复投保，本次无法一并投保交强险。是否切换为仅投保商业险方案继续？」等用户明确回复「是/切换/继续」后，再展示单商报价方案。用户拒绝则终止流程。 |
| `result="0"` 且 `noCompelReason="zaXRules"` | **【交强险不可投保 · 禁止静默展示单商方案】** 展业地区限制，交强险不可投保。Agent **禁止**直接展示单商方案，必须先告知用户：「当前投保地暂不支持交强险线上投保，本次仅可投保商业险。是否切换为仅投保商业险方案继续？」等用户明确确认后，再展示单商报价方案。 |
| `409006` | 车主姓名与车牌不匹配 | 提示姓名不匹配，让用户重新提供 carOwnerName 后重试                                                |
| `A12488` | 车主信息与交管不一致，请正确输入 | 提示车主信息与交管登记不一致（**交管系统数据源校验失败，单纯重提姓名无效**），引导用户**同时**提供正确的车主姓名 + 身份证号后重试 |
| `A10203` | 车辆信息不完整 | 从 `missingFiveInfoFields` 获取缺失字段，引导用户补充后重试。可引导用户上传行驶证走 `<gateway域名>/api/quickInsure/licenseOcr` 自动填充 |
| `22000` | 请选择投保城市 | 手动指定 insurePlaceCode，省会城市兜底 |
| `22004` | 请选择品牌型号 | 向用户索取 jyCarModuleCode 后重试 |
| `A12512` | 车型不匹配或未选择 | 向用户索取品牌型号重试 |
| `VTYD001` | 省外地旧车需本地使用证明 | 切换投保地为车辆所在地或提示用户 |
| `Y12430` | 保费计算出错 | 重试 3 次仍失败则终止 |
| `P11002` | 该车辆需新车备案 | **立即终止** |
| `F0001` | 系统错误 | 重试 3 次仍失败则告知用户 |
| 未绑车缺车主信息 | 车辆未绑定 | 向用户索取 carOwnerName+certificateNo 后重试 |

---

## 四、投保地自动推断

`insurePlaceProvinceCode`、`insurePlaceCode` 均可选，不传时后端自动推断（无需 Agent 计算）。

**兜底优先级**：① 请求直接传入 → ② 历史保单回填 → ③ 车牌前缀推断（用车牌前 2 位推断省份和城市，城市推断不出时再用省会城市兜底）。

**常见省份编码参考**：浙江 330000/杭州 330100、广东 440000/广州 440100、江苏 320000/南京 320100、上海 310000/310100、北京 110000/110100。

---

## 五、Bash 调用方式

> ‼️ **【强制使用脚本】** 调用本接口时，**必须使用 `scripts/api.sh`**，禁止手动拼接含中文的 curl 命令。调用方组装完整 JSON body 后传入脚本，脚本负责 Unicode 转义后发送。

```bash
# 场景A — 查询绑定车辆（不传车牌）
bash scripts/api.sh quickQuote '{}' "$CAR_API_KEY"

# 场景B — 已绑车报价（车牌含中文省份，脚本自动转义）
bash scripts/api.sh quickQuote '{"vehicleNo":"粤B88888"}' "$CAR_API_KEY"

# 场景C — 未绑车报价（车牌 + 车主姓名 + 身份证）
bash scripts/api.sh quickQuote '{"vehicleNo":"粤B88888","carOwnerName":"张三","certificateNo":"110101199001011234","isInquireBusiness":true,"isInquireCompel":true}' "$CAR_API_KEY"
```

---

## 六、方案调整

报价成功后，用户可改险种/保额，将调整后的 `coverageList` 传入 `quickQuote` 重新报价：

- **改保额**（如「三责险改200万」）：从上次报价 `coverageList` 找到对应险种，改其 `sumInsured`，整个列表传入重新调用
- **去险种**（如「去掉车损险」）：从 `coverageList` 删除对应险种（含子险种 `childrenCoverageList`），剩余列表传入重新调用
- **加险种**（如「加上司机险」）：从 `coverageList` 响应字段找到该险种，加入列表后传入重新调用

> ⚠️ **必须保留上次报价返回的原始 `coverageList` 完整结构，仅改 `sumInsured`**，不能只传 `coverageCode+sumInsured`，否则保司报错：
> - 缺 `coverageName` → 报 `23017 险别名称不可为空`
> - 缺 `baseRiderType`/`coverageType`/`parentCoverageCode` → 报 `23013 险别性质不可为空`
> - `tag` 仅展示用，无需修改；保司用 `sumInsured` 计费

> 🔒 **`baseRiderType` 取值铁律（主险/附加险标识，禁止统一填 0）**：`coverageList` 每一项的 `baseRiderType` 必须按 `parentCoverageCode` 是否为空决定，**严禁全部填 `0`**：
> - `parentCoverageCode` 为空（`""`）= **主险** → `baseRiderType` 传 `"0"`
> - `parentCoverageCode` **不为空**（挂在某主险下，如 `95L` 医保外用药责任险-三者 `parentCoverageCode="952"`、`95D` 医保外用药责任险-乘客 `parentCoverageCode="954"`）= **附加险** → `baseRiderType` 必须传 `"1"`
> - ⚠️ 直接照搬上次报价返回的 `coverageList` 时也要逐项核对：凡 `parentCoverageCode` 不为空的子险种，`baseRiderType` 一律改/保持为 `"1"`，不得跟随主险填 `"0"`

调整后展示新报价，用户确认或继续调整，直到回复「确认投保」进入核保。

---

## 七、报价结果展示模板

⛔ **取值总原则**：展示模板中所有 `[字段]` 占位符，**直接参照「二、成功出参 JSON」的字段结构取值，JSON 给什么用什么，逐字复制原值，一字不差**。唯一允许的运算是险种保额的 ÷10000 换算（见下方险种明细规则）。其余一律严禁：数学运算/加总、格式转换、用其他字段替代、上下文推断、填默认值、复用上轮缓存/历史报价。每次调用后以新返回值覆盖所有缓存字段；若某值在本次返回 JSON 中找不到，立即停止回到 JSON 重新取，不得编造。

**保费/折扣/日期类**（金额、折扣、优惠、起保日期）→ 全部取自 `data.quotePriceInfo` 下同名字段（`businessSumPreimum`/`compelSumPreimum`/`sumPreimum`/`taxPreimum`/`businessDiscount`/`bizDiscountPremium`/`businessEffectiveDate`/`compelEffectiveDate`），按 JSON 原值输出。

**⚠️ 取值易错点（必须遵守）：**
- **投保地**：取 `data.customerInfo.applicantProvinceName` + `applicantCityName`（空格拼接）；**禁止用** `quotePriceInfo.insurePlaceProvinceName`/`insurePlaceName`（后端返回为空）
- **车辆**：取 `data.customerInfo.vehicleNo`（`quotePriceInfo` 下无 carInfo）
- **交强险**：`compelSumPreimum` 不为空且不为 "0" 时，交强险金额及起保日期为必展示行，不得省略或填 0
- **起保日期**：取 `businessEffectiveDate`/`compelEffectiveDate` 原文，禁止填今天/上次/编造日期
- **折扣/优惠**：`businessDiscount`/`bizDiscountPremium` 原文，禁止增删小数位或自行计算

**险种明细（分两部分按序展示，不得合并、不得遗漏）：**

1. 逐项取 `quotePriceInfo.coverageList[]`：险种取 `coverageSimpleName`，保费取 `coveragePreimum`（原文），保额按 `coverageType` 换算（**严禁截断省略数字**）：
   - `coverageType="0"`（车损险）：`amount` 原文 + 元，如 `197714` → `197714 元`
   - `coverageType="2"`（责任险）且 `amount ≥ 10000`：`amount ÷ 10000` + 万，如 `3000000` → `300 万`，`10000` → `1 万`
   - 其他：`amount` 原文 + 元
2. 紧接逐项取 `quotePriceInfo.addServiceList[]`：险种取 `tittle`，保额取 `amount`+`time` 拼接（如"2次"），保费固定显示 `—`；列表为空则跳过

**向用户输出必须严格按以下格式，使用 Markdown 表格，禁止改用列表或纯文本：**

```
✅ 报价成功

🚗 车辆：[customerInfo.vehicleNo]
🏙️ 投保地：[customerInfo.applicantProvinceName] [customerInfo.applicantCityName]
📅 商业险起保日期：[businessEffectiveDate]
📅 交强险起保日期：[compelEffectiveDate]

💰 保费汇总

| 项目 | 金额 |
|------|------|
| 商业险合计 | [businessSumPreimum] 元 |
| 交强险 | [compelSumPreimum] 元 |
| 车船税 | [taxPreimum] 元 |
| **总保费** | **[sumPreimum] 元** |

> 商业险折扣：[businessDiscount] 折（优惠 [bizDiscountPremium] 元）

📋 险种明细

| 险种 | 保额 | 保费 |
|------|------|------|
| [coverageSimpleName] | [换算后保额] | [coveragePreimum] 元 |
| [tittle] | [amount][time] | — |

---

如您满意此方案，回复「确认投保」开始核保
如需调整险种或保额，告诉我您想修改的内容
```

---

## 八、行驶证 OCR

### `POST <gateway域名>/api/quickInsure/licenseOcr`

**触发场景**：报价时车五项缺失（如 `quickQuote` 返回 `A10203` + `missingFiveInfoFields`），引导用户上传行驶证图片自动提取。

**请求**：multipart/form-data，字段 `file`（行驶证图片，png/jpeg），Header `car-api-key: $CAR_API_KEY`

**响应字段：**

```json
{
  "code": 0, "msg": "ok",
  "data": {
    "result": "0",
    "vehicleNo": "<车牌号>", "vinNo": "<车架号>", "engineNo": "<发动机号>",
    "registerDate": "YYYY-MM-DD", "carOwnerName": "<车主姓名>",
    "vehicleType": "<车辆类型>", "brandModel": "<品牌型号>",
    "useCharacter": "<使用性质>", "issueDate": "YYYY-MM-DD",
    "ocrFileUrl": "<行驶证图片 URL>"
  }
}
```

**Agent 处理流程：**

1. 用户上传行驶证图片后调用此接口
2. **【强制】将识别结果脱敏展示给用户二次确认** — OCR 可能存在误识别，**不得在用户确认前直接调用 quickQuote**
3. 用户确认无误后，字段透传 quickQuote：
   - `vinNo` / `engineNo` / `registerDate` → 直接对应
   - `brandModel` → 作为 `jyCarModuleCode`（后端自动转精友编码）
   - `carOwnerName` → 作为车主姓名候选
4. 用户指出某字段错误时，按用户更正值传入，未提及字段沿用 OCR 结果
5. **OCR 字段属敏感信息**，按脱敏规则展示（车牌、VIN、发动机号、姓名均需脱敏）

**⚠️ 关键：OCR 不返回身份证号** — 行驶证上不含身份证号，OCR 不会返回 `certificateNo`。当 quickQuote 缺 `certificateNo` 时：
- **首次报价（无历史/未绑车）** → 直接向用户索取车主身份证号，带 `carOwnerName` + `certificateNo` 调 quickQuote。**不要**走亲友通道（`isOwnerRelative=true`）
- **亲友通道（`409005`）** → 例外场景：用户确认是车主亲友后，只传 `carOwnerName` + `isOwnerRelative=true`（不传 certificateNo），后端用历史车辆证件号回填

**二次确认话术（字段以 OCR 实际返回为准，未识别字段不展示，识别失败字段提示用户手动提供）：**

```
已识别到行驶证信息，请确认是否正确：

车牌号：<脱敏车牌>
车架号：<脱敏 VIN>
发动机号：<脱敏发动机号>
注册日期：YYYY-MM-DD
品牌型号：<品牌型号>
车主姓名：<脱敏姓名>

如全部正确请回复「确认」，如有错误请告诉我具体哪一项需要修正。
```
