## Description: <br>
Patient-side chronic disease medication reminder skill that builds structured medication schedules and reminder lists from medication plan inputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to turn medication names, doses, frequencies, reminder times, and date ranges into structured medication reminder schedules and daily reminder summaries. The skill is for reminder management only and does not determine medication suitability or adjust medical orders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles medication-related information and can process imported medical documents before sending reminder prompts to a remote medical-model endpoint. <br>
Mitigation: Use only with appropriate consent, privacy, and compliance controls; avoid real patient or regulated health data unless those controls are in place. <br>
Risk: The skill provides reminder content but does not provide clinical review, medication suitability checks, or prescription changes. <br>
Mitigation: Use the output for reminder management only and have medication plans verified by qualified healthcare professionals. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-medication-reminder) <br>
- [MedTimer reference app](https://f-droid.org/en/packages/com.futsch1.medtimer/) <br>
- [Remote medical model endpoint](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [UTF-8 JSON containing structured reminder data and Markdown reminder text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an appkey Bearer token and sends prepared medication reminder prompts to a remote medical-model API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
