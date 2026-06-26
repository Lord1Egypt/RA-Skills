## Description: <br>
Safely publish skills to ClawHub by sanitizing, formatting, verifying, and publishing without modifying local source files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and skill authors use this skill to turn existing local instructions or knowledge into a sanitized, publish-ready ClawHub skill. It guides transformation, review, explicit approval, and final publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prepared public skill content could expose personal data, credentials, internal references, or unsafe commands if not reviewed. <br>
Mitigation: Run the sanitization checklist and inspect the publish folder, file list, and sanitized content before approving publication. <br>
Risk: A publish command can create a public release with an incorrect slug, name, version, description, or file set. <br>
Mitigation: Require explicit user approval of the exact release metadata and files, then run the ClawHub CLI only in a trusted environment. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a separate publish-ready skill folder and approval checklist before any publish command is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
