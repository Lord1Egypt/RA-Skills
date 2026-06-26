# 公司详情 API 参考

## python脚本参数
- `--companyIds`：公司ID列表（空格分隔，必需，最多20个）

## 请求参数

### 必需参数
- companyIds（整数数组）：公司编号列表（最多20个）

## 响应参数

### 基本信息
- companyId：公司编号
- name：公司名
- logo：公司logo
- introduce：公司介绍
- industry：行业
- scope：经营范围

### 位置信息
- location：公司位置
- country：国家
- province：省、州
- city：城市
- address：地址
- postcode：邮编

### 注册信息
- registerPerson：注册法人
- registerNumber：注册编号
- registerDate：注册日期
- registerType：注册类型
- registerCapital：注册资金
- registerState：注册状态

### 贸易信息
- companyType：公司贸易类型
  - 0：未知
  - 1：供应商
  - 2：采购商
  - 3：采购商和供应商

### 国家信息
- country.id：国家编号
- country.name_cn：国家中文名
- country.name_en：国家英文名
- country.code_iso2：国家二字码
- country.icon：国旗链接
