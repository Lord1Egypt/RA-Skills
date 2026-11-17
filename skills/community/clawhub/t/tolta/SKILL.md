---
name: tolta
description: Find jobs that fit the user, apply to their matches and follow their applications with Tolta, an AI job application agent that applies on employers' own career forms. Use when the user asks for job matches or job openings, wants to apply to a job, or asks where their job applications stand.
version: 1.0.0
license: MIT
metadata:
  openclaw:
    homepage: https://tolta.ai/ai-assistants
---

# Tolta: job matches, applications and their status

[Tolta](https://tolta.ai) finds fresh roles on company career boards (Greenhouse, Lever, Ashby, Workday and others), matches them to the user's profile, tailors their CV to each job and applies on the employer's own form. When a form asks something the profile can't answer, Tolta holds the application and asks the user in Tolta instead of guessing.

This skill uses Tolta's remote MCP server. It needs no API key: the user signs in to Tolta and approves access once.

## Connect

If the `tolta` MCP server isn't connected yet, ask the user to run:

```bash
openclaw mcp set tolta '{"url":"https://tolta.ai/mcp","transport":"streamable-http","auth":"oauth"}'
openclaw mcp login tolta
```

The login opens a Tolta page in the browser. The user signs in and approves OpenClaw. If you use the Control UI for the callback, use `http://localhost:18789`, not `127.0.0.1`.

The user needs a Tolta account with a plan or a free trial ([pricing](https://tolta.ai/pricing)). During the trial the tools can read matches, jobs and applications but can't apply. If sign-in says the account needs a plan or a finished profile, send the user to https://app.tolta.ai to finish it, then run the login again.

## Tools

| Tool | Use it to |
|---|---|
| `todays_matches` | Show today's matches, best first, each with a fit score out of 100 and the reasons. |
| `search_jobs` | Search open jobs by keywords, remote arrangement or seniority. Plain sentences work. |
| `get_job` | Read one job's role, salary, requirements and benefits, and the user's fit score. |
| `list_applications` | List the user's applications and which ones are waiting on them. |
| `get_application` | Read one application's status and the questions waiting for the user. |
| `apply_to_match` | Apply to one of today's matches. |

## Rules

- Call `apply_to_match` only when the user asked to apply to that job. It sends a real application (or a draft to review, if the user reviews applications in Tolta).
- Only matches can be applied to from chat. For any other job, give the user its `open_in_tolta` link.
- Never ask the user to type answers to application questions in the chat. Questions are answered in Tolta, through the `open_in_tolta` link.
- Links point to Tolta only; job postings' own links are not returned.

## Learn more

- How Tolta works: https://tolta.ai/how-it-works
- Using Tolta from AI assistants: https://tolta.ai/ai-assistants
