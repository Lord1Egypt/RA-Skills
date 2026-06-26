## Description: <br>
Work on Xiaohongshu post/comment collection, cookie handling, refresh flows, and browser plugin integration in the forbidden_company repo. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pengluday](https://clawhub.ai/user/pengluday) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to update or operate local Xiaohongshu post and comment collection, including cookie handling, single-URL refreshes, pagination, and browser plugin integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved Xiaohongshu cookies are private session credentials. <br>
Mitigation: Read or update cookies only for the intended local workflow and do not share cookie values in chat or generated output. <br>
Risk: Single-URL refresh can replace existing collected rows. <br>
Mitigation: Confirm refresh targets and keep backups when preserving prior collected rows matters. <br>
Risk: Collection workflows can be misapplied outside the intended local, user-driven model. <br>
Mitigation: Keep usage scoped to the intended local collector repo and avoid shared-server mass collection patterns. <br>


## Reference(s): <br>
- [Xiaohongshu Collector Workflow](references/collector-workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, code edits, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local collection or refresh guidance; should not echo private cookie values.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
