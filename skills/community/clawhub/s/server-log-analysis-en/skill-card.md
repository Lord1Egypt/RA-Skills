## Description: <br>
Connect to remote servers over SSH, read sibling config.yaml to understand service metadata and log locations, download only required log snippets to local temp for analysis, and diagnose issues from evidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hgvgfgvh](https://clawhub.ai/user/hgvgfgvh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to troubleshoot remote service incidents by using configured service metadata and log paths to scope SSH checks, retrieve minimal log snippets, and produce an evidence-based diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The example SSH configuration uses root and password-style credential fields. <br>
Mitigation: Replace example credentials with a least-privileged account and a secure secret source such as SSH keys, environment variables, or a vault before installation. <br>
Risk: Downloaded logs are kept locally by default and may contain sensitive operational data. <br>
Mitigation: Limit collection to the smallest useful snippets, protect local temp files, and delete or archive them according to the incident handling policy after troubleshooting. <br>
Risk: SSH-based investigation can inspect the wrong host, service, log path, or time window if configuration is stale. <br>
Mitigation: Confirm the target host, service, log files, and time window before running remote checks or copying logs. <br>


## Reference(s): <br>
- [Reference Notes](artifact/reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/hgvgfgvh/server-log-analysis-en) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown diagnosis with evidence, confidence, and suggested next steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include proposed SSH log-check commands and references to locally downloaded log snippets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
