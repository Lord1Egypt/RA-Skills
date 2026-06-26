## Description: <br>
Self Improving Local helps an agent retain user corrections, preferences, and self-reflection notes in local files so it can improve future work while keeping memory auditable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[reknottycat](https://clawhub.ai/user/reknottycat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent users use this skill to give an agent persistent local memory for explicit corrections, confirmed preferences, reusable work patterns, and post-task self-reflection. It is suited for agents that should improve across sessions while exposing stored memory for review, export, and deletion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persists user corrections, preferences, and self-reflection notes on local disk, which can retain sensitive or outdated information if used carelessly. <br>
Mitigation: Review ~/self-improving/ regularly, avoid storing secrets or sensitive personal data, and use stricter confirmation behavior when privacy matters. <br>
Risk: Optional setup can suggest installing a Proactivity companion skill, which may change agent behavior beyond this local-memory workflow. <br>
Mitigation: Decline the optional companion unless the user separately trusts and wants that skill. <br>


## Reference(s): <br>
- [ClawHub listing: Self Improving Local](https://clawhub.ai/reknottycat/self-improving-local) <br>
- [Publisher profile: reknottycat](https://clawhub.ai/user/reknottycat) <br>
- [Skill homepage](https://clawic.com/skills/self-improving) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create and update local markdown memory files under ~/self-improving/ when installed and used.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
