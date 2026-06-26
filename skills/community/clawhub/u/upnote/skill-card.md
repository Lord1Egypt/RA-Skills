## Description: <br>
Manage UpNote notes and notebooks via x-callback-url automation for creating notes, opening notes, creating notebooks, viewing tags, and managing content in UpNote. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wemcdonald](https://clawhub.ai/user/wemcdonald) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to automate local UpNote note, notebook, tag, filter, and search operations through a shell wrapper for UpNote x-callback-url commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create persistent content in the user's local UpNote app. <br>
Mitigation: Review note titles, note content, notebook targets, and create actions before approving commands. <br>
Risk: Search and open requests may expose or navigate to local note content in UpNote. <br>
Mitigation: Confirm note IDs, notebook IDs, tag names, and search terms before running commands. <br>


## Reference(s): <br>
- [ClawHub UpNote skill page](https://clawhub.ai/wemcdonald/upnote) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands open the local UpNote app and may create persistent notes or notebooks.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
