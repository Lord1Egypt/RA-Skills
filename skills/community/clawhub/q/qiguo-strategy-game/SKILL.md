---
name: qiguo-strategy-game
description: This skill launches the single-file HTML strategy game 七国群雄传 (Seven Kingdoms Tactics), a 三国群英传-style isometric turn-based wargame. Use it when the user wants to play a browser strategy game, mentions 七国群雄传 / 战棋 / 三国群英传-style web game, or asks to open / play this game. It copies the self-contained HTML into the workspace and opens it directly in the built-in preview so the user can play immediately with zero setup.
metadata:
  agent_created: true
---

# 七国群雄传 · 网页战棋（Seven Kingdoms Tactics）

## Overview

A zero-dependency, single-file HTML5 Canvas strategy wargame in the spirit of 三国群英传 — isometric 3D 战棋, seven-warring-states theme, with combo chains, bond auras, co-op ultimate (合击必杀), and a general codex (武将图鉴). Two modes are bundled, and **each supports two play styles**:

- **人机对战 (vs AI)** — default; you command one side, the computer commands the other.
- **双人轮流 Hotseat（同设备）** — two human players share one device and take turns on the same screen. Chosen on the state-select screen via the 👥 双人轮流（同设备） toggle.
- **联机对战 (Net Play)** — two players on **separate tabs / separate devices** play live. Chosen on the state-select screen via the 🌐 联机对战 toggle. Two transports: 本机多标签 (BroadcastChannel, same browser, zero setup) and 跨设备 (WebSocket relay `net-server.js`, two devices). **Both skirmish and campaign support net play**, host = red/我方, client = blue/敌方 (viewpoint swapped on client).

- **战役模式 (Campaign)** — `campaign-mode.html`: pick a state, conquer cities, recruit generals, and unify the realm. Includes the 武将图鉴 collection system. Hotseat **and 联机** apply to each battle (the strategic map stays single-player setup).
- **普通模式 (Skirmish)** — `skirmish-mode.html`: pick a state + scenario, fast single battle. **10 历史名局** (长平/即墨火牛/宜阳/蓟城/桂陵/鄢郢/函谷关/邯郸/伊阙/阏与) each with bespoke terrain & 史实剧情. Hotseat **and 联机** fully supported.

The skill is purely a launcher: it copies the bundled HTML into the current workspace and opens it in the built-in preview panel so the user plays instantly. No server, no build step, no network.

## When To Use

- The user says "玩七国群雄传", "打开战棋游戏", "来一局三国群英传那种游戏", or similar.
- The user references 战棋 / 回合制策略 / 七国群雄传 by name.
- The user wants **two-player / 双人 / 双人对战 / Hotseat / 同设备轮流** — launch either mode and tell them to pick 👥 双人轮流 on the state-select screen.
- The user wants **联机 / 远程双人 / 双设备 / 线上对战 / 一起玩 / 不在一个设备** — launch either mode and tell them to pick 🌐 联机对战, then 创建房间（主机）on one side and 加入房间（客机）with the same room number on the other. Same browser → 本机多标签 (no server); different devices → run `net-server.js` and use 跨设备.
- The user installs the skill and invokes it to play.

## How To Launch (required procedure)

Follow these steps exactly. The game is bundled under `assets/` in this skill's directory.

1. **Resolve the skill directory.** The current skill lives at `~/.workbuddy/skills/qiguo-strategy-game/`. The bundled files are:
   - `assets/campaign-mode.html` — 战役模式
   - `assets/skirmish-mode.html` — 普通模式
   - `net-server.js` — zero-dependency WebSocket relay for 跨设备 联机 (only needed for two-device matches)

2. **Choose which mode to open** based on the user's words:
   - Mentions 战役 / 剧情 / 统一 / campaign / 天下 → `campaign-mode.html`
   - Mentions 普通 / 快速 / 单局 / skirmish / 一局 → `skirmish-mode.html`
   - Mentions 双人 / 双人对战 / Hotseat / 同设备轮流 / 两个人玩 → open either mode (both support Hotseat); tell the user to tap 👥 双人轮流（同设备） on the state-select screen before picking a state.
   - Ambiguous or just "玩这个游戏" → open **both** (present as two files).

   > **Hotseat note:** the 人机 / 双人 toggle lives on the state-select screen (a row reading `对战模式： 🤖 人机对战 · 👥 双人轮流（同设备）`). It is selected *before* choosing a state and applies to the whole battle. In Hotseat, Player 1 commands the blue side and Player 2 the red side; 结束回合 passes control to the other player (not the AI).

