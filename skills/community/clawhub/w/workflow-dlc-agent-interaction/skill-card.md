## Description:

Agent interaction design workflow for compressing conversational confirmation into a three-step flow: natural language input, implicit validation with highlighted form fields, and user-confirmed submission.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mistyhuqwq-art](https://clawhub.ai/user/mistyhuqwq-art)

### License/Terms of Use:

MIT-0

## Use Case:

Product designers, agent builders, and workflow owners use this skill to design Copilot-style interaction flows with structured confirmation cards, implicit validation, field highlighting, quick actions, templates, and collaboration awareness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Implementations of page-context access, operation-log checks, template sharing, or submit flows may exceed the active product workflow if copied without review.

Mitigation: Keep integrations scoped to the active workflow and require user confirmation before applying or submitting changes.

Risk: The source skill is written for Chinese-language Agent interaction design work, so applying it outside that domain may produce a poor fit.

Mitigation: Confirm the language, product context, and intended interaction model before installing or adapting the skill.

Risk: Dynamic generation of quick action controls can create inconsistent or delayed user interactions.

Mitigation: Use deterministic product rules for quick actions and templates, and reserve model output for guidance and parameter interpretation.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/mistyhuqwq-art/skills/workflow-dlc-agent-interaction)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with structured checklists, state-machine text, confirmation card templates, and JSON log examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable output; guidance is intended to be reviewed and adapted before implementation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
