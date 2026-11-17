## Description:

Query and monitor UniFi network via local gateway API (Cloud Gateway Ultra / UniFi OS).

This skill is ready for commercial/non-commercial use.

## Publisher:

[ricanwarfare](https://clawhub.ai/user/ricanwarfare)

### License/Terms of Use:

MIT-0

## Use Case:

Network operators and technical users use this skill to check UniFi gateway health, connected devices, active clients, DPI traffic, and recent alerts from a local UniFi OS deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill accesses sensitive UniFi gateway credentials and network inventory.

Mitigation: Use a dedicated local read-only account, restrict credentials file permissions, and avoid sharing raw command output.

Risk: The scripts disable TLS verification for local gateway requests.

Mitigation: Run the skill only against a trusted local gateway and verify the configured host before use.

Risk: The dashboard script writes a local debug dump containing network inventory.

Mitigation: Protect the working directory and delete dashboard_debug_dump.json when it is no longer needed.

## Reference(s):

- [UniFi Local Gateway Read-Only API Calls](references/unifi-readonly-endpoints.md)
- [Community UniFi Controller API Reference](https://ubntwiki.com/products/software/unifi-controller/api)
- [ClawHub Skill Page](https://clawhub.ai/ricanwarfare/skills/unifi-network)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON]

**Output Format:** [Human-readable terminal tables, Markdown guidance, shell commands, and optional raw JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq, network access to a local UniFi gateway, and a local credentials file.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
