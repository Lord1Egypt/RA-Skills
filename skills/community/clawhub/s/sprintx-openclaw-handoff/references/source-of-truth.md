# Source Of Truth

Use these upstream references instead of re-explaining SprintX behavior inside multiple repo files.

## SprintX public docs

- OpenClaw handoff quickstart
  https://www.sprintx.co.kr/docs/getting-started/openclaw-handoff-quickstart
  Why: primary public handoff story and success signals.

- CLI quickstart (English)
  https://www.sprintx.co.kr/docs/getting-started/cli-quickstart
  Why: exact CLI examples, headless notes, and environment-variable details.

- CLI quickstart (Korean)
  https://www.sprintx.co.kr/docs/getting-started/cli-quickstart.ko
  Why: Korean operator-facing detail for the same CLI path.

## SprintX engineering truth

- CLI auth boundary and current truth
  https://github.com/terry3838/SprintX/blob/main/docs/engineering/SX_AUTH_V1.md
  Why: browser-approved auth is the primary path; device flow remains follow-up.

- Product boundary and runtime contract
  https://github.com/terry3838/SprintX/blob/main/docs/engineering/TECH_SPEC.md
  Why: confirms SprintX is the governed delivery control plane, not the executor.

## ClawHub references

- Skill format
  https://raw.githubusercontent.com/openclaw/clawhub/main/docs/skill-format.md
  Why: frontmatter, allowed files, semver, and MIT-0 publish rules.

- CLI docs
  https://raw.githubusercontent.com/openclaw/clawhub/main/docs/cli.md
  Why: manual `clawhub skill publish` flow and supported commands.
