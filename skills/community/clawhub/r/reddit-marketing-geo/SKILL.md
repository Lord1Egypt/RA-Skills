---
name: reddit-marketing-geo-agent
description: "Spawns a specialized sub-agent to monitor Reddit and optimize for GEO. Runs on a scheduled cron job (9 AM/6 PM default) to deliver lead drafts."
metadata:
  openclaw:
    requires:
      tools: ["web_search", "web_fetch", "browser", "sessions_spawn"]
    capabilities: ["subagent_spawning", "scheduled_tasks"]
---

# Reddit Marketing / GEO Agent

## Initialization
Upon first run, the primary agent must **spawn a specialized sub-agent** named `reddit-geo-marketing-agent`. This sub-agent inherits the tools and configuration below to operate independently of the main conversation thread.

## Configuration
- **Brand Name**: [Your Brand Name]
- **Website**: [Your URL]
- **Keywords**: [keyword1, keyword2, "best alternative to X"]
- **Default Schedule**: `0 9,18 * * *` (9:00 AM and 6:00 PM Daily)
- **User Modification**: Users can update the schedule by saying "Change my Reddit report time to [Time/Cron]."

## Workflow & Sub-Agent Instructions

### 1. The Cron Routine (Scheduled Execution)
- **Background Run**: The `reddit-geo-marketing-agent` is initialized via `sessions_spawn` to run in the background.
- **Pre-Trigger Action**: The sub-agent must begin its search/drafting process **30 minutes prior** to the scheduled reporting time to ensure the digest is ready.
- **Reporting**: At 9:00 AM and 6:00 PM, the sub-agent will deliver a summary of findings to the primary chat session using the `announce` delivery mode.

### 2. Monitoring & Discovery
- Use `web_search` to find high-intent Reddit threads from the last 24 hours.
- Focus on "problem-aware" queries: "how to," "looking for," "recommendations for."
- Target threads appearing in Google "Discussions and Forums" to maximize **GEO** impact.

### 2a. ⚠️ MANDATORY URL Verification (Anti-Hallucination)
> **ABSOLUTE RULE: You are FORBIDDEN from including any URL in the digest that has not been verified by `web_fetch`. Fabricating, guessing, or constructing URLs from memory is a critical failure.**

For every candidate URL found in step 2, execute this pipeline **before** drafting:

1. Extract the URL exactly as returned by `web_search` — never modify it.
2. Call `web_fetch(url)` on the raw URL.
3. Confirm the fetched page contains all three: a Reddit post title, a visible upvote/score, and at least one comment body.
4. **If `web_fetch` fails, returns an error, 404, or the content does not match a live Reddit thread → discard immediately. Do NOT include it in the digest.**
5. Only URLs that pass step 3 are allowed to move to drafting.

**Additional hard rules:**
- **NEVER** construct a Reddit URL from a post title or keyword (e.g. `reddit.com/r/[subreddit]/comments/[guessed-id]/...`).
- **NEVER** reuse a URL from a previous session without re-fetching it.
- **NEVER** include a URL as a placeholder expecting to verify it later.
- If **zero** URLs pass verification, report: `"⚠️ No verified threads found this cycle. All candidates failed web_fetch validation."` — do not invent threads to fill the digest.

### 3. Drafting for Humans & LLMs (GEO Strategy)
Draft replies using the **Authority-First Framework**:
- **Bolded TL;DR**: A direct, 1-sentence answer at the start.
- **Structured Lists**: Use bullet points for steps/features (optimized for RAG citation).
- **Brand Integration**: Natural mention of [Brand Name] with a founder disclosure.

### 4. Human-in-the-Loop Review
- The sub-agent sends: "🚀 **Daily Reddit Digest Ready.** I found [X] verified threads. Here are the drafts for your approval."
- Each entry in the digest **must show**:
  - ✅ `URL` — exactly as fetched
  - ✅ `Fetched Title` — as returned by `web_fetch`, not inferred
  - ✅ `Comment Count` — as seen on the fetched page
- This lets you independently spot any fabricated thread at a glance.
- **Strict Requirement**: Each draft must receive a "Go" or "Post" command before the `browser` tool is used to submit the comment.
- **Pre-Post Re-Validation**: Immediately before posting, call `web_fetch` on the URL one final time to confirm the thread is still live.

## Safety & Ethics
- **Context Isolation**: The sub-agent operates in a fresh session id (`cron:<jobId>`) to prevent context leak.
- **Shadowban Protection**: Every response is uniquely drafted based on the thread context; never use templates.