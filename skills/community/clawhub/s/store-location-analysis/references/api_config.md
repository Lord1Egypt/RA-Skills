# 高德地图 API 配置指南

## 获取 API Key

1. 访问 [高德开放平台](https://console.amap.com/dev/key/app)
2. 注册/登录账号
3. 创建应用 → 选择「Web服务」类型
4. 获取 Key（格式如：`xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`）

## 配置方式

**方式一：环境变量（推荐）**
```bash
export AMAP_KEY="your_amap_key_here"
```

**方式二：命令行参数**
```bash
python analyze_location.py --address "..." --store-type "..." --amap-key "your_key"
```

## API 调用配额

高德 Web服务 API 免费额度：
- 地理编码：300,000次/日
- POI搜索：5,000次/日
- 交通态势：2,000次/日

本技能单次分析约消耗：
- 地理编码：1次
- POI搜索：9-12次（8类设施 + 1-3页竞品）
- 交通态势：1次

总计约 11-14 次/分析。

## 备用数据源：百度热力图

如需要更直观的实时人流量数据，可补充百度地图热力图：
- 访问: https://map.baidu.com/ → 图层 → 热力图
- 通过截图 + OCR 可提取热力等级
- 本技能暂未集成百度热力图自动采集

## 摄像头实时数据说明

公共道路摄像头实时画面**不可通过公开API获取**。
本技能使用高德交通态势API（拥堵指数+路段流速）作为人流量代理指标。
如需真实摄像头数据，需对接特定城市的交管开放平台（如北京、上海、深圳等有开放数据平台）。
