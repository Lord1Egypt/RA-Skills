## Description: <br>
Unified query router combining content-type detection, complexity scoring, and prefix-based routing to recommend or route queries to a model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[walterwkchoy](https://clawhub.ai/user/walterwkchoy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to classify queries by prefix, content type, and complexity, then receive a recommended model route or a routed action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may overstate model-switching, verification, and rollback safety. <br>
Mitigation: Use dry-run or recommendation mode for sensitive workflows and independently verify the active model before relying on a route. <br>
Risk: Local audit logs can store query snippets. <br>
Mitigation: Avoid routing secrets, private code, or regulated data unless local logging is acceptable, and review or clear audit logs as needed. <br>
Risk: Recommended routes use cloud-hosted models for most query types. <br>
Mitigation: Do not route confidential inputs through the skill unless the selected cloud model and data handling are approved for that use. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, code, guidance] <br>
**Output Format:** [Plain text or JSON from command-line scripts, plus Python dictionary results for library usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local JSONL audit entries containing truncated query snippets when routing or recommending.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
