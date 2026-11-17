## Description:

Zopia Skills helps agents manage Zopia projects for AI video and image creation, including project setup, script, character, storyboard, progress polling, media download, and final episode rendering workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lambdua](https://clawhub.ai/user/lambdua)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to operate Zopia's project-based AI video creation flow from an agent, including configuring projects, sending creative requests, tracking generation status, downloading generated media, and rendering completed episodes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Zopia account token and can submit prompts, project data, and credit-consuming generation requests to Zopia.

Mitigation: Use a dedicated ZOPIA_ACCESS_KEY with limited balance where possible, and review requests before spending credits.

Risk: Changing ZOPIA_BASE_URL can redirect authenticated requests away from the official service.

Mitigation: Leave ZOPIA_BASE_URL at the default official HTTPS endpoint unless intentionally testing a trusted environment.

Risk: The skill downloads remote generated media to local paths.

Mitigation: Review the output directory, media type, and downloaded file list; rely on the script's file-size cap for large media.

Risk: Episode deletion is irreversible according to the artifact behavior.

Mitigation: Confirm the target episode ID and project context before running delete operations.

## Reference(s):

- [Zopia platform](https://zopia.ai)
- [Zopia Skills on ClawHub](https://clawhub.ai/lambdua/skills/zopia-skill)
- [lambdua publisher profile](https://clawhub.ai/user/lambdua)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands, JSON command results, project links, and downloaded image or video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and ZOPIA_ACCESS_KEY; generated media downloads are capped by the skill's download script at 200 MB per file.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
