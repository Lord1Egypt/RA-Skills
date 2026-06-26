# Novel Writing Tools Guide / 小说写作工具使用指南

> **Version:** v1.1 (2026-03-31) — Generalized for any book project

---

## 📖 Tool Architecture / 工具分层架构

```
tools/
├── 【Prompt Generation / 提示词生成】
│   └── simple_writer_enhanced.py  # Generate chapter prompt ⭐ Core
│
├── 【Context Loading / 上下文加载】
│   ├── world_context_loader.py    # Load world settings, previous summaries
│   └── canon_generator.py         # Canon data generation
│
├── 【Quality Check / 质量检查】
│   ├── comprehensive_check.py     # 8-item comprehensive check ⭐ Core
│   ├── chapter_checker.py         # Chapter checker
│   ├── format_checker.py          # Format check
│   ├── finance_calculator.py      # Finance calculation
│   ├── system_rules_validator.py  # System rules validation
│   ├── protagonist_checker.py     # Protagonist personality check
│   ├── next_chapter_checker.py    # Next chapter preview check
│   ├── logic_checker.py           # Logic check
│   └── rhythm_analyzer.py         # Pacing analysis
│
├── 【Archive / 归档工具】
│   └── archive_chapter_with_truth.py  # Extract variables, update continuity ⭐ Core
│
└── 【Planning / 规划工具】
    ├── chapter_planner.py         # Chapter planning
    └── novel_planner.py           # Novel-wide planning
```

---

## 🚀 Core Tools / 核心工具

### 1. Prompt Generation (simple_writer_enhanced.py) ⭐⭐⭐

**Purpose:** Generate chapter writing prompt

```bash
cd skills/ZF-novel-writer/tools
python simple_writer_enhanced.py --chapter 6 --book {BOOK_NAME} --prompt-only
```

**What it loads:**
1. ✅ canon_bible.json (protagonist, era, heroines, style)
2. ✅ story_outline.xlsx (chapter plan)
3. ✅ Previous chapter summary (from summaries_json/)
4. ✅ pending_setups (unresolved foreshadowing)

### 2. Comprehensive Check (comprehensive_check.py) ⭐⭐⭐

**Purpose:** 8-item quality check

```bash
# Content QC mode
python comprehensive_check.py path/to/chapter.txt --mode=content
# Archive check mode
python comprehensive_check.py path/to/chapter.txt --mode=archive
```

**8 Checks:**
1. Word count: 3000-3500 Chinese characters (excluding punctuation)
2. Format: UTF-8, no garbled text
3. Finance: Accurate income/expenses/balance
4. System rules: Level, multiplier, limits
5. Protagonist personality: Assertive, decisive, not naive
6. Next chapter preview: ≤30 words, suspenseful
7. Logic: Timeline, character relations, location continuity
8. Pacing: 5-7 payoff points, rising emotional curve

### 3. Archive (archive_chapter_with_truth.py) ⭐⭐⭐

**Purpose:** Extract variables, update continuity during archive

```bash
python archive_chapter_with_truth.py path/to/chapter.txt --chapter 6
```

---

## 🔧 Auxiliary Tools / 辅助工具

| Tool | Purpose |
|------|---------|
| `world_context_loader.py` | Load world settings + previous summaries |
| `canon_generator.py` | Generate canon data |
| `finance_calculator.py` | Calculate chapter finances |
| `system_rules_validator.py` | Validate system-level rules |
| `protagonist_checker.py` | Check protagonist personality consistency |
| `next_chapter_checker.py` | Verify next chapter preview |
| `logic_checker.py` | Check logical consistency |
| `rhythm_analyzer.py` | Analyze pacing and payoff density |
| `chapter_planner.py` | Generate chapter plans |
| `novel_planner.py` | Generate full novel outline |
| `status.py` | Show current writing status |
| `setup_health_check.py` | Check foreshadowing health |
| `update_canon.py` | Update canon_bible.json |
| `update_pending_setups.py` | Update pending setups |
| `character_matrix.py` | Character relationship matrix |
| `emotional_arcs.py` | Track emotional arcs |

---

## ⚠️ Important Notes / 重要说明

- All tools use `book_name` as a variable parameter — no hardcoded book titles
- No external API keys required / 无需额外API key
- Tools are invoked by the Orchestrator agent or Quality agent during workflow

---

*Last updated: 2026-03-31*
