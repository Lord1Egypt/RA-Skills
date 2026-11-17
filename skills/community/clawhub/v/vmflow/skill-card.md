## Description:

Manage your vending machine fleet - send credits, inspect device health, query sales and inventory, and trigger firmware updates via MQTT RPC and Supabase.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nodestark](https://clawhub.ai/user/nodestark)

### License/Terms of Use:

MIT-0

## Use Case:

External fleet operators and developers use this skill to inspect vending machine sales, inventory, telemetry, and device health, and to issue authenticated Supabase and MQTT control actions for ESP32-based vending devices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can issue real-world fleet-control actions, including credits, restart, OOS recovery, buzzer, DEX, and OTA commands.

Mitigation: Require explicit human confirmation before sending credit, restart, OOS, buzzer, DEX, or OTA actions to devices.

Risk: Device passkeys and operator credentials enable authenticated Supabase and MQTT actions.

Mitigation: Use a dedicated low-privilege operator account, keep passkeys out of logs and shell history, and avoid passing passkeys directly on the command line.

Risk: MQTT transport configuration can affect command confidentiality and broker access control.

Mitigation: Configure MQTT with TLS and broker authentication before using the skill with real devices.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nodestark/skills/vmflow)
- [Project homepage](https://github.com/nodestark/mdb-esp32-cashless)
- [AGENTS.md](./AGENTS.md)
- [RPC helper script](./tools/rpc.sh)
- [Firmware RPC handler](https://github.com/nodestark/mdb-esp32-cashless/blob/main/mdb-slave-esp32s3/main/mdb-slave-esp32s3.c)
- [Supabase schema](https://github.com/nodestark/mdb-esp32-cashless/tree/main/docker/supabase/migrations)
- [VMflow dashboard](https://vmflow.xyz/dashboard)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, JSON, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Supabase REST calls, MQTT command payloads, fleet reports, device diagnostics, and operational playbooks.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
