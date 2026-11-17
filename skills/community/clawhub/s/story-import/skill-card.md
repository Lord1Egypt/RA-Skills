## Description:

逆向导入已有小说，将半成品或完本解析为标准项目结构，供后续写作流程续写。

This skill is ready for commercial/non-commercial use.

## Publisher:

[worldwonderer](https://clawhub.ai/user/worldwonderer)

### License/Terms of Use:

MIT

## Use Case:

小说作者可将已有的半成品或完本整理成设定、大纲、正文和追踪文件，并从导入进度继续写作。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The inspected behavior may not fully match the advertised novel-import workflow, and the security scan was partial.

Mitigation: Review the skill's outline-viewing and validation behavior and inspect any incompletely scanned or missing files before installation.

Risk: The skill has file and shell capabilities and a broad activation trigger, as noted in the security guidance.

Mitigation: Check that the requested file access, shell actions, and activation scope match your needs before enabling it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/worldwonderer/skills/story-import)
- [Length routing guide](artifact/references/length-routing.md)
- [Deep analysis workflow](artifact/references/deep-analysis.md)
- [Long-form structure mapping](artifact/references/structure-mapping-long.md)
- [Short-form structure mapping](artifact/references/structure-mapping-short.md)
- [Outline reverse workflow](artifact/references/outline-reverse.md)
- [Import tracking guide](artifact/references/import-tracking.md)
- [Import report guide](artifact/references/import-report.md)

## Skill Output:

**Output Type(s):** [Files, Markdown, JSON, Configuration instructions, Guidance]

**Output Format:** [A novel project directory containing Markdown project documents and JSON tracking data, plus a Markdown import report.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Project files and tracking scope depend on the author's confirmed source range, novel length, and import choices.]

## Skill Version(s):

1.0.46 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
