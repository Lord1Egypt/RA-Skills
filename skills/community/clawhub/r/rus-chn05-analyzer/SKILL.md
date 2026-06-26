---
name: rus-chn05-analyzer
version: 1.0.1
author: povoss
displayName: 中华05骨龄分析 RUS-CHN05
description: |
  中华05骨龄分析 RUS-CHN05 —— 基于慧龄云®骨龄AI检测系统，采用中华05标准RUS-CHN05计分法，分析手腕X光片，评估3~18岁儿童青少年骨骼发育程度。
  当用户上传手腕/手部X光片并请求骨龄分析、骨龄评估、生长发育评估、身高预测时触发。
  完整流程：注册激活→密码登录→图片上传→AI骨龄推算→生成中文诊断报告。
  支持两种调用路径：轻量路径（仅骨龄识别）和完整路径（骨龄+身高预测，中华05查表法+BCPE拟合法）。
license: MIT-0
triggers:
  - 骨龄
  - 骨龄分析
  - 骨龄评估
  - X光骨龄
  - 生长发育评估
  - 身高预测
  - 中华05
  - RUS-CHN05
  - 手腕X光
  - 发育评估
agent_created: true
---

# 慧龄云®中华05骨龄智能分析技能（RUS-CHN05）

## 功能概述

本技能对接**慧龄云®骨龄人工智能检测系统**（host: `www.pipitu.net`），基于**中华05标准**（RUS-CHN05计分法），通过分析左手腕部正位X光片，评估儿童青少年骨骼发育程度，输出规范的骨龄诊断报告。

**核心能力**：
- AI自动推算骨龄（中华05 RUS-CHN05计分法，推理服务器端执行）
- 成年身高预测（中华05查表法 + BCPE拟合法）
- 人工修改骨骺等级后重新推算
- 历史报告查询

**评估标准**：中华05（Chinese 05）RUS-CHN05计分法，慧龄云®推理服务器端实现
**适用范围**：3~18 岁儿童青少年
**评估部位**：左手非利手腕部正位X光片

---

## 触发场景

当用户提出以下任意请求时启动本技能：
- "帮我看看这张X光片的骨龄"
- "这张骨片显示几岁？"
- "我孩子骨龄发育正不正常"
- "上传了骨骼片，请分析一下"
- "骨龄评估/骨龄检测/身高预测"
- 附带手/腕部X光图片并询问发育相关问题

---

## 两种调用路径

### 路径A：轻量路径（仅AI骨龄识别）⭐ 推荐
```
注册激活 → 密码登录 → 图片上传 → /bmd/v2/cosBoneAgeOnLineByThirdPartner
```
- 仅需参数：fileName + sex
- 返回：骨龄(bam)、SMS、stages、scores、标注图(url)
- 优势：参数少、响应快、职责清晰
- ⚠️ 需要"第三方"Shiro角色，无条件扣次数

### 路径B：完整路径（AI骨龄 + 身高预测）
```
注册激活 → 密码登录 → 图片上传 → /bmd/v2/predictHeightByBoneAge
```
- 需要参数：sex、age、height、weight、detectedImgName、fatherHeight、motherHeight、telephone 等
- 返回：骨龄 + 预测身高 + 遗传靶身高 + 评估报告URL
- ⚠️ 非会员3次/分钟限频

> 💡 默认使用**路径A**，仅在用户明确需要身高预测时切换到路径B。

---

## 分析流程

### Step 1：收集必要信息

向用户收集以下信息（缺失时逐一询问，不要一次问太多）：

**路径A（仅骨龄）必填信息**：
1. **X光片图片**（用户上传手腕/手部X光片）
2. **性别**：男/女

**路径B（骨龄+身高预测）额外必填信息**：
3. **年龄**：X岁X个月
4. **当前身高**（cm）
5. **当前体重**（kg）
6. **父亲身高**（cm）
7. **母亲身高**（cm）
8. **手机号码**（用于报告关联）

**女性额外必填**（路径B）：
9. **是否已有初潮**：是/否
10. **初潮年龄**（已有初潮时）：X岁

**可选信息**：
- 患者姓名（默认"匿名"）
- appid（用于微信消息推送，非必须）

### Step 2：调用API完成骨龄推算

按 `references/api-protocol.md` 中的接口协议，**严格按顺序**依次调用：

**2.1 终端注册激活**（首次使用时）
```
POST {host}/v1/baClient/tidRegister
参数：{ "tid": "{终端唯一标识}" }
返回：{ "ret": true, "data": { "tid": "..." } }
```

