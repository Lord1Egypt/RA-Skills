## Description:

Generate and edit video with InfiniteTalk through RunAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create, edit, and transform video with RunAPI's InfiniteTalk service while validating the current operation contract, task response, and returned media.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing an unpinned third-party RunAPI CLI or Homebrew tap can introduce supply-chain exposure.

Mitigation: Use an approved, verified CLI version in stricter environments and review the RunAPI distribution path before installation.

Risk: RunAPI credentials and paid task submission can create billing or access exposure.

Mitigation: Limit the API key's privileges or billing scope, prefer environment or saved CLI authentication, and submit paid requests only after validating the operation contract.

Risk: Local media supplied to the skill may be uploaded to RunAPI.

Mitigation: Provide only media files intended for RunAPI processing and verify all requested media deliverables before reporting completion.

## Reference(s):

- [InfiniteTalk model overview, pricing, and rate limits](https://runapi.ai/models/infinitetalk.md)
- [InfiniteTalk model homepage](https://runapi.ai/models/infinitetalk)
- [Meigen AI provider overview](https://runapi.ai/providers/meigen-ai.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [InfiniteTalk SDK integration](https://github.com/runapi-ai/infinitetalk-sdk)
- [ClawHub skill page](https://clawhub.ai/runapi-ai/skills/runapi-infinitetalk)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands and JSON request or result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce task metadata and downloaded video files after response validation.]

## Skill Version(s):

0.2.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
