---
name: trip-planner-0to1
version: 2.0.0
slug: trip-planner-0to1
description: 从 0 到 1 制作一份完整的自由行出行攻略，覆盖需求采集、多源资源调研（小红书 MCP + 地图 + Web 搜索）、方案决策、Markdown 行程书产出、多页交互式网页（指挥中心 + 攻略详情 + 航班卡片）、跨设备 Todo 同步、三链路部署的端到端工作流。适用于东南亚海岛、日本、欧洲自驾、美洲公路旅行等任何自由行场景。触发词：出行攻略、行程规划、自由行、做攻略、旅游计划、travel plan、itinerary、行程单、Todo 清单、旅行规划、路线规划、trip planning、旅行攻略。
---

# Trip Planner 0→1 —— 自由行攻略端到端工作流 v2

## 🔄 版本自检（Skill 加载时自动执行）

**AI 在加载本 Skill 时，必须静默执行以下检查**：

```bash
clawhub inspect trip-planner-0to1 --json 2>/dev/null | grep -o '"version":"[^"]*"' | head -1
```

将远程 `latestVersion.version` 与本文件 frontmatter 中的 `version` 字段对比：

- **远程版本 > 本地版本** → 提醒用户：
  > 📦 trip-planner-0to1 有新版本可用（远程 vX.Y.Z > 本地 vA.B.C）。
  > 运行 `clawhub update trip-planner-0to1` 即可升级。要我帮你更新吗？

  如果用户同意，直接执行 `clawhub update trip-planner-0to1`。

- **版本一致** → 静默，不打扰用户。
- **clawhub 命令不存在 / 网络失败** → 静默跳过，不影响正常使用。

把一次出行攻略从「一张机票 + 模糊的目的地」做到「结构化行程书 + 多页作战指挥网站 + 跨设备 Todo 同步 + 三链路部署」，全流程标准化、可复用、可迭代。

---

## 🎯 核心理念

### 迭代循环，不是瀑布流

```
        ┌─────────────────────────────────────────┐
        │                                         │
        ▼                                         │
  P1 需求澄清 → P2 资源调研 → P3 方案决策       │
        │              ▲            │              │
        │              │            ▼              │
        │         交叉验证     P4 行程书+话术      │
        │              │            │              │
        │              └────────────┘              │
        │                           │              │
        │                           ▼              │
        │              P5 Todo → P6 多页网页       │
        │                           │              │
        │                           ▼              │
        │              P7 同步 → P8 三链路部署     │
        │                           │              │
        └───── 用户反馈 / 新信息 ───┘
```

**P2-P4 是可回溯的循环**。发现路线不对、班次有误、主人砍了某个景点 → 回 P2 重新调研 → 改 P4 → 改 P6 网页。实际项目平均迭代 15-20 轮，不要指望一次性完工。

### 上手即用，而非框架占位

**铁律**：行程书里每个 POI 必须做到"拿起手机照着念就行"。不允许出现：
- `HH:MM | 地点A | 动作描述 | ¥XX` ← 空壳格式
- "到了之后再找" ← 没有具体方案
- "天气不好改室内" ← 不叫 Plan B

---

## 📋 工作流总览（8 Phase + 迭代）

```
Phase 1  需求澄清       → 时间/人数/预算/硬需求/风格/作息
Phase 2  资源调研       → 小红书 MCP + 地图 + Web + 交叉验证
Phase 3  方案决策       → 住宿/交通/一日游/餐厅 + 决策推理链
Phase 4  行程书+话术    → Markdown 行程 + 实操英文话术 + 版本日志
Phase 5  Todo 清单      → 出发前准备 / 行李装备 两大类
Phase 6  多页网页       → 指挥中心 + 攻略详情 + 航班卡片 + 地图路线
Phase 7  数据同步       → localStorage 兜底 + 可选云端（5 种方案）
Phase 8  三链路部署     → 主站 + CDN 镜像 + 本地 HTML 离线
```

