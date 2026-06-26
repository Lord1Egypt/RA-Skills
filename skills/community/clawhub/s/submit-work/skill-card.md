## Description: <br>
Submit Work guides an agent through uploading deliverables and submitting completed task work to OpenAnt with text, media keys, proof URLs, or proof hashes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ant-1984](https://clawhub.ai/user/ant-1984) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent workers use this skill after completing an OpenAnt task to identify deliverables, upload files, submit text or proof links, and check or withdraw a recent submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send task text and generated files to OpenAnt without final user confirmation. <br>
Mitigation: Use explicit submission wording, review deliverables before upload where possible, and avoid use in workspaces that may contain sensitive or unrelated artifacts. <br>
Risk: A text-only submission may omit expected deliverable files. <br>
Mitigation: Review produced files before submission and upload required deliverables before passing media keys to the submit command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ant-1984/submit-work) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON-oriented CLI outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May upload files and submit task text, media keys, proof URLs, or proof hashes to OpenAnt.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
