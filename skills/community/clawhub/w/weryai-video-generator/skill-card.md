## Description:

Generate and transform WeryAI videos from text, images, storyboard frames, or first-frame and last-frame guidance, with bounded polling for final video output, status checks, model switching, and dry-run payload previews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weryai-developer](https://clawhub.ai/user/weryai-developer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative operators use this skill to submit WeryAI text-to-video, image-to-video, storyboard, first-frame/last-frame, model lookup, balance, and status workflows through an agent. It is intended for paid WeryAI API use with explicit credential setup and bounded polling for generation results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Runtime behavior depends on external core/weryai-core and core/weryai-video modules that are outside this package.

Mitigation: Review and pin the surrounding runtime modules before production use or before processing sensitive media.

Risk: The skill uses a paid WeryAI API credential and can submit generation jobs that consume credits.

Mitigation: Keep WERYAI_API_KEY secret, confirm model parameters before paid submissions, and use dry-run or status/model checks when possible.

Risk: Endpoint override variables can redirect requests to non-default hosts.

Mitigation: Use WERYAI_BASE_URL and WERYAI_MODELS_BASE_URL only with hosts that the operator controls or explicitly trusts.

## Reference(s):

- [WeryAI Skill Page](https://clawhub.ai/weryai-developer/skills/weryai-video-generator)
- [WeryAI Publisher Profile](https://clawhub.ai/user/weryai-developer)
- [WeryAI API Keys](https://www.weryai.com/api/keys)
- [WeryAI Video Generation Models](references/api-models.md)
- [WeryAI Error Codes](references/error-codes.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON command output and playable video links when generation completes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generation results can include task identifiers, task status, video URLs, request summaries, balance data, and error details.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
