## Description: <br>
Auto-routes tasks to the cheapest z.ai (GLM) model likely to work correctly, escalating from Flash to Standard to Plus/32B as complexity increases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PrincNL](https://clawhub.ai/user/PrincNL) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to choose an appropriate z.ai (GLM) model tier for each task, starting with lower-cost models and escalating for code, analysis, architecture, and critical decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cost-first routing may select a model that is too weak for security reviews, production changes, legal, medical, financial, or other sensitive work. <br>
Mitigation: Explicitly request a stronger model or disable cost-first routing for sensitive and high-impact tasks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PrincNL/smart-model-routing-for-zai) <br>
- [Publisher profile](https://clawhub.ai/user/PrincNL) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline code and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Model selection guidance for z.ai (GLM) Flash, Standard, and Plus/32B tiers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
