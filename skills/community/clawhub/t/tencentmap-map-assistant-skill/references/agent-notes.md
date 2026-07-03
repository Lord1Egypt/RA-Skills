# 调用指引（供 AI 阅读）

本文件补充 SKILL.md 未展开的调用细节，帮助 AI 稳定完成任务。

## 能力命中本 skill 时，用 client 完成

用户需求涉及旅游攻略、找地点、路线规划、地址坐标转换、行政区划、距离计算等，均通过 `TmapClient` 完成，返回的是腾讯位置服务真实数据。

- client 仅依赖 `requests`，多数环境已自带，可直接调用；仅当报 `ModuleNotFoundError: requests` 时执行 `pip install requests` 后重试。
- 调用报错时，读返回的报错信息（key / 网络 / 参数）定位，对应调整后重试。

## Key 策略：检查 tempkey，按需配置正式 Key

每个使用者的腾讯位置服务额度独立。

- **Key 解析顺序**：用户传入参数 → 环境变量 `TMAP_KEY` → skill 包内 `.env` 文件 → `~/.tencentmap/tempkey.json`（临时体验 Key）。
- **无 Key 时**：client 初始化成功，但调用 WebService API 时会抛出 `TmapError`。此时 AI 应引导用户通过 tempkey 流程申请临时体验 Key（手机验证，14 天有效，覆盖 WebService API + JSAPI 底图加载）。**必须读取 `tempkey-guide.md` 获取完整申请流程**（协议展示、脚本调用、错误码表、输出模板等），严格按照其中步骤执行。
- **配置正式 Key**：使用者提供 Key 时，用 `save_key_to_dotenv("Key")` 持久化到 skill 包内 `.env`，重新初始化 client 后自动走正式通道。

```python
from tmap_client import TmapClient, save_key_to_dotenv
c = TmapClient()                 # 自动解析 Key（env / .env / tempkey.json）
# save_key_to_dotenv("XXX-...")  # 使用者提供 Key 时调用
```

## 返回结构：对齐腾讯位置服务官方

所有 WebService 能力（搜索、提示、详情、地址解析、区划、IP、距离矩阵、路线规划）均返回**腾讯位置服务官方原生响应**，结构与官网文档一致。调用后读取实际返回即可，无需预设字段名。

> 行政区划三个方法（`district_list` / `district_children` / `district_search`）的 `result` 是**二维数组**——`result[0]` 才是区划对象列表（官方分组设计），读取时注意取 `result[0]` 而非 `result`。

路线规划 `direction` 仅在调用前自动把起终点的地址/景点名转成坐标，返回的是路线接口原生响应（`result.routes`）。其中驾车/步行/骑行的 `polyline` 为压缩格式，画线前需解压（解压方法见 `jsapi-guide/README.md`）。

## travel_guide 的回复方式

`travel_guide` 返回的 `output_markdown` 是成品攻略文件（含行程正文与小程序入口二维码图片）。

**必须做的事（缺一不可）：**

1. 用 Read 读取 `result["output_markdown"]`，将文件内容**完整作为回复**——包含末尾的 `![腾讯地图小程序入口图](...)` 图片语法。**Markdown 图片语法 `![]()` 完全可以直接在 WorkBuddy 会话中渲染显示**，不需要转换成 base64、不需要上传、不需要用其他方式——直接输出 `![]()` 语法就能看到二维码图。
2. **同时**将 `result["qr_path"]` 指向的二维码 PNG 文件复制到当前工作空间，确保二维码作为实体文件留存在工作区，用户可以随时找到和使用。复制命令参考：`cp /path/to/qrcodes/xxx.png <工作空间路径>/`

文件末尾结构示例：

```markdown
---
![腾讯地图小程序入口图](/path/to/qrcodes/travel_guide_xxx.png)

👆 扫码保存自己的专属地图，在手机上随时查看和导航。
```

> ⚠️ Markdown 图片语法 `![...](...)` 可在 WorkBuddy 会话中内联渲染，请务必通过此方式展示二维码图片，而非仅提供文件路径、转 base64 或其他方式。

## 网页生成（HTML 地图可视化）

涉及"多 POI 对比 / 路线 / 多天行程 / 个人专属地图"等"看图比看字更直观"的场景，可基于结构化数据生成 HTML 网页地图。底图 key、HTML 生成示例、polyline 解压方法、各类 API 与 demo 全部见 `references/jsapi-guide/README.md`，照其中模板生成即可。

> 使用系统默认样式即可。若用户希望修改地图样式，可引导其前往腾讯位置服务官网登录账号，在控制台为对应 Key 配置样式后使用。

## 个人地图指南（generate_map_guide）

`generate_map_guide` 是独立于 A2A 攻略的指南生成能力，可将任意 POI 列表直接生成腾讯地图小程序指南（含二维码），用户扫码即可在手机上查看、导航、分享、编辑。与 `travel_guide` 内含出码不同，本方法需显式调用。

### 业务场景

| 用户说… | 动作 |
|---------|------|
| "帮我记录这几个打卡点" / "生成一个XX地图" / "存到手机上" | 调用 `generate_map_guide()` 生成指南 |
| "帮我搜一下深圳的咖啡馆" → 返回 ≥2 个 POI | 同一回复中调用 `generate_map_guide()` |
| "从A到B怎么走" → direction 路线规划 | 同一回复中调用 `generate_map_guide()` |
| 生成了 HTML 地图可视化 | 同一回复中调用 `generate_map_guide()`，HTML 桌面看 + 小程序手机导航 |
| `travel_guide` 攻略 | 已内置出码，直接 Read `output_markdown`，**无需额外调用** |
| 单点查询 | 只返回数据，不出码 |

### 调用示例

```python
# 路线规划 + 出码的标准流程
route = client.direction("深圳北站", "深圳湾口岸", mode="driving")

# 先用 poi_search 获取真实 POI（id + location 坐标），再映射生成指南
p1 = client.poi_search("深圳北站", region="深圳")["data"][0]
p2 = client.poi_search("深圳湾口岸", region="深圳")["data"][0]
guide = client.generate_map_guide(
    [{"name": p1["title"], "lat": p1["location"]["lat"], "lng": p1["location"]["lng"], "poi_id": p1["id"], "day": 1, "num": 1},
     {"name": p2["title"], "lat": p2["location"]["lat"], "lng": p2["location"]["lng"], "poi_id": p2["id"], "day": 1, "num": 2}],
    city="深圳",
    description="深圳北站 → 深圳湾口岸，约15公里，驾车约30分钟"
)
# guide["output_markdown"] → Read 后作为回复的一部分输出
```

### pois 字段说明

> **数据来源**：`lat` / `lng` / `poi_id` 取自 `poi_search()` / `poi_sug()` 的真实返回（搜索结果中坐标位于 `location.lat/lng`、ID 为 `id`），映射后填入。生成指南前先逐点搜索。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | str | 是 | 地点名称，取自搜索返回的 `title` |
| `lat` / `lng` | float | 是 | GCJ02 坐标，取自搜索返回的 `location.lat` / `location.lng` |
| `poi_id` | str | 是 | POI ID，取自搜索返回的 `id`，保证定位精度 |
| `day` | int | 否 | 天分组，默认 1 |
| `num` | int | 否 | 序号，默认按输入顺序编号 |
| `type` | int | 否 | POI 类型，默认 1。`2` 表示搜索词类型（需配合 `search_query`） |
| `search_query` | str | 否 | 仅在 `type=2` 时使用 |
| `inday` | int | 否 | 散点所属天数，默认 0 |
