# amap — 高德地图

## 👤 人类可读区

查地点、找清华校内餐厅、规划路径、查天气——这些以前要打开高德 App 的事，现在对 AI 说一句话就能做。

- "清华附近有什么好吃的" → 周边餐饮 POI
- "从清华主楼到第六教学楼怎么走" → 步行/驾车路径
- "清华大学地址在哪" → 地理编码
- "海淀今天天气" → 实时天气
- "这个经纬度是哪儿" → 逆地理编码

需要高德 Web 服务 API Key（免费，每日 5000 次个人额度）。详见下方"KEY 申请"。

---

# amap 子技能（AI 操作手册）

## 你的职责

- 路由：用户提地图/位置/天气/路径类需求 → 直接调 `amap.py` 对应子命令
- 解析：高德返回结构化 JSON（含 `pois[]` / `route.paths` / `lives[]` / `regeocode` 等），整理后自然语言回复用户
- 错误：AMAP_KEY 未配置 → 引导用户获取并写入 `.env`；city 必须 adcode 不是中文名 → 提示先用 `district` 查

## CLI 速查（amap.py）

| 子命令 | 典型用法 | 场景 |
|--------|----------|------|
| `text` | `text --keywords "清华大学" --city 110000` | 搜地点/POI（按关键字） |
| `around` | `around --location "116.326,40.003" --radius 500 --type 050000` | 周边搜索（清华校内找餐饮）|
| `detail` | `detail --id B000A7BD6C` | 查某 POI 详情 |
| `route` | `route walking --origin "116.326,40.003" --destination "116.333,40.000"` | 路径规划（walking/driving/transit/bicycling）|
| `geocode` | `geocode --address "北京市海淀区清华大学"` | 地址→坐标 |
| `regeo` | `regeo --location "116.326,40.003"` | 坐标→地址 |
| `weather` | `weather --city 110108` | 天气（city 必传 adcode，如海淀 110108）|
| `ip` | `ip` 或 `ip --ip 8.8.8.8` | IP 定位（仅国内 IPv4）|
| `district` | `district --keywords 北京 --subdistrict 2` | 行政区划（全国/省/市/区）|
| `distance` | `distance --origins "116.326,40.003\|116.330,40.000" --destination "116.333,40.000"` | 距离测量 |
| `staticmap` | `staticmap --location "116.326,40.003" --zoom 16 --save tmp/map.png` | 静态地图 PNG（可保存本地）|
| `campus-dining` | `campus-dining --near "116.334,39.994" --radius 2000` | 清华食堂数据查询（本地快照，附距离）|
| `campus-orgs` | `campus-orgs --category 学院` | 清华机构数据查询（院系/系/研究院/书院/中心，本地快照）|
| `campus-buildings` | `campus-buildings --scope surrounding --name-contains 智造大街` | 清华校内建筑 + 周边建筑（本地快照）|

## 清华常用场景

| 你说 | AI 调 |
|------|-------|
| "清华大学在哪/地址/坐标" | `geocode --address "北京市海淀区清华大学"` |
| "清华主楼附近有什么吃的" | `around --location "116.326936,40.003213" --radius 500 --type 050000` |
| "从清华西门到北门怎么走" | `route walking --origin <西门坐标> --destination <北门坐标>` |
| "海淀今天天气" | `weather --city 110108` |
| "第六教学楼在哪儿" | `text --keywords "清华大学第六教学楼"` → 拿到坐标后 `regeo` |
| "这个坐标在哪" | `regeo --location "<坐标>"` |
| "清华周围 1km 公交站" | `around --location "116.326,40.003" --radius 1000 --type 150200` |
| "X 附近有哪些食堂" | `campus-dining --near <坐标>` + `around --type 050000` → **AI 自己比对两份数据** |

**清华主楼坐标**：`116.326936,40.003213`（高德 GCJ-02 火星坐标系，可直接复用）

## 清华 POI typecode 速查（常用分类）

