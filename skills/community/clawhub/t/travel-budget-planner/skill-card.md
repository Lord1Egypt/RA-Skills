## Description: <br>
零配置即装即用，智能估算20+目的地旅行预算含机票签证保险，四档风格对比一人一价，支持多目的地性价比排名。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-planning agents use this skill to estimate RMB-denominated trip budgets for supported destinations, compare travel styles, and rank multiple destinations by estimated cost. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan marked the release suspicious because it reported a review helper that can run nested Codex with full sandbox bypass by default. <br>
Mitigation: Install only in a trusted ClawHub maintenance worktree, review the helper before use, and prefer --no-yolo unless full sandbox bypass is intentional. <br>
Risk: Budget, flight, visa, insurance, and exchange-rate values are static estimates and may be inaccurate for current travel conditions. <br>
Mitigation: Treat outputs as planning guidance and verify prices, exchange rates, visa requirements, and insurance costs with authoritative sources before booking. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travel-skills/travel-budget-planner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, guidance] <br>
**Output Format:** [Markdown budget reports and comparison tables; JSON error messages for unsupported inputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses embedded estimates and does not make external requests; amounts are RMB estimates and should be verified before booking.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata, VERSION) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
