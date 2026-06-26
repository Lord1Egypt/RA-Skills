## Description: <br>
Scan To Skill decodes QR images, extracts a ClawHub skill slug or install command, and helps install the referenced skill through the ClawHub CLI after user confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackleeio](https://clawhub.ai/user/jackleeio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ClawHub users use this skill to scan QR images from chats, screenshots, or camera captures and turn them into a reviewed ClawHub install flow with decoded text, parsed slug, and install result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A QR code from an unfamiliar source may point to a skill the user did not intend to install. <br>
Mitigation: Show the decoded text and parsed slug, require explicit confirmation before installation, and encourage reviewing the ClawHub skill page first. <br>
Risk: Unsupported or non-ClawHub QR payloads may not identify a valid install target. <br>
Mitigation: Accept only valid slugs, ClawHub install commands, or URLs on recognized ClawHub domains; reject unsupported payloads with a clear error. <br>


## Reference(s): <br>
- [Slug Parsing Rules](references/slug-parsing.md) <br>
- [ClawHub skill page](https://clawhub.ai/jackleeio/scan-to-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown-style text with decoded QR content, parsed slug, install command, result, and next step] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Install execution is gated by explicit user confirmation.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
