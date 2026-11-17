# Runtime contract

All commands emit JSON. Exit 0 means the command completed, not that a real-world action ran; exit 2 includes a safe error code. Python 3.10+ and standard library only. Credentials/data default to `~/.local/share/xjev`; `XJEV_HOME` overrides that dedicated directory. `TYPESAFE_API_KEY` overrides the saved key. Never print/read config contents into the conversation.

## Install and setup

`python3 <source>/install.py` copies to `~/.agents/skills/xjev` and starts a localhost key form if needed. It refuses to overwrite an existing directory. `--target <full-skill-directory>` supports another host; `--no-setup` prints the setup command instead. A folder install also works; SKILL.md performs first-use onboarding. No scheduled jobs or host-wide hooks are installed.

`python3 <skill>/scripts/xjev.py status` is local only. `status --check` sends a small, billable real API probe. `setup` opens a 10-minute localhost form; `--no-browser` only prints the URL. Invalid keys are not saved. The runtime uses only `https://api.typesafe.ai/v1/systemone`, does not follow redirects, and never accepts a key as a CLI argument.

## Decision input

Start from `examples/compare.json` (a synthetic example, not user facts). Input:

- `scope`, `goal`: nonempty strings. Use a stable scope ID; matching is exact, not fuzzy.
- `mode`: `assist` (default) or `delegate`.
- `context`: relevant current state; omit unrelated history.
- `preferences`: current explicit preference strings, optional.
- `options`: 2–12 objects with unique `id`, `label`, `facts`, `evidence_refs` (strings), `eligibility` (`pass/fail/unknown`) and `reason`. The host must actually verify hard constraints; the runtime cannot prove the host’s label or evidence link is true. `pass` without evidence becomes unknown.
- `dimensions`: 1–8 unique IDs. Each has `type`, `instructions`, and criteria as needed. Score: 2–10 descriptive levels and `direction: min|max`. Noul: single clear proposition and direction. Choice: 2–255 named choices and `utilities` mapping each to 0–1. Score can have a level-aligned `utilities` list; otherwise levels use an explicit evenly spaced 0–1 convention. `direction=min` reverses desirability after calculation.
- `priority`: optional ordered list of every dimension ID once. Explicit current priority wins over saved defaults; omit to reuse learned priority.
- `min_margin`: optional 0–0.5, default 0.05. A practical ranking tolerance, not a statistical confidence interval or calibrated action threshold.
- `excluded_policy_ids`: policies to skip for this decision (one-off exceptions).

The runtime blocks on any unknown decisive candidate, excludes failed candidates, and bypasses Jev when only one candidate passes. Otherwise it batches candidate/dimension questions against the same state. Each question is isolated; dependent questions require another call with updated state.

For each dimension in priority order, it keeps options within the tolerance of the best expected utility, then breaks remaining ties on the next dimension. No unique survivor gives `ask`. The numerical scale is a decision convention: ensure it fits the task, show tradeoffs, and avoid claiming exact optimality. A low-confidence or unstable factual judgment may require the host to gather evidence despite a nominal ranking.

## Commands

```text
xjev.py decide --input input.json
xjev.py decide --input corrected.json --parent dec_...
xjev.py show dec_...
xjev.py show dec_... --raw
xjev.py feedback dec_... --input feedback.json
xjev.py policies --scope personal-tools
xjev.py policies --scope personal-tools --all
xjev.py policy-new --input policy.json
xjev.py policy-trial pol_... --input cases.json
xjev.py policy-adopt pol_... --trial trial_...
xjev.py policy-revoke pol_...
```

`show --raw` is for requested tracing/debugging: it includes the limited state/request/response saved at decision time. Do not dump private evidence by default. `contributions[].adopted` means that question participated in the comparison, not that the user accepted the recommendation. Responses include actual model version; call IDs are locally generated, never presented as provider request IDs.

Facts and constraints changing require a new decision revision. Selection and historical execution are separate. No command performs the recommended external action. Trials likewise never select or execute real actions.

## Official contracts checked 2026-09-21

- https://docs.typesafe.ai/api — endpoint, questions, answer shape, 401/422/429/529.
- https://docs.typesafe.ai/confidence — confidence is a statistic of the returned distribution.
- https://developers.openai.com/codex/skills/ — user discovery at ~/.agents/skills and implicit invocation.

The package validates question IDs, answer types, distributions, Choice argmax, Score mean and legend. It preserves server probabilities rather than normalizing malformed results. Rate-limit/overload retries are bounded at three attempts; network ambiguity is returned to the host instead of silently retried. No claim of actual latency, accuracy or calibration is made by the package.
