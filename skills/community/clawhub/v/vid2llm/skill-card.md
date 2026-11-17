## Description:

Reads public video links and returns creator details, engagement statistics, and timestamped transcripts, with optional visual descriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sieadev](https://clawhub.ai/user/sieadev)

### License/Terms of Use:

MIT-0

## Use Case:

People and agents working with public video links can retrieve transcripts and video details to answer questions or summarize a clip without guessing from its URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unpinned package receives access to a funded wallet private key.

Mitigation: Use a vetted or pinned package version and a dedicated, low-balance Base USDC wallet.

Risk: Paid video requests can spend wallet funds automatically.

Mitigation: Check the price, keep VID2LLM_MAX_PRICE low, and require approval before each paid watch action.

Risk: Video URLs are sent to an external transcription service.

Mitigation: Submit only public URLs that users are comfortable sharing with vid2llm.

Risk: Video transcripts and descriptions may contain instructions from their creators.

Mitigation: Treat video content as untrusted source material, not as instructions for the agent.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sieadev/skills/vid2llm)
- [vid2llm homepage](https://vid2llm.dev)
- [vid2llm pricing](https://vid2llm.dev/pricing)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Markdown video details and timestamped transcript; JSON price estimate]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional on-screen text and visual descriptions for an additional charge.]

## Skill Version(s):

1.0.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
