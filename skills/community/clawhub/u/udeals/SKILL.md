# UDeal 会员权益查询

查询美团、淘宝、京东、喜茶、银联等平台会员权益，支持搜索、筛选、对比。

## API 基础信息

- 地址: `https://udeals.utools.icu`
- 格式: JSON
- 鉴权: 无

## 接口列表

### GET /api/benefits
获取所有权益，支持筛选。

| 参数 | 说明 | 示例 |
|------|------|------|
| q | 搜索关键词 | 洁牙、外卖 |
| platform | 平台ID | meituan, taobao-88vip |
| tag | 标签ID | dental-cleaning, airport-lounge |
| type | 类型 | free, paid |

### GET /api/platforms
获取所有平台列表。

### GET /api/platforms/:id
获取指定平台全部权益。

### GET /api/tags
获取所有标签。

## 平台 ID

| ID | 平台 |
|----|------|
| meituan | 美团 |
| taobao-88vip | 淘宝 |
| jd | 京东 |
| heytea | 喜茶 |
| unionpay | 银联 |
| 12306 | 12306 |
| alipay | 支付宝 |
| ctrip | 携程 |

## 标签 ID

| ID | 名称 |
|----|------|
| dental-cleaning | 洁牙 |
| airport-lounge | 机场贵宾室 |
| rail-lounge | 高铁贵宾室 |
| birthday-gift | 生日礼 |
| coupon | 优惠券 |
| member-price | 会员价 |
| points | 积分 |
| video | 视频会员 |
| ticket | 度假 |
| important | 重要 |
| skin-care | 医美护肤 |
| housekeeping | 保洁 |
| powerbank | 充电宝 |
| hair-salon | 美发 |
| airport-fast | 机场快速通道 |
| music | 音乐会员 |
| storage | 网盘 |
| delivery-coupon | 外卖优惠 |
| movie | 电影 |

## System Prompt

```
你是一个会员权益查询助手，帮用户查询各平台会员权益。

API 地址: https://udeals.utools.icu

接口列表:
- GET /api/benefits — 获取所有权益，支持筛选参数: q(搜索), platform, tag, type
- GET /api/platforms — 获取所有平台列表
- GET /api/platforms/平台ID — 获取指定平台的全部权益
- GET /api/tags — 获取所有标签

平台ID: meituan, taobao-88vip, jd, heytea, unionpay, 12306, alipay, ctrip
类型: free(免费), paid(付费)
标签: dental-cleaning(洁牙), airport-lounge(贵宾厅), birthday-gift(生日礼), coupon(优惠券), video(视频会员) 等

使用规则:
1. 用户问权益时调用 API 获取实时数据
2. 支持组合筛选: /api/benefits?platform=meituan&type=free&tag=dental-cleaning
3. 回答时列出权益名称、类型、描述、兑换时间
4. 对比问题多次调用不同平台数据后汇总
```

## 调用示例

```
用户: 我有哪些免费的洁牙权益？
→ GET /api/benefits?q=洁牙&type=free

用户: 美团黑金会员有什么权益？
→ GET /api/platforms/meituan

用户: 哪个平台的机场贵宾厅最好？
→ GET /api/benefits?tag=airport-lounge

用户: 淘宝88VIP有什么权益？
→ GET /api/platforms/taobao-88vip
```
