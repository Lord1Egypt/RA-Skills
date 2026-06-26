## Description: <br>
Verify the optional local Switchyard runtime path without changing Campus-owned response semantics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaojiou176](https://clawhub.ai/user/xiaojiou176) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to check whether a local Campus/Switchyard runtime is ready and to keep any follow-on interaction within Campus response semantics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents may query local Campus or Switchyard API endpoints in environments where that access is not intended. <br>
Mitigation: Confirm before installation that agents using this skill are allowed to reach the local Campus/Switchyard /api endpoints. <br>
Risk: A response could misrepresent raw upstream provider payloads as Campus-owned response semantics. <br>
Mitigation: Keep responses constrained to the Campus fields named by the skill: answerText, optional structuredAnswer, nextActions, trustGaps, and citations. <br>


## Reference(s): <br>
- [Switchyard Runtime Check on ClawHub](https://clawhub.ai/xiaojiou176/switchyard-runtime-check) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, text] <br>
**Output Format:** [Markdown guidance with endpoint names and response-field checks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instructs the agent to check local runtime readiness and preserve named Campus response fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
