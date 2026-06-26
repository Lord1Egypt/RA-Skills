## Description: <br>
AList file management API for OpenClaw that supports upload, download, list, mkdir, rm, mv, search, and offline download operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leeshunee](https://clawhub.ai/user/leeshunee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage files on an AList cloud storage server through agent-guided CLI commands for authentication, listing, upload, download, folder creation, removal, moves, and search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects to an AList account using URL, username, and password settings. <br>
Mitigation: Store credentials in a trusted secret mechanism and prefer least-privilege AList credentials. <br>
Risk: Upload, move, and delete operations can affect remote storage paths. <br>
Mitigation: Verify remote paths and requested operations before executing file-changing commands. <br>
Risk: The artifact references a helper CLI script that is not included in the package. <br>
Mitigation: Review the actual CLI implementation before using the skill with real storage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leeshunee/test-502) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include destructive file-management commands that should be reviewed before execution.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
