---
name: openclaw-ui-theme-coach
description: 引导式 UI 主题设计顾问：通过问答引导帮用户定制任意风格的 OpenClaw Control UI 主题（像素/赛博朋克/卡通/极简/暗色科技等），含主色派生调色板、双保险注入、升级自愈（cron+快照）与反馈学习循环。触发词：主题、换皮、皮肤、UI 美化、风格。
version: 1.5.0
emoji: 🎨
categories: [theme, ui-customization, design]
tags: [theme, control-ui, pixel, cyberpunk, accessibility, palette]
---

# OpenClaw UI Theme Coach（OpenClaw 主题设计顾问）

> 引导式 UI 主题设计 skill：通过问答引导帮用户定制任意风格的 OpenClaw Control UI 主题。
> 五大能力：通用方法论、风格技术库、自助检索、升级自愈、反馈学习。

## 何时使用
- 用户想让某个 AI/Web 界面变成某个风格：OpenClaw Control UI、**DSH web UI（DeepSeek Harness 界面）**、任意 Web 项目/静态稿——像素/MC、赛博/霓虹、卡通/可爱、极简/现代、暗色科技……
- 关键词：主题、换皮、皮肤、UI 美化、风格

## 核心哲学
1. **可读性优先**：不挡阅读、不挡点击；好看但挡字的东西砍掉。
2. **一步步来**：一次改一块，先配色→逐元素→统一打磨。
3. **素材策略（默认官方，自绘兜底）**：skill 默认帮用户找 **IP 明确的官方/授权素材**（素材指路，见第五步）——官方图最贴原版、最好看，**除非用户明确要求自绘、或官方素材不可得/无授权渠道**，否则不自绘。skill 内置素材/示范案例必须干净（自绘或已授权），不内置、不下载第三方版权素材进 skill 包；用户个人使用官方素材属合理使用（适用于所有作品）；用户自行发布时，素材授权由用户自行确认。
4. **注入安全**：改前备份 dist/control-ui/index.html；改完 node --check 验证。
5. **重启误区**：改静态文件，Ctrl+Shift+R 强制刷新即生效，不用重启网关。
6. **开放但不盲从**：主动找外部工具，但引入一律过安全门槛。
7. **具体风格→先调研再设计（重要）**：用户指定具体风格（赛博朋克/Minecraft/极简/卡通…）时，**默认先到网上查该风格的权威资料（视觉特征/配色/字体/材质/反模式/真实案例）再动手**，不靠脑内泛泛认知硬做。风格越具体，越要先查。

---

## 第一步：问答引导
一次 2-3 个问题：
- **风格**：像素/赛博朋克/卡通/极简/暗色科技/拟物？参考 IP？（素材用户自备即可，skill 不内置第三方图）
- **色彩**：主色调？点缀色？深/浅背景？
- **氛围**：硬核/温馨/趣味/冷静？动画？特殊元素？
- **可读性**：文字优先清晰（默认必须）。

> 用户给不出就推荐默认：通用像素风 + 深色 + 一个主色。

---

## 第一步·补：风格资料调研（用户给了具体风格 → 必做前置）

> **核心规则**：只要用户给出了**具体风格/IP/参考**（赛博朋克、Minecraft、极简、卡通、暗色科技、某知名 IP 等），在进入设计令牌**之前**，先查这个风格的资料。不查就设计 = 靠印象硬做，还原度会飘。

**查什么（web_search / web_fetch）：**
1. **核心视觉特征**：典型配色、形状语言（圆角/硬边）、材质/纹理、光影规律
2. **字体**：该风格常用字体（像素→Zpix 等；赛博→等宽科技感等）
3. **标志性元素**：按钮/卡片/光标/状态栏在该风格下长什么样
4. **反模式**：这个风格里最容易踩的坑（例：像素风忌渐变/抗锯齿）
5. **真实案例/参考图**：找到 2-3 个该风格的真实产品或界面参考，别凭空想

