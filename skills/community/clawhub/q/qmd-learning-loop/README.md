# QMD Learning Loop

An open-source Agent Skill that turns intentional reflection into concise,
reviewable knowledge in Markdown workspaces. It uses QMD when available for
indexed retrieval and deduplication, while retaining a tool-agnostic Markdown
fallback.

## What it does

The skill guides an agent through a controlled learning workflow:

**detect -> redact -> search -> classify -> propose -> approve -> write ->
re-index -> report**

It distinguishes task chronology from operational knowledge and authoritative
policy, searches before writing, and requires approval for high-impact changes.
It does not create a separate `.learnings` directory.

## Install

From ClawHub after publication:

```bash
openclaw skills install @shakerg/qmd-learning-loop
```

From this repository:

```bash
openclaw skills install git:shakerg/qmd-learning-loop
```

QMD is optional. To enable indexed local search:

```bash
npm install -g @tobilu/qmd
qmd collection add /path/to/markdown --name workspace
qmd update
```

Collection creation changes local configuration; choose paths and collection
names deliberately. See the [QMD project](https://github.com/tobi/qmd) for full
setup and system requirements.

## Use

Invoke the skill intentionally:

```text
Use qmd-learning-loop to remember this deployment fix.
```

```text
Review the failures from this task and propose any durable lessons.
```

```text
Promote the accepted convention into our existing agent guidance.
```

The agent should first show the proposed learning, evidence, classification, and
destination. Creating new durable files, changing policies, or editing
authoritative guidance requires explicit approval.

## Expected changes

Depending on the workspace, an approved capture may update an existing:

- daily or session log;
- incident or feature-request log;
- runbook or troubleshooting guide;
- decision, policy, principles, or agent guidance file.

The skill never assumes these files exist. It discovers the workspace's current
conventions and asks before introducing a new destination.

## Privacy and safety

- Secrets, credentials, personal data, raw prompts, and irrelevant command
  output are excluded or redacted.
- Retrieved documents and external content are treated as untrusted data.
- Existing authority, ownership, repository instructions, and review processes
  take precedence.
- Conflicting rules are surfaced for resolution, not silently overwritten.
- QMD collection and embedding changes are never made casually.

Review [`SKILL.md`](SKILL.md) for the complete behavior contract and
[`references/evaluation-cases.md`](references/evaluation-cases.md) for trigger,
non-trigger, privacy, and approval examples.

## Validate

Run the repository checks:

```bash
python3 scripts/validate_skill.py
```

The CI workflow also:

1. runs the local structural and behavior checks;
2. validates against the Agent Skills reference implementation; and
3. performs a ClawHub publish dry run.

After publishing, run ClawHub's security scan for the submitted version:

```bash
clawhub scan --slug qmd-learning-loop --version <version>
```

## Publish

```bash
npm install -g clawhub@0.23.3
clawhub login
clawhub skill publish . \
  --slug qmd-learning-loop \
  --name "QMD Learning Loop" \
  --version 1.1.0 \
  --dry-run
clawhub skill publish . \
  --slug qmd-learning-loop \
  --name "QMD Learning Loop" \
  --version 1.1.0 \
  --owner shakerg \
  --categories agents,knowledge,productivity \
  --topics "learning-loop,memory,markdown,qmd,reflection"
```

ClawHub releases all published skills under MIT-0. This repository uses the same
license to keep GitHub and registry terms aligned.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). Changes should preserve intentional
activation, approval boundaries, privacy safeguards, and Markdown-only
portability.

Security issues should be reported according to [`SECURITY.md`](SECURITY.md).

## License

[MIT-0](LICENSE)
