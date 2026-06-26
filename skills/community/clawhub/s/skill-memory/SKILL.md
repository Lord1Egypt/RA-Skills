---
name: skill-memory
description: Self-learning task-to-skill routing table. Automatically records new skills and updates parameters based on usage. 自学习型技能记忆表，自动记录新技能、更新参数。Use when: (1) Selecting skill for a task (2) Recording new skill usage (3) Updating skill parameters (4) Looking up preset configurations.
---

# Skill Memory / 技能记忆

Self-learning task-to-skill routing table with automatic recording and updating.
自学习型技能记忆表，支持自动记录和更新。

## How It Works / 工作机制

### 1. Check Before Use / 使用前检查
When executing a task, check memory table first:
```
Task → Look up memory.json → Found? → Use preset params
                              ↓ Not found
                         Use default → Record to memory
```

### 2. Auto Record / 自动记录
When using a skill not in memory:
```json
{
  "task_type": "新任务类型",
  "skill": "技能名称",
  "parameters": {...},
  "scenario": "使用场景描述",
  "created_at": "2026-03-27T13:00:00+08:00",
  "usage_count": 1
}
```

### 3. Auto Update / 自动更新
When same task type but different scenario/params:
```json
{
  "task_type": "网页截图",
  "skill": "Playwright CDP",
  "parameters": {"resolution": "1920x1080"},  // 新参数
  "scenario": "高清截图",
  "updated_at": "2026-03-27T14:00:00+08:00",
  "usage_count": 5
}
```

## Memory File Location / 记忆文件位置

Memory is stored in workspace:
```
~/.openclaw/workspace/skills/skill-memory/references/memory.json
```

## Core Mapping Table / 核心映射表

| Task Type | Preferred Skill | Preset Parameters |
|-----------|-----------------|-------------------|
| **Analyze Image / 分析图片** | `doubao-api-toolkit` | Vision analysis |
| **Analyze Video / 分析视频** | `doubao-video-analyzer` | Doubao 2.0 model |
| **Web Screenshot / 网页截图** | Playwright CDP | 1280×1024, 20s wait |
| **Text-to-Image / 文生图** | `doubao-api-toolkit` | Doubao API |
| **Image-to-Image / 图生图** | `doubao-api-toolkit` | Doubao API |
| **Text-to-Video / 文生视频** | `doubao-api-toolkit` | Doubao API |
| **TTS Voice / TTS配音** | `mambo-tts` | Mambo +50Hz |
| **News Aggregation / 新闻聚合** | `news-aggregator-skill` | 28-source |
| **Weibo Hot Search / 微博热搜** | `weibo-hot-search` | Hot + Entertainment |

## Web Screenshot Details / 网页截图详细参数

**Technical Solution**: Playwright connects to existing Chrome (CDP port 9222)

**Preset Parameters / 预设参数**:
```
Wait Time / 等待时间: 20 seconds (page load)
Resolution / 分辨率: 1280×1024
Capture Scope / 截取范围: Webpage content only
Style / 风格要求: Clean, no scrollbars, no borders
```

**Usage / 调用方式**:
```python
# Connect to existing Chrome / 连接已有Chrome
browser = await playwright.chromium.connect_over_cdp("http://localhost:9222")
page = browser.contexts[0].pages[0]
await page.wait_for_timeout(20000)  # Wait 20s / 等待20秒
await page.screenshot(path="output.png", full_page=False)
```

## TTS Voice Presets / TTS音色预设

| Preset | Voice | Pitch | Use Case / 适用场景 |
|--------|-------|-------|---------------------|
| **Mambo / 曼波** | zh-CN-XiaoyiNeural | +50Hz | Lively, energetic / 活泼有活力 |
| **Xiaoyi / 晓伊** | zh-CN-XiaoyiNeural | default | Fast-paced, news / 快节奏新闻 |
| **Xiaoxiao / 晓晓** | zh-CN-XiaoxiaoNeural | default | Natural, general / 自然通用 |
| **Yunyang / 云扬** | zh-CN-YunyangNeural | default | Narration, documentary / 旁白纪录片 |

## Update Script / 更新脚本

Use the update script to record or update skill memory:
```bash
python scripts/update_memory.py --task "任务类型" --skill "技能名称" --params '{"key":"value"}' --scenario "场景描述"
```

### Script Options / 脚本参数

| Option | Description |
|--------|-------------|
| `--task` | Task type (任务类型) |
| `--skill` | Skill name (技能名称) |
| `--params` | JSON parameters (参数JSON) |
| `--scenario` | Usage scenario (使用场景) |
| `--list` | List all memory entries (列出所有记忆) |

## Usage Workflow / 使用流程

### Step 1: Check Memory / 检查记忆
```bash
python scripts/update_memory.py --list
```

### Step 2: Execute Task / 执行任务
- If task in memory → Use preset params
- If task NOT in memory → Use best skill → Record to memory

### Step 3: Auto Update / 自动更新
- Same task, new scenario → Update memory entry
- Increment usage_count automatically

## Example Scenarios / 示例场景

### Scenario 1: New Task Type / 新任务类型
```
User: "帮我分析这个音频"
  ↓
Check memory: No "音频分析" entry
  ↓
Use best skill: doubao-api-toolkit (audio feature)
  ↓
Record to memory:
{
  "task_type": "分析音频",
  "skill": "doubao-api-toolkit",
  "parameters": {"mode": "audio"},
  "scenario": "音频内容分析",
  "usage_count": 1
}
```

### Scenario 2: Updated Parameters / 参数更新
```
User: "截个高清网页图，要1920x1080"
  ↓
Check memory: Found "网页截图" but params differ
  ↓
Use new params: 1920x1080
  ↓
Update memory:
{
  "task_type": "网页截图",
  "parameters": {"resolution": "1920x1080", "high_res": true},
  "scenario": "高清截图",
  "updated_at": "...",
  "usage_count": 6  // incremented
}
```

## Extension Rules / 扩展规则

- If task type not in table, use default skill selection
- User's explicit skill choice overrides table mapping
- Preset parameters can be overridden by user specification
- Always record new skill usage to memory
- Always update memory when scenario/params differ
