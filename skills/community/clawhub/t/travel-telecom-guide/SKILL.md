---
name: travel-telecom-guide
display_name: 出境旅行通讯助手
description: 出境旅行通讯方案对比与选择助手；帮旅行者对比漫游/当地SIM/eSIM/WiFi蛋方案，推荐最划算的上网通话方式。当用户需要查询出境上网方案、漫游资费、eSIM推荐、当地SIM卡购买、境外通讯对比时使用。
version: 1.0.1
tools:
  - name: query_telecom
    description: 查询目的地通信信息

---

# 旅行出境通讯助手

出境上网通话不踩坑——帮你对比漫游、当地SIM、eSIM、WiFi蛋，选最划算的方案。

## 能力概览

| 序号 | 工具 | 说明 |
|------|------|------|
| 1 | compare_plans | 目的地通讯方案全面对比 |
| 2 | esim_guide | eSIM购买与激活指引 |
| 3 | data_tips | 省流量技巧与离线工具推荐 |

## 工作流程

1. 根据用户需求判断调用哪个工具
2. 执行 `python3 scripts/telecom_guide.py <tool> '<json_params>'`
3. 解析JSON输出，以自然语言回复用户

## 工具参数说明

### compare_plans
对比目的地所有通讯方案。参数：destination(必填，目的地国家或地区), days(选填，旅行天数，默认7), data_need(选填，日均流量需求MB，默认500), need_calls(选填，是否需要通话，默认false)

### esim_guide
查询eSIM购买与激活指引。参数：destination(必填), provider(选填，指定eSIM提供商如airalo/holafly)

### data_tips
省流量技巧与离线工具推荐。参数：scenario(选填，场景如长途飞行/偏远地区/城市游览)

## 数据说明

- 漫游资费基于三大运营商2026年公开标准
- eSIM价格参考主流平台实时报价区间
- 零配置，无需申请任何API Key

## 数据流向

所有数据为本地内置，不发送任何外部请求，不收集用户数据。
