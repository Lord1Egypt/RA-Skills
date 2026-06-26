## Description: <br>
Template-driven RapidAPI client with auto-registered actions and a universal call entrypoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[web3aivc](https://clawhub.ai/user/web3aivc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation agents use this skill to call repeatable RapidAPI endpoints through named JSON templates or a direct RapidAPI request entrypoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The RapidAPI key can be sent to caller-chosen non-RapidAPI hosts when non-RapidAPI hosts are allowed. <br>
Mitigation: Set ALLOW_NON_RAPIDAPI_HOSTS=false unless other hosts are explicitly required, and review templates before use. <br>
Risk: RAPIDAPI_KEY is a paid-service secret that could require rotation if exposed. <br>
Mitigation: Provide the key through secret management or environment injection, restrict use to trusted callers, and rotate it if exposure is suspected. <br>
Risk: Direct ad hoc calls can reach endpoints outside the reviewed template set. <br>
Mitigation: Prefer reviewed action templates and avoid unreviewed direct calls in shared or production workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/web3aivc/rapidapi) <br>
- [Template schema documentation](docs/template-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [JSON responses with optional JavaScript and shell usage snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses template-defined query, body, header, and path parameters; requires RAPIDAPI_KEY for live calls.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence; artifact package.json reports 0.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
