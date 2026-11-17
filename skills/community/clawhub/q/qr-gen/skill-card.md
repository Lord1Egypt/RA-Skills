## Description:

Generates QR codes from text, URLs, WiFi credentials, vCards, or arbitrary data, with PNG, SVG, or ASCII output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[claudiodrusus](https://clawhub.ai/user/claudiodrusus)

### License/Terms of Use:


## Use Case:

Developers and end users can use this skill when they need an agent to create scannable QR codes for links, text payloads, WiFi login details, or contact cards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script automatically installs an unpinned Python dependency at runtime if qrcode[pil] is missing.

Mitigation: Use an isolated or controlled Python environment and preinstall a pinned qrcode[pil] dependency before running the skill.

Risk: WiFi passwords can be provided as command-line arguments, which may expose them through shell history or local process inspection.

Mitigation: Avoid using real WiFi passwords on shared systems; clear command history and run only in trusted local environments when credentials are necessary.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/claudiodrusus/skills/qr-gen)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Text]

**Output Format:** [PNG, SVG, or ASCII QR code output with shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports text, URL, WiFi, and vCard payloads with configurable size, border, format, and error correction level.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
