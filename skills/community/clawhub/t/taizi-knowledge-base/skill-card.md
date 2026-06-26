## Description: <br>
Personal knowledge base support for vector search, entity relationships, and note management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangepier-crypto](https://clawhub.ai/user/tangepier-crypto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to save selected text, entity relationships, and note files into a local personal knowledge base, then search or inspect that stored knowledge later. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-selected conversations or files can become searchable later in the local knowledge base. <br>
Mitigation: Use explicit save commands and avoid storing private content unless it is intended to remain searchable. <br>
Risk: The referenced vector_kb.py script is outside the artifact and should not be trusted blindly. <br>
Mitigation: Review the referenced script before relying on the workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tangepier-crypto/taizi-knowledge-base) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands reference a local knowledge-base workflow for adding, searching, summarizing, and indexing user-selected content.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
