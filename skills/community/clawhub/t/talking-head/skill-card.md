## Description:

Turns a portrait plus a short user-provided script into a one-person talking-head video clip through the Ofox video workflow, with explicit cost approval before billable generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ofoxai](https://clawhub.ai/user/ofoxai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill when a user has permission to use a person's likeness and wants that portrait to speak a short, finished script to camera. It guides briefing, prompt construction, cost approval, generation, and post-run checks for identity, spoken words, and gross lip sync.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Portraits and scripts are sent to Ofox for generation, and the output can depict a likeness saying words the person did not say.

Mitigation: Confirm the user has permission to use the face this way, avoid identifiable public figures, and make the data-sharing step explicit before generation.

Risk: Billable Ofox jobs can be submitted if an agent runs generation without meaningful user approval.

Mitigation: Use dry-run pricing first, show the cost table and full script, and only run billable commands with --approved after the user says yes.

Risk: If the delegated core skill is missing, an installer command could modify the user's broader agent environment.

Mitigation: Ask the user to run the installer themselves and prefer installing only the missing ofox-video-core skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ofoxai/skills/talking-head)
- [Skill homepage](https://github.com/ofoxai/skills/tree/main/skills/talking-head)
- [Ofox application](https://app.ofox.ai)

## Skill Output:

**Output Type(s):** [Guidance, Text, Shell commands, Files]

**Output Format:** [Markdown guidance with bash commands, prompt text, generated video paths, and cost/status values from the Ofox workflow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OFOX_API_KEY for paid generation, uses curl and jq, and delegates execution to ofox-video-core 2.0.0 or newer.]

## Skill Version(s):

2.0.0 (source: server release metadata, SKILL.md frontmatter, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