3. **Copy the chosen HTML into the current workspace** so the user owns a playable, editable copy. Use the Bash tool:
   ```bash
   mkdir -p "<cwd>/七国群雄传" && cp "<skill_dir>/assets/<file>.html" "<cwd>/七国群雄传/<file>.html"
   ```
   Replace `<cwd>` with the current working directory (from context) and `<skill_dir>` with the resolved skill path. Keep the English filename so the path stays portable.

4. **CRITICAL — open in the built-in preview via present_files.** After copying, call the `present_files` tool with the **absolute path** of the copied HTML file(s). This renders the game directly inside the conversation's preview panel and shows an artifact card.

   - ✅ MUST: `present_files` with the absolute local path, e.g. `C:\Users\...\七国群雄传\campaign-mode.html`
   - ❌ NEVER: only print a `file://...` URL or a relative path and tell the user to open it themselves. The user must be able to play immediately in the preview.

5. **Tell the user, in one short line**, that the game is open in the preview and how to start (choose a state → start battle; in campaign, march from your capital to an adjacent enemy city).

## Game Feature Summary (for describing to the user)

- **连击 Combo**: consecutive friendly hits build a combo counter; at 3+ a 🔥 badge pops; combo ≥5 scales damage up to +30%.
- **羁绊光援 (Bond Aura)**: adjacent friendly units buff each other (ATK +2 / DEF +4), shown as a gold ring under the unit.
- **合击必杀 (Co-op Ultimate)**: when a second different friendly unit hits the same enemy in one turn, a full-screen 合击 triggers with bonus splash damage + screen shake.
- **名将专属必杀 (Signature Ultimate)**: 16 位史实名将会施展贴合人设的专属必杀，取代通用★级必杀——白起·武安君令、王翦·灭国长策、李牧·雁门大捷、田单·火牛烈阵、孙膑·诡道奇谋、乐毅·连横破齐等群体横扫；蒙恬·北逐匈奴、赵奢·阏与之勇直线破阵；甘茂·宜阳苦战、庞涓·魏武卒单体斩将。史实厚度远超三国群英传的通用必杀。
- **武将图鉴 (Codex, campaign only)**: every enemy general faced is recorded (defeated / captured / retreated) into `localStorage`; open via the 图鉴 button, shows "collected / total".
- Controls: click a unit → move/attack; 结束回合 (end turn) passes to the other side (AI in 人机 mode, the other human in 双人 Hotseat); terrain, morale, and formation bonuses apply.
- **3D 地图（v1.4.0 → v1.5.0 沉浸再升级）**：在 v1.3.0 史诗化地基之上，把地图打磨成战棋真正的"亮点与特色"——v1.4.0 已落地①**动态天气层**（雨/雪/雷暴闪电+镜头微震/沙尘暴尘霾，由剧本天气自动驱动）②**战役剧本专属主题**（长平血色黄昏+焦土、即墨暗夜火光、蓟城冰蓝雪原）③**单位与地形互动痕迹**（踩踏/车辙/焦痕，最多 520 处按寿命淡出）④**视差多层远景 + 镜头微震**；**v1.5.0 再叠加**⑤**自适应大气透视**（按地图实际纵深计算：远景朦胧、近景清晰，纵深感拉满）⑥**体积光上帝光晕 + 蓬松积云软投影**⑦**活水焦散微光带 + 镜面太阳反光点**⑧**夜间城堡暖光晕 / 窗光 / 火炬辉光**（成为夜战视觉锚点）⑨**植被随风轻摆 + 飘落叶**⑩**46 颗缓动花粉/尘埃环境粒子**（火/雷主题升起余烬）。所有增强均以"不污染地块本征色"为前提，配色可读性 ΔE 稳定在 22+。实测（Playwright/Chromium 真机）全绿：可读性 ΔE 22.1、大气透视背景Δ39.5/前景Δ0、体积光亮像素比 0.032、活水帧间差 7.49、环境粒子帧差 11、夜间城堡暖色像素 0→27、0 pageerror。

## 上手友好 & 留存设计（Player Retention & Virality）

These hooks keep players coming back and help the game spread — mention them when describing the skill:

