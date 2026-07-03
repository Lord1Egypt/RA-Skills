## Description: <br>
Triage and answer support requests for the xrow-public/ci-tools GitLab components catalog. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xrowgmbh](https://clawhub.ai/user/xrowgmbh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Support engineers and agents use this skill to triage GitLab support issues or discussions for the CI Tools components catalog, answer from public evidence, and hand off requests that are private, unsafe, or outside scope. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Support replies could expose private customer details, private URLs, private logs, or internal project names if handled in a public thread. <br>
Mitigation: Confirm confidentiality before replying, avoid quoting private logs into public places, and hand off private customer-system cases to a human maintainer. <br>
Risk: The skill could provide support to untrusted requesters or for harmful, credential-recovery, access-bypass, or unrelated requests. <br>
Mitigation: Require SUPPORT_TRUSTED_DOMAINS to be configured correctly, verify CI Tools scope, refuse or hand off unsafe requests, and grant only the GitLab permissions needed for support replies and labels. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xrowgmbh/skills/xrowgmbh-ci-tools-support) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or text support replies with source citations and triage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses SUPPORT_TRUSTED_DOMAINS to gate eligible requester domains before providing support.] <br>

## Skill Version(s): <br>
4.156.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