---

## Phase 1 —— 需求澄清

**不要自己脑补，缺信息就直接问。**

1. **硬约束**：航班已定？日期/机场/行李额？PNR 号？
2. **人数 & 关系**：几人？夫妻/亲子/朋友团？
3. **预算**：人均总预算 or 每晚住宿上限
4. **强需求**：必做项目？（潜水/极光/米其林/跳伞…）
5. **交通偏好**：自驾 vs 公共？有驾照翻译件？
6. **酒店会籍**：IHG/Marriott/Hilton/GHA/Hyatt
7. **作息偏好**：精确到小时（如"10:00 自然醒，早于此算早起"），早起日必标 ⚠️ 原因
8. **同步需求**：是否需要和同行者跨设备共享 Todo

---

## Phase 2 —— 资源调研（多源并行 + 交叉验证）

### 🔴 交叉验证铁律

**每条关键信息必须 2+ 来源确认**，单一来源不可作为决策依据：

| 信息类型 | 来源 A | 来源 B（验证） |
|---------|--------|---------------|
| 景点/餐厅评价 | 小红书笔记 | Google Maps 评分 + 评论区验证 |
| 自驾距离/时间 | 小红书文字描述 | **Google Maps 实测**（以此为准） |
| 渡轮/船票班次 | 小红书 | **运营方官网/电话确认** |
| 配额/预约制 | 小红书 | 官网 + 潜店/运营方 WhatsApp 确认 |
| 坐标/定位 | AI 记忆/估算 | **Google Maps / Wanderlog 官方链接** |

### 2.1 小红书 MCP

**推荐作为第一信源**——中文攻略帖的"避坑信息"密度远高于英文 Google。

**三种公网可用方案**（按推荐顺序）：

#### 方案 A：npx 一键启动（推荐，零配置）

```json
{
  "mcpServers": {
    "xiaohongshu": {
      "command": "npx",
      "args": ["xiaohongshu-mcp@latest"]
    }
  }
}
```

首次运行自动打开浏览器登录页，扫码后 cookie 持久化到 `~/.mcp/rednote/cookies.json`。

无头模式（服务器/后台）：
```json
{ "args": ["xiaohongshu-mcp@latest", "--headless"] }
```

#### 方案 B：Docker（xpzouying/xiaohongshu-mcp，13k+ star）

```bash
docker pull xpzouying/xiaohongshu-mcp
wget https://raw.githubusercontent.com/xpzouying/xiaohongshu-mcp/main/docker/docker-compose.yml
docker compose up -d
# 暴露 http://localhost:18060/mcp
```

MCP 配置：
```json
{
  "mcpServers": {
    "xiaohongshu": {
      "url": "http://localhost:18060/mcp"
    }
  }
}
```

首次使用调 `get_login_qrcode` 扫码登录，或上传 Cookie JSON。

#### 方案 C：Cookie 环境变量模式（轻量，适合 CI/脚本）

```json
{
  "mcpServers": {
    "xiaohongshu": {
      "command": "npx",
      "args": ["@dengpengfei/xiaohongshu-mcp"],
      "env": { "xiaohongshu_cookie": "<浏览器 F12 复制的 cookie>" }
    }
  }
}
```

#### 常用工具

| 工具 | 用途 | 关键技巧 |
|------|------|---------|
| `search_feeds` | 搜攻略帖 | 至少 3 组关键词，看发帖 <3 月的 |
| `get_feed_detail` | 笔记正文 + 评论区 | **评论区才是金矿**！看差评和追问 |
| `list_feeds` | 首页推荐 | 找当季热门目的地 |
| `user_profile` | 博主历史笔记 | 深挖专业玩家 |

#### 搜索关键词模板

