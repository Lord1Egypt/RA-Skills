## Description: <br>
SocialVault helps OpenClaw agents acquire, encrypt, store, monitor, and refresh social-platform login sessions, including cookie import, session checks, adapter creation, and browser fingerprint management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2019-02-18](https://clawhub.ai/user/2019-02-18) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and developers use SocialVault to manage social-media account credentials for supported platforms, verify session health, refresh sessions, and load credentials into browser-based agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to provide live social-platform cookies or tokens and stores them for later reuse. <br>
Mitigation: Treat pasted cookies like passwords, use a dedicated low-risk account where possible, and revoke or log out sessions if credentials were pasted into the wrong place. <br>
Risk: The skill can reuse stored sessions for automated account actions and scheduled refreshes. <br>
Mitigation: Avoid write-capable tokens unless needed, disable or closely monitor automatic refresh, and confirm account activity remains within the user's intended platform usage. <br>


## Reference(s): <br>
- [ClawHub SocialVault listing](https://clawhub.ai/2019-02-18/social-vault) <br>
- [SocialVault README](artifact/README.md) <br>
- [Platform adapter specification](artifact/adapters/_spec.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration steps, status reports, and local file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or update encrypted vault files, account metadata, adapter files, browser profile settings, and session health reports.] <br>

## Skill Version(s): <br>
0.1.7 (source: server release metadata; artifact frontmatter and package.json report 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
