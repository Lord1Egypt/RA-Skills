---
name: trip-planner-0to1
description: 从 0 到 1 制作一份完整的自由行出行攻略，覆盖需求采集、多源资源调研（小红书 MCP + 地图 + Web 搜索）、方案决策、Markdown 行程书产出、交互式 Todo 网页（本地存储 + 可选云端同步）、一键部署到静态托管的端到端工作流。适用于东南亚海岛、日本、欧洲自驾、美洲公路旅行等任何自由行场景。触发词：出行攻略、行程规划、自由行、做攻略、旅游计划、travel plan、itinerary、行程单、Todo 清单、旅行规划、路线规划、trip planning、旅行攻略。
---

# Trip Planner 0→1 —— 自由行攻略端到端工作流

把一次出行攻略从「一张机票 + 模糊的目的地」做到「结构化行程书 + 可勾选的 Todo 网页 + 跨设备同步」，全流程标准化、可复用。

---

## 🎯 适用场景

- 用户抛出一个目的地（"五一去冲绳"、"十一带孩子去日本"），希望系统化规划
- 已有部分预订（机票/酒店），需要补齐剩余一切
- 需要和同行者（配偶/朋友）跨设备共享待办
- 攻略不仅是文档，还要有可交互的"作战指挥页"

## 📋 工作流总览（8 个 Phase）

```
Phase 1  需求澄清     → 时间/人数/预算/硬需求/风格偏好
Phase 2  资源调研     → 小红书 MCP + 地图 + Web 搜索
Phase 3  方案决策     → 住宿/交通/一日游/餐厅 四大决策
Phase 4  行程书草稿   → Markdown 逐日行程 + Plan B
Phase 5  Todo 清单    → 紧急/次紧急/已完成 三段 + 装备
Phase 6  交互式网页   → index.html（Leaflet 地图 + Todo + 进度条）
Phase 7  数据同步     → localStorage 兜底 + 可选云端同步
Phase 8  部署 & 预览  → 本地预览 / 静态托管 / 公网分享
```

---

## Phase 1 —— 需求澄清（必问清单）

**不要自己脑补，缺信息就直接问。**

1. **硬约束**：往返航班是否已定？日期、机场、行李额？
2. **人数 & 关系**：几人？夫妻/亲子/朋友团？
3. **预算**：人均总预算或每晚住宿上限
4. **强需求**：有没有"必须做"的项目？（潜水/看极光/吃米其林…）
5. **风格偏好**：自驾 vs 公共交通？酒店 vs 民宿？深度 vs 打卡？
6. **同行者会籍**：IHG/Marriott/Hilton/GHA 等会员权益
7. **作息偏好**：早鸟 vs 夜猫，决定每日第一个行程的起始时间
8. **共享房间 ID**（如启用云端同步）：`<destination>-<user1>-<user2>`，全小写用 `-` 分隔

---

## Phase 2 —— 资源调研（多源并行）

### 2.1 小红书 MCP（`xiaohongshu` server）

**推荐作为第一信源**，中文攻略帖的"避坑信息"密度远高于 Google。

**安装**（开源版 `xpzouying/xiaohongshu-mcp`，GitHub 13k+ star）：

```bash
# 方式 A：Docker（最简单）
docker pull xpzouying/xiaohongshu-mcp
wget https://raw.githubusercontent.com/xpzouying/xiaohongshu-mcp/main/docker/docker-compose.yml
docker compose up -d
# 默认暴露 http://localhost:18060/mcp

# 方式 B：二进制
# macOS Apple Silicon 下载：
# https://github.com/xpzouying/xiaohongshu-mcp/releases → xiaohongshu-login-darwin-arm64
# 先运行 login 工具扫码登录，再运行主程序
./xiaohongshu-login-darwin-arm64
./xiaohongshu-mcp-darwin-arm64
```

**MCP 配置**（写入 AI 客户端的 mcp.json / settings）：

