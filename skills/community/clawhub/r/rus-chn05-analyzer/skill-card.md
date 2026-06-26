## Description: <br>
Analyzes hand or wrist X-ray images with the HuiLingYun RUS-CHN05 bone-age service to estimate bone age, support height prediction, and draft a Chinese bone-age assessment report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[povoss](https://clawhub.ai/user/povoss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to a third-party bone-age analysis workflow for children and adolescents, collect required inputs, upload X-ray images, interpret returned scores, and draft a non-diagnostic Chinese report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send children's X-ray images and personal data to a third-party medical analysis service. <br>
Mitigation: Use it only with authority to submit the data, confirm guardian consent, prefer the lightweight path when possible, and avoid real phone numbers or identifiers unless required. <br>
Risk: Service credentials and tokens are required for API calls. <br>
Mitigation: Keep credentials scoped to the HuiLingYun service, store them outside prompts and reports, and rotate or revoke them if exposed. <br>
Risk: History lookup may expose patient records associated with the service account. <br>
Mitigation: Avoid history lookup unless the account is known to contain only the intended patient records. <br>
Risk: Bone-age and height-prediction outputs may be mistaken for a medical diagnosis. <br>
Mitigation: Present results as AI-assisted reference material and direct users to qualified clinicians for medical decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/povoss/rus-chn05-analyzer) <br>
- [HuiLingYun bone-age service](https://www.pipitu.net) <br>
- [API protocol reference](references/api-protocol.md) <br>
- [Python API client](scripts/bone_age_api_client.py) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown report guidance with JSON API request examples, Python helper code, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended for Chinese-language bone-age reporting and API integration; execution can require service credentials and transmission of medical images and personal data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
