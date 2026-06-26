## Description: <br>
Helps users publish or update a skill on ClawhHub by guiding folder selection, versioning, changelog collection, confirmation, and `clawhub publish` CLI execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xingke2023](https://clawhub.ai/user/xingke2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill publishers use this skill to release new or updated ClawHub skills with a confirmed slug, version, changelog, and local CLI account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing the wrong skill folder, slug, version, changelog, tags, or local account could release unintended content. <br>
Mitigation: Verify the selected folder, slug, version, changelog, tags, and active `clawhub` CLI account before confirming publication. <br>
Risk: The skill has a broad activation trigger for publishing requests. <br>
Mitigation: Use it only for user-directed ClawHub publishing tasks and require explicit confirmation before running the publish command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xingke2023/xingke-clawhub-publish) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/xingke2023) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and confirmation prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce `clawhub inspect`, `clawhub publish`, `clawhub whoami`, and related local CLI commands for user review and execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
