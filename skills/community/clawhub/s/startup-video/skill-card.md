## Description: <br>
Startup Video helps an agent submit a user's startup brief, site, or media to Pexo so Pexo can generate a publish-ready brand or intro video with script, shots, model choices, music, and subtitles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pexo](https://clawhub.ai/user/pexo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and startup teams use this skill through an agent to request homepage, fundraising deck, social, brand, or intro videos. The agent creates a Pexo project, uploads provided media, relays the user's request, polls for status, and returns the final asset URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends startup descriptions, website content, and uploaded media to Pexo's hosted service. <br>
Mitigation: Use only with information approved for sharing with Pexo; avoid confidential or regulated data unless the user's policy allows it. <br>
Risk: The skill uses a Pexo API key stored in a plaintext shell-sourced config file. <br>
Mitigation: Protect ~/.pexo/config as a secret file, restrict local permissions, and rotate the API key if the file may have been exposed. <br>
Risk: The skill can consume credits or trigger paid-service workflows. <br>
Mitigation: Confirm the user's intent and credit status before starting production or retrying after credit-related errors. <br>


## Reference(s): <br>
- [Pexo homepage](https://pexo.ai) <br>
- [ClawHub skill page](https://clawhub.ai/pexo/startup-video) <br>
- [Setup Checklist](references/SETUP-CHECKLIST.md) <br>
- [Troubleshooting](references/TROUBLESHOOTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and plain-text project or asset URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return JSON from helper scripts while polling project state or fetching assets.] <br>

## Skill Version(s): <br>
0.1.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
