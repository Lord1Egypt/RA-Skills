---
name: social-listening
description: 'Find the LinkedIn conversations worth joining every week: each Monday the week''s public LinkedIn posts about the problem you solve are judged against your ICP, and one Slack digest lists the posts worth joining and the commenters who look like buyers, each with a link. Triggers: "tell me which linkedin posts we should comment on", "watch linkedin for people talking about our problem", "social listening on linkedin", "weekly digest of linkedin conversations in our space", "who is engaging with posts about our category", "monitor linkedin posts mentioning our competitors". Cargo project, LinkedIn fetchPosts, searchPostComments, defineModel, defineAgent, Slack postMessage. Skip when: you want named target accounts checked for hiring, news or detection-feed events, once, which is monitor-buying-signals; or you want people who just took a role you sell to, which is new-hire-detection.'
version: "0.1.2"
compatibility: "Requires @cargo-ai/cli with @cargo-ai/cdk 1.0.92 or later, a Cargo workspace, and authorized LinkedIn, Slack and Anthropic connectors. Reads the ICP, pains and competitors from the workspace context."
homepage: https://github.com/getcargohq/gtm-skills/tree/main/social-listening
metadata:
  author: getcargo
  source: cookbook
  personas:
    - marketing
    - sales-development
  openclaw:
    requires:
      bins:
        - cargo-ai
    install:
      - kind: node
        package: "@cargo-ai/cli@latest"
        bins:
          - cargo-ai
    homepage: https://github.com/getcargohq/gtm-skills
---

# Social listening

