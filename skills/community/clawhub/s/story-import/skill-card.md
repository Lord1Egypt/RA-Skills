## Description:

逆向导入已有小说。将已写好的小说（半成品或完本）反向解析为标准项目目录结构，兼容 story-long-write / story-short-write 后续写作流程；内部复用 story-long-analyze / story-short-analyze 的拆解管道，按篇幅自动分流。

This skill is ready for commercial/non-commercial use.

## Publisher:

[worldwonderer](https://clawhub.ai/user/worldwonderer)

### License/Terms of Use:

MIT

## Use Case:

Writers use this skill to turn an existing novel or partial manuscript into a structured project for continued writing, including analysis, settings, outlines, prose files, and (for long works) continuity tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generic import phrases may activate the skill when the user did not intend to start an import workflow.

Mitigation: Invoke it with the explicit /story-import command when a clear activation is needed.

Risk: Some components were only partially inspected, so the scan does not establish that all behavior is safe.

Mitigation: Review the skill before installing and seek a complete inspection of the partially analyzed components.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/worldwonderer/skills/story-import)
- [deep-analysis.md](references/deep-analysis.md)
- [import-report.md](references/import-report.md)
- [import-tracking.md](references/import-tracking.md)
- [outline-reverse-rules.md](references/outline-reverse-rules.md)
- [outline-reverse.md](references/outline-reverse.md)
- [structure-mapping-long.md](references/structure-mapping-long.md)
- [structure-mapping-short.md](references/structure-mapping-short.md)
- [Project link listed in skill metadata](https://github.com/zenstory-ai/oh-story-claudecode)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance]

**Output Format:** [A structured writing project made of Markdown files, plus a plain-language completion report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Project contents vary by confirmed manuscript scope and whether it is routed as a long or short work.]

## Skill Version(s):

1.0.55 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