**查完产出（调研小结，写进设计依据）：**
- 该风格的**可提取特征清单**（能落实到 CSS 的具体点，不是抽象形容词）
- **配色锚点**（该风格的代表色/材质参考值）
- **反模式清单**（对照第四步自查）
- **参考链接**（存到 `data/style-refs.json` 或本目录，方便复查）

**优先级：** 用户给的风格越具体 → 调研越认真；用户给的是宽泛方向（如"想要温馨点"）→ 可轻查或不查，直接走内置风格库（`references/styles/`）。

> 内置风格库（第四步）是**兜底**，不是代替调研——两者互补：调研给还原度，内置库给实现技巧。

---

## 第二步：设计令牌 + 主色派生调色板

### 2.1 CSS 变量覆盖（:root + !important）

| 变量 | 作用 |
|------|------|
| `--bg` / `--bg-elevated` / `--bg-muted` / `--bg-content` / `--bg-hover` | 背景层级（含悬停） |
| `--card` / `--card-foreground` | 卡片底色/文字 |
| `--chat-text` / `--chat-box-inset` | 聊天文字/输入框底 |
| `--border` / `--border-hover` / `--border-strong` | 边框 |
| `--accent` / `--accent-hover` / `--accent-muted` / `--accent-foreground` | 强调色 |
| `--accent-glow` | 辉光 |
| `--accent-2` / `--accent-2-muted` / `--accent-2-subtle` | 第二强调色 |

> **通用设计令牌**：这套变量名继承自 OpenClaw Control UI 的令牌约定，但本身是**通用设计令牌**——任何 Web UI 拿到这 20 个变量都能直接消费。目标 UI 用别的变量名时，按语义映射过去即可（如 `--bg`→对方的主背景变量）。这保证了本 skill 的设计成果不只用于 Control UI，也可交付给任意 Web 项目（见 3.0 目标环境判定）。

### 2.2 主色派生调色板（1 个基色 → 全套变量）

**方法 A：HSL 偏移**（Python 标准库，零依赖）
从主色 hex 提取 HSL，保持色相、阶梯亮度，自动派生 20 个 CSS 变量。默认深色主题；浅色主题加 `--light` 亮度反转（背景转浅、文字转深、主色不变）：

```bash
python3 scripts/derive-palette.py '#7ca843'          # 深色（默认）
python3 scripts/derive-palette.py '#7ca843' --light  # 浅色（亮度反转）
```

> 两种模式派生的变量都要过第四步「必查配对清单」；浅色版 `--accent-foreground` 特意保持深字，与中亮度强调色保证 ≥ 4.5:1；**border 类单独处理**：以最终 `--bg` 为基准自动二分对齐对比度（`--border` ≈3.2:1 / `--border-strong` ≈4.2:1 / `--border-hover` ≈5.5:1，任意色相都过 UI 组件 ≥3:1 且不刺眼）。非法 hex（缺 `#`/3 位简写/非 hex 字符）脚本会友好报错并打印用法，不会吐 Python traceback。
完整脚本见 `scripts/derive-palette.py`。

**方法 B：OKLCH**（色彩空间更均匀，需要额外库）
同样思路但用 OKLCH 插值，渐变更自然。

> 选择方法 A/B 取决于用户偏好；方法 A 零依赖够用。

---

## 第三步：通用实现流程

### 3.0 目标环境判定（先问清目标，再选交付形态）

> 通用方法论（v1.3.0 起，源自 DSH 适配版回合）：本 skill 不只服务 OpenClaw Control UI。动手前先判定目标形态，按形态选交付方式：

| 目标形态 | 判定方式 | 交付形态 |
|---------|---------|---------|
| A. 构建产物 index.html（OpenClaw Control UI / **DSH web UI** 即此类：静态入口文件 + 会被升级覆盖） | 目标存在一个会被构建/升级覆盖的静态入口文件 | 3.1 双保险注入 + 备份 + 主题包快照（7.0） |
| B. 静态原型/设计稿 | 用户只要效果，没有固定宿主 | 直接产出完整 HTML/CSS（单文件或小项目），无需注入 |
| C. 其他运行时（非 Web/插件体系） | 目标不是浏览器页面 | 只做设计令牌 + 配色方案（第二步产物），实现细节按目标环境调整 |

