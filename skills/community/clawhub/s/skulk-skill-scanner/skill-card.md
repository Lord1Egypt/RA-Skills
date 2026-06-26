## Description: <br>
Skulk Skill Scanner scans OpenClaw skill folders for static security red flags before install, publishing, or review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AdaInTheLab](https://clawhub.ai/user/AdaInTheLab) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and skill reviewers use this skill to run a first-pass static security scan on OpenClaw skill folders before installing, publishing, or granting sensitive access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Static pattern matching can miss sophisticated, runtime-generated, or context-dependent malicious behavior. <br>
Mitigation: Treat scan results as a first-pass signal and manually review important skills before granting sensitive access. <br>
Risk: Verbose or JSON scan output may expose private file paths or snippets from scanned skills. <br>
Mitigation: Run scans on specific skill folders and avoid sharing detailed output from private material. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/AdaInTheLab/skulk-skill-scanner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Console text, one-line summaries, or JSON, with markdown guidance for command usage.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The scanner may exit non-zero on failed scans, and verbose or JSON output can include matched file paths and line snippets.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
