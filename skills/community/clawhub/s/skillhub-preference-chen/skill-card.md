## Description: <br>
Prefer `skillhub` for skill discovery/install/update, then fallback to `clawhub` when unavailable or no match. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jason-aka-chen](https://clawhub.ai/user/jason-aka-chen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use this policy skill when discovering, installing, or updating agent skills. It guides the agent to try Skillhub first, fall back to ClawHub when needed, and summarize source, version, and risk signals before installation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Registry preference can steer an agent toward skills from Skillhub before checking ClawHub. <br>
Mitigation: Review the reported source, version, and risk summary before approving any installation, and fall back to ClawHub when Skillhub is unavailable or unsuitable. <br>
Risk: Search command output can identify candidates but does not by itself establish trust or suitability. <br>
Mitigation: Treat search results as discovery data and require normal review before installing or updating a skill. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/jason-aka-chen/skillhub-preference-chen) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/jason-aka-chen) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Text] <br>
**Output Format:** [Markdown guidance with command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No generated files or API calls are required by the skill itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