**State: to-be-approved.** Deploy-verified against a live workspace: yes, on 2026-10-04: a
`limit: 20` search landed 21 posts from the past week, the listener surfaced 3 of them in one Slack
digest, read no comments because none of the picked posts had any, called no engagement action,
and wrote 4 ledger rows (3 posts and the week's digest row); a re-run the same day found the digest
row and posted nothing. Treat `Done when`
below as the acceptance test and review `cargo-ai project plan` before deploying. Make no outcome claim
for this skill until it is approved.

## The outcome

The conversations your buyers have in public stop going past unseen. Every Monday:

1. **A model buys one capped search.** `linkedin_posts` syncs LinkedIn's post search for the past
   week, on keywords taken from your workspace context: the pains in the buyer's own words, the
   category term, competitor names. The query is the spend, so it lives in the model's config.
2. **An agent judges.** It reads the ICP and pains from the context, drops every post already
   surfaced, and picks at most five worth joining, each with the context line that decided it.
3. **It reads comments only on those five**, and names at most ten commenters whose headline
   matches an ICP persona, quoting the first sentence of what they said.
4. **One digest lands in a locked Slack channel**, and the picked posts go into the
   `surfaced_posts` ledger, so a post never headlines twice.

It never likes, comments, connects or messages. Those actions sit on the same LinkedIn connector
and none is wired; the contract fails if one is. A human reads the digest and decides whether to
join. The ledger keeps posts, not people: an engager appears in that week's digest, quoted from a
public comment, and is not stored as a list.

## Example

> Every Monday, tell #gtm-signals which LinkedIn conversations about lead routing are worth joining.

Illustrative output, fictional records:

```text
:ear: *What the market said this week*
_Routing breakage after CRM migrations came up three times._

*Worth joining*
• Dana Ruiz, VP RevOps at Fabrikam: "Our Salesforce migration broke every
  routing rule we had" — ICP persona, pain "routing breaks on field changes"
  (linkedin.com/posts/dana-ruiz_fab…) · 41 comments
• Wingtip Toys Engineering: a teardown of hand-built lead routing — category
  term "speed to lead" (linkedin.com/posts/wingtip…) · 12 comments

*Warm engagers*
• Sam Okafor, Head of Revenue Operations at Contoso, on Dana's post:
  "We rebuilt ours three times this year." (linkedin.com/in/sam-okafor)

_Searched: 40 posts read, 3 already surfaced_
```

Forty posts were read; two were picked and recorded in `surfaced_posts`, one commenter matched an ICP
persona, and nothing was sent to anyone.

## Put it in your project

This folder is a **worked example**: real project resources written for some other company. The job is
to end up with the code your company would have written, in your project, and an agent does the
adapting. If the `cargo-project` skill is in your session it carries the long form of this; if not, this
is enough.

1. **Install it — the CLI does the copy.** From inside the project (the folder holding `cargo.json`),
   `cargo-ai project add cookbook/social-listening` writes this example to `infra/social-listening/` and
   this procedure to `.claude/skills/social-listening/`. No project yet?
   `cargo-ai project init <dir> --cookbook social-listening && cd <dir> && npm install` does both. **If
   you are reading this from the project's `.claude/skills/`, the install already happened — start
   at step 2.**
2. **Reconcile it with what is already declared.** If the project already has a LinkedIn, Slack or
   Anthropic connector, rewire the imports to the existing one and drop the copy; two resources with
   one slug is a collision at deploy.
3. **Write the keywords from the context.** Replace `searchKeywords` in
   `infra/models/linkedin-posts.ts` with phrases a buyer would post, read from the ICP and pains in
   the workspace context, plus competitor names. Run the search once by hand
   (`cargo-ai orchestration action execute` on `linkedin.searchPosts` with the same keywords and
   `datePosted: "Past week"`) and read ten results out loud before you keep them.
4. **Point Slack at your channel.** Set `channelId` in `infra/agents/listener.ts` to a channel id
   (`C…`) from the Slack connector's autocomplete, and invite the bot.
5. **Adapt.** Work the sections below in order: _What should not change_ is what you argue back
   about; _What you can change_ is what you offer unprompted; _What you will be asked_ is the floor,
   and you derive before you ask. Record what you changed and why under a `## Decisions` section in
   your copy of this file.
6. **Check, then plan.** `node --import tsx evals/contract.mjs` from this skill's folder, then
   `npm run check && cargo-ai project plan` from the project root. Show the diff, and deploy only on an
   explicit yes: `cargo-ai project deploy`.
7. **Verify.** Trigger the model sync once, then send the agent its trigger text by hand
   (`cargo-ai ai message create`), and walk _Done when_ with evidence. Send it again: the second run
   must post nothing.

## What you will be asked

**Derive before you ask.** An input with a lookup is looked up, not asked.

| Input                                                       | Kind    | How it is answered                                                                                                                                                              | Why it matters                                                                                                                                         |
| ----------------------------------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `searchKeywords` (`infra/models/linkedin-posts.ts`)         | derived | From the ICP pains, category term and competitors in the workspace context, confirmed against one manual search. Asked only when the context has none.                           | It is what you buy each week. Positioning copy as keywords returns vendors talking to each other; buyer language returns buyers.                        |
| `limit` (`infra/models/linkedin-posts.ts`)                  | asked   | 20 to 100 in steps of 20. Price it from the live per-post cost before you pick.                                                                                                 | It is the weekly spend ceiling on the search.                                                                                                          |
| `channelId` (`infra/agents/listener.ts`)                    | asked   | The Slack channel id (`C…`) from the connector's autocomplete. Invite the bot.                                                                                                  | The digest names people. Locked so it never lands in a customer shared channel.                                                                         |
| connectors (`infra/connectors/`)                            | value   | **derived**: `cargo-ai connection connector list` shows authorized LinkedIn, Slack and Anthropic connectors. `default: true` binds each.                                          | Without LinkedIn the sync returns nothing and the digest reads "quiet week" forever.                                                                   |
| our own company and people                                  | derived | From the workspace context (company, positioning).                                                                                                                              | They are excluded from picks. Miss them and the digest recommends joining your own posts.                                                              |

## What you can change

| Variation         | When it is right                                                   | How                                                                                                             | What it costs                                                                                                                                                     |
| ----------------- | ------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `two-searches`    | Pain language and competitor names return different crowds        | Add a second `fetchPosts` model with its own keywords and give the listener read access to both                 | Two searches billed each week. The ledger still dedupes a post that matches both.                                                                                 |
| `with-reactions`  | Comments are rare in your niche and reactions are the only signal   | Add `linkedin.actions.searchPostReactions` to `uses` and a §4 line to read them on picked posts                 | Billed per reactor, often hundreds a post, and a reaction carries no words to quote. Cap it in the prompt.                                                        |
| `with-tiers`      | `account-scoring` is installed and you want engagers at A/B accounts first | Add the tiered companies model to `uses` read-only, and in §4 match the headline's stated employer by name      | Name matching misses on abbreviations. Only a headline that states the employer can match; never look it up.                                                      |
| `daily`           | The category moves fast and a weekly digest is stale               | `datePosted: "Past 24 hours"`, a daily cron on both the model and the agent                                     | Seven searches a week instead of one, and a digest most days will be quiet.                                                                                       |
| `competitor-only` | You only want to hear when a competitor is discussed               | Keywords become competitor names only                                                                           | You lose the buyers who describe the pain without naming any vendor, which is most of them.                                                                       |

## What should not change

- **No engagement action on `uses`.** (`infra/agents/listener.ts`) Liking, commenting, connecting
  or messaging from an agent is automated outreach to people who never asked. The contract fails on
  any of them.
- **The ledger stores posts, never people.** (`infra/models/surfaced-posts.ts`) A standing list of
  everyone who commented on a topic is a scraped list. The digest names engagers that week, quoted
  from a public comment, for a human to read.
- **The search is the spend, so it stays in the model's config and capped.**
  (`infra/models/linkedin-posts.ts`) Removing `limit` or widening `datePosted` re-buys last week's
  posts every Monday; the sync replaces the rows, so nothing is gained.
- **The ledger is checked before comments are read, and written after the post.**
  (`infra/agents/listener.prompt.ts` §2, §5, §6) Check late and every re-run re-pays for comments.
  Write early and a failed post marks posts as surfaced that nobody saw.
- **Comments are read only on picked posts, under the cap.** (`infra/agents/listener.prompt.ts` §4)
  The comment read bills per comment returned; reading every post's comments is the bill that grows
  without anyone choosing it.
- **No invented employer.** (`infra/agents/listener.prompt.ts` §4) An engager's company is what their
  headline states, or nothing. Looking people up elsewhere turns a digest into a dossier.
- **`channelId` is locked.** (`infra/agents/listener.ts`) The digest quotes people by name.

## Done when

- `node --import tsx evals/contract.mjs` passes
- `cargo-ai project plan` reports the agent, the two models, the three connectors and the two folders
- the first sync landed rows in `linkedin_posts`, all from the past week, no more than `limit`
- one digest landed in the locked channel in the `references/digest.md` shape, every pick citing a
  context line and linking its post
- `surfaced_posts` has one row per pick plus one `digest-<date>` row, and no column holding a person
- a second run the same day posted nothing and read no comments
- the run transcript shows no LinkedIn action other than `searchPostComments`, and only on picks
- every quoted comment exists on the linked post, and every employer shown is in the commenter's
  own headline

## What it costs

Read the live price of each paid step immediately before the plan, and say each one out loud:

- `cargo-ai connection integration get linkedin`: the `fetchPosts` extractor (per post returned, so
  the weekly ceiling is `limit` times that price) and `searchPostComments` (per comment returned).
- `cargo-ai orchestration action list postMessage --kind connector --integration-slug slack`.

The weekly cost is one search capped by `limit`, comment reads on at most five posts each capped by
the prompt's comment limit, one Slack post, and the agent run billed as LLM tokens through the
Anthropic connector. On the live run the agent run, not the search, was most of the bill: it reads
the ICP, personas, objections and insights before it judges a post. A re-run that stops at the
ledger costs a small fraction of a full run. Read the run's usage after the first week
(`cargo-ai ai message get`) before you widen `limit`.

## Composes into

`account-scoring` (the `with-tiers` variation puts engagers at A and B accounts first),
`web-capture` (what the market says next to what competitors publish), and `find-linkedin-url` /
`enrich-linkedin-profile` when a human decides one engager is worth a closer look.
