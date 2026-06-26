## Description: <br>
Generate, review, and export tailored application materials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanghong5233](https://clawhub.ai/user/wanghong5233) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job applicants and career-support agents use this skill to generate tailored resume bullets, cover letters, and greeting messages for a job, review the draft with explicit approval or regeneration, and export approved materials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends job and resume-version inputs to a local service on 127.0.0.1:8010, and an unexpected process on that port could receive or return application-material data. <br>
Mitigation: Install and use the skill only when the expected resume-tailoring service is running on that port, and do not proceed if an unknown process is listening there. <br>
Risk: Generated resumes and cover letters may contain inaccurate, overstated, or unsuitable application content. <br>
Mitigation: Review every generated resume bullet, cover letter, and greeting message before approving or exporting materials. <br>


## Reference(s): <br>
- [Resume Tailor ClawHub page](https://clawhub.ai/wanghong5233/wanghong5233-offerpilot-resume-tailor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with JSON request examples, curl commands, reviewed draft content, and exported file path or download URL details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Calls a disclosed local resume-tailoring service on 127.0.0.1:8010 and requires explicit user confirmation before approve, reject, regenerate, or export actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
