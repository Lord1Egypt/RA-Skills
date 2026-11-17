## Description:

Test and certify AI agent skills: 7 automated checks, grade A-D, certificate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vnbochkarev-netizen](https://clawhub.ai/user/vnbochkarev-netizen)

### License/Terms of Use:

SKILLQA PRO Software License Agreement (v0.1.0)

## Use Case:

Developers and skill publishers use this skill to test agent skill folders before marketplace publication or after edits, producing quality findings, grades, and certification artifacts for review or CI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads the selected target skill folder, including .env-like files, to produce masked secret findings.

Mitigation: Run it only with explicit user consent and disclose the scanned folder and local report paths before execution.

Risk: The skill executes scripts from the target skill under a limited sandbox that is not a strong VM or container security boundary.

Mitigation: Use a disposable VM or container when testing unknown or potentially hostile skills.

Risk: The skill writes QA reports locally and stores a machine-bound license file.

Mitigation: Review retention needs and delete qa_reports/<skill>/ or ~/.config/skillqa/skillqa_license.dat when those artifacts are no longer needed.

## Reference(s):

- [ClawHub listing](https://clawhub.ai/vnbochkarev-netizen/skills/vibo-skillqa)
- [Publisher profile](https://clawhub.ai/user/vnbochkarev-netizen)
- [ViBo SkillQA product site](https://wwwvibo.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON reports, console text, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pro mode can produce certificate-quality Markdown and CI-ready JSON; demo mode produces a static-scan teaser report.]

## Skill Version(s):

0.2.8 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
