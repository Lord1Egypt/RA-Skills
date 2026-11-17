## Description:

Turns unstructured Chinese source text such as chat logs, drafts, meeting notes, reading notes, industry analysis, or market reviews into a structured WeChat Official Account article with headings, emphasis, a risk notice, and share-oriented closing text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ninetyhe-90](https://clawhub.ai/user/ninetyhe-90)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and operators use this skill to convert loosely structured Chinese text into publish-ready WeChat Official Account markdown. It is especially oriented toward preserving source viewpoints while reorganizing material into standard or premium long-form article structures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated articles may be saved automatically to a root-owned default path without confirmation.

Mitigation: Edit or configure the skill before installation so saving requires explicit approval, uses a non-privileged user-selected directory, and sanitizes generated filenames.

Risk: Financial market-review content generated from user material could be mistaken for investment advice.

Mitigation: Keep the risk disclaimer, preserve source attribution where applicable, and require human review before publishing financial commentary.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ninetyhe-90/skills/text-to-wechat-official)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown article with section headings, bolded key points, a risk notice, and closing engagement text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The artifact asks the agent to save generated articles to a user-specified WeChat directory, with a default root-owned path.]

## Skill Version(s):

1.2.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
