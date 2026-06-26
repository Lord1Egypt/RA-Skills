---
name: test-publish-dev1
description: 自动将商品从跨睿优质货盘铺货到Ozon电商平台。
version: 1.1.0
author: 跨睿官方技术团队
input_schema:
  type: Object
  properties:
    category:
      type: string
      description: 品类名
    store:
      type: string
      description: 店铺名
    price:
      type: string
      description: 价格区间(比如：0.0~50.0, 注意保留一位小数)

output_display: 此技能不要求输出格式
---

# 自动铺货技能

## 技能描述

本技能用于将商品从跨睿优质商品货盘自动铺货到Ozon电商平台。适用于需要快速将商品在Ozon平台同步上架的场景。该Skill采用浏览器驱动策略，直接操作跨睿自动铺货智能体界面完成工作。

触发词：自动铺货、批量铺货、Ozon铺货、商品同步到Ozon、商品上架到Ozon。

## 什么时候使用

用户需要将商品自动铺货到Ozon电商平台

## 工作流程
1. 根据用户发话内容，解析出铺货品类、店铺、价格区间。
2. 如果品类、店铺、价格区间3个参数齐全，调用scripts/auto_distribute.py脚本，开始铺货逻辑
3. 如果品类、店铺、价格区间3个参数不齐全，则重新进行参数解析。如果最后实在无法解析出完整参数，则输出数据不全的提问，让用户进行补充。此时不需要调用scripts/auto_distribute.py脚本

## 强制限制
1. 不需要自己编程，如果发现已有脚本完成不了任务，直接作为任务失败返回失败结果即可
2. 当识别到用户要铺货时，必须重新识别和收集用户的铺货参数：品类、店铺、价格区间。不允许使用上下文中之前的铺货参数进行铺货，除非用户明确说明，比如用户说： 和上一次品类相同。

## 输出要求
1. 最终输出任务执行结果
