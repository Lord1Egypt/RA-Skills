## Description: <br>
Lists installed OpenClaw skills, summarizes what each skill does, groups skills by function, and identifies overlapping capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[damienCronw](https://clawhub.ai/user/damienCronw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users and developers use this skill to inventory local skills, inspect descriptions, compare functional categories, and identify duplicate or overlapping skill capabilities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper reads the local OpenClaw skills directory and can print locally installed skill descriptions. <br>
Mitigation: Run it only in environments where local skill metadata may be inspected and shared with the user requesting the inventory. <br>
Risk: The helper invokes the installed clawhub CLI, so output depends on the trusted local CLI and PATH. <br>
Mitigation: Use it only where the installed clawhub CLI and PATH are trusted, and treat printed descriptions as informational metadata. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/damienCronw/skill-list) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with command examples and plain-text CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local OpenClaw skill metadata and may invoke the installed clawhub CLI when the helper script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
