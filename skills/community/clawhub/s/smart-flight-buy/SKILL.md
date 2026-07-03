---
name: smart-flight-buy
display_name: 机票聪明买
description: 多旅游平台机票比价与购票决策助手，帮你找到最便宜的机票并告诉你该买还是再等等，含低价日历和降价监控，多旅游平台数据直连。
tags: [机票比价, 低价机票, 购票建议, 机票价格, 航班搜索]
homepage: https://rollinggo.store
tools:
  - name: search
    description: 搜索航班的实时价格并给出购票建议
    parameters:
      - name: from
        type: string
        description: 出发城市，如"北京""上海"
        required: true
      - name: to
        type: string
        description: 到达城市，如"上海""广州"
        required: true
      - name: date
        type: string
        description: 出发日期 YYYY-MM-DD
        required: true
  - name: calendar
    description: 扫描多天价格找到最低价日期
    parameters:
      - name: from
        type: string
        description: 出发城市
        required: true
      - name: to
        type: string
        description: 到达城市
        required: true
      - name: start_date
        type: string
        description: 起始日期 YYYY-MM-DD
        required: true
      - name: days
        type: integer
        description: 扫描天数，默认14
        required: false
  - name: monitor
    description: 输出降价监控请求，由宿主Agent承接定时检查和通知
    parameters:
      - name: from
        type: string
        description: 出发城市
        required: true
      - name: to
        type: string
        description: 到达城市
        required: true
      - name: date
        type: string
        description: 出发日期 YYYY-MM-DD
        required: true
metadata:
  openclaw:
    emoji: "✈️"
    skillKey: smart-flight-buy
---

# 机票聪明买 — 多平台比价+低价日历+买/等建议，帮你买对时机

> 不是搜索工具，是购票决策助手。飞猪+途牛+RG多源实时比价，5维度决策引擎输出🟢买/🟡等/🔴观望信号。

🔥 **核心亮点：**
- **多平台比价** — 飞猪+途牛+RG多源实时对比，同类技能全部为单数据源
- **购票建议** — 5维度决策引擎，输出买/等信号，不再纠结
- **低价日历** — 一键扫描7-30天价格洼地，找最便宜的那天飞
- **降价监控** — 设定阈值，降价自动通知
- **零配置** — 免申请Key，装上就能用

## 快速入门

**3个开场白示例，复制即用：**

1. "北京飞上海7月1号"
2. "下周哪天飞上海最便宜"
3. "帮我盯着北京到三亚的机票"

## 核心能力

1. **单航线搜索+购票建议** — 多源合并航班列表，按价格排序，附带🟢/🟡/🔴购票信号
2. **低价日历** — 扫描多天价格，标注🟢低价/🟡适中/🔴偏贵，找最便宜的日期
3. **降价监控** — 设定降价阈值，触发通知
4. **5维度决策引擎** — 价格分位/距出发天数/旺季判断/多源价差/星期效应综合判断
5. **多源实时比价** — 飞猪+途牛+RG三源数据实时对比
6. **预订链接** — 最低价航班附带预订链接，直接跳转下单

## 能做什么

- 多平台实时比价，找到最便宜的机票
- 给出"买还是等"的明确购票建议
- 低价日历扫描多天价格，找价格洼地
- 设置降价监控，降价自动通知
- 支持直飞/中转、舱位筛选

## 不能做什么

- 不支持直接下单（提供预订链接跳转平台完成）
- 购票建议基于行业规律和数据，不构成消费承诺
- 不支持国际航线

## 使用提示

- 日期灵活时先用低价日历找最便宜的日期
- 🟢建议购买时尽快下手，低价不等人
- 监控功能需要宿主Agent配合定时执行
- 价格实时变动，查询结果仅供参考

## 🔗 搭配使用

- **国内航班查询** — 单纯查航班时刻表用这个更快
- **高铁查询** — 对比火车和飞机哪个更划算
- **旅行预算规划** — 机票确定后规划整体预算

## 数据流向

用户输入（城市/日期等查询参数）→ 本技能脚本 → 代理服务 → 多个旅游平台API → 返回结果给用户。

- 查询参数（城市、日期等）会发送到代理服务以获取实时机票数据
- 代理服务仅做请求转发，不存储任何用户数据或查询记录
- 本技能不收集、存储或传输用户的个人身份信息

## 安全声明

- 认证令牌通过环境变量 `PROXY_TOKEN` 安全读取，源码中无任何硬编码密钥
- 所有HTTPS请求均启用证书验证（verify=True）
- 本技能不处理支付流程、不存储支付凭证、不记录用户敏感信息
