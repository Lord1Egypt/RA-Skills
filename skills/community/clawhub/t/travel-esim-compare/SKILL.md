---
name: travel-esim-compare
display_name: 旅行eSIM比价助手
description: 出境上网比价助手，支持eSIM套餐比价和WiFi租借查询，覆盖Airalo/Holafly等主流运营商和30+热门目的地，零配置即装即用。
tags: [eSIM比价, 出境上网, 旅行WiFi, 国际漫游, 境外流量]
tools:
  - name: esim_search
    description: 按目的地搜索eSIM套餐，返回多个运营商的价格、流量和有效期对比
    parameters:
      - name: destination
        type: string
        description: 目的地国家或地区，如"日本""泰国""欧洲"
        required: true
      - name: data_gb
        type: string
        description: 需要的流量大小(GB)，如"5""10""20"，默认不限
        required: false
      - name: days
        type: string
        description: 旅行天数，如"7""14"，默认不限
        required: false
  - name: wifi_rental
    description: 查询目的地WiFi租借方案，含随身WiFi和当地SIM卡实体店信息
    parameters:
      - name: destination
        type: string
        description: 目的地国家或地区
        required: true
      - name: pickup
        type: string
        description: 取还方式，可选：airport(机场取还)、delivery(快递)、local(当地购买)
        required: false
  - name: data_tips
    description: 出境上网省钱技巧和注意事项，包含手机兼容性检查和运营商推荐
    parameters:
      - name: destination
        type: string
        description: 目的地国家或地区
        required: true
      - name: usage
        type: string
        description: 主要用途，可选：social(社交聊天)、video(看视频)、work(办公)、nav(导航地图)
        required: false
---

# 旅行eSIM比价助手 — 对比30+目的地eSIM和WiFi方案，选最便宜的上网方式

> 覆盖Airalo/Holafly/eSIM.net等主流运营商，帮你找到性价比最高的出境上网方案。

🔥 **核心亮点：**
- **多运营商比价** — 同目的地多套餐对比，标注每GB单价和性价比排名
- **WiFi租借查询** — 随身WiFi/当地SIM卡实体店信息，含取还方式
- **手机兼容性检查** — 告诉你手机是否支持eSIM功能
- **省钱技巧** — 根据用途推荐最划算方案，短途/长途/多人各有最优解
- **零配置** — 纯本地数据，无需网络

## 快速入门

**3个开场白示例，复制即用：**

1. "去日本7天用什么上网方案最便宜"
2. "泰国eSIM套餐多少钱"
3. "欧洲多国游怎么上网"

## 核心能力

1. **eSIM套餐搜索** — 输入目的地，返回多运营商套餐价格/流量/有效期对比
2. **性价比排名** — 标注每GB单价，帮你找到最划算的套餐
3. **WiFi租借查询** — 随身WiFi租借方案，含机场取还/快递/当地购买
4. **手机兼容性** — 检查手机是否支持eSIM，避免买了用不了
5. **省钱建议** — 根据目的地和用途给出最省钱方案
6. **多国套餐** — 区域套餐(欧洲通/东南亚通)比单国更划算

## 能做什么

- 搜索目的地的eSIM套餐，多运营商价格对比
- 查询目的地WiFi租借方案
- 给出出境上网省钱技巧和手机兼容性检查

## 不能做什么

- 不提供eSIM在线购买链接（价格变动快，请到运营商官网购买）
- 不提供国际漫游方案对比（漫游资费高不建议使用）
- 不提供手机解锁或运营商解绑服务

## 使用提示

- 短途旅行(1-5天)优先看Holafly无限流量，长途(7天+)优先看Airalo按量套餐
- 多国游选择"区域套餐"（如欧洲通/东南亚通），比单国划算
- 纯社交聊天每天500MB够用，看视频每天至少3GB
- 随身WiFi适合多人(3-5人共享)，eSIM适合1-2人
- iPhone XS及以上、多数2022年后安卓旗舰支持eSIM；华为/小米部分型号不支持

## 🔗 搭配使用

- **出境游旅行助手** — 出境游全链路助手
- **旅行插头电压查询** — 出国前的电器和插头准备
- **签证聪明办** — 出境签证办理攻略

## 数据流向

所有数据为本地内置，不发送任何外部请求，不收集用户数据。
