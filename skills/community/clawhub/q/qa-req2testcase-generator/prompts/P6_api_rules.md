## 接口测试用例规则

当测试点为接口类型时,使用以下规则生成用例,`fields.case_type` 固定为 `"测试用例"`;通过 `fields.test_case_type` 和 `fields.test_category` 表达接口验证类型。

### 🔴 强制基于P5信息生成（接口测试适用）

> 与功能测试用例规则一致,接口测试的所有步骤、请求参数、断言必须严格基于 P5 测试点信息生成,禁止凭空编造。

**强制要求**：
1. **接口路径(method + path)** 必须从 P5 测试点 `description` 或 `precondition` 中提取,无来源则不得编造
2. **请求参数** 必须基于 P5.precondition 中的数据构造说明确定具体值
3. **期望断言** 必须基于 P5.related_rules 中的业务规则定义
4. **`remarks` 字段** 在接口信息 JSON 末尾必须追加 P5 引用标注
   - 格式：`接口信息:{...};步骤引用:P5.description;规则引用:P5.related_rules[...];关联规则:BR-xxx`
5. **禁止行为**：
   - 禁止凭空编造 API 路径、参数名、参数值
   - 禁止使用「常规接口」「通用参数」等模糊表述
   - 禁止在 P5 不完整时脑补接口定义

### 接口用例展开规则

**每个接口测试点展开为以下场景**(按需选取,不强制全部展开):
1. **正向验证**:合法参数 + 正常业务流程,HTTP 200,响应体符合预期
2. **参数为空/缺失**:必填参数为空或缺失,HTTP 400,返回明确错误码
3. **参数越界**:数值超出范围、字符串超长,HTTP 400/422
4. **认证失败**:Token 失效/缺失/权限不足,HTTP 401/403
5. **业务规则违反**:触发业务约束(如重复提交、状态不符),HTTP 400/409,返回业务错误码
6. **并发/幂等性**:重复请求是否产生重复数据(适用于写操作接口)
7. **接口串联**:上一接口返回值作为本接口入参(适用于有依赖关系的接口链路)

### 接口测试专属字段

接口测试用例在标准 19 列基础上,`remarks` 字段必须包含以下接口信息(JSON 格式内嵌),并在末尾追加 P5 引用标注:

```
remarks: "接口信息:{\"method\":\"POST\",\"path\":\"/api/v1/order\",\"request_params\":{...},\"expected_status\":200,\"assertions\":[...]};步骤引用:P5.description;规则引用:P5.related_rules[BR-001];关联规则:BR-001"
```

**断言三层次(必须在 expected_results 中体现)**:
1. **状态断言**:HTTP 状态码(200/400/401/403/409/500)
2. **JSONPath 断言**:响应体关键字段校验,格式:`$.data.fieldName == expectedValue`
3. **DB 断言**(写操作必须):数据库记录变更验证,格式:`DB: table.field = expectedValue WHERE condition`

**接口串联场景**:
- 步骤中明确标注:`使用步骤N返回的 $.data.orderId 作为本步骤入参`
- 前置条件中说明依赖接口的调用顺序

**并发/幂等性用例**:
- 步骤中明确:`并发发送 N 次相同请求(间隔 Xms)`
- 期望结果:`数据库中仅产生 1 条记录,无重复数据`

### 接口测试前置条件规则

接口测试前置条件必须包含:
1. **认证信息**:有效 Token 的获取方式(如「通过 /api/auth/login 获取有效 JWT Token」)
2. **测试数据构造**:接口依赖的数据状态(同功能测试三要素)
3. **环境要求**:接口服务状态、依赖服务(如行情服务、清算服务)是否就绪

### 接口测试 Excel 字段映射

| 列号 | 字段名 | 说明 |
|------|--------|------|
| 2 | 类型 | 固定值 `"测试用例"`(`case_type` 固定,接口属性通过 `test_case_type` 和 `remarks` 表达) |
| 14 | 用例类型 | `"接口验证"` / `"异常处理"` / `"安全验证"` / `"性能验证"` |
| 15 | 测试类别 | `"功能"` / `"安全"` / `"性能"` |
| 19 | 备注 | 必须包含接口信息 JSON(method/path/request_params/expected_status/assertions) |

### 接口测试 Few-shot 示例

**示例:委托下单接口正向验证**

