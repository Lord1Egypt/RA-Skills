---
name: "腾讯地图"
version: "2.0.0"
description: "腾讯位置服务 WebService API 工具与微信小程序 LBS 指南。Use for: (1) 用附带的零依赖 CLI 查地理编码/POI/路线/IP定位, (2) 微信小程序地图开发（腾讯地图是微信官方推荐）, (3) GCJ-02 坐标系避坑。Tencent Maps WebService API CLI (zero-dependency) plus WeChat Mini-Program LBS integration guide."
tags: ["tencent", "qqmap", "map", "lbs", "miniprogram", "cli"]
author: "ClawSkills Team"
category: "navigation"
---

# 腾讯位置服务 Skill

附带零依赖 CLI（`scripts/qqmap.py`，仅 Python 标准库）。腾讯地图的
核心优势场景是**微信小程序**——微信官方推荐，坐标系同为 GCJ-02，
小程序 map 组件无缝配合。

## 快速开始

```bash
# lbs.qq.com 免费申请 Key，启用 WebServiceAPI
export QQMAP_KEY=你的key

python3 scripts/qqmap.py geocode "北京市海淀区中关村"
python3 scripts/qqmap.py search 咖啡 北京
python3 scripts/qqmap.py driving 39.984154,116.307490 39.90816,116.434446
```

脚本行为声明：仅请求 `apis.map.qq.com`，不读写本地文件。

## 命令手册

| 命令 | 作用 |
|------|------|
| `geocode <地址>` | 地址 → 坐标 |
| `regeo <lat,lng>` | 坐标 → 结构化地址 |
| `search <关键词> <城市>` | POI 搜索 |
| `suggestion <关键词> <城市>` | 输入联想（做搜索框补全） |
| `driving / walking <起点> <终点>` | 路线规划 |
| `ip [地址]` | IP 定位 |
| `call <path> k=v ...` | 通用兜底：调任意 /ws/ 接口 |

**⚠️ 坐标顺序陷阱**：腾讯地图是 `纬度,经度`（lat,lng），
与高德的 `经度,纬度`（lng,lat）**相反**。跨平台迁移最容易在这里翻车——
症状是坐标点跑到完全不相关的地方（不是偏移几百米，是差出几千公里）。

## 微信小程序 LBS 要点（腾讯地图主场）

1. **选型**：小程序内嵌地图只能用 map 组件（腾讯地图内核），
   配套 API 用腾讯位置服务是阻力最小路径
2. **域名白名单**：小程序后台把 `https://apis.map.qq.com` 加入
   request 合法域名，否则真机必挂（开发者工具不校验，最易漏）
3. **小程序 SDK**：官方提供 `qqmap-wx-jssdk`，封装了本 skill 同款
   WebService 接口
4. **用户定位授权**：`wx.getLocation` 需在 app.json 声明
   `requiredPrivateInfos` 并配置隐私协议，审核收紧后未声明直接拒审

## Agent 典型用法

1. **小程序开发排障**：真机地图接口失败 → 按序查域名白名单、Key 的
   WebServiceAPI 是否启用、Key 是否绑定了小程序 AppID 校验
2. **找地点**：`geocode` + `search` 组合，结果按距离整理
3. **搜索框补全**：`suggestion` 接口做输入联想数据源

## 高频错误码（实测）

| status | 含义 | 处理 |
|--------|------|------|
| 311 | Key 格式错误 | 检查 Key 拼写 |
| 306 | 请求有护网校验/签名错误 | 控制台开了 SK 签名就必须算 sig |
| 301 | 缺少必要参数 | 对照文档补参数 |
| 120x | 配额/QPS 超限 | 免费版每接口日配额独立计算，次日重置 |

签名说明：控制台启用 SK 后，`sig=md5(路径?按key排序的参数&sk=SECRET)`，
本脚本未内置签名，启用 SK 的 Key 请用 `call` 前自行关闭或换 Key。

## 与其他平台对比

微信小程序 → 腾讯（本 skill）；导航/车机 → 高德（`gaode` skill）；
百度系集成/全景 → 百度（`baidu-map` skill）。坐标系迁移见各 skill
的坐标系章节，腾讯↔高德同为 GCJ-02 可直接互用。

## 本 skill 不做什么

- 不含 JavaScript API GL（前端渲染）细节，只覆盖服务端 WebService
- 不提供绕过配额或反爬的方法
