## Description: <br>
Validates token/auth JSON configuration files, optionally probes access tokens online, and produces redacted reports that classify configs as valid, no quota, or invalid. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joe12801](https://clawhub.ai/user/joe12801) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to validate batches of Codex/OpenAI-compatible token or auth JSON files, separate usable, no-quota, and invalid configs, and generate redacted troubleshooting reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Online probing can send live credentials over the network. <br>
Mitigation: Prefer offline checks first, use --probe only with trusted endpoints, and avoid custom probe URLs unless you control them. <br>
Risk: Saved bucket directories, report files, and index files may contain usable credentials or sensitive account metadata. <br>
Mitigation: Use a narrow input path, restrict access to generated files, and treat valid/no_quota/invalid outputs as sensitive. <br>


## Reference(s): <br>
- [Token Config Checker ClawHub page](https://clawhub.ai/joe12801/token-config-checker) <br>
- [Default OpenAI probe endpoint](https://api.openai.com/v1/models) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown/text guidance with shell commands; scripts can emit text reports, JSON lines, index.json, and copied configuration files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are intended to redact sensitive values, while optional saved valid/no_quota/invalid directories and index files may still contain sensitive credential material.] <br>

## Skill Version(s): <br>
1.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
