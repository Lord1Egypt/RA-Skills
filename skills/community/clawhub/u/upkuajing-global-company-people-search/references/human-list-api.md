# 人物列表搜索 API 参考

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

续跑前向用户展示任务中已保存的唯一记录数、累计列表调用次数与费用、剩余调用额度、原查询与联系方式条件以及剩余最高费用，并再次等待明确确认。执行时只传 `--task_id` 和 `--user_confirmed`；不得用续跑修改数量、增加联系方式阶段、改变联系方式类型或匹配方式。脚本从保存的 cursor 继续，累计调用次数和费用不归零，只能消耗原确认预算中的剩余额度；已有结果按 `hid` 去重，已具备本任务所需具体联系方式的 ID 不再调用联系方式接口。

缺少 `list_call_count`、`max_list_calls`、列表/联系方式累计费用等账本字段的旧任务没有可靠的剩余额度依据，脚本会拒绝自动续跑。此时应重新展示完整确认单并新建任务，避免重复追加或重复计费。

新任务必须包含人物身份、公司/学校，或“职位/专业条件 + 行业/地区范围”的可靠搜索锚点；否则脚本拒绝收费查询。

脚本按人物 `hid` 去重并按 `query_count` 保存唯一记录，最后一页只保留达到目标数量所需的部分。具体联系方式任务可在基础分页外补取 1 页，调用上限必须计入执行前确认单。带职位条件时，脚本使用职位业务词检查匹配质量，将目标职位匹配记录排在完整文件前部，并只对这些记录执行自动联系方式补全。

服务端搜索锚点使用 `titleNames`。当输入仅提供 `titleRoles` 或 `titleSubRoles` 时，脚本在本地校验与联网前自动归一到 `titleNames`；`titleLevels` 只用于职级过滤。

## params API业务参数

### ID筛选
- hids（数组）：人物ID列表
- pids（数组）：公司ID列表
- sids（数组）：学校ID列表

### 关键词搜索
- keywords（数组）：关键词列表（涉及人名、公司名、行业、简介、职位、角色等）
- humanNames（数组）：人物名关键词列表
- humanNamesFilter（数组）：人物名不包含的关键词
- companyNames（数组）：公司名称关键词列表
- companyNamesFilter（数组）：公司名称不包含的关键词
- profiles（数组）：个人简介关键词列表

### 行业筛选
- humanIndustries（数组）：人物行业列表
- humanIndustriesFilter（数组）：不包含的人物行业列表
- companyIndustries（数组）：公司行业列表
- companyIndustriesFilter（数组）：不包含的公司行业列表

### 职位参数
- titleNames（数组）：职位名称关键词列表
- titleNamesFilter（数组）：不包含的职位名称关键词列表
- titleRoles（数组）：职位角色关键词列表
- titleSubRoles（数组）：职位子角色关键词列表
- titleLevels（数组）：职位级别关键词列表
- jobStartDate（整数）：当前职位开始时间（秒级时间戳）
- jobEndDate（整数）：当前职位结束时间（秒级时间戳）
- minExperienceNum（整数）：最小工作经历次数（包含当前值）
- maxExperienceNum（整数）：最大工作经历次数（不包含当前值）
- experienceDesc（字符串）：经历总结描述

### 公司与学校
- schoolNames（数组）：学校名称列表
- companySizes（数组）：公司规模（0-10, 11-50, 51-200, 201-500, 501-1000, 1001-5000, 5001-10000, 10001+）

### 个人信息
- gender：F=女性，M=男性
- humanType（整数）：0=未检测，1=个人，2=公司，3=不确定
- interests（数组）：兴趣爱好列表
- skills（数组）：技能列表
- languages（数组）：语言列表
- certifications（数组）：证书列表

### 地理筛选
- countryCodes（数组）：国家代码列表
- countryCodesFilter（数组）：不包含的国家代码

### 链接筛选
- humanUrls（数组）：人物链接（官网、领英）列表
- companyUrls（数组）：公司链接（官网、领英）列表

### 联系方式筛选
- existPhone：0=全部，1=存在，2=不存在
- existEmail：0=全部，1=存在，2=不存在
- existWhatsApp：0=全部，1=存在，2=不存在
- existWebsite：0=全部，1=存在，2=不存在
- existSocial：0=全部，1=存在，2=不存在

### 其他参数
- sourceNames（数组）：数据来源（depth_company=全球企业库，linkedin=领英）
- sort（整数）：0=匹配度排序，1=综合排序
- isExact（布尔值）：本技能固定为 true；服务端检查目标字段是否包含完整 query，不拆分 query。脚本拒绝 false；同一查询字段内多个 query 之间为 OR
- cursor（字符串）：查询游标；首次请求不传

## 响应数据

### 人物标识
- hid：人物唯一标识
- pid：公司唯一标识
- human_name：人物名称
- company_name：公司名称
- country_code：人物所属国家ISO代码

### 职位信息
- title_names：职位名称列表
- title_levels：职位级别列表
- employee：公司员工人数范围
- experience_num：工作经历次数

### 行业信息
- human_industries：人物行业描述列表
- company_industries：公司行业描述列表

### 个人信息
- gender：F=女性，M=男性
- humanType：1=个人，2=公司，3=不确定

### 联系方式数量
- phone_num：电话数量
- email_num：邮箱数量
- website_num：网址数量
- social_num：社媒数量
- ws_num：WhatsApp数量
- exist_company_website：1=存在，2=不存在

### 其他
- rate：数据评分
- es_score：es匹配评分
- cursor：查询游标（用于下一页）

## 本地结果交付

脚本完成后同时生成包含全部记录的 `result.jsonl` 和 `result.xlsx`。最终输出的 `delivery.displayRows` 最多包含前 10 条默认基础信息；Agent 必须根据用户问题弹性选择有意义的列，并在当前回复中用简洁表格展示，不得展示 ID、游标、内部评分或全空列。用户可以继续基于完整 JSONL 提问，这些操作不调用 API、不产生查询费用。

用户要求具体邮箱、电话、WhatsApp 或联系方式时，在查询前把列表费用与联系方式最高费用纳入同一张确认单。用户确认一次后，直接给列表脚本添加 `--include_contacts` 和所需 `--contact_types email phone whatsapp`。脚本会在内部自动完成列表搜索、按最多 20 个 ID 分批获取联系方式、合并 JSONL 和 Excel；中间不得展示列表或再次确认，只交付最终结果。不得只交付存在状态或库存数量。

最终输出增加 `qualityAssessment`，报告职位质量检查是否启用、检查数量、目标职位匹配数量和扩展结果数量。联系方式输出中的 `successfulIdCount` 只统计已合并具体值的唯一人物；该数量少于 `query_count` 时完整任务为部分完成。每批接口原始响应保存在任务目录的 `contact_response_batches.jsonl`。