| 类别 | typecode | 说明 |
|------|----------|------|
| 餐饮 | `050000` | 总餐饮（中餐 050100、咖啡 050500）|
| 购物 | `060000` | 超市 060100、便利店 060400 |
| 生活 | `070000` | 银行 070500、邮局 070400 |
| 教育 | `141201` | 高等院校（清华即此） |
| 交通 | `150000` | 公交站 150200、地铁站 150100 |
| 休闲 | `080000` | 公园 080100、健身 080600 |
| 医疗 | `090000` | 医院 090100、药店 090200 |

完整 6 位分类码表：https://a.amap.com/lbs/static/amap_3dmap_lite/amap_poicode.zip

## 清华官方数据快照

**位置**：`amap/data/` 下三个 JSON 文件。

### tsinghua_canteens.json（**截止 2026-09-11**）

来源：清华饮食服务中心官方页 https://www.tsinghua.edu.cn/ysfwzx（学生食堂/教工餐厅/特色餐厅三页）。

内容：**27 个饮食服务点**（8 学生食堂 + 9 教工餐厅 + 10 特色餐厅），含官方名/类别/电话/位置/简介/高德 POI 名/GCJ-02 坐标。

### tsinghua_orgs.json（**截止 2026-09-11**）

来源：清华官网"院系设置"页（https://www.tsinghua.edu.cn/yxsz.htm）+ 科研机构分类页。

内容：**64 个机构**（23 学院 + 3 非实体学院 + 6 系 + 8 研究院 + 2 实验室 + 5 中心 + 16 书院 + 1 其他），含官方名/类型/官网 URL/下属系所。**清华大学人工智能学院**（collegeai.tsinghua.edu.cn）已收录。

### tsinghua_buildings.json（**截止 2026-09-11**）

来源：清华官网"校园风光"/"走进清华"/"校园景观" + 维基百科 + 北京旅游/中关村/五道口公开资料。

内容：**清华校内 21 个标志性建筑**（主楼/图书馆/四大建筑/教学楼/历史景观）+ **五道口/中关村周边 16 个地标**（清华科技园各楼、智造大街/AI 原点社区、东升大厦、文津国际酒店、搜狐/赛尔/威盛大厦、蓝旗营、华联 U-Center 等）。**校内建筑无坐标**——需坐标时 AI 自行用 `amap text --keywords "<建筑名>"` 补全。

### 调用原则

三个命令（`campus-dining` / `campus-orgs` / `campus-buildings`）**只读**对应 JSON，**不参与召回过滤**。"哪个是用户要的"由 AI 自己根据语义判断。

### 推荐工作流（"X 附近有哪些清华食堂"）
```
1. campus-dining --near "<X>" --radius 2000 → 清华官方食堂 + 距离
2. around --location "<X>" --radius 2000 --type 050000 → amap 周边餐饮
3. AI 比对 poi_name/location/address
4. 整理答复
```

### 推荐工作流（"清华有哪些 AI 相关机构"）
```
1. campus-orgs --name-contains "AI" → 清华 AI 相关机构（人工智能学院/智能产业研究院/碳中和/未来实验室等）
2. campus-orgs --category 书院 → 16 个书院清单（含 AI 方向）
3. 整合答复（含官网 URL）
```

### 推荐工作流（"清华附近有什么"）
```
1. campus-buildings --scope surrounding --name-contains <AI 自传关键词> → 周边建筑
2. campus-orgs --category 学院 --name-contains <关键词> → 周边学院/研究院
3. 整理答复
```

### 为什么不用硬匹配

业务判断（"这是不是清华食堂/哪个机构做 AI 方向"）必须由 AI 做——脚本只给数据，不做关键词匹配（具体案例见每个子命令的 `hint_to_ai`）。

## KEY 申请（用户必看）

1. 打开 https://lbs.amap.com → 注册开发者（手机号/邮箱都行）
2. 进入控制台 https://console.amap.com/dev/key/app
3. 「应用管理」→「我的应用」→「创建新应用」（名称随便填，如"校园技能包"）
4. 在应用里点「添加 Key」：
   - **服务平台必须选【Web 服务】**（不是 Web 端 / JS API，那两个是浏览器用的，本技能调不了）
   - 白名单 IP 不填（个人开发够用；生产场景建议填 IP）
