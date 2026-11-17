## Description: <br>
智能灯控(免费版) helps an agent guide and execute local-network commands for a single compatible TP-Link Kasa smart bulb, including power, brightness, HSV color, color temperature, discovery, and status operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to control or prototype automation for one local-network TP-Link Kasa smart bulb without a cloud account. It is suited for basic on/off, brightness, color, discovery, and status workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary flags unrelated trigger wording that could make the skill activate for data-analysis or reporting requests. <br>
Mitigation: Narrow the trigger to smart-light tasks only before automatic use. <br>
Risk: The skill can lead an agent to run local-network smart-light commands. <br>
Mitigation: Confirm the target bulb IP and requested light change before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/smart-light-controller-free) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with bash command snippets and JSON result examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.11+, python-kasa, uv, and local-network access to a compatible TP-Link Kasa bulb.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
