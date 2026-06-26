## Description: <br>
Analyzes fixed-camera video to identify hand rubbing, nail biting, and pacing, then returns behavior counts, durations, trend signals, and a non-diagnostic anxiety-behavior index. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, mental-health support teams, and developers can use this skill to send consented home, office, school, or counseling-room video to a remote analysis service for anxiety-related behavior statistics and self-awareness guidance. It is not a diagnostic or treatment tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive mental-health video, identity-linked metadata, and report history may be sent to remote services. <br>
Mitigation: Use only with explicit consent from every recorded person, avoid third-party or workplace footage unless consent and policy allow it, and minimize retained data. <br>
Risk: The authoritative scan verdict is suspicious because the skill uses remote services, accounts, token persistence, and mismatched health/pet-analysis components. <br>
Mitigation: Review endpoints, credentials, token storage, and dependencies before installation; pin dependencies and prefer a revised release that removes unrelated components. <br>
Risk: Behavior classification may produce false positives or be misread as a mental-health diagnosis. <br>
Mitigation: Present outputs as behavior statistics and self-awareness cues only, and require qualified clinical review for diagnosis or treatment decisions. <br>
Risk: Open-id values or API credentials may expose personal identifiers or reusable secrets. <br>
Mitigation: Use least-privilege credentials, avoid phone numbers or reusable identifiers when possible, and store secrets outside prompts and logs. <br>


## Reference(s): <br>
- [API interface document](references/api_doc.md) <br>
- [ClawHub skill release page](https://clawhub.ai/smyx-sunjinhui/smyx-anxiety-behavior-recognition-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON or Markdown report text with CLI commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include behavior counts, durations, an anxiety-behavior index, baseline comparison, alert level, self-care guidance, and report links.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