5. 创建后复制 Key → 写入 `skill/campus/.env` 的 `AMAP_KEY=...`

**免费额度**：个人未认证开发者 **5000 次/日**（地理/逆地理/IP 定位/静态地图/路径规划分别计数）。超额停服（不扣费）。认证后升级到月配额（约 300 万次/月）。

**计费说明**：高德 Web 服务 API 调用次数有限制，但**不直接扣费**；超额后会停服直到次日。商用/高频请升级"商用账号"。

## 铁律

- **铁律 1：KEY 走 .env，不硬编码**。所有调用从 `campus/.env` 的 `AMAP_KEY` 读取；`.env` 在 `.gitignore` 内，不上传。
- **铁律 2：天气/路径 city 必须用 adcode**。`weather --city 110108` 而不是 `weather --city 海淀区`；transit 路径必填 city。**如果用户只给了中文城市名** → 先跑 `district --keywords <城市> --subdistrict 1` 查 adcode。
- **铁律 3：经纬度顺序是 经度,纬度**（最容易写反）。`"116.326,40.003"` ✅、`"40.003,116.326"` ❌。
- **铁律 4：坐标系 GCJ-02（火星坐标）**。高德返回的坐标是 GCJ-02；如果用户给的是 WGS-84（GPS 原始数据），需要用 `/v3/assistant/coordinate/convert` 转换（当前脚本未自动转，必要时手动调用）。
- **铁律 5：路径规划中文只走 walking/bicycling 自动判定，transit/driving 必填 origin/destination**（已是 CLI 强制）。
- **铁律 6：脚本不阻塞、不留进程**。`urllib.request.urlopen` 同步调用 → 立即返回 → sys.exit。单次 HTTP 超时 15s。
- **铁律 7：写静态地图用 `--save`**。默认只返回 PNG URL，需要本地文件时传 `--save path.png`。

## 常见错误

| 现象 | 原因 | 修复 |
|------|------|------|
| `AMAP_KEY 未配置` | .env 缺失或字段为空 | 复制 .env.example 为 .env，填入 AMAP_KEY |
| `INVALID_USER_KEY` | Key 类型错（用了 Web 端/JS API 的）| 控制台删掉重建，选【Web 服务】 |
| `CITY_NOT_SUPPORT` | weather/transit 传了中文 city | 改传 adcode（如海淀 110108、北京 110000）；先用 district 查 |
| `NO_DATA` 或 `COUNT=0` | keywords 写错或城市过滤太严 | 简化关键字，去掉 city 试一次 |
| `USER_DAILY_QUERY_OVER_LIMIT` | 5000/日额度用完 | 次日恢复；商用升级 |
| `INVALID_PARAMETERS` | 经纬度顺序写反 | 经度在前纬度在后 |

## 边界

- 仅支持 **Web 服务 API**（后端 HTTP）。**JS API / Web 端 / 移动端 SDK 不在本技能范围**（需要浏览器或原生应用，本技能只在脚本里调 HTTP）。
- 静态地图返回 PNG URL（不直接渲染），需 `--save` 才下载到本地。
- IP 定位仅支持**国内 IPv4**，局域网/国外 IP 返回"局域网"或失败。
- 不支持：实时公交车辆位置（需 G IS 数据权限）、打车（属高德打车 SDK）、路线导航（属 JS API）。

## 如果你是用户，请阅读以下内容

对 AI 说"查一下清华附近有什么好吃的"或"今天海淀天气怎么样"就能直接用。

**前提**：你的 `campus/.env` 里已经有 `AMAP_KEY=...`。如果没配，AI 会告诉你怎么申请（免费、个人版每日 5000 次）。

**隐私**：高德会接收你的查询关键词和坐标。本技能不会上报你的身份信息，但**请勿在 AI 对话里粘贴包含个人信息的地址**（如家庭住址）。
