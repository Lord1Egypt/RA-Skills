## Description:

Technical Eval guides a structured technology selection workflow from requirements definition through market scan, maturity assessment, weighted comparison, PoC planning, risk control, recommendation, and report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincentlau2046-sudo](https://clawhub.ai/user/vincentlau2046-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and technical decision makers use this skill to compare technology options with quantified evaluation criteria, PoC decision thresholds, risk matrices, and implementation recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Evaluation topics may be sent to external research sources.

Mitigation: Use the skill only for non-confidential evaluation topics unless external-source sharing is approved.

Risk: The Tavily configuration loads variables from ~/.openclaw/.env broadly.

Mitigation: Keep only TAVILY_API_KEY in that file for this workflow or patch the configuration to read only that key.

Risk: Evaluation topics are used in persistent output paths.

Mitigation: Sanitize or slug topics before running the workflow and confirm the destination directory before sharing results.

Risk: The skill automatically writes reports, data files, source lists, and presentation output.

Mitigation: Run it in a controlled workspace and review generated files before relying on or distributing them.

Risk: Generated presentation HTML pulls remote browser resources.

Mitigation: Inspect the generated HTML and allow remote resources only in an approved environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/vincentlau2046-sudo/skills/technical-eval)
- [Publisher Profile](https://clawhub.ai/user/vincentlau2046-sudo)
- [Technical Evaluation Design Specifications](references/design-spec.md)
- [Technical Evaluation Slide Types](references/slide-types.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, HTML presentation output, CSV/JSON analysis data, source lists, and concise conversational summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes persistent evaluation artifacts under ~/.openclaw/workspace/tech-insight/technical-eval/{topic} and uses Tavily search when TAVILY_API_KEY is configured.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
