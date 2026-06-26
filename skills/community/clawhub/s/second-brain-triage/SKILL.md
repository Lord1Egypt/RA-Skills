---
name: second-brain-triage
description: Intelligent information triage system based on Tiago Forte's PARA method (Projects/Areas/Resources/Archive) for automatic categorization and priority scoring. Use when the user wants to organize notes, classify content, prioritize tasks, or manage their second brain knowledge base.
version: v1.0.0
tags: para-method, content-triage, knowledge-management
---

# Second Brain Triage

## Usage Scenarios

### Scenario 1: Triage a Single Task
**User input:** "Categorize this task: 'Complete quarterly report, due next Friday'"
**Expected output:** The tool classifies the item under "Projects" with high urgency score (7-8), recommends processing within 24 hours, and provides the full triage summary including type, category, and action.

### Scenario 2: Batch Organize Bookmarks into PARA Categories
**User input:** "Organize my 20 bookmarked articles and resources using PARA"
**Expected output:** The tool processes each item through batch triage, categorizes them into Projects/Areas/Resources/Archive with individual urgency scores, and returns a consolidated report.

### Scenario 3: Export Triage Report as Markdown
**User input:** "Export all my triaged items as a formatted Markdown report"
**Expected output:** The tool generates a readable Markdown report with all categorized items, their scores, and recommended actions, saved or printed to stdout.

Intelligent information triage system based on Tiago Forte's PARA method (Projects/Areas/Resources/Archive) for automatic categorization and priority scoring.
### Scenario 4: 微信收藏夹快满了
**User input:** "我的微信收藏夹有324条内容，看了就想收藏但从来不回看，怎么清理和整理？"
**Expected output:** 提供'碎片信息分诊'三步法：1）批量导出微信收藏夹内容到Notion/飞书/印象笔记；2）用PARA分类法（Projects/Areas/Resources/Archives）快速标记；3）制定每日15分钟回顾规则：只保留当前需要的信息，其他直接归档。建议以后看到好内容先判断：对我当前的项目有用吗？如果5分钟内用不上就暂时不收藏。

## Features

- **Content Analyzer**: Automatically identify content types (articles, videos, tasks, code, etc.) and extract metadata
- **PARA Classifier**: Smart categorization into Projects/Areas/Resources/Archive
- **Urgency Scorer**: Multi-dimensional algorithm to evaluate processing priority (1-10 scale)
- **Relatedness Detector**: Discover similarities and relationships between content items

## Usage

### Basic Usage

```javascript
const { SecondBrainTriage } = require('./src');

const triage = new SecondBrainTriage();

// Triage single content item
const result = triage.triage('TODO: Complete project report, due this Friday');
console.log(result.summary);
// {
//   title: "Complete project report, due this Friday",
//   type: "task",
//   category: "Projects",
//   urgency: "High urgency",
//   urgencyScore: 8,
//   action: "Process today: recommend completing within 24 hours"
// }

// Batch triage
const results = triage.triageBatch([
  'https://github.com/user/repo',
  'Notes on learning React Hooks',
  'TODO: Fix login bug',
]);

// Export report
const report = triage.exportReport(results, 'markdown');
```

### CLI Usage

```bash
# Analyze single content item
node scripts/triage.js "Text content to process"

# Analyze file
node scripts/triage.js --file ./notes.txt

# Batch analysis
node scripts/triage.js --batch ./items.json --output report.md
```

## Classification Guide

### PARA Categories

| Category | Description | Examples |
|----------|-------------|----------|
| **Projects** | Items with clear goals and deadlines | "Develop new feature", "Complete report" |
| **Areas** | Long-term responsibilities and standards | "Health management", "Skill development" |
| **Resources** | Topics of interest and reference materials | "Technical articles", "Learning notes" |
| **Archive** | Completed or inactive items | "Finished projects", "Historical records" |
| **Inbox** | Temporary storage for uncategorized items | Content that cannot be determined |

### Urgency Levels

| Score | Level | Description | Recommendation |
|-------|-------|-------------|----------------|
| 9-10 | Critical | Process immediately | Take action now |
| 7-8 | High | Process today | Complete within 24 hours |
| 5-6 | Medium | Process this week | Schedule within the week |
| 3-4 | Low | Low priority | Can be deferred |
| 1-2 | Minimal | Archive for reference | No immediate action needed |

## Technical Architecture

```
src/
├── content-analyzer.js    # Content type recognition and metadata extraction
├── para-classifier.js     # PARA classification algorithm
├── urgency-scorer.js      # Urgency scoring algorithm
├── relatedness-detector.js # Relatedness detection
└── index.js               # Main entry and API
```

## Scoring Algorithm

### Urgency Scoring Dimensions

1. **Time Sensitivity** (30%): Deadlines, time keywords
2. **Action Requirement** (25%): Action verbs like must/plan/maybe
3. **Consequences** (20%): Potential impact of not processing
4. **Context Signals** (15%): Blockers, external dependencies
5. **User Preferences** (10%): Configurable priorities

### Relatedness Detection

- Tag similarity (Jaccard coefficient)
- Title/description text similarity (Cosine similarity)
- Semantic similarity (based on semantic groups)
- Type matching

## Configuration Options

```javascript
const triage = new SecondBrainTriage({
  enableRelatedness: true,    // Enable relatedness detection
  urgencyThreshold: 5,        // Urgency threshold
});
```

## Output Formats

Supported export formats:
- JSON (complete data)
- Markdown (readable format)
- CSV (spreadsheet format)

## Dependencies

- Node.js >= 14
- No external dependencies (pure JavaScript implementation)

## License

MIT
