## Description: <br>
Use when completing tasks, implementing major features, or before merging to verify work meets requirements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[demo112](https://clawhub.ai/user/demo112) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to request focused code reviews after tasks, major features, bug fixes, refactors, or before merging. It provides a repeatable prompt template for reviewing a git range against requirements and categorizing findings by severity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence reports that related autoreview behavior may launch nested reviewers with broad filesystem access and sandbox bypass. <br>
Mitigation: Install only if the publisher is trusted, and prefer --no-yolo or AUTOREVIEW_YOLO=0 before using autoreview workflows. <br>
Risk: Fallback reviewers may receive repository diffs. <br>
Mitigation: Use the skill only with repositories and git ranges whose diffs are appropriate to share with the selected reviewer. <br>
Risk: Security guidance warns that moderation commands can affect public skills, users, roles, and tokens. <br>
Mitigation: Use moderation commands only with explicit targets, reasons, and confirmation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/demo112/superpowers-requesting-code-review) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [code-reviewer.md](artifact/code-reviewer.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown instructions with inline shell commands and a structured review template] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces reviewer prompts and severity-categorized code review guidance; does not execute commands by itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
