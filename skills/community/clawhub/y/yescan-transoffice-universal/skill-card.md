## Description:

Converts user-supplied images, screenshots, and scans into editable Word, Excel, or PDF files using Quark Scan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yescan-ai](https://clawhub.ai/user/yescan-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and operators use this skill to convert a single image, screenshot, or scan into an editable Office document or PDF while preserving layout where possible.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected images, scans, or screenshots are uploaded to Quark's third-party service for conversion.

Mitigation: Use the skill only for documents you are comfortable sending to that service, and avoid sensitive documents unless the service terms and data handling meet your requirements.

Risk: The SCAN_WEBSERVICE_KEY credential is required and could be exposed through misconfiguration or shared environments.

Mitigation: Store the key in the configured environment variable only, avoid pasting it into prompts or logs, and rotate it promptly if exposure is suspected.

Risk: Generated Word, Excel, or PDF files are saved under the system temporary directory and can persist after the session.

Mitigation: Inspect and remove generated files from the temp directory after use, especially on shared machines.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yescan-ai/skills/alibaba-quark-transoffice)
- [ClawHub Publisher Profile](https://clawhub.ai/user/yescan-ai)
- [Quark Scan Open Platform](https://scan.quark.cn/business)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, files, guidance]

**Output Format:** [JSON response with a local file path when conversion succeeds]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCAN_WEBSERVICE_KEY; accepts one image URL, local path, or base64 input; generated files are saved under the system temporary directory.]

## Skill Version(s):

1.1.19 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
