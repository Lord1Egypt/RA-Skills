## Description: <br>
Helps track how AI skill verification results decay over time as dependencies, attack vectors, and ecosystem context change. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, marketplace maintainers, and security reviewers use this skill to estimate whether prior skill verification results have become stale and to prioritize re-verification across single skills or portfolios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trust freshness scores are heuristic triage signals and may be mistaken for proof that a skill is safe or unsafe. <br>
Mitigation: Use the report to prioritize re-verification, then confirm findings with a current security review before relying on a verification decision. <br>
Risk: Marketplace, dependency, or internal portfolio data supplied for analysis may contain sensitive information. <br>
Mitigation: Avoid submitting private marketplace or internal dependency data unless the user intends the agent to analyze that information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/andyxinweiminicloud/trust-decay-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown trust freshness report with scores, decay factors, urgency, and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scores are heuristic triage signals and should not be treated as proof that a skill is safe or unsafe.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
