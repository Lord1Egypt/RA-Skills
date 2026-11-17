## Description: <br>
Helps agents produce UI/UX design-system guidance, technology-stack implementation notes, and optional persisted design-system files for web and app projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Designers, developers, and product teams use this skill to ask an agent for UI/UX design decisions, design-system rules, page-level overrides, and implementation guidance across common web and mobile stacks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run local Python commands and write design-system files into the project workspace. <br>
Mitigation: Use persistence only in repositories where design-system/ may be created or updated, then review generated diffs before accepting them. <br>
Risk: Setup or verification examples may involve local package-management or shell commands. <br>
Mitigation: Review commands before execution and do not allow an agent to run sudo or administrator package-install commands automatically. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/ui-ux-toolkit) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update design-system/MASTER.md and design-system/pages/*.md when persistence is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
