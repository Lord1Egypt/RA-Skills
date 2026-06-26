## Description: <br>
SecureVibes Scanner helps agents run AI-powered application security scans, threat models, code reviews, incremental scans, and continuous monitoring for local codebases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anshumanbh](https://clawhub.ai/user/anshumanbh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security engineers use this skill to scan authorized local repositories, generate threat models and vulnerability reports, review code changes, and configure recurring incremental security checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and invokes the third-party securevibes CLI and uses an Anthropic OAuth session or API key. <br>
Mitigation: Verify that the securevibes package and the selected Anthropic account or API key are trusted before installing or running scans. <br>
Risk: Full scans and optional DAST can inspect code and make network requests to configured targets. <br>
Mitigation: Run scans only against repositories and web targets you own or are authorized to test, and enable DAST only deliberately with the intended target URL. <br>
Risk: Cron-based incremental monitoring performs recurring background scans and writes .securevibes state, logs, and reports. <br>
Mitigation: Create the cron job only when ongoing monitoring is intended, use an isolated session where available, and review generated logs and reports. <br>


## Reference(s): <br>
- [SecureVibes website](https://securevibes.ai) <br>
- [SecureVibes PyPI package](https://pypi.org/project/securevibes/) <br>
- [SecureVibes GitHub repository](https://github.com/anshumanbh/securevibes) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and scan-result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference SecureVibes-generated .securevibes reports, JSON findings, logs, and incremental scan state files.] <br>

## Skill Version(s): <br>
0.5.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
