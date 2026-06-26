---
name: wininsales-crm
description: Use when users need 赢在销客CRM, wininsales, WininSales CRM, 企业微信CRM, 企微CRM, or CRM sales operations, including customer search, duplicate check, ownership lookup, customer creation, follow-up records, assignment, sharing, public-pool recovery, lead and opportunity management, contracts, payments, expiry reminders, inactive-customer lists, product lookup, employee lookup, performance analysis, or daily reports. 适用于“客户是否存在/在谁名下/录入客户/记录跟进/分配共享/查合同回款/查到期或未跟进客户/写日报”等场景。
---

# 赢在销客CRM (WininSales CRM)

## 概述

此 skill 面向赢在销客 CRM 的日常销售运营场景，帮助销售、主管和运营人员直接完成客户查询、录入、跟进、线索、商机、合同回款、业绩分析和日报等工作。

客户常见问题包括：
- “这个客户系统里有没有？在谁名下？”
- “帮我把这家公司录入 CRM，并先查重。”
- “给客户加一条电话/微信/面访跟进记录。”
- “把客户共享给同事，或把线索分配给某个人。”
- “查一下本月到期客户、长期未跟进客户、合同回款和团队业绩。”
- “基于今天的跟进情况帮我写日报。”

底层集成赢在销客CRM的 MCP API（24个接口），覆盖客户管理全流程。
**数据来源：** 通过 `tools/list` 接口获取实际API定义，确保与系统一致。

## 快速导航

| 你要做什么 | 优先阅读 |
|------------|----------|
| 查客户是否存在、在谁名下 | 流程1、API 1、客户分析 API 5 |
| 录入新客户 | 流程2、API 2、工商字段映射、注意事项 |
| 记录电话/微信/面访跟进 | 流程3、API 7、往来方式映射 |
| 分配/共享客户或线索 | 流程4、流程6、员工ID查询 |
| 查合同回款、到期、未跟进、业绩 | 流程9-12、API 12-15 |
| 新增线索、商机、产品 | 流程6-7、API 17、API 21-23 |
| 写日报 | 流程13、API 24 |
| 处理字段选项、字典值 | 流程14、API 16、API 23 |

## 场景示范（客户可直接这样问）

| 场景 | 客户可以这样问 | 技能会怎么做 |
|------|----------------|--------------|
| 客户查重与归属 | “帮我查一下南京某某科技在 CRM 里有没有，在谁名下？” | 先用公司名查重；查到后展示客户状态、跟进人、最近跟进；需要归属详情时再用公司全称分析。 |
| 新客户录入 | “帮我录入南京某某科技，先查重，再查工商信息。” | 先查重；未存在时查工商；复述企业和联系人关键字段，用户确认后再创建客户。 |
| 跟进记录 | “给南京某某科技加一条微信跟进：今天沟通了企业微信 CRM 试用，下周约演示。” | 定位客户ID；映射微信为 `VisitType.5`；确认跟进内容、时间和联系人后写入。 |
| 客户共享 | “把南京某某科技共享给张涛，让他也能看到。” | 查客户；查张涛 user_id；确认共享对象后调用 ShareCustomer；失败时提示权限或姓名降级方案。 |
| 客户分配 | “把南京某某科技转给李四跟进。” | 查客户和目标员工；提醒分配后原跟进关系可能变化；确认后调用 AssignCustomer。 |
| 新增线索 | “帮我新增一个线索，联系人王总，手机号 138****8888，来源主动开发。” | 优先查 source 选项；默认使用 `MessageSource.3`；检查至少有一种联系方式；确认后添加线索。 |
| 线索分配 | “把这个线索分给张涛，备注：客户对 CRM 有兴趣。” | 查询线索ID；查询员工ID；确认分配原因后调用 AssignLead；员工ID无权限时尝试姓名降级。 |
| 创建商机 | “给南京某某科技建一个商机，产品是赢在销客，预算 3 万，预计 6 月签约。” | 查客户；查产品；收集预算、预计签约时间、需求和竞品；确认后创建商机。 |
| 合同回款 | “查一下南京某某科技的合同和回款情况。” | 先查客户并确认 `check_look=1`；有权限时查询合同、到账、回款、利润；无权限时说明原因。 |
| 到期提醒 | “查一下本月即将到期的客户。” | 确认时间范围和个人/团队/全部范围；调用到期客户查询；按到期时间和风险输出。 |
| 未跟进客户 | “查一下 30 天没跟进的客户。” | 计算最后跟进截止日期；必要时查询客户等级字典；输出长期未跟进客户和建议动作。 |
| 日报 | “根据今天 CRM 记录帮我写日报。” | 拉取当日日报上下文；整理今日工作、客户推进、问题风险和明日计划。 |

## 角色与场景入口

- 销售人员：查客户、录入客户、写跟进、建线索/商机、查到期和未跟进客户、写日报。
- 销售主管：看团队业绩、分配客户/线索、共享客户、盘点合同回款和续费风险。
- CRM运营：维护字段选项、确认字典全称、处理公海、检查录入失败原因、沉淀规范。

## 安全、权限与隐私边界

- 不在技能文件里保存真实 token、密码、API key、客户手机号、邮箱、合同金额截图等隐私数据。
- token 由用户在赢在销客 CRM 授权获取；调用时只使用当前用户授权，不绕过 CRM 权限。
- 查询结果只能展示当前账号有权查看的数据；遇到无权限、查不到、字段不可见时，明确说明原因。
- 对外展示客户信息时默认脱敏：手机号、邮箱、微信、QQ、电话中间用 `****`；内部写入参数可用用户提供的完整值。
- 写入类动作（录入客户、分配/共享、添加跟进、添加线索、添加商机、通话标记）必须先复述关键字段并获得用户确认。
- 禁止编造客户、联系人、合同、回款、员工ID、产品ID、字段选项值；缺字段时问用户补充。