```json
{
  "mcpServers": {
    "xiaohongshu": {
      "url": "http://localhost:18060/mcp",
      "description": "小红书内容检索与发布"
    }
  }
}
```

**常用工具**：

| 工具 | 用途 |
|------|------|
| `search_feeds` | 搜"XX目的地攻略"、"XX踩坑"等长尾词 |
| `get_feed_detail` | 拿到笔记正文 + 评论区（评论才是金矿！） |
| `list_feeds` | 首页刷热门帖 |
| `user_profile` | 深挖专业博主的历史笔记 |

**搜索关键词模板**：
- `<目的地> 避坑`
- `<目的地> 最新攻略 <年份>`
- `<目的地> <月份> 天气`
- `<目的地> 防宰`
- `<目的地> 物价`
- `<景点名> 值不值得去`

**陷阱识别**：90% "精品一日游"帖子是商业推广，看评论区 + 发帖时间筛真实内容。详细筛选标准见 `references/research-prompts.md`。

### 2.2 地图 API

查**实际行车距离和时间**，不要信小红书文字描述。可选工具：

| 工具 | 特点 |
|------|------|
| Google Maps API（`google-maps-api` skill） | 全球覆盖，数据权威，需 API Key |
| 高德 / 百度 Maps API | 国内数据更准 |
| OpenStreetMap Nominatim | 免费无 Key，但覆盖与准确性一般 |
| `gmaps.to` / `maps.app.goo.gl` 手工比对 | 快速验证两点时间 |

**经验**：默认路线可能非最快，手工对比至少 2 条备选路线。山区/岛屿尤其明显（海岸线绕远反而比内陆快）。

### 2.3 Web Search + WebFetch

- 酒店比价：同时查 Agoda / Booking / Kayak / 官网 / Trip.com，列成**比价表**
- 渡轮/船票：查官网班次，电话/邮箱记录到行程书
- 签证/入境：查外交部官网 + 大使馆公告（**不要**只信小红书）
- 机场接送、SIM 卡、租车：查 Klook / KKday / GetYourGuide

详细提示词模板见 `references/research-prompts.md`。

---

## Phase 3 —— 方案决策（四大块）

按优先级处理，早定早安心：

### 3.1 住宿（决策树）

```
是否有酒店会籍？
├─ 是 → IHG/Marriott/Hilton/GHA 官网直订（升房 + 早餐 + 酒廊）
└─ 否 → Agoda + Booking + Trip.com + Kayak 四方比价
            └─ 含早？免费停车？步行到景点？取消政策？
```

**产出**：`<目的地>酒店比价_<日期>.md` 对比表格，金额同时标本币 + CNY。

### 3.2 交通（自驾 vs 公共）

- **自驾** → 选车（Klook / Rentalcars / 本地租车行）+ **保险**（第三方保险公司单独买通常比租车行附加便宜）+ 国际驾照
- **公共** → 画**交通方案图**，时间戳对齐每段，给足换乘 buffer（≥20min）

### 3.3 一日游 / 体验项目

- 优先级：**官网直订** > Klook > 民宿代订 > 码头现场
- 明确版本：`self-drive, meet at jump-off` vs `with hotel pickup` —— 能省不少钱
- 提前查**配额制**项目（船潜、鲸鲨、跳伞）是否要预先锁名额

### 3.4 餐厅清单

- 每天午/晚餐各候选 2 家，一家主选一家 Plan B
- 查 Google Maps 评分 ≥4.3 + 评论数 ≥300，并扫一眼差评辨水军

---

## Phase 4 —— 行程书 Markdown

文件名：`<目的地><出行方式>行程_v<N>_<日期>.md`

**骨架参考**：`references/templates/itinerary-template.md`

关键段落：
1. **封面摘要**：日期、航班、人数、预算总览
2. **Day by Day**：每天一个 H2，含 **时间/地点/动作/费用** 四列
3. **住宿清单表**：N 晚酒店 + 入住/退房时间 + 金额 + 确认号
4. **交通清单**：航班/渡轮/租车，带确认号/订单号
5. **备选方案 / Plan B**：每个关键节点都要有备胎
6. **费用明细**：按付款人拆分
7. **应急联系**：使领馆、保险、租车紧急电话

