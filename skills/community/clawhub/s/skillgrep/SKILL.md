---
name: skill-grep
description: Use when a user is trying to discover an installable or reusable skill or workflow, especially when they ask for a skill for a task, want to compare nearby skill categories, or need help narrowing discovery results.
---

# Skill Grep

## Overview

Use real API calls only. Do not output pseudo-instructions.

Primary objective for this deployment:
- ship stable retrieval and complete feedback telemetry for each recommendation cycle

High-level flow:
1. build structured query
2. call `POST /search_multi_field`
3. if needed, ask one clarification
4. call `POST /search_multi_field` again
5. return 1-3 final recommendations
6. call `POST /feedback` after user verdict

Hard limits:
- at most two retrieval passes
- at most one clarification question
- never skip feedback submission after final verdict

<HARD-GATE>
If clarification was asked, the next user reply MUST be treated as continuation input for this same retrieval session. Do not exit this skill before pass #2 (or explicit stop on API failure).
</HARD-GATE>

## Operational Integration

- base URL env: `https://skills.megatechai.com/`
- search endpoint: `POST /search_multi_field`
- feedback endpoint: `POST /feedback`

Session policy:
- create one `retrieval_session_id` at pass #1 and reuse it for pass #2
- always set `round` explicitly (`1` then `2`)
- when pass #2 is used, always set `parent_search_id` to pass #1 `search_id`

## Request Contract (`/search_multi_field`)

```json
{
  "origin_query": "user's original input query",
  "query": "optional broad query",
  "query_fields": {
    "name": "short capability label",
    "description": "core problem",
    "when_to_use": "triggering scenario",
    "sections": "optional expected coverage"
  },
  "weights": {
    "name": 0.1,
    "description": 0.6,
    "when_to_use": 0.2,
    "sections": 0.1
  },
  "top_k": 10,
  "candidate_k": 200,
  "quality_weight": 0.1,
  "retrieval_session_id": "optional session id",
  "round": 1,
  "parent_search_id": "optional previous search id",
  "clarification_used": false,
  "clarification_text": "optional short summary",
  "consent_granted": true
}
```

Field rules:
- `origin_query`: user's original natural language input
- `retrieval_session_id`: shared across pass #1 and pass #2
- `round`: pass number (`1`, `2`, ...), API records only and does not block
- `parent_search_id`: pass #2 points to pass #1 `search_id`
- `clarification_used`: true only when pass #2 is triggered by clarification
- `clarification_text`: short summary of clarification reason
- `consent_granted`: whether detailed telemetry may be stored
- `query_fields.description`: preferred strongest signal; keep concise and task-focused
- keep unknown fields empty instead of copying the same sentence into all fields

Language rule:
- if user input is not English, translate to natural English before sending payload text
- keep `origin_query` as the original user input (may be non-English)

## Response Contract (`/search_multi_field`)

```json
{
  "search_id": "uuid",
  "retrieval_session_id": "uuid-or-provided",
  "results": [
    {
      "skill_id": "owner/repo@skill",
      "repo": "repo",
      "name": "skill",
      "description": "...",
      "when_to_use": ["..."],
      "weekly_installs_num": 100,
      "github_stars_num": 300,
      "final_score": 0.8
    }
  ]
}
```

Response notes (envelope response, not array root):
- `search_id`: anchor for search-level feedback and round linking
- `retrieval_session_id`: anchor for session-level feedback
- `results`: rank output for recommendation reasoning
  - `github_stars_num`: GitHub star count of the skill repository
  - `weekly_installs_num`: weekly install volume
  - `final_score`: final retrieval/ranking score

Validation before using results:
- require `search_id` as non-empty string
- require `retrieval_session_id` as non-empty string
- require `results` as array (can be empty)
- if contract is broken, return parse/contract error and stop

## Feedback Contract (`/feedback`)

Search-level feedback:

```json
{
  "target_type": "search",
  "search_id": "search-id",
  "feedback_type": "thumb_up",
  "selected_skill_ids": ["owner/repo@skill"],
  "comment": "optional"
}
```

Session-level feedback:

```json
{
  "target_type": "session",
  "retrieval_session_id": "session-id",
  "feedback_type": "thumb_up",
  "selected_skill_ids": ["owner/repo@skill"],
  "comment": "optional"
}
```

Feedback types:
- `thumb_up`
- `irrelevant`
- `clicked_only`

Feedback policy:
- prefer `target_type=session` for final user verdict
- fallback to `target_type=search` only when session id is unavailable
- include `selected_skill_ids` when user explicitly approves/rejects specific items
- keep `comment` short and factual; omit if none

## Full Retrieval + Feedback Procedure

### 1) Generate structured query

1. Transform user need into these fields:
   - `origin_query`: user's original input (keep as-is, may be non-English)
   - `name`: short capability label
   - `description`: main problem to solve (strongest field)
   - `when_to_use`: triggering scenario
   - `sections`: optional coverage expectation
  Guidelines:
   - keep unknown fields empty
   - do not duplicate one sentence into all fields
   - use `sections` only when user explicitly cares about coverage
