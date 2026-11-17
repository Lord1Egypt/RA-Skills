## Description:

研究生开题专利调研。当用户说「开题前帮我查查专利」「我的课题别人做过没有」「开题报告研究现状里的专利部分怎么写」「导师让我先调研一下专利」「选题前看看这个方向有哪些专利」时使用。输出带公开号和出处的开题专利调研表（Excel 能打开），以及研究现状专利部分的草稿。 Patent survey for graduate thesis proposals. Turns the research topic into search queries, groups related patents by technical route into a sourced table, and drafts the patent part of the literature review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

Graduate students and researchers use this skill to survey patents related to a thesis proposal, compare technical approaches, and prepare a sourced patent section for a research-status review.

### Deployment Geography for Use:

Global (China, United States, Europe, Japan, Korea, and WIPO)

## Known Risks and Mitigations:

Risk: The security review flags unsafe credential routing and cache paths for review.

Mitigation: Prefer a version that restricts credential destinations and validates cache filenames before installation.

Risk: Search queries are sent to PatentMax, while API keys and research state persist locally.

Mitigation: Do not submit confidential invention details; use a limited key and set an explicit spending budget.

Risk: Repeated requests may incur charges.

Mitigation: Check request status and billing before retrying; do not assume retries are free.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/ip930/skills/thesis-patent-survey)
- [Publisher profile](https://clawhub.ai/user/ip930)
- [PatentMax API platform](https://api.ip930.com/features/api-platform)
- [PatentMax API reference](references/api-reference.md)
- [Patent search workflow](references/search-workflow.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, CSV]

**Output Format:** [UTF-8 CSV patent survey table and a Markdown research-status draft]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Patent entries include publication numbers and source references; a candidate-patent CSV may also be exported.]

## Skill Version(s):

1.0.2 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
