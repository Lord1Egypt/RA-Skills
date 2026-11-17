# 公司列表搜索 API 参考

## python脚本参数
- `--params`: API业务参数（JSON字符串）
- `--task_id`：任务ID；用于继续之前的任务或断点续传
- `--query_count`：期望获取的总记录数；默认20；范围20~1000
- params、task_id 必须指定其一，不能同时指定

## params API业务参数

### 必需参数
- sort（整数）：排序类型；0=匹配度排序，1=综合排序
- isExact（布尔值）：true=精确匹配，false=模糊匹配

### 关键词搜索
- keywords（数组）：关键词列表（涉及公司名、行业、简介、经营范围、产品、标签）
- companyNames（数组）：公司名称关键词列表
- companyNamesFilter（数组）：公司名称不包含的关键词
- products（数组）：产品关键词列表
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
