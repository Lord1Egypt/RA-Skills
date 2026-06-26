## Description: <br>
Senseguard scans OpenClaw skills for prompt injection, data exfiltration, hidden instructions, and other natural-language security risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fermionoid](https://clawhub.ai/user/fermionoid) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security reviewers use Senseguard to scan OpenClaw skills before installation or deployment, with a focus on natural-language instructions that conventional malware scanners may miss. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner may report safe semantic results when Layer 2 semantic analysis was not actually performed. <br>
Mitigation: Treat Senseguard as a local rule-based scanner unless the generated Layer 2 audit has been manually performed and integrated. <br>
Risk: Security decisions can be misleading if users rely on a single scanner verdict. <br>
Mitigation: Review findings before relying on the result, use narrow scan targets, and treat clean VirusTotal results as only one signal. <br>
Risk: Scan caching can retain results for private skill targets. <br>
Mitigation: Use --no-cache or a controlled --cache-file when scanning private or sensitive skills. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fermionoid/senseguard) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown risk report with optional JSON scan output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include a 0-100 score, SAFE/CAUTION/DANGEROUS/MALICIOUS rating, findings, evidence snippets, line numbers, and recommendations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
