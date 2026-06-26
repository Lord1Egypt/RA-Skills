## Description: <br>
Guides an agent through collecting recent research-report metadata, asking for report requirements, and drafting customized market-analysis summaries. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[meidetong](https://clawhub.ai/user/meidetong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users can use this skill to draft Chinese-language market research summaries from recent report metadata with a custom outline, focus area, style, and audience. It is best treated as an exploratory report-writing workflow, not proof that source reports were downloaded or reviewed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make users believe real logins, downloads, and PDF reports happened when the scripts mostly simulate those steps. <br>
Mitigation: Treat generated reports as drafts and verify every cited source, downloaded file, and output format before relying on the result. <br>
Risk: The workflow asks for website credentials while the security guidance says real scoped authentication is not implemented. <br>
Mitigation: Avoid valuable site credentials unless the skill is updated to perform scoped authentication, verified downloads, and truthful output reporting. <br>


## Reference(s): <br>
- [Workflow guide](references/workflow_guide.md) <br>
- [ClawHub release page](https://clawhub.ai/meidetong/report-writing-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown report files and console progress text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The artifact claims PDF delivery, but the current scripts save Markdown output and may create metadata placeholders when authenticated downloads are unavailable.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence; artifact docs identify v1.03) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
