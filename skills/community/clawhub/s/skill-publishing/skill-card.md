## Description: <br>
Guide to publishing and sharing Hermes skills through ClawHub, including safe login practices, release hygiene, and security scan preparation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuxuclassmate](https://clawhub.ai/user/xuxuclassmate) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill publishers use this guide to prepare Hermes skills for ClawHub publication, update published versions, handle login tokens safely, and check release hygiene before security scanning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Command examples include publish, delete, and merge operations that can change ClawHub skill state if copied without review. <br>
Mitigation: Review the target slug, source skill, and account context before running publish, delete, or merge commands. <br>
Risk: ClawHub tokens can be exposed if pasted into shared command history or stored in files. <br>
Mitigation: Read tokens privately, pass them through environment variables only for the login command, unset them afterward, and avoid persisting them in shell history. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xuxuclassmate/skill-publishing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Plain guidance only; no executable code is included in the artifact.] <br>

## Skill Version(s): <br>
1.1.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
