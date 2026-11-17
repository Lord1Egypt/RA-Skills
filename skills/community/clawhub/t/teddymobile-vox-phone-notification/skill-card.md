## Description:

Converts natural-language notification requests into TeddyMobile Vox phone notifications, beginning with no-credential dry-run parsing and then guiding users to limited trial calls or registered live setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ziliangzhu](https://clawhub.ai/user/ziliangzhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to turn a natural-language notification request into a TeddyMobile Vox outbound phone notification workflow. It supports masked dry-run parsing before registration and moves to trial or registered live calling only after recipient authorization and setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that dry-run analytics may send prompts, phone numbers, notification text, and run metadata to TeddyMobile analytics without clear disclosure.

Mitigation: Review before installing and set SKILL_ANALYTICS_DISABLED=1 unless analytics transmission is explicitly accepted.

Risk: Trial and live modes place real outbound phone calls and transmit recipient phone numbers and notification text to TeddyMobile Vox.

Mitigation: Use only recipient numbers the user is authorized to contact, require dry-run preview first, and require explicit confirmation before a real call.

Risk: Live mode depends on TeddyMobile credentials and outbound-number configuration.

Mitigation: Keep real credentials in environment variables, a secure local store, or a restricted local credentials file; do not paste or commit secrets.

Risk: The local trial-state file can retain trial history.

Mitigation: Treat the trial-state file as sensitive and remove it when trial history should not be retained.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ziliangzhu/skills/teddymobile-vox-phone-notification)
- [TeddyMobile Vox registration](https://vox-ai.teddymobile.cn/?utm_source=clawhub&utm_medium=skill&utm_campaign=vox-phone-notification)
- [TeddyMobile Vox outbound endpoint](https://vox.teddymobile.cn/vox/v2/outbound)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include masked dry-run parsing results, trial or live call setup steps, and local credential configuration guidance.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