- **⚡ 快速开始（Quick Start）**: on the state-select screen, a one-tap button picks a random state and jumps straight into a battle / campaign — zero decision friction. The first launch auto-pops the tutorial so new players learn by playing.
- **AI 难度（Difficulty）**: in 人机 mode, choose 😌 简单 / 🙂 普通 / 😈 困难 (scales enemy troops / stats). Welcomes beginners and challenges veterans.
- **📖 玩法说明（Tutorial）**: both battle and strategy screens have a 📖 button that opens a rules cheat-sheet anytime (unit counters, 军师技, net play…).
- **📋 战绩分享（Share Battle Report）**: every end-of-battle banner has 「复制战绩」 — one tap generates a shareable battle-report text, ready to paste into WeChat groups / Moments for social virality.
- **🏆 成就系统 + 📖 武将图鉴（Campaign）**: cumulative wins unlock achievements and collect the realm's famous generals, giving long-term goals and a reason to return.
- **🏆 战绩记录（Best Records）**: per-scenario fastest-clear turns are saved locally and flagged as a new record on the win banner.
- **🔥 每日登录连签（Daily Streak）**: the game tracks consecutive-day logins in `localStorage` and toasts `连续登录 N 天：每日一战，终将一统天下！` on launch — a lightweight daily-return hook that rewards habitual play without gating content.

## Hotseat 双人轮流（同设备）— how it works

