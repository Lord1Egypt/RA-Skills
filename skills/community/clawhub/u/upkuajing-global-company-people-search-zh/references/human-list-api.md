# 人物列表搜索 API 参考

## python脚本参数
- `--params`: API业务参数（JSON字符串）
- `--task_id`：任务ID；用于继续之前的任务或断点续传
- `--query_count`：期望获取的总记录数；默认20；范围20~1000
- params、task_id 必须指定其一，不能同时指定

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
- isExact（布尔值）：true=精确匹配，false=模糊匹配
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
