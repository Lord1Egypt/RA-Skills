## Description: <br>
Red Alarm reviews Xiaohongshu-style AI content compliance for submitted text and media descriptions, producing structured risk findings, scores, and revision guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mars2003](https://clawhub.ai/user/mars2003) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, operators, and reviewers use this skill to pre-check Xiaohongshu posts, captions, media descriptions, and account behavior context for AI-content policy risks and get remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill's compliance conclusions are advisory and may not match final platform enforcement decisions. <br>
Mitigation: Treat results as guidance, review material facts before publishing, and escalate borderline decisions to a human reviewer. <br>
Risk: Submitted account history or moderation context may contain sensitive data. <br>
Mitigation: Redact personal, private, or unnecessary account details before using the skill. <br>
Risk: Image and video review is based on user-provided descriptions rather than direct media inspection. <br>
Mitigation: Provide accurate media descriptions and keep uncertain visual issues as risk points rather than definitive violations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mars2003/red-alarm) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown content review report with risk score, risk level, findings, and suggested revisions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language report; image and video assessment depends on user-provided descriptions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
