## Description:

Iteratively improves code or text with an LM Studio LLM by generating, critiquing, fixing, and verifying candidate outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nerua1](https://clawhub.ai/user/nerua1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run an iterative Generator, Critic, Fixer, and Verifier loop for improving source code, generated code, or text outputs before final review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied files and prompts can be sent to a configurable LLM API endpoint.

Mitigation: Use only a trusted local LM Studio endpoint; avoid remote LMSTUDIO_URL or --api-url values unless data sharing is acceptable, and do not process secrets or proprietary repositories without additional safeguards.

## Reference(s):

- [Ralph Wiggum Loop ClawHub listing](https://clawhub.ai/nerua1/skills/ralph-wiggum-loop)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Plain text, source code, Markdown, or JSON depending on the selected command options.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can print to stdout or write to an output file; the default loop limit is three iterations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