```
<目的地> 避坑
<目的地> 最新攻略 2026
<目的地> <月份> 天气 穿什么
<目的地> 自驾 RORO 带车（岛屿场景）
<活动名> 预约 配额 提前多久
<景点> 值不值得去
<餐厅名> 评价 踩坑
```

#### 陷阱识别

- 90% "精品一日游"帖子是商业推广 → 只看**评论区真实反馈**
- 博主说"xx km / xx 分钟" → **必须 Google Maps 验证**，小红书距离描述经常不准
- "提前一天都能约" vs "提前一个月订满" → 取**保守值**，关键活动按"可能订满"安排

详细筛选标准见 `references/research-prompts.md`。

### 2.2 地图 API

查**实际行车距离和时间**，至少对比 2 条路线：

| 工具 | 场景 |
|------|------|
| Google Maps（手工 / `google-maps-api` skill） | 全球权威，路线对比必用 |
| 高德/百度 | 国内目的地 |
| OSRM（浏览器侧实时调用） | 网页地图路线渲染 |

**经验**：
- 山区/岛屿：海岸线绕远反而比内陆快（路况好）
- 凌晨/深夜：可压缩 30-40% 时间（无车）
- 必须标注**出发酒店→目的地**的精确 km 和 min，不是"大概 1 小时"

### 2.3 Web Search + WebFetch + agent-browser

| 任务 | 工具 | 产出 |
|------|------|------|
| 酒店比价 | WebSearch + agent-browser（Agoda/Booking 反爬严重） | 比价 .md 表格 |
| 渡轮/船票班次 | WebFetch 官网 | 班次表 + 电话 |
| 签证/入境 | WebSearch 外交部/大使馆 | 要求清单 |
| 租车/SIM/一日游 | Klook / KKday | 链接 + 价格 |

### 2.4 better-icons skill（图标检索）

网页需要图标时：
```bash
better-icons search <关键词>   # 搜索 200+ 图标库
better-icons get <icon-id>     # 获取 SVG
```

推荐组合：**Noto 3D**（装饰锚点）+ **Lucide**（功能图标）。

---

## Phase 3 —— 方案决策

### 3.1 住宿

```
有酒店会籍？
├─ 是 → 官网直订（升房 + 早餐 + 酒廊）
└─ 否 → Agoda + Booking + Trip.com + Kayak + 官网 五方比价
          └─ 必查：含早？免费停车？步行到景点？取消政策？
```

**产出**：`<目的地>酒店比价_<日期>.md`，金额同标本币 + CNY。

### 3.2 交通

- **自驾**：选车 + **第三方全险**（比租车行 CDW 便宜且覆盖全）+ 国际驾照
- **自驾酒店必查**：有没有免费停车？（影响选型！）
- **跨岛/渡轮**：精确到班次时刻表 + 带车费用 + 购票方式（线上/现场/电话）

### 3.3 一日游 / 体验

- 自驾版选 `self-drive, meet at jump-off`（省接送费 ₱500-800/人）
- 提前查**配额制**项目：船潜/鲸鲨/跳伞 → 提前多久锁名额？黄金周是否会满？
- 用小红书评论区验证"提前几天订够不够"

### 3.4 餐厅

- 每天午/晚各 2 家候选（主选 + Plan B）
- Google Maps ≥4.3 + 评论数 ≥300
- 选择理由写进行程书（为什么选这家、为什么不选另一家）

---

## Phase 4 —— 行程书 + 实操话术

### 4.1 行程书 Markdown

文件名：`<目的地><出行方式>行程_v<N>_<日期>.md`

**骨架**：`references/templates/itinerary-template.md`

**🔴 v2 新增强制要求**：

#### 版本变更日志（文档顶部）

```markdown
> **版本说明**：2026-04-23 10:55 第六次更新。
> - v2.0：初版
> - v2.1：xx 改成 yy（原因：xxx）
> - v2.2：砍掉 xx（原因：走那条路多开 2.5h，性价比低）
```

每次改动都写 WHY，让行程逻辑可追溯。

