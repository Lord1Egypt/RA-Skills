---
name: shuzhi-open
description: 数秦开放平台统一接口封装，支持区块链API服务、自动化取证、保管单组件、电子签章
keywords:
  - 数秦
  - 区块链
  - 上链
  - 自动化取证
  - 保管单
  - 电子签章
  - 电子印章
  - 签章
  - 合同
  - 合同签署
---

# shuzhi-open

数秦开放平台统一接口封装，支持区块链API服务、自动化取证、保管单组件、电子签章。

> ⚠️ **重要原则：所有不确定的信息必须询问用户，禁止自动填充！**
>
> 本 skill 涉及法律效力文件（保管单、电子合同等），所有字段必须：
> - ✅ 由用户明确提供
> - ✅ 来源可追溯
> - ✅ 格式已确认
>
> **禁止行为：**
> - ❌ 自动填充任何未确认的字段
> - ❌ 假设字段的计算方式（如 evidenceHash）
> - ❌ 猜测模板的字段定义

## 配置

编辑 `config.json`，填入你的凭证和产品标识：

```json
{
  "baseUrl": "接口地址",
  "appKey": "你的 appKey",
  "appSecret": "你的 appSecret",
  "products": {
    "chain": {
      "endpoints": {
        "upload": { "productId": "上链产品标识" },
        "queryResult": { "productId": "查询结果产品标识" }
      }
    },
    "evidence": { "productId": "自动化取证产品标识" },
    "certificate": { "productId": "保管单产品标识" },
    "sign": { "productId": "电子签章产品标识" }
  }
}
```

> ⚠️ 注意：
> - `appKey` 和 `appSecret` 由数秦开放平台提供
> - 区块链API服务的每个接口都有独立的产品标识，需要分别配置

## 用法

### 区块链API服务

支持数据上链存证，支持 `tritium` 和 `conflux` 两条链。

#### 数据上链
```bash
node scripts/chain/upload.js --data "业务数据"
```

#### 带可选参数上链
```bash
node scripts/chain/upload.js --data '{"ano":"BQ123","sha256":"xxx"}' --business EVIDENCE_PRESERVATION --source BQ_INTERNATIONAL
```

#### 批量查询上链结果
```bash
node scripts/chain/query.js --index "交易索引"
```

#### 查询多个交易
```bash
node scripts/chain/query.js --index "索引1,索引2,索引3"
```

---

### 自动化取证

支持拼多多、淘宝、抖音、公众号取证。

**⚠️ 重要：所有不确定的信息必须询问用户！**

**取证类型：**
- `1` - 拼多多电商取证
- `3` - 淘宝电商取证
- `4` - 抖音电商取证
- `12` - 公众号取证

**🌟 推荐：交互式取证（会询问所有必要信息）**
```bash
node scripts/evidence/create-task-interactive.js
```

#### 创建取证任务（命令行）
```bash
node scripts/evidence/create-task.js --batch-id "批次ID" --url "https://..." --type 1 --att-id "保全号"
```

---

### 📋 自动化取证流程（交互式）

**核心原则：所有不确定的信息必须询问用户！**

#### Step 1: 询问取证类型

```
📋 请选择取证类型：

| 序号 | 类型 | 说明 |
|------|------|------|
| 1 | 拼多多电商取证 | 商品详情页、店铺信息等 |
| 3 | 淘宝电商取证 | 商品详情页、店铺信息等 |
| 4 | 抖音电商取证 | 商品详情页、店铺信息等 |
| 12 | 公众号取证 | 公众号文章内容 |

请输入序号或类型代码：
```

#### Step 2: 询问取证信息

```
❓ 请提供以下信息：

取证类型: [已选择]

取证信息:
  取证URL: [填写网页地址]
  批次ID: [填写]
  保全号: [填写]
  取证名称: [可选，直接回车跳过]

可选参数:
  是否取证营业执照: [yes/no]
```

**示例回复：**
```
取证类型: 拼多多电商取证

取证信息:
  取证URL: https://mobile.yangkeduo.com/goods.html?goods_id=xxx
  批次ID: batch-001
  保全号: att-001
  取证名称: 测试取证

可选参数:
  是否取证营业执照: no
```