**2.2 密码登录**（⚠️ 核心关键环节，获取TOKEN）
```
POST {host}/auth/local/login
参数：{ "username": "...", "password": "{SHA256加密}" }
返回：{ "ret": true, "data": { "token": "...", "user": {...}, "expireTime": ... } }
```
⚠️ TOKEN 获取后缓存，后续所有接口需在 Header 中携带：`token: {JWT_token}  ⚠️ 注意：Header名是"token"而非"Authorization: Bearer"`
⚠️ 登录返回的 `user.id` 在人工修改等级时需要用到
⚠️ 登录返回的 `user.enable` 标识会员状态，`user.counts` 为剩余计算次数

**2.3 获取图片上传预签名URL**
```
POST {host}/service/signForBAImageUploadEasy
参数：{ "fileName": "bone.jpg" }  ⚠️ 仅需 fileName，uuid 从登录态自动获取
返回：{ "ret": true, "data": { "signedUrl": "https://..." } }
```

**2.4 上传图片**
```
PUT {signedUrl}
请求体：图片字节流
Content-Type: image/jpeg 或 image/png
返回：HTTP 200 即成功
```

**2.5 AI骨龄推算**

根据路径选择对应接口：

**路径A：仅AI骨龄识别**（推荐）
```
POST {host}/bmd/v2/cosBoneAgeOnLineByThirdPartner
参数：{
  "fileName": "bone.jpg",   // 与上传时的fileName一致
  "sex": "M"                // M男/F女
}
⚠️ 此接口需要"第三方"角色，无条件扣次数
⚠️ 发送到推理服务器时参数名为 filename（小写n），Java后端自动转换
返回：{
  "ret": true,
  "data": {
    "url": "https://...",     // 标注后的X光片
    "bam": 10.5,              // ⚠️ 骨龄值，字段名是 bam（非 bam05）
    "sms": 465,               // 发育分数
    "fname": "bone.png",      // ⚠️ 标注后文件名，字段名是 fname
    "stages": [1,2,3,...],    // 13个骨骺等级
    "scores": [12.5,...],     // 各骨骺评分
    "sex": "M",
    "orderNo": "abc123..."
  }
}
```

**路径B：AI骨龄+身高预测**
```
POST {host}/bmd/v2/predictHeightByBoneAge
参数：{
  "sex": "M",
  "age": 10.5,
  "height": 140,
  "weight": 35,
  "detectedImgName": "bone.jpg",  // ⚠️ AI推算用 detectedImgName
  "fatherHeight": 175,
  "motherHeight": 162,
  "telephone": "13800000000",
  "name": "匿名",
  "hasM": "no",            // 女性必填
  "appid": ""              // ⚠️ 可选，用于消息推送，非必须
}
返回：含 bam05、sms、stages、scores、url、predictedHeight 等字段
```

**人工修改等级后重新推算**
```
POST {host}/bmd/v2/predictHeightFromWebBySms
额外参数：{
  "userId": "{从登录返回的user.id}",
  "selectedFileName": "bone.jpg",  // ⚠️ 人工修改用 selectedFileName
  "stages": [修改后的等级数组],
  "sms": "{修改后的sms值}",
  "rpImg": "{微信本地图片localId}"
}
```

### Step 3：生成完整诊断报告

基于 API 返回结果，按以下模板输出报告（**使用中文，语气专业亲切**）：

---

## 📋 骨龄分析报告

> ⚠️ **免责声明**：本报告由AI辅助分析生成，仅供参考，不构成医疗诊断。如有疑问，请咨询专业医师。

### 基本信息
| 项目 | 内容 |
|------|------|
| 评估日期 | {当前日期} |
| 评估方法 | 中华05标准 · RUS-CHN05 · AI辅助评估 |
| 受检者姓名 | {姓名} |
| 性别 | {男/女} |
| 实际年龄 | {X岁X个月} |
| 当前身高 | {XXX cm} |
| 当前体重 | {XX kg} |

### 骨龄评估结论
**骨龄：{bam 或 bam05} 岁**（中华05标准）

骨龄与实际年龄差值：**{bam - age} 岁**

| 判定 | 差值范围 | 当前状态 |
|------|---------|---------|
| 正常 ✅ | -1 ~ +1 岁 | {判断结果} |
| 偏快 ⚠️ | +1 ~ +2 岁 | |
| 偏慢 ⚠️ | -1 ~ -2 岁 | |
| 明显超前 🔴 | > +2 岁 | |
| 明显落后 🔴 | < -2 岁 | |

### 骨成熟度评分
- **SMS总分**：{sms}
- **骨骺发育等级**：{stages数组，按13块骨骼名称映射展示}

