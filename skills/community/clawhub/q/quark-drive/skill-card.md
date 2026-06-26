## Description: <br>
Quark helps an agent manage Quark Drive files with login, listing, search, upload, download, sharing, transfer-save, delete, clear, folder creation, and batch upload workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imeiming](https://clawhub.ai/user/imeiming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate a Quark Drive account from shell commands, including authenticated file management, sharing, transfer-save, and batch upload tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Quark Drive account cookies and can save them in a local config file. <br>
Mitigation: Protect QUARK_COOKIE and the saved config file like passwords, and install the skill only for accounts you are comfortable granting this level of access. <br>
Risk: Delete, clear, download, and upload commands can affect broad cloud or local paths. <br>
Mitigation: Review exact paths before running destructive or broad file commands, and avoid uploading hidden or agent directories such as ~/.hermes. <br>
Risk: Share commands can create public or long-lived access to files. <br>
Mitigation: Prefer short-lived password-protected shares over public or permanent links. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/imeiming/quark-drive) <br>
- [Quark Drive authentication reference](references/auth.md) <br>
- [Quark Drive sharing and transfer-save API reference](references/share-api.md) <br>
- [Quark Drive upload API reference](references/upload-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local Quark CLI configuration and may produce share links, file listings, download paths, and upload progress output.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
