# 人物详情 API 参考

## python脚本参数
- `--hids`：人物ID列表（空格分隔，必需，最多20个）

## 响应数据

### 人物标识
- hid：人物ID
- human_name：人物名称
- gender：F=女性，M=男性
- humanType：1=个人，2=公司，3=不确定
- profiles：人物简介

### 头像信息
- logo_info：头像相关信息
  - logo_url：原始链接
  - logo_url_local：对象存储地址

### 个人属性
- languages_info：语言相关信息
- certifications_info：证书相关信息

### 教育经历
- education_info：教育经历列表
  - sid：学校ID
  - school_name：学校名称
  - start_date：开始日期（秒级时间戳）
  - end_date：结束日期（秒级时间戳）
  - degrees：学业程度列表
  - majors：专业列表
  - minors：辅修科目列表

### 地址信息
- addresses_info：地址相关信息列表
  - address：详细地址
  - postal_code：邮政编码
  - address_type_id：地址类型
  - start_date：地址使用开始时间（秒级时间戳）
  - end_date：地址使用结束时间（秒级时间戳）
  - country_code：地址所属国家代码
  - province_id：省份ID
  - city_id：城市ID
  - country_en：国家名称
  - province_en：省份名称
  - city_en：城市名称
  - street：街道
