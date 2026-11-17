## Description:

Three-pass reflection loop that takes draft code, runs a senior-engineer critique, then produces a revised version to catch bugs, API misuse, and pattern drift.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stephenlthorn](https://clawhub.ai/user/stephenlthorn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to review generated code, revise it against critique findings, and return a confidence rating for the final result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reviewed code can be sent to a configured LLM service.

Mitigation: Use a trusted local or HTTPS endpoint and avoid automatic use on sensitive or proprietary code unless that endpoint is approved.

Risk: Revised output may be incorrect or unsuitable for deployment.

Mitigation: Review revised code manually before saving, executing, or deploying it.

## Reference(s):

- [Reflect Critique Revise on ClawHub](https://clawhub.ai/stephenlthorn/skills/reflect-critique-revise)

## Skill Output:

**Output Type(s):** [code, text, guidance]

**Output Format:** [Revised code text, or JSON containing revised code, critique history, confidence, and passes used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default behavior uses up to two critique-and-revision passes; JSON mode includes critique history and confidence.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
