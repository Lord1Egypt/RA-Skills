## Description:

Transform AI-generated content into natural, human-sounding writing, measure the improvement, and optionally verify the result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ch4812](https://clawhub.ai/user/ch4812)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and agents use this skill to polish AI-assisted drafts, remove formulaic writing patterns, and produce a local before-and-after evaluation without sending raw text to external verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional verification could expose sensitive content if raw original or rewritten text is sent outside the local environment.

Mitigation: Send only aggregate metrics such as counts, deltas, and boolean checks, and never send secrets, credentials, private content, or rewritten text to verification.

Risk: The skill may activate broadly on general polishing requests.

Mitigation: Use it when the user asks for style cleanup, human-sounding rewriting, or measurable before-and-after evaluation, and keep claims limited to writing transformation rather than proof of authorship.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ch4812/skills/verified-humanizer-new)
- [Verified Humanizer examples](artifact/references/examples.md)
- [OpenClaw integration notes](artifact/references/openclaw-integration.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Rewritten text with change notes, local evaluation metrics, optional verification status, and supporting Markdown or JSON reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Rewriting and evaluation are local by default; optional verification should use structured metrics only.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
