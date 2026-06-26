## Description: <br>
Search, download, and upload files in a single Seafile library using a repo token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andrewreid](https://clawhub.ai/user/andrewreid) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to search, download, and upload files in a single Seafile library through repo-token API commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repo tokens grant access to a Seafile library, and commands can read, download, or upload files within that token's scope. <br>
Mitigation: Use a repo token limited to the intended library, verify the Seafile base URL, and run the repo-info check before search, download, or upload operations. <br>
Risk: Upload commands can overwrite existing files when replace=1 is used. <br>
Mitigation: Review upload commands before execution and prefer replace=0 unless overwriting the existing file is intended. <br>
Risk: Incorrect paths or server URLs can target the wrong library location or fail unexpectedly. <br>
Mitigation: Confirm SEAFILE_BASE_URL and absolute library paths before running generated curl commands. <br>


## Reference(s): <br>
- [Seafile Repo-Token API Notes](references/seafile-api.md) <br>
- [Command Patterns](references/command-patterns.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/andrewreid/seafile) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON-processing examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, SEAFILE_BASE_URL, and SEAFILE_REPO_TOKEN; optional SEAFILE_LIBRARY_ROOT and SEAFILE_OUTPUT_DIR.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
