## Description: <br>
Searches JisuAPI trademark records by keyword, registration number, applicant, or class and retrieves trademark details such as registrant, category, announcements, and status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to check whether trademarks are registered, identify registrants, and retrieve details for a specific application or registration number. It requires a user-provided JisuAPI AppKey. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trademark search terms, registration numbers, and related identifiers are sent to JisuAPI under the user's AppKey. <br>
Mitigation: Avoid confidential brand research unless JisuAPI's privacy, retention, and billing terms are acceptable. <br>
Risk: The skill depends on a third-party API key, quota, permissions, and service availability. <br>
Mitigation: Configure JISU_API_KEY before use and handle API errors, quota limits, and no-result responses in downstream workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/trademark) <br>
- [JisuAPI trademark documentation](https://www.jisuapi.com/api/trademark/) <br>
- [JisuAPI](https://www.jisuapi.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration] <br>
**Output Format:** [JSON responses and Markdown usage guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; sends lookup terms and identifiers to JisuAPI.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