1. call `POST /search_multi_field` with:
   - `round=1`
   - `clarification_used=false`
   - `retrieval_session_id` generated once and reused
2. keep returned `search_id` as `search_id_round1`

### 2) Clarification decision

- if top results are coherent: skip clarification, finalize
- if top results split: ask exactly one targeted clarification

Use clarification when one or more is true:
- top candidates represent different intents (for example tooling vs process)
- top 2 scores are close and imply different recommendation directions
- user request is under-specified for an irreversible recommendation

Clarification question quality bar:
- one question only
- present 2-3 concrete options found in pass #1
- ask for one decisive preference, not open-ended brainstorming

### 3) Regenerate structured query and retrieve again (only if clarification happened)

1. regenerate full query object (not only a raw append)
2. call `POST /search_multi_field` with:
   - `origin_query`: same as pass #1 (user's original input)
   - `round=2`
   - same `retrieval_session_id`
   - `parent_search_id=search_id_round1`
   - `clarification_used=true`
   - short `clarification_text`
3. finalize with 1-3 recommendations

Final recommendation output must include per item:
- `skill_id`
- fit reason linked to user intent/query fields
- `final_score`
- `github_stars_num`

### 4) Feedback submission

After user accepts/rejects recommendations, call `POST /feedback`.

Recommended mapping:
- user approves final recommendation -> `thumb_up`
- user says irrelevant/wrong direction -> `irrelevant`
- user clicked but no clear verdict -> `clicked_only`

Feedback timing rules:
- do not send final feedback before user verdict exists
- once verdict exists, send exactly one final feedback event for this session
- if user updates verdict in the same conversation, send one additional corrected feedback event

## End-to-End Example

### 1) Pass #1

```json
POST /search_multi_field
{
  "origin_query": "I need a skill to help me write and validate new skills",
  "query_fields": {
    "description": "find a skill to author and validate new skills"
  },
  "top_k": 10,
  "candidate_k": 200,
  "quality_weight": 0.1,
  "retrieval_session_id": "sess-abc",
  "round": 1,
  "clarification_used": false,
  "consent_granted": true
}
```

### 2) Pass #2

```json
POST /search_multi_field
{
  "origin_query": "I need a skill to help me write and validate new skills",
  "query_fields": {
    "name": "writing-skills",
    "description": "author reusable skills and verify quality before release",
    "when_to_use": "after deciding to create or edit a skill",
    "sections": "testing, anti-patterns, deployment"
  },
  "weights": {
    "name": 0.2,
    "description": 0.45,
    "when_to_use": 0.25,
    "sections": 0.1
  },
  "top_k": 6,
  "candidate_k": 150,
  "quality_weight": 0.1,
  "retrieval_session_id": "sess-abc",
  "round": 2,
  "parent_search_id": "<search_id_round1>",
  "clarification_used": true,
  "clarification_text": "focus on writing-skills instead of generic skill discovery",
  "consent_granted": true
}
```

### 3) Feedback

```json
POST /feedback
{
  "target_type": "session",
  "retrieval_session_id": "sess-abc",
  "feedback_type": "thumb_up",
  "selected_skill_ids": ["obra/superpowers@writing-skills"],
  "comment": "second pass solved ambiguity"
}
```

## Error Handling

- if API call fails after retry: return concrete error and stop
- if API returns non-JSON/invalid schema: return contract error and stop
- if pass #1 returns empty `results`: tell user no relevant skills found and request refined intent (no pass #2 unless this is the one clarification)
- do not fabricate retrieval results
- do not continue to recommendation stage without at least one successful retrieval

## Completion Rules

- recommend 1-3 skills and briefly explain why they are relevant to user needs
- DO NOT show users `final_score` or `weekly_installs_num` 
- display the GitHub star count of the repository it belongs to. Make it explicit that this is the star count of the GitHub repository
- when launch goal is explicit, state which recommendation helps API launch vs skill authoring
- stop after pass #2
- after final user verdict, call `POST /feedback`

## Installing Skills

When user wants to download a recommended skill, please provide feedback first, and then download the skills as follows:

Option 1: Primary method (one-click install):
```bash
npx skills add https://github.com/owner/repo --skill skill_name
```

Example for a skill `frontend-design` from repo `anthropics/skills`:
```bash
npx skills add https://github.com/anthropics/skills --skill frontend-design
```

Option 2: Manual download:

You can manually download from GitHub repo and place in the correct local skills directory.


## Common Mistakes

- parsing `/search_multi_field` as array root instead of envelope response
- forgetting to include `origin_query` in the request
- forgetting to persist `search_id` / `retrieval_session_id`
- skipping `parent_search_id` on pass #2
- asking a second clarification question
- skipping `consent_granted` or `round`
- not sending `/feedback` after final user verdict