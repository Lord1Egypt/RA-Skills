# ski-assistant

Global ski resort assistant for trip planning, pricing, coaching & presale monitoring.
全球滑雪综合服务助手 — 行程规划、智能查价、AI 电子教练、早鸟预售。

## v7.0.0 — Remove Tutorial System + Streamline Architecture

Removed the entire tutorial subsystem to simplify the skill architecture. Coaching module now provides generic practice suggestions instead of referencing tutorial curriculum files.

移除教程子系统，精简技能架构。教练模块的"场景 C"从教程推荐改为通用练习建议，不再依赖课程文件。

Key changes:
- **Removed `modules/tutorial.md`**: Tutorial intent routing removed from SKILL.md
- **Removed `references/tutorial-curriculum/`**: Entire curriculum directory (12 files) removed
- **Coaching module updated**: Scene C now gives generic, actionable practice suggestions based on weak dimensions — no external file dependency
- **Version bump**: 6.0.1 → 7.0.0 (breaking: tutorial functionality no longer available)

核心变更：
- **移除 `modules/tutorial.md`**：SKILL.md 中移除教程意图路由
- **移除 `references/tutorial-curriculum/`**：整个课程目录（12 个文件）移除
- **教练模块更新**：场景 C 改为基于薄弱维度的通用练习建议，无外部文件依赖
- **版本号**：6.0.1 → 7.0.0（破坏性变更：教程功能不再可用）

## v5.3.6 — Complete Tutorial System + Style Branches + DOCX Export

Complete 4-level tutorial system (Level 0-3) × 2 board types (snowboard/ski), with style branches and DOCX export.

Key additions:
- **Level 2-3 tutorials**: 4 new files with advanced techniques
- **Style branches**: Carving/Park/Freeride (snowboard), Carving/Mogul/Freeride (ski)
- **CASI/CSIA terminology**: Full integration (Scheme C) in Level 2+ core skills
- **DOCX export**: Professional Word document generation for tutorials
- **Complete technical tree**: From beginner to expert, all skills covered

完善 4 级别教程体系（Level 0-3）× 2 种板型（单板/双板），含风格分支和 DOCX 导出。

新增内容：
- **Level 2-3 教程**：4 个新文件，含高级技术
- **风格分支**：刻滑/公园/野雪（单板），卡宾/蘑菇/野雪（双板）
- **CASI/CSIA 术语**：Level 2+ 核心技能完整集成（方案 C）
- **DOCX 导出**：专业 Word 文档生成
- **完整技术树**：从零基础到专家，所有技能覆盖

## v5.3.5 — Ski Tutorial System + Complete Technical Framework

New ski tutorial system with 4 levels (0-3) × 2 board types (snowboard/ski), complete technical coverage from beginner to advanced. Features:

- **Complete technical tree**: PSIA-AASI framework + CASI/CSIA terminology reference (Scheme C: PSIA primary, CASI/CSIA supplementary)
- **Separate files by board type**: Snowboard users only see snowboard content, ski users only see ski content
- **Level 0-1 implemented**: 4 tutorial files with full technical coverage (854 resorts, search strategies, structured output, rich user profile, pre-departure, tutorials)
- **International terminology**: Level 2+ will show terminology对照 (PSIA-AASI / CASI / CSIA) for core skills
- **Tutorial-to-coaching loop**: AI coaching scores can recommend specific tutorial chapters for improvement

新增滑雪教程系统，4 个级别（0-3）× 2 种板型（单板/双板），从零基础到高级的完整技术覆盖。特性：

- **完整技术树**：PSIA-AASI 框架 + CASI/CSIA 术语对照（方案 C：PSIA 为主，CASI/CSIA 为辅）
- **按板型分离文件**：单板用户只看单板内容，双板用户只看双板内容
- **Level 0-1 已实现**：4 个教程文件，完整技术覆盖（899 雪场、搜索策略、结构化输出、丰富用户画像、行前提醒、教程）
- **国际术语对照**：Level 2+ 核心技能显示术语对照（PSIA-AASI / CASI / CSIA）
- **教程-教练闭环**：AI 教练评分可推荐对应教程章节进行改进

新增模块：`modules/tutorial.md`、`references/tutorial-curriculum/`（8 个教程文件 + 索引 + 通用内容）

## v5.3.3 — Structured Output + Rich User Profile

All 5 modules now define scenario-based output format templates with mandatory tables, fallback handling, and personalized columns for agent flexibility. Trip planning scoring formula expanded with board_type, style, and experience dimensions (snow_hours, ski_days, mileage). Added National Alpine Skiing Centre (Olympic venue) to resorts_db.

全部 5 个模块定义了基于场景的输出格式模板，含强制表格、兜底处理和个性化列。行程规划打分公式新增板型、风格和雪时/天数/里程维度。新增国家高山滑雪中心（奥运场馆）。

## v5.3.2 — Search Strategies Maintenance

