## Description: <br>
Search and browse the x402 bazaar marketplace for paid API services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xRAG](https://clawhub.ai/user/0xRAG) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to search, browse, and inspect paid API services in the x402 bazaar marketplace before deciding whether to call an external service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs an unpinned npm CLI that contacts external x402 marketplace services. <br>
Mitigation: Install and use it only when external marketplace access and execution of the current npm CLI package are acceptable for the environment. <br>
Risk: Endpoint inspection may send POST, PUT, DELETE, or PATCH requests while checking payment requirements for arbitrary URLs. <br>
Mitigation: Inspect only trusted x402 endpoint URLs and review the target endpoint before running details commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0xRAG/search-for-service) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results may be cached locally by the underlying CLI and can be refreshed with the documented force-refresh option.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
