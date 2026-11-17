## Description:

Use when submitting a product to AI/startup directories, covering the full pipeline from collecting product info, analyzing directories, discovering forms, auto-submitting, handling captchas/OAuth/GitHub PRs, and tracking progress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[man0l](https://clawhub.ai/user/man0l)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, founders, and launch teams use this skill to submit a product or startup to AI and startup directories. It helps collect product details, classify directory targets, discover forms, automate eligible submissions, coordinate manual captcha/OAuth/GitHub PR steps, and track progress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send credentials, contact details, product details, and uploaded assets to many third-party websites.

Mitigation: Use only throwaway credentials and non-sensitive submission assets, run in an isolated project with no unrelated secrets, and require manual confirmation before password entry, OAuth, uploads, or final submission.

Risk: Some directory targets may be untrusted or use plaintext HTTP.

Mitigation: Review the directory list and generated submission_plan.json before execution, and remove or disable plaintext HTTP and untrusted targets.

Risk: Generated tracking files can contain contact or product submission data.

Mitigation: Inspect submission_plan.json and checkpoint.md before sharing or committing; keep passwords out of saved files and strip personal data before publishing.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON files, guidance]

**Output Format:** [Markdown instructions with shell commands and generated local JSON/Markdown tracking files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update submission_plan.json, checkpoint.md, browser_check_list.json, and per-directory status data; credentials are configured through environment variables.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