- On the state-select screen, tap **👥 双人轮流（同设备）** (default is 🤖 人机对战). This sets `gameMode='hotseat'`.
- Player 1 = blue side (你/玩家1 · 国名), Player 2 = red side (敌军/玩家2 · 国名). The active side is shown by the turn pill (e.g. `玩家1 · 秦 行动`) and the status bar (`玩家1` / `玩家2` counts, current side's 阵型 and 军师).
- Each side gets its own 阵型 and a random 军师技 per turn (the 阵型 selector and 军师技 dropdown switch to the active side automatically). The 结束回合 button reads `玩家2 结束回合 ▶` when it is Player 2's turn.
- Win banner shows `🏆 玩家1 · 秦 胜利！` / `🏆 玩家2 · 赵 胜利！` so both humans get credit.
- **Campaign caveat:** only the tactical battle is Hotseat; the overland strategy map (choose state, march cities, recruit) remains single-player setup — this is by design, since the map reacts to one player's moves.

## 联机对战 (Net Play) — how it works

On the state-select screen, tap **🌐 联机对战** (default 🤖 人机对战). A room row appears with a room number, a transport toggle (本机多标签 / 跨设备), an optional server box, and 创建房间（主机）/ 加入房间（客机）buttons.

**Two transports**
- **本机多标签 (BroadcastChannel)** — zero setup. Two tabs in the *same browser* join the same room number and play live. No server, no network.
- **跨设备 (WebSocket relay)** — two devices (or two different browsers) join the same room through a tiny zero-dependency relay server. Bundled as `net-server.js` in this skill's directory. Start it with `node net-server.js` (default port 8770) on a machine reachable by both players; both enter `ws://<host-ip>:8770` in the 服务器 box before joining.

**Match flow**
1. Host taps 创建房间（主机）and picks a state (campaign) / state+scenario (skirmish), then starts the battle.
2. Client taps 加入房间（客机）with the **same room number**. The client's 选国 modal closes automatically and a "等待主机开始战斗" overlay shows until the host launches the battle.
3. When the host starts, the full state is pushed to the client; both see the same board. The client's viewpoint is swapped (commands the blue/敌方 side, shown as 我方).

**Rules**
- Host is authoritative: the client only *sends* actions (move / attack / 军师技 / 武将技 / 结束回合); the host rebroadcasts the full state each turn. Latency is negligible at this scale.
- Turn pill reads `🟢 你方回合（红方）` / `⏳ 等待对方（蓝方）` so each side knows when to act.
- A 断线 / 服务器未启动 message appears if the WS relay is unreachable — start `net-server.js` first.

**Note:** in campaign net play, only the tactical battle is networked (host plays the strategy map; the client joins the battle the host launches). This is by design.

## Notes

- Both HTML files are fully self-contained (all CSS/JS inline, no external requests). Safe to open offline.
- If the user wants to tweak the game, they edit their copied file in the workspace — the bundled asset stays untouched.
- To add a new mode or balance change, edit the asset HTML, then re-run this skill's launch procedure.

## 更新日志 (Changelog)

### v1.4.0 · 地图沉浸四大增强（天气 / 主题 / 痕迹 / 视差微震）
- **动态天气层**：新增 `drawWeather()` 粒子系统——下雨/下雪斜线飘落、雷暴随机闪电（白屏 + 折线）+ 命中触发镜头微震、大风/沙尘暴横向尘霾飘移；天气类型由既有 `weather` 全局（剧本天气）自动驱动，无需额外操作即随战场气候呈现对应天象。
- **战役剧本专属主题**：新增 `THEME_BY_SCENARIO` 与 `GAME_THEME`——长平之战（血色黄昏天空 + 焦土红偏色）、即墨火牛（暗夜 + 营地底部火光闪烁）、蓟城死守（冰蓝雪原偏色）等，开战时按 `scenario.name` 自动套用天空渐变 / 太阳光晕 / 雾色 / 地表 tint，并强化夜战暗角。
- **单位与地形互动痕迹**：新增 `GAME_TRACES` + `addTrace()` + `drawTileTraces()`——单位移动在草地/丘陵/平原烙下**踩踏痕**、攻城/车系武将攻击留下**车辙**、灼烧产生**焦黑痕**（带余烬），最多 520 处并按寿命淡出；由移动（D 钩子）、命中/车辙（C 钩子）、灼烧（E 钩子）自动写入。
- **视差多层远景 + 镜头微震**：`drawWorldBackdrop` 远山/云/鸟随 `cam.panX` 按 0.06%~0.42% 不同速率视差位移营造纵深；`render` 顶部按 `cam.shake` 做随机平移、命中/雷暴衰减触发微震（A 钩子），渲染末尾配对 `ctx.restore()`。
- **发布**：Playwright/Chromium 真机全绿（双文件 0 pageerror），回归地形视觉指标（ΔE/σ/河流/丰富度）保持 v1.3.0 水平不退化。

### v1.5.0 · 地图沉浸再升级（大气透视 / 体积光 / 活水焦散 / 夜城辉光 / 植被摆动 / 环境粒子）
- **自适应大气透视 `drawDepthFog`**：按地图实际屏幕纵向范围（minY/maxY）计算每格雾化强度——远景（上方）浓、近景（下方）淡，背景Δ≈39.5、前景Δ≈0，纵深感拉满且不压暗近处信息；雾色随 `THEME.fog` 走，主题切换自动适配。
- **体积光上帝光晕 + 蓬松积云软投影 `drawGodRays` / 新云层**：太阳处 7 道放射状线性渐变光（lighter 叠加），顶部亮像素比升至 0.032；云由单层改为 puffs 数组的蓬松积云 + 软投影（0.12 视差），云影随光位漂移。
- **活水再升级 `decoWater`**：在 v1.3.0 径向渐变/波光/拍岸浪之上，新增 3 条 `lighter` 焦散微光带 + 镜面太阳反光点（椭圆高光），活水帧间差 7.49。
- **夜间城堡辉光 `decoCastle`**：火/夜主题下城体加暖色径向光晕、四角楼窗光（闪烁）、双层火炬火焰、主楼窗光 + 暖色描边，夜战暖色像素由 0 升至 27，城堡成为暗夜视觉锚点。
- **植被随风轻摆 + 飘落叶 `decoForest`**：每棵树 `translate/rotate` 随风轻摆，3 片秋/绿飘落叶缓降，告别"死板绿钉"。
- **环境粒子 `drawAmbient`**：46 颗缓动花粉/尘埃（lighter 微光）漂浮；火/雷暴主题额外升起 26 颗余烬，氛围更"活"。
- **可读性硬约束守卫**：所有新视觉层均"不污染地块本征色"——沼泽/桥梁因装饰撞色（ΔE 一度跌至 15.4）已修复（沼泽中心改黄绿、桥梁改深棕，三者拉开），8 地形最小 ΔE 回升至 20.1~20.5（≥18），纯地块底色可读性 22.1；新增 `GAME_NO_DECO / GAME_NO_DEPTHFOG / GAME_NO_AMBIENT` 测试隔离开关隔离瞬态层测量。
- **发布**：Playwright/Chromium 真机全绿（双文件 0 pageerror）；v15_verify（可读性/大气透视/体积光/活水/环境粒子/夜城辉光/微噪声）ALL PASS；terrain_visual_verify2 与 v14_verify 回归 ALL PASS，零退化。

### v1.3.0 · 3D 地图史诗化美化（成为战棋亮点）
- **山脉史诗化**：山体由直线三角改为**曲线山体**，受光/背光二分 + 岩层横向条纹；雪冠改为**柔和白→冷蓝渐变**（非生硬锯齿）；峰间加**云絮**飘绕；基座加**碎石坡**（散布受光/背光双色碎石）。多峰按相邻山地数**连脉缩放**，形成山脉群。
- **河流"活水"升级**：水深由单一色改为**径向渐变**（中部亮、边缘深，呈现水深感）；流动波纹顶端加**泡沫冠**白点；新增**波光闪点**随机闪烁；与陆地交界处绘制明暗起伏的**拍岸浪**白线；实测帧间差 11.4（≥3）。
- **森林物种多样化**：松树（三层锥形）与**阔叶树**（三层椭圆冠）混交；按确定性随机注入**秋色红叶**；偶发**倒木**；林下加**斑驳光影**，告别"清一色绿钉"。
- **城堡要塞化**：由单体小城堡升级为**要塞**——等距菱形**城墙** + 前缘**城垛** + **门洞** + **四角楼**（锥顶 + 小旗）+ 中央**主楼**（锥顶 + 主旗）+ **炊烟**动画，多旗飘动，成为地图视觉锚点。
- **丘陵/平原/沼泽细节**：丘陵加草簇/小花/碎石与高光脊；平原加小花（红/黄/白/橙）+ 碎石；沼泽加**睡莲**（绿盘缺口）+ 芦苇丛 + 水洼反光 + 枯木冒泡，质感更"湿润腥臭"。
- **天空与大气沉浸式**：渐变天 + **太阳光晕 + 射线** + **漂移云**（随时间横移）+ **四层远山**雾霭 + **飞鸟**剪影 + **低空薄雾**（漂移）+ **电影暗角**，整体从"扁平底色"升级为可入画的风景。
- **配色余量加固**：在 v1.2.0 基础上把沼泽由暗橄榄绿微调为**浊黄褐**，进一步拉开与森林绿的差距，最小色差 ΔE 稳定在 21+，确保 8 地形一眼可辨。
- **真机验证（双文件全绿）**：几何面积比 1.000/重叠率 0；最小 ΔE 21.6（skirmish）/21.0（campaign）；最小纹理 σ 9.54；河流帧间差 11.44；侧壁方向差 21.9、AO 变暗 5.8~7.5；柱体命中 3/3；悬停白像素 128；图例开关 OK；**细节丰富度（边缘梯度）** plain 12.9 / forest 10.6 / hill 10.5 / mountain 14.9 / river 14.8 / swamp 8.8 / castle 25.9 / bridge 9.9。12 回合 skirmish 冒烟 0 错误 0 警告；剪影 15/15 唯一、图鉴、战役出征战斗回归全 PASS。

### v1.2.0 · 3D 地图重做（等距几何 + 山川河流质感 + 地形可辨识度）
- **修复等距瓦片几何（根因级 BUG）**：原 `tileCorners` 返回的是**矩形**而不是等距菱形（实测包围盒 52×26、面积 1377，正确菱形应为 688，相邻瓦片 2 个角点互相重叠），导致地图实际是"一堆互相重叠的矩形条靠画家算法裁剪"，完全没有等距斜边——这是"地图又丑又难辨"的病根。现改为标准菱形 `(0,-TH/2)→(TW/2,0)→(0,TH/2)→(-TW/2,0)`，实测面积比 1.000、相邻重叠率 0。
- **地形配色全面重做**：8 地形按"色相 + 明度 + 彩度"三维拉开，实测最小色差 **ΔE 22.3**（阈值 18）。原先 hill/swamp/castle/bridge 四者同为土黄系、几乎无法区分；现在 丘陵=明亮金黄、沼泽=暗橄榄、城堡=青灰砖石、桥梁=深木棕，一眼可辨。
- **统一光照 + 立体感**：固定光源方向（屏幕左上），侧壁按法线明暗渐变 + 岩层/土层**层理线** + 亮边高光；实测顶面最亮、两侧壁亮度差 21.7，立体感明确。
- **接触阴影 / AO**：相邻高差 ≥3 时自动绘制暗边（被高处遮挡）或亮边（临崖受光），实测贴丘陵侧比对照平原暗 8.0，地形起伏一眼可读。
- **山川质感**：山峰改三角形主峰 + 受光/背光二分 + 岩纹 + **雪冠**（高度阈值触发），并按相邻山地数自动**连脉缩放**；森林改为三层锥形树冠 + 落地阴影；丘陵加等高线圈层。
- **河流质感**：按上下游自动检测水流方向，绘制**定向流动波纹**（3 条相位动画）+ 波光 + 白色**岸线**（与陆地分离）；实测帧间差 6.6~10.9，水是"活"的。沼泽加冒泡/枯木/芦苇，城堡改青灰砖石城墙 + 箭塔 + **飘动旗帜**，桥梁按水流方向旋转。
- **远景与大气**：天空六段渐变 + 太阳光晕 + 流云 + 三层远山剪影 + 地平线雾化 + 分层大气雾，替代原来的扁平底色。
- **交互改善**：
  - **柱体命中**：高台（山地/丘陵/城堡）点击区从"仅顶面"改为顶面+侧壁的凸包柱体，实测顶面/右壁/左壁三点全部命中同一格，解决"高地点不中"。
  - **悬停高亮**：鼠标所指格显示白色描边 + 地形信息条（名称/移动力/防御加成）。
  - **地形图例**：右下角常驻图例面板（**L 键**开关），色块 + 名称 + 移动力；同时把侧栏硬编码的旧色块同步为新配色。
- **BUG 修复**：战役模式未开战时 `terrain` 为空，`render()` 每帧抛 `Cannot read properties of undefined`（每回合 1 次）；已加空地图保护，实测 0 报错。
- **真机验证**：几何/配色/纹理/河流流动/光照/AO/柱体命中/悬停/图例共 9 类指标，skirmish 与 campaign 双文件全绿；12 回合冒烟 0 错误 0 警告，15 兵种剪影唯一性、兵种图鉴、战役出征战斗回归全部 PASS。

### v1.1.1 · 品牌辨识（自定义技能图标）
- 新增**自定义技能图标**（512×512 真机渲染的战场实拍图），解决平台上"默认图标千篇一律"问题。
- 同步 `package.json` 版本号至 1.1.1，clawhub.ai / skillhub.cn 双平台版本一致。

### v1.1.0 · 兵种辨识度 + 平衡性大修
- **兵种外观差异化（重做）**：15 兵种全部绘制**专属剪影**（步兵/骑兵/弓/弩/枪/水军/蛮兵/车兵/兽兵/军犬/刀兵/盾兵/辎重/医疗/通信各一套独特轮廓），配 15 色专属配色 `UCOL`，战场与图鉴同源渲染，一眼可辨"谁是谁"。解决"造出来的士兵长得都一样"的玩家痛点。
- **新增「兵种图鉴」(U 键 / 📗 按钮)**：每张卡片用游戏同款剪影重绘，并展示 攻/防/移/射 + 克制 + 被克 + 地形适应 + 辅助能力 + **史实小传(lore)**，让每个兵种有"人设"与来历（Fire Emblem 式角色驱动留存）。
- **全网战棋设计研究落地**：参考 Advance Wars（高对比配色 + chunky 剪影）、Fire Emblem（角色人格驱动）、三国志·战棋版（兵种独特区隔、拒绝上位替代）等，做数据驱动改造——
  - 补全**完整克制网**：原 8 个兵种从不被克制、5 个兵种无克制目标；现 12 战斗兵种互相形成"克制三角"式闭环，每个兵种都有猎物与被克者。
  - 消除**真上位替代**：原 蛮兵/刀兵被骑兵、车兵完全碾压（属性严格支配且无补偿）；现调为「蛮兵=山地重甲bruiser」「刀兵=高速破阵散兵」，各有独特定位。
  - 水军保留**唯一可涉河**能力，辎重/医疗/通信保留补给/治疗/鼓舞专属辅助定位。
- **教程软锁死修复**（前版 BUG）：选国界面教程关闭按钮选择器不匹配导致无法关闭，已修复，新玩家首启教程可正常跳过。

### v1.0.0 · 首发
- 单文件 HTML5 等距 3D 战棋《七国群雄传》：战役 + 遭遇战双模式。
- 连击 Combo / 羁绊光援 / 合击必杀 / 名将专属必杀（16 名史实名将）。
- 武将图鉴(Codex)、成就系统、战绩记录、每日连签。
- 人机 / 双人 Hotseat / 联机对战（BroadcastChannel 本机 + WebSocket 跨设备 `net-server.js`）。
