## Description: <br>
Instructs embodied AI agents to process LiDAR, camera, and tactile data, avoid visual illusions through cross-validation, and produce 1-60s physical causal predictions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spacesq](https://clawhub.ai/user/spacesq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and robotics or embodied AI teams use this skill to feed multimodal sensor readings into an agent workflow, resolve sensor conflicts such as transparent obstacles, and generate short-horizon causal narratives for physical decision support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Predictions may be unsafe if used directly for real-world movement or safety decisions without validating the connected sensor stack. <br>
Mitigation: Validate the skill with the actual LiDAR, camera, and tactile inputs in controlled simulations or test environments, and keep independent safety controls in place. <br>
Risk: The skill intentionally treats PIR-like inputs as unsupported. <br>
Mitigation: Confirm that this sensor policy fits the deployment and provide higher-dimensional sensor inputs before relying on its output. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/spacesq/s2-multimodal-fusion-predictor) <br>
- [Taohuayuan World Model Whitepaper V3.1](artifact/s2-swm-v3.1-multimodal-fusion.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [Structured JSON from the tool and concise natural-language causal narratives.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Causal prediction windows cover t+1s through t+60s and may include aligned sensor state.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release, SKILL.md frontmatter, package.json, openclaw.plugin.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
