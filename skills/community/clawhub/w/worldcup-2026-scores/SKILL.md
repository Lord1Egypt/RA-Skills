---
name: worldcup-2026-scores
description: 一键部署2026世界杯实时比分系统，双数据源（worldcup26.ir + 直播吧），免API Key，纯前端+Node.js
agent_created: true
---

# 2026世界杯实时比分系统

一键部署一个完整的**2026世界杯实时比分网站**，包含：实时比分、赛程赛果、积分榜、球队阵容（含球员头像+中文名+FIFA排名）、比赛详情（首发阵容、事件、技术统计）。

## 核心特性

| 特性 | 说明 |
|:-----|:------|
| ⚡ 实时比分 | 比赛中自动刷新比分、时间、进球事件 |
| 🆓 完全免费 | 无需任何API Key，数据源均为免费开放API |
| 🏗️ 双数据源 | worldcup26.ir（赛程/积分榜）+ 直播吧（实时数据/阵容/统计） |
| 🇨🇳 中文 | 完整的中文球队名、球员名、分组信息 |
| 🖼️ 球员头像 | 48支球队全部球员头像 + 射手榜球员照片 |
| 🏆 FIFA排名 | 球队阵容页显示FIFA世界排名 |
| ⚽ 射手榜 | Top 20射手（含照片+国旗+国家名）|
| 📊 技术统计 | 控球率、射门、角球+赛事统计卡片 |
| 🏳️ 国旗 | 积分榜+射手榜显示国旗 |
| 📱 响应式 | PC和手机均可 |

## 技术栈

- **后端**: Node.js + Express
- **前端**: 原生JS + CSS3（无框架依赖）
- **数据**: worldcup26.ir（主赛程）+ 直播吧API（实时数据）

## 用法

用户说"帮我部署2026世界杯实时比分系统"，或者直接运行此Skill即可。

---

## 安装与部署

### 前置条件

- Linux/macOS 服务器（Windows 需要 WSL）
- Node.js >= 18（推荐 v22）
- Git

### 一键部署

```bash
# 1. 克隆仓库
git clone https://github.com/liuboacean/WorldCup-2026.git worldcup-app
cd worldcup-app

# 2. 安装依赖
npm install

# 3. 创建必要目录
mkdir -p data/matches cache

# 4. 创建球队ID映射（从直播吧发现配置）
# 在 config/ 目录创建 teamIdMapping.json
```

### 启动

```bash
# 开发模式（前台）
node server.js

# 生产模式（后台守护）
nohup node server.js > server.log 2>&1 &
```

访问 `http://你的服务器IP:3001` 即可使用。

---

## 数据架构

### 双数据源策略

```
┌─────────────────────────────────────────────────────────┐
│                   用户浏览器                              │
│  main.js(matches) │ modal.js(detail) │ squad.js(阵容)    │
└──────┬──────────────────────┬────────────────────────────┘
       │                      │
┌──────▼──────────────┐ ┌────▼────────────────────────────┐
│  GET /api/matches   │ │  GET /api/matches/:id           │
│  GET /api/standings │ │  GET /api/matches/:id/lineups   │
│  GET /api/teams     │ │  GET /api/matches/:id/events    │
│  GET /api/rankings  │ │  GET /api/matches/:id/stats     │
└──────┬──────────────┘ └────┬────────────────────────────┘
       │                      │
┌──────▼──────────────┐ ┌────▼────────────────────────────┐
│  dataFetcher.js     │ │  zhiboFetcher.js                │
│  worldcup26.ir      │ │  直播吧(qiumibao.com)            │
│  定时轮询(5分钟)     │ │  按需拉取(60s缓存)               │
│  静态数据+比赛列表   │ │  实时比分+阵容+事件+统计          │
└─────────────────────┘ └─────────────────────────────────┘
```

### 数据源详情

| 数据源 | 基URL | 用途 | 限制 |
|:-------|:------|:-----|:-----|
| **worldcup26.ir** | `https://worldcup26.ir` | 赛程列表、积分榜、球队/球场基础信息 | 比赛中不更新，赛后更新 |
| **直播吧(qiumibao)** | `https://s.qiumibao.com` / `https://dc.qiumibao.com` / `https://bifen4m.qiumibao.com` | 实时比分、比赛事件、首发阵容、技术统计、战报 | 无限制 |

### API端点

| 端点 | 功能 | 数据源 |
|:-----|:-----|:-------|
| `GET /api/matches` | 全部比赛列表（含实时比分增强） | worldcup26.ir + zhibo8 |
| `GET /api/matches/:id` | 单场比赛详情 | worldcup26.ir + zhibo8 |
| `GET /api/matches/:id/lineups` | 首发阵容 | 【zhibo8】 |
| `GET /api/matches/:id/events` | 比赛事件 | 【zhibo8】 |
| `GET /api/matches/:id/stats` | 技术统计 | 【zhibo8】 |
| `GET /api/standings` | 小组积分榜 | worldcup26.ir |
| `GET /api/teams` | 球队列表（含FIFA排名） | 本地静态数据 |
| `GET /api/teams/:id/squad` | 球队阵容（球员头像+中文名） | 本地+fifa数据 |
| `GET /api/rankings` | FIFA世界排名 | 本地静态数据 |

