## Description:

Analyzes orchid images or videos to identify new shoots, flower-spike growth, root color and condition, then returns a growth-status assessment with care guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

External users and horticulture operators use this skill to analyze orchid plant and transparent-pot root imagery for growth monitoring, repotting timing, and care-direction decisions. It is intended for home orchid care, greenhouses, and horticulture studios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Orchid photos, videos, or supplied URLs may be sent to the configured cloud service.

Mitigation: Use only approved media, disclose the remote processing behavior to users, and avoid privacy-sensitive images unless consent and policy review are in place.

Risk: The skill may silently provision or reuse a remote identity and store service tokens in the local workspace.

Mitigation: Document identity handling, restrict workspace access, and rotate or remove stored tokens when uninstalling or changing users.

Risk: Historical reports are associated with an internal identity.

Mitigation: Confirm the intended account context before querying history and avoid using the skill in shared workspaces without access controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-orchid-growth-status-detection-analysis)
- [Publisher profile](https://clawhub.ai/user/smyx-sunjinhui)
- [API documentation](artifact/references/api_doc.md)
- [Skill demo](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown report with optional JSON detail and report link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include structured analysis results, visual growth indicators, care guidance, and historical report links.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
