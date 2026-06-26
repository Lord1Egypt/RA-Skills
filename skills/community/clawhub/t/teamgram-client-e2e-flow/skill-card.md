## Description: <br>
Documents the KHF Android client architecture and complete end-to-end data flows for login, messaging, and file operations through all Teamgram Server layers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhihang9978](https://clawhub.ai/user/zhihang9978) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers working with Teamgram Server use this knowledge skill to understand KHF Android client compatibility requirements, login flow, messaging flow, file transfer flow, service routing, and common troubleshooting paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes guidance for bypassing Teamgram enterprise feature locks. <br>
Mitigation: Use that section only in authorized development, audit, or licensing contexts; prefer legitimate licensing, configuration, or vendor-supported enablement paths for enterprise-gated features. <br>
Risk: Incorrect compatibility values for MTProto layer, API ID, API hash, or TL schema can lead to failed client-server communication. <br>
Mitigation: Verify client constants against the deployed Teamgram Server configuration before applying the guidance. <br>
Risk: Troubleshooting guidance can become stale as Teamgram Server handlers, routing, or service paths change. <br>
Mitigation: Check the referenced Teamgram Server source and deployment configuration before making operational changes. <br>


## Reference(s): <br>
- [Teamgram Client E2E Flow on ClawHub](https://clawhub.ai/zhihang9978/teamgram-client-e2e-flow) <br>
- [Publisher profile](https://clawhub.ai/user/zhihang9978) <br>
- [Teamgram Server repository](https://github.com/teamgram/teamgram-server) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown reference material with text flow diagrams, code paths, compatibility notes, and troubleshooting tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only output; no executable code, network calls, or credential handling are provided by the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
