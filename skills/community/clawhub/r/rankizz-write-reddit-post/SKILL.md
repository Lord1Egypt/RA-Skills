---
name: rankizz-write-reddit-post
description: Research a subreddit's current rules, culture, and successful topic patterns, then draft an original, useful Reddit post that sounds like a real community member rather than an advertisement. Use when a user wants a founder post, educational post, build-in-public post, discussion, case study, or product-adjacent Reddit post with a catchy but honest title, short paragraphs, useful bullets, and at most one transparent mention of the user's app. Rankizz Reddit research is optional.
---

# Write a useful Reddit post

Write for one subreddit, not for Reddit in general. Give readers a complete payoff even if they never search for the product. Treat a soft product mention as brief and contextual, never hidden.

Read [references/reddit-post-standards.md](references/reddit-post-standards.md) before researching or drafting.

## Invoke Rankizz MCP tools

When using Rankizz through MCP, the initial tool list is intentionally compact. Call `search_tools` with a capability query or exact domain-tool name and set `includeSchemas: true` unless the arguments are already known. Invoke a discovered tool with `call_read_tool` when its `readOnlyHint` is `true`; use `call_tool` for every other tool. Pass the discovered name as `tool` and its original input object as `arguments`. REST callers continue to use the direct `/api/v1/tools/<tool-name>` endpoint.

## Build the brief

Resolve:

- target subreddit and the reader's problem
- post goal: teach, discuss, share data, tell a real story, show work, or request feedback
- author's genuine relationship to the topic
- app name, verified purpose, real differentiator, and target user
- author's relationship to the app: founder, employee, client, affiliate, or ordinary user
- facts, measurements, screenshots, failures, and lessons the author can prove
- whether the user wants a product link and whether the subreddit permits one
- language, region, and desired posting window

Do not invent first-hand experience, customer outcomes, revenue, experiments, quotations, or mistakes. Ask for missing evidence or narrow the post.

## Pass the subreddit gate

Open the current subreddit rules, pinned moderator posts, wiki guidance, post composer notices, and several recent posts. Record:

- topic and format restrictions
- self-promotion, survey, link, and showcase rules
- flair, account-age, karma, title, and posting-frequency requirements
- whether moderator permission is required
- recurring tone and formatting norms
- examples of posts moderators removed or locked, when visible

Classify the draft path:

- `allowed`: the planned post and one disclosed mention fit the written rules
- `permission needed`: contact moderators before drafting a promotable version
- `no product mention`: the topic is allowed but promotion is not
- `do not post`: the post itself would be off-topic or disallowed

Never disguise a commercial post to evade a no-promotion rule. If the rules are unclear, draft a value-only version or recommend ModMail.

## Study relevant posts

Use public browsing or Rankizz Reddit search when connected research will change the angle. For Rankizz, call `search_social_research` with `platform: "reddit"`, focused `queries`, a suitable `sort`, and a bounded `timeframe`. A provider search costs one credit and requires at least 10 available credits.

Study posts from the same subreddit and topic. Compare posts within similar time windows because age and community size distort raw scores. Record:

- title pattern and opening move
- specific promise, tension, result, question, or surprise
- evidence and detail that make the post credible
- paragraph and bullet structure
- whether the post asks for discussion
- available score and comment count
- whether the author participated in replies
- product mentions, disclosures, links, and moderator response

Call a post `top observed` or `high engagement in this sample`, not viral, unless the evidence supports that claim. Do not copy a title, anecdote, phrasing, or post structure too closely.

## Choose a native angle

Prefer one clear contribution:

- a practical checklist tested on a real task
- a teardown with screenshots or measurements
- a mistake and what changed afterward
- original data with collection method and limitations
- a detailed answer to a recurring subreddit question
- a build log focused on the problem and decisions
- a useful resource shared with moderator permission

The product must not be the only contribution. If removing the app sentence makes the post collapse, the draft is an advertisement.

## Write the title and hook

A catchy Reddit hook creates curiosity through specificity, not suspense tricks.

Use:

- a concrete result with context
- an unexpected finding the post can prove
- a recognizable pain stated plainly
- a strong but supportable opinion
- a specific question that invites informed replies

Avoid `You won't believe`, `This changed everything`, fake confessions, rage bait, vague founder drama, or withholding the answer until the end.

Keep the first paragraph to one or two short sentences. State why the post is worth reading. Do not start with the app.

## Structure the post

Use short one- or two-sentence paragraphs. Prefer bullets for steps, findings, mistakes, comparisons, or resources when the subreddit uses them.

A useful sequence is:

