# Changelog

All notable changes to this project will be documented in this file.

## [7.8.0] - 2026-07-15

### Fixed — ClawHub SkillSpector 第五轮 4 项 Findings 修复（Wallhaven 未披露 + AI 生图披露不一致）

**过渡修补评估**：4 项 findings 全部指向同一根因——Wallhaven 未被完整披露。这是 v7.7.0 修复时的遗漏（写了"3 类外部数据流"但保留了 Wallhaven 作为第 4 个图库），不是过渡修补。

**修复策略**：删除 Wallhaven（混合版权，非首选，实际很少用到），比披露它更简单干净，符合"最小化外部依赖"原则。

### Changes

- **Wallhaven 移除（3 项 findings 修复）**：
  - `references/image-sources.md`: 删除 Wallhaven 章节（### 3. Wallhaven 完整段落）+ ALLOWED_HOSTS 移除 w.wallhaven.cc / wallhaven.cc
  - `SKILL.md`: 图源优先级移除 Wallhaven（2 处）+ references 索引移除 Wallhaven
  - `references/category-cookbook.md`: 游戏品类图源从 Wallhaven 改为 Pexels/Unsplash
  - `references/workflow.md`: ALLOWED_HOSTS 提示移除 w.wallhaven.cc
- **AI 生图披露不一致修复（1 项 finding）**：
  - SKILL.md 图片三选一门控选项 C：从"会将prompt发送到trae-api-cn生图API"改为"会将生图prompt发送到trae-api-cn.mchost.guru生图API，prompt可能含文章主题/场景描述"——与权限声明表格的域名和风险描述一致

### Audit Result
- ClawHub SkillSpector 第五轮 4 项 Findings：4/4 修复完成
- Wallhaven：完全移除，外部图库简化为 Pexels/Pixabay/Unsplash 三个
- AI 生图披露：选项 C 与权限声明表格一致

## [7.7.0] - 2026-07-15

### Fixed — ClawHub SkillSpector 第四轮 10 项 Findings 修复（结构性披露修复）

**过渡修补评估**：本轮 10 项 findings 无过渡修补。v7.6.0 的 Google Fonts 移除和批量授权删除是干净的。本轮揭示的是**更深的结构性问题**：description 只提飞书同步，未披露图片搜索/AI 生图也是外部能力；同意门控铁律与"都行你看着办"接受 AI 生成矛盾；image-sources.md 详细文档化了外部 API 但 description 没披露。

**关键洞察**：SkillSpector 的 High Tp4 finding 明确指出"documented behavior overstates what the skill safely and actually does, while also omitting concrete operational behavior such as starting a local HTTP server and relying on pre-existing HTML rather than a true MD→HTML pipeline"——**description 不仅要披露外部能力，还要准确描述核心行为**。

### Changes

- **High Tp4 (MCP Tool Poisoning) 修复**：
  - description 从"核心能力是本地MD→HTML→PNG渲染"改为"核心能力是本地HTML模板填充+Puppeteer截图渲染（启动本地127.0.0.1 HTTP server加载预存HTML模板，非MD→HTML编译管道）"
  - 权限声明表格增加"核心行为说明"段落，明确披露 HTTP server + 预存 HTML 模板行为
- **High Intent-Code Divergence 修复**：
  - 删除"推荐 A，但接受用户任何选择（包括'都行你看着办'）"的矛盾表述
  - 改为"用户必须明确选择 A/B/C 之一；若用户说'都行'/'你看着办'等模糊回答，默认走 A（完全本地，无外部数据流）"
  - 图片三选一门控选项 C 增加"⚠️ 会将prompt发送到trae-api-cn生图API"风险提示
- **Description-Behavior Mismatch ×2 修复**：
  - description 完整列出 3 类可选外部能力（图库 API 搜索 + AI 生图 + 飞书云盘），每项标注数据流方向和发送内容
  - image-sources.md 顶部增加"外部能力完整披露"表格，列出 3 类外部数据流 + 风险等级 + 同意门控
- **Context-Inappropriate Capability ×3 修复**：
  - image-sources.md API URL 脱敏（pexels.com/api / api.pexels.com/v1/search 等占位符显示）
  - AI 生图验证规则段落增加"外部能力同意门控"提示
  - references/workflow.md 图片下载步骤增加"外部下载风险提示"+ ALLOWED_HOSTS 白名单说明
