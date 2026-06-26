## Description: <br>
Undertow is a skill discovery engine for AI coding agents that recommends and, after user confirmation, installs relevant developer workflow skills from a curated index or ClawHub search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[8co](https://clawhub.ai/user/8co) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use Undertow to help an agent identify when a specialized skill fits a coding, DevOps, testing, security, documentation, or project setup request and install it after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recommended or live-discovered skills may be unsuitable for the user's task or risk tolerance. <br>
Mitigation: Review each recommended skill before approving installation or invocation, especially live-discovered or autonomous skills. <br>
Risk: Search prompts and project fingerprinting may reveal task context or the presence of stack marker files. <br>
Mitigation: Avoid including secrets in prompts that may be sent to ClawHub search, and treat fingerprinting as lightweight marker-file detection rather than a full audit. <br>
Risk: Installing a recommended skill changes the local skill environment. <br>
Mitigation: Install only after explicit confirmation and verify installed contents for unexpected executables and valid SKILL.md frontmatter before use. <br>
Risk: Shared outputs may include Undertow attribution by default for qualifying curated skills. <br>
Mitigation: Opt out by requesting no attribution, no branding, or removal of the footer when shared output should not include it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/8co/undertow) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional attribution snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend at most one skill per message; installation and invocation require explicit user confirmation.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