> 本 skill 的主场景 = 形态 A 的 OpenClaw Control UI（注入架构见 3.1，自愈见 3.2）。形态 A 的注入步骤是**通用 Web 技术**，用于其他目标时，注入位置、资源路径必须按实际目标环境核对（备份→注入→验证三件套不变）。

### 3.1 注入架构（Control UI 是 Lit shadow DOM）
- CSS 变量（:root）能穿透 shadow DOM → 配色改 :root 全局生效
- 通用选择器打不进 shadow root → 改内部元素必须注入到每个 shadow root

**双保险注入法**：
1. `</head>` 前加 `<style>` 定义 :root 变量
2. `</body>` 前加 `<script>`：`ensureDocStyle()` + `WeakSet` + `MutationObserver` **递归遍历**所有 shadow root（shadow root 套 shadow root 的套娃也钻进去，见 minecraft-example.md 的 `walk()`）
3. 完整模板见 `references/minecraft-example.md`

### 3.2 升级自愈机制（独门能力）

> 问题：OpenClaw dist 升级会覆盖 `dist/control-ui/index.html`，主题注入丢失。
> 解决：注入时留指纹 + 存快照 → 检测到指纹缺失则自动从快照重新注入。
> **自愈闭环 = 注入 + 快照 + cron + 验证，四步缺一不可。**

**实现（注入 → 快照 → 自愈，按顺序全部必做）**：
1. **注入带指纹**：注入的 `<style>` 与 `<script>` 块必须带三个属性——`data-theme-id="<主题名>"`（识别装的哪个主题）、`data-theme-version="<主题版本>"`（主题自身版本）、`data-upstream-version="<注入时的 dist 上游版本>"`（从 OpenClaw `package.json` 的 version 字段读，如 `2026.7.1-2`）；heal.sh 靠前两个判断「当前装的是哪个主题、有没有丢」，靠第三个在重注入前做上游版本比对
2. **快照固定文件名（契约，不许自由发挥）**：快照必须存到 `~/.openclaw/workspace/theme-coach/snapshot/<主题名>/`，且只存这两个文件、文件名固定：
   - `theme-vars.html`：注入到 `</head>` 前的内容（含指纹的 `<style>` 块）
   - `injector.html`：注入到 `</body>` 前的内容（含指纹的 `<script>` 块）
   - 内容必须与注入 index.html 的逐字节一致；目录里**不许留草稿/中间文件**（否则 heal 报 snapshot incomplete 或误灌）
3. **自愈脚本 `scripts/heal.sh`**：自动探测 OpenClaw 安装路径（不硬编码）；检查指纹 → 缺失则从快照恢复；同主题跳过、不同主题明确报出（先 `heal.sh uninstall` 再重灌）；`heal.sh uninstall [主题名]` 卸载还原原版；`--force` 切换时**先验目标快照（目录 + 契约文件 + 指纹全对上）再卸载旧主题**——目标快照缺失/契约违反直接报错退出（exit 非 0），现有主题原样不动；**重注入前比对 `data-upstream-version` 与当前 dist 版本，主版本跳大先警告再注入**（DOM/CSS 钩子可能已变，注入后必须人工验证；样式坏了就按新 dist 重做快照）
4. **当场注册 cron（必做，不是可选项）**：注入验收通过后立即注册每天自检。合并式追加，不覆盖现有 crontab：
   ```bash
   ( crontab -l 2>/dev/null | grep -v 'heal.sh' ; echo '0 6 * * * /bin/bash "<skill 安装目录>/scripts/heal.sh" <主题名> >> ~/.openclaw/workspace/theme-coach/heal.log 2>&1' ) | crontab -
   crontab -l | grep heal.sh   # 确认注册成功
   ```
   > `<skill 安装目录>` 换成 skill 实际路径（在 skill 目录里执行 `pwd` 即得）；`<主题名>` 换成刚注入的主题。改现有 crontab 前必须先 `crontab -l` 看现状。
