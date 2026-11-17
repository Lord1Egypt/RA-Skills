## Description:

Analyze codebases for architecture, patterns, diagrams, and agent context so developers and agents can understand repositories quickly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[selvatuple](https://clawhub.ai/user/selvatuple)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to submit a GitHub repository for Revibe analysis, review architecture and design summaries, inspect drill-down sections, and save agent_context.json for later agent work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository code can be sent to and retained by Revibe for analysis and re-analysis.

Mitigation: Use the skill only for repositories whose code may be shared with Revibe, and review Revibe privacy and retention terms before using it with private, proprietary, regulated, or client code.

Risk: Broad or silent triggers may analyze the current repository without strong per-run consent.

Mitigation: Prefer explicit repository URLs and confirm the target repository before submission, especially when working in private or sensitive workspaces.

Risk: Reducing permission prompts with broad allowed-tools grants can allow network calls with less user friction.

Mitigation: Grant only the narrow tool permissions needed for trusted use, and avoid broad allowed-tools entries unless the Revibe service and current workspace are trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/selvatuple/skills/revibe)
- [Revibe homepage](https://www.revibe.codes)
- [Revibe app](https://app.revibe.codes)

## Skill Output:

**Output Type(s):** [text, markdown, json, html, guidance]

**Output Format:** [Markdown summaries with JSON agent context and optional HTML diagram files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REVIBE_API_KEY plus curl, jq, and git; saves agent_context.json in the working directory.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
