## Description:

Generate an AI image via Gemini and post it to X (Twitter) using OAuth1. Supports text-only or text+image tweets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zero2ai-hub](https://clawhub.ai/user/zero2ai-hub)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to generate an image from a prompt and publish a text-only or text-plus-image post to X/Twitter from one command.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses X/Twitter credentials for public posting.

Mitigation: Use credentials only for an account intended for this workflow and review text and image prompts before posting.

Risk: Helper commands may receive broader account or API credential environment than necessary.

Mitigation: Prefer a version or local wrapper that passes only required environment variables to uv and xurl and constrains the image-generator path.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Command output and stdout status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Posts public X/Twitter content and logs media ID and confirmation details when available.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
