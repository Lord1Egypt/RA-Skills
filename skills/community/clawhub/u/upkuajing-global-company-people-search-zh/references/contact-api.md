# 获取联系方式 API 参考

## python脚本参数
- `--bus_type`：业务类型（必需）；1=公司，2=人物
- `--bus_ids`：公司ID或人物ID列表（空格分隔，必需，最多20个）

## 响应数据

### 邮箱列表 emails
- val：邮箱地址
- is_valid：是否有效（0=未检测，1=是，2=否，3=不确定）
- reason：原因

### 电话列表 phones
- val：电话
- is_valid：是否有效（0=未检测，1=是，2=否，3=不确定）
- is_ws：是否WhatsApp（0=未检测，1=是，2=否，3=不确定）
- phone_type：号码类型（0=未检测，1=固定电话，2=移动电话，3=已检测但未知）
- country_code：电话所属国家二字码
- dialing_code：电话所属国际冠码
- area_code：电话所属地区码
- international_number：国际格式号码
- telephone：号码（去除冠码与区码）
- national_number：号码属国格式

### 社交媒体列表 socials
- val：社媒完整链接
- social_url：社媒链接路径
- social_type：社媒类型（linkedin, facebook, twitter, youtube, instagram, pinterest, github, tiktok）
- is_valid：是否有效（0=未检测，1=是，2=否，3=不确定）
- reason：原因

### 网站列表 websites
- val：网址
- is_valid：是否有效（0=未检测，1=是，2=否，3=不确定）
- is_sensitive：是否敏感（0=未检测，1=是，2=否，3=不确定）
- reason：原因
