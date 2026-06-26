## Description: <br>
AI-powered video editing guidance that routes users to the right Sparki workflow for vlogs, highlights, short-form clips, captions, montages, and related video-editing tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fischerlam](https://clawhub.ai/user/fischerlam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to choose the right Sparki video-editing skill, configure the Sparki CLI, upload local or Telegram Mini App videos, start edits, check status, and download results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded videos are processed by Sparki cloud services. <br>
Mitigation: Only upload videos intended for Sparki processing and avoid sensitive footage unless the user trusts the service. <br>
Risk: The skill relies on a Sparki API key that can be stored locally or read from SPARKI_API_KEY. <br>
Mitigation: Protect the API key, prefer environment-based configuration when appropriate, and revoke or rotate it if exposure is suspected. <br>
Risk: Edited videos may be downloaded to local paths chosen by the agent or user. <br>
Mitigation: Use explicit output paths only where the user wants edited video files saved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fischerlam/which-sparki-skill) <br>
- [Sparki homepage](https://sparki.io) <br>
- [Sparki Telegram bot](https://t.me/Sparki_AI_bot) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with bash command examples and structured JSON CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Sparki API key, may upload video files to Sparki cloud services, and may save edited videos to a local output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, pyproject.toml, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
