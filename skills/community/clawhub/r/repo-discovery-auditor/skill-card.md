## Description: <br>
Repo Discovery Auditor helps an agent audit an unfamiliar codebase, map its architecture and user-facing features, assess maturity, surface risks, and prepare a practical coding brief. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nalendrax8](https://clawhub.ai/user/nalendrax8) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to inspect unfamiliar repositories before planning, refactoring, or implementation work. It produces an evidence-based architecture summary, feature map, maturity assessment, risk list, and implementation handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to read repository contents, which may expose secrets or sensitive files to the agent. <br>
Mitigation: Use it only on repositories the user is comfortable exposing to the agent, and avoid repos containing unredacted secrets or highly sensitive data. <br>
Risk: Static repository inspection can produce incorrect assumptions about runtime behavior. <br>
Mitigation: Tie claims to inspected files or patterns, and label any runtime behavior that was not directly verified. <br>


## Reference(s): <br>
- [Repo Discovery Auditor release page](https://clawhub.ai/nalendrax8/repo-discovery-auditor) <br>
- [Publisher profile](https://clawhub.ai/user/nalendrax8) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown report with structured audit sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include file references, maturity labels, risk notes, and recommended next steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