---

## Phase 5 —— Todo 清单结构化

Todo 分**三段**（顺序有讲究）：

```
紧急 (urgent)      → 需要 1-3 天内处理的（订酒店/锁名额/买行李额）
次紧急 (important) → 出发前搞定即可（下载保单/买防晒/买转换插头）
已完成 (done)      → 已预订/已购买的，作为"备忘证据"不删除
```

**每条 Todo 必须有**：
- 主标题（动词 + 对象）：如 `买当地 SIM 卡`
- 副说明 `<small>`：**具体去哪买、多少钱、对应哪条行李**
- 紧急标签（仅 urgent 段）
- 图标（Lucide / Heroicons）
- `data-id` 唯一（`u0`-`uN` / `i0`-`iN` / `d0`-`dN` 分段命名）

**装备清单 / 行李清单**单独一个 `<ul id="todoPack">`，便于出发前最后核对。

---

## Phase 6 —— 交互式网页（index.html）

**模板**：`references/templates/index-skeleton.html`

核心能力：
- **顶部进度条**：`N / 总数`、百分比、渐变条
- **地图**：Leaflet + OpenStreetMap（免费无 Key），标出住宿/景点/餐厅/机场，点击弹出信息
- **Todo 勾选**：点击切换 done，**done 自动沉底**（`flying` 动画 → DocumentFragment 重排）
- **同步徽章**：右下角小圆点 + 文字 `已保存` / `已同步到云端` / `离线`
- **暗色主题**：低亮屏下不刺眼，户外强光下也清晰

关键 CSS（Todo 沉底动画）：
```css
.todo-item {
  transition: background .2s, opacity .3s, transform .3s;
  /* ⚠️ 不要用 transition: all，会让 hover 卡顿 */
}
.todo-item.flying { opacity: 0.35; transform: scale(0.98); }
```

关键 JS（勾选沉底）：
```js
todoItems.forEach(item => {
  item.addEventListener('click', () => {
    const willBeDone = !item.classList.contains('done');
    item.classList.toggle('done');
    saveTodos();
    const ul = item.parentElement;
    if (willBeDone) {
      item.classList.add('flying');
      setTimeout(() => { ul.appendChild(item); item.classList.remove('flying'); }, 220);
    } else {
      const firstDone = ul.querySelector('.todo-item.done');
      item.classList.add('flying');
      setTimeout(() => {
        if (firstDone && firstDone !== item) ul.insertBefore(item, firstDone);
        else ul.appendChild(item);
        item.classList.remove('flying');
      }, 180);
    }
  });
});
```

完整可拷贝代码：`references/templates/todo-sync.js`。

---

## Phase 7 —— 数据同步

**默认策略（0 服务器成本）**：`localStorage` + URL 分享，够 95% 场景用。

**跨设备同步可选方案**（按集成难度从易到难）：

### 方案 A：localStorage 本地存储（默认）
- 所有勾选状态存浏览器本地
- 无服务端、无账号、无限制
- **局限**：不同设备状态独立

### 方案 B：GitHub Gist（零服务器，需 GitHub 账号）
- 把勾选状态 POST 到一个 public Gist
- 用 Personal Access Token（只需 `gist` 权限）
- 代码模板见 `references/templates/todo-sync.js` 的 Gist 变体

### 方案 C：JSONBin.io / jsonbin.io（零服务器，免费 1 万次/月）
- 注册后拿 X-Master-Key
- REST API 非常简单：`GET /b/<binId>` + `PUT /b/<binId>`
- 代码模板见 `references/templates/todo-sync.js`

### 方案 D：自建轻量同步服务
- 任何能跑 Node / Python / Go 的 VPS
- 40 行代码搞定（示例见 `references/self-host-sync.md`）
- 推荐配 Cloudflare Tunnel / Cloudflare Workers，免公网暴露

