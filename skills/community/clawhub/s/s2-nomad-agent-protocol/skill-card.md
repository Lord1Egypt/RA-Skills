## Description: <br>
Instructs the OpenClaw agent on how to request geolocation, claim P-SSSU Habitable Slots with user consent, and negotiate boundaries with other agents in the outdoor environment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spacesq](https://clawhub.ai/user/spacesq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to guide an OpenClaw agent through consent-based outdoor geolocation, P-SSSU slot claiming, and boundary negotiation. It is intended to keep spatial actions transparent and advisory unless additional authorization is granted. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests sensitive geolocation and environmental-sensor access. <br>
Mitigation: Run it only in an environment that prompts before location reads, claim actions, expansion radius changes, and priority-based override decisions. <br>
Risk: Grid claiming and boundary negotiation may be mistaken for authorization to intervene in physical systems. <br>
Mitigation: Treat outputs as advisory unless the user and any required building-management or public-hardware authority grants additional authorization. <br>
Risk: The handler relies on the agent or runtime to enforce consent checks. <br>
Mitigation: Require explicit human-in-the-loop approval before invoking location-related tools or executing outdoor takeover actions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/spacesq/s2-nomad-agent-protocol) <br>
- [Publisher profile](https://clawhub.ai/user/spacesq) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown instructions, plugin configuration, shell entrypoint, and JSON tool-call results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user or system authorization before location reads, grid claiming, expansion actions, or priority-based override decisions.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence, SKILL.md frontmatter, package.json, openclaw.plugin.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
