---
name: xiaozhi-recycle-order
description: 小智回收自助下单。用于通过小智回收开放平台 API 创建回收订单。当用户需要提交设备回收订单、小智回收下单、回收估价下单时触发此 skill。支持自定义填写回收设备信息（品牌、型号、品类）、联系人、上门地址等。支持设备品类和衣服品类。
agent_created: true
---

# 小智回收自助下单

## Overview

通过小智回收开放平台 REST API 完成自助下单。支持两类订单：

- **设备品类（device）**：手机、电脑、家电等电子设备回收，固定价格 0.01 元
- **衣服品类（clothing）**：旧衣物回收，按重量计价，需先询价后下单

设备下单和衣服下单均需微信登录授权（`jr_sso_token`）。
衣服询价接口无需授权，可直接调用。

## 触发场景

- 用户说「帮我提交一个回收订单」
- 用户提供设备/衣物信息要求「小智回收下单」
- 用户需要「获取回收报价并下单」
- 用户询问「怎么自助回收XX」

## 下单流程

### Step 1: 判断品类并收集信息

首先询问用户要回收的是**设备**还是**衣服**。

---

#### A. 设备品类信息收集

| 字段 | 说明 | 示例 |
|------|------|------|
| `name` | 联系人姓名 | 张三 |
| `mobile` | 联系电话 | 13800138000 |
| `prov_name` | 省份 | 北京 |
| `city_name` | 城市 | 北京市 |
| `area_name` | 区/县 | 朝阳区 |
| `address` | 详细地址 | XX路XX号 |
| `item_brand` | 设备品牌 | 华为 |
| `item_cates` | 设备品类 | 手机 |
| `item_model` | 设备型号 | Mate 60 Pro |
| `remark` | 备注（可选） | 期望上门时间 YYYY-MM-DD |

以下字段使用默认值，**无需向用户询问，也不在订单摘要中展示**：
- `price`: 固定 `0.01`（不展示给用户）
- `source`: 固定 `172`
- `sale_item_name`: 自动取 `item_cates` 的值

---

#### B. 衣服品类信息收集

| 字段 | 说明 | 示例 |
|------|------|------|
| `name` | 联系人姓名 | 彭先生 |
| `mobile` | 联系电话 | 15711111111 |
| `prov_name` | 省份 | 北京 |
| `city_name` | 城市 | 北京市 |
| `area_name` | 区/县 | 朝阳区 |
| `address` | 详细地址 | 北苑路北 |
| `item_weight` | 衣服重量（kg） | 11 |
| `in_express_time` | 期望上门时间 | 2026-06-16 16:00:00 |
| `detail` | 订单备注（可选） | 无 |

以下字段使用默认值，**无需向用户询问**：
- `source`: 固定 `172`
- `goods_type`: 固定 `1`
- `category_id`: 固定 `2767`
- `item_cates`: 固定 `衣服`
- `item_name`: 固定 `衣服`
- `in_express`: 固定 `2`

### Step 2: 确认订单摘要

信息收集完成后向用户展示订单摘要，等用户确认。

### Step 3: 衣服品类 — 询价

（仅衣服品类需要此步骤）

用户确认信息后，先调询价接口获取单价：

```bash
python3 scripts/create_order.py \
  --order-type clothing \
  --query-price-only \
  --prov-name "北京" \
  --city-name "北京市" \
  --area-name "朝阳区"
```

将返回的单价展示给用户，确认总价（单价 × 重量），用户确认后进入下单步骤。

### Step 4: 生成小程序码 + 微信扫码授权 + 自动下单

用户确认后，先生成小程序码图片：

```bash
python3 scripts/create_order.py --login-url-only
```

输出 `code_image` 字段中包含小程序码图片的本地路径。使用 Read 工具读取该图片展示给用户，用户用微信扫描小程序码即可跳转到小智回收小程序完成授权登录。

> 如需网页二维码模式（向后兼容），可加 `--code-type qrcode`。

然后**在前台执行**轮询下单脚本（不要用后台/异步方式）：

**设备品类：**

```bash
python3 scripts/create_order.py \
  --order-type device \
  --name "张三" \
  --mobile "13800138000" \
  --prov-name "北京" \
  --city-name "北京市" \
  --area-name "朝阳区" \
  --address "XX路XX号" \
  --item-brand "华为" \
  --item-cates "手机" \
  --item-model "Mate 60 Pro" \
  --send-code "<sendCode>"
```

**衣服品类：**

```bash
python3 scripts/create_order.py \
  --order-type clothing \
  --name "彭先生" \
  --mobile "15711111111" \
  --prov-name "北京" \
  --city-name "北京市" \
  --area-name "朝阳区" \
  --address "北苑路北" \
  --item-weight 11 \
  --item-price 0.60 \
  --in-express-time "2026-06-16 16:00:00" \
  --send-code "<sendCode>"
```

脚本会先提示用户扫码授权，然后**实时输出**轮询进度。用户扫码点击「允许」后，脚本立即提示「已收到您的确认授权，正在为您自动下单...」并提交订单，**用户立刻看到下单成功的响应**。无需用户再次输入任何指令。

## 行政编码说明

衣服品类下单需要 `provId`、`cityId`、`areaId`（国家标准 GB/T 2260 行政区划代码）。脚本内置了主要省市区映射，会自动根据名称解析。如果解析失败，可以使用 `--prov-id`、`--city-id`、`--area-id` 手动指定。

## 关键注意事项

1. 信息收集完成后向用户展示订单摘要，确认后再提交
2. 衣服品类需先询价，用户确认价格后再下单
3. 微信扫码授权：默认使用小程序码（miniprogram），生成图片后展示给用户扫描；如需网页二维码可用 `--code-type qrcode`
4. sendCode 每次请求动态生成，不可重复使用
5. 轮询超时（120s）后需重新生成 sendCode 发起授权
6. 若返回「该询价信息已下单，请勿重复使用」，说明该询价对应的订单已存在，需要新的询价记录

## Resources

### scripts/create_order.py
下单核心脚本，可直接执行，也可被 import 使用。支持设备/衣服双品类、微信扫码授权、询价和下单。

### references/api.md
API 接口参考文档，包含参数说明和请求示例。