### 方案 E：Cloudflare Workers KV（推荐，零运维）
- 免费额度：10 万次读 + 1 千次写/天
- 浏览器直调 Workers URL，无 CORS 烦恼
- 示例代码见 `references/cloudflare-workers-sync.md`

**选型建议**：

| 场景 | 推荐 |
|------|------|
| 一个人出行 | A（localStorage） |
| 两人共享，不想折腾 | C（JSONBin.io） |
| 已有 GitHub 账号 | B（Gist） |
| 有 Cloudflare 账号 + 想免运维 | E（Workers KV） |
| 有自己的 VPS | D（自建） |

---

## Phase 8 —— 部署 & 预览

### 8.1 本地预览
```bash
# 原生 Python 临时 server
python3 -m http.server 8000
# 或 Node
npx serve .
```

### 8.2 静态托管（推荐平台）

| 平台 | 特点 | 自定义域名 |
|------|------|-----------|
| **Cloudflare Pages** | 免费无限流量，CI/CD 自动部署 | ✅ |
| **Vercel** | Next.js 友好，预览 URL 丰富 | ✅ |
| **Netlify** | 表单 / 函数开箱即用 | ✅ |
| **GitHub Pages** | 公开仓库免费 | ✅ |
| **自己 VPS + nginx** | 完全控制 | ✅ |

### 8.3 分享注意事项

- URL 加**缓存破坏参数**：`?v=20260501`，避免用户看到旧版本
- 微信分享：直接发 URL，**不要**发 HTML 文件（iOS 微信不渲染 HTML 附件）
- 敏感信息脱敏：对外分享的攻略不要暴露酒店确认号、信用卡尾号、订单号等

---

## ✅ 最终交付物检查清单

完整一份攻略应包含：

- [ ] `<slug>行程_v<N>.md` 行程书（必须）
- [ ] `index.html` 指挥页（必须）
- [ ] `icons/` SVG 图标集（可选，Lucide / Heroicons）
- [ ] 酒店比价 md
- [ ] 地图 KML / HTML 路线图（如果自驾）
- [ ] Day by Day 大图指南 / 登机日流程页（可选）
- [ ] 部署 URL + 缓存破坏参数
- [ ] 同行者跨设备访问测试

---

## 🔴 常见坑

1. **直接做，不要反复问"要不要我帮你…"** —— 在获得基本信息后就推进，缺啥再单点问
2. **Todo 动词要对齐行李** —— 用副说明标注"对应行李清单：XX"，否则打包时易漏
3. **动画不要 `transition: all`** —— 改成显式 `transition: background, opacity, transform`，否则 hover 卡顿
4. **DocumentFragment 重排** —— 批量移动 DOM 用 `fragment.appendChild` 避免多次 reflow
5. **同步 key 不要重名** —— 不同攻略用不同 roomId，否则互相覆盖
6. **作息偏好要确认** —— 用户可能是早鸟也可能是夜猫，早于其自然醒时间的活动必须明确标注原因
7. **Plan B 不是装饰** —— 关键节点（跨岛渡轮、鲸鲨配额、跨国航班转乘）必须写备胎
8. **脱敏** —— 对外分享不暴露确认号 / 信用卡尾号 / 订单号等

---

## 📚 参考文件

- `references/workflow-checklist.md` —— 8 个 Phase 的 DoD 检查清单
- `references/research-prompts.md` —— 小红书 / WebSearch 提示词模板库
- `references/templates/itinerary-template.md` —— 行程 Markdown 骨架
- `references/templates/index-skeleton.html` —— 交互式网页骨架
- `references/templates/todo-sync.js` —— Todo 同步完整 JS（含 localStorage / Gist / JSONBin 三种后端）
- `references/cloudflare-workers-sync.md` —— Cloudflare Workers KV 同步服务示例
- `references/self-host-sync.md` —— 自建 40 行同步服务示例

---

_Built 2026-04-24. 沉淀自一次完整的东南亚自由行攻略制作实践。_
