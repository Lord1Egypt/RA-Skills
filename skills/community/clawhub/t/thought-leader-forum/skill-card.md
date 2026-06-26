## Description: <br>
AI大佬思想蒸馏框架 helps an agent generate clearly labeled AI-simulated thought-leader discussions, single-person opinion responses, and meeting commentary using a 32-person persona library across AI, hospitality, and venture capital. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chaoliuzhu](https://clawhub.ai/user/chaoliuzhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external users use this skill for internal brainstorming, strategic discussion, and meeting preparation by asking an agent to simulate labeled viewpoints from predefined or newly distilled executive personas. It is intended to keep outputs labeled as AI-generated viewpoint simulations rather than real quotes, endorsements, or authorized opinions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Simulated persona output could be mistaken for real quotes, endorsements, or authorized opinions. <br>
Mitigation: Keep the required viewpoint-simulation labels in every generated persona response and include the skill's disclaimer in reports. <br>
Risk: Sensitive meeting notes or strategy material may be exposed if used with agents that have external search or retrieval tools enabled. <br>
Mitigation: Avoid sharing confidential material with tool-enabled agents unless the deployment environment and tool access are approved for that data. <br>
Risk: Persona simulations based on public information may be inaccurate, outdated, or incomplete. <br>
Mitigation: Treat outputs as brainstorming aids, review important recommendations independently, and refresh persona source material for high-stakes use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chaoliuzhu/thought-leader-forum) <br>
- [Publisher profile](https://clawhub.ai/user/chaoliuzhu) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Role distillation system overview](artifact/README.md) <br>
- [AI-native strategy guide](artifact/guides/ai-native-strategy.md) <br>
- [Industry background guide](artifact/guides/industry-background.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands] <br>
**Output Format:** [Markdown reports, structured discussion summaries, labeled persona viewpoints, and optional shell command templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should preserve viewpoint-simulation labels and avoid presenting simulated persona content as real quotes or authorized positions.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
