## Description:

Audits user requests before execution to classify whether an LLM can handle them safely or should route parts to humans or professional tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianzhiceng297-boop](https://clawhub.ai/user/tianzhiceng297-boop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to screen capability-sensitive user requests, classify them as safe, restricted, or prohibited for LLM execution, and route unsafe portions to humans or professional tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be overcautious and pause or reroute requests that could otherwise receive direct best-effort assistance.

Mitigation: Review the audit verdict against the user's actual request and proceed directly when the task is clearly a safe-zone text, translation, summarization, extraction, or formatting task.

Risk: Strict boundary classifications can slow workflows that involve code audits, proofs, predictions, professional judgments, or completeness guarantees.

Mitigation: Use the skill to define the LLM's supporting role, then involve formal tools, domain experts, or human reviewers for the part that requires verification or responsibility.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown task-boundary audit with a verdict, optional decomposition table, and division-of-labor guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution, API calls, file writes, data access, or persisted state.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