## 标准输出模板

**查询类输出：**
```
结论：查到/未查到/无权限/需要补充条件
关键信息：客户名称、状态、跟进人、最近跟进、合同/回款/到期等必要字段
风险提示：重复客户、公海、他人跟进、长期未跟进、即将到期、权限不足
下一步：录入、共享、分配、跟进、建商机、继续筛选
```

**写入类确认：**
```
请确认以下信息：
- 操作：录入客户/添加跟进/分配客户/共享客户/添加线索/添加商机
- 对象：客户或线索名称
- 关键字段：联系人、电话、来源、跟进方式、员工、产品、时间
确认后再提交 CRM。
```

**失败类输出：**
```
结果：本次操作未完成
原因：无权限/字段缺失/字典值不匹配/客户已存在/API返回错误
建议：补充字段、先查字典、换用员工姓名降级、请管理员授权、稍后重试
```

## API总览（24个接口，按功能分组）

### 🔵 客户管理（7个）

| # | API名称 | 功能 | 使用频率 |
|---|---------|------|----------|
| 1 | SearchExistingCustomers | 客户查重/搜索 | ⭐⭐⭐⭐⭐ |
| 2 | CreateNewBusinessCustomer | 新客户录入（40+字段） | ⭐⭐⭐⭐⭐ |
| 3 | CompanyBusinessRegistrationInquiry | 工商信息查询（天眼查） | ⭐⭐⭐⭐ |
| 4 | CompanyInformationSearch | 工商信息补全 | ⭐⭐⭐ |
| 5 | AnalyzeCustomers | 客户数据分析 | ⭐⭐⭐⭐ |
| 6 | CRMOperationManual | 查询操作手册 | ⭐⭐ |
| 7 | QueryDictByCode | 查询数据字典（辅助工具） | ⭐⭐ |

### 🟢 跟进与拜访（1个）

| # | API名称 | 功能 | 使用频率 |
|---|---------|------|----------|
| 8 | AddCustomerVisit | 添加跟进/拜访记录 | ⭐⭐⭐⭐⭐ |

### 🟡 客户协作（4个）

| # | API名称 | 功能 | 使用频率 |
|---|---------|------|----------|
| 9 | ShareCustomer | 客户共享给同事 | ⭐⭐⭐ |
| 10 | AssignCustomer | 客户分配给同事 | ⭐⭐⭐ |
| 11 | QueryEmployeeUserId | 查询员工ID | ⭐⭐⭐ |
| 12 | ReclaimPublicPoolCustomer | 公海客户捡回提示 | ⭐⭐⭐ |

### 🟠 业绩与分析（4个）

| # | API名称 | 功能 | 使用频率 |
|---|---------|------|----------|
| 13 | EmployeeAnalysis | 员工/团队业绩分析 | ⭐⭐⭐⭐ |
| 14 | QueryCustomerContractPayment | 客户合同与回款查询 | ⭐⭐⭐ |
| 15 | QueryCustomersRecentExpiry | **🆕** 查询即将到期客户 | ⭐⭐⭐ |
| 16 | QueryNoFollowUpCustomers | **🆕** 查询长期未跟进客户 | ⭐⭐⭐ |

### 🔴 线索管理（4个）

| # | API名称 | 功能 | 使用频率 |
|---|---------|------|----------|
| 17 | AddOpportunity | 添加销售线索 | ⭐⭐⭐ |
| 18 | QueryLead | 查询线索 | ⭐⭐⭐ |
| 19 | AssignLead | 分配线索给同事 | ⭐⭐⭐ |
| 20 | SignLeadCall | 线索通话标记 | ⭐⭐ |

### 🟣 商机与产品（2个）

| # | API名称 | 功能 | 使用频率 |
|---|---------|------|----------|
| 21 | AddClue | 为客户添加商机 | ⭐⭐⭐ |
| 22 | SearchProducts | 按名称/编号查产品 | ⭐⭐⭐ |

### ⚪ 辅助工具（2个）

| # | API名称 | 功能 | 使用频率 |
|---|---------|------|----------|
| 23 | SearchFieldOptions | 查询下拉/单选字段选项 | ⭐⭐ |
| 24 | QueryDailyWriteContext | **🆕** 拉取日报上下文 | ⭐⭐ |

---

## 基础配置

### 授权Token

如果没有 token，引导用户登录 CRM 并在系统内授权获取；不要让用户把 token 写进技能文件或聊天记录。
登录地址：
https://www.wininsales.com/login

授权注意：
- token 属于当前 CRM 账号，权限以 CRM 后台为准。
- token 无效、过期或权限不足时，提示用户重新授权或联系管理员。
- 上架技能包只能包含 `SKILL.md` 和必要的上架元数据，不能包含密码文件、运维脚本、数据库备份配置。

### curl调用方式

```bash
# ⚠️ 中文参数必须用 heredoc 方式传入，避免编码异常！
cat > /tmp/crm_query.json << 'JSONEOF'
{"jsonrpc":"2.0","method":"tools/call","params":{"name":"工具名称","arguments":{参数}},"id":1}
JSONEOF
curl -s "https://www.wininsales.com/mcp_api/mcp?token=" \
  -X POST -H "Content-Type: application/json" \
  -d @/tmp/crm_query.json
```

调试建议：
- 中文参数用 heredoc 写入临时 JSON，避免 shell 编码问题。
- 如果 shell 仍出现中文乱码，优先用 Python3 `tempfile` 写 UTF-8 JSON 文件，再调用 `curl -d @file`。
- 不要把真实 token 写进示例命令；本文件只保留 `?token=` 占位。
- 如果返回非预期字段，优先以 `tools/list` schema 和实际 API 返回为准，不以操作手册的文字说明为准。

