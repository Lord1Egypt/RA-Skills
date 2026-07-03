## Description: <br>
Analyzes living-room video of an older adult watching TV to estimate continuous seated viewing time and generate a friendly activity reminder when the configured sedentary threshold is exceeded. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill in eldercare, nursing-home, community-care, or home-monitoring workflows to analyze TV-watching posture duration and produce structured reports, reminders, and report links. It is intended for behavior monitoring and friendly activity prompts, not medical diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends sensitive in-home eldercare video and historical report queries to cloud services. <br>
Mitigation: Use only with informed consent from the monitored person or guardian, avoid unauthorized third-party video URLs, and confirm that cloud processing is acceptable for the deployment. <br>
Risk: The skill may create or reuse local identity state and cache tokens in a workspace SQLite database. <br>
Mitigation: Run it in a controlled workspace, restrict access to local data files, and clear or rotate workspace state according to the operator's privacy and retention policy. <br>
Risk: Video-based posture and TV-orientation analysis can be affected by camera placement, multiple people, visitors, pets, lighting, or ambiguous activity. <br>
Mitigation: Review the generated report before acting on it, ensure the camera covers the sofa and TV direction clearly, and treat reminders as behavior prompts rather than medical advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-elderly-tv-sedentary-reminder-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [API interface documentation](references/api_doc.md) <br>
- [Shared analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and JSON analysis output with report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can process local video files or video URLs and can write the returned analysis output to a file when requested.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
