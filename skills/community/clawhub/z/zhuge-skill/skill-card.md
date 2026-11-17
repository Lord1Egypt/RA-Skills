## Description:

Zhuge Skill helps agents run football match predictions using multi-source sports data, local 64-hexagram scoring, optional LLM commentary, and self-learning prediction records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangfei222666-9](https://clawhub.ai/user/yangfei222666-9)

### License/Terms of Use:

MIT-0

## Use Case:

Agent users and developers use this skill to run local football prediction workflows, batch predictions, backfill match results, review accuracy statistics, and generate optional LLM-written reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be stored in a plaintext .env file for local CLI use.

Mitigation: Use a dedicated virtual environment, keep the skill directory private, and rotate provider keys if the local environment is exposed.

Risk: Configured sports and LLM providers receive the match data or prompts needed for the requested workflow.

Mitigation: Configure only providers you trust, prefer official provider endpoints, and avoid relay mode unless that proxy is trusted.

Risk: Crystal-based confidence and public crystal data are unverified and may be affected by data quality issues.

Mitigation: Treat predictions as decision support, validate outputs against independent sources, and avoid relying on them as sole wagering or financial advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangfei222666-9/skills/zhuge-skill)
- [README.en.md](artifact/README.en.md)
- [PRIVACY.md](artifact/PRIVACY.md)
- [CHANGELOG.md](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented text with inline shell commands and local file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local JSONL prediction, crystal, error-log, report, and export files inside the skill directory.]

## Skill Version(s):

1.1.1 (source: server release metadata and CHANGELOG, released 2026-04-19)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
