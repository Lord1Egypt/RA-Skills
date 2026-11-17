# 联系方式获取 API 参考

## python脚本参数
- `--companyIds`：公司ID列表（空格分隔，必需，最多20个）

## 请求参数

### 必需参数
- companyIds（整数数组）：公司编号列表（最多20个）

## 响应参数
- companyId：公司编号

### 邮箱信息 emails
- val：邮箱地址
- is_valid：是否有效
  - 0：未检测
  - 1：是
  - 2：否
  - 3：不确定
- reason：原因

### 电话信息 phones
- val：电话号码
- is_valid：是否有效（0未检测，1是，2否，3不确定）
- is_ws：是否WhatsApp
  - 0：未检测
  - 1：是
  - 2：否
  - 3：不确定
- phone_type：号码类型
  - 0：未检测
  - 1：固定电话
  - 2：移动电话
  - 3：已检测但未知
- country_code：电话所属国家二字码
- dialing_code：电话所属国际冠码
- area_code：电话所属地区码
- international_number：国际格式号码
- telephone：号码(去除冠码与区码)
- national_number：号码属国格式

### 社交媒体信息 socials
- val：社媒完整链接
- social_url：社媒链接路径
- social_type：社媒链接类型
  - linkedin、facebook、twitter、youtube、instagram、pinterest、github、tiktok
- is_valid：是否有效（0未检测，1是，2否，3不确定）
- reason：原因

### 网站信息 websites
- val：网址
- is_valid：是否有效（0未检测，1是，2否，3不确定）
- is_sensitive：是否敏感
  - 0：未检测
  - 1：是（如电子商务网站）
  - 2：否
  - 3：不确定
- reason：原因
