## Description:

Getting started with Signet Mind - local mental health companion with grounding exercises, breathing guides, and mood tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amrree](https://clawhub.ai/user/amrree)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to get started with Signet Mind, configure a local mental health companion, and understand its grounding exercises, breathing guides, mood tracking, and privacy model. The skill provides support guidance only and is not a substitute for professional mental health care.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Privacy and encryption claims may overstate the protection provided for sensitive mental-health data.

Mitigation: Review storage behavior before installation, update privacy wording to match implementation, and avoid entering highly sensitive information unless plaintext local storage is acceptable.

Risk: Conversation and history context may be passed to the local Signet CLI during personalized response generation.

Mitigation: Obtain clear user consent before sharing prompt or history context with the CLI, and document what data is passed.

Risk: Crisis guidance may not be appropriate for every user's location.

Mitigation: Add region-aware crisis resources and direct users to local emergency services when immediate harm is possible.

Risk: Users may rely on the tool as professional mental health care.

Mitigation: Keep the non-therapy limitation prominent and route crisis or clinical needs to professional support.

## Reference(s):

- [Find a Helpline](https://findahelpline.com)
- [ClawHub Skill Page](https://clawhub.ai/amrree/skills/signet-guide)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration guidance]

**Output Format:** [Markdown with inline shell commands and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include setup walkthroughs, first-session guidance, privacy explanations, and wellness tool instructions.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
