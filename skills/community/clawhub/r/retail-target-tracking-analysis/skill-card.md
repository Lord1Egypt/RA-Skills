## Description:

门店目标追踪分析 helps agents track retail target attainment across daily, weekly, and monthly periods with T-N data delay handling and status-based alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gwyang7](https://clawhub.ai/user/gwyang7)

### License/Terms of Use:

MIT-0

## Use Case:

Retail operations teams and agents use this skill to analyze store, city, province, region, or group target progress, format attainment reports, and identify locations that need attention. It supports daily meeting checks, weekly reviews, monthly assessment, and scheduled alert checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill imports executable code from a hard-coded local directory outside the package, so the artifact alone does not prove what code will run.

Mitigation: Install only after replacing that dependency with a packaged, reviewed client or otherwise verifying and controlling the exact api_client module path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gwyang7/skills/retail-target-tracking-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include target attainment status, warning levels, period summaries, and sorted alert lists; behavior depends on local target files and available business data.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
