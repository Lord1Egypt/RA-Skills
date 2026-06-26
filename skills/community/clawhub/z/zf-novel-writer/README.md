# ZF-novel-writer / 三Agent协作小说写作系统

Three-agent collaborative novel writing system for OpenClaw. Orchestrator plans chapters, Writer Agent generates content, Quality Agent checks quality.

OpenClaw 三Agent协作小说写作系统。Orchestrator规划章节，Writer Agent生成内容，Quality Agent检查质量。

## Features / 功能特性

- 🤖 **Three-agent architecture:** Orchestrator + Writer + Quality / 三Agent架构
- 📖 **Multi-book support:** Manage multiple novel projects / 支持多书籍管理
- 📊 **Excel-driven outline:** story_outline.xlsx as single source of truth / xlsx驱动大纲
- 🔍 **Continuity tracking:** Truth Files + canon_bible.json / 连续性追踪
- ✅ **Automated QC:** 8-item quality check + scoring / 自动化质量检查
- 📦 **No API keys needed:** Uses host agent's model / 无需额外API key
- 🔄 **Full pipeline:** Plan → Write → QC → Archive → Repeat / 全流程自动化

## Quick Start / 快速开始

```bash
# 1. Copy example book project
cp -r skills/ZF-novel-writer/example-book books/{YOUR_BOOK_NAME}

# 2. Customize settings
# - Edit meta/canon_bible.json
# - Create story_outline.xlsx
# - Edit genre_rules.md, WORLD_SETTING.md

# 3. Start writing
# Trigger in OpenClaw: "写小说" or "/novel"
```

## Directory Structure / 目录结构

```
ZF-novel-writer/
├── SKILL.md                      # Skill definition (OpenClaw reads this)
├── README.md                     # This file
├── config.json                   # Quality standards config
├── ORCHESTRATOR_ARCHIVE_GUIDE.md # Archive workflow guide
├── example-book/                 # Template book project
│   ├── meta/canon_bible.json
│   ├── genre_rules.md
│   ├── WORLD_SETTING.md
│   ├── LEVEL_BRONZE.md
│   ├── chapters/
│   ├── summaries_json/
│   ├── temp_chapters/
│   └── plans/
├── docs/
│   └── ARCHITECT_AGENT_DESIGN.md
└── tools/                        # Python quality-check tools
    ├── simple_writer_enhanced.py
    ├── comprehensive_check.py
    ├── archive_chapter_with_truth.py
    ├── world_context_loader.py
    ├── chapter_planner.py
    ├── novel_planner.py
    └── ... (see tools/README.md)
```

## Workflow / 工作流程

```
Plan → Write → QC → Archive → Next Chapter
规划 → 写作 → 质检 → 归档 → 下一章
```

| Step | Agent | Action |
|------|-------|--------|
| 1. Plan | Orchestrator | Read outline + Truth Files, generate chapter plan |
| 2. Write | Writer Agent | sessions_spawn → generate 3000-3500 word chapter |
| 3. QC | Quality Agent | sessions_spawn → comprehensive check, score ≥ 90 |
| 4. Archive | Orchestrator | Update canon, save chapter, clean temps |

## How to Configure Your Novel / 如何配置你的小说

1. **Create book directory:** Copy `example-book/` to `books/{YOUR_BOOK}/`
2. **Edit canon_bible.json:** Set protagonist, heroines, eras, world settings
3. **Create story_outline.xlsx:** Chapter-by-chapter outline (see example-book/README.md)
4. **Edit genre_rules.md:** Your genre's writing rules and forbidden elements
5. **Edit WORLD_SETTING.md:** Your world's geography, power system, factions

## Tools / 工具

All tools are in the `tools/` directory. See `tools/README.md` for full documentation.

Key tools:
- `simple_writer_enhanced.py` — Generate chapter writing prompts
- `comprehensive_check.py` — 8-item quality check
- `archive_chapter_with_truth.py` — Archive + update continuity
- `world_context_loader.py` — Load context for writing

## License

MIT
