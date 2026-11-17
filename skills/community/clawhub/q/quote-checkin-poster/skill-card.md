## Description:

Turn quotes and reflections from books or films into polished shareable check-in posters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuminliu026](https://clawhub.ai/user/shuminliu026)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this agent skill to turn a book, film, documentary, anime, drama, or similar media quote plus a short reflection into a shareable check-in poster. The workflow helps collect poster inputs, choose mood and style, call Mew image and design APIs, and return a polished poster link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends quote text, reflections, optional image URLs, and the user's Mew API key to mew.design.

Mitigation: Use the skill only when the user accepts this third-party API disclosure and avoid supplying sensitive text, images, or credentials beyond what the workflow requires.

Risk: Local or attached images may require temporary third-party upload before they can be used by downstream image APIs.

Mitigation: Prefer public image URLs; upload local images only after the user explicitly accepts the privacy tradeoff.

Risk: Some consent and onboarding prompts are written in Chinese, which may be unclear to non-Chinese users.

Mitigation: Restate consent, credential, and upload prompts in the user's preferred language before proceeding.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shuminliu026/skills/quote-checkin-poster)
- [mew.design account setup](https://mew.design/login)
- [Mew image-process API endpoint](https://api.mew.design/open/api/image/process)
- [Mew design-generate API endpoint](https://api.mew.design/open/api/design/generate)

## Skill Output:

**Output Type(s):** [Markdown, API calls, Guidance]

**Output Format:** [Markdown image link with a short mood summary and optional source image link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces social poster image URLs from mew.design and may include concise retry/style guidance.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
