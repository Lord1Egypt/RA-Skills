## Description: <br>
Skill Proposal Gen helps create and export structured proposal drafts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zimuge-doudou](https://clawhub.ai/user/zimuge-doudou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create, update, list, export, and generate proposal documents for events, cultural tourism, meetings, and exhibitions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted project names can cause JSON or Markdown reads and writes outside the intended proposals folder. <br>
Mitigation: Validate project names to reject slashes, backslashes, absolute paths, and '..', and force all file access to remain inside the proposals folder. <br>
Risk: The skill stores generated proposal content locally. <br>
Mitigation: Review local storage handling before using sensitive proposal data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zimuge-doudou/skill-proposal-gen) <br>
- [Publisher profile](https://clawhub.ai/user/zimuge-doudou) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, files] <br>
**Output Format:** [Command-line text plus generated JSON and Markdown proposal files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Proposal content is stored locally in the skill's proposals folder.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