#### Step 3: 确认信息

```
📝 确认信息

取证类型: 拼多多电商取证

取证信息:
  取证URL: https://mobile.yangkeduo.com/goods.html?goods_id=xxx
  批次ID: batch-001
  保全号: att-001
  取证名称: 测试取证

可选参数:
  是否取证营业执照: 否

确认创建取证任务？(yes/no)
```

#### Step 4: 执行并返回结果

```
确认后执行：
1. 创建取证任务
2. 返回任务状态
3. 提供查询和下载方式
```

---

### ❓ 必须询问的问题

| 信息 | 必须询问的问题 |
|------|----------------|
| 取证类型 | 选择哪种取证类型？ |
| URL | 要取证的网页地址是什么？ |
| 批次ID | 如何标识这批取证任务？ |
| 保全号 | 如何标识单个取证任务？ |
| 是否需要营业执照 | 是否需要取证营业执照？（可选） |

---

### CAP-保管单组件

生成和管理保管单 PDF 文件。

**🌟 推荐：交互式生成（会询问所有不确定的信息）**
```bash
node scripts/certificate/generate-interactive.js
```

#### 生成保管单（命令行）
```bash
node scripts/certificate/create.js --file params.json
```

#### 下载保管单
```bash
node scripts/certificate/download.js --cert-no "存证编号"
```

#### 获取模板列表
```bash
node scripts/certificate/templates.js
```

---

### 电子签章

完整的电子签章流程管理。

**⚠️ 重要：所有不确定的信息必须询问用户！**

**🌟 推荐：AI 助手通过对话收集信息后调用**
```bash
node scripts/sign/workflow.js --contract "合同文件路径" --signers '[{"signerNo":"甲方","type":"enterprise",...}]'
```

**交互式模式（用户直接在终端输入）**
```bash
node scripts/sign/workflow.js --interactive
```

**使用配置文件**
```bash
node scripts/sign/workflow.js --file signers.json
```

#### 企业主体管理
```bash
# 创建企业
node scripts/sign/enterprise.js create --name "公司名称" --credit-code "统一社会信用代码"

# 查询企业列表
node scripts/sign/enterprise.js list --name "公司名称"

# 查询企业详情
node scripts/sign/enterprise.js detail --user-id "用户ID"

# 删除企业
node scripts/sign/enterprise.js delete --user-id "用户ID"
```

#### 个人主体管理
```bash
# 创建个人
node scripts/sign/person.js create --name "姓名" --id-card "身份证号"

# 查询个人列表
node scripts/sign/person.js list --name "姓名"

# 查询个人详情
node scripts/sign/person.js detail --user-id "用户ID"

# 删除个人
node scripts/sign/person.js delete --user-id "用户ID"
```

#### 签署流程管理
```bash
# 创建签署流程
node scripts/sign/sign-flow.js create --file params.json

# 查询流程详情
node scripts/sign/sign-flow.js detail --flow-id "流程ID"

# 获取签署链接
node scripts/sign/sign-flow.js preview --flow-id "流程ID"

# 获取签署文件
node scripts/sign/sign-flow.js files --flow-id "流程ID"

# 获取签署方列表
node scripts/sign/sign-flow.js signers --flow-id "流程ID"

# 下载签署后的文件
node scripts/sign/sign-flow.js download --flow-id "流程ID" [--output "输出路径"]
```

---

## 📋 电子签章流程（交互式）

**核心原则：所有不确定的信息必须询问用户！**

### Step 1: 询问合同文件和签署方数量

```
❓ 请提供以下信息：

合同文件:
  文件路径: [填写PDF/DOCX/DOC路径，最大10MB]

签署方:
  共几个签署方: [填写总数，最多6个]
  其中企业方: [填写几方企业]
  其中个人方: [填写几方个人]
```

### Step 2: 提供信息填写模板

根据签署方数量，提供填写模板：

