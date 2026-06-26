## Description: <br>
Generate and edit video with Seedance through RunAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runapi-ai](https://clawhub.ai/user/runapi-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create, edit, or transform video with Seedance through RunAPI, using the RunAPI CLI for one-off tasks and SDKs for application integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, request JSON, and uploaded inputs are sent to RunAPI for video generation. <br>
Mitigation: Review inputs before submission and use a RunAPI account or API key with intended permissions and spending limits. <br>
Risk: The skill depends on the external runapi CLI and authentication state. <br>
Mitigation: Install the documented runapi binary and authenticate with runapi login, saved CLI configuration, or RUNAPI_API_KEY before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/runapi-ai/runapi-seedance) <br>
- [RunAPI Seedance model](https://runapi.ai/models/seedance) <br>
- [RunAPI Seedance model documentation](https://runapi.ai/models/seedance.md) <br>
- [RunAPI Bytedance provider documentation](https://runapi.ai/providers/bytedance.md) <br>
- [RunAPI model catalog](https://runapi.ai/models.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline shell commands and SDK package names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference request JSON for RunAPI CLI calls and SDK integration choices.] <br>

## Skill Version(s): <br>
0.2.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
