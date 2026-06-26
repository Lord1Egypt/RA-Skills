## Description: <br>
Connects an agent to Puzle Read so users can save URLs, uploaded files, and pre-fetched content to a searchable reading library and work with saved readings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zinklu](https://clawhub.ai/user/zinklu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to add articles, files, and extracted page content to a Puzle reading library, then list, retrieve, search, summarize, or analyze those readings through the agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill's broad activation rules could send links, files, pasted text, or protected content to Puzle when the user has not clearly chosen that action. <br>
Mitigation: Require explicit user confirmation before uploading files, pasted text, private links, internal documents, or authenticated-browser content. <br>
Risk: Uploaded files and extracted content are processed by the Puzle service. <br>
Mitigation: Review Puzle's privacy and retention terms before using the skill with sensitive, confidential, or regulated material. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zinklu/puzle-read) <br>
- [Puzle Read homepage](https://read-web.puzle.com.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with Python and shell snippets; CLI data commands return JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a local Puzle token configuration and send user-selected URLs, files, or content to the Puzle service.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
