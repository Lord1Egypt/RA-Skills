## Description: <br>
Score a specific trade show against a company profile using Lensmor to help decide whether to exhibit, attend, monitor, or skip. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weilun88313](https://clawhub.ai/user/weilun88313) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External B2B marketing, sales, and event teams use this skill to request a quantified Lensmor fit score for a named trade show or event ID before committing exhibit, attendance, or travel budget. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a Lensmor account, company profile, and API key, so event scores may expose or depend on sensitive company profile data stored in Lensmor. <br>
Mitigation: Confirm Lensmor is trusted for the intended data, use a scoped API key where possible, and avoid sharing the API key in prompts or outputs. <br>
Risk: Fit scores and recommendations can influence exhibit, travel, and budget decisions but are still recommendations rather than final business decisions. <br>
Mitigation: Review score cards against internal strategy, budget constraints, and current event facts before committing spend. <br>
Risk: API usage may be subject to billing, rate limits, invalid credentials, incomplete company profiles, or transient service errors. <br>
Mitigation: Check account terms and limits before broad use, handle Lensmor error responses explicitly, and retry transient failures only when appropriate. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/weilun88313/trade-show-fit-score) <br>
- [Publisher profile](https://clawhub.ai/user/weilun88313) <br>
- [Lensmor platform](https://platform.lensmor.com) <br>
- [Lensmor API documentation](https://api.lensmor.com/) <br>
- [Lensmor event intelligence](https://www.lensmor.com/?utm_source=github&utm_medium=skill&utm_campaign=trade-show-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown score card with a decision band, per-dimension scores, recommendation text, and follow-up guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LENSMOR_API_KEY and uses Lensmor event lookup and fit-score responses; scores and breakdown values should come directly from the API.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
