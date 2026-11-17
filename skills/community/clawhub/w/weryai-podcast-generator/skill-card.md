## Description:

Generate, query, and deliver WeryAI podcasts through the official podcast generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weryai-developer](https://clawhub.ai/user/weryai-developer)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create spoken WeryAI podcast episodes from a topic or existing task, including speaker lookup, text generation, audio generation, status checks, and final audio delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid podcast submission, audio generation, and wait flows may consume WeryAI credits and send podcast inputs, webhook URLs, caller IDs, and task IDs to WeryAI.

Mitigation: Use dry-run checks first, confirm query, speakers, language, and mode before paid runs, and protect WERYAI_API_KEY as a paid account credential.

Risk: Under-scoped credential routing could expose API credentials or podcast inputs if WERYAI_BASE_URL is pointed at an untrusted host.

Mitigation: Use the official WeryAI API host unless a trusted override has been explicitly reviewed.

Risk: The package includes bundled music and upload helper code outside the declared podcast workflow.

Mitigation: Invoke only the documented podcast entrypoints and do not use bundled weryai-music or upload helpers from this podcast package.

## Reference(s):

- [WeryAI Podcast API](references/podcast-api.md)
- [ClawHub skill page](https://clawhub.ai/weryai-developer/skills/weryai-podcast-generator)
- [Podcast speakers API](https://docs.weryai.com/api-reference/podcast-generation/get-podcast-speakers-list)
- [Podcast text generation API](https://docs.weryai.com/api-reference/podcast-generation/submit-podcast-text-generation-task)
- [Podcast audio generation API](https://docs.weryai.com/api-reference/podcast-generation/generate-podcast-audio)
- [Task status API](https://docs.weryai.com/api-reference/tasks/query-task-details)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries with audio links; helper scripts return JSON status or result objects.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >=18 and WERYAI_API_KEY; uses paid network API calls; supports dry-run checks before submitting paid work.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