Search strategies maintenance tool, health check & quarterly review workflow.

搜索策略维护工具，健康检查 + 季度复核流程。

## v5.3.1 — 854 Resorts + Search Strategy Engine

854 ski resorts across 40+ countries. Three-layer architecture (instruction + protocol + knowledge). Flyai integration expanded with keyword-search & search-poi. 8-tier price credibility labels. Search strategy engine covering 161 regions.

854 座雪场覆盖 40+ 国。三层架构（指令层+协议层+知识层）。flyai 扩展 keyword-search 和 search-poi。8 级价格可信度标签。搜索策略引擎覆盖 161 个区域。

## Use Cases / 使用场景

Ski enthusiasts need a knowledgeable assistant for trip planning, price comparison, skill improvement, and finding deals. Here's what ski-assistant can do for you:

滑雪爱好者在规划行程、对比价格、提升技术、寻找优惠时，需要一个懂滑雪的助手：

### 1. Where to ski this weekend? / 周末不知道去哪滑？

**Smart recommendation + trip planning — 智能推荐 + 行程规划**

You might ask:
- "周末从北京出发，中级水平，推荐个雪场"
- "Recommend a ski resort near Beijing for beginners this weekend"
- "How much for a 5-day trip to Niseko for 2 people?"
- "去二世谷滑雪要花多少钱？2人5天"

What I'll do: Understand your skill level, budget, and schedule, then match from 854 global resorts using a structured scoring formula. You'll get a complete plan with transport, accommodation, gear checklist, and mountaintop weather forecast.

了解你的水平、预算、时间后，从 854 座全球雪场用结构化打分公式智能匹配，输出包含交通、住宿、装备清单的完整方案，并附带山顶天气预报。

### 2. Lift tickets too expensive? / 雪票太贵？

**Multi-channel pricing + deal hunting — 四路径查价 + 低价捡漏**

You might ask:
- "万龙现在什么价？有没有残票转让"
- "Find discounted lift tickets for Wanlong"
- "飞猪上有什么滑雪套餐？"

What I'll do: Check four channels — flyai keyword-search for Fliggy packages, search-flight/hotel for real-time transport, WebSearch for official ticket prices, social platforms for resale tickets. Automatic currency conversion for international trips. Every price labeled with 8-tier credibility source.

同时查四个渠道 — flyai keyword-search 飞猪套餐、search-flight/hotel 实时交通住宿、WebSearch 官网雪票、社交平台转让票。涉及外币时自动换算。每项价格标注 8 级可信度来源标签。

### 3. Want to improve your technique? / 想提升滑雪技术？

**AI electronic coach — AI 电子教练**

You might ask:
- "帮我看看这张滑雪照片，姿态打个分"
- "Rate my skiing form from this photo"

What I'll do: Analyze your photos/videos across four dimensions (posture, turning, freestyle, overall), highlight strengths and areas for improvement, provide actionable practice suggestions, and track your progress over time.

分析你的照片/视频，按四维度（基础姿态、转弯技术、自由式、综合滑行）打分，指出亮点和改进建议，给出针对性练习方案，并记录进步轨迹。

### 4. When's the best time to buy? / 早鸟票什么时候买最划算？

**Presale monitoring — 预售监听**

You might ask:
- "万龙的早鸟票什么时候开售？帮我盯着"
- "When do early-bird passes go on sale?"

What I'll do: Share historical sale timelines, search for the latest season announcements, and compare single-trip vs multi-day vs season pass value. Add to watchlist for periodic checks and notifications.

告诉你历年开售时间规律，搜索当季最新公告，对比单次票/次卡/季卡的性价比。添加监听后，定期检查并通知你。

### 5. What to pack for an international trip? / 第一次外滑要准备什么？

**Gear guide + travel tips — 装备 + 攻略**

You might ask:
- "去北海道滑雪要带什么装备？"
- "What gear should I bring for a Japan ski trip?"

What I'll do: Based on your level and destination, list essential gear, clothing tips, visa/insurance reminders, local transport options, and cultural notes like onsen etiquette.

根据你的水平和目的地，列出必备装备、穿衣建议、签证/保险提醒、当地交通方式，以及温泉文化等本地贴士。

### 6. Mountain weather check / 查雪场天气

**Summit-level forecasts, not valley-town weather — 必须是山顶的**

You might ask:
- "查一下万龙未来7天的山顶天气"
- "Check the mountaintop weather at Wanlong for the next 7 days"

What I'll do: Query professional weather forecasts at the resort's summit elevation (not the town below), including snowfall, wind speed, visibility, and a ski condition rating.

查询雪场山顶海拔（而非山脚城镇）的专业天气预报，包括降雪量、风速、能见度，并给出滑雪条件评分。

## Quick Start / 快速开始

```bash
clawhub install ski-assistant
```

安装后直接对话即可开始，无需额外配置。Just start chatting — no configuration needed.

