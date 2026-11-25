## Description:

Creates a coordinated vertical food-image sequence and REDnote post plan from a dish photo or restaurant-visit concept, with optional Xiaohongshu research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and restaurant marketers use this skill to turn a dish photo or visit concept into a coordinated REDnote food post, including a food image sequence and supporting title, caption, and tag ideas. It can also perform optional, separately priced Xiaohongshu lookups for topic notes, comments, or an account's recent notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The requested shared account permissions may extend beyond food-post creation.

Mitigation: Review the authorization scopes and account access described in the installation guidance before connecting; do not authorize if the access is broader than you accept.

Risk: Installation registration automatically reports coarse installation and runtime information to Beatra.

Mitigation: Review the registration fields and privacy terms in the installation guidance before installing, and avoid installing if this reporting is not acceptable.

Risk: Uninstall cleanup may affect shared Beatra connection data when the local installation inventory is malformed or incomplete.

Mitigation: Check the installation inventory and whether other Beatra skills remain before disconnecting or uninstalling.

## Reference(s):

- [Food-note planning](references/food-note-planning.md)
- [Food-note workflow](references/workflow.md)
- [Xiaohongshu note lookup](references/note-lookup.md)
- [Installation, authentication, and permissions](references/installation-and-auth.md)
- [Updates and security](references/updates-and-security.md)
- [Beatra skill page](https://beatra.ai/skills/zhongcao-food-note-maker)
- [ClawHub release page](https://clawhub.ai/beatra-ai/skills/zhongcao-food-note-maker)

## Skill Output:

**Output Type(s):** [Images, Text, Markdown, Guidance]

**Output Format:** [A coordinated food-image sequence with title ideas, caption beats, and tags; optional Xiaohongshu lookup summaries]

**Output Parameters:** [Typically four vertical 3:4 images at 2K when the live model supports the requested sequence]

**Other Properties Related to Output:** [Food and restaurant claims are grounded in user-provided facts; optional platform lookups are separately priced and require confirmation.]

## Skill Version(s):

0.2.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
