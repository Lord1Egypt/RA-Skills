## Description:

Generates per-shot image and video prompts from WBFlow story and storyboard files, carrying character appearance locks, reference images, and inherited forbidden terms into `04_prompts/prompts.json`.

This skill is ready for commercial/non-commercial use.

## Publisher:

[junci003](https://clawhub.ai/user/junci003)

### License/Terms of Use:

MIT-0

## Use Case:

WBFlow users and creators use this pipeline stage to turn story and storyboard data into per-shot prompts for image and video generation. It must be installed with the WBFlow controller and companion stages to run as part of the pipeline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires the WBFlow controller and companion stages; installed alone, it cannot run as a complete pipeline stage.

Mitigation: Review and install the controller and required companion skills together, assessing each companion skill separately.

Risk: The skill warns that negative prompts may not prevent drift with distilled turbo models at low step counts and CFG=1.0.

Mitigation: Use positive spatial and pose constraints plus reference images as the primary consistency controls; treat negative prompts as supplementary.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/junci003/skills/wbflow-prompt)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON containing per-shot image and video prompts]

**Output Parameters:** [1D (one prompt set per storyboard shot)]

**Other Properties Related to Output:** [Preserves storyboard shot order and carries appearance locks, reference images, and forbidden terms forward from the source data.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
