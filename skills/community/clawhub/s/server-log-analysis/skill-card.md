## Description: <br>
Connects to remote servers over SSH, reads config.yaml for service and log locations, downloads targeted log segments to a local temp directory, and analyzes them to diagnose server issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hgvgfgvh](https://clawhub.ai/user/hgvgfgvh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to investigate remote service failures by selecting configured services, fetching minimal relevant log segments, and producing a concise diagnosis with evidence and next-step checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release security summary flags templated root SSH/password access. <br>
Mitigation: Replace sample credentials with a least-privileged read-only SSH account and prefer SSH keys or environment-backed secrets before use. <br>
Risk: The release security summary notes that downloaded logs are preserved locally. <br>
Mitigation: Confirm the host, service, log paths, and time window before collection, and delete downloaded log copies when they are no longer needed. <br>


## Reference(s): <br>
- [reference.md](reference.md) <br>
- [ClawHub skill page](https://clawhub.ai/hgvgfgvh/server-log-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown diagnostic report with evidence, confidence, and recommended next steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local log segment files under temp/server-log-analysis according to the skill configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
