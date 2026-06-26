---
name: unifuncs-deep-research
description: Use UniFuncs Deep Research API to run in-depth research and generate long-form reports (10,000 words or more). Use this skill when users request deep research, research reports, or comprehensive analysis.
argument-hint: [query]
allowed-tools: Bash(python3:*)
---

# UniFuncs Deep Research Skill

Use this tool for in-depth analysis and long-form report generation (10,000 words or more). It is suitable when the task requires multiple rounds of searching and reading, or when the user explicitly asks for deep research/deep digging. This is a relatively expensive operation and usually takes **3-10 minutes**.

**Mandatory second confirmation:** Before invoking any Deep Research script (`deep-research-report.py`, `deep-research-create-task.py`, etc.), you **must** pause and get explicit user confirmation in the **same conversation** after you have summarized the request. In one message, briefly restate: (1) the research topic / question to be sent, (2) that it is long-running (~3–10 minutes) and higher cost than deep search, and (3) any key options you plan to use (e.g. `output-type`, `model`) if non-default. **Do not run** the scripts until the user clearly confirms (e.g. “确认 / 可以 / yes / proceed”). If the user adjusts the topic or options, repeat this confirmation step once more before running.

If the intent is still ambiguous after your summary, ask one short clarifying question before offering the confirmation summary.

## First-Time Setup

1. Go to <https://unifuncs.com/account> to get your API key.
2. Set the environment variable: `export UNIFUNCS_API_KEY="sk-your-api-key"`

## When to Use

You need deep, structured research on a topic.
You want a report-style output instead of search report, if the user has not explicitly requested a deep research, consider using [unifuncs-deep-search](https://github.com/UniFuncs/skills/blob/main/skills/unifuncs-deep-search/SKILL.md) instead.
Typical completion time is around **3-10 minutes**, depending on topic complexity.

## Usage Guidelines

1. Complete **Mandatory second confirmation** above.
2. Then use one of the entries below as appropriate.

The skills is split into 3 independent entries:

- `deep-research-report.py` - Synchronously gets the research report. Because it can take longer, set a sufficiently large timeout.
- `deep-research-create-task.py` - Asynchronously creates a research task and returns a task ID. Keep the task ID for later status/result queries to avoid creating duplicate tasks.
- `deep-research-query-task.py` - Queries task status and returns task result/report content.

### 1) Sync report: deep-research-report.py

```bash
python3 deep-research-report.py "query"
```

### 2) Async task creation: create_task

```bash
python3 deep-research-create-task.py "query"
```

This returns `task_id`.

### 3) Async task query: query_task

```bash
python3 deep-research-query-task.py "task_id"
```

## Options

```text
usage: deep-research-report.py [-h] [--model {u1,u1-pro,u2,u3}]
                               [--stream | --no-stream]
                               [--timeout TIMEOUT]
                               [--stream-file STREAM_FILE]
                               [--read-stream-file]
                               [--introduction INTRODUCTION]
                               [--plan-approval]
                               [--reference-style {link,character,hidden}]
                               [--max-depth MAX_DEPTH]
                               [--domain-scope DOMAIN_SCOPE]
                               [--domain-blacklist DOMAIN_BLACKLIST]
                               [--output-type {report,summary,wechat-article,xiaohongshu-article,toutiao-article,zhihu-article,zhihu-answer,weibo-article}]
                               [--output-prompt OUTPUT_PROMPT]
                               [--output-length OUTPUT_LENGTH]
                               [--raw-response]
                               [query]

UniFuncs Deep Research client

positional arguments:
  query                 User query sent to Deep Research.

options:
  -h, --help            show this help message and exit
  --model {u1,u1-pro,u2,u3}
                        Model to use (default: u3).
  --stream              Enable streaming output (default).
  --no-stream           Disable streaming and wait for full response.
  --timeout TIMEOUT     Max streaming wait time in seconds (default:
                        1800).
  --stream-file STREAM_FILE
                        Path to persist/read stream chunks. If omitted,
                        temp file is auto-created when writable.
  --read-stream-file    Read and render already received content from
                        --stream-file, without calling API.
  --introduction INTRODUCTION
                        Researcher role/tone introduction.
  --plan-approval       Generate research plan and wait for approval
                        before execution.
  --reference-style {link,character,hidden}
                        Reference marker style.
  --max-depth MAX_DEPTH
                        Maximum research depth.
  --domain-scope DOMAIN_SCOPE
                        Comma-separated domain allowlist.
  --domain-blacklist DOMAIN_BLACKLIST
                        Comma-separated domain blocklist.
  --output-type {report,summary,wechat-article,xiaohongshu-article,toutiao-article,zhihu-article,zhihu-answer,weibo-article}
                        Desired output style (default: report).
  --output-prompt OUTPUT_PROMPT
                        Custom output prompt template.
  --output-length OUTPUT_LENGTH
                        Expected output length hint (default: 10000).
  --raw-response        Print full API response JSON.
```

## Output Types

- `report` - Long-form report（Default）
- `summary` - Concise summary
- `wechat-article` - WeChat public account article
- `xiaohongshu-article` - Xiaohongshu post
- `toutiao-article` - Toutiao article
- `zhihu-article` - Zhihu article
- `zhihu-answer` - Zhihu answer
- `weibo-article` - Weibo article