```
【企业方 1】
  企业名称: [填写]
  统一社会信用代码: [填写]
  联系人姓名: [填写]
  联系人身份证: [填写]
  联系人手机: [填写]

【个人方 1】
  姓名: [填写]
  身份证: [填写]
  手机: [填写]

（如有多个企业方/个人方，按序号继续：企业方 2、个人方 2...）
```

### Step 3: 确认信息

```
📝 确认信息

合同文件: [文件路径]
签署方: [X]方企业 + [Y]方个人

【企业方】
  签署方标识: xxx
  企业名称: xxx
  ...

【个人方】
  签署方标识: xxx
  姓名: xxx
  ...

确认创建签署流程？(yes/no)
```

### Step 4: 执行流程

用户确认后，AI 助手执行脚本：

```bash
node scripts/sign/workflow.js --contract "合同文件路径" --signers '[
  {
    "signerNo": "甲方",
    "type": "enterprise",
    "enterpriseName": "企业名称",
    "creditCode": "统一社会信用代码",
    "contactName": "联系人姓名",
    "contactIdCard": "联系人身份证",
    "contactMobile": "联系人手机"
  },
  {
    "signerNo": "乙方",
    "type": "person",
    "name": "姓名",
    "idCard": "身份证号",
    "mobile": "手机号"
  }
]'
```

**注意**：
- `--signers` 参数需要用单引号包裹 JSON 字符串
- 企业签署方 `type` 为 `"enterprise"`
- 个人签署方 `type` 为 `"person"`

执行结果：
1. 创建主体（企业/个人）
2. 创建印章
3. 上传合同文件
4. 创建合同模板
5. 返回预览链接（用户配置签署位置）

---

### ❓ 必须询问的问题

| 信息 | 必须询问的问题 |
|------|----------------|
| 合同文件 | 合同文件路径是什么？文件格式是否符合要求？ |
| 签署方数量 | 共有几个签署方？ |
| 签署主体类型 | 是企业签署还是个人签署？ |
| 企业信息 | 企业名称、统一社会信用代码是什么？ |
| 个人信息 | 姓名、身份证号、手机号是什么？ |
| 印章样式 | 使用什么印章样式？（默认：模板印章） |

---

### ⚠️ 禁止行为

**❌ 禁止自动填充以下信息：**
- 签署方的姓名、身份证、手机号
- 企业名称、统一社会信用代码
- 合同文件路径
- 印章样式（除非用户确认使用默认）

**❌ 禁止假设：**
- 假设用户只有一个签署方
- 假设签署方的角色（甲方/乙方）
- 假设印章样式或字体

---

### 信息收集模板

请用户提供以下信息：

**1. 合同文件（必填）**
- 合同文件路径（支持格式：PDF、DOCX、DOC，最大10MB）

**2. 签署方信息（最多6个）**

| 字段 | 说明 | 示例 |
|------|------|------|
| 签署方标识 | 如：甲方、乙方、丙方等 | 甲方 |
| 签署主体类型 | 企业 或 个人 | 企业 |
| 企业名称 | 公司全称（企业必填） | XX科技有限公司 |
| 统一社会信用代码 | 18位信用代码（企业必填） | 91XXXXXXXXXXXXXXX |
| 姓名 | 签署人姓名（个人必填）/ 联系人姓名（企业必填） | 张三 |
| 身份证 | 18位身份证号 | 36XXXXXXXXXXXXXXX |
| 手机号码 | 11位手机号 | 138XXXXXXXX |

**注意**：用户必须先提供合同文件路径，才能创建合同模板。

**示例格式**：
```
【合同文件】
- 文件路径：D:\合同文件\contract.pdf

【甲方】
- 签署主体类型：企业
- 企业名称：XX科技有限公司
- 统一社会信用代码：91XXXXXXXXXXXXXXX
- 姓名：张三
- 身份证：36XXXXXXXXXXXXXXX
- 手机号码：138XXXXXXXX

【乙方】
- 签署主体类型：个人
- 姓名：李四
- 身份证：33XXXXXXXXXXXXXXX
- 手机号码：139XXXXXXXX
```