---

## 智能工作流（14个核心流程）

### 流程1：客户查重+归属查询（最高频）

> 触发：用户说"XX公司存在吗"、"在谁名下"、"这个客户是谁的"

```
Step 1: SearchExistingCustomers(query=公司名)
    ↓
    ├─ 未查到 → "系统中不存在该客户，需要录入吗？"
    └─ 查到了 → 展示：客户名称、状态（私海/公海/他人跟进）、录入时间
    ↓
Step 2: 用户追问"谁的客户" → AnalyzeCustomers(customer=公司全称, analysis_type=客户)
    ↓
    ⚠️ customer必须用公司全称，不能缩写！
    ↓
Step 3: 输出：主跟进人、地址、意向等级
    ↓
Step 4: 根据状态给建议
    - "他人跟进" → "需要我帮你共享或分配过来吗？"
    - "客户公海" → "需要我帮你捡回吗？"
```

### 流程2：客户录入（含工商查询）

> 触发：用户说"帮我录入XX公司"、"XX公司录入CRM"

```
Step 1: 询问客户名称
    ↓
Step 2: SearchExistingCustomers 查重
    ├─ 已存在 → 展示信息，问是否需要其他操作（查归属/共享/分配）
    └─ 不存在 → 继续
    ↓
Step 3: CompanyBusinessRegistrationInquiry 工商查询
    ├─ 查到 → 展示工商信息，让用户确认
    └─ 未查到 → 问是否手动录入
    ↓
Step 4: 补充联系人信息（用户提供时直接用，否则用法人默认）
    ↓
Step 5: CreateNewBusinessCustomer 提交
    ├─ 成功 → "客户录入成功"
    └─ 失败 → 根据错误提示处理（见踩坑经验）
```

**录入字段经验：**
- 必填：company_name, contact_contact_name, contact_sex
- 建议填：industry, source, level, scope, main_product, region, label, memo
- ⚠️ scope 是"企业规模"（EmployeesNum.1~EmployeesNum.9），不是主营产品！主营产品用 main_product

### 流程3：跟进录入

> 触发：用户说"记录一下跟进"、"加个拜访记录"

```
Step 1: SearchExistingCustomers 获取客户ID
Step 2: 询问：往来方式（面访/电话/微信/QQ/邮件）、时间、内容
Step 3: 面访需补充：结束时间（默认+4小时）、拜访地址
Step 4: AddCustomerVisit 提交
```

**往来方式映射：** 面访=VisitType.1, 电话=VisitType.2, 邮件=VisitType.3, QQ=VisitType.4, 微信=VisitType.5, 其他=VisitType.6, 企业微信=VisitType.105

### 流程4：客户分配/共享（核心优化）

> 触发：用户说"把XX客户分给XX"、"让XX也能看到这个客户"、"把XX客户转给XX"

```
Step 1: SearchExistingCustomers 获取 customer_id
    ↓
Step 2: QueryEmployeeUserId 查询目标员工ID
    - employee_name: 员工姓名（支持"我"/"自己"）
    - multiple: 0（单人分配）
    - status: 0（仅在职）
    ↓
    ├─ ✅ 查询成功 → 获取 user_id，继续
    └─ ❌ 查询失败（无权限）→ 尝试直接用员工姓名
    ↓
Step 3: 执行分配/共享
    ├─ 分配客户: AssignCustomer(customer_id, assignee=user_id)
    └─ 共享客户: ShareCustomer(customer_id, share_with=user_id)

【容错策略】
- 如果 QueryEmployeeUserId 返回错误，尝试直接把 receiver/assignee 参数设为员工姓名
- 部分API支持直接用姓名代替user_id
```

**分配 vs 共享区别：**
| 操作 | 效果 | 适用场景 |
|------|------|----------|
| AssignCustomer | 客户转给对方，**自己不再跟进** | 正式交接、全权移交 |
| ShareCustomer | **双方都能看到**，各自独立跟进 | 协作查看、数据同步 |

**完整示例（客户分配）：**
```bash
# Step 1: 查客户
curl ... -d '{"method":"tools/call","params":{"name":"SearchExistingCustomers","arguments":{"query":"XX公司"}}}'

# Step 2: 查员工ID（如果有权限）
curl ... -d '{"method":"tools/call","params":{"name":"QueryEmployeeUserId","arguments":{"employee_name":"张涛","multiple":0,"status":0}}}'

# Step 3: 分配客户
curl ... -d '{"method":"tools/call","params":{"name":"AssignCustomer","arguments":{"customer_id":"xxx","assignee":"查到的user_id"}}}'
```

**完整示例（客户共享）：**
```bash
# Step 1: 查客户
curl ... -d '{"method":"tools/call","params":{"name":"SearchExistingCustomers","arguments":{"query":"XX公司"}}}'

# Step 2: 查员工ID（如果有权限）
curl ... -d '{"method":"tools/call","params":{"name":"QueryEmployeeUserId","arguments":{"employee_name":"李四","multiple":0,"status":0}}}'

# Step 3: 共享客户
curl ... -d '{"method":"tools/call","params":{"name":"ShareCustomer","arguments":{"customer_id":"xxx","share_with":"查到的user_id"}}}'
```

### 流程5：公海捡回

> 触发：用户说"XX客户在公海，帮我捡回来"

```
Step 1: SearchExistingCustomers 确认客户在公海（status_name=客户公海）
Step 2: ReclaimPublicPoolCustomer 获取操作指引
Step 3: AddCustomerVisit 添加一条跟进记录 → 自动捡回私海
```

### 流程6：线索管理（核心优化）

