# Technical Research Skill

A Claude skill for systematic, in-depth technical research that produces structured reports across four dimensions.

## Overview

This skill performs comprehensive technical research on any domain, producing professional reports covering:

1. **Concept Analysis** - Deep understanding of principles and architecture
2. **Industry Intelligence** - Latest open-source projects, papers, and blogs
3. **Solution Comparison** - Horizontal evaluation of multiple approaches
4. **Essence Integration** - Condensed summary for knowledge sharing

## Usage

Invoke with:
```
/technical-research
```

Or ask directly:
```
调研 {technology domain}
```

Examples:
- `调研 Agent Memory 机制`
- `调研 RAG 技术`
- `调研 向量数据库`

## Output Structure

For each research topic, the skill produces:

```
research/{topic}/
├── 00-索引.md              # File index and execution stats
├── 01-完整调研报告.md       # Complete report (all dimensions)
├── 02-The-All-in-One.md     # Essence summary
├── 03-STAR-总结.md          # STAR methodology summary
├── {topic}-concept.md       # Concept analysis
├── {topic}-intel.md         # Industry intelligence
├── {topic}-analysis.md      # Solution comparison
└── {topic}-research.md      # Final integrated report
```

## Use Cases

- **Technology Selection** - Comprehensive research before choosing tools/frameworks
- **Domain Learning** - Rapid onboarding to new technical areas
- **Competitive Analysis** - Compare multiple solutions systematically
- **Team Sharing** - Prepare materials for internal tech talks

## Quality Standards

- **Data Freshness** - All intelligence includes source and date (prioritize recent 2 years)
- **Completeness** - Each report >100 characters, total ~6000+ words
- **Actionable** - Selection advice includes scenarios and cost estimates
- **Structured** - Markdown format with proper tables, code blocks, diagrams

## Research Framework

```
First Layer (independent, can run in parallel):
  ├── Concept Analysis  - Technical principles & architecture
  ├── Industry Intelligence - Projects, papers, blogs
  └── Solution Comparison - Horizontal evaluation

Second Layer (depends on first layer):
  ├── Essence Integration - Condensed summary
  └── Final Integration - Complete markdown report
```
---

**Version**: 4.0 | **Type**: Knowledge Process
