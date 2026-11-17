## Description:

Turn a one-line idea into a full short video: Revid writes the script, picks visuals, and assembles the cut.

This skill is ready for commercial/non-commercial use.

## Publisher:

[api00](https://clawhub.ai/user/api00)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and agents use this skill to turn a topic, question, or one-line concept into a short Revid-generated video without first writing a script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, optional style notes, and video-generation settings are sent to Revid.

Mitigation: Avoid private, regulated, or proprietary prompt content unless the user's Revid account terms permit that use.

Risk: The skill requires a Revid API key.

Mitigation: Store REVID_API_KEY as configuration or secret material and do not include it in prompts, logs, or shared examples.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/api00/skills/revid-prompt-to-video)
- [Revid render API endpoint](https://www.revid.ai/api/public/v3/render)
- [Revid status API endpoint](https://www.revid.ai/api/public/v3/status)
- [Publisher profile](https://clawhub.ai/user/api00)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API payloads and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REVID_API_KEY and sends the prompt, optional style notes, and video-generation settings to Revid.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