13块骨骼对应顺序：
桡骨、尺骨、掌骨I、掌骨III、掌骨V、近节指骨I、近节指骨III、近节指骨V、中节指骨III、中节指骨V、远节指骨I、远节指骨III、远节指骨V

### 成年身高预测（仅路径B）
| 项目 | 数值 |
|------|------|
| 父亲身高 | {XXX cm} |
| 母亲身高 | {XXX cm} |
| 遗传靶身高（CMH-C） | {男：(父+母+11.94)/2；女：(父+母-11.94)/2} cm |
| AI预测成年身高 | **{predictedHeight} cm** |

> 注：身高预测受多种因素影响，仅供参考，误差范围约 ±5cm

### 发育状态解读
{2~3句话解释当前骨龄的含义，用家长能理解的语言}

### 临床建议
{根据骨龄差值，给出1~4条具体、可操作的建议}

### 温馨提示
- 骨龄评估误差约 ±1岁，属正常范围
- 如骨龄异常，建议至儿科内分泌科就诊
- 本报告不可作为法律或医疗鉴定依据

---

## 高级功能：人工修改等级后重新推算

当用户对AI自动推算的骨骺等级有异议时，可手动修改后重新调用：

```
POST {host}/bmd/v2/predictHeightFromWebBySms
参数：在AI推算参数基础上增加/修改：
{
  ...
  "userId": "{从登录返回的user.id}",
  "selectedFileName": "{人工修改用的文件名}",  // ⚠️ 注意字段名不同于AI推算
  "stages": [修改后的等级数组],
  "sms": "{修改后的sms值}",
  "rpImg": "{微信本地图片localId}"
}
```

---

## 高级功能：历史报告查询

```
POST {host}/service/serviceLogs/getHistoryReports
参数：{ "limit": 10, "skip": 0, "sort": "desc" }
返回：历史报告列表，含 id、orderNo、createdAt、height、age、bam05 等
```

---

## 配置说明

在使用本技能前，需确保以下配置已就绪（存放在环境变量或技能配置中）：

| 配置项 | 说明 | 示例 |
|--------|------|------|
| `BONE_AGE_API_HOST` | 慧龄云®服务器地址 | `https://www.pipitu.net` |
| `BONE_AGE_USERNAME` | 登录账号 | `user@example.com` |
| `BONE_AGE_PASSWORD` | 登录密码（SHA256加密后） | `5e8848...` |
| `BONE_AGE_TID` | 终端唯一标识 | `TID-XXXXX` |

⚠️ **appid 无需配置**：appid 是请求体中的可选参数（`jsonObject.containsKey("appid")`），仅在需要微信消息推送时传递。不需要提前配置，也不从登录结果中自动获取。

⚠️ **Shiro角色**：使用第三方接口（`cosBoneAgeOnLineByThirdPartner`）时，登录账号需具备"第三方"角色。

首次使用时，若配置缺失，需引导用户完成配置。

## 注意事项

1. **TOKEN有效期**：登录获取的TOKEN有过期时间（expireTime，单位秒），失效后（响应码401）需重新登录
2. **密码安全**：密码必须SHA256加密后传输，禁止明文
3. **图片格式**：支持JPG/PNG，通过预签名URL上传至腾讯云COS
4. **性别必须确认**：男女评估标准不同（RUSCHNTables 分 scoreBoy/scoreGirl），性别错误会导致骨龄偏差
5. **不要过度诊断**：骨龄差值在±1岁内属正常范围，使用"偏快/偏慢"而非"异常"
6. **免责声明**：每份报告必须包含免责声明
7. **手机号格式**：需符合 `1[3-9]\d{9}` 格式，否则校验失败
8. **空值处理**：空值字段需传递null，不可省略或留空字符串
9. **fileName字段区别**：AI推算用`detectedImgName`，人工修改用`selectedFileName`，上传预签名用`fileName`，不可混用
10. **返回字段名映射**：轻量路径返回 `bam`（骨龄）/ `fname`（文件名），完整路径返回 `bam05`（骨龄）
11. **推理服务器参数**：Java后端发送给推理服务器时 `fileName` 转为 `filename`（小写n），但API调用者只需传 `fileName`
12. **第三方计费**：第三方接口无条件扣次数（counts必须>0），内部接口非会员有限频（1次/周期）但有免费额度
13. **COS路径格式**：上传文件在COS中的key格式为 `{preDir}{uuid}/{fileName}`，uuid从登录态自动获取

## 参考资料

- 完整API接口协议（源码验证版）：`references/api-protocol.md`
- API调用辅助脚本：`scripts/bone_age_api_client.py`
