## Description:

Estimates concrete volumes and rebar ranges from structural drawings for material planning, with review flags and stated accuracy limits.

This skill is for research and development only.

## Publisher:

[lisong2003-lgtm](https://clawhub.ai/user/lisong2003-lgtm)

### License/Terms of Use:

CC-BY-NC-SA-4.0

## Use Case:

Construction technicians and quantity estimators use it to prepare preliminary concrete and rebar material plans by floor or pour zone from structural drawings. Results are planning estimates, not final takeoffs or settlement quantities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanners report mismatches between the declared quantity-estimation purpose and some implemented behavior, and automatic execution of a separately downloaded dependency; inspection was partial.

Mitigation: Avoid installation unless needed; review the setup and quantity outputs before relying on them.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/lisong2003-lgtm/skills/tujian-suanliang)
- [Publisher profile](https://clawhub.ai/user/lisong2003-lgtm)
- [Usage and quantity rules](references/on-demand.md)
- [Input contract](references/base-contract.md)
- [Usage examples](references/usage-examples.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, CSV, JSON]

**Output Format:** [Markdown, CSV, and JSON quantity reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Per-floor or pour-zone planning estimates with review flags; rebar quantities are ranges.]

## Skill Version(s):

0.9.45 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
