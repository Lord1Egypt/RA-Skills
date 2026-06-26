# quote — 快速报价流程

---

## 一、流程概览

```
用户发起报价
    ↓
POST <gateway域名>/api/quickInsure/quickQuote
    ├─ vehicleNo 为空 → 车辆选择
    │       ├─ 无绑定车辆 → 提示用户提供车牌号
    │       ├─ 1 辆绑定车辆 → 提示用户确认是否使用此车牌
    │       └─ 多辆绑定车辆 → 返回列表供用户选择
    │       用户确认/选择后 → 带 vehicleNo 重新调用本接口
    │
    ├─ vehicleNo 不为空 → 报价主流程
    │       ├─ vehicleFiveInfoOk=false → 从 missingFiveInfoFields 获取缺失字段
    │       │       缺 vinNo/engineNo/registerDate → 用户提供后传入对应参数重试
    │       │       缺 品牌型号(jyCarModuleCode) → 用户提供品牌型号（行驶证上有）传入重试
    │       ├─ 报价成功 → 展示报价结果 → 用户确认/调整方案
    │       └─ 失败 → 按错误码处理（见三、错误处理）
    └─ 全部逻辑在同一接口内完成，仅通过 vehicleNo 是否为空区分流程分支
```

---

## 二、接口详情

### `POST /api/quickInsure/quickQuote`

#### 车辆选择（vehicleNo 留空时触发）

用户未提供车牌号时，调用 quickQuote 且 **不传 vehicleNo**（或传空字符串），后端自动查询该用户已绑定的车辆列表，根据绑定数量返回不同结果：

| 绑定数量 | result | 返回内容 | Agent 处理 |
|---------|--------|---------|-----------|
| 0 辆 | `-1` | resultMessage: "亲，未查询到您有绑定的车辆信息，请先提供车牌号" | 引导用户提供车牌号后重新调用 |
| 1 辆 | `409001` | boundVehicles: ["\<车牌号\>"]，resultMessage 含车牌号 | 向用户确认是否使用此车牌，确认后带 vehicleNo 重新调用 |
| 多辆 | `409002` | boundVehicles: ["\<车牌号1\>", "\<车牌号2\>", ...]，resultMessage 含数量 | 展示列表供用户选择，选择后带 vehicleNo 重新调用 |

**入参（Step 0）：**

```json
{}
```

> vehicleNo 留空或不传，其余字段均无需传入。

**出参示例（1 辆绑定车辆）：**

```json
{
  "code": 0,
  "msg": "ok",
  "data": {
    "result": "409001",
    "resultMessage": "检测到您有 1 辆已绑定车辆，请确认是否使用此车牌号：<车牌号>",
    "boundVehicles": ["<车牌号>"]
  }
}
```

**出参示例（多辆绑定车辆）：**

```json
{
  "code": 0,
  "msg": "ok",
  "data": {
    "result": "409002",
    "resultMessage": "检测到您有 <N> 辆已绑定车辆，请选择其中一辆",
    "boundVehicles": ["<车牌号1>", "<车牌号2>", "<车牌号3>"]
  }
}
```

**出参示例（无绑定车辆）：**

```json
{
  "code": 0,
  "msg": "ok",
  "data": {
    "result": "-1",
    "resultMessage": "亲，未查询到您有绑定的车辆信息，请先提供车牌号"
  }
}
```

---

#### 报价主流程（传入 vehicleNo 时执行）

**入参模板**

**场景 A：已绑定车辆**
```json
{
  "vehicleNo": "<车牌号>"
}
```

**场景 B：未绑定车辆（需车主信息）**
> ⚠️ **严禁自行编造车主信息**：`carOwnerName` 和 `certificateNo` 必须由用户提供（行驶证或身份证），Agent 不得猜测或虚构。

```json
{
  "vehicleNo": "<车牌号>",
  "carOwnerName": "<车主姓名>",
  "certificateNo": "<车主身份证号>",
  "isInquireBusiness": true,
  "isInquireCompel": true
}
```

**场景 C：车五项不全，用户手动补全**
> ⚠️ **严禁自行编造车辆信息**：以下所有字段必须由用户提供（行驶证），Agent 不得猜测或虚构。

```json
{
  "vehicleNo": "<车牌号>",
  "carOwnerName": "<车主姓名>",
  "certificateNo": "<车主身份证号>",
  "vinNo": "<车架号VIN>",
  "engineNo": "<发动机号>",
  "registerDate": "<注册日期YYYY-MM-DD>",
  "jyCarModuleCode": "<品牌型号>",
  "isInquireBusiness": true,
  "isInquireCompel": true
}
```

#### 字段说明

