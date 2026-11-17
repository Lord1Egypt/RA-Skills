# 公司详情 API 参考

## python脚本参数
- `--pids`：公司ID列表（空格分隔，必需，最多20个）

## 响应数据

### 公司标识
- pid：公司ID
- company_name：公司名称
- company_names：公司曾用名列表
- country_code：国家ISO代码

### 公司规模
- employee：员工人数范围
- employee_num：员工人数
- entity_type：公司实体类型

### 财务与状态
- incorp_date：公司成立时间（秒级时间戳）
- revenue_usd：营收（千美元）
- status：公司状态（1=在业，2=注销，3=吊销，4=迁出，5=经营异常）

### 行业与地址
- industries：行业描述列表
- addresses：公司地址列表
  - address：详细地址
  - postal_code：邮政编码
  - address_type_id：地址类型（0=未知，1=注册，2=服务，3=邮寄，4=发票，5=贸易，6=家庭，7=工作，8=主要，9=其他）
  - start_date：地址开始时间（秒级时间戳）
  - end_date：地址结束时间（秒级时间戳）
  - country_code：国家ISO2
  - province_id：省份ID
  - city_id：城市ID
  - country_en：国家名称
  - province_en：省份名称
  - city_en：城市名称
  - street：街道

### 其他
- stock_codes：股票代码列表
- logos：公司logo信息
- products：公司产品列表
