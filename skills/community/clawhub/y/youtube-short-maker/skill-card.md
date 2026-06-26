## Description: <br>
Make YouTube Shorts with Pexo by relaying a user's topic or media to the hosted Pexo video agent, which writes the script, generates shots, chooses models, and assembles a finished vertical video with music and captions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pexo](https://clawhub.ai/user/pexo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to create short-form YouTube videos through Pexo, including project creation, optional media upload, polling, revision handling, and delivery of the generated video URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User prompts, uploaded media, generated projects, and output assets are sent to the hosted Pexo service. <br>
Mitigation: Review before using sensitive prompts or private media, and only upload content appropriate for processing by Pexo. <br>
Risk: The skill requires a Pexo API key stored in a persistent local config file. <br>
Mitigation: Protect ~/.pexo/config with restrictive permissions, avoid pointing PEXO_CONFIG at untrusted files, and rotate the API key if the config may have been exposed. <br>
Risk: Video creation can consume Pexo credits or require paid top-ups. <br>
Mitigation: Check credit status before production use and confirm spending-sensitive actions with the account owner. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pexo/youtube-short-maker) <br>
- [Pexo homepage](https://pexo.ai) <br>
- [Setup Checklist](references/SETUP-CHECKLIST.md) <br>
- [Troubleshooting](references/TROUBLESHOOTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON responses, status text, and plain-text asset URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PEXO_API_KEY and PEXO_BASE_URL; generated projects, uploaded files, and prompts are sent to Pexo.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
