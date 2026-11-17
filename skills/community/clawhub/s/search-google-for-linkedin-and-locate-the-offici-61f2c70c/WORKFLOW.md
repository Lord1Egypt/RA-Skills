---
id: "workflow.a15dcc0297b3fc2c"
type: executable-workflow
schema_version: "oyster-workflow-graph-v2"
revision: 1
revision_id: "workflow.a15dcc0297b3fc2c:rev-1:ebb729b57019"
source_skill_id: "a15dcc0297b3fc2c"
source_episode_id: "20260717T022346Z-g5ybl8-ep-0001"
---

# Find official LinkedIn result via Google

> Review projection only / 仅供审查。`workflow.json` is the canonical executable graph / 是规范执行图。

## Goal / 目标

Find the official LinkedIn entry point from Google search results.

## Provenance / 来源

- Source skill: `skill:a15dcc0297b3fc2c`
- Skill ID: `a15dcc0297b3fc2c`
- Run: `20260717T022346Z-g5ybl8`
- Episode: `20260717T022346Z-g5ybl8-ep-0001`
- Revision: `workflow.a15dcc0297b3fc2c:rev-1:ebb729b57019`
- Content hash: `ebb729b570190ec3e0b84c5ff53a9f4ff35142589e13a44471af76aad11f45df`

## Graph / 图

```mermaid
flowchart TD
  N1["Search Google for LinkedIn"]
  N2(["Wait: Wait for Google results"])
  N3["Locate official LinkedIn entry point"]
  N4(["Official LinkedIn result located"])
  N1 -->|next| N2
  N2 -->|resume (Google results page for “linkedin” has loaded.)| N3
  N3 -->|next| N4
```

## Nodes / 节点

### search-linkedin

**Search Google for LinkedIn**

- Type: `action`
- Objective: Start from Chrome and submit a Google web search for the query “linkedin.”
- Act: Open Google Chrome to a new tab or another Google search entry point.; Enter “linkedin” in the address bar or Google search box and submit the search.
- App: Google Chrome
- Hints: Use Google search rather than typing a potentially incomplete or unverified URL directly.
- Source refs:
  - Search Google for LinkedIn and locate the official sign-in result — `skill:a15dcc0297b3fc2c`
  - 20260717T022346Z-g5ybl8-ep-0001 — `episode:20260717T022346Z-g5ybl8:20260717T022346Z-g5ybl8-ep-0001`
- Routes:
  - next → [Wait for Google results](#wait-for-results)

### wait-for-results

**Wait for Google results**

- Type: `wait`
- Wait for: Google search results page for the submitted query to load.
- Resume when: The results page is visible and shows the query “linkedin.”
- Source refs:
  - Search Google for LinkedIn and locate the official sign-in result — `skill:a15dcc0297b3fc2c`
  - 20260717T022346Z-g5ybl8-ep-0001 — `episode:20260717T022346Z-g5ybl8:20260717T022346Z-g5ybl8-ep-0001`
- Routes:
  - resume (Google results page for “linkedin” has loaded.) → [Locate official LinkedIn entry point](#locate-official-result)

### locate-official-result

**Locate official LinkedIn entry point**

- Type: `action`
- Objective: Identify the official LinkedIn result on the Google results page.
- Act: Confirm the results are for “linkedin.”; Find the official linkedin.com result, such as “LinkedIn: Log In or Sign Up.”
- App: Google Chrome
- Hints: The official result indicator may appear as “LinkedIn: Log In or Sign Up” from linkedin.com.
- Source refs:
  - Search Google for LinkedIn and locate the official sign-in result — `skill:a15dcc0297b3fc2c`
  - 20260717T022346Z-g5ybl8-ep-0001 — `episode:20260717T022346Z-g5ybl8:20260717T022346Z-g5ybl8-ep-0001`
- Routes:
  - next → [Official LinkedIn result located](#official-result-located)

### official-result-located

**Official LinkedIn result located**

- Type: `terminal`
- Outcome: `completed`
- Summary: The Google results page for “linkedin” is loaded and the official LinkedIn log in or sign up result from linkedin.com is visible.
- Source refs:
  - Search Google for LinkedIn and locate the official sign-in result — `skill:a15dcc0297b3fc2c`
  - 20260717T022346Z-g5ybl8-ep-0001 — `episode:20260717T022346Z-g5ybl8:20260717T022346Z-g5ybl8-ep-0001`
