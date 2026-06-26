---
name: tmap-lbs-skills
description: 腾讯地图位置服务，支持POI搜索、路径规划、旅游规划、周边搜索，轨迹数据可视化和地图数据可视化
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - TMAP_LBS_CONFIG
      bins:
        - node
    homepage: https://lbs.qq.com/service/webService/webServiceGuide/webServiceOverview
---

# 腾讯地图位置服务 Skill

腾讯地图位置服务向开发者提供完整的地图数据服务，包括周边搜索，地点搜索、路径规划、旅游规划等功能。

## 功能特性

- 搜索
  - 支持关键词和 POI 搜索功能
  - 支持基于中心点坐标和半径周边搜索
- 规划
  - 旅行日程规划
  - 路径规划（步行、驾车、骑行、公交）
- 数据可视化
  - 地图数据可视化
  - 轨迹数据可视化展示

当用户想要搜索地址、地点、周边信息（如美食、酒店、景点等）、规划路线时，使用此 skill。

## 触发条件

用户表达了以下意图之一：

- 搜索某类地点或某个确定地点（比如"故宫在哪"，"搜酒店"、"找加油站"）
- 基于某个位置搜索周边（如"奥林匹克公园周边美食"、"北京西站附近的加油站"）
- dan 包含"搜"、"找"、"查"、"附近"、"周边"、"路线"、"规划"等关键词
- 旅游规划（如"帮我规划北京一日游"、"杭州西湖游览路线"）
- 规划路线（如"从故宫到南锣鼓巷怎么走"、"规划一条骑行路线"）
- 轨迹可视化（如"帮我生成轨迹图"、"上传轨迹数据"、"GPS 轨迹展示"）

## 场景判断

收到用户请求后，先判断属于哪个场景：

- **场景一**：用户搜索一个**明确的类别**（美食、酒店）或**确定的地点**（天安门、西湖），没有指定"在哪个位置附近"
- **场景二**：用户搜索**某个位置周边或者附近**的某类地点，输入中同时包含「位置」和「搜索类别或者 POI 类型」两个要素（如"西直门周边美食"、"北京南站附近酒店", "搜索亚洲金融大厦附近的奶茶店"）
- **场景三**：POI 详细搜索（使用 Web 服务 API）
- **场景四**：路径规划
- **场景五**：旅游规划
- **场景七**：轨迹可视化（用户提供了轨迹数据地址，想生成轨迹图）

---

## 场景一：明确关键词搜索

直接搜索一个类别或地点，不涉及特定位置的周边搜索。

> 📖 详细的 URL 格式、执行步骤、示例和回复模板请参考 [references/scene1-keyword-search.md](references/scene1-keyword-search.md)

---

## 场景二：基于位置的周边或者附近搜索

用户想搜索**某个位置周边或者附近**的某类地点。需要先通过地理编码 API 获取该位置的经纬度，再拼接带坐标的搜索链接。

> 📖 匹配到此场景后，**必须先读取** `references/scene2-nearby-search.md` 获取详细的执行步骤、API 格式、完整示例和回复模板，严格按照文档中的步骤执行。

---

## 场景三：POI 详细搜索

使用腾讯地图 Web 服务 API 通过 shell curl 进行 POI 搜索，支持关键词搜索、城市限定、周边搜索等。

> 📖 详细的 curl 请求格式、参数说明和返回数据格式请参考 [references/scene3-poi-search.md](references/scene3-poi-search.md)

---

## 场景四：路径规划

使用腾讯地图 Web 服务 API 通过 shell curl 规划路线。支持步行、驾车、骑行（自行车）、电动车、公交等多种出行方式。

> 📖 详细的 curl 请求格式、各出行方式的 API 端点、参数说明和返回数据格式请参考 [references/scene4-route-planning.md](references/scene4-route-planning.md)

---

## 场景五：旅游规划

用户想去某个城市旅游，提供了多个想去的景点，需要规划最佳行程路线，并可选推荐餐厅、酒店等。需要先通过地理编码 API 获取各景点的经纬度，再拼接旅游规划链接。

> 📖 匹配到此场景后，**必须先读取** `references/scene5-travel-planner.md` 获取详细的执行步骤、API 格式、完整示例和回复模板，严格按照文档中的步骤执行。

---

## 场景七：地图数据可视化

当用户有一份包含轨迹坐标的数据，希望在地图上以轨迹图的形式可视化展示。不需要 API Key。

## 触发条件

用户提到"轨迹"、"轨迹图"、"轨迹可视化"、"GPS 轨迹"、"运动轨迹"、"行驶轨迹"等意图，并提供了数据地址或轨迹数据。

> 📖 匹配到此场景后，**必须先读取** `references/scene7-trail-map.md` 获取详细的 URL 格式、执行步骤、完整示例和回复模板，严格按照文档中的步骤执行。

---

---

## 注意事项

- **场景判断是关键**：区分用户是"直接搜某个东西"、"在某个位置附近搜某个东西"、"规划路线"还是"旅游规划"
- 关键词应尽量精简准确，提取用户真正想搜的内容
- URL 中的中文关键词浏览器会自动处理编码，无需手动 encode
- 如果 API 返回 `status` 不为 `0`，说明请求失败，需提示用户检查地址是否有效
- 腾讯地图坐标格式为 `纬度,经度`（注意：纬度在前，经度在后）
- 场景二的搜索范围默认 1000 米，用户如有需要可调整 `radius` 参数
- 腾讯地图 Web 服务 API 有调用频率限制，请合理使用
- 特别注意，需要在后台登录配置白名单，否则 API KEY 是无效的，分享后临时的 API KEY 请及时销毁
- the URLs can not be shared or logged. these keys are restricted referrers/quotas.

## 文档引用（references）

各场景的详细操作文档存放在 `references/` 目录下：

| 文件                                                                       | 说明                                                           |
| -------------------------------------------------------------------------- | -------------------------------------------------------------- |
| [references/scene1-keyword-search.md](references/scene1-keyword-search.md) | 场景一：明确关键词搜索 — URL 格式、执行步骤、示例、回复模板    |
| [references/scene2-nearby-search.md](references/scene2-nearby-search.md)   | 场景二：周边/附近搜索 — 执行步骤、API 格式、完整示例、回复模板 |
| [references/scene3-poi-search.md](references/scene3-poi-search.md)         | 场景三：POI 详细搜索 — curl 请求格式、参数说明、返回数据格式   |
| [references/scene4-route-planning.md](references/scene4-route-planning.md) | 场景四：路径规划 — curl 请求格式、API 端点、参数和返回数据说明 |
| [references/scene5-travel-planner.md](references/scene5-travel-planner.md) | 场景五：旅游规划 — 使用方法、功能说明                          |
| [references/scene7-trail-map.md](references/scene7-trail-map.md)           | 场景七：轨迹可视化 — URL 格式、执行步骤、完整示例、回复模板    |

---

## 相关链接

- [腾讯位置服务](https://lbs.qq.com/)
- [地点搜索 API 文档](https://lbs.qq.com/service/webService/webServiceGuide/webServiceSearch)
- [Web 服务 API 总览](https://lbs.qq.com/service/webService/webServiceGuide/webServiceOverview)
