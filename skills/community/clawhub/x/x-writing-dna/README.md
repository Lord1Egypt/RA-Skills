# X Writing DNA

An agent skill for researching an X author's writing from complete public works and producing separate, evidence-backed profiles for posts and long-form articles.

## What it does

- Collects and audits at least 50 independent complete posts or 20 complete articles per requested author and genre.
- Separates original narration, quotations, threads, native articles, external archives, duplicates and incomplete captures.
- Analyzes six expression axes plus judgment origin, choices and tradeoffs, and recurring evaluation criteria.
- Produces reusable writing methods with source works, counterexamples, scope limits and a training handoff.

This is an agent-operated browser workflow. Installation does not create an unattended crawler. An authenticated browser tool or an authorized official API must be available to the host agent. It does not bypass access controls or extract credentials.

## Install

Clone this repository into your agent's skills directory under `x-writing-dna`. For Codex:

```bash
git clone https://github.com/0xcjl/x-writing-dna.git ~/.codex/skills/x-writing-dna
```

Use an empty destination. Claude Code, Hermes and OpenClaw can use the same `SKILL.md` and reference files in their supported skill directories. The optional `agents/` metadata, when present, is specific to Codex. Installation paths and discovery behavior depend on the host.

From ClawHub, after the registry release is available:

```bash
clawhub install @0xcjl/x-writing-dna
```

## Use

Ask your agent:

> Use x-writing-dna to research https://x.com/example. Analyze posts and articles separately. Collect 50 complete posts and 20 complete articles, save checkpoints, and report missing branches honestly. Extract methods I can practice without copying the author's identity or experiences.

If only one genre is needed, request it explicitly. The same author's two genres require independent evidence. Different authors cannot establish within-author differences.

The local audit helper needs Python 3 and uses the standard library:

```bash
python3 scripts/corpus_audit.py /absolute/path/corpus.jsonl --author example --out /absolute/path/fresh-audit
```

The helper audits supplied observations; it neither collects content nor proves identity or completeness. Use a fresh output directory for each audit.

## Outputs

A traceable capture and normalized corpus, audit JSON and CSV, per-work annotations, `post-dna.md` and/or `article-dna.md`, and `run-status.md`. A same-author comparison is produced only when both genres have evidence. Five unseen works per genre are reserved for holdout validation before profiling; otherwise validation is reported as unperformed.

## Pair with Personal Content DNA

Pass methods, source work IDs, genre, limitations and practice actions to [personal-content-dna](https://github.com/0xcjl/personal-content-dna). Reference-author experiences remain attributed to that author; only the user's real feedback supports adopting a method.

## Limits

Sample counts do not prove representativeness. Engagement observations do not establish that style caused popularity. Partial collection, unverifiable identity, unseen visuals and missing holdout checks must remain explicit. Content collection does not grant permission to republish complete third-party works.

## Edition, credit and license

This ClawHub edition is an independently written MIT-0 package. Its collection contract, analysis instructions and audit helper are maintained by 0xcjl. The multi-aspect writing-analysis idea was informed by [writing-dna-skill](https://github.com/larashero3-dotcom/writing-dna-skill); no upstream templates or workflow prose are included in this registry package. The GitHub root edition retains MIT licensing and its upstream attribution. See [LICENSE](LICENSE).
