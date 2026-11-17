## Description:

Analyzes images or videos of plant cuttings in transparent containers to assess visible root development and suggest when to transplant.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Home propagators, growers, and agricultural researchers use images or videos of cuttings in transparent containers to monitor rooting stages without disturbing the plants and inform transplant timing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images or media URLs are sent to lifeemergence.com services, and cloud report history can be retrieved.

Mitigation: Review the data-sharing and cloud-history behavior before installation; use only media approved for external processing.

Risk: The skill silently creates or reuses a local account identity and stores authentication tokens in a workspace SQLite database.

Mitigation: Use only if account-linked processing and local credential persistence are acceptable; protect access to the workspace.

Risk: Unrelated pet and generic analysis artifacts remain in the package.

Mitigation: Review the installed package and prefer a plant-only release with explicit privacy controls.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/smyx-sunjinhui/skills/smyx-cutting-rooting-status-detection-analysis)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured analysis report or Markdown table of historical reports; optional JSON or saved file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include root-stage assessments, transplant suggestions, and links to cloud reports.]

## Skill Version(s):

1.0.13 (source: ClawHub release metadata; bundled SKILL.md states 1.0.18)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