| 字段 | 类型 | 必填 | 说明                      |
|------|------|------|-------------------------|
| `vehicleNo` | string | 条件 | 车牌号（带省份前缀）；留空触发 Step 0 车辆选择 |
| `carOwnerName` | string | 条件 | 车主姓名（未绑车时必填，**仅从用户输入获取，严禁自行编造**） |
| `certificateNo` | string | 条件 | 车主身份证号（未绑车时必填，**仅从用户输入获取，严禁自行编造**） |
| `insurePlaceProvinceCode` | string | 否 | 投保地省份编码（不传则后端自动推断）      |
| `insurePlaceCode` | string | 否 | 投保地城市编码（不传则后端自动推断）      |
| `isInquireBusiness` | bool | 否 | 是否投保商业险，默认 true         |
| `isInquireCompel` | bool | 否 | 是否投保交强险，默认 true         |
| `vinNo` | string | 条件 | 车架号（手动补全时传）             |
| `engineNo` | string | 条件 | 发动机号（手动补全时传）            |
| `registerDate` | string | 条件 | 注册日期 YYYY-MM-DD（手动补全时传） |
| `jyCarModuleCode` | string | 条件 | 品牌型号（手动补全时传）            |

#### 成功出参

```json
{
  "code": 0,
  "msg": "ok",
  "data": {
    "result": "0",
    "resultMessage": "操作成功",
    "vehicleBound": true,
    "vehicleFiveInfoOk": true,
    "missingFiveInfoFields": [],
    "vehicleInfo": {
      "vehicleNo": "<车牌号>",
      "vehicleEngineNo": "<发动机号>",
      "vehicleFrameNo": "<车架号VIN>",
      "brand": "<品牌>",
      "carSerials": "<品牌+车型名称>"
    },
    "insureFlowCode": "<流程主键>",
    "quotePriceInfo": {
      "quotePriceId": "<报价ID>",
      "businessDiscount": "<折扣，如0.85>",
      "businessSumPreimum": "<商业险合计保费>",
      "bizStandardTotalPremium": "<商业险标准保费>",
      "bizDiscountPremium": "<商业险优惠金额>",
      "businessEffectiveDate": "<商业险起保日期YYYY-MM-DD>",
      "compelSumPreimum": "<交强险保费>",
      "sumPreimum": "<总保费>",
      "taxPreimum": "<车船税>",
      "insureFlowCode": "<流程主键>",
      "coverageList": [
        {
          "coverageCode": "<险种代码>",
          "coverageSimpleName": "<险种简称>",
          "amount": "<保额>",
          "coveragePreimum": "<险种保费>"
        }
      ],
      "carInfo": {
        "vehicleNo": "<车牌号>",
        "brand": "<品牌>",
        "carSerials": "<品牌+车型名称>"
      },
      "insurePlaceName": "<投保城市>",
      "insurePlaceProvinceName": "<投保省份>"
    },
    "coverageList": [
      {
        "baseRiderType": "0",
        "coverageCode": "<险种代码>",
        "coverageType": "<保额类型>",
        "coverageName": "<险种全称>",
        "coverageSimpleName": "<险种简称>",
        "isNonDeductible": "0",
        "parentCoverageCode": "",
        "sumInsured": "<保额>",
        "coveragePreimum": "<险种保费>",
        "tag": ""
      }
    ],
    "customerInfo": {
      "result": "0",
      "vehicleOwnerName": "<车主姓名（脱敏）>",
      "vehicleOwnerCertificateNo": "<车主身份证（脱敏）>",
      "vehicleOwnerPhoneNo": "<车主手机号（脱敏）>",
      "applicantName": "<投保人姓名（脱敏）>",
      "applicantCertificateNo": "<投保人身份证（脱敏）>",
      "applicantPhoneNo": "<投保人手机号（脱敏）>",
      "isAuthCert": true
    }
  }
}
```

#### 失败出参

```json
{
  "code": 0,
  "msg": "ok",
  "data": {
    "result": "A10203",
    "resultMessage": "亲，车辆信息不完整，请补充完整车五项信息",
    "vehicleFiveInfoOk": false,
    "missingFiveInfoFields": ["车架号", "发动机号", "注册日期", "品牌型号"]
  }
}
```

> `missingFiveInfoFields` 可能包含：`"车架号"`、`"发动机号"`、`"注册日期"`、`"品牌型号"`。前三个通过 `vinNo`/`engineNo`/`registerDate` 补传；`"品牌型号"` 通过 `jyCarModuleCode` 补传。

---

## 三、错误处理

