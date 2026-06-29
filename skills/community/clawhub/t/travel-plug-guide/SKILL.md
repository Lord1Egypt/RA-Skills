---
name: travel-plug-guide
display_name: "旅行插头电压查询"
description: "零配置即装即用，提供3项目的地插头电压查询工具，支持全球200+国家和地区的插头类型、电压标准和转换器推荐，基于国际电工委员会标准数据。"
tags: [旅行插头, 电压查询, 转换插头, 出境充电, 插头类型, 电源适配器, 旅行充电, 万能转换器, 插座标准, 出国充电, travel plug, voltage guide]
tools:
  - name: plug_query
    description: 查询目的地的插头类型、电压、频率和充电注意事项
    parameters:
      - name: destination
        type: string
        description: 目的地国家或地区名称，如"日本""英国""泰国"
        required: true
  - name: adapter_guide
    description: 根据出发地和目的地推荐需要的转换插头类型和购买建议
    parameters:
      - name: from_country
        type: string
        description: 出发地国家，如"中国"，默认中国
        required: false
      - name: to_country
        type: string
        description: 目的地国家
        required: true
      - name: devices
        type: string
        description: 携带的电器类型，可选：phone(手机)、laptop(笔记本)、camera(相机)、hair_dryer(吹风机)、electric_kettle(电热水壶)
        required: false
  - name: voltage_check
    description: 检查电器在目的地电压下是否安全使用，避免烧毁设备
    parameters:
      - name: device_name
        type: string
        description: 电器名称，如"iPhone充电器""戴森吹风机""电热水壶"
        required: true
      - name: destination
        type: string
        description: 目的地国家
        required: true
---

# 旅行插头电压查询

查询全球200+国家和地区的插头类型、电压标准和频率，推荐转换插头，帮你避免到了目的地充不了电或烧毁电器的尴尬。基于国际电工委员会(IEC)标准数据。

## 能做什么

- **插头电压查询**：输入目的地，返回插头类型(ABC等)、电压(110V/220V)、频率(50Hz/60Hz)和充电注意事项
- **转换插头推荐**：根据出发地和目的地，推荐需要购买哪种转换插头，标注是否需要变压器
- **电器安全检查**：检查具体电器在目的地电压下能否安全使用，区分"宽电压"和"单电压"设备

## 不能做什么

- 不提供在线购买转换插头的链接，请到淘宝/京东搜索推荐型号
- 不保证100%准确，部分国家不同地区/酒店可能有差异（如中国港澳用英标）
- 不提供电器维修建议

## 使用示例

1. "去日本需要带转换插头吗？"
2. "中国电器在英国能用吗？"
3. "戴森吹风机带到美国需要变压器吗？"
4. "泰国用什么插头？"
5. "去欧洲多国要带几种转换头？"

## 注意事项

- 所有数据为本地内置，不发送任何外部请求，不收集用户数据
- 部分国家内部不同地区插头标准可能不同（如巴西不同城市不同标准）
- 高档酒店通常备有万能插座，但数量有限建议自备转换头
- 标注"需变压器"的电器如果强行使用可能烧毁，请务必确认

## 使用提示

- 手机/笔记本/相机充电器大多是宽电压(100-240V)，只需转换插头不需变压器
- 吹风机/电热水壶/卷发棒大多是单电压(220V)，带到110V国家需变压器
- 万能转换插头(￥30-50)可覆盖大部分国家，比买单国转换头更实用
- USB充电器+多口USB线是最省空间的方案，减少转换插头数量
- 日本和台湾是110V，充电速度比国内220V慢约一半（手机充电器不受影响）

## 数据流向

所有数据为本地内置，不发送任何外部请求，不收集用户数据。

