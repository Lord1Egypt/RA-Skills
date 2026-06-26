## Description: <br>
Pre-install safety check for ClawHub skills that scans the three highest-risk signals before anything is written to disk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ordo-tech](https://clawhub.ai/user/ordo-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill before installing ClawHub community skills to fetch the target manifest, check publisher and content risk signals, and decide whether to proceed, warn, or block the install. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The free scanner covers only the highest-risk pre-install signals and is not a full audit. <br>
Mitigation: Use it as a lightweight pre-install gate, review the reported flags, and run a broader post-install audit when deeper assurance is needed. <br>
Risk: The skill relies on network lookups and publisher or manifest data that may be unavailable or incomplete. <br>
Mitigation: Treat unreachable or uncertain sources conservatively, surface the limitation to the user, and require explicit confirmation before continuing when risk is not low. <br>
Risk: The release advertises an external paid upgrade link. <br>
Mitigation: Review the external Gumroad link separately before purchasing or relying on the paid security pack. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ordo-tech/skill-pre-install-scanner) <br>
- [ClawHub Security Pack](https://theagentgordo.gumroad.com/l/clawhub-security-pack) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown risk report with a LOW, MEDIUM, or HIGH rating, flagged signals, summary, and install guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask for explicit confirmation on MEDIUM risk and block HIGH-risk installs unless a force override is acknowledged.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
