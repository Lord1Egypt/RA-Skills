## Description:

A WeRead/WeChat Reading skill for reading dashboards, book analysis, cross-book connections, and confirmed note exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yamyeed](https://clawhub.ai/user/yamyeed)

### License/Terms of Use:

MIT

## Use Case:

External readers use the skill to review WeRead reading activity, analyze books, connect ideas across books, and create requested Markdown or HTML exports. It requests confirmation before accessing each new private-data scope and before writing files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private reading history, highlights, or personal notes may be exposed through analysis or agent context.

Mitigation: Keep the API key in the environment rather than chat, request only the books and data fields needed, and obtain explicit confirmation for each new private-data scope.

Risk: Exported notes or analysis may persist sensitive content in local files.

Mitigation: Before writing, confirm the exact file path and content; review the export and destination before saving.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/yamyeed/skills/weread-ai-brain)
- [Project homepage (skill metadata)](https://github.com/yamyeed/weread-ai-brain)
- [Dashboard guidance](artifact/references/dashboard.md)
- [Analysis and export guidance](artifact/references/analysis-and-export.md)

## Skill Output:

**Output Type(s):** [Text, Analysis, Markdown, HTML files]

**Output Format:** [Conversational text or Markdown; optional offline HTML dashboards and Markdown exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Private reading data is limited to the confirmed scope; file exports require confirmation of content and destination.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