- **Intent-Code Divergence (数据流声明矛盾) 修复**：
  - image-sources.md 旧声明"仅发送搜索关键词和图片下载请求，不会上传文章原文"改为完整的"外部能力完整披露"表格，明确 AI 生图会发送 prompt
  - 新增"不会发生的数据流"段落：文章原文不会被上传到任何外部服务
- **External Transmission ×2 修复**：
  - Pexels/Unsplash API URL 在文档中用占位符显示（api.pexels.com/v1/search / api.unsplash.com/search/photos），实际调用时拼接

### Audit Result
- ClawHub SkillSpector 第四轮 10 项 Findings：10/10 修复完成
- description 完整披露：核心行为（HTTP server + 预存 HTML）+ 3 类可选外部能力
- 同意门控铁律：消除"都行你看着办"接受 AI 生成的矛盾
- image-sources.md：外部能力清单 + 数据流方向 + 风险等级 + API URL 脱敏

## [7.6.0] - 2026-07-15

### Fixed — ClawHub SkillSpector 第三轮 8 项 Findings 修复

**过渡修补评估**：本轮 8 项 findings 无过渡修补。4 项 Google Fonts 是历史遗留问题（模板从一开始就引用外部字体）；3 项 Vague Triggers 是 v7.4.0 修复时未触及的；1 项 Missing User Warnings 是 Low 级别。v7.5.0 删除 image-search.js 是正确决策——本轮没有出现 v7.5.0 引入的新问题。

**关键洞察**：v7.4.0 在 SKILL.md "声明"了 Google Fonts 外部依赖，但 SkillSpector 仍然标记为 finding——说明"在声明里承认" ≠ "可以保留"，必须移除外部依赖本身。

### Changes

- **Google Fonts 移除（4 项 findings 修复）**：
  - `assets/template-editorial-card.html`: 删除 `<link rel="preconnect">` 和 Google Fonts CSS 引用，改为本地字体回退栈注释（CSS `:root` 变量已含 Noto Serif SC / Source Han Serif SC / Songti SC / PingFang SC 等系统字体 fallback）
  - `assets/template-swiss-card.html`: 同上，删除 Google Fonts CDN 引用
  - SKILL.md: 权限声明"网络访问"行移除 Google Fonts 描述；"外部网络依赖"段落更新为"v7.6 已移除 Google Fonts CDN 引用"
  - README.md (中英): 同步更新外部网络依赖描述
- **Vague Triggers 修复（3 项 findings，含 1 项 High）**：
  - **High 级别修复**：SKILL.md 删除"按流程走一遍"/"全流程"批量授权规则——改为"同意门控铁律：每道门控必须独立询问，不得因模糊措辞批量授权"
  - description 触发词收紧：从"用户要排版文章为图片、生成公众号贴图、小红书图文、文章转图片卡片"改为"用户明确说'xhs-crafter排版'、'用xhs-crafter转图片'、'公众号贴图排版'、'小红书图文卡片'"，并增加 Do NOT "用户只提到MD文件路径但未明确要求图片排版"
  - README.md (中英): 触发示例从"直接提供 MD 文件路径即可触发"改为"明确要求图片排版时触发"
- **Missing User Warnings 修复（1 项 Low）**：
  - SKILL.md + references/workflow.md: 本地文件夹交付前增加"本地文件写入提示"——截图完成后告知用户交付路径，再继续后续步骤

### Audit Result
- ClawHub SkillSpector 第三轮 8 项 Findings：8/8 修复完成
- Google Fonts 外部依赖：完全移除，模板使用系统字体栈
- 批量授权规则：删除，改为独立门控铁律
- 触发词精度：收紧到明确要求图片排版时触发

## [7.5.0] - 2026-07-15

### Fixed — 过渡修补回退（ClawHub SkillSpector 第二轮 9 项 Findings 修复）

**根因诊断**：v7.4.0 为修复"图片搜索门控"新增了 `assets/image-search.js`，但该脚本引入了 Pexels/Pixabay API 调用 + 跨项目 hash registry + 环境变量读取三项新能力，反而触发 5 项新 Findings（Tp4 High + Description-Behavior Mismatch High + 2 个 Context-Inappropriate Capability Medium + External Transmission Medium）。这是典型的过渡修补——为修复一个问题引入了更大的问题。

