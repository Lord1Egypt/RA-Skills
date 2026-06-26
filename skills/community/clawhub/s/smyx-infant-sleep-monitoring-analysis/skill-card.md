## Description: <br>
Analyzes infant sleep-monitoring videos to identify deep sleep, light sleep, waking, and restlessness, then generates sleep reports and routine analysis for caregivers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Caregivers and agents use this skill to analyze infant sleep-monitoring video or video URLs, summarize sleep state durations and wake events, and retrieve cloud-stored historical sleep reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Baby-monitoring videos or URLs, user identifiers, and report history requests are sent to the provider's cloud service. <br>
Mitigation: Use only with informed caregiver consent, minimize the video and identifier data submitted, and review the provider's data handling and retention terms before deployment. <br>
Risk: Account creation, token storage, report history access, and data retention behavior are under-disclosed in the available evidence. <br>
Mitigation: Verify these behaviors with the provider and restrict credentials and report access until they are clearly documented. <br>
Risk: The security evidence flags the release as suspicious and calls out a dependency issue requiring review. <br>
Mitigation: Resolve the dependency issue, scan the package in the target environment, and test it in a sandbox before installing it for regular use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/smyx-infant-sleep-monitoring-analysis) <br>
- [API 接口文档](references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports and tables, JSON responses, and CLI command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can output local or URL-based video analysis results and historical report lists; reports are for caregiver reference and are not medical advice.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence; artifact frontmatter reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
