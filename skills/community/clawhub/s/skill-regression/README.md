# skill-regression

> Regression testing framework for AgentSkills — script-layer assertions + AI-layer semantic scoring, in one pipeline.

Part of [**build-better-skills**](https://github.com/Songhonglei/build-better-skills) — the Testing stage.

## Why

Most skills break silently:

- A subtle SKILL.md rewrite changes how an LLM interprets the trigger
- A new script dependency isn't reflected in the doc
- An edge case stops being handled correctly

**skill-regression** runs your skill through:

1. **Script-layer tests** — subprocess + assertion (contains/regex/exact)
2. **AI-layer tests** — LLM acts as the agent following your SKILL.md, output scored 0-10 by an LLM-as-judge
3. **Markdown report** — pass/fail breakdown + (optional) LLM-generated improvement suggestions

You define test cases in `TEST.md` (placed in your target skill dir). Or let the LLM infer them from your SKILL.md.

## Dual backend

| Backend | Auto-detected when | Tests |
|---------|--------------------|-------|
| **`api`** | No `openclaw` CLI present | Whether SKILL.md is well-written enough for an LLM to follow correctly (stateless, parallel-safe, works anywhere) |
| **`openclaw`** | `openclaw` CLI found | End-to-end real agent + skill integration via cron probe job |

Both backends use the same scoring layer.

## Quick start

```bash
# 1. First time: configure LLM credentials
python3 scripts/setup.py

# 2. Run regression
bash scripts/run_regression.sh /path/to/my-skill
```

## Configuration

Required (api backend):

```bash
SR_LLM_API_KEY=sk-...
SR_LLM_BASE_URL=https://api.openai.com/v1
SR_LLM_MODEL=gpt-4o-mini
```

Additional (openclaw backend):

```bash
SR_TARGET_AGENT=main
```

Storage priority (high → low):

1. CLI args
2. Process env vars
3. Project-local `./.env`
4. Global `~/.config/skill-regression/.env`
5. Missing → interactive onboarding (TTY) or error hint (non-TTY)

## TEST.md format

````yaml
# In <target-skill>/TEST.md

```yaml
id: case_001
name: Basic test
type: normal
trigger: "Please use my-skill to do X"
script_cmd: "python3 {SKILL_DIR}/scripts/foo.py"
expected_output: "Success"
expected_output_mode: contains
expected_agent_response: "Confirms X was done, returns result"
skip_agent: false
```
````

## Common workflows

```bash
# Detailed report (every case full input/output)
bash scripts/run_regression.sh /path/to/my-skill --detail

# Re-run only failures from a previous run
bash scripts/run_regression.sh /path/to/my-skill \
  --rerun ~/.skill-regression-space/output/my-skill/20260622_001500

# Script layer only (no LLM cost)
bash scripts/run_regression.sh /path/to/my-skill --skip-agent

# Force backend
bash scripts/run_regression.sh /path/to/my-skill --backend api

# Show or reset config
python3 scripts/setup.py --show
python3 scripts/setup.py --reset
```

## Report upload hook

Set `SR_REPORT_UPLOAD_HOOK` to push the generated report to your preferred destination:

```bash
# Hook receives: $1=report-path, $2=skill-name, $3=date
# Print the URL to stdout on success
SR_REPORT_UPLOAD_HOOK=~/bin/gist-upload.sh \
  bash scripts/run_regression.sh /path/to/my-skill
```

## Dependencies

- **Required**: Python 3.8+, `bash`, `pip install pyyaml --break-system-packages`
- **Optional (openclaw backend)**: `openclaw` CLI

Network calls use stdlib `urllib`. Zero non-stdlib Python packages except `pyyaml`.

## Caveats

- **Same-family LLM scoring**: the judging LLM and the simulating LLM are usually the same family. Treat scores as directional, not absolute.
- **api backend ≠ true agent test**: it tests whether your SKILL.md is well-written enough for an LLM to follow. For real agent + skill interaction tests, use the `openclaw` backend.
- **`normalize_testfile.py` side effects**: renames `Test.md`/`TESTS.md` → `TEST.md` in your target skill dir. Use `--dry-run` to preview.

## License

MIT — see [LICENSE](LICENSE).

## Part of build-better-skills suite

| Stage | Skill | Status |
|-------|-------|--------|
| Creation | [`skill-creator`](https://github.com/Songhonglei/build-better-skills) | Coming soon |
| Install | [`skill-hub-united`](https://github.com/Songhonglei/build-better-skills/tree/main/skills/skill-hub-united) | ✅ v1.0.0 |
| Audit | [`glic-check`](https://github.com/Songhonglei/build-better-skills/tree/main/skills/glic-check) | ✅ v1.0.1 |
| Audit | [`skill-deep-audit`](https://github.com/Songhonglei/build-better-skills/tree/main/skills/skill-deep-audit) | ✅ v1.0.0 |
| Audit | [`skill-release-audit`](https://github.com/Songhonglei/build-better-skills/tree/main/skills/skill-release-audit) | ✅ v1.0.1 |
| Release | [`skill-sign`](https://github.com/Songhonglei/build-better-skills/tree/main/skills/skill-sign) | ✅ v1.0.0 |
| Release | `skill-release` | Coming soon |
| **Testing** | **`skill-regression`** | **✅ v1.0.0** |
| Sediment | `skill-sediment` | Coming soon |

## Contributing

Issues and PRs welcome at [Songhonglei/build-better-skills](https://github.com/Songhonglei/build-better-skills).
