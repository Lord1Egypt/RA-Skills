## Description: <br>
Publishes selected files or folders to Qutke static hosting and returns a public {slug}.on.qutke.cn URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haio](https://clawhub.ai/user/haio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to publish static sites, individual files, media, PDFs, and generated web artifacts to a shareable Qutke URL. It supports anonymous 24-hour publishes and account-backed permanent publishes when an API key is configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing targets may contain secrets, private files, or unintended content. <br>
Mitigation: Review the selected files or folders before publishing and avoid uploading credentials, private data, or unrelated workspace contents. <br>
Risk: API keys, claim tokens, and local publish state are sensitive and can grant access to published sites. <br>
Mitigation: Use the credential file or environment variable flow, keep ~/.onqutke/credentials and .onqutke/state.json out of version control, and share claim URLs only with intended recipients. <br>
Risk: Anonymous publishes expire after 24 hours unless claimed. <br>
Mitigation: Tell users when a publish is anonymous, provide the claim URL when available, and recommend authenticated publishing for permanent account-backed sites. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/haio/publish-on-qutke) <br>
- [Qutke API reference](artifact/references/REFERENCE.md) <br>
- [Qutke service](https://on.qutke.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and published URL text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs the current site URL and publish_result stderr fields; anonymous publishes may also include a claim URL and expiration details.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
