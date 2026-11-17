## Description:

Use when diagnosing PPT Skill setup or failures involving source parsing, Playwright or Chromium rendering, HTML-to-PPTX export, Workbench startup, or bundled search and image-tool configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sensenova-skills](https://clawhub.ai/user/sensenova-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and PPT skill users run the doctor to diagnose local rendering dependencies, workspace readiness, and optional search or image-tool configuration. It helps identify missing capabilities and shows configuration guidance without changing the task directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configuration loading and online probes depend on separately installed PPT helper skills.

Mitigation: Use trusted companion PPT skills when running the doctor.

Risk: An image-generation probe may incur charges and save an image in the selected directory.

Mitigation: Run the image-generation probe only when wanted, and choose its output directory deliberately.

## Reference(s):

- [ClawHub release](https://clawhub.ai/sensenova-skills/skills/sn-ppt-doctor)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Configuration guidance, Shell commands]

**Output Format:** [JSON diagnostic report with explanatory guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports detected environment and optional media status; does not install dependencies or modify configuration.]

## Skill Version(s):

2026.10.29 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
