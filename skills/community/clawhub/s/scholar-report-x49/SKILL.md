---
name: scholar-report
description: Generate AI-powered academic research reports via the Scholar API (scholar.x49.ai). Creates comprehensive literature review reports with inline citations, paper evidence, and downloadable Markdown. Use when the user wants a research report, literature review, academic survey, state-of-the-art summary, or systematic overview of a topic. Triggers when the user mentions generating a report, reviewing literature, surveying a field, summarizing research trends, or asks complex questions that benefit from a synthesized academic report.
allowed-tools: Bash
argument-hint: "[research question]"
effort: high
metadata:
  skill-author: scholar.x49.ai
---

# Scholar Report

Generate AI-powered academic research reports via the Scholar API at `https://scholar.x49.ai`.

Reports are comprehensive literature reviews with inline citations, paper evidence, and downloadable Markdown output. The process is asynchronous: create a report, poll its progress, then download the result.

## When to Use This Skill

Use this skill when the user needs to:
- Generate a comprehensive literature review on a research topic
- Get an AI-summarized survey of a field or subfield
- Produce a research report with verified academic citations
- Understand the state of the art on a topic with paper-level evidence
- Download a structured Markdown report for reference or further editing

**Consider using `scholar-search` first** to validate the topic and refine the query before generating a full report. Searching first helps confirm the right direction and filters before committing to a longer report generation.

## API Configuration

The API base URL is `https://scholar.x49.ai/api/v1`.

Authentication uses a Bearer token. Resolve the key in this order:

1. Environment variable `SCHOLAR_API_KEY`
2. Built-in free key: `psk_tLzPCmJdUw5oAHGeXL2H_fMrDdSyiF_SBJfn2p5uCO4`

Users can get their own higher-quota key at: https://scholar.x49.ai/docs?section=api-keys

**Always construct API calls like this:**

```bash
SCHOLAR_KEY="${SCHOLAR_API_KEY:-psk_tLzPCmJdUw5oAHGeXL2H_fMrDdSyiF_SBJfn2p5uCO4}"
BASE="https://scholar.x49.ai/api/v1"
```

---

## Workflow: Create → Poll → Download

### Step 1: Create a Report

`POST /reports` — Start an asynchronous report generation job.

```bash
SCHOLAR_KEY="${SCHOLAR_API_KEY:-psk_tLzPCmJdUw5oAHGeXL2H_fMrDdSyiF_SBJfn2p5uCO4}"
curl -s "https://scholar.x49.ai/api/v1/reports" \
  -H "Authorization: Bearer ${SCHOLAR_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the latest advances in transformer attention mechanisms for NLP?",
    "target_language": "en",
    "include_papers": true,
    "filters": {
      "year_from": 2020,
      "year_to": 2025
    }
  }'
```

**Request body fields:**

| Field | Type | Required | Meaning |
|---|---|---|---|
| `query` | string | Yes | The report topic. Write it as a research question or task |
| `target_language` | string | No | Output language: `en` (English) or `zh` (Chinese), etc. |
| `include_papers` | boolean | No | Whether to include paper-level evidence in the result |
| `filters.year_from` | integer | No | Restrict to papers published from this year |
| `filters.year_to` | integer | No | Restrict to papers published up to this year |
| `filters.paper_types` | string[] | No | e.g. `["article", "review"]` |

**Optional: Idempotency-Key header** — For safe retries. If the client may retry the same create request, include `Idempotency-Key: <unique-key>` header. The API replays the same `report_id` on duplicate requests.

**Response**: Returns HTTP 202 with:

```json
{
  "data": {
    "report_id": "fdaca9e7-b1cc-4286-a7fc-8c466d8e8554",
    "status": "pending",
    "stage": "queued",
    "progress": 0
  }
}
```

Save the `report_id` immediately — you need it for polling and downloading.

---

### Step 2: Poll Report Status

`GET /reports/{report_id}` — Check progress until `status=completed`.

```bash
curl -s "${BASE}/reports/${REPORT_ID}" \
  -H "Authorization: Bearer ${KEY}"
```

**Key response fields:**

| Field | Meaning |
|---|---|
| `status` | `pending`, `running`, or `completed` |
| `stage` | Current stage: `queued`, `searching`, `retrieving`, `deduplicating`, `summarizing` |
| `progress` | 0 to 100 |
| `message` | Human-readable progress message |
| `timing.running_seconds` | Time spent so far |
| `result.summary` | Report summary (only when completed) |
| `result.artifacts.markdown_available` | Whether markdown is ready to download |
| `result.papers` | Paper evidence (when `include_papers=true`) |
| `result.references` | Reference entries |
| `result.directions` | Research directions covered |

**Polling strategy**: Poll every 15 seconds until `status=completed`. Reports typically take 2-5 minutes.

```bash
REPORT_ID="fdaca9e7-b1cc-4286-a7fc-8c466d8e8554"
SCHOLAR_KEY="${SCHOLAR_API_KEY:-psk_tLzPCmJdUw5oAHGeXL2H_fMrDdSyiF_SBJfn2p5uCO4}"

while true; do
  STATUS=$(curl -s "https://scholar.x49.ai/api/v1/reports/${REPORT_ID}" \
    -H "Authorization: Bearer ${SCHOLAR_KEY}")
  echo "$STATUS" | python3 -c "
import sys, json
d = json.load(sys.stdin)['data']
print(f'Status: {d[\"status\"]} | Stage: {d[\"stage\"]} | Progress: {d[\"progress\"]}% | Message: {d.get(\"message\",\"\")}')
"
  if echo "$STATUS" | python3 -c "import sys,json; sys.exit(0 if json.load(sys.stdin)['data']['status']=='completed' else 1)"; then
    break
  fi
  sleep 15
done
```

