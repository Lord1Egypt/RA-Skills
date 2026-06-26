## Description: <br>
Automatically find remote jobs every day, score them against a resume, identify skill gaps, and prepare or submit applications for strong matches with JD-tailored resume support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RajkiranVS](https://clawhub.ai/user/RajkiranVS) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and job seekers use this skill to automate remote job discovery, compare openings with their resume, review skill gaps, generate daily summaries, and manage application workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes auto-apply behavior that can send resumes and application data externally. <br>
Mitigation: Use dry-run, report-only, or no-auto-apply modes until each target job and destination is reviewed and approved. <br>
Risk: Application workflows may use SMTP, LinkedIn, browser automation, resume uploads, and local application records. <br>
Mitigation: Confirm account permissions, outbound data flows, and local retention expectations before enabling application submission. <br>
Risk: Documentation is inconsistent about whether auto-apply behavior is included. <br>
Mitigation: Treat the executable artifact behavior and security evidence as authoritative, and require clear user approval before submission actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/RajkiranVS/remote-job-hunter) <br>
- [Publisher Profile](https://clawhub.ai/user/RajkiranVS) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, configuration, guidance] <br>
**Output Format:** [Markdown reports, plain-text summaries, JSON application state, and local resume or application files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local reports, pending-application records, tailored resumes, and application logs based on user configuration.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