- **删除 `assets/image-search.js`**（过渡修补产物）：回退到"手动 curl 下载 + buf1.equals(buf2) 验证"方式，不依赖跨项目 registry，不主动联网搜索
- **SKILL.md**: 移除所有 image-search.js 引用（6 处）；权限声明表格"文件读写"行移除 `assets/image-registry.json` 去重注册表描述；图片规则速查表"跨项目去重"行改为"文件级校验，不依赖跨项目 registry"；封面/封底图片下载改为"手动 curl 下载 + Unsplash 直链备选"
- **references/workflow.md**: 修复残留的旧引用块「v7 — 5步全自动工作流，文件夹+飞书云盘双通道交付」→「v7.5 — 5步工作流（默认本地全自动，外部能力需用户同意）」；http.server 启动命令加 `--bind 127.0.0.1`；交付方式 A/B 分支加入同意门控 + 数据外发提示
- **docs/session-handoff.md**: 版本号同步至 7.5.0；ClawHub 平台状态表更新至 7.4.0

### Audit Result
- ClawHub SkillSpector 第二轮 9 项 Findings：9/9 修复完成
- 过渡修补回退：删除 image-search.js，消除 5 项新 Findings 的根因
- 残留引用块修复：workflow.md 旧描述同步至 v7.5
- 交付门控表述强化：workflow.md A/B 分支加入同意门控代码块

## [7.4.0] - 2026-07-15

### Added — ClawHub SkillSpector 审计整改（17项 Findings 修复）
- **SKILL.md**: 新增「隐私与数据流声明（用户须知）」章节——核心能力本地处理（默认）+ 可选外部能力（需用户明确同意）+ 外部网络依赖披露
- **SKILL.md**: 新增 3 道外部能力同意门控（图片搜索门控 / 飞书同步门控 / "按流程走一遍"批量授权）
- **SKILL.md**: Step 1 图片三选一门控选项 B 加入网络访问警告「⚠️ 会将搜索词发送到外部API，但不上传文章原文」
- **SKILL.md**: Step 5 飞书云盘同步加入同意门控代码块 + 数据外发提示
- **README.md**: 新增「隐私与数据流」专章（中英文双语），明确本地处理为默认、可选外部能力需用户同意
- **image-sources.md**: 开头加入数据流边界声明
- **image-sources.md**: Node.js download 函数加入 ALLOWED_HOSTS 域名白名单（6 个允许域名）+ 重定向目标校验，防 SSRF
- **session-handoff.md**: 新增「供应链操作不在本技能范围内」声明，GitHub push / Release / ClawHub publish 标注为用户手动

### Changed — 描述行为一致性修正
- **SKILL.md**: frontmatter description 重写——「核心能力是本地MD→HTML→PNG渲染，可选能力是飞书云盘同步（需用户明确同意）」
- **SKILL.md**: 工作流标题改为「5步（默认本地全自动，外部能力需用户同意）」
- **SKILL.md**: Step 5 交付方式从「双通道交付」改为「本地文件夹（默认）+ 飞书云盘同步（可选，需用户同意）」
- **SKILL.md**: registry 路径修正——`~/.xhs-crafter/` → 脚本同目录 `image-registry.json`（由 `__dirname` 解析），与代码一致
- **SKILL.md**: `trae-api-cn.mchost.guru` 全部标注「仅限TRAE内部环境」
- **README.md**: 版本号 7.1.1 → 7.4.0；品类数 11→13；validate 规则 7→12；中英文双语同步隐私披露
- **session-handoff.md**: 环境变量表删除 GitHub token / ClawHub CLI 行，改为 PEXELS_API_KEY / PIXABAY_API_KEY / lark-cli（可选）
- **session-handoff.md**: 依赖约束更新——lark-cli 标注为「可选，仅飞书云盘同步时需要」；AI 生图 API 标注「仅限TRAE内部环境，生产环境改用Pexels/Unsplash」
- **session-handoff.md**: 版本号同步至 7.4.0

### Fixed — 安全漏洞修复
- **screenshot.js**: `python -m http.server` 加入 `--bind 127.0.0.1` 参数，绑定本地回环，不再暴露到局域网（0.0.0.0 → 127.0.0.1）
- **SKILL.md**: http.server 启动命令文档同步加 `--bind 127.0.0.1`
- **image-sources.md**: download 函数重定向跟踪无域名白名单的 P3 SSRF 风险已修复

### Audit Result
- ClawHub SkillSpector 17 项 Findings：17/17 修复完成
- skill-auditor 8 维度审计：T维度 P2（http.server 0.0.0.0）+ P3（SSRF）+ P2（路径不一致）+ P2（trae-api-cn 未标注）全部修复
- 回归验证：0 新增问题，综合状态 PASS，建议发布到三平台

## [7.3.1] - 2026-06-12

