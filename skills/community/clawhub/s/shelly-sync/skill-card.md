## Description:

Monitor real-time power consumption from Shelly Pro 3EM and control local appliances/automation based on solar yield or grid usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcbuer](https://clawhub.ai/user/jcbuer)

### License/Terms of Use:

MIT-0

## Use Case:

External users and home automation developers use this skill to check Shelly Pro 3EM power readings and decide whether surplus solar energy can be used by local appliances.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use Home Assistant credentials and may change appliance state when target_load is supplied.

Mitigation: Use a dedicated, minimally privileged Home Assistant token and only map appliances that are safe to turn on automatically.

Risk: Network calls are directed at local Shelly and Home Assistant endpoints.

Mitigation: Point SHELLY_EM_IP and HOME_ASSISTANT_URL only at trusted local endpoints, preferably over HTTPS or a trusted private network.

Risk: The security review notes under-disclosed Home Assistant credential use and limited safety controls.

Mitigation: Review the skill before installation and avoid target_load unless automatic activation of the mapped appliance is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jcbuer/skills/shelly-sync)
- [Publisher Profile](https://clawhub.ai/user/jcbuer)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON responses and concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call local Shelly and Home Assistant APIs when configured.]

## Skill Version(s):

1.0.1 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
