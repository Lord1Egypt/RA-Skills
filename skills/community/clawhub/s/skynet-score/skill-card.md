## Description: <br>
Use for searching CertiK Skynet project scores, looking up blockchain project security ratings, comparing score breakdowns, and integrating the public Skynet project search endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[certik-ai](https://clawhub.ai/user/certik-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to search blockchain projects by keyword and summarize CertiK Skynet scores, tiers, update times, and score breakdowns. It can also provide minimal Python or curl examples for integrating the public project search endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends project keywords supplied by the user to CertiK's public API. <br>
Mitigation: Avoid submitting confidential or sensitive project names unless sharing them with CertiK's public API is acceptable. <br>
Risk: The skill relies on executing a bundled Python script with outbound HTTPS access. <br>
Mitigation: Review the script and run it only in environments where outbound requests to open.api.certik.com are permitted. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/certik-ai/skynet-score) <br>
- [CertiK public project API](https://open.api.certik.com/projects) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown summaries with optional bash, Python, curl, or JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns score data from CertiK's public API and should not invent scores when no match is returned.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
