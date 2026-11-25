---
name: rankizz-find-reddit-reply-opportunities
description: Use Rankizz Reddit search to find public posts for a keyword, inspect each thread and subreddit, qualify where the user's expertise or product can genuinely help, draft transparent non-spammy replies, and save a local Markdown opportunity report with direct post links for later manual review. Use for Reddit reply research, community listening, founder-led engagement, keyword monitoring, support opportunities, or a queue of useful Reddit comments. Requires Rankizz MCP or REST API.
---

# Find Reddit reply opportunities

Build a small, high-quality reply queue. Do not turn keyword matches into mass promotion. The user reviews and posts every reply manually.

Read [references/reddit-reply-research.md](references/reddit-reply-research.md) before searching or drafting.

## Invoke Rankizz MCP tools

When using Rankizz through MCP, the initial tool list is intentionally compact. Call `search_tools` with a capability query or exact domain-tool name and set `includeSchemas: true` unless the arguments are already known. Invoke a discovered tool with `call_read_tool` when its `readOnlyHint` is `true`; use `call_tool` for every other tool. Pass the discovered name as `tool` and its original input object as `arguments`. REST callers continue to use the direct `/api/v1/tools/<tool-name>` endpoint.

## Confirm the scope

Collect:

- project ID and Rankizz access method
- product name, verified purpose, useful capabilities, limitations, and target user
- user's relationship to the product
- topics, pain points, phrases, and competitor-neutral keywords
- target or excluded subreddits
- region, language, freshness window, and maximum opportunities
- user's genuine expertise and first-hand examples
- desired local report directory

Do not request a secret in chat. Use OAuth for interactive clients. Direct headless users to `https://www.rankizz.com/api-access`.

## Protect the credit boundary

Rankizz MCP and API calls require at least 10 available credits. `search_social_research` costs one credit for each provider request, even when its `queries` array contains several terms.

Start with one focused request. Add another sort or time window only when the first result set leaves a specific gap. If the balance is low, stop Rankizz calls and direct the user to `https://www.rankizz.com/billing`.

Do not run one call per keyword when a focused combined query will answer the task. Record calls and charged credits in the report.

## Search Reddit

Call `search_social_research` with:

```json
{
  "projectId": "PROJECT_ID",
  "platform": "reddit",
  "queries": ["problem phrase", "job to be done", "specific symptom"],
  "sort": "relevance",
  "timeframe": "month"
}
```

Supported Reddit sorts are `relevance`, `new`, `top`, and `comment_count`. Supported timeframes are `all`, `day`, `week`, `month`, and `year`.

Use:

- `relevance` to find direct problem matches
- `new` to find conversations where a reply is still timely
- `top` to learn what the community values, not necessarily where to reply
- `comment_count` to inspect discussion-heavy formats and saturation

Use `nextCursor` with the same query and `runId` only when another page is likely to produce qualified opportunities. Use `list_social_research_history` when a recent saved run already covers the scope.

## Inspect every candidate live

Rankizz discovery is not the final permission check. Open each original URL and verify:

- the post is public, live, open to replies, and still relevant
- the question or problem has not been fully resolved
- the subreddit topic and current rules
- self-promotion, links, surveys, and solicitation rules
- pinned moderator guidance and required flair
- the thread's tone and the author's actual request
- existing replies, including whether a similar product answer already exists
- whether the user's product is necessary, merely relevant, or irrelevant

Do not collect private data, infer sensitive traits, or move the conversation into unsolicited direct messages.

## Qualify the opportunity

Score with evidence, not optimism:

| Factor | Score |
| --- | ---: |
| Direct match to the stated problem | 0 to 3 |
| User can add a new, concrete answer | 0 to 3 |
| Thread is fresh and open | 0 to 2 |
| Rules permit the drafted reply | 0 to 2 |
| Existing replies already solve it | subtract 0 to 2 |
| Product mention would be forced | subtract 0 to 3 |

Classify each result:

- `reply with disclosure`: a useful answer and one product mention are allowed
- `help only`: the user can contribute, but the product should not appear
- `watch`: relevant research, weak reply timing or fit
- `skip`: off-topic, prohibited, closed, saturated, risky, or low value

No score can override subreddit rules.

## Draft the reply

Reddit comment replies do not need a catchy hook. Answer the person's question in the first sentence.

Then:

1. add the missing explanation, step, example, or tradeoff
2. use one or two short paragraphs or a compact list when helpful
3. mention the product at most once only if it materially solves the stated problem
4. disclose the relationship in the same sentence
5. avoid a product link unless the rules allow it and the reader explicitly needs it
6. close naturally, without asking for a DM, demo, signup, or generic engagement

