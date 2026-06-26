## Description: <br>
Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parker-xferops](https://clawhub.ai/user/parker-xferops) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to set up and run gog commands for Google Workspace tasks across Gmail, Calendar, Drive, Contacts, Sheets, and Docs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing and authorizing the external gog CLI can grant broad access to Google Workspace account data. <br>
Mitigation: Install only if the external CLI and Homebrew tap are trusted, and review Google OAuth scopes before approving access. <br>
Risk: Commands can send email or change Calendar, Drive, Docs, Contacts, or Sheets data. <br>
Mitigation: Confirm intent before running mutating commands, especially mail sending, event creation, file changes, and spreadsheet updates. <br>
Risk: Putting GOG_KEYRING_PASSWORD directly in shell profiles or service environment lines can expose credentials. <br>
Mitigation: Use the narrowest practical account and avoid storing the keyring password directly in shell profiles or systemd Environment lines. <br>


## Reference(s): <br>
- [gog CLI homepage](https://gogcli.sh) <br>
- [ClawHub skill page](https://clawhub.ai/parker-xferops/xferops-gog) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gog CLI and Google OAuth setup.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
