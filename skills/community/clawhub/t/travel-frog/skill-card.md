## Description: <br>
A travel frog that autonomously explores the world, sends postcards, and takes photos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NibbinNone](https://clawhub.ai/user/NibbinNone) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to run a persistent virtual travel companion that plans trips, sends status updates, archives postcards and photos, and maintains local game memories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores persistent game state, memories, diary entries, collections, and media artifacts on the local filesystem. <br>
Mitigation: Use the default or a dedicated state directory, avoid entering sensitive personal information, and review reset behavior before deleting game progress. <br>
Risk: Postcard and photo workflows can hand prompts to separate image-generation skills. <br>
Mitigation: Review the image-generation skills and generated prompts before use in environments with stricter data or content policies. <br>
Risk: Scheduled autonomous updates can produce messages without an immediate user request. <br>
Mitigation: Deploy only where scheduled companion-style notifications are expected and keep message destinations scoped to the intended account and channel. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/NibbinNone/travel-frog) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and plain text with shell command examples and JSON-shaped engine outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local state, collections, diary entries, and media-generation prompts during normal use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
