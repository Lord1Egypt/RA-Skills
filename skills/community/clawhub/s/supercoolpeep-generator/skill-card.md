## Description: <br>
Generate a SuperCoolPeep avatar from supercoolpeeps.com using a 68-digit seed and optional trait type like ape, skeleton, or zombie. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dbdbking](https://clawhub.ai/user/dbdbking) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to generate SuperCoolPeep avatar images for creative or profile-style workflows by running the included Node script with an optional seed and trait selection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script opens an external website through Puppeteer and depends on that site being available and trustworthy. <br>
Mitigation: Run it only in environments where access to supercoolpeeps.com is acceptable and review network access expectations before use. <br>
Risk: The script launches Chromium with no-sandbox flags and writes a PNG file into the current working directory. <br>
Mitigation: Install Puppeteer from a trusted source and run the script from a low-privilege working directory where local file output is expected. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/dbdbking/supercoolpeep-generator) <br>
- [SuperCoolPeeps website](https://supercoolpeeps.com) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [PNG image file with console status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a 68-digit seed and can bias generation toward ape, skeleton, or zombie traits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
