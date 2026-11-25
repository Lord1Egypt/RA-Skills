---
name: vivid-menu
description: Turn a restaurant menu — as plain text, structured JSON, or a list of dishes — into a print-ready single-page menu design (SVG/PNG) with hand-drawn style dish illustrations, section dividers, themed paper-and-ink palettes, signature-dish spotlighting, and an automated layout/contrast/legibility inspection pass. Also ships the full runnable web app for interactive editing. This skill should be used when a user asks to design, redesign, beautify, or typeset a menu; wants a menu image for print, WeChat Moments, delivery platforms or a shop window; needs dish descriptions written for a menu; has a menu that is too long, badly spaced, unreadable, or inconsistent in price formatting; or asks to generate a restaurant menu from a list of dishes.
agent_created: true
---

# 生动菜单

把一段菜单文字变成一张**能打印、能发朋友圈、能贴门口**的菜单设计稿：分节、配色、逐道菜的线条插图、招牌菜放大、自动质检一次走完。

核心判断：**用户要的不是一张好看的图，是一张顾客看得清、老板敢印的菜单。**

## 四条铁律

**铁律一：价格只照抄，绝不编造。**
用户没给价格就留空，并在交付时说明「这几道没标价」。菜单上的数字会被当真，编一个就是事故。

**铁律二：招牌必须有依据。**
`signature_note` 要写清为什么推这道（销量最高 / 菜名带「招牌」/ 价位最高）。没有依据就不要标招牌——招牌是承诺，不是装饰。

**铁律三：先出完整一版，再迭代。**
不要一开始就追问十几个细节。先按默认值（米白宣纸、自动挑招牌、自动补描述）出一版给用户看，再说明「这几个是我替你定的」。看到实物，用户才知道要改什么。

**铁律四：不做 OCR。**
浏览器本地识别不了照片上的文字，本 skill 不提供图片转文字。用户发菜单照片时，明确说明需要把菜名和价格粘一遍（照片可以留作对照）。**不要假装能识别。**

## 何时使用

- 用户给一段菜品清单 / 菜单文字，要「做成一张菜单」
- 用户有菜单照片或截图，要重排成好看的样子
- 用户的菜单太长、太挤、字号乱、价格写法不统一
- 用户要为一组菜写菜单描述（一句话说明）
- 用户要菜单的印刷稿、朋友圈图、外卖平台头图
- 用户要一套能自己改的菜单工具（复制可运行的应用给他）

不适用：纯 logo / VI 设计、外卖平台店铺装修、菜品摄影、菜谱（做法）编写。遇到直接说明并建议另找工具。

## 工作流

### 第一步：判断输入形态，拿到菜品

三种输入，优先级从高到低：

1. **文字**（最常见）：每行一道菜，`红烧肉 68`，可用 `【热菜】` 标记分节。直接喂 CLI。
2. **JSON**：用户已有结构化数据，或需要精确控制某道菜的插图类别、招牌标记。
3. **只有照片**：让用户把菜名和价格敲一遍。可以帮他从照片里逐条读出来、整理成文字再确认——这属于人工转录，不是自动 OCR，要说清楚。

拿到的菜品数量、分节、是否有价格，先在心里过一遍：**少于 4 道**会太空，**超过 30 道**单页放不下。

### 第二步：出第一版

```bash
# 文字菜单（最常用）
node scripts/make_menu.mjs --text menu.txt --out out/menu.svg --png

# 指定店名、副标题、配色
node scripts/make_menu.mjs --text menu.txt \
  --theme kraft --name "城南面馆" --subtitle "手工现做 · 每日限量" \
  --footer "人均 45 元 · 11:00–21:00" \
  --out out/menu.svg --png --report out/qc.json
```

配色按 `references/themes.md` 的规则选，不要随机挑：辣用 `rice`/`clay`，鲜用 `indigo`，清用 `moss`，暖用 `kraft`。

出图后**必须看一眼 PNG**（用 ViewImage 读），不要只看质检报告就交付。质检查不出「画面空洞」「插图认不出」这类问题。

### 第三步：读质检，改能改的

CLI 会打印 `error / warn` 清单。规则含义见 `references/qc-rules.md`。

处理原则：

- **error 必须清零**，否则版面已破损
- **warn 逐条判断**，不是全都要修
- 自动修复已经跑过一轮（`--no-fix` 可关闭），剩下的基本都是需要人判断的

