## Description:

Control and automate Tuya Smart devices with official cloud APIs, secure request signing, region-aware routing, and safe command execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and smart-home operators use this skill to configure Tuya cloud access, discover device capabilities, build signed API requests, and execute or troubleshoot guarded device-control workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tuya Access ID, Access Secret, project tokens, device IDs, and command payloads can expose operational control data if mishandled.

Mitigation: Keep credentials in local environment variables, never paste production secrets into chat logs, avoid storing raw secrets in notes, and use least-privilege Tuya project permissions.

Risk: Device write operations can affect real-world devices, including high-impact classes such as locks, alarms, HVAC, heating controls, high-power switches, and bulk device cohorts.

Mitigation: Default to read-only inspection, discover capability schemas before command generation, require explicit confirmation before writes, use canary-first rollout, and verify state after each command.

Risk: Wrong regional endpoints, stale signatures, or mismatched account-linking assumptions can cause failed requests or operations against the wrong project context.

Mitigation: Confirm data center, project scope, app account model, timestamp, nonce, signed path, and body hash before API calls, then stop and reconcile account linkage when device lists disagree.

Risk: The local ~/tuya workspace may contain endpoint choices, device identifiers, command dictionaries, automation constraints, and incident details.

Mitigation: Store only Tuya-relevant non-secret notes, use restrictive local file permissions, and treat the workspace as an operational notebook that should not be shared casually.

## Reference(s):

- [Tuya Smart Skill on ClawHub](https://clawhub.ai/ivangdavila/skills/tuya)
- [Tuya Smart Skill Homepage](https://clawic.com/skills/tuya)
- [Tuya Developer Documentation](https://developer.tuya.com)
- [Tuya US OpenAPI Endpoint](https://openapi.tuyaus.com)
- [Tuya Europe OpenAPI Endpoint](https://openapi.tuyaeu.com)
- [Tuya China OpenAPI Endpoint](https://openapi.tuyacn.com)
- [Tuya India OpenAPI Endpoint](https://openapi.tuyain.com)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown guidance with inline shell commands, JSON request examples, and operational checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose signed Tuya API calls, local note structures, device command payloads, and guarded rollout plans.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
