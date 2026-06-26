## Description: <br>
数字大脑工厂 provides AI cognitive governance and research services, including paper review, research analysis, system audit, cognitive diagnosis, and V19 governance checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuyanfeng1234](https://clawhub.ai/user/liuyanfeng1234) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to request paper review, research analysis, system architecture audit, cognitive diagnosis, and V19 governance protocol checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends potentially sensitive papers, research ideas, system architecture, logs, or decision context to an external provider and may use a configured callback URL. <br>
Mitigation: Review before installing, submit only content suitable for that provider and callback destination, and confirm privacy, retention, API-key, and callback-safety behavior before use. <br>
Risk: The reviewed security evidence reports Python import path mutation outside the package. <br>
Mitigation: Remove or justify the home-directory import paths before deployment, and review the local environment used for payment verification and service calls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liuyanfeng1234/v19-cognition) <br>
- [Service gateway](https://clawtip.jd.com) <br>
- [V19 governance protocol guide](governance_protocol.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [JSON responses and human-readable analysis or governance guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results may be returned asynchronously through a configured callback URL.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
