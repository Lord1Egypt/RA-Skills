## Description: <br>
Comprehensive pre-install guard that audits third-party skills across nine risk areas, covering semantic integrity, supply chain, secrets, data exfiltration, injection resistance, permission scope, destructive potential, resource abuse, and persistence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yxf203](https://clawhub.ai/user/yxf203) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill before installing or enabling externally sourced skills to review package artifacts, identify security and trust risks, and produce a plain-language risk assessment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release has limited external provenance metadata. <br>
Mitigation: Confirm the ClawHub publisher handle and release version before relying on the skill in a sensitive environment. <br>
Risk: The skill reviews untrusted third-party skill artifacts. <br>
Mitigation: Use the documented package-directory scope boundary and do not execute, follow, or traverse paths from candidate artifacts during review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yxf203/skill-risk-auditor) <br>
- [Publisher profile](https://clawhub.ai/user/yxf203) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown risk assessment with severity ratings and plain-language explanations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Covers nine risk areas and includes evidence-backed findings for non-technical readers.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
