---
name: travel-esim-compare
display_name: "旅行eSIM比价助手"
description: "零配置即装即用，提供3项出境上网工具，支持eSIM套餐比价和WiFi租借查询，覆盖30+热门目的地，基于主流eSIM运营商实时数据。"
tags: [eSIM比价, 出境上网, 旅行WiFi, 国际漫游, 境外流量, eSIM套餐, 上网卡, WiFi蛋, 出国上网, 国际数据, esim compare, travel wifi]
tools:
  - name: esim_search
    description: 按目的地搜索eSIM套餐，返回多个运营商的价格、流量和有效期对比
    primaryEnv: PROXY_TOKEN
    env:
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置，无需手动设置）
        required: false
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
    primaryEnv: PROXY_TOKEN
    env:
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置，无需手动设置）
        required: false
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

# 旅行eSIM比价助手

对比全球30+热门目的地的eSIM套餐价格和WiFi租借方案，帮出境旅客选到最便宜的上网方式。覆盖Airalo、Holafly、eSIM.net等主流eSIM运营商和国内WiFi租赁平台。

## 能做什么

- **eSIM套餐搜索**：输入目的地，返回多个eSIM运营商的套餐价格、流量、有效期对比，标注每GB单价和性价比排名
- **WiFi租借查询**：查询目的地随身WiFi租借方案（机场取还/快递送达/当地购买），含价格和取还方式
- **上网省钱技巧**：根据目的地和用途给出最省钱的上网方案建议，包含手机eSIM兼容性检查方法

## 不能做什么

- 不提供eSIM在线购买链接（价格变动快，请到各运营商官网实时购买）
- 不提供国际漫游方案对比（漫游资费高不建议使用）
- 不保证价格的实时准确性（eSIM价格可能随时调整，查询结果仅供参考）
- 不提供手机解锁或运营商解绑服务

## 使用示例

1. "去日本7天用什么上网方案最便宜？"
2. "泰国eSIM套餐多少钱？"
3. "欧洲多国游怎么上网？"
4. "去韩国WiFi蛋和eSIM哪个划算？"
5. "东南亚出差10天需要多少流量？"

## 注意事项

- eSIM价格可能随时调整，查询结果仅供参考，购买前请到运营商官网确认最新价格
- 使用eSIM前需确认手机支持eSIM功能（iPhone XS及以上、多数2022年后安卓旗舰机支持）
- 部分国产手机（华为/小米/OPPO部分型号）不支持eSIM，需使用实体SIM卡或WiFi方案
- 所有数据为本地内置，不发送任何外部请求，不收集用户数据

## 使用提示

- 短途旅行(1-5天)优先看Holafly无限流量套餐，长途旅行(7天+)优先看Airalo按量套餐
- 多国游选择"区域套餐"（如欧洲通/东南亚通），比单国套餐划算
- 纯社交聊天每天500MB够用，看视频每天至少3GB
- 国内手机号出国前开通国际漫游（用于接收验证码），数据流量用eSIM/WiFi
- 随身WiFi适合多人出行(3-5人共享)，eSIM适合1-2人出行

## 数据流向

所有数据为本地内置，不发送任何外部请求，不收集用户数据。