#### 每个 POI 必须包含

| 要素 | 示例 |
|------|------|
| 精确地点 | Jollibee Bulacao Cebu, Cebu South Road |
| 选择理由 | "Bulacao 之后再往南没 24h 店了" |
| 导航关键词 | Google Maps 搜 `Jollibee Bulacao` |
| 电话/联系方式 | (032) 273-1199 |
| 费用 | ₱130-160（≈¥17-21） |
| 避坑提示 | "别搜成 Tabunok 那家不是 24h" |

#### Plan B 精确度要求

**禁止**：
- ❌ "天气不好改室内"
- ❌ "航班异常另行安排"

**必须**：
- ✅ "Argao 误船 → 等 18:00 末班（班次实查确认存在）"
- ✅ "Tubigon 出幺蛾子 → 切 Loon 11:00 班（35km/45min）"
- ✅ Plan B 精确到**替代航线/班次/耗时/费用**

### 4.2 实操话术（Phase 4.5）

**🔴 新增层**：对自驾取还车、语言沟通、拒绝推销等场景写**英文/当地语原话**。

```markdown
### 🛫 取车柜台话术（拒绝推销加保险）

员工说：*"Sir, do you want to add Super CDW? PHP 2,000/day."*
**你回**：
> "No thanks, I already have third-party coverage with RentalCover.
> Here's the policy. Please note in the contract that I declined the CDW upgrade."

### 🏞 Canyoneering 运营商沟通

关键词：**"self-drive, meet at jump-off, no pickup, finish by 15:00"**

### 🐋 鲸鲨现场 SOP

1. 05:45 走到 briefing area（住宿步行即到）
2. 6:00 第一波下水
3. 浮潜 ₱1,500/人，直接跟工作人员买票
```

**话术覆盖场景**：
- 租车取还车（拒绝加保险、争取新车、还车验车签字）
- 一日游集合（自驾版沟通关键词）
- 酒店入住（会籍权益请求）
- 事故处理 SOP（报警→拍照→通知租车行→索赔流程）
- 砍价/拒绝宰客

---

## Phase 5 —— Todo 清单

分**两大类**（不是三段）：

```
📋 出发前准备    → 紧急（u0-uN）+ 重要（i0-iN）+ 已完成（d0-dN 沉底）
🎒 行李装备清单  → 全部装备（p0-pN）+ 已确认/已带（d 沉底）
```

**每条必须有**：
- 主标题（动词 + 对象）
- `<small>` 副说明：去哪办、多少钱、对应哪个行李项
- 图标（Lucide SVG，内联 sprite）
- `data-id` 唯一

---

## Phase 6 —— 多页交互式网页

### 🔴 多页架构（替代单页假设）

| 页面 | 职责 | 文件名 |
|------|------|--------|
| **指挥中心** | 地图 + 行程概览表 + Todo + 进度条 + 同步 | `index.html` |
| **完整攻略** | Day by Day 时间轴 + 全部话术 + 避坑 + 折叠详情 | `guide.html` |
| **航班卡片** | 登机牌视觉 + PNR + 柜台话术 + 机场重点提示 | `flight.html` |

三页互相导航链接，顶部 sticky nav 快速切换。

### 视觉设计系统

| 位置 | 图标类型 | 示例 |
|------|---------|------|
| 卡片标题装饰徽章 | **Noto 3D 彩色**（立体渐变方块） | 飞机、酒店、地图 |
| 功能性图标（Todo/导航/操作） | **Lucide 线性白色** | check、clipboard、backpack |
| 内联 SVG sprite | `<svg><symbol id="i-xxx">` 放 body 开头 | 全站共享 |

**设计约束**：
- 深色海洋主题（`#0a1628` 底色 + `#4fc3f7` 主色 + `#ffab40` 强调色）
- 卡片左侧彩色渐变竖条
- Todo 紧急标签带 2s 脉冲光晕动画
- 进度条渐变填充 + 百分比大字

