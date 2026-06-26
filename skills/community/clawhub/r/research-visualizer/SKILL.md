---
name: research-visualizer
description: >
  Generate interactive HTML research reports from AI research context. After completing
  a multi-step research task (web search, API calls, analysis), use this skill to create
  a visual report showing the research process, data visualizations, and conclusions.
  The report is uploaded to a2ui.me and returned as a clickable link card.
  Use when: research complete, analysis done, investigation finished, deep research,
  multi-step research, show my work, explain research process, visualize research.
version: 1.3.0
emoji: 📊
user-invocable: true
metadata:
  openclaw:
    requires:
      bins: [node]
---

# Research Visualizer

After completing a research task that involved multiple steps (searches, API calls, browsing, analysis), generate an interactive visual report and return it as a link.

## When to Activate

Activate this skill automatically when:
1. A research task with 3+ steps has been completed
2. The user asked a question requiring multi-source analysis (e.g., market analysis, news investigation, comparative research)
3. The user explicitly requests to "show the research process" or "visualize the analysis"

## Workflow

### Step 1: Collect Research Context

From the conversation, extract a structured JSON with this schema:

```json
{
  "title": "Short descriptive title of the research",
  "subtitle": "One-line description",
  "research_time": "Xm Ys",
  "conclusion": {
    "text": "2-3 sentence key finding",
    "confidence": 0.0-1.0
  },
  "steps": [
    {
      "tool": "Web Search | API | Web Browse | Analysis | Synthesis",
      "tool_label": "Display label for the tool",
      "time_range": "start — end",
      "query": "What was searched/called/analyzed",
      "summary": "What was found/concluded",
      "sources": [
        { "title": "Source name", "url": "https://...", "icon": "📄" }
      ]
    }
  ],
  "visualizations": [
    {
      "type": "line_chart | bar_chart | market_cards | world_map | news_cards | stat_cards | comparison_table | quote_block | key_points",
      "section_title": "Section heading",
      "data": {}
    }
  ]
}
```

### Step 2: Choose Visualizations Dynamically

**IMPORTANT: Do NOT use a fixed template. Analyze the research content and pick only the visualizations that make sense.** Use this decision guide:

| Research involves... | Use these visualizations |
|---|---|
| Time-series data, trends, probabilities | `line_chart` or `bar_chart` |
| Prediction markets, odds, pricing | `market_cards` |
| Geopolitics, regional impact, locations | `world_map` |
| News articles, media coverage | `news_cards` |
| Key metrics, statistics, KPIs | `stat_cards` |
| Comparing products, options, candidates | `comparison_table` |
| Expert opinions, notable quotes | `quote_block` |
| Summarized takeaways, bullet points | `key_points` |

**Rules:**
- Use 2-4 visualization types per report (don't overload)
- Always include the research timeline (steps)
- Pick visualizations that ADD VALUE, not just fill space
- If unsure, `stat_cards` + `news_cards` is a safe default combo

### Visualization Data Schemas

- **line_chart**: Time-series data, trends, probability changes
  ```json
  { "title": "Chart Title", "y_format": "percent", "y_min": 0, "y_max": 100,
    "x_labels": ["Label1", "Label2"],
    "series": [{ "name": "Series Name", "values": [10, 20, 30] }] }
  ```

- **bar_chart**: Categorical comparisons, rankings
  ```json
  { "title": "Chart Title", "y_format": "number",
    "bars": [{ "label": "Category A", "value": 85, "color": "#00d2a0" },
             { "label": "Category B", "value": 62, "color": "#6c5ce7" }] }
  ```

- **market_cards**: Prediction markets, pricing, comparisons
  ```json
  [{ "name": "Market Name", "yes_price": 85, "no_price": 15, "volume": "128M", "change_7d": 3.2 }]
  ```

- **world_map**: Geopolitical analysis, regional impacts
  ```json
  { "regions": [{ "id": "united_states|europe|east_asia|...", "name": "Display Name", "info": "Impact description" }] }
  ```
  Valid region IDs: north_america, united_states, canada, mexico, south_america, europe, africa, russia, middle_east, east_asia, china, southeast_asia, australia

- **news_cards**: Related news, source citations
  ```json
  [{ "title": "Headline", "source": "Publisher", "date": "Mar 28, 2026", "sentiment": "positive|negative|neutral|warning", "tag": "Category", "url": "https://..." }]
  ```

- **stat_cards**: Key metrics and statistics (use for any numerical highlights)
  ```json
  [{ "label": "Total Volume", "value": "$4.2B", "change": "+12.5%", "trend": "up|down|neutral", "icon": "💰" }]
  ```

- **comparison_table**: Side-by-side comparisons
  ```json
  { "headers": ["Feature", "Option A", "Option B"],
    "rows": [["Price", "$10/mo", "$25/mo"], ["Users", "5", "Unlimited"]],
    "highlight_col": 1 }
  ```

- **quote_block**: Notable quotes from sources
  ```json
  [{ "text": "The quote text here", "author": "Person Name", "role": "Title / Organization", "url": "https://..." }]
  ```

- **key_points**: Bullet-point takeaways with icons
  ```json
  [{ "icon": "✅", "title": "Point Title", "text": "Explanation of the point" }]
  ```

### Step 3: Generate and Upload

Save the JSON to a temp file, then run:

```bash
node {baseDir}/scripts/generate-report.js --input /tmp/research-data.json --output /tmp/report.html
node {baseDir}/scripts/upload-report.js --file /tmp/report.html
```

The upload script automatically:
1. Encrypts the HTML with AES-256-GCM (key never touches the server)
2. Uploads the encrypted viewer page to R2
3. Outputs the full URL with the decryption key in the fragment (`#key=...`)

**Privacy guarantee**: The URL fragment (`#key=...`) is never sent to the server. Only the person with the complete URL can view the report.

Return the URL to the user as:

```
📊 Research Report Ready
[Title of Research](https://r.a2ui.me/r/xxxxx.html#key=yyy)
6 steps · 14 sources · 87% confidence
🔒 End-to-end encrypted — only this link can decrypt
```

### Step 4: Local Fallback

If no upload credentials are set, the report saves locally to `{baseDir}/output/`. Inform the user:

```
📊 Research report saved locally:
file:///path/to/output/report.html#key=yyy
(Set A2UI_R2_BUCKET to enable cloud hosting at r.a2ui.me)
```

### Step 5: No-encrypt option

If the user explicitly wants a public (unencrypted) report, add `--no-encrypt`:

```bash
node {baseDir}/scripts/upload-report.js --file /tmp/report.html --no-encrypt
```

## Important

- Always include ALL research steps, not just the final answer
- Include real source URLs whenever available
- Set confidence based on source agreement (high if multiple sources agree, lower if contradictory)
- The report should make the research process transparent and verifiable
- Keep step summaries concise but informative (1-2 sentences each)
