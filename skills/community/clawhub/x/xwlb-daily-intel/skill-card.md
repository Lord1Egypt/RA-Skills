## Description:

Fetches CCTV Xinwen Lianbo transcripts for a selected day and prepares a source-attributed Chinese-language news intelligence report separating facts from analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suaifu](https://clawhub.ai/user/suaifu)

### License/Terms of Use:

MIT-0

## Use Case:

Readers and analysts use this skill to collect a day's CCTV Xinwen Lianbo coverage and produce a concise Chinese-language briefing with categorized news, source confidence, potential implications, and follow-up signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad prompts such as ‘早报’ may invoke this specialized news workflow unintentionally.

Mitigation: Confirm the user wants a CCTV Xinwen Lianbo briefing before using broad triggers.

Risk: Recurring runs can create unwanted local report archives.

Mitigation: Choose an output directory deliberately and enable scheduled runs or long-term notes only when wanted.

Risk: Early or incomplete transcripts can leave items without full text.

Mitigation: Label missing details as unverified and retry or cross-check sources rather than filling gaps with speculation.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/suaifu/skills/xwlb-daily-intel)
- [CCTV Xinwen Lianbo](https://tv.cctv.com/lm/xwlb/index.shtml)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance]

**Output Format:** [Chinese-language Markdown report and optional dated Markdown transcript archive]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Source links and confidence labels; facts distinguished from interpretation.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