> 触发：用户说"帮我加个线索"、"查一下线索"、"把线索分给XX"

```
【添加线索】
Step 1: SearchFieldOptions(tool_name="AddOpportunity", field_key="source") 查来源选项
    ├─ ✅ 成功 → 获取 source 选项值
    └─ ❌ 失败（无权限）→ 使用常见默认值: MessageSource.1=线索转化, MessageSource.3=主动开发
Step 2: 收集信息（联系人、公司、电话等，phone/email/qq/tel/wechat至少一个）
Step 3: AddOpportunity 提交

【查询线索】
Step 1: QueryLead(keyword) → 展示线索列表（含id、can_make_call_flag、is_opp_assign）
Step 2: 如需展示更多字段，手动查询

【分配线索】⚠️ 重要优化
Step 1: QueryLead 找到线索ID
    ↓
Step 2: QueryEmployeeUserId 查询目标员工ID
    - employee_name: 员工姓名
    - multiple: 0
    - status: 0
    ↓
    ├─ ✅ 查询成功 → 获取 user_id，继续
    └─ ❌ 查询失败（无权限）→ 直接用员工姓名作为 receiver
    ↓
Step 3: AssignLead(id=线索ID, receiver=员工ID或姓名, suggest=分配原因)
    └─ ⚠️ receiver 参数支持直接用员工姓名字符串（系统会自动匹配）

【通话标记】
Step 1: QueryLead 找到线索，确认 can_make_call_flag 权限
Step 2: SearchFieldOptions(tool_name="SignLeadCall", field_key="labeling_status") 查选项
Step 3: SignLeadCall 提交
```

**添加线索示例（无权限时降级）：**
```bash
# 如果 SearchFieldOptions 失败，用默认值
curl ... -d '{"method":"tools/call","params":{"name":"AddOpportunity","arguments":{
  "contact_name":"联系人名", "phone":"手机号", "source":"MessageSource.1", "memo":"备注"
}}}'
```

**分配线索示例（查询ID + 分配）：**
```bash
# Step 1: 查询线索
curl ... -d '{"method":"tools/call","params":{"name":"QueryLead","arguments":{"keyword":"手机号或公司名"}}}'
# 返回: [{"id":"xxx","contact_name":"...","phone":"...","create_time":"...","is_opp_assign":0}]

# Step 2: 查询员工ID（如果有权限）
curl ... -d '{"method":"tools/call","params":{"name":"QueryEmployeeUserId","arguments":{"employee_name":"张涛","multiple":0,"status":0}}}'

# Step 3: 分配线索
curl ... -d '{"method":"tools/call","params":{"name":"AssignLead","arguments":{
  "id":"查到的线索ID", "receiver":"张涛或user_id", "suggest":"了解CRM系统，分配给张涛跟进"
}}}'
```

### 流程7：商机添加

> 触发：用户说"帮这个客户建个商机"、"给XX公司加个商机"

```
Step 1: SearchExistingCustomers 获取 company_id
Step 2: SearchProducts 查询产品ID（如需指定产品）
Step 3: 收集商机信息：预算、预计签约时间、需求描述、竞品
Step 4: AddClue 提交
```

**品牌ID：** 腾讯标准产品(1)/赢在销客(122)/企业微信私有化(123)/惠岚品牌(1566)/定制开发(1639)

### 流程8：客户分析

> 触发：用户说"分析一下XX公司"、"看一下XX客户的数据"

```
Step 1: AnalyzeCustomers(customer=公司全称, analysis_type=all)
Step 2: 可选类型：客户、联系人、往来记录、商机记录、合同记录、all
Step 3: 格式化输出（隐藏手机号、用表格呈现）
```

### 流程9：业绩分析

> 触发：用户说"查一下本周的业绩"、"团队成交情况"

```
Step 1: 确认范围（个人/团队）和时间（本周/上周/本月/自定义）
Step 2: EmployeeAnalysis(employee_name, start_time, end_time, scope, analysis_type)
Step 3: 汇总输出（按业绩排序、计算总计）
```

### 流程10：合同查询

> 触发：用户说"看一下XX公司的合同"、"XX客户回款情况"

```
Step 1: SearchExistingCustomers 获取 customer_id（需 check_look=1）
Step 2: QueryCustomerContractPayment(customer_id)
Step 3: 输出合同、到账、回款、利润信息
```

### 流程11：🆕 到期客户查询

> 触发：用户说"最近哪些客户要到期"、"本月到期名单"、"续费提醒"

```
Step 1: 确认时间范围和查询范围
Step 2: QueryCustomersRecentExpiry(start_time, end_time, scope, userids?)
    - scope: "全部" / "团队" / "个人"
    - 时间格式: YYYY-MM-DD
    - scope="个人"时 userids 可省略（默认当前登录人），或传 me/自己/我
Step 3: 输出到期客户列表
```

### 流程12：🆕 未跟进客户查询

> 触发：用户说"多久没跟进的客户"、"哪些客户没联系"、"跟进超期"

```
Step 1: 确认时间阈值（如30天、60天）
Step 2: QueryNoFollowUpCustomers(end_time, company_level?)
    - end_time: 最后跟进截止日期（YYYY-MM-DD），如距今30天前的日期
    - company_level: 可选，客户等级筛选（需先 QueryDictByCode(dict_code="CompanyLevel") 获取）
Step 3: 输出未跟进客户列表
```

### 流程13：🆕 日报上下文

> 触发：用户说"帮我写日报"、"今日工作汇总"

```
Step 1: QueryDailyWriteContext(date=YYYY-MM-DD)
    - 获取当日工作要点与明日计划等上下文
Step 2: 基于上下文生成日报内容
```

### 流程14：数据字典查询

> 触发：需要查询某个字段的全部可选值（当 SearchFieldOptions 不适用时）

