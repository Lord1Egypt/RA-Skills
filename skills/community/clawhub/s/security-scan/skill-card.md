## Description:

Security Scan helps agents perform a lightweight static security review of OpenClaw skills and small code folders before publishing, installing, or trusting them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shadowloong](https://clawhub.ai/user/shadowloong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, skill publishers, and reviewers use this skill to run a quick static security pass over OpenClaw skills or small code folders and produce a concise risk summary with recommended next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scan output can include sensitive matched lines from repositories that contain real credentials or private code.

Mitigation: Keep scan output private, avoid sharing raw matches broadly, and rotate any exposed credentials confirmed during review.

Risk: The bundled scanner is lightweight and heuristic, so it can miss issues or report benign matches.

Mitigation: Treat results as review signals, inspect flagged code manually, and use deeper security tooling when publish or install risk remains unclear.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or compact plain-text security summary with optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sensitive matched lines from scanned files; keep scan output private and review findings manually.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
