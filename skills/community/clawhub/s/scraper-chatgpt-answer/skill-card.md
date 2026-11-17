## Description:

Collect ChatGPT answers by page URL or prompt, including answer text, citations, attached links, and prompt details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers collect ChatGPT answers for supplied prompts or ChatGPT page URLs through Dataify, with citations and related links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Implicit invocation may send prompts or ChatGPT URLs to the third-party Dataify API.

Mitigation: Review before installing and use only when that transfer is intended; avoid confidential prompts or private conversation links unless acceptable.

Risk: Successful collection consumes paid credits.

Mitigation: Monitor credit usage and prefer session-scoped token setup where possible.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dataify-server/skills/scraper-chatgpt-answer)
- [Dataify tool parameters](references/tool-params.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands]

**Output Format:** [ChatGPT answer text or Markdown with citations and links; shell commands for collection]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include prompt, send time, and source URL; raw variants available on request.]

## Skill Version(s):

1.0.1 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
