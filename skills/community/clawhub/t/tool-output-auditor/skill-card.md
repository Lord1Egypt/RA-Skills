## Description:

Tool Output Auditor helps agents audit command and tool results before acting on them, especially when failed, partial, ambiguous, or suspicious output could be overlooked.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daowuu](https://clawhub.ai/user/daowuu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to classify command or tool output as success, failure, partial, or ambiguous before continuing multi-step workflows. It is most relevant for packaging, publishing, deployments, authentication checks, background processes, and file-generation steps where the next action depends on actual output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can activate frequently after meaningful commands, which may add review steps to normal workflows.

Mitigation: Use it when command output materially affects the next action, especially for publishing, deployment, authentication, process, and file-generation workflows.

Risk: Captured output from untrusted programs may contain terminal control characters or very large streams that make summaries misleading or slow.

Mitigation: Run the helper only on intended command logs or bounded files, and inspect suspicious or oversized output manually before acting on the recommendation.

## Reference(s):

- [Tool Output Auditor Skill Page](https://clawhub.ai/daowuu/skills/tool-output-auditor)
- [ClawHub Homepage](https://clawhub.ai)
- [Tool Output Audit Checklist](references/checklist.md)
- [Real Output Patterns](references/examples.md)
- [Real Mistakes This Skill Is Designed To Catch](references/real-mistakes.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance and plain-text command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The optional Python helper reads stdin or a bounded output file and emits a context, verdict, recommendation, and decisive lines.]

## Skill Version(s):

0.1.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