---

### Step 3: Download Markdown

`GET /reports/{report_id}/markdown` — Download the final report as Markdown text.

```bash
curl -s "${BASE}/reports/${REPORT_ID}/markdown" \
  -H "Authorization: Bearer ${KEY}"
```

**This endpoint returns raw Markdown text**, not a JSON envelope. The markdown content includes:
- Report metadata (generated time, query, target language)
- Research directions
- Comprehensive summary with inline citations like `[(Author et al., Year)](#ref-REF_001)`
- A references section with full citations and DOIs/URLs

---

## Common Usage Patterns

### Pattern 1: Quick research report

User asks: "Generate a report on recent advances in CRISPR gene therapy"

1. (Optional) Use `scholar-search` first to validate the query returns good results
2. Call `POST /reports` with the query
3. Poll every 15 seconds until complete
4. Download the markdown and present it to the user
5. Offer to save it to a file

### Pattern 2: Targeted report with filters

User asks: "Create a Chinese-language report on LLM safety from 2023-2025, only articles and reviews"

1. Build the request:
   ```json
   {
     "query": "What are the safety challenges and solutions for large language models?",
     "target_language": "zh",
     "include_papers": true,
     "filters": {
       "year_from": 2023,
       "year_to": 2025,
       "paper_types": ["article", "review"]
     }
   }
   ```
2. Create, poll, download as usual

### Pattern 3: Report with paper evidence

User asks: "I need a report with supporting papers included"

1. Set `include_papers: true` in the create request
2. The completed report's `result.papers` array will contain paper cards with:
   - Title, authors, year, venue
   - `summary_snippet` — relevant excerpt
   - `evidence.matched_questions` — how many directions this paper supports
   - `metrics.citation_count` and `metrics.relevance`
3. Download the markdown for the full synthesized report

### Pattern 4: Safe retry with idempotency

User asks: "Create that report again" or client may retry

1. Use the `Idempotency-Key` header:
   ```bash
   curl -s "${BASE}/reports" \
     -H "Authorization: Bearer ${KEY}" \
     -H "Content-Type: application/json" \
     -H "Idempotency-Key: my-unique-key-123" \
     -d '{"query": "..."}'
   ```
2. Duplicate requests with the same key return the same `report_id`
3. Check response header `Idempotency-Replayed: true` to know it was a replay

---

## Report Lifecycle Stages

| Stage | What happens | Typical duration |
|---|---|---|
| `queued` | Job received, waiting to start | < 1 second |
| `searching` | Searching paper databases | 10-30 seconds |
| `retrieving` | Fetching paper metadata and full text | 20-60 seconds |
| `deduplicating` | Removing duplicate papers | 5-10 seconds |
| `summarizing` | AI synthesizing the report | 60-180 seconds |
| `completed` | Report ready for download | — |

**Note**: The `summarizing` stage takes the longest. Progress may stay at 82% for a while during this stage — this is normal.

---

## Presenting Results

When a report completes, present it to the user in this format:

1. **Summary**: Show the key findings and structure of the report
2. **Metrics**: Report how many papers were found and used
3. **File**: Offer to save the full Markdown to a file

```
## Report Complete

- **Report ID**: fdaca9e7-b1cc-4286-a7fc-8c466d8e8554
- **Papers retrieved**: 100 | **Deduplicated**: 53 | **Matched**: 50
- **Generation time**: ~3 minutes

### Summary Preview
[First few paragraphs of the report summary]

The full report is available as Markdown. Would you like me to save it to a file?
```

---

## Error Handling

| Scenario | What to do |
|---|---|
| HTTP 401 | Check API key — verify `SCHOLAR_API_KEY` env var or use the built-in key |
| HTTP 429 | Rate limited — wait and retry. Reports have separate rate limits from searches |
| Report stuck (progress unchanged for 5+ minutes) | The `data.error` field may contain details. Report the issue to the user |
| Markdown download returns empty | Check `result.artifacts.markdown_available` is `true` before downloading |
| `status` remains `pending` for > 2 minutes | The job queue may be busy. Continue polling. |

---

## Integration with scholar-search

These two skills work together naturally:

1. **Search first, report second**: Use `scholar-search` to explore a topic and confirm it has enough literature
2. **Refine filters**: Use search facets (years, venues, paper types) to set report filters
3. **Author-context**: Search for key authors first, then include their `author_refs` in report filters if needed
4. **Deep dive**: After a report, use `scholar-search` to find more papers on specific subtopics from the report

---

## Notes

- Reports are asynchronous — always poll after creating
- The free API key has monthly quotas; higher quotas available at https://scholar.x49.ai/docs?section=api-keys
- Report markdown includes inline citations linking to a References section at the bottom
- The `result.papers[].author_ref` may be `null` in report results — use `scholar-search` for full author details
- Save completed reports to the project directory for future reference