5. **当场跑一次验证闭环（必做）**：注册完立刻手动执行一次 `bash "<skill 安装目录>/scripts/heal.sh" <主题名>`，输出应为 `[heal] Theme '<主题名>' is present, skipping.`——确认「已注入状态能被自愈脚本正确识别」后闭环才算成立。**只注册不验证 = 没做**；以后可用 `tail ~/.openclaw/workspace/theme-coach/heal.log` 查看每日自检结果
6. **幂等安全**：检测到同主题已注入则跳过，不会重复注入

### 3.2·补 主题切换与还原工作流（与 heal.sh 能力对齐）

> 换主题/还原默认都走 `scripts/heal.sh`，与自愈共用同一套指纹 + 快照机制，不需要手工删注入块。`<skill 安装目录>` = 本 skill 实际安装位置（在 skill 目录里 `pwd` 即得）。

**切换主题（A → B，B 已有快照）**：
1. 先探当前状态：`bash "<skill 安装目录>/scripts/heal.sh" B`——检测到当前装的是 A 会明确报出并退出（不静默覆盖）
2. 用户确认要换 → `bash "<skill 安装目录>/scripts/heal.sh" B --force`（能力细节见 3.2 第 3 条：先验目标快照 → 卸载 A → 注入 B，全程自动备份 + 上游版本比对，此处不再重复）
3. **同步 cron 主题名**：crontab 里 heal.sh 行还带着旧主题 A，必须改成 B，否则每天自检拿错主题误报：
   ```bash
   crontab -l | sed 's#heal.sh" A#heal.sh" B#' | crontab -   # A/B 换成实际主题名
   crontab -l | grep heal.sh   # 确认已更新
   ```
4. Ctrl+Shift+R 强制刷新验收

**还原默认（摘掉主题，回到 OpenClaw 原版 UI）**：
1. `bash "<skill 安装目录>/scripts/heal.sh" uninstall [主题名]`——主题名省略 = 自动检测当前注入的主题；自动备份（`index.html.bak-heal-<时间戳>`）后移除带指纹的 `<style>`/`<script>` 注入块
2. 从 crontab 摘掉对应自愈行（不再每天自检）：
   ```bash
   ( crontab -l 2>/dev/null | grep -v 'heal.sh' ) | crontab -
   ```
3. Ctrl+Shift+R 看回原版 UI

**注意**：uninstall 只摘注入块，不动快照目录（以后想换回来直接 `--force` 秒切）；切换/还原属于改变用户环境的操作，动手前先跟用户确认。

### 3.3 可读性细则
- 气泡纯色底 + 主题色顶条 + 名字主题色
- 背景纹理够暗（浅色主题反向：纹理够浅）；面板用中性纹理
- 半透明元素 `pointer-events: none` 不挡点击

### 3.4 落地验证
1. 备份 index.html
2. 注入器 JS 用 node --check 验证
3. 静态资源 curl 确认可访问
4. 用户强制刷新验收 → 迭代

### 3.5 交付前验证清单（每次交付前显式过一遍）

- [ ] **改前备份**：备份 `dist/control-ui/index.html`，可回滚
- [ ] **node --check**：所有注入器 JS 通过语法校验（node --check 注入.js）
- [ ] **静态资源 HTTP 200**：curl 确认引用的 CSS/字体/纹理资源返回 200（非 404）
- [ ] **强制刷新生效**：改的是静态文件，**Ctrl+Shift+R 强制刷新**即生效，**不用重启网关**
- [ ] 对比度必查配对清单逐对跑 `contrast-check.py`，全部达标
- [ ] 反模式自查：实战反模式清单逐条过

---

## 第四步：风格技术库 + 反模式 + 无障碍

### 风格技术库（数据化：按需从 references/styles/ 加载）

> 每种风格的**技术要点 + 反模式**都拆成独立模板存在 `references/styles/<风格>.md`，SKILL.md 不再内嵌风格数据——**社区加新风格只加一个文件，不用改主文件**。

