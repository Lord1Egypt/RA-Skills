# 商户列表搜索 API 参考

## python脚本参数
- `--params`：搜索参数JSON字符串
- `--task_id`：任务ID（断点续查用）
- `--query_count`：期望获取的总记录数（非必填，默认20）

## 请求参数 (params JSON)

### 核心参数
- `keywords`：搜索词列表（JSON数组）
- `keywordsFilter`：过滤关键词列表（JSON数组）
- `countryCodes`：国家二字码列表（JSON数组，如["CN", "US"]）
- `countryCodesFilter`：过滤二字码列表（JSON数组）
- `provinceIds`：省份ID列表（JSON数组）
- `cityIds`：城市ID列表（JSON数组）
- `companyNames`：店铺名称列表（JSON数组）
- `industries`：行业名称列表（JSON数组）
- `existPhone`：存在电话筛选（boolean，true=只返回有电话的商户）
- `existWebsite`：存在网址筛选（boolean，true=只返回有网址的商户）
- `cursor`：搜索游标（分页用）

### 坐标查询（附近搜索）
- `geoDistance.location.lat`：纬度
- `geoDistance.location.lon`：经度
- `geoDistance.distance`：搜索半径（如"5km"）

## 响应数据

### 商户标识
- companyId：公司ID
- name：名称
- industry：行业

### 地址信息
- country：国家名称
- countryIsoCode：国家二字码
- provinceName：省份名称
- provinceId：省份ID
- cityName：城市名称
- cityId：城市ID
- addressDetail：详细地址
- postcode：邮编

### 坐标信息
- location.lat：纬度
- location.lon：经度
