## Description: <br>
Routes #kb-tagged content into a unified knowledge base by extracting supported inputs, uploading them to IMA, archiving them locally, and recording a memory entry. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sundmop](https://clawhub.ai/user/sundmop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Knowledge workers and agents use this skill to capture #kb-tagged WeChat articles, web pages, YouTube transcripts, plain text, and local files into IMA and a local workspace knowledge archive. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload arbitrary #kb content, local files, and extracted transcripts to IMA and retain copies in a local workspace archive. <br>
Mitigation: Use it only for content approved for the configured IMA knowledge base; exclude secrets, private keys, customer data, and sensitive documents unless retention and deletion expectations are confirmed. <br>
Risk: YouTube subtitle handling relies on a browser cookie file at a fixed temporary path. <br>
Mitigation: Use a low-risk account, restrict cookie file permissions, and delete the cookie file after processing. <br>
Risk: The helper depends on a preconfigured IMA knowledge-base ID, credential file, and local workspace paths. <br>
Mitigation: Confirm the target IMA knowledge-base ID, credential source, and local storage paths before running the script. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sundmop/unified-kb) <br>
- [Publisher profile](https://clawhub.ai/user/sundmop) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and a Python helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When executed, the helper can create local KB files, append memory records, call IMA note and knowledge-base APIs, and print status text.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
