## Description: <br>
Token Guard helps agents estimate prompt token use and throttle model requests against local per-minute quota limits before API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edmonddantesj](https://clawhub.ai/user/edmonddantesj) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use Token Guard as a local Python helper before LLM API calls to estimate token demand, track usage, and return proceed, wait, block, or fallback decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Advertised duplicate detection, response caching, and 429 parser behavior are not fully supported by the reviewed implementation. <br>
Mitigation: Treat those features as unverified until implemented and reviewed; rely on the local quota-checking behavior that is present. <br>
Risk: Automatic fallback can switch important workflows to a different model. <br>
Mitigation: Review fallback decisions before enabling the helper in workflows where model choice affects quality, cost, or policy requirements. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and YAML examples; JSON status output from the helper script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local quota decisions and status data; no external dependencies are required.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata and artifact documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
