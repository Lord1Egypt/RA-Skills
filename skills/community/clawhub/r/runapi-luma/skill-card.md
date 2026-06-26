## Description: <br>
Generate and edit video with Luma through RunAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runapi-ai](https://clawhub.ai/user/runapi-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to create, edit, or transform video with Luma through RunAPI. The skill is suited for one-off CLI-driven video tasks and for identifying when SDK integration is the better path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, request JSON, task metadata, and input media may be sent to RunAPI/Luma for video generation or editing. <br>
Mitigation: Avoid submitting confidential, regulated, private, or copyrighted media unless the user has permission and accepts the provider's retention and data-use policies. <br>
Risk: RunAPI authentication through RUNAPI_API_KEY, CLI login, or saved CLI configuration grants access to the user's RunAPI account. <br>
Mitigation: Use only user-approved credentials, avoid exposing tokens in logs or generated files, and prefer scoped or disposable keys where available. <br>


## Reference(s): <br>
- [RunAPI Luma model documentation](https://runapi.ai/models/luma.md) <br>
- [RunAPI Luma homepage](https://runapi.ai/models/luma) <br>
- [RunAPI Luma provider comparison](https://runapi.ai/providers/luma.md) <br>
- [RunAPI model catalog](https://runapi.ai/models.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include request JSON guidance and RunAPI task identifiers when an agent executes CLI workflows.] <br>

## Skill Version(s): <br>
0.2.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
