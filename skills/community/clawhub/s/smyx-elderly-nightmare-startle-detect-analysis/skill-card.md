## Description: <br>
This skill analyzes fixed infrared bedroom camera video with microphone audio to detect elderly nighttime startle and nightmare-related behaviors, including sudden sitting up, screams, and arm thrashing, and reports event timing, frequency, and duration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Caregivers, elder-care operators, and developers use this skill to submit fixed-camera nighttime sleep video or audio/video URLs for behavioral event statistics, family-facing summaries, and prior report retrieval. The outputs are observational sleep-event records and referral guidance, not medical diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive bedroom audio/video may be uploaded or forwarded to external services for analysis. <br>
Mitigation: Use only with explicit consent from the monitored person and only when the publisher and processing service are trusted. <br>
Risk: Reports and analysis activity may be associated with an open-id that can be a phone number or username. <br>
Mitigation: Use a minimally identifying open-id when possible and review account, retention, and access controls before deployment. <br>
Risk: Local credential storage and prior report retrieval can expose historical health-related records. <br>
Mitigation: Protect local configuration files, restrict workspace access, and review report history access before installing or running the skill. <br>
Risk: Behavioral event classifications could be mistaken for medical diagnoses. <br>
Mitigation: Treat outputs as observational records only and route repeated or concerning patterns to qualified neurology or sleep-medicine professionals. <br>


## Reference(s): <br>
- [Elderly sleep nightmare/startle API documentation](artifact/references/api_doc.md) <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/smyx-elderly-nightmare-startle-detect-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON text containing sleep-event counts, timelines, report links, summaries, and suggested next actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local file or URL input handling, cloud report lookup, and optional output-file writing.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
