## Description: <br>
Records user-provided listing, SEO, and advertising outcome metrics against a prior Yufluent run_id for later attribution and optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[metahuan](https://clawhub.ai/user/metahuan) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External sellers and ecommerce agents use this skill to register post-publication outcomes, such as sales, impressions, clicks, and revenue, for a previously returned Yufluent run_id. It supports outcome tracking when a direct record_outcome tool is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a sensitive TOKENAPI_KEY and submits business outcome metrics to a remote service. <br>
Mitigation: Keep the token narrowly scoped and require confirmation of the run_id, event type, metrics, and destination before submission. <br>
Risk: A changed TOKENAPI_BASE_URL could redirect submitted outcome data to an unintended backend. <br>
Mitigation: Control TOKENAPI_BASE_URL in the execution environment and install the skill only when the configured backend is trusted. <br>
Risk: Security evidence notes helper capabilities broader than the stated outcome-recording purpose. <br>
Mitigation: Review whether generic remote skill execution helpers are needed before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/metahuan/yufluentcn-record-outcome) <br>
- [Yufluent homepage](https://claw.changzhiai.com) <br>
- [OpenClaw app](https://claw.changzhiai.com/app/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [CLI status text or JSON response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TOKENAPI_KEY and submits user-provided outcome metrics to the configured Yufluent API.] <br>

## Skill Version(s): <br>
1.1.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
