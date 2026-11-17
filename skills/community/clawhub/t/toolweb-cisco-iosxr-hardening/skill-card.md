## Description:

Generate security hardening configurations for Cisco IOS XR devices with customizable hardening options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Network engineers, security teams, and infrastructure automation developers use this skill to generate reviewable Cisco IOS XR hardening configurations from selected security options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends hardening options and session metadata to a disclosed external API.

Mitigation: Install only when use of the external API is acceptable for the intended environment and data handling requirements.

Risk: Generated network device configurations can disrupt production devices if applied without review.

Mitigation: Treat generated configurations as drafts, review them with a network engineer, test them in a lab or staged environment, back up current device configurations, and prepare a rollback plan before deployment.

## Reference(s):

- [Cisco IOS XR Hardening API Route](https://api.mkkpro.com/hardening/cisco-iosxr)
- [Cisco IOS XR Hardening API Docs](https://api.mkkpro.com:8138/docs)

## Skill Output:

**Output Type(s):** [configuration, guidance, text]

**Output Format:** [JSON response containing generated Cisco IOS XR configuration sections, applied options, status, timestamps, and warnings when present.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated configurations should be reviewed, tested in a lab or staged environment, backed up, and paired with a rollback plan before production deployment.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
