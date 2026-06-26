---
name: sentry-error-analyzer
description: Analyze Sentry error patterns, prioritize issues by user impact, identify root causes, and suggest targeted fixes. Use when asked to triage errors, analyze crash reports, or find the most impactful bugs to fix.
metadata:
  tags: ["sentry", "error-tracking", "debugging", "observability", "triage"]
---

# Sentry Error Analyzer

Analyze Sentry error data to find the bugs that actually matter. Parse error events, group by root cause, rank by user impact, and produce actionable fix recommendations — not just a list of stack traces.

Use when: "analyze our Sentry errors", "what should we fix first", "triage these crashes", "find the root cause of this error spike", "which errors affect the most users", or when you have Sentry export data or API responses to analyze.

## Why This Matters

Most teams drown in Sentry noise. Thousands of issues, most irrelevant. The difference between a good team and a great team is knowing which 5 errors to fix this sprint. This skill turns raw error data into a prioritized action plan.

## Input Formats

This skill works with any of the following:

1. **Sentry API JSON** — output from `/api/0/projects/{org}/{project}/issues/`
2. **Sentry CSV export** — exported from the Issues page
3. **Raw error logs** — stack traces with timestamps and metadata
4. **Sentry event JSON** — individual event payloads from the event detail API
5. **Pasted Sentry issue URLs** — extract org/project/issue ID and describe analysis steps

## Analysis Steps

### 1. Parse and Normalize Error Data

Extract these fields from each error/issue:

```
- issue_id: Unique Sentry issue identifier
- title: Error message (first line)
- culprit: File/function where the error originated
- type: Exception class (TypeError, ValueError, HTTP 500, etc.)
- count: Total event count in the time window
- user_count: Unique users affected
- first_seen: When the error first appeared
- last_seen: Most recent occurrence
- level: fatal / error / warning
- tags: browser, os, release, environment
- stack_trace: Full traceback (most recent frame first)
```

For Sentry API data:
```bash
# Fetch issues sorted by frequency
curl -s -H "Authorization: Bearer $SENTRY_AUTH_TOKEN" \
  "https://sentry.io/api/0/projects/{org}/{project}/issues/?query=is:unresolved&sort=freq&limit=50" \
  | jq '.[] | {id, title, culprit, count, userCount, firstSeen, lastSeen, level}'

# Fetch events for a specific issue
curl -s -H "Authorization: Bearer $SENTRY_AUTH_TOKEN" \
  "https://sentry.io/api/0/issues/{issue_id}/events/?limit=10" \
  | jq '.[].entries[] | select(.type == "exception")'

# Get issue tags breakdown
curl -s -H "Authorization: Bearer $SENTRY_AUTH_TOKEN" \
  "https://sentry.io/api/0/issues/{issue_id}/tags/" \
  | jq '.[] | {key, totalValues, topValues: [.topValues[] | {value, count}]}'
```

### 2. Classify Error Types

Group every error into one of these categories:

| Category | Indicators | Typical Impact |
|----------|-----------|----------------|
| **Crash** | Unhandled exception, SIGABRT, OOM | Users lose data/session |
| **Data Corruption** | Integrity errors, failed validations downstream | Silent, devastating |
| **Integration Failure** | HTTP 5xx from third-party, timeout, connection refused | Feature broken |
| **Client Error** | TypeError, undefined access, null ref in frontend | Broken UI element |
| **Performance Degradation** | Timeout errors, slow query warnings, 504s | Frustrated users |
| **Config/Deploy** | Errors that start exactly at a deploy timestamp | Usually affects everyone |
| **Edge Case** | Low frequency, specific user agents or inputs | Low priority unless data loss |

### 3. Calculate Impact Score

Rank each issue using this composite score:

```
Impact Score = (user_count * 3) + (event_count * 0.5) + (severity_weight * 10) + (recency_bonus) + (trend_bonus)

Where:
  severity_weight:
    fatal = 5, error = 3, warning = 1

  recency_bonus:
    last_seen < 1 hour ago  = 20
    last_seen < 24 hours    = 10
    last_seen < 7 days      = 5
    older                   = 0

  trend_bonus:
    events increasing week-over-week = 15
    events stable                    = 0
    events decreasing                = -5
```

### 4. Identify Root Causes

For each top-priority issue, perform root cause analysis:

**Stack Trace Analysis:**
```
1. Read the stack trace bottom-to-top (most recent call first in Python/JS)
2. Skip framework internals — find the first frame in YOUR code
3. Identify the exact line and the variable/value that caused the error
4. Check if the same culprit file appears in multiple issues (systemic problem)
```