**说明**：
- 签署主体类型填写"企业"或"个人"
- 企业签署方需填写企业名称和统一社会信用代码
- 个人签署方无需填写企业相关字段

### Step 0: 信息校验

**检查签署方是否存在，并验证信息一致性：**

1. **企业校验**
   - 根据「统一社会信用代码」查询企业是否存在
   - 如果存在：检查「企业名称」是否与系统记录一致
   - 如果不一致：返回错误提示，告知用户系统中该信用代码对应的企业名称

2. **个人校验**
   - 根据「身份证号」查询个人是否存在
   - 如果存在：检查「姓名」是否与系统记录一致
   - 如果不一致：返回错误提示，告知用户系统中该身份证对应的姓名

**校验失败示例：**
```
❌ 信息校验失败

【甲方】企业信息不一致：
- 提供的企业名称：XXX公司
- 系统中该信用代码对应的企业名称：YYY公司
- 统一社会信用代码：91340124MA8N303B80

请确认企业名称是否正确，或联系管理员处理。
```

### Step 1: 创建主体

- **企业签署**：创建企业主体 → 获取企业的 userId
- **个人签署**：创建个人主体 → 获取个人的 userId

### Step 2: 创建印章

- **企业签署**：为企业创建印章（默认：enterpriseSealType: 1, sealMode: 2）
- **个人签署**：为个人创建签名（默认：sealMode: 2）

### Step 3: 上传合同文件

- 上传待签署的合同文件
- **支持格式**：PDF、DOCX、DOC
- **文件大小**：最大10MB

### Step 4: 创建合同模板

- 创建模板，配置签署方

### Step 5: 获取模板预览链接

- 返回预览链接供用户配置签署位置
- **链接格式**：使用超链接格式，用户可直接点击打开配置
  ```
  📋 模板预览链接：[点击打开配置]({preview_url})
  ```

### Step 6: 创建签署流程

根据签署主体类型使用对应的 userId：

**企业签署：**
```json
{
  "signerNo": "甲方",
  "userId": "{enterprise_user_id}",    // 企业的 userId
  "name": "{contact_name}",            // 联系人姓名
  "idCard": "{contact_idcard}",        // 联系人身份证
  "mobile": "{contact_mobile}"         // 联系人手机
}
```

**个人签署：**
```json
{
  "signerNo": "乙方",
  "userId": "{person_user_id}",        // 个人的 userId
  "name": "{person_name}",             // 个人姓名
  "idCard": "{person_idcard}",         // 个人身份证
  "mobile": "{person_mobile}"          // 个人手机
}
```

### Step 7: 获取签署链接

- 返回 PC 预览链接和 H5 签署链接
- **链接格式**：
  - 模板预览链接：超链接格式，点击可直接配置
  - 签署链接：同时提供超链接和纯文本链接（方便手机签署时复制）
  ```
  📋 模板预览链接：[点击打开配置]({preview_url})
  
  🖥️ PC预览链接：[点击打开]({preview_url})
  📱 H5签署链接：[点击签署]({sign_url})
  或复制链接：{sign_url}
  ```

### 输出结果

流程完成后，系统将返回：

1. **主体信息** - userId、sealId（企业或个人）
2. **合同模板信息** - templateId
3. **模板预览链接** - 超链接格式，点击可直接配置签署位置
4. **签署流程信息** - signFlowId、signFlowNo
5. **签署链接** - PC预览链接、H5签署链接（超链接格式，可直接点击）

---

## 代码调用

也可在代码中直接调用模块：

```javascript
const path = require('path');
const { init } = require('./lib/client');
const chain = require('./lib/modules/chain');
const evidence = require('./lib/modules/evidence');
const certificate = require('./lib/modules/certificate');
const sign = require('./lib/modules/sign');

// 初始化配置
const config = require(path.join(__dirname, 'config.json'));
init(config);

// 区块链API服务
async function demoChain() {
  // 上链
  const result = await chain.upload('{"ano":"BQ123","sha256":"xxx"}');
  console.log('交易索引:', result.index);
  console.log('请求ID:', result.requestId);
  
  // 查询结果
  const status = await chain.queryResult([result.index]);
  console.log('上链状态:', status);
}

// 自动化取证
async function demoEvidence() {
  // 创建任务
  const task = await evidence.createTask('batch-001', [{
    att_id: 'att-001',
    url: 'https://example.com',
    evidence_name: '测试取证',
    type: 1
  }]);
  console.log('任务创建:', task);
  
  // 等待完成
  const result = await evidence.waitForComplete('att-001');
  console.log('取证结果:', result);
}
```