## Coverage / 覆盖范围

| Region / 区域 | Resorts / 雪场数 | Countries / 代表国家 |
|---------------|-----------------|---------------------|
| China / 中国 | 470 | 崇礼、北京、东北、新疆、全国 30 省份 |
| Japan / 日本 | 51 | 北海道、长野、新潟、东北 |
| North America / 北美 | 104 | 美国（科罗拉多/犹他/加州）、加拿大（惠斯勒） |
| Europe / 欧洲 | 134 | 法国、瑞士、奥地利、意大利、德国等 |
| Korea / 韩国 | 23 | 江原道平昌、旌善、洪川 |
| Southern Hemisphere / 南半球 | 40 | 新西兰、澳大利亚、智利、阿根廷 |
| Other / 其他 | 32 | 其他欧洲国家、东南亚室内等 |

## Architecture / 架构

v7.0.0 adopts a three-layer architecture:

- **Instruction Layer** (`SKILL.md`): Intent routing, 5 global MUST rules
- **Protocol Layer** (`modules/`): 6 protocol files with MUST/SHOULD/MAY grading, explicit output formats
- **Knowledge Layer** (`references/`): Reference files with pure reference data, no imperative language

Plus:
- **Data Layer** (`data/`): Resort database + search strategy engine
- **Tools Layer** (`tools/`): 5 Python tools with security documentation (incl. strategy maintenance)

v7.0.0 采用三层架构：

- **指令层**（`SKILL.md`）：意图路由，5 条全局 MUST 规则
- **协议层**（`modules/`）：6 个协议文件，MUST/SHOULD/MAY 分级，明确输出格式
- **知识层**（`references/`）：参考文件，纯参考数据，无指令性语言

外加：
- **数据层**（`data/`）：雪场数据库 + 搜索策略引擎
- **工具层**（`tools/`）：5 个 Python 工具，含安全文档（含策略维护工具）

## Search Strategy Engine / 搜索策略引擎

`data/search_strategies.json` covers 161 regions with:

- 11 region strategies (崇礼/东北/新疆/北京/国内其他/日本/韩国/欧洲/北美/南半球/default)
- 16 official WeChat channels for top Chinese resorts
- Fliggy keyword templates for package deals
- flyai search parameters (search-poi, keyword-search)

Each strategy includes websearch keywords, fliggy keywords, flyai parameters, priority level, and season info.

`data/search_strategies.json` 覆盖 161 个区域：

- 11 个区域策略
- 16 个中国头部雪场官方微信公众号渠道
- 飞猪套餐关键词模板
- flyai 搜索参数

## Data Storage / 数据存储

Default: `~/.ski-assistant/` (customizable via `SKI_ASSISTANT_DATA_DIR`). All data stored locally only, never uploaded.
默认 `~/.ski-assistant/`，可通过环境变量自定义。所有数据仅存储在用户本机。



## Changelog

- **v7.0.0** (2026-05-31): Remove tutorial system — deleted `modules/tutorial.md` and `references/tutorial-curriculum/`, coaching Scene C replaced with generic practice suggestions, architecture streamlined to 6 modules
- **v6.0.1** (2026-04-12): Tutorial reading optimization (44% reduction), terminology consistency (刻滑/卡宾), records.json cross-module consistency, 6-round comprehensive verification
- **v6.0.0** (2026-04-11): Progressive Disclosure + Data Deduplication
- **v5.3.6** (2026-04-11): Complete tutorial system + style branches + DOCX export
- **v5.3.5** (2026-04-11): Ski tutorial system (4 levels × 2 board types), complete technical tree, PSIA-AASI + CASI/CSIA terminology, tutorial-to-coaching loop
- **v5.3.4** (2026-04-11): Pre-departure reminder module with dynamic checklist, cron scheduling support
- **v5.3.1** (2026-04-11): Search strategy engine (161 regions), flyai keyword-search + search-poi integration, 8-tier price credibility labels, three-layer architecture refinement
- **v5.3.0** (2026-04-11): Three-layer architecture refactor (SKILL.md 550→115 lines, 5 module protocols, 5 references)
- **v5.2.4** (2026-04-11): ClawHub security audit fix — removed broad `Bash(python3 -c *)` permission
- **v5.2.2** (2026-04-11): International resort database expansion to 854 resorts (40+ countries)
- **v5.1.0** (2026-04-11): Bilingual frontmatter, 304-resort database (27 countries), expanded discovery regions, tightened allowed-tools
- **v5.0.1**: Restricted allowed-tools to specific scripts only
- **v5.0.0**: Knowledge-hub architecture refactor (10 scripts → 4 tools, 86% reduction)
- **v4.4.0**: Fixed ClawHub security review transparency issues
- **v4.3.0**: Local usage statistics
- **v4.2.0**: XHS sharing + international packages + price trends
- **v4.0.0**: 155-resort database + OSM discovery + mountain weather

## License

MIT