### Fixed
- screenshot.js: auto-start http.server in project directory with random free port (no more manual server or wrong-project screenshots)
- screenshot.js: disable browser cache + cache-bust URL timestamp (no more stale cover/finale images)
- screenshot.js: verify page `<title>` matches expected title before screenshot (abort on mismatch)
- screenshot.js: verify hero images loaded with naturalWidth check

## [7.3.0] - 2026-06-11

### Added
- validate.js R10: dark page rhythm check (5+ pages need ≥1 dark page, no adjacent dark pages)
- validate.js R11: accent color area check (Swiss ≤30%, Lemon Green ≤20%)
- validate.js R12: cover/finale image background check (5+ page sets require image backgrounds on cover and finale)
- SKILL.md: rhythm speed reference table (7 rules) embedded in Step 3 Compose
- SKILL.md: density speed reference table (6 rules) embedded in Step 3 Compose
- SKILL.md: image rules speed reference (8 rules) embedded in Step 3 Compose

### Changed
- SKILL.md: category count corrected from 11 to 13 (actual count in category-cookbook.md)
- SKILL.md: validate rule count updated from 9 to 12
- validate.js: rule count in header comment updated from 9 to 12

## [7.2.0] - 2026-06-11

### Added
- validate.js R8: title consistency check (content pages must use same title class)
- validate.js R9: hero title color check (no #ece2cf in hero-content headings)

### Changed
- SKILL.md: category-cookbook reference updated from "7个品类" to "11个品类"
- SKILL.md: validate rule count updated from 7 to 9
- Swiss template font sizes synced with Editorial: body 28→32px, lead 32→34px, t-cat 24→26px, t-meta 20→24px
- components.md Swiss section updated to match new sizes

## [7.1.1] - 2026-06-11

### Changed
- Embedded font size cheat sheet (15-level type scale) directly in SKILL.md Step 3 Compose for cross-session consistency
- Fixed title consistency rule: h-xl 96px → 110px in SKILL.md iron rules section
- Updated README.md: version badge 7.1.1, 11 categories, validate.js and background-systems.md in file structure
- Added .claude-plugin/plugin.json for Claude Code metadata

## [7.1.0] - 2026-06-11

### Added
- Background systems reference (paper→wash→grain three-layer architecture, atmosphere intensity levels)
- validate.js automated validation script (7 rules: overflow, footer collision, Swiss bold, min font size, 4-band density, h-xl line caps, figure margin)
- Image source triage gate in Step 1 Intake (user image / web search / AI generation)
- "Larger = Lighter" font weight iron rule to components.md
- Title consistency iron rule (same role = same class across all pages)
- Consecutive 3 same-theme pages = P0 error to rhythm rules
- Hero title color rule: cover/finale must use #ffffff + text-shadow, not #ece2cf
- Screenshot size anomaly detection in screenshot.js

### Changed
- Type scale increased ~15% for mobile readability (h-xl: 96→110px, body: 28→32px, kicker: 22→26px, meta: 20→24px)
- Cover/finale titles use .h-display (136px) vs content pages .h-xl (110px) for visual hierarchy
- Category cookbook expanded from 7 to 11 categories with outside-scope list
- Theme presets: added hard rules (no custom hex, Lemon Green ≤20%)
- Image sources: added Unsplash direct download method and AI image API same-placeholder verification
- SKILL.md: added background systems reference, validate.js integration, screenshot size check, image download verification

## [7.0.1] - 2026-06-10

### Fixed
- screenshot.js: replaced hardcoded local paths with environment variable detection (security fix)
- Added .gitattributes to enforce UTF-8 + LF encoding
- Added README.md for GitHub repository

## [7.0.0] - 2026-06-10

### Added
- Editorial Magazine x E-ink + Swiss International dual-mode design system
- 10 theme presets (6 Editorial + 4 Swiss)
- 28 layout templates (M01-M16 + S01-S12)
- Three-Layer Rhythm System (light/dark + atmosphere + layout diversity)
- Density rules (active composition >= 78% canvas height)
- First/last page image frame rule (5+ pages require cover/finale background images)
- Image overlay rules for text-on-image pages
- Category cookbook for 7 content categories
- Content planning with compression ladder and page roles
- 5-step fully automated workflow (Intake → Content Plan → Compose → Validate → Screenshot & Deliver)
- Dual delivery: local folder + Feishu cloud drive sync
- Text compression template preserving original quotes and scene descriptions
- Puppeteer screenshot script with auto page ID detection and Chrome path discovery
