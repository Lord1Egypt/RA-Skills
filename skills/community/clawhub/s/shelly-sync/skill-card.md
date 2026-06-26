## Description: <br>
Monitor real-time power consumption from Shelly Pro 3EM and control local appliances/automation based on solar yield or grid usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcbuer](https://clawhub.ai/user/jcbuer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Home energy users and automation developers use this skill to read Shelly Pro 3EM power metrics and decide whether to trigger configured local appliance loads when solar surplus is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control real appliances through Home Assistant, including high-load devices, with limited safety gating. <br>
Mitigation: Review before installing, configure only the intended Home Assistant entities, use the narrowest possible token permissions, and treat optimize_load as capable of switching appliances on immediately. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jcbuer/shelly-sync) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration] <br>
**Output Format:** [JSON status objects with Markdown command examples and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SHELLY_EM_IP; Home Assistant control also depends on local Home Assistant URL and token configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
