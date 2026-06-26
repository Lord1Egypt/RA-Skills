# 校验规则管理 - 使用示例

## 环境准备

**方式 1 — 环境变量**（推荐）：
```bash
export VALIDATE_BASE_URL=http://global-masterdata-http.default.yf-bw-test-2.test.51baiwang.com
export VALIDATE_TOKEN=your-token-here
```

**方式 2 — config.json**（项目根目录）：
```json
{
  "baseUrl": "http://global-masterdata-http.default.yf-bw-test-2.test.51baiwang.com",
  "token": "your-token-here",
  "appId": "your-app-id-here"
}
```

---

## 示例 1: 完整新增流程（中国增值税专票）

### 步骤 1: 创建规则组

```bash
node scripts/cli.js create-rule-group \
  --groupName "卖方信息校验组" \
  --description "校验发票卖方相关信息" \
  --orderNum 1
```

输出：`{ "success": true, "data": [{ "id": 1001 }] }`

---

### 步骤 2: 创建规则

```bash
node scripts/cli.js create-rule \
  --groupId 1001 \
  --objectId Invoice \
  --countryCode CN \
  --ruleCode CN-SELLER-001 \
  --ruleName "卖方名称必填校验" \
  --description "校验卖方名称不能为空" \
  --fieldKey sellerName \
  --ruleType required \
  --errorLevel error \
  --errorCode E10001 \
  --errorMessage "{field}不能为空" \
  --executionOrder 1 \
  --status enabled
```

> 💡 值含 `{}`、空格等特殊字符时，shell 引号会自动处理，无需额外转义。

---

### 步骤 3: 创建场景

```bash
node scripts/cli.js create-scene \
  --sceneCode CN_VAT_SPECIAL \
  --sceneName "中国增值税专票场景" \
  --errorStrategy stop_on_error \
  --status enabled
```

---

## 示例 2: 查询操作

```bash
# 查询场景
node scripts/cli.js query-scenes --status enabled --pageNum 1 --pageSize 20

# 查询规则
node scripts/cli.js query-rules --groupId 1001 --countryCode CN --ruleType required

# 查询规则组
node scripts/cli.js query-rule-groups --groupName "卖方信息" --pageSize 10
```

---

## 示例 3: 启用 / 禁用 / 删除

```bash
node scripts/cli.js enable-rule  --id 2001 --status enabled
node scripts/cli.js enable-rule  --id 2001 --status disabled
node scripts/cli.js enable-scene --id 10   --status enabled
node scripts/cli.js delete-rule  --id 2001
node scripts/cli.js delete-scene --id 10
```

---

## 示例 4: 含复杂参数时使用 --json

```bash
node scripts/cli.js create-rule --json '{
  "groupId": 1001,
  "objectId": "Invoice",
  "countryCode": "CN",
  "ruleCode": "CN-SELLER-002",
  "ruleName": "卖方税号格式校验",
  "fieldKey": "sellerTaxNumber",
  "ruleType": "regex",
  "errorMessage": "卖方税号格式不正确",
  "status": "enabled"
}'
```

---

## 直接调用 API（curl / Postman）

### 创建规则组
```json
POST /admin/validateRuleGroup/create
{ "groupName": "卖方信息校验组", "description": "...", "orderNum": 1 }
```

### 查询场景列表
```json
POST /admin/validateScene/queryPageList
{ "sceneCode": "CN_VAT", "status": "enabled", "pageNum": 1, "pageSize": 20 }
```

### 更新规则组顺序
```json
POST /admin/validateRuleGroup/saveGroupOrders
{ "groupOrders": [{ "id": 1001, "orderNum": 1 }, { "id": 1002, "orderNum": 2 }] }
```

### 获取校验对象结构
```json
POST /admin/validateRule/validateEntitySchemas
{ "countryCode": "CN" }
```

---

## 常见规则类型速查

```json
// 必填
{ "ruleType": "required", "fieldKey": "sellerName", "errorMessage": "{field}不能为空" }

// 正则
{ "ruleType": "regex", "fieldKey": "taxNumber", "errorMessage": "税号格式不正确",
  "extensions": { "pattern": "^[0-9A-Z]{15,20}$" } }

// 范围
{ "ruleType": "range", "fieldKey": "amount", "errorMessage": "金额超出范围",
  "extensions": { "min": 0, "max": 999999999 } }

// 长度
{ "ruleType": "length", "fieldKey": "remark", "errorMessage": "备注不能超过200字",
  "extensions": { "max": 200 } }
```