```
Step 1: QueryDictByCode(dict_code="编码名")
    - 必须使用系统字典全称，如 CompanyLevel、CompanyType、EmployeesNum、Industry
    - 禁止用简称、中文名或猜测值，例如 level、type、规模、行业
Step 2: 输出字典值列表
Step 3: 录入客户、线索、商机前，必须从返回结果中选择准确 value
```

---

## API详细参考

### 1. SearchExistingCustomers — 客户查重/搜索

```
参数: query（必填）— 公司名/电话/联系人，优先：客户名称 > 电话 > 联系人姓名
返回: 客户列表（含customer_id、contact_id、status_name、check_look）
约束: 禁止在未指明查询行为时自动调用；不泄露客户ID/联系方式
```

### 2. CreateNewBusinessCustomer — 客户录入（40+字段）

```
必填: company_name, contact_contact_name, contact_sex(1男/0女/2未知)

--- 企业信息 ---
company_name      [必填] 客户名称
short_name        [可选] 客户简称
customer_no       [可选] 客户编号
type              [可选] 客户类型: 直接客户(CompanyType.1)/经销商(CompanyType.2)/合作伙伴(CompanyType.3)
level             [可选] 意向等级: 信息无效(CompanyLevel.110)/无意向(CompanyLevel.0)/信息不完整(CompanyLevel.113)/未沟通(CompanyLevel.103)/潜在(CompanyLevel.1)/意向(CompanyLevel.2)
source            [可选] 客户来源（需SearchFieldOptions查）常用: 主动开发(MessageSource.3)/线索转化(MessageSource.1)
industry          [可选] 所属行业（需SearchFieldOptions查）
scope             [可选] 企业规模: 1-10人(EmployeesNum.1)/11-50(EmployeesNum.2)/51-100(EmployeesNum.3)/101-200(EmployeesNum.4)/201-500(EmployeesNum.5)/501-1000(EmployeesNum.6)/1001-2000(EmployeesNum.7)/2001-5000(EmployeesNum.8)/5000人以上(EmployeesNum.9)
main_product      [可选] 主营产品（文本）
label             [可选] 客户标签（多选，需SearchFieldOptions查）
region            [可选] 区域
address           [可选] 企业地址
url               [可选] 企业网址
tel               [可选] 企业电话（手机号格式，严格11位）
fax               [可选] 企业传真（座机格式）
memo              [可选] 备注
dealer_id         [可选] 经销商（需SearchFieldOptions查）
customer16        [可选] 现用品牌（需SearchFieldOptions查）
customer200634    [可选] 管理员账号/企业ID
customer52643     [可选] 销售归属
customer32000     [可选] 购买账户数（整数）
customer52633     [可选] 服务到期时间（YYYY-MM-DD）
customer152787    [可选] 到期年月（YYYY-MM）
customer212687    [可选] 客户咨询: 400咨询(ext1)/IM咨询(ext2)/从未咨询(ext3)
customer156559    [可选] 产品培训: 已培训(ext1)/未培训(ext2)
cooperater        [可选] 协作人（需SearchFieldOptions查）
relevance_customer [可选] 被关联客户（需SearchFieldOptions查）

--- 联系人信息 ---
contact_contact_name [必填] 联系人姓名
contact_sex          [必填] 性别: 男(1)/女(0)/未知(2)
contact_phone        [可选] 联系人手机（手机号格式，严格11位）
contact_tel          [可选] 联系人座机（座机格式）
contact_email        [可选] 联系人邮箱
contact_qq           [可选] 联系人QQ
contact_wechat       [可选] 联系人微信
contact_department   [可选] 联系人部门
contact_role         [可选] 联系人角色: 公司负责人(ContactRole.1)/财务决策人(ContactRole.2)/项目影响人(ContactRole.3)/项目负责人(ContactRole.4)/项目执行人(ContactRole.5)
contact_duty         [可选] 联系人职务
contact_kp           [可选] 关键人: 否(0)/是(1)
contact_birthday     [可选] 联系人生日（YYYY-MM-DD）
contact_memo         [可选] 联系人备注
```

### 3. CompanyBusinessRegistrationInquiry — 工商信息查询

```
参数: tyc_keyword（必填）— 企业全称
返回: companyName, juridicalPerson, registedCapital, registedDate,
      companyStatUs, address, actualAddress, industry, products,
      creditCode, webSites, staffNumber, socialSecurityNum,
      annualTurnover, reportTaxTotal
```

### 4. CompanyInformationSearch — 工商信息补全

```
参数: tyc_keyword（必填）— 企业全称
用途: 创建客户流程中补充企业工商信息
```

### 5. AnalyzeCustomers — 客户分析

```
参数: customer（必填, 公司全称）, analysis_type（必填）, start_time, end_time
类型: 客户/联系人/往来记录/商机记录/合同记录/all
```

### 6. CRMOperationManual — 操作手册

```
参数: question（必填）— 操作问题
用途: 查询CRM系统操作指南
⚠️ 注意: 返回的信息可能不准确（如字段名），以 tools/list 实际schema为准
```

### 7. AddCustomerVisit — 跟进录入

```
必填: company_id, type, expect_start_time(YYYY-MM-DD HH:MM), memo
可选: contact_id, expect_end_time(面访必填), visit_address
type: VisitType.1(面访)/VisitType.2(电话)/VisitType.3(邮件)/VisitType.4(QQ)/VisitType.5(微信)/VisitType.6(其他)/VisitType.105(企业微信)
```

### 8. ShareCustomer — 客户共享

```
必填: customer_id, share_with（接收人userid，多人用逗号分隔）
效果: 双方都能看到客户
```

### 9. AssignCustomer — 客户分配

