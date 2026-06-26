# 慧龄云®骨龄人工智能检测系统 API接口协议

> 来源：基于 Java 后端源码（neutronnet-new）逆向校验
> Host: `www.pipitu.net`（HTTPS 443端口）
> 最后更新：2026-06-04

## 1. 适用范围

本协议为第三方系统接入慧龄云®骨龄人工智能检测系统的 API 接口规范。所有接口结构、参数、返回值均经源码验证，确保开发对接无歧义。

## 2. 两种调用路径

第三方系统可根据业务需求选择以下路径：

### 路径A：轻量路径（仅AI骨龄识别）
```
注册激活 → 密码登录 → 图片上传 → AI骨龄识别
```
- 接口：`/bmd/v2/cosBoneAgeOnLineByThirdPartner`
- 优势：参数少（只需 fileName + sex），响应快
- 适用：仅需骨龄评估，不需要身高预测
- ⚠️ 需要"第三方"角色，无条件扣次数

### 路径B：完整路径（AI骨龄 + 身高预测）
```
注册激活 → 密码登录 → 图片上传 → AI骨龄+身高预测
```
- 接口：`/bmd/v2/predictHeightByBoneAge`
- 优势：返回骨龄 + 预测身高 + 遗传靶身高等完整信息
- 适用：需要生长发育全面评估
- ⚠️ 需要更多参数（身高、体重、父母身高等）

> 💡 **推荐**：第三方接入优先使用**路径A**（轻量路径），参数简单、职责清晰。

## 3. 基础通用规范

- **传输协议**：HTTPS（443端口，证书 www.pipitu.net.jks）
- **请求方式**：核心业务接口统一采用 POST（请求体为 JSON 格式）；文件上传接口通过预签名 URL 采用 PUT
- **字符编码**：统一使用 UTF-8
- **数据格式**：请求体、返回体均为标准 JSON 格式；空值字段需传递 null（不可省略或留空字符串）；字段名严格大小写匹配
- **鉴权规则**：
  - 除"注册激活、密码登录"接口外，其余所有接口均需携带有效 TOKEN
  - TOKEN 从登录接口返回的 `data.token` 字段获取
  - TOKEN 失效（响应码 401）时需重新执行登录流程
  - ⚠️ **Header 格式：`token: {JWT_token}`**（源码验证：`req.getHeader(Constants.PARAM_DIGEST)` 其中 `PARAM_DIGEST = "token"`，**不是** `Authorization: Bearer`）
- **Shiro 角色**：第三方接口需要 `"第三方"` 角色（`@RequiresRoles("第三方")`），登录账号需具备此角色
- **文件上传**：通过预签名 URL 直传文件至腾讯云 COS（bucket: pipitu-1255772158, region: ap-chengdu），PUT 请求提交文件字节流，响应码 200 即为上传成功

## 4. 核心交互流程

### 4.1 终端注册激活（前置接口，无鉴权）

| 项目 | 详情 |
|------|------|
| 接口地址 | `{host}/v1/baClient/tidRegister` |
| 请求方式 | POST |
| 是否鉴权 | 否 |

**请求参数**：

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| tid | string | 是 | 终端唯一标识 |

**返回参数**：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| ret | boolean | 成功标识 |
| msg | string | 失败时返回错误原因 |
| data.tid | string | 与请求一致的 TID |

---

### 4.2 密码登录（核心鉴权入口，获取TOKEN）

| 项目 | 详情 |
|------|------|
| 接口地址 | `{host}/auth/local/login` |
| 请求方式 | POST |
| 是否鉴权 | 否 |

**请求参数**：

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| username | string | 是 | 登录账号 |
| password | string | 是 | 登录密码，需 SHA256 加密后传输，禁止明文 |

**返回参数**：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| ret | boolean | 成功标识 |
| msg | string | 失败提示信息 |
| data.token | string | 鉴权 TOKEN，后续所有接口需携带 |
| data.user | object | 用户信息，含 id、enable（VIP 状态）、counts（剩余次数）等 |
| data.expireTime | number | TOKEN 过期时间（秒） |

