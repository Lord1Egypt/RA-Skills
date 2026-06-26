## Description: <br>
Deep distributed tracing workflow guidance for instrumentation boundaries, context propagation, sampling, tail-based analysis, service maps, and latency debugging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mikeclaw007](https://clawhub.ai/user/mikeclaw007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site reliability engineers use this skill to plan and operate distributed tracing for microservices, OpenTelemetry adoption, service maps, latency debugging, and trace cost governance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Applying tracing guidance in production can expose PII or secrets in span attributes. <br>
Mitigation: Review and enforce PII redaction, secret exclusion, and attribute limits before rollout. <br>
Risk: Unbounded tracing volume, retention, or sampling changes can increase storage cost or hide important error traces. <br>
Mitigation: Set sampling, retention, and budget policies that preserve errors and latency outliers while controlling trace volume. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mikeclaw007/tracing) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown] <br>
**Output Format:** [Markdown workflow guidance and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance with no code execution, credential use, or persistence indicated by security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
