## Description:

Search images and boards in zizo library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[foobarhe](https://clawhub.ai/user/foobarhe)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search Zizo for images, photos, visual assets, and boards or collections from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends search queries and a user-provided token to a configured HTTPS Zizo server.

Mitigation: Install only for intended Zizo image and board search use, keep ZIZO_TOKEN private, and leave ZIZO_SERVER at the default unless the alternate server is trusted.

Risk: Generic image-search prompts may be routed to Zizo by this skill.

Mitigation: Review agent routing and prompt handling so Zizo is used only when the user expects Zizo-backed image or board search.

## Reference(s):

- [Zizo](https://zizo.pro)
- [Zizo token settings](https://zizo.pro/#/?settings=token)
- [ClawHub skill page](https://clawhub.ai/foobarhe/skills/zizo)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search output lists matching images or boards with titles, IDs, URLs, sizes, descriptions, and result counts when returned by Zizo.]

## Skill Version(s):

1.0.4 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
