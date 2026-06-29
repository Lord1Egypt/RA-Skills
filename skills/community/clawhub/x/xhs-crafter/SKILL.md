---
name: "xhs-crafter"
description: "将MD文章排版为3:4比例的精美图片+压缩文字稿，用于公众号/小红书贴图发布。Invoke when用户要排版文章为图片、生成公众号贴图、小红书图文、文章转图片卡片。Do NOT use for原创写作、纯文字排版、视频制作。"
---

# XHS Crafter — 文章转图片卡片

## 任务
将用户提供的MD文章内容，排版为多张3:4比例(1080×1440)的精美HTML页面，截图为PNG，压缩为≤1000字文字稿，文件夹交付。不做原创写作，不做视频，不做纯文字排版。

## 输出格式

```
<桌面>/<slug>公众号素材/
├── p1-cover.png
├── p2-xxx.png
├── ...
├── pN-finale.png
└── <slug>-文字稿.txt   # ≤1000字压缩文字
```

## 工作流：5步（全自动，中间不停顿）

**核心原则：用户给MD，直接出文件夹。** Step 1-2在脑内完成（不输出长文规划），Step 3-5连续执行不等待用户确认。

### Step 1: Intake — 识别品类（脑内完成，不输出）
从MD内容自动推断：
- **内容品类**: 读 `references/category-cookbook.md` 路由。13个品类：商业/科技分析、职场/干货、旅行/生活方式、教程/工具、影视/读书、游戏、美食、彩妆、穿搭、家居、健身、情感、推荐。超出范围的品类（梦核/氛围感装饰风、Y2K/千禧辣妹、纯摄影展示）必须在设计前明确告知用户
- **目标平台**: 默认小红书3:4（除非用户指定公众号）
- **用户图片**: (a)用户指定截图文件夹路径；(b)解析MD中 `![描述](路径)` 和 `[🖼️配图建议：xxx]` 标记
- **图片三选一门控**（仅在用户无图时触发，一次性提问不反复追问）：
  ```
  这篇我需要 1-2 张图。三种走法：
  A. 你自己有照片/截图，传给我（推荐——最不"AI感"）
  B. 我去 Pexels/Unsplash 帮你找
  C. 用 AI 生成
  ```
  推荐 A，但接受用户任何选择（包括"都行你看着办"），不再追问
- **仅在品类无法推断时才问用户**，否则直接进入Step 2

### Step 2: Content Plan — 内容规划（脑内完成，不输出）
读 `references/content-planning.md`，完成：
- 压缩阶梯：核心论点1句 → 读者承诺 → 4-8个分论点 → 页面钩子 → 正文片段
- 页面角色分配：7页组图至少5种不同形态
- **页面节奏规划**：为每页标注明暗(Light/Dark)、氛围强弱(Strong/Subtle)、版式类型，读 `references/portrait-fill.md` 的"Three-Layer Rhythm System"
- 封面钩子：用具体承诺而非空洞口号
- 页数指导：600-1000字→5-7图，1000-1800字→7-9图
- **5页及以上：封面和封底都必须有图片背景**

### Step 3: Compose — 组装HTML（直接执行）
- 拷贝种子模板：Editorial→ `assets/template-editorial-card.html`；Swiss→ `assets/template-swiss-card.html`
- 设置 `data-theme` 或 `data-accent` 属性切换主题
- 在 `<!-- POSTERS_HERE -->` 处添加页面

**字号速查表（必须严格遵循，不得自行调整）**：

| Role | Class | Size | Weight | Family | 用途 |
|------|-------|------|--------|--------|------|
| Display | `.h-display` | 136px | 500 | serif-zh | 封面/封底主标题 |
| Section title | `.h-xl` | 110px | 500 | serif-zh | 内容页主标题（必须统一） |
| Mid title | `.h-md` | 60px | 500 | serif-zh | 次级标题/数据页标题 |
| Subtitle | `.h-sub` | 46px | 400 italic | serif-en | 英文副标题 |
| Pull quote | `.pullquote` | 80px | 500 italic | serif-zh | 引言页大字引语 |
| Lead | `.lead` | 34px | 400 | serif-zh | 导语/段落首句 |
| Body | `.body` | 32px | 400 | serif-zh | 正文段落 |
| Kicker | `.kicker` | 26px | 500 | mono | 页面顶部标签 |
| Meta | `.meta` | 24px | 500 | mono | 页面底部注释 |
| Label | `.label` | 24px | 500 | mono | 数据标签 |
| Stat number | `.stat-nb` | 72px | 500 | serif-zh | 大数字 |
| Step title | `.step-title` | 34px | 500 | serif-zh | 流程步骤标题 |
| Step desc | `.step-desc` | 28px | 400 | serif-zh | 流程步骤描述 |
| Ledger title | `.ledger-title` | 30px | 500 | serif-zh | 表格行标题 |
| 辅助文字 | — | 22px | 500 | mono | stat-label/stat-unit/ledger-note/step-nb/callout-src/issue-strip |

