## Description: <br>
Use when users need to audit local OpenClaw skills, generate trust scores, and optionally publish those scores to SafeSpace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vpn2004](https://clawhub.ai/user/vpn2004) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and teams use this skill to audit local OpenClaw skills for security risk, produce trust scores and concise reports, and optionally submit reputation signals to SafeSpace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Normal use can automatically download, build, and run an unpinned external Go tool before auditing. <br>
Mitigation: Prefer a preinstalled, pinned, and reviewed safespace-rater binary via SAFESPACE_RATER_BIN instead of relying on auto-build or go install @latest. <br>
Risk: Publishing ratings or enabling LLM fallback can send audit-related data to external services. <br>
Mitigation: Use local-only dry-run mode for private skills, and enable publishing or LLM fallback only when the data is approved for external transmission. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vpn2004/safespace-rater) <br>
- [SafeSpace service endpoint](https://skillvet.cc.cd) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with bash command examples, audit summaries, and local report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local audit reports under ~/.safespace/audit-reports and pending upload state under ~/.safespace/pending-uploads.json.] <br>

## Skill Version(s): <br>
1.3.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
