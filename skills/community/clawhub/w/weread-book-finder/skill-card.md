## Description: <br>
Searches WeRead for a requested book and adds confident matches to the user's shelf, falling back to Z-Library search and non-PDF download when WeRead is unavailable or has no reliable match. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinntrance](https://clawhub.ai/user/jinntrance) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to satisfy requests such as adding a named book to WeRead, with a disclosed fallback that searches Z-Library and downloads an ebook when WeRead cannot add a reliable match. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automates logged-in WeRead and Z-Library browser sessions, which can expose account state through the reused browser profile. <br>
Mitigation: Use a dedicated browser profile for this skill and avoid sharing that profile with unrelated browsing. <br>
Risk: The Z-Library fallback may raise copyright or terms-of-use concerns depending on the requested book and user context. <br>
Mitigation: Use the fallback only when it is lawful and appropriate for the user's situation. <br>
Risk: Downloaded ebook files may be unsafe or untrusted. <br>
Mitigation: Inspect or scan downloaded ebook files before opening them. <br>


## Reference(s): <br>
- [WeRead](https://weread.qq.com/) <br>
- [Z-Library](https://z-lib.by/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON status from the script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create downloaded ebook files under ~/Downloads/OpenClaw-Books and reuse a local browser profile.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