**字号铁律**：
1. **内容页主标题必须统一用 `.h-xl` 110px**——不得混用 `.h-md`，标题太长拆行而非降级
2. **封面/封底主标题用 `.h-display` 136px**——比内容页大24%，形成"书挡"层级
3. **满铺图页标题颜色必须 `#ffffff` + `text-shadow`**——禁止 `#ece2cf`（与暖调背景太接近）
4. **字重"越大越轻"**：≥110px用500，60-80px用500，32-46px用400，24-26px用500
5. **任何文字不得低于18px**

**节奏速查表（必须严格遵循）**：

| 规则 | 要求 | 违反后果 |
|------|------|---------|
| 暗色页数量 | 5页+至少1页Midnight Ink，7页+至少1-2页 | 全light=单调 |
| 暗色页位置 | 引言页或结尾页最佳 | 中间也行，但不可相邻 |
| 暗色页相邻 | 禁止！2个暗色页必须隔至少1个light页 | 相邻=对比抵消 |
| 氛围强度 | 封面/引言/封底=strong，数据/清单=subtle，正文=medium | 全同一强度=死板 |
| 版式重复 | 禁止连续2页用同一种版式骨架 | 密集ledger后接宽松essay |
| 首尾图框 | 5页+封面和封底都必须有图片背景 | 无图=缺"书挡" |
| 连续同色 | 连续3页相同主题色=P0错误 | 第3页必须插入暗色/氛围变化 |

**密度速查表（必须严格遵循）**：

| 规则 | 要求 |
|------|------|
| 活跃构图 | ≥78%画布高度（≈1123px of 1440px） |
| 4横带密度 | 1440px切4段(360px)，每段有内容或主动留白理由 |
| 纯空白带 | >216px必须有设计理由（如atmospheric hero页） |
| 最少元素 | 每页至少3种内容元素（标题+正文+数据/图/引言） |
| 表格行高 | 不足45%画布时加左侧大数字列或转M08 Tall Ledger |
| 重复模式 | 避免"标题+lead+3行"重复超过2次 |

**图片规则速查（必须严格遵循）**：

| 规则 | 要求 |
|------|------|
| 图片下载 | 必须下载到本地`assets/`，禁止引用外部URL |
| 唯一性验证 | 下载后用`buf1.equals(buf2)`验证，相同则换Unsplash |
| 满铺图页 | 选图→无遮罩构图→局部色调遮罩→缩略图检查 |
| 满铺图标题色 | 必须`#ffffff`+`text-shadow`，禁止`#ece2cf` |
| 主体感知裁切 | 根据`object-position`确保主体完整可见 |
| 截图展示 | 用`.frame-shot`包壳，给45-65%页面高度 |
| 图源优先级 | 用户图>Unsplash>Pexels>Wallhaven>AI生成 |
| accent面积 | Swiss≤30%，Lemon Green≤20% |

- **满铺图页必须遵循 `references/image-overlay.md`**：选图→无遮罩构图→局部色调遮罩→缩略图检查
- **密度保障**：每页活跃构图≥78%画布高度，读 `references/portrait-fill.md`
- **节奏保障**：暗色页插入、氛围强弱交替、版式不重复
- **背景系统**：Editorial 必须使用三层背景（paper→wash→grain），禁止纯平背景。读 `references/background-systems.md`。氛围强度按页面角色分级：封面/引言/封底用 strong，数据/清单用 subtle
- **图片必须下载到本地**（关键！Puppeteer headless无法可靠加载外部API图片）：
  1. 用WebFetch获取API返回的CDN URL
  2. 用curl下载到项目`assets/`目录
  3. HTML中用本地相对路径引用：`src="assets/cover.jpg"`
  4. 禁止直接引用外部URL（trae-api-cn / unsplash / pexels等），一律先下载再引用
