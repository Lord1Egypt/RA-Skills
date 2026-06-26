# Campaign Harness Stack

Use this reference when a SOTA campaign needs stronger orchestration, bounded subagents, and an
explicit local-first runtime policy.

## Why SOTA Work Underperforms

A SOTA campaign underperforms when it has:

- a loose benchmark contract
- too much literature copying and not enough reproduction
- no bounded subagent decomposition
- no campaign harness for accepting or rejecting candidates
- no rerun discipline for small deltas
- no runtime policy, so the workflow drifts toward paid API-key dependencies

That failure mode produces a lot of notes and not enough real wins.

## What To Reuse

### `karpathy/autoresearch`

Reuse the decomposition pattern:

- one topic or campaign per workspace
- short, cheap experiments with keep or discard decisions
- one explicit program file or contract that humans steer
- journals and artifacts that survive long-running research loops

Source:
- https://github.com/karpathy/autoresearch

### Codex multi-agent and customization guidance

Use Codex subagents for bounded campaign work:

- main thread owns the benchmark contract and final claim wording
- scout subagents read papers, leaderboards, and repos
- reproducer or executor subagents inspect concrete code paths or configs
- reviewer subagents check contamination, regressions, and missing evidence

For repeated audits, use manifest-driven fanout instead of asking one agent to hold the whole
campaign in context.

Sources:
- https://developers.openai.com/codex/multi-agent/
- https://developers.openai.com/codex/concepts/customization/

### OpenAI harness engineering

The campaign harness must own acceptance:

- humans steer, agents execute
- increase application legibility before adding more autonomy
- validators, reruns, and review gates belong in the harness itself

For SOTA work, that means:

- fixed metric and split
- explicit baseline and target threshold
- rerun policy for small gains
- evidence bundle before claim language

Source:
- https://openai.com/index/harness-engineering/

### `algorithmicsuperintelligence/openevolve`

Reuse the evaluator-first search pattern:

- mutate one meaningful change set at a time
- score every candidate with the same harness
- keep search state and candidate diffs
- think in Pareto tradeoffs when compute, latency, or memory matter

Source:
- https://github.com/algorithmicsuperintelligence/openevolve

### `openai/symphony`

Reuse:

- workflow contracts
- isolated workspaces
- persistent logs and observability for many concurrent branches

This helps when a SOTA program has several active reproductions or ablation families.

Source:
- https://github.com/openai/symphony

### `paperclipai/paperclip`

Reuse only the management ideas when the research program becomes a portfolio:

- recurring work on heartbeats
- task lineage
- cost awareness
- auditability across many agents

Source:
- https://github.com/paperclipai/paperclip

### `algorithmicsuperintelligence/optillm`

Selective reuse only:

- plan search
- best-of-n or candidate selection ideas
- self-consistency or reasoning-time compute for analysis and review

Do not make an API-key-based proxy a required campaign dependency under a local-first policy.

Source:
- https://github.com/algorithmicsuperintelligence/optillm

## Local-First Campaign Rule

Default allowed paths:

- local Python helpers
- public papers, public repositories, and public leaderboard pages
- user-supplied result artifacts and run summaries
- repo-local tests and review scripts that the user explicitly asks to run

Default forbidden requirements:

- `OPENAI_API_KEY`
- provider-specific paid API keys
- account-bound live sessions as a requirement for this planning skill
- "buy API access first" as a prerequisite for the SOTA planning workflow

If a framework cannot run from public artifacts or local tools, keep the idea and drop the
dependency from the SOTA planning package.

## Recommended Composition

For serious benchmark pushes:

- `sota-agent` owns the benchmark contract, literature triage, candidate ranking, and claim review
- `data-science-cv-repro-lab` owns notebooks, external execution, artifact capture, and promotion evidence
- the campaign harness owns whether a candidate is real, noisy, or cut

That split prevents "frontier theater" where a campaign sounds advanced but still lacks a valid win.
