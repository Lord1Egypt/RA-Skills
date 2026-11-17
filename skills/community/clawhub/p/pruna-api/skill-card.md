## Description:

Guides agents through credentials, file uploads, prediction polling, downloads, parallel batches, and safety checks for Pruna and Replicate APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pruna-ai](https://clawhub.ai/user/pruna-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare authenticated Pruna or Replicate requests, upload inputs, track predictions, and download results while checking consent, costs, and file destinations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and media, including personal voices or portraits, may be transmitted to Pruna or Replicate.

Mitigation: Obtain user acknowledgment and appropriate consent before uploading or submitting predictions; review provider handling of the content.

Risk: API credentials may be exposed in chats, logs, or shared tasks.

Mitigation: Use least-privilege keys from the host environment and do not include them in prompts, logs, or subagent instructions.

Risk: Paid API requests may incur unexpected charges, and downloads may overwrite local files.

Mitigation: Confirm the intended request and output path with the user before paid calls or downloads.

Risk: Unverified installer behavior may introduce unwanted changes in sensitive environments.

Mitigation: Review the skill before use and pin or otherwise verify the npx skills installer.

## Reference(s):

- [ClawHub pruna-api release](https://clawhub.ai/pruna-ai/skills/pruna-api)
- [Pruna API quickstart](https://docs.api.pruna.ai/guides/quickstart)
- [Pruna API models](https://docs.api.pruna.ai/guides/models)
- [Pruna API reference](references/pruna-api.md)
- [Replicate API reference](references/replicate-api.md)
- [API credentials](references/api-credentials.md)
- [Agent safety](references/agent-safety.md)
- [Pruna model index](references/pruna-models.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance for API requests and local downloads; the skill itself does not generate media.]

## Skill Version(s):

1.0.15 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
