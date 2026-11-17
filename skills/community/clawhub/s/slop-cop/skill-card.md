## Description:

Judges visual design assets and AI-generated images before they ship, including layout defects, hallucinated text, and semantic consistency between copy and visuals/data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chchchadzilla](https://clawhub.ai/user/chchchadzilla)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, founders, and design reviewers use this skill to audit image assets, UI screenshots, marketing creative, dashboard visuals, and A/B variants before release. It produces strict SHIP, FIX, or KILL verdicts with concrete defects, recommendations, and deploy notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images, URLs, or screenshots provided for visual QA can contain sensitive or unreleased content.

Mitigation: Provide only assets you are comfortable having inspected by the agent and vision tool.

Risk: A visual QA verdict may be incomplete when the image cannot be rendered or the vision pass fails.

Mitigation: Use direct rendered-image inspection when available, mark no-inspection cases as BEST-EFFORT, and review findings before shipping.

Risk: The skill can flag misleading or inconsistent visual claims but does not verify business data sources.

Mitigation: Confirm underlying metrics, copy, and chart data with the responsible owner before releasing production creative.

## Reference(s):

- [Per-Asset Checklist](references/checklist.md)
- [Anti-Patterns to Flag](references/anti-patterns.md)
- [Semantic Consistency Checks](references/semantic-consistency.md)
- [Vision Prompt Template](references/vision-prompt-template.md)
- [OpenClaw Getting Started](https://docs.openclaw.ai/start/getting-started)
- [ClawHub Skill Page](https://clawhub.ai/chchchadzilla/skills/slop-cop)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown with verdicts, defects, anti-patterns, recommendation, and deploy notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses SHIP, FIX, KILL, and BEST-EFFORT labels when supported by the inspection evidence.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
