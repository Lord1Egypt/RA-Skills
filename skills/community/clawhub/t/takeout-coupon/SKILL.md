---
name: takeout-coupon
description: 调用外卖优惠券API获取各平台（美团、淘宝闪购/饿了么、京东）的隐藏外卖券列表及聚合领券页面。返回优惠券代码和领取说明，用户可复制优惠码到对应APP领取。
english_description: Call takeout coupon API to fetch hidden coupon lists and aggregated redemption pages for platforms (Meituan, Taobao Flash/Ele.me, JD.com). Returns coupon codes and redemption instructions for users to copy and redeem in corresponding apps.
version: 1.0.1
author: moooai
permissions: 网络访问权限（调用外卖优惠券API）
homepage: https://github.com/moooai/skills
---

# 外卖优惠券

## Overview

此skill通过调用外卖优惠券API接口，获取美团、淘宝闪购/饿了么、京东三大外卖平台的隐藏优惠券，以及一个聚合H5领券页面。返回优惠券代码（coupon_code）和领取指南，供用户复制到对应APP领取优惠。

## Quick Start

1. 调用API: `GET https://agskills.moontai.top/coupon/takeout`
2. 解析返回的JSON数据，包含4个主要部分
3. 按平台分类展示优惠券信息
4. **重要**: coupon_code字段必须原样呈现给用户，不可修改任何内容

## API配置

### 基础信息

| 配置项 | 值 |
|--------|-----|
| API地址 | `https://agskills.moontai.top/coupon/takeout` |
| 认证方式 | 无需认证 |
| 请求方法 | GET |
| 返回格式 | JSON |

### 响应数据结构

```json
{
  "美团隐藏外卖券列表": [
    {
      "title": "美团外卖节(主推)🔥🔥",
      "coupon_code": "1 %复制信息#% 打开团App http:/¥wnYjVmNWRlNmU¥一起领",
      "guideline": "请复制完整的优惠券代码，打开美团APP领取"
    }
  ],
  "饿了么/淘宝闪购隐藏外卖券列表": [
    {
      "title": "淘宝闪购-天天领红包(全场景通用)",
      "coupon_code": "39 HU7405 666:/WtPyUwSf7WL✔三最高抢66元大红包",
      "guideline": "请复制完整的优惠券代码，打开淘宝闪购APP领取"
    }
  ],
  "京东隐藏外卖券列表": [
    {
      "title": "京东外卖-惊喜红包(主推)",
      "coupon_code": "1！C92RX3cy6JJac3M8！ MF8335",
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

### 响应字段说明

| 字段路径 | 类型 | 说明 |
|----------|------|------|
| 美团隐藏外卖券列表 | Array | 美团外卖平台优惠券数组 |
| 饿了么/淘宝闪购隐藏外卖券列表 | Array | 淘宝闪购/饿了么优惠券数组 |
| 京东隐藏外卖券列表 | Array | 京东外卖优惠券数组 |
| 聚合H5页面 | Object | 聚合领券页面信息 |
| [].title | String | 优惠券标题名称 |
| [].coupon_code | String | **优惠券代码，必须原样呈现，不可修改任何字符** |
| [].guideline | String | 领取说明 |
| 聚合H5页面.coupon_h5_qrcode_img_url | String | 聚合二维码图片URL |
| 聚合H5页面.guideline | String | H5页面使用说明 |

## 任务类型

### 1. 获取全平台外卖优惠券

调用API获取所有平台的外卖优惠券，按平台分类展示给用户。

### 2. 获取特定平台优惠券

根据用户指定平台，返回该平台的专属优惠券：
- 美团外卖 → 美团隐藏外卖券列表
- 饿了么/淘宝闪购 → 饿了么/淘宝闪购隐藏外卖券列表
- 京东外卖 → 京东隐藏外卖券列表

### 3. 获取聚合领券页面

返回聚合H5二维码图片，供无法复制优惠券代码的用户使用微信扫码领取。

### 4. 主推优惠券优先

在展示时，主推标记的优惠券（如带🔥🔥或标注"主推"）应优先展示。

## When to use（触发场景）

此skill在以下场景下使用：

1. 用户询问外卖优惠相关信息，例如：
   - "有什么外卖优惠券？"
   - "帮我找外卖红包"
   - "外卖券怎么领？"
   - "美团外卖有什么优惠？"
   - "饿了么优惠券在哪领？"
   - "京东外卖红包"
   - "外卖平台哪个优惠最大？"

2. 用户明确指定某一平台的外卖优惠券，例如：
   - "我要美团外卖优惠券"
   - "淘宝闪购红包"
   - "帮我找京东外卖优惠"

3. 用户遇到优惠券复制问题，例如：
   - "优惠码复制不了"
   - "优惠券怎么用不了"

## 重要规则

### coupon_code 处理规则

**严格禁止修改coupon_code字段的任何内容！**

- 不允许添加、删除、修改任何字符
- 不允许格式化、美化或重新排列
- 不允许翻译或解释代码含义
- 必须原样从API获取、原样呈现给用户

coupon_code可能包含特殊字符（如%、¥、✔、！、£等），这些是平台特定的格式，必须保持原样。

## 使用示例

### 示例1: 用户请求外卖优惠

**用户输入:** "有什么外卖优惠券可以领？"

**处理流程:**
1. 调用 GET https://agskills.moontai.top/coupon/takeout
2. 解析返回的JSON数据
3. 按平台分类展示（美团、淘宝闪购、京东）
4. 每条优惠券展示：标题、优惠券代码、领取说明
5. 同时展示聚合H5二维码图片

**输出格式:**
```
【美团外卖】
1. 美团外卖节(主推)🔥🔥
   优惠券代码：1 %复制信息#% 打开团App http:/¥wnYjVmNWRlNmU¥一起领
   领取说明：请复制完整的优惠券代码，打开美团APP领取