**Correlation Checks:**
```bash
# Check if errors correlate with a specific release
# Look at firstSeen vs deploy timestamps
jq '.[] | select(.firstSeen > "2026-04-25") | {title, firstSeen, count}' issues.json

# Check if errors correlate with a specific browser/OS
jq '.tags[] | select(.key == "browser") | .topValues' event.json

# Check if errors cluster at specific times (cron job? peak traffic?)
jq '[.[].dateCreated | split("T")[1] | split(":")[0]] | group_by(.) | map({hour: .[0], count: length})' events.json
```

**Common Root Cause Patterns:**
- Same exception in multiple endpoints = shared utility function bug
- Null/undefined errors after a deploy = missing migration or config
- Timeout errors at specific hours = resource contention or cron overlap
- Errors only on specific browser = missing polyfill or CSS issue
- Errors with specific user IDs = data-dependent bug (corrupt record)

### 5. Generate Fix Recommendations

For each root cause, produce:

```
1. Immediate mitigation (can we reduce impact NOW?)
   - Feature flag to disable broken path
   - Add a try/catch with graceful fallback
   - Revert the deploy that introduced it

2. Root fix (what code change resolves this?)
   - Specific file and function to modify
   - The defensive check or logic fix needed
   - Example code patch when possible

3. Prevention (how do we stop this class of bug?)
   - Missing test case to add
   - Type safety improvement
   - Input validation to add
   - Monitoring/alerting to add
```

### 6. Detect Anti-Patterns

Flag these common Sentry anti-patterns in the project:

- **Swallowed Exceptions** — catch blocks that log but don't report to Sentry
- **Missing Context** — errors without user ID, request URL, or breadcrumbs
- **Over-Grouping** — Sentry fingerprinting is too aggressive, hiding distinct bugs
- **Under-Grouping** — Same bug appears as 50 separate issues due to dynamic error messages
- **Alert Fatigue** — More than 100 unresolved issues with no assignee
- **Stale Issues** — Issues open for 90+ days with no activity (resolve or assign)
- **Missing Source Maps** — JavaScript errors showing minified code (useless stack traces)
- **No Release Tracking** — Errors not tagged with release version (can't correlate with deploys)

## Output Format

```markdown
# Sentry Error Analysis Report

**Project:** {project_name}
**Time Window:** {start_date} to {end_date}
**Total Issues Analyzed:** {count}
**Total Events:** {event_count}
**Unique Users Affected:** {user_count}

## Executive Summary

{2-3 sentences: what's the biggest problem, how many users are affected, what's the recommended action}

## Top 5 Issues by Impact

### 1. {Issue Title} (Impact Score: {score})
- **Issue ID:** PROJ-{id}
- **Events:** {count} | **Users:** {user_count} | **First Seen:** {date}
- **Category:** {Crash|Integration|Client|Performance|Config}
- **Root Cause:** {one-line explanation}
- **Fix:** {specific recommendation}
- **Effort:** {Low|Medium|High}

### 2. {Issue Title} (Impact Score: {score})
...

## Error Trends

- **New This Week:** {count} issues introduced since last deploy
- **Regression:** {count} previously resolved issues that reappeared
- **Improving:** {count} issues with decreasing frequency
- **Worsening:** {count} issues with increasing frequency

## Systemic Issues

- {List of shared root causes that affect multiple issues}
- {Anti-patterns detected in error handling}

## Recommended Sprint Plan

1. **Fix immediately (P0):** {issue} — affects {N} users, data loss risk
2. **Fix this sprint (P1):** {issue} — affects {N} users, broken feature
3. **Schedule (P2):** {issue} — low impact but easy fix
4. **Monitor (P3):** {issue} — watch for trend change
5. **Resolve as won't-fix:** {issue} — reason: {noise/expected/third-party}
```

## Tips

- Always check if errors correlate with deploys before diving into code — a revert may be the fastest fix
- User count matters more than event count — one user hitting a retry loop inflates event count
- Fatal errors with 1 user may matter more than warnings with 1000 if that user is a paying customer
- Look at breadcrumbs (user actions before the error) to understand reproduction steps
- Group errors by culprit file first — if one file causes 40% of errors, that file needs refactoring
- Check the "first seen" date — errors that exist since project inception are usually accepted tech debt
- Monitor error rates as a percentage of traffic, not absolute numbers — growth hides bug fixes
