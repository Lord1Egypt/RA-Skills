## Description:

Helps creators prepare and publish image-and-text Xiaohongshu notes, with a logged-out check for public visibility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catsmansion](https://clawhub.ai/user/catsmansion)

### License/Terms of Use:

MIT-0

## Use Case:

Creators use the skill to prepare and publish image-and-text notes to their own Xiaohongshu account, then check the note's public visibility.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The browser setup may close unrelated browser sessions.

Mitigation: Use a dedicated browser session and save other work before setup.

Risk: The verification step may not reliably establish that the actual post is publicly visible.

Mitigation: Check the note in a logged-out browser and confirm its title and body are visible before treating it as public.

Risk: The scan was partial, and setup includes a global CLI installation instruction.

Mitigation: Review the setup and install commands before running them, and use a global CLI install only if its scope is acceptable.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/catsmansion/skills/xiaohongshu-post)
- [Publisher profile](https://clawhub.ai/user/catsmansion)
- [Selectors and publishing notes](artifact/references/selectors.md)
- [Copy and image guide](artifact/references/copy-guide.md)

## Skill Output:

**Output Type(s):** [Text, Links]

**Output Format:** [An image-and-text Xiaohongshu note with a title, body, images, topics, and shareable URL, plus a concise publication and visibility status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports image-and-text notes only; publishing requires the user's account to be logged in.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
