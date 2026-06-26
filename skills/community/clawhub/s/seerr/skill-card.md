## Description: <br>
Search for movies and TV shows through a Seerr instance, check availability, and request unavailable titles for download through Radarr or Sonarr. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ximga](https://clawhub.ai/user/ximga) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and media server operators use this skill to search Seerr for movies or TV shows, show result details in Discord, and submit media requests to a configured Seerr, Radarr, and Sonarr stack. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unavailable movies or shows may be automatically queued in Seerr, which can trigger real downloads through Radarr or Sonarr. <br>
Mitigation: Require confirmation of the exact movie or show before submitting request API calls, especially on production Seerr instances. <br>
Risk: The skill requires SEERR_URL and SEERR_API_KEY for authenticated Seerr API access. <br>
Mitigation: Store credentials only in the agent environment, keep them out of chat, and use a limited API key where possible. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ximga/seerr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown and plain text messages with inline JSON or bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Discord messages with poster media links and Seerr status or request confirmations.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
