---
name: video-shot-demos
description: 视频分镜演示动画生成技能：每个镜头产出一个独立 HTML（统一播放器底盘+每页不同视觉风格），覆盖风格分配、双角色立绘素材、口播时间轴对齐、批量截图质检与 index 总览的完整工具链。适用于制作技术实测、产品发布、课程、叙事类分镜演示视频。
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 9db5aa32bb416ff6601e09a7b615dacc_ed36f1baab6a11f18874525400287e28
    ReservedCode1: u6yOsEv22jbdVtYRWeJaUyUlNn7iQVd5R+izu80cHEUl0QXQimpRoLP/V4lLT8wSetgDQwgxvKxuFrVNpr7DvyB+S2cbW82pWgd5UPkMw7h2fkEvQ5XOs5udi4e1YV9Yx7+B8ot4fhI7FprxG84LKsHvnQK1mx3gEk7jIb/rg548zqvseXyaTsTVbuk=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 9db5aa32bb416ff6601e09a7b615dacc_ed36f1baab6a11f18874525400287e28
    ReservedCode2: u6yOsEv22jbdVtYRWeJaUyUlNn7iQVd5R+izu80cHEUl0QXQimpRoLP/V4lLT8wSetgDQwgxvKxuFrVNpr7DvyB+S2cbW82pWgd5UPkMw7h2fkEvQ5XOs5udi4e1YV9Yx7+B8ot4fhI7FprxG84LKsHvnQK1mx3gEk7jIb/rg548zqvseXyaTsTVbuk=
---



# 视频分镜演示动画（每镜头一个 HTML）

一个镜头 = 一个独立 HTML，统一播放器底盘 + 每页一种完全不同的视觉风格，全屏录屏即成片。内容开放（技术实测/产品发布/课程/叙事皆可），不变的是电影化机制、镜头语言与完成度标准。

## 创作哲学

1. **风格轮换**：连续镜头绝不同风格。问"这段内容若是一件实物/一个场所，它是什么"——复古报纸、POS 小票、审讯室、像素游戏……把抽象内容**具象成一个世界观**，页面就活了。
2. **禁默认科技暗色**：黑底+霓虹+玻璃拟态的"乌漆墨黑油光锃亮"两页即疲劳，除非内容本身是终端主题。
3. **想象力优先**：底盘之上放开写——会砸下的印章、会掉进存钱罐的硬币，用户要惊喜感。
4. **完成度是纪律**：元素有入有出（或定格）、无重叠遮挡、无孤儿元素、结尾有重播暗示、数据有出处角注。
5. **音画同步**：关键动作有音效、镜头移动配 whoosh；安静也是设计。

## Token 纪律（硬性）

- **禁止通读** `assets/template.html` 与 `assets/examples/` 下任何成片页（单个 20–50KB，读完耗尽预算）。
- 模板一律 `cp` 复制后**只读标记区域**（第 1 步）；成片页仅当写完仍卡壳时，grep 定位后按行号窗口读 ≤80 行。
- 机制与风格知识优先取自 `references/` 三份浓缩文档，不要现场读源码反推。

## 工作流

**第 0 步 · 输入与风格分配表**：通读素材（大纲/口播稿/画面设计/口述），拿到分镜列表 + 口播时间戳（时间轴对齐基准）+ 角色素材。排表 `镜头|时长|视觉风格|字体组合|主色`：相邻不同风格、整辑不重复、**同一实体全系列锁同一颜色**（观众靠颜色跨页追踪）。表给用户确认后再动工。

**工具化（推荐）**：镜头清单落成 JSON（`{"project":"...","shots":[{"id":"0-1","title":"...","dur":14,"brief":"震撼数字 事件宣告"}],"locks":[...]}`，格式见 plan.js 头注释）后 `node scripts/plan.js new 清单.json` 生成风格分配草表（自动校验：相邻不同风格 / 整辑不重复 / 实体锁色一致性），确认后 `node scripts/init.js <清单同名>.plan.json --root <输出根目录>` 一步完成初始化：建输出目录 → 校验并复制双角色立绘 → 按分配表批量生成带命名的 shot 骨架页（已带 shot-meta 风格标签）。手工路径（无清单文件时）与素材清单、cp 前校验规则见文末「工程规范」。

```bash
cp -r "assets/examples/<项目>/anan - emotion rename" <输出目录>/    # 安安 15 情绪立绘；图标同理
cp -r "assets/shery - emotion rename" <输出目录>/                   # 橘雪莉 20 情绪（笨蛋吐槽役，重点页与安安同框）
```

**第 1 步 · 逐页实现**（cp 起步，只读标记区）：

