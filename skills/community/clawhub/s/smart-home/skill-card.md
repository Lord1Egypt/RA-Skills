## Description:

Set up, automate, secure, and troubleshoot smart home devices with protocol selection, network isolation, and ecosystem-agnostic automation patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users and smart-home operators use this skill to choose device protocols, set up hubs, plan renter-friendly deployments, create automations, and troubleshoot or secure smart-home systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Presence-based automation could weaken alarm safety if geofencing, phone presence, or motion timeout alone is allowed to disarm alarms.

Mitigation: Require explicit confirmation or an authenticated local action before disarming alarms, and test automations with realistic household scenarios.

Risk: Device reset or takeover workflows could erase camera or doorbell history needed for disputes, incidents, warranty support, or law enforcement.

Mitigation: Review and export needed footage or history before clearing recordings, removing accounts, or factory resetting devices.

## Reference(s):

- [Smart Home skill page](https://clawhub.ai/ivangdavila/skills/smart-home)
- [setup.md](artifact/setup.md)
- [automations.md](artifact/automations.md)
- [security.md](artifact/security.md)
- [troubleshooting.md](artifact/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown guidance with tables and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
