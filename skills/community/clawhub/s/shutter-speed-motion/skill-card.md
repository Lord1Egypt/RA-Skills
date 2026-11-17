## Description:

Guides agents in choosing shutter speeds for moving subjects, including freezing action, conveying motion blur, and using panning techniques.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bianchunhui](https://clawhub.ai/user/bianchunhui)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to select shutter speeds for sports, children, pets, vehicles, water, and other moving subjects. It helps decide whether to freeze motion, show motion blur, or apply panning while distinguishing shutter-speed motion control from depth-of-field and exposure-calculation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may answer primarily in Chinese even when the user expects another language.

Mitigation: Clarify the intended response language during publication or instruct the agent to answer in the user's preferred language.

Risk: Photography recommendations can misdiagnose blur if subject motion, camera shake, focus, and exposure tradeoffs are not separated.

Mitigation: Prompt the agent to ask about subject speed, movement direction, distance, focal length, light level, and the desired creative effect before giving final shutter-speed guidance.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/bianchunhui/nyip-photography-skills/tree/main/shutter-speed-motion)
- [ClawHub skill page](https://clawhub.ai/bianchunhui/skills/shutter-speed-motion)

## Skill Output:

**Output Type(s):** [guidance, text, markdown]

**Output Format:** [Markdown or plain text guidance with concrete shutter-speed recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include step-by-step factor evaluation, specific shutter-speed ranges, and panning instructions.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