The reply must still solve something if the product sentence is removed.

Good disclosure:

> I built TaskLoom for this exact handoff, but the same setup works in a spreadsheet if you keep one owner and one due date per row.

Bad disguise:

> I recently found a tool called TaskLoom that might be perfect for you.

Never claim to be a customer when the user owns, works for, or is paid by the product.

## Sound like a person

- Match the thread's vocabulary and level of detail.
- Use simple words and specific steps.
- Keep paragraphs short.
- Do not force jokes, slang, typos, gratitude, or a personal story.
- Use first person only for experience the user supplied.
- Remove corporate claims, praise adjectives, canned empathy, and AI filler.
- Do not copy language from existing replies.
- Remove em dashes and en dashes from final drafts.

## Save the report locally

Write a Markdown file to the user's requested directory. If none is given, use the current project directory with a name such as:

```text
reddit-reply-opportunities-YYYY-MM-DD.md
```

Do not overwrite an existing report. Add a time or numeric suffix instead. Include direct Reddit URLs so the user can review opportunities later.

The report is a research artifact, not authorization to post. Do not submit replies, vote, follow accounts, contact moderators, or send messages.

## Do and do not

| Do | Do not |
| --- | --- |
| Start with one bounded paid search | Spend credits on broad one-keyword calls without a plan |
| Open and verify every candidate | Draft from search snippets alone |
| Read current subreddit rules | Treat platform rules as the only rules |
| Answer the actual question first | Lead with the app or founder story |
| Disclose the product relationship | Pose as a happy independent customer |
| Use one product mention at most | Repeat the brand or hide it behind a link |
| Keep help-only opportunities | Force a product plug into every thread |
| Report why a candidate was excluded | Pad the list to meet a requested count |
| Save direct links and checked dates | Present old or locked threads as ready opportunities |
| Leave posting to the user | Automate comments, votes, DMs, or cross-posts |

## Examples

### Qualified opportunity

Post: `How do small agencies stop client approvals from disappearing in email?`

Why it qualifies:

- the user can explain a concrete approval workflow
- the thread is open and has no complete process answer
- the subreddit allows disclosed tool mentions in comments

Draft:

> Give every deliverable one approval owner and one deadline. If feedback arrives anywhere else, copy it back to that record before making the change.
>
> A simple setup is:
>
> - one link to the current version
> - one person who can approve
> - one visible status
> - one place for final comments
>
> I work on TaskLoom, which handles that record, but a shared sheet works if the team treats it as the source of truth.

### Help-only opportunity

If the subreddit bans any product mention, keep the workflow answer and remove the last sentence. Do not replace it with `check my profile`.

### Skip

Skip a six-month-old thread that is locked, already has several complete answers, or asks for a solution the product does not provide.

## Limitations

- Rankizz results may omit posts, comments, removals, or metrics and may contain stale snapshots.
- Search score, comments, and post age do not reveal subreddit size, impressions, or the author's intent.
- Rules, thread state, and moderator interpretation can change after the report is written.
- The skill cannot verify private account standing, karma requirements, or personal experience not supplied by the user.
- Disclosure and advertising requirements vary by jurisdiction and employer.
- A relevant reply can still be downvoted or removed.
- The user must fact-check, personalize, post, and respond manually.

## Report template

```markdown
# Reddit reply opportunity report

- Product:
- Relationship disclosure:
- Topics:
- Subreddits:
- Search date:
- Report path:

## Search log
| Run | Query | Sort/timeframe | Results | Credits charged |
| --- | --- | --- | ---: | ---: |

## Opportunity queue
| Priority | Post | Subreddit | Status | Score | Product mention |
| ---: | --- | --- | --- | ---: | --- |
| 1 | [Post title](https://reddit.com/...) | r/example | Reply with disclosure | 8 | Allowed once |

## Opportunity 1: [Post title]
- Link:
- Subreddit:
- Published:
- Thread state checked:
- Rule sources:
- Author's actual need:
- What existing replies miss:
- Why the user can help:
- Classification:
- Product fit:
- Risks or unknowns:

### Draft reply
[Direct answer]

[Steps or evidence]

[One disclosed product mention only if allowed]

### Before posting
- [ ] Reopen the post and rules
- [ ] Personalize every first-person detail
- [ ] Confirm the reply adds something new
- [ ] Confirm the product appears zero or one time
- [ ] Post manually and return for replies

## Help-only opportunities
[Useful threads where no product should be mentioned]

## Excluded results
| Post | Reason excluded |
| --- | --- |

## Research limitations
[Missing metrics, inaccessible pages, uncertain rules, or stale results]
```