> ⚠️ 登录返回的 `data.user.id` 在人工修改等级时需要用到。`data.user.enable` 标识会员状态，`data.user.counts` 为剩余计算次数。

---

### 4.3 图片上传前置（获取预签名URL）

| 项目 | 详情 |
|------|------|
| 接口地址 | `{host}/service/signForBAImageUploadEasy` |
| 请求方式 | POST |
| 是否鉴权 | 是 |

**请求参数**：

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| fileName | string | 是 | 文件名（含后缀，如：bone.jpg 或 bone.dcm） |

> 💡 **源码验证**：此接口仅需 `fileName` 参数。uuid 从 Shiro 登录态自动获取（`SecurityUtils.getSubject().getPrincipal()`），COS 对象 key 格式为 `{preDir}{uuid}/{fileName}`。预签名 URL 有效期 30 分钟，PUT 方式上传。

**返回参数**：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| ret | boolean | 成功标识 |
| data.signedUrl | string | 预签名上传地址（PUT 请求直传文件） |

---

### 4.4 图片上传（通过预签名URL）

| 项目 | 详情 |
|------|------|
| 接口地址 | signedUrl（从 4.3 获取） |
| 请求方式 | PUT |
| 是否鉴权 | 否（预签名 URL 已包含鉴权信息） |
| 请求体 | 文件字节流（Content-Type: image/jpeg 或 image/png） |

**返回结果**：

| 响应码 | 说明 |
|--------|------|
| 200 | 上传成功 |

---

### 4.5 AI骨龄识别（轻量路径 — 第三方专用）

| 项目 | 详情 |
|------|------|
| 接口地址 | `{host}/bmd/v2/cosBoneAgeOnLineByThirdPartner` |
| 请求方式 | POST |
| 是否鉴权 | 是（需 TOKEN + "第三方"角色） |
| 超时时间 | 20秒 |
| 计费方式 | **无条件扣次数**（counts 必须 > 0，否则返回"需要购买计算次数"） |

**请求参数**：

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| fileName | string | 是 | 上传图片时的文件名（与 4.3 中 fileName 一致） |
| sex | string | 是 | 性别：M（男）/F（女），支持中文"男"/"女"自动转换 |
| logo | string | 否 | 水印 logo 标识 |

> ⚠️ **关键细节**：发送到推理服务器（Flask）时，参数名为 `filename`（小写 n），不是 `fileName`。Java 后端自动做了字段名转换。另外还自动附带 `uuid`（从登录态获取）和 `vip`（布尔值，从用户会员状态判断）。

**返回结果**：

统一返回格式：
```json
{
  "ret": true,
  "data": {
    "url": "https://...",     // 标注后的X光片图片URL
    "bam": 10.5,              // ⚠️ 骨龄值（岁），字段名是 bam，不是 bam05
    "sms": 465,               // 骨成熟度评分（会员返回浮点，非会员返回整数）
    "fname": "bone.png",      // ⚠️ 标注后文件名（统一转为.png），字段名是 fname
    "stages": [1,2,3,...],    // 13个骨骺发育等级数组
    "scores": [12.5,...],     // 各骨骺评分（会员返回浮点scores，非会员用RUSCHNTables重新计算）
    "sex": "M",               // 性别
    "orderNo": "abc123..."    // 订单号（UUID，无横线）
  }
}
```

**返回字段详细说明**：

| 字段名 | 类型 | 会员返回 | 非会员返回 | 说明 |
|--------|------|---------|-----------|------|
| url | string | ✅ | ✅ | 标注后的X光片图片URL |
| bam | number | ✅（浮点） | ✅（浮点） | 骨龄值（岁），中华05标准 |
| sms | number | ✅（浮点，插值法） | ✅（整数） | 骨成熟度评分 |
| fname | string | ✅ | ✅ | 标注后文件名（统一.png后缀） |
| stages | array[int] | ✅ | ✅ | 13个骨骺等级数组 |
| scores | array[float/int] | ✅（浮点，推理服务器原始值） | ✅（整数，RUSCHNTables重算） | 各骨骺评分 |
| sex | string | ✅ | ✅ | 性别 |
| orderNo | string | ✅ | ✅ | 订单号 |

