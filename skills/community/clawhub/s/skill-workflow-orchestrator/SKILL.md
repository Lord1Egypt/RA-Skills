---
name: skill-workflow-orchestrator
description: Multi-skill workflow orchestrator. Chain multiple skills into automated pipelines, triggering entire sequences like "search → summarize → generate report → send email" with a single phrase. Supports conditional branching and error handling; serves as foundational infrastructure for building complex Agent workflows.
---

# Skill Workflow Orchestrator

## Overview

This skill orchestrates multiple sub-skills into automated pipelines. A complete skill chain can be triggered through natural language descriptions, supporting sequential execution, conditional branching, and error handling.

## Use Cases

Automatically triggers when user descriptions involve multi-step tasks, for example:
- "Search for the latest AI news, generate a summary report, and then email it to me."
- "Check the stock price; if it rises more than 5%, remind me."
- "Read the PDF file, extract the content, summarize it, and save it to notes."

## Workflow Definition

### 1. Parse User Intent

Parse the user's natural language description into a structured skill chain:

```
User: "Search AI news → Summarize → Send email"
→ Parsed into:
[
  {"skill": "multi-search-engine", "task": "Search latest AI news"},
  {"skill": "content-summarizer", "task": "Generate summary"},
  {"skill": "email-skill", "task": "Send email"}
]
```

### 2. Sequential Execution

Invoke each skill in order, with the output of the previous skill serving as the input for the next:

```python
# Pseudocode example
results = []
for step in workflow:
    skill = load_skill(step.skill)
    input_data = results[-1] if results else None
    result = skill.execute(step.task, input_data)
    results.append(result)
```

### 3. Conditional Branching

Supports if/else logic:

```
If [condition] → Execute [Skill A]
Else → Execute [Skill B]
```

Supported comparison operators:
- Numeric comparison: `>`, `<`, `>=`, `<=`, `==`, `!=`
- String containment: `contains`, `startswith`, `endswith`
- Boolean checks: `is_true`, `is_false`, `exists`

### 4. Error Handling

- **Retry Mechanism**: Automatically retry failed steps up to 2 times
- **Skip and Continue**: Optionally continue executing subsequent steps when a step fails
- **Fallback Execution**: Support defining an alternative skill chain on failure

## Built-in Templates

### Template 1: Information Gathering Chain

```
Search → Content Extraction → Organize and Save
```

Use Cases: Competitor research, news tracking, data collection

### Template 2: Analysis Report Chain

```
Fetch Data → Analyze and Process → Generate Report → Send Notification
```

Use Cases: Stock analysis, operational reports, data dashboards

### Template 3: Content Creation Chain

```
Topic Selection → Search Material → Create Content → Review and Publish
```

Use Cases: Blog posts, social media management

## Configuration Options

Specifiable within a workflow:

| Option | Description | Example |
|--------|-------------|---------|
| `timeout` | Timeout per skill (seconds) | `30` |
| `retry` | Number of retry attempts on failure | `2` |
| `continue_on_error` | Whether to continue after failure | `true/false` |
| `output_format` | Final output format | `json/markdown/text` |

## Usage Examples

### Example 1: Simple Chain

> User: Search for the latest developments in quantum computing, generate a summary, and save it to notes.

```json
{
  "steps": [
    {"skill": "multi-search-engine", "task": "Latest developments in quantum computing"},
    {"skill": "content-summarizer", "task": "Generate summary"},
    {"skill": "ima-skill", "task": "Save to notes"}
  ]
}
```

### Example 2: With Conditional Branching

> User: Check the price of BTC; if it drops below $50,000, remind me to sell.

```json
{
  "steps": [
    {"skill": "neodata-financial-search", "task": "BTC price"},
    {
      "condition": "price < 50000",
      "then": [{"skill": "message", "task": "Remind to sell"}],
      "else": []
    }
  ]
}
```

### Example 3: With Error Handling

> User: Read this PDF, extract the table data; if it fails, send me an email notification.

```json
{
  "steps": [
    {"skill": "pdf", "task": "Read PDF", "retry": 3},
    {"skill": "xlsx", "task": "Extract table data"}
  ],
  "on_error": {
    "skill": "email-skill",
    "task": "Send error notification"
  }
}
```

## Notes

1. Total skill chain length is recommended not to exceed 10 steps
2. Complex workflows should be split into multiple simpler chains
3. Sensitive operations (e.g., sending emails, messages) require user confirmation
4. Periodically check the validity and latest versions of all sub-skills