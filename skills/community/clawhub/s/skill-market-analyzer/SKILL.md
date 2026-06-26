# Skill Market Analyzer

Analyze the OpenClaw skill marketplace to identify trends, gaps, and opportunities.

## Overview

Skill Market Analyzer helps you understand the skill ecosystem by analyzing:
- Market trends and popular categories
- Competitive landscape
- Underserved areas and opportunities
- User demand patterns

## When to Use

- Planning a new skill and need market research
- Analyzing competitive landscape
- Identifying gaps in the marketplace
- Understanding user demand patterns

## Core Concepts

### Market Dimensions

| Dimension | Description |
|-----------|-------------|
| demand | User interest and request frequency |
| supply | Number of available skills in category |
| quality | Average quality of existing solutions |
| saturation | How crowded the market segment is |

### Analysis Types

| Type | Purpose |
|------|---------|
| landscape | Overall market overview |
| gap | Find underserved areas |
| competitive | Compare to competitors |
| trend | Identify emerging patterns |

## Usage

### Analyze Market Landscape

```bash
./scripts/analyze.sh productivity report.md
```

This generates a market analysis report for the productivity category.

### Find Market Gaps

```bash
./scripts/analyze.sh all gaps-report.md
```

Analyzes all categories and identifies underserved areas.

## Scripts

- `scripts/analyze.sh` - Generate market analysis reports

## Output Format

Market analysis reports include:
- Executive summary
- Supply/demand analysis
- Opportunity rankings
- Strategic recommendations

## Technical Information

| Attribute | Value |
|-----------|-------|
| **Skill ID** | skill-market-analyzer |
| **Version** | 2.0.1 |
| **Author** | harrylabsj |
| **License** | MIT-0 |

## Notes

- Analysis based on publicly available skill data
- No external API calls required
- All processing done locally
