## Description: <br>
Skin Pro calls the RageHealth /face/skin-pro API to analyze face photos for more than 28 skin indicators, including oil and water balance, pores, spots, sensitivity, wrinkles, blackheads, acne, dark circles, eye bags, skin type, skin age, and overall score. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qianchen94](https://clawhub.ai/user/qianchen94) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents assisting external users use this skill when a consenting person provides a front-facing face photo and asks for skin analysis, skin-age estimation, skin scoring, or issue-specific checks for pores, acne, spots, wrinkles, sensitivity, blackheads, dark circles, or eye bags. The skill returns quality-gated, non-diagnostic skin-analysis results and care guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends sensitive face photos to RageHealth for automated skin analysis. <br>
Mitigation: Use it only when the photographed person has explicitly consented, and do not analyze other people's faces without permission. <br>
Risk: Face ID detection can increase identity and tracking sensitivity. <br>
Mitigation: Keep face ID detection disabled unless there is a clear need and explicit consent for that use. <br>
Risk: Credentials are required to call the API. <br>
Mitigation: Keep SKIN_PRO_AK and SKIN_PRO_SK private, inject them through environment variables, and never include them in prompts, command arguments, logs, or user-facing responses. <br>
Risk: The script accepts a custom endpoint, which could redirect face photos and credentials to an unintended destination. <br>
Mitigation: Use the default RageHealth endpoint unless the alternative endpoint is fully trusted. <br>
Risk: Skin-analysis output can be mistaken for medical or dermatology diagnosis. <br>
Mitigation: State that results are for reference only and recommend in-person professional care for serious skin concerns. <br>


## Reference(s): <br>
- [Skin Pro response schema](references/response_schema.md) <br>
- [RageHealth skin-pro API endpoint](https://facepro.ragehealth.cn/openapi-test/face/skin-pro) <br>
- [RageHealth credential portal](https://chayan-test.ragehealth.cn/client) <br>
- [ClawHub release page](https://clawhub.ai/qianchen94/skin-pro) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON API responses and Markdown skin-analysis reports with optional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write JSON output to a requested file; compact summaries omit polygons, landmarks, and face maps.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