```bash
cp assets/template.html "<输出目录>/shot-x-x_名称.html"
grep -n "改这里\|DUR=" "<输出目录>/shot-x-x_名称.html"    # 行号地图（7 处改这里 + DUR）
```

用 Read 的 offset/limit 只读标记行附近区域（字体 link+舞台底色 / 画面层 CSS / 画面 HTML / cue 表+DUR），逐一替换：① 字体与配色（Google Fonts 随风格）；② 重画画面层；③ 按口播时间戳写 cue（注释引用口播句，如 `// 5:20「正常充值」`）；④ `DUR`=规定时长±0.5s。底盘（引导脚本/音效引擎/时间轴/镜头调度/HUD）不动。

口播时间戳 → cue 毫秒换算：`node scripts/timeline.js calc 5:01 5:18`（mm:ss→毫秒）；写完页面后 `node scripts/timeline.js table 页面.html --base 5:01` 生成 cue×口播对照并校验时间轴。

按需读参考（都很小）：`references/mechanics.md` 播放器+镜头+音效机制 ｜ `references/style-cards.md` 40 种风格卡片（字体/主色/材质/样板页号） ｜ `references/character-reactions.md` 双角色吐槽体系（安安×橘雪莉情绪表、中段快闪切立绘、双人同框 cue、气泡强约束模板）。

**第 2 步 · 质检**：`node scripts/shot.js 页面.html <毫秒> _t.png [fx fy scale]` 多时间点无头截图，逐张查重叠遮挡/中间态穿帮/收尾定格，最后完整播一遍。整辑批量落图：`node scripts/batch-shot.js <目录> [--times 25,50,75,95] [--only 关键词] [--limit N]`（全页 × 多节拍点，先 --limit 1 试点再全量）。交付前 `node scripts/lint.js <目录>` 跑脚本化 checklist（角色出场≥2 次 / 相邻风格主色撞车 / 实体锁色 / DUR 与末 cue 越界 / 标题与 shot-meta 规范），红灯必须清零。

> Chrome/Edge 132+ 已移除旧 headless 截图开关：shot.js 检测到 CLI 静默失败会自动回退内置 CDP 后端（无依赖），无需干预；可用 `SHOT_ENGINE=cdp` 跳过 CLI 直走 CDP 提速。

**第 3 步 · index 总览**：`node scripts/gen-index.js <目录> --title "辑名" --chapters "00=引子,02=实测"` 自动按章分组汇总编号/时长/标题/风格标签卡片（风格取自每页 `<!-- shot-meta style="..." -->` 注释，骨架页已自动带上）。已存在 index.html 时自动按版本规范备份。index 自成一种风格，可再手改报头。

**翻新已有页面时**：先盘点并列清单（用户点名保留的页面一字不动）→ 底盘统一注入 → 逐页重设计画面层 → 补角色/镜头/音效 cue → 质检。

## 交付标准

- [ ] 黑场「启动播放」起手，2s 渐变后开演；1920×1080 自适应；HUD 底部唤出；可暂停重播；DUR 准确
- [ ] 相邻镜头风格/字体/配色不同；无默认科技暗色；emoji→内联扁平 SVG
- [ ] 关键节拍有镜头运动（推/拉/跟/摇）+ whoosh；关键动作有音效；计数滚动有连击键音
- [ ] 角色出场**每页 ≥2 次**（中段 30–45% DUR 快闪 + 结尾 75–85% 定场，短页仅结尾）：快闪=同一元素换台词换立绘、160ms 闪换重弹；重点页双角色（雪莉先吐槽→安安 1.2s 后接茬，同框退场）；气泡**必须用统一强约束模板**（形态锁定，仅 4 配色可调，见 character-reactions.md）
- [ ] 无底部字幕条（口播只以 cue 注释对齐，不上屏）；截图验证无重叠遮挡；数据角注出处；index 可逐页打开

## 工程规范

### 素材资产清单与 cp 前校验（缺口①配套）

| 资产 | 位置（相对技能根） | 数量基准 | 用途 |
|---|---|---|---|
| 安安立绘 | `assets/examples/glm-5.3-range-test/anan - emotion rename/` | 15 张 PNG | 双角色主役（doubao 项目同套复制件可作备用源） |
| 橘雪莉立绘 | `assets/shery - emotion rename/` | 20 张 PNG | 吐槽役（16-20 号为后补 900KB 档，尺寸略异属正常） |
| 项目图标 | `assets/examples/glm-5.3-range-test/icons/` | GLM/GPT 各 1 | 实体锁色图标 |
| 参考页 | `assets/examples/glm-5.3-range-test/reference/` | typewriter 1 页 | 打字机参考 |

