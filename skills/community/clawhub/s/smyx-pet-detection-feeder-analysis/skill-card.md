## Description: <br>
This skill analyzes feeder or IPC camera images and videos to detect cats and dogs, recognize pet identities, enroll pets, and retrieve cloud report history for smart feeding workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ClawHub users use this skill to run pet detection and identity recognition on feeder or IPC camera media, enroll pets into a recognition database, and retrieve cloud-hosted report history for smart feeding workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary reports handling of user identifiers, credentials, cloud uploads, report history, and token persistence without clear user-facing disclosure. <br>
Mitigation: Review before installing, use a purpose-limited open-id instead of an API key, username, or phone number, and check local token storage behavior before production use. <br>
Risk: Feeder or IPC camera media uploaded for analysis may contain people or private home context. <br>
Mitigation: Avoid uploading sensitive home camera footage unless the remote service and retention policy are trusted. <br>
Risk: The security verdict is suspicious and the dependency list may need review. <br>
Mitigation: Scan and validate dependencies and remote-service configuration before using the skill in a production workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/smyx-pet-detection-feeder-analysis) <br>
- [Pet detection API documentation](references/api_doc.md) <br>
- [Shared analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report text or JSON, with optional saved output file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an open-id and sends local files or public media URLs to a remote API; history output can include links to cloud report images.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; bundled frontmatter says 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
