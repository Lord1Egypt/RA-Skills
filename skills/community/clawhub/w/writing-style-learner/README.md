# Style Learner

A skill that helps extract and learn writing styles from documents.

## Overview

Style Learner analyzes documents to identify writing patterns and characteristics, then saves them as reusable style guides. Perfect for teams wanting to maintain consistent documentation or individuals wanting to improve their writing.

## Features

### Single Document Learning
Learn from one document and extract its unique style characteristics.

### Batch Learning
Learn from multiple documents and extract common patterns, especially focusing on:
- Document structure
- Title hierarchy
- Code block formats
- Table layouts
- List styles

### Team Style Guide
Build a team-wide writing standard from multiple team members' documents.

## Usage Examples

### Example 1: Personal Style
```
User: Help me learn this document's style https://xfmkp6q7le.feishu.cn/wiki/xxx -as "Zhang Haoyu"

AI:
# Style Profile: Zhang Haoyu

## Core Characteristics
- Strong structure with fixed templates
- Technical-driven: full of CAN/topic/interface terms
- Problem-oriented: Background → Solution → Todo

## Structural Features
- Title hierarchy: Clear # ## ### usage
- Document structure: Change Record → Requirements Details

... (continues analysis)

Saved to MEMORY.md ✓
```

### Example 2: Batch Learning
```
User: Learn these 3 docs as team style
https://xfmkp6q7le.feishu.cn/wiki/doc1
https://xfmkp6q7le.feishu.cn/wiki/doc2
https://xfmkp6q7le.feishu.cn/wiki/doc3

AI:
Analyzing 3 documents...

## Common Patterns Found

### Structure
- All use "Background → Solution → Todo" structure
- Version history table at the beginning

### Format
- Code blocks: cpp, json, plaintext
- Frequent use of tables for interfaces

### Vocabulary
- High-frequency: "赋能", "闭环", "承接"

Team Style Guide saved ✓
```

## Commands

```
/learn-style [doc_url] [-as author_name]
/style-batch [doc_url1] [doc_url2] [doc_url3]
/style-team [doc_links]
```

## Installation

```bash
# Clone to skills directory
git clone https://github.com/your-repo/style-learner ~/.agents/skills/style-learner
```

## Requirements

- Feishu integration for document reading
- Write access to MEMORY.md or target storage

## Output Storage

Extracted styles are saved to:
- **Personal**: `MEMORY.md` in workspace
- **Team**: Configured shared knowledge base

## Extracted Dimensions

| Dimension | Description |
|----------|-------------|
| Title Hierarchy | How # ## ### are used |
| Structure | Background→Solution→Todo or other |
| Code Blocks | Preferred languages |
| Tables | Usage frequency and purpose |
| Tone | Casual vs formal |
| Vocabulary | High-frequency terms |
| Layout | Whitespace, lists, quotes |
| Collaboration | @mentions, references |

---

*Contribute: PRs welcome!*