**加载流程（必做）**：
1. `ls references/styles/` 看当前有哪些风格模板（`TEMPLATE.md` 是新增风格用的空模板）
2. 命中用户要的风格 → **整篇读进来**，技术要点+反模式逐条对照落地
3. 没命中 → 走「第一步·补」调研 + 第五步自助检索，做完可沉淀成新模板（按 `TEMPLATE.md` 复制一份填好）
4. 内置 5 个：`pixel-game`（像素/游戏）/ `cyberpunk`（赛博/霓虹）/ `cartoon-cute`（卡通/可爱）/ `minimal-modern`（极简/现代）/ `dark-tech`（暗色科技）——以 `ls` 实际结果为准

### 反模式清单（跟着风格模板走）

- 每个 `<风格>.md` 自带「反模式」节：用哪个风格就读哪个风格的反模式，逐条自查
- 跨风格通用的坑见下方「实战反模式清单」

### 实战反模式清单（实战踩坑沉淀，跨风格通用）

> 这些是真实踩过的坑，不是泛泛之谈。每次交付前对着自查：

- **渐变气泡丑且影响阅读** → 气泡一律纯色底 + 主题色顶条，**不做气泡渐变**
- **标签背景太亮要反色** → 标签/tool 等标签背景过亮时转反色（深底浅字或浅底深字），保证文字可读
- **测试偏好绝不能进 feedback.json**（⚠️ 红线）→ 测试时改的偏好（如赛博朋克测试色）只是「试」，不是「真喜欢」；只有用户明确表示真正喜欢某风格/配色才落盘，否则污染下次推荐
- **风格越具体越要先调研** → 赛博朋克/MC 等具体风格，先 Web 查权威资料再动手，不靠脑内泛泛认知（见「第一步·补」）

### 无障碍检查（WCAG 2.1 AA）
- **文字对比度**：正常 ≥ 4.5:1，大文字(≥18px bold) ≥ 3:1
- **非文字元素**：UI 组件 ≥ 3:1
- **焦点指示器**：可见且清晰
- **不依赖颜色**：不用纯颜色传达信息
- 对比度计算脚本见 `scripts/contrast-check.py`

### 必查配对清单（对比度检查流程，逐对跑，全过才算达标）

> 只查一对不算数。下面每对文字-背景配对都必须用 `python3 scripts/contrast-check.py <文字色> <背景色> "<标签>"` 跑一遍，全部达标才交付：

| 文字变量 | 背景变量 | 要求 |
|---------|---------|------|
| `--chat-text` | `--bg` | ≥ 4.5:1 |
| `--chat-text` | `--bg-content` | ≥ 4.5:1 |
| `--chat-text` | `--card` | ≥ 4.5:1 |
| `--chat-text` | `--chat-box-inset` | ≥ 4.5:1 |
| `--card-foreground` | `--card` | ≥ 4.5:1 |
| `--accent-foreground` | `--accent` | ≥ 4.5:1 |
| `--accent-foreground` | `--accent-hover` | ≥ 4.5:1 |
| 非文字 | `--border` vs `--bg` | ≥ 3:1（UI 组件） |
| 非文字 | `--border-strong` vs `--bg` | ≥ 3:1（UI 组件） |
| 非文字 | `--border-hover` vs `--bg` | ≥ 3:1（UI 组件） |

- 任一配对不达标：调整该对涉及的变量再跑，不许带着 ❌ 交付
- 大文字场景（≥18px bold）下限 3:1，但默认按 4.5:1 设计更稳
- **border 为 UI 描边，通常需人工微调**：`derive-palette.py` 派生已自动对齐 ≥3:1（贴 3.2 不刺眼），但风格化需要（更低调/更亮的描边、双线边框等）改完后**必须重跑本清单**，确认 `--border`/`--border-strong`/`--border-hover` 对 `--bg` 仍 ≥3:1 才交付

---

## 第五步：自助检索与外部工具（自举）

> 内置工具箱只是兜底。不熟风格/更高还原度时，主动"觅食"。**注意：用户给了具体风格时，这一步（查风格资料）应在设计前就先做（见第一步·补），这里是查字体/纹理/图标/CSS 技巧等实现细节。**

