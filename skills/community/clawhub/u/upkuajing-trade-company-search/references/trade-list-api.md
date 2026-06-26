# 贸易列表 API 参考

## python脚本参数
- `--params`: API业务参数
- `--task_id`：任务ID；指定task_id时，脚本会找到task_id的执行参数，从最后一条数据继续游标查询；一般用于大数据量查询、异常中断后继续查询；
- `--query_count`：期望获取的总记录数，脚本据此自动计算次数并轮询调用API；非必填；默认值20；取值范围 20~1000；
params、task_id 必须指定其一，不能同时指定时

## params API业务参数
### 贸易时间
- dateStart（整数）：贸易开始时间（毫秒级时间戳）
- dateEnd（整数）：贸易截止时间（毫秒级时间戳）
### 产品筛选
- products（字符串数组）：产品名称列表
- hscodes（字符串数组）：HS海关编码（超过6位，只取前6位）
- productTags（字符串数组）：产品类别标签
### 公司筛选
- seller（字符串）：供应商公司名称
- sellerCompanyId（整数）：供应商公司ID
- buyer（字符串）：采购商公司名称
- buyerCompanyId（整数）：采购商公司ID
### 地理筛选
- sellerCountryCodes（数组）：供应商国家代码
- buyerCountryCodes（数组）：采购商国家代码
- originCountryCodes（数组）：起运国国家代码
- arrivalCountryCodes（数组）：抵运国国家代码
- sellerPort（字符串）：装运港
- buyerPort（字符串）：卸货港
### 运输筛选
- transportModeCodes（数组）：运输方式代码列表
### 联系方式筛选
供应商（exist*Seller）和采购商（exist*Buyer）：
- existEmail*、existPhone*、existWhatsapp*、existWebsite*、existSocial*
- 取值：1（有）、2（无）、0（全部）
- 例如：existEmailSeller=1  需要供应商有邮箱
### 其他参数
- tradeCode（字符串）：提关单号
- isExact（布尔值）：true=精确匹配，false=模糊匹配（默认true）
### 排序
- sorting_field：tradeDate、quantity、weight、amount（默认：tradeDate）
- sorting_direction：asc、desc（默认：desc）

## 响应参数

### 标识字段
- uuid：唯一标识，记录ID
- tradeCode：提关单号
- tradeDate：交易日期（毫秒时间戳）

### 公司标识
- sellerCompanyId/buyerCompanyId：公司ID
- seller/buyer：公司名称

### 贸易指标
- amount：交易金额
- quantity：交易数量
- weight：交易重量
- price：单价
- *Unit: 指标的单位

### 产品信息
- productNames：产品名称列表
- productDesc：产品描述
- productHscode：产品HS编码
- productHscodes6：产品HS编码（6位）
- productCategory：产品类别列表
- productAlias：产品相似词列表
- productSuperordinate：产品上游词列表
- productDownstream：产品下游词列表

### 地理信息
- sellerCountryInfo: 供应商国家信息
- buyerCountryInfo: 采购商国家信息
- originCountryInfo: 起运国信息
- arrivalCountryInfo: 抵运国信息
- productCountryInfo: 生产国信息
- sellerPort/buyerPort: 起运港/抵运港口
- transportModeCode：运输方式代码
