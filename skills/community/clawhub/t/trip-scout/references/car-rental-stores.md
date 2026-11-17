# 租车网点查询参考

双平台租车网点查询：神州租车（C端公开JSON API）+ 一嗨租车（SSR页面解析）。
实现: `vendor/car_rental/`，CLI: `scripts/car_stores.py`。

## 快速使用

```bash
python scripts/car_stores.py 乌鲁木齐                # 双平台查询
python scripts/car_stores.py 乌鲁木齐 --source zuche # 仅神州
python scripts/car_stores.py 乌鲁木齐 --source ehi   # 仅一嗨（需 Playwright，较慢）
python scripts/car_stores.py 乌鲁木齐 --json          # JSON 输出
```

```python
from vendor.car_rental import get_stores
result = get_stores("乌鲁木齐")          # {"zuche": [...], "ehi": [...]}
stores = get_stores("乌鲁木齐", source="zuche")["zuche"]
```

## 神州租车 (zuche)

C 端公开 API，**无需登录/Cookie/签名，只需 Referer**。

| 端点 | URI | 入参 | 说明 |
|------|-----|------|------|
| 城市列表 | `/action/carrctapi/order/cityList/v1` | `data={}` | 返回 hotCities + allCities（含 cityId/cityName/经纬度） |
| 网点列表 | `/action/carrctapi/order/deptList/v1` | `data={"cityId": "329", "entrance": 1, "pickupFlag": 1}` | 返回 districtList → deptList |

Base: `POST https://www.zuche.com/api/gw.do?uri=<URI>`
Headers: `Referer: https://www.zuche.com/`（缺失会返回 code=6）+ `Content-Type: application/x-www-form-urlencoded`

网点字段: deptId, deptName, deptAddress, deptLat/deptLon(高德坐标), deptPhone, workTime,
selfServiceFlag(自助), inStationFlag(1=机场，但实测多数城市机场店该值为0，故机场识别以名称含"机场"为准), pickupWebsite。
deptPhone 缺失时回退 servicePhone(400电话)。

### 商家开放平台（本期未用）

`https://developer.zuche.com/api.do` — 面向商家入驻的正式 API（城市/车型/还车网点/报价/下单），
需 pid + key + AES加密 + SHA256验签。网点端点:
- 网点列表: `/resource/openapi/dept/deptList/v1`（lat/lon 必填，车型时间选填）
- 还车网点: `/resource/openapi/dept/returnDept/v1`（车型+时间必填）
后续做报价/下单集成时需申请入驻，走此通道。

## 一嗨租车 (ehi)

无公开 JSON API；booking.1hai.cn 的请求/响应全加密，不可直接调用。
方案: Playwright 解析 SSR 页面。

| 页面 | URL | 说明 |
|------|-----|------|
| 城市列表 | `https://www.1hai.cn/Premises/Index` | **精选页，不完整**（实测连哈密/喀什/阿勒泰/博乐都没有） |
| 网点列表 | `https://www.1hai.cn/yyd_{拼音}/` | SSR HTML，每个网点一个 `<ul>` |

> **⚠️ Premises/Index 城市列表不完整**：它缺漏很多实际有网点的城市。`ehi.py` 内置 `_CITY_PINYIN_SUPPLEMENT`
> 补充已实测验证的城市（阿勒泰→aletai、博乐→bole、伊宁→yining、克拉玛依、哈密、吐鲁番、库尔勒、喀什、和田、阿克苏）。
> 补充城市的拼音通过访问 `yyd_<拼音>/` 页面标题含"`<城市>租车`"验证真实存在（无效城市返回通用首页标题，HTTP 200 但标题不含城市名）。
> 若再遇到"APP 有网点但工具查不到"，按此方法探测拼音后加入补充表。

网点 HTML 结构（实测 2026-08-11）:
```html
<ul>
  <li class="store-nummark">1</li>
  <li class="store-name">天山国际机场店(站内取还)<em class="all-day-ico"></em><em class="icon-common">机场</em></li>
  <li class="store-address">乌鲁木齐市新市区...</li>
  <li class="store-phone">门店电话：<span>18599219983</span></li>
  <li class="store-time">营业时间：<span>0:00-23:59</span><span class="time-tips time-use">可订全天用车</span></li>
</ul>
```
解析要点: name 只取 `.store-name` 的直接文本（em 徽标"机场/高铁站/自助"单独提取用于标志推断）；
营业时间取 `.store-time` 首个 span（第二个 span 是提示文本，如"蜂巢柜"，需排除）。
无经纬度字段（如需可后续用高德 geocode 补齐）。

## 统一数据模型 StoreInfo

```python
name, address, phone, work_time, source("zuche"|"ehi")
lat, lon        # 高德坐标；一嗨为 None
district        # 区域（神州返回；一嗨为 None）
is_self_service, is_airport, is_train_station  # 推断标志
```

机场/火车站推断: 神州 inStationFlag==1 或名称含关键词；一嗨名称含"机场"/"高铁"/"火车站"。

## 降级策略

- `get_stores()` 单平台异常不抛错: 对应 key 为空列表，错误记录在 `{source}_error`
- CLI 仅当全部平台失败时 exit 1，并提示神州可用城市列表
- 神州 API 加鉴权 → 转商家开放平台（需入驻）
- 一嗨 HTML 改版 → 结构化解析失败先走全文正则兜底；仍解析不出则抛错，
  上层降级为只返回神州（`ehi_error` 记录原因）

## 实测基线（2026-08-11）

| 城市 | 神州 | 一嗨 | 备注 |
|------|------|------|------|
| 乌鲁木齐 | 23 个网点 | 20 个网点 | |
| 成都 | 83 个网点 | - | |
| 阿勒泰 | 3 个网点（含雪都机场） | 11 个网点（含联华时代广场店） | 一嗨靠补充映射 |
| 博乐 | 2 个网点（含阿拉山口机场店） | 10 个网点（含博乐站服务点） | 一嗨靠补充映射；阿拉山口机场租车实际要查"博乐" |

## 城市名匹配

两平台均支持精确匹配 + 包含匹配（"乌鲁木齐市" → "乌鲁木齐"）。
神州 cityId 每次从城市列表 API 动态获取，不硬编码。
一嗨拼音从 Premises/Index 页面动态抓取 + `_CITY_PINYIN_SUPPLEMENT` 补充（页面缺漏的城市）。
