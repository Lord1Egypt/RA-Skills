## Description: <br>
Generate and edit images with Flux Kontext through RunAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runapi-ai](https://clawhub.ai/user/runapi-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to route Flux Kontext image generation and editing requests through RunAPI, choosing CLI commands for one-off tasks and SDK packages for application integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the third-party RunAPI CLI and Homebrew tap, and prompts or image inputs are sent to RunAPI. <br>
Mitigation: Install only after trusting the RunAPI CLI and tap; review RunAPI pricing and data handling before use. <br>
Risk: Authentication may use RUNAPI_API_KEY or saved RunAPI CLI credentials. <br>
Mitigation: Use a scoped API key when possible and avoid exposing credentials in shared logs, prompts, or files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/runapi-ai/runapi-flux-kontext) <br>
- [RunAPI Flux Kontext model overview](https://runapi.ai/models/flux-kontext) <br>
- [RunAPI Flux Kontext documentation](https://runapi.ai/models/flux-kontext.md) <br>
- [RunAPI Black Forest Labs provider comparison](https://runapi.ai/providers/black-forest-labs.md) <br>
- [RunAPI model catalog](https://runapi.ai/models.md) <br>
- [Flux Kontext Pro variant](https://runapi.ai/models/flux-kontext/pro.md) <br>
- [Flux Kontext Max variant](https://runapi.ai/models/flux-kontext/max.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline shell commands and SDK package names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the runapi CLI for the CLI path; RUNAPI_API_KEY, runapi login, or saved CLI configuration can authenticate requests.] <br>

## Skill Version(s): <br>
0.2.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