> 💡 **会员 vs 非会员 scores 差异**：推理服务器返回的 scores 为浮点数（非标准），会员直接使用；非会员则用 `RUSCHNTables.calculateSmsByStages()` 重新计算标准整数分值。会员使用 `SMSTables.calculateBoneAgeBySMSLinear()` 线性插值法提升精度。

---

### 4.6 AI骨龄识别（内部在线接口，非第三方专用）

| 项目 | 详情 |
|------|------|
| 接口地址 | `{host}/bmd/v2/cosBoneAgeOnLine` |
| 请求方式 | POST |
| 是否鉴权 | 是（需 TOKEN） |
| 超时时间 | 20秒 |
| 限频 | 非会员 1 次/周期（AI_CD_EXPIRE_TIME），会员无限 |

**请求参数**：同 4.5（fileName + sex + 可选 telephone/logo）

**返回结果**：同 4.5

> ⚠️ 此接口为内部使用，非会员有限频但查看次数不扣次数；第三方应使用 4.5 的 `cosBoneAgeOnLineByThirdPartner`。

---

### 4.7 AI骨龄推算+身高预测（完整路径）

| 项目 | 详情 |
|------|------|
| 接口地址 | `{host}/bmd/v2/predictHeightByBoneAge` |
| 请求方式 | POST |
| 是否鉴权 | 是（需 TOKEN + `report.create` 权限） |
| 超时时间 | 10秒 |
| 限频 | 非会员 3 次/分钟 |

**请求参数**：

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| sex | string | 是 | 性别：M/F/O |
| age | number | 是 | 年龄（岁），男1~18，女1~16.5 |
| height | number | 是 | 身高（cm），30~300 |
| weight | number | 是 | 体重（kg），需大于0 |
| detectedImgName | string | 是 | ⚠️ AI推算用 `detectedImgName`（非 fileName） |
| fatherHeight | number | 是 | 父亲身高（cm），需大于0 |
| motherHeight | number | 是 | 母亲身高（cm），需大于0 |
| telephone | string | 是 | 手机号码，需符合 `1[3-9]\d{9}` |
| name / pname / panme | string | 否 | 患者姓名，三种字段名兼容 |
| hasM | string | 女性必填 | yes/no，是否有初潮 |
| moonAge | number | 条件必填 | 初潮年龄，hasM=yes 时必填 |
| appid | string | 否 | ⚠️ 可选参数，用于微信消息推送（如需推送评估结果通知则传递） |
| userId | string | 否 | 指定关联用户ID，不传则使用当前登录用户 |
| isWhiteMan | boolean | 否 | 是否白种人，默认 false |
| orderNo | string | 否 | 订单号，有值时携带 |
| scores | array | 否 | 会员可直接传 scores 跳过 AI 评分 |
| sms | number | 否 | 会员可直接传 sms 跳过 AI 评分 |

> ⚠️ **appid 说明**：appid 是请求体中的**可选参数**（`jsonObject.containsKey("appid")`），用于微信小程序消息推送。不需要提前配置或从登录结果中获取——如果需要推送通知则传递对应小程序的 appid，否则可不传。

**返回结果关键字段**：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| bam05 | number | 骨龄值（岁），中华05标准 |
| sms | number | 骨成熟度评分 |
| stages | array[int] | 13个骨骺发育等级数组 |
| scores | array | 各骨骺评分详情 |
| url | string | 标注后的X光片图片URL |
| predictedHeight | number | 预测成年身高（cm） |
| geneticHeight | number | 遗传靶身高（cm），CMH-C 法计算 |
| needPay | number | 非会员时返回，需支付金额（分） |
| discount | number | 非会员时返回，折扣系数 |
| orderNo | string | 订单号 |

**非会员特殊处理**：
- 非会员有 counts > 0 时：扣次数，返回完整结果
- 非会员 counts = 0 时：保存欠费记录，返回**模糊结果**（预测身高末位用 `*` 替换），并返回 needPay 和 discount
- 报告URL：`https://www.pipitu.net/RUSCHNAIReport.html?orderNo={orderNo}`

