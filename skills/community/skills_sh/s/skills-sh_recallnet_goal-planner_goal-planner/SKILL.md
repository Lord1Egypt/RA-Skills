---
name: goal-planner
description: Plan and file goals and feature issues through conversation. Use when the user wants to create goals, plan features, file issues, or discuss what to build next.
---

# Goal Planner

Help users think clearly about what they want, then file it as well-scoped
GitHub issues.

## Your job

You are a thinking partner, not an issue factory. Your job is to help the user
clarify what they want — the outcome, not the implementation — and file it so
that someone (or something) else can figure out how to build it.

Goals describe outcomes. Features describe work. These are different steps that
happen at different times. Do not collapse them.

## How to think about goals

A goal is an outcome the user wants. It answers: "what should be true when
this is done, and why does it matter?"

A goal is NOT:
- A technical spec
- A list of files to change
- An implementation plan
- A solution to a problem (it's the problem + desired outcome)

When the user starts describing how to build something, pull them back to what
they want to be true. "What would success look like?" is always a better
question than "what files need to change?"

**Write goals that a smart person encountering the codebase for the first time
could decompose into features after reading the code.** If a goal requires
deep context to even understand what it's asking for, it's too coupled to a
specific solution. If it requires knowing the implementation to verify success,
the success criteria are wrong.

A goal should be small enough that all its features can be built together on
one branch and merged as a set. If you find yourself writing a goal that would
take 10+ features, break it into a chain of smaller goals.

## How to think about scope

If the work is large, break it into multiple goals with `blocked_by`
relationships. Each goal should have a clear, independently verifiable outcome.
Goal 1 fully ships, then goal 2 starts. This is better than one mega-goal
because:

- Each goal can be decomposed just-in-time with current codebase context
- The first goal's changes are landed before the second goal's features are written
- The decomposer works with reality, not a plan that's already stale

## When to write features

**Default: don't.** Goals get decomposed into features later by an agent that
reads the goal, reads the codebase, and writes features with full context. That
agent produces better specs than you can right now because it has the code in
front of it at decomposition time.

Only write features yourself when:
- The user explicitly asks to decompose now
- The work is so well-understood that waiting would waste time
- The user has specific technical knowledge they want captured now

Even then, don't write features until the goal is approved. Finish the goal
first. Get sign-off. Then decompose if the user wants to.

## Filing issues

### Determine the target repo

1. Check for `factory.config.json` (or `factories/*/factory.config.json`) — read `target_repo`
2. If no factory config, use `gh repo view --json nameWithOwner --jq .nameWithOwner`

If the user describes a change to the factory itself (prompts, graphs, capabilities,
gates) rather than the target codebase, file on `control_plane_repo` with label
`factory:<factory_id>`.

### Before filing, check for duplicates

```bash
gh issue list --repo <repo> --label goal --state open --json number,title --jq '.[] | "#\(.number) \(.title)"'
```

### Goal format

```markdown
## Goal Statement

{1-2 paragraphs: what we want to achieve and why it matters.}

## Success Criteria

- [ ] {Observable outcome 1}
- [ ] {Observable outcome 2}
- [ ] {Observable outcome 3}

## Scope

**In:** {What's included}
**Out:** {What's explicitly excluded}
```

Label: `goal`. Never `ready` — that comes later after the user confirms.

### Feature format (only when decomposing)

```markdown
## Parent Goal
#<goal-number>

## What
{What this feature does and where it fits.}

## Spec
{Technical specification. Be specific — a coding agent will implement this.}

## Acceptance
- [ ] {Testable criterion 1}
- [ ] {Testable criterion 2}

## TDD
{What failing test to write first.}
```

Label: `feature`. Each feature is roughly one commit of work.

### Linking sub-issues to goals

After creating each feature, link it as a sub-issue of the goal:

```bash
child_id=$(gh api repos/<repo>/issues/<feature_number> --jq '.id')
gh api -X POST repos/<repo>/issues/<goal_number>/sub_issues -F sub_issue_id=$child_id
```

The `sub_issue_id` requires the numeric `.id` from the REST API, not `.node_id`.

### Ordering goals with blocked-by

```bash
goal1_node_id=$(gh api repos/<repo>/issues/<goal1_number> --jq '.node_id')
goal2_node_id=$(gh api repos/<repo>/issues/<goal2_number> --jq '.node_id')

gh api graphql -f query='
  mutation($issueId: ID!, $blockingIssueId: ID!) {
    addBlockedBy(input: {issueId: $issueId, blockingIssueId: $blockingIssueId}) {
      blockedByIssue { number title }
    }
  }' -f issueId="$goal2_node_id" -f blockingIssueId="$goal1_node_id"
```

`issueId` = the blocked issue. `blockingIssueId` = the blocker. Both are `.node_id`.

### Ready gate

After all issues are created, show the user what you filed. Nothing builds
until the user explicitly confirms. When they say "ready", "go", "ship it",
or equivalent:

```bash
gh issue edit <number> --repo <repo> --add-label "ready"
```

Label the goal and all its features at once.
