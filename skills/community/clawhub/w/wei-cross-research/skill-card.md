## Description:

Wei Cross Research cross-validates research answers by querying multiple LLMs in parallel and synthesizing their responses with a judge model to surface agreement, disagreement, and confidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikehankk](https://clawhub.ai/user/mikehankk)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, developers, and analysts use this skill for higher-confidence research on complex or high-stakes questions where cross-model comparison, disagreement surfacing, and judge-based synthesis are useful.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented Bun installation path includes a curl-to-shell pattern.

Mitigation: Install Bun through a package manager or verified download channel before running the skill.

Risk: Prompts, raw model responses, and judge outputs can be saved locally after each run.

Mitigation: Avoid submitting secrets or sensitive data to configured providers, and delete generated report and intermediate files when retention is not needed.

Risk: Research queries and outputs are sent to third-party model providers selected by configuration.

Mitigation: Use only approved providers and model configurations for the data classification and business context of the query.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mikehankk/skills/wei-cross-research)
- [Skill Homepage](https://github.com/MikeHanKK/wei-skills/tree/main/skills/wei-cross-research)
- [Bun Runtime](https://bun.sh)
- [Configuration Guide](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, JSON, files, guidance]

**Output Format:** [JSON response with a synthesized final answer, confidence score, model status details, and saved text report/raw-output files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs can store prompts, model responses, and judge outputs locally under report and intermediate output paths.]

## Skill Version(s):

1.0.4 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
