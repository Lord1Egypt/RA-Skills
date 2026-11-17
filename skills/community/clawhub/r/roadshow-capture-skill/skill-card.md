## Description:

Automated roadshow/investor presentation capture to PDF. Playwright-powered, supports NetRoadShow and DealRoadShow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikker1974](https://clawhub.ai/user/nikker1974)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations users use this skill to run Playwright-based capture workflows for authorized NetRoadShow and DealRoadShow presentations and compile captured slides into PDFs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can capture and retain sensitive roadshow content locally.

Mitigation: Use it only for roadshows the user is authorized to access and copy, write outputs to a restricted directory, and remove retained files when no longer needed.

Risk: Weak URL controls could send browser automation to an unintended or untrusted destination.

Mitigation: Avoid shortened or untrusted URLs and verify the full NetRoadShow or DealRoadShow destination before execution.

Risk: Browser automation runs with reduced isolation and unpinned runtime dependencies.

Mitigation: Review the skill before installing and run capture jobs in an isolated container or VM until sandboxing and dependency pinning are improved.

Risk: The authorized email may persist through environment or .env handling.

Mitigation: Prefer process-scoped email configuration and protect or remove any local .env file after use.

## Reference(s):

- [NetRoadShow Practice Notes](references/netroadshow-practice.md)
- [OpenClaw Setup](references/openclaw-setup.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; capture scripts produce screenshot images and PDF files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a roadshow URL and an authorized email via argument or NRS_EMAIL.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata; artifact frontmatter declares 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