1. title with the concrete reason to read
2. short hook
3. relevant context and evidence
4. useful findings or steps, often as bullets
5. honest limitation, tradeoff, or unresolved point
6. one disclosed app mention only when allowed and relevant
7. a specific discussion question

Do not force every post into this order. Match successful native formats without imitating individual posts.

## Mention the app once

Count visible uses of the app name in the title, body, link label, image caption, and call to action. The final draft may contain no more than one.

The one sentence must disclose the relationship naturally:

- `I built [App] to handle this step, but the checklist above works without it.`
- `I work on [App], which is why I have been looking closely at this problem.`

Do not write `I found`, `I came across`, or `you could try` when the author owns, works for, or is paid by the product. Do not add a product URL unless the subreddit permits it and the reader needs it. Never use link shorteners or a second app reference in the closing.

## Make it sound human

- Use the author's supplied voice and real details.
- Prefer common words, contractions, and direct sentences.
- Let an honest uncertainty or tradeoff remain.
- Vary rhythm without stacking dramatic one-line fragments.
- Use subreddit vocabulary only when the author naturally understands it.
- Remove corporate copy, generic praise, forced slang, emojis used as decoration, and AI filler.
- Do not add fake typos, invented vulnerability, or a fictional personal story.
- Remove em dashes and en dashes from the final draft.

## Do and do not

| Do | Do not |
| --- | --- |
| Read current subreddit rules before drafting | Assume all subreddits treat promotion the same way |
| Give the full useful answer in the post | Tease the answer and send readers to the app |
| Disclose `I built` or `I work on` | Pose as an unaffiliated customer |
| Mention the app no more than once | Repeat the brand in the title, bullets, and CTA |
| Use short paragraphs and useful bullets | Turn every sentence into a one-line growth hack |
| Base the hook on a fact the post delivers | Use clickbait that withholds the payoff |
| Include a real limitation | Claim the method or app works for everyone |
| Ask a question the subreddit can answer | End with `Thoughts?` or engagement bait |
| Let the user review and post manually | Automate posting, voting, or repeated cross-posting |
| Draft a value-only version when promotion is banned | Reword the promotion to evade moderators |

## Examples

### Weak title and opening

> I built the ultimate productivity app that will change how you work
>
> Hey Reddit! After months of hard work, I am excited to share my revolutionary solution.

This is generic product copy with no community payoff.

### Better title and opening

> I tracked every interruption for 14 days. Notifications were not the main problem.
>
> I expected Slack to be the obvious culprit. It was not even close. Most interruptions started when I reopened a task without writing down the next step.

The hook makes a specific promise and immediately begins paying it off.

### Better body and single mention

> Three things helped:
>
> - Write the next physical action before closing a task.
> - Keep a separate list for questions that need someone else.
> - Review abandoned tasks at the end of the day, not every hour.
>
> I built FocusFox around the first step, but a text file works fine if you keep it visible.
>
> For people who work across several client projects, where does this break down?

The app appears once, the relationship is clear, and the advice works without it.

### Promotion is prohibited

Good: remove the product sentence and keep the complete method.

Bad: replace the app name with `a tool I happen to use` or ask readers to check the profile.

## Limitations

- Rules and moderator interpretations can change without notice. Recheck immediately before posting.
- Search results and visible engagement do not reveal every removed post, impression, downvote, or audience-size effect.
- A strong post can fail because of timing, competition, account history, or community fit.
- The skill cannot establish personal experience the author did not supply.
- A one-time disclosure may not satisfy every jurisdiction, employer policy, or subreddit rule.
- The skill drafts content only. The user must review and post manually.

## Output template

```markdown
# Reddit post brief
- Subreddit:
- Reader and problem:
- Post type:
- Author expertise:
- Product relationship:
- Evidence available:

## Rule check
- Status: allowed | permission needed | no product mention | do not post
- Promotion rule:
- Link rule:
- Flair/account requirements:
- Source links and checked date:

## Observed subreddit patterns
- Sample and time window:
- Hooks that earned attention:
- Useful formats:
- Patterns to avoid:
- Evidence limitations:

## Draft
### Title
[Specific, honest title without the app name]

### Body
[One- or two-sentence hook]

[Context and evidence]

- [Useful point]
- [Useful point]

[Tradeoff or limitation]

[One disclosed app mention, only if allowed]

[Specific discussion question]

## Final review
- [ ] The post remains useful without the product sentence
- [ ] The app name appears zero or one time
- [ ] Ownership, employment, or compensation is clear
- [ ] Rules and links were checked today
- [ ] Every result and first-person claim is real
- [ ] Paragraphs are short and bullets are useful
- [ ] No clickbait, corporate copy, fake slang, or invented story
- [ ] The user will post and respond manually
```