---

## 实现细节

### 目录结构

```
worldcup-app/
├── server.js              # Express 主入口
├── package.json           # 依赖配置
├── services/
│   ├── dataFetcher.js     # worldcup26.ir 定时轮询（主数据）
│   ├── dataFetcherAlt.js  # 比赛增强（事件/统计合并）
│   ├── zhiboFetcher.js    # 直播吧API服务（实时数据）
│   ├── squadFetcher.js    # 球队阵容（FIFA球员数据）
│   └── dataRelay.js       # 数据中继（HE注入）
├── routes/
│   └── api.js             # 全部 REST API 路由
├── public/
│   ├── index.html         # 首页
│   ├── css/               # 样式文件
│   └── js/
│       ├── main.js        # 主页逻辑（比赛列表渲染）
│       ├── modal.js       # 比赛详情弹窗
│       ├── standings.js   # 积分榜渲染
│       ├── squad.js       # 球队阵容弹窗
│       └── filters.js     # 筛选功能
├── static/                # 静态基础数据（git跟踪）
│   ├── static_teams.json      # 48支球队数据
│   ├── static_stadiums.json   # 16座球场数据
│   ├── static_groups.json     # 12个小组积分榜
│   └── static_rankings.json   # 48队FIFA排名
├── config/
│   └── teamIdMapping.json # 直播吧ID ↔ worldcup26.ir ID 映射
├── data/
│   ├── fifaSquadData.json # 48队球员阵容（含头像、中文名）
│   └── zhibo_mapping.json # worldcup26.ir → 直播吧 matchId
└── cache/                 # 运行时缓存（自动生成）
```

### 关键实现说明

#### 1. 实时比分增强（路由层）
`routes/api.js` 的 `/api/matches` 路由会检查每场比赛的状态：
- 已结束 → 直接返回原始数据
- 未开始且开赛时间 > 1小时 → 跳过
- 进行中或即将开始 → 从zhibo8拉取实时比分，30秒缓存

#### 2. 比赛详情（数据合并）
`dataFetcherAlt.js` 的 `getMatchEnhanced()` 合并两个数据源：
- 从 worldcup26.ir 获取基础比赛数据
- 从 zhibo8 获取实时比分、事件、阵容、统计
- 对进球事件进行±2分钟模糊去重（`isNearExistingGoal()`）

#### 3. 首发阵容（主客队识别）
`zhiboFetcher.js` 的 `transformLineups()` 使用双重判断：
- 优先用 `liveScoreData.left.id` 匹配
- 后备用 `lineupRaw.info[teamId].court === 'home'`

#### 4. 时区转换
`dataFetcher.js` 的 `localToBeijing()` 按16座球场所在时区分别转换：
- 墨西哥3座: UTC-6
- 美国东部4座: UTC-4  
- 美国中部3座: UTC-5
- 美加西部4座: UTC-7

#### 5. 球队阵容
`services/squadFetcher.js` ：
- 优先从 `data/fifaSquadData.json` 读取（包含球员头像、中文名）
- 查询 FIFA 排名（从 `/api/rankings` 获取）
- `getSquad()` 中自动应用 `PLAYER_NAME_ZH` 映射添加中文名

#### 6. 首页实时比分
- `enhanceLiveMatches()` 异步为进行中比赛拉取zhibo8实时比分
- 比分、状态、比赛时间（如"32′18″"）实时更新到比赛卡片
- 30秒缓存避免频繁API调用

---

## 常见问题排查

### 国旗不显示
检查 `static/static_teams.json`，确保所有48支球队的 `flag` 字段不为空。`dataFetcher.js` 已改为从本地静态文件加载，不会在轮询中被覆盖。

### 比赛时间不对
确认球场ID对应的时区在 `localToBeijing()` 中正确配置。

### 首发阵容缺一支队
检查 `zhiboFetcher.js` 中 `transformLineups()` 的主客队判断逻辑。可能原因：直播吧API未返回该队阵容，或 `lineupRaw.info` 字段未正确使用。

### 球员无头像
- 对大部分球队，头像已内置在 `data/fifaSquadData.json` 中
- 小部分球队（如波黑、刚果）因API-Football无数据无法提供
- 运行 `scripts/fetch_player_photos.py`（如存在）可批量补充

### 球员无中文名
`services/squadFetcher.js` 中的 `PLAYER_NAME_ZH` 映射表需补充新增球员。

---

## 维护

### 定时任务
`dataFetcher.js` 内置定时轮询：
- 比赛日: 每5分钟
- 非比赛日: 每30分钟

### gitignore 说明
- `data/` 目录（运行时缓存、阵容数据）不在git跟踪中
- `cache/` 目录（运行时缓存）不在git跟踪中
- `static/` 目录中的JSON文件被git跟踪（基础数据）

### 数据备份
修改 `data/fifaSquadData.json` 前建议先备份。阵容数据包含HE注入的球员信息，覆盖可能丢失数据。
