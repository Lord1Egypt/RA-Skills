## Description:

Creates Xiaohongshu/REDnote titles, post copy, cover wording, hashtags, and comment starters from a brief, with optional Xiaohongshu research and a matching cover image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and businesses use it to turn a product, experience, topic, or audience brief into Xiaohongshu/REDnote post copy and, after approval, a matching cover. Optional paid Xiaohongshu note, comment, and account lookups can ground the research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authorization requests broader account permissions than the writing task needs.

Mitigation: Review the full Beatra authorization and prefer a release with narrower permissions; revoke access through the Beatra Console when it is no longer needed.

Risk: An uninstall cleanup flaw can disconnect other Beatra skills.

Mitigation: Prefer a release with corrected uninstall inventory validation and check the inventory before removing the skill.

Risk: Optional Xiaohongshu lookups and cover generation consume credits.

Mitigation: Review the current price and approve each paid lookup or image generation separately before it runs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beatra-ai/skills/zhongcao-note-copywriter)
- [Beatra skill homepage](https://beatra.ai/skills/zhongcao-note-copywriter)
- [Workflow and writing guidance](references/workflow.md)
- [Xiaohongshu lookup guidance](references/note-lookup.md)
- [Updates and security guidance](references/updates-and-security.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Images]

**Output Format:** [Markdown post copy and a vertical 3:4 cover image]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Title options, note body, cover wording, hashtags, and a comment starter; one cover image when approved.]

## Skill Version(s):

0.2.7 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