**遗传靶身高计算公式**（源码验证）：
- CMH-C 法：男 `(fatherHeight + motherHeight + 11.94) / 2`；女 `(fatherHeight + motherHeight - 11.94) / 2`
- FPH-C 法：男 `36.82 + 0.81 × (fatherHeight + motherHeight)`；女 `23.05 + 0.83 × (fatherHeight + motherHeight)`

---

### 4.8 人工修改等级后重新推算

| 项目 | 详情 |
|------|------|
| 接口地址 | `{host}/bmd/v2/predictHeightFromWebBySms` |
| 请求方式 | POST |
| 是否鉴权 | 是 |

**请求参数**：在 4.7 的基础上增加：

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| userId | string | 是 | 从登录返回的 user.id 获取 |
| selectedFileName | string | 是 | ⚠️ 人工修改用 `selectedFileName`（非 detectedImgName） |
| stages | array[int] | 是 | 修改后的骨骺等级数组 |
| sms | string | 是 | 修改后的 sms 值 |
| rpImg | string | 是 | 微信本地图片 localId |

---

### 4.9 修改等级/分数重新计算（工具接口）

| 场景 | 接口地址 | 说明 |
|------|---------|------|
| 修改等级重算 | `{host}/bmd/v1/calculateBoneAgeByStages` | 传 stages + sex |
| 修改分数重算 | `{host}/bmd/v1/calculateBoneAgeByScores` | 传 scores + sex |
| 直接上传分数 | `{host}/bmd/v1/calculateBoneAgeByPureScores` | 传 sms 数组 |
| v2终端测评 | `{host}/bmd/v2/smsBoneAge` | 桡骨等级6支持自定义 |
| v3终端测评 | `{host}/bmd/v3/smsBoneAge` | 各等级使用浮点类型 |

---

### 4.10 历史报告查询

| 项目 | 详情 |
|------|------|
| 接口地址 | `{host}/service/serviceLogs/getHistoryReports` |
| 请求方式 | POST |
| 是否鉴权 | 是 |

**请求参数**：

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| limit | number | 是 | 每页条数，默认 10 |
| skip | number | 是 | 跳过条数（分页） |
| sort | string | 是 | desc（降序）/ asc（升序） |

**返回参数**：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| ret | boolean | 成功标识 |
| data.data | array | 报告列表，含 id、orderNo、createdAt、height、age、bam05 等 |
| data.total | number | 报告总条数 |

---

## 5. 统一返回格式

```json
{
  "ret": true,          // boolean，成功标识
  "msg": "提示信息",     // string，失败时返回错误原因
  "data": {},           // object，成功时返回的业务数据
  "error": "错误信息"    // string，可选，服务器异常时返回
}
```

## 6. 骨龄差值解读标准

| 骨龄差值（骨龄 - 实际年龄）| 解读 |
|---------------------------|------|
| > +2岁 | 骨龄明显超前，需警惕性早熟 |
| +1 ~ +2岁 | 骨龄偏大，发育偏快 |
| -1 ~ +1岁 | 骨龄正常范围 |
| -1 ~ -2岁 | 骨龄偏小，发育偏慢 |
| < -2岁 | 骨龄明显落后，需警惕生长激素缺乏等 |

## 7. 遗传靶身高计算（源码验证）

- **CMH-C 法**（中华05标准）：
  - 男：(父亲身高 + 母亲身高 + 11.94) / 2
  - 女：(父亲身高 + 母亲身高 - 11.94) / 2
- **FPH-C 法**：
  - 男：36.82 + 0.81 × (父亲身高 + 母亲身高)
  - 女：23.05 + 0.83 × (父亲身高 + 母亲身高)

> ⚠️ 遗传靶身高 ±11.94 是中华05标准与经典 CMH（±13）的区别。

## 8. 免责声明

本系统评估结果由 AI 辅助生成，仅供参考，不构成医疗诊断。骨龄评估存在约 ±1 岁的正常观察误差。如有异常，请前往正规医疗机构儿科内分泌科就诊。