### 地图路线（指挥中心必备）

**铁律**：地图必须同时有 marker + 路线 + 里程表 + 导航链接。

1. 地图上按 marker 顺序串接的**真实公路路线**（OSRM 浏览器侧实时调用 + localStorage 缓存 + 失败回退直线）
2. 地图正下方"**自驾里程汇总**"表格（每段 km / 耗时 / 方式 + 顶部总里程）
3. marker 递增数字标号（严格按行程顺序）
4. 底部"各路段一键导航"链接（自驾 → Google Maps，飞行 → Google Flights）

**不要只放大头针就交付。**

用 `references/templates/patch-trip-page-v2.js` 一键注入路线 + 里程表 + 导航。

### 🔴 坐标验证 SOP

景点/潜点/餐厅坐标**禁止**：
- ❌ 复用酒店坐标（酒店在马路边，下水点在海岸）
- ❌ 凭记忆/估算写坐标
- ❌ 小红书文字描述转坐标

**必须**：
- ✅ 从 Google Maps / Wanderlog 官方链接提取坐标（`?api=1&query=lat,lng`）
- ✅ 卫星图确认坐标在正确位置（海里的在海里，岸上的在岸上）
- ✅ 沿海点位：验证经度是否在海岸线正确侧

### 瓦片选择

| 瓦片 | 适用 | 注意 |
|------|------|------|
| **Esri ArcGIS**（街道+卫星） | 首选，无 Referer 限制 | ✅ |
| **CARTO**（Voyager/Positron） | 备选，免费 CDN | ✅ |
| ❌ OSM 官方 `tile.openstreetmap.org` | 禁用 | 需要 Referer，file:// 会 403 |

默认卫星影像（看海岸线/地形更直观），提供图层切换按钮。

---

## Phase 7 —— 数据同步

**默认**：`localStorage`（95% 场景够用）。

**跨设备方案**（按难度从易到难）：

| 方案 | 成本 | 适合 |
|------|------|------|
| A. localStorage | 0 | 一人出行 |
| B. GitHub Gist | 0（需 GitHub） | 有技术背景 |
| C. JSONBin.io | 0（1 万次/月） | 两人共享 |
| D. Cloudflare Workers KV | 0（10 万读/天） | 推荐，零运维 |
| E. 自建 Node 服务 | VPS 费 | 有自己服务器 |

代码模板见 `references/templates/todo-sync.js`。

---

## Phase 8 —— 三链路部署

### 🔴 必须三链路（任一挂了切另一条）

| 链路 | 用途 | 特点 |
|------|------|------|
| **主站**（Cloudflare Pages / Vercel / 自有域名） | 日常使用 | 全球 CDN |
| **镜像站**（备选平台 / CloudBase） | 主站挂时切换 | 不同运营商 |
| **本地 HTML**（手机浏览器直接打开） | 完全离线 | 断网/境外信号差 |

### 部署检查

- URL 加缓存破坏参数 `?v=<yyyymmdd>`
- 微信分享发 URL 不发文件
- 敏感信息脱敏（确认号/信用卡/订单号）
- 菲律宾/东南亚等地测试延迟 + 丢包

---

## ✅ 最终交付物完整文件树

```
<project>/
├── <目的地>行程_v<N>.md          # 行程书（含版本日志 + 话术 + Plan B）
├── <目的地>酒店比价_<日期>.md    # 酒店比价报告
├── index.html                    # 🔴 指挥中心（地图+Todo+同步+进度条）
├── guide.html                    # 🔴 完整攻略详情（Day by Day 时间轴）
├── flight.html                   # 航班卡片页
├── icons/                        # SVG 图标集（Noto 3D + Lucide）
│   ├── plane.svg
│   ├── hotel.svg
│   └── ...
├── <目的地>自驾路线.kml          # 自驾 KML（可选）
└── 部署 URL × 2 + 本地 HTML     # 三链路
```

