## Description: <br>
Writes, updates, and reads OpenNote notes through the public API for publishing notes, uploading note images, managing labels, and looking up previously written notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liam-duan](https://clawhub.ai/user/liam-duan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create, update, read, and organize OpenNote notes through the public API, including labels, images, stickers, and local note history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an OpenNote API token that may grant access to create, update, upload images for, or read notes depending on token scopes. <br>
Mitigation: Use the minimum token scopes needed, revoke unused or compromised tokens, and store OPENNOTE_API_TOKEN as a private secret. <br>
Risk: Local .opennote cache and history files may reveal note titles, labels, image names, and short content previews. <br>
Mitigation: Treat .opennote files as private local data and avoid committing or sharing them. <br>


## Reference(s): <br>
- [OpenNote](https://opennote.cc) <br>
- [OpenNote App Store Listing](https://apps.apple.com/app/opennote-notes-journal/id6450187057) <br>
- [OpenNote API Base](https://api.opennote.cc/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON, Text] <br>
**Output Format:** [Markdown guidance with curl commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses OPENNOTE_API_TOKEN and local .opennote cache/history files when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
