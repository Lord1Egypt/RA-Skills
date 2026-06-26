## Description: <br>
Generates and adjusts personalized daily triathlon training plans from TrainingPeaks, Garmin health data, race goals, and weather, with optional daily push or note export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ciaefengye](https://clawhub.ai/user/ciaefengye) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Triathletes or coaches use this skill to generate daily swim, bike, and run plans plus training recaps that adapt to race calendars, TrainingPeaks load metrics, Garmin readiness data, and weather. It is intended as training assistance and should be reviewed before acting on intense or health-sensitive recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access TrainingPeaks cookies, Garmin credentials, health metrics, workout history, weather lookups, and external note uploads. <br>
Mitigation: Grant access only after review, store credentials in environment variables or protected local files, and restrict cookie, token, and cache file permissions. <br>
Risk: The security scan reports weak credential boundaries, including IMA credential handling. <br>
Mitigation: Replace bundled or hardcoded IMA credentials with user-controlled secure configuration and rotate any exposed credentials before use. <br>
Risk: Generated training plans and recaps may include health or performance-sensitive data and may be uploaded externally. <br>
Mitigation: Inspect output destinations, disable external uploads unless needed, and review generated training guidance before following it. <br>


## Reference(s): <br>
- [Ai Coach on ClawHub](https://clawhub.ai/ciaefengye/triathlon-ai-coach) <br>
- [TrainingPeaks Web App](https://tpstack.trainingpeaks.com) <br>
- [IMA note import endpoint](https://ima.qq.com/openapi/note/v1/import_doc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown training plans and recaps, console text, and JSON configuration or cache files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local plan, health, and training cache files and upload Markdown note content when notification or IMA export is configured.] <br>

## Skill Version(s): <br>
3.2.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