**交付标准**：
- [ ] 行程书每个 POI 有选择理由 + 避坑提示 + 导航关键词
- [ ] 行程书有 Plan B，精确到替代班次/路线/费用
- [ ] 行程书有实操英文话术（至少覆盖取车/活动沟通/事故处理）
- [ ] 行程书顶部有版本变更日志（每次改动标 WHY）
- [ ] 指挥中心地图有**路线**（不是只有大头针）
- [ ] 指挥中心有里程表 + 一键导航
- [ ] Todo 可勾选 + 进度条 + 沉底动画
- [ ] 三链路部署（主站 + 镜像 + 离线 HTML）
- [ ] 同行者跨设备验证（如启用同步）

---

## 🔴 常见坑（血泪教训）

1. **直接做，不要反复问"要不要我帮你…"** —— 获得基本信息后就推进
2. **小红书距离描述 100% 不可信** —— 必须 Google Maps 实测
3. **坐标不能复用酒店坐标** —— 酒店在马路边，潜点在海里
4. **Plan B 不是装饰** —— 精确到班次/时间/路线/费用，否则就是废话
5. **话术要写原话** —— 用户到异国他乡语言不通，照念即用才是价值
6. **版本日志写 WHY** —— "砍掉 Simala（走那条多开 2.5h，非教徒价值低）"
7. **瓦片别用 OSM 官方** —— file:// 打开会 403，用 Esri/CARTO
8. **单页塞不下** —— 超过 60KB 就分页，指挥中心/详情/航班三页互链
9. **地图行程调整了但忘改路线** —— markers + drawRoute 是独立维护的，必须同步
10. **迭代时旧 data-id 不能改** —— 云同步的 key 靠 id 匹配，改了历史状态全丢

---

## 📚 参考文件

| 文件 | 用途 |
|------|------|
| `references/workflow-checklist.md` | 8 Phase DoD 检查清单 |
| `references/research-prompts.md` | 小红书 / WebSearch 提示词模板 |
| `references/templates/itinerary-template.md` | 行程 Markdown 骨架 |
| `references/templates/index-skeleton.html` | 指挥中心网页骨架 |
| `references/templates/itinerary-page-skeleton.html` | 行程详情页骨架（地图 + marker） |
| `references/templates/patch-trip-page-v2.js` | 🔴 地图路线 + 里程表 + 导航注入器 |
| `references/templates/patch-trip-page.js` | v1 兼容（不含里程表） |
| `references/templates/todo-sync.js` | Todo 同步 JS（5 种后端） |
| `references/cloudflare-workers-sync.md` | Workers KV 同步教程 |
| `references/self-host-sync.md` | 自建 40 行同步教程 |

---

## 🛠️ 关键工具清单

| 工具 | Phase | 用途 |
|------|-------|------|
| 小红书 MCP（npx/Docker/Cookie） | P2 | 中文攻略第一信源 |
| Google Maps（手工 / API） | P2-P4 | 路线验证、坐标提取 |
| WebSearch + WebFetch | P2-P3 | 酒店比价、官网班次、签证 |
| agent-browser | P2-P3 | 反爬严重的 OTA 比价 |
| better-icons skill | P6 | 图标搜索（Noto 3D / Lucide） |
| patch-trip-page-v2.js | P6 | 地图路线 + 里程表一键注入 |
| Leaflet + OSRM（浏览器侧） | P6 | 实时路由 + 缓存 |
| Leaflet.Locate | P6 | 用户到达目的地后实时定位 |
| CloudBase MCP / Cloudflare Pages | P8 | 静态托管部署 |

---

_v2.0 · 2026-04-29. 从 20+ 轮迭代的东南亚自驾环线实战中提炼，覆盖 P1-P8 全流程 + 话术 + 坐标 SOP + 三链路部署。_
