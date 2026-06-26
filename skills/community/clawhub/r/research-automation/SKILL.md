---
name: research-automation
description: Automated web research for peptides, biohacking protocols, longevity science, and trending health topics. Use when you need to discover new information, track emerging trends, monitor scientific updates, or generate content ideas based on current research. Runs periodically via heartbeat or on-demand.
---

# Research Automation

Automated research system that searches the web for new developments in peptides, biohacking, longevity, and trending health topics.

## What It Does

- **Web Search**: Queries multiple sources for latest research, protocols, and trends
- **Content Curation**: Filters and organizes findings by topic
- **Insight Generation**: Extracts actionable insights and content angles
- **Auto-Save**: Stores research in structured markdown files for easy access

## Topics Covered

1. **Peptides**: New peptides, clinical studies, protocols, dosing updates
2. **Biohacking Protocols**: Emerging techniques, stack combinations, optimization methods
3. **Longevity Science**: Aging research, interventions, biomarkers, clinical trials
4. **Trending Topics**: Viral health content, controversial topics, zeitgeist shifts
5. **Performance Optimization**: Founder health, cognitive enhancement, metabolic optimization

## Usage

### On-Demand Research

Run a targeted research query:

```
Run research on [topic] - focus on [specific angle]
```

Example:
```
Run research on GLP-1 peptides - focus on recent clinical trials and dosing protocols
```

### Scheduled Research (Heartbeat)

The skill runs automatically via heartbeat rotation, cycling through research topics:
- Peptides (weekly)
- Biohacking protocols (twice weekly)
- Longevity updates (weekly)
- Trending topics (daily)

## Output Format

Research is saved to `research/[topic]/[date].md`:

```markdown
# [Topic] Research - [Date]

## Key Findings

1. **[Finding Title]**
   - Source: [URL]
   - Key Insight: [1-2 sentence summary]
   - Actionable: [What you can do with this]
   - Content Angle: [How to turn this into content]

2. **[Next Finding]**
   ...

## Trending Discussions

- [Topic]: [Summary of discourse]
- [Topic]: [Summary of discourse]

## Content Ideas Generated

1. [Tweet/thread angle]
2. [LinkedIn post angle]
3. [Article angle]

## Sources Reviewed

- [Source 1]
- [Source 2]
...
```

## Search Strategy

For each research run:

1. **Query Construction**: Build 3-5 targeted search queries
2. **Source Diversity**: Mix academic, clinical, and practical sources
3. **Recency Filter**: Prioritize last 30 days (configurable)
4. **Signal Extraction**: Identify novel information vs. repetition
5. **Content Angle Generation**: Translate findings into tweet/post ideas

## Integration with Content Creation

Research outputs feed directly into:
- `content/biohacker-angles-[date].md` (Twitter content)
- `content/tokuflow-angles-[date].md` (Nattokinase angles)
- `notes/research-insights/` (Long-form reference)

## Search Queries by Topic

### Peptides
- "new peptides 2026"
- "GLP-1 peptides clinical trials"
- "peptide protocols biohacking"
- "BPC-157 latest research"
- "thymosin beta-4 studies"

### Biohacking
- "biohacking protocols 2026"
- "founder health optimization"
- "cognitive enhancement stack"
- "metabolic optimization techniques"
- "bloodwork optimization protocols"

### Longevity
- "aging research 2026"
- "longevity interventions clinical trials"
- "senolytics latest studies"
- "rapamycin longevity research"
- "NAD+ aging protocols"

### Trending
- "health twitter trending"
- "biohacking controversy"
- "peptide discussion twitter"
- "longevity debate 2026"

## Filtering Criteria

**Include:**
- Novel findings (not widely covered)
- Clinical/scientific backing
- Actionable protocols
- Controversial/debate-worthy topics
- Counter-narrative insights

**Exclude:**
- Generic wellness advice
- Repeated information
- Non-peer-reviewed claims without strong reasoning
- Pure speculation without mechanism

## Best Practices

1. **Run research before content creation sprints** - Fresh angles generate better ideas
2. **Review weekly summaries** - Track emerging patterns and shifts
3. **Cross-reference findings** - Connect dots between topics (e.g., peptides + longevity)
4. **Archive high-value findings** - Move breakthrough research to `notes/research-insights/`

## Manual Research Workflow

When you need deep research on a specific topic:

1. **Specify the topic and angle**:
   ```
   Research [topic] with focus on [specific angle] - find clinical backing and protocols
   ```

2. **Review the output**:
   - Check `research/[topic]/[date].md`
   - Assess signal vs. noise
   - Request refinement if needed

3. **Generate content**:
   ```
   Turn the [specific finding] into 5 tweet angles
   ```

## Heartbeat Integration

To enable scheduled research, add to `HEARTBEAT.md`:

```markdown
### 8. Research Automation - Peptides (Priority: Medium)
- Run research-automation skill for peptides
- Focus: New compounds, clinical studies, protocols
- Save to `research/peptides/[date].md`
- Frequency: Once per week

### 9. Research Automation - Trending (Priority: High)
- Run research-automation skill for trending topics
- Focus: Viral health content, debates, controversies
- Save to `research/trending/[date].md`
- Frequency: Daily
```

## Output Locations

```
workspace/
├── research/
│   ├── peptides/
│   │   └── 2026-02-05.md
│   ├── biohacking/
│   │   └── 2026-02-05.md
│   ├── longevity/
│   │   └── 2026-02-05.md
│   └── trending/
│       └── 2026-02-05.md
└── notes/
    └── research-insights/
        └── breakthrough-findings.md
```

## Tips for Maximizing Value

- **Run daily for trending topics** - Capture zeitgeist shifts early
- **Run weekly for scientific topics** - Avoid overwhelming with noise
- **Review findings during content planning** - Best source of fresh angles
- **Cross-pollinate topics** - Peptides + longevity = unique positioning
- **Archive breakthroughs** - High-value findings go to permanent notes

---

**Created:** 2026-02-05  
**Last Updated:** 2026-02-05
