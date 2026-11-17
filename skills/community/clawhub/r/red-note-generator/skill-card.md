## Description:

Red Note Generator creates complete Xiaohongshu (RED) style notes from a topic and optional style requirements using the wsdsocial.com API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wsd-mj](https://clawhub.ai/user/wsd-mj)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, and agents use this skill to draft publishing-ready Xiaohongshu (RED) notes from a required topic plus optional tone, word count, and formatting guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Topics and style instructions are sent to wsdsocial.com for generation.

Mitigation: Do not submit secrets, private customer data, confidential business material, or sensitive unpublished campaign details.

Risk: The API key is required for access and could be exposed through logs or shared shell history.

Mitigation: Store WSD_API_KEY in the environment or a secret manager and avoid printing it in logs or examples.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/WSD-MJ/red-note-generator)
- [ClawHub skill page](https://clawhub.ai/wsd-mj/skills/red-note-generator)
- [Publisher profile](https://clawhub.ai/user/wsd-mj)
- [WSD Social API key page](https://ai.wsdsocial.com/skills)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Generated RED note content as plain text or Markdown-style prose]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WSD_API_KEY and sends the topic and optional request to wsdsocial.com.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
