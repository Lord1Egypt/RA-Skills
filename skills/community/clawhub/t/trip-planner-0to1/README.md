# trip-planner-0to1

> 从 0 到 1 制作一份完整的自由行出行攻略 Skill — 端到端，开箱即用。

## 🎯 能做什么

一次完整的旅行规划，涵盖：

- **需求澄清** → 问清硬约束、预算、偏好
- **多源调研** → 小红书 MCP（外网开源版）+ 地图 API + WebSearch
- **方案决策** → 住宿 / 交通 / 一日游 / 餐厅四大决策
- **行程书** → 逐日 Markdown，含 Plan B + 费用明细
- **交互式指挥页** → Leaflet 地图 + Todo 勾选沉底 + 进度条
- **数据同步** → localStorage 兜底 + 可选 Gist / JSONBin / Cloudflare Workers
- **部署上线** → Cloudflare Pages / Vercel / Netlify / GitHub Pages 任选

## 🚀 快速上手

在 AI 对话里直接说：

- "帮我做一份 XX 目的地的自由行攻略"
- "XX 旅行规划，X 天 X 晚"
- "XX 出行 Todo 清单"

AI 会自动加载本 Skill 并按 8 个 Phase 推进。

## 📂 目录结构

```
trip-planner-0to1/
├── SKILL.md                        # 主文件，定义触发词和工作流
├── README.md                       # 你正在看的这个
└── references/
    ├── workflow-checklist.md       # 8 Phase 详细检查清单
    ├── research-prompts.md         # 调研提示词模板库
    ├── cloudflare-workers-sync.md  # Workers KV 同步服务示例
    ├── self-host-sync.md           # 自建同步服务示例（40 行）
    └── templates/
        ├── itinerary-template.md   # 行程 Markdown 骨架
        ├── index-skeleton.html     # 指挥页 HTML 骨架
        └── todo-sync.js            # Todo 同步完整 JS（三种后端可选）
```

## 🔧 前置依赖

### 必需
- 任何支持 MCP 的 AI 客户端（Claude Code CLI / Cursor / VSCode / Cline / Gemini CLI）

### 推荐安装

**小红书 MCP**（外网开源版，第一信源）：
```bash
# Docker 最简单
docker pull xpzouying/xiaohongshu-mcp
docker compose up -d
# → http://localhost:18060/mcp
```
GitHub 仓库：https://github.com/xpzouying/xiaohongshu-mcp

**地图能力**：推荐安装 `google-maps-api` skill 或自备 API Key。

### 可选
- `km` / `iWiki` 等内部知识库 MCP（企业内部出差场景）
- Cloudflare 账号（如需跨设备云同步）

## ✨ 亮点设计

### Todo 勾选沉底动画
点击勾选 → 220ms 淡出动画 → DOM 移动到列表末端。取消勾选 → 回到"未完成区"末尾。视觉上永远让未完成事项浮在顶部。

### 乐观同步 + 版本戳
- 本地 localStorage 立即写 → 界面 0 延迟
- 600ms debounce 后上传云端
- 加载时 `remoteTs > localTs` 才覆盖，避免回写旧数据

### 多攻略天然隔离
每次旅行换一个 `roomId`，localStorage key 自动按 roomId 前缀隔离。同一浏览器可同时打开多个攻略页互不污染。

### 同步方案可插拔
`todo-sync.js` 抽象出 `SyncBackend` 接口，默认 localStorage，可一行切换到 Gist / JSONBin / Cloudflare Workers / 自建服务。

## 📌 维护建议

- 每次旅行结束后，把**独特经验**（新开的酒店、被坑的雷点、靠谱渡轮线路）沉淀成 markdown 片段
- 新目的地模板可以追加到 `references/templates/`
- 同步方案踩坑记录可追加到 `references/` 下对应文件

## 🔗 相关资源

- 小红书 MCP 开源版：https://github.com/xpzouying/xiaohongshu-mcp
- Leaflet.js：https://leafletjs.com/
- Lucide 图标：https://lucide.dev/
- Cloudflare Workers：https://developers.cloudflare.com/workers/
- JSONBin.io：https://jsonbin.io/

## 📄 License

MIT

---

_Built 2026-04-24. Inspired by a real Southeast Asia self-driving trip._
