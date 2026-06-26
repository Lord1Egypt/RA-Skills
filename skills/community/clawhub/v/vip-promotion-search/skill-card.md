## Description: <br>
Queries Vipshop promotion activity data and summarizes current or upcoming campaigns, including activity names, timing, brands, links, images, status, and activity types. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vip](https://clawhub.ai/user/vip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and shopping assistants use this skill to retrieve and present Vipshop promotion campaigns, grouped by status and activity type, when a user asks about current or upcoming discounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may automatically install or run a separate Vipshop login skill and start QR-code login when it detects no valid session. <br>
Mitigation: Require explicit user approval before installing or invoking any login skill, and proceed only when the user intentionally requested Vipshop account access. <br>
Risk: The skill reads a stored Vipshop session token and sends it to a Vipshop API endpoint to query promotion data. <br>
Mitigation: Install and run it only when the user is comfortable using their Vipshop login session for promotion lookup, and avoid using it for non-Vipshop shopping-platform requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vip/vip-promotion-search) <br>
- [Vipshop promotion activity API endpoint](https://api.union.vip.com/vsp/common/getActListForAI) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [JSON from the script, typically transformed by the agent into concise Markdown or text summaries for the user] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes promotion counts, status and type groupings, activity names, time ranges, brand descriptions, links, images, and raw API data when available.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
