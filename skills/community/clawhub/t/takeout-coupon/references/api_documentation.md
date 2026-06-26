# 外卖优惠券API接口文档

## 接口信息

| 配置项 | 值 |
|--------|-----|
| 接口地址 | `https://agskills.moontai.top/coupon/takeout` |
| 请求方法 | GET |
| 认证方式 | 无需认证 |
| 返回格式 | JSON |

## 接口说明

获取各平台外卖优惠券列表，包括美团、淘宝闪购/饿了么、京东的隐藏外卖券，以及聚合H5领券页面。

## 请求示例

```
GET https://agskills.moontai.top/coupon/takeout
```

无请求参数，直接调用即可。

## 响应参数

### 完整响应结构

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 美团隐藏外卖券列表 | Array | 美团外卖平台优惠券 |
| 饿了么/淘宝闪购隐藏外卖券列表 | Array | 淘宝闪购/饿了么优惠券 |
| 京东隐藏外卖券列表 | Array | 京东外卖优惠券 |
| 聚合H5页面 | Object | 聚合领券页面信息 |

### 优惠券对象 (数组元素)

| 字段名 | 类型 | 说明 |
|--------|------|------|
| title | String | 优惠券标题 |
| coupon_code | String | **优惠券代码，原样呈现，禁止修改** |
| guideline | String | 领取说明 |

### 聚合H5页面对象

| 字段名 | 类型 | 说明 |
|--------|------|------|
| title | String | 页面标题 |
| coupon_h5_qrcode_img_url | String | 二维码图片URL |
| guideline | String | 使用说明 |

## 响应示例

```json
{
  "美团隐藏外卖券列表": [
    {
      "title": "美团外卖节(主推)🔥🔥",
      "coupon_code": "1 %复制信息#% 打开团App http:/¥wnYjVmNWRlNmU¥一起领",
      "guideline": "请复制完整的优惠券代码，打开美团APP领取"
    },
    {
      "title": "美团外卖【品质会场】",
      "coupon_code": "1 %复制信息#% 打开团App http:/¥yuNmIwYjhlNzg¥一起领",
      "guideline": "请复制完整的优惠券代码，打开美团APP领取"
    },
    {
      "title": "美团外卖【商品券】",
      "coupon_code": "1 %复制信息#% 打开团App http:/¥4nOGM1YTQxYzM¥一起领",
      "guideline": "请复制完整的优惠券代码，打开美团APP领取"
    }
  ],
  "饿了么/淘宝闪购隐藏外卖券列表": [
    {
      "title": "淘宝闪购-天天领红包(全场景通用)",
      "coupon_code": "39 HU7405 666:/WtPyUwSf7WL✔三最高抢66元大红包",
      "guideline": "请复制完整的优惠券代码，打开淘宝闪购APP领取"
    },
    {
      "title": "淘宝闪购-叠红包🔥🔥",
      "coupon_code": "77 HU7405 1:/£9QxHUwSSPeC《十最高22元，可叠加",
      "guideline": "请复制完整的优惠券代码，打开淘宝闪购APP领取"
    },
    {
      "title": "淘宝闪购-宵夜专场",
      "coupon_code": "37 HU7405 1:/5Pz1UwSRubC欢每晚8点抢免单红包",
      "guideline": "请复制完整的优惠券代码，打开淘宝闪购APP领取"
    },
    {
      "title": "淘宝闪购-新客专享高额券",
      "coupon_code": "58 HU7405 1:/✔OqQdUwSsScL₤四闪购大额满减红包",
      "guideline": "请复制完整的优惠券代码，打开淘宝闪购APP领取"
    }
  ],
  "京东隐藏外卖券列表": [
    {
      "title": "京东外卖-惊喜红包(主推)",
      "coupon_code": "1！C92RX3cy6JJac3M8！ MF8335",
      "guideline": "请复制完整的优惠券代码，打开京东APP领取"
    },
    {
      "title": "京东外卖-百亿补贴券",
      "coupon_code": "1！C92RX3cy6JJac3M8！ MF8335",
      "guideline": "请复制完整的优惠券代码，打开京东APP领取"
    },
    {
      "title": "京东外卖-综合大额券",
      "coupon_code": "！S4JkL3azkALi8hUp！ ZH9112",
      "guideline": "请复制完整的优惠券代码，打开京东APP领取"
    }
  ],
  "聚合H5页面": {
    "title": "外卖券统一领取页面",
    "coupon_h5_qrcode_img_url": "https://moontai-static.oss-cn-shenzhen.aliyuncs.com/coupon-takeout-mar.png",
    "guideline": "若无法复制优惠券代码，可以使用微信扫码打开领券页面"
  }
}
```

## 重要说明

### coupon_code 处理规则

**严格禁止修改coupon_code字段的任何内容！**

- 优惠券代码可能包含特殊字符：%、¥、✔、！、£、《等
- 这些特殊字符是平台特定格式，必须原样保持
- 禁止添加空格、换行或任何格式化
- 禁止翻译、解释或重新排列代码顺序

### 平台标识

| 平台 | 字段名 |
|------|--------|
| 美团 | 美团隐藏外卖券列表 |
| 淘宝闪购/饿了么 | 饿了么/淘宝闪购隐藏外卖券列表 |
| 京东 | 京东隐藏外卖券列表 |
| 聚合页面 | 聚合H5页面 |

## 错误码

| 情况 | 说明 |
|------|------|
| 正常返回 | 返回JSON数据，包含4个主要字段 |
| 网络错误 | 返回"无法获取优惠券信息，请稍后重试" |
| 解析错误 | 返回"数据解析异常，请联系技术支持" |
