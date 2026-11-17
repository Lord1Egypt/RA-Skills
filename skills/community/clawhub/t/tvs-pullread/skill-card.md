## Description:

分析远程代码变更，既能对比本地差异，也能深入解释远程变更的具体实现和业务逻辑。聚焦业务/功能层面（而非逐文件列出所有改动），帮助开发者快速理解 PR/拉取的实质内容，并可深入解读任何感兴趣的变更细节。分析后主动询问是否合并，以及是否需要协助处理冲突。

This skill is ready for commercial/non-commercial use.

## Publisher:

[inksnowhailong](https://clawhub.ai/user/inksnowhailong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review incoming Git changes at the business and functional level before deciding whether to pull or merge them. It summarizes remote diffs, explains implementation details on request, highlights merge risks, and suggests testing focus.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run git fetch, which contacts the configured remote and may use the user's normal Git credentials.

Mitigation: Use it only with trusted repository remotes and expected credentials; review the fetched diff before approving any pull or merge.

Risk: Its summaries and merge guidance can be incomplete or incorrect for complex changes.

Mitigation: Review the summarized changes and validate important behavior with targeted tests before merging.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/inksnowhailong/skills/tvs-pullread)

## Skill Output:

**Output Type(s):** [analysis, markdown, shell commands, guidance]

**Output Format:** [Markdown with concise summaries, risk notes, testing guidance, and optional Git shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language responses focused on business-level Git change review.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
