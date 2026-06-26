# 公司列表 API 参考

## python脚本参数
- `--params`: API业务参数
- `--task_id`：任务ID；指定task_id时，脚本会找到task_id的执行参数，从最后一条数据继续游标查询；一般用于大数据量查询、异常中断后继续查询；
- `--query_count`：期望获取的总记录数，脚本据此自动计算次数并轮询调用API；非必填；默认值20；取值范围 20~1000；
params、task_id 必须指定其一，不能同时指定时

## params API业务参数
### 必需参数
- companyType（整数）：公司类型`1`：供应商，`2`：采购商
### 贸易时间
- dateStart（整数）：贸易开始时间（毫秒级时间戳）
- dateEnd（整数）：贸易截止时间（毫秒级时间戳）
### 产品筛选
- products（数组）：产品名称列表
- hscodes（数组）：HS海关编码（超过6位，只取前6位）
- productSuperordinate（数组）：产品的上游产品名称列表
- productDownstream（数组）：产品的下游产品名称列表
### 公司筛选
- sellerIds（数组）：供应商公司ID列表
- buyerIds（数组）：采购商公司ID列表
- seller（字符串）：供应商公司名称
- buyer（字符串）：采购商公司名称
### 地理筛选
- sellerCountryCodes（数组）：供应商国家代码
- buyerCountryCodes（数组）：采购商国家代码
- originCountryCodes（数组）：起运国国家代码
- arrivalCountryCodes（数组）：抵运国国家代码
- sellerPort（字符串）：装运港
- buyerPort（字符串）：卸货港
### 联系方式筛选
- existPhone：1（有电话），2（无电话），0（全部）
- existEmail：1（有邮箱），2（无邮箱），0（全部）
- existWhatsApp：1（有WhatsApp），2（无WhatsApp），0（全部）
- existWebsite：1（有网站），2（无网站），0（全部）
- existSocial：1（有社媒），2（无社媒），0（全部）
### 其他参数
- tradeCode（字符串）：提关单号
- minTradeCount（整数）：最小贸易频次数量
- createTimeStart/createTimeEnd（整数）：数据创建日期范围
- isExact（布尔值）：true=精确匹配，false=模糊匹配（默认true）

### 排序
- sorting_field：tradeCount（默认）、latestTradeDate
- sorting_direction：asc、desc（默认：desc）

## 响应

### 公司标识
- companyId：公司ID
- companyType：1（供应商），2（采购商）
- name：公司名称
### 贸易统计
- tradeTotal：贸易总量
- tradeMatchTotal：匹配贸易量
- tradeMatchPercent：匹配贸易占比（%）
- latestTradeDate：最后贸易日期（毫秒时间戳）
### 公司信息
- countryInfo：所属国信息
- scope：公司主营
- address：公司地址
### 产品信息
- productDesc：产品描述
- productTag：产品标签列表
- productNames：标准化产品名称
- productAlias：产品别名
- productSuperordinate：产品的上游产品名称列表
- productDownstream：产品的下游产品名称列表
