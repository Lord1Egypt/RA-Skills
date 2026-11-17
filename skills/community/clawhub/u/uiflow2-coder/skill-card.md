## Description:

UIFlow2 MicroPython coding assistant for writing, debugging, reviewing, and explaining code for M5Stack devices using bundled official UIFlow2 documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyun2000](https://clawhub.ai/user/yuyun2000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to produce UIFlow2 MicroPython code for M5Stack devices, select documented APIs, and troubleshoot runtime or hardware-integration issues. It is intended to keep generated code grounded in the bundled UIFlow2 docs and curated examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated or copied examples may contact network services or use device features when a user chooses to run them.

Mitigation: Review endpoints and device actions before execution, and run examples only on intended M5Stack hardware with expected connectivity.

Risk: Network examples may expose public IP location data or use public unauthenticated MQTT topics if copied without changes.

Mitigation: Disable IP geolocation when it is not intended, avoid public unauthenticated MQTT for real data, and provide Wi-Fi or service credentials only deliberately.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuyun2000/skills/uiflow2-coder)
- [UIFlow2 get started overview](artifact/docs/get-started/_overview.md)
- [M5UI overview](artifact/docs/m5ui/_overview.md)
- [Widgets overview](artifact/docs/widgets/_overview.md)
- [Curated UIFlow2 examples](artifact/references/complex-examples.md)

## Skill Output:

**Output Type(s):** [Code, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with UIFlow2 MicroPython code blocks and concise verification steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include device-specific assumptions, referenced documentation paths, and minimal hardware validation steps.]

## Skill Version(s):

1.0.13 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
