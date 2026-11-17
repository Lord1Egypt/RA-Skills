## Description:

Adaptive multi-model AI roundtable that runs configurable AI panels through debate, critique, consensus scoring, validation, and neutral synthesis for OpenClaw workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimmyclanker](https://clawhub.ai/user/jimmyclanker)

### License/Terms of Use:


## Use Case:

Developers and teams use this skill to run structured multi-model roundtables for architecture decisions, debates, red-team reviews, votes, and synthesis-backed action plans. It is intended for OpenClaw workflows that can configure provider credentials, optional Discord output, and local persistence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Roundtable topics and outputs may be sent to Discord, web search, and multiple model providers, which can expose confidential discussion content.

Mitigation: Use explicit roundtable commands, verify the Discord destination before running, avoid sensitive topics, and use --no-search for private material.

Risk: The optional Blockrun proxy can add third-party model providers and paid usage paths.

Mitigation: Review, pin, and separately approve the Blockrun plugin before installing or funding it.

Risk: The skill stores roundtable results locally, which can retain sensitive prompts, scores, and synthesis text.

Mitigation: Review the workspace memory directory, apply local retention controls, and avoid running confidential topics unless storage is acceptable.

## Reference(s):

- [Roundtable Adaptive on ClawHub](https://clawhub.ai/jimmyclanker/skills/roundtable-adaptive)
- [OpenClaw](https://openclaw.ai)
- [README](artifact/README.md)
- [Panel Configuration](artifact/panels.json)
- [Final Output Schema](artifact/schemas/final-output.schema.json)
- [Example Roundtable Output](artifact/examples/debate-ai-developer-2026-02-23.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Structured Markdown synthesis with optional JSON persistence]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May post to a configured Discord channel or thread and save run records under the workspace memory directory.]

## Skill Version(s):

2.9.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