- **cp 前强制校验**：任何素材复制前先数 PNG 数量（anan=15 / shery=20），不足即中止并报告缺哪些——往期项目里出现过 shery 目录整个为空的坑。`init.js` 已内置该校验（缺张即红字退出），手工 cp 时照此自查。
- 素材只 cp 不读内容（PNG 不进上下文）。

### 重制与备份版本规范（替代 `_重制`/`_全新重制`/`_backup_*` 混乱命名）

- **禁止**再产出 `*_重制.html`、`*_全新重制.html`、`_backup_xxx/` 这类自由命名——往期目录已为此出现三版 shot-7-1 并存、无法判定哪版是交付版。
- **页面重制**：新版用 `.v2.html` / `.v3.html` 递增后缀（`shot-7-1_出厂默认.v2.html`），旧版直接删或移入 `<项目>/_archive/`，**同一时刻目录内一页只留一个有效版本**（`_backup`/`.bak`/`_archive` 均被 lint/gen-index/batch-shot 排除）。
- **index 备份**：gen-index.js 自动把旧 index 存为 `index.backup.<yyyymmdd-hhmmss>.html`，不接受手工改名备份。
- **成片归档**：整辑交付后移动到独立归档目录（见下），不留副本在工作目录。

### 多项目共存的目录与命名隔离

- 一个视频项目 = 一个独立目录，目录名 `项目代号-日期`（如 `glm53-2026q1/`），**禁止两个项目的 shot 页混放同一目录**（往期根目录 67 页两辑混放、编号撞车 shot-0-1 双份的教训）。
- 编号空间 `shot-<章>-<镜>[_<字母变体>]` 只在项目内自洽；跨项目不要求连续，但同项目内不得重复。
- 素材目录（立绘/icons）随项目目录走，不跨项目引用技能 assets 之外的相对路径。
- 归档：`【AI城】/往期视频/` 下的 dsh2shell 辑与 GLM 辑混放已成事实，新归档按项目子目录存放（`往期视频/<项目名>/`），不再往根目录堆。

### 录屏成片指引

- **环境**：Chrome/Edge 全屏（F11），1920×1080 显示器且系统缩放 100%（否则 canvas 分辨率漂移）；OBS 采集窗口或显示器，`1920×1080 @ 60fps`，色彩空间 sRGB。
- **起手**：每页从「启动播放」黑场录到结尾定格（HUD 隐藏态），页间剪辑留 0.5s 黑场；暂停键别按（暂停会冻结 CSS 但计时器仍在走）。
- **Google Fonts 闪烁规避**：录前先开一遍每页等字体加载完再刷新重录；或一次性预载（页面已带 `<link rel=preconnect>`，若仍闪烁，在模板 head 追加 `<link rel="preload" as="style">` + 字体 CSS 内联）。
- **离线回退**：断网录制时 Google Fonts 失败回退系统字体（Noto 缺失 → 宋体/黑体），录制前 `ping fonts.googleapis.com` 确认可达；要求像素级稳定的镜头可把该页字体下载为 woff2 本地引用。
- **音轨**：页面 SFX 由 WebAudio 输出，OBS 需采集"桌面音频"；BGM 后期叠加，不进页面。

### 工具链速查（scripts/，全部 node 可运行、零依赖）

| 脚本 | 一步命令 | 用途 |
|---|---|---|
| plan.js | `node scripts/plan.js new 清单.json`（清单格式见脚本头注释） | 风格分配草表 + 相邻/整辑/锁色校验 |
| init.js | `node scripts/init.js plan.json --root <目录>` | 建目录 + 素材校验复制 + 批量 shot 骨架 |
| timeline.js | `node scripts/timeline.js calc 5:01 5:18` / `table 页.html` | 口播 mm:ss ↔ cue 毫秒换算与对照校验 |
| shot.js | `node scripts/shot.js 页.html <ms> <png> [fx fy s]` | 单页单点快进截图（CLI 失效自动走 CDP） |
| batch-shot.js | `node scripts/batch-shot.js <目录> [--times 25,50,75,95]` | 整辑 × 多节拍批量落图 |
| lint.js | `node scripts/lint.js <目录>` | 交付 checklist 脚本化质检 |
| gen-index.js | `node scripts/gen-index.js <目录> --title "辑名"` | index 总览自动生成（旧版自动备份） |

环境变量：`BROWSER_PATH` 指定浏览器；`SHOT_ENGINE=cdp` 跳过旧 CLI 直走 CDP（Chrome 132+ 建议）；`SHOT_DEBUG=1` 输出 CDP 诊断日志。
*（内容由AI生成，仅供参考）*
