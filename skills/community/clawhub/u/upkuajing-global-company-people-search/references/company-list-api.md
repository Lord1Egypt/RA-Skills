# 公司列表搜索 API 参考

## python脚本参数
- `--params`: API业务参数（JSON字符串）
- `--task_id`：任务ID；用于继续之前的任务或断点续传。续跑时自动恢复原确认配置和累计账本
- `--query_count`：期望获取的总记录数；新任务默认20，范围20~1000；续跑时省略并沿用原任务数量
- `--user_confirmed`：用户已在独立消息中确认自然语言查询单和费用后必须传入；否则脚本拒绝调用API
- `--include_contacts`：原始需求包含具体联系方式时启用；列表结束后自动连续调用联系方式接口，不产生中间交付
- `--contact_types`：与 `--include_contacts` 同用；可选 `email`、`phone`、`whatsapp`，只传用户实际要求的类型
- `--contact_match`：脚本保留 `any|all` 参数，但本技能的收费列表流程只使用 `all`。`any` 会把第一个联系方式类型作为列表库存锚点，不能实现真正的“邮箱或电话”，因此不得用于用户任务。邮箱和电话只允许仅邮箱、仅电话、同时具备邮箱和电话三种选择
- params、task_id 必须指定其一，不能同时指定

## 断点续跑

续跑前向用户展示任务中已保存的唯一记录数、累计列表调用次数与费用、剩余调用额度、原查询与联系方式条件以及剩余最高费用，并再次等待明确确认。执行时只传 `--task_id` 和 `--user_confirmed`；不得用续跑修改数量、增加联系方式阶段、改变联系方式类型或匹配方式。脚本从保存的 cursor 继续，累计调用次数和费用不归零，只能消耗原确认预算中的剩余额度；已有结果按 `pid` 去重，已具备本任务所需具体联系方式的 ID 不再调用联系方式接口。

缺少 `list_call_count`、`max_list_calls`、列表/联系方式累计费用等账本字段的旧任务没有可靠的剩余额度依据，脚本会拒绝自动续跑。此时应重新展示完整确认单并新建任务，避免重复追加或重复计费。

新任务必须包含公司ID/链接/名称、产品、行业或关键词中的至少一种正向搜索锚点。仅提供排序、联系方式、国家、规模或排除条件时，脚本会拒绝收费查询。

## params API业务参数

### 必需参数
- sort（整数）：排序类型；0=匹配度排序，1=综合排序
- isExact（布尔值）：本技能固定为 true；服务端检查目标字段是否包含完整 query，不拆分 query。脚本拒绝 false

### 关键词搜索
- keywords（数组）：关键词列表（涉及公司名、行业、简介、经营范围、产品、标签）
- companyNames（数组）：公司名称关键词列表
- companyNamesFilter（数组）：公司名称不包含的关键词
- products（数组）：产品精准短语列表；数组元素之间为 OR，完整命中任意一个即可。每个目标使用 1 个主短语和最多 2 个高置信度等价短语
- productsFilter（数组）：不包含的产品关键词

### 行业与规模
- industries（数组）：行业列表
- industriesFilter（数组）：不包含的行业列表
- companySizes（数组）：公司规模（0-10, 11-50, 51-200, 201-500, 501-1000, 1001-5000, 5001-10000, 10001+）

### 地理筛选
- countryCodes（数组）：国家代码列表（ISO 3166-1 alpha-2）
- countryCodesFilter（数组）：不包含的国家代码

### 营收与成立时间
- minRevenue（数字）：最低营收（千美元，包含当前值）
- maxRevenue（数字）：最高营收（千美元，不包含当前值）
- minCompanyFounded（整数）：最早成立年（包含当前值）
- maxCompanyFounded（整数）：最近成立年（不包含当前值）

### 公司类型与状态
- companyTypeIds（数组）：公司类型ID列表
- companyStatusIds（数组）：公司状态（1=在业，2=注销，3=吊销，4=迁出，5=经营异常）

### 联系方式筛选
- existPhone：0=全部，1=存在，2=不存在
- existEmail：0=全部，1=存在，2=不存在
- existWhatsApp：0=全部，1=存在，2=不存在
- existWebsite：0=全部，1=存在，2=不存在
- existSocial：0=全部，1=存在，2=不存在
- existValidPhone：0=全部，1=存在，2=不存在
- existValildEmail：0=全部，1=存在，2=不存在
- existValildWebsite：0=全部，1=存在，2=不存在
- existPersonContact：0=全部，1=存在，2=不存在

### 其他筛选
- pids（数组）：公司ID列表
- companyUrls（数组）：公司链接列表
- sourceNames（数组）：数据来源（apollo=阿波罗，customs=海关，depth_company=全球企业库，linkedin=领英）
- cursor（字符串）：查询游标；首次请求不传

## 响应数据

### 公司标识
- pid：公司ID
- company_name：公司名称
- company_names：公司曾用名列表
- country_code：国家二字码

### 公司规模
- employee：员工范围
- employee_num：员工数量
- entity_type：公司实体类型

### 财务与状态
- incorp_date：公司成立时间戳（秒级）
- revenue_usd：营收（千美元）
- status：公司状态ID（1=在业，2=注销，3=吊销，4=迁出，5=经营异常）

### 行业与地址
- industries：行业描述列表
- addresses：公司地址列表（含邮编、国家、省、市、街道）
- stock_codes：股票代码列表

### 产品与标签
- products：产品名称列表
- tags：公司标签
- product_alias：产品近似词列表
- product_downstream：产品下游词列表
- product_superordinate：产品上游词列表

### 联系方式数量
- phone_num：电话数量
- email_num：邮箱数量
- website_num：网址数量
- social_num：社媒数量
- ws_num：WhatsApp数量

### 其他
- logos：公司logo信息
- person_contact_show：一条存在的员工联系方式
- source_name：数据来源
- rate：数据评分
- es_score：es匹配评分
- cursor：查询游标（用于下一页）

## 本地结果交付

脚本完成后同时生成包含全部记录的 `result.jsonl` 和 `result.xlsx`。最终输出的 `delivery.displayRows` 最多包含前 10 条默认基础信息；Agent 必须根据用户问题弹性选择有意义的列，并在当前回复中用简洁表格展示，不得展示 ID、游标、内部评分或全空列。用户可以继续基于完整 JSONL 提问，这些操作不调用 API、不产生查询费用。

用户要求具体邮箱、电话、WhatsApp 或联系方式时，在查询前把列表费用与联系方式最高费用纳入同一张确认单。列表按公司 `pid` 去重，并为补足唯一记录预留 1 次列表调用。用户确认一次后，直接给列表脚本添加 `--include_contacts` 和所需 `--contact_types email phone whatsapp`。脚本会在内部自动完成列表搜索、按最多 20 个 ID 分批获取联系方式、合并 JSONL 和 Excel；中间不得展示列表或再次确认，只交付最终结果。不得只交付存在状态或库存数量。
