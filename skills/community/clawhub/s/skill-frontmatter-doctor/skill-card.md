## Description: <br>
Reviews and helps repair skill frontmatter, metadata, requires/install declarations, and directory structure so they align with current OpenClaw conventions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to audit, repair, and review OpenClaw skill packaging metadata before release or batch cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence marks the release suspicious because its behavior appears broader than simple metadata repair. <br>
Mitigation: Review the skill before installation and install it only when the broader audit and scanning behavior is intended. <br>
Risk: Running the skill over private or sensitive workspaces could expose more local project content than needed for metadata repair. <br>
Mitigation: Limit inputs to specific skill directories and remove sensitive material before use. <br>
Risk: Shell execution or file writes can affect local workspace files if approved by the agent runtime. <br>
Mitigation: Require explicit approval before shell commands or writes, and prefer dry-run or review-only output first. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/skill-frontmatter-doctor) <br>
- [Publisher profile](https://clawhub.ai/user/52YuanChangXing) <br>
- [Skill specification resource](artifact/resources/spec.json) <br>
- [Output template resource](artifact/resources/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON reports with review findings, repair suggestions, and optional shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can run locally with python3 and standard-library dependencies; dry-run and output-file modes are documented.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
