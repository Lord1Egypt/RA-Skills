## Description:

Write and publish Beehiiv posts with AI by researching via YouMind, drafting Beehiiv-native newsletter content, converting Markdown to HTML, and publishing through the user's connected Beehiiv account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mindy-youmind](https://clawhub.ai/user/mindy-youmind)

### License/Terms of Use:

MIT-0

## Use Case:

External users, newsletter operators, creator businesses, and editorial growth teams use this skill to create, adapt, preview, and publish Beehiiv newsletter posts through a YouMind-connected Beehiiv account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can act on a connected Beehiiv account through YouMind, including creating, updating, listing, and deleting posts.

Mitigation: Install only when that connected-account access is acceptable, prefer draft mode, and run update or delete actions only when the user explicitly intends to change existing posts.

Risk: The local YouMind API key in ~/.youmind/config.yaml is tied to the connected publishing account.

Mitigation: Protect the config file and rotate the API key if the file is exposed.

Risk: Untrusted Markdown can be converted to preview HTML or published content.

Mitigation: Review Markdown from untrusted sources before previewing or publishing it.

Risk: Changing youmind.base_url away from the official YouMind endpoint can route credentials and content to a different service.

Mitigation: Keep youmind.base_url set to https://youmind.com/openapi/v1 unless deliberately performing local backend debugging.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mindy-youmind/skills/youmind-beehiiv-article)
- [Beehiiv Pipeline](references/pipeline.md)
- [YouMind Beehiiv OpenAPI Reference](references/api-reference.md)
- [Platform DNA](references/platform-dna.md)
- [Generation Playbook](references/content-generation-playbook.md)
- [Content Adaptation Playbook](references/content-adaptation-playbook.md)
- [Dispatch Capability Manifest](dispatch-capabilities.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown drafts, concise status text, configuration steps, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce local Markdown drafts, Beehiiv-safe HTML previews, post status details, and result links when available.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