2. 美团外卖【品质会场】
   ...

【淘宝闪购/饿了么】
1. 淘宝闪购-天天领红包(全场景通用)
   优惠券代码：39 HU7405 666:/WtPyUwSf7WL✔三最高抢66元大红包
   ...

【京东外卖】
1. 京东外卖-惊喜红包(主推)
   优惠券代码：1！C92RX3cy6JJac3M8！ MF8335
   ...

【聚合领券页面】
二维码图片：https://moontai-static.oss-cn-shenzhen.aliyuncs.com/coupon-takeout-mar.png
领取说明：若无法复制优惠券代码，可以使用微信扫码打开领券页面
```

### 示例2: 用户指定平台

**用户输入:** "帮我找美团的外卖优惠券"

**处理流程:**
1. 调用API获取数据
2. 仅提取"美团隐藏外卖券列表"部分
3. 按顺序展示美团优惠券

### 示例3: 用户无法复制优惠码

**用户输入:** "优惠券代码复制不了怎么办"

**处理流程:**
1. 展示聚合H5二维码图片
2. 提示用户使用微信扫码打开领券页面

## 错误处理

- API调用失败时，返回友好提示："暂时无法获取优惠券信息，请稍后重试"
- 网络异常时，提供错误原因和重试建议
- 数据解析异常时，提示用户联系技术支持

## Edge cases（边缘场景处理）

### 1. API调用失败
- **场景**: 网络超时、服务器不可用
- **处理**: 返回友好提示"暂时无法获取优惠券信息，请稍后重试"，并建议用户稍后再试

### 2. 数据结构变化
- **场景**: API返回的数据结构与文档不符
- **处理**: 尽量解析可用字段，对无法解析的部分给出提示

### 3. 特定平台无优惠券
- **场景**: 某一平台（如京东）暂无优惠券
- **处理**: 跳过该平台，仅展示有优惠券的平台，并说明"该平台暂无优惠券"

### 4. 用户无法复制coupon_code
- **场景**: 用户反馈优惠券代码复制失败
- **处理**: 提供聚合H5二维码图片URL，提示用户使用微信扫码领取

### 5. coupon_code包含特殊字符
- **场景**: coupon_code可能包含%、¥、✔、！等特殊字符
- **处理**: 严格原样呈现，不进行任何转义或格式化处理

## Resources

### scripts/

- `fetch_coupons.py` - 获取外卖优惠券的主脚本

### references/

- `api_documentation.md` - 完整的API接口文档
