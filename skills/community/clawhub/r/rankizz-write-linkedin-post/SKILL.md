---
name: rankizz-write-linkedin-post
description: Research current LinkedIn posts around a keyword with Rankizz, identify evidence-backed hooks and formats, and write a useful LinkedIn post in the user's real voice with a transparent, restrained product mention. Use when a user wants LinkedIn topic research, a knowledge-first product post, hook options, or a local Markdown report containing sources and a ready-to-review draft.
---

# Write a LinkedIn post from current research

Create a post worth saving even if the reader never tries the product. Research what is currently resonating, then add the user's own experience instead of imitating another creator.

Read [references/linkedin-post-research.md](references/linkedin-post-research.md) before searching or drafting.

## Invoke Rankizz MCP tools

When using Rankizz through MCP, the initial tool list is intentionally compact. Call `search_tools` with a capability query or exact domain-tool name and set `includeSchemas: true` unless the arguments are already known. Invoke a discovered tool with `call_read_tool` when its `readOnlyHint` is `true`; use `call_tool` for every other tool. Pass the discovered name as `tool` and its original input object as `arguments`. REST callers continue to use the direct `/api/v1/tools/<tool-name>` endpoint.

## Guardrails

- Use Rankizz LinkedIn search. This workflow requires Rankizz and normally consumes one credit for one provider search.
- Confirm the Rankizz account has at least 10 credits before making a paid MCP or API call. If it does not, stop and tell the user to add credits.
- Never invent personal experience, customer results, revenue, experiments, credentials, or product capabilities.
- Disclose the writer's relationship to a mentioned product. Prefer plain language such as `I built`, `our team makes`, or `I work on`.
- Do not copy another post's wording, story, distinctive structure, or creative asset.
- Do not automate publishing, comments, likes, follows, connection requests, or direct messages.
- Treat `90% knowledge, 10% promotion` as an editorial standard, not a LinkedIn ranking formula.
- Describe popularity only relative to the sampled posts and time window. Do not promise virality or reach.

## Gather the brief

Ask for or locate:

- the topic or seed keyword;
- the intended reader and their job-to-be-done;
- the author's role, voice, expertise, and genuine first-hand observations;
- the product name, purpose, differentiator, and relationship to the author;
- verified examples, data, screenshots, or lessons that may be shared publicly;
- the post goal: teach, start a discussion, announce a lesson, or explain a workflow;
- the desired report directory.

If first-hand detail is missing, write from documented facts and label any open slot for the user. Never manufacture a personal anecdote to make the draft sound human.

## Research current LinkedIn posts

### 1. Reuse useful research

Use `list_social_research_history` when the user may already have a recent, relevant run. Reusing saved research costs no new search credit.

### 2. Search once with focused variants

Start with one `search_social_research` request. Combine up to a few useful query variants instead of spending one request per phrase.

```json
{
  "platform": "linkedin",
  "queries": ["technical SEO workflow", "technical SEO mistakes", "site audit lessons"],
  "filters": { "datePosted": "last-month" }
}
```

Record the run ID, search date, queries, filter, and credits charged. A returned result is a research lead, not proof that every claim in the post is true.

### 3. Build a comparable sample

Review roughly 10-20 relevant results when available. For each useful result, record:

- URL, author, publication date, and topic;
- hook type and the promise it makes;
- point of view and audience problem;
- evidence used: experience, example, data, screenshot, or none;
- structure: story, framework, list, teardown, contrarian argument, or case study;
- media and call to action;
- available views, likes, comments, or score;
- why it appears useful, specific, or discussable.

Open public post URLs when necessary to inspect context. Do not infer a post's quality from a title or truncated description alone.

### 4. Find patterns without reverse-engineering myths

Compare posts from a similar topic and time window. Note repeated audience problems, underserved questions, evidence styles, readable structures, and hooks associated with stronger observed engagement.

Do not calculate an engagement rate unless both engagement and a valid exposure denominator are available. Do not call a post `viral` because it has a large raw count. LinkedIn's feed considers many signals, including professional relevance, freshness, engagement, and reading behavior; there is no public fixed formula to reproduce.

## Choose an original angle

Pick an angle only when the author can add at least one of:

- a first-hand observation;
- a useful framework or checklist;
- a concrete before-and-after example;
- a well-supported disagreement;
- a clearer explanation of an overlooked problem;
- a repeatable workflow the reader can try.

State the post's one-sentence value promise. If it merely restates the sampled posts, change the angle or gather better input.

## Draft the post

### Open with a strong, honest hook

A good hook exposes a concrete result, tension, mistake, observation, or useful promise. It earns attention without withholding the entire point.

Prefer:

- `We audited 42 landing pages. The pages losing clicks shared one fixable problem.`
- `Most SEO dashboards answer what changed. The useful ones explain what to do next.`
- `A five-minute canonical check prevented us from rewriting the wrong page.`

Avoid:

- `You won't believe what happened next.`
- `This one weird trick changed everything.`
- `Agree?` with no useful argument;
- invented failure, drama, or success;
- generic throat-clearing such as `In today's fast-paced digital world`.

### Deliver the knowledge first

- Use one- or two-sentence paragraphs.
- Use bullets when they make a process, comparison, or checklist easier to scan.
- Put the lesson, method, or example before the product.
- Include specifics the author can defend.
- Vary sentence length naturally. Remove empty hype and repetitive summaries.
- End with a meaningful question, next step, or reflection. Do not use engagement bait.

### Mention the product transparently and briefly

Usually mention the app once. The sentence should explain why it is relevant, not interrupt the lesson.

Good:

> I built Rankizz around this workflow because the hard part was turning audit data into a prioritized next step.

Weak:

> Luckily, Rankizz is the world's best all-in-one solution. Sign up now!

If the post works better without a product mention, omit it. A product mention is not mandatory simply because product information was supplied.

## Do

- Base the post on current research and the author's actual point of view.
- Keep the useful material substantially larger than the promotion.
- Link every research example in the report.
- Distinguish observed patterns from conclusions or recommendations.
- Use natural language the author would say aloud.
- Check all product, number, and performance claims before delivery.
- Give the user a final manual-review checklist.

## Do not

- Rewrite the top-performing post with synonyms.
- Treat hashtags, post length, posting time, or a hook formula as guaranteed ranking factors.
- Fabricate a founder story, client quote, or result.
- Hide the author's commercial relationship to the app.
- Add several product mentions, a sales pitch, or an unrelated link dump.
- Use fake vulnerability, manufactured controversy, or empty contrarianism.
- Claim a post will rank, trend, or go viral.

## Save the local report

Create `linkedin-post-research-YYYY-MM-DD.md` in the user's requested directory, or the current project when no directory is given. If that filename exists, append a short topic slug or timestamp instead of overwriting it.

Use this structure:

```markdown
# LinkedIn post research: [topic]

## Brief
- Audience:
- Author perspective:
- Product and relationship:
- Goal:

## Research log
- Rankizz run ID:
- Searched at:
- Queries and date filter:
- Credits charged:

## Reference posts
| Post | Date | Available metrics | Hook and format | Useful observation |
|---|---|---:|---|---|
| [Author or title](URL) | YYYY-MM-DD | ... | ... | ... |

## Observed patterns
- Common audience problems:
- Stronger observed hooks:
- Evidence and formats:
- Gaps worth addressing:

## Chosen angle
[One-sentence value promise and why the author can credibly make it]

## Hook options
1. ...
2. ...
3. ...

## Draft post
[Ready-to-review post]

## Optional visual
[A useful chart, screenshot, diagram, or `None`]

## Final review
- [ ] Every first-person statement is true
- [ ] Claims and product capabilities are verified
- [ ] The product relationship is clear
- [ ] The post is useful without clicking or buying
- [ ] Source posts influenced the research but were not copied
- [ ] The author will review and publish manually
```

Return the report path, a short summary of the selected angle, the number of source posts reviewed, and the exact Rankizz credits charged.

## Limitations

- Search results and public engagement metrics can be incomplete, delayed, or unavailable.
- A small sample reveals patterns, not universal platform behavior.
- Feed distribution is personalized; observed performance does not predict the user's result.
- The agent cannot verify private analytics, audience fit, or unpublished personal stories without user evidence.
- Final legal, employment, brand, and disclosure review remains the user's responsibility.
