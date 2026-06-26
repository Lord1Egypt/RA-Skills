# PR Review Loop

An [Agent Skills](https://agentskills.io) skill that automates iterative PR comment resolution
with an opinionated, resumable workflow.

## What it does

1. Discovers project safeguards (tests, linting, compilation) from project conventions
2. Collects all unresolved PR comments from any reviewer
3. Triages each comment: MUST_FIX, SHOULD_FIX, PARK, or OUT_OF_SCOPE
4. Addresses comments one at a time: test → fix → test → commit → reply → resolve
5. Posts a final PR summary when done

## Key property: resumable

The skill can be interrupted and restarted in a fresh context window at any point
without losing progress. Each fix is committed and pushed before moving on.

## Prerequisites

- `gh` CLI (recommended).
- PR branch checked out locally

## Install

```bash
npx skills add xpepper/pr-review-agent-skill/pr-review-loop
```

## Usage

Once installed, just describe what you want — the agent activates the skill automatically:

```
Address all open review comments on this PR
```
```
Work through the code review feedback on PR #42
```
```
Fix the review comments left by @alice on this pull request
```

You can also invoke it explicitly by naming the skill:

```
Use pr-review-loop on PR #123
```
```
Run the PR review loop on this branch
```

## Optional: Perplexity for deep research

If you have the [Perplexity Web Research skill](https://github.com/xpepper/perplexity-agent-skill) installed, the agent will use it for research-heavy triage decisions.
