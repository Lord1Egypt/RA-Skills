## Description: <br>
Audits a user's current AI tool stack, scores each tool by ROI, identifies redundancies and gaps, and produces a structured report with a disclosed paid upgrade for personalized stack recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fresh3](https://clawhub.ai/user/fresh3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and teams use this skill to audit AI-tool subscriptions, compare tool ROI, identify redundant spend, and surface the top AI workflow gaps before deciding whether to buy personalized stack recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The free audit includes a disclosed paid upsell and does not provide specific replacement-tool recommendations. <br>
Mitigation: Install only if that free-versus-paid boundary is acceptable before relying on the generated report. <br>
Risk: Cost-cutting or gap analysis may be misleading if the user's inventory, costs, or usage details are incomplete. <br>
Mitigation: Review the generated report before acting on cancellation, downgrade, or workflow-change advice. <br>
Risk: Optional report export writes to a user-approved file path. <br>
Mitigation: Approve export only after confirming the exact destination path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fresh3/taizi-ai-productivity-audit) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown report; optionally saved as a local Markdown file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided tool inventory, approximate monthly costs, primary use cases, and usage frequency; the free report names gap categories but does not provide specific replacement-tool recommendations.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
