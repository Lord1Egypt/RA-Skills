# StylePilot

StylePilot：个人衣橱助手（Personal Wardrobe Assistant）。  
用于管理衣橱、生成穿搭建议，并通过显式反馈（like/dislike/neutral）持续优化推荐结果。

**English:** StylePilot is a local-first personal wardrobe assistant. It stores clothing metadata in SQLite, suggests outfits by scene, weather, and trip length, and improves ranking over time using explicit feedback (like / dislike / neutral). See **English** below for a full introduction.

## 功能概览

- 衣橱管理：添加、查看衣服（本地 SQLite）
- 穿搭推荐：按场景、天气、天数生成方案
- 出行打包：自动生成旅行携带清单
- 显式反馈加权：根据历史反馈重排推荐候选
- JSON 契约：命令支持 `--json`，便于集成

## 项目结构

```text
style-pilot/
├── SKILL.md
├── run.sh                 # 可选入口，与 wardrobe.py 等价
├── scripts/
│   ├── wardrobe.py
│   └── db.py
├── tests/
│   ├── test_wardrobe_smoke.py
│   └── test_season_rank.py
└── data/                  # 运行后自动生成/使用（被 gitignore 忽略）
```

## 环境要求

- Python 3.9+
- macOS / Linux / Windows（命令示例使用 `python3`）

## 快速开始

```bash
# 1) 初始化数据库
python3 scripts/wardrobe.py init

# 2) 添加衣服
python3 scripts/wardrobe.py add \
  --name "蓝色牛仔外套" \
  --category "外套" \
  --color "蓝色" \
  --season "春" \
  --style "休闲"

# 3) 查看衣橱
python3 scripts/wardrobe.py list --limit 50

# 4) 生成搭配
python3 scripts/wardrobe.py outfit --scene today --weather "25°C晴天"
```

## JSON 模式（推荐集成方式）

```bash
python3 scripts/wardrobe.py list --limit 50 --json
python3 scripts/wardrobe.py outfit --scene commute --weather "18°C多云" --json
```

`outfit --json` 关键字段：

- `outfit_id`: 本次搭配记录 ID
- `selected_items`: 本次选中的衣服
- `missing_categories`: 缺失关键品类
- `preference_applied`: 是否应用了显式反馈加权
- `preference_reasons`: 每件衣服的加权解释

## 显式反馈加权（Layer 1）

生成搭配后，使用 `outfit_id` 写入反馈：

```bash
python3 scripts/wardrobe.py feedback \
  --outfit-id "<outfit_id>" \
  --feedback like \
  --note "适合通勤" \
  --json
```

反馈值：

- `like`
- `dislike`
- `neutral`

系统会在下次推荐时基于历史显式反馈进行重排（单品/颜色/风格/品类）。

## 测试

```bash
python3 tests/test_wardrobe_smoke.py
```

## 触发与边界（简述）

- 仅在用户明确请求搭配建议时激活
- 不主动触发，不在闲聊场景误触发
- 英文触发场景也已支持（详见 `SKILL.md`）

---

## English

### Overview

StylePilot helps you manage a personal clothing database and get outfit suggestions. Everything runs locally: data is stored in SQLite under `data/` (ignored by Git). A Python CLI (`scripts/wardrobe.py`) supports human-readable output and `--json` for agents and integrations.

### Features

- **Wardrobe CRUD**: add and list items (category, color, season, style, occasion, optional image path)
- **Outfits**: recommendations by scene, weather string, and optional trip days
- **Travel packing**: packing-style lists for multi-day trips
- **Explicit feedback**: `like` / `dislike` / `neutral` on past outfits to re-rank future candidates
- **JSON contract**: pass `--json` on commands for machine-readable output

### Project layout

```text
style-pilot/
├── SKILL.md
├── run.sh                 # optional entrypoint (same CLI as wardrobe.py)
├── scripts/
│   ├── wardrobe.py
│   └── db.py
├── tests/
│   ├── test_wardrobe_smoke.py
│   └── test_season_rank.py
└── data/                  # created at runtime (gitignored)
```

### Requirements

- Python 3.9+
- macOS / Linux / Windows (examples use `python3`)

### Quick start

```bash
python3 scripts/wardrobe.py init
python3 scripts/wardrobe.py add \
  --name "Blue denim jacket" \
  --category "外套" \
  --color "blue" \
  --season "spring" \
  --style "casual"
python3 scripts/wardrobe.py list --limit 50
python3 scripts/wardrobe.py outfit --scene today --weather "25°C sunny"
```

You can also use `./run.sh` from the repo root with the same arguments as `wardrobe.py` (see `SKILL.md`).

### JSON mode

```bash
python3 scripts/wardrobe.py list --limit 50 --json
python3 scripts/wardrobe.py outfit --scene commute --weather "18°C cloudy" --json
```

Notable `outfit --json` fields: `outfit_id`, `selected_items`, `missing_categories`, `preference_applied`, `preference_reasons`.

### Feedback (Layer 1)

```bash
python3 scripts/wardrobe.py feedback \
  --outfit-id "<outfit_id>" \
  --feedback like \
  --note "works for commute" \
  --json
```

Allowed values: `like`, `dislike`, `neutral`.

### Tests

```bash
python3 tests/test_wardrobe_smoke.py
python3 tests/test_season_rank.py
```

### Activation (for AI assistants)

Only activate when the user clearly asks for outfit help; do not trigger on casual mentions of clothes. Full trigger rules are in `SKILL.md`.

## License

本项目采用 MIT License，详见 `LICENSE`。

---
**作者**: Mars  
**日期**: 2026-04-13
