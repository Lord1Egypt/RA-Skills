## Description:

Create native TikTok video ads with Pexo by relaying a product brief to Pexo's hosted video agent, which writes the script, sequences shots, selects models, and returns a ready-to-post vertical ad.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pexo](https://clawhub.ai/user/pexo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create TikTok-style video ads from product briefs and optional media assets through Pexo's hosted generation service. The agent coordinates project creation, uploads, status polling, user responses, revisions, and final asset delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Briefs and uploaded media are sent to Pexo's hosted service for video generation.

Mitigation: Use the skill only with briefs and media that are appropriate to share with Pexo.

Risk: The scripts require a PEXO_API_KEY and source ~/.pexo/config as shell code.

Mitigation: Store the API key with restrictive file permissions or a secrets manager, and inspect ~/.pexo/config before running the scripts.

Risk: PEXO_BASE_URL controls the endpoint used by the helper scripts.

Mitigation: Set PEXO_BASE_URL only to a trusted HTTPS Pexo endpoint.

Risk: Asset retrieval can write downloaded files into ~/.pexo/tmp or PEXO_TMP_DIR.

Mitigation: Use a trusted writable temp directory and treat downloaded generated assets according to the user's data handling requirements.

## Reference(s):

- [Pexo homepage](https://pexo.ai)
- [ClawHub skill page](https://clawhub.ai/pexo/skills/tiktok-video-ad)
- [Setup Checklist](references/SETUP-CHECKLIST.md)
- [Troubleshooting](references/TROUBLESHOOTING.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell command invocations and plain-text asset URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return JSON from helper scripts while orchestrating Pexo projects; final delivery is a full signed asset URL and project link.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
