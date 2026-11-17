# secret-leak-scan-lite

Free agent skill: statically scan a project directory for leaked credentials
before committing. Masked fingerprints only — raw secret values are never
emitted.

Detects: AWS access key IDs, GitHub personal access tokens, Slack tokens,
PEM private-key blocks.

## Install

```bash
npx skills add NenadZivotic/secret-leak-scan-lite
```

or clone into your agent's skill directory:

```bash
git clone <repo> ~/.claude/skills/secret-leak-scan-lite
```

## Use

Requires Node 18+, zero dependencies.

```bash
node scripts/scan.mjs <directory>
```

JSON report on stdout. Exit code `1` when findings are present — drop it
straight into a pre-commit hook or CI step.

## Full version

This is the lite edition. The full `secret-leak-scan` skill adds:

- `.asar` bundle scanning (Electron release checks)
- Stripe live keys, Google API keys, fine-grained GitHub PATs
- Complete triage & rotation workflow, git-history cleanup, CI gate recipe

Available on [Agensi](https://agensi.io/skills/secret-leak-scan) and
[SkillHQ](https://skillhq.dev/skills/sone94/secret-leak-scan).
