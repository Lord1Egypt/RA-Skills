## Description:

AI agent for wiki retriever tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[urrrich](https://clawhub.ai/user/urrrich)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to identify the most relevant wiki or uploaded documents for a knowledge-base query, narrowing candidates by file names and then confirming relevance by reading file contents before submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect wiki and user-uploaded files in a workspace containing sensitive uploads.

Mitigation: Use it only for intended document retrieval tasks and review the workspace contents before activation when sensitive files may be present.

Risk: Broad retrieval requests can produce too many candidate documents or include irrelevant files.

Mitigation: Narrow results by reading document contents, limit final submissions to 10 documents, and ask the user for clarification when the scope remains too broad.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, tool calls, files]

**Output Format:** [Markdown guidance with selected attached files submitted through the retrieval workflow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Submits at most 10 finally selected documents and asks for clarification when the scope cannot be narrowed below that limit.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
