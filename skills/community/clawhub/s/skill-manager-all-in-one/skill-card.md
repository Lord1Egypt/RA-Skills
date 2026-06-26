## Description: <br>
Manage OpenClaw skills end-to-end. 一站式管理 OpenClaw 技能的创建、修改、发布、更新、升版与审计。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moroiser](https://clawhub.ai/user/moroiser) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to create, modify, publish, update, promote, and audit OpenClaw skills across ClawHub and GitHub workflows. It is intended for administrative skill-management tasks that require explicit review before publishing or writing changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports administrative actions for skill creation, modification, publishing, updating, hiding, deletion, promotion, and audit. <br>
Mitigation: Before signing confirmation, verify the exact target slug, repository, active account, command, version, changelog, and public post text. <br>
Risk: The skill may rely on authenticated ClawHub, Git, or GitHub CLI sessions and may propose memory-file or workspace edits. <br>
Mitigation: Confirm the active account and inspect proposed workspace or memory-file changes before allowing writes or external publishing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/moroiser/skill-manager-all-in-one) <br>
- [ClawHub Publish Reference](references/clawhub-publish.md) <br>
- [GitHub Publishing Guide](references/github-publish.md) <br>
- [ClawFlows Workflow Format Guide](references/clawflows-workflow.md) <br>
- [Promotion Guide](references/promotion.md) <br>
- [Search and Audit Guide](references/search-and-audit.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose file edits, publishing commands, changelog text, audit findings, and promotion text for user review.] <br>

## Skill Version(s): <br>
4.5.14 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
