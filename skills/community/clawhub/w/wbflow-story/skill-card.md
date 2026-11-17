## Description:

Turns a one-line story theme into a structured story outline and character profiles in story.json for the WBFlow pipeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[junci003](https://clawhub.ai/user/junci003)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and developers use this skill to turn a story theme and episode count into a structured outline, world setting, and character descriptions for downstream WBFlow stages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A generated story may be inaccurate or unsuitable for the project.

Mitigation: Review the generated story.json before passing it to downstream stages.

Risk: Running this stage without its companion WBFlow skills leaves the pipeline incomplete.

Mitigation: Install and review the WBFlow controller and companion stages as a set.

Risk: An existing story.json could be replaced.

Mitigation: Check the project directory and confirm before replacing an existing story.json.

## Reference(s):

- [WBFlow·第1环 企划人设 on ClawHub](https://clawhub.ai/junci003/skills/wbflow-story)
- [Publisher profile: junci003](https://clawhub.ai/user/junci003)

## Skill Output:

**Output Type(s):** [JSON, Files]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes 01_story/story.json with the story outline, worldview, characters, episode beats, and style guide; character IDs are stable pipeline keys.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