典型判断：

| 情况 | 怎么做 |
|---|---|
| `too-long` 超上限 | 先砍描述，再砍标签；仍超就拆成两张菜单（正餐/酒水） |
| `no-price` 连着几条 | 问用户补价格，等不到就留空并说明 |
| `no-blurb` 一片 | 词典没覆盖这些菜，手动补一句，比让机器猜好 |
| `contrast-low` | 主题选错了，直接换，不要微调颜色 |

### 第四步：调整与重出

需要改内容时改数据，不要改 SVG。改完重跑同一条命令。反复调整构图就用 `_seed` 换插图，不要换 `kind`（换类别会让插图变成另一种东西）。

### 第五步：交付

同时给三样东西，缺一样用户就用不上：

1. **PNG** — 直接看、直接发
2. **SVG** — 印刷用，矢量不失真
3. **JSON 或文字稿** — 下次要改的时候不用重敲

打印说明：PNG 走 `Ctrl+P` 或图片打印，选实际尺寸。菜单是 880×N 的窄长版式，打印时按「适合页面」缩放即可。

## 交付可运行的应用

用户要「自己改」「以后还能用」时，把整个应用复制给他：

```bash
cp -r assets/app /目标目录/vivid-menu
```

然后告诉他：**双击 `index.html` 就能用**，不需要服务器、不需要装东西、不上传数据。功能包括：粘贴文字生成、点击任意菜品改名字/价格/说明、换配色、换插图、导出 SVG、复制 PNG、打印。

改了 `js/` 里的源码后，必须跑一次 `node tools/build.js`（或双击 `build.bat`）重新打包，否则界面读的还是旧的 `app.bundle.js`。

## 命令行速查

| 参数 | 作用 |
|---|---|
| `--text <file\|->` | 文字菜单，`-` 表示从 stdin 读 |
| `--json <file>` | 菜单 JSON，结构见 `references/data-model.md` |
| `--demo <0\|1\|2>` | 内置示例（川味小馆 / 夜灯小食堂 / 山间茶事） |
| `--theme <id>` | `rice` `kraft` `moss` `indigo` `clay` |
| `--name` `--subtitle` `--footer` `--seal` | 覆盖菜单信息；`--seal` 建议两个字 |
| `--out <file.svg>` | 默认 `./menu.svg` |
| `--png [file.png]` | 另存 PNG，2 倍分辨率。找不到浏览器会跳过并提示，SVG 仍可用 |
| `--report <file.json>` | 质检报告落盘，含自动修复记录 |
| `--preview <file.html>` | 生成可直接双击查看的 HTML |
| `--no-fix` | 关自动修复 |
| `--allow-errors` | 有 error 也返回 0 |
| `--themes` | 列出配色 |

退出码：`0` 正常 ／ `1` 有未解决的 error ／ `2` 参数错误 ／ `3` 解析不出菜品。

## 常见错误

| 错误 | 后果 | 正确做法 |
|---|---|---|
| 只交一张 PNG | 用户要改一个字就得重来 | PNG + SVG + 数据稿三件套一起给 |
| 编造价格填满版面 | 印出来就是错的价格 | 留空并明确说明 |
| 标三道招牌 | 只有第一道会放大，其余名不副实 | 只标一道，排在最前面 |
| 三十道菜硬塞一页 | 缩到 6 号字，门口根本看不清 | 拆成两张菜单 |
| 描述写成「选用上等食材」 | 等于没写 | 写具体的：什么部位、什么口感、怎么做的 |
| 自称能识别照片文字 | 用户等着，结果什么都没出来 | 说清楚要人工转录 |
| 只看质检报告不看图 | 报告 0 error，但插图认不出 | 每次交付前用眼睛看一遍 PNG |
| 直接改 SVG 调排版 | 下次重出就丢了 | 改数据、改 CSS、改 `layout.js` 常量 |

## 参考资料

- `references/data-model.md` — 菜单与菜品的字段定义、版式常量、篇幅估算
- `references/themes.md` — 五套配色、选色规则、自定义主题的三项自检
- `references/art-kinds.md` — 22 个插图类别、推断优先级、换图方法、外部 SVG 接入
- `references/qc-rules.md` — 全部质检规则、触发阈值、自动修复的边界
- `assets/app/` — 完整可运行的应用；`assets/app/README.md` 是给最终用户看的说明
