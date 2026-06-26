## Description: <br>
Use when submitting a product to AI/startup directories - covers the full pipeline from collecting product info, analyzing directories, discovering forms, auto-submitting, handling captchas/OAuth/GitHub PRs, and tracking progress in checkpoint.md. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[man0l](https://clawhub.ai/user/man0l) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, founders, and growth teams use this skill to prepare product submission data, analyze AI and startup directories, discover submission forms, automate eligible submissions, and track manual follow-up work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send product details, contact information, optional throwaway credentials, and images to many third-party directory sites. <br>
Mitigation: Review and prune directories.json before running submissions, use throwaway contact details and credentials, and avoid real personal passwords. <br>
Risk: The broad directory list can include unintended, low-quality, blocked, paid, or login-gated destinations. <br>
Mitigation: Require manual approval per destination or category and review the generated submission plan before form discovery or submission. <br>
Risk: OAuth flows, captcha handling, and GitHub PR creation require user-controlled actions outside simple form filling. <br>
Mitigation: Treat OAuth login, captcha solving, and GitHub PR creation as explicit confirmation points before proceeding. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/man0l/submit-directories) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Markdown] <br>
**Output Format:** [Markdown instructions with shell commands and generated JSON/checkpoint files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and updates local submission planning, directory analysis, form discovery, submission status, and progress-tracking files.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
