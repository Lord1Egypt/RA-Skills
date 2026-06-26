## Description: <br>
Creates video ads with Pexo from a product brief, brand details, or uploaded media, then returns project updates and final asset links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pexo](https://clawhub.ai/user/pexo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing teams, founders, and agents supporting commercial promotion use this skill to create Pexo video-ad projects from briefs or uploaded assets, manage revisions, and deliver the completed video link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, ad briefs, product details, and uploaded media are sent to Pexo's hosted service. <br>
Mitigation: Avoid sending secrets or regulated data, and confirm uploaded assets are appropriate to share with Pexo. <br>
Risk: The skill requires a Pexo API key stored in configuration. <br>
Mitigation: Keep ~/.pexo/config private, restrict file permissions, and rotate the API key if it may have been exposed. <br>
Risk: Running video generation can consume Pexo credits. <br>
Mitigation: Check account credits before starting work and confirm that the user wants to proceed when credit or purchase prompts appear. <br>


## Reference(s): <br>
- [Video Ad on ClawHub](https://clawhub.ai/pexo/video-ad) <br>
- [Pexo](https://pexo.ai) <br>
- [Pexo Publisher Profile](https://clawhub.ai/user/pexo) <br>
- [Setup Checklist](artifact/references/SETUP-CHECKLIST.md) <br>
- [Troubleshooting](artifact/references/TROUBLESHOOTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain-text status messages with shell command usage and final asset URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PEXO_API_KEY and PEXO_BASE_URL; video generation runs through Pexo's hosted service and may consume account credits.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