```
必填: customer_id, assignee（新跟进人userid）
可选: previous_follower(原跟进人userid), sync_wecom_customer("1"开启/"0"关闭)
效果: 客户转给对方，可同步企业微信客户交接
```

### 10. QueryEmployeeUserId — 查询员工ID

```
必填: employee_name（支持"我"/"自己"）, multiple(0单/1多), status(0在职/all)
用途: 分配/共享客户、分配线索时需要
```

### 11. ReclaimPublicPoolCustomer — 公海捡回

```
参数: customer_name
用途: 提示操作方式（不直接发请求），实际通过 AddCustomerVisit 添加跟进记录捡回
```

### 12. EmployeeAnalysis — 业绩分析

```
必填: employee_name, start_time, end_time, scope(个人/团队)
可选: analysis_type
```

### 13. QueryCustomerContractPayment — 合同查询

```
必填: customer_id（需来自SearchExistingCustomers且check_look=1）
返回: 合同、到账、回款、利润
```

### 14. 🆕 QueryCustomersRecentExpiry — 到期客户查询

```
必填: start_time(YYYY-MM-DD), end_time(YYYY-MM-DD), scope("全部"/"团队"/"个人")
可选: userids（多人逗号分隔；scope=个人时可省略或传 me/自己/我）
用途: 查询即将到期/最近到期的客户，用于续费提醒
```

### 15. 🆕 QueryNoFollowUpCustomers — 未跟进客户查询

```
必填: end_time(YYYY-MM-DD) — 最后跟进截止日期/阈值
可选: company_level — 客户等级筛选（须与字典CompanyLevel一致，用QueryDictByCode查询）
用途: 查询长期未跟进的客户
```

### 16. 🆕 QueryDictByCode — 数据字典查询

```
必填: dict_code — 字典编码
常用编码: CompanyLevel, CompanyType, EmployeesNum, Industry 等
用途: 辅助工具，获取下拉选项值列表
约束: dict_code 必须传系统字典全称，不能传简称、中文名或字段名猜测值；简称会导致查不到或选项不准，影响精准录入
```

### 17. AddOpportunity — 添加线索

```
必填: contact_name, source（需先SearchFieldOptions查选项）
可选: company_name, phone, duty, region, address, email, qq, wechat, memo, receiver
注意: phone/email/qq/tel/wechat 至少填一个
```

### 18. QueryLead — 查询线索

```
参数: keyword（必填）— 公司名称/联系人/手机号
返回: 线索列表（含id和can_make_call_flag）
```

### 19. AssignLead — 分配线索

```
必填: id（线索ID）, receiver（接收人userid）, suggest（备注说明）
```

### 20. SignLeadCall — 通话标记

```
全部可选: id, labeling_status（需SearchFieldOptions查）, labeling_memo
⚠️ 必须先 QueryLead 确认 can_make_call_flag 有权限
```

### 21. AddClue — 添加商机

```
必填: clue_name, company_id, clue_brand, budget(数字), expect_date(YYYY-MM),
      belong_user(自己的user_id), used_brand(需求描述), competitive_brands(竞品分析)
可选: product_ids, cooperater（需SearchFieldOptions查）
品牌: 腾讯标准产品(1)/赢在销客(122)/企业微信私有化(123)/惠岚(1566)/定制开发(1639)
```

### 22. SearchProducts — 产品查询

```
参数: keyword（必填）— 产品名或编号
```

### 23. SearchFieldOptions — 字段选项查询

```
必填: tool_name, field_key
可选: keyword（筛选子串）, limit（最大条数）
tool_name: AddClue/AddCustomerVisit/AddOpportunity/CreateNewBusinessCustomer
用途: 查询单选/多选/下拉字段的 label 和 value
约束: 查询不到字段选项时再用 QueryDictByCode，且 QueryDictByCode 的 dict_code 必须用系统字典全称
```

### 24. 🆕 QueryDailyWriteContext — 日报上下文

```
必填: date（YYYY-MM-DD）— 查询日期
用途: 拉取工作汇总上下文，用于填写日报
```

---

## 员工ID查询（统一规范）

### 需要user_id的接口汇总

| # | 接口 | user_id参数 | 说明 |
|---|------|-------------|------|
| 1 | AssignCustomer | assignee | **必填** - 新跟进人userid |
| 2 | ShareCustomer | share_with | **必填** - 接收人userid（多人用逗号分隔） |
| 3 | AssignLead | receiver | **必填** - 接收人userid |
| 4 | AddClue | belong_user | **必填** - 自己的userid |
| 5 | QueryCustomersRecentExpiry | userids | 可选 - 多人用逗号分隔 |

### 查询员工ID的标准流程

```
Step 1: 调用 QueryEmployeeUserId 查询员工ID
    - employee_name: 员工姓名（支持"我"/"自己"）
    - multiple: 0（单人）或 1（多人）
    - status: 0（仅在职员工）
    ↓
    ├─ ✅ 查询成功 → 获取 user_id，继续调用目标接口
    └─ ❌ 查询失败（无权限/查不到）→ 尝试降级策略（见下方）
```

### 降级策略（QueryEmployeeUserId失败时）

**方案A：直接用员工姓名**
部分接口的userid参数支持直接传入员工姓名字符串，系统会自动匹配：

| 接口 | 参数 | 支持姓名？ |
|------|------|----------|
| AssignLead | receiver | ✅ 支持 |
| AssignCustomer | assignee | ⚠️ 可能支持 |
| ShareCustomer | share_with | ⚠️ 可能支持 |

**方案B：用"我/自己/我"代替**
如果操作对象是当前登录人，可以：
- QueryCustomersRecentExpiry: scope="个人"时可不传userids
- EmployeeAnalysis: 直接用 employee_name="我"

### 调用示例