1. web_search 找字体/纹理/图标/CSS 技巧
2. clawhub 搜现成主题 skill 参考
3. 外部命令：PIL 画纹理、ffmpeg 处理、下载脚本
4. 让客户 Agent 自己用这套流程找工具

### 素材指路（帮用户找官方内容 · 所有主题通用）

> 用户要某 IP/风格（Hello Kitty、MC、某游戏、某动画等）时，**默认路径 = 帮用户找到官方/授权素材**（自绘只是兜底，见下）。官方渠道通常自带「个人使用授权」（如 Sanrio 官方壁纸专区、IP 官方素材页），比自绘/野图更贴原版、更好看。

**自绘降级判定（仅在以下情况才自绘）**：① 用户明确要求自绘/原创；② 官方素材不可得（无官方渠道/无授权下载）；③ 用户提供不了可用图。否则一律走官方素材。

**流程**：
1. 查该 IP/风格的**官方素材渠道**：官方壁纸/素材专区、授权图库、正版字体/纹理站（web_search + 直接访问官网确认）
2. 给用户**链接 + 用法说明**（怎么下载、存哪里、怎么自用）
3. 用户下载后把素材放**本地用户目录**（不进 skill 包）
4. skill 用**本地路径引用**把它做成背板/装饰/纹理，完成主题

**边界（红线真正的位置）**：
- ✅ skill 可以**指路**：找渠道、给链接、教用法——这是"帮用户找"，不复制不存储不分发
- ✅ 用户**个人使用**官方素材 = 合理使用（著作权法第 24 条，适用于所有作品，不限一家公司）
- ❌ skill **不搬运**：下载的官方素材**不进 skill 包 / 主题包 / 示范案例 / 仓库**（进包 = 公开分发 = 越界；主题包 assets 只放自绘/已授权素材，用户素材放用户侧目录）

### ⚠️ 安全门槛
- 第三方 skill：verify 来源/签名 → 内容审查（有无外传数据/危险 shell）→ 用户批准 → 装后验证
- 任何一条不过就不装，风险讲清楚
- 不下载执行不明代码；skill 不内置第三方版权素材（示范/打包素材须自绘或已授权）；用户自备素材的发布授权由用户自行确认

---

## 第六步：反馈学习循环

> 不只是一次性顾问，持续学习用户偏好。

**机制**：
1. 每次主题对话结束，记录到**本 skill 目录内 `data/feedback.json`**（统一落点：跟 skill 走，开源/迁移不丢偏好；skill 目录 = 实际安装位置，在目录里 `pwd` 即得）：
   ```json
   {
     "preferences": { "style": "pixel-game", "baseColor": "#7ca843",
       "likes": ["readable-textures", "border-image-buttons"],
       "dislikes": ["gradients"],
       "accessibility": true },
     "history": [ { "theme": "mc-pixel", "date": "2026-08-09", "rating": "positive" } ]
   }
   ```
2. 下次触发 skill 时自动读取 → 优先延续上次风格
3. likes/dislikes 积累 → 推荐越来越精准
4. 用户随时说"忘掉我的偏好"清除

---

## 第七步：发布工程化

### 7.0 主题包结构（交付物标准形态，v1.3.0 起）

> 无论注入到哪个目标（Control UI / 任意 Web 项目），交付物建议打包成标准主题包——它就是「快照的通用化形态」：

```
<主题名>-theme/
├── theme-vars.html   # :root 变量注入块（带 data-theme-id 指纹）
├── injector.html     # 样式注入器（带指纹，见 references/minecraft-example.md）
├── assets/           # 字体/纹理/图标（内置素材须自绘或已授权；用户自备素材放用户侧，不打包）
└── README.md         # 风格说明 + 安装步骤（3.1/3.2·补）+ 对比度实测表
```

- `theme-vars.html` / `injector.html` 与注入目标的内容**逐字节一致**（升级覆盖后靠它重灌）
- Control UI 场景：快照目录（`~/.openclaw/workspace/theme-coach/snapshot/<主题名>/`）就是主题包的本地落点，两者是同一套东西
- 形态 B（静态稿）交付时：主题包换成完整 HTML/CSS 项目，其余标准不变

