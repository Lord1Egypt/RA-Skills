## Description:

Security Audit Tools helps agents inspect third-party skills, plugins, repositories, packages, shell installers, and GitHub Actions before download or installation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luojin520520](https://clawhub.ai/user/luojin520520)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to triage third-party installs, run source/package/history checks, and generate quantified security review reports before deciding whether to proceed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can overstate scanner coverage or present LOW RISK/PASS outputs as stronger assurance than the evidence supports.

Mitigation: Treat tool output as triage only; require manual review of relevant source, package metadata, and remaining limitations before approving installation.

Risk: Helper scripts may fetch package metadata, download tarballs, clone repositories, or inspect untrusted content with insufficient argument validation.

Mitigation: Run helper scripts only in an isolated workspace with no credentials, validate and quote package names, versions, tarball paths, and repository URLs, and prefer read-only review first.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/luojin520520/skills/security-audit-tools)
- [README](artifact/README.md)
- [Findings Catalog](artifact/findings-catalog.md)
- [Review Report Template](artifact/report-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance, JSON]

**Output Format:** [Markdown and text reports with shell command snippets and optional JSON scanner output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local audit directories or scanner report files when helper scripts are run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