```bash
# 标准查询员工ID
cat > /tmp/crm_query.json << 'JSONEOF'
{"jsonrpc":"2.0","method":"tools/call","params":{"name":"QueryEmployeeUserId","arguments":{"employee_name":"","multiple":0,"status":0}},"id":1}
JSONEOF
curl -s "https://www.wininsales.com/mcp_api/mcp?token=" \
  -X POST -H "Content-Type: application/json" \
  -d @/tmp/crm_query.json

# 降级：直接用姓名分配线索
cat > /tmp/crm_query.json << 'JSONEOF'
{"jsonrpc":"2.0","method":"tools/call","params":{"name":"AssignLead","arguments":{"id":"线索ID","receiver":"","suggest":"备注"}},"id":1}
JSONEOF
curl -s "https://www.wininsales.com/mcp_api/mcp?token=" \
  -X POST -H "Content-Type: application/json" \
  -d @/tmp/crm_query.json
```

### 特殊说明

- **EmployeeAnalysis** 的 employee_name 参数直接用姓名，不需要先查user_id
- **QueryCustomersRecentExpiry** 的 scope="个人" 时，可以不传userids（自动用当前登录人）
- **AddClue** 的 belong_user 需要自己的user_id，可用 QueryEmployeeUserId(employee_name="我", multiple=0, status=0) 查询

---

## 工商信息 → CRM字段映射

| 工商字段 | CRM字段 | 说明 |
|---------|---------|------|
| companyName | company_name | 直接使用 |
| juridicalPerson | contact_contact_name | 建议作默认联系人 |
| registedCapital | memo | 填入备注 |
| registedDate | memo | 填入备注 |
| address | address | 直接使用 |
| actualAddress | memo | 如与address不同则备注 |
| industry | industry | 可能需要SearchFieldOptions匹配 |
| products | main_product | 主营产品字段 |
| creditCode | memo | 填入备注 |
| webSites | url | 取第一个 |
| staffNumber | scope | 需转换为EmployeesNum编号 |
| province + city | region | 组合填入 |

---

## 场景速查表

> 按老板实际说法整理，零技术术语

| 老板怎么说 | 做什么 | 用什么工具 |
|-----------|--------|-----------|
| "XX公司存在吗" | 客户查重 | SearchExistingCustomers |
| "在谁名下" | 查客户归属和跟进人 | SearchExistingCustomers → AnalyzeCustomers |
| "帮我录入XX公司" | 创建新客户（自动查工商） | 查重 → 工商查询 → CreateNewBusinessCustomer |
| "记录一下跟进" | 添加拜访/电话/微信记录 | SearchExistingCustomers → AddCustomerVisit |
| "看一下XX公司的合同" | 查合同、回款、利润 | SearchExistingCustomers → QueryCustomerContractPayment |
| "查一下本周的业绩" | 团队或个人业绩分析 | EmployeeAnalysis |
| "把XX客户分给XX" | 客户转给同事 | SearchExistingCustomers → QueryEmployeeUserId → AssignCustomer |
| "让XX也能看到这个客户" | 共享客户给同事 | SearchExistingCustomers → QueryEmployeeUserId → ShareCustomer |
| "XX客户在公海，帮我捡回来" | 公海客户捡回 | SearchExistingCustomers → AddCustomerVisit |
| "帮我加个线索" | 添加新销售线索 | SearchFieldOptions → AddOpportunity |
| "查一下线索" | 按名称/电话查线索 | QueryLead |
| "把线索分给XX" | 线索分配给同事 | QueryLead → QueryEmployeeUserId → AssignLead |
| "打了个电话标记一下" | 线索通话标记 | QueryLead → SearchFieldOptions → SignLeadCall |
| "帮这个客户建个商机" | 为客户创建商机 | SearchExistingCustomers → SearchProducts → AddClue |
| "查一下产品" | 按名称或编号查产品 | SearchProducts |
| "有哪些选项可以选" | 查询下拉选项值 | SearchFieldOptions |
| "最近哪些客户要到期" | 查询即将到期客户 | QueryCustomersRecentExpiry |
| "哪些客户很久没联系了" | 查询长期未跟进客户 | QueryNoFollowUpCustomers |
| "帮我写日报" | 拉取工作汇总生成日报 | QueryDailyWriteContext |

---

## 注意事项

1. **必须先查重** — 录入/操作前先 SearchExistingCustomers
2. **工商查询优先** — 录入新客户时自动查工商信息填充
3. **必须二次确认** — 工商信息展示后需用户确认才录入
4. **隐私保护** — 手机号、邮箱中间用 **** 代替
5. **错误处理** — API失败告知原因，不隐瞒
6. **时间格式** — 严格 YYYY-MM-DD HH:MM 或 YYYY-MM
7. **字段选项先查** — 创建商机/线索时，单选字段须先 SearchFieldOptions
8. **字典必须用全称** — QueryDictByCode 的 dict_code 必须传系统字典全称，禁止用简称、中文名或猜测值，否则会导致选项不准、录入不精准
9. **枚举值必须带字典前缀** — 属于字典/选项的值不要写裸数字，统一写成 CompanyLevel.1、EmployeesNum.2、VisitType.5、ContactRole.3、MessageSource.1 这类完整值
10. **禁止编造ID** — customer_id、线索id、产品id必须来自查询结果
11. **禁止编造信息** — 不得编造任何客户信息，不完整时须向用户请求补充
12. **CRMOperationManual仅供参考** — 其返回信息可能不准确，以 tools/list 实际schema为准
13. **分配容错策略** — QueryEmployeeUserId 失败时，可直接用员工姓名作为 receiver/assignee/share_with 参数
14. **员工ID优先查询** — 所有需要user_id的接口（AssignCustomer/ShareCustomer/AssignLead/AddClue）都应先调用 QueryEmployeeUserId

