## Description: <br>
Tencent IMA Skill Publish helps agents work with Tencent IMA notes and knowledge bases, including searching, browsing, creating notes, adding URLs, and uploading files through the IMA OpenAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wat2012](https://clawhub.ai/user/wat2012) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to connect an agent to Tencent IMA for note and knowledge-base workflows, including credential-aware API calls, content search, note creation or editing, URL ingestion, and file uploads. It is most useful when users want the agent to operate on their IMA workspace while preserving documented write-operation checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access or modify Tencent IMA notes, knowledge bases, uploaded files, and URLs when credentials are available. <br>
Mitigation: Install only when that access is intended, keep credentials in protected secret or environment storage, and confirm sensitive write operations before execution. <br>
Risk: Security evidence flags under-scoped credential, routing, and unofficial automation guidance, including optional alternate base URL and cookie or Playwright probing paths. <br>
Mitigation: Use the official IMA endpoint by default, avoid setting IMA_BASE_URL unless the destination is trusted, and reserve cookie, Playwright, or undocumented endpoint probing for isolated test accounts. <br>
Risk: File uploads and note writes can create duplicate, misplaced, or hard-to-remove content in IMA. <br>
Mitigation: Follow the documented preflight checks, folder validation, duplicate-name checks, and post-upload validation before and after write operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wat2012/tencent-ima-hermes) <br>
- [Tencent IMA homepage](https://ima.qq.com) <br>
- [Tencent IMA agent interface](https://ima.qq.com/agent-interface) <br>
- [Official IMA OpenAPI skill package](https://app-dl.ima.qq.com/skills/ima-skills-1.1.7.zip) <br>
- [IMA write flow reference](references/ima-write-flow.md) <br>
- [Official endpoint coverage](references/official-endpoint-coverage.md) <br>
- [Post-upload validation reference](references/post-upload-validation.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON, markdown] <br>
**Output Format:** [Markdown guidance with shell commands, configuration notes, and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or execute IMA API workflows that require user-provisioned IMA OpenAPI credentials and may affect notes or knowledge-base contents.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