---

## 回调验签

电子签章组件的回调需要验证签名：

```javascript
const { verifyCallback } = require('./lib/callback');

// 验证回调
app.post('/callback', (req, res) => {
  const params = req.body;
  
  if (!verifyCallback(params, config.appSecret)) {
    return res.status(400).json({ error: '签名验证失败' });
  }
  
  // 处理回调
  console.log('回调数据:', params);
  res.json({ code: 200 });
});
```

---

## 🧪 开发规则

在开发调试接口时，遵循以下规则：

### 1. 不确定信息必须询问

对于 API 文档中**未明确说明**的字段或参数，**必须询问用户**，禁止自行假设或填充。

**示例 - 需要询问的情况**:
- 字段的值应该从哪个接口获取？
- 字段的计算规则是什么？（如哈希算法）
- 字段的格式要求是什么？
- 字段之间的关联关系是什么？

**错误做法**:
```javascript
// ❌ 错误：自行假设 evidenceHash 的计算方式
const evidenceHash = crypto.createHash('sha256').update(data).digest('hex');
```

**正确做法**:
```
✅ 正确：询问用户
"evidenceHash 字段应该如何获取？是从上链接口返回，还是需要自行计算？如果需要计算，使用什么算法？"
```

### 2. 数据来源追溯

开发时需要明确每个字段的数据来源：

| 字段类型 | 来源说明 |
|----------|----------|
| 用户输入 | 由用户提供（如姓名、身份证号） |
| 接口返回 | 从其他接口响应中获取 |
| 系统生成 | 由系统自动生成（如时间戳、UUID） |
| 计算得出 | 需明确计算规则，并确认规则来源 |

### 3. 开发前确认

在编写代码前，需要确认：
1. 所有必填字段的数据来源
2. 关联字段之间的依赖关系
3. 字段的格式和取值范围

---

## 📋 保管单生成流程（交互式）

**⚠️ 核心原则：所有不确定的信息必须询问用户！**

当用户请求生成保管单时，采用**多次交互确认**的方式：

### Step 1: 查询并选择模板

```
📋 可用的保管单模板：

| 序号 | 模板ID | 模板名称 |
|------|--------|----------|
| 1 | 2036284038445596672 | hash存证 |
| 2 | 2036020528155262976 | 自动化取证模版111 |

请选择要使用的模板（输入序号或模板ID）：
```

### Step 2: 询问字段信息

**⚠️ 重要：模板字段因客户而异，必须询问用户！**

```
❓ 请提供以下信息：

模板ID: [填写模板ID或序号]

默认字段:
  申请人: [填写]
  账号: [填写]
  [其他字段...]

自定义字段:
  [字段名]: [值]
  [如无则写"无"]
```

**示例回复：**
```
模板ID: 2036020528155262976

默认字段:
  申请人: 张三
  账号: zhangsan

自定义字段:
  testname: 中欧城
```

### Step 3: 确认信息

**展示完整信息让用户确认：**

```
📝 确认信息

模板ID: 2036020528155262976 (自动化取证模版111)

默认字段:
  申请人: 张三
  账号: zhangsan

自定义字段:
  testname: 中欧城

上链数据:
  applicantName: 张三
  applicantAccount: zhangsan
  testname: 中欧城
  timestamp: （将在上链时自动生成）

确认生成保管单？(yes/no)
```

### Step 4: 执行并返回结果

```
用户确认后执行：
1. 数据上链 → 获取交易索引
2. 查询上链结果 → 获取区块链哈希、区块高度
3. 生成保管单 → 获取存证编号
4. 获取下载链接 → 返回 PDF 下载地址
```

---

