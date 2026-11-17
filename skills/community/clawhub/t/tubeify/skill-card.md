## Description:

AI video editor for YouTube creators that removes pauses, filler words, and dead air automatically via API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[esokullu](https://clawhub.ai/user/esokullu)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and agents use Tubeify to authenticate with a wallet, submit a public raw video URL for automated cleanup, poll processing status, and retrieve a processed video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow sends video URLs, wallet addresses, transaction hashes, session cookies, and processed-video links to a third-party service.

Mitigation: Install only if you trust tubeify.xyz with that data, and start with test or non-confidential media.

Risk: The workflow stores a session cookie in session.txt.

Mitigation: Avoid shared workspaces for session.txt and delete the cookie file after use.

Risk: Wallet-address-only authentication should not be treated as strong account protection.

Mitigation: Avoid relying on this authentication model for sensitive or shared production workflows.

## Reference(s):

- [Tubeify ClawHub skill page](https://clawhub.ai/esokullu/skills/tubeify)
- [Tubeify website](https://tubeify.xyz)
- [Publisher profile](https://clawhub.ai/user/esokullu)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with curl command examples and parameter guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl; the workflow uses a session cookie file and submits video URL, wallet address, and transaction hash data to Tubeify.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
