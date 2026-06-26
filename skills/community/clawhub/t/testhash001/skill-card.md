## Description: <br>
Log meals, check nutrition, manage medications, and view daily health dashboard via Hash Health. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devak208](https://clawhub.ai/user/devak208) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to log meals, review nutrition totals, manage medication records, and summarize daily health information through Hash Health. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send sensitive food, nutrition, medication, and user identifier data to an external API. <br>
Mitigation: Use it only with trusted Hash Health accounts and avoid sending health details you do not want stored remotely. <br>
Risk: The skill can add or delete meal and medication records. <br>
Mitigation: Require explicit user confirmation before saving or deleting any record, and look up record IDs instead of guessing them. <br>
Risk: A misconfigured HASH_HEALTH_USER_ID could expose or modify the wrong user's health records. <br>
Mitigation: Verify HASH_HEALTH_USER_ID before use and avoid logging the identifier or retrieved health details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/devak208/testhash001) <br>
- [Publisher profile](https://clawhub.ai/user/devak208) <br>
- [Hash Health API endpoint](https://hash-claude-mcp.vercel.app) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Guidance] <br>
**Output Format:** [Markdown and text responses with JSON API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires HASH_HEALTH_USER_ID and uses an external API for meal, nutrition, and medication records.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