| 错误码 | resultMessage | 处理方式                                       |
|--------|--------------|--------------------------------------------|
| `-1` | 未查询到绑定车辆 | 引导用户提供车牌号后重新调用                         |
| `409001` | 检测到 1 辆绑定车辆 | 向用户确认是否使用该车牌，确认后带 vehicleNo 重新调用      |
| `409002` | 检测到多辆绑定车辆 | 展示 boundVehicles 列表供选择，选择后带 vehicleNo 重新调用 |
| `A10203` | 车辆信息不完整 | 从 `missingFiveInfoFields` 获取缺失字段，引导用户补充后重试 |
| `22000` | 请选择投保城市 | 手动指定 insurePlaceCode，省会城市兜底                |
| `22004` | 请选择品牌型号 | 向用户索取 `jyCarModuleCode` 后传入重试              |
| `A12512` | 车型不匹配或未选择 | 向用户索取品牌型号传入重试                              |
| `VTYD001` | 省外地旧车需本地使用证明 | 切换投保地为车辆所在地或提示用户                           |
| `Y12430` | 保费计算出错 | 重试 3 次仍失败则终止                               |
| `P11002` | 该车辆需进行新车备案 | **立即终止**                                   |
| `F0001` | 系统错误 | 重试 3 次仍失败则告知用户                             |
| 未绑车缺少车主信息 | 亲，车辆未绑定 | 向用户索取 carOwnerName + certificateNo 后重试     |

---

## 四、投保地自动推断

`insurePlaceProvinceCode` 和 `insurePlaceCode` **均为可选字段**，不传时后端自动推断（无需 Agent 计算）。

**兜底优先级**：
1. 请求直接传入（不为空则直接使用）
2. 历史保单回填
3. 车牌前缀自动推断（省会城市兜底）

**常见省份编码参考**：

| 省份 | 编码 | 省会城市编码 |
|------|------|-------------|
| 浙江省 | 330000 | 330100 杭州 |
| 广东省 | 440000 | 440100 广州 |
| 江苏省 | 320000 | 320100 南京 |
| 上海市 | 310000 | 310100 |
| 北京市 | 110000 | 110100 |

---

## 五、CURL 示例

```bash
# 场景 A：未提供车牌，查询绑定车辆
curl -X POST "<gateway域名>/api/quickInsure/quickQuote" \
  -H "car-api-key: $CAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'

# 场景 B：已绑车（或用户选择/确认后传入车牌）
curl -X POST "<gateway域名>/api/quickInsure/quickQuote" \
  -H "car-api-key: $CAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"vehicleNo": "<车牌号>"}'

# 场景 C：未绑车
curl -X POST "<gateway域名>/api/quickInsure/quickQuote" \
  -H "car-api-key: $CAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "vehicleNo": "<车牌号>",
    "carOwnerName": "<车主姓名>",
    "certificateNo": "<车主身份证号>",
    "isInquireBusiness": true,
    "isInquireCompel": true
  }'
```

---

## 六、方案调整

报价成功后，用户可修改险种或保额，将调整后的 `coverageList` 传入 `quickQuote` 重新报价：

**保额调整**（如「三责险改200万」）：
- 从上次报价返回的 `coverageList` 中找到对应险种，修改其 `sumInsured` 字段
- 将完整 `coverageList` 作为入参 `coverageList` 传入，重新调用 `quickQuote`

**去除险种**（如「去掉车损险」、「不要三责险」）：
- 从上次报价返回的 `coverageList` 中删除对应险种（包括其子险种 `childrenCoverageList`）
- 将剩余 `coverageList` 传入重新调用 `quickQuote`

**添加险种**（如「加上司机险」）：
- 从 `coverageList` 响应字段中找到该险种，加入列表后传入重新调用

> ⚠️ **重要**：`coverageList` 必须使用上次报价返回的原始结构，并补充以下字段，否则保司报错：
> - `coverageName`（险别名称，如"第三者责任险"）— 缺失报 `23017 险别名称不可为空`
> - `baseRiderType`、`coverageType`、`parentCoverageCode` — 缺失报 `23013 险别性质不可为空`
> - `tag` 字段无需修改，保司用 `sumInsured` 计费，`tag` 仅为展示用推荐保额标记
>
> **不能只传 `coverageCode + sumInsured`**，必须保留原始结构中所有字段，仅修改 `sumInsured`。

- 调整后展示新报价，用户再次确认或继续调整，直到回复「确认投保」进入核保

---

## 七、报价结果展示模板

```
✅ 报价成功

🚗 车辆：[carInfo.carSerials]（[vehicleNo]）
📅 投保地：[insurePlaceProvinceName] [insurePlaceName]
📅 商业险起保日期：[quotePriceInfo.businessEffectiveDate]

💰 保费汇总
| 项目 | 金额 |
|------|------|
| 商业险合计 | [businessSumPreimum] 元 |
| 交强险 | [compelSumPreimum] 元 |
| **总保费** | **[sumPreimum] 元** |

> 商业险折扣：[businessDiscount] 折（优惠 [bizDiscountPremium] 元）
> 车船税：[taxPreimum] 元

📋 险种明细
| 险种 | 保额 | 保费 |
|------|------|------|
[对 quotePriceInfo.coverageList 逐项展示]
| 机动车损失保险 | [amount] 元（实际价值）| [coveragePreimum] 元 |
| 第三者责任险 | [amount/10000] 万 | [coveragePreimum] 元 |

---
如您满意此方案，回复「确认投保」开始核保
如需调整险种或保额，告诉我您想修改的内容
```
