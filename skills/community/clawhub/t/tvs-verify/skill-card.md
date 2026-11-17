## Description:

Tvs Verify checks whether recent AI-made changes actually satisfy the user's original request by turning the request into acceptance criteria, collecting evidence, and reporting a clear validation result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[inksnowhailong](https://clawhub.ai/user/inksnowhailong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to validate recent AI code, configuration, UI, or documentation changes against the original request with focused evidence rather than a broad code review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Verification may require running tests, lint, builds, scripts, or browser checks in the target workspace.

Mitigation: Keep checks narrowly tied to acceptance criteria, review commands before execution, and report missing environment or permissions instead of claiming success.

Risk: A validation report can overstate completion if evidence is incomplete.

Mitigation: Map every acceptance criterion to file, diff, static, runtime, or UI evidence and use partial pass, fail, or unverifiable when evidence is missing.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown validation report with acceptance criteria, evidence summaries, risk notes, and next steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The conclusion is constrained to pass, partial pass, fail, or unverifiable.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
