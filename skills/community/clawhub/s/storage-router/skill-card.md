## Description: <br>
Decides where to save information across monday.com, local files, and MEMORY.md before any content is written. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netanel-abergel](https://clawhub.ai/user/netanel-abergel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill before saving research, documents, operational state, credentials, or memory so content is routed to monday.com, GitHub/private memory, or local files according to the owner's storage rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill routes content to external and persistent destinations, including monday.com and GitHub/private memory. <br>
Mitigation: Confirm the destination and get explicit approval before saving sensitive or business-critical content externally. <br>
Risk: The skill may load local .context values for monday.com workspace, folder, board, and document IDs. <br>
Mitigation: Use .context only when the file is trusted, and verify monday.com IDs against the Structure Index before saving new content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/netanel-abergel/storage-router) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with routing tables and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes saved content to monday.com, GitHub/private memory, or local files; does not itself execute storage operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
