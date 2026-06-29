# 2026世界杯实时比分系统 ⚽

一键部署 **2026 FIFA World Cup 实时比分网站**，零费用、零 API Key、纯免费数据源。

## 快速开始

在 WorkBuddy 中直接运行 Skill：

```
worldcup-2026-scores
```

或手动部署：

```bash
git clone https://github.com/liuboacean/WorldCup-2026.git
cd WorldCup-2026
npm install
node server.js
```

访问 `http://localhost:3001` 即可。

## 功能特性

| 特性 | 说明 |
|:-----|:------|
| ⚡ 实时比分 | 比赛中自动刷新比分、时间、进球事件 |
| 🆓 完全免费 | 无需任何 API Key |
| 🏗️ 双数据源 | worldcup26.ir（赛程/积分榜）+ 直播吧（实时数据） |
| 🇨🇳 中文 | 完整的中文球队名、球员名 |
| 🖼️ 球员头像 | 48支球队全部球员头像 + 射手榜照片 |
| ⚽ 射手榜 | Top 20 射手（含照片+国旗）|
| 🏆 FIFA排名 | 球队阵容页显示世界排名 |
| 🏳️ 国旗 | 积分榜+射手榜显示国旗 |
| 📊 技术统计 | 控球率、射门、角球 + 赛事统计 |
| 📱 响应式 | PC 和手机均可 |

## 项目架构

```
├── server.js              # Express 入口
├── routes/api.js          # API 路由（比分/积分榜/阵容/射手榜）
├── services/              # 数据服务层
│   ├── dataFetcher.js     # worldcup26.ir 主数据轮询
│   ├── dataFetcherAlt.js  # 直播吧增强数据 + 被取消进球过滤
│   ├── zhiboFetcher.js    # 直播吧数据抓取与缓存
│   └── squadFetcher.js    # 球队阵容数据
├── public/                # 前端静态文件
│   ├── index.html
│   ├── css/style.css
│   └── js/                # main.js, modal.js, squad.js 等
├── static/                # 静态数据（球队/球场/积分榜/排名）
└── data/                  # 运行时数据缓存
```

## 数据源

- **worldcup26.ir** — 赛程、比分、积分榜（免费，主数据源）
- **zhibo8.cc** — 首发阵容、比赛事件、技术统计（免费）
- **FIFA** — 球员头像、世界排名

项目地址：https://github.com/liuboacean/WorldCup-2026
