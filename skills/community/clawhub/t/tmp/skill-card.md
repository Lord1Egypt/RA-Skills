## Description: <br>
Google Workspace CLI guidance for Gmail, Calendar, Drive, Contacts, Sheets, Docs, and related Google services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jambo-Jet-Love](https://clawhub.ai/user/Jambo-Jet-Love) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to configure and run the gog CLI for Google Workspace tasks such as email, calendar, drive, contacts, sheets, and docs automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI can request broad Google Workspace authority beyond the root description. <br>
Mitigation: Review required services before installation and prefer explicit --services, --readonly, or narrower Drive scopes where possible. <br>
Risk: Email tracking behavior can raise privacy or compliance concerns. <br>
Mitigation: Avoid enabling email tracking unless it is approved for the workspace and clearly understood by users. <br>
Risk: Docs or Slides image import flows may temporarily make local images publicly readable. <br>
Mitigation: Review those flows before use and avoid processing sensitive local images through them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Jambo-Jet-Love/tmp) <br>
- [gog homepage](https://gogcli.sh) <br>
- [gog CLI README](artifact/gmail/gogcli/README.md) <br>
- [gog CLI command specification](artifact/gmail/gogcli/docs/spec.md) <br>
- [Email tracking documentation](artifact/gmail/gogcli/docs/email-tracking.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs emphasize OAuth setup, CLI invocation, and optional JSON output flags.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
