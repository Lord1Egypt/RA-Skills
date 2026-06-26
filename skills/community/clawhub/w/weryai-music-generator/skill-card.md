## Description: <br>
Generate WeryAI music, vocal songs, or instrumental tracks through the WeryAI music API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weryai-developer](https://clawhub.ai/user/weryai-developer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to prepare and submit WeryAI music generation requests, check account balance, poll existing tasks, and return generated audio links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled podcast API code is present even though the release is presented as a music generation skill. <br>
Mitigation: Review the bundled scripts before installation and limit use to the documented music entrypoints unless the extra modules are separately disclosed and accepted. <br>
Risk: Local reference_audio paths can result in local files being uploaded to WeryAI. <br>
Mitigation: Pass local file paths only when the user intentionally wants that file uploaded; otherwise use public http or https reference audio URLs. <br>
Risk: WERYAI_BASE_URL can redirect API calls to a non-default host. <br>
Mitigation: Use the default WeryAI API host or set WERYAI_BASE_URL only to a host the operator controls and trusts. <br>
Risk: Real submit and wait runs can consume paid WeryAI credits and are not idempotent. <br>
Mitigation: Use dry-run previews and explicit confirmation before paid submission, and use status checks for existing task IDs instead of submitting again. <br>


## Reference(s): <br>
- [WeryAI Music API Reference](references/api-music.md) <br>
- [WeryAI Music Error Codes](references/error-codes.md) <br>
- [ClawHub WeryAI Music Generator Listing](https://clawhub.ai/weryai-developer/weryai-music-generator) <br>
- [WeryAI API Keys](https://www.weryai.com/api/keys) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, JSON] <br>
**Output Format:** [Markdown guidance with JSON command results and generated audio links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Paid WeryAI API submissions are possible; dry-run output is available before real generation.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
