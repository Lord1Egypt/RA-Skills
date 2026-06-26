## Description: <br>
Regex-based routing sends simple tasks to local AI, medium to mid-tier, complex to premium, helping reduce API costs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to route prompts by estimated task complexity across local, mid-tier, and premium models. It supports cost-conscious model selection for normal agent workflows while allowing custom routing rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Routing rules can send confidential, regulated, credential-bearing, or high-risk prompts to an unintended model tier. <br>
Mitigation: Review routing rules before deployment and configure explicit safeguards for sensitive workloads and model destinations. <br>
Risk: Regex-based complexity detection can misclassify ambiguous or novel requests. <br>
Mitigation: Test representative prompts, add custom rules for critical workflows, and allow manual overrides when model choice matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TheShadowRose/task-complexity-router) <br>
- [Publisher profile](https://clawhub.ai/user/TheShadowRose) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [code, configuration, guidance] <br>
**Output Format:** [JavaScript objects and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routing decisions include a model name, reason, confidence score, and matched rule names.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
