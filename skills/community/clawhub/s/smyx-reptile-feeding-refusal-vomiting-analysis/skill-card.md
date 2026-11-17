## Description:

Analyzes reptile feeding and post-feeding videos to record prey-attack, swallowing, feeding-refusal, and regurgitation behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Reptile keepers use feeding footage to review whether an animal attacked and swallowed prey, refused food, or regurgitated after feeding. The skill provides behavior records and alerts; it does not diagnose disease.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports credential and account handling and broad credentialed network requests; the scan was partial and its findings do not establish intent.

Mitigation: Review credential scope and account behavior before use, and run with only the access required for the task.

Risk: The security summary reports that video may be uploaded even in export-only mode.

Mitigation: Confirm whether footage is transmitted and where it goes before using private enclosure video; use non-sensitive footage until verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-reptile-feeding-refusal-vomiting-analysis)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [API reference](artifact/references/api_doc.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Alerts]

**Output Format:** [Structured feeding-event report with behavior findings, recommendations, and report links; JSON or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include event timing, confidence values, and feeding-context indicators when available.]

## Skill Version(s):

1.0.16 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