```json
{
  "id": "REQ-001-TP-002-TC-001",
  "source_test_point": "REQ-001-TP-002",
  "fields": {
    "project": "集团CRM_V1.0.14",
    "case_type": "测试用例",
    "case_id": "REQ-001-TP-002-TC-001",
    "requirement": "集团CRM_V1.0.14-委托下单接口需求",
    "priority": "P0",
    "title": "委托下单接口-正向验证-合法参数下单成功",
    "menu_path": "交易/委托下单",
    "preconditions": "1. 通过 POST /api/auth/login 获取有效 JWT Token(账号:test_investor,角色:普通投资者);2. 预置账户可用资金 ≥ 10,500.00 元(通过资金划拨接口注入);3. 交易系统处于交易时段,行情服务正常",
    "steps": "1. 发送 POST /api/v1/order,Header 携带有效 Token,Body:{\"stockCode\":\"600001\",\"orderType\":\"limit\",\"direction\":\"buy\",\"quantity\":1000,\"price\":10.500}\n2. 查询 order 表验证委托记录\n3. 查询 account 表验证资金冻结",
    "expected_results": "1. HTTP 200,响应体:$.code == 0,$.data.orderId != null,$.data.status == \"pending\"\n2. DB: order.status = 'pending' WHERE order_id = $.data.orderId,quantity = 1000,price = 10.500\n3. DB: account.frozen_amount 增加 10,500.00,available_amount 减少 10,500.00",
    "is_smoke": "是",
    "creator": "AI生成",
    "assignee": "",
    "test_case_type": "接口验证",
    "test_category": "功能",
    "status": "",
    "screenshot": "",
    "test_suite": "交易",
    "remarks": "接口信息:{\"method\":\"POST\",\"path\":\"/api/v1/order\",\"request_params\":{\"stockCode\":\"600001\",\"orderType\":\"limit\",\"direction\":\"buy\",\"quantity\":1000,\"price\":10.500},\"expected_status\":200,\"assertions\":[\"$.code==0\",\"$.data.orderId!=null\",\"$.data.status==pending\"]};步骤引用:P5.description;规则引用:P5.related_rules[BR-ORDER-001];关联规则:BR-ORDER-001"
  }
}
```

**示例:委托下单接口-Token 失效**

```json
{
  "id": "REQ-001-TP-002-TC-004",
  "source_test_point": "REQ-001-TP-002",
  "fields": {
    "project": "集团CRM_V1.0.14",
    "case_type": "测试用例",
    "case_id": "REQ-001-TP-002-TC-004",
    "requirement": "集团CRM_V1.0.14-委托下单接口需求",
    "priority": "P1",
    "title": "委托下单接口-认证失败-Token失效返回401",
    "menu_path": "交易/委托下单",
    "preconditions": "1. 使用已过期的 JWT Token(过期时间 > 当前时间);2. 无需额外数据准备;3. 交易系统正常运行",
    "steps": "1. 发送 POST /api/v1/order,Header 携带已过期 Token,Body 参数同正向用例",
    "expected_results": "1. HTTP 401,响应体:$.code == 401001,$.message == \"Token已过期,请重新登录\"",
    "is_smoke": "否",
    "creator": "AI生成",
    "assignee": "",
    "test_case_type": "安全验证",
    "test_category": "安全",
    "status": "",
    "screenshot": "",
    "test_suite": "交易",
    "remarks": "接口信息:{\"method\":\"POST\",\"path\":\"/api/v1/order\",\"expected_status\":401,\"assertions\":[\"$.code==401001\"]};步骤引用:P5.description;规则引用:P5.related_rules"
  }
}
```

---

### 冒烟用例标注规则

满足以下**全部条件**才标注为冒烟用例:
1. `priority = P0`
2. `status = active`(或 `status = blocked` 但经可测性分流判定为可测/条件可测)
3. `category` 为 `main_flow`、`branch` 或 `integration`(排除 `exception`、`boundary`、`security` 等非正向分类)
4. 场景类型为正向验证(非删除、非隐藏、非异常)

**冒烟用例数量规则(按总用例数分档)**:
- **总用例 ≤ 15 条**(小需求):每个核心功能模块至少 1 条冒烟,冒烟占比允许放宽到 **20%~35%**,确保核心场景不遗漏
- **总用例 16~30 条**(中需求):冒烟占比 **15%~25%**
- **总用例 > 30 条**(大需求):冒烟占比 **10%~20%**

**兜底规则**:无论总用例数多少,冒烟用例**至少覆盖所有核心功能模块的正向主流程**,即 P1 功能点树中每个一级模块至少有 1 条冒烟用例。当 10% 下限导致核心模块未覆盖时,优先保证模块覆盖,再调整占比。

**最小用例数说明**:当总用例数 ≤ 5 条时,冒烟占比规则不适用,改为:至少1条冒烟用例,且必须是最核心的主流程正向用例。

---