### 📌 API 参数格式

**自定义字段格式：**

```json
{
  "templateId": "模板ID",
  "requestId": "请求ID",
  "defaultFields": {
    "applicantName": "张三",
    "applicantAccount": "zhangsan",
    "evidenceHash": "...",
    "blockchainHash": "...",
    "blockchainHeight": "...",
    "attestTime": "..."
  },
  "customFieldList": [
    {
      "name": "testname",
      "value": "中欧城"
    }
  ]
}
```

---

### 📌 字段取值逻辑

| 字段 | 来源 | 计算方式 |
|------|------|----------|
| `evidenceHash` | 计算得出 | SHA256(JSON.stringify(上链数据)) |
| `blockchainHash` | 接口返回 | chain_results[].hash（交易哈希） |
| `blockchainHeight` | 接口返回 | chain_results[].height |
| `attestTime` | 系统生成 | 上链成功后的北京时间 |

**⚠️ 注意：**
- `blockchainHash` 使用 `block_hash`（区块哈希），不是 `hash`（交易哈希）
- `attestTime` 在上链成功后获取北京时间

---

### 📌 字段来源确认表

**必须向用户确认每个字段的来源：**

| 字段 | 必须确认的问题 |
|------|----------------|
| evidenceHash | 从哪个接口获取？还是自行计算？用什么算法？ |
| blockchainHash | 从上链结果的哪个字段获取？ |
| blockchainHeight | 从上链结果的哪个字段获取？ |
| attestTime | 使用上链时间还是当前时间？格式要求？ |
| 自定义字段 | 模板定义了哪些字段？必填还是可选？ |

---

### ❓ 询问提示模板

**当字段来源不明时，使用以下提示：**

```
❓ 需要确认：[字段名]

该字段应该：
A. 从上链接口返回获取
B. 自行计算（请指定算法）
C. 手动填写

请选择并提供具体值：
```

---

### ⚠️ 禁止行为

**❌ 错误示例（禁止这样做）：**

```javascript
// 禁止：自行假设 evidenceHash 计算方式
const evidenceHash = crypto.createHash('sha256').update(data).digest('hex');

// 禁止：自动填充时间
const attestTime = new Date().toISOString();

// 禁止：假设模板字段
if (!params.testname) {
  params.testname = 'default'; // ❌ 禁止！
}
```

**✅ 正确做法：**

```javascript
// 1. 先检查字段是否存在
if (!params.evidenceHash) {
  // 2. 询问用户如何获取
  console.log('❓ evidenceHash 字段未提供。');
  console.log('   该字段应该：');
  console.log('   A. 从上链接口返回获取');
  console.log('   B. 自行计算（请指定算法）');
  console.log('   C. 手动填写');
  // 3. 等待用户确认后再继续
}
```

---

## API 文档

详见 `references/` 目录：
- `chain-api.md` - 区块链API服务文档
- `evidence-api.md` - 自动化取证 API 文档
- `certificate-api.md` - 保管单组件 API 文档
- `sign-api.md` - 电子签章 API 文档

---

## 环境说明

线上环境请使用 `shuqin-open` skill。

---

## 错误处理

所有接口调用失败会抛出错误，建议使用 try-catch：

```javascript
try {
  const result = await chain.upload('data');
  console.log(result);
} catch (error) {
  console.error('请求失败:', error.message);
}
```

---

## 状态枚举

### 上链状态
| 值 | 说明 |
|----|------|
| 0 | 上链失败 |
| 1 | 上链成功 |
| 2 | 等待上链 |

### 批次状态
| 值 | 说明 |
|----|------|
| NEW | 新建 |
| ASSIGNED | 已分配 |
| LOGIN | 账号登录中 |
| CHECKING | 账号自检中 |
| CHECKED | 账号自检完成 |
| UNDERWAY | 取证中 |
| SUCCESSED | 取证成功 |
| FAILED | 取证失败 |

### 任务状态
| 值 | 说明 |
|----|------|
| NEW | 新建 |
| RUNNING | 执行中 |
| SUCCESSED | 成功 |
| FAILED | 失败 |