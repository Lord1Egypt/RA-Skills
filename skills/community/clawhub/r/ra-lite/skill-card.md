## Description:

Ra Lite -- Research Intelligence. Drop a topic and get an instant structured 3-source research brief. Free tier of Ra.

This skill is ready for commercial/non-commercial use.

## Publisher:

[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Ra Lite to turn a research topic into a concise, sourced brief with an executive summary, key findings, implications, and three cited sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup step may modify system Python packages for presentation-only formatting.

Mitigation: Run the skill in an isolated virtual environment or remove the rich installation step before use.

Risk: The generated research brief depends on three web sources selected at runtime, so source quality and recency can vary.

Mitigation: Review the cited sources and verify important claims before relying on the brief.

Risk: The skill includes an upgrade prompt after producing the Lite brief.

Mitigation: Expect the prompt as part of the release behavior and remove it if it is not appropriate for the deployment context.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/occupythemilkyway/skills/ra-lite)
- [OpenClaw Homepage](https://clawhub.ai/occupythemilkyway/ra-lite)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown research brief with inline setup commands and cited source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires RESEARCH_TOPIC and expects the agent to use web search for three authoritative sources.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
