## Description:

新闻联播中翻中 translates CCTV XinWenLianBo official language into plain Chinese, fetching public transcripts from tv.cctv.com, decoding bureaucratic phrasing, identifying policy signals, and producing structured summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ltryee](https://clawhub.ai/user/ltryee)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to read, translate, explain, or summarize CCTV XinWenLianBo transcripts in accessible Chinese. It is intended for structured plain-language explanations, key information extraction, policy-signal interpretation, and daily summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests that only loosely mention 联播 or policy trends may trigger the skill broadly.

Mitigation: Confirm the user's intent before fetching or interpreting XinWenLianBo content when the request is ambiguous.

Risk: Policy-signal analysis is inferential and may be mistaken for an official position.

Mitigation: Label interpretations as analysis, preserve source facts separately, and note uncertainty when multiple readings are possible.

Risk: Fetching current or historical transcripts from public CCTV pages can fail because of network issues or unavailable archived pages.

Mitigation: Report source retrieval failures clearly and avoid filling gaps with unsourced content.

## Reference(s):

- [CCTV XinWenLianBo page](https://tv.cctv.com/lm/xwlb/index.shtml)
- [《新闻联播》话术词典](references/xinwenlianbo-jargon-dictionary.md)
- [《新闻联播》节目结构与信号体系指南](references/xinwenlianbo-structure-guide.md)
- [ClawHub skill page](https://clawhub.ai/ltryee/skills/xinwenlianbo-translator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Markdown with headings, bullet lists, tables, and plain-language Chinese analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include daily summaries, per-story explanations, jargon translation tables, and policy-signal notes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
