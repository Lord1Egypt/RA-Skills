# Trip Planner 0→1

从一张机票 + 模糊目的地 → 结构化行程书 + 多页作战指挥网站 + 跨设备 Todo 同步 + 三链路部署。

## 快速开始

对话中说"帮我做 XX 出行攻略"或"XX 行程规划"即自动加载本 Skill。

## 前置工具

| 工具 | 必须？ | 安装方式 |
|------|--------|---------|
| 小红书 MCP | 强烈推荐 | `npx xiaohongshu-mcp@latest`（首次扫码登录） |
| Google Maps | 必须 | 浏览器手工查 / `google-maps-api` skill |
| better-icons | 推荐 | `npm i -g better-icons`（图标搜索） |
| Node.js | 推荐 | 跑 `patch-trip-page-v2.js` 注入地图路线 |

## 工作流

```
P1 需求澄清 → P2 多源调研+交叉验证 → P3 方案决策
     ↓                ↑↓                    ↓
P4 行程书+话术 ←→ 迭代循环 ←→ P5 Todo清单
     ↓                                     ↓
P6 多页网页（指挥中心+攻略详情+航班卡片）
     ↓
P7 云端同步 → P8 三链路部署
```

P2-P4 是可回溯的循环。实际项目平均迭代 15-20 轮。

## v2 核心升级（vs v1）

| 维度 | v1 | v2 |
|------|----|----|
| 架构 | 瀑布 8 Phase | 迭代循环 |
| 网页 | 单页 | 多页（指挥+详情+航班） |
| 信息密度 | 框架格式 | 每 POI 含理由+避坑+话术 |
| Plan B | "天气不好改室内" | 精确到班次/路线/费用 |
| 坐标 | 估算/复用 | Google Maps 官方提取+卫星验证 |
| 部署 | 单站 | 三链路（主站+镜像+离线） |
| 交叉验证 | 无 | 每条关键信息 2+ 来源 |
| 话术 | 无 | 取车/活动/事故 SOP |

## 文件结构

```
trip-planner-0to1-public/
├── SKILL.md                    # 主文件（工作流全文）
├── README.md                   # 本文件
└── references/
    ├── workflow-checklist.md    # 逐 Phase DoD 检查清单
    ├── research-prompts.md     # 小红书/Web 搜索提示词模板
    ├── cloudflare-workers-sync.md
    ├── self-host-sync.md
    └── templates/
        ├── itinerary-template.md
        ├── index-skeleton.html
        ├── itinerary-page-skeleton.html
        ├── patch-trip-page-v2.js
        ├── patch-trip-page.js
        └── todo-sync.js
```

## 许可

MIT. 沉淀自 2026 年东南亚自驾环线 + 多次实战迭代。
