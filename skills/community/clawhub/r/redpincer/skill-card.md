## Description:

AI/LLM red team testing skill for running authorized automated security assessments against LLM API endpoints with attack payloads, variant transforms, adaptive follow-ups, heuristic analysis, vulnerability heatmaps, regression testing, and exportable pen-test reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rustyorb](https://clawhub.ai/user/rustyorb)

### License/Terms of Use:


## Use Case:

External developers, security engineers, and AI safety teams use this skill to configure LLM API targets, run authorized red-team assessments, compare attack results, and generate Markdown penetration-test reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the skill requires running mutable external code that was not included in the reviewed package.

Mitigation: Review the external repository and package scripts before installation, pin a specific audited commit, and run the tool in a restricted local environment.

Risk: The dashboard can be exposed beyond localhost in production mode.

Mitigation: Keep access limited to localhost unless authentication and network controls are added.

Risk: The tool can be misused against LLM systems without authorization.

Mitigation: Use it only on LLM systems you own or have explicit permission to assess.

## Reference(s):

- [RedPincer ClawHub listing](https://clawhub.ai/rustyorb/skills/redpincer)
- [RedPincer repository referenced by artifact](https://github.com/rustyorb/pincer.git)
- [RedClaw companion tool referenced by artifact](https://github.com/rustyorb/redclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command blocks, workflow steps, and report-generation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides an agent through cloning and running a Node/npm dashboard, configuring LLM API targets, executing authorized security tests, reviewing heuristic results, and exporting reports.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