- **图片下载后必须验证唯一性**（关键！AI生图API可能返回相同占位图）：
  1. 下载多张图片后，用 `buf1.equals(buf2)` 验证它们确实不同
  2. 如果两张图完全相同，说明API返回了占位图，必须换用Unsplash真实图片
  3. Unsplash直链格式：`https://images.unsplash.com/photo-{id}?w=1080&h=1440&fit=crop&auto=format&q=85`
  4. 禁止假设URL不同=内容不同
- 图源优先级: 用户图 > Unsplash > Pexels > Wallhaven > AI生成(trae-api-cn text_to_image)
- 截图用 `.frame-shot` 包壳

### Step 4: Validate — 自检（自动执行，不等待）
截图前自动检查，不通过则自动修复：

**密度检查**：每页活跃构图≥78% | 每页≥3种内容元素 | 纯空白带>216px需理由
**图片检查**：封面1秒说清主题 | 文字未压主体 | 无broken image | **多张背景图文件内容不同（buf1.equals(buf2)===false）**
**标题一致性检查**：所有内容页主标题使用同一字号class | 不得混用.h-xl和.h-md | 封面允许更大字号
**节奏检查**：5页+至少1暗色页 | 暗色页不相邻 | 氛围强弱交替 | 版式不重复
**风格检查**（读 `references/style-system.md`）：
- [ ] 全套风格统一（同一主题色+同一风格）
- [ ] Editorial身份测试：有atmosphere层 + serif标题 + 至少一个magazine结构元素
- [ ] Swiss身份测试：大标题字重≤300 + 无serif + 单一accent + 无卡片阴影
- [ ] 无文字溢出/footer碰撞

**自动验证**（读 `assets/validate.js`）：
- 运行 `node assets/validate.js <项目目录>` 执行 12 项自动检查
- R1 溢出检查 / R2 footer碰撞 / R3 Swiss粗体 / R4 最小字号 / R5 4横带密度 / R6 h-xl换行 / R7 figure margin / R8 标题一致性 / R9 满铺图页标题颜色 / R10 暗色页节奏 / R11 accent面积 / R12 封面封底图背景
- FAIL 项必须修复后才能交付，WARN 项为建议

### Step 5: Screenshot & Deliver — 截图交付（直接执行）
- 用`assets/screenshot.js`截图（自动检测页面ID，无需手动配置）
  - 用法：先启动`python -m http.server 8090`，然后`node assets/screenshot.js <项目目录>`
  - puppeteer-core + 系统Chrome，deviceScaleFactor:2
  - 等待networkidle0 + fonts.ready + 6秒（确保图片加载）
  - Chrome路径: 自动检测`$env:LOCALAPPDATA\ms-playwright\chromium-*\chrome.exe`
- **截图大小异常检测**（关键！文件过小说明图片未渲染）：
  - 带背景图的页面（封面/封底）PNG应 >1MB（2x分辨率下）
  - 纯文字页面 PNG 通常 800KB-1.5MB
  - 如果封面/封底截图 <500KB，大概率背景图未渲染，需检查图片文件是否有效
- 文字压缩：保留原话引言+场景描述+核心数据，≤1000字
  - **压缩模板**：标题(1句) → 场景开场(1-2句，含人物/时间/地点) → 核心论点(1-2句) → 关键原话(1-2条，用「」包裹) → 数据支撑(3-5个关键数字) → 结尾原话(1条)
  - **必须保留**：原文中的人物原话（用「」标记）、访谈/会议场景描述、关键数据
  - **可以删减**：过渡句、重复论述、次要细节、纯背景铺垫
- **交付方式：本地文件夹 + 飞书云盘同步**（双通道交付）

  **A. 本地文件夹（首选）**
  1. 在`$env:TEMP`创建`<slug>公众号素材/`文件夹
  2. 将PNG+txt复制到该文件夹
  3. 用`explorer.exe`打开文件夹，用户可拖到桌面

  **B. 飞书云盘同步（手机端访问）**
  1. 用`lark-cli drive +create-folder`创建`<slug>公众号素材`文件夹
  2. cd到output目录，用`lark-cli drive +upload --file <filename> --folder-token <token>`逐个上传PNG+txt
  3. 返回飞书云盘文件夹URL，用户手机飞书App打开即可逐张保存到相册
  4. 注意：lark-cli要求用相对路径，必须先cd到output目录再上传

