## Description: <br>
Retrieves relevant wiki, Feishu, or uploaded documents for knowledge-base query tasks by narrowing candidates with filenames and file contents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[urrrich](https://clawhub.ai/user/urrrich) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to retrieve the most relevant knowledge-base or uploaded documents for a user's query. It is intended to submit a focused set of matching files, capped at 10 documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may expose private or unrelated documents if it is run in a workspace containing sensitive files outside the intended retrieval scope. <br>
Mitigation: Install and run it only where the agent may inspect the relevant wiki, Feishu, or uploaded documents, and keep unrelated confidential files out of scope. <br>
Risk: File-reading code could access unintended local files if Python use is not constrained to declared uploads. <br>
Mitigation: Limit Python file access to files listed in the runtime upload_files parameter and use the uploaded filenames directly. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/urrrich/wiki-retriever) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Markdown or plain text guidance with selected attached files submitted through the runtime tool] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Final retrieved document set is limited to a maximum of 10 files.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
