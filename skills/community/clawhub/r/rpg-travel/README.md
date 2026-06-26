# RPG Travel — Game Pilgrimage Planner

**English** | [中文](#中文说明)

---

## Overview

**RPG Travel** maps game scenes to real-world travel itineraries. Users input a game name, AI automatically extracts filming locations/prototype sites, fills in real flight/hotel/attraction data via FlyAI, and generates RPG-style adventure maps and questbooks.

### Core Value

- **Game × Travel Crossover**: Turn game filming locations into real travel destinations
- **RPG Immersive Experience**: Flights = Portals, Hotels = Save Points, Attractions = Main Dungeons, Food = Healing Items
- **One-Click Purchase**: Every bookable item includes a Fliggy purchase link
- **30-Second Generation**: Pre-generated HTML template, AI only replaces data

---

## Dependencies

### Required Tools

| Tool | Purpose | Check | Notes |
|------|---------|-------|-------|
| **FlyAI CLI** | Query real flight/hotel/attraction/food data | `flyai --version` | Requires FlyAI platform account, credentials configured by user |
| **Python 3** | Run `generate_map.py` to generate HTML + questbook | `python3 --version` (≥3.9) | macOS `python` may point to python2, must use `python3` |
| **websearch / webfetch** | Search game filming locations, background images | Built-in AI tools | webfetch may return 403, try multiple sources |

### Quick Environment Check

```bash
bash scripts/setup.sh
```

### FlyAI Commands

```bash
# Flight search
flyai search-flight --origin "Departure" --destination "Destination" --dep-date "YYYY-MM-DD" --sort-type 3

# Hotel search
flyai search-hotels --dest-name "Destination" --check-in-date "YYYY-MM-DD" --check-out-date "YYYY-MM-DD" --sort "rate_desc"

# Attraction search
flyai search-poi --city-name "City Name"

# General search (food/experiences)
flyai fliggy-fast-search --query "Search term"
```

### Background Image Sources

| Priority | Source | Use Case |
|----------|--------|----------|
| 1 | **Steam API** | Game on Steam | `store.steampowered.com/api/appdetails?appids={appid}` |
| 2 | **PlayStation Store** | PS exclusive or PS-first release | `playstation.com/{region}/games/{game}/` |
| 3 | **HDQWalls** | Popular game wallpapers | `images.hdqwalls.com/wallpapers/{slug}.jpg` |
| 4 | **PAKUTASO** | Japan location stock photos | `user0514.cdnw.net/shared/img/thumb/{id}.jpg` |
| 5 | **Wikimedia** | Fallback | `upload.wikimedia.org/...` |
| 6 | **CSS Solid Color** | Last resort | `var(--bg)` dark background |

---

## Directory Structure

```
rpg-travel/
├── SKILL.md                    # Main skill file (English, AI instructions)
├── SKILL.zh.md                 # Chinese version (reference)
├── README.md                   # This file
├── clawhub.json                # Package metadata (dependencies, credentials, privacy)
├── scripts/
│   ├── __init__.py
│   ├── generate_map.py         # Main entry: argument parsing + orchestration
│   ├── models.py               # Data models + configuration + utilities
│   ├── html_generator.py       # HTML generation: template/style/grid/locations
│   ├── node_builder.py         # Node cards: combat/rest/shop/transport/plot
│   ├── text_generator.py       # Text questbook generation
│   └── setup.sh                # Dependency check script
├── references/
│   ├── pixel-map-template.md   # HTML adventure map template
│   ├── output-format.md        # Text questbook output format
│   ├── style-mapping.md        # Game style mapping table
│   ├── fliggy-links.md         # Fliggy link generation rules
│   ├── game-locations.md       # Common game filming locations quick reference
│   └── flyai-commands.md       # FlyAI command detailed parameters
└── assets/                     # Reserved: images, icons, etc.
```

---

## Usage

### Trigger

Users trigger by:
- Entering a game name: "Sekiro", "Ghost of Tsushima", "The Witcher 3"
- Descriptive requests: "Travel following games", "Game location pilgrimage", "Where was XX game filmed"

### Workflow

```
User enters game name
    ↓
Collect preferences (departure city / player level / budget / style)
    ↓
Calculate travel dates and confirm
    ↓
Search game filming locations (web_fetch)
    ↓
FlyAI fills real data (flights/hotels/attractions/food)
    ↓
Map to RPG elements
    ↓
Assemble JSON → call generate_map.py
    ↓
Output: Questbook .txt + Adventure Map .html
```

### Key Commands

```bash
# FlyAI data queries
flyai search-flight --origin "Hangzhou" --destination "Sapporo" --dep-date "2026-04-11" --sort-type 3
flyai search-hotels --dest-name "Sapporo" --check-in-date "2026-04-11" --check-out-date "2026-04-15"
flyai search-poi --city-name "Hokkaido"
flyai fliggy-fast-search --query "Hokkaido food"

# Generation script (two modes, must use python3)
python3 scripts/generate_map.py --data input.json
echo '{"game_name":"..."}' | python3 scripts/generate_map.py --stdin
```

---

## Style System

9 visual styles, auto-matched by game type or user-selected:

| Style | Suitable Games | CSS Key |
|-------|---------------|---------|
| In-Game UI | Universal (strongest immersion) | `game-ui` |
| Travel Journal | Universal (default) | `travel-journal` |
| Vintage Parchment | Witcher 3, Elder Scrolls | `parchment` |
| Modern Minimal Cards | Urban/modern games | `minimal-card` |
| Pixel Retro | Mario, Stardew Valley | `pixel-retro` |
| Neon City | GTA, Cyberpunk 2077 | `neon-city` |
| Japanese Samurai | Ghost of Tsushima, Sekiro | `japanese` |
| Chinese Ancient | Black Myth, Genshin·Liyue | `chinese` |
| Sci-Fi Future | Mass Effect, Starfield | `scifi` |

See [references/style-mapping.md](references/style-mapping.md).

---

## Fallback Mechanisms

### Background Image Fallback

| game_type | Priority 1 | Priority 2 | Priority 3 | Fallback |
|-----------|-----------|-----------|-----------|----------|
| japanese | Steam AppID 1325200 (Nioh 2) | HDQWalls wallpapers | PAKUTASO Japan | Himeji Castle Wikimedia |
| western | Steam AppID 292030 | HDQWalls wallpapers | Wikimedia | Gdańsk Old Town |
| chinese | Steam AppID 2358720 | HDQWalls wallpapers | Wikimedia | Zhangjiajie |
| cyberpunk | Steam AppID 1091500 | HDQWalls wallpapers | Wikimedia | Tokyo Night |

> ⚠️ When game is not on Steam (e.g., Ghost of Yotei), `_get_bg_image()` will fail. AI should actively search HDQWalls, PlayStation Store, etc., and manually replace the background URL in HTML.

### Other Fallbacks

| Situation | Handling |
|-----------|----------|
| Insufficient location info | Downgrade message, provide possible locations |
| Location no longer exists | Mark "⚠️ Scene no longer exists, similar ones nearby" |
| Purely fictional game | Explain fiction, provide inspiration source city |
| Flights/hotels unavailable | Mark "⚠️ No data", provide alternatives |
| Budget exceeded | Script marks "⚠️ Budget alert", AI provides saving options |

---

## Security & Privacy

### Runtime Dependencies
- **Python 3** (≥3.9): Runs `generate_map.py` generation scripts
- **FlyAI CLI**: Third-party CLI for flight/hotel/attraction data. Requires user-installed and configured credentials
- This skill does not install additional system dependencies or modify global configurations

### Credential Management
- FlyAI CLI requires user-configured credentials (API key or account)
- This skill does not store or transmit any user credentials
- Recommended to run in an isolated environment

### Local Output
- Scripts generate HTML/TXT files in the current working directory only
- Does not write to system directories or modify other files
- Output files may contain user-provided itinerary information

### External Data Sources
- Scripts fetch images from: Steam API, HDQWalls, PAKUTASO, Wikimedia Commons
- All image requests are read-only GET/HEAD, no user data uploaded
- Fliggy purchase links are public URLs, no privacy involvement
- ⚠️ **Network Exposure**: Generated HTML embeds external image URLs. Opening the HTML in a browser causes GET requests to third-party servers (Steam, HDQWalls, PAKUTASO, Wikimedia), potentially revealing your IP and User-Agent. For privacy, download images locally before opening HTML.

### Copyright
- Game plot summaries and dialogues in node cards are AI-generated from game content, for reference only
- Game screenshots are copyrighted to original game developers/publishers, for personal travel planning only
- Evaluate copyright risk for commercial use

---

## Known Limitations

- FlyAI flight search may return multi-segment connecting flights requiring manual `flight_no`拼接
- Steam API may timeout in China network, multi-source fallback configured (HDQWalls → PAKUTASO → Wikimedia → CSS)
- Some attractions/food may lack `picUrl`, script skips image rendering
- `search-poi` may return empty results (e.g., Hokkaido), fallback to `fliggy-fast-search`
- `librarian` agent may timeout or get 403, fallback to AI self-search
- macOS `python` may point to python2, must use `python3`
- When game is unreleased or not on Steam, script cannot auto-fetch screenshots, AI must manually search and replace

---

---

# 中文说明

## 概述

**RPG Travel** 是一个游戏圣地巡礼技能，将游戏中的虚拟世界映射到现实旅行行程。用户输入游戏名，AI 自动提取取景地/原型地点，用 FlyAI 填充真实航班、酒店、景点数据，生成游戏风格的冒险地图和 RPG 任务书。

### 核心价值

- **游戏 × 旅行跨界**：把游戏取景地变成真实旅行目的地
- **RPG 沉浸式体验**：航班=传送门、酒店=存档点、景点=主线副本、美食=回血道具
- **一键购买**：每个可预订项都附带飞猪购买链接
- **30秒生成**：预生成 HTML 模板，AI 只替换数据，不手写结构

## 工具依赖

| 工具 | 用途 | 检查方式 | 注意事项 |
|------|------|---------|---------|
| **FlyAI CLI** | 查询真实航班/酒店/景点/美食数据 | `flyai --version` | 需要 FlyAI 平台账号认证 |
| **Python 3** | 运行生成脚本 | `python3 --version`（≥3.9） | 必须用 `python3` |

### 快速检查环境

```bash
bash scripts/setup.sh
```

## 使用方式

**触发**：输入游戏名或描述性请求（"跟着游戏去旅行"、"游戏圣地巡礼"）

**工作流程**：
```
输入游戏名 → 收集偏好 → 推算日期 → 搜索取景地 → FlyAI 填充数据 → 映射 RPG 元素 → 生成输出
```

## 风格系统

| 风格 | 适用游戏 | CSS 变量名 |
|------|---------|-----------|
| 游戏内UI风 | 通用 | `game-ui` |
| 旅行手账风 | 通用（默认） | `travel-journal` |
| 复古羊皮纸 | 巫师3、上古卷轴 | `parchment` |
| 现代极简卡片 | 都市/现代游戏 | `minimal-card` |
| 像素复古 | 马里奥、星露谷 | `pixel-retro` |
| 都市霓虹 | GTA、赛博朋克2077 | `neon-city` |
| 和风武士 | 对马岛、只狼、羊蹄山 | `japanese` |
| 中国古风 | 黑神话、原神·璃月 | `chinese` |
| 科幻未来 | 质量效应、星空 | `scifi` |

## 安全与隐私

- **凭据**：FlyAI CLI 凭据由用户自行配置，技能不存储或传输
- **输出**：仅在当前目录生成 HTML/TXT 文件
- **网络暴露**：HTML 嵌入外部图片 URL，打开时会向第三方服务器发起请求
- **版权**：游戏内容仅供参考，商业使用请自行评估风险

## 已知限制

- Steam API 在国内可能超时，已配置多源兜底
- FlyAI 中转航班需手动拼接航班号
- 游戏未上架 Steam 时需手动搜索截图