---

## 可靠性检查清单

执行前：
- 查询/写入对象是否明确：客户名、联系人、手机号、线索ID、员工、时间范围。
- 写入前是否已查重：客户录入、建商机、添加跟进必须先定位客户。
- 字典/枚举是否准确：字段选项先用 SearchFieldOptions；字典查询用 QueryDictByCode 全称；枚举值带前缀。
- 权限是否足够：合同、回款、团队业绩、他人客户、员工ID查询可能受 CRM 权限限制。

执行中：
- 查询结果多条时，让用户选择，不自动猜测。
- API 失败时保留原始错误要点，给出下一步方案。
- 降级策略只用于已知可兼容字段，例如员工ID查询失败时尝试员工姓名；不得对客户ID、产品ID、线索ID降级编造。

执行后：
- 查询类给结论、关键字段、风险提示、下一步。
- 写入类给成功/失败状态、对象名称、关键字段、后续建议。
- 对敏感字段继续脱敏展示。

## FAQ

**Q：为什么录入客户前一定要查重？**  
A：CRM 中客户可能在自己名下、他人名下或公海。先查重可以避免重复客户、误录入和后续归属争议。

**Q：为什么字典要用全称，不能写 level、type？**  
A：QueryDictByCode 依赖系统字典全称，例如 CompanyLevel、CompanyType、EmployeesNum。简称或中文名可能查不到，导致录入字段不准。

**Q：为什么枚举值要写 VisitType.2，而不是 2？**  
A：带前缀能明确这是哪个字段的选项，避免不同字段的数字值混淆，例如 VisitType.2 和 CompanyLevel.2 代表完全不同的含义。

**Q：查不到员工ID怎么办？**  
A：先说明可能是权限不足或姓名不匹配；分配线索时可尝试直接用员工姓名，客户分配/共享也可按接口兼容性尝试姓名，但必须说明这是降级方案。

**Q：合同、回款、团队业绩查不到怎么办？**  
A：先检查当前账号是否有权限，再确认客户ID、时间范围、团队范围。不能绕过 CRM 权限，也不能编造数据。

**Q：这个技能能不能保存我的 token？**  
A：不能。token 应由 CRM 授权流程提供，技能文件和上架包不能保存真实 token、密码、API key 或客户隐私。

**Q：CRMOperationManual 返回内容和实际接口不一致怎么办？**  
A：以 `tools/list` schema 和真实 API 返回为准，CRMOperationManual 只作为操作说明参考。

---

## 踩坑经验

（以下由AI在实际调用中自动积累，请勿手动删除）

- SearchExistingCustomers / curl中文参数：shell直接传中文字符串到JSON时可能编码异常，建议用 heredoc 写入临时文件再 `curl -d @file`，或用 printf 管道传入
- AnalyzeCustomers / customer参数必须用公司全称：SearchExistingCustomers返回的company_name是什么就传什么，不能缩写或截断，否则查不到
- QueryDictByCode / 字典编码必须用全称：如 CompanyLevel、CompanyType、EmployeesNum、Industry，不能用 level、type、规模、行业 等简称或中文名，否则会导致查不到选项或选项不精准，进而影响客户/线索/商机录入
- CreateNewBusinessCustomer / 实际无contact_way/follow_up_way字段：CRMOperationManual声称有这两个字段但实际MCP schema中不存在，传入会被静默忽略
- CreateNewBusinessCustomer / tel字段是手机号格式：虽然描述为"企业电话"，但要求11位手机号格式；座机用fax字段
- CreateNewBusinessCustomer / 占位手机号问题：系统会校验手机号真实性，不能用13800000001等明显假号，如无真实手机号可不填contact_phone，用fax填座机
- CreateNewBusinessCustomer / label标识值：Label.16462=潜在客户，Label.16401=企微CRM客户，Label.16469=签约客户，Label.16408=合作代理商，Label.16409=项目合作
- CreateNewBusinessCustomer / scope是企业规模：不是主营产品！scope值用EmployeesNum.1~EmployeesNum.9；主营产品用main_product字段（文本输入）
- CreateNewBusinessCustomer / 建议填全字段：系统有较多隐式必填校验，建议尽量填 level、scope、main_product、region、source、industry、label，减少报错
- CreateNewBusinessCustomer / 联系人字段区分：contact_phone=联系人手机(11位)，contact_tel=联系人座机，tel=企业电话(11位手机格式)，fax=企业传真(座机格式)
- CreateNewBusinessCustomer / 电话冲突：如果报手机号被占用，去掉contact_phone字段重试
- CRMOperationManual / 不可信：返回的字段名、参数格式等信息经常与实际不一致，仅作参考，以 tools/list 获取的实际schema为准
- QueryEmployeeUserId / 可能无权限：部分账号没有查询其他员工ID的权限，此时可降级用员工姓名
- QueryEmployeeUserId / 支持"我"字：用 employee_name="我" 可查询当前登录人的user_id
- AssignLead / 支持姓名直接分配：receiver 参数可直接用员工姓名字符串
- AssignCustomer / 可能支持姓名：assignee 参数降级时可尝试直接用姓名
- ShareCustomer / 可能支持姓名：share_with 参数降级时可尝试直接用姓名
- AddClue / belong_user 必填：添加商机需要自己的user_id，须先 QueryEmployeeUserId(employee_name="我") 查询
- SearchFieldOptions / 可能无权限：如查询来源选项失败，AddOpportunity 的 source 可用默认值 MessageSource.1=线索转化，MessageSource.3=主动开发
- AddOpportunity / contact_name 必填：如果系统报类似“请补充收票人姓名”，优先检查是否缺少 contact_name 或字段映射异常
