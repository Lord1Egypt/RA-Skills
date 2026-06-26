## Description: <br>
Manage Trilium Notes by reading, searching, and creating notes via the ETAPI with a provided server URL and ETAPI token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mtbf999](https://clawhub.ai/user/mtbf999) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Trilium users use this skill to connect an agent to their Trilium database so it can search, read, and create notes with an ETAPI token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The ETAPI token can allow the agent to read and modify notes in the configured Trilium instance. <br>
Mitigation: Use a token with the least access you are comfortable granting for the connected Trilium instance. <br>
Risk: Important note-management requests could create, update, or delete content the user did not intend. <br>
Mitigation: Ask for confirmation before create, update, or delete operations when the requested change is important. <br>


## Reference(s): <br>
- [Trilium ETAPI Reference](references/api.md) <br>
- [Trilium ETAPI Wiki](https://github.com/zadam/trilium/wiki/Etapi) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Guidance] <br>
**Output Format:** [Markdown or plain text responses with Trilium note content handled through ETAPI requests.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TRILIUM_ETAPI_TOKEN and TRILIUM_SERVER_URL for Trilium access.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