### 7.1 前端规范
- frontmatter 已置于**本文件最顶部**（name/description/version/emoji/categories/tags），是发布元数据唯一真源；7.1 不再重复贴 YAML，改字段只改顶部
- 发布前按 ClawHub 要求核对 frontmatter 字段完整（尤其 name/description）

### 7.2 发布前清单
- [ ] README.md 含 2-3 张截图
- [ ] node --check 所有注入器 JS 通过
- [ ] 对比度必查配对清单（第四步）全部达标
- [ ] 内置素材授权标注完成（自绘/已授权）；用户自备素材的授权由用户发布时自行确认
- [ ] semver 版本号定好
- [ ] clawhub skill publish --dry-run 预检通过
- [ ] frontmatter 按 Agent Skills 标准自查（name 规则 7 条 / description ≤1024 / 缺 description 不加载），清单+自动化脚本见 `references/open-source-checklist.md`
- [ ] 安全审计：注入代码/素材零外链、字体纹理全部本地化（web 调研/curl 校验属开发期行为，不进注入产物）、无敏感文件读取、无 curl|bash 模式

### 7.3 版本策略
- Patch（1.0.x）：颜色微调、bug 修复
- Minor（1.x.0）：新风格模板、新工具
- Major（x.0.0）：注入架构变更

---

## Checklist（完整执行清单）
- [ ] 问答锁定风格/色彩/氛围/可读性
- [ ] **用户给了具体风格 → 先 web 查该风格资料（视觉特征/字体/反模式/参考案例），产出调研小结再动手**
- [ ] 主色派生产出 :root 令牌（HSL 或 OKLCH；浅色主题用 `derive-palette.py <hex> --light`）
- [ ] 备份 index.html
- [ ] 双保险注入（document 根级 + shadow root）
- [ ] 先读 `references/styles/` 对应风格模板（`ls` 找）；没有→调研+自助检索
- [ ] 反模式自查：该风格要避免的事项逐条过
- [ ] 对比度必查配对清单逐对跑 `contrast-check.py` 全部达标
- [ ] 第三方工具/插件过安全门槛
- [ ] 素材放 assets 并伺服测试；node --check 通过
- [ ] 写入升级自愈快照：`theme-vars.html` + `injector.html` 固定文件名、带 `data-theme-id`/`data-theme-version`/`data-upstream-version` 指纹、目录无草稿
- [ ] **注册 heal cron（必做，合并式追加）+ 当场跑一次 `heal.sh <主题名>` 验证闭环**
- [ ] 切换主题用 `heal.sh <新主题> --force`、还原默认用 `heal.sh uninstall`，切换后同步 cron 主题名（见 3.2·补）
- [ ] 用户强制刷新验收→迭代
- [ ] 记录反馈到本 skill 目录 `data/feedback.json`（统一落点）

---

## 参考文件
- `references/minecraft-example.md`：完整 MC 像素风 Worked Example
- `references/styles/`：风格技术库（每种风格的技术要点+反模式独立模板，含 `TEMPLATE.md` 新风格模板）
- `scripts/derive-palette.py`：HSL 主色派生脚本（实出 20 个 CSS 变量；默认深色，`--light` 亮度反转出浅色版；border 类自动对齐 UI 组件 ≥3:1；非法 hex 友好报错）
- `scripts/contrast-check.py`：WCAG 对比度检查脚本（第四步必查配对清单逐对跑；非法 hex 友好报错）
- `scripts/heal.sh`：升级自愈脚本（heal 自愈 / `--force` 切换 / `uninstall` 还原三用法，自动探测安装路径 + 指纹识别主题 + `--force` 先验目标快照再卸载 + 重注入前上游版本比对；工作流见 3.2·补）
- `test-prompts.json`：达尔文自测用例（6 条：3 happy path + 3 负面/边界——测试偏好红线/模糊输入/切换还原路径），每次改完用其验证流程通不通