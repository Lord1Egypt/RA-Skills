---
name: taobao-selection
slug: taobao-selection-new
displayName: 淘宝精选比价
version: 1.0.0
display_name: 淘宝精选
description: 淘宝天猫好货搜索比价领券，标品按到手价排序找最低价，非标品按销量排序找口碑好货，自动筛选包邮+消保+高评分商品，返回优惠券和购买链接。夏日淘宝精选比价，好货不贵
tags:
  - 淘宝比价
  - 天猫购物
  - 好货搜索
  - 领券购物
  - 淘宝天猫
tools:
  - name: search_standard
    description: 标品比价搜索
    env:
      - name: PROXY_URL
        description: 代理服务器地址（自动配置，无需手动设置）
        required: false
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置，无需手动设置）
        required: false
    parameters:
      - name: keyword
        type: string
        description: 搜索关键词
        required: true
      - name: price_min
        type: number
        description: 最低价格
        required: false
      - name: price_max
        type: number
        description: 最高价格
        required: false
      - name: is_tmall
        type: boolean
        description: 仅天猫，默认true
        required: false
      - name: page
        type: number
        description: 页码，默认1
        required: false
  - name: search_lifestyle
    description: 非标品搜索
    env:
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置，无需手动设置）
        required: false
    parameters:
      - name: keyword
        type: string
        description: 搜索关键词
        required: true
      - name: price_min
        type: number
        description: 最低价格
        required: false
      - name: price_max
        type: number
        description: 最高价格
        required: false
      - name: is_tmall
        type: boolean
        description: 仅天猫，默认不限
        required: false
      - name: page
        type: number
        description: 页码，默认1
        required: false
---

# 淘宝精选
> 淘宝天猫一站式购物比价，标品找最低价，非标品找口碑款

## 📌 简介
淘宝天猫好货搜索比价领券技能，2项能力覆盖购物全场景。标品搜索（3C数码家电）按到手价排序，帮你找同款最低价；非标品搜索（服饰美妆家居）按销量排序，帮你找口碑好货。自动筛选包邮+消保+高评分商品。

## ✨ 核心亮点
- ✅ **双模式智能切换**：标品按价格排序找最低价，非标品按销量排序找口碑款
- ✅ **自动筛选品质**：包邮+消保+高评分三重过滤，避免踩坑
- ✅ **优惠券展示**：返回优惠价格和优惠券信息，领券后再下单
- ✅ **天猫优先**：标品默认仅天猫（正品保障），非标品C店好货也能上
- ✅ **类目智能识别**：自动识别品类，避免搜手机壳却出手机壳贴膜配件

## 🚀 快速入门
| 你这样说 | 技能做什么 |
|---------|----------|
| "帮我搜一下iPhone 16" | 标品搜索，按到手价排序找最低价 |
| "1000元以内的电视" | 标品搜索+价格筛选 |
| "夏季连衣裙推荐" | 非标品搜索，按销量排序找口碑款 |

## 🔧 核心能力

### 标品搜索（search_standard）
适用：手机、电脑、耳机、电视、空调、扫地机器人等品牌型号明确的商品。
- 按到手价排序，同款比价格
- 优先天猫店，正品保障
- 自动识别类目避免搜出配件

### 非标品搜索（search_lifestyle）
适用：连衣裙、运动鞋、面膜、绿植、收纳等看销量和口碑的商品。
- 按销量排序，千人千面
- C店好货也能上，不局限天猫
- 找的是大家都在买的口碑款

### 核心功能
1. **标品比价**：3C数码家电等按到手价排序，找同款最低价
2. **非标品找口碑**：服饰美妆家居按销量排序，找口碑好货
3. **价格区间**：设置最低/最高价格，锁定预算
4. **天猫筛选**：标品默认仅天猫，非标品默认不限
5. **翻页浏览**：每页20条，说"下一页"查看更多

## ✅ 能做什么
- 搜索淘宝天猫商品，标品比价格、非标品找口碑
- 按价格区间筛选，锁定预算
- 天猫/全店筛选
- 翻页浏览商品列表

## ❌ 不能做什么
- 不能下单购买，只提供商品信息和购买链接
- 不能查询订单状态或物流信息
- 不能设置降价提醒通知

## 💡 使用提示
- 数据通过云端代理服务器安全转发至淘宝联盟API获取商品数据，代理服务不存储用户个人信息和查询数据
1. 买手机/电脑/家电 → search_standard（按到手价找最低价）
2. 买衣服/鞋包/美妆 → search_lifestyle（按销量找口碑款）
3. 有预算限制 → 加 price_min + price_max 筛选价格区间
4. 搜索无结果时建议换关键词或放宽价格范围
5. 价格参数格式：整数直接传，如1000；小数直接传，如99.9

## 🔗 搭配使用
- [淘宝天天特卖](https://clawhub.ai/cn-shopping/taobao-tiantian)：搜索比价+天天特卖，多渠道找好价
- [淘宝好券精选](https://clawhub.ai/cn-shopping/taobao-haoquan)：搜索比价+领券叠加，双重省钱
- [购物比价助手](https://clawhub.ai/cn-shopping/best-price)：淘宝价 vs 京东拼多多，跨平台确认最低