## 标题一致性铁律（非协商）

1. **内容页主标题统一字号**：所有内容页（P02-P08）的主标题必须使用同一个 class（Editorial 用 `.h-xl` 110px，Swiss 用 `.h-xl` 128px）
2. **封面允许更大字号**：封面用 `.h-display`（Editorial 136px）或 `.h-hero`/`.h-statement`（Swiss）
3. **通过拆行适配而非降级字号**：标题太长时拆为两行，太短时加副标题增加视觉重量，不得降级到 `.h-md`
4. **不得混用不同级别标题 class**：同一套卡片中，内容页主标题不得混用 `.h-xl` 和 `.h-md`

## 密度铁律（非协商）

1. **活跃构图 ≥78% 画布高度**（≈1123px of 1440px）
2. **4横带密度**：1440px切4段(360px)，每段有内容或主动留白理由
3. **纯空白带 >216px 必须有设计理由**（如atmospheric hero页）
4. **每页至少3种内容元素**（标题+正文+数据/图/引言）
5. **表格/ledger行高不足45%画布时**：加左侧大数字列、加pull quote列、或转M08 Tall Ledger
6. **避免"标题+lead+3行"重复超过2次**

## 节奏铁律（非协商）

1. **明暗节奏**：5页以上组图至少1页暗色页(Midnight Ink)，7页以上至少1-2页。暗色页不是换主题，是同一主题内的明暗对比
2. **暗色页位置**：最佳位置是引言页(Pull Quote)或结尾页(Closing)。2个暗色页不可相邻
3. **氛围节奏**：封面/引言/结尾用强氛围(strong grain+wash)，数据/截图/清单用弱氛围(subtle grain only)。不可所有页同一氛围强度
4. **版式节奏**：不可连续2页用同一种版式骨架。密集ledger后接宽松essay或pull quote
5. **首尾图框**：5页及以上组图，封面和封底都必须有图片背景（满铺图或大图区），形成"书挡"效果。图片必须与主题适配——封面图抓主题，封底图收情绪
6. **连续3页相同主题=P0错误**：连续3页以上使用相同主题色（全light或全dark）视为严重错误，必须在第3页插入暗色页或氛围变化页

## 必读参考文件

| 文件 | 用途 |
|------|------|
| `references/style-system.md` | **风格系统**：Editorial vs Swiss视觉锚点+身份测试+反模式 |
| `references/category-cookbook.md` | **品类路由表**：13个品类的风格/主题/版式/图源映射 |
| `references/content-planning.md` | **内容规划**：压缩阶梯+页面角色+钩子模式+页数指导 |
| `references/portrait-fill.md` | **3:4密度规则**：垂直分区+密度铁律+稀疏页修复 |
| `references/image-overlay.md` | **文字压图**：选图→无遮罩→局部色调→缩略图检查+主体避让 |
| `references/theme-presets.md` | 10套主题色CSS变量 |
| `references/components.md` | 字体/字号/间距/图片容器/卡片/截图容器规范 |
| `references/layout-recipes.md` | 28种布局模板(M01-M16+S01-S12) |
| `references/screenshot-treatment.md` | 截图美化：设备外壳+背景材质+风格默认 |
| `references/background-systems.md` | **背景系统**：三层架构（paper→wash→grain）+ 氛围强度分级 + 满铺图页 + Swiss极简 |
| `references/image-sources.md` | Pexels/Unsplash/Wallhaven图库接入 + AI生图验证规则 |

## 示例

**输入**: SpaceX上市分析MD → 自动推断：商业/科技分析 → Editorial × Indigo Porcelain

**输出**: 7张PNG + spacex-文字稿.txt → `SpaceX公众号素材/` 文件夹

**输入**: skill-forge教程MD+截图文件夹 → 自动推断：教程/工具 → Swiss × IKB Blue

**输出**: 6张PNG + skillforge-文字稿.txt → `skillforge公众号素材/` 文件夹
